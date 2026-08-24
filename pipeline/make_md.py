import json,os,datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d=json.load(open('dash_data.json',encoding='utf-8'))
TRK=['AP','LDL','PMN','SS','SPL']; BN={'AP':'애니포트','LDL':'엘디엘마운트','PMN':'포미니','SS':'신성전기','SPL':'쏘플링'}
allk=[p['k'] for p in d['periods']]; lump=[k for k in allk if '-' not in k][:3]
def csum(b,ks): return sum(c['p'][k][b][1] for c in d['channels'] for k in ks if k in c['p'])
bs=d['bstock_by_snap'][d['latest_snap']]
latest=d['latest_snap']; periods_l=[p['l'] for p in d['periods']]
short=[m for m in d['models'] if m['avg']>0 and m['stock_s'].get(latest,0)<=m['avg']]
def deaddays(m): return 9e9 if m['avg']<=0 else m['stock']/(m['avg']/30)
dead90=[m for m in d['models'] if m['stock']>0 and deaddays(m)>90]
deadzero=[m for m in d['models'] if m['stock']>0 and m['avg']<=0]
# 브랜드 표
rows=""
for b in TRK:
    rows+=f"| {BN[b]} | {csum(b,lump):,} | {csum(b,allk):,} | {bs[b][2]:,} | {bs[b][0]} |\n"
chan=', '.join(c['name'] for c in d['channels'])
closed = '진행 중(일별)' if any('-' in k for k in allk) else '마감(월누계)'
curm = ([k for k in allk if '-' in k][0].split('-')[0]+'월') if any('-' in k for k in allk) else '없음'
md=f"""# KAID HUB — 데이터 현황 (자동 생성)

> 생성: {datetime.date.today().isoformat()} · 재고 기준: {latest} · **이 파일은 파이프라인이 매일 자동 갱신합니다.**
> ※ 상세 설계·규칙 문서는 별도(수기) 정리본 참고. 이 파일은 "현재 수치" 스냅샷.

## 현재 기간 상태
- 반영 기간: {' · '.join(periods_l)}
- 현재 진행월: {curm} ({closed}) — 다음 달 데이터가 들어오면 이 달은 자동으로 월누계(합계)로 접힘
- 재고 스냅샷: {len(d['snaps'])}개 (최신 {latest})

## 브랜드별 요약
| 브랜드 | 매출(완료월 3개월) | 매출(전체) | 재고총액({latest[5:]}) | 재고품목 |
|---|--:|--:|--:|--:|
{rows}
- 채널 {len(d['channels'])}개 · 모델 {len(d['models'])}개

## 재고 경보
- **부족(현재고 ≤ 월평균): {len(short)}건** (그중 품절/초과판매 {len([m for m in short if m['stock_s'].get(latest,0)<=0])}건)
- **악성재고(재고 있는데 90일↑ 소진): {len(dead90)}건** (그중 판매 0: {len(deadzero)}건)

## 채널 목록 ({len(d['channels'])})
{chan}

## 대시보드
- 게시(직원 공유): https://kaid0925.github.io/ld-dashboard/
- 탭: 개요 · 채널별 매출 · 모델별 판매수량(매출처 드릴다운) · 재고현황 · 적정재고 분석 · 악성재고
"""
open('KAID_HUB_현황.md','w',encoding='utf-8').write(md)
print('생성 완료: KAID_HUB_현황.md ('+str(len(md))+'자) · 진행월',curm,closed)
