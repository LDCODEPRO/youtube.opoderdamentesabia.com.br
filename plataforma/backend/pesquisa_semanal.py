#!/usr/bin/env python3
"""
Pesquisador semanal do território — ordem do Diretor (16/07/2026):
"O que funciona de verdade visto em pesquisa é REGRA nos vídeos e tem que ser
atualizado TODA SEMANA."

Toda segunda (systemd timer) varre as buscas do território no YouTube (ordenadas
por views), extrai os vídeos que estão estourando, mede quais peças do PARÂMETRO
os títulos usam e a duração dominante, e salva data/pesquisa_semana.json — que a
página "O que funciona" mostra como regra viva.

100% dado público, zero invenção. Roda sozinho: python3 pesquisa_semanal.py
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(BASE_DIR, "data", "pesquisa_semana.json")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

QUERIES = [
    "mentalidade",
    "napoleon hill",
    "poder da mente",
    "reprogramar sua mente",
    "joseph murphy",
    "disciplina mental",
]

AUTORES = ["napoleon hill", "joseph murphy", "jung", "dispenza", "lipton", "cury",
           "marco aurélio", "seneca", "sêneca", "goggins", "tolle", "goddard", "brunet"]


def _busca(query: str) -> list:
    """Busca do YouTube ordenada por views — o ytInitialData vem no HTML."""
    url = ("https://www.youtube.com/results?search_query="
           + urllib.parse.quote(query) + "&sp=CAMSAhAB")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    m = re.search(r"var ytInitialData = ({.*?});</script>", html)
    if not m:
        return []
    data = json.loads(m.group(1))
    achados = []

    def walk(o, prof=0):
        if not isinstance(o, (dict, list)) or prof > 30 or len(achados) > 20:
            return
        if isinstance(o, dict):
            v = o.get("videoRenderer")
            if v:
                achados.append({
                    "id": v.get("videoId"),
                    "titulo": ((v.get("title") or {}).get("runs") or [{}])[0].get("text", ""),
                    "canal": ((v.get("ownerText") or {}).get("runs") or [{}])[0].get("text", ""),
                    "views": _views_int(((v.get("viewCountText") or {}).get("simpleText")) or ""),
                    "quando": ((v.get("publishedTimeText") or {}).get("simpleText")) or "",
                    "duracao": ((v.get("lengthText") or {}).get("simpleText")) or "",
                    "query": query,
                })
            for val in o.values():
                walk(val, prof + 1)
        else:
            for item in o:
                walk(item, prof + 1)

    walk(data)
    return achados


def _views_int(txt: str) -> int:
    m = re.search(r"([\d.,]+)", txt or "")
    if not m:
        return 0
    return int(m.group(1).replace(".", "").replace(",", ""))


def _dur_min(txt: str):
    partes = (txt or "").split(":")
    try:
        if len(partes) == 3:
            return int(partes[0]) * 60 + int(partes[1])
        if len(partes) == 2:
            return int(partes[0])
    except ValueError:
        pass
    return None


def _recente(quando: str) -> bool:
    """'há X dias/semanas/meses' — consideramos quente até 12 meses."""
    q = (quando or "").lower()
    if any(t in q for t in ["hora", "dia", "semana"]):
        return True
    m = re.search(r"há (\d+) m[eê]s", q)
    if m:
        return int(m.group(1)) <= 12
    return False  # anos = clássico, não "desta semana"


def _pecas(titulo: str) -> list:
    t = titulo.lower()
    pecas = []
    if re.search(r"\b(você|sua|seu|suas|seus|te|sua mente|seu cérebro)\b", t):
        pecas.append("você no centro")
    if re.search(r"\b(\d+\s*(dia|dias|semana|semanas|minuto|minutos|segundo|segundos|"
                 r"noite|noites|hora|horas)|1 noite|rápido|hoje|agora|imediat)", t):
        pecas.append("prazo")
    if "|" in titulo or any(a in t for a in AUTORES):
        pecas.append("autoridade")
    if re.search(r"(nunca mais|como se nada|nada te|nada o|para sempre|irreconhec|"
                 r"inabal|impar[áa]vel|blindad|99%|100%|tudo muda)", t):
        pecas.append("estado-limite")
    return pecas


def main() -> int:
    todos, erros = {}, []
    for q in QUERIES:
        try:
            for v in _busca(q):
                if v["id"] and v["views"] > 0:
                    todos.setdefault(v["id"], v)
        except Exception as e:  # noqa: BLE001 — uma query falhar não derruba a varredura
            erros.append(f"{q}: {e}")

    videos = sorted(todos.values(), key=lambda v: -v["views"])
    # só o nosso idioma (fora devanágari/cirílico/CJK — a regra é para vídeos PT-BR)
    videos = [v for v in videos
              if not re.search(r"[ऀ-ॿЀ-ӿ一-鿿぀-ヿ]", v["titulo"])]
    quentes = [v for v in videos if _recente(v["quando"])][:15]
    if not quentes:
        quentes = videos[:15]

    duracoes = [d for d in (_dur_min(v["duracao"]) for v in quentes) if d]
    dur_5a30 = sum(1 for d in duracoes if 5 <= d <= 30)
    contagem = {"você no centro": 0, "prazo": 0, "autoridade": 0, "estado-limite": 0}
    for v in quentes:
        v["pecas"] = _pecas(v["titulo"])
        for p in v["pecas"]:
            contagem[p] += 1

    resultado = {
        "varredura_em": datetime.now(timezone.utc).isoformat(),
        "queries": QUERIES,
        "total_analisado": len(videos),
        "quentes": quentes,  # os que estão estourando agora (≤12 meses), por views
        "pecas_pct": {k: round(100 * n / max(1, len(quentes))) for k, n in contagem.items()},
        "duracao": {
            "mediana_min": sorted(duracoes)[len(duracoes) // 2] if duracoes else None,
            "dentro_da_regua_5a30_pct": round(100 * dur_5a30 / max(1, len(duracoes))),
        },
        "erros": erros,
    }
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"[pesquisa] ok: {len(videos)} vídeos, {len(quentes)} quentes, "
          f"peças {resultado['pecas_pct']}, erros={len(erros)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
