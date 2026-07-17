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
    return JSONResponse(dados)


class DecisaoIn(BaseModel):
    item: str
    decisao: str


ITENS_VALIDOS = {"kit_visual": {"aprovado", "refazer", "manter_atual"}, "sessao_navegador": {"pronto"},
                 "video_aprovacao": {"aprovado", "reprovado"}}


@app.post("/api/decisao")
def decidir(body: DecisaoIn, request: Request, _=Depends(require_auth)):
    """O Diretor decide no painel; a decisão fica registrada e o agente executa."""
    if body.item not in ITENS_VALIDOS or body.decisao not in ITENS_VALIDOS[body.item]:
        raise HTTPException(status_code=400, detail="Decisão desconhecida")
    return {"ok": True, "decisoes": grava_decisao(body.item, body.decisao)}


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
