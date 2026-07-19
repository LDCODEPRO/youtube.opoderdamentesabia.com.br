# Mandato de pesquisa — Elaborador Visual

## Varredura ciclo 2 — 2026-07-17
**O que estudei:** temas avançados de b-roll — bancos de vídeo GRATUITOS além do Mixkit
(Pexels, Pixabay, Videvo, Coverr) com licença comercial e como baixar; e como VARIAR 3
vídeos/semana sem repetir clipes (biblioteca tagueada, rotação, disfarce, coleta em lote).
Composição/continuidade (regra dos terços, direção do olhar, match cut) já ficou pronta em
`COMPOSICAO-E-CONTINUIDADE-DO-B-ROLL.md` — não repeti. 6 buscas + 5 fontes lidas a fundo.
**Resultado:** 2 guias novos — `BANCOS-DE-VIDEO-GRATUITOS-LICENCAS-E-DOWNLOAD.md` e
`VARIAR-TRES-VIDEOS-POR-SEMANA-SEM-REPETIR.md`.

**Aprendizados-chave:**
- Licença cobre o CLIPE, não o conteúdo: marca/logo/rosto reconhecível têm direitos próprios; nenhum banco garante model release.
- Pexels e Pixabay: grátis, comercial, SEM atribuição — nossos padrões (fontes oficiais).
- MUDANÇA DE DOUTRINA: Coverr EXIGE crédito no download grátis (creditar Coverr.co ou o autor); só Coverr+ isenta → precisa entrar na descrição do YouTube. Avisar o Gerente.
- Videvo é armadilha: licença muda por clipe (Royalty Free vs Attribution vs Premium) e o site virou parte do Freepik em 2026 → só usar clipe "Royalty Free", na dúvida pular.
- Um criador semanal junta 500–1000 clipes/ano; nós 3× mais rápido → variação se resolve no SISTEMA (biblioteca+rotação), não na edição.
- Sistema de biblioteca: pastas por emoção com prefixo numérico, nome-padrão AAAA-MM-DD/fonte, 5 tags por clipe (15 s/clipe) + tag `ultimo_uso` que alimenta a janela de rotação.
- Disfarce de reuso (punch-in, trecho diferente, velocidade, hflip, grading) é plano B: máx. 1–2 por vídeo; símbolo de marca PODE repetir, b-roll de pessoas não.

**Fontes:**
- https://www.pexels.com/license/
- https://pixabay.com/service/license-summary/
- https://coverr.co/license
- https://www.licenseorg.com/guide/video/videvo
- https://mixkit.co/license/
- https://videoassetmanager.com/organize-b-roll-footage/
- https://www.podcastvideos.com/how-to-organize-b-roll-asset-libraries-for-rapid-video-editing-workflows/
- https://beverlyboy.com/film-technology/dont-be-that-editor-stock-footage-mistakes-that-kill-your-video/

**Próximo estudo:** implementar de fato a árvore `B-ROLL_MENTE_SABIA/` + esquema de tags no
pipeline (onde guardar `ultimo_uso` — manifesto ou sidecar); e testar image-to-video (Sora/Kling)
para dar movimento de câmera dirigido aos clipes de banco estáticos.

---

## Varredura 2026-07-17
**O que estudei:** direção visual de vídeo motivacional longo — b-roll que casa com a narração
(regra nova do Diretor), gramática visual (quando cortar, duração por plano), grading P&B
cinematográfico e prompts de imagem IA para cenas. 6 buscas + 7 fontes lidas a fundo.
**Resultado:** 2 guias novos na BIBLIOTECA/ — `B-ROLL-QUE-CASA-COM-A-NARRACAO.md` e
`GRADING-PB-E-PROMPTS-DE-CENA-IA.md`.

**Aprendizados-chave:**
- Eixo vertical de edição: marcar picos emocionais na narração e ancorar cada plano na palavra evocativa — sincronia palavra→imagem, não decoração.
- Em vídeo longo, clareza > densidade de cortes: quem super-edita "esgota o espectador antes de esgotar o assunto"; b-roll mudo (sem voz nem texto) é risco de retenção.
- Números de duração: b-roll 3–8 s/clipe; documentário 7–25 s (ASL ~15 s); trocar enquadramento antes de 7–10 s parado.
- Todo corte nosso já é L-cut (voz contínua); o ganho novo é o J-cut nas transições de bloco (voz nova entra antes da imagem nova).
- Grading P&B: ajustar canais RGB ANTES de dessaturar, esmagar pretos antes de levantar, LUT antes da dessaturação — só dessaturar é o erro nº 1 ("flat e video-ish").
- Prompt cinematográfico: fórmula plano+ângulo → sujeito → luz → lente+film stock; para nosso P&B o stock é Kodak Tri-X 400 + chiaroscuro; <60 palavras; lista de negativos anti-plástico.
- Canais estoicos virais casam o b-roll com o tom emocional da frase (montanha/tempestade/ruína conforme a citação) — confirma a regra nova do Diretor.

**Fontes:**
- https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8
- https://www.podcastvideos.com/articles/editing-b-roll-frameworks-video-storytelling/
- https://tinymedialab.com/2025/10/578/
- https://vidpros.com/video-clip-length/
- https://www.epidemicsound.com/blog/j-cuts-and-l-cuts/
- https://noamkroll.com/how-to-color-grade-a-perfectly-cinematic-black-and-white-look/
- https://promptsera.com/midjourney-prompts-cinematic-realism/
- https://fluxnote.io/guides/stoicism-youtube-shorts-ideas-2026

**Próximo estudo:** image-to-video (Sora/Kling/Runway 2026) para transformar o b-roll real
gerado em microvídeo com movimento de câmera dirigido; e bancos de b-roll REAL de licença
limpa (Pexels/Mixkit/Pixabay) — curadoria por emoção para não depender só de geração.

SUA ESPECIALIDADE: geração visual por IA.
Pesquisar: Sora e image-to-video (novidades, prompts que funcionam), estilos de b-roll simbólico nos virais, motions/overlays novos de licença limpa para a biblioteca.
## Como registrar o que aprender
Todo achado vira arquivo na sua BIBLIOTECA/ (um tema por arquivo, com fonte e data).
Achado que muda REGRA da produção → avisar o Gerente para atualizar a DOUTRINA e o painel.
Cadência: revisão da função TODA SEMANA junto da varredura de segunda-feira do Pesquisador.
