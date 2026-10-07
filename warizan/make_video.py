# 小学4年生向け わり算(2けたでわる) 解説動画ジェネレータ
import os, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont
W, H = 1280, 720
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
def F(s): return ImageFont.truetype(FONT, s)
BG=(255,248,225); INK=(60,50,40); BLUE=(66,133,244); RED=(229,57,53)
GREEN=(46,160,90); ORANGE=(255,152,0); PINK=(255,205,210)
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)))
FR=os.path.join(OUT,"frames"); shutil.rmtree(FR,ignore_errors=True); os.makedirs(FR)
scenes=[]  # (path, seconds)
def new(): 
    im=Image.new("RGB",(W,H),BG); return im, ImageDraw.Draw(im)
def text(d,xy,s,size,col=INK,anchor="mm"): d.text(xy,s,font=F(size),fill=col,anchor=anchor)
def save(im,sec):
    p=os.path.join(FR,f"f{len(scenes):04d}.png"); im.save(p); scenes.append((p,sec))
def rnd(n): return (n+5)//10*10

def intro():
    im,d=new()
    text(d,(W/2,200),"わり算は「何回入る？」ゲーム",64,BLUE)
    text(d,(W/2,350),"わり算 = ある数の中に",44); text(d,(W/2,420),"ほかの数が 何回入るか を数えること",44)
    text(d,(W/2,560),"むずかしい数も 「ざっくり」→「たしかめ」で かんたん！",36,ORANGE)
    save(im,6)
def question(A,B,story=True):
    im,d=new()
    text(d,(W/2,180),f"{A} ÷ {B}",150,BLUE)
    text(d,(W/2,350),f"{A}の中に {B}が 何回入る？",54)
    if story: text(d,(W/2,470),f"{A}円で、{B}円のおかしが 何こ買える？",44,GREEN)
    save(im,6)
def bars(A,B):
    q=A//B; r=A-q*B; scale=1100/((q+1)*B); x0=90
    cols=[BLUE,GREEN,ORANGE]
    for k in range(1,q+2):
        im,d=new()
        text(d,(W/2,70),f"{A} ÷ {B}   {B}を ならべていこう",42)
        # whole amount bar
        d.rounded_rectangle([x0,150,x0+A*scale,230],8,outline=INK,width=4,fill=(255,255,255))
        text(d,(x0+A*scale/2,190),f"{A}",40)
        # blocks
        for i in range(k):
            xs=x0+i*B*scale; xe=xs+B*scale
            over=(i==q)
            c=RED if over else cols[i%3]
            d.rounded_rectangle([xs+2,290,xe-2,370],8,fill=c)
            text(d,((xs+xe)/2,330),f"{B}",34,(255,255,255))
            text(d,((xs+xe)/2,400),f"{i+1}回目",28,c)
        if k<=q:
            text(d,(W/2,520),f"{k}回で {B*k}   （{A}まで あと {A-B*k}）",46)
            text(d,(W/2,610),"まだ入る！ つづけよう",36,GREEN)
        else:
            text(d,(W/2,520),f"{k}回目は {B*k} … {A}を こえちゃった！",46,RED)
            text(d,(W/2,610),f"だから {q}回 までで、あまりは {r}",42,RED)
        save(im,2.2 if k<=q else 4.5)
def estimate(A,B):
    a,b=rnd(A),rnd(B); e=a//b
    im,d=new()
    text(d,(W/2,70),"ざっくり作戦：切りのいい数に近づけよう",46,BLUE)
    text(d,(W/2,190),f"{B} は {b} に近い",48); text(d,(W/2,270),f"{A} は {a} に近い",48)
    text(d,(W/2,400),f"{a} ÷ {b} = {e}",90,GREEN)
    text(d,(W/2,530),f"だから「だいたい {e}回」と 予想！",48)
    text(d,(W/2,620),"（ほんとうに合ってるか、次でたしかめるよ）",32,ORANGE)
    save(im,8); return e
def check(A,B,e):
    q=A//B; r=A-q*B; cur=e
    while True:
        p=B*cur; im,d=new()
        text(d,(W/2,70),f"たしかめ：{B} × {cur} をけいさん",46,BLUE)
        text(d,(W/2,200),f"{B} × {cur} = {p}",90)
        if p>A:
            text(d,(W/2,350),f"{p} は {A} より 大きい！",54,RED)
            text(d,(W/2,450),f"入りすぎ → {cur} を 1 へらして {cur-1} に",50,RED)
            save(im,8); cur-=1; continue
        rem=A-p
        text(d,(W/2,320),f"{A} - {p} = {rem}   これが「あまり」",54)
        if rem>=B:
            text(d,(W/2,430),f"あまり {rem} は {B} 以上 → まだ入る！",50,RED)
            text(d,(W/2,520),f"少なかった → {cur} を 1 ふやして {cur+1} に",50,RED)
            save(im,8); cur+=1; continue
        text(d,(W/2,430),f"あまり {rem} は {B} より小さい → OK！",50,GREEN)
        text(d,(W/2,520),"あまりは、わる数より 小さくなるのがルール",36,ORANGE)
        save(im,8); break
    assert cur==q
def answer(A,B):
    q=A//B; r=A-q*B; im,d=new()
    text(d,(W/2,150),"答え",50,ORANGE)
    s=f"{A} ÷ {B} = {q}" + (f" あまり {r}" if r else "")
    text(d,(W/2,300),s,90,BLUE)
    text(d,(W/2,470),"たしかめ算",40,GREEN)
    text(d,(W/2,550),f"{B} × {q}" + (f" + {r}" if r else "") + f" = {A}",64)
    save(im,8)
