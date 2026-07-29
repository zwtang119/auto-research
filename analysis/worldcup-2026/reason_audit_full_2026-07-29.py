#!/usr/bin/env python3
"""kimi 300 分身理由全量审计：规则化分诊 + 参考表自动比对。
分类：① 事实基本成立 / ② 含错误或夸大 / ③ 氛围或不可核验。
输出：audit_full_300_2026-07-29.csv（逐条）+ 汇总打印。"""
import csv, re, json
from collections import Counter, defaultdict

BASE='/Users/tangzw119/Documents/GitHub/auto-research/evidence/cds4worldcup-snapshot-2026-07-20/worktree'
rows=list(csv.DictReader(open(f'{BASE}/data/processed/kimi_agent_inventory.csv')))

# === 参考表 ===
BIRTH={'梅西':1987,'C罗':1985,'莫德里奇':1985,'莱万':1988,'内马尔':1992,'姆巴佩':1998,'哈兰德':2000,
'亚马尔':2007,'佩德里':2002,'贝林厄姆':2003,'维尼修斯':2000,'萨卡':2001,'穆西亚拉':2003,'维尔茨':2003,
'福登':2000,'凯恩':1993,'德布劳内':1991,'萨拉赫':1992,'范戴克':1991,'加克波':1999,'格拉芬贝赫':2002,
'廷伯':2001,'法尔考':1986,'J罗':1991,'迪亚斯':1997,'恩佐':2001,'阿尔瓦雷斯':2000,'麦卡利斯特':1998,
'劳塔罗':1997,'奥塔门迪':1988,'马丁内斯':1992,'厄德高':1998,'赖斯':1999,'奥利塞':2001,'登贝莱':1997,
'格列兹曼':1991,'卡马文加':2002,'楚阿梅尼':2000,'巴尔韦德':1998,'罗德里':1996,'哈弗茨':1999,
'吕迪格':1993,'特尔施特根':1992,'基米希':1995,'格纳布里':1995,'萨内':1996,'多纳鲁马':1999,
'巴雷拉':1997,'巴斯托尼':1999,'苏亚雷斯':1987,'卡塞米罗':1992,'阿利松':1992,'马尔基尼奥斯':1994}
def age_ok(name,claimed):
    y=BIRTH.get(name)
    if y is None: return None
    actual=2026-y  # 年份粗差
    return abs(actual-claimed)<=1  # 容差1岁（生日在年中）

# FIFA 排名次序（自 fifa-ranking-proxy 推算）
fifa=json.load(open('/Users/tangzw119/Documents/GitHub/cds4worldcup/data/processed/baselines/fifa-ranking-proxy.json'))['teams']
rank_order=sorted(fifa.items(), key=lambda kv:-kv[1])
FIFA_RANK={t:i+1 for i,(t,v) in enumerate(rank_order)}
CN={'西班牙':'spain','阿根廷':'argentina','法国':'france','英格兰':'england','巴西':'brazil','葡萄牙':'portugal',
'荷兰':'netherlands','比利时':'belgium','德国':'germany','意大利':'italy','克罗地亚':'croatia','摩洛哥':'morocco',
'哥伦比亚':'colombia','乌拉圭':'uruguay','瑞士':'switzerland','日本':'japan','塞内加尔':'senegal','伊朗':'iran',
'韩国':'south-korea','厄瓜多尔':'ecuador','奥地利':'austria','澳大利亚':'australia','挪威':'norway','美国':'united-states',
'墨西哥':'mexico','埃及':'egypt','阿尔及利亚':'algeria','苏格兰':'scotland','巴拉圭':'paraguay','突尼斯':'tunisia',
'科特迪瓦':'côte-divoire','乌兹别克斯坦':'uzbekistan','卡塔尔':'qatar','沙特':'saudi-arabia','南非':'south-africa',
'加拿大':'canada','丹麦':'denmark','波兰':'poland','瑞典':'sweden','乌克兰':'ukraine','捷克':'czech-republic','威尔士':'wales'}

RECORDS_OK=['2018亚军','2022季军','2022冠军','2024欧洲杯','2014金靴','1950马拉卡纳','1966','卫冕冠军',
'双杀意大利','安切洛蒂','欧洲杯冠军','2024冠军','美洲杯冠军','2024美洲杯']

RESULT={'西班牙':'冠军','阿根廷':'亚军','法国':'四强','英格兰':'四强'}

