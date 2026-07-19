# Acessibilidade, contraste em vídeo P&B e norma PT-BR de legendagem (2026)

> Varredura de 2026-07-17. Todo número tem fonte ao lado. O que é interpretação está marcado como "leitura minha".
> Referência-mestra adotada: Netflix Timed Text Style Guide — Português (Brasil), o padrão profissional mais rigoroso disponível para PT-BR.

## 1. Norma PT-BR (Netflix TTSG pt-BR) — os números que valem para nós

Fonte de tudo nesta seção: https://partnerhelp.netflixstudios.com/hc/en-us/articles/215600497-Portuguese-Brazil-Timed-Text-Style-Guide

- Máximo **42 caracteres por linha**; máximo **2 linhas** por evento.
- Velocidade de leitura: até **17 CPS** (caracteres/segundo) para adulto; 13 CPS para infantil; SDH até 20 CPS.
- Duração por evento: mínimo **5/6 de segundo** (~0,83s), máximo **7 segundos**.
- Fonte de referência: Arial, branca (bate com o nosso estilo provado da casa).
- Números: 1 a 10 por extenso; acima de 10 em algarismos; métrico sem espaço ("5km", "3h"); datas em diálogo por extenso ("1º de abril de 2024").
- Reticências: caractere único … (U+2026), não três pontos.
- Itálico: títulos de obras, palavras estrangeiras, voz por telefone/eletrônico, voice-over.
- Leitura minha: nosso padrão dinâmico (~5 palavras/tela) fica MUITO abaixo dos 42 caracteres — ótimo. O risco real é o CPS: em narração acelerada, grupos curtos com tempo curto estouram 17 CPS. É isso que precisa de checagem automática.

### Quebra de linha (a parte que separa amador de profissional)
Mesma fonte (TTSG pt-BR):
- Quebrar DEPOIS de pontuação; ANTES de conjunções ("que", "mas", "porque"); ANTES de preposições ("de", "para", "com").
- NUNCA separar: artigo do substantivo ("a | mente" ❌), adjetivo do substantivo, nome do sobrenome, verbo do pronome-sujeito.
- Leitura minha aplicada ao canal: em 2 linhas, a quebra deve cair na respiração da frase do Narrador — "Sua mente é o campo | onde tudo começa" ✅, nunca "Sua mente é o | campo onde tudo começa" ❌.

## 2. Contraste: contorno vs caixa vs sombra — e o caso especial do vídeo P&B

Fonte dos números: https://blitzcutai.com/blog/caption-background-vs-outline-vs-shadow

