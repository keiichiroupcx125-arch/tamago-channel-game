# 小学4年生向け わり算 解説動画(音声・イラスト付き) ジェネレータ
# 使い方: pip install pyopenjtalk && python3 make_video_voice.py
import os, shutil, subprocess, wave
import numpy as np, pyopenjtalk
from PIL import Image, ImageDraw, ImageFont
W,H=1280,720
FONT="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
def F(s): return ImageFont.truetype(FONT,s)
BG=(255,248,225); INK=(60,50,40); BLUE=(66,133,244); RED=(229,57,53)
GREEN=(46,160,90); ORANGE=(255,152,0)
OUT=os.path.dirname(os.path.abspath(__file__))
FR=os.path.join(OUT,"frames"); shutil.rmtree(FR,ignore_errors=True); os.makedirs(FR)
SR=48000; scenes=[]; audio=[]
def kan(n):
    if n==0: return "ゼロ"
    d="ゼロ一二三四五六七八九"; s=""
    h,t,o=n//100,n//10%10,n%10
    if h: s+=("" if h==1 else d[h])+"百"
    if t: s+=("" if t==1 else d[t])+"十"
    if o: s+=d[o]
    return s
def new():
    im=Image.new("RGB",(W,H),BG); return im,ImageDraw.Draw(im)
def text(d,xy,s,size,col=INK,anchor="mm"): d.text(xy,s,font=F(size),fill=col,anchor=anchor)
def cookie(d,cx,cy,r=26):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(205,150,80),outline=(140,90,40),width=3)
    for dx,dy in [(-9,-8),(8,-10),(0,6),(-11,9),(11,5)]:
        d.ellipse([cx+dx-4,cy+dy-4,cx+dx+4,cy+dy+4],fill=(90,50,30))
def egg(d,cx=95,cy=90,mood="smile"):
    d.ellipse([cx-45,cy-55,cx+45,cy+50],fill=(255,255,255),outline=INK,width=4)
    for ex in (-16,16): d.ellipse([cx+ex-5,cy-14,cx+ex+5,cy-4],fill=INK)
    if mood=="smile": d.arc([cx-18,cy-2,cx+18,cy+26],10,170,fill=INK,width=4)
    else: d.ellipse([cx-8,cy+8,cx+8,cy+24],outline=INK,width=4)
    d.ellipse([cx-34,cy+4,cx-20,cy+16],fill=(255,190,190)); d.ellipse([cx+20,cy+4,cx+34,cy+16],fill=(255,190,190))
def wallet(d,cx,cy,label):
    d.rounded_rectangle([cx-110,cy-55,cx+110,cy+55],18,fill=(190,120,70),outline=(110,60,30),width=4)
    d.rounded_rectangle([cx+50,cy-18,cx+110,cy+18],10,fill=(230,190,120),outline=(110,60,30),width=3)
    text(d,(cx-20,cy),label,40,(255,255,255))
_cache={}
def tts(s):
    if s not in _cache:
        x,sr=pyopenjtalk.tts(s,speed=1.25); x=np.clip(x,-32768,32767).astype(np.int16)
        if sr!=SR: raise SystemExit("sr")
        _cache[s]=x
    return _cache[s]
def save(im,say,minsec=3.0,mood="smile"):
    d=ImageDraw.Draw(im); egg(d,mood=mood)
    a=tts(say); dur=max(minsec,len(a)/SR+0.4)
    p=os.path.join(FR,f"f{len(scenes):04d}.png"); im.save(p); scenes.append((p,dur))
    pad=np.zeros(int(dur*SR)-len(a),dtype=np.int16); audio.append(np.concatenate([a,pad]))
def rnd(n): return (n+5)//10*10

def intro():
    im,d=new()
    text(d,(W/2,190),"わり算は「何回入る？」ゲーム",64,BLUE)
    for i in range(7): cookie(d,330+i*100,330)
    text(d,(W/2,450),"ざっくり予想 → たしかめ で かんたん！",44,ORANGE)
    text(d,(W/2,560),"まちがえても だいじょうぶ！",40,GREEN)
    save(im,"こんにちは。たまごせんせいだよ。きょうは、わりざんを、いっしょにやってみよう。わりざんは、なんかい、はいるかな？ゲームなんだ。ざっくりよそうして、たしかめれば、かんたんだよ。")
