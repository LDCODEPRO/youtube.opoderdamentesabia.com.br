# Loudness no YouTube 2026 + Ducking automático (sidechain)

> Compositor de Áudio · Varredura 2026-07-17 · Complementa MIX-POR-MEDICAO.md (não repete a fundação; aqui é o estado da arte de plataforma e o próximo passo técnico: ducking).

## 1. O que o YouTube FAZ com o nosso áudio (normalização)

- Alvo da plataforma: **-14 LUFS integrado**, teto de pico real **-1 dBTP** (fonte: https://apu.software/youtube-audio-loudness-target/).
- A normalização é **só para baixo**: vídeo mais alto que -14 LUFS é atenuado na reprodução; vídeo mais baixo **NÃO é aumentado** — toca no volume original (fontes: https://apu.software/youtube-audio-loudness-target/ e https://www.loudfix.com/lufs-standard-youtube-2026/).
- Consequência: subir além de -14 não ganha nada (o YouTube abaixa e ainda arrisca distorção nos picos); ficar abaixo de -14 = tocar mais baixo que todo mundo.
- Como conferir depois do upload: player → botão direito → "Stats for nerds" → **"Content Loudness"** mostra o offset em relação a -14 LUFS (fonte: https://apu.software/youtube-audio-loudness-target/). Offset perto de 0 dB = mix no alvo.

### O que isso significa PARA O NOSSO CANAL
- Nossa v3 aprovada saiu em **-16,3 LUFS** (ver MIX-POR-MEDICAO.md). Isso toca ~2,3 dB mais baixo que a média da plataforma, porque o YouTube não sobe áudio baixo.
- **Leitura minha:** nossa regra "LUFS final -16 a -14" deve virar "**mirar -14 cravado**" (o intervalo era prudente na fundação; agora que medimos por loudnorm, dá pra cravar). Isso é mudança de REGRA → avisar o Gerente antes de virar doutrina.

## 2. Receita loudnorm em 2 passadas (o jeito certo)

1 passada só ESTIMA e erra o alvo; 2 passadas MEDEM primeiro e aplicam ganho linear preciso (fontes: https://dev.to/masonwritescode/two-pass-loudness-normalization-with-ffmpeg-loudnorm-the-right-way-1nm3 e https://32blog.com/en/ffmpeg/ffmpeg-audio-normalization-loudnorm).

**Passada 1 — medir (não gera arquivo):**
```
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1
```
Anotar do JSON: `measured_I`, `measured_TP`, `measured_LRA`, `measured_thresh`, `offset`.

**Passada 2 — aplicar com os valores medidos:**
```
ffmpeg -i mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:measured_I=XX:measured_TP=XX:measured_LRA=XX:measured_thresh=XX:offset=XX" -ar 48000 mix_final.wav
```
- `linear=true` = ganho uniforme, preserva a dinâmica original (fonte: https://mitz17.com/en/blog/ffmpeg-loudnorm-guide/).
- **TP=-1.5 e não -1.0:** o teto do YouTube é -1 dBTP, mas codecs com perda (AAC/Opus) criam picos intersample; -1,5 a -2,0 dBTP dá folga e evita clipping no decode (fonte: https://32blog.com/en/ffmpeg/ffmpeg-audio-normalization-loudnorm).
- Conferência final independente: `ffmpeg -i mix_final.wav -af ebur128 -f null -` e registrar o Integrated no mix_manifesto.json (nossa lei do crivo continua valendo).

## 3. Separação voz/música — nossa regra confere com o estado da arte

- Consenso profissional: música **18–20 dB abaixo** da voz (fonte: https://pureaudioinsight.com/blogs/content-production/background-music-volume-how-loud-should-it-be).
- W3C (acessibilidade): sons não-fala ao menos **20 dB abaixo** da fala em primeiro plano (citado na mesma fonte Pure Audio Insight).
- Perigo dos extremos (mesma fonte): **menos de 15 dB** de separação = mascaramento da fala (pior em caixinha de celular); **mais de 25 dB** = música praticamente inaudível.
- Nossa fórmula `alvo_musica_dB = voz_mean - 20` (MIX-POR-MEDICAO.md) já mira 20 dB — **estamos no ponto ótimo**; a lei "≥18 dB" é o piso, 20 é o alvo. Nada a mudar aqui.

## 4. Ducking automático (sidechain) — a música respira quando a voz para

Hoje nossa música fica FIXA 20 dB abaixo o vídeo inteiro. Com sidechain, a música **sobe sozinha nos silêncios** da narração e abaixa quando a voz volta — mais vida, sem invadir a fala.

**Comando base (fonte: https://www.ffmpeglab.com/articles/ffmpeg-audio-mixing-amix-guide.html):**
```
ffmpeg -i voz.wav -i musica.mp3 -filter_complex \
"[1:a][0:a]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck]; \
 [0:a][duck]amix=inputs=2:duration=first:normalize=0[a]" \
-map "[a]" mix.wav
```
- `threshold=0.03` — nível de voz que dispara o ducking
- `ratio=8` — força da compressão (8:1 abaixa bem a música quando há fala)
- `attack=20` — ms para reagir quando a voz entra (rápido = não pisa na primeira sílaba)
- `release=300` — ms para a música voltar quando a voz para
- Variante mais suave encontrada na pesquisa: `threshold=0.02, ratio=10, attack=50, release=500` (fonte: https://cloudinary.com/guides/video-effects/ffmpeg-add-audio-to-video). Exemplo real com `asplit`/`apad` em: https://gist.github.com/mhavo/533fa9586bdd090836116bac71c769f0
- **NOSSAS LEIS continuam por cima:** `normalize=0` no amix (a voz NUNCA abaixa) e a música pré-ajustada pela fórmula -20 dB ANTES do sidechain. O ducking é refinamento, não substitui a medição.
- **Leitura minha:** para narração contínua (nosso formato), release entre 300–500 ms soa natural; release curto demais "bombeia". Calibrar ouvindo os respiros entre frases e MEDIR o resultado (volumedetect por trecho) antes de aprovar.

## 5. Checklist de mix atualizado (ordem das operações)

1. Medir voz (`volumedetect`) → aplicar fórmula música = voz_mean - 20
2. Sidechain ducking (seção 4) com normalize=0
3. Fades: in 2 s / out 6 s (lei da casa)
4. loudnorm 2 passadas → I=-14, TP=-1.5 (seção 2)
5. Conferir com ebur128 + volumedetect → mix_manifesto.json (md5 + números)
6. Pós-upload: Stats for nerds → Content Loudness ≈ 0 dB

## Como aplicar no próximo vídeo

1. Rodar o mix do próximo vídeo com **loudnorm 2 passadas mirando I=-14, TP=-1.5** e comparar o resultado A/B com o pipeline atual (-16,3) no celular e no fone.
2. Testar o **sidechaincompress** (threshold=0.03, ratio=8, attack=20, release=300) num trecho de 2 min com pausas de narração; medir voz e música por trecho antes/depois.
3. Registrar no mix_manifesto.json dois campos novos: `lufs_integrado_pos_loudnorm` e `ducking` (on/off + parâmetros).
4. Depois do upload, printar o **Stats for nerds → Content Loudness** e anexar ao manifesto (prova real de que o alvo foi atingido).
5. Levar ao Gerente a proposta de mudar a doutrina de "LUFS -16 a -14" para "-14 cravado via loudnorm 2 passadas" (mudança de regra = decisão dele).
