# Ducking sidechain avançado no ffmpeg — receita de produção completa

> Compositor de Áudio · Varredura ciclo 2 — 2026-07-17 · Complementa LOUDNESS-YOUTUBE-DUCKING-SIDECHAIN.md seção 4 (lá: conceito e comando base; aqui: tabela oficial COMPLETA de parâmetros, o roteamento correto com asplit que evita o comando falhar, threshold calculado em dB em vez de chutado, ducking parcial com `mix`, e a receita de ponta a ponta integrada ao nosso pipeline).

## 1. Tabela oficial completa do sidechaincompress (FFmpeg 8.0)

Fonte de TODOS os números desta tabela: https://ayosec.github.io/ffmpeg-filters-docs/8.0/Filters/Audio/sidechaincompress.html (espelho da documentação oficial de filtros do FFmpeg).

| Parâmetro | Default | Faixa | O que faz |
|---|---|---|---|
| `level_in` | 1 | 0.015625–64 | ganho de entrada do sinal principal (a música, no nosso caso) |
| `mode` | downward | upward/downward | downward = abaixa o que passa do threshold (o que queremos) |
| `threshold` | 0.125 | 0.00097563–1 | nível do SIDECHAIN (voz) que dispara a redução |
| `ratio` | 2 | 1–20 | força da redução (2 = suave; 8+ = agressivo) |
| `attack` | 20 ms | 0.01–2000 | quanto tempo a voz precisa ficar acima do threshold para o ducking começar |
| `release` | 250 ms | 0.01–9000 | quanto tempo depois da voz cair a música volta |
| `makeup` | 1 | 1–64 | ganho de compensação PÓS-compressão (nós não usamos: quem crava nível é o loudnorm) |
| `knee` | 2.82843 | 1–8 | arredonda a entrada na compressão (maior = transição mais macia) |
| `link` | average | average/maximum | como os canais do sidechain contam para o gatilho |
| `detection` | rms | peak/rms | rms = mais suave (default); peak = reage a picos exatos |
| `level_sc` | 1 | 0.015625–64 | ganho SÓ do sidechain — sobe/desce a sensibilidade sem mexer no threshold |
| `mix` | 1 | 0–1 | quanto do sinal comprimido entra na saída (menos de 1 = ducking parcial) |

## 2. Roteamento correto: asplit (o detalhe que faz o comando falhar)

Forma canônica da documentação oficial (mesma fonte da seção 1) — o stream que serve de gatilho E entra no mix precisa ser DUPLICADO com `asplit`:

```
[1:a]asplit=2[sc][mix];[0:a][sc]sidechaincompress[compr];[compr][mix]amerge
```

Adaptado ao nosso caso (voz = gatilho E precisa estar no mix final; música = quem é comprimida):

```
ffmpeg -i voz.wav -i musica_pre.wav -filter_complex ^
"[0:a]asplit=2[voz_sc][voz_mix]; ^
 [1:a][voz_sc]sidechaincompress=threshold=0.01:ratio=3:attack=20:release=400:detection=rms[duck]; ^
 [voz_mix][duck]amix=inputs=2:duration=first:normalize=0[a]" ^
-map "[a]" -ar 48000 mix_bruto.wav
```

- Ordem dos rótulos no sidechaincompress: **primeiro quem apanha (música), segundo quem manda (voz)**.
- **Leitura minha (alerta):** o comando base do ciclo 1 (via ffmpeglab) referencia `[0:a]` duas vezes SEM asplit; em versões estritas do ffmpeg isso falha porque cada stream de entrada só pode alimentar um filtro. A forma com `asplit` é a canônica da documentação oficial — usar SEMPRE esta. Testar as duas no nosso ffmpeg e padronizar a que roda.
- `normalize=0` no amix continua LEI: a voz nunca abaixa (guia anterior).

## 3. Threshold calculado em dB (parar de chutar)