def short(A,B):
    q=A//B; r=A-q*B; e=rnd(A)//rnd(B)
    im,d=new(); text(d,(W/2,220),f"{A} ÷ {B}",120,BLUE)
    text(d,(W/2,400),f"ざっくり {rnd(A)} ÷ {rnd(B)} → だいたい {e}回",46)
    text(d,(W/2,500),"さあ、自分で たしかめてみよう！",40,ORANGE)
    save(im,9)
    im,d=new(); text(d,(W/2,130),"こたえあわせ",46,ORANGE)
    text(d,(W/2,270),f"{A} ÷ {B} = {q}"+(f" あまり {r}" if r else ""),84,BLUE)
    text(d,(W/2,420),f"{B} × {q}"+(f" + {r}" if r else "")+f" = {A}",56)
    if e!=q: text(d,(W/2,540),f"ざっくり予想の {e} は ちょっと ちがった → {q} にちょうせい！",36,RED)
    else: text(d,(W/2,540),"予想どおり！ すごい！",40,GREEN)
    save(im,8)

def hissan(A,B,num,secs=4):
    q=A//B; p=B*q; r=A-p
    ds=str(A); n=len(ds); cw=100; x0=480; y0=230
    for stage in (1,2,3):
        im,d=new()
        text(d,(W/2,60),f"{num}  {A} ÷ {B}  の 筆算",44,BLUE)
        # bracket
        d.line([x0-20,y0-45,x0-20,y0+55],fill=INK,width=5)
        d.line([x0-20,y0-45,x0+n*cw+10,y0-45],fill=INK,width=5)
        text(d,(x0-80,y0),f"{B}",64,INK,"rm")
        for i,c in enumerate(ds): text(d,(x0+i*cw+cw/2,y0),c,64)
        def col(k): return x0+(n-1-k)*cw+cw/2   # k=0 ones place
        text(d,(col(0),y0-90),f"{q}",64,RED)
        cap=""
        if stage>=1: cap=f"① {A} の中に {B} が {q}回 入る → 一の位に {q} をたてる"
        if stage>=2:
            ps=str(p)
            for k,c in enumerate(reversed(ps)): text(d,(col(k),y0+90),c,64,GREEN)
            d.line([x0-10,y0+135,x0+n*cw,y0+135],fill=INK,width=4)
            cap=f"② {B} × {q} = {p} を下に書く"
        if stage>=3:
            rs=str(r)
            for k,c in enumerate(reversed(rs)): text(d,(col(k),y0+190),c,64,ORANGE)
            cap=f"③ {A} - {p} = {r}" + ("  あまり" if r else "  ぴったり！")
        text(d,(W/2,540),cap,44)
        if stage==3:
            text(d,(W/2,620),f"答え  {q}"+(f" あまり {r}" if r else "")+f"    たしかめ  {B}×{q}"+(f"+{r}" if r else "")+f" = {A}",40,BLUE)
        save(im,secs)

def section(t,sub):
    im,d=new(); text(d,(W/2,300),t,76,BLUE); text(d,(W/2,430),sub,40); save(im,3.5)
def outro():
    im,d=new()
    text(d,(W/2,200),"まとめ",70,BLUE)
    for i,s in enumerate(["① 「何回入る？」と考える","② 切りのいい数で ざっくり予想","③ かけ算でたしかめて、大きすぎ・小さすぎは 1 ちょうせい","④ あまりは わる数より 小さい"]):
        text(d,(W/2,320+i*75),s,44)
    text(d,(W/2,660),"まちがえても大丈夫！ 直せたらそれが成長",36,GREEN); save(im,9)

intro()
section("① 359 ÷ 58","ワークシートの①"); question(359,58); bars(359,58); e=estimate(359,58); check(359,58,e); answer(359,58); hissan(359,58,"①",5)
section("② 180 ÷ 34","予想がズレる例"); question(180,34); bars(180,34); e=estimate(180,34); check(180,34,e); answer(180,34); hissan(180,34,"②",5)
section("③〜⑫","ざっくり予想 → 筆算 → たしかめ")
nums="③④⑤⑥⑦⑧⑨⑩⑪⑫"
for n_,(A,B) in zip(nums,[(635,79),(101,25),(259,37),(400,58),(172,26),(191,24),(100,28),(145,29),(272,39),(190,28)]):
    q=A//B; e=rnd(A)//rnd(B)
    im,d=new(); text(d,(W/2,100),n_,60,ORANGE); text(d,(W/2,250),f"{A} ÷ {B}",120,BLUE)
    text(d,(W/2,420),f"ざっくり {rnd(A)} ÷ {rnd(B)} → だいたい {e}回",46)
    text(d,(W/2,520),"まず自分で予想してみよう！",40,ORANGE); save(im,7)
    if e!=q:
        im,d=new(); text(d,(W/2,250),f"予想の {e} から {q} に ちょうせい！",54,RED)
        text(d,(W/2,380),f"{B} × {e} = {B*e}" + ("  → 大きすぎ！" if B*e>A else f"  → あまり {A-B*e} が {B} 以上、まだ入る！"),46,RED); save(im,6)
    hissan(A,B,n_,4)
outro()
with open(os.path.join(OUT,"list.txt"),"w") as f:
    for p,s in scenes: f.write(f"file '{p}'\nduration {s}\n")
    f.write(f"file '{scenes[-1][0]}'\n")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",os.path.join(OUT,"list.txt"),
  "-vf","fps=24,format=yuv420p","-c:v","libx264",os.path.join(OUT,"warizan_359_58.mp4")],check=True)
print("frames",len(scenes),"sec",sum(s for _,s in scenes))
