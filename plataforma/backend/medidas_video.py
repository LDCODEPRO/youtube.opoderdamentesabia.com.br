#!/usr/bin/env python3
"""
O pesquisador MEDE O ARQUIVO INTEIRO (ordem do Diretor 16/07: "não só o som, tudo").
Bateria de medições objetivas sobre o vídeo final (preview):
  - duração real, resolução, fps (ffprobe)
  - identidade P&B: saturação média de frames amostrados (PIL)
  - estabilidade: tremor/jitter por deslocamento alternante entre frames consecutivos
  - volume: LUFS integrado (ffmpeg ebur128)
Tudo com cache por (tamanho, mtime) — mede 1x por arquivo. Zero invenção: só números.
"""
import json
import os
import re
import subprocess
import tempfile

from PIL import Image, ImageChops

CACHE_SUFIXO = ".medidas.json"


def _ffprobe_basico(caminho: str) -> dict:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,avg_frame_rate",
         "-show_entries", "format=duration",
         "-of", "json", caminho],
        capture_output=True, text=True, timeout=60)
    d = json.loads(r.stdout or "{}")
    st = (d.get("streams") or [{}])[0]
    num, _, den = (st.get("avg_frame_rate") or "0/1").partition("/")
    fps = round(float(num) / float(den or 1), 1) if float(den or 1) else 0
    return {
        "duracao_s": round(float((d.get("format") or {}).get("duration") or 0), 1),
        "width": st.get("width"), "height": st.get("height"), "fps": fps,
    }


def _extrai_frames(caminho: str, em_s: float, n: int, tam: str, pasta: str) -> list:
    padrao = os.path.join(pasta, f"f{int(em_s)}_%02d.png")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-ss", str(em_s), "-i", caminho,
         "-frames:v", str(n), "-vf", f"scale={tam}", padrao],
        capture_output=True, text=True, timeout=120)
    return sorted(p for p in (padrao % i for i in range(1, n + 1)) if os.path.exists(p))


def _saturacao_media(frames: list) -> float:
    if not frames:
        return -1.0
    tot = 0.0
    for p in frames:
        s = Image.open(p).convert("HSV").split()[1]
        h = s.histogram()
        npx = sum(h)
        tot += sum(i * c for i, c in enumerate(h)) / max(1, npx)
    return round(100 * (tot / len(frames)) / 255, 1)


def _desloc_otimo(a: Image.Image, b: Image.Image, alcance: int = 2):
    """Deslocamento (dx,dy) que melhor alinha b sobre a — jitter global aparece aqui."""
    w, h = a.size
    m = alcance
    base = a.crop((m, m, w - m, h - m))
    melhor, melhor_soma = (0, 0), None
    for dx in range(-m, m + 1):
        for dy in range(-m, m + 1):
            cand = b.crop((m + dx, m + dy, w - m + dx, h - m + dy))
            hist = ImageChops.difference(base, cand).histogram()
            soma = sum(i * c for i, c in enumerate(hist))
            if melhor_soma is None or soma < melhor_soma:
                melhor_soma, melhor = soma, (dx, dy)
    return melhor


def _mede_jitter(caminho: str, duracao: float, pasta: str) -> dict:
    """3 janelas de 12 frames; tremor = micro-deslocamento que ALTERNA de sinal
    entre pares consecutivos (zoom suave desloca sempre no MESMO sentido)."""
    pontos = [duracao * f for f in (0.25, 0.5, 0.78)]
    pares = 0
    alternantes = 0
    for t in pontos:
        frames = _extrai_frames(caminho, t, 12, "160:90", pasta)
        imgs = [Image.open(p).convert("L") for p in frames]
        ultimos = []
        for a, b in zip(imgs, imgs[1:]):
            dx, dy = _desloc_otimo(a, b)
            pares += 1
            if ultimos:
                pdx, pdy = ultimos[-1]
                if (dx * pdx < 0) or (dy * pdy < 0):
                    alternantes += 1
            ultimos.append((dx, dy))
    pct = round(100 * alternantes / max(1, pares))
    return {"pares": pares, "alternantes_pct": pct}


def _mede_lufs(caminho: str):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", caminho, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, timeout=300)
    m = re.findall(r"I:\s*(-?[\d.]+)\s*LUFS", r.stderr)
    return float(m[-1]) if m else None


def mede_tudo(caminho: str, cache_dir: str) -> dict:
    """Bateria completa com cache por (size, mtime)."""
    st = os.stat(caminho)
    cache_p = os.path.join(cache_dir, os.path.basename(caminho) + CACHE_SUFIXO)
    try:
        with open(cache_p, encoding="utf-8") as f:
            c = json.load(f)
        if c.get("_size") == st.st_size and c.get("_mtime") == int(st.st_mtime):
            return c
    except Exception:
        pass

    m = _ffprobe_basico(caminho)
    with tempfile.TemporaryDirectory() as tmp:
        frames_cor = _extrai_frames(caminho, m["duracao_s"] * 0.5, 8, "320:180", tmp)
        m["saturacao_pct"] = _saturacao_media(frames_cor)
        m.update({"jitter": _mede_jitter(caminho, m["duracao_s"], tmp)})
    m["lufs"] = _mede_lufs(caminho)
    m["_size"], m["_mtime"] = st.st_size, int(st.st_mtime)
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_p, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False)
    return m


if __name__ == "__main__":
    import sys
    print(json.dumps(mede_tudo(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "."),
                     ensure_ascii=False, indent=2))
