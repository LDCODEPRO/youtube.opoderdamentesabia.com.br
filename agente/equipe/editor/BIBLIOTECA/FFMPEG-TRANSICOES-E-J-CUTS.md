# ffmpeg na prática — xfade, J-cuts automatizados e mix de áudio para o nosso pipeline
*Varredura de 2026-07-17 · Receitas prontas para o pipeline seg/ → concat → filtros → mux. Fontes ao lado; "leitura minha" = opinião/adaptação nossa.*

## 1. xfade — a transição nativa do ffmpeg (sem plugin, 100% automatizável)
Fonte principal: https://www.ffmpeglab.com/articles/ffmpeg-xfade-transitions-guide.html e https://ottverse.com/crossfade-between-videos-ffmpeg-xfade-filter/

Sintaxe mínima (3 parâmetros: tipo, duração, offset):
```
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=6.5[v]" \
  -map "[v]" out.mp4
```
- **offset = duração do clipe A − duração da transição** (medido na timeline do 1º input). Clipe A de 7s + transição de 0,5s → `offset=6.5` (https://www.ffmpeglab.com/articles/ffmpeg-xfade-transitions-guide.html).
- 30+ transições em famílias: dissolves (`fade, fadeblack, fadewhite, fadegrays, dissolve, pixelize`), wipes, slides, shapes (`circleopen...`), efeitos (`radial, hblur...`) (https://www.ffmpeglab.com/articles/ffmpeg-xfade-transitions-guide.html).
- **Para a nossa marca P&B**: usar SÓ `fade`, `fadeblack`, `dissolve` e — achado bom — **`fadegrays`** (dessatura durante a transição; no nosso material já P&B fica invisível e elegante). Wipes/slides/circle = efeito circo, proibido (leitura minha, coerente com a regra da casa).

## 2. Encadear N cenas com xfade — o offset é CUMULATIVO
```
[0:v][1:v]xfade=transition=fade:duration=0.5:offset=6.5[ab];
[ab][2:v]xfade=transition=fade:duration=0.5:offset=12.7[v]
```
- O offset seguinte é medido contra a timeline JÁ combinada (https://www.ffmpeglab.com/articles/ffmpeg-xfade-transitions-guide.html).
- Fórmula para automação (script): `offset_i = offset_(i-1) + dur_i − trans_dur`, com `offset_1 = dur_1 − trans_dur`. Cada transição "come" `trans_dur` segundos da duração total — o roteiro de tempos do Narrador precisa compensar isso, senão a sincronia bloco-a-bloco desliza (leitura minha; matemática decorre da definição do filtro).
- Script bash pronto que encadeia N arquivos com xfade existe como referência: https://github.com/qq2225936589/xfade-ffmpeg-script
- **Custo**: xfade obriga re-encode de tudo que passa pelo filter_complex. Para vídeo de 30 min, avaliar transição só nas viradas de capítulo e corte seco (concat demuxer) no resto — corte seco não re-encoda se os segmentos já forem uniformes (leitura minha; nosso pipeline já re-encoda uniforme, então o custo real é tempo de render).

## 3. Erros clássicos do xfade (checklist antes de rodar)
Fonte: https://www.ffmpeglab.com/articles/ffmpeg-xfade-transitions-guide.html
- [ ] Resolução/SAR iguais nas duas entradas → normalizar com `scale=1920:1080,setsar=1`.
- [ ] fps constante e IGUAL nos dois lados → forçar `fps=30` em cada input antes do xfade (fps misto = flash preto).
- [ ] Offset certo → errado demais = clipe some ou sobrepõe antes da hora.
- [ ] Timestamps limpos → usar `settb=AVTB` e `setpts=PTS-STARTPTS` em cada ramo antes do xfade (leitura minha, prática consolidada do nosso pipeline com trim/concat).

## 4. Áudio junto: acrossfade
```
[0:a][1:a]acrossfade=d=0.5[a]
```
- `acrossfade` casa o crossfade de áudio com a transição visual; `d` = duração, `o`/`overlap` controla sobreposição (https://ottverse.com/crossfade-between-videos-ffmpeg-xfade-filter/).
- No NOSSO caso a narração é uma faixa contínua por cima — acrossfade vale para a TRILHA quando ela troca na virada de capítulo, não para a voz (leitura minha).

## 5. J-cut automatizado no nosso pipeline (a receita que faltava)
Conceito: J-cut = áudio da próxima cena/ideia chega antes da imagem trocar; L-cut = áudio antigo continua sobre a imagem nova (https://www.adobe.com/creativecloud/video/post-production/cuts-in-film/l-and-j-cut.html). Como nossa narração é contínua, o jeito de "fazer J-cut" é deslocar a FRONTEIRA VISUAL em relação à fronteira da frase:

**Receita A — deslocar cortes na montagem por lista (barato, sem filtro novo):**
No gerador do `concat.txt`/tempos de cena, aplicar `inicio_cena_visual = inicio_frase − 0.4` nas viradas marcadas. A imagem nova entra ~0,4s antes da frase nova = antecipação de J-cut. Valor 0,3–0,5s é leitura minha (as fontes recomendam "alguns frames a ~1s", sem número fixo: https://borisfx.com/blog/l-and-j-cuts-smoother-more-cinematic/).

**Receita B — L-cut de respiro:** na frase de impacto do capítulo, SEGURAR a imagem 0,5–1s após o fim da frase (silêncio + imagem parada em movimento lento) antes de cortar — o eco emocional do L-cut (https://www.filmsupply.com/articles/j-cut-vs-l-cut/). Exceção controlada à regra "corte a cada 4–8s": o plano continua tendo movimento interno (zoompan/overlay), só não corta.

**Onde usar:** só nas viradas de ideia (3–6 por vídeo). J/L-cut em todo corte = desconexo (aviso da fonte: https://www.filmsupply.com/articles/j-cut-vs-l-cut/).

## 6. Mix de trilha vs. voz — medir, não chutar (regra da casa: voz ≥18 dB acima)
Ferramentas nativas (documentação oficial dos filtros: https://ffmpeg.org/ffmpeg-filters.html):
- **Medir**: `ffmpeg -i faixa.wav -af astats=measure_overall=RMS_level -f null -` (ou `volumedetect`) para RMS/pico de voz e trilha separadas; ajustar `volume=` da trilha até a diferença ≥18 dB.
- **Ducking automático**: `sidechaincompress` com a voz como sidechain abaixa a trilha SÓ quando a voz fala:
```
[trilha][voz]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=400[trilha_duck]
```
  (parâmetros de partida — calibrar por teste; leitura minha).
- **Consistência entre vídeos**: `loudnorm=I=-14:TP=-1.5:LRA=11` no master final — -14 LUFS é o alvo de normalização usado por plataformas de streaming (documentação do filtro loudnorm: https://ffmpeg.org/ffmpeg-filters.html#loudnorm). Com `print_format=json` dá para fazer a passada dupla (measure → apply) em script.

## 7. Pattern interrupts baratos em ffmpeg (sem asset novo)
Leitura minha — receitas com filtros documentados em https://ffmpeg.org/ffmpeg-filters.html:
- **Punch-in de 2s** (zoom seco no meio da cena): recortar a cena em t e aplicar `crop=iw/1.15:ih/1.15,scale=1920:1080` no segundo pedaço = "troca de ângulo" sem material novo.
- **Flash de b-roll 1–2s**: inserir plano curtíssimo entre duas cenas longas (tipo listado como interrupt visual em https://joyspace.ai/pattern-interrupt-reset-attention-span).
- **SFX de virada**: whoosh/riser baixinho (-24 dB) sob o J-cut da virada de capítulo — interrupt sonoro (https://joyspace.ai/pattern-interrupt-reset-attention-span). Nunca acima da voz.

## Como aplicar no próximo vídeo
1. **Adotar o padrão de transição da marca**: corte seco por padrão; `xfade=fade` ou `fadegrays` de 0,5s SÓ nas viradas de capítulo; `fadeblack` no máximo 2–3 no vídeo — já deixar o tipo/duração parametrizado no script de montagem.
2. **Implementar a fórmula de offset cumulativo** no gerador de concat/filter_complex e COMPENSAR os segundos comidos pelas transições nos tempos do Narrador (validar sincronia no bloco final).
3. **Rodar o checklist da seção 3** (scale+setsar, fps=30 forçado, setpts) em todo segmento antes de qualquer xfade — elimina o flash preto de uma vez.
4. **Testar a Receita A de J-cut** (imagem antecipa a frase em 0,4s) em 3 viradas do próximo vídeo e comparar o retention graph dessas regiões com vídeos anteriores.
5. **Automatizar o mix**: medir RMS de voz e trilha com astats, ajustar para ≥18 dB de diferença, aplicar sidechaincompress na trilha e fechar o master com loudnorm -14 LUFS em duas passadas.
6. **Adicionar 1 punch-in de crop** por capítulo longo (cena >8s) como pattern interrupt de custo zero.
