# Sound design sutil — whoosh, riser e impacto no vídeo motivacional (onde entram e onde NÃO)
*Varredura ciclo 2 · 2026-07-17 · Fontes ao lado de cada número. "Leitura minha" = opinião/adaptação para o nosso canal P&B de narração.*

## 1. O vocabulário (para pedir/procurar o som certo)
Fonte: https://blog.prosoundeffects.com/sound-effects-terms-explained-part-1
- **Whoosh**: sublinha MOVIMENTO (câmera, objeto, transição). Varia em velocidade, tom e textura.
- **Riser**: som que SOBE gradualmente (pitch/volume/intensidade) — constrói tensão antes de uma revelação.
- **Impact / hit**: contato de objeto com objeto — pontua chegada, título, corte forte.
- **Braam**: hit metálico, grande, de trailer — anuncia "algo épico vem aí". Leitura minha: para nós, quase sempre é EXAGERO; no máximo 1 por vídeo, na virada central.
- **Drop**: pausa deliberada que LIBERA a tensão — o silêncio depois do riser é o efeito.
- **Drone**: cama contínua de textura/atmosfera — suspense de fundo, não chama atenção.
- **Glitch**: "mau funcionamento estilizado" — linguagem sci-fi/tech, NÃO combina com a nossa marca (leitura minha).

