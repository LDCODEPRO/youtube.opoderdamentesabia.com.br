# A batida que anima a imagem — sendcmd, timeline e transições por expressão (ffmpeg puro)
*Varredura ciclo 2 · 2026-07-17 · A METADE que faltava do "corte na batida": o guia CORTE-NA-BATIDA-E-TRANSICOES-INVISIVEIS.md ensinou a DETECTAR a batida (aubio/librosa) e a mover o corte. Aqui a imagem REAGE à batida sem editor manual — pulsos, respiros e transições invisíveis dirigidos por comando/expressão dentro do próprio ffmpeg. Fontes ao lado de cada número. "leitura minha" = adaptação para o nosso P&B de narração. NÃO repete detecção nem o algoritmo de snap.*

## 1. A ideia (o que muda em relação ao guia anterior)
- No guia de corte na batida, o beat só decidia ONDE cortar. Aqui o beat também decide QUANDO a imagem pulsa/respira/transiciona — a costura vira evento sonoro-visual único.
- Duas ferramentas nativas do ffmpeg fazem isso sem DAW e sem NLE: **`sendcmd`** (agenda comandos em tempos exatos) e **timeline editing / `enable`** (liga um filtro só numa janela) — ambas documentadas em https://ffmpeg.org/ffmpeg-filters.html e https://www.ffmpeglab.com/articles/ffmpeg-dynamic-runtime-commands.html
- Leitura minha (régua da casa): a imagem "sente" a batida por LUMINÂNCIA e MICRO-ZOOM, nunca por efeito. Um respiro de brilho de 0,1s no downbeat é invisível-mas-sentido; um zoom-punch visível a cada beat é linguagem de music video (proibido, coerente com a seção 1 do guia de corte na batida).

