#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estúdio de Cortes — corta nosso vídeo (fonte limpa), aplica capa+moldura OFICIAIS da marca,
título na moldura acima do vídeo (1 ou 2 linhas conforme couber), cartela-sinal pro YouTube,
e entrega na aprovacao (o bot do Postador pergunta). Junção re-codificada (velocidade normal)."""
import json
import os
import subprocess
import time

from PIL import Image, ImageDraw, ImageFont

M = "/opt/cortes/contas/opoderdamentesabia/marca"
CAPA = M + "/capa.png"
MOLD = M + "/moldura.mp4"
SRC = "/opt/automacao/marcas/opoder/youtube/frontend/previews/video-02.mp4"
APROV = "/opt/automacao/marcas/opoder/motor/contas/opoderdamentesabia/reels/aprovacao"
BEBAS = "/usr/share/fonts/truetype/bebasneue/BebasNeue-Regular.ttf"
FALLBACK = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
INI, DUR = 110.3, 29.0
TITULO = "DISCIPLINA VENCE MOTIVAÇÃO"

os.makedirs(APROV, exist_ok=True)
os.makedirs("/tmp/ce", exist_ok=True)
_probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))


def sh(a):
    subprocess.run(a, check=True)


def tem_acento(caminho):
    try:
        m = ImageFont.truetype(caminho, 40).getmask("Ç")
        return m.getbbox() is not None
    except Exception:
        return False


FONT = BEBAS if tem_acento(BEBAS) else FALLBACK
print("[fonte]", "BebasNeue" if FONT == BEBAS else "LiberationSans-Bold (fallback)")


def fnt(s):
    return ImageFont.truetype(FONT, s)


def linhas_titulo(txt, font, maxw=980):
    """1 linha se couber; senão 2 linhas equilibradas por largura."""
    if _probe.textlength(txt, font=font) <= maxw:
        return [txt]
    palavras = txt.split()
    melhor = None
    for i in range(1, len(palavras)):
        a, b = " ".join(palavras[:i]), " ".join(palavras[i:])
        wa, wb = _probe.textlength(a, font=font), _probe.textlength(b, font=font)
        if wa <= maxw and wb <= maxw:
            dif = abs(wa - wb)
            if melhor is None or dif < melhor[0]:
                melhor = (dif, [a, b])
    return melhor[1] if melhor else [txt]


def cen(d, t, y, f, fill, W=1080, sombra=(0, 0, 0)):
    w = d.textlength(t, font=f)
    d.text(((W - w) / 2 + 2, y + 2), t, font=f, fill=sombra)
    d.text(((W - w) / 2, y), t, font=f, fill=fill)


def desenha_titulo(draw, linhas, y_uma, y_duas, font, fill):
    """Centraliza 1 linha em y_uma, ou 2 linhas em (y_duas, y_duas+passo)."""
    passo = int(font.size * 1.12)
    if len(linhas) == 1:
        cen(draw, linhas[0], y_uma, font, fill)
    else:
        cen(draw, linhas[0], y_duas, font, fill)
        cen(draw, linhas[1], y_duas + passo, font, fill)


# 1) clip da fonte (já tem NOSSA legenda, sem duplicar)
sh(["ffmpeg", "-y", "-v", "error", "-ss", str(INI), "-t", str(DUR), "-i", SRC,
    "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-r", "30", "/tmp/ce/clip.mp4"])

# 2) CAPA (2.5s) — capa oficial + titulo (1 ou 2 linhas)
f_capa = fnt(60)
lin_capa = linhas_titulo(TITULO, f_capa, 940)
im = Image.open(CAPA).convert("RGB")
d = ImageDraw.Draw(im)
desenha_titulo(d, lin_capa, 849, 806, f_capa, (255, 255, 255))
im.save("/tmp/ce/capa.png")
sh(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", "2.5", "-i", "/tmp/ce/capa.png",
    "-f", "lavfi", "-t", "2.5", "-i", "anullsrc=r=44100:cl=stereo",
    "-vf", "scale=1080:1920,setsar=1,fps=30,format=yuv420p", "-c:v", "libx264",
    "-c:a", "aac", "-b:a", "160k", "-shortest", "/tmp/ce/p_capa.mp4"])

# 3) TITULO NA MOLDURA (overlay transparente, ACIMA do video que fica em y=640)
f_mold = fnt(48)
lin_mold = linhas_titulo(TITULO, f_mold, 980)
tov = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
dt = ImageDraw.Draw(tov)
desenha_titulo(dt, lin_mold, 520, 486, f_mold, (255, 255, 255, 255))
tov.save("/tmp/ce/titulo_mold.png")

# 4) CORPO — moldura oficial + clip P&B (janela y=640) + titulo na moldura
sh(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", MOLD, "-i", "/tmp/ce/clip.mp4",
    "-i", "/tmp/ce/titulo_mold.png", "-filter_complex",
    "[1:v]hue=s=0,scale=1000:-2,setsar=1[pb];[0:v]setsar=1[bg];"
    "[bg][pb]overlay=(W-w)/2:640[comp];[comp][2:v]overlay=0:0,format=yuv420p[v]",
    "-map", "[v]", "-map", "1:a", "-t", str(DUR), "-r", "30", "-c:v", "libx264",
    "-c:a", "aac", "-b:a", "160k", "/tmp/ce/p_corpo.mp4"])

# 5) CARTELA-SINAL pro YouTube (3s)
c = Image.new("RGB", (1080, 1920), (6, 7, 13))
d = ImageDraw.Draw(c)
cen(d, "ESSA É 1 DAS 5 LEIS", 470, fnt(56), (201, 205, 216))
cen(d, "VÍDEO COMPLETO NO YOUTUBE", 900, fnt(66), (46, 230, 168))
cen(d, "@opoderdamentesabia", 1010, fnt(52), (255, 255, 255))
cen(d, "link na bio", 1090, fnt(44), (138, 147, 166))
c.save("/tmp/ce/cta.png")
sh(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", "3", "-i", "/tmp/ce/cta.png",
    "-f", "lavfi", "-t", "3", "-i", "anullsrc=r=44100:cl=stereo",
    "-vf", "scale=1080:1920,setsar=1,fps=30,format=yuv420p", "-c:v", "libx264",
    "-c:a", "aac", "-b:a", "160k", "-shortest", "/tmp/ce/p_cta.mp4"])

# 6) concat pelo FILTRO (velocidade travada 30fps)
nome = f"estudio_{int(time.time())}"
out = f"{APROV}/{nome}.mp4"
sh(["ffmpeg", "-y", "-v", "error",
    "-i", "/tmp/ce/p_capa.mp4", "-i", "/tmp/ce/p_corpo.mp4", "-i", "/tmp/ce/p_cta.mp4",
    "-filter_complex",
    "[0:v]fps=30,setsar=1[v0];[1:v]fps=30,setsar=1[v1];[2:v]fps=30,setsar=1[v2];"
    "[v0][0:a][v1][1:a][v2][2:a]concat=n=3:v=1:a=1[v][a]",
    "-map", "[v]", "-map", "[a]", "-r", "30", "-fps_mode", "cfr",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])

# 7) legenda + json
legenda = ("Disciplina vence motivação: quem depende de estar motivado vive refém do próprio humor. \U0001F9E0\n\n"
           "Essa é 1 das 5 Leis que reprogramam a mente. O vídeo completo, com as 5, está no nosso canal \U0001F449 link na bio.\n\n"
           "Segue @opoderdamentesabia pra treinar a mente todo dia.\n\n"
           "#disciplina #mentalidade #napoleonhill #motivacao #foco #desenvolvimentopessoal")
open(f"{APROV}/{nome}.txt", "w", encoding="utf-8").write(legenda)
json.dump({"fonte": "https://youtu.be/zkVylQ4cXak", "autor": "O Poder da Mente Sábia (canal)",
           "trecho": [INI, INI + DUR], "origem": "estudio_de_cortes", "titulo": TITULO,
           "criado": time.strftime("%Y-%m-%d %H:%M:%S")},
          open(f"{APROV}/{nome}.json", "w", encoding="utf-8"), ensure_ascii=False)

specs = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                        "-show_entries", "stream=duration,nb_read_packets", "-of", "csv=p=0", out],
                       capture_output=True, text=True).stdout.strip()
print(f"CORTE PRONTO: {out} | titulo capa={len(lin_capa)}L moldura={len(lin_mold)}L | frames/dur={specs} | nome={nome}")

# --- entrega no Telegram do dono pra aprovação (senão fica preso na pasta) ---
# antes o script só depositava o .mp4 na pasta e confiava que "o bot perguntaria";
# mas quem envia é o enviar_aprovacao. Sem isto, o corte ficava preso e ninguém via.
_r = subprocess.run(["/usr/bin/python3",
                     "/opt/automacao/marcas/opoder/motor/enviar_aprovacao.py",
                     out, "opoderdamentesabia", "reels"], timeout=180)
print(f"ENVIADO PRA APROVACAO NO TELEGRAM: {nome} (rc={_r.returncode})")