def section(t,sub,say):
    im,d=new(); text(d,(W/2,290),t,80,BLUE); text(d,(W/2,420),sub,42); save(im,say,3)
def question(A,B,say_long=True):
    im,d=new()
    text(d,(W/2,150),f"{A} ÷ {B}",130,BLUE)
    wallet(d,330,350,f"{A}円")
    text(d,(W/2-40,350),"で",44)
    cookie(d,800,350,50); text(d,(800,430),f"1こ {B}円",36,GREEN)
    text(d,(W/2,540),f"{A}円で、{B}円の クッキーは 何こ買える？",46)
    text(d,(W/2,620),f"{A}の中に {B}が 何回入るか を考えるのが わり算",34,ORANGE)
    say=(f"{kan(A)}円で、{kan(B)}円のクッキーは、なんこ買えるかな？これを、{kan(A)} わる {kan(B)}、と書くよ。{kan(A)}の中に、{kan(B)}が、なんかい入るか、を考えるのが、わりざんだよ。"
         if say_long else f"{kan(A)} わる {kan(B)}。{kan(B)}円のクッキーを、{kan(A)}円で、なんこ買えるかな？")
    save(im,say,5)
def bars(A,B):
    q=A//B; r=A-q*B; scale=1100/((q+1)*B); x0=90; cols=[BLUE,GREEN,ORANGE]
    for k in range(1,q+2):
        im,d=new()
        text(d,(W/2,70),f"{A} ÷ {B}   {B}円の クッキーを 買っていこう",40)
        d.rounded_rectangle([x0,150,x0+A*scale,230],8,outline=INK,width=4,fill=(255,255,255))
        text(d,(x0+A*scale/2,190),f"持ってるお金 {A}円",36)
        for i in range(k):
            xs=x0+i*B*scale; xe=xs+B*scale; over=(i==q); c=RED if over else cols[i%3]
            d.rounded_rectangle([xs+2,290,xe-2,370],8,fill=c)
            cookie(d,(xs+xe)/2,330,max(14,min(26,(xe-xs)/2-6)))
            text(d,((xs+xe)/2,405),f"{i+1}こ目",26,c)
        if k<=q:
            text(d,(W/2,520),f"{k}こで {B*k}円   （のこり {A-B*k}円）",46)
            text(d,(W/2,610),"まだ買える！ つづけよう",36,GREEN)
            say=f"{kan(k)}こ目。ぜんぶで、{kan(B*k)}円。のこりは、{kan(A-B*k)}円。まだ、買えるよ。"
            if k==1: say=f"まず、{kan(B)}円のクッキーを、一こ買うよ。のこりは、{kan(A-B)}円。まだまだ買えるね。"
            save(im,say,3,"smile")
        else:
            text(d,(W/2,520),f"{k}こ目は {B*k}円 … {A}円を こえちゃった！",46,RED)
            text(d,(W/2,610),f"買えるのは {q}こ まで。あまりは {r}円",42,RED)
            save(im,f"{kan(k)}こ目は、{kan(B*k)}円で、{kan(A)}円をこえちゃう！だから、買えるのは、{kan(q)}こまで。おつりの、あまりは、{kan(r)}円だよ。",4,"o")
def estimate(A,B):
    a,b=rnd(A),rnd(B); e=a//b
    im,d=new()
    text(d,(W/2,70),"ざっくり作戦：切りのいい数に近づけよう",46,BLUE)
    text(d,(W/2,190),f"{B} は {b} に近い",48); text(d,(W/2,270),f"{A} は {a} に近い",48)
    text(d,(W/2,400),f"{a} ÷ {b} = {e}",90,GREEN)
    text(d,(W/2,520),f"だから「だいたい {e}回」と 予想！",48)
    text(d,(W/2,610),"（ほんとうに合ってるか、次でたしかめるよ）",32,ORANGE)
    save(im,f"一つ一つ入れていくのは、たいへんだよね。そこで、ざっくり作戦。{kan(B)}は、{kan(b)}に近いね。{kan(A)}は、{kan(a)}に近いね。{kan(a)} わる {kan(b)} は、{kan(e)}。だから、だいたい、{kan(e)}回だと、よそうするよ。つぎに、ほんとうに合ってるか、たしかめよう。",8)
    return e
