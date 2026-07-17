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
import re
import secrets
import time

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from auth import check_password, require_auth
from dados import (atualiza_status_video, carrega_decisoes, carrega_pipeline,
                   grava_decisao, resumo)

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
        if v.get("capa_url"):
            v["crivo"] = carrega_crivo(v["codigo"])
        v["portao"] = pode_publicar(v, dados["decisoes"])
    return JSONResponse(dados)


class DecisaoIn(BaseModel):
    item: str
    decisao: str
    motivo: str | None = None


ITENS_VALIDOS = {"kit_visual": {"aprovado", "refazer", "manter_atual"}, "sessao_navegador": {"pronto"},
                 "video_aprovacao": {"aprovado", "reprovado"}}


def _decisao_permitida(item: str, decisao: str) -> bool:
    if item.startswith("capa_"):
        return decisao in {"aprovado", "refazer"}
    if item.startswith("aprovar_video_"):
        return decisao in {"aprovado", "reprovado"}
    return item in ITENS_VALIDOS and decisao in ITENS_VALIDOS[item]


@app.post("/api/decisao")
def decidir(body: DecisaoIn, request: Request, _=Depends(require_auth)):
    """O Diretor decide no painel; a decisão fica registrada E MOVE a fila."""
    if not _decisao_permitida(body.item, body.decisao):
        raise HTTPException(status_code=400, detail="Decisão desconhecida")
    decisoes = grava_decisao(body.item, body.decisao, body.motivo or "")
    if body.item.startswith("aprovar_video_"):
        codigo = body.item.replace("aprovar_video_", "")
        from datetime import datetime
        hoje = datetime.now().strftime("%d/%m %H:%M")
        if body.decisao == "reprovado":
            nota = f"⛔ REPROVADO pelo Diretor em {hoje}" + \
                   (f" — motivo: {body.motivo}" if body.motivo else " (sem motivo informado)") + \
                   ". Voltou para a fábrica; nova versão vai para sua aprovação."
            atualiza_status_video(codigo, "producao", nota)
        else:
            atualiza_status_video(codigo, "aprovado",
                                  f"✅ Aprovado pelo Diretor em {hoje} — no Repositório, pronto para publicar.")
    return {"ok": True, "decisoes": decisoes}


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


def _prompt_capa(video: dict, instrucao: str = "", variar: bool = False) -> str:
    palavras = video.get("palavras_capa") or video.get("titulo_trabalho", "")
    sub = video.get("subtitulo_capa") or ""
    p = (
        f"CAPA (thumbnail) de vídeo do YouTube, formato HORIZONTAL 16:9 (1280x720) — NÃO é post "
        f"de Instagram, NÃO usar layout vertical. Vídeo: '{video.get('titulo_trabalho')}'. "
        "Cena única e forte: fundo preto cósmico com estrelas e névoa, um elemento prateado/cromado "
        "central (lâmpada com cérebro dentro, estilo do logo da marca), luz fria dramática. "
        f"Texto GIGANTE legível em miniatura de celular: '{palavras}' em LETRAS 3D — "
        "tipografia sans-serif bold condensada com EXTRUSÃO de profundidade real, acabamento "
        "CROMADO/prata metálico polido com reflexos de estúdio, bisel nas bordas, luz fria — "
        "efeito premium de logo de cinema. "
    )
    if sub:
        p += (f"Logo ABAIXO do texto principal, uma segunda linha MENOR (cerca de 40% do tamanho), "
              f"mesma fonte e mesmo efeito 3D cromado: '{sub}'. ")
    p += ("Alto contraste, uma emoção só, sem poluição, sem rodapé de CTA, sem cards, "
          "sem rostos reais, sem marca d'água.")
    if variar:
        p += (" IMPORTANTE: componha uma versão DIFERENTE da anterior — mude o ângulo, a posição "
              "dos elementos ou o enquadramento, mantendo a mesma identidade da marca.")
    if instrucao:
        p += f" MUDANÇA PEDIDA PELO DIRETOR (obedecer exatamente): {instrucao.strip()}"
    return p


_CAPAS_EM_CURSO: dict = {}  # codigo -> "desenhando" | "erro: ..."
CRIVO_DIR = os.path.join(BASE_DIR, "data", "crivo")


