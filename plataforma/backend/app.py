"""
Estúdio YouTube — O Poder da Mente Sábia
Plataforma da federação em youtube.opoderdamentesabia.com.br

  GET /health  -> a loja está viva
  GET /status  -> o que a loja sabe AGORA (dados reais, Lei Zero Ghost)
  POST /api/login|logout, GET /api/me  -> sessão do Diretor (padrão da casa)
  GET /api/resumo  -> retrato do canal + pipeline (auth)
  GET /  -> painel (frontend/index.html)

Porta 5065 (systemd youtube_opoder.service), atrás do nginx.
"""
import json
import os
import secrets
import time

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from auth import check_password, require_auth
from dados import carrega_decisoes, carrega_pipeline, grava_decisao, resumo

APP_NAME = "youtube-opoder"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONT = os.path.join(BASE_DIR, "frontend")
INICIO = time.time()

app = FastAPI(title="Estúdio YouTube — O Poder da Mente Sábia", docs_url=None, redoc_url=None)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("YOUTUBE_OPODER_SESSION_SECRET", secrets.token_hex(32)),
    max_age=30 * 24 * 3600,
    same_site="lax",
    https_only=True,
)


# ── Contrato de Loja (o hub lê sem auth) ─────────────────────────────────────
@app.get("/health")
def health():
    return {"ok": True, "loja": APP_NAME, "uptime_s": int(time.time() - INICIO)}


@app.get("/status")
def status():
    pipe = carrega_pipeline()
    contagem = {}
    for v in pipe.get("videos", []):
        contagem[v.get("status", "?")] = contagem.get(v.get("status", "?"), 0) + 1
    return {
        "ok": True,
        "loja": APP_NAME,
        "missao": "canal @opoderdamentesabia rumo ao YPP (1.000 inscritos + 4.000h)",
        "pipeline": contagem,
        "decisoes_do_diretor": carrega_decisoes(),
        "uptime_s": int(time.time() - INICIO),
    }


# ── Sessão do Diretor (padrão da casa: bcrypt + rate-limit) ──────────────────
class LoginIn(BaseModel):
    senha: str


_tentativas: dict = {}


def _client_ip(request: Request) -> str:
    return request.headers.get("x-real-ip") or (request.client.host if request.client else "?")


@app.post("/api/login")
def login(body: LoginIn, request: Request):
    ip = _client_ip(request)
    agora = time.time()
    historico = [t for t in _tentativas.get(ip, []) if agora - t < 600]
    if len(historico) >= 8:
        raise HTTPException(status_code=429, detail="Muitas tentativas. Aguarde 10 minutos.")
    if not check_password(body.senha):
        historico.append(agora)
        _tentativas[ip] = historico
        raise HTTPException(status_code=401, detail="Senha incorreta")
    _tentativas.pop(ip, None)
    request.session["authenticated"] = True
    return {"ok": True}


