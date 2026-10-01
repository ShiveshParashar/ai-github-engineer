const $ = (id) => document.getElementById(id);
const dashboard = $("dashboard"), loading = $("loading"), errorBox = $("error");
const form = $("analyze-form"), analyzeButton = $("analyze-btn");

/* ---------- helpers ---------- */
const asText = (v) => (v === undefined || v === null || v === "" ? "—" : String(v));
const label = (k) => k.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
function first(o, keys, fb) {
  if (!o || typeof o !== "object") return fb;
  for (const k of keys) if (o[k] !== undefined && o[k] !== null && o[k] !== "") return o[k];
  return fb;
}
function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
}
function empty(c, msg = "No data available.") { c.innerHTML = ""; c.appendChild(el("div", "empty", msg)); }
function toast(msg) {
  const t = $("toast"); t.textContent = msg; t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 1600);
}
function showError(m) { errorBox.textContent = m; errorBox.classList.remove("hidden"); }
function countUp(node, target) {
  const n = Number(target);
  if (!Number.isFinite(n)) { node.textContent = asText(target); return; }
  const start = performance.now(), dur = 700;
  (function tick(now) {
    const p = Math.min((now - start) / dur, 1);
    node.textContent = Math.round(n * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(tick);
  })(start);
}
const COLORS = { Python: "#3572A5", JavaScript: "#f1e05a", TypeScript: "#3178c6", HTML: "#e34c26", CSS: "#563d7c",
  Java: "#b07219", "C++": "#f34b7d", C: "#555555", Go: "#00ADD8", Rust: "#dea584", PHP: "#4F5D95", Ruby: "#701516",
  Kotlin: "#A97BFF", Swift: "#F05138", Dart: "#00B4AB", SQL: "#e38c00", SCSS: "#c6538c" };
function hue(s) { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 360; return `hsl(${h} 65% 50%)`; }

/* ---------- pretty value renderer (replaces raw JSON) ---------- */
function pretty(v) {
  if (v === null || v === undefined) return document.createTextNode("—");
  if (typeof v === "boolean") return el("span", "tag " + (v ? "yes" : "no"), v ? "Yes" : "No");
  if (Array.isArray(v)) {
    if (!v.length) return document.createTextNode("—");
    if (v.every((i) => typeof i !== "object")) {
      const w = el("span"); v.forEach((i) => w.appendChild(el("span", "tag", String(i)))); return w;
    }
  }
  if (typeof v === "object") return el("pre", "json", JSON.stringify(v, null, 2));
  return document.createTextNode(String(v));
}
function rows(container, data) {
  container.innerHTML = "";
  if (!data || typeof data !== "object" || !Object.keys(data).length) return empty(container);
  Object.entries(data).forEach(([k, v], i) => {
    const row = el("div", "row fade-in"); row.style.animationDelay = i * 40 + "ms";
    row.appendChild(el("span", "label", label(k)));
    const val = el("span", "value"); val.appendChild(pretty(v)); row.appendChild(val);
    container.appendChild(row);
  });
}
function setBadge(e, text, type = "neutral") { e.textContent = text; e.className = "badge " + type; }

/* ---------- languages ---------- */
function renderLanguages(lang) {
  const c = $("languages-content"); c.innerHTML = "";
  let entries = Array.isArray(lang) ? lang.map((l) => [String(l), 1]) : Object.entries(lang || {});
  entries = entries.filter(([, n]) => typeof n === "number").sort((a, b) => b[1] - a[1]);
  if (!entries.length) return empty(c);
  const total = entries.reduce((s, [, n]) => s + n, 0);
  const bar = el("div", "lang-bar");
  entries.forEach(([name, n]) => {
    const s = el("span"); s.style.width = (n / total) * 100 + "%"; s.style.background = COLORS[name] || hue(name);
    s.title = `${name}: ${n} files`; bar.appendChild(s);
  });
  c.appendChild(bar);
  entries.forEach(([name, n]) => {
    const r = el("div", "lang-row fade-in");
    const sw = el("span", "swatch"); sw.style.background = COLORS[name] || hue(name);
    r.append(sw, el("b", "", name), el("span", "pct", `${n} file${n > 1 ? "s" : ""} · ${((n / total) * 100).toFixed(1)}%`));
    c.appendChild(r);
  });
}

/* ---------- git ---------- */
let commitData = [];
function commitNode(cm) {
  const d = el("div", "commit fade-in");
  d.appendChild(el("div", "msg", asText(cm.message)));
  const meta = el("div", "meta");
  const h = el("button", "hash", String(cm.hash || "").slice(0, 7)); h.title = "Click to copy full hash";
  h.onclick = () => { navigator.clipboard?.writeText(cm.hash); toast("Hash copied"); };
  meta.append(h, el("span", "", cm.author || ""), el("span", "", cm.date ? new Date(cm.date).toLocaleString() : ""));
  d.appendChild(meta); return d;
}
function drawCommits(filter = "") {
  const box = $("commit-list"); if (!box) return; box.innerHTML = "";
  const q = filter.toLowerCase();
  const list = commitData.filter((c) => !q || `${c.message} ${c.author} ${c.hash}`.toLowerCase().includes(q));
  if (!list.length) return box.appendChild(el("div", "empty", "No matching commits."));
  list.forEach((c) => box.appendChild(commitNode(c)));
}
function renderGit(git, repo) {
  const c = $("git-content"); c.innerHTML = "";
  const g = git && Object.keys(git).length ? git : repo;
  if (!g || !Object.keys(g).length) return empty(c);
  const branches = g.branches || [], contribs = g.contributors || [];
  const ms = el("div", "mini-stats");
  [[first(g, ["total_commits", "commit_count"], "—"), "Commits"],
   [first(g, ["contributor_count"], contribs.length || "—"), "Contributors"],
   [branches.length || "—", "Branches"]].forEach(([n, t]) => {
    const d = el("div"); d.append(el("b", "", asText(n)), el("small", "", t)); ms.appendChild(d);
  });
  c.appendChild(ms);
  if (branches.length) { c.appendChild(el("div", "sub", "Branches")); const w = el("div"); branches.forEach((b) => w.appendChild(el("span", "tag", b))); c.appendChild(w); }
  if (contribs.length) {
    c.appendChild(el("div", "sub", "Contributors"));
    const max = Math.max(...contribs.map((x) => x.commits || 1));
    contribs.forEach((p) => {
      const r = el("div", "contrib"), a = el("div", "avatar", (p.author || "?").split(" ").map((w) => w[0]).join("").slice(0, 2).toUpperCase());
      a.style.background = hue(p.author || "?");
      const bar = el("div", "bar"), fill = el("i"); fill.style.width = ((p.commits || 0) / max) * 100 + "%"; bar.appendChild(fill);
      r.append(a, el("span", "", p.author || "Unknown"), bar, el("b", "", String(p.commits || 0))); c.appendChild(r);
    });
  }
  commitData = g.recent_commits || [];
  c.appendChild(el("div", "sub", "Recent commits"));
  const tl = el("div", "timeline"); tl.id = "commit-list"; c.appendChild(tl);
  drawCommits($("commit-filter").value);
}

/* ---------- project structure: collapsible tree ---------- */
function buildTree(lines) {
  const root = { children: [] }, stack = [{ depth: 0, node: root }];
  lines.forEach((raw) => {
    if (typeof raw !== "string") return;
    const depth = Math.floor((raw.length - raw.trimStart().length) / 4);
    const text = raw.trim(), isDir = text.endsWith("/");
    while (stack.length > 1 && stack[stack.length - 1].depth >= depth) stack.pop();
    const node = { name: text, dir: isDir, children: [] };
    stack[stack.length - 1].node.children.push(node);
    if (isDir) stack.push({ depth, node });
  });
  return root;
}
function drawNode(n) {
  if (!n.dir) return el("div", "file", "📄 " + n.name);
  const d = document.createElement("details"), s = el("summary", "", "📁 " + n.name);
  d.appendChild(s); n.children.forEach((ch) => d.appendChild(drawNode(ch))); return d;
}
function renderStructure(structure) {
  const c = $("structure-content"); c.innerHTML = "";
  if (!Array.isArray(structure) || !structure.length) return empty(c, "No project structure data available.");
  buildTree(structure).children.forEach((n) => c.appendChild(drawNode(n)));
  c.querySelectorAll(":scope > details").forEach((d) => (d.open = true));
}
function filterTree(q) {
  q = q.toLowerCase(); const c = $("structure-content");
  c.querySelectorAll(".file").forEach((f) => (f.style.display = !q || f.textContent.toLowerCase().includes(q) ? "" : "none"));
  c.querySelectorAll("details").forEach((d) => {
    const visible = [...d.querySelectorAll(".file")].some((f) => f.style.display !== "none");
    d.style.display = !q || visible ? "" : "none"; if (q && visible) d.open = true;
  });
}

/* ---------- main render ---------- */
function render(data, url) {
  const root = data.analysis || data;
  const repo = root.repository || root.repository_analysis || {};
  const git = root.git_history || root.git || {};
  const lang = repo.languages || root.languages || {};
  const tests = root.tests || root.test_analysis || {};
  const ci = root.ci_cd || root.ci || {};
  const structure = repo.project_structure || root.project_structure || [];

  if (!Object.keys(repo).length) showError("Unexpected API response. Top-level keys: " + Object.keys(root).join(", "));

  $("repo-name").textContent = first(repo, ["name", "repository_name"], url.split("/").filter(Boolean).pop()?.replace(".git", "") || "Repository");
  $("repo-url-display").textContent = url; $("repo-url-display").href = url;

  $("stat-branch").textContent = asText(first(repo, ["current_branch", "default_branch", "branch"], first(git, ["current_branch", "branch"])));
  countUp($("stat-commits"), first(repo, ["commit_count", "total_commits"], first(git, ["total_commits", "commit_count"])));
  countUp($("stat-languages"), Array.isArray(lang) ? lang.length : Object.keys(lang || {}).length || "—");
  let tf = first(tests, ["test_file_count", "test_files_count", "test_files", "count"]);
  if (tf && typeof tf === "object") tf = Array.isArray(tf) ? tf.length : Object.keys(tf).length;
  countUp($("stat-tests"), tf);

  renderLanguages(lang); renderGit(git, repo); renderStructure(structure);
  $("tree-filter").value = "";
  rows($("tests-content"), tests); rows($("cicd-content"), ci);

  if (ci.ci_found === true) { setBadge($("ci-badge"), "CI/CD detected", "success"); setBadge($("cicd-status"), `${ci.workflow_count || 0} workflow(s)`, "success"); }
  else if (ci.ci_found === false) { setBadge($("ci-badge"), "No CI/CD"); setBadge($("cicd-status"), "Not detected"); }
  else { setBadge($("ci-badge"), "No data"); setBadge($("cicd-status"), "No data"); }

  dashboard.classList.remove("hidden");
  dashboard.querySelectorAll(".stat-card,.panel").forEach((n, i) => { n.classList.add("fade-in"); n.style.animationDelay = i * 70 + "ms"; });
  dashboard.scrollIntoView({ behavior: "smooth" });
}

/* ---------- history chips ---------- */
function history() { try { return JSON.parse(localStorage.getItem("repoHistory") || "[]"); } catch { return []; } }
function saveHistory(u) { try { localStorage.setItem("repoHistory", JSON.stringify([u, ...history().filter((x) => x !== u)].slice(0, 5))); } catch {} drawHistory(); }
function drawHistory() {
  const box = $("history"); box.innerHTML = "";
  history().forEach((u) => { const b = el("button", "chip", u.replace("https://github.com/", "")); b.type = "button"; b.onclick = () => { $("repo-url").value = u; form.requestSubmit(); }; box.appendChild(b); });
}

/* ---------- API ---------- */
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const url = $("repo-url").value.trim(); if (!url) return;
  errorBox.classList.add("hidden"); dashboard.classList.add("hidden"); loading.classList.remove("hidden");
  analyzeButton.disabled = true; analyzeButton.textContent = "Analyzing...";
  try {
    const res = await fetch("/repositories/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ url }) });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Repository analysis failed.");
    render(data, url); saveHistory(url);
  } catch (err) { console.error(err); showError(err.message || "Something went wrong."); }
  finally { loading.classList.add("hidden"); analyzeButton.disabled = false; analyzeButton.textContent = "Analyze repository"; }
});

/* ---------- interactions ---------- */
$("commit-filter").addEventListener("input", (e) => drawCommits(e.target.value));
$("tree-filter").addEventListener("input", (e) => filterTree(e.target.value));
$("expand-all").onclick = () => $("structure-content").querySelectorAll("details").forEach((d) => (d.open = true));
$("collapse-all").onclick = () => $("structure-content").querySelectorAll("details").forEach((d) => (d.open = false));

const root = document.documentElement;
try { root.dataset.theme = localStorage.getItem("theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"); } catch {}
$("theme-toggle").onclick = () => {
  root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
  try { localStorage.setItem("theme", root.dataset.theme); } catch {}
};

/* sidebar scroll-spy */
const links = [...document.querySelectorAll(".nav-item")];
const spy = new IntersectionObserver((entries) => {
  entries.forEach((en) => { if (en.isIntersecting) links.forEach((l) => l.classList.toggle("active", l.getAttribute("href") === "#" + en.target.id)); });
}, { rootMargin: "-30% 0px -60% 0px" });
links.forEach((l) => { const t = document.querySelector(l.getAttribute("href")); if (t) spy.observe(t); });

drawHistory();
