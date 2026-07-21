/**
 * panorama.js — CDS4WorldCup 全景赛程页面
 *
 * 加载 schedule.json + odds.json，渲染 12 组赛程矩阵 + 淘汰赛签表。
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

let scheduleData = null;
let oddsData = null;
let oddsMap = {};
let currentView = "group"; // "group" | "knockout" | "date"

/* ── Init ────────────────────────────────────────── */

async function initPanorama() {
  const container = document.querySelector("[data-panorama-grid]");
  if (!container) return;

  try {
    const [schedRes, oddsRes] = await Promise.all([
      fetch("data/schedule.json"),
      fetch("data/odds.json"),
    ]);
    if (!schedRes.ok) throw new Error("赛程数据加载失败 (" + schedRes.status + ")");
    if (!oddsRes.ok) throw new Error("赔率数据加载失败 (" + oddsRes.status + ")");

    scheduleData = await schedRes.json();
    oddsData = await oddsRes.json();

    // Build odds lookup: match_id → prediction
    oddsData.predictions.forEach(function (p) {
      oddsMap[p.match_id] = p;
    });

    // Detect mobile and set default view
    if (window.innerWidth <= 768) {
      currentView = "date";
    }

    setupViewSwitcher();
    render();
    updateGeneratedAt();
  } catch (err) {
    container.innerHTML =
      '<div class="empty-state">数据加载失败：' + escapeHtml(err.message) +
      '。请刷新页面或访问 <a href="index.html">首页</a>。</div>';
  }
}

/* ── View Switcher ───────────────────────────────── */

function setupViewSwitcher() {
  var switcher = document.querySelector("[data-view-switcher]");
  if (!switcher) return;

  switcher.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-view]");
    if (!btn) return;
    currentView = btn.getAttribute("data-view");
    // Update active state
    switcher.querySelectorAll("[data-view]").forEach(function (b) {
      b.classList.toggle("active", b.getAttribute("data-view") === currentView);
    });
    render();
  });

  // Set initial active
  switcher.querySelectorAll("[data-view]").forEach(function (b) {
    b.classList.toggle("active", b.getAttribute("data-view") === currentView);
  });
}

/* ── Render Dispatch ─────────────────────────────── */

function render() {
  var grid = document.querySelector("[data-panorama-grid]");
  var bracket = document.querySelector("[data-knockout-bracket]");
  var dateView = document.querySelector("[data-date-view]");

  // Hide all
  if (grid) grid.style.display = "none";
  if (bracket) bracket.style.display = "none";
  if (dateView) dateView.style.display = "none";

  if (currentView === "group") {
    if (grid) {
      grid.style.display = "";
      renderGroupStage(grid);
    }
  } else if (currentView === "knockout") {
    if (bracket) {
      bracket.style.display = "";
      renderKnockoutStage(bracket);
    }
  } else if (currentView === "date") {
    if (dateView) {
      dateView.style.display = "";
      renderDateView(dateView);
    }
  }
}

/* ── Group Stage ─────────────────────────────────── */

function renderGroupStage(container) {
  var groups = scheduleData.groups || {};
  var letters = scheduleData.summary.group_letters || [];
  var html = "";

  letters.forEach(function (letter) {
    var group = groups[letter];
    if (!group) return;
    var teams = group.teams || [];
    var matches = group.matches || [];

    html += '<div class="panorama-group" data-group="' + escapeAttr(letter) + '">';
    html += '<div class="group-header">';
    html += '<span class="group-label">' + escapeHtml(letter) + " 组</span>";
    html += '<div class="group-teams">' + teams.map(function (t) {
      var slug = codeSlug(t.code);
      var nameHtml = codeFlag(t.code) + " " + escapeHtml(codeName(t.code));
      return slug
        ? '<a class="group-team" href="team.html?team=' + escapeAttr(slug) + '">' + nameHtml + "</a>"
        : '<span class="group-team">' + nameHtml + "</span>";
    }).join("") + "</div>";
    html += "</div>";

    // 3 rounds
    [1, 2, 3].forEach(function (round) {
      html += '<div class="group-round"><span class="round-label">第' + round + "轮</span>";
      html += '<div class="round-matches">';
      var roundMatches = matches.filter(function (m) { return m.round === round; });
      roundMatches.forEach(function (match) {
        html += renderMatchCard(match);
      });
      html += "</div></div>";
    });

    html += "</div>";
  });

  container.innerHTML = html;
  bindMatchCardClicks(container);
}

