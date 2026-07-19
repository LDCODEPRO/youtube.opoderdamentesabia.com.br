# Checklist de upload completo + horário e frequência para canal pequeno
> Publicador · pesquisado em 2026-07-17 · estudos de 2025/2026 + páginas oficiais do YouTube

## 1. Horário: o que os grandes estudos dizem (e por que divergem)
- Estudo Buffer (1,8 milhão de vídeos): vídeo LONGO performa melhor de MANHÃ (8–11h), melhores dias domingo, terça e segunda; pico isolado domingo 10h. Shorts é o OPOSTO: noite (18–21h), sexta/sábado/quinta (fonte: https://buffer.com/resources/best-time-to-post-on-youtube/).
- Estudos agregadores de 2026 (SocialPilot ~301 mil vídeos; RecurPost 2M+) apontam quarta/quinta entre 12h e 16h como janela consistente (fontes: https://www.socialpilot.co/insights/best-time-to-post-on-youtube e https://recurpost.com/blog/best-time-to-post-on-youtube/).
- Conclusão honesta: os estudos NÃO concordam entre si — cada base mede público diferente. Leitura minha: para canal pequeno e novo, benchmark externo serve só de chute inicial; a única fonte que vale é o heatmap do PRÓPRIO canal.
- Ferramenta oficial: YouTube Studio → Analytics → Público → "Quando seus espectadores estão no YouTube" — heatmap dos últimos 28 dias, no fuso local do canal (fonte: https://buffer.com/resources/best-time-to-post-on-youtube/). Regra prática dos estudos: publicar 1–2 horas ANTES do pico do próprio público, para o vídeo já estar processado (HD/legendas) quando a audiência chegar.
- Canal pequeno vive de busca + browse (não de feed de inscritos), então o horário pesa menos que para canal grande — mas um bom primeiro dia ajuda o algoritmo a ganhar confiança no vídeo (leitura minha, apoiada no raciocínio de https://vidseeds.ai/blog/best-time-to-post-youtube/).
- Nosso caso: público motivacional PT-BR; a doutrina da casa é 19h Brasília ±jitter. Isso bate com "noite = consumo de vídeo no Brasil" mas CONTRADIZ o achado do Buffer (manhã para longo). Leitura minha: manter 19h até termos ~8 semanas de dados, depois testar 1 vídeo/semana de manhã (9–11h) por 4 semanas e comparar views nas primeiras 24h — decisão pelos dados, na revisão de segunda.

## 2. Frequência: o que os experimentos mostram
- Experimentos documentados (Social Video Plaza): upload DIÁRIO por 2 semanas rendeu ~25% mais views por 7x o trabalho ("muito ineficiente"); 3/semana por 4 semanas "importou tão pouco que não foi incentivo"; o que move crescimento é o MOMENTUM do vídeo anterior, não a quantidade (fonte: https://www.socialvideoplaza.com/en/articles/youtube-upload-schedule).
- Consenso das fontes PT-BR para canal pequeno: 1 a 2 vídeos/semana consistentes valem mais que rajadas; consistência > quantidade (fonte: https://ricoproducoes.com.br/quantos-videos-devo-postar-no-youtube/).
- Cruzamento com a meta do YPP: 4.000 horas em 12 meses = ~77h de exibição/semana. Com vídeos de 15 min e retenção de 40% (6 min assistidos), são ~770 views/semana somando o catálogo (conta minha, aritmética simples — não é estatística externa). Ou seja: catálogo que continua sendo assistido vale mais que frequência alta — cada vídeo precisa ter vida longa (busca/browse), não só estreia.
- Nossa cadência 3/semana (seg-qua-sex) é sustentável porque a produção é IA; o risco não é burnout, é REPETIÇÃO (ver guia CONFORMIDADE-IA-E-MONETIZACAO-2025.md). Se a qualidade cair para cumprir cadência, cortar para 2/semana sem dó (leitura minha).

## 3. Checklist de upload COMPLETO (ordem de preenchimento no Studio)
Fontes gerais do bloco: https://www.overseeros.com/blog/youtube-metadata-checklist e https://influenceflow.io/resources/youtube-metadata-and-descriptions-the-complete-2026-creators-guide-to-video-discoverability/ ; regras de capítulo e tag são oficiais do YouTube.

**Antes de abrir o Studio (pré-condições da casa):**
- [ ] pode_publicar() == True (crivo 100% do Pesquisador + carimbo do Diretor) — sem isso, NADA acontece.
- [ ] Arquivo final conferido: áudio com música ≥18 dB abaixo da voz (padrão da casa), sem clip, thumb P&B 3D cromada pronta em 1280x720.
- [ ] Licença da música registrada no pipeline.

**Metadados:**
- [ ] TÍTULO: até ~60 caracteres (acima disso trunca na busca/celular), palavra-chave principal no começo, promessa concreta (fonte: https://www.overseeros.com/blog/youtube-metadata-checklist).
- [ ] DESCRIÇÃO: 200–300 palavras; as 1–2 primeiras linhas são o que aparece antes do "mostrar mais" — gancho + palavra-chave ali (fonte: https://influenceflow.io/resources/youtube-metadata-and-descriptions-the-complete-2026-creators-guide-to-video-discoverability/).
- [ ] CAPÍTULOS na descrição: primeiro timestamp em 00:00, mínimo 3 timestamps, cada capítulo com ≥10 segundos — regra oficial para capítulos funcionarem (fonte: https://support.google.com/youtube/answer/9884579).
- [ ] TAGS: 10–15, misto de amplas e específicas; papel HOJE é pequeno — servem principalmente para erros de grafia comuns (fonte oficial: https://support.google.com/youtube/answer/146402). Não gastar mais que 5 min nisso.
- [ ] HASHTAGS: até 3 relevantes (as 3 primeiras aparecem acima do título); exagerar (>60) faz o YouTube ignorar todas (fonte: https://support.google.com/youtube/answer/6390658).
- [ ] Idioma do vídeo = Português (Brasil); legendas PT-BR revisadas (auto-caption tem precisão bem menor que legenda revisada — fonte: https://influenceflow.io/resources/youtube-metadata-and-descriptions-the-complete-2026-creators-guide-to-video-discoverability/).

**Conformidade (o nosso portão):**
- [ ] Caixa "Conteúdo alterado ou sintético": marcar se houver cena realista gerada por IA (fonte: https://support.google.com/youtube/answer/14328491). Registrar a decisão no pipeline.
- [ ] "Feito para crianças" = NÃO (nosso conteúdo é motivacional adulto).
- [ ] Playlist correta do canal selecionada.

**Elementos finais:**
- [ ] TELA FINAL: últimos 5–20s com 1 vídeo recomendado + botão de inscrição (não deixar o Studio em branco).
- [ ] CARDS: 1–2 cards apontando para vídeo relacionado do catálogo (ajuda a sessão continuar no canal).
- [ ] Thumb carregada e conferida em tamanho pequeno (legível no celular).
- [ ] AGENDAR para o horário da doutrina (19h ±jitter, nunca em rajada com outro vídeo).

**Pós-publicação (até 10 min depois):**
- [ ] Abrir o permalink como espectador deslogado: thumb certa, capítulos funcionando, legenda presente, selo IA visível se marcado.
- [ ] Registrar permalink no pipeline (status: publicado).
- [ ] Fixar 1 comentário com pergunta que puxa resposta (engajamento no primeiro dia; leitura minha — prática comum, sem estudo forte que eu tenha verificado).

## Como aplicar no próximo vídeo
1. Rodar o checklist acima item por item no upload — imprimir/seguir a ordem, sem pular a caixa de conteúdo sintético.
2. Escrever as 2 primeiras linhas da descrição ANTES do resto (gancho + palavra-chave), e só depois o corpo e os capítulos.
3. Colocar capítulos com 00:00 + mínimo 3 marcas, seguindo a regra oficial, com títulos de capítulo que usam as palavras do tema.
4. Agendar às 19h ±jitter e anotar no pipeline as views/impressões das primeiras 24h — é a série histórica que vai alimentar o teste de horário.
5. Quando o canal tiver 28 dias de dados, tirar print do heatmap "Quando seus espectadores estão no YouTube" e levar para a revisão de segunda: manter 19h ou iniciar o teste de manhã.
6. Adicionar tela final + 1 card apontando para o vídeo mais forte do catálogo (o de melhor retenção, não o mais recente).
