#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PILOTO do corte no formato melhorado (crivo do Pesquisador):
- SEM capa parada: vídeo já em movimento no frame 0
- título ENTRA animado sobre o vídeo (gancho nos primeiros segundos)
- vídeo maior + fundo P&B em movimento (mais imersão que a janelinha)
- logo + @ da marca leves e persistentes (identidade mantida)
- P&B alto contraste
- fecho: SALVA/COMPARTILHA, canal como menção leve
Entrega o piloto no preview do Estúdio pra o Diretor ver (não posta)."""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

M = "/opt/cortes/contas/opoderdamentesabia/marca"
LOGO = M + "/logo.png"
SRC = "/opt/automacao/marcas/opoder/youtube/frontend/previews/video-02.mp4"
OUTDIR = "/opt/automacao/marcas/opoder/youtube/frontend/previews"
BEBAS = "/usr/share/fonts/truetype/bebasneue/BebasNeue-Regular.ttf"
INI, DUR = 110.3, 30.0
TITULO = "DISCIPLINA VENCE MOTIVAÇÃO"
os.makedirs("/tmp/pil", exist_ok=True)


def fnt(s):
    try:
        return ImageFont.truetype(BEBAS, s)
    except Exception:
        return ImageFont.load_default()


_probe = ImageDraw.Draw(Image.new("RGB", (4, 4)))


def linhas(txt, f, maxw):
    if _probe.textlength(txt, font=f) <= maxw:
        return [txt]
    w = txt.split()
    best = None
    for i in range(1, len(w)):
        a, b = " ".join(w[:i]), " ".join(w[i:])
        wa, wb = _probe.textlength(a, font=f), _probe.textlength(b, font=f)
        if wa <= maxw and wb <= maxw and (best is None or abs(wa - wb) < best[0]):
            best = (abs(wa - wb), [a, b])
    return best[1] if best else [txt]


def cen(d, t, y, f, fill, W=1080, sh=(0, 0, 0, 200)):
    w = d.textlength(t, font=f)
    d.text(((W - w) / 2 + 2, y + 2), t, font=f, fill=sh)
    d.text(((W - w) / 2, y), t, font=f, fill=fill)


# 1) PERSISTENTE: logo pequeno no topo + @ no rodapé (marca leve, sem tapar o vídeo)
persist = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
d = ImageDraw.Draw(persist)
try:
    lg = Image.open(LOGO).convert("RGBA")
    lg.thumbnail((150, 150), Image.LANCZOS)
    persist.paste(lg, (int((1080 - lg.width) / 2), 40), lg)
except Exception as e:
    print("[logo]", e)
cen(d, "@opoderdamentesabia", 1815, fnt(40), (235, 238, 245, 235))
persist.save("/tmp/pil/persist.png")

# 2) TÍTULO (entra animado sobre o vídeo, área superior sobre o fundo)
title = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
d = ImageDraw.Draw(title)
ft = fnt(66)
ls = linhas(TITULO, ft, 960)
y0 = 300 if len(ls) == 2 else 335
passo = int(ft.size * 1.1)
for i, ln in enumerate(ls):
    cen(d, ln, y0 + i * passo, ft, (255, 255, 255, 255))
title.save("/tmp/pil/title.png")

# 3) CTA final (últimos segundos): SALVA/COMPARTILHA + canal como menção leve
cta = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
d = ImageDraw.Draw(cta)
d.rectangle([0, 1440, 1080, 1720], fill=(6, 7, 13, 180))
cen(d, "🔖  SALVA PRA REOUVIR", 1470, fnt(52), (46, 230, 168, 255))
cen(d, "manda pra quem precisa disso", 1545, fnt(38), (235, 238, 245, 235))
cen(d, "as 5 leis completas no canal", 1615, fnt(40), (201, 205, 216, 235))
cen(d, "@opoderdamentesabia", 1665, fnt(40), (255, 255, 255, 245))
cta.save("/tmp/pil/cta.png")

# ffmpeg: fundo P&B em movimento (cobre a tela) + vídeo nítido maior + overlays
out = OUTDIR + "/piloto.mp4"
filtro = (
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
    "boxblur=20:2,hue=s=0,eq=contrast=1.12:brightness=-0.16[bg];"
    "[0:v]scale=1080:-2,hue=s=0,eq=contrast=1.18:brightness=0.02,setsar=1[fg];"
    "[bg][fg]overlay=(W-w)/2:(H-h)/2[b1];"
    "[b1][1:v]overlay=0:0[b2];"
    "[2:v]format=rgba,fade=t=in:st=0.3:d=0.6:alpha=1,fade=t=out:st=4.7:d=0.6:alpha=1[titf];"
    "[b2][titf]overlay=0:0:enable='between(t,0,5.4)'[b3];"
    "[3:v]format=rgba,fade=t=in:st=26:d=0.5:alpha=1[ctaf];"
    "[b3][ctaf]overlay=0:0:enable='gte(t,26)',format=yuv420p[v]"
)
subprocess.run([
    "ffmpeg", "-y", "-v", "error",
    "-ss", str(INI), "-t", str(DUR), "-i", SRC,
    "-loop", "1", "-i", "/tmp/pil/persist.png",
    "-loop", "1", "-i", "/tmp/pil/title.png",
    "-loop", "1", "-i", "/tmp/pil/cta.png",
    "-filter_complex", filtro, "-map", "[v]", "-map", "0:a",
    "-t", str(DUR), "-r", "30", "-fps_mode", "cfr",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out
], check=True, timeout=600)
info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                       "-show_entries", "stream=duration,nb_read_packets", "-of", "csv=p=0", out],
                      capture_output=True, text=True).stdout.strip()
print("PILOTO PRONTO:", out, "| frames/dur:", info)
