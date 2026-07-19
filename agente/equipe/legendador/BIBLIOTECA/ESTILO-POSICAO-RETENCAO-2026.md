# Estilo, posição e tamanho de legenda que aumentam retenção (estado da arte 2026)

> Varredura de 2026-07-17. Todo número tem fonte ao lado. O que é interpretação está marcado como "leitura minha".
> Contexto do canal: vídeos LONGOS (5–30 min), 16:9, estética P&B, narração PT-BR, meta = retenção para monetizar.

## 1. Por que legenda queimada importa (os números)

- 85%+ dos vídeos em redes sociais são assistidos SEM SOM; ~50% dos espectadores dependem de legenda (https://www.kapwing.com/resources/subtitle-statistics/ e https://www.manchesterdigital.com/post/title-productions/mute-is-the-new-norm-why-captions-win-in-2025-video).
- 69% assistem mudo em locais públicos; 25% mesmo sozinhos (https://www.kapwing.com/resources/subtitle-statistics/).
- Vídeo legendado: só 22% dos espectadores pulam, contra 39% sem legenda (https://www.captioncut.com/blog/video-captions-seo-engagement-2025/).
- Legendas aumentam o tempo médio de exibição em ~12% e a chance de assistir até o fim chega a 80% (https://www.captioncut.com/blog/video-captions-seo-engagement-2025/).
- Em Shorts, legenda queimada = 15–25% mais retenção (https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention) — dado de short-form, mas confirma a direção.
- Leitura minha: no nosso nicho motivacional, muita audiência ouve COM som (é quase áudio-livro). A legenda aqui não substitui o som — ela REFORÇA a palavra do Narrador e segura o olho na tela. Não é enfeite, é âncora de atenção.

## 2. Karaokê (palavra-a-palavra) vs bloco — a decisão para vídeo LONGO

O que as fontes dizem:
- Word-by-word vence em completion rate no short-form (<60s, TikTok/Reels/Shorts) (https://www.aividgenie.com/blog/caption-styles-that-boost-engagement).
- Para vídeo >90s no YouTube, a recomendação é bloco estático, com ênfase pontual palavra-a-palavra a cada 8–10s numa palavra-chave (recomendação do autor, não estudo controlado — https://emax.studio/blog/word-by-word-ai-captions-vs-static-subtitles).
- Mecanismo: bloco deixa o olho "descansar" depois de ler; karaokê nunca deixa o olho relaxar — fixação a cada 250–400ms contra 2–4s do bloco (análise técnica do autor, não estudo revisado — https://emax.studio/blog/word-by-word-ai-captions-vs-static-subtitles).
- Karaokê contínuo por 10–30 minutos cansa (leitura minha, coerente com o mecanismo acima: fadiga de fixação constante em vídeo longo).

**Regra do canal (leitura minha, a validar com o Gerente):**
1. Corpo do vídeo longo = BLOCO curto (1–2 linhas, ~5 palavras quando dinâmico — padrão já validado da casa).
2. ÊNFASE karaokê só em momentos-chave: o gancho dos primeiros 30s, a frase-tese de cada capítulo e a chamada final. Nunca o vídeo inteiro.
3. A palavra enfatizada = a MESMA palavra-chave que o Narrador acentua e que o b-roll ilustra (fala, imagem e legenda casadas no mesmo instante — regra do Diretor).

## 3. Posição: zona segura no player do YouTube (16:9)

- Manter ~120 px do rodapé (barra de progresso/controles), ~120 px do topo (título/canal) e ~150 px das laterais em 1080p (https://clickyapps.com/creator/thumbnails/guides/thumbnail-safe-text-areas e https://eks.tv/title-safe-still-matters/).
- O CC automático do YouTube também desenha no rodapé: legenda queimada no rodapé extremo = risco de sobreposição dupla (leitura minha; a UI cobre — já era regra da casa).
- Posição recomendada para o canal: baixo-central, mas ACIMA da faixa dos 120 px. Em force_style com PlayResX=1920,PlayResY=1080: `Alignment=2,MarginV=130` (leitura minha, derivada dos números acima; conferir visualmente no primeiro render).
- Se um vídeo tiver arte/letras 3D cromadas no terço inferior, subir a legenda para não brigar com a arte — legenda nunca disputa com o título 3D (leitura minha).

## 4. Tamanho de fonte (16:9, 1080p)

- Regra prática do mercado: fonte de legenda ≈ 3–5% da altura do vídeo; em 1080p, render de ~24–36 px, linha ocupando ~1/20 a 1/30 da altura (https://convertaudiototext.com/blog/subtitle-styling-best-practices e https://blitzcutai.com/blog/best-caption-placement-short-form-video).
- Faixa 2026 para 16:9 (1920×1080): 24–32 px de altura de fonte (https://convertaudiototext.com/blog/subtitle-styling-best-practices).
- Leitura minha para o canal: nosso público inclui gente 40+ vendo no celular; ficar no TOPO da faixa (32–40 px renderizados em 1080p) sem passar de 2 linhas. No force_style, fixar `PlayResX=1920,PlayResY=1080,FontSize=56` dá cap-height efetiva nessa faixa com Arial Bold — MEDIR no frame exportado e ajustar; o que vale é o pixel renderizado, não o número do estilo.
- Nunca deixar o tamanho variar entre vídeos: consistência é marca (leitura minha).

## 5. Se um dia fizermos Shorts (9:16) — referência rápida

- Zona segura ~888×1500 centrada em 1080×1920: ~120 px topo, ~300 px rodapé (nome do canal/descrição), ~96 px direita (botões) (https://kreatli.com/guides/youtube-shorts-safe-zone).
- Legenda no terço médio-baixo da zona segura (Y≈1200–1550 em 1920) e fonte 36–48 px (https://blitzcutai.com/blog/best-caption-placement-short-form-video e https://convertaudiototext.com/blog/subtitle-styling-best-practices).

## Como aplicar no próximo vídeo

1. Renderizar com `force_style` fixando `PlayResX=1920,PlayResY=1080,Alignment=2,MarginV=130` e conferir num frame exportado que a legenda fica fora dos 120 px do rodapé e não cobre arte 3D.
2. Medir a altura da letra renderizada num screenshot 1080p: alvo 32–40 px; ajustar FontSize até bater e ANOTAR o valor final em LEGENDA-DA-MARCA.md (via Gerente).
3. Manter o corpo do vídeo em blocos de ~5 palavras / 1–2 linhas; marcar no roteiro 3–5 momentos-chave (gancho, tese de capítulo, encerramento) e aplicar ênfase karaokê SÓ neles.
4. Garantir que a palavra enfatizada na legenda é a mesma que o Narrador acentua e que o visual mostra naquele instante — checar com o Editor antes da queima.
5. Propor ao Gerente o teste A/B mais simples possível: um vídeo com ênfase karaokê nos momentos-chave vs um sem, comparando retenção nos primeiros 30s no YouTube Studio.
