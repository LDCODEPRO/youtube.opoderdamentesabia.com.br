# Corte na batida (sem editor manual) + transições invisíveis
*Varredura ciclo 2 · 2026-07-17 · Como o corte acompanha a música via aubio/librosa dentro do nosso pipeline ffmpeg, e como esconder a costura. Fontes ao lado; "leitura minha" = adaptação nossa. Complementa (não repete) FFMPEG-TRANSICOES-E-J-CUTS.md.*

## 1. As regras do corte musical (antes da ferramenta)
Fonte principal: https://beat2cut.com/blog/beat-sync-video-editing-complete-guide/
- Quando o corte cai na batida, o cérebro funde som+imagem numa experiência só — o espectador SENTE a edição em vez de assistir (https://bitcut.app/blog/beat-sync-video-editing).
- **NÃO cortar em toda batida** — "editing to every beat usually feels frantic". Cortes principais nos DOWNBEATS (tempos 1 e 3); acentos secundários no snare (2 e 4).
- **Cortar 1–2 frames ANTES da batida** parece mais "no tempo" que cortar em cima — o processamento visual leva tempo; a imagem nova chega, aí a batida bate (https://beat2cut.com/blog/beat-sync-video-editing-complete-guide/). A 30fps isso é 33–66ms de antecipação (conversão minha).
- Erros mapeados: over-syncing (fadiga visual), cortar no beat ignorando o que acontece na tela (descontinuidade), sincronia inconsistente (quebra o padrão), música com andamento errado para o conteúdo (https://beat2cut.com/blog/beat-sync-video-editing-complete-guide/).
- Leitura minha para NARRAÇÃO: a voz manda, a música serve. Nosso corte não persegue a batida — ele se ENCAIXA nela quando a fronteira da frase está perto de um beat. Beat-sync total é linguagem de music video, não de narração contemplativa.

## 2. Detectar batidas por linha de comando — aubio
Fontes: https://aubio.org/manual/latest/cli.html e https://aubio.org/
- Ferramentas: `aubioonset` (ataques/eventos), `aubiotrack` (batidas musicais), `aubiocut` (fatia o arquivo nos pontos detectados), além de `aubio onset|beat|tempo|pitch|quiet`.
- Opções que importam: `-i` input, `-O` método de detecção de onset (hfc, energy, complex...), `-t` threshold, `-T` formato de tempo (samples/ms/segundos), `-B` bufsize (padrão 512), `-H` hopsize (padrão 256), `-M` intervalo mínimo entre onsets.
```bash
# batidas da trilha, em segundos (uma por linha) — é o nosso beat grid
aubiotrack -i trilha.wav -T s > beats.txt

# onsets (ataques de qualquer evento sonoro), com filtro anti-duplicata de 30ms
aubio onset trilha.wav -M 30ms -t 0.3 -T s > onsets.txt
```
- `aubioonset --onset-threshold 0.1 --time-format ms` = receita testada de extração; threshold mais baixo → mais onsets (https://sighack.com/post/extract-onset-beat-times-from-audio-files).
- Converter ms→frame: `frame = ms × fps / 1000` — o mesmo artigo traz o script bash pronto dessa conversão (https://sighack.com/post/extract-onset-beat-times-from-audio-files).
- Leitura minha: para TRILHA instrumental calma (nosso caso), `aubiotrack` dá o grid limpo; `aubioonset` serve melhor para achar os SWELLS da música (entradas de instrumento) — que são os melhores pontos de virada de capítulo.

## 3. Alternativa Python — librosa (mais controle, mesmo custo zero)
```python
import librosa
y, sr = librosa.load("trilha.wav")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)      # tempo em BPM + frames das batidas
times = librosa.frames_to_time(beats, sr=sr)             # segundos
```
- `beat_track` devolve o BPM estimado + array de batidas; `frames_to_time` converte para segundos (https://librosa.org/doc/latest/generated/librosa.beat.beat_track.html).
- Existe utilitário pronto que exporta batidas/onsets como timestamps e marcadores EDL para NLEs (https://github.com/emjjkk/beat-detection) — útil como referência de formato, mas nós consumimos direto no gerador de concat (leitura minha).

## 4. A receita da casa — "snap to beat" no gerador de timeline
Leitura minha (algoritmo nosso; regras de base nas fontes da seção 1):
1. Rodar `aubiotrack` na trilha ANTES da montagem → `beats.txt`.
2. Para cada fronteira de cena vinda do roteiro (fim de ideia da narração), procurar a batida mais próxima.
3. **Se |cena − batida| ≤ 0,5s**: mover o corte para `batida − 0,05s` (o "1–2 frames antes" da seção 1). **Senão: não mexer** — a narração NUNCA desliza por causa da música.
4. Viradas de capítulo: escolher, entre as batidas candidatas, a que coincide com swell/onset forte (`onsets.txt`) — corte + música chegando juntos = interrupt de graça.
5. Downbeat só: se o BPM é conhecido (librosa), aceitar apenas batidas em posição 1 do compasso para cortes de capítulo (grade de 4 em 4 a partir do primeiro downbeat).
6. Pseudo-código do snap:
```python
def snap(t_cena, beats, tol=0.5, antecipo=0.05):
    b = min(beats, key=lambda x: abs(x - t_cena))
    return (b - antecipo) if abs(b - t_cena) <= tol else t_cena
```
7. Custo por vídeo: 1 rodada de aubiotrack (~segundos) + ajuste de lista — zero render extra. Cabe na cadência de 3/semana.

## 5. Transições invisíveis — a teoria (por que algumas costuras somem)
- **Invisible cut**: esconder a emenda com movimento rápido de câmera, oclusão (algo cobre a lente) ou escuridão breve — ilusão de take contínuo (https://morphic.com/ai-glossary/Match-Cut e https://medium.com/applaudience/invisible-cuts-a-new-trend-in-video-editing-b858ede7403d).
- **Match cut / cut on action**: casar a AÇÃO (ou a forma) do fim do plano A com o começo do B — a continuidade engole o corte (https://filmlifestyle.com/match-cuts-creative-transitions/ e https://www.studiobinder.com/blog/what-is-continuity-editing-in-film/).
- **Continuidade de movimento**: o efeito só funciona se direção, velocidade e estado de movimento se MANTÊM através do corte (https://www.soundstripe.com/blogs/the-invisible-editor-a-guide-to-continuity-editing-for-film-and-video).
- Meta da edição de continuidade: tornar o mecanismo invisível para o espectador mergulhar (https://www.studiobinder.com/blog/what-is-continuity-editing-in-film/).

## 6. Transições invisíveis no NOSSO pipeline (imagens + zoompan, sem filmagem)
Leitura minha — aplicação das 4 técnicas da seção 5 ao nosso material estático animado:
- **Match de movimento (a principal)**: o corte fica invisível quando o zoompan da cena B CONTINUA a direção e velocidade da cena A (A: zoom-in lento → B: zoom-in lento; nunca zoom-in → zoom-out na mesma sequência de ideia). Inverter direção SÓ na virada de capítulo — aí a quebra é proposital (base: continuidade de movimento, https://www.soundstripe.com/blogs/the-invisible-editor-a-guide-to-continuity-editing-for-film-and-video).
- **Match de luminância**: em P&B, um salto de brilho entre o último frame de A e o primeiro de B denuncia o corte. Medir com `signalstats` e reordenar/ajustar quando o salto for grosseiro:
```bash
# YAVG do último segundo da cena — comparar A(fim) com B(início); >40 de diferença (0-255) = salto visível (número meu, calibrar)
ffmpeg -sseof -1 -i cenaA.mp4 -vf signalstats,metadata=print:key=lavfi.signalstats.YAVG -f null - 2>&1 | tail -5
```
- **Oclusão sintética**: nossos overlays (fumaça/partículas em blend screen) são o "objeto que cobre a lente": programar o pico de densidade do overlay para cruzar o frame do corte — a textura mascara a emenda (técnica da oclusão: https://morphic.com/ai-glossary/Match-Cut).
- **Escuridão breve** (dip-to-black rápido): 4–6 frames de fade-out + 4–6 de fade-in lê como piscada, não como fade — usar 1–2x por vídeo em virada dramática; é diferente do fadeblack longo de 0,5–1s que já regramos (base "brief darkness": https://morphic.com/ai-glossary/Match-Cut).
- **Máscara sonora**: whoosh/riser com pico exatamente no frame do corte desvia a atenção da costura — som e imagem chegando juntos leem como evento único (https://bitcut.app/blog/beat-sync-video-editing). Casa com o guia SOUND-DESIGN-SUTIL-WHOOSH-RISER-IMPACTO.md: a MESMA virada ganha corte na batida + whoosh + troca de imagem.
- **Hierarquia da casa**: corte seco com match de movimento (padrão, custo zero) → + máscara sonora (viradas) → oclusão por overlay (2–3x/vídeo) → dip-to-black rápido (1–2x) → xfade/fadegrays (já regrado no guia anterior, só virada de clima).

## 7. Checklist antes do render
- [ ] `aubiotrack` rodado na trilha; fronteiras de cena passaram pelo snap (tol 0,5s, antecipo 0,05s)?
- [ ] Nenhuma cena deslizou a narração para perseguir batida?
- [ ] Direção do zoompan é contínua dentro de cada capítulo (só inverte na virada)?
- [ ] Viradas de capítulo: batida forte + swell + SFX + troca de imagem no MESMO ponto?
- [ ] Saltos de luminância entre cenas vizinhas conferidos (YAVG) nos cortes que "piscaram" no preview?
- [ ] Dip-to-black rápido usado no máximo 2x; overlays com pico cruzando o corte nas cenas marcadas?

## Como aplicar no próximo vídeo
1. **Integrar o snap-to-beat no gerador de concat**: rodar `aubiotrack -T s` na trilha escolhida e aplicar a função snap (seção 4) nas fronteiras de cena antes de gerar o filter_complex — narração intocável, tolerância 0,5s, antecipo de 50ms.
2. **Regra de direção do zoompan**: no plano de montagem, anotar a direção (in/out, esq/dir) por capítulo e manter contínua; inversão vira marcador de virada.
3. **Programar 2–3 oclusões por overlay**: escolher os cortes mais "duros" do vídeo e fazer o pico da fumaça/partícula cruzar o frame da emenda.
4. **Sincronizar a tríade da virada**: nas 3–6 viradas de capítulo, alinhar batida (downbeat/swell) + whoosh + troca de imagem no mesmo frame — 1 comando adelay+amix já resolve o som.
5. **Adicionar YAVG ao QC**: script compara luminância média fim-de-A vs início-de-B em toda emenda e lista as piores 3 para revisão manual rápida.
6. **Medir o efeito**: nos 3 vídeos da semana, aplicar snap-to-beat em 2 e deixar 1 sem (controle) — comparar retention graph na semana seguinte e registrar no PESQUISA.md.
