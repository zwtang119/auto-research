/**
 * team-detail.js — CDS4WorldCup 球队详情页（论证链版）
 *
 * 结构：论点 → 证据链 → 反证 → 关键变量 → 验证 → 共识 → 附录
 */

var els = {
  meta:              document.querySelector("[data-team-meta]"),
  title:             document.querySelector("[data-team-title]"),
  opening:           document.querySelector("[data-team-opening]"),
  thesis:            document.querySelector("[data-team-thesis]"),
  thesisCards:       document.querySelector("[data-thesis-cards]"),
  groupMatches:      document.querySelector("[data-team-group-matches]"),
  pathAttenuation:   document.querySelector("[data-path-attenuation]"),
  bullCase:          document.querySelector("[data-bull-case]"),
  counterEvidence:   document.querySelector("[data-counter-evidence]"),
  keyVariable:       document.querySelector("[data-key-variable]"),
  verification:      document.querySelector("[data-verification]"),
  consensus:         document.querySelector("[data-market-consensus]"),
  aiPerspective:     document.querySelector("[data-team-ai-perspective]"),
  swans:             document.querySelector("[data-team-swans]"),
  analysis:          document.querySelector("[data-team-analysis]"),
};

/* ═══ Bootstrap ════════════════════════════════════ */

async function initTeamDetail() {
  if (!els.title) return;

  var payload = await loadTeamDetails();
  var slug = getRequestedTeamSlug(payload);
  var team = payload.teams?.[slug] || Object.values(payload.teams || {})[0];

  if (!team) {
    renderMissing("暂时没有球队详情数据。");
    return;
  }

  document.title = team.team.zh_name + "夺冠路 - CDS4WorldCup";
  var bc = document.querySelector("[data-breadcrumb-team]");
  if (bc) bc.textContent = team.team.zh_name;

  // ── Argument chain rendering ──
  renderThesis(team);

  var extra = await loadExtraData();
  if (extra) {
    renderGroupMatches(team, extra);
    renderConsensus(team, extra);
  }

  renderPathAttenuation(team);
  renderBullCase(team);
  renderCounterEvidence(team);
  renderKeyVariable(team);
  renderVerification(team);

  // Appendix
  renderAiPerspective(team);
  renderSwans(team);
  renderAnalysis(team);
}

/* ═══ Data Loaders (unchanged) ═══════════════════ */

async function loadTeamDetails() {
  if (window.CDS4WORLDCUP_TEAM_DETAILS) {
    return window.CDS4WORLDCUP_TEAM_DETAILS;
  }
  var response = await fetch("data/team-details.json");
  if (!response.ok) throw new Error("球队详情加载失败 (" + response.status + ")");
  return response.json();
}

function getRequestedTeamSlug(payload) {
  var params = new URLSearchParams(window.location.search);
  var direct = params.get("team") || params.get("slug");
  var hash = window.location.hash ? window.location.hash.replace("#", "") : "";
  var slug = normalizeSlug(direct || hash || "argentina");
  if (payload.teams?.[slug]) return slug;
  return "argentina";
}

function normalizeSlug(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9-]/g, "");
}

async function loadExtraData() {
  try {
    var results = await Promise.all([
      fetch("data/schedule.json"),
      fetch("data/odds.json"),
      fetch("data/baselines.json"),
    ]);
    var schedule = results[0].ok ? await results[0].json() : null;
    var odds     = results[1].ok ? await results[1].json() : null;
    var baselines= results[2].ok ? await results[2].json() : null;
    if (!schedule && !odds && !baselines) return null;
    var oddsMap = {};
    if (odds) {
      (odds.predictions || []).forEach(function (p) { oddsMap[p.match_id] = p; });
    }
    return { schedule: schedule, odds: odds, oddsMap: oddsMap, baselines: baselines };
  } catch (e) {
    return null;
  }
}

/* ═══ Helper: find CDS team by name ═══════════════ */

function findCdsTeam(canonicalName) {
  var data = window.CDS4WORLDCUP_CDS_PATHS;
  if (!data || !data.teams) return null;
  var t = data.teams[canonicalName];
  if (t) return t;
  var keys = Object.keys(data.teams);
  for (var i = 0; i < keys.length; i++) {
    if (keys[i].toLowerCase() === canonicalName.toLowerCase()) {
      return data.teams[keys[i]];
    }
  }
  return null;
}

