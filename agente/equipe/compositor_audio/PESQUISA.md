# Mandato de pesquisa — Compositor

## Varredura ciclo 2 — 2026-07-17
**O que estudei:** aprofundamento dos três eixos avançados. (1) A taxonomia REAL de filtros do YouTube Audio Library (6 filtros: título/gênero/humor/artista/atribuição/duração; 10 humores) e o mapa humor-do-filtro → seção. (2) Escolha de TEMPO (BPM) por seção com faixas numéricas + casar corte e batida + receita `acrossfade` para trocar faixa entre seções. (3) O lado da FREQUÊNCIA do ducking: EQ "espaço para a voz" (high-pass + corte 2–4 kHz na música), que complementa o sidechain de nível do ciclo anterior. Já existiam (run anterior deste ciclo) os guias de sidechain avançado e de trilha-por-seção/catálogo-por-artista; NÃO repeti — fui para o operacional e para a frequência.

**Aprendizados-chave:**
- O Audio Library tem 6 filtros combináveis e o humor é um deles; para a marca, filtrar sempre por **Calm + Ambient** primeiro (humores úteis: calm/bright/inspirational; angry/funky/happy/dramatic fora).
- Content ID não reivindica o que sai do Audio Library; download é MP3 pelo botão dentro do Studio (fonte oficial Google).
- BPM por seção: GANCHO 60–80, LEI 60–75, PRÁTICA 85–105, CTA 90–110 (faixas de tempo da artist.io: slow 20–70, medium-slow 70–90, medium 90–110, medium-fast 110–130, fast 130–200).
- O Audio Library NÃO filtra por BPM — medir depois e anotar no banco de trilhas.
- Troca de faixa entre seções = `acrossfade=d=2:c1=tri:c2=tri`, montada ANTES do mix com a voz; cruzar só em respiro da narração.
- Mascaramento de frequência: a voz mora em 2–4 kHz; se a música tem energia lá, compete com a fala MESMO 20 dB abaixo — sidechain (nível) não resolve isso, só EQ (frequência).
- Solução = EQ subtrativo NA MÚSICA: high-pass ~150 Hz + sino largo -3 dB em ~3 kHz (`highpass=f=150,equalizer=f=3000:t=q:w=1.2:g=-3`), aplicado antes do sidechain/amix e antes do loudnorm.
- Diagnóstico na ordem: mascarou → mexer PRIMEIRO no EQ (frequência), SÓ DEPOIS no sidechain (nível).
- Confirmação externa da nossa regra: guia de voice-over cita música começando em ~-20 dB (bate com `alvo = voz_mean - 20`).

**Fontes:** https://support.google.com/youtube/answer/3376882 · https://typecast.ai/learn/youtube-audio-library/ · https://www.voices.com/blog/your-complete-guide-to-the-youtube-audio-library/ · https://www.socialpilot.co/youtube-marketing/youtube-audio-library · https://new-blog.artlist.io/blog/music-bpm/ · https://www.dl-sounds.com/how-to-sync-music-in-your-edit-like-a-pro/ · https://www.silvermansound.com/bpm-to-fps-calculator · https://ffmpeg.org/ffmpeg-filters.html · https://www.masteringbox.com/learn/frequency-masking · https://theproducerschool.com/blogs/music-production/frequency-masking-explained-complete-guide-for-producers · https://unison.audio/eq-frequency-chart/ · https://omegafilminstitute.com/voice-over-mixing/ · https://www.audiolibrary.com.co/ · https://inaudio.org/

**Guias gerados:** AUDIO-LIBRARY-FILTROS-HUMOR-E-TEMPO.md · EQ-ESPACO-PARA-A-VOZ-DUCKING-POR-FREQUENCIA.md

**Próximo estudo:** medir BPM das faixas do banco e criar o `BANCO-TRILHAS.md` com 12 aprovadas (3 por seção); testar dynamic EQ / `anequalizer` para pocket que só corta quando a voz fala (EQ + sidechain no mesmo passo); calibrar release do sidechain por medição no vídeo real; confirmar termos da Pixabay License na fonte primária (pendência herdada do ciclo 1).

