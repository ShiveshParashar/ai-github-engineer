const $ = (id) => document.getElementById(id);
 
const dashboard = $("dashboard");
const loading = $("loading");
const errorBox = $("error");
const form = $("analyze-form");
const analyzeButton = $("analyze-btn");
 
console.log("dashboard.js v2 loaded");
 
/* ---------------------------------------------------------------
   Helpers
--------------------------------------------------------------- */
 
function asText(value) {
    if (value === undefined || value === null || value === "") return "—";
    return String(value);
}
 
function first(object, keys, fallback = undefined) {
    if (!object || typeof object !== "object") return fallback;
    for (const key of keys) {
        if (object[key] !== undefined && object[key] !== null && object[key] !== "") {
            return object[key];
        }
    }
    return fallback;
}
 
function formatLabel(key) {
    return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
 
function formatValue(value) {
    if (value === null || value === undefined) return "—";
    if (typeof value === "boolean") return value ? "Yes" : "No";
    if (typeof value === "object") return JSON.stringify(value, null, 2);
    return String(value);
}
 
function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
}
 
function emptyState(container, message = "No data available.") {
    container.innerHTML = `<div class="empty">${message}</div>`;
}
 
/* ---------------------------------------------------------------
   Render rows
--------------------------------------------------------------- */
 
function addRow(container, labelText, valueText) {
    const row = document.createElement("div");
    row.className = "row";
 
    const label = document.createElement("span");
    label.className = "label";
    label.textContent = labelText;
 
    const value = document.createElement("span");
    value.className = "value";
    value.textContent = valueText;
 
    row.appendChild(label);
    row.appendChild(value);
    container.appendChild(row);
}
 
function rows(container, data) {
    container.innerHTML = "";
 
    if (!data || typeof data !== "object") {
        emptyState(container);
        return;
    }
 
    if (Array.isArray(data)) {
        if (data.length === 0) {
            emptyState(container);
            return;
        }
        data.forEach((item, i) => addRow(container, `Item ${i + 1}`, formatValue(item)));
        return;
    }
 
    const entries = Object.entries(data);
    if (entries.length === 0) {
        emptyState(container);
        return;
    }
    entries.forEach(([key, value]) => addRow(container, formatLabel(key), formatValue(value)));
}
 
/* ---------------------------------------------------------------
   Badge
--------------------------------------------------------------- */
 
function setBadge(element, text, type = "neutral") {
    element.textContent = text;
    element.className = `badge ${type}`;
}
 
/* ---------------------------------------------------------------
   Project structure
--------------------------------------------------------------- */
 
function renderStructure(structure) {
    const container = $("structure-content");
    container.innerHTML = "";
 
    if (Array.isArray(structure)) {
        if (structure.length === 0) {
            emptyState(container, "No project structure data available.");
            return;
        }
        container.textContent = structure
            .slice(0, 300)
            .map((item) => (typeof item === "string" ? item : JSON.stringify(item)))
            .join("\n");
        return;
    }
 
    if (structure && typeof structure === "object" && Object.keys(structure).length > 0) {
        container.textContent = JSON.stringify(structure, null, 2);
        return;
    }
 
    emptyState(container, "No project structure data available.");
}
 
/* ---------------------------------------------------------------
   Main render
--------------------------------------------------------------- */
 
function render(data, url) {
    console.log("FULL API RESPONSE:", data);
 
    // Backend returns { repository_url, analysis: { ... } }
    const root = data.analysis || data;
    console.log("ANALYSIS:", root);
 
    const repo = root.repository || root.repository_analysis || {};
    const git = root.git_history || root.git || {};
    const lang = repo.languages || root.languages || {};
    const tests = root.tests || root.test_analysis || {};
    const ci = root.ci_cd || root.ci || {};
    const structure = repo.project_structure || root.project_structure || [];
 
    console.log("REPOSITORY:", repo);
    console.log("LANGUAGES:", lang);
    console.log("GIT:", git);
    console.log("TESTS:", tests);
    console.log("CI:", ci);
    console.log("STRUCTURE:", structure);
 
    // Make a wrong response shape visible instead of silently showing "—"
    if (Object.keys(repo).length === 0) {
        showError(
            "Unexpected API response shape. Top-level keys: " +
            Object.keys(root).join(", ")
        );
    }
 
    /* Repository name + URL */
    const urlName = url.split("/").filter(Boolean).pop()?.replace(".git", "") || "Repository";
    $("repo-name").textContent = first(repo, ["name", "repository_name", "repo_name"], urlName);
    $("repo-url-display").textContent = url;
    $("repo-url-display").href = url;
 
    /* Branch */
    const branch = first(
        repo,
        ["current_branch", "default_branch", "branch"],
        first(git, ["current_branch", "branch"])
    );
    $("stat-branch").textContent = asText(branch);
 
    /* Commits */
    const commitCount = first(
        repo,
        ["commit_count", "total_commits", "commits"],
        first(git, ["commit_count", "total_commits", "commits"])
    );
    $("stat-commits").textContent = asText(commitCount);
 
    /* Language count */
    let languageCount = 0;
    if (Array.isArray(lang)) languageCount = lang.length;
    else if (lang && typeof lang === "object") languageCount = Object.keys(lang).length;
    $("stat-languages").textContent = languageCount || "—";
 
    /* Test files */
    const testFileCount = first(tests, [
        "test_file_count",
        "test_files_count",
        "test_files",
        "count",
    ]);
 
    if (typeof testFileCount === "object" && testFileCount !== null) {
        $("stat-tests").textContent = Array.isArray(testFileCount)
            ? testFileCount.length
            : Object.keys(testFileCount).length;
    } else {
        $("stat-tests").textContent = asText(testFileCount);
    }
 
    /* Panels */
    rows($("languages-content"), lang);
 
    if (git && Object.keys(git).length > 0) {
        rows($("git-content"), git);
    } else {
        rows($("git-content"), {
            current_branch: repo.current_branch,
            commit_count: repo.commit_count,
            recent_commits: repo.recent_commits,
        });
    }
 
    rows($("tests-content"), tests);
    renderStructure(structure);
 
    /* CI/CD badges */
    if (ci.ci_found === false) {
        setBadge($("ci-badge"), "No CI/CD", "neutral");
        setBadge($("cicd-status"), "Not detected", "neutral");
    } else if (ci.ci_found === true) {
        setBadge($("ci-badge"), "CI/CD detected", "success");
        setBadge($("cicd-status"), `${ci.workflow_count || 0} workflow(s)`, "success");
    } else {
        setBadge($("ci-badge"), "No data", "neutral");
        setBadge($("cicd-status"), "No data", "neutral");
    }
 
    rows($("cicd-content"), ci);
 
    dashboard.classList.remove("hidden");
}
 
/* ---------------------------------------------------------------
   API request
--------------------------------------------------------------- */
 
form.addEventListener("submit", async (event) => {
    event.preventDefault();
 
    const url = $("repo-url").value.trim();
    if (!url) return;
 
    errorBox.classList.add("hidden");
    dashboard.classList.add("hidden");
    loading.classList.remove("hidden");
    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";
 
    try {
        const response = await fetch("/repositories/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url }),
        });
 
        const data = await response.json();
 
        if (!response.ok) {
            throw new Error(data.detail || "Repository analysis failed.");
        }
 
        render(data, url);
    } catch (error) {
        console.error("Repository analysis error:", error);
        showError(error.message || "Something went wrong.");
    } finally {
        loading.classList.add("hidden");
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze repository";
    }
});
 