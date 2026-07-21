/**
 * match.js — CDS4WorldCup 比赛详情页
 *
 * 从 URL 参数读取 match_id，加载 schedule.json + odds.json + teams.json，
 * 渲染单场比赛的深度分析。
 * 纯 HTML/CSS/JS，零外部依赖。
 */

/* ── Country code helpers (from common.js) ─────── */

// Short aliases — delegate to common.js shared functions
function codeFlag(code) {
  return cdsCodeFlag(code);
}

function codeName(code) {
  return cdsCodeName(code);
}

function codeSlug(code) {
  return cdsCodeSlug(code);
}

/* ── State ───────────────────────────────────────── */

var scheduleData = null;
var oddsData = null;
var teamsData = null;
var oddsMap = {};

/* ── Init ────────────────────────────────────────── */

async function initMatch() {
  var params = new URLSearchParams(window.location.search);
  var matchId = params.get("id");

  if (!matchId) {
      renderError("缺少比赛 ID。请从全景赛程页面选择一场比赛。");
    return;
  }

  try {
    var [schedRes, oddsRes, teamsRes] = await Promise.all([
      fetch("data/schedule.json"),
      fetch("data/odds.json"),
      fetch("data/teams.json"),
    ]);

    if (!schedRes.ok) throw new Error("赛程数据加载失败 (" + schedRes.status + ")");
    if (!oddsRes.ok) throw new Error("赔率数据加载失败 (" + oddsRes.status + ")");
    // teams.json is optional — don't fail if missing
    if (teamsRes.ok) {
      teamsData = await teamsRes.json();
    }

    scheduleData = await schedRes.json();
    oddsData = await oddsRes.json();

    // Build odds lookup
    oddsData.predictions.forEach(function (p) {
      oddsMap[p.match_id] = p;
    });

    // Find match in schedule
    var match = findMatch(matchId);

    if (!match) {
        renderError("找不到比赛 " + matchId + "。请从全景赛程页面选择一场比赛。");
      return;
    }

    renderMatch(match);

    // Update page title
    document.title = codeName(match.home_code) + " vs " + codeName(match.away_code) + " - CDS4WorldCup";

    // Update breadcrumb with match info
    var bcCurrent = document.querySelector(".breadcrumb .current");
    if (bcCurrent) {
      bcCurrent.textContent = codeName(match.home_code) + " vs " + codeName(match.away_code);
    }

  } catch (err) {
    renderError("数据加载失败：" + escapeHtml(err.message));
  }
}

/* ── Find match by ID ────────────────────────────── */

function findMatch(matchId) {
  var groups = scheduleData.groups || {};

  // Search group stage
  for (var letter in groups) {
    var matches = groups[letter].matches || [];
    for (var i = 0; i < matches.length; i++) {
      if (matches[i].match_id === matchId) {
        matches[i]._group = letter;
        matches[i]._stage = "group";
        return matches[i];
      }
    }
  }

  // Search knockout stage
  var knockout = scheduleData.knockout || [];
  for (var j = 0; j < knockout.length; j++) {
    if (knockout[j].match_id === matchId) {
      knockout[j]._stage = "knockout";
      return knockout[j];
    }
  }

  return null;
}

/* ── Render ──────────────────────────────────────── */

function renderMatch(match) {
  renderHero(match);
  renderProbabilities(match);
  renderInfo(match);
}

function renderError(message) {
  var hero = document.querySelector("[data-match-hero]");
  if (hero) {
    hero.innerHTML = '<div class="empty-state">' + escapeHtml(message) + '</div>';
  }
}

/* ── Hero ────────────────────────────────────────── */

