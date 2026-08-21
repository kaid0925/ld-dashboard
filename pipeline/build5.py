import json,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
data=open('dash_data.json',encoding='utf-8').read()
chartjs=open('chartjs.txt',encoding='utf-8').read()
css=open('orig_css.txt',encoding='utf-8').read()
HTML = r'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LD 온라인 채널 대시보드</title>
<style>__CSS__
.two-brand th.grp{text-align:center;border-left:1px solid var(--border2);}
td.bl,th.bl{border-left:1px solid var(--border2);}
.legend-row{display:flex;align-items:center;gap:7px;padding:4px 0;font-size:11px;}
.legend-dot{width:9px;height:9px;border-radius:2px;flex-shrink:0;}
.neg{color:var(--red);font-weight:700;}
thead th.sortable::after{content:" ⇅";color:var(--border2);font-size:9px;}
thead th.sortable.asc::after{content:" ▲";color:var(--blue);}
thead th.sortable.desc::after{content:" ▼";color:var(--blue);}
</style></head><body>
<header>
<div class="logo"><div class="logo-mark">LD</div>
<div><div class="logo-text">온라인 채널 대시보드</div>
<div class="logo-sub">애니포트 · 엘디엘마운트 · 포미니 · 신성전기 · 쏘플링 | 온라인 채널 전용</div></div></div>
<div style="display:flex;align-items:center;gap:14px;">
<div class="status-badge"><div class="status-dot"></div>업데이트 완료</div>
<div style="font-size:11px;color:var(--text3);">매출 5~8월 / 재고 시점별</div></div>
</header>
<div class="tabs">
<button class="tab-btn active" onclick="switchTab('ov',this)">📊 개요</button>
<button class="tab-btn" onclick="switchTab('ch',this)">💰 채널별 매출</button>
<button class="tab-btn" onclick="switchTab('md',this)">📦 모델별 판매수량</button>
<button class="tab-btn" onclick="switchTab('inv',this)">🏭 재고현황</button>
<button class="tab-btn" onclick="switchTab('adq',this)">🎯 적정재고 분석</button>
</div>

<div id="tab-ov" class="tab-panel active"><div class="container">
<div class="kpi-grid" id="ov-kpi"></div>
<div class="grid2">
<div class="card"><div class="card-header"><div class="card-title">채널별 매출 현황</div><span class="cbadge cb-blue">브랜드별 누적 · 전체기간</span></div>
<div class="card-body"><div style="height:270px;"><canvas id="ov-ch"></canvas></div></div></div>
<div class="card"><div class="card-header"><div class="card-title">기간별 매출 추이</div><span class="cbadge cb-teal">5·6·7월+8월</span></div>
<div class="card-body"><div style="height:270px;"><canvas id="ov-tr"></canvas></div></div></div>
</div>
<div class="grid2">
<div class="card"><div class="card-header"><div class="card-title">TOP 10 판매 모델</div><span class="cbadge cb-teal">전체 수량</span></div>
<div class="card-body" id="ov-top" style="max-height:340px;overflow-y:auto;"></div></div>
<div class="card"><div class="card-header"><div class="card-title">⚠️ 재고 부족 알림</div><span class="cbadge cb-red" id="ov-low-b">0건</span></div>
<div class="card-body" id="ov-low" style="max-height:340px;overflow-y:auto;"></div></div>
</div>
</div></div>

<div id="tab-ch" class="tab-panel"><div class="container">
<div class="date-select-bar">
<label>📅 기간</label><select class="date-dropdown" id="ch-period"></select>
<label style="margin-left:8px;">기준</label>
<div class="view-toggle" id="ch-view"><button class="active" data-v="amt">매출액</button><button data-v="qty">수량</button><button data-v="profit">이익</button></div></div>
<div class="kpi-grid" id="ch-kpi"></div>
<div class="grid2">
<div class="card"><div class="card-header"><div class="card-title">채널별 비중 (애니포트)</div><span class="cbadge cb-blue" id="ch-donut-b"></span></div>
<div class="card-body"><div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:center;">
<div style="height:220px;"><canvas id="ch-donut"></canvas></div>
<div id="ch-legend" style="overflow-y:auto;max-height:220px;"></div></div></div></div>
<div class="card"><div class="card-header"><div class="card-title">채널별 순위 (자사 브랜드 합계)</div><span class="cbadge cb-orange" id="ch-bar-b"></span></div>
<div class="card-body"><div style="height:260px;"><canvas id="ch-bar"></canvas></div></div></div>
</div>
<div class="card"><div class="card-header"><div class="card-title">채널 × 브랜드 × 기간 상세</div><span class="cbadge cb-purple" id="ch-tbl-b"></span></div>
<div class="card-body"><div class="tbl-wrap" style="max-height:640px;"><table class="two-brand" id="ch-tbl"></table></div>
<div style="font-size:11px;color:var(--text3);margin-top:8px;">* 5~7월 월누계 / 8월 일별. 기타 = 자사 4개 브랜드 외 판매액. 텐바이텐은 채널만 표기.</div></div></div>
</div></div>

