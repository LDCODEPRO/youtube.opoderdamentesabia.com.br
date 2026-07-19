# A voz da narração — tratamento e espaço sonoro (a matéria-prima do canal)
*Varredura ciclo 2 · 2026-07-17 · O guia SOUND-DESIGN-SUTIL-WHOOSH-RISER-IMPACTO.md cuidou dos SFX e das RÉGUAS de mix (níveis, LUFS, camadas). Ele NÃO trata a VOZ em si. Aqui: limpar, equalizar, de-essar, comprimir e dar espaço à narração motivacional, tudo em ffmpeg, sem DAW. A voz é o gancho do nosso canal — se ela soa amadora, nenhum b-roll salva. Fontes ao lado de cada número. "leitura minha" = opinião/adaptação. NUNCA número inventado.*

## 1. A ordem da cadeia (importa — leitura minha, com razão técnica)
Ordem que uso, do bruto ao pronto:
**denoise → highpass → EQ (tira barro, dá presença) → de-ess → compressor → loudnorm (LUFS + true peak).**
- Por que denoise ANTES de tudo: comprimir/equalizar primeiro amplifica o chiado junto (leitura minha; consequência de ganho antes de limpeza).
- Por que de-ess DEPOIS da EQ de presença: o boost de 3-5 kHz (seção 5) acende os "sss" — o de-esser desce logo em seguida (leitura minha).
- Por que loudnorm por ÚLTIMO: normalização final é sempre a última etapa da cadeia (padrão de mastering; alvo na seção 9).