/* ── Match Card ──────────────────────────────────── */

function renderMatchCard(match) {
  var pred = oddsMap[match.match_id];
  var isPlayed = match.status === "played";
  var heatClass = getHeatZone(pred);

  var html = '<div class="match-card ' + heatClass + (isPlayed ? " match-played" : "") +
    '" data-match-id="' + escapeAttr(match.match_id) + '">';

  // Teams
  html += '<div class="match-teams">';
  html += '<div class="match-team match-home">';
  html += '<span class="match-flag">' + codeFlag(match.home_code) + "</span>";
  html += '<span class="match-team-name">' + escapeHtml(codeName(match.home_code)) + "</span>";
  if (isPlayed && match.home_score != null) {
    html += '<span class="match-score">' + escapeHtml(String(match.home_score)) + "</span>";
  }
  html += "</div>";
  html += '<div class="match-team match-away">';
  html += '<span class="match-flag">' + codeFlag(match.away_code) + "</span>";
  html += '<span class="match-team-name">' + escapeHtml(codeName(match.away_code)) + "</span>";
  if (isPlayed && match.away_score != null) {
    html += '<span class="match-score">' + escapeHtml(String(match.away_score)) + "</span>";
  }
  html += "</div>";
  html += "</div>";

  // Date/time
  html += '<div class="match-meta">';
  html += '<span class="match-date">' + escapeHtml(match.date || "") + "</span>";
  if (match.kickoff) {
    html += '<span class="match-time">' + escapeHtml(match.kickoff) + "</span>";
  }
  html += "</div>";

  // Probability bar
  if (pred) {
    var _pcts = distributePct([pred.home_win, pred.draw, pred.away_win]);
    var hw = _pcts[0];
    var dr = _pcts[1];
    var aw = _pcts[2];
    html += '<div class="prob-bar" title="主胜 ' + hw + "% / 平 " + dr + "% / 客胜 " + aw + '%">';
    html += '<div class="prob-seg prob-home" style="width:' + hw + '%">' + (hw >= 12 ? hw + "%" : "") + "</div>";
    html += '<div class="prob-seg prob-draw" style="width:' + dr + '%">' + (dr >= 10 ? dr + "%" : "") + "</div>";
    html += '<div class="prob-seg prob-away" style="width:' + aw + '%">' + (aw >= 12 ? aw + "%" : "") + "</div>";
    html += "</div>";

    // Confidence indicator + source badge
    html += '<div class="match-confidence">';
    html += '<span class="confidence-dot confidence-' + escapeAttr(pred.confidence || "low") + '"></span>';
    html += '<span class="confidence-text">' + escapeHtml(confidenceLabel(pred.confidence)) + "</span>";
    if (pred.expected_goals_home != null) {
      html += '<span class="expected-goals">xG ' + pred.expected_goals_home.toFixed(1) + " - " + pred.expected_goals_away.toFixed(1) + "</span>";
    }
    html += '</div>';
    html += '<div class="cds-prob-source">';
    html += '<span class="cds-prob-source-text">Elo+泊松</span>';
    html += '</div>';
  } else {
    html += '<div class="prob-bar prob-bar-empty"><div class="prob-seg" style="width:100%"></div></div>';
  }

  // Venue
  if (match.venue) {
    html += '<div class="match-venue">' + escapeHtml(match.venue) + "</div>";
  }

  html += "</div>";
  return html;
}

/* ── Knockout Stage ──────────────────────────────── */