<div id="tab-md" class="tab-panel"><div class="container">
<div class="date-select-bar"><label>📅 기간</label><select class="date-dropdown" id="md-period"></select></div>
<div class="card"><div class="card-header"><div class="card-title">모델별 매출수량 (온라인 채널 합산)</div><span class="cbadge cb-teal" id="md-cnt">0</span></div>
<div class="card-body">
<div class="filter-row" id="md-brand"><button class="flt-btn active" data-v="ALL">전체</button><button class="flt-btn" data-v="AP">애니포트</button><button class="flt-btn" data-v="LDL">엘디엘마운트</button><button class="flt-btn" data-v="PMN">포미니</button><button class="flt-btn" data-v="SS">신성전기</button><button class="flt-btn" data-v="SPL">쏘플링</button></div>
<input class="search-input" id="md-search" placeholder="모델·상품명 검색...">
<div class="tbl-wrap" style="max-height:600px;"><table id="md-tbl"></table></div>
<div style="font-size:11px;color:var(--text3);margin-top:8px;">* 월평균 = 완료월(5~7월) 합계 ÷ 3 · 현재고는 08-04 시점재고 · 헤더 클릭 정렬</div>
</div></div>
</div></div>

<div id="tab-inv" class="tab-panel"><div class="container">
<div class="date-select-bar"><label>📅 시점(재고 스냅샷)</label><select class="date-dropdown" id="inv-snap"></select></div>
<div class="kpi-grid" id="inv-kpi"></div>
<div class="card" style="margin-bottom:16px;"><div class="card-header"><div class="card-title">브랜드별 재고총액 추이</div><span class="cbadge cb-teal">시점별 추이</span></div><div class="card-body"><div style="height:230px;"><canvas id="inv-trend"></canvas></div></div></div>
<div class="card"><div class="card-header"><div class="card-title">시점 재고 현황</div><span class="cbadge cb-blue" id="inv-cnt">0</span><span style="font-size:11px;color:var(--text3);" id="inv-snaplbl">최신 시점 기준</span></div>
<div class="card-body">
<div class="filter-row" id="inv-brand"><button class="flt-btn active" data-v="AP">애니포트</button><button class="flt-btn" data-v="LDL">엘디엘마운트</button><button class="flt-btn" data-v="PMN">포미니</button><button class="flt-btn" data-v="SS">신성전기</button><button class="flt-btn" data-v="SPL">쏘플링</button></div>
<input class="search-input" id="inv-search" placeholder="상품명 검색...">
<div class="tbl-wrap" style="max-height:580px;"><table id="inv-tbl"></table></div>
<div style="font-size:11px;color:var(--text3);margin-top:8px;">* 재고수량 마이너스 = 초과판매(백오더). 헤더 클릭 정렬.</div>
</div></div>
</div></div>

<div id="tab-adq" class="tab-panel"><div class="container">
<div class="kpi-grid" id="adq-kpi"></div>
<div class="card"><div class="card-header"><div class="card-title">적정재고 · 부족재고 예상보유일</div><span class="cbadge cb-red" id="adq-cnt">0</span></div>
<div class="card-body">
<div class="date-select-bar" style="margin-bottom:12px;"><label>📅 재고 시점</label><select class="date-dropdown" id="adq-snap"></select></div>
<div style="font-size:11px;color:var(--text2);background:var(--bg3);padding:10px 13px;border-radius:8px;margin-bottom:12px;line-height:1.7;">
<b>적정재고</b> = 월평균 판매량 × 2 &nbsp;|&nbsp; <b>예상보유일</b> = 현재고 ÷ 일평균판매(월평균÷30) &nbsp;|&nbsp; <b>부족</b> = 현재고 ≤ 월평균
<br>상태: <span class="pill p-red">품절</span> 재고 0 이하 · <span class="pill p-orange">부족</span> ≤ 월평균 · <span class="pill p-yellow">주의</span> ≤ 적정재고 · <span class="pill p-green">적정</span> 적정재고 초과 &nbsp;·&nbsp; <b>컬럼 헤더 클릭 시 정렬</b>
</div>
<div class="filter-row" id="adq-brand"><button class="flt-btn active" data-v="ALL">전체</button><button class="flt-btn" data-v="AP">애니포트</button><button class="flt-btn" data-v="LDL">엘디엘마운트</button><button class="flt-btn" data-v="PMN">포미니</button><button class="flt-btn" data-v="SS">신성전기</button><button class="flt-btn" data-v="SPL">쏘플링</button></div>
<div class="filter-row" id="adq-filt"><button class="flt-btn active" data-v="shortwarn">부족+주의</button><button class="flt-btn" data-v="short">부족만</button><button class="flt-btn" data-v="all">전체</button></div>
<input class="search-input" id="adq-search" placeholder="모델·상품명 검색...">
<div class="tbl-wrap" style="max-height:580px;"><table id="adq-tbl"></table></div>
</div></div>
</div></div>

