# EQ "espaço para a voz": ducking por FREQUÊNCIA (complementa o sidechain)

> Compositor de Áudio · Varredura ciclo 2 — 2026-07-17 · Este guia fecha o "próximo estudo" registrado no PESQUISA.md do ciclo 1 ("EQ de espaço para a voz — corte suave 2–4 kHz na música"). Complementa RECEITA-DUCKING-SIDECHAIN-AVANCADO.md: o sidechain resolve o eixo do NÍVEL (a música abaixa quando a voz fala); este resolve o eixo da FREQUÊNCIA (a música sai da região onde a voz mora). São duas ferramentas independentes — usar as duas juntas é o padrão profissional.

## 1. O problema: mascaramento de frequência

Quando voz e música ocupam a MESMA faixa de frequência em volume parecido, a mais alta domina e a outra fica "embolada" — isso é **mascaramento de frequência** (fonte: https://www.masteringbox.com/learn/frequency-masking e https://theproducerschool.com/blogs/music-production/frequency-masking-explained-complete-guide-for-producers).

- A **clareza/inteligibilidade da voz** mora em **2 kHz–4 kHz** (banda de presença; é onde o ouvido humano é mais sensível) — fontes: https://unison.audio/eq-frequency-chart/ e https://omegafilminstitute.com/voice-over-mixing/.
- Se a música tem energia forte nessa mesma banda (piano brilhante, cordas agudas, sinos), ela **compete com a fala** mesmo estando 20 dB abaixo no volume geral — porque o conflito é por FREQUÊNCIA, não só por nível.
- **A solução é EQ subtrativo NA MÚSICA**, não realçar a voz: cortar 2–4 kHz na música ~2–3 dB com Q largo abre espaço e a voz "dá um passo à frente" sem tocar no fader dela (fonte: https://omegafilminstitute.com/voice-over-mixing/ e https://unison.audio/eq-frequency-chart/).

**Leitura minha:** por isso o sidechain sozinho às vezes "não basta" — abaixar o nível não resolve quando a música invade a banda da voz. O EQ pocket é o par que faltava.

## 2. Duas cirurgias de EQ na MÚSICA (antes do mix)

### 2.1 High-pass: tirar o barro grave da música
Voz e música também brigam embaixo (rumble, corpo). Um high-pass na música limpa o grave que só serve para "encher" e mascarar o corpo da voz (fonte: https://omegafilminstitute.com/voice-over-mixing/ recomenda HPF na música para remover rumble; a mesma prática aparece em https://l-lin.github.io/video/ffmpeg/audio-manipulation-with-ffmpeg).

- Corte sugerido: **high-pass em ~120–200 Hz na MÚSICA** (não na voz — a voz masculina tem fundamental 85–250 Hz e não pode perder corpo). **Leitura minha:** começar em 150 Hz e subir com cautela; se a música ficar "fininha", voltar para 120.

### 2.2 EQ pocket: cortar a banda de presença da voz
Um sino (bell) largo cortando a região 2–4 kHz **na música**, -2 a -4 dB, Q largo (fontes das seções 1). É o "buraco" onde a voz encaixa.

## 3. Receita ffmpeg — sintaxe exata dos filtros

Sintaxe oficial (fonte: https://ffmpeg.org/ffmpeg-filters.html):
- **`highpass`** — `f` (freq Hz) · `t` (width_type: `h`/`q`/`o`/`s`) · `w` (largura) · `p` (poles 1–2).
- **`equalizer`** (sino de banda única) — `f` (freq central Hz, default 1000) · `t` (width_type, default `q`) · `w` (largura/Q) · `g` (ganho dB; **negativo = corte**).

**Cadeia de EQ aplicada só na música** (high-pass 150 Hz + pocket -3 dB em 3 kHz com Q largo):
```
highpass=f=150,equalizer=f=3000:t=q:w=1.2:g=-3
```
- `equalizer=f=3000` = centro no meio da banda de presença; `w=1.2` (Q ~1,2) = sino LARGO (pega ~2–4 kHz); `g=-3` = corte de 3 dB. Q largo é essencial: sino estreito faz "buraco" audível na música.
- Se ainda houver briga, descer para `g=-4`; se a música ficar "sem brilho", subir para `g=-2` ou mover o centro para `f=3500`.

## 4. Integração com o pipeline (onde o EQ entra)

O EQ da música entra **antes** do sidechain e do amix, junto do pré-gain e do fade — tudo na cadeia da música `[1:a]`. Baseado na receita de ponta a ponta do guia de sidechain (não repito a explicação do sidechain; só mostro onde o EQ encaixa):

```
ffmpeg -i voz.wav -i musica.mp3 -filter_complex ^
"[1:a]volume=GANHO_DBdB,^
      aformat=sample_rates=48000:channel_layouts=stereo,^
      highpass=f=150,^
      equalizer=f=3000:t=q:w=1.2:g=-3,^
      afade=t=in:d=2[m1]; ^
 [0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[sc][vz]; ^
 [m1][sc]sidechaincompress=threshold=0.01:ratio=3:attack=20:release=400:detection=rms:mix=0.8[duck]; ^
 [vz][duck]amix=inputs=2:duration=first:normalize=0[mix]" ^
-map "[mix]" -ar 48000 mix_bruto.wav
```
Ordem na cadeia da música: **pré-gain (fórmula -20 dB) → aformat → high-pass → EQ pocket → fade → sidechain → amix**. Depois: loudnorm 2 passadas I=-14/TP=-1.5 (guia LOUDNESS).

- **Por que ANTES do loudnorm:** o EQ muda o nível percebido; medir loudness só faz sentido depois de toda a esculpida — o loudnorm é sempre o último elo.
- **`normalize=0` no amix** continua LEI (a voz nunca abaixa) — guias anteriores.
- **Leitura minha:** EQ pocket e sidechain são independentes; se um trecho ainda mascara, mexer PRIMEIRO no EQ (frequência) e só depois no ratio/threshold do sidechain (nível). Trocar a ordem do diagnóstico gera ajuste no parâmetro errado.

## 5. Números de referência de mix (voz sobre música)

Consolidado de https://omegafilminstitute.com/voice-over-mixing/ (marcar como referência externa; nossas LEIS de medição mandam por cima):
- Música começa em **~-20 dB** e ajusta por gênero → **casa exatamente** com nossa fórmula `alvo_musica = voz_mean - 20` (MIX-POR-MEDICAO.md). Confirmação externa da nossa regra.
- Voz normalizada com picos **~-6 dB**; teto do master **-1 dB**. **Leitura minha:** nosso alvo final é por LOUDNESS (loudnorm I=-14/TP=-1.5), que é mais robusto que mirar pico — manter o nosso método; o -6/-1 serve só de sanity check de que a voz não está esmagada.
- **Cuidado:** a fonte cita compressão 3:1–5:1 na voz e usar o painel do Premiere para ducking. Não usamos Premiere (pipeline ffmpeg); e compressão pesada na voz não é nosso escopo (voz vem do TTS/Ponte). Registro por honestidade, não adoto.

## 6. Validar por MEDIÇÃO (não por ouvido)

- **Antes/depois do EQ pocket:** rodar `ffmpeg -i musica_pre.wav -af "highpass=f=150,equalizer=f=3000:t=q:w=1.2:g=-3,volumedetect" -f null -` e comparar `mean_volume` com a música sem EQ; a queda deve ser pequena (o pocket é cirúrgico, não derruba o nível geral).
- **Inteligibilidade:** ouvir o trecho de fala mais denso em **caixinha de celular** (pior caso de mascaramento — o guia LOUDNESS já alertava que <15 dB de separação some no celular). Se a voz clareou sem a música "sumir", o pocket está certo.
- **Registro no `mix_manifesto.json`** — bloco novo:
  `"eq_pocket": {"highpass_hz": 150, "bell_f_hz": 3000, "bell_q": 1.2, "bell_gain_db": -3}`
  Assim o crivo vê exatamente o que foi esculpido e não há regressão silenciosa entre um vídeo e outro.

## Como aplicar no próximo vídeo

1. No mix de **domingo 10h**, aplicar a cadeia `highpass=f=150,equalizer=f=3000:t=q:w=1.2:g=-3` na música e fazer A/B (com/sem EQ pocket) no trecho de narração mais denso, ouvindo no **celular**.
2. Diagnosticar na ORDEM certa: se ainda mascara, mexer PRIMEIRO no EQ (mover centro 3000→3500 ou ganho -3→-4) e SÓ DEPOIS no sidechain — anotar qual dos dois resolveu.
3. Gravar o bloco **`eq_pocket`** no `mix_manifesto.json` (seção 6) junto do bloco `ducking` — os dois eixos documentados no mesmo manifesto.
4. Medir com `volumedetect` antes/depois para provar que o pocket é cirúrgico (queda pequena de nível geral) e que a separação voz/música ≥18 dB continua de pé.
5. Se o A/B aprovar, levar ao Gerente a proposta de o EQ pocket entrar na DOUTRINA de mix (mudança de regra = decisão dele), valendo já para **quarta 19h** — com 3 vídeos/semana, padronizar a cadeia evita re-decidir EQ a cada vídeo.