function renderKnockoutStage(container) {
  var knockout = scheduleData.knockout || [];
  var rounds = {
    round_of_32: { label: "1/16 决赛", matches: [] },
    round_of_16: { label: "1/8 决赛", matches: [] },
    quarterfinal: { label: "四分之一", matches: [] },
    semifinal: { label: "半决赛", matches: [] },
    third_place: { label: "季军赛", matches: [] },
    final: { label: "决赛", matches: [] },
  };
  var roundOrder = ["round_of_32", "round_of_16", "quarterfinal", "semifinal", "third_place", "final"];

  knockout.forEach(function (m) {
    if (rounds[m.round]) {
      rounds[m.round].matches.push(m);
    }
  });

  var html = '<div class="bracket-container">';
  html += '<div class="bracket-rounds">';

  roundOrder.forEach(function (key) {
    var round = rounds[key];
    if (!round.matches.length) return;
    html += '<div class="bracket-round" data-round="' + escapeAttr(key) + '">';
    html += '<div class="bracket-round-label">' + escapeHtml(round.label) + "</div>";
    html += '<div class="bracket-matches">';
    round.matches.forEach(function (match) {
      html += renderKnockoutCard(match);
    });
    html += "</div></div>";
  });

  html += "</div></div>";
  container.innerHTML = html;
  bindMatchCardClicks(container);
}

function renderKnockoutCard(match) {
  var homeLabel = match.home || match.slot_home || "?";
  var awayLabel = match.away || match.slot_away || "?";
  var homeCode = match.home_code || "";
  var awayCode = match.away_code || "";

  // If slot-based (no actual teams yet), show slot labels
  var isSlot = !match.home;

  var html = '<div class="match-card match-card-knockout" data-match-id="' + escapeAttr(match.match_id) + '">';
  html += '<div class="match-teams">';
  html += '<div class="match-team match-home">';
  if (!isSlot && homeCode) {
    html += '<span class="match-flag">' + codeFlag(homeCode) + "</span>";
    html += '<span class="match-team-name">' + escapeHtml(codeName(homeCode)) + "</span>";
  } else {
    html += '<span class="match-slot">' + escapeHtml(homeLabel) + "</span>";
  }
  html += "</div>";
  html += '<div class="match-team match-away">';
  if (!isSlot && awayCode) {
    html += '<span class="match-flag">' + codeFlag(awayCode) + "</span>";
    html += '<span class="match-team-name">' + escapeHtml(codeName(awayCode)) + "</span>";
  } else {
    html += '<span class="match-slot">' + escapeHtml(awayLabel) + "</span>";
  }
  html += "</div>";
  html += "</div>";

  html += '<div class="match-meta">';
  html += '<span class="match-date">' + escapeHtml(match.date || "") + "</span>";
  if (match.kickoff) {
    html += '<span class="match-time">' + escapeHtml(match.kickoff) + "</span>";
  }
  html += "</div>";

  // Probability bar for knockout (Elo baseline, same as group stage)
  var pred = oddsMap[match.match_id];
  if (pred) {
    var _pcts = distributePct([pred.home_win, pred.draw, pred.away_win]);
    var hw = _pcts[0];
    var dr = _pcts[1];
    var aw = _pcts[2];
    html += '<div class="cds-knockout-prob">';
    html += '<div class="prob-bar" title="主胜 ' + hw + "% / 平 " + dr + "% / 客胜 " + aw + '%">';
    html += '<div class="prob-seg prob-home" style="width:' + hw + '%">' + (hw >= 12 ? hw + "%" : "") + "</div>";
    html += '<div class="prob-seg prob-draw" style="width:' + dr + '%">' + (dr >= 10 ? dr + "%" : "") + "</div>";
    html += '<div class="prob-seg prob-away" style="width:' + aw + '%">' + (aw >= 12 ? aw + "%" : "") + "</div>";
    html += "</div>";
    html += '<div class="cds-prob-source">';
    html += '<span class="cds-prob-source-text">Elo+泊松</span>';
    html += "</div>";
    html += "</div>";

    // Expanded detail (click to see)
    html += '<div class="cds-knockout-detail" id="knockout-detail-' + escapeAttr(match.match_id) + '">';
    html += '<div class="detail-probs">';
    html += '<span>主胜 ' + (pred.home_win * 100).toFixed(1) + "%</span>";
    html += '<span>平 ' + (pred.draw * 100).toFixed(1) + "%</span>";
    html += '<span>客胜 ' + (pred.away_win * 100).toFixed(1) + "%</span>";
    html += "</div>";
    if (pred.expected_goals_home != null) {
      html += '<div class="detail-row"><span>预期进球</span><span>xG ' + pred.expected_goals_home.toFixed(1) + " - " + pred.expected_goals_away.toFixed(1) + "</span></div>";
    }
    html += '<div class="detail-note">数值模型输出，非事实。不作为投注建议。</div>';
    html += "</div>";
  }

  if (match.venue) {
    html += '<div class="match-venue">' + escapeHtml(match.venue) + "</div>";
  }
  html += "</div>";
  return html;
}

