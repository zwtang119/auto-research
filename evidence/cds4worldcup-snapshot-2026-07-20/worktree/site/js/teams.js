const state = {
  teams: [],
  filters: {
    query: "",
    confederation: "all",
    depth: "all",
  },
};

const els = {
  grid: document.querySelector("[data-team-grid]"),
  count: document.querySelector("[data-count-line]"),
  query: document.querySelector("[data-filter-query]"),
  confederation: document.querySelector("[data-filter-confederation]"),
  depth: document.querySelector("[data-filter-depth]"),
};

async function initTeamsPage() {
  if (!els.grid) return;

  const data = await loadTeamsData();
  state.teams = Object.values(data).sort(compareTeams);

  bindControls();
  render();
}

function bindControls() {
  els.query.addEventListener("input", (event) => {
    state.filters.query = event.target.value.trim().toLowerCase();
    render();
  });

  els.confederation.addEventListener("change", (event) => {
    state.filters.confederation = event.target.value;
    render();
  });

  els.depth.addEventListener("change", (event) => {
    state.filters.depth = event.target.value;
    render();
  });

}

async function loadTeamsData() {
  if (window.CDS4WORLDCUP_TEAMS) {
    return window.CDS4WORLDCUP_TEAMS;
  }

  const response = await fetch("data/teams.json");
  if (!response.ok) throw new Error(`球队数据加载失败 (${response.status})`);
  return response.json();
}

function render() {
  const teams = state.teams.filter(matchesFilters);
  els.count.textContent = `当前显示 ${teams.length} / ${state.teams.length} 支球队`;
  els.grid.innerHTML = teams.length
    ? teams.map(renderTeamCard).join("")
    : `<div class="empty-state">没有符合筛选条件的球队。</div>`;
}

function matchesFilters(team) {
  const query = state.filters.query;
  const haystack = `${team.zh_name} ${team.en_name} ${team.canonical_name} ${team.slug}`.toLowerCase();
  if (query && !haystack.includes(query)) return false;
  if (state.filters.confederation !== "all" && team.confederation !== state.filters.confederation) return false;
  if (state.filters.depth === "deep" && !team.is_deep) return false;
  if (state.filters.depth === "thin" && team.is_deep) return false;
  return true;
}

function renderTeamCard(team) {
  const statusLabel = team.is_deep ? "深度版" : "简版";
  const statusClass = team.is_deep ? "deep" : "thin";
  const group = team.group ? team.group : "?";

  // Get championship probability from baselines (Elo data)
  const baselines = window.CDS4WORLDCUP_BASELINES || {};
  const eloTeams = (baselines.baselines && baselines.baselines.elo && baselines.baselines.elo.teams) || {};
  const eloVal = eloTeams[team.slug];
  // Elo values are ratings (~1.8-2.5), convert to rough probability percentage
  const probPct = eloVal ? Math.max(0.1, Math.min(99, (eloVal / 3.0) * 100)).toFixed(1) : null;

  const probBar = probPct
    ? `<div class="tsc-prob-bar"><div class="tsc-prob-fill" style="width:${Math.min(100, probPct)}%"></div></div>
       <span class="tsc-prob-label" style="color:${probPct > 20 ? 'var(--grass-green)' : (probPct > 5 ? 'var(--energy-blue)' : 'var(--alert-gold)')}">${probPct}%</span>`
    : `<div class="tsc-prob-bar"><div class="tsc-prob-fill" style="width:2%"></div></div>
       <span class="tsc-prob-label" style="color:var(--neutral-gray)">—</span>`;

  return `
    <article class="team-star-card" id="${escapeAttr(team.slug)}" data-detail-href="team.html?team=${escapeAttr(team.slug)}">
      <div class="tsc-top">
        <span class="tsc-flag">${escapeHtml(team.flag)}</span>
        <span class="tsc-depth ${statusClass}">${statusLabel}</span>
      </div>
      <h3 class="tsc-name">${escapeHtml(team.zh_name)}</h3>
      <p class="tsc-group">${escapeHtml(group)}组 · ${escapeHtml(team.confederation_label || team.confederation)}</p>
      ${probBar}
      <a class="tsc-link" href="team.html?team=${escapeAttr(team.slug)}">查看夺冠路 →</a>
    </article>
  `;
}

function compareTeams(a, b) {
  if (a.is_deep !== b.is_deep) return a.is_deep ? -1 : 1;
  return a.en_name.localeCompare(b.en_name);
}

els.grid.addEventListener("click", (event) => {
  if (event.target.closest("a")) return;
  const card = event.target.closest("[data-detail-href]");
  if (card) window.location.href = card.dataset.detailHref;
});

function stripMarkdown(value) {
  return String(value || "")
    .replace(/`/g, "")
    .replace(/\*\*/g, "")
    .replace(/\s+/g, " ")
    .trim();
}



initTeamsPage().catch((error) => {
  const detail = window.location.protocol === "file:"
    ? "本地直接打开 HTML 时，部分浏览器会拦截数据读取。当前版本已内置兜底数据；如果仍看不到球队，请刷新页面，或在仓库里运行 python3 -m http.server 8000 --directory site 后访问 http://localhost:8000/。"
    : `球队数据加载失败：${error.message}`;
  els.grid.innerHTML = `<div class="empty-state">${escapeHtml(detail)}</div>`;
});