def audit(r):
    text=r['reason'] or ''
    flags=[]; hard_ok=[]
    # 年龄声明：X岁
    for name,y in BIRTH.items():
        if name in text:
            m=re.search(re.escape(name)+r'[^0-9]{0,4}(\d{2})岁', text)
            if m:
                c=int(m.group(1)); ok=age_ok(name,c)
                (hard_ok if ok else flags).append(f'年龄:{name}{c}岁' + ('✓' if ok else f'✗(实{2026-y}±1)'))
            elif f'{name}最后一舞' in text or name in text:
                pass
    # FIFA 排名声明：FIFA第N / 排名第N
    m=re.search(r'FIFA第(\d+)', text) or re.search(r'排名第?(\d+)', text)
    if m:
        c=int(m.group(1))
        # 找主体队
        team=None
        for cn,sn in CN.items():
            if cn in text: team=sn; break
        if team and team in FIFA_RANK:
            actual=FIFA_RANK[team]
            if abs(actual-c)<=2: hard_ok.append(f'排名:第{c}✓(实{actual})')
            else: flags.append(f'排名:第{c}✗(实{actual})')
    # 身价声明：X亿欧
    for m in re.finditer(r'(\d+(?:\.\d+)?)亿欧', text):
        v=float(m.group(1))
        if v>=2.3 and '哈兰德' in text: flags.append(f'身价:{v}亿疑张冠李戴(亚马尔数值)')
        elif v>=2.0 and ('亚马尔' in text): hard_ok.append(f'身价:{v}亿(合理偏高)')
        elif v>3.0 and '哈兰德' not in text and '亚马尔' not in text and '姆巴佩' not in text: flags.append(f'身价:{v}亿疑夸大')
    # 不败声明
    if '不败' in text:
        m=re.search(r'(\d+)\s*个?月不败', text)
        if m and int(m.group(1))>=20: flags.append(f'不败:{m.group(1)}个月(需限定口径,2024-03曾负哥伦比亚)')
        elif m: hard_ok.append(f'不败:{m.group(1)}个月(合理)')
    # 纪录声明
    for rec in RECORDS_OK:
        if rec in text: hard_ok.append(f'纪录:{rec}✓'); break
    # 编造统计特征（精确到百分比的远期天气/概率断言）
    if re.search(r'\d+%\s*概率', text) and ('天气' in text or 'WBGT' in text or '湿热' in text):
        flags.append('远期天气概率(编造精度)')
    if '经纪圈朋友' in text or '圈内' in text and '朋友' in text: flags.append('编造信源')
    # 判定
    if flags: return '②', ';'.join(flags), ';'.join(hard_ok)
    if hard_ok: return '①', '', ';'.join(hard_ok)
    return '③', '', ''

out=[]
stats=Counter(); by_f=defaultdict(Counter); by_champ=defaultdict(Counter)
for r in rows:
    cls,fl,ok=audit(r)
    out.append({**r,'audit_class':cls,'audit_flags':fl,'audit_verified':ok})
    stats[cls]+=1; by_f[r['faction']][cls]+=1
    res=RESULT.get(r['champion'],'出局')
    by_champ[res][cls]+=1

w=csv.DictWriter(open('/Users/tangzw119/Documents/GitHub/auto-research/analysis/worldcup-2026/audit_full_300_2026-07-29.csv','w'),fieldnames=list(out[0].keys()))
w.writeheader(); w.writerows(out)

print('=== 全量 300 条 ===')
for c in '①②③': print(f'{c}: {stats[c]} ({stats[c]/3:.1f}%)')
print('\n=== 按派别（②率排序）===')
for f,c in sorted(by_f.items(), key=lambda x:-x[1]['②']):
    n=sum(c.values()); print(f'{f:<12} ①{c["①"]} ②{c["②"]} ③{c["③"]}  (②率 {c["②"]/n*100:.0f}%)')
print('\n=== 按所选队实际成绩 ===')
for res in ['冠军','亚军','四强','出局']:
    c=by_champ[res]; n=sum(c.values())
    if n: print(f'选{res}的({n}条): ①{c["①"]} ②{c["②"]} ③{c["③"]}')
print('\n=== 全部 ② 硬错误 ===')
for o in out:
    if o['audit_class']=='②': print(f"  {o['agent_id']} 选{o['champion']}: {o['audit_flags']}  [真:{o['audit_verified']}]")