function renderHero(match) {
  var hero = document.querySelector("[data-match-hero]");
  if (!hero) return;

  var pred = oddsMap[match.match_id];
  var roundLabel = match._stage === "group"
    ? (match._group + " 组 · 第" + escapeHtml(String(match.round)) + "轮")
    : (roundName(match.round) || "淘汰赛");

  var html = '<div class="section-head">';
  html += '<p class="eyebrow">比赛详情</p>';
  html += '</div>';

  html += '<div class="match-hero-content">';
  // Home team
  var homeSlug = codeSlug(match.home_code);
  html += '<div class="match-hero-team">';
  html += '<span class="match-hero-flag">' + codeFlag(match.home_code) + '</span>';
  html += '<span class="match-hero-team-name">' + (homeSlug ? '<a href="team.html?team=' + escapeAttr(homeSlug) + '">' + escapeHtml(codeName(match.home_code)) + '</a>' : escapeHtml(codeName(match.home_code))) + '</span>';
  html += '</div>';

  // VS
  html += '<div class="match-hero-vs">VS</div>';

  // Away team
  var awaySlug = codeSlug(match.away_code);
  html += '<div class="match-hero-team">';
  html += '<span class="match-hero-flag">' + codeFlag(match.away_code) + '</span>';
  html += '<span class="match-hero-team-name">' + (awaySlug ? '<a href="team.html?team=' + escapeAttr(awaySlug) + '">' + escapeHtml(codeName(match.away_code)) + '</a>' : escapeHtml(codeName(match.away_code))) + '</span>';
  html += '</div>';
  html += '</div>';

  // Meta
  html += '<div class="match-hero-meta">';
  html += '<span class="match-group-badge">' + escapeHtml(roundLabel) + '</span>';
  if (match.date) {
    html += '<span>' + escapeHtml(match.date) + '</span>';
  }
  if (match.kickoff) {
    html += '<span>' + escapeHtml(match.kickoff) + '</span>';
  }
  if (pred && pred.expected_goals_home != null) {
    html += '<span>xG ' + pred.expected_goals_home.toFixed(1) + ' - ' + pred.expected_goals_away.toFixed(1) + '</span>';
  }
  html += '</div>';

  hero.innerHTML = html;
}

/* ── Probabilities ───────────────────────────────── */

function renderProbabilities(match) {
  var section = document.querySelector("[data-match-probs]");
  var container = document.querySelector("[data-prob-sources]");
  if (!section || !container) return;

  var pred = oddsMap[match.match_id];
  var html = "";

  if (pred) {
    var hw = pred.home_win || 0;
    var dr = pred.draw || 0;
    var aw = pred.away_win || 0;

    // Fan-mode: big numbers + wide bar
    html += '<div class="fan-prob-row">';
    html += '<span class="fan-pct-big home">' + pct(hw) + '</span>';
    html += '<div class="fan-prob-track">';
    html += '<div class="fan-prob-seg home" style="width:' + (hw * 100).toFixed(1) + '%">' + (hw * 100).toFixed(0) + '</div>';
    html += '<div class="fan-prob-seg draw" style="width:' + (dr * 100).toFixed(1) + '%">平</div>';
    html += '<div class="fan-prob-seg away" style="width:' + (aw * 100).toFixed(1) + '%">' + (aw * 100).toFixed(0) + '</div>';
    html += '</div>';
    html += '<span class="fan-pct-big away">' + pct(aw) + '</span>';
    html += '</div>';
    html += '<p class="fan-draw-note">平局概率 <strong>' + pct(dr) + '</strong></p>';

    // Three-signal comparison (compact, below)
    html += '<div class="tri-signal">';
    html += '<p class="tri-signal-label">三源对比</p>';
    html += '<div class="tri-signal-row">';
    html += '<div class="tri-signal-item">';
    html += '<span class="tri-src-name">Elo</span>';
    html += '<div class="tri-track">';
    html += '<div class="tri-fill-home" style="width:' + (hw * 100).toFixed(1) + '%"></div>';
    html += '<div class="tri-fill-draw" style="width:' + (dr * 100).toFixed(1) + '%"></div>';
    html += '<div class="tri-fill-away" style="width:' + (aw * 100).toFixed(1) + '%"></div>';
    html += '</div>';
    html += '<span class="tri-val">' + pct(hw) + '/' + pct(dr) + '/' + pct(aw) + '</span>';
    html += '</div>';
    html += '<div class="tri-signal-item">';
    html += '<span class="tri-src-name">市场</span>';
    html += '<div class="tri-track"><div style="width:100%;background:#eee;height:100%"></div></div>';
    html += '<span class="tri-val" style="color:var(--muted)">待接入</span>';
    html += '</div>';
    html += '<div class="tri-signal-item">';
    html += '<span class="tri-src-name">AI</span>';
    html += '<div class="tri-track"><div style="width:100%;background:#eee;height:100%"></div></div>';
    html += '<span class="tri-val" style="color:var(--muted)">待接入</span>';
    html += '</div>';
    html += '</div></div>';
  } else {
    html += '<div class="prob-source-placeholder">暂无数据</div>';
  }

  container.innerHTML = html;
  section.style.display = "";
}

