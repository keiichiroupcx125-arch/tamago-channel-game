# 録画（webm）の時間の伸びを、吹き出しが出た時刻を目印に直して、events.json の時刻どおりの30fps動画を作る
import json, subprocess, numpy as np
d = json.load(open('events.json')); off = d['offset']; src = d['path']
ev = d['ev']; fin = [e['t'] for e in ev if e['name'] == 'finish'][0]; DUR = fin + 0.4
voice_t = {e['extra']: e['t'] for e in ev if e['name'] == 'voice'}
# 吹き出しエリアの変化を検出
W, H = 108, 192
g = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', src, '-vf', 'scale=108:192,format=gray', '-f', 'rawvideo', '-vsync', '0', '-'], capture_output=True).stdout
fr = np.frombuffer(g, np.uint8).reshape(-1, H, W).astype(float)
pts = np.array([float(x) for x in subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'frame=pts_time', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.split() if x])[:len(fr)]
# 吹き出しの中に文字（暗い点）が出はじめた瞬間 = セリフ表示
dark = (fr[:, 168:184, 6:102] < 90).mean((1, 2))
dif = np.r_[0, np.abs(fr[1:, 168:184] - fr[:-1, 168:184]).mean((1, 2))]
ons = []
for i in range(1, len(fr) - 6):
    if pts[i] <= off or dif[i] <= 4: continue
    if dark[i] > 0.02 and abs(dark[i] - dark[i - 1]) > 0.005:  # 吹き出しに新しい文字が出た
        if not ons or pts[i] - ons[-1] > 0.3: ons.append(pts[i])
anc = [(0.0, off)]
for k in sorted(voice_t):
    t = voice_t[k]; v0 = anc[-1][1]
    v = [c for c in ons if c > v0 + 0.3][0]
    anc.append((t, v)); print('voice', k, 'event', round(t, 2), 'video', round(v - off, 2))
anc = anc[1:]  # 先頭は外挿
tt = np.array([a[0] for a in anc]); vv = np.array([a[1] for a in anc])
def vmap(t):
    if t <= tt[0]: return vv[0] + (t - tt[0]) * (vv[1] - vv[0]) / (tt[1] - tt[0])
    if t >= tt[-1]: return vv[-1] + (t - tt[-1]) * (vv[-1] - vv[-2]) / (tt[-1] - tt[-2])
    return np.interp(t, tt, vv)
# 出力フレームごとに元フレームを選んで書き出し
FW, FH = 1080, 1920
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-vf', f'scale={FW}:{FH}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-vsync', '0', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{FW}x{FH}', '-r', '30', '-i', '-', '-i', 'audio.wav',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', 'short_v2_voice.mp4'], stdin=subprocess.PIPE)
fsz = FW * FH * 3; idx = -1; cur = None
for n in range(int(DUR * 30)):
    want = int(np.searchsorted(pts, vmap(n / 30), 'right') - 1); want = max(0, min(want, len(pts) - 1))
    while idx < want:
        b = dec.stdout.read(fsz)
        if len(b) < fsz: break
        cur = b; idx += 1
    enc.stdin.write(cur)
enc.stdin.close(); enc.wait(); dec.kill()
print('done', DUR)