@app.post("/api/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@app.get("/api/me")
def me(request: Request):
    return {"autenticado": bool(request.session.get("authenticated"))}


# ── Dados do painel ──────────────────────────────────────────────────────────
@app.get("/api/resumo")
def api_resumo(request: Request, force: bool = False, _=Depends(require_auth)):
    dados = resumo(force=force)
    dados["decisoes"] = carrega_decisoes()  # decisão do Diretor nunca espera cache
    dados["pipeline"] = carrega_pipeline()  # capa recém-salva aparece sem esperar cache
    for v in dados["pipeline"].get("videos", []):
        estado = _CAPAS_EM_CURSO.get(v.get("codigo"))
        if estado:
            v["capa_status"] = estado
    return JSONResponse(dados)


class DecisaoIn(BaseModel):
    item: str
    decisao: str


ITENS_VALIDOS = {"kit_visual": {"aprovado", "refazer", "manter_atual"}, "sessao_navegador": {"pronto"},
                 "video_aprovacao": {"aprovado", "reprovado"}}


def _decisao_permitida(item: str, decisao: str) -> bool:
    if item.startswith("capa_"):
        return decisao in {"aprovado", "refazer"}
    return item in ITENS_VALIDOS and decisao in ITENS_VALIDOS[item]


@app.post("/api/decisao")
def decidir(body: DecisaoIn, request: Request, _=Depends(require_auth)):
    """O Diretor decide no painel; a decisão fica registrada e o agente executa."""
    if not _decisao_permitida(body.item, body.decisao):
        raise HTTPException(status_code=400, detail="Decisão desconhecida")
    return {"ok": True, "decisoes": grava_decisao(body.item, body.decisao)}


# ── Fábrica de capas: a ponte da assinatura (Studio, porta 5063) desenha ─────
PONTE_URL = os.getenv("PONTE_ASSINATURA_URL", "http://127.0.0.1:8000")
CAPAS_DIR = os.path.join(FRONT, "capas")


MARCA_MENTE_SABIA = {
    "name": "O Poder da Mente Sábia",
    "niche": "mentalidade, psicologia e sabedoria (canal de YouTube)",
    "style": ("preto cósmico com estrelas e névoa sutil; elementos metálicos PRATA/cromados "
              "(lâmpada cromada, cérebro prateado, luz fria); premium, misterioso, monocromático "
              "preto e branco. NUNCA: aves, animais, produtos, pessoas reais, verde, elementos de loja."),
    "colors": ["preto #05060A", "prata #C9CDD8", "branco-gelo #F0F3FA"],
    "tom": "sábio, direto, profundo",
}


def _prompt_capa(video: dict) -> str:
    palavras = video.get("palavras_capa") or video.get("titulo_trabalho", "")
    return (
        f"CAPA (thumbnail) de vídeo do YouTube, formato HORIZONTAL 16:9 (1280x720) — NÃO é post "
        f"de Instagram, NÃO usar layout vertical. Vídeo: '{video.get('titulo_trabalho')}'. "
        "Cena única e forte: fundo preto cósmico com estrelas e névoa, um elemento prateado/cromado "
        "central (lâmpada com cérebro dentro, estilo do logo da marca), luz fria dramática. "
        f"Texto GIGANTE legível em miniatura de celular: '{palavras}' (máx. 4 palavras) em "
        "branco/prata com brilho suave, sans-serif bold. Alto contraste, uma emoção só, sem poluição, "
        "sem rodapé de CTA, sem cards, sem rostos reais, sem marca d'água."
    )


_CAPAS_EM_CURSO: dict = {}  # codigo -> "desenhando" | "erro: ..."


def _job_capa(codigo: str, video: dict) -> None:
    """Roda em thread: pede o desenho à ponte, baixa e salva. O painel acompanha pelo estado."""
    import urllib.request
    try:
        payload = json.dumps({"descricao": _prompt_capa(video), "marca": MARCA_MENTE_SABIA,
                              "recipe_key": "dica_unica"}).encode("utf-8")
        req = urllib.request.Request(f"{PONTE_URL}/api/gerar-imagem", data=payload,
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=280) as resp:
            res = json.loads(resp.read().decode("utf-8"))
        if not res.get("ok") or not res.get("image_url"):
            raise RuntimeError("a ponte não devolveu imagem")
        os.makedirs(CAPAS_DIR, exist_ok=True)
        destino = os.path.join(CAPAS_DIR, f"{codigo}.png")
        with urllib.request.urlopen(f"{PONTE_URL}{res['image_url']}", timeout=60) as img:
            with open(destino, "wb") as f:
                f.write(img.read())
        grava_decisao(f"capa_{codigo}", "aguardando_diretor")
        _CAPAS_EM_CURSO.pop(codigo, None)
    except Exception as e:  # noqa: BLE001 — o erro vira estado visível, nunca silêncio
        _CAPAS_EM_CURSO[codigo] = f"erro: {e}"


@app.post("/api/capas/gerar/{codigo}")
def gerar_capa(codigo: str, request: Request, _=Depends(require_auth)):
    """Dispara o desenho da capa em segundo plano (a ponte leva ~1-2 min)."""
    import threading

    if _CAPAS_EM_CURSO.get(codigo) == "desenhando":
        return {"ok": True, "status": "desenhando"}
    pipe = carrega_pipeline()
    video = next((v for v in pipe.get("videos", []) if v.get("codigo") == codigo), None)
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não está na fila")
    _CAPAS_EM_CURSO[codigo] = "desenhando"
    threading.Thread(target=_job_capa, args=(codigo, video), daemon=True).start()
    return {"ok": True, "status": "desenhando"}


# ── Frontend ─────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    # o painel nunca pode ficar velho no navegador do Diretor
    return FileResponse(os.path.join(FRONT, "index.html"),
                        headers={"Cache-Control": "no-store, must-revalidate"})


@app.get("/logo.png")
def logo():
    return FileResponse(os.path.join(FRONT, "logo.png"))


@app.get("/kit/{arquivo}")
def kit(arquivo: str):
    caminho = os.path.join(FRONT, "kit", os.path.basename(arquivo))
    if not os.path.isfile(caminho):
        raise HTTPException(status_code=404, detail="não existe")
    return FileResponse(caminho)


@app.get("/capas/{arquivo}")
def capa(arquivo: str):
    caminho = os.path.join(FRONT, "capas", os.path.basename(arquivo))
    if not os.path.isfile(caminho):
        raise HTTPException(status_code=404, detail="não existe")
    return FileResponse(caminho, headers={"Cache-Control": "no-cache"})