/* ── Date View (Mobile) ──────────────────────────── */

function renderDateView(container) {
  var groups = scheduleData.groups || {};
  var allMatches = [];

  Object.keys(groups).forEach(function (letter) {
    (groups[letter].matches || []).forEach(function (m) {
      var mc = Object.assign({}, m);
      mc._group = letter;
      allMatches.push(mc);
    });
  });

  // Group by date
  var byDate = {};
  allMatches.forEach(function (m) {
    var d = m.date || "TBD";
    if (!byDate[d]) byDate[d] = [];
    byDate[d].push(m);
  });

  var sortedDates = Object.keys(byDate).sort();
  var today = new Date().toISOString().slice(0, 10);

  var html = '<div class="date-view-container">';
  sortedDates.forEach(function (date) {
    var matches = byDate[date];
    var isToday = date === today;
    var label = isToday ? "今天 (" + date + ")" : date;

    html += '<div class="date-section' + (isToday ? " date-today" : "") + '">';
    html += '<div class="date-header">' + escapeHtml(label) + ' <span class="date-count">' + matches.length + " 场</span></div>";
    html += '<div class="date-matches">';
    matches.forEach(function (match) {
      var pred = oddsMap[match.match_id];
      html += '<div class="date-match-item">';
      html += '<span class="date-match-group">' + escapeHtml(match._group) + "组</span>";
      html += '<span class="date-match-teams">' + codeFlag(match.home_code) + " " + escapeHtml(codeName(match.home_code)) + " vs " + codeFlag(match.away_code) + " " + escapeHtml(codeName(match.away_code)) + "</span>";
      if (match.kickoff) {
        html += '<span class="date-match-time">' + escapeHtml(match.kickoff) + "</span>";
      }
      if (pred) {
        var _pcts = distributePct([pred.home_win, pred.draw, pred.away_win]);
        var hw = _pcts[0];
        var dr = _pcts[1];
        var aw = _pcts[2];
        html += '<div class="prob-bar prob-bar-sm">';
        html += '<div class="prob-seg prob-home" style="width:' + hw + '%"></div>';
        html += '<div class="prob-seg prob-draw" style="width:' + dr + '%"></div>';
        html += '<div class="prob-seg prob-away" style="width:' + aw + '%"></div>';
        html += "</div>";
      }
      html += "</div>";
    });
    html += "</div></div>";
  });
  html += "</div>";

  container.innerHTML = html;
}

/* ── Match Card Click Handler ────────────────────── */

function bindMatchCardClicks(container) {
  container.querySelectorAll(".match-card").forEach(function (card) {
    card.style.cursor = "pointer";
    card.addEventListener("click", function () {
      var id = card.getAttribute("data-match-id");
      if (!id) return;
      window.location.href = "match.html?id=" + encodeURIComponent(id);
    });
  });
}

/* ── Helpers ─────────────────────────────────────── */

function getHeatZone(pred) {
  if (!pred) return "";
  var max = Math.max(pred.home_win, pred.away_win);
  if (max >= 0.75) return "heat-zone-hot";
  if (max >= 0.60) return "heat-zone-yellow";
  if (max >= 0.50) return "heat-zone-red";
  return "";
}

function confidenceLabel(level) {
  if (level === "high") return "高信心";
  if (level === "medium") return "中信心";
  return "低信心";
}

function updateGeneratedAt() {
  var el = document.querySelector("[data-generated-at]");
  if (el && scheduleData && scheduleData.generated_at) {
    el.textContent = "数据生成：" + formatDate(scheduleData.generated_at);
  }
}

/* ── Boot ────────────────────────────────────────── */

initPanorama().catch(function (err) {
  var container = document.querySelector("[data-panorama-grid]");
  if (container) {
    container.innerHTML = '<div class="empty-state">全景页加载失败：' + escapeHtml(err.message) + "</div>";
  }
});