/**
 * Build 6-stage probability array from CDS data:
 * [qual_prob, R32_cum, R16_cum, QF_cum, SF_cum, championship_prob]
 */
function buildStages(cdsTeam) {
  if (!cdsTeam) return null;
  var q = cdsTeam.qualification;
  var ch = cdsTeam.championship;
  if (!q || !ch) return null;

  var stages = [q.qual_prob];
  var nodes = ch.path_nodes || [];
  // path_nodes: R32, R16, QF, SF (4 nodes before final)
  for (var i = 0; i < Math.min(nodes.length, 4); i++) {
    stages.push(nodes[i].cumulative_prob);
  }
  stages.push(ch.championship_prob);
  return stages;
}

/* ═══ Block 1: Thesis ═════════════════════════════ */

function renderThesis(detail) {
  var team = detail.team;

  // Hero
  els.meta.textContent = (team.confederation_label || team.confederation) + " · " +
    (team.group ? team.group + " 组" : "小组待定") + " · " + team.status_label;
  els.title.innerHTML = escapeHtml(team.flag) + " " + escapeHtml(team.zh_name) +
    " <span>" + escapeHtml(team.en_name) + "</span>";
  els.opening.textContent = detail.analysis.opening;
  els.thesis.textContent = detail.analysis.thesis;

  // 3 probability cards
  var cdsTeam = findCdsTeam(team.canonical_name || team.en_name || detail.slug);
  var qualP = null, sfP = null, champP = null;
  if (cdsTeam) {
    qualP = cdsTeam.qualification ? cdsTeam.qualification.qual_prob : null;
    champP = cdsTeam.championship ? cdsTeam.championship.championship_prob : null;
    var nodes = (cdsTeam.championship && cdsTeam.championship.path_nodes) || [];
    // SF cumulative = path_nodes[3] (index 3 = semifinal)
    if (nodes.length >= 4) sfP = nodes[3].cumulative_prob;
  }

  els.thesisCards.innerHTML =
    thesisCard("出线", qualP, "小组出线") +
    thesisCard("四强", sfP, "进半决赛") +
    thesisCard("夺冠", champP, "最终夺冠");
}

function thesisCard(label, prob, desc) {
  var pct = prob != null ? (prob * 100).toFixed(1) : "—";
  var cls = prob == null ? " thesis-card-muted" : "";
  var bar = prob != null ? '<div class="thesis-card-bar"><span class="thesis-card-fill" style="width:' +
    Math.max(2, prob * 100) + '%"></span></div>' : "";
  return '<div class="thesis-prob-card' + cls + '">' +
    '<div class="thesis-card-label">' + escapeHtml(label) + '</div>' +
    '<div class="thesis-card-pct">' + pct + '<span class="thesis-card-unit">%</span></div>' +
    bar +
    '<div class="thesis-card-desc">' + escapeHtml(desc) + '</div>' +
    '</div>';
}

/* ═══ Block 2: Group Matches ═════════════════════ */