def check(A,B,e):
    q=A//B; cur=e
    while True:
        p=B*cur; im,d=new()
        text(d,(W/2,70),f"たしかめ：{B} × {cur} をけいさん",46,BLUE)
        text(d,(W/2,200),f"{B} × {cur} = {p}",90)
        if p>A:
            text(d,(W/2,350),f"{p} は {A} より 大きい！",54,RED)
            text(d,(W/2,450),f"入りすぎ → {cur} を 1 へらして {cur-1} に",50,RED)
            save(im,f"{kan(B)} かける {kan(cur)} は、{kan(p)}。{kan(A)}より、大きいね。入りすぎだ。だから、{kan(cur)}を、一つへらして、{kan(cur-1)}にしよう。",6,"o"); cur-=1; continue
        rem=A-p
        text(d,(W/2,320),f"{A} - {p} = {rem}   これが「あまり」",54)
        if rem>=B:
            text(d,(W/2,430),f"あまり {rem} は {B} 以上 → まだ入る！",50,RED)
            text(d,(W/2,520),f"少なかった → {cur} を 1 ふやして {cur+1} に",50,RED)
            save(im,f"{kan(B)} かける {kan(cur)} は、{kan(p)}。{kan(A)} ひく {kan(p)} は、{kan(rem)}。あまりの{kan(rem)}は、{kan(B)}より、大きいから、まだ入るよ。{kan(cur)}を、一つふやして、{kan(cur+1)}にしよう。",6,"o"); cur+=1; continue
        text(d,(W/2,430),f"あまり {rem} は {B} より小さい → OK！",50,GREEN)
        text(d,(W/2,520),"あまりは、わる数より 小さくなるのがルール",36,ORANGE)
        save(im,f"{kan(B)} かける {kan(cur)} は、{kan(p)}。{kan(A)} ひく {kan(p)} は、{kan(rem)}。あまりの{kan(rem)}は、{kan(B)}より、小さいね。だから、これで、せいかい。あまりは、わる数より、小さくなるのが、ルールだよ。",6); break
    assert cur==q
def hissan(A,B,num,fin=True):
    brief=num not in '①②'
    q=A//B; p=B*q; r=A-p; ds=str(A); n=len(ds); cw=100; x0=480; y0=240
    for stage in (1,2,3):
        im,d=new()
        text(d,(W/2,50),f"{num}  {A} ÷ {B}  の 筆算",44,BLUE)
        d.line([x0-20,y0-45,x0-20,y0+55],fill=INK,width=5); d.line([x0-20,y0-45,x0+n*cw+10,y0-45],fill=INK,width=5)
        text(d,(x0-80,y0),f"{B}",64,INK,"rm")
        for i,c in enumerate(ds): text(d,(x0+i*cw+cw/2,y0),c,64)
        col=lambda k:x0+(n-1-k)*cw+cw/2
        text(d,(col(0),y0-90),f"{q}",64,RED)
        cap=f"① {A} の中に {B} が {q}回 入る → 一の位に {q} をたてる"
        say=f"まず、{kan(A)}の中に、{kan(B)}が、なんかい入るかな？{kan(q)}回。だから、一のくらいに、{kan(q)}を書くよ。"
        if stage>=2:
            for k,c in enumerate(reversed(str(p))): text(d,(col(k),y0+90),c,64,GREEN)
            d.line([x0-10,y0+135,x0+n*cw,y0+135],fill=INK,width=4)
            cap=f"② {B} × {q} = {p} を下に書く"
            say=f"つぎに、かけ算。{kan(B)} かける {kan(q)} は、{kan(p)}。これを、下に書くよ。"
        if stage>=3:
            for k,c in enumerate(reversed(str(r))): text(d,(col(k),y0+190),c,64,ORANGE)
            cap=f"③ {A} - {p} = {r}"+("  あまり" if r else "  ぴったり！")
            say=f"さいごに、ひき算。{kan(A)} ひく {kan(p)} は、{kan(r)}。"+(f"あまりは、{kan(r)}。" if r else "ぴったり、わりきれたね。")+f"答えは、{kan(q)}"+(f"、あまり、{kan(r)}。" if r else "。")+f"たしかめは、{kan(B)} かける {kan(q)}"+(f" たす {kan(r)}" if r else "")+f"、で、{kan(A)}。せいかい。"
        if brief:
            say=[f"{kan(A)}の中に、{kan(B)}は、{kan(q)}回。{kan(q)}をたてる。",f"{kan(B)} かける {kan(q)} は、{kan(p)}。",
                 f"{kan(A)} ひく {kan(p)} は、{kan(r)}。答えは、{kan(q)}"+(f"、あまり、{kan(r)}。" if r else "。")][stage-1]
        text(d,(W/2,540),cap,44)
        if stage==3: text(d,(W/2,625),f"答え  {q}"+(f" あまり {r}" if r else "")+f"    たしかめ  {B}×{q}"+(f"+{r}" if r else "")+f" = {A}",40,BLUE)
        save(im,say,2.5)
