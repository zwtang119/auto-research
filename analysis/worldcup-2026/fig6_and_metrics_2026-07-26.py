#!/usr/bin/env python3
"""图6：三线轨迹（市场西班牙/法国、CDS西班牙、kimi冻结线）+ 两个补充指标计算。
数据源：封存仓库 git 历史（只读）。输出：analysis/worldcup-2026/fig6-three-trajectories-2026-07-26.png"""
import subprocess, json, math, sys
from pathlib import Path
from datetime import date, datetime

REPO = '/Users/tangzw119/Documents/GitHub/cds4worldcup'
OUT = Path('/Users/tangzw119/Documents/GitHub/auto-research/analysis/worldcup-2026')

def git_show(spec):
    return subprocess.run(['git','-C',REPO,'show',spec],capture_output=True,text=True).stdout

def series(path, extractor):
    log = subprocess.run(['git','-C',REPO,'log','--reverse','--format=%h %aI','--',path],capture_output=True,text=True).stdout.strip().split('\n')
    pts = {}
    for line in log:
        h, dt = line.split()
        try: d = json.loads(git_show(f'{h}:{path}'))
        except Exception: continue
        v = extractor(d)
        if v is not None: pts[dt[:10]] = v
    return pts

# 市场：西班牙/法国逐日
mkt_es = series('data/processed/market_public_snapshot.json', lambda d: d['teams'].get('spain',{}).get('probability'))
mkt_fr = series('data/processed/market_public_snapshot.json', lambda d: d['teams'].get('france',{}).get('probability'))
# CDS：西班牙逐日
cds_es = series('data/processed/cds_championship.json', lambda d: {t['team']:t['championship_prob'] for t in d['teams']}.get('Spain'))
cds_es = {k: v*100 for k,v in cds_es.items()}

# 只画赛前→决赛（7-19），赛后 100% 段不进入叙事
CUTOFF = '2026-07-19'
def cut(d): return {k:v for k,v in d.items() if k <= CUTOFF}
mkt_es, mkt_fr, cds_es = cut(mkt_es), cut(mkt_fr), cut(cds_es)

all_days = sorted(set(mkt_es) | set(cds_es))
xs = [datetime.strptime(d,'%Y-%m-%d').date() for d in all_days]
def align(s): return [s.get(d) for d in all_days]

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

setup_plot()
fig, ax = plt.subplots(figsize=(11.5, 6.2))

ax.plot(xs, align(mkt_es), color='#1f6fb2', lw=2.2, label='市场：西班牙（Polymarket 日度）')
ax.plot(xs, align(mkt_fr), color='#c94f42', lw=2.0, label='市场：法国')
ax.plot(xs, align(cds_es), color='#8a8a8a', lw=1.8, ls='-.', label='CDS 引擎：西班牙（每日重生成，先验平坦）')
ax.axhline(23.82, color='#2e8b57', lw=2.2, ls='--', label='kimi 冻结信号：西班牙 23.82%（6-13 起未变）')

D = lambda s: datetime.strptime(s,'%Y-%m-%d').date()
# 佛得角之夜
ax.axvline(D('2026-06-19'), color='#555', lw=1, ls=':')
ax.annotate('6-19 西班牙 0-0 佛得角\n市场开始恐慌', xy=(D('2026-06-19'), 30), fontsize=9, ha='left', xytext=(D('2026-06-20'), 33))
# 法国时代
ax.axvspan(D('2026-06-21'), D('2026-07-14'), color='#c94f42', alpha=0.08)
ax.text(D('2026-06-27'), 42, '市场的"法国时代"：6-21 → 7-14 法国为头号热门', fontsize=10, color='#a03d32', ha='center')
ax.annotate('7-14 半决赛日：法国 39.0%\n市场对两场半决赛的热门判断全错', xy=(D('2026-07-14'), 39.0), xytext=(D('2026-06-24'), 48), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='#a03d32'))
# 谷底
ax.annotate('7-01 谷底：西班牙 10.05%\n（冻结信号仍 23.82%）', xy=(D('2026-07-01'), 10.05), xytext=(D('2026-07-03'), 5.5), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='#1f6fb2'))
# 决赛
ax.axvline(D('2026-07-19'), color='#555', lw=1, ls=':')
ax.text(D('2026-07-19'), 62, '7-19 决赛\n西班牙 1-0 阿根廷', fontsize=9, ha='right')

ax.set_ylim(0, 65)
ax.set_ylabel('夺冠概率（%）')
ax.set_title('谁先知道西班牙会赢？——冻结信号 vs 市场 vs CDS 引擎（2026-06-12 → 07-19）', fontsize=13)
ax.legend(loc='upper left', fontsize=9)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax.grid(alpha=0.25)
fig.tight_layout()
out = OUT / 'fig6-three-trajectories-2026-07-26.png'
fig.savefig(out, dpi=200, bbox_inches='tight')
print('saved:', out)

# ===== 补充指标 1：时间积分 log score（市场每日 −ln p_spain 均值 vs kimi 常数） =====
vals = [v/100 for v in mkt_es.values()]
mkt_tls = sum(-math.log(p) for p in vals)/len(vals)
kimi_tls = -math.log(0.2382)
print(f'时间积分 log score（6-12→7-19，n={len(vals)} 个日度快照）：市场 {mkt_tls:.3f} vs kimi 常数 {kimi_tls:.3f}')

# ===== 补充指标 2：同池多项 Brier（kimi 21 队池，西班牙=1） =====
kimi = json.loads(git_show('ef30658:data/processed/kimi_baseline_signals_matrix.csv')) if False else None
# kimi 信号从 homepage.json 的 public_model_crowd 取（冻结版 0ff58a7）
hp = json.loads(git_show('0ff58a7:site/data/homepage.json'))
crowd = {t['team_slug']: t['probability']/100 for t in hp['public_signal_snapshots']['public_model_crowd']['top_teams']}
# 需要全 21 队：从 kimi_baseline_signals_matrix.csv
import csv, io
mat = git_show('0ff58a7:data/processed/kimi_baseline_signals_matrix.csv')
rows = list(csv.DictReader(io.StringIO(mat)))
k21 = {}
for r in rows:
    slug = r.get('team_slug') or r.get('slug') or r.get('team','').lower().replace(' ','-')
    for cand in ('championship_prob','kimi_championship_prob','prob','probability'):
        if cand in r and r[cand]:
            try: k21[slug] = float(r[cand]); break
            except: pass
print('kimi 矩阵队数:', len(k21), '样例:', list(k21.items())[:3])
EOF_MARKER = None