function renderGroupMatches(detail, extra) {
  if (!els.groupMatches || !extra.schedule) return;

  var schedule = extra.schedule;
  var groupName = detail.team.group;
  if (!groupName) {
    els.groupMatches.innerHTML = '<div class="empty-state">小组分配待定。</div>';
    return;
  }

  var group = schedule.groups[groupName];
  if (!group) {
    els.groupMatches.innerHTML = '<div class="empty-state">未找到 ' + escapeHtml(groupName) + ' 组赛程数据。</div>';
    return;
  }

  var teamName = detail.team.canonical_name;
  var matches = (group.matches || []).filter(function (m) {
    return m.home === teamName || m.away === teamName;
  }).sort(function (a, b) {
    return (a.date || "").localeCompare(b.date || "");
  });

  var html = '<div class="group-match-cards">';
  matches.forEach(function (match) {
    var isHome = match.home === teamName;
    var opponent = isHome ? match.away : match.home;
    var oppCode = isHome ? match.away_code : match.home_code;

    // Probability from odds
    var pred = extra.oddsMap[match.match_id];
    var teamWinP = null;
    var label = "";
    if (pred) {
      teamWinP = isHome ? pred.home_win : pred.away_win;
      if (teamWinP >= 0.6) label = "应拿下";
      else if (teamWinP >= 0.4) label = "关键战";
      else label = "看情况";
    }

    html += '<a class="group-match-card" href="match.html?id=' + escapeAttr(match.match_id) + '">';
    html += '<div class="gmc-head">';
    html += '<span class="gmc-round">第' + escapeHtml(String(match.round)) + '轮</span>';
    html += '<span class="gmc-date">' + escapeHtml(match.date || "") + '</span>';
    html += '</div>';
    html += '<div class="gmc-opponent">' + teamFlag(oppCode) + ' ' + escapeHtml(opponent) + '</div>';

    if (teamWinP != null) {
      var pctVal = (teamWinP * 100).toFixed(0);
      var barWidth = Math.max(5, teamWinP * 100);
      html += '<div class="gmc-prob-bar">';
      html += '<span class="gmc-prob-fill" style="width:' + barWidth + '%"></span>';
      html += '</div>';
      html += '<div class="gmc-prob-footer">';
      html += '<span class="gmc-prob-val">' + pctVal + '%</span>';
      html += '<span class="gmc-prob-label ' + probLabelClass(teamWinP) + '">' + escapeHtml(label) + '</span>';
      html += '</div>';
    } else {
      html += '<div class="gmc-prob-bar gmc-prob-empty"></div>';
    }
    html += '</a>';
  });
  html += '</div>';
  html += '<p class="source-note">概率来源：Elo+泊松数值模型模拟，非事实。仅作参考。</p>';
  els.groupMatches.innerHTML = html;
}

function probLabelClass(p) {
  if (p >= 0.6) return "label-fav";
  if (p >= 0.4) return "label-key";
  return "label-uncertain";
}

/* ═══ Block 3: Path Attenuation ══════════════════ */

function renderPathAttenuation(detail) {
  if (!els.pathAttenuation) return;

  var canonicalName = detail.team.canonical_name || detail.team.en_name || detail.slug;
  var cdsTeam = findCdsTeam(canonicalName);
  if (!cdsTeam) {
    els.pathAttenuation.innerHTML = '<div class="empty-state">这支队暂时没有路径推演数据。</div>';
    return;
  }

  var stages = buildStages(cdsTeam);
  if (!stages || stages.length < 6) {
    els.pathAttenuation.innerHTML = '<div class="empty-state">路径节点数据不完整。</div>';
    return;
  }

  var stageLabels = ["出线", "R32", "R16", "八强", "四强", "夺冠"];
  var deltas = [];
  for (var i = 0; i < stages.length - 1; i++) {
    deltas.push(stages[i] - stages[i + 1]);
  }
  // Find biggest drop
  var maxDrop = 0, maxDropIdx = 0;
  for (var j = 0; j < deltas.length; j++) {
    if (deltas[j] > maxDrop) { maxDrop = deltas[j]; maxDropIdx = j; }
  }

  // Build horizontal path bar
  var html = '<div class="path-atten-bar">';
  for (var k = 0; k < stages.length; k++) {
    var pct = (stages[k] * 100).toFixed(1);
    var dropPct = k > 0 ? "↓" + (deltas[k - 1] * 100).toFixed(1) + "%" : "";
    var isMaxDrop = (k > 0 && k - 1 === maxDropIdx);
    var warnIcon = isMaxDrop ? ' ⚠' : '';
    html += '<div class="path-atten-node' + (isMaxDrop ? " path-atten-warn" : "") + '">';
    html += '<div class="pa-label">' + escapeHtml(stageLabels[k]) + '</div>';
    html += '<div class="pa-bar-wrap"><span class="pa-fill" style="width:' + Math.max(2, stages[k] * 100) + '%"></span></div>';
    html += '<div class="pa-value">' + pct + '%</div>';
    if (dropPct) {
      html += '<div class="pa-drop' + (isMaxDrop ? " pa-drop-max" : "") + '">' + dropPct + warnIcon + '</div>';
    } else {
      html += '<div class="pa-drop pa-drop-placeholder"> </div>';
    }
    html += '</div>';
  }
  html += '</div>';

  // Highlight the biggest drop explanation
  html += '<div class="path-atten-highlight">';
  html += '<p><strong>最大衰减：</strong>' + escapeHtml(stageLabels[maxDropIdx]) + ' → ' +
    escapeHtml(stageLabels[maxDropIdx + 1]) + '，掉 ' + (maxDrop * 100).toFixed(1) + ' 个百分点。</p>';
  html += '</div>';

  // Compare with top 3 other teams
  html += renderPathComparison(canonicalName, stages, stageLabels);

  html += '<p class="source-note">Elo+泊松 模型模拟 · 三信号并列不融合 · 仅作参考</p>';
  els.pathAttenuation.innerHTML = html;
}

