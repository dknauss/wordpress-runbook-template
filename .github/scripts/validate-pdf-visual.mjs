import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { createReadStream, existsSync } from "node:fs";
import http from "node:http";
import path from "node:path";

import pixelmatch from "pixelmatch";
import { chromium } from "playwright";
import { PNG } from "pngjs";

const CASES = [
  {
    name: "page-5-running-header-and-conventions-table",
    page: 5,
    clip: { x: 350, y: 56, width: 800, height: 690 },
  },
  {
    name: "page-10-running-header-and-cache-table",
    page: 10,
    clip: { x: 350, y: 56, width: 800, height: 690 },
  },
];

const PDF_FILE = "WP-Operations-Runbook.pdf";
const BASELINE_DIR = path.join(".github", "test-artifacts", "pdf-baselines");
const OUTPUT_DIR = path.join("output", "playwright", "pdf-visual");
const VIEWPORT = { width: 1200, height: 760 };
const PIXELMATCH_THRESHOLD = 0.1;
const DHASH_WIDTH = 17;
const DHASH_HEIGHT = 16;
const MAX_DHASH_DISTANCE = 20;

function parseArgs(argv) {
  return {
    headed: argv.includes("--headed"),
    updateBaselines: argv.includes("--update-baselines"),
  };
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function pngPaths(name) {
  return {
    baseline: path.join(BASELINE_DIR, `${name}.png`),
    actual: path.join(OUTPUT_DIR, "actual", `${name}.png`),
    diff: path.join(OUTPUT_DIR, "diff", `${name}.png`),
  };
}

function grayscaleAt(image, x, y) {
  const index = (y * image.width + x) * 4;
  const r = image.data[index];
  const g = image.data[index + 1];
  const b = image.data[index + 2];
  return 0.299 * r + 0.587 * g + 0.114 * b;
}

function differenceHash(image, width = DHASH_WIDTH, height = DHASH_HEIGHT) {
  const bits = [];
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width - 1; x += 1) {
      const leftX = Math.floor(((x + 0.5) * image.width) / width);
      const rightX = Math.floor(((x + 1.5) * image.width) / width);
      const sampleY = Math.floor(((y + 0.5) * image.height) / height);
      bits.push(grayscaleAt(image, leftX, sampleY) > grayscaleAt(image, rightX, sampleY) ? 1 : 0);
    }
  }
  return bits;
}

function hammingDistance(left, right) {
  assert(left.length === right.length, "Cannot compare hashes of different lengths");
  let distance = 0;
  for (let index = 0; index < left.length; index += 1) {
    if (left[index] !== right[index]) {
      distance += 1;
    }
  }
  return distance;
}

function contentTypeFor(filePath) {
  if (filePath.endsWith(".pdf")) {
    return "application/pdf";
  }
  if (filePath.endsWith(".png")) {
    return "image/png";
  }
  if (filePath.endsWith(".html")) {
    return "text/html; charset=utf-8";
  }
  return "application/octet-stream";
}

async function startStaticServer(rootDir) {
  const server = http.createServer(async (req, res) => {
    const urlPath = decodeURIComponent((req.url || "/").split("?")[0]);
    const relativePath = urlPath === "/" ? PDF_FILE : urlPath.replace(/^\/+/, "");
    const filePath = path.resolve(rootDir, relativePath);
    if (!filePath.startsWith(rootDir)) {
      res.writeHead(403).end("Forbidden");
      return;
    }
    if (!existsSync(filePath)) {
      res.writeHead(404).end("Not found");
      return;
    }

    res.writeHead(200, { "Content-Type": contentTypeFor(filePath) });
    createReadStream(filePath).pipe(res);
  });

  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });

  const address = server.address();
  assert(address && typeof address === "object", "Could not determine static server address");
  return { server, baseUrl: `http://127.0.0.1:${address.port}` };
}

async function captureCase(browser, baseUrl, caseSpec) {
  const page = await browser.newPage({ viewport: VIEWPORT });
  const url = `${baseUrl}/${PDF_FILE}#page=${caseSpec.page}`;

  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);

  const screenshot = await page.screenshot({
    clip: caseSpec.clip,
    scale: "css",
    type: "png",
  });
  await page.close();
  return screenshot;
}

async function updateBaselines(browser, baseUrl) {
  await mkdir(BASELINE_DIR, { recursive: true });
  for (const caseSpec of CASES) {
    const screenshot = await captureCase(browser, baseUrl, caseSpec);
    const { baseline } = pngPaths(caseSpec.name);
    await writeFile(baseline, screenshot);
    console.log(`Updated baseline: ${baseline}`);
  }
}

async function compareCase(browser, baseUrl, caseSpec) {
  const screenshot = await captureCase(browser, baseUrl, caseSpec);
  const paths = pngPaths(caseSpec.name);

  assert(existsSync(paths.baseline), `Missing baseline image: ${paths.baseline}`);
  await mkdir(path.dirname(paths.actual), { recursive: true });
  await mkdir(path.dirname(paths.diff), { recursive: true });
  await writeFile(paths.actual, screenshot);

  const baseline = PNG.sync.read(await readFile(paths.baseline));
  const actual = PNG.sync.read(screenshot);
  assert(
    baseline.width === actual.width && baseline.height === actual.height,
    `Screenshot size mismatch for ${caseSpec.name}: baseline ${baseline.width}x${baseline.height}, actual ${actual.width}x${actual.height}`
  );

  const diff = new PNG({ width: actual.width, height: actual.height });
  const diffPixels = pixelmatch(
    baseline.data,
    actual.data,
    diff.data,
    actual.width,
    actual.height,
    { threshold: PIXELMATCH_THRESHOLD }
  );
  await writeFile(paths.diff, PNG.sync.write(diff));
  const dHashDistance = hammingDistance(differenceHash(baseline), differenceHash(actual));

  if (dHashDistance > MAX_DHASH_DISTANCE) {
    throw new Error(
      `${caseSpec.name} perceptual diff too large: dHash distance ${dHashDistance}, raw diff ${diffPixels} pixels`
    );
  }

  console.log(`OK   [${caseSpec.name}] dHash distance ${dHashDistance}, raw diff ${diffPixels} pixels`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const rootDir = process.cwd();

  assert(existsSync(path.join(rootDir, PDF_FILE)), `Missing PDF artifact: ${PDF_FILE}`);

  await rm(OUTPUT_DIR, { recursive: true, force: true });
  const { server, baseUrl } = await startStaticServer(rootDir);
  const browser = await chromium.launch({ headless: !args.headed });

  try {
    if (args.updateBaselines) {
      await updateBaselines(browser, baseUrl);
      return;
    }

    for (const caseSpec of CASES) {
      await compareCase(browser, baseUrl, caseSpec);
    }
    console.log(`All PDF visual smoke checks passed (${CASES.length} cases).`);
  } finally {
    await browser.close();
    await new Promise((resolve, reject) => server.close((error) => (error ? reject(error) : resolve())));
  }
}

main().catch((error) => {
  console.error(`FAIL ${error.message}`);
  process.exitCode = 1;
});
