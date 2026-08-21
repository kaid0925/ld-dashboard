import json,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BNAME={'AP':'애니포트','LDL':'엘디엘마운트','PMN':'포미니','SS':'신성전기','SPL':'쏘플링'}
d=json.load(open('dash_data.json',encoding='utf-8'))
snap=d['latest_snap']; snapL=[s['l'] for s in d['snaps'] if s['k']==snap][0]
def stk(m): return m['stock_s'].get(snap,m['stock'])
def days(m):
    st=stk(m)
    if st<=0: return 0.0
    dv=m['avg']/30
    return round(st/dv,1) if dv>0 else 9999
rows=[m for m in d['models'] if m['avg']>0 and stk(m)<=m['avg']]  # 부족
rows.sort(key=lambda m:(days(m), -m['avg']))
soldout=[m for m in rows if stk(m)<=0]
warn=[m for m in d['models'] if m['avg']>0 and m['avg']<stk(m)<=m['avg']*2]
print(f"# 📦 KAID HUB 재고 알림 — 재고기준 {snapL}")
print(f"부족 {len(rows)}건 (그중 품절/초과판매 {len(soldout)}건) · 주의 {len(warn)}건\n")
print("## ⚠️ 급한 순 TOP 15 (예상보유일↑)")
print("| 브랜드 | 모델 | 상품명 | 현재고 | 월평균 | 보유일 | 발주필요 |")
print("|---|---|---|--:|--:|--:|--:|")
for m in rows[:15]:
    st=stk(m); adq=round(m['avg']*2); order=max(0,adq-st); dd='품절' if st<=0 else f"{days(m)}일"
    nm=(m['name'] or '')[:26]
    print(f"| {BNAME[m['brand']]} | {m['model'] or '-'} | {nm} | {st:,} | {m['avg']} | {dd} | {order:,} |")
# 브랜드별 발주 필요 SKU 수
from collections import Counter
c=Counter(m['brand'] for m in rows)
print("\n## 브랜드별 부족 SKU")
print(" · ".join(f"{BNAME[b]} {c[b]}건" for b in ['AP','LDL','PMN','SS','SPL'] if c[b]))