<script>__CHARTJS__</script>
<script>
const D=__DATA__;
const TRK=['AP','LDL','PMN','SS','SPL'];
const AUG=D.day_keys;
const f=n=>Math.round(n).toLocaleString('ko-KR');
const BC={AP:'#3b6ef8',LDL:'#0bbfa0',PMN:'#7c3aed',SS:'#f46b1b',SPL:'#ec4899',ETC:'#c0c7d4'};
const BNAME={AP:'애니포트',LDL:'엘디엘마운트',PMN:'포미니',SS:'신성전기',SPL:'쏘플링',ETC:'기타'};
const PILL={AP:'p-blue',LDL:'p-teal',PMN:'p-purple',SS:'p-orange',SPL:'p-pink'};
const ICO={AP:'blue',LDL:'teal',PMN:'purple',SS:'orange',SPL:'pink'};
const IDX={qty:0,amt:1,profit:2};
let charts={};
function switchTab(id,btn){document.querySelectorAll('.tab-panel').forEach(e=>e.classList.remove('active'));document.getElementById('tab-'+id).classList.add('active');document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active');}
function seg(w,cb){const el=document.getElementById(w);el.querySelectorAll('button').forEach(b=>b.onclick=()=>{el.querySelectorAll('button').forEach(x=>x.classList.remove('active'));b.classList.add('active');cb(b.dataset.v);});}
function esc(s){return(s||'').replace(/"/g,'&quot;');}
function mkChart(id,type,data,opts){const c=document.getElementById(id);if(charts[id])charts[id].destroy();charts[id]=new Chart(c,{type,data,options:Object.assign({maintainAspectRatio:false,responsive:true},opts)});}
// period helpers
const ALLK=D.periods.map(p=>p.k);
function expandKey(k){ if(k=='8')return AUG.slice(); if(k=='ALL')return ALLK.slice(); return [k]; }
function cval(ch,k,brand,metric){let s=0;expandKey(k).forEach(pk=>{s+=ch.p[pk][brand][IDX[metric]];});return s;}
function mval(m,k){let s=0;expandKey(k).forEach(pk=>{s+=(m.p[pk]||0);});return s;}
function colsFor(sel){
 if(sel=='month')return {cols:[{k:'5',l:'5월'},{k:'6',l:'6월'},{k:'7',l:'7월'},{k:'8',l:'8월'}]};
 if(sel=='augday')return {cols:AUG.map(dk=>({k:dk,l:'8/'+(+dk.split('-')[1])})).concat([{k:'8',l:'8월계'}])};
 if(sel=='all')return {cols:[{k:'ALL',l:'전체'}]};
 const lbl={'5':'5월','6':'6월','7':'7월','8':'8월누계'}[sel]||('8/'+(+String(sel).split('-')[1]));
 return {cols:[{k:sel,l:lbl}]};
}
function scopeKeys(sel){ if(sel=='month'||sel=='all')return ALLK; if(sel=='augday'||sel=='8')return AUG; return [sel]; }
function periodOptions(){let h='<option value="month">전체 (월별)</option><option value="augday">8월 (일별)</option><option value="all">전체 합계</option><option disabled>──</option><option value="5">5월</option><option value="6">6월</option><option value="7">7월</option><option value="8">8월 누계</option>';AUG.forEach(dk=>h+=`<option value="${dk}">8/${+dk.split('-')[1]}</option>`);return h;}
function sumScope(sel,brand,metric){const ks=scopeKeys(sel);let s=0;D.channels.forEach(c=>ks.forEach(k=>s+=c.p[k][brand][IDX[metric]]));return s;}
function daysLeftV(avg,stock){if(stock<=0)return 0;const dv=avg/30;return dv>0?Math.round(stock/dv*10)/10:9999;}
function daysLeft(m){return daysLeftV(m.avg,m.stock);}
const SNAPS=D.snaps;const LATEST=D.latest_snap;
function snapOptions(){return SNAPS.map(s=>`<option value="${s.k}"${s.k==LATEST?' selected':''}>${s.l}</option>`).join('');}
function stockAt(m,snap){return (m.stock_s&&m.stock_s[snap]!=null)?m.stock_s[snap]:m.stock;}
function lowStock(){return D.models.filter(m=>m.stock<=m.avg&&m.avg>0).sort((a,b)=>daysLeft(a)-daysLeft(b));}

// OVERVIEW (전체기간 기준)
function renderOv(){
 const bs=D.bstock_by_snap[D.latest_snap];const low=lowStock();
 const active=D.channels.filter(c=>ALLK.some(k=>TRK.some(b=>c.p[k][b][1]>0))).length;
 const K=[
  ['blue','🔵','애니포트 매출',f(sumScope('all','AP','amt')),'수량 '+f(sumScope('all','AP','qty'))+'개'],
  ['teal','🟢','엘디엘마운트 매출',f(sumScope('all','LDL','amt')),'수량 '+f(sumScope('all','LDL','qty'))+'개'],
  ['purple','🟣','포미니 매출',f(sumScope('all','PMN','amt')),'수량 '+f(sumScope('all','PMN','qty'))+'개'],
  ['orange','🟠','신성전기 매출',f(sumScope('all','SS','amt')),'수량 '+f(sumScope('all','SS','qty'))+'개'],
  ['pink','🧵','쏘플링 매출',f(sumScope('all','SPL','amt')),'수량 '+f(sumScope('all','SPL','qty'))+'개'],
  ['blue','🏭','애니포트 재고',f(bs.AP[2]),f(bs.AP[1])+'개'],
  ['teal','🏭','엘디엘 재고',f(bs.LDL[2]),f(bs.LDL[1])+'개'],
  ['orange','🏬','활성 채널',active+' / '+D.channels.length,'매출 발생'],
  ['red','⚠️','부족재고',low.length+'건','현재고 ≤ 월평균'],
 ];
 document.getElementById('ov-kpi').innerHTML=K.map(k=>`<div class="kpi"><div class="kpi-icon ${k[0]}">${k[1]}</div><div class="kpi-label">${k[2]}</div><div class="kpi-val ${k[0]}">${k[3]}</div><div class="kpi-sub">${k[4]}</div></div>`).join('');
 const rows=D.channels.map(c=>({n:c.name,vals:TRK.map(b=>cval(c,'ALL',b,'amt'))})).filter(r=>r.vals.some(v=>v>0)).sort((a,b)=>b.vals.reduce((s,v)=>s+v,0)-a.vals.reduce((s,v)=>s+v,0));
 mkChart('ov-ch','bar',{labels:rows.map(r=>r.n),datasets:TRK.map((b,i)=>({label:BNAME[b],data:rows.map(r=>r.vals[i]),backgroundColor:BC[b]}))},{indexAxis:'y',scales:{x:{stacked:true,ticks:{callback:v=>(v/1e6).toFixed(0)+'M'}},y:{stacked:true}},plugins:{legend:{position:'bottom'},tooltip:{callbacks:{label:c=>c.dataset.label+': '+f(c.raw)+'원'}}}});
 mkChart('ov-tr','line',{labels:D.periods.map(p=>p.l),datasets:TRK.map(b=>({label:BNAME[b],data:ALLK.map(k=>D.channels.reduce((s,c)=>s+c.p[k][b][1],0)),borderColor:BC[b],backgroundColor:'transparent',tension:.3}))},{plugins:{legend:{position:'bottom'},tooltip:{callbacks:{label:c=>c.dataset.label+': '+f(c.raw)+'원'}}},scales:{y:{ticks:{callback:v=>(v/1e6).toFixed(0)+'M'}}}});
 const top=D.models.slice(0,10);const mx=top[0]?top[0].total:1;
 document.getElementById('ov-top').innerHTML=top.map((m,i)=>`<div class="rank-item"><div class="rank-num">${i+1}</div><span class="pill ${PILL[m.brand]}">${m.brand}</span><div class="rank-name" title="${esc(m.name)}">${m.model||m.name}</div><div class="rank-bar-wrap"><div class="rank-bar" style="width:${m.total/mx*100}%;background:${BC[m.brand]}"></div></div><div class="rank-val">${f(m.total)}</div></div>`).join('');
 document.getElementById('ov-low-b').textContent=low.length+'건';
 document.getElementById('ov-low').innerHTML=low.slice(0,20).map(m=>{const d=daysLeft(m);const crit=m.stock<=0;return `<div class="alert-item ${crit?'crit':'warn'}"><div><div class="alert-name">${m.model||m.name}</div><div class="alert-meta">${BNAME[m.brand]} · 월평균 ${m.avg} · 적정 ${Math.round(m.avg*2)}</div></div><div style="text-align:right"><div class="alert-stock" style="color:${crit?'var(--red)':'var(--yellow)'}">${f(m.stock)}</div><div class="alert-meta">${d==0?'품절':d+'일'}</div></div></div>`;}).join('')||'<div style="color:var(--text3);padding:12px;">부족 품목 없음</div>';
}

// CHANNEL
let chSel='month',chView='amt';
function renderCh(){document.getElementById('ch-period').innerHTML=periodOptions();document.getElementById('ch-period').value='month';document.getElementById('ch-period').onchange=e=>{chSel=e.target.value;chAll();};seg('ch-view',v=>{chView=v;chAll();});chAll();}
function chAll(){
 const unit=chView=='amt'?'매출액':chView=='qty'?'수량':'이익';const suf=chView=='qty'?'개':'원';
 ['ch-donut-b','ch-bar-b','ch-tbl-b'].forEach(id=>document.getElementById(id).textContent=unit);
 const K=TRK.map(b=>[ICO[b],BNAME[b]+' '+unit,f(sumScope(chSel,b,chView))+suf]);
 let etc=0;scopeKeys(chSel).forEach(k=>D.channels.forEach(c=>etc+=c.p[k].ETC[IDX[chView]]));K.push(['','기타 '+unit,f(etc)+suf]);
 document.getElementById('ch-kpi').innerHTML=K.map(k=>`<div class="kpi"><div class="kpi-icon ${k[0]||'blue'}">📊</div><div class="kpi-label">${k[1]}</div><div class="kpi-val ${k[0]}">${k[2]}</div></div>`).join('');
 const dd=D.channels.map(c=>({n:c.name,v:cval(c,scopeAgg(chSel),'AP',chView)})).map((r,i)=>r).filter(r=>r.v>0).sort((a,b)=>b.v-a.v);
 const pal=['#3b6ef8','#0bbfa0','#f46b1b','#7c3aed','#e53855','#f59e0b','#10b981','#ec4899','#6b8cff','#14b8a6','#fb923c','#a78bfa'];
 mkChart('ch-donut','doughnut',{labels:dd.map(r=>r.n),datasets:[{data:dd.map(r=>r.v),backgroundColor:dd.map((_,i)=>pal[i%pal.length]),borderWidth:1,borderColor:'#fff'}]},{cutout:'62%',plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.label+': '+f(c.raw)+suf}}}});
 const tot=dd.reduce((s,r)=>s+r.v,0)||1;
 document.getElementById('ch-legend').innerHTML=dd.slice(0,12).map((r,i)=>`<div class="legend-row"><div class="legend-dot" style="background:${pal[i%pal.length]}"></div><div style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${r.n}</div><b>${(r.v/tot*100).toFixed(1)}%</b></div>`).join('');
 const rows=D.channels.map(c=>({n:c.name,v:TRK.reduce((s,b)=>s+cval(c,scopeAgg(chSel),b,chView),0)})).filter(r=>r.v>0).sort((a,b)=>b.v-a.v);
 mkChart('ch-bar','bar',{labels:rows.map(r=>r.n),datasets:[{data:rows.map(r=>r.v),backgroundColor:'#6b8cff',borderRadius:4}]},{indexAxis:'y',plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>f(c.raw)+suf}}}});
 chTable();
}
function scopeAgg(sel){ // single aggregate key for charts
 if(sel=='month'||sel=='all')return 'ALL'; if(sel=='augday')return '8'; return sel;
}
function chTable(){
 const cf=colsFor(chSel).cols;
 let h='<thead><tr><th rowspan="2">채널</th>';
 h+=`<th class="grp right" colspan="${cf.length+1}" style="color:${BC.AP}">애니포트</th>`;
 h+=`<th class="grp right" colspan="${cf.length+1}" style="color:${BC.LDL}">엘디엘마운트</th>`;
 h+=`<th class="grp right" rowspan="2" style="color:${BC.PMN}">포미니</th><th class="grp right" rowspan="2" style="color:${BC.SS}">신성전기</th><th class="grp right" rowspan="2" style="color:${BC.SPL}">쏘플링</th><th class="grp right" rowspan="2">기타</th></tr><tr>`;
 cf.forEach((c,i)=>h+=`<th class="right ${i==0?'bl':''}">${c.l}</th>`);h+='<th class="right">계</th>';
 cf.forEach((c,i)=>h+=`<th class="right ${i==0?'bl':''}">${c.l}</th>`);h+='<th class="right">계</th>';
 h+='</tr></thead><tbody>';
 const agg=scopeAgg(chSel);
 D.channels.forEach(c=>{
  h+=`<tr><td>${c.name}</td>`;
  cf.forEach((col,i)=>h+=`<td class="right ${i==0?'bl':''}">${f(cval(c,col.k,'AP',chView))}</td>`);
  h+=`<td class="right"><b>${f(cval(c,agg,'AP',chView))}</b></td>`;
  cf.forEach((col,i)=>h+=`<td class="right ${i==0?'bl':''}">${f(cval(c,col.k,'LDL',chView))}</td>`);
  h+=`<td class="right"><b>${f(cval(c,agg,'LDL',chView))}</b></td>`;
  h+=`<td class="right" style="color:${BC.PMN}">${f(cval(c,agg,'PMN',chView))}</td><td class="right" style="color:${BC.SS}">${f(cval(c,agg,'SS',chView))}</td><td class="right" style="color:${BC.SPL}">${f(cval(c,agg,'SPL',chView))}</td><td class="right" style="color:var(--text3)">${f(cval(c,agg,'ETC',chView))}</td></tr>`;});
 // totals
 h+='</tbody><tfoot><tr><td>합계</td>';
 const tot=(k,b)=>D.channels.reduce((s,c)=>s+cval(c,k,b,chView),0);
 cf.forEach((col,i)=>h+=`<td class="right ${i==0?'bl':''}">${f(tot(col.k,'AP'))}</td>`);h+=`<td class="right">${f(tot(agg,'AP'))}</td>`;
 cf.forEach((col,i)=>h+=`<td class="right ${i==0?'bl':''}">${f(tot(col.k,'LDL'))}</td>`);h+=`<td class="right">${f(tot(agg,'LDL'))}</td>`;
 h+=`<td class="right">${f(tot(agg,'PMN'))}</td><td class="right">${f(tot(agg,'SS'))}</td><td class="right">${f(tot(agg,'SPL'))}</td><td class="right">${f(tot(agg,'ETC'))}</td></tr></tfoot>`;
 document.getElementById('ch-tbl').innerHTML=h;
}