function renderPathComparison(currentName, currentStages, stageLabels) {
  var data = window.CDS4WORLDCUP_CDS_PATHS;
  if (!data || !data.teams) return "";

  // Collect all teams with complete stage data
  var allTeams = [];
  Object.keys(data.teams).forEach(function (name) {
    var s = buildStages(data.teams[name]);
    if (s && s.length >= 6) {
      allTeams.push({ name: name, stages: s });
    }
  });

  if (allTeams.length < 2) return "";

  // Pick top 3 by championship_prob (excluding current team)
  allTeams.sort(function (a, b) { return b.stages[5] - a.stages[5]; });
  var topOthers = allTeams.filter(function (t) { return t.name !== currentName; }).slice(0, 3);
  if (!topOthers.length) return "";

  // Show total attenuation (qual → champ) comparison
  var html = '<div class="path-compare">';
  html += '<h3>对比热门球队的总衰减</h3>';
  html += '<div class="path-compare-rows">';

  // Current team
  var curDrop = (currentStages[0] - currentStages[5]) * 100;
  html += pathCompareRow(currentName, curDrop, true);

  topOthers.forEach(function (t) {
    var drop = (t.stages[0] - t.stages[5]) * 100;
    html += pathCompareRow(t.name, drop, false);
  });

  html += '</div></div>';
  return html;
}

function pathCompareRow(name, dropPct, isCurrent) {
  var maxDrop = 100; // theoretical max
  var barW = Math.max(5, (dropPct / maxDrop) * 100);
  var cls = isCurrent ? " path-compare-current" : "";
  return '<div class="path-compare-row' + cls + '">' +
    '<span class="pcr-name">' + escapeHtml(name) + '</span>' +
    '<div class="pcr-bar-wrap"><span class="pcr-fill" style="width:' + barW + '%"></span></div>' +
    '<span class="pcr-val">↓' + dropPct.toFixed(1) + '%</span>' +
    '</div>';
}

/* ═══ Block 4: Bull Case ══════════════════════════ */

function renderBullCase(detail) {
  if (!els.bullCase) return;
  var items = detail.required_breakthroughs || [];
  if (!items.length) {
    els.bullCase.innerHTML = '<div class="empty-state">这支队的突破条件还在补资料。</div>';
    return;
  }

  // Show first 3
  var shown = items.slice(0, 3);
  var html = '<div class="bull-cards">';
  shown.forEach(function (item, idx) {
    html += '<div class="bull-card">';
    html += '<div class="bull-index">' + (idx + 1) + '</div>';
    html += '<h3>' + escapeHtml(item.breakthrough) + '</h3>';
    html += '<p>' + escapeHtml(item.minimum) + '</p>';
    if (item.failure_signal) {
      html += '<div class="bull-danger">危险信号：' + escapeHtml(item.failure_signal) + '</div>';
    }
    html += '</div>';
  });
  html += '</div>';
  els.bullCase.innerHTML = html;
}

/* ═══ Block 5: Counter-evidence ═══════════════════ */

function renderCounterEvidence(detail) {
  if (!els.counterEvidence) return;
  var items = detail.primary_obstacles || [];
  if (!items.length) {
    els.counterEvidence.innerHTML = '<div class="empty-state">这支队还没有完整难点拆解。</div>';
    return;
  }

  var html = '<div class="counter-cards">';
  items.forEach(function (item) {
    html += '<div class="counter-card">';
    html += '<div class="counter-type">' + escapeHtml(item.type_label) + '</div>';
    html += '<h3>' + escapeHtml(item.obstacle) + '</h3>';
    html += '<p>' + escapeHtml(item.why) + '</p>';
    if (item.observable_proxy) {
      html += '<div class="counter-proxy">可观测：' + escapeHtml(item.observable_proxy) + '</div>';
    }
    html += '</div>';
  });
  html += '</div>';
  els.counterEvidence.innerHTML = html;
}

