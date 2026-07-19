# Mandato de pesquisa — Editor

## Varredura ciclo 2 — 2026-07-17
**O que estudei:** aprofundamento AVANÇADO dos temas do ciclo (sound design + transições invisíveis + corte na batida), evitando repetir os 4 guias já existentes. Foco em duas fronteiras não cobertas: (1) fazer a IMAGEM reagir à batida com ffmpeg puro (`sendcmd`, timeline `enable`, `xfade=custom:expr` com easing, pulso em `zoompan`) e (2) tratar a VOZ da narração (denoise, EQ, de-ess, compressão, espaço/reverb, LUFS). 7 buscas + 8 fontes lidas a fundo, sintaxe oficial do ffmpeg conferida antes de escrever receita. Resultado: 2 guias novos — `BATIDA-QUE-ANIMA-VISUAL-SENDCMD-E-EXPRESSOES.md` e `VOZ-DA-NARRACAO-TRATAMENTO-E-ESPACO-SONORO.md`.

**Aprendizados-chave:**
- `sendcmd` agenda comando em tempo exato: `INÍCIO-FIM [enter/leave] ALVO COMANDO ARG;` — só filtros com flag `T` (eq, crop, scale, overlay, drawtext) aceitam runtime command; `zoompan` NÃO (https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Multimedia/sendcmd.html, https://www.ffmpeglab.com/articles/ffmpeg-dynamic-runtime-commands.html).
- Pulso de batida mais invisível = respiro de `eq contrast/brightness` (não muda o tamanho do frame); `eq` precisa `eval=frame` e suporta comando (https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Video/eq.html).
- `xfade=transition=custom:expr=...` usa P/X/Y/W/H/A/B; easing via `st()`/`ld()` exige `-filter_complex_threads 1` (state não é thread-safe) — dissolve easada some melhor que a linear (https://github.com/scriptituk/xfade-easing).
- `enable='between(t,a,b)'` liga um filtro só na janela da virada (grão/overlay) — menos CPU, mais intenção (https://ffmpeg.org/ffmpeg-filters.html).
- Voz: highpass 80-100 Hz é o 1º movimento; cortar barro 250-500 Hz (-2/-3 dB); presença ~3 kHz (+2 dB) faz a voz "chegar perto" (https://producerhive.com/music-production-recording-tips/how-to-use-a-vocal-eq-chart/, https://www.hollyland.com/blog/topics/use-equalization-in-audacity).
- ffmpeg tem `deesser` (i/m/f/s), `acompressor` (narração = threshold e ratio BAIXOS), `afftdn`/`arnndn` (denoise), `aecho` (reverb sutil) — cadeia curta, cada filtro uma função (https://ffmpeg.org/ffmpeg-filters.html, https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Audio/deesser.html).
- Alvo de loudness da fala: -14 a -16 LUFS (YouTube), AES -18 para voz/diálogo, TP máx -1/-2 dBTP; não esmagar a dinâmica só para bater número (https://www.criticallisteninglab.com/en/learn/loudness/youtube, https://lanceblairvo.com/lufs-voiceover-levels/, https://clickyapps.com/creator/video/guides/lufs-targets-2025).

**Fontes ciclo 2:**
- https://www.ffmpeglab.com/articles/ffmpeg-dynamic-runtime-commands.html
- https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Multimedia/sendcmd.html
- https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Video/eq.html
- https://github.com/scriptituk/xfade-easing/blob/main/README.md
- https://mko.re/blog/ken-burns-ffmpeg/
- https://ffmpeg.org/ffmpeg-filters.html
- https://producerhive.com/music-production-recording-tips/how-to-use-a-vocal-eq-chart/
- https://www.hollyland.com/blog/topics/use-equalization-in-audacity
- https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Audio/deesser.html
- https://ayosec.github.io/ffmpeg-filters-docs/8.0/Filters/Audio/afftdn.html
- https://odan.github.io/2023/08/20/reducing-background-audio-noise.html
- https://creativecow.net/forums/thread/using-ffmpeg-to-optimize-vocals-in-recordings-an/
- https://www.criticallisteninglab.com/en/learn/loudness/youtube
- https://lanceblairvo.com/lufs-voiceover-levels/
- https://clickyapps.com/creator/video/guides/lufs-targets-2025

**Próximo estudo:** testar em 1 vídeo real o respiro de `eq contrast` na batida (Receita A) e medir render/tempo com `-filter_complex_threads 1` nas viradas com `xfade=custom`; calibrar o preset de voz (seção 10 do guia de voz) com a voz sintetizada do Narrador e travar timbre+LUFS para os 3 vídeos/semana; estudar `arnndn` (baixar modelo `.rnnn`) vs `afftdn` no nosso material; conferir se o pipeline atual do Editor já expõe as fronteiras de virada para gerar `flash.cmd`/`zoom.cmd` automático.

## Varredura 2026-07-17
**O que estudei:** estado da arte de retention editing 2026 (pacing, benchmarks, pattern interrupts), pesquisa acadêmica sobre duração de plano (ASL) e atenção, J-cuts/L-cuts para narração, disciplina de transições, e automação prática em ffmpeg (xfade, acrossfade, sidechaincompress, loudnorm). 6 buscas + 5 fontes lidas a fundo. Resultado: 2 guias novos na BIBLIOTECA (`RITMO-DE-RETENCAO-2026.md` e `FFMPEG-TRANSICOES-E-J-CUTS.md`).

**Aprendizados-chave:**
- Edição sozinha muda retenção: top 25% de 100 canais long-form seguram 20–30% a mais só pela edição (AIR Media-Tech).
- Benchmarks 2026 para nós: ≥40% de retenção em vídeos de 5–15min e ≥30% em 15–30min é saudável; <30% = problema de gancho/pacing (Humble&Brag, Lenostube).
- Regra dos 5 segundos: nenhum bloco de 5s sem mudança (corte, zoom, texto ou som) — cada janela parada é vazamento (Joyspace).
- Pacing em marchas, não constante: abertura com trocas quase constantes (15–30s iniciais), corpo com interrupt a cada 20–40s (Etwell Studio).
- Nosso alvo 4–8s/cena é validado pela pesquisa de ASL (cinema ~2,5–4s, documentário ~15s) — estamos no meio certo para narração contemplativa.
- J-cut/L-cut é a cola da narração: dessincronizar a troca de imagem da troca de frase (~0,3–0,5s) cria fluidez e antecipação; usar só nas viradas (Filmsupply, Adobe, BorisFX).
- Corte seco é o padrão; dissolve só em virada de tempo/clima — excesso barateia (Filmpac, Adobe). Para nossa marca P&B, `xfade=fadegrays` é transição invisível e elegante.
- xfade automatizável com offset cumulativo (`offset_i = offset_(i-1) + dur_i − trans_dur`), mas cada transição come segundos da timeline — compensar nos tempos do Narrador (FFmpegLab).

**Fontes:**
- https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8
- https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
- https://joyspace.ai/pattern-interrupt-reset-attention-span
- https://etwell.studio/blog/high-retention-editing-what-it-is-and-how-to-get-it
- https://www.filmsupply.com/articles/j-cut-vs-l-cut/
- https://www.ffmpeglab.com/articles/ffmpeg-xfade-transitions-guide.html
- https://ottverse.com/crossfade-between-videos-ffmpeg-xfade-filter/
- https://www.researchgate.net/publication/342285366_How_filmmakers_guide_the_eye_The_effect_of_average_shot_length_on_intersubject_attentional_synchrony
- https://stephenfollows.com/p/many-shots-average-movie
- https://filmpac.com/the-difference-between-dissolves-and-cuts-in-video-edit/

**Próximo estudo:** ler o retention graph dos nossos primeiros vídeos publicados contra os benchmarks (onde caímos?); estudar sound design de interrupts (whoosh/risers de licença livre e como dosar); testar `fadegrays` vs `fade` no nosso material P&B e medir tempo de render do xfade em vídeo de 20min.

SUA ESPECIALIDADE: edição de retenção.
Pesquisar: cutting patterns dos virais (quando cortam, como transicionam), técnicas ffmpeg novas (filtros, blends), como os tops editam vídeo de narração.
## Como registrar o que aprender
Todo achado vira arquivo na sua BIBLIOTECA/ (um tema por arquivo, com fonte e data).
Achado que muda REGRA da produção → avisar o Gerente para atualizar a DOUTRINA e o painel.
Cadência: revisão da função TODA SEMANA junto da varredura de segunda-feira do Pesquisador.
