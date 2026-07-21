// ═══════════════════════════════════════════════════════
// homepage.js — Fan-centric conversation flow
// Hero → Heatmap → Focus Matches → Choose Team → AI → Footer
// ═══════════════════════════════════════════════════════

var homeEls = {
  headline: document.querySelector("[data-home-hero-headline]"),
  lede: document.querySelector("[data-home-hero-lede]"),
  hook: document.querySelector("[data-home-hero-hook]"),
  boundary: document.querySelector("[data-home-hero-boundary]"),
  summary: document.querySelector("[data-home-signals-hero]"),
  teamTeasers: document.querySelector("[data-home-team-teasers]"),
  aiPerspectives: document.querySelector("[data-ai-perspectives]"),
  heatmap: document.querySelector("[data-home-heatmap]"),
  focusMatches: document.querySelector("[data-home-focus-matches]"),
};

async function initHomepage() {
  if (!homeEls.summary) return;

  var data = await loadHomepageData();

  renderHero(data);
  renderSummary(data);
  renderHeatmap();
  renderFocusMatches();
  renderTeamTeasers(data.team_teasers || []);
  renderAiPerspectives(data.ai_perspectives);
}

/* ── Data loading ─────────────────────────────── */

async function loadHomepageData() {
  if (window.CDS4WORLDCUP_HOMEPAGE) {
    return window.CDS4WORLDCUP_HOMEPAGE;
  }

  var response = await fetch("data/homepage.json");
  if (!response.ok) throw new Error("首页数据加载失败 (" + response.status + ")");
  return response.json();
}

/* ── Hero (copy is static in HTML, only update hook from data) ── */

function renderHero(data) {
  var hero = data.hero || {};
  var hooks = Array.isArray(hero.hooks) ? hero.hooks.filter(Boolean) : [];
  if (hooks.length && homeEls.hook) {
    homeEls.hook.textContent = hooks[0];
  }
}

/* ── Summary: top 5 team probability cards ─────── */

function renderSummary(data) {
  var el = homeEls.summary;
  if (!el) return;

  // Get top 5 teams by probability from public model data
  var publicModel = data.public_signal_snapshots?.public_model_crowd?.top_teams || [];
  var market = data.public_signal_snapshots?.market_public_baseline?.teams || {};

  // Build team probability list from public_model_crowd (has flag+name)
  var teamProbs = publicModel.map(function(t) {
    return {
      slug: t.team_slug,
      name: t.team_name,
      flag: t.flag || "",
      prob: Number(t.probability) || 0,
      href: t.href || "team.html?team=" + t.team_slug
    };
  }).sort(function(a, b) { return b.prob - a.prob; }).slice(0, 5);

  // Fallback: if no public model data, use market data
  if (!teamProbs.length) {
    for (var slug in market) {
      teamProbs.push({
        slug: slug,
        name: slug,
        flag: "",
        prob: Number(market[slug].probability) || 0,
        href: "team.html?team=" + slug
      });
    }
    teamProbs.sort(function(a, b) { return b.prob - a.prob; }).slice(0, 5);
  }

  if (!teamProbs.length) {
    el.innerHTML = '<div class="empty-state">概率数据待更新</div>';
    return;
  }

  var maxProb = teamProbs[0].prob || 1;
  el.innerHTML = '<p class="hero-signals-label">热门球队夺冠信号</p>' +
    teamProbs.map(function(t) {
      var pct = t.prob < 1 ? (t.prob * 100).toFixed(1) : t.prob.toFixed(1);
      var cls = t.prob / maxProb > 0.6 ? "" : (t.prob / maxProb > 0.2 ? " mid" : " low");
      return '<a class="signal-card-mini" href="' + escapeAttr(t.href) + '">' +
        '<span class="signal-flag">' + t.flag + '</span>' +
        '<div class="signal-info">' +
          '<p class="signal-team-name">' + escapeHtml(t.name) + '</p>' +
          '<span class="signal-meta">来源信号</span>' +
        '</div>' +
        '<span class="signal-pct' + cls + '">' + pct + '%</span>' +
      '</a>';
    }).join("");
}

