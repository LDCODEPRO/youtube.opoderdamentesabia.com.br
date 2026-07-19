# Mandato de pesquisa — Sintetizador

## Varredura ciclo 2 — 2026-07-17
**O que estudei:** a camada AVANÇADA de métricas — como montar um SCORE ÚNICO de retenção-no-papel a partir das peças objetivas (ILF, PPM, densidade de payoff, RPE, burstiness) e como CALIBRAR esse score contra a retenção real do YouTube Studio. Resultado: 2 guias novos (SCORE-AUTOMATICO-DE-RETENCAO-NO-PAPEL.md e CALIBRACAO-DO-SCORE-COM-RETENCAO-REAL.md), fechando a referência que o guia METRICAS-OBJETIVAS (deste mesmo ciclo) deixou pendente.

**Aprendizados-chave:**
- Existe molde científico pra score: média ponderada normalizada `S = 10·Σ(w·s)/Σw`, com POUCOS fatores (top-5), e o teto realista de um bom score é Spearman ρ ≈ 0,71 com engajamento real (arXiv:2512.21402) — nenhum score de papel acerta 100%, a meta é ORDENAR bem.
- Poucos fatores > muitos: concentrar peso nas 7 dimensões que movem a agulha; Muro do 1º minuto é a única com poder de VETO (55%+ some antes de 60s).
- Humanidade tem número: burstiness = desvio-padrão do tamanho das frases; <4 = "cara de robô" (fonte vendor, direcional) — vira a defesa objetiva contra os 70% de penalidade de conteúdo "IA".
- YouTube define oficialmente Intro (30s), Top moments, Spikes (reassistido/compartilhado), Dips; relatório só com ≥60s e ≥100 views, 1–2 dias pra processar — meu instrumento de calibração.
- Calibração = Spearman entre S_bloco previsto e retenção real por bloco (alinhados por PPM); meta humilde ρ ≥ 0,5; NÃO mexer em peso com <~15 pares ou p>0,05 (amostra pequena engana — usar permutação).
- A cadência de 3/semana (~12 vídeos/mês, ~50–70 pares bloco-retenção) dá amostra pra 1º ciclo sério de calibração em ~3–4 semanas.
- Regra anti-deriva: entre calibrações os pesos ficam CONGELADOS; mexer a cada vídeo é perseguir ruído.

**Fontes:** https://arxiv.org/html/2512.21402 · https://arxiv.org/pdf/2508.02516 · https://support.google.com/youtube/answer/9314415 · https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report · https://www.write-humanly.com/blog/burstiness-perplexity-deep-dive · https://www.sketchengine.eu/glossary/type-token-ratio-ttr/ · https://arxiv.org/abs/2201.03445 · https://statisticsbyjim.com/basics/spearmans-correlation/ · https://www.tandfonline.com/doi/full/10.1080/03610926.2022.2121144

**Próximo estudo:** rodar a 1ª calibração real com os primeiros vídeos publicados (Intro% + curva vs meu S_bloco) e reportar o ρ ao Gerente; e punch-up de PT-BR falado (ritmo/contração/oralidade) para elevar burstiness sem soar forçado.

## Varredura 2026-07-17
**O que estudei:** rubricas de avaliação de roteiro (script coverage de Hollywood + ciência de "LLM como juiz"), como prever retenção lendo o roteiro (benchmarks 2025 com 10k+ vídeos), e técnicas de fusão de múltiplas versões (paper LLM-Blender + processo real de writers' rooms de TV). Resultado: 2 guias novos na BIBLIOTECA (JULGAMENTO-CEGO-E-RETENCAO-NO-PAPEL.md e PROTOCOLO-DE-FUSAO-DAS-3-VERSOES.md).

**Aprendizados-chave:**
- Fusão VENCE escolha: fundir os melhores candidatos num texto NOVO supera escolher o melhor roteiro inteiro (LLM-Blender, ACL 2023) — meu mandato de "montar, não escolher" tem prova científica.
- Julgar às cegas e em dupla ordem (A-vs-B e B-vs-A) é obrigatório: vieses de posição, verbosidade e autopreferência atacam todo juiz LLM não tratado.
- Critério binário (SIM/NÃO por pergunta) é mais confiável que nota 0–10 "no olho" — minha rubrica precisa dessa conversão.
- Muro do 1º Minuto: 55%+ dos espectadores somem antes de 60s; janela de decisão de 8s; valor claro nos primeiros 15s dá +18% de retenção no marco de 60s (Retention Rabbit, 10k vídeos).
- Vídeos >10min têm êxodo secundário em 55–65% do vídeo → re-hook escrito no marco 40–60% do roteiro.
- Conteúdo percebido como IA: 70% menos retenção; narração IA perde 35% nos primeiros 45s — para nosso canal 100% IA, humanizar é sobrevivência, não estética.
- Writers' rooms fundem versões por "alts" pontuais (5–10 alternativas por ponto, entra 1) com UM árbitro final — nunca versão-inteira contra versão-inteira.
- O famoso "+32% de watch time com open loops" NÃO se confirma na fonte (ela mesma diz que os números variam) — nunca citar como fato.

**Fontes:** https://arxiv.org/abs/2306.02561 · https://arxiv.org/pdf/2503.24235 · https://www.evidentlyai.com/llm-guide/llm-as-a-judge · https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report · https://learn.tubeai.app/blog/youtube-script-writing-retention · https://michaeljamin.substack.com/p/whats-the-rewrite-process-like-in · https://www.antonschettini.com/post/tv-writers-room-a-day-in-the-life · https://en.wikipedia.org/wiki/Script_coverage · https://youtubershub.com/blog/how-to-write-a-video-script-and-hook · https://www.premiumbeat.com/blog/art-of-movie-script-revision/

**Próximo estudo:** calibração do júri com dados reais — como cruzar minhas notas por bloco com a curva de retenção do YouTube Studio dos nossos primeiros vídeos publicados (juiz que não confere a realidade deriva); e punch-up de PT-BR falado: ritmo, contração e oralidade para narração que não soa IA.
SUA ESPECIALIDADE: script doctoring (consertar e elevar roteiros).
Pesquisar: técnicas de punch-up e reescrita; como writers' rooms reais juntam versões; padrões de roteiro dos vídeos que estouram no território.
## Como registrar o que aprender
Todo achado vira arquivo na sua BIBLIOTECA/ (um tema por arquivo, com fonte e data).
Achado que muda REGRA da produção → avisar o Gerente para atualizar a DOUTRINA e o painel.
Cadência: revisão da função TODA SEMANA junto da varredura de segunda-feira do Pesquisador.