- Ranking de legibilidade: **1º caixa de fundo, 2º contorno (outline), 3º sombra**.
- Caixa preta sólida com texto branco = contraste **21:1** (WCAG AA exige 4.5:1; AAA exige 7:1).
- Contorno de **3–4 px** + texto branco ≈ 12:1 em fundos médios; contorno de 1–2 px é menos confiável em contrastes extremos.
- Caixa semi-transparente **70–80% de opacidade** = meio-termo usado por streamings (contraste alto, menos intrusão).
- Sombra sozinha: 3:1 a 20:1 dependendo do fundo — não confiável.
- Branco com contorno preto é o padrão de mercado justamente por ser o fallback seguro quando o fundo clareia (https://aurisai.io/blog/best-and-worst-font-colors-for-subtitles/).

**O problema específico do nosso canal (leitura minha):** vídeo P&B é o PIOR cenário para contorno fino — o fundo oscila entre preto puro e branco estourado o tempo todo. Texto branco + Outline=2 desaparece parcialmente sobre céu branco, pele clara em alto contraste, fumaça. Sobre preto, fica perfeito. Ou seja: nosso estilo atual é forte em metade dos frames e frágil na outra metade.

**Proposta (leitura minha — muda REGRA da marca, então precisa de aval do Gerente antes de virar padrão):**
- Opção A (mínima): subir para `Outline=3` (dentro da faixa 3–4 px recomendada) e adicionar `Shadow=1` como reforço — mantém a cara atual.
- Opção B (máxima legibilidade): `BorderStyle=4` (caixa) com `BackColour=&HA0000000&` (~63–75% opacidade) — contraste garantido em qualquer frame P&B, visual "streaming".
- Testar as duas num trecho com fundo branco estourado e decidir olhando o frame, não a teoria.

## 3. Acessibilidade de verdade (não é só queimar legenda)

- WCAG nível A: vídeo pré-gravado com áudio EXIGE legenda; a legenda deve conter fala E sons relevantes para entender o conteúdo (https://www.w3.org/WAI/media/av/captions/).
- Legenda automática NÃO conta como acessível sem revisão: "precisam de edição significativa" (https://www.w3.org/WAI/media/av/captions/). Por isso subir o NOSSO .srt revisado, nunca confiar no auto-CC do YouTube.
- Recomendações gerais de mercado: manter na tela tempo suficiente para leitura confortável, ~130–180 wpm de fala legendável (DCMP 130–160, BBC 160–180), acima de ~180 wpm fica rápido demais (https://onenine.com/wcag-captioning-standards-for-video-content/ e https://www.ucop.edu/electronic-accessibility/standards-and-best-practices/ecourse-accessibility-checklist/captioning-best-practices.html).
- Sons não-verbais relevantes entram entre colchetes: [música intensifica], [silêncio] (https://www.w3.org/WAI/media/av/captions/). Leitura minha para o canal: usar com MUITA parcimônia no arquivo .srt (acessibilidade), e NUNCA na legenda queimada — a estética P&B não comporta ruído visual.
- Bônus SEO: o .srt enviado vira texto indexável e há registro de +12% de visualizações em vídeo legendado vs não legendado (dado do Facebook — https://www.kapwing.com/resources/subtitle-statistics/); no YouTube o ganho é de indexação e alcance (https://www.captioncut.com/blog/video-captions-seo-engagement-2025/).

## 4. Checklist de qualidade do Legendador (rodar em TODO vídeo)

- [ ] UTF-8 sem BOM; acentuação PT-BR 100% (à, ç, ê, õ...).
- [ ] ≤42 caracteres/linha; ≤2 linhas/evento (TTSG pt-BR).
- [ ] CPS ≤17 em todos os eventos (TTSG pt-BR) — medir, não estimar.
- [ ] Nenhum evento <0,83s nem >7s (TTSG pt-BR).
- [ ] Quebras de linha gramaticais (nunca artigo|substantivo etc.).
- [ ] Reticências U+2026; números 1–10 por extenso.
- [ ] Legenda fora dos 120 px do rodapé (zona da UI do player).
- [ ] Frame-teste em trecho de fundo BRANCO: legenda legível? (ponto fraco do P&B)
- [ ] Palavra-chave da tela = palavra que o Narrador acentua naquele instante.
- [ ] Entrega dupla: vídeo queimado + .srt revisado subido no YouTube.

Verificação de CPS num SRT (miniatura em Python, leitura minha):

```python
import re, sys
srt = open(sys.argv[1], encoding="utf-8-sig").read()
for m in re.finditer(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)\n((?:.+\n?)+?)(?:\n|$)", srt):
    t = lambda s: sum(f*x for f, x in zip([3600,60,1,.001], map(int, re.split("[:,]", s))))
    dur = t(m.group(2)) - t(m.group(1))
    txt = m.group(3).replace("\n", " ").strip()
    cps = len(txt) / dur if dur else 99
    if cps > 17 or dur < 0.83 or dur > 7:
        print(f"REPROVADO {m.group(1)} cps={cps:.1f} dur={dur:.2f}s: {txt[:40]}")
```

## Como aplicar no próximo vídeo

1. Rodar o verificador de CPS/duração no legendas.srt antes da queima; corrigir todo evento reprovado (juntar ou encurtar grupos).
2. Revisar as quebras de linha de todos os eventos de 2 linhas contra as regras gramaticais da seção 1 (conjunção/preposição puxam a linha de baixo).
3. Exportar 1 frame do trecho mais BRANCO do vídeo e conferir a legibilidade; anexar o frame na entrega para o Gerente.
4. Levar ao Gerente a proposta Outline=3 vs caixa 70–80% (seção 2) com os dois frames de teste — decisão dele, pois muda a LEGENDA-DA-MARCA.
5. Subir o .srt revisado no YouTube em pt-BR (nunca deixar só o auto-CC) e confirmar que apareceu como faixa oficial.
6. Conferir com o Narrador os trechos de fala >170 wpm: ou a narração respira, ou a legenda condensa (sem trair a fala).