def outro():
    im,d=new(); text(d,(W/2,150),"まとめ",70,BLUE)
    for i,s in enumerate(["① 「何回入る？」と考える","② 切りのいい数で ざっくり予想","③ かけ算でたしかめて、大きすぎ・小さすぎは 1 ちょうせい","④ あまりは わる数より 小さい"]): text(d,(W/2,270+i*80),s,42)
    text(d,(W/2,640),"まちがえても大丈夫！ 直せたらそれが成長",36,GREEN)
    save(im,"まとめだよ。一つ、なんかい入るかな、と考える。二つ、切りのいい数で、ざっくりよそう。三つ、かけ算でたしかめて、大きすぎたら、一つへらす。小さすぎたら、一つふやす。四つ、あまりは、わる数より、小さい。まちがえても、だいじょうぶ。直せたら、それが、せいちょうだよ。またね！",8)

intro()
for n_,(A,B) in zip("①②",[(359,58),(180,34)]):
    section(f"{n_} {A} ÷ {B}","ていねいに やってみよう" if A==359 else "予想がズレる れいだい",f"{n_.translate(str.maketrans('①②','一二'))}ばんめの、もんだい。{kan(A)} わる {kan(B)}。")
    question(A,B); bars(A,B); e=estimate(A,B); check(A,B,e); hissan(A,B,n_)
section("③〜⑫","ざっくり予想 → 筆算 → たしかめ","ここからは、三ばんから、十二ばんまで、れんしゅうだよ。ざっくりよそう、ひっさん、たしかめ、の じゅんばんでいくよ。")
for n_,(A,B) in zip("③④⑤⑥⑦⑧⑨⑩⑪⑫",[(635,79),(101,25),(259,37),(400,58),(172,26),(191,24),(100,28),(145,29),(272,39),(190,28)]):
    q=A//B; e=rnd(A)//rnd(B)
    im,d=new(); text(d,(W/2,100),n_,60,ORANGE); text(d,(W/2,240),f"{A} ÷ {B}",120,BLUE)
    for i in range(5): cookie(d,440+i*100,370,28)
    text(d,(W/2,470),f"ざっくり {rnd(A)} ÷ {rnd(B)} → だいたい {e}回",46)
    text(d,(W/2,560),f"{B}円の クッキーが {A}円で 何こ買える？",36,GREEN)
    save(im,f"{kan(A)} わる {kan(B)}。ざっくり、{kan(rnd(A))} わる {kan(rnd(B))}。だいたい、{kan(e)}回、とよそうするよ。",5)
    if e!=q:
        im,d=new(); text(d,(W/2,230),f"予想の {e} から {q} に ちょうせい！",54,RED)
        t=f"{B} × {e} = {B*e}"+("  → 大きすぎ！" if B*e>A else f"  → あまり {A-B*e} が {B} 以上、まだ入る！")
        text(d,(W/2,370),t,46,RED)
        say=f"たしかめるよ。{kan(B)} かける {kan(e)} は、{kan(B*e)}。"+("大きすぎるから、一つへらして、"+kan(q)+"。" if B*e>A else f"あまりが、{kan(B)}以上だから、まだ入る。一つふやして、{kan(q)}。")
        save(im,say,5,"o")
    hissan(A,B,n_)
outro()

with open(os.path.join(OUT,"list.txt"),"w") as f:
    for p,s in scenes: f.write(f"file '{p}'\nduration {s:.3f}\n")
    f.write(f"file '{scenes[-1][0]}'\n")
wp=os.path.join(OUT,"voice.wav")
with wave.open(wp,"wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.concatenate(audio).tobytes())
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",os.path.join(OUT,"list.txt"),"-i",wp,
  "-vf","fps=24,format=yuv420p","-c:v","libx264","-c:a","aac","-b:a","128k","-shortest",os.path.join(OUT,"warizan_voice.mp4")],check=True)
print("scenes",len(scenes),"sec",round(sum(s for _,s in scenes)))