/* ═══ Block 6: Key Variable ═══════════════════════ */

function renderKeyVariable(detail) {
  if (!els.keyVariable) return;

  // Priority: dominant_failure_node > biggest obstacle
  var canonicalName = detail.team.canonical_name || detail.team.en_name || detail.slug;
  var cdsTeam = findCdsTeam(canonicalName);
  var keyText = "";
  var keyLabel = "决定性变量";

  if (cdsTeam && cdsTeam.championship && cdsTeam.championship.dominant_failure_node) {
    keyText = cdsTeam.championship.dominant_failure_node;
    keyLabel = "最大阻力节点";
  } else if (detail.primary_obstacles && detail.primary_obstacles.length) {
    keyText = detail.primary_obstacles[0].obstacle;
    keyLabel = detail.primary_obstacles[0].type_label || "主要难点";
  }

  if (!keyText) {
    els.keyVariable.innerHTML = '<div class="empty-state">关键变量待补。</div>';
    return;
  }

  els.keyVariable.innerHTML =
    '<div class="key-var-block">' +
    '<div class="key-var-icon">⚡</div>' +
    '<div class="key-var-content">' +
    '<span class="key-var-label">' + escapeHtml(keyLabel) + '</span>' +
    '<p class="key-var-text">' + escapeHtml(keyText) + '</p>' +
    '</div>' +
    '</div>';
}

/* ═══ Block 7: Verification ═══════════════════════ */

function renderVerification(detail) {
  if (!els.verification) return;
  var watchlist = detail.watchlist || [];
  if (!watchlist.length) {
    els.verification.innerHTML = '<div class="empty-state">观察清单待补。</div>';
    return;
  }

  // Split watchlist items into pre-match signals and post-match reconciliation
  // Heuristic: items with keywords like "后", "赛后", "对账", "验证" → post-match
  var preMatch = [];
  var postMatch = [];
  watchlist.forEach(function (item) {
    var text = String(item).toLowerCase();
    if (text.indexOf("赛后") >= 0 || text.indexOf("对账") >= 0 || text.indexOf("验证") >= 0 ||
        text.indexOf("确认") >= 0 || text.indexOf("复盘") >= 0) {
      postMatch.push(item);
    } else {
      preMatch.push(item);
    }
  });

  var html = '<div class="verify-grid">';

  html += '<div class="verify-col">';
  html += '<h3>赛前盯什么</h3>';
  if (preMatch.length) {
    html += '<ul class="verify-list">';
    preMatch.forEach(function (item) {
      html += '<li>' + escapeHtml(item) + '</li>';
    });
    html += '</ul>';
  } else {
    html += '<div class="empty-state compact">赛前信号待补。</div>';
  }
  html += '</div>';

  html += '<div class="verify-col">';
  html += '<h3>赛后对什么账</h3>';
  if (postMatch.length) {
    html += '<ul class="verify-list">';
    postMatch.forEach(function (item) {
      html += '<li>' + escapeHtml(item) + '</li>';
    });
    html += '</ul>';
  } else {
    html += '<div class="empty-state compact">赛后验证指标待补。</div>';
  }
  html += '</div>';

  html += '</div>';
  els.verification.innerHTML = html;
}

/* ═══ Block 8: Market Consensus ═══════════════════ */

