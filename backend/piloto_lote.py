#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SÉRIE das 5 Leis no formato viral (crivo do Pesquisador): gancho em movimento no frame 0,
título animado com contraste garantido, P&B alto contraste imersivo, @ leve, fecho salva/compartilha.
Gera os 5 cortes + legendas na pasta de cortes prontos do Estúdio."""
import json
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

SRC = "/opt/automacao/marcas/opoder/youtube/frontend/previews/video-02.mp4"
DEST = "/opt/automacao/marcas/opoder/youtube/data/cortes"
PREV = "/opt/automacao/marcas/opoder/youtube/frontend/previews"
BEBAS = "/usr/share/fonts/truetype/bebasneue/BebasNeue-Regular.ttf"
os.makedirs(DEST, exist_ok=True)
os.makedirs("/tmp/lote", exist_ok=True)
_p = ImageDraw.Draw(Image.new("RGB", (4, 4)))

# (nome, ini, dur, titulo, legenda)
LEIS = [
    ("lei1_responsabilidade", 68.4, 31.4, "RESPONSABILIDADE TOTAL",
     "Enquanto a culpa é do governo, do chefe ou da sorte, a solução também fica na mão deles. Responsabilidade total é pegar o volante de volta. \U0001F9E0 Essa é 1 das 5 Leis que reprogramam a mente. Salva pra reouvir e manda pra quem precisa. As 5 completas no canal @opoderdamentesabia. #mentalidade #responsabilidade #napoleonhill #foco #disciplina"),
    ("lei2_disciplina", 110.3, 29.7, "DISCIPLINA VENCE MOTIVAÇÃO",
     "Disciplina vence motivação: quem depende de estar motivado vive refém do próprio humor. Sistema, não vontade. \U0001F9E0 Uma das 5 Leis que reprogramam a mente. Salva pra reouvir. As 5 no canal @opoderdamentesabia. #mentalidade #disciplina #napoleonhill #motivacao #foco"),
    ("lei3_ambiente", 150.3, 31.4, "SEU AMBIENTE MOLDA VOCÊ",
     "Você é a média das 5 pessoas com quem mais convive. Seu ambiente é mais forte que sua força de vontade — proteja sua mente como um cofre. \U0001F9E0 1 das 5 Leis. Salva e compartilha. As 5 no canal @opoderdamentesabia. #mentalidade #ambiente #disciplina #desenvolvimentopessoal"),
    ("lei4_preco", 190.7, 30.8, "PAGUE O PREÇO PRIMEIRO",
     "A vida cobra adiantado: primeiro o esforço, depois a recompensa. O perdedor quer o prêmio antes e nunca sai do lugar. \U0001F9E0 1 das 5 Leis que reprogramam a mente. Salva pra reouvir. As 5 no canal @opoderdamentesabia. #mentalidade #disciplina #sucesso #napoleonhill"),
    ("lei5_medo", 231.84, 30.7, "AJA COM MEDO",
     "A 5ª lei que quase ninguém tem coragem de aplicar: aja com medo. O medo não é fraqueza — é sinal de que aquilo importa. Do outro lado dele está a vida que você pediu. \U0001F9E0 Salva e manda pra quem precisa. As 5 no canal @opoderdamentesabia. #mentalidade #coragem #napoleonhill #foco"),
]


def fnt(s):
    try:
        return ImageFont.truetype(BEBAS, s)
    except Exception:
        return ImageFont.load_default()


def linhas(txt, f, maxw):
    if _p.textlength(txt, font=f) <= maxw:
        return [txt]
    w = txt.split(); best = None
    for i in range(1, len(w)):
        a, b = " ".join(w[:i]), " ".join(w[i:])
        wa, wb = _p.textlength(a, font=f), _p.textlength(b, font=f)
        if wa <= maxw and wb <= maxw and (best is None or abs(wa - wb) < best[0]):
            best = (abs(wa - wb), [a, b])
    return best[1] if best else [txt]


def cen(d, t, y, f, fill, W=1080, sh=(0, 0, 0, 220)):
    w = d.textlength(t, font=f)
    d.text(((W - w) / 2 + 3, y + 3), t, font=f, fill=sh)
    d.text(((W - w) / 2, y), t, font=f, fill=fill)


# overlays fixos (iguais p/ todos): @ no rodapé + CTA final
persist = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
cen(ImageDraw.Draw(persist), "@opoderdamentesabia", 1820, fnt(42), (240, 243, 250, 240))
persist.save("/tmp/lote/persist.png")

cta = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
d = ImageDraw.Draw(cta)
d.rectangle([0, 1430, 1080, 1730], fill=(6, 7, 13, 190))
cen(d, "\U0001F516  SALVA PRA REOUVIR", 1465, fnt(54), (46, 230, 168, 255))
cen(d, "manda pra quem precisa disso", 1543, fnt(38), (235, 238, 245, 235))
cen(d, "as 5 leis completas no canal", 1615, fnt(40), (201, 205, 216, 235))
cen(d, "@opoderdamentesabia", 1667, fnt(42), (255, 255, 255, 250))
cta.save("/tmp/lote/cta.png")


def faz_titulo(titulo, path):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ft = fnt(70)
    ls = linhas(titulo, ft, 980)
    passo = int(ft.size * 1.08)
    alt = passo * len(ls)
    y0 = 320
    # faixa escura de contraste atrás do título (garante leitura em qualquer cena)
    d.rectangle([0, y0 - 40, 1080, y0 + alt + 30], fill=(6, 7, 13, 150))
    for i, ln in enumerate(ls):
        cen(d, ln, y0 + i * passo, ft, (255, 255, 255, 255))
    img.save(path)


FILT = (
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
    "boxblur=20:2,hue=s=0,eq=contrast=1.12:brightness=-0.16[bg];"
    "[0:v]scale=1080:-2,hue=s=0,eq=contrast=1.18:brightness=0.02,setsar=1[fg];"
    "[bg][fg]overlay=(W-w)/2:(H-h)/2[b1];"
    "[b1][1:v]overlay=0:0[b2];"
    "[2:v]format=rgba,fade=t=in:st=0.3:d=0.6:alpha=1,fade=t=out:st=4.9:d=0.6:alpha=1[titf];"
    "[b2][titf]overlay=0:0:enable='between(t,0,5.6)'[b3];"
    "[3:v]format=rgba,fade=t=in:st={cta}:d=0.5:alpha=1[ctaf];"
    "[b3][ctaf]overlay=0:0:enable='gte(t,{cta})',format=yuv420p[v]"
)

feitos = []
for nome, ini, dur, titulo, legenda in LEIS:
    faz_titulo(titulo, "/tmp/lote/title.png")
    out = f"{DEST}/{nome}.mp4"
    cta_t = round(dur - 4.0, 1)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", str(ini), "-t", str(dur), "-i", SRC,
        "-loop", "1", "-i", "/tmp/lote/persist.png",
        "-loop", "1", "-i", "/tmp/lote/title.png",
        "-loop", "1", "-i", "/tmp/lote/cta.png",
        "-filter_complex", FILT.format(cta=cta_t), "-map", "[v]", "-map", "0:a",
        "-t", str(dur), "-r", "30", "-fps_mode", "cfr",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out
    ], check=True, timeout=600)
    open(f"{DEST}/{nome}.txt", "w", encoding="utf-8").write(legenda)
    feitos.append(nome)
    print("[ok]", nome, "->", out)

# a mais forte (lei5) vai pro preview pra o Diretor ver / eu postar
import shutil
shutil.copy(f"{DEST}/lei5_medo.mp4", f"{PREV}/piloto_lei5.mp4")
json.dump({"cortes": feitos, "criado_em": "2026-07-17"},
          open(f"{DEST}/serie.json", "w", encoding="utf-8"), ensure_ascii=False)
print("SERIE PRONTA:", len(feitos), "cortes em", DEST)