## 2. A tríade que funciona junto (riser → corte → impacto → drop)
- Regra de posicionamento do riser: o PICO do riser alinha exatamente com o momento-chave (corte visual, revelação de título, virada) — não o começo, o PICO (https://www.epidemicsound.com/sound-effects/categories/designed/riser/).
- Durações típicas de riser em biblioteca: 1–4s (curto), ~6s (médio), até ~10s (longo) (https://www.epidemicsound.com/sound-effects/categories/designed/riser/).
- Combinação clássica: riser + fade/zoom visual no mesmo ponto = transição mais forte que qualquer um sozinho (https://www.epidemicsound.com/sound-effects/categories/designed/riser/).
- O silêncio DEPOIS do pico é metade do efeito: o drop dá o momento de absorver (https://blog.prosoundeffects.com/sound-effects-terms-explained-part-1). Leitura minha: no nosso formato, riser de 2–4s subindo até a fronteira do capítulo → 0,5–1s de quase-silêncio (só ambiente) → a frase de impacto do Narrador entra limpa. Isso é o nosso "amém" sonoro.

## 3. Anatomia do whoosh (para escolher/ajustar, não só colar)
Fonte: https://sound.krotosaudio.com/whoosh-sound-effects/
- Três partes: **ataque** (início), **corpo** (energia central), **cauda** (dissipação). O caráter vem da automação de volume — fade longo = transição lenta e elegante; subida rápida + impacto = pontuação seca.
- 4 bases de construção: gravações de ambiente (caráter), pratos/címbalos (brilho), ruído sintetizado (consistência), sub senoidal (peso).
- Prato REVERTIDO é o riser clássico de custo zero (inverter a waveform).
- Layering: sincronizar o PICO de cada camada no mesmo ponto; carve de EQ entre camadas para não embolar.
- Leitura minha para o nosso P&B: whoosh de textura "ar/ambiente" (vento, respiro) casa com a estética prata; whoosh "cartoon/swish agudo" é proibido.

## 4. ONDE NÃO ENTRA (a parte mais importante)
- SFX em TODO corte/zoom/texto é o erro nº1 de iniciante — vira ruído e irrita (https://creatorfactory.in/sound-effect-mistakes/ e https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing).
- "Se tudo é dramático, nada é especial" — o efeito só destaca se for raro (https://creatorfactory.in/sound-effect-mistakes/).
- Som stock genérico sem alteração = barato e reconhecível; alterar pitch/EQ/camadas antes de usar (https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing).
- SFX repentino e alto faz o espectador FECHAR o vídeo; a voz é sempre a prioridade, SFX senta atrás (https://creatorfactory.in/sound-effect-mistakes/).
- Meta profissional: áudio "invisível mas sentido" — tensão no silêncio, energia no impacto certo (https://www.nostairway.com/video-sound-effects-mistakes/).
- **Tabela de decisão da casa (leitura minha, coerente com as fontes):**
  | Momento | SFX? |
  |---|---|
  | Corte comum dentro do bloco (4–8s) | NUNCA |
  | Punch-in/zoom de pattern interrupt | NÃO por padrão; no máx. ambiente sobe 1 dB |
  | Virada de capítulo (3–6 por vídeo) | SIM: whoosh suave OU riser com pico no corte |
  | Frase de impacto central do vídeo | SIM: riser → drop (silêncio) → frase; impacto/braam só se o texto pedir peso |
  | Abertura (primeiros 5s) | 1 elemento no máximo — o gancho é a VOZ |
  | Encerramento/CTA | Nada novo; trilha resolve sozinha |

## 5. Níveis e mixagem — números de referência
Fonte: https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing
- Pico do master: **-6 a -3 dB**; limiter no bus com ceiling **-1 a -1.5 dBTP**.
- Alvo de loudness streaming: **-14 LUFS** (bate com o nosso loudnorm do guia FFMPEG-TRANSICOES-E-J-CUTS.md).
- Camas de ambiente/drones: **-25 a -40 dB** — presença que só se nota quando falta.
- Máximo **3–5 camadas sonoras simultâneas**; hierarquia: voz → trilha → SFX/ambiente.
- High-pass em **80–100 Hz** nos SFX para não brigar com o corpo da voz; corte SUBTRATIVO em vez de boost.
- Testar em mono e em 3 sistemas (monitor, fone, alto-falante de celular).
- Leitura minha — régua da casa: voz segue ≥18 dB acima da trilha (regra já vigente); whoosh/riser mixados a **-20 a -26 dB abaixo do pico da voz**, nunca acima da trilha no momento em que a voz fala. Sincronia é crítica: atraso de poucos frames entre pico do SFX e o corte já é percebido (https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing).

## 6. Receita ffmpeg — colocar SFX no ponto exato sem DAW
Leitura minha; filtros documentados em https://ffmpeg.org/ffmpeg-filters.html
```bash
# whoosh no corte do capítulo em t=83.4s, -24dB, sem tocar na voz nem no vídeo
ffmpeg -i video_master.mp4 -i whoosh.wav -filter_complex \
  "[1:a]adelay=83400|83400,volume=-24dB[sfx];\
   [0:a][sfx]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy out.mp4
```
- `adelay` em **milissegundos**, um valor por canal; `normalize=0` impede o amix de abaixar a voz.
- Vários SFX = várias entradas com seus adelay somados no mesmo amix (`inputs=N`).
- Alinhar o PICO, não o início: se o riser tem 3s e o pico está no fim, `adelay = (t_corte − 3s) × 1000` (regra do pico: https://www.epidemicsound.com/sound-effects/categories/designed/riser/).
- Riser barato de prato revertido: `ffmpeg -i prato.wav -af areverse riser.wav` (técnica da reversão: https://sound.krotosaudio.com/whoosh-sound-effects/).
- Conferir que o SFX não estourou a régua: `ffmpeg -i out.mp4 -af astats=measure_overall=Peak_level -f null -`.

## 7. Checklist de sound design antes de exportar
- [ ] Contei os SFX do vídeo inteiro? (alvo: 3–8 no total para 10–20min; leitura minha)
- [ ] Todo SFX está numa VIRADA de capítulo ou momento central — nenhum em corte comum?
- [ ] Pico do riser cai NO frame do corte (não perto — nele)?
- [ ] Todo SFX passou por pitch/EQ/volume — nenhum som cru de biblioteca?
- [ ] Voz ≥18 dB acima de tudo no momento em que fala; SFX abaixo da trilha?
- [ ] Existe pelo menos 1 momento de quase-silêncio deliberado (drop) no vídeo?
- [ ] Master: pico -6 a -3 dB, loudnorm -14 LUFS, teste em fone + celular?

## Como aplicar no próximo vídeo
1. **Orçamento de SFX por vídeo**: fixar 3–8 efeitos no total (1 por virada de capítulo + 1 tríade riser→drop na frase central). Anotar no plano de montagem ANTES de editar — SFX não decidido na hora.
2. **Montar a mini-biblioteca da marca** (1x, serve para os 3 vídeos/semana): 2 whooshes de ar/vento, 2 risers (2s e 4s), 1 impacto grave suave, 1 drone P&B — todos re-pitchados/EQ para não soarem stock.
3. **Automatizar o adelay+amix** no script de montagem: o gerador de timeline já sabe onde estão as viradas — emitir a linha de filter_complex com os tempos calculados (pico no corte).
4. **Implantar o drop**: em cada vídeo, 1 momento de quase-silêncio de 0,5–1s após o riser central, antes da frase de impacto.
5. **Régua de mix no checklist de QC**: rodar astats no master e recusar export com SFX acima da régua (-20 dB do pico da voz) ou master fora de -14 LUFS.
6. **Cadência 3/semana**: sound design é etapa de 15min por vídeo usando a biblioteca pronta — se passar disso, simplificar (menos SFX, nunca mais SFX).