function renderConsensus(detail, extra) {
  if (!els.consensus) return;

  // Build one sentence from baselines data
  var publicModel = detail.public_references ? detail.public_references.public_model_crowd : null;
  var marketSnap = detail.public_references ? detail.public_references.market_snapshot : null;

  var parts = [];

  if (publicModel && publicModel.probability != null) {
    parts.push("公开模型群体给出 " + formatPercent(publicModel.probability) + " 的夺冠概率");
  }
  if (marketSnap && marketSnap.probability != null) {
    parts.push("市场快照为 " + formatPercent(marketSnap.probability));
  }

  // Add baseline comparison if available
  if (extra.baselines && extra.baselines.baselines) {
    var slug = detail.slug;
    var baselines = extra.baselines.baselines;
    var blParts = [];
    var blMeta = { fifa_ranking: "FIFA 排名代理", elo: "Elo 评级", market: "市场公开赔率" };
    Object.keys(blMeta).forEach(function (key) {
      var bl = baselines[key];
      if (bl && bl.teams && bl.teams[slug] != null) {
        blParts.push(blMeta[key] + " " + bl.teams[slug].toFixed(2) + "%");
      }
    });
    if (blParts.length) {
      parts.push("各基线：{ " + blParts.join(" / ") + " }");
    }
  }

  if (!parts.length) {
    els.consensus.innerHTML = '<div class="empty-state">市场共识数据待补。</div>';
    return;
  }

  els.consensus.innerHTML =
    '<div class="consensus-block">' +
    '<p class="consensus-text">' + parts.join("。") + "。</p>" +
    '<p class="source-note">各基线使用不同方法计算，仅作参考对比，不是结论。</p>' +
    '</div>';
}

/* ═══ Block 9: Appendix renderers ═════════════════ */

function renderAiPerspective(detail) {
  if (!els.aiPerspective) return;
  var ai = detail.ai_perspective || {};
  var snippets = Array.isArray(ai.snippets) ? ai.snippets : [];
  if (!snippets.length) {
    els.aiPerspective.innerHTML =
      '<div class="empty-state">' + escapeHtml(ai.display_rule || "这支队还没有外部模型群体参考。") + '</div>';
    return;
  }
  var html = '<div class="team-ai-summary">' +
    '<strong>' + escapeHtml(ai.count || snippets.length) + ' 个视角提到这队</strong>' +
    '<span class="source-badge source-red">只能参考</span></div>';
  html += '<div class="team-ai-snippets">';
  snippets.forEach(function (item) {
    html += '<article><span class="label">' + escapeHtml(item.persona || "代表视角") + '</span>' +
      '<p>' + escapeHtml(item.reason || "") + '</p></article>';
  });
  html += '</div>';
  els.aiPerspective.innerHTML = html;
}

function renderSwans(detail) {
  if (!els.swans) return;
  var items = detail.black_swan_helpers || [];
  if (!items.length) {
    els.swans.innerHTML = '<div class="empty-state">这支队的意外变量还在补资料。</div>';
    return;
  }
  var html = '<div class="detail-list">';
  items.forEach(function (item) {
    html += '<article>' +
      '<span class="tag">' + escapeHtml(item.observable ? "可观测：" + item.observable : "可观测性待补") + '</span>' +
      '<h3>' + escapeHtml(item.event) + '</h3>' +
      '<p>' + escapeHtml(item.mechanism) + '</p>' +
      (item.note ? '<small>' + escapeHtml(item.note) + '</small>' : '') +
      '</article>';
  });
  html += '</div>';
  els.swans.innerHTML = html;
}

function renderAnalysis(detail) {
  if (!els.analysis) return;
  var sections = detail.analysis.sections || [];
  els.analysis.innerHTML = sections.map(function (section, index) {
    return '<article class="analysis-card">' +
      '<span class="analysis-index">' + (index + 1) + '</span>' +
      '<div>' +
      '<h2>' + escapeHtml(section.title) + '</h2>' +
      '<p>' + escapeHtml(section.body) + '</p>' +
      '<div class="so-what">' + escapeHtml(section.so_what) + '</div>' +
      '</div></article>';
  }).join("");
}

/* ═══ Utilities ════════════════════════════════════ */

function teamCode(name) { return cdsEnNameToCode(name); }
function teamFlag(code) { return cdsCodeFlag(code); }

function renderMissing(message) {
  if (els.title) els.title.textContent = "没有找到球队";
  if (els.opening) els.opening.textContent = message;
}

function formatPercent(value) {
  return typeof value === "number" ? value + "%" : "";
}

/* ═══ Launch ═══════════════════════════════════════ */

initTeamDetail().catch(function (error) {
  var detail = window.location.protocol === "file:"
    ? "本地直接打开 HTML 时，部分浏览器会拦截数据读取。当前版本已内置兜底数据；如果仍看不到内容，请刷新页面，或在仓库里运行 python3 -m http.server 8000 --directory site 后访问 http://localhost:8000/team.html?team=argentina。"
    : "球队详情加载失败：" + error.message;
  renderMissing(detail);
});
