import{$ as e,C as t,E as n,F as r,M as i,N as a,R as o,U as s,b as c,et as l,g as u,rt as d}from"./src-DUBXPdxE.js";import{t as f}from"./ordinal-B18sgwlE.js";import{n as p}from"./path-CuyvWNAH.js";import{p as m}from"./math-B7b0HgJF.js";import{t as h}from"./arc-CE-LMSPx.js";import{t as g}from"./array-CYkMkqnU.js";import{f as _,r as v}from"./chunk-O4NI6UNU-CHf13HOt.js";import{t as y}from"./chunk-4BMEZGHF-Dv-L0w3K.js";import{t as b}from"./chunk-7B677QYD-B4y0Fn7Y.js";import{t as x}from"./mermaid-parser.core-BITAY7-8.js";function S(e,t){return t<e?-1:t>e?1:t>=e?0:NaN}function C(e){return e}function w(){var e=C,t=S,n=null,r=p(0),i=p(m),a=p(0);function o(o){var s,c=(o=g(o)).length,l,u,d=0,f=Array(c),p=Array(c),h=+r.apply(this,arguments),_=Math.min(m,Math.max(-m,i.apply(this,arguments)-h)),v,y=Math.min(Math.abs(_)/c,a.apply(this,arguments)),b=y*(_<0?-1:1),x;for(s=0;s<c;++s)(x=p[f[s]=s]=+e(o[s],s,o))>0&&(d+=x);for(t==null?n!=null&&f.sort(function(e,t){return n(o[e],o[t])}):f.sort(function(e,n){return t(p[e],p[n])}),s=0,u=d?(_-c*b)/d:0;s<c;++s,h=v)l=f[s],x=p[l],v=h+(x>0?x*u:0)+b,p[l]={data:o[l],index:s,value:x,startAngle:h,endAngle:v,padAngle:y};return p}return o.value=function(t){return arguments.length?(e=typeof t==`function`?t:p(+t),o):e},o.sortValues=function(e){return arguments.length?(t=e,n=null,o):t},o.sort=function(e){return arguments.length?(n=e,t=null,o):n},o.startAngle=function(e){return arguments.length?(r=typeof e==`function`?e:p(+e),o):r},o.endAngle=function(e){return arguments.length?(i=typeof e==`function`?e:p(+e),o):i},o.padAngle=function(e){return arguments.length?(a=typeof e==`function`?e:p(+e),o):a},o}var T=n.pie,E={sections:new Map,showData:!1,config:T},D=E.sections,O=E.showData,k=structuredClone(T),A={getConfig:u(()=>structuredClone(k),`getConfig`),clear:u(()=>{D=new Map,O=E.showData,c()},`clear`),setDiagramTitle:d,getDiagramTitle:o,setAccTitle:l,getAccTitle:a,setAccDescription:e,getAccDescription:i,addSection:u(({label:e,value:t})=>{D.has(e)||(D.set(e,t),s.debug(`added new section: ${e}, with value: ${t}`))},`addSection`),getSections:u(()=>D,`getSections`),setShowData:u(e=>{O=e},`setShowData`),getShowData:u(()=>O,`getShowData`)},j=u((e,t)=>{y(e,t),t.setShowData(e.showData),e.sections.map(t.addSection)},`populateDb`),M={parse:u(async e=>{let t=await x(`pie`,e);s.debug(t),j(t,A)},`parse`)},N=u(e=>`
  .pieCircle{
    stroke: ${e.pieStrokeColor};
    stroke-width : ${e.pieStrokeWidth};
    opacity : ${e.pieOpacity};
  }
  .pieOuterCircle{
    stroke: ${e.pieOuterStrokeColor};
    stroke-width: ${e.pieOuterStrokeWidth};
    fill: none;
  }
  .pieTitleText {
    text-anchor: middle;
    font-size: ${e.pieTitleTextSize};
    fill: ${e.pieTitleTextColor};
    font-family: ${e.fontFamily};
  }
  .slice {
    font-family: ${e.fontFamily};
    fill: ${e.pieSectionTextColor};
    font-size:${e.pieSectionTextSize};
    // fill: white;
  }
  .legend text {
    fill: ${e.pieLegendTextColor};
    font-family: ${e.fontFamily};
    font-size: ${e.pieLegendTextSize};
  }
`,`getStyles`),P=u(e=>{let t=[...e.entries()].map(e=>({label:e[0],value:e[1]})).sort((e,t)=>t.value-e.value);return w().value(e=>e.value)(t)},`createPieArcs`),F={parser:M,db:A,renderer:{draw:u((e,n,i,a)=>{s.debug(`rendering pie chart
`+e);let o=a.db,c=r(),l=v(o.getConfig(),c.pie),u=b(n),d=u.append(`g`);d.attr(`transform`,`translate(225,225)`);let{themeVariables:p}=c,[m]=_(p.pieOuterStrokeWidth);m??=2;let g=l.textPosition,y=h().innerRadius(0).outerRadius(185),x=h().innerRadius(185*g).outerRadius(185*g);d.append(`circle`).attr(`cx`,0).attr(`cy`,0).attr(`r`,185+m/2).attr(`class`,`pieOuterCircle`);let S=o.getSections(),C=P(S),w=f([p.pie1,p.pie2,p.pie3,p.pie4,p.pie5,p.pie6,p.pie7,p.pie8,p.pie9,p.pie10,p.pie11,p.pie12]);d.selectAll(`mySlices`).data(C).enter().append(`path`).attr(`d`,y).attr(`fill`,e=>w(e.data.label)).attr(`class`,`pieCircle`);let T=0;S.forEach(e=>{T+=e}),d.selectAll(`mySlices`).data(C).enter().append(`text`).text(e=>(e.data.value/T*100).toFixed(0)+`%`).attr(`transform`,e=>`translate(`+x.centroid(e)+`)`).style(`text-anchor`,`middle`).attr(`class`,`slice`),d.append(`text`).text(o.getDiagramTitle()).attr(`x`,0).attr(`y`,-400/2).attr(`class`,`pieTitleText`);let E=d.selectAll(`.legend`).data(w.domain()).enter().append(`g`).attr(`class`,`legend`).attr(`transform`,(e,t)=>{let n=22*w.domain().length/2;return`translate(216,`+(t*22-n)+`)`});E.append(`rect`).attr(`width`,18).attr(`height`,18).style(`fill`,w).style(`stroke`,w),E.data(C).append(`text`).attr(`x`,22).attr(`y`,14).text(e=>{let{label:t,value:n}=e.data;return o.getShowData()?`${t} [${n}]`:t});let D=512+Math.max(...E.selectAll(`text`).nodes().map(e=>e?.getBoundingClientRect().width??0));u.attr(`viewBox`,`0 0 ${D} 450`),t(u,450,D,l.useMaxWidth)},`draw`)},styles:N};export{F as diagram};