Conversão (usada no exemplo real do gist https://gist.github.com/mhavo/533fa9586bdd090836116bac71c769f0): `threshold_linear = 10^(dB/20)`.

| dBFS desejado | threshold |
|---|---|
| -20 dB | 0.1 |
| -30 dB | 0.0316 |
| -40 dB | 0.01 |
| -50 dB | 0.0032 |
| -60 dB | 0.001 |

- O `0.03` que usamos no ciclo 1 equivale a ≈ **-30,5 dBFS**; o gist usa `0.00098` ≈ **-60 dBFS** (dispara com qualquer sopro de voz).
- **Como calibrar com a NOSSA medição** (leitura minha): a voz da v3 mede mean ≈ -16,6 dB falando; o threshold deve ficar entre o nível de fala e o ruído de fundo dos silêncios. Ponto de partida: **-35 a -40 dBFS (0.018–0.01)** — a música só volta quando a voz realmente parou, não em micro-pausas de vírgula. Ajustar `level_sc` (não o threshold) se o gatilho estiver sensível demais ou de menos.

## 4. Ducking parcial e suave — receita do mundo real (gist mhavo)

Comando completo do gist (fonte: https://gist.github.com/mhavo/533fa9586bdd090836116bac71c769f0) — caso deles: abaixar a MÚSICA quando entra uma vinheta/ID em momento específico:

```
ffmpeg -y -i audio.wav -i id.wav -filter_complex \
"[1]apad,adelay=17900|17900,aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[sc][id]; \
 [0][sc]sidechaincompress=threshold=0.00098:ratio=1.2:makeup=1:level_sc=0.5:release=150:mix=0.7[compr]; \
 [compr][id]amix=inputs=2:duration=first" out.wav
```

O que aproveitar dele:
- **`mix=0.7`** = ducking PARCIAL: 70% do sinal comprimido + 30% do original → a música cede sem "sumir e voltar" (efeito bomba). É o parâmetro que deixa o ducking imperceptível.
- **`ratio=1.2` (baixíssimo)** funciona porque lá o objetivo é ceder pouco; combinado com `mix`, o efeito total é suave.
- **`aformat=sample_rates=48000:channel_layouts=stereo`** antes do sidechain evita mismatch de formato entre voz e música (nossas fontes vêm de origens diferentes — TTS mono vs MP3 estéreo — este filtro é obrigatório no nosso caso).
- `apad`/`adelay` são do caso deles (vinheta entrando aos 17,9 s) — NÃO copiar cegamente.
- **Leitura minha:** no nosso pipeline a música já entra 20 dB abaixo da voz (fórmula da casa), então o ducking é REFINO, não salvação: `ratio=2–4` com `mix=0.7–0.8` deve bastar; o `ratio=8` do ciclo 1 provavelmente é agressivo demais em cima de música que já está -20 dB. Decidir por A/B medido, não por gosto.

## 5. Receita de produção de ponta a ponta (ordem das operações)

1. Medir a voz: `ffmpeg -i voz.wav -af volumedetect -f null -` → anotar `mean_volume`.
2. Pré-gain da música pela fórmula da casa: `alvo = voz_mean - 20`; calcular `GANHO_DB = alvo - musica_mean` (MIX-POR-MEDICAO.md).
3. Mix com ducking (uma chamada só — pré-gain + fade + sidechain + amix):

```
ffmpeg -i voz.wav -i musica.mp3 -filter_complex ^
"[1:a]volume=GANHO_DBdB,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=2[m1]; ^
 [0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[sc][vz]; ^
 [m1][sc]sidechaincompress=threshold=0.01:ratio=3:attack=20:release=400:detection=rms:mix=0.8[duck]; ^
 [vz][duck]amix=inputs=2:duration=first:normalize=0[mix]" ^
-map "[mix]" -ar 48000 mix_bruto.wav
```

4. `afade` out de 6 s no fechamento (lei da casa) — aplicar no corte final da música.
5. loudnorm em 2 passadas mirando I=-14, TP=-1.5 (receita completa no guia LOUDNESS — não repito).
6. Conferir com `ebur128` + `volumedetect` e gravar tudo no mix_manifesto.json, agora com o bloco:
   `"ducking": {"on": true, "threshold": 0.01, "ratio": 3, "attack": 20, "release": 400, "mix": 0.8, "detection": "rms"}`

### Como validar que o ducking está BOM (medição, não ouvido)
- Recortar 2 trechos: um COM narração contínua e um respiro ≥2 s SEM voz; rodar `volumedetect` em cada um no mix final.
- Esperado: música no respiro ~4–8 dB mais alta que música sob a fala (subiu, respirou) e separação voz/música ≥18 dB nos trechos falados (lei da casa intacta).
- Se a música "bombear" (sobe e desce audível dentro de frases): aumentar `release` (400→600) ou abaixar o threshold; se ela nunca subir nos respiros: threshold alto demais ou `release` maior que o respiro.

## Como aplicar no próximo vídeo

1. No mix do vídeo de domingo 10h, rodar a receita da seção 5 num trecho de teste de 2 min com pausas reais de narração e validar pela medição (música sobe 4–8 dB nos respiros, ≥18 dB sob a fala).
2. Fazer A/B de 3 configurações no MESMO trecho: ciclo 1 (threshold=0.03, ratio=8), gist suave (ratio=1.2, mix=0.7) e a minha proposta (threshold=0.01, ratio=3, mix=0.8) — escolher pela medição + escuta no celular.
3. Padronizar o filtergraph com `asplit` + `aformat` (seção 2) no script de mix e aposentar a forma sem asplit antes que ela quebre num update do ffmpeg.
4. Gravar o bloco `ducking` no mix_manifesto.json do vídeo (parâmetros exatos + números da validação) — com 3 vídeos/semana, o manifesto é o que impede regressão silenciosa entre um mix e outro.
5. Se o A/B aprovar o ducking, avisar o Gerente: entrada do ducking na DOUTRINA de mix (mudança de regra = decisão dele), valendo já para quarta 19h.
