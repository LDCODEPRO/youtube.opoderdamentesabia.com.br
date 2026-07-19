"""
Estúdio YouTube — O Poder da Mente Sábia | Autenticação
Usuário único (o Diretor). Senha nunca fica em texto puro — só o hash bcrypt
vive no .env (YOUTUBE_OPODER_PASSWORD_HASH). Sessão via cookie assinado
(Starlette SessionMiddleware, chave em YOUTUBE_OPODER_SESSION_SECRET).
Mesmo padrão do Postador (a casa toda autentica igual).
"""
import os

import bcrypt
from fastapi import HTTPException, Request


def check_password(plain: str) -> bool:
    hashed = os.getenv("YOUTUBE_OPODER_PASSWORD_HASH", "")
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def require_auth(request: Request) -> None:
    if not request.session.get("authenticated"):
        raise HTTPException(status_code=401, detail="Sessão expirada ou não autenticada")