/* ── Heatmap: Top 12 × 6 stages ──────────────── */

function renderHeatmap() {
  var el = homeEls.heatmap;
  if (!el) return;

  var cdsData = window.CDS4WORLDCUP_CDS_PATHS;
  if (!cdsData || !cdsData.teams) {
    el.innerHTML = '<div class="empty-state">路径数据待加载</div>';
    return;
  }

  // Build team lookup from teams-data.js (canonical_name → {flag, zh_name, slug})
  var teamsLookup = window.CDS4WORLDCUP_TEAMS || {};
  var nameToInfo = {};
  for (var slug in teamsLookup) {
    var t = teamsLookup[slug];
    if (t.canonical_name) nameToInfo[t.canonical_name] = t;
  }

  var stages = ["组出线", "R32", "R16", "四强", "决赛", "冠军"];
  var entries = [];
  for (var teamName in cdsData.teams) {
    var team = cdsData.teams[teamName];
    if (!team.championship || !team.qualification) continue;
    var champProb = team.championship.championship_prob || 0;
    var qualProb = team.qualification.qual_prob || 0;
    var nodes = team.championship.path_nodes || [];

    var cells = [
      qualProb * 100,
      nodes.length > 0 ? (nodes[0].cumulative_prob || 0) * 100 : 0,
      nodes.length > 1 ? (nodes[1].cumulative_prob || 0) * 100 : 0,
      nodes.length > 2 ? (nodes[2].cumulative_prob || 0) * 100 : 0,
      nodes.length > 3 ? (nodes[3].cumulative_prob || 0) * 100 : 0,
      champProb * 100
    ];
    entries.push({ name: teamName, info: nameToInfo[teamName] || {}, cells: cells, champProb: champProb });
  }

  // Sort by championship probability, take top 12
  entries.sort(function(a, b) { return b.champProb - a.champProb; });
  var top12 = entries.slice(0, 12);

  if (!top12.length) {
    el.innerHTML = '<div class="empty-state">暂无路径概率数据</div>';
    return;
  }

  // Render header
  var html = '<div class="heatmap-head tl">球队</div>';
  for (var s = 0; s < stages.length; s++) {
    html += '<div class="heatmap-head">' + stages[s] + '</div>';
  }

  // Render rows
  for (var i = 0; i < top12.length; i++) {
    var entry = top12[i];
    var flag = entry.info.flag || '';
    var zhName = entry.info.zh_name || entry.name;
    var href = entry.info.slug ? 'team.html?team=' + escapeAttr(entry.info.slug) : '#';
    html += '<div class="heatmap-team"><span class="team-flag-sm">' + flag + '</span>' + escapeHtml(zhName) + '</div>';

    for (var c = 0; c < entry.cells.length; c++) {
      var v = entry.cells[c];
      var alpha = Math.max(0.06, v / 100);
      var bg = 'rgba(15, 140, 72, ' + alpha.toFixed(2) + ')';
      var dim = v < 5 ? ' dim' : '';
      var display = v >= 10 ? v.toFixed(0) : (v >= 1 ? v.toFixed(1) : v.toFixed(2));
      html += '<a class="heatmap-cell' + dim + '" style="background:' + bg + '" href="' + escapeAttr(href) + '"><span class="pct">' + display + '</span></a>';
    }
  }

  el.innerHTML = html;
}

/* ── Team Teasers ─────────────────────────────── */