def _crivo_capa(codigo: str, video: dict) -> dict:
    """O CRIVO DO PESQUISADOR (ordem do Diretor 16/07): toda thumbnail é comparada
    com o padrão visual dos virais DESTA semana antes de ir ao Diretor."""
    from dados import carrega_pesquisa
    from pesquisa_semanal import medir_imagem

    caminho = os.path.join(CAPAS_DIR, f"{codigo}.png")
    medida = medir_imagem(caminho)
    padrao = (carrega_pesquisa() or {}).get("padrao_visual") or {}
    palavras = ((video.get("palavras_capa") or "") + " " + (video.get("subtitulo_capa") or "")).split()

    checks = []

    def check(nome, ok, detalhe):
        checks.append({"nome": nome, "ok": bool(ok), "detalhe": detalhe})

    check("Formato de YouTube (16:9)", 1.6 <= medida["proporcao"] <= 1.9,
          f"proporção {medida['proporcao']} (alvo ~1,78)")
    check("Poucas palavras, impacto", 2 <= len(palavras) <= 8,
          f"{len(palavras)} palavras na capa")
    if padrao:
        check("Escura como os virais da semana",
              medida["escuro_pct"] >= padrao.get("escuro_pct_mediana", 0) * 0.6,
              f"nossa: {medida['escuro_pct']}% escuro · virais: {padrao.get('escuro_pct_mediana')}%")
        check("Contraste de viral",
              medida["contraste"] >= padrao.get("contraste_mediana", 0) * 0.7,
              f"nossa: {medida['contraste']} · virais: {padrao.get('contraste_mediana')}")
    else:
        check("Padrão da semana", True, "sem gabarito ainda (1ª varredura pendente)")

    aprovada = all(c["ok"] for c in checks)
    veredito = {
        "quando": datetime_agora(),
        "aprovada": aprovada,
        "resumo": ("✔ dentro do padrão dos virais desta semana" if aprovada
                   else "✖ fora do padrão: " + "; ".join(c["nome"] for c in checks if not c["ok"])),
        "checks": checks,
        "medida": medida,
        "gabarito": padrao,
    }
    os.makedirs(CRIVO_DIR, exist_ok=True)
    with open(os.path.join(CRIVO_DIR, f"{codigo}.json"), "w", encoding="utf-8") as f:
        json.dump(veredito, f, ensure_ascii=False, indent=2)
    return veredito


