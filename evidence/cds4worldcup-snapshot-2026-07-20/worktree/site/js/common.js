/**
 * common.js — CDS4WorldCup 共享前端工具函数
 *
 * 被 homepage.js、team-detail.js、teams.js 共用。
 * 必须在 data-*.js 之后、页面 JS 之前加载。
 */

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value).replace(/`/g, "&#096;");
}

function sourceClass(label) {
  if (label === "可靠事实") return "source-green";
  if (label === "待核验线索") return "source-yellow";
  if (label === "只能参考") return "source-red";
  return "source-mixed";
}

/* ── Shared Country Code Map ─────────────────────── */

var CDS4WORLDCUP_COUNTRY_MAP = {
  MEX: { flag: "\u{1F1F2}\u{1F1FD}", name: "墨西哥", slug: "mexico", enName: "Mexico" },
  RSA: { flag: "\u{1F1FF}\u{1F1E6}", name: "南非", slug: "south-africa", enName: "South Africa" },
  KOR: { flag: "\u{1F1F0}\u{1F1F7}", name: "韩国", slug: "south-korea", enName: "South Korea" },
  CZE: { flag: "\u{1F1E8}\u{1F1FF}", name: "捷克", slug: "czech-republic", enName: "Czech Republic" },
  CAN: { flag: "\u{1F1E8}\u{1F1E6}", name: "加拿大", slug: "canada", enName: "Canada" },
  BIH: { flag: "\u{1F1E7}\u{1F1E6}", name: "波斯尼亚", slug: "bosnia-and-herzegovina", enName: "Bosnia and Herzegovina" },
  QAT: { flag: "\u{1F1F6}\u{1F1E6}", name: "卡塔尔", slug: "qatar", enName: "Qatar" },
  SUI: { flag: "\u{1F1E8}\u{1F1ED}", name: "瑞士", slug: "switzerland", enName: "Switzerland" },
  BRA: { flag: "\u{1F1E7}\u{1F1F7}", name: "巴西", slug: "brazil", enName: "Brazil" },
  MAR: { flag: "\u{1F1F2}\u{1F1E6}", name: "摩洛哥", slug: "morocco", enName: "Morocco" },
  HAI: { flag: "\u{1F1ED}\u{1F1F9}", name: "海地", slug: "haiti", enName: "Haiti" },
  SCO: { flag: "\u{1F3F4}\u{E0067}\u{E0062}\u{E0073}\u{E0063}\u{E0074}\u{E007F}", name: "苏格兰", slug: "scotland", enName: "Scotland" },
  USA: { flag: "\u{1F1FA}\u{1F1F8}", name: "美国", slug: "united-states", enName: "United States" },
  PAR: { flag: "\u{1F1F5}\u{1F1FE}", name: "巴拉圭", slug: "paraguay", enName: "Paraguay" },
  AUS: { flag: "\u{1F1E6}\u{1F1FA}", name: "澳大利亚", slug: "australia", enName: "Australia" },
  TUR: { flag: "\u{1F1F9}\u{1F1F7}", name: "土耳其", slug: "turkey", enName: "Turkey" },
  GER: { flag: "\u{1F1E9}\u{1F1EA}", name: "德国", slug: "germany", enName: "Germany" },
  CUW: { flag: "\u{1F1E8}\u{1F1FC}", name: "库拉索", slug: "curaçao", enName: "Curaçao" },
  CIV: { flag: "\u{1F1E8}\u{1F1EE}", name: "科特迪瓦", slug: "côte-divoire", enName: "Côte d'Ivoire" },
  ECU: { flag: "\u{1F1EA}\u{1F1E8}", name: "厄瓜多尔", slug: "ecuador", enName: "Ecuador" },
  NED: { flag: "\u{1F1F3}\u{1F1F1}", name: "荷兰", slug: "netherlands", enName: "Netherlands" },
  JPN: { flag: "\u{1F1EF}\u{1F1F5}", name: "日本", slug: "japan", enName: "Japan" },
  SWE: { flag: "\u{1F1F8}\u{1F1EA}", name: "瑞典", slug: "sweden", enName: "Sweden" },
  TUN: { flag: "\u{1F1F9}\u{1F1F3}", name: "突尼斯", slug: "tunisia", enName: "Tunisia" },
  BEL: { flag: "\u{1F1E7}\u{1F1EA}", name: "比利时", slug: "belgium", enName: "Belgium" },
  EGY: { flag: "\u{1F1EA}\u{1F1EC}", name: "埃及", slug: "egypt", enName: "Egypt" },
  IRN: { flag: "\u{1F1EE}\u{1F1F7}", name: "伊朗", slug: "iran", enName: "Iran" },
  NZL: { flag: "\u{1F1F3}\u{1F1FF}", name: "新西兰", slug: "new-zealand", enName: "New Zealand" },
  ESP: { flag: "\u{1F1EA}\u{1F1F8}", name: "西班牙", slug: "spain", enName: "Spain" },
  CPV: { flag: "\u{1F1E8}\u{1F1FB}", name: "佛得角", slug: "cape-verde", enName: "Cape Verde" },
  KSA: { flag: "\u{1F1F8}\u{1F1E6}", name: "沙特", slug: "saudi-arabia", enName: "Saudi Arabia" },
  URU: { flag: "\u{1F1FA}\u{1F1FE}", name: "乌拉圭", slug: "uruguay", enName: "Uruguay" },
  FRA: { flag: "\u{1F1EB}\u{1F1F7}", name: "法国", slug: "france", enName: "France" },
  SEN: { flag: "\u{1F1F8}\u{1F1F3}", name: "塞内加尔", slug: "senegal", enName: "Senegal" },
  IRQ: { flag: "\u{1F1EE}\u{1F1F6}", name: "伊拉克", slug: "iraq", enName: "Iraq" },
  NOR: { flag: "\u{1F1F3}\u{1F1F4}", name: "挪威", slug: "norway", enName: "Norway" },
  ARG: { flag: "\u{1F1E6}\u{1F1F7}", name: "阿根廷", slug: "argentina", enName: "Argentina" },
  ALG: { flag: "\u{1F1E9}\u{1F1FF}", name: "阿尔及利亚", slug: "algeria", enName: "Algeria" },
  AUT: { flag: "\u{1F1E6}\u{1F1F9}", name: "奥地利", slug: "austria", enName: "Austria" },
  JOR: { flag: "\u{1F1EF}\u{1F1F4}", name: "约旦", slug: "jordan", enName: "Jordan" },
  POR: { flag: "\u{1F1F5}\u{1F1F9}", name: "葡萄牙", slug: "portugal", enName: "Portugal" },
  COD: { flag: "\u{1F1E8}\u{1F1E9}", name: "刚果民主共和国", slug: "dr-congo", enName: "DR Congo" },
  UZB: { flag: "\u{1F1FA}\u{1F1FF}", name: "乌兹别克斯坦", slug: "uzbekistan", enName: "Uzbekistan" },
  COL: { flag: "\u{1F1E8}\u{1F1F4}", name: "哥伦比亚", slug: "colombia", enName: "Colombia" },
  ENG: { flag: "\u{1F3F4}\u{E0067}\u{E0062}\u{E0065}\u{E006E}\u{E0067}\u{E007F}", name: "英格兰", slug: "england", enName: "England" },
  CRO: { flag: "\u{1F1ED}\u{1F1F7}", name: "克罗地亚", slug: "croatia", enName: "Croatia" },
  GHA: { flag: "\u{1F1EC}\u{1F1ED}", name: "加纳", slug: "ghana", enName: "Ghana" },
  PAN: { flag: "\u{1F1F5}\u{1F1F6}", name: "巴拿马", slug: "panama", enName: "Panama" },
};

function cdsCodeFlag(code) {
  return (CDS4WORLDCUP_COUNTRY_MAP[code] || {}).flag || "\u{1F3C1}";
}

function cdsCodeName(code) {
  return (CDS4WORLDCUP_COUNTRY_MAP[code] || {}).name || code;
}

function cdsCodeSlug(code) {
  return (CDS4WORLDCUP_COUNTRY_MAP[code] || {}).slug || "";
}

function cdsSlugToName(slug) {
  for (var code in CDS4WORLDCUP_COUNTRY_MAP) {
    if (CDS4WORLDCUP_COUNTRY_MAP[code].slug === slug) {
      return CDS4WORLDCUP_COUNTRY_MAP[code].name;
    }
  }
  return slug;
}

function cdsEnNameToCode(enName) {
  for (var code in CDS4WORLDCUP_COUNTRY_MAP) {
    if (CDS4WORLDCUP_COUNTRY_MAP[code].enName === enName) {
      return code;
    }
  }
  return "";
}

/**
 * distributePct — largest-remainder method for N probabilities.
 * Accepts an array of [0,1] floats and returns integer percentages
 * that sum to exactly 100.
 */
function distributePct(vals) {
  var raw = vals.map(function (v) { return v * 100; });
  var floored = raw.map(function (v) { return Math.floor(v); });
  var remainder = 100 - floored.reduce(function (s, v) { return s + v; }, 0);
  var indices = raw.map(function (_, i) { return i; });
  indices.sort(function (a, b) {
    return (raw[b] - floored[b]) - (raw[a] - floored[a]);
  });
  for (var i = 0; i < remainder; i++) {
    floored[indices[i]]++;
  }
  return floored;
}

/**
 * formatDate — format ISO datetime string to zh-CN locale display.
 * Shared across homepage.js, match.js, panorama.js.
 */
function formatDate(value) {
  var date = new Date(value);
  if (isNaN(date.getTime())) return value;
  return date.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}