// MODELS
let mdSel='month',mdB='ALL',mdQ='',mdSort={c:'total',d:-1};
function renderMd(){document.getElementById('md-period').innerHTML=periodOptions();document.getElementById('md-period').value='month';document.getElementById('md-period').onchange=e=>{mdSel=e.target.value;mdTbl();};seg('md-brand',v=>{mdB=v;mdTbl();});document.getElementById('md-search').oninput=e=>{mdQ=e.target.value.trim();mdTbl();};mdTbl();}
function mdTbl(){
 const cf=colsFor(mdSel).cols;
 let rows=D.models.filter(m=>(mdB=='ALL'||m.brand==mdB)&&(mdQ==''||(m.name+m.model).toLowerCase().includes(mdQ.toLowerCase())));
 const gv=(m,c)=>c=='total'?m.total:c=='avg'?m.avg:c=='stock'?m.stock:mval(m,c);
 rows.sort((a,b)=>{const x=gv(a,mdSort.c),y=gv(b,mdSort.c);return (x<y?-1:x>y?1:0)*mdSort.d;});
 let h='<thead><tr><th>브랜드</th><th>모델</th><th>상품명</th><th>카테고리</th>';
 cf.forEach(c=>h+=`<th class="right sortable ${mdSort.c==c.k?(mdSort.d>0?'asc':'desc'):''}" data-c="${c.k}">${c.l}</th>`);
 h+=`<th class="right sortable ${mdSort.c=='total'?(mdSort.d>0?'asc':'desc'):''}" data-c="total">합계</th>`;
 h+=`<th class="right sortable ${mdSort.c=='avg'?(mdSort.d>0?'asc':'desc'):''}" data-c="avg">월평균</th>`;
 h+=`<th class="right sortable ${mdSort.c=='stock'?(mdSort.d>0?'asc':'desc'):''}" data-c="stock">현재고</th></tr></thead><tbody>`;
 rows.forEach(m=>{h+=`<tr><td><span class="pill ${PILL[m.brand]}">${BNAME[m.brand]}</span></td><td class="mono">${m.model||'-'}</td><td style="max-width:290px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${esc(m.name)}">${m.name}</td><td style="color:var(--text3)">${m.cat||'-'}</td>`;
  cf.forEach(c=>h+=`<td class="right">${f(mval(m,c.k))}</td>`);
  h+=`<td class="right"><b>${f(m.total)}</b></td><td class="right" style="color:var(--blue)"><b>${m.avg.toLocaleString('ko-KR')}</b></td><td class="right ${m.stock<0?'neg':''}">${f(m.stock)}</td></tr>`;});
 h+='</tbody>';
 const t=document.getElementById('md-tbl');t.innerHTML=h;
 t.querySelectorAll('th.sortable').forEach(th=>th.onclick=()=>{const c=th.dataset.c;if(mdSort.c==c)mdSort.d*=-1;else{mdSort.c=c;mdSort.d=-1;}mdTbl();});
 document.getElementById('md-cnt').textContent=rows.length+'모델';
}

