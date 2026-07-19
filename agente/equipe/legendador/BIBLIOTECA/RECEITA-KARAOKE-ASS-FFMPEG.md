# Receita: karaokê ASS a partir de SRT com ffmpeg (testada em 2026-07-17)

> Varredura ciclo 2, 2026-07-17. TUDO desta receita foi executado e verificado NESTA máquina (ffmpeg 8.1.1, Python 3.11, Windows): converti SRT→ASS, queimei com ffmpeg e conferi os frames exportados. Fontes externas ao lado de cada fato; opinião marcada como "leitura minha".

## 1. Como o karaokê ASS funciona (a teoria mínima)

Fonte: https://aegisub.org/docs/latest/ass_tags/

- Tags de karaokê marcam a duração de cada sílaba/palavra em **centissegundos** (100 = 1s): `{\k28}Sua {\k47}mente`.
- **`\k`** — a palavra começa na cor SECUNDÁRIA e vira cor PRIMÁRIA instantaneamente quando chega a vez dela (o "acender" limpo — o que usamos).
- **`\kf` (=`\K`)** — mesma coisa, mas com VARREDURA da esquerda para a direita (efeito karaokê clássico; bom para a chamada final).
- **`\ko`** — variante em que o contorno some antes do destaque (não nos serve).
- As cores do efeito são o `SecondaryColour` (antes) e o `PrimaryColour` (depois) do estilo — é aí que entra nosso P&B: secundária prata `&H00A0A0A0`, primária branco `&H00FFFFFF`.
- Ênfase extra sem karaokê: `\c&H...&` (troca cor), `\fscx110\fscy110` (escala +10%), `\t(...)` (anima a transição) — mesma fonte.
- SRT NÃO suporta nada disso; karaokê exige ASS. O ffmpeg queima ASS com o filtro `ass=` (confirmado no teste abaixo). A comunidade confirma: para karaokê real o caminho é ASS, não SRT (https://github.com/ggml-org/whisper.cpp/issues/884).

## 2. ⚠️ A PEGADINHA do force_style (descoberta no teste — corrige o ciclo 1)

Ao queimar **SRT direto** com `subtitles=arquivo.srt:force_style=...`, o libass usa uma resolução interna padrão de **384×288** — e escala tudo para o vídeo. Consequência MEDIDA no teste desta máquina (frames exportados em 1920×1080):

- `FontSize=56` no force_style de um SRT = letra GIGANTE (~210 px, 3 linhas tomando metade da tela) — porque 56/288×1080 ≈ 210 px.
- O certo em 1080p: **`FontSize=15`** (15/288×1080 ≈ 56 px renderizados) e **`MarginV=35`** (35/288×1080 ≈ 131 px do rodapé — fora da zona da UI do player).
- `Outline=1` nesse espaço vira ~3,75 px renderizados — dentro da faixa 3–4 px recomendada para contraste (ciclo 1: https://blitzcutai.com/blog/caption-background-vs-outline-vs-shadow). Testado sobre fundo BRANCO PURO: legível.
- **Correção ao ciclo 1 (leitura minha, agora provada):** o guia ESTILO-POSICAO-RETENCAO-2026.md sugeria `PlayResX=1920,PlayResY=1080` dentro do force_style — isso NÃO tem efeito (PlayRes é campo de Script Info, não de estilo; o force_style ignora). Avisar o Gerente: a regra prática correta é a tabela abaixo.

| Alvo em 1080p | Em ASS próprio (PlayRes 1920×1080) | Em force_style sobre SRT (espaço 384×288) |
|---|---|---|
| Letra ~56 px | FontSize=56 | FontSize=15 |
| Margem rodapé ~130 px | MarginV=130 | MarginV=35 |
| Contorno ~3–4 px | Outline=3 | Outline=1 |

- Leitura minha: gerar ASS próprio com `PlayResX: 1920 / PlayResY: 1080` no header é SEMPRE melhor — os números passam a ser pixels de verdade e o karaokê vem junto de graça.

## 3. A receita completa (executada e aprovada)

### Passo A — SRT de entrada (o nosso, já revisado pelo checklist do ciclo 1)

```
1
00:00:00,500 --> 00:00:03,200
Sua mente é o campo
onde tudo começa
```

### Passo B — conversor SRT→ASS karaokê (script testado; distribui \k proporcional ao tamanho da palavra)

Salvar como `srt2ass_karaoke.py`. Rodar: `python srt2ass_karaoke.py legendas.srt legendas.ass`

```python
# -*- coding: utf-8 -*-
import re, sys

def t2s(s):
    h, m, sec = s.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(sec)

def s2ass(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Marca,Arial,56,&H00FFFFFF,&H00A0A0A0,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,1,2,150,150,130,1
"""
# PrimaryColour = cor DEPOIS do karaokê (branco). SecondaryColour = ANTES (prata P&B).
# Outline=3 já embutido (proposta do ciclo 1); Alignment=2 + MarginV=130 = zona segura.

def convert(srt_path, ass_path):
    raw = open(srt_path, encoding="utf-8-sig").read()
    events = []
    for m in re.finditer(
        r"(\d+:\d+:\d+,\d+)\s*-->\s*(\d+:\d+:\d+,\d+)\s*\n((?:.+\n?)+?)(?:\n|\Z)", raw
    ):
        ini, fim = t2s(m.group(1)), t2s(m.group(2))
        linhas = [l.strip() for l in m.group(3).strip().split("\n")]
        texto = " ".join(linhas)
        palavras = texto.split()
        dur_cs = max(int((fim - ini) * 100), len(palavras))
        total_chars = sum(len(p) for p in palavras) or 1
        ks, usados = [], 0
        for i, p in enumerate(palavras):
            k = int(round(dur_cs * len(p) / total_chars))
            if i == len(palavras) - 1:
                k = dur_cs - usados
            usados += k
            ks.append(k)
        partes = []
        quebra = len(linhas[0].split()) if len(linhas) > 1 else None
        for i, (p, k) in enumerate(zip(palavras, ks)):
            if quebra is not None and i == quebra:
                partes.append(r"\N")
            partes.append(f"{{\\k{k}}}{p}")
            if i < len(palavras) - 1 and (quebra is None or i != quebra - 1):
                partes.append(" ")
        events.append(
            f"Dialogue: 0,{s2ass(ini)},{s2ass(fim)},Marca,,0,0,0,,{''.join(partes)}"
        )
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write("\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        f.write("\n".join(events) + "\n")
    print(f"OK: {len(events)} eventos -> {ass_path}")

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
```

Saída real do teste (note os \k em centissegundos, proporcionais à palavra, e o \N preservando a quebra de linha do SRT):

```
Dialogue: 0,0:00:00.50,0:00:03.20,Marca,,0,0,0,,{\k28}Sua {\k47}mente {\k9}é {\k9}o {\k47}campo\N{\k37}onde {\k37}tudo {\k56}começa
```

### Passo C — queimar no vídeo

```
ffmpeg -i video.mp4 -vf "ass=legendas.ass" -c:a copy video_legendado.mp4
```

Verificado: no frame de teste em t=2s, as palavras já faladas estão em branco puro e as ainda não faladas em prata — exatamente o efeito "acende com a voz", 100% dentro da estética P&B.

### Passo C2 — alternativa BLOCO simples direto do SRT (sem karaokê), com os valores CORRETOS

```
ffmpeg -i video.mp4 -vf "subtitles=legendas.srt:force_style='FontName=Arial,Bold=1,FontSize=15,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,Outline=1,Shadow=0,Alignment=2,MarginV=35'" -c:a copy video_legendado.mp4
```

(Formato da cor no force_style: `&HBBGGRR&` — https://www.samgalope.dev/2024/11/05/diy-karaoke-videos-with-ffmpeg-and-srt-format-sync-and-style/)

### Passo D — frame de conferência (rodar SEMPRE antes do render completo)

```
ffmpeg -y -i video.mp4 -vf "ass=legendas.ass" -ss 00:00:02 -frames:v 1 confere.png
```

Checar: altura da letra ~56 px, fora dos ~120 px do rodapé, legível no trecho mais branco do vídeo.

## 4. Timestamps por PALAVRA de verdade (quando a distribuição proporcional não bastar)

O script acima ESTIMA a duração de cada palavra pelo tamanho dela — bom o suficiente para ênfase pontual, impreciso para karaokê longo. Para timing real por palavra:

- **whisperX** (https://github.com/m-bain/whisperx): Whisper + forced alignment wav2vec2 = timestamp por palavra com precisão **±50 ms** (vs ~±500 ms do Whisper puro) (https://whipscribe.com/tools/whisperx e https://localaimaster.com/blog/whisperx-guide). Tem flag `--highlight_words True` que já gera SRT com a palavra corrente destacada.
- **stable-ts** (https://github.com/jianfch/stable-ts): transcrição + alinhamento forçado com word timestamps; instala com `pip install stable-ts`.
- Fluxo recomendado (leitura minha): nós JÁ temos o texto exato (roteiro do Roteirista) — então o caminho é **alinhamento forçado** (áudio + texto conhecido → tempos por palavra), não re-transcrição. O stable-ts faz `stable_ts.align(audio, texto)`. Os tempos por palavra substituem a distribuição proporcional no Passo B.
- Precisão importa: karaokê dessincronizado é pior que bloco (https://www.vocallab.ai/blog/word-highlighting-subtitles). Se não der para alinhar direito, ficar no bloco.

## 5. Regras de uso na produção (amarra com o guia irmão)

- Onde aplicar karaokê vs bloco: seguir a matriz do KARAOKE-VS-BLOCO-DECISAO-POR-DADOS.md (gancho karaokê, corpo bloco, tese destaque, final \kf).
- Adiantar legendas ~100–200 ms e o acender da palavra 50–100 ms antes da voz (https://www.opus.pro/blog/best-caption-presets-styles-boost-retention) — no script, basta subtrair 0,1s dos tempos do SRT antes de converter.
- O .srt LIMPO (sem tags) continua sendo entregue à parte para upload no YouTube — karaokê é só na queima; a faixa oficial é bloco puro (regra da casa, ciclo 1).

## Como aplicar no próximo vídeo

1. Adotar o fluxo B→C→D desta receita no vídeo de quarta 19h: converter o SRT aprovado, queimar um TRECHO de 30s (gancho) com karaokê prata→branco e mostrar ao Gerente antes de aplicar no vídeo inteiro.
2. Corrigir na LEGENDA-DA-MARCA (via Gerente) a regra do force_style: valores em espaço 384×288 quando queimar SRT direto (FontSize=15 / MarginV=35 / Outline=1) — a nota antiga do PlayRes no force_style não funciona.
3. Instalar e testar `stable-ts` com o áudio do Narrador + roteiro (alinhamento forçado) e comparar os tempos por palavra com a distribuição proporcional — se a diferença for visível no gancho, adotar o alinhado.
4. Padronizar o frame de conferência (Passo D) como anexo obrigatório da entrega de TODO vídeo — custa 1 comando, evita reprovação depois do render de 30 min.
5. Guardar `srt2ass_karaoke.py` na pasta de ferramentas da equipe e versionar junto do projeto (pedir ao Gerente onde ele quer o script oficial).
6. Com a cadência 3/semana: automatizar até sexta o pipeline SRT→ASS→frame de conferência num único .bat, para o custo por vídeo cair a ~2 minutos.