function renderTeamTeasers(teasers) {
  if (!homeEls.teamTeasers) return;
  if (!teasers.length) {
    homeEls.teamTeasers.innerHTML = '<div class="empty-state">暂时没有球队入口。</div>';
    return;
  }

  homeEls.teamTeasers.innerHTML = teasers.slice(0, 8).map(function(team) {
    return '<a class="team-teaser-card" href="' + escapeAttr(team.href || "teams.html") + '">' +
      '<div class="team-teaser-top">' +
        '<span class="flag" aria-hidden="true">' + escapeHtml(team.flag || "🏳️") + '</span>' +
        '<span class="tag ' + (team.source_completeness === "deep" ? "deep" : "thin") + '">' + escapeHtml(team.display_status_label) + '</span>' +
      '</div>' +
      '<h3>' + escapeHtml(team.team_name) + '</h3>' +
      '<p>' + escapeHtml(team.path_thesis) + '</p>' +
      '<div class="inline-list">' +
        (team.top_obstacle_types || []).map(function(item) {
          return '<span class="pill">' + escapeHtml(item) + '</span>';
        }).join("") +
      '</div>' +
      '<span class="team-link-text">看它的夺冠路</span>' +
    '</a>';
  }).join("");
}

/* ═══ Focus Matches: Top 6 by model disagreement ═══ */

function renderFocusMatches() {
  var el = homeEls.focusMatches;
  if (!el) return;

  var odds = window.CDS4WORLDCUP_ODDS;
  var coach = window.CDS4WORLDCUP_COACH_SIM;
  var schedule = window.CDS4WORLDCUP_SCHEDULE;

  if (!odds || !coach || !odds.predictions || !coach.predictions) {
    el.innerHTML = '<div class="empty-state">焦点比赛数据待加载</div>';
    return;
  }

  // Build coach lookup by match_id
  var coachMap = {};
  for (var i = 0; i < coach.predictions.length; i++) {
    coachMap[coach.predictions[i].match_id] = coach.predictions[i];
  }

  // Build schedule lookup by match_id
  var schedMap = {};
  if (schedule && schedule.groups) {
    for (var g in schedule.groups) {
      var matches = schedule.groups[g].matches || [];
      for (var m = 0; m < matches.length; m++) {
        schedMap[matches[m].match_id] = matches[m];
      }
    }
  }

  // Calculate disagreement for each match
  var items = [];
  for (var j = 0; j < odds.predictions.length; j++) {
    var o = odds.predictions[j];
    var c = coachMap[o.match_id];
    if (!c) continue;

    var gapHome = Math.abs(o.home_win - c.home_win);
    var gapDraw = Math.abs(o.draw - c.draw);
    var gapAway = Math.abs(o.away_win - c.away_win);
    var gap = Math.max(gapHome, gapDraw, gapAway);
    items.push({ odds: o, coach: c, gap: gap, sched: schedMap[o.match_id] || {} });
  }

  // Sort by gap descending, take top 6
  items.sort(function(a, b) { return b.gap - a.gap; });
  var top6 = items.slice(0, 6);

  if (!top6.length) {
    el.innerHTML = '<div class="empty-state">暂无焦点比赛数据</div>';
    return;
  }

  // Team flag lookup
  var teamsData = window.CDS4WORLDCUP_TEAMS || {};

  el.innerHTML = top6.map(function(item) {
    var o = item.odds;
    var c = item.coach;
    var s = item.sched;
    var gapPct = (item.gap * 100).toFixed(0);
    var round = s.round ? '第' + s.round + '轮' : '';
    var date = s.date || '';

    // Find flags from schedule codes first, fallback to team name lookup
    var homeFlag = '', awayFlag = '';
    if (s.home_code) homeFlag = cdsCodeFlag(s.home_code);
    if (s.away_code) awayFlag = cdsCodeFlag(s.away_code);

    // Fallback: search teams by name if no schedule code
    if (!homeFlag || !awayFlag) {
      for (var slug in teamsData) {
        var t = teamsData[slug];
        if (t.canonical_name === o.home_team || t.zh_name === o.home_team) homeFlag = homeFlag || t.flag || '';
        if (t.canonical_name === o.away_team || t.zh_name === o.away_team) awayFlag = awayFlag || t.flag || '';
      }
    }

    return '<div class="focus-match-card">' +
      '<div class="fmc-header">' +
        '<span class="fmc-teams">' + homeFlag + ' ' + escapeHtml(o.home_team) + ' vs ' + awayFlag + ' ' + escapeHtml(o.away_team) + '</span>' +
        '<span class="fmc-meta">' + escapeHtml(round) + (date ? ' · ' + escapeHtml(date) : '') + '</span>' +
      '</div>' +
      renderModelBar('Elo+泊松', o.home_win, o.draw, o.away_win) +
      renderModelBar('教练对位', c.home_win, c.draw, c.away_win) +
      '<div class="fmc-gap">分歧 ' + gapPct + '%</div>' +
    '</div>';
  }).join("");
}