// INVENTORY
let invB='AP',invQ='',invSort={c:'amt',d:-1},invSnap=D.latest_snap;
function renderInv(){document.getElementById('inv-snap').innerHTML=snapOptions();document.getElementById('inv-snap').value=D.latest_snap;document.getElementById('inv-snap').onchange=e=>{invSnap=e.target.value;invTbl();};seg('inv-brand',v=>{invB=v;invTbl();});document.getElementById('inv-search').oninput=e=>{invQ=e.target.value.trim();invTbl();};invTrend();invTbl();}
function invTrend(){mkChart('inv-trend','line',{labels:SNAPS.map(s=>s.l),datasets:TRK.map(b=>({label:BNAME[b],data:SNAPS.map(s=>D.bstock_by_snap[s.k][b][2]),borderColor:BC[b],backgroundColor:'transparent',tension:.3}))},{plugins:{legend:{position:'bottom'},tooltip:{callbacks:{label:c=>c.dataset.label+': '+f(c.raw)+'원'}}},scales:{y:{ticks:{callback:v=>(v/1e8).toFixed(1)+'억'}}}});}
function invTbl(){
 const bs=D.bstock_by_snap[invSnap];const snapL=SNAPS.find(s=>s.k==invSnap).l;
 document.getElementById('inv-snaplbl').textContent='기준 '+snapL;
 document.getElementById('inv-kpi').innerHTML=TRK.map(b=>`<div class="kpi"><div class="kpi-icon ${ICO[b]}">🏭</div><div class="kpi-label">${BNAME[b]} 재고총액</div><div class="kpi-val ${ICO[b]}" style="font-size:18px">${f(bs[b][2])}원</div><div class="kpi-sub">${f(bs[b][1])}개 · ${bs[b][0]}품목</div></div>`).join('');
 let rows=D.inv_by_snap[invSnap].filter(x=>x.brand==invB&&(invQ==''||x.name.toLowerCase().includes(invQ.toLowerCase())));
 rows.sort((a,b)=>{const x=a[invSort.c],y=b[invSort.c];return(typeof x=='string'?x.localeCompare(y):(x<y?-1:x>y?1:0))*invSort.d;});
 let h=`<thead><tr><th class="sortable" data-c="name">상품명</th><th class="sortable" data-c="cat">카테고리</th><th class="right sortable ${invSort.c=='qty'?(invSort.d>0?'asc':'desc'):''}" data-c="qty">재고수량</th><th class="right sortable" data-c="unit">재고단가</th><th class="right sortable ${invSort.c=='amt'?(invSort.d>0?'asc':'desc'):''}" data-c="amt">재고총액</th></tr></thead><tbody>`;
 let sq=0,sa=0;
 rows.forEach(x=>{sq+=x.qty;sa+=x.amt;h+=`<tr><td style="max-width:360px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${esc(x.name)}">${x.name}</td><td style="color:var(--text3)">${x.cat||'-'}</td><td class="right ${x.qty<0?'neg':''}">${f(x.qty)}</td><td class="right mono">${f(x.unit)}</td><td class="right ${x.amt<0?'neg':''}">${f(x.amt)}</td></tr>`;});
 h+=`</tbody><tfoot><tr><td colspan="2">합계 (${rows.length}품목)</td><td class="right">${f(sq)}</td><td></td><td class="right">${f(sa)}</td></tr></tfoot>`;
 const t=document.getElementById('inv-tbl');t.innerHTML=h;
 t.querySelectorAll('th.sortable').forEach(th=>th.onclick=()=>{const c=th.dataset.c;if(invSort.c==c)invSort.d*=-1;else{invSort.c=c;invSort.d=(c=='name'||c=='cat')?1:-1;}invTbl();});
 document.getElementById('inv-cnt').textContent=rows.length+'품목';
}

