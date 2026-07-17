"""
Estúdio YouTube — O Poder da Mente Sábia | Coleta de dados REAIS (Lei Zero Ghost)
Fontes:
  - Feed RSS público do canal (títulos, views, datas — dado oficial do YouTube)
  - Página pública do canal (inscritos, best-effort com cache; se falhar → None, nunca inventa)
  - pipeline.json (fila de produção da fábrica — mantido pela equipe)
Cache em memória + disco (data/cache.json) com TTL, para não martelar o YouTube.
"""
import json
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

CHANNEL_ID = os.getenv("YOUTUBE_OPODER_CHANNEL_ID", "UCjpdA-aERgsqep3Dn0giFig")
CHANNEL_HANDLE = os.getenv("YOUTUBE_OPODER_HANDLE", "@opoderdamentesabia")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE_PATH = os.path.join(BASE_DIR, "pipeline.json")
CACHE_PATH = os.path.join(BASE_DIR, "data", "cache.json")
TTL_SEGUNDOS = 30 * 60  # 30 min

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

_cache = {"quando": 0, "dados": None}


def _http_get(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept-Language": "pt-BR"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _busca_feed() -> list:
    """Vídeos do feed RSS oficial (últimos ~15), com views por vídeo."""
    xml = _http_get(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}")
    ns = {
        "a": "http://www.w3.org/2005/Atom",
        "m": "http://search.yahoo.com/mrss/",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }
    root = ET.fromstring(xml)
    videos = []
    for e in root.findall("a:entry", ns):
        titulo = e.findtext("a:title", "", ns)
        vid = e.findtext("yt:videoId", "", ns)
        pub = e.findtext("a:published", "", ns)
        stats = e.find(".//m:community/m:statistics", ns)
        views = int(stats.get("views", "0")) if stats is not None else 0
        rating = e.find(".//m:community/m:starRating", ns)
        likes = int(rating.get("count", "0")) if rating is not None else 0
        dias = _dias_desde(pub[:10])
        # dois mundos que NÃO se misturam: corte vertical (veio do motor do Instagram,
        # subiu como Short) vs vídeo LONGO original (o foco deste projeto no YouTube)
        eh_corte = titulo.strip().startswith("✨") or titulo.count("#") >= 3
        videos.append({
            "tipo": "corte" if eh_corte else "longo",
            "id": vid,
            "titulo": titulo,
            "publicado": pub[:10],
            "views": views,
            "likes": likes,
            "dias_no_ar": dias,
            "views_por_dia": round(views / (dias + 1), 2) if dias is not None else None,
            "url": f"https://www.youtube.com/watch?v={vid}",
        })
    return videos


def _busca_inscritos():
    """Raspa inscritos da página pública. Best-effort: falhou → None (nunca inventa)."""
    try:
        html = _http_get(f"https://www.youtube.com/{CHANNEL_HANDLE}")
        m = re.search(r'"subscriberCountText"[^}]*?"(?:simpleText|content)"\s*:\s*"([^"]+)"', html)
        if not m:
            m = re.search(r'([\d.,]+ ?(?:mil|mi)?) de inscritos|(\d+) inscritos', html)
        if m:
            bruto = next(g for g in m.groups() if g)
            return _numero_br(bruto)
    except Exception:
        pass
    return None


def _numero_br(texto: str):
    """'33', '1,2 mil', '2,11 mi' -> int aproximado."""
    t = texto.lower().replace("inscritos", "").replace("de", "").strip()
    mult = 1
    if "mil" in t:
        mult = 1_000
        t = t.replace("mil", "").strip()
    elif "mi" in t:
        mult = 1_000_000
        t = t.replace("mi", "").strip()
    t = t.replace(".", "").replace(",", ".")
    try:
        return int(float(t) * mult)
    except ValueError:
        return None


def _dias_desde(data_iso: str):
    try:
        d = datetime.fromisoformat(data_iso).replace(tzinfo=timezone.utc)
        return max(0, (datetime.now(timezone.utc) - d).days)
    except Exception:
        return None


CAPAS_DIR = os.path.join(BASE_DIR, "frontend", "capas")


def carrega_pipeline() -> dict:
    try:
        with open(PIPELINE_PATH, encoding="utf-8") as f:
            pipe = json.load(f)
    except Exception as e:
        return {"erro": f"pipeline.json ilegível: {e}", "videos": []}
    # estado da capa e do preview de cada vídeo = existência real do arquivo (Zero Ghost)
    for v in pipe.get("videos", []):
        arq = os.path.join(CAPAS_DIR, f"{v.get('codigo', '')}.png")
        v["capa_url"] = f"/capas/{v['codigo']}.png" if os.path.isfile(arq) else None
        prev = os.path.join(BASE_DIR, "frontend", "previews", f"{v.get('codigo', '')}.mp4")
        v["preview_url"] = f"/previews/{v['codigo']}.mp4" if os.path.isfile(prev) else None
    return pipe


def carrega_pautas() -> dict:
    """Banco de pautas do Agente Youtuber (agente/pautas.json)."""
    try:
        with open(os.path.join(BASE_DIR, "agente", "pautas.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"erro": f"pautas.json ilegível: {e}", "pautas": []}


def carrega_equipe() -> dict:
    """O time do Agente Gerente YouTube (agente/equipe/equipe.json)."""
    try:
        with open(os.path.join(BASE_DIR, "agente", "equipe", "equipe.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"membros": []}


PESQUISA_PATH = os.path.join(BASE_DIR, "data", "pesquisa_semana.json")


def carrega_pesquisa() -> dict:
    """A regra viva: última varredura semanal do território (timer de segunda)."""
    try:
        with open(PESQUISA_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


DECISOES_PATH = os.path.join(BASE_DIR, "data", "decisoes.json")


def carrega_decisoes() -> dict:
    """Decisões do Diretor tomadas no painel (aprovações, avisos)."""
    try:
        with open(DECISOES_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def grava_decisao(item: str, decisao: str, motivo: str = "") -> dict:
    todas = carrega_decisoes()
    registro = {"decisao": decisao, "quando": datetime.now(timezone.utc).isoformat()}
    if motivo:
        registro["motivo"] = motivo[:400]
    todas[item] = registro
    os.makedirs(os.path.dirname(DECISOES_PATH), exist_ok=True)
    with open(DECISOES_PATH, "w", encoding="utf-8") as f:
        json.dump(todas, f, ensure_ascii=False, indent=2)
    return todas


def atualiza_status_video(codigo: str, novo_status: str, nota: str = "") -> bool:
    """A decisão do Diretor MOVE o vídeo na fila (reprovou → volta pra produção)."""
    try:
        with open(PIPELINE_PATH, encoding="utf-8") as f:
            pipe = json.load(f)
        for v in pipe.get("videos", []):
            if v.get("codigo") == codigo:
                v["status"] = novo_status
                if nota:
                    v["nota"] = nota
                tmp = PIPELINE_PATH + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(pipe, f, ensure_ascii=False, indent=2)
                os.replace(tmp, PIPELINE_PATH)
                return True
    except Exception:
        pass
    return False


HIST_PATH = os.path.join(BASE_DIR, "data", "historico.jsonl")


def _grava_historico(d: dict) -> None:
    """Um ponto REAL por coleta fresca: o histórico do canal nasce e cresce sozinho."""
    try:
        os.makedirs(os.path.dirname(HIST_PATH), exist_ok=True)
        with open(HIST_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "t": d.get("coletado_em"),
                "inscritos": d.get("inscritos"),
                "views_feed": d.get("views_somadas_feed"),
            }, ensure_ascii=False) + "\n")
    except Exception:
        pass


def carrega_historico(n: int = 120) -> list:
    try:
        with open(HIST_PATH, encoding="utf-8") as f:
            pontos = [json.loads(ln) for ln in f if ln.strip()]
        return pontos[-n:]
    except Exception:
        return []


def _le_cache_disco():
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _grava_cache_disco(dados: dict) -> None:
    try:
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
    except Exception:
        pass


def resumo(force: bool = False) -> dict:
    """O retrato REAL do canal agora. Cache 30 min (memória + disco)."""
    agora = time.time()
    if not force and _cache["dados"] and agora - _cache["quando"] < TTL_SEGUNDOS:
        return _cache["dados"]

    dados = {"coletado_em": datetime.now(timezone.utc).isoformat(), "fonte": "youtube-publico"}
    try:
        videos = _busca_feed()
        ultimo = videos[0] if videos else None
        dados.update({
            "ok": True,
            "videos": videos,
            "total_videos_no_feed": len(videos),
            "views_somadas_feed": sum(v["views"] for v in videos),
            "ultimo_upload": ultimo["publicado"] if ultimo else None,
            "dias_sem_postar": _dias_desde(ultimo["publicado"]) if ultimo else None,
        })
    except Exception as e:
        # YouTube fora de alcance: devolve o último retrato do disco, avisando a idade
        antigo = _le_cache_disco()
        if antigo:
            antigo["aviso"] = f"YouTube inacessível agora ({e}); mostrando último retrato salvo."
            _cache.update(quando=agora, dados=antigo)
            return antigo
        dados.update({"ok": False, "erro": str(e), "videos": []})

    dados["inscritos"] = _busca_inscritos()
    dados["pipeline"] = carrega_pipeline()
    dados["agente"] = carrega_pautas()
    dados["equipe"] = carrega_equipe()
    if dados.get("ok"):
        _grava_historico(dados)
    dados["historico"] = carrega_historico()
    dados["decisoes"] = carrega_decisoes()
    dados["pesquisa"] = carrega_pesquisa()

    _cache.update(quando=agora, dados=dados)
    _grava_cache_disco(dados)
    return dados
