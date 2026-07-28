import { runDebugTests } from "./tests.js";

const report = runDebugTests();
console.log(JSON.stringify(report, null, 2));

if (report.failed > 0) {
  process.exitCode = 1;
}
