const byId = (id) => document.getElementById(id);

function parseAllocation(value) {
  const counts = value
    .split(/[^0-9]+/)
    .map((item) => Number(item))
    .filter((item) => Number.isInteger(item) && item >= 0);
  return counts.length ? counts : [2];
}

function totalInputs(counts) {
  return counts.reduce((total, count) => total + count, 0);
}

function renderMpptSummary(counts) {
  const list = byId("mpptSummary");
  list.replaceChildren();
  counts.forEach((count, index) => {
    const item = document.createElement("li");
    item.textContent = `MPPT ${index + 1}: ${count} input${count === 1 ? "" : "s"}`;
    list.appendChild(item);
  });
  byId("mpptCount").textContent = String(counts.length);
  byId("derivedStringCount").textContent = String(totalInputs(counts));
}

function syncStringsFromMppts() {
  const counts = parseAllocation(byId("mpptInputs").value);
  const total = Math.max(1, totalInputs(counts));
  byId("stringCount").value = String(total);
  renderMpptSummary(counts);
  byId("stringCount").dispatchEvent(new Event("input", { bubbles: true }));
}

function relabelInverter() {
  const stage = byId("stage");
  if (!stage) {
    return;
  }
  stage.querySelectorAll("text").forEach((label) => {
    if (label.textContent === "INVERTER" || label.textContent === "INV") {
      label.textContent = "MPPT 1";
    }
  });
}

function observeRenderer() {
  const stage = byId("stage");
  const observer = new MutationObserver(relabelInverter);
  observer.observe(stage, { childList: true, subtree: true, characterData: true });
  relabelInverter();
}

byId("mpptInputs").addEventListener("input", syncStringsFromMppts);
byId("mpptInputs").addEventListener("change", syncStringsFromMppts);

await import("../b9-sandbox/app.js");
syncStringsFromMppts();
observeRenderer();
