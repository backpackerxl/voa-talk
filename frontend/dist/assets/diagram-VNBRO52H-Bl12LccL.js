import{$ as e,C as t,E as n,M as r,N as i,P as a,R as o,U as s,b as c,et as l,g as u,rt as d}from"./src-DUBXPdxE.js";import{r as f}from"./chunk-O4NI6UNU-CHf13HOt.js";import{t as p}from"./chunk-4BMEZGHF-Dv-L0w3K.js";import{t as m}from"./chunk-7B677QYD-B4y0Fn7Y.js";import{t as h}from"./mermaid-parser.core-BITAY7-8.js";var g={packet:[]},_=structuredClone(g),v=n.packet,y={pushWord:u(e=>{e.length>0&&_.packet.push(e)},`pushWord`),getPacket:u(()=>_.packet,`getPacket`),getConfig:u(()=>{let e=f({...v,...a().packet});return e.showBits&&(e.paddingY+=10),e},`getConfig`),clear:u(()=>{c(),_=structuredClone(g)},`clear`),setAccTitle:l,getAccTitle:i,setDiagramTitle:d,getDiagramTitle:o,getAccDescription:r,setAccDescription:e},b=1e4,x=u(e=>{p(e,y);let t=-1,n=[],r=1,{bitsPerRow:i}=y.getConfig();for(let{start:a,end:o,label:c}of e.blocks){if(o&&o<a)throw Error(`Packet block ${a} - ${o} is invalid. End must be greater than start.`);if(a!==t+1)throw Error(`Packet block ${a} - ${o??a} is not contiguous. It should start from ${t+1}.`);for(t=o??a,s.debug(`Packet block ${a} - ${t} with label ${c}`);n.length<=i+1&&y.getPacket().length<b;){let[e,t]=S({start:a,end:o,label:c},r,i);if(n.push(e),e.end+1===r*i&&(y.pushWord(n),n=[],r++),!t)break;({start:a,end:o,label:c}=t)}}y.pushWord(n)},`populate`),S=u((e,t,n)=>{if(e.end===void 0&&(e.end=e.start),e.start>e.end)throw Error(`Block start ${e.start} is greater than block end ${e.end}.`);return e.end+1<=t*n?[e,void 0]:[{start:e.start,end:t*n-1,label:e.label},{start:t*n,end:e.end,label:e.label}]},`getNextFittingBlock`),C={parse:u(async e=>{let t=await h(`packet`,e);s.debug(t),x(t)},`parse`)},w=u((e,n,r,i)=>{let a=i.db,o=a.getConfig(),{rowHeight:s,paddingY:c,bitWidth:l,bitsPerRow:u}=o,d=a.getPacket(),f=a.getDiagramTitle(),p=s+c,h=p*(d.length+1)-(f?0:s),g=l*u+2,_=m(n);_.attr(`viewbox`,`0 0 ${g} ${h}`),t(_,h,g,o.useMaxWidth);for(let[e,t]of d.entries())T(_,t,e,o);_.append(`text`).text(f).attr(`x`,g/2).attr(`y`,h-p/2).attr(`dominant-baseline`,`middle`).attr(`text-anchor`,`middle`).attr(`class`,`packetTitle`)},`draw`),T=u((e,t,n,{rowHeight:r,paddingX:i,paddingY:a,bitWidth:o,bitsPerRow:s,showBits:c})=>{let l=e.append(`g`),u=n*(r+a)+a;for(let e of t){let t=e.start%s*o+1,n=(e.end-e.start+1)*o-i;if(l.append(`rect`).attr(`x`,t).attr(`y`,u).attr(`width`,n).attr(`height`,r).attr(`class`,`packetBlock`),l.append(`text`).attr(`x`,t+n/2).attr(`y`,u+r/2).attr(`class`,`packetLabel`).attr(`dominant-baseline`,`middle`).attr(`text-anchor`,`middle`).text(e.label),!c)continue;let a=e.end===e.start,d=u-2;l.append(`text`).attr(`x`,t+(a?n/2:0)).attr(`y`,d).attr(`class`,`packetByte start`).attr(`dominant-baseline`,`auto`).attr(`text-anchor`,a?`middle`:`start`).text(e.start),a||l.append(`text`).attr(`x`,t+n).attr(`y`,d).attr(`class`,`packetByte end`).attr(`dominant-baseline`,`auto`).attr(`text-anchor`,`end`).text(e.end)}},`drawWord`),E={draw:w},D={byteFontSize:`10px`,startByteColor:`black`,endByteColor:`black`,labelColor:`black`,labelFontSize:`12px`,titleColor:`black`,titleFontSize:`14px`,blockStrokeColor:`black`,blockStrokeWidth:`1`,blockFillColor:`#efefef`},O={parser:C,db:y,renderer:E,styles:u(({packet:e}={})=>{let t=f(D,e);return`
	.packetByte {
		font-size: ${t.byteFontSize};
	}
	.packetByte.start {
		fill: ${t.startByteColor};
	}
	.packetByte.end {
		fill: ${t.endByteColor};
	}
	.packetLabel {
		fill: ${t.labelColor};
		font-size: ${t.labelFontSize};
	}
	.packetTitle {
		fill: ${t.titleColor};
		font-size: ${t.titleFontSize};
	}
	.packetBlock {
		stroke: ${t.blockStrokeColor};
		stroke-width: ${t.blockStrokeWidth};
		fill: ${t.blockFillColor};
	}
	`},`styles`)};export{O as diagram};