// ADEQUACY
let adqB='ALL',adqF='shortwarn',adqQ='',adqSort={c:'days',d:1},adqSnap=D.latest_snap;
function statusRankV(avg,stock){if(stock<=0)return 0;if(stock<=avg)return 1;if(stock<=avg*2)return 2;return 3;}
function statusPillV(r){return [['품절','p-red'],['부족','p-orange'],['주의','p-yellow'],['적정','p-green']][r];}
function renderAdq(){document.getElementById('adq-snap').innerHTML=snapOptions();document.getElementById('adq-snap').value=D.latest_snap;document.getElementById('adq-snap').onchange=e=>{adqSnap=e.target.value;adqTbl();};seg('adq-brand',v=>{adqB=v;adqTbl();});seg('adq-filt',v=>{adqF=v;adqTbl();});document.getElementById('adq-search').oninput=e=>{adqQ=e.target.value.trim();adqTbl();};adqTbl();}
function adqTbl(){
 const snap=adqSnap;
 let rows=D.models.filter(m=>m.avg>0&&(adqB=='ALL'||m.brand==adqB)&&(adqQ==''||(m.name+m.model).toLowerCase().includes(adqQ.toLowerCase())));
 const stk=m=>stockAt(m,snap);
 if(adqF=='short')rows=rows.filter(m=>stk(m)<=m.avg);
 else if(adqF=='shortwarn')rows=rows.filter(m=>stk(m)<=m.avg*2);
 const gv=(m,c)=>({avg:m.avg,adq:m.avg*2,stock:stk(m),diff:stk(m)-Math.round(m.avg*2),order:Math.max(0,Math.round(m.avg*2)-stk(m)),days:daysLeftV(m.avg,stk(m)),status:statusRankV(m.avg,stk(m))}[c]);
 rows.sort((a,b)=>{const x=gv(a,adqSort.c),y=gv(b,adqSort.c);return(x<y?-1:x>y?1:0)*adqSort.d;});
 const base=D.models.filter(m=>m.avg>0);
 const short=base.filter(m=>stk(m)<=m.avg);
 const snapL=SNAPS.find(s=>s.k==snap).l;
 document.getElementById('adq-kpi').innerHTML=[
  ['red','⚠️','부족 품목',short.length+'건','현재고 ≤ 월평균 ('+snapL+')'],
  ['red','🚫','품절/초과판매',short.filter(m=>stk(m)<=0).length+'건','현재고 0 이하'],
  ['yellow','📌','주의 품목',base.filter(m=>stk(m)>m.avg&&stk(m)<=m.avg*2).length+'건','월평균~적정재고'],
  ['blue','📉','부족 애니포트',short.filter(m=>m.brand=='AP').length+'건','']
 ].map(k=>`<div class="kpi"><div class="kpi-icon ${k[0]}">${k[1]}</div><div class="kpi-label">${k[2]}</div><div class="kpi-val ${k[0]=='yellow'?'orange':k[0]}">${k[3]}</div><div class="kpi-sub">${k[4]}</div></div>`).join('');
 const S=c=>`sortable ${adqSort.c==c?(adqSort.d>0?'asc':'desc'):''}`;
 let h=`<thead><tr><th>브랜드</th><th>모델</th><th>상품명</th><th class="right ${S('avg')}" data-c="avg">월평균</th><th class="right ${S('adq')}" data-c="adq">적정재고</th><th class="right ${S('stock')}" data-c="stock">현재고</th><th class="right ${S('diff')}" data-c="diff">과부족</th><th class="right ${S('days')}" data-c="days">예상보유일</th><th class="right ${S('order')}" data-c="order">발주필요량</th><th class="${S('status')}" data-c="status">상태</th></tr></thead><tbody>`;
 rows.forEach(m=>{const st=stk(m);const adq=Math.round(m.avg*2);const diff=st-adq;const order=Math.max(0,adq-st);const d=daysLeftV(m.avg,st);const sp=statusPillV(statusRankV(m.avg,st));
  h+=`<tr><td><span class="pill ${PILL[m.brand]}">${BNAME[m.brand]}</span></td><td class="mono">${m.model||'-'}</td><td style="max-width:270px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${esc(m.name)}">${m.name}</td><td class="right">${m.avg.toLocaleString('ko-KR')}</td><td class="right">${f(adq)}</td><td class="right ${st<0?'neg':''}">${f(st)}</td><td class="right ${diff<0?'neg':''}">${diff>0?'+':''}${f(diff)}</td><td class="right"><b>${st<=0?'품절':d+'일'}</b></td><td class="right"><b style="color:${order>0?'var(--red)':'var(--text3)'}">${order>0?f(order):'-'}</b></td><td><span class="pill ${sp[1]}">${sp[0]}</span></td></tr>`;});
 h+='</tbody>';
 const t=document.getElementById('adq-tbl');t.innerHTML=h;
 t.querySelectorAll('th.sortable').forEach(th=>th.onclick=()=>{const c=th.dataset.c;if(adqSort.c==c)adqSort.d*=-1;else{adqSort.c=c;adqSort.d=1;}adqTbl();});
 document.getElementById('adq-cnt').textContent=rows.length+'품목';
}

renderOv();renderCh();renderMd();renderInv();renderAdq();
</script>
</body></html>'''
HTML=HTML.replace('__CSS__',css).replace('__CHARTJS__',chartjs).replace('__DATA__',data)
open('2026.08_index.html','w',encoding='utf-8').write(HTML)
print('written KB',round(len(HTML)/1024))