## 2. Limpeza — tirar chiado e ambiente (afftdn / arnndn)
Fontes: https://ayosec.github.io/ffmpeg-filters-docs/8.0/Filters/Audio/afftdn.html e https://odan.github.io/2023/08/20/reducing-background-audio-noise.html
- **afftdn** (denoiser no domínio da frequência): `nr` = redução em dB (default 12, faixa 0,01–97), `nf` = piso de ruído em dB (default -50, faixa -80 a -20), `nt` = tipo (white/vinyl/...), `tn` = rastrear ruído sozinho. Ponto de partida citado: `afftdn=nr=20:nf=-40`.
- **arnndn** (denoiser por rede neural, mais forte para ambiente): `arnndn=m=modelo.rnnn` — precisa baixar um modelo `.rnnn` (https://odan.github.io/2023/08/20/reducing-background-audio-noise.html).
- Leitura minha: se a gravação já é limpa (estúdio/booth), usar `afftdn=nr=10` leve ou pular — denoise pesado deixa a voz "debaixo d'água". Denoise é para SALVAR áudio ruim, não para embelezar áudio bom.

## 3. Highpass — o primeiro corte, sempre
Fonte da regra: https://producerhive.com/music-production-recording-tips/how-to-use-a-vocal-eq-chart/ (o high-pass "deve ser seu primeiríssimo movimento de EQ, entre 80–100 Hz")
- Tira ronco de mesa, ar-condicionado, plosivas e lama abaixo da voz. `highpass=f=90` (leitura minha: 90 Hz é o meio-termo seguro para voz masculina; subir para 100 Hz em voz mais aguda — https://producerhive.com/music-production-recording-tips/how-to-use-a-vocal-eq-chart/).
- Cuidado: cortar alto demais (>120 Hz) tira o CORPO da voz e a deixa fininha — o corpo mora em 100-300 Hz (https://producerhive.com/music-production-recording-tips/how-to-use-a-vocal-eq-chart/).

## 4. O "barro" — cortar 250-500 Hz (o que separa amador de profissional)
Fonte: https://producerhive.com/music-production-recording-tips/how-to-use-a-vocal-eq-chart/ e https://www.hollyland.com/blog/topics/use-equalization-in-audacity
- A zona **250-500 Hz** é a "mud zone": energia demais aí = voz abafada, "dentro de uma caixa de papelão". Corte suave de **-2 a -3 dB** limpa (https://www.hollyland.com/blog/topics/use-equalization-in-audacity).
- ffmpeg (`equalizer` = sino paramétrico; `width_type=q`): `equalizer=f=350:width_type=q:width=1.2:g=-3`.

## 5. Presença e ar — onde a voz motivacional "chega perto"
Fonte: https://producerhive.com/music-production-recording-tips/how-to-use-a-vocal-eq-chart/ e https://www.musicguymixing.com/eq-for-voice-over/
- **Presença 2-5 kHz**: boost gentil de **+2 dB** ~3 kHz faz a voz "cortar" e soar próxima/íntima (https://www.hollyland.com/blog/topics/use-equalization-in-audacity). `equalizer=f=3000:width_type=q:width=1.0:g=2`.
- **Ar 10 kHz+**: shelf alto suave dá "brilho/sopro" sem sibilância; opcional (https://producerhive.com/music-production-recording-tips/how-to-use-a-vocal-eq-chart/). ffmpeg shelf: `treble=g=2:f=10000` (highshelf).
- Leitura minha para P&B motivacional: presença SIM (a voz tem que soar como se falasse no ouvido do espectador), ar com parcimônia (exagero = voz sibilante e cansativa). EQ subtrativo primeiro (tirar barro), aditivo depois e pouco — mesma filosofia de "corte subtrativo" do guia de sound design.

## 6. De-esser — domar os "sss" sem tirar a clareza
Fonte dos parâmetros: https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Audio/deesser.html
- `i` = intensidade do gatilho (0–1, default 0), `m` = quanto duckar o agudo (0–1, default 0,5), `f` = quanto do conteúdo original manter (0–1, default 0,5), `s` = saída (`o` filtrado / `i` intacto / `e` só o "ess" para conferir onde ele age).
- Receita de partida (leitura minha, calibrar por teste): `deesser=i=0.1:m=0.5:f=0.5`. Usar `s=e` numa passada de teste para OUVIR só a sibilância e confirmar que ele pega os "s" e não a voz toda.
- Leitura minha: de-esser é cirurgia — intensidade mínima que resolve. Exagero deixa a voz com "lisp" (sem S).

## 7. Compressor — consistência sem esmagar (acompressor)
Fonte dos defaults/faixas: https://ffmpeg.org/ffmpeg-filters.html · filosofia para narração: https://creativecow.net/forums/thread/using-ffmpeg-to-optimize-vocals-in-recordings-an/
- `acompressor`: `threshold` (default 0,125; faixa 0,0009–1), `ratio` (default 2; faixa 1–20), `attack` ms (default 20), `release` ms (default 250), `makeup` (default 1; faixa 1–64), `knee` (default ~2,83).
- **Narração pede threshold BAIXO + ratio BAIXO** — o começo da compressão fica mais sutil que threshold/ratio altos (https://creativecow.net/forums/thread/using-ffmpeg-to-optimize-vocals-in-recordings-an/). Ponto de partida (leitura minha): `acompressor=threshold=0.1:ratio=3:attack=20:release=250:makeup=2`.
- Leitura minha: 2 compressores leves em série (ratio 2-3 cada) soam mais naturais que 1 pesado (ratio 8) — a voz fica constante sem "bombear". Attack ~20 ms deixa passar o ataque da consoante (inteligibilidade); release ~250 ms segue a fala sem chiar.
- Lembrete das fontes: dá para ter voz ótima com POUCO ou NENHUM processamento se o microfone/sala forem bons (https://creativecow.net/forums/thread/using-ffmpeg-to-optimize-vocals-in-recordings-an/). Processar é para corrigir, não para "dar produção".

## 8. Espaço/reverb sutil — a "grandeza íntima" (onde entra e onde NÃO)
Fonte dos parâmetros: https://ffmpeg.org/ffmpeg-filters.html (aecho)
- Voz totalmente seca soa "colada no rosto"; um fio de reverb dá ar e emoção sem tirar a intimidade. Reverb barato = `aecho` (eco curtíssimo simulando reflexão): `in_gain` (default 0,6), `out_gain` (default 0,3), `delays` ms (0–90000, separados por `|`), `decays` 0–1.
- Receita de partida (leitura minha, MUITO sutil): `aecho=0.8:0.85:40:0.08` — um único reflexo de 40 ms baixíssimo (decay 0,08). Predelay curto = sala pequena/íntima; delays longos = igreja (evitar — vira karaokê).
- **Onde NÃO**: nunca na frase de impacto seca com drop (o silêncio do guia de sound design pede voz LIMPA); nunca reverb audível — se dá para "ouvir o eco", está errado. Leitura minha: no máximo um véu; teste ligando/desligando — a versão certa é a que você sente falta quando tira, não a que você nota quando põe.

## 9. Loudness da voz — o alvo final (números com fonte)
- **-14 LUFS** é o padrão de normalização de YouTube/Spotify/Amazon; para fala (tutorial/podcast), a faixa saudável é **-14 a -16 LUFS** (https://www.criticallisteninglab.com/en/learn/loudness/youtube e https://clickyapps.com/creator/video/guides/lufs-targets-2025).
- AES define **-18 LUFS para voz/diálogo** e -14 para música; podcast costuma mirar **-16 LUFS estéreo / -19 LUFS mono** (https://lanceblairvo.com/lufs-voiceover-levels/ e https://www.natebegle.com/blog/voice-acting-lufs-loudness-vs-volume-explained).
- **True peak máximo -1 a -2 dBFS** em todas as plataformas (https://clickyapps.com/creator/video/guides/lufs-targets-2025).
- NÃO comprimir demais só para bater o número: um -14 LUFS sem dinâmica soa "sem vida" (https://clickyapps.com/creator/video/guides/lufs-targets-2025).
- Leitura minha (fecha com o guia de sound design): a VOZ mira **-16 LUFS** limpa; o MASTER final (voz+trilha+SFX) fecha em **-14 LUFS / TP -1,5** com `loudnorm=I=-14:TP=-1.5:LRA=11` (já regrado). A voz um pouco abaixo do master deixa espaço para a trilha sem estourar.

## 10. A receita completa da casa (uma passada, ordem da seção 1)
Leitura minha; todos os filtros documentados em https://ffmpeg.org/ffmpeg-filters.html
```bash
ffmpeg -i voz_bruta.wav -af \
"afftdn=nr=12:nf=-40,\
 highpass=f=90,\
 equalizer=f=350:width_type=q:width=1.2:g=-3,\
 equalizer=f=3000:width_type=q:width=1.0:g=2,\
 deesser=i=0.1:m=0.5:f=0.5,\
 acompressor=threshold=0.1:ratio=3:attack=20:release=250:makeup=2,\
 loudnorm=I=-16:TP=-1.5:LRA=11" \
 voz_tratada.wav
```
- Conferir depois: `ffmpeg -i voz_tratada.wav -af astats=measure_overall=RMS_level,volumedetect -f null -` (RMS/pico), e ouvir com o `deesser s=e` numa passada de teste para checar a sibilância.
- Para consistência entre os 3 vídeos/semana: guardar essa string como um preset único; só o `afftdn` varia conforme a limpeza da gravação (leitura minha).

## 11. Onde NÃO mexer (a disciplina da voz)
- Não apagar as RESPIRAÇÕES todas: um pouco de respiro é humano; voz sem respiro nenhum soa robótica (leitura minha).
- Não empilhar 5 EQs e 3 compressores: cadeia curta, cada filtro com uma função clara (seção 1).
- Não usar denoise/de-ess/reverb no talo: os três, no exagero, DESTROEM naturalidade (afftdn "debaixo d'água", de-esser "sem S", aecho "karaokê").
- A voz é PRIORIDADE absoluta na mix: SFX e trilha sentam atrás dela (regra já vigente no guia de sound design). O tratamento aqui é para a voz mandar sozinha, limpa.

## 12. Checklist antes de exportar a voz
- [ ] Highpass em 90-100 Hz aplicado (primeiro movimento)?
- [ ] Barro 250-500 Hz cortado -2/-3 dB; presença ~3 kHz com boost leve (+2 dB)?
- [ ] De-esser conferido com `s=e` — pega só os "sss", não a voz?
- [ ] Compressão leve (ratio 2-3), voz constante SEM bombear?
- [ ] Reverb (se usado) inaudível — só some quando tira?
- [ ] Voz em ~-16 LUFS, master final -14 LUFS, TP ≤ -1,5 dBTP?
- [ ] Ouvi em fone E em alto-falante de celular (teste da régua do guia de sound design)?

## Como aplicar no próximo vídeo
1. **Fixar o preset de voz** (seção 10) como etapa automática do pipeline, ANTES da mix com trilha/SFX — a voz entra na montagem já tratada, não crua.
2. **Calibrar uma vez com a voz do canal**: gravar 30s de teste, ajustar só o `afftdn` (limpeza) e o boost de presença ao timbre real; congelar o resto do preset para os 3 vídeos/semana.
3. **Adicionar a checagem de LUFS ao QC**: recusar export com voz fora de -14 a -16 LUFS ou master com TP acima de -1,5 (roda em segundos com loudnorm/astats).
4. **Reservar o reverb `aecho` sutil só para a abertura e o fechamento** (onde a voz quer soar "grande"); manter seca a frase de impacto com drop.
5. **Testar A/B numa semana**: 1 vídeo com o preset completo, 1 só com highpass+loudnorm (mínimo) — ouvir qual soa mais natural e anotar no PESQUISA.md; a meta é a voz mais crível, não a mais "produzida".
6. **Padronizar entre agentes**: se o Narrador entrega a voz sintetizada, aplicar o mesmo preset garante que os 3 vídeos da semana tenham o MESMO timbre e loudness — consistência de marca.