## Varredura 2026-07-17
**O que estudei:** normalização de loudness do YouTube (alvo, comportamento, Stats for nerds), loudnorm em 2 passadas, ducking automático via sidechaincompress no ffmpeg, separação voz/música (consenso profissional + W3C + BBC), regras de licença das 3 fontes de trilha (YouTube Audio Library, incompetech/Kevin MacLeod, Pixabay) e emoção da trilha por seção do vídeo (retenção).

**Aprendizados-chave:**
- YouTube normaliza para -14 LUFS integrado SÓ PARA BAIXO: áudio abaixo de -14 toca mais baixo que a plataforma inteira — nossa v3 em -16,3 LUFS perde ~2,3 dB de presença.
- Teto de pico: YouTube pede -1 dBTP, mas exportar com TP=-1,5 dá folga para picos intersample do codec AAC/Opus.
- loudnorm em 2 passadas (medir com print_format=json → aplicar com linear=true e measured_*) crava o alvo; 1 passada só estima.
- Nossa regra de 18–20 dB de separação voz/música é exatamente o consenso profissional (W3C pede ≥20 dB; <15 dB mascara a fala; >25 dB some a música).
- sidechaincompress (threshold=0.03, ratio=8, attack=20, release=300) faz a música respirar nos silêncios da voz sem invadir a fala — próximo upgrade do pipeline.
- Audio Library é a única fonte que o YouTube GARANTE contra Content ID; faixas CC da biblioteca exigem crédito na descrição (texto gerado pela própria biblioteca).
- Crédito exato do Kevin MacLeod (CC BY 4.0): título + "Kevin MacLeod (incompetech.com)" + link da licença; monetização permitida com crédito.
- Retenção: cada capítulo/virada emocional pede faixa nova ou variação; BPM casa com o ritmo do corte; nunca 1 faixa em loop por 20–30 min.

**Fontes:** https://apu.software/youtube-audio-loudness-target/ · https://support.google.com/youtube/answer/3376882 · https://incompetech.com/music/royalty-free/faq.html · https://dev.to/masonwritescode/two-pass-loudness-normalization-with-ffmpeg-loudnorm-the-right-way-1nm3 · https://32blog.com/en/ffmpeg/ffmpeg-audio-normalization-loudnorm · https://www.ffmpeglab.com/articles/ffmpeg-audio-mixing-amix-guide.html · https://pureaudioinsight.com/blogs/content-production/background-music-volume-how-loud-should-it-be · https://soundraw.io/blog/post/how-to-use-music-to-improve-viewer-engagement-and-retention-on-youtube · https://www.nature.com/articles/s41599-022-01461-5

**Guias gerados:** LOUDNESS-YOUTUBE-DUCKING-SIDECHAIN.md · TRILHA-LICENCA-LIVRE-EMOCAO-POR-SECAO.md

**Próximo estudo:** confirmar termos da Pixabay License na fonte primária; testar sidechain no pipeline real e calibrar release por medição; pesquisar EQ de "espaço para a voz" (corte suave 2–4 kHz na música) e stems/variações de intensidade da mesma faixa para builds por seção.

## Mandato
SUA ESPECIALIDADE: trilha e loudness.
Pesquisar: faixas novas de licença limpa no clima da marca (piano/ambient inspirador), padrões de loudness do YouTube, técnicas de ducking automático (sidechain) para subir a música nos silêncios da voz.
## Como registrar o que aprender
Todo achado vira arquivo na sua BIBLIOTECA/ (um tema por arquivo, com fonte e data).
Achado que muda REGRA da produção → avisar o Gerente para atualizar a DOUTRINA e o painel.
Cadência: revisão da função TODA SEMANA junto da varredura de segunda-feira do Pesquisador.
