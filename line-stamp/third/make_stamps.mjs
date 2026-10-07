// LINEスタンプ第三弾「くにボールのひとこと」の画像を作る。
// ボールは kuttsuke/index.html の drawBall をそのまま取り出して使う（見本は毎回同じ）。
// 使い方: node make_stamps.mjs   （playwright が必要）
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');

const src = fs.readFileSync(path.join(root, 'kuttsuke/index.html'), 'utf8');
const a = src.indexOf('function paintBody'), b = src.indexOf('function iconBall');
const ballCode = `const INK='#1D2742';\n` + src.slice(a, b);

const W = 370, H = 320, M = 10;
const STAMPS = JSON.parse(fs.readFileSync(path.join(here, 'stamps.json'), 'utf8'));

const page_html = `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:M;src:url('${pathToFileURL(path.join(here, 'MochiyPopOne-subset.ttf'))}')}
html,body{margin:0;background:transparent}canvas{display:block}</style>
<canvas id="c" width="${W}" height="${H}"></canvas>
<script>
${ballCode}
const W=${W},H=${H},M=${M};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
function drop(x,y,s){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.beginPath();ctx.moveTo(0,-14);ctx.bezierCurveTo(11,2,9,12,0,12);ctx.bezierCurveTo(-9,12,-11,2,0,-14);ctx.fillStyle='#8FD3F4';ctx.fill();ctx.lineWidth=2.6;ctx.strokeStyle=INK;ctx.stroke();ctx.restore();}
function heart(x,y,s,col){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.beginPath();ctx.moveTo(0,8);ctx.bezierCurveTo(-16,-4,-8,-16,0,-7);ctx.bezierCurveTo(8,-16,16,-4,0,8);ctx.fillStyle=col;ctx.fill();ctx.lineWidth=2.4;ctx.strokeStyle=INK;ctx.stroke();ctx.restore();}
function spark(x,y,s){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.beginPath();ctx.moveTo(0,-12);ctx.quadraticCurveTo(2,-2,12,0);ctx.quadraticCurveTo(2,2,0,12);ctx.quadraticCurveTo(-2,2,-12,0);ctx.quadraticCurveTo(-2,-2,0,-12);ctx.fillStyle='#FFD84A';ctx.fill();ctx.lineWidth=2.4;ctx.strokeStyle=INK;ctx.stroke();ctx.restore();}
function line(x,y,s,rot){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.lineCap='round';ctx.strokeStyle=INK;ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-s,0);ctx.lineTo(s,0);ctx.stroke();ctx.restore();}
function exclaim(x,y,s){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.lineCap='round';ctx.strokeStyle=INK;ctx.lineWidth=7;ctx.beginPath();ctx.moveTo(0,-14);ctx.lineTo(0,3);ctx.stroke();ctx.fillStyle=INK;ctx.beginPath();ctx.arc(0,13,4.2,0,7);ctx.fill();ctx.restore();}
function check(x,y,s){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle='#fff';ctx.lineWidth=13;ctx.beginPath();ctx.moveTo(-12,0);ctx.lineTo(-3,10);ctx.lineTo(13,-10);ctx.stroke();ctx.strokeStyle='#2FA84F';ctx.lineWidth=7;ctx.stroke();ctx.restore();}
function zzz(x,y,s){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle=INK;ctx.lineWidth=4.5;ctx.beginPath();ctx.moveTo(-9,-8);ctx.lineTo(9,-8);ctx.lineTo(-9,9);ctx.lineTo(9,9);ctx.stroke();ctx.restore();}
function note(x,y,s){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle=INK;ctx.strokeStyle=INK;ctx.lineWidth=4;ctx.lineCap='round';ctx.beginPath();ctx.ellipse(-5,10,7,5,-.4,0,7);ctx.fill();ctx.beginPath();ctx.moveTo(1,8);ctx.lineTo(1,-12);ctx.quadraticCurveTo(10,-8,13,0);ctx.stroke();ctx.restore();}
const SYM={drop:(cx,cy,r)=>drop(cx+r*.95,cy-r*.55,1),hearts:(cx,cy,r)=>{heart(cx+r*.98,cy-r*.62,1.05,'#FF6F8E');heart(cx-r*1.0,cy-r*.3,.75,'#FF9DB3');},
 spark:(cx,cy,r)=>{spark(cx+r*.95,cy-r*.6,1.1);spark(cx-r*.98,cy-r*.45,.7);},
 sweat2:(cx,cy,r)=>{drop(cx+r*1.0,cy-r*.45,1);line(cx+r*.62,cy-r*1.08,7,-.9);line(cx+r*.95,cy-r*.98,7,-.35);},exclaim:(cx,cy,r)=>exclaim(cx+r*1.0,cy-r*.5,1),check:(cx,cy,r)=>check(cx+r*1.02,cy-r*.52,1),
 zzz:(cx,cy,r)=>{zzz(cx+r*.9,cy-r*.45,1);zzz(cx+r*1.12,cy-r*.98,.65);},note:(cx,cy,r)=>{note(cx+r*1.0,cy-r*.55,1);note(cx-r*1.0,cy-r*.3,.7);},
 speed:(cx,cy,r)=>{line(cx-r*1.12,cy-r*.3,10,0);line(cx-r*1.12,cy+r*.1,10,0);line(cx-r*.95,cy+r*.5,8,0);},none:()=>{}};
function render(s){
  ctx.clearRect(0,0,W,H);
  const r=58,cx=W/2+(s.dx||0),cy=M+r+10+(s.dy||0);
  ctx.save();ctx.translate(cx,cy);ctx.rotate(s.tilt*Math.PI/180);ctx.scale(1+(s.sq||0),1-(s.sq||0));
  drawBall(ctx,s.c,r,s.eye);ctx.restore();
  (SYM[s.sym]||SYM.none)(cx,cy,r);
  const lines=s.lines,maxW=W-2*M-16;
  const top=cy+r+(s.gap||6),bot=H-M-8;let size=Math.min(Math.floor((bot-top)/(lines.length*1.06)),Math.floor(maxW/Math.max(...lines.map(t=>t.length))));
  ctx.font=size+'px M';
  while(Math.max(...lines.map(t=>ctx.measureText(t).width))>maxW){size--;ctx.font=size+'px M';}
  const lh=size*1.06,blockH=lh*lines.length;
  let y=top+(bot-top-blockH)/2+lh/2;
  ctx.textAlign='center';ctx.textBaseline='middle';ctx.lineJoin='round';
  for(const t of lines){ctx.lineWidth=11;ctx.strokeStyle='#fff';ctx.strokeText(t,W/2,y);ctx.fillStyle=INK;ctx.fillText(t,W/2,y);y+=lh;}
}
window.go=async s=>{await document.fonts.load('40px M',s.lines.join(''));render(s);return cv.toDataURL('image/png');};
</script>`;
const html = page_html;
fs.writeFileSync(path.join(here, '_gen.html'), html);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, '_gen.html')).href);
const outDir = path.join(here, 'png'); fs.mkdirSync(outDir, { recursive: true });
for (const s of STAMPS) {
  const url = await page.evaluate(x => window.go(x), s);
  fs.writeFileSync(path.join(outDir, s.id + '.png'), Buffer.from(url.split(',')[1], 'base64'));
  console.log('wrote', s.id);
}
await browser.close();
fs.unlinkSync(path.join(here, '_gen.html'));