def datetime_agora() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def carrega_crivo(codigo: str) -> dict:
    try:
        with open(os.path.join(CRIVO_DIR, f"{codigo}.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _md5(caminho: str) -> str:
    import hashlib
    h = hashlib.md5()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


_MEDICOES_EM_CURSO: set = set()


def _medidas_cache(caminho: str):
    try:
        with open(os.path.join(CRIVO_DIR, os.path.basename(caminho) + ".medidas.json"),
                  encoding="utf-8") as f:
            c = json.load(f)
        st = os.stat(caminho)
        if c.get("_size") == st.st_size and c.get("_mtime") == int(st.st_mtime):
            return c
    except Exception:
        pass
    return None


def _dispara_medicao(codigo: str, caminho: str) -> None:
    import threading
    if codigo in _MEDICOES_EM_CURSO:
        return
    _MEDICOES_EM_CURSO.add(codigo)

    def rodar():
        try:
            from medidas_video import mede_tudo
            mede_tudo(caminho, CRIVO_DIR)
        except Exception:
            pass
        finally:
            _MEDICOES_EM_CURSO.discard(codigo)

    threading.Thread(target=rodar, daemon=True).start()


def _crivo_arquivo_checks(codigo: str, check) -> None:
    """O pesquisador mede o ARQUIVO INTEIRO (ordem: 'não só o som, tudo'):
    imagem (tremor, P&B, resolução), som (LUFS, voz×música) e duração real."""
    prev = os.path.join(FRONT, "previews", f"{codigo}.mp4")
    if not os.path.isfile(prev):
        check("Arquivo medido pelo pesquisador", False, "vídeo ainda não subiu para o painel")
        return
    m = _medidas_cache(prev)
    if not m:
        _dispara_medicao(codigo, prev)
        check("Arquivo em medição", False, "🔬 o pesquisador está medindo imagem e som deste arquivo (~1–2min)")
        return
    check("Duração real na régua (5–30min)",
          m.get("duracao_s") and 300 <= m["duracao_s"] <= 1800,
          f"{(m.get('duracao_s') or 0) / 60:.1f} min")
    check("Qualidade de imagem (1080p, 24fps+)",
          (m.get("width") or 0) >= 1920 and (m.get("fps") or 0) >= 24,
          f"{m.get('width')}x{m.get('height')} @ {m.get('fps')}fps")
    check("Identidade P&B da marca",
          m.get("saturacao_pct") is not None and 0 <= m["saturacao_pct"] <= 6,
          f"saturação {m.get('saturacao_pct')}% (P&B pede ~0)")
    jit = (m.get("jitter") or {}).get("alternantes_pct")
    check("Imagem estável, sem tremor", jit is not None and jit <= 25,
          f"micro-tremor em {jit}% dos quadros analisados")
    check("Volume padrão YouTube (−17 a −12 LUFS)",
          m.get("lufs") is not None and -17.0 <= m["lufs"] <= -12.0,
          f"{m.get('lufs')} LUFS")
    manif_p = os.path.join(CRIVO_DIR, f"{codigo}_mix.json")
    try:
        with open(manif_p, encoding="utf-8") as f:
            manif = json.load(f)
        if manif.get("arquivo_md5") == _md5(prev):
            dif = manif.get("diferenca_voz_musica_db")
            check("Música atrás da voz (≥18 dB)", dif is not None and dif >= 18.0,
                  f"voz {manif.get('voz_mean_db')} dB · música {manif.get('musica_mean_db')} dB · diferença {dif} dB")
        else:
            check("Música atrás da voz (≥18 dB)", False,
                  "o manifesto de mix não é DESTE arquivo — mix não medida")
    except Exception:
        check("Música atrás da voz (≥18 dB)", False, "sem manifesto de mix medido")


def _crivo_video(video: dict) -> dict:
    """CRIVO GERAL do vídeo (ordem do Diretor: TUDO passa pelo pesquisador antes de postar).
    Julga título, capa, duração e descrição contra a pesquisa e as regras da casa."""
    from pesquisa_semanal import _pecas

    codigo = video.get("codigo", "")
    checks = []

    def check(nome, ok, detalhe):
        checks.append({"nome": nome, "ok": bool(ok), "detalhe": detalhe})

    titulo = video.get("titulo_youtube") or ""
    pecas = _pecas(titulo) if titulo else []
    check("Título com o parâmetro (≥2 peças)", titulo and len(pecas) >= 2,
          f"'{titulo[:50]}…' → {', '.join(pecas) if pecas else 'nenhuma peça'}" if titulo
          else "sem título de YouTube definido")
    check("Título cabe no YouTube (≤70)", titulo and len(titulo) <= 70,
          f"{len(titulo)} caracteres" if titulo else "—")

    crivo_capa = carrega_crivo(codigo)
    check("Capa aprovada no crivo visual", crivo_capa.get("aprovada"),
          crivo_capa.get("resumo", "capa ainda não gerada/avaliada"))

    faixa = re.findall(r"\d+", video.get("duracao_alvo") or "")
    dur_ok = faixa and 5 <= int(faixa[0]) and int(faixa[-1]) <= 30
    check("Duração na régua (5–30min)", dur_ok, video.get("duracao_alvo") or "sem alvo")

    check("Descrição SEO pronta", bool((video.get("descricao_seo") or "").strip()),
          "pronta" if (video.get("descricao_seo") or "").strip() else "ainda falta escrever")

    _crivo_arquivo_checks(codigo, check)

    aprovado = all(c["ok"] for c in checks)
    return {"aprovado": aprovado, "checks": checks,
            "resumo": "✔ liberado pelo pesquisador" if aprovado
            else "✖ segura a publicação: " + "; ".join(c["nome"] for c in checks if not c["ok"])}


def pode_publicar(video: dict, decisoes: dict) -> dict:
    """O PORTÃO: só publica com crivo 100% + aprovação do Diretor. O uploader usará isto."""
    crivo = _crivo_video(video)
    dec = (decisoes.get(f"aprovar_video_{video.get('codigo')}") or {}).get("decisao")
    faltas = []
    if not crivo["aprovado"]:
        faltas.append("crivo do pesquisador")
    if dec != "aprovado":
        faltas.append("aprovação do Diretor")
    return {"pode": not faltas, "faltas": faltas, "crivo": crivo}


def _gera_e_salva(codigo: str, video: dict, instrucao: str, variar: bool) -> None:
    import urllib.request
    payload = json.dumps({"descricao": _prompt_capa(video, instrucao, variar),
                          "marca": MARCA_MENTE_SABIA,
                          "recipe_key": "dica_unica"}).encode("utf-8")
    req = urllib.request.Request(f"{PONTE_URL}/api/gerar-imagem", data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=280) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    if not res.get("ok") or not res.get("image_url"):
        raise RuntimeError("a ponte não devolveu imagem")
    os.makedirs(CAPAS_DIR, exist_ok=True)
    with urllib.request.urlopen(f"{PONTE_URL}{res['image_url']}", timeout=60) as img:
        with open(os.path.join(CAPAS_DIR, f"{codigo}.png"), "wb") as f:
            f.write(img.read())


def _job_capa(codigo: str, video: dict, instrucao: str = "", variar: bool = False) -> None:
    """Thread: desenha → CRIVO DO PESQUISADOR → reprovou? refaz 1x sozinha → salva veredito."""
    try:
        _gera_e_salva(codigo, video, instrucao, variar)
        veredito = _crivo_capa(codigo, video)
        if not veredito.get("aprovada"):
            _CAPAS_EM_CURSO[codigo] = "desenhando"  # segue ocupado no refazer automático
            correcao = ("Correção do pesquisador (obrigatória): "
                        + "; ".join(c["nome"] + " — " + c["detalhe"]
                                    for c in veredito["checks"] if not c["ok"])
                        + ". Fundo mais escuro e texto com mais contraste, como os virais da semana.")
            _gera_e_salva(codigo, video, (instrucao + " " + correcao).strip(), True)
            _crivo_capa(codigo, video)  # veredito final (aprovada ou não, o Diretor vê a verdade)
        grava_decisao(f"capa_{codigo}", "aguardando_diretor")
        _CAPAS_EM_CURSO.pop(codigo, None)
    except Exception as e:  # noqa: BLE001 — o erro vira estado visível, nunca silêncio
        _CAPAS_EM_CURSO[codigo] = f"erro: {e}"


class GerarCapaIn(BaseModel):
    instrucao: str | None = None


@app.post("/api/capas/gerar/{codigo}")
def gerar_capa(codigo: str, request: Request, body: GerarCapaIn | None = None,
               _=Depends(require_auth)):
    """Dispara o desenho da capa em segundo plano (a ponte leva ~1-2 min).
    Se já existe capa, é um REFAZER: sai versão diferente, obedecendo a instrução do Diretor."""
    import threading

    if _CAPAS_EM_CURSO.get(codigo) == "desenhando":
        return {"ok": True, "status": "desenhando"}
    pipe = carrega_pipeline()
    video = next((v for v in pipe.get("videos", []) if v.get("codigo") == codigo), None)
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não está na fila")
    instrucao = (body.instrucao or "").strip() if body else ""
    variar = bool(video.get("capa_url"))  # já tinha capa → a próxima tem que vir diferente
    if instrucao:
        grava_decisao(f"capa_{codigo}_instrucao", instrucao[:300])
    _CAPAS_EM_CURSO[codigo] = "desenhando"
    threading.Thread(target=_job_capa, args=(codigo, video, instrucao, variar), daemon=True).start()
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


@app.get("/previews/{arquivo}")
def preview(arquivo: str, request: Request, _=Depends(require_auth)):
    """O vídeo em revisão, para o Diretor assistir DENTRO da plataforma (só logado)."""
    caminho = os.path.join(FRONT, "previews", os.path.basename(arquivo))
    if not os.path.isfile(caminho):
        raise HTTPException(status_code=404, detail="não existe")
    return FileResponse(caminho, media_type="video/mp4")
