# Catálogo de trilha com licença livre + emoção por seção do vídeo

> Compositor de Áudio · Varredura 2026-07-17 · Onde buscar música SEGURA (regras exatas de cada fonte) e COMO escolher a emoção da trilha para cada parte do nosso vídeo motivacional (5–30 min).

## 1. As três fontes seguras — regras exatas de cada uma

### 1.1 YouTube Audio Library (primeira escolha)
- Acesso exclusivo pelo YouTube Studio (menu lateral) ou youtube.com/audiolibrary (fonte oficial: https://support.google.com/youtube/answer/3376882).
- Música e efeitos da biblioteca são copyright-safe e **não são reivindicados pelo Content ID** (mesma fonte).
- Maioria das faixas: **sem atribuição** — filtrar por "Attribution not required" (mesma fonte).
- Faixas marcadas **CC (Creative Commons)**: crédito OBRIGATÓRIO na descrição do vídeo; a própria biblioteca gera o texto para copiar (coluna "License type") (mesma fonte).
- Monetização permitida para quem está no YPP (mesma fonte).
- AVISO oficial: o YouTube só garante o que sai da PRÓPRIA biblioteca — "royalty-free" de outros canais/bibliotecas é risco do criador (mesma fonte).

### 1.2 Kevin MacLeod / incompetech (segunda escolha — clima sob medida)
- ~2.000 faixas categorizadas por "feel" (calming, triumphant, frantic...), todas CC BY 4.0 (fonte: https://vidiq.com/blog/post/royalty-free-music-youtube-audio-library/ e https://incompetech.com/music/royalty-free/faq.html).
- Texto EXATO do crédito (obrigatório, na descrição ou no próprio vídeo):
  `"[Título]" Kevin MacLeod (incompetech.com) — Licensed under Creative Commons: By Attribution 4.0 — https://creativecommons.org/licenses/by/4.0/`
  (fonte: https://incompetech.com/music/royalty-free/faq.html)
- Monetização: permitida com crédito — o FAQ diz literalmente que pode monetizar, desde que credite (mesma fonte).
- Regra do crédito: colocado de forma que quem quiser saber de onde veio a música ache SEM dificuldade (mesma fonte). Nossa prática de crédito automático na descrição já cumpre isso.
- Já aprovada na casa: "Inspired" (ver MIX-POR-MEDICAO.md).

### 1.3 Pixabay Music (terceira opção)
- Pixabay License: uso comercial e não-comercial, pode copiar/modificar, **sem atribuição exigida** (fontes de levantamento 2026: https://swarmify.com/blog/free-music-for-your-videos-the-importance-and-where-to-find/ e https://www.videoweaver.app/en/blog/post/free-music-copyright-guide/ — honestidade: li os levantamentos, não a página de termos do Pixabay; confirmar os termos na fonte primária antes da primeira faixa de lá).
- **Leitura minha:** usar Pixabay só quando as duas primeiras não tiverem o clima; qualquer faixa de fora da Audio Library pode gerar disputa manual mesmo sendo legal — guardar no manifesto o link da faixa + print da licença no dia do download.

### Ordem de preferência (leitura minha)
1. Audio Library "Attribution not required" → zero fricção, zero Content ID.
2. Audio Library CC → crédito gerado pela própria biblioteca.
3. incompetech → quando precisamos de "feel" específico; crédito automático.
4. Pixabay → exceção documentada.

## 2. Emoção da trilha por seção do vídeo

### Princípios (com fonte)
- **Cada capítulo/virada emocional merece faixa nova ou variação** — cue de energia na abertura, instrumental calmo na explicação, algo novo e ascendente na revelação/conclusão (fonte: https://soundraw.io/blog/post/how-to-use-music-to-improve-viewer-engagement-and-retention-on-youtube).
- **O tempo (BPM) da música casa com o ritmo do corte**: edição rápida = tempo rápido; trecho contemplativo = trilha contida (mesma fonte).
- **Música marca os momentos-chave** (revelação, virada, frase de impacto) — eleva o impacto emocional e segura o espectador (mesma fonte).
- Ciência da tensão: tensão musical nasce da EXPECTATIVA de que algo vai acontecer e se resolve em emoção positiva ou negativa conforme o desfecho — estudo com medidas subjetivas e fisiológicas (fonte: https://www.nature.com/articles/s41599-022-01461-5).
- Retenção pós-minuto 8 depende de variar estímulos — trilha é um dos estímulos que renova a atenção (fonte: https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8).

### Mapa aplicado AO NOSSO VÍDEO motivacional (leitura minha, apoiada nas fontes acima)
| Seção | Emoção-alvo | Trilha | "Feel" p/ busca (incompetech/Audio Library) |
|---|---|---|---|
| Gancho (0:00–0:30) | curiosidade + peso | entrada com identidade, motivo curto, sem clímax | mysterious, contemplative |
| Ensinamento (corpo) | calma confiante | piano/ambient contido, quase invisível | calming, meditative |
| História/virada | tensão crescendo | build sutil (camadas entram devagar) | building, suspense |
| Clímax motivacional | elevação | uplift, entrada de cordas/camada nova | inspiring, triumphant, uplifting |
| Fechamento + CTA | resolução serena | volta ao motivo do gancho, mais quente; shift sutil na hora do CTA | hopeful, calm |
- **Anti-fadiga:** NUNCA uma única faixa em loop por 20–30 min; alternar variação/faixa a cada capítulo (soundraw, acima). Faixa curta em loop dentro de UMA seção continua ok com nossa técnica `-stream_loop + atrim + afade` (MIX-POR-MEDICAO.md).
- **Coerência de marca (leitura minha):** paleta sonora fixa do canal = piano, ambient e cordas leves — combina com o P&B cromado; evitar percussão eletrônica pesada e qualquer coisa "drone/zumbido" (bronca fundadora do Diretor).
- **Transições:** trocar de faixa SEMPRE num respiro da narração ou corte de cena, com crossfade (`acrossfade` ~2 s); troca no meio de frase denuncia edição (leitura minha).

## 3. Checklist de escolha de trilha (antes de mixar)

1. A seção pede qual emoção? (tabela acima)
2. BPM casa com o ritmo do corte daquele trecho?
3. A faixa tem espaço (sem melodia gritante na frequência da voz)?
4. Licença: fonte, tipo, crédito exigido? → anotar no mix_manifesto.json: `trilhas: [{titulo, autor, fonte, licenca, credito_texto, url}]`
5. Crédito CC BY montado e pronto para a descrição (Roteirista/Uploader recebe junto com o mix)?

## Como aplicar no próximo vídeo

1. Montar o vídeo com **no mínimo 3 momentos musicais distintos** (gancho / corpo / clímax+fechamento) em vez de 1 faixa única — usar a tabela da seção 2.
2. Buscar 2 candidatas por seção na Audio Library (filtro "Attribution not required") e 1 no incompetech pelo "feel"; guardar as aprovadas na pasta de trilhas da BIBLIOTECA.
3. Fazer as trocas de faixa só em respiros da narração, com `acrossfade` de ~2 s, e medir cada trecho (a lei dos 18–20 dB vale por seção, não só na média).
4. Adicionar ao mix_manifesto.json o bloco `trilhas` com licença e texto de crédito de CADA faixa usada.
5. Entregar junto do mix o texto de créditos pronto para a descrição (obrigatório se houver faixa CC BY).
6. Confirmar os termos da Pixabay License na fonte primária antes de usar a primeira faixa de lá (pendência de honestidade da seção 1.3).
