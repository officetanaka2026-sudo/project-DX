#!/usr/bin/env python3
"""HP見本を作る: python3 make_hp.py config.json -> samples/<slug>/index.html
写真は Googleマップの lh3 URL（=w の前まで）を photos に入れる。"""
import json,sys,os,html,urllib.parse as up
E=html.escape
c=json.load(open(sys.argv[1],encoding='utf-8'))
d=os.path.dirname(os.path.abspath(__file__))
css=open(os.path.join(d,'base.css'),encoding='utf-8').read()
v=c.get('vars',{})
root=':root{--sea:%s;--sand:%s;--ink:%s;--sub:%s;--accent:%s;--line:%s}'%(v.get('sea','#2f6b85'),v.get('sand','#f7f2ea'),v.get('ink','#2d2a26'),v.get('sub','#6d675f'),v.get('accent','#b8734a'),v.get('line','#e6ddd0'))
css=css.split('\n',1)[1] if css.startswith('\n') else css
import re
css=re.sub(r':root\{[^}]*\}',root,css,count=1)
extra=c.get('css','')
P={k:(v if v.startswith('http') else 'https://lh3.googleusercontent.com/gps-cs-s/'+v) for k,v in c['photos'].items()}
def img(k,alt=''):
    return f'<img src="{P[k]}=w1600" alt="{E(alt)}">'
nav=''.join(f'<a href="#{h}">{E(t)}</a>' for h,t in [('about','お店について'),('menu',c.get('menu_label','こだわり')),('gallery','ギャラリー'),('info','営業案内')])
pts=''.join(f'<div><div class="photo">{img(p["photo"],p["title"])}</div><div class="num">0{i+1}</div><h3>{E(p["title"])}</h3><p>{E(p["text"])}</p></div>' for i,p in enumerate(c['points']))
gal=''.join(f'<div class="{cl}">{img(k)}</div>' for cl,k in zip(['t','w','','','w'],c['gallery']))
voi=''.join(f'<div class="v"><div class="star">★★★★★</div>{E(t)}</div>' for t in c['voices'])
rows=''.join(f'<tr><th>{E(k)}</th><td>{E(vv).replace("&lt;br&gt;","<br>")}</td></tr>' for k,vv in c['info'])
btn=f'<a class="btn" href="{E(c["link"])}">{E(c.get("link_label","Instagram"))}</a>' if c.get('link') else ''
mapq=up.quote(c['map_q'])
fonts=c.get('fonts','family=Shippori+Mincho:wght@500;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Cormorant+Garamond:ital,wght@0,500;1,500')
page=f'''<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{E(c['name'])}｜{E(c['title'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
<style>{css}{extra}</style></head><body>
<header><div class="logo">{E(c['logo'])}<small>{E(c.get('logo_sub',''))}</small></div><nav>{nav}</nav></header>
<div class="hero">{img(c['hero'],'メイン写真')}
 <div class="hero-copy"><h1>{c['h1']}</h1><p>{E(c['lede'])}</p></div>
 <div class="rating"><b>★{E(c['rating'])}</b><span>Googleクチコミ {E(c['reviews'])}件</span></div></div>
<section id="about"><div class="intro">
 <div class="photo">{img(c['about_photo'])}</div>
 <div><div class="head"><div class="en">About us</div><h2>{c['about_h2']}</h2></div>{''.join(f'<p>{x}</p>' for x in c['about'])}</div>
</div></section>
<section id="menu" class="points"><div class="head" style="text-align:center"><div class="en">Our Point</div><h2>{E(c['points_h2'])}</h2></div><div class="pgrid">{pts}</div></section>
<div class="wide">{img(c['wide'])}<div>{c['wide_text']}</div></div>
<section id="gallery"><div class="head"><div class="en">Gallery</div><h2>{E(c.get('gallery_h2','店内の様子'))}</h2></div><div class="gallery">{gal}</div></section>
<section class="voice"><div class="head" style="text-align:center"><div class="en">Voice</div><h2>お客さまの声</h2><p style="color:var(--sub);font-size:13px;margin:0">Googleマップのクチコミより（要約）</p></div><div class="vgrid">{voi}</div></section>
<section id="info"><div class="head"><div class="en">Information</div><h2>営業案内・アクセス</h2></div>
<div class="info"><div><div class="ext">{img(c.get('info_photo',c['hero']))}</div><table>{rows}</table>
<p style="font-size:12px;color:var(--sub)">{E(c.get('info_note','※営業時間は変更になる場合があります。'))}</p>{btn}</div>
<iframe class="map" loading="lazy" src="https://www.google.com/maps?q={mapq}&output=embed"></iframe></div></section>
<footer><div class="logo">{E(c['logo'])}</div>{E(c['address'])}<br>© {E(c['name'])}</footer>
</body></html>'''
out=os.path.join(d,'..',c['slug'],'index.html');os.makedirs(os.path.dirname(out),exist_ok=True)
open(out,'w',encoding='utf-8').write(page);print(os.path.normpath(out))
