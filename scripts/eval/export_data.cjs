/* Export the public synthetic fixtures of prototype/data.js for the Python server.
   Usage: node scripts/eval/export_data.cjs [--check]  (--check fails if the JSON is stale) */
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..", "..");
require(path.join(root, "prototype/data.js"));
const target = path.join(root, "flowassist/fixtures.json");
const json = JSON.stringify(globalThis.FlowData, null, 2) + "\n";
if (process.argv.includes("--check")) {
  const current = fs.existsSync(target) ? fs.readFileSync(target, "utf8") : "";
  if (current !== json) {
    console.error("flowassist/fixtures.json is stale: run `make export-data`.");
    process.exit(1);
  }
  console.log("flowassist/fixtures.json matches prototype/data.js");
} else {
  fs.writeFileSync(target, json);
  console.log(`Wrote ${path.relative(root, target)}`);
}
