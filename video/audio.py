import json, numpy as np, wave
SR = 44100
d = json.load(open('events.json')); ev = d['ev']
fin = [e['t'] for e in ev if e['name'] == 'finish'][0]
DUR = fin + 0.4
N = int(DUR * SR); out = np.zeros(N)
def env(n, a=0.005, decay=None):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a)
    return e * (np.exp(-t / decay) if decay else 1)
def add(t0, sig, vol=1.0):
    i = int(t0 * SR)
    if i >= N: return
    j = min(N, i + len(sig)); out[i:j] += sig[:j - i] * vol
def osc(kind, f, dur, slide=None):
    n = int(dur * SR); t = np.arange(n) / SR
    fr = f if slide is None else f * (slide / f) ** (t / dur)
    ph = 2 * np.pi * np.cumsum(fr) / SR
    if kind == 'sine': return np.sin(ph)
    if kind == 'tri': return 2 / np.pi * np.arcsin(np.sin(ph))
def note(kind, f, dur, vol, decay, slide=None): return osc(kind, f, dur, slide) * env(int(dur * SR), decay=decay) * vol
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)

# BGM（ゲームと同じ曲：ヘ長調・104BPM）
MEL = [[69,0,72,0,69,67,65,0],[67,0,72,0,76,0,74,72],[74,0,77,0,76,74,72,0],[74,0,72,70,69,0,67,0],
       [69,72,77,0,76,0,72,0],[67,0,76,0,74,72,74,0],[74,72,70,0,67,69,70,0],[69,0,65,0,65,0,0,0]]
CH = {'F':[65,69,72],'C':[64,67,72],'Dm':[62,65,69],'Bb':[62,65,70]}
RT = {'F':41,'C':36,'Dm':38,'Bb':34}
PR = [['F'],['C'],['Dm'],['Bb'],['F'],['C'],['Bb','C'],['F']]
bgm = np.zeros(N); rng = np.random.default_rng(1)
eighth = 60 / 104 / 2; s = 0; t = 0.0
def badd(t0, sig, vol):
    i = int(t0 * SR)
    if i >= N: return
    j = min(N, i + len(sig)); bgm[i:j] += sig[:j - i] * vol
while t < DUR:
    bar, i = (s >> 3) % 8, s & 7
    ch = PR[bar][1 if len(PR[bar]) > 1 and i >= 4 else 0]
    m = MEL[bar][i]
    if m: badd(t, note('sine', mtof(m), .45, .2, .16), 1); badd(t, note('sine', mtof(m) * 4, .08, .035, .025), 1)
    r = RT[ch]
    if i == 0: badd(t, note('tri', mtof(r), .35, .3, .14), 1)
    if i == 4: badd(t, note('tri', mtof(r + 7), .3, .26, .12), 1)
    if i == 6: badd(t, note('tri', mtof(r + 12), .18, .18, .07), 1)
    if i in (2, 6):
        for k, n_ in enumerate(CH[ch]): badd(t + k * .012, note('tri', mtof(n_), .22, .045, .08), 1)
    if i in (0, 4): badd(t, note('sine', 140, .14, .32, .05, slide=45), 1)
    if i % 2:
        n = int(.05 * SR); hh = rng.uniform(-1, 1, n); hh = hh - np.convolve(hh, np.ones(4) / 4, 'same')
        badd(t, hh * env(n, .001, .012) * .06, 1)
    s += 1; t += eighth
fade = np.ones(N); fi = int(.6 * SR); fade[:fi] = np.linspace(0, 1, fi)
fo = int(1.2 * SR); fade[-fo:] = np.linspace(1, 0, fo)
out += bgm * fade * 0.85

# 効果音
def pop(t0, f, vol=.5):
    add(t0, note('tri', f, .12, vol, .05)); add(t0 + .04, note('sine', f * 1.5, .18, vol * .6, .07))
for e in ev:
    t0, nm, x = e['t'], e['name'], e.get('extra')
    if nm == 'land': add(t0, note('sine', 160, .25, .6, .08, slide=60))
    elif nm == 'crack':
        n = int(.08 * SR); add(t0, rng.uniform(-1, 1, n) * env(n, .001, .02) * .5); pop(t0 + .05, 660, .45); pop(t0 + .15, 990, .4)
    elif nm == 'whoosh':
        n = int(.4 * SR); w = rng.uniform(-1, 1, n); w = np.convolve(w, np.ones(12) / 12, 'same')
        add(t0, w * np.sin(np.linspace(0, np.pi, n)) * .7)
    elif nm == 'title':
        for k, f in enumerate([784, 988, 1319]): add(t0 + k * .11, note('tri', f, .35 if k == 2 else .14, .35, .12))
    elif nm == 'drop': add(t0, note('sine', 420, .1, .25, .04, slide=260))
    elif nm == 'merge':
        f = 330 * 1.122 ** (x); pop(t0, f, .5)
        if x >= 7: add(t0, note('sine', 90, .5, .5, .18, slide=45))
        if x == 10:
            add(t0, note('sine', 70, .9, .9, .35, slide=30)); add(t0, note('tri', 55, .9, .5, .3, slide=28))
            for k, f2 in enumerate([784, 988, 1319, 1568]): add(t0 + .25 + k * .1, note('tri', f2, .4 if k == 3 else .14, .3, .12))
    elif nm == 'tick': pop(t0, 520 * 1.07 ** len([q for q in ev if q['name'] == 'tick' and q['t'] < t0]), .3)
    elif nm == 'end':
        for k, f in enumerate([523, 659, 784, 1047]): add(t0 + k * .12, note('tri', f, .5 if k == 3 else .15, .35, .15))

out = out / np.max(np.abs(out)) * 0.89
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print('dur', round(DUR, 2), 'offset', d['offset'])
