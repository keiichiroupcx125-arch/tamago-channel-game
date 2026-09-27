import os, re
FAV = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='46' fill='white' stroke='%231D2742' stroke-width='6'/%3E%3Ccircle cx='50' cy='54' r='21' fill='%23D7263D'/%3E%3C/svg%3E"
YT_URL = 'https://www.youtube.com/@%E3%81%9F%E3%81%BE%E3%81%94%E3%83%9C%E3%83%BC%E3%83%AB-f2j'
YT_CSS = """  .yt {
    display: inline-flex; align-items: center; gap: 8px; font-size: 14px; color: #fff; text-decoration: none;
    background: #E0302E; border: 3px solid #1D2742; border-radius: 999px; padding: 6px 16px 6px 10px; box-shadow: 0 4px 0 #1D2742;
  }
  .yt svg { width: 24px; height: 17px; flex: none; }
  .yt:active { transform: translateY(3px); box-shadow: 0 1px 0 #1D2742; }
  .yt:focus-visible { outline: 3px solid #F5B700; outline-offset: 3px; }
"""
YT_A = f'<a class="yt" href="{YT_URL}" target="_blank" rel="noopener"><svg viewBox="0 0 24 17" aria-hidden="true"><rect width="24" height="17" rx="5" fill="#fff"/><path d="M9.5 4.5v8l6.5-4z" fill="#E0302E"/></svg>YouTubeチャンネルを見る</a>'

def wrap(src, title, desc):
    i = src.index('</style>\n') + len('</style>\n')
    head, body = src[:i], src[i:]
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#7CCBF0">
<link rel="icon" href="{FAV}">
<style>
  [hidden] {{ display: none !important; }}
  :root {{ padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); box-sizing: border-box; height: 100%; }}
  img {{ max-width: 100%; }}
</style>
{head}</head>
<body>
{body}</body>
</html>
'''
def rep(s, a, b):
    assert s.count(a) == 1, a
    return s.replace(a, b)

os.makedirs('site/kuttsuke', exist_ok=True); os.makedirs('site/quiz', exist_ok=True)

# トップ
hub = open('hub_body.html').read()
open('site/index.html', 'w').write(wrap(hub, 'たまごボール ゲーム', '国ボールのゆる雑学チャンネル「たまごボール」のゲーム。国ボール くっつけパズルと国旗クイズで あそべるよ！'))

# くっつけパズル
k = open('kuttsuke.html').read()
k = rep(k, '<div class="brand"><canvas id="brandBall" width="48" height="48"></canvas><span>たまごボール</span></div>',
           '<a class="brand" href="../" aria-label="ゲームえらびに もどる"><span aria-hidden="true">←</span><canvas id="brandBall" width="48" height="48"></canvas><span>たまごボール</span></a>')
k = rep(k, '  .toggles { display: flex; gap: 6px; }', '  .toggles { display: flex; gap: 6px; }\n  a.brand { color: inherit; text-decoration: none; }')
open('site/kuttsuke/index.html', 'w').write(wrap(k, '国ボール くっつけパズル｜たまごボール', '同じ国ボールをくっつけて、ひとつ大きい国を生み出そう！ さいごはロシアを目指せ！'))

# 国旗クイズ
q = open('tamago-quiz.html').read()
q = rep(q, '<title>たまごチャンネル クイズ</title>', '<title>たまごボール 国旗クイズ</title>')
q = rep(q, '<div class="brand" id="brand"></div>', '<a class="ghost" href="../">← ゲームえらび</a>')
q = rep(q, "  $('#brand').innerHTML = `${ball('jp', 'smile')}<span>たまごチャンネル</span>`;\n", '')
q = rep(q, '<h1><small>クイズであそぼう！</small>たまごチャンネル</h1>', '<h1><small>クイズであそぼう！</small>たまごボール</h1>')
q = rep(q, '<p class="note">小学4年生の息子とパパで作っている、国ボールのゆる雑学チャンネル。<br>ゲームは しさく版です。</p>',
           f'<div style="display:grid;justify-items:center;gap:8px;margin-top:22px">{YT_A}<p class="note" style="margin:0">小学4年生の息子とパパで作っている、国ボールのゆる雑学チャンネル。</p></div>')
q = rep(q, '  a.ghost, ', '  a.ghost, ') if '  a.ghost, ' in q else q
q = rep(q, '  /* ボール */', YT_CSS + '  a.ghost { text-decoration: none; }\n  /* ボール */')
assert 'たまごチャンネル' not in q.replace('単一テーマ', ''), [l for l in q.splitlines() if 'たまごチャンネル' in l]
open('site/quiz/index.html', 'w').write(wrap(q, '国旗クイズ｜たまごボール', '国旗・大きさくらべ・ことば・パラオさがし。たまごボールの動画を見た人は きっとわかる！'))
print('ok')