## 2. sendcmd — o relógio de comandos do ffmpeg
Fonte da sintaxe oficial: https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Multimedia/sendcmd.html · prática: https://www.ffmpeglab.com/articles/ffmpeg-dynamic-runtime-commands.html
- Formato do arquivo de comandos: `INÍCIO[-FIM] [FLAG] ALVO COMANDO ARG;` — **`;` fecha o intervalo, `,` separa comandos** no mesmo intervalo.
- FLAGS: `[enter]` (dispara ao ENTRAR na janela — é o padrão), `[leave]` (ao SAIR), `[expr]` (o ARG é avaliado como expressão, com constantes `T`, `N`, `W`, `H`...).
- Exemplo oficial verbatim (desatura entre 15s e 20s e volta):
```
15.0-20.0 [enter] hue s 0,
          [leave] hue s 1;
```
- **Regra de posição**: o `sendcmd` tem que vir ANTES, na cadeia, do filtro que ele controla (https://www.ffmpeglab.com/articles/ffmpeg-dynamic-runtime-commands.html).
- Só filtros marcados com **`T`** (timeline+commands) em `ffmpeg -filters` aceitam comando em runtime. Úteis para nós: `eq`, `crop`, `scale`, `overlay`, `drawtext`, `volume`, `hue` (lista em https://www.ffmpeglab.com/articles/ffmpeg-dynamic-runtime-commands.html). **`zoompan` NÃO aceita comando** — por isso ele fica na Receita C (expressão).

## 3. Gerar o arquivo de comandos a partir do beats.txt (custo zero)
Leitura minha (o `beats.txt` vem do `aubiotrack -T s`, seção 2 do guia de corte na batida). Script Python que transforma cada downbeat num respiro de brilho:
```python
# beats.txt = uma batida por linha, em segundos. Gera flash.cmd para o sendcmd.
dur = 4/30            # 4 frames a 30fps = 0.133s de respiro
brilho = 0.06         # +0.06 em eq brightness (faixa -1..1); sutil de propósito
linhas = []
for i, s in enumerate(open("beats.txt")):
    t = float(s)
    if i % 2:  continue          # só metade das batidas (downbeats aprox.) — não pulsar em tudo
    linhas.append(f"{t:.3f}-{t+dur:.3f} [enter] eq brightness {brilho}, [leave] eq brightness 0;")
open("flash.cmd","w").write("\n".join(linhas))
```
- `i % 2` derruba metade das batidas: pulsar em TODA batida cansa (mesma lição do "não cortar em toda batida", https://beat2cut.com/blog/beat-sync-video-editing-complete-guide/). Ajustar para 1-em-4 (só compasso) quando a trilha for muito marcada — leitura minha.

## 4. Receita A (hero) — respiro de luminância no downbeat, sem mudar o tamanho do frame
Por que `eq brightness`: muda o brilho SEM redimensionar o vídeo (diferente de crop/scale) — é o pulso mais invisível. Params e suporte a comando em https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Video/eq.html (brightness -1..1 default 0; precisa `eval=frame` para reavaliar).
```bash
ffmpeg -i video_master.mp4 -filter_complex \
  "[0:v]sendcmd=f=flash.cmd,eq=eval=frame[v]" \
  -map "[v]" -map 0:a -c:a copy -c:v libx264 -crf 18 out.mp4
```
- Alternativa mais "cinema" que brilho: pulsar `contrast` (+0.10, faixa -1000..1000, default 1) em vez de brightness — o preto fica mais preto no golpe, casa com o P&B prata. Leitura minha: contrast 1.0→1.12 no beat, voltando; combina com o `eq contrast=1.12` que já é padrão da marca (MONTAGEM-DA-CASA.md).
- **Onde NÃO**: nunca durante a frase de impacto (a atenção é a voz) — só no corpo e nas viradas.

## 5. Receita B — punch-in de micro-zoom na batida (crop comandável + scale de volta)
`crop` aceita comando; para o zoom não mudar a resolução de saída, recompõe com `scale` depois. Cada beat encolhe o crop por 4-6 frames e volta.
```
# zoom.cmd — 3% de punch por ~5 frames no beat de t=12.400
12.400-12.567 [enter] crop w 1862 h 1047 x 29 y 16,
              [leave] crop w 1920 h 1080 x 0  y 0;
```
```bash
ffmpeg -i in.mp4 -filter_complex \
  "[0:v]sendcmd=f=zoom.cmd,crop=1920:1080:0:0,scale=1920:1080[v]" \
  -map "[v]" -map 0:a -c:a copy out.mp4
```
- Matemática do centro (leitura minha): para punch de fator f (ex.: 1,03), `w=1920/f`, `h=1080/f`, `x=(1920-w)/2`, `y=(1080-h)/2` — mantém o quadro centrado. Gerar as 4 linhas por beat no mesmo script da seção 3.
- Leitura minha: punch de 2-3% é o teto para narração; acima disso vira "tremor de batida" e briga com o zoompan contínuo. Usar Receita A OU B por trecho, nunca as duas no mesmo beat.

## 6. Receita C — pulso dentro do zoompan (quando não dá para usar sendcmd)
`zoompan` não é comandável, então o pulso vai na EXPRESSÃO `z`, somando um bump nas batidas. Base do zoompan/Ken Burns: https://mko.re/blog/ken-burns-ffmpeg/ e https://creatomate.com/blog/how-to-zoom-images-and-videos-using-ffmpeg
```
# ken burns contínuo (zoom-in lento) + micro-bump de 0.02 perto de cada beat
z='1.0008^on + 0.02*exp(-40*pow(mod(in_time,0.5)-0,2))'
```
- Leitura minha: a soma `base_kenburns + gaussiana_no_beat` mantém a direção contínua (regra do match de movimento, guia anterior) e injeta o pulso. Para beats irregulares, o script gera a expressão como uma SOMA de gaussianas nos tempos reais do `beats.txt` (uma por beat) — funciona, mas fica longa; preferir sendcmd (Receita A/B) quando o filtro permitir. Custo: nenhum asset novo, só render.

## 7. Transições invisíveis por EXPRESSÃO — `xfade=transition=custom:expr=...`
O guia FFMPEG-TRANSICOES-E-J-CUTS.md regrou `xfade` pronto (`fade`, `fadegrays`). Aqui vai o nível avançado: transição com curva de EASING para a dissolve não parecer mecânica. Fonte: https://github.com/scriptituk/xfade-easing/blob/main/README.md e doc do filtro https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Video/xfade.html
- Variáveis do `expr`: **`P`** progresso da transição, **`X`/`Y`** pixel, **`W`/`H`** tamanho, **`A`/`B`** valor do 1º e 2º vídeo, **`PLANE`** plano de cor.
- Dissolve linear (o `fade` comum, para comparar): `expr='A*(1-P)+B*P'`.
- Dissolve com easing cúbico (começa e termina suave — some melhor): guarda o progresso suavizado em `st(0,...)` e usa `ld(0)`:
```
xfade=transition=custom:duration=0.6:offset=6.4:expr=
 'st(0, if(lt(P,0.5), 4*P^3, 1-4*(1-P)^3)); A*(1-ld(0))+B*ld(0)'
```
- **OBRIGATÓRIO** com `st()`/`ld()`: rodar `ffmpeg ... -filter_complex_threads 1`, senão as variáveis de estado corrompem entre threads (render fica mais lento — https://github.com/scriptituk/xfade-easing/blob/main/README.md).
- Leitura minha para a marca: a dissolve easada de 0,4-0,6s SÓ na virada de capítulo (3-6 por vídeo); no P&B ela desaparece melhor que a linear. Wipes/shapes continuam proibidos. Para 30min, ligar `-filter_complex_threads 1` só nos trechos com xfade custom, não no vídeo todo (custo de CPU).

## 8. `enable` — ligar um efeito só na janela da virada (sem sendcmd)
Muitos filtros aceitam `enable='expressão'`: se dá diferente de zero, o filtro age; senão o frame passa intacto (https://ffmpeg.org/ffmpeg-filters.html, seção Timeline editing).
```bash
# grão de filme só nos 2s da virada (12.0–14.0), overlay de partícula só na virada seguinte
[0:v]noise=alls=6:allf=t:enable='between(t,12,14)'[v1]
```
- `between(t,a,b)` liga na janela; `gte(t,x)` liga a partir de x (exemplo oficial: `smartblur=enable='between(t,10,180)'`). 
- Leitura minha: casa com o overlay de oclusão do guia anterior — em vez de deixar a fumaça o vídeo todo, `enable` acende o overlay só nos ~1,5s que cruzam o corte da virada. Menos CPU, mais intenção.

## 9. Custo, CPU e disciplina (para caber em 3 vídeos/semana)
- `sendcmd`+`eq`/`crop` re-encoda o vídeo (é filtro de vídeo) — mas é 1 passada, sem asset novo. Gerar `flash.cmd`/`zoom.cmd` é instantâneo a partir do `beats.txt`.
- `-filter_complex_threads 1` (exigido pelo xfade custom) reduz paralelismo → render mais lento; isolar em segmentos curtos das viradas e concatenar (leitura minha; consequência direta da nota de thread-safety da fonte da seção 7).
- Regra da casa (leitura minha): **1 técnica de pulso por trecho** (A ou B ou C), **respiro só em metade/quarto das batidas**, **transição custom só na virada**. Se a timeline "dança", cortar pulsos — o padrão é sobriedade.

## 10. Checklist antes do render
- [ ] `beats.txt` gerado (aubiotrack) e `flash.cmd`/`zoom.cmd` derivados dele por script?
- [ ] `sendcmd` posicionado ANTES do filtro-alvo (`eq`/`crop`) na cadeia, e `eq=eval=frame`?
- [ ] Pulso ativo em no máximo metade das batidas; nenhum pulso sobre a frase de impacto?
- [ ] Receita A **ou** B por trecho — nunca as duas no mesmo beat?
- [ ] `xfade=custom` só na virada, com `-filter_complex_threads 1` ligado nesse segmento?
- [ ] Overlays/grão em `enable='between(t,...)'` só na janela da virada, não no vídeo todo?
- [ ] Preview conferido: o pulso é SENTIDO, não VISTO (se dá para apontar "aqui pulsou", está forte demais)?

## Como aplicar no próximo vídeo
1. **Plugar o gerador de comandos no pipeline**: depois do `aubiotrack`, rodar o script da seção 3 e emitir `flash.cmd` — o respiro de `eq contrast` no downbeat entra como etapa automática, zero decisão manual.
2. **Escolher Receita A como padrão** (respiro de luminância, invisível) e reservar a B (punch-in) só para 1-2 capítulos de maior energia por vídeo.
3. **Trocar a dissolve das viradas pela versão easada** (`xfade=custom` cúbico, seção 7) nas 3-6 viradas, com `-filter_complex_threads 1` só nesses segmentos; comparar no preview com a `fadegrays` atual e ficar com a que some mais.
4. **Migrar overlays e grão para `enable=between(t,...)`**: acender só na janela da virada — corta CPU e concentra o efeito onde tem intenção.
5. **Rodar a auditoria dos 5s (RITMO-DE-RETENCAO-2026.md) já com os pulsos ativos**: o respiro na batida conta como "mudança" e tampa janelas paradas sem precisar de corte extra.
6. **Medir com controle**: na semana de 3 vídeos, aplicar pulso na batida em 2 e deixar 1 sem; anotar diferença de retenção no PESQUISA.md antes de virar regra fixa.