function renderModelBar(label, hw, d, aw) {
  var hp = (hw * 100).toFixed(0);
  var dp = (d * 100).toFixed(0);
  var ap = (aw * 100).toFixed(0);
  return '<div class="fmc-model">' +
    '<span class="fmc-model-label">' + escapeHtml(label) + '</span>' +
    '<div class="fmc-bar-track">' +
      '<div class="fmc-bar-fill fmc-bar-home" style="width:' + hp + '%"></div>' +
      '<div class="fmc-bar-fill fmc-bar-draw" style="width:' + dp + '%"></div>' +
      '<div class="fmc-bar-fill fmc-bar-away" style="width:' + ap + '%"></div>' +
    '</div>' +
    '<div class="fmc-bar-labels">' +
      '<span style="width:' + hp + '%">' + hp + '%</span>' +
      '<span style="width:' + dp + '%">' + dp + '%</span>' +
      '<span style="width:' + ap + '%">' + ap + '%</span>' +
    '</div>' +
  '</div>';
}

/* ═══ AI Perspectives: quote wall ═══ */

function renderAiPerspectives(ai) {
  if (!homeEls.aiPerspectives) return;
  var factions = Array.isArray(ai && ai.factions) ? ai.factions : [];
  if (!factions.length) {
    homeEls.aiPerspectives.innerHTML = '<div class="empty-state">AI 多视角数据还在整理。</div>';
    return;
  }

  // Show top 4 representative quotes as opinion wall
  var topFactions = factions
    .filter(function(f) { return f.representative && f.representative.reason; })
    .sort(function(a, b) { return (Number(b.count) || 0) - (Number(a.count) || 0); })
    .slice(0, 4);

  homeEls.aiPerspectives.innerHTML =
    '<div class="ai-summary-row">' +
      '<strong>' + escapeHtml(ai.perspective_count) + ' 个独立视角</strong>' +
      '<span>' + escapeHtml(ai.faction_count) + ' 个派别</span>' +
      '<span>' + escapeHtml(ai.covered_team_count) + ' 支球队有参考</span>' +
    '</div>' +
    '<div class="quote-wall">' +
      topFactions.map(function(f) {
        var rep = f.representative || {};
        return '<div class="quote-card">' +
          '<span class="quote-mark">“</span>' +
          '<p class="quote-text">' + escapeHtml(rep.reason || "暂无代表理由。") + '</p>' +
          '<span class="quote-source">' + escapeHtml(f.name) + ' · ' + escapeHtml(f.count) + ' 个同类观点</span>' +
        '</div>';
      }).join("") +
    '</div>';
}

/* ── Bootstrap ────────────────────────────────── */

initHomepage().catch(function(error) {
  var detail = window.location.protocol === "file:"
    ? "本地直接打开 HTML 时，部分浏览器会拦截数据读取。当前版本已内置兜底数据；如果仍看不到内容，请刷新页面，或在仓库里运行 python3 -m http.server 8000 --directory site 后访问 http://localhost:8000/。"
    : "首页数据加载失败：" + error.message;
  var message = '<div class="empty-state">' + escapeHtml(detail) + '</div>';
  [homeEls.summary, homeEls.heatmap, homeEls.focusMatches, homeEls.teamTeasers, homeEls.aiPerspectives]
    .filter(Boolean)
    .forEach(function(element) {
      element.innerHTML = message;
    });
});
