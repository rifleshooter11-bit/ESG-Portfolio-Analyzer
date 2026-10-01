const ids = ['baseWacc','riskAdjustment','capex','opex','score'];
const input = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));
const fmt = n => `₹${Math.round(n).toLocaleString('en-IN')} Cr`;
function update(){
  const baseWacc=+input.baseWacc.value, adjustment=+input.riskAdjustment.value, capex=+input.capex.value, opex=+input.opex.value, score=+input.score.value;
  const adjusted=baseWacc+adjustment;
  const baseEV=11360*(10.8/baseWacc)**1.15;
  const transitionDrag=(capex-120)*2.2+(opex-45)*4.1;
  const scoreBenefit=(score-76)*24;
  const capitalBenefit=(10.8/adjusted)**1.15*588;
  const esgEV=Math.max(0,baseEV+capitalBenefit-transitionDrag+scoreBenefit);
  const delta=esgEV-baseEV;
  document.getElementById('baseWaccOut').textContent=`${baseWacc.toFixed(1)}%`;
  document.getElementById('riskAdjustmentOut').textContent=`${adjustment<0?'−':'+'}${Math.abs(adjustment).toFixed(1)}%`;
  document.getElementById('capexOut').textContent=fmt(capex);
  document.getElementById('opexOut').textContent=fmt(opex);
  document.getElementById('scoreOut').textContent=`${score} / 100`;
  document.getElementById('baseEv').textContent=fmt(baseEV);
  document.getElementById('esgEv').textContent=fmt(esgEV);
  document.getElementById('baseEvHeadline').textContent=fmt(baseEV);
  document.getElementById('esgEvHeadline').textContent=fmt(esgEV);
  document.getElementById('baseWaccValue').textContent=`${baseWacc.toFixed(1)}%`;
  document.getElementById('adjustedWacc').textContent=`${adjusted.toFixed(1)}%`;
  document.getElementById('capexValue').textContent=`${fmt(capex)} / year`;
  document.getElementById('opexValue').textContent=`${fmt(opex)} / year`;
  document.getElementById('scoreValue').textContent=`${score} / 100`;
  const sign=delta>=0?'+':'−', pct=(Math.abs(delta)/baseEV*100).toFixed(1);
  const movement=`${sign}${fmt(Math.abs(delta))}`;
  document.getElementById('valueDelta').innerHTML=`${movement} <small>(${sign}${pct}%)</small>`;
  document.getElementById('valueMovement').textContent=movement;
  document.getElementById('baseBar').style.width=`${Math.min(100,baseEV/Math.max(baseEV,esgEV)*100)}%`;
  document.getElementById('esgBar').style.width=`${Math.min(100,esgEV/Math.max(baseEV,esgEV)*100)}%`;
}
ids.forEach(id=>input[id].addEventListener('input',update)); update();
function download(name, content, type='text/plain'){const blob=new Blob([content],{type});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.click();URL.revokeObjectURL(url)}
document.getElementById('downloadLedger').addEventListener('click',e=>{e.preventDefault();download('verdant-ledger-evidence-snapshot.csv','Record ID,Topic,Method / factor,Source,Sign-off\nEV-00182,Scope 2 electricity,CEA factor 0.716 kgCO2e/kWh,Meter set Jul 2026,Operations Verified\nEV-00207,Supplier emissions,Supplier activity data Scope 3,101 Tier-1 submissions,Procurement Reviewed\nEV-00215,Workplace safety,LTIFR per 1m hours,HR & safety register,People Verified\nVA-00031,DCF scenario,5-year cash flow terminal growth 4.5%,Finance planning case,Finance Approved\n','text/csv')});
document.getElementById('downloadReport').addEventListener('click',()=>window.print());