/* ── Info ────────────────────────────────────────── */

function renderInfo(match) {
  var section = document.querySelector("[data-match-info]");
  var grid = document.querySelector("[data-info-grid]");
  if (!section || !grid) return;

  var html = "";
  var venueInfo = scheduleData.venues ? scheduleData.venues[match.venue] : null;

  // Venue
  if (match.venue) {
    html += infoCard("比赛城市", match.venue);
  }
  if (venueInfo && venueInfo.stadium) {
    html += infoCard("场馆", venueInfo.stadium);
  }
  if (venueInfo && venueInfo.country) {
    html += infoCard("国家", venueInfo.city + ", " + venueInfo.country);
  }
  if (venueInfo && venueInfo.timezone) {
    html += infoCard("时区", venueInfo.timezone);
  }

  // Match context
  if (match._stage === "group" && match._group) {
    html += infoCard("小组", match._group + " 组");
  }
  if (match.round) {
    var label = match._stage === "group"
      ? "第" + escapeHtml(String(match.round)) + "轮"
      : roundName(match.round);
    html += infoCard("轮次", label);
  }

  // Match ID
  html += infoCard("比赛编号", match.match_id);

  // Data timestamp
  if (scheduleData.generated_at) {
    html += infoCard("数据更新", formatDate(scheduleData.generated_at));
  }

  if (!html) {
    html = '<div class="prob-source-placeholder">暂无比赛信息</div>';
  }

  grid.innerHTML = html;
  section.style.display = "";
}

function infoCard(label, value) {
  return '<div class="info-card">' +
    '<div class="info-card-label">' + escapeHtml(label) + '</div>' +
    '<div class="info-card-value">' + escapeHtml(value) + '</div>' +
    '</div>';
}

/* ── Probability bar ─────────────────────────────── */

function renderProbBar(homeWin, draw, awayWin) {
  var _pcts = distributePct([homeWin, draw, awayWin]);
  var hw = _pcts[0];
  var dr = _pcts[1];
  var aw = _pcts[2];

  var html = '<div class="prob-bar" title="主胜 ' + hw + '% / 平 ' + dr + '% / 客胜 ' + aw + '%">';
  html += '<div class="prob-seg prob-home" style="width:' + hw + '%">' + (hw >= 12 ? hw + "%" : "") + '</div>';
  html += '<div class="prob-seg prob-draw" style="width:' + dr + '%">' + (dr >= 10 ? dr + "%" : "") + '</div>';
  html += '<div class="prob-seg prob-away" style="width:' + aw + '%">' + (aw >= 12 ? aw + "%" : "") + '</div>';
  html += '</div>';
  return html;
}

/* ── Helpers ─────────────────────────────────────── */

function pct(val) {
  return (val * 100).toFixed(1) + "%";
}

function roundName(round) {
  var names = {
    round_of_32: "1/16 决赛",
    round_of_16: "1/8 决赛",
    quarterfinal: "四分之一决赛",
    semifinal: "半决赛",
    third_place: "季军赛",
    final: "决赛"
  };
  return names[round] || round || "";
}

// formatDate is now in common.js

/* ── Boot ────────────────────────────────────────── */

initMatch().catch(function (err) {
  renderError("比赛页加载失败：" + escapeHtml(err.message));
});
