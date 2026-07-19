"""Busca grupos do nicho por scraping server-side (sem navegador), no molde do pesquisa_semanal.
Dado um nicho, varre diretórios públicos e extrai links reais de grupos (chat.whatsapp.com / t.me).
Zero Ghost: só devolve link que apareceu de verdade no HTML — nunca inventa nem completa código.
O achado do servidor é best-effort; a varredura profunda (centenas) é feita pelo catalogador (workflow)."""
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

# diretórios que costumam expor os links direto no HTML
FONTES_WPP = [
    "https://gruposwhats.app/?s={q}",
    "https://www.gruposdezap.com/?s={q}",
    "https://linkgrupos.com.br/?s={q}",
]
FONTES_TG = [
    "https://meusgrupos.com/busca?q={q}",
    "https://combot.org/telegram/top?q={q}",
]

RX_WPP = re.compile(r"https://chat\.whatsapp\.com/[A-Za-z0-9]{18,26}")
RX_TG = re.compile(r"https://t\.me/(?:joinchat/)?[A-Za-z0-9_+\-]{4,40}")
# nome perto do link (âncora ou título) — best-effort
RX_TITULO = re.compile(r"<(?:h[1-4]|a|strong|b)[^>]*>([^<>{}]{4,70})</", re.I)

# t.me que NÃO são grupo (evitar telegram.org, share, etc.)
TG_IGNORA = {"share", "s", "iv", "addstickers", "joinchat"}


def _http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        bruto = r.read()
    for enc in ("utf-8", "latin-1"):
        try:
            return bruto.decode(enc)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", "replace")


def _nome_perto(html, pos):
    janela = html[max(0, pos - 400):pos]
    achados = RX_TITULO.findall(janela)
    if achados:
        nome = achados[-1].strip()
        nome = re.sub(r"\s+", " ", nome)
        if 3 < len(nome) < 70 and "http" not in nome:
            return nome
    return ""


def _varre(url, plataforma, rx):
    grupos = []
    try:
        html = _http_get(url)
    except Exception:
        return grupos
    vistos = set()
    for m in rx.finditer(html):
        link = m.group(0)
        if plataforma == "telegram":
            slug = link.rsplit("/", 1)[-1].lower()
            if slug in TG_IGNORA or link.endswith("t.me"):
                continue
        if link in vistos:
            continue
        vistos.add(link)
        grupos.append({
            "nome": _nome_perto(html, m.start()) or (plataforma.capitalize() + " · grupo"),
            "plataforma": plataforma,
            "link": link,
            "tema": "",
            "permite_divulgacao": "verificar nas regras do grupo",
            "fonte": url,
        })
    return grupos


def buscar(nicho: str, limite: int = 60) -> list:
    """Retorna grupos reais achados nos diretórios para o nicho. Best-effort, pode vir vazio."""
    q = urllib.parse.quote_plus(nicho.strip()[:60])
    achados = []
    vistos = set()
    for url in FONTES_WPP:
        for g in _varre(url.format(q=q), "whatsapp", RX_WPP):
            if g["link"] not in vistos:
                vistos.add(g["link"])
                g["tema"] = nicho
                achados.append(g)
    for url in FONTES_TG:
        for g in _varre(url.format(q=q), "telegram", RX_TG):
            if g["link"] not in vistos:
                vistos.add(g["link"])
                g["tema"] = nicho
                achados.append(g)
        if len(achados) >= limite:
            break
    return achados[:limite]


if __name__ == "__main__":
    import json
    import sys
    print(json.dumps(buscar(sys.argv[1] if len(sys.argv) > 1 else "mentalidade"),
                     ensure_ascii=False, indent=1))
