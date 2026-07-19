# Ferramentas de Caça a Virais + a Regra do Conteúdo IA (varredura 17/07/2026)

> **Pesquisador · O Poder da Mente Sábia** · Duas frentes num guia só porque se cruzam: COMO achar o que estoura (ferramentas de outlier) e COMO não morrer monetizando com IA (política de conteúdo inautêntico 2026).
> **Honestidade:** preços e features vêm dos sites/blogs das próprias ferramentas e de comparativos — todo comparativo de ferramenta tem viés comercial (aviso onde houver). Números de enforcement vêm de imprensa/blogs de mercado, não de comunicado oficial do YouTube. Opinião minha marcada como **"leitura minha"**.

---

## 1. O mercado de ferramentas de outlier (o que existe e quanto custa)

"Outlier" = vídeo que performou MUITO acima da média do canal/nicho (5x, 10x, 25x). É a industrialização do que já fazemos na mão nas 6 buscas semanais.

| Ferramenta | Preço/ano | Força | Fraqueza |
|---|---|---|---|
| **vidIQ** | US$ 198,96 | tudo-em-um: SEO, volume de busca por palavra-chave, ideias diárias, score de competição | outlier é secundário |
| **TubeLab** | US$ 178,80 | outliers com filtros 5x/10x/25x, análise de padrões de título, saturação de nicho, API/n8n | comparativo abaixo é do blog DELES (viés) |
| **1of10** | US$ 348 (Basic US$29/mês anual; Pro US$69) | especialista em outliers + gerador de thumbnail/título IA | sem volume de busca, banco não divulgado, sem API |
| **ViewStats** | US$ 479,88 | co-fundado por MrBeast; A/B de título/thumb, rastreio de concorrentes | caro; nota de usuários baixa (2,5/5 no comparativo do vidIQ) |
| **NexLev** | ~US$ 540 | focado em faceless + curso/Discord | o mais caro |

Fontes: [TubeLab — 5 alternatives to 1of10](https://tubelab.net/blog/5-alternatives-to-1of10) (⚠️ blog do próprio TubeLab), [1of10 — 1of10 vs vidIQ](https://1of10.com/blog/1of10-vs-vidiq/) (⚠️ blog do próprio 1of10), [vidIQ vs ViewStats](https://vidiq.com/compare/vidiq-vs-viewstats/) e [vidIQ vs 1of10](https://vidiq.com/compare/vidiq-vs-1of10/) (⚠️ blog do próprio vidIQ), [OutlierKit — 1of10 vs vidIQ](https://outlierkit.com/blog/1of10-vs-vidiq).

**Leitura minha (regra da casa = modo econômico, custo zero até a receita entrar):**
- **NÃO assinar nada agora.** Nosso método manual já replica 80% do valor: buscas do território ordenadas por views + conta de outlier na mão (views do vídeo ÷ mediana de views do canal; ≥10x = outlier de verdade).
- O que as ferramentas têm que a mão não tem: alerta automático de viral recente e busca reversa em escala. Quando entrar verba, a 1ª candidata é **TubeLab (US$178,80/ano)** pela relação preço/filtros/API (encaixa na nossa automação via n8n/scripts) — mas validar fora do blog deles antes de pagar.
- O gerador de thumbnail IA do 1of10 não nos serve: nossa identidade P&B com letras 3D cromadas é regra do Diretor, não se terceiriza.

## 2. O workflow de outlier manual (custo zero) — padrão do Pesquisador

1. Rodar as 6 buscas do território (já na rotina de segunda) ordenadas por contagem de views, filtro "este ano" e "este mês".
2. Para cada candidato: abrir o canal → mediana de views dos últimos 10 vídeos → **multiplicador = views do vídeo ÷ mediana**. Registrar só ≥5x; destacar ≥10x.
3. Anotar no pesquisa_semana.json: título completo, duração, idade, multiplicador, quais das 4 peças do PARÂMETRO o título usa, e padrão visual da thumb (% escuro, contraste — manter o gabarito).
4. Cruzar recência: outlier com <3 meses vale mais que o de 1 ano (território pagando AGORA).
5. Conceito com 2+ outliers em canais DIFERENTES = conceito comprovado → vira pauta prioritária (nossa prova interna: "aja como se nada te afetasse" estourou em 2 canais, 5,1M + 2M).

## 3. Benchmarks do nosso nicho (motivacional/desenvolvimento pessoal)

- RPM do nicho motivacional: **US$ 5–9 por mil views monetizadas** ([OutlierKit — Most Profitable Niches](https://outlierkit.com/blog/most-profitable-youtube-niches)); outra fonte crava ~**US$ 5,70** ([TubeAnalytics — RPM by niche](https://www.tubeanalytics.net/blog/youtube-rpm-benchmarks-by-niche)). Para comparação: finança US$10–15, true crime US$8–12, animação US$9–13.
- **Leitura minha:** RPM médio não é teto — nosso público (prosperidade/alta performance) atrai anunciante de curso/coaching, faixa **US$ 9–12 de CPM** segundo [Stripo Research](https://research.stripo.email/youtube-benchmarks). Vídeo LONGO com retenção alta permite mid-rolls, que multiplicam o RPM efetivo — mais um motivo para os 15–40min bem sustentados.
- Métricas médias do YouTube para nos situarmos: retenção média geral 23,7%, pico de retenção 31,5% em vídeos de 5–10min ([Stripo Research](https://research.stripo.email/youtube-benchmarks)). Nosso alvo de 50–60% de AVD (ver guia ALGORITMO-2026) está MUITO acima da média — é assim que canal pequeno fura a bolha.

## 4. ⚠️ A REGRA DA SOBREVIVÊNCIA — conteúdo inautêntico e IA em 2026

Nós somos um canal 100% IA porém humanizado. Esta é a linha entre nós e o "AI slop" que o YouTube está EXPURGANDO:

**O enforcement é real e recente:**
- Jul/2025: política "conteúdo repetitivo" renomeada para **"conteúdo inautêntico"** — mira produção em massa com template e pouca variação ([ScaleLab](https://scalelab.com/en/why-youtube-is-cracking-down-on-ai-generated-content-in-2026), [YTStudioDesktop](https://ytstudiodesktop.com/blog/youtube-inauthentic-content-policy-demonetization)).
- Jan/2026: **16 canais grandes removidos do YPP — 4,7 bilhões de views e ~US$10M/ano** — todos faceless com voz sintética, roteiro template e volume industrial ([ScaleLab](https://scalelab.com/en/why-youtube-is-cracking-down-on-ai-generated-content-in-2026), [MilX](https://milx.app/en/news/why-youtube-just-suspended-thousands-of-ai-channels-and-how-to-protect-yours)).
- Jul/2026: imprensa reporta remoção de ~35M de inscritos "fantasmas" ligados a canais de AI slop ([TechTimes](https://www.techtimes.com/articles/320629/20260715/youtube-wiped-35m-subscribers-over-ai-slop-now-its-judging-your-taste.htm) — número de imprensa, não conferido em fonte oficial).
- A avaliação agora é do **CANAL INTEIRO**, não vídeo a vídeo ([ScaleLab](https://scalelab.com/en/why-youtube-is-cracking-down-on-ai-generated-content-in-2026)).

**O que marca um canal para queda** (padrões citados pelo [ScaleLab](https://scalelab.com/en/why-youtube-is-cracking-down-on-ai-generated-content-in-2026) e [Flocker](https://flocker.tv/posts/youtube-inauthentic-content-ai-enforcement/)):
- volume industrial (ex.: 10+ uploads/dia) sem variação;
- vídeos clones (só muda título/nome);
- slideshow de imagens IA paradas sem edição real;
- narração sintética + roteiro template sem ponto de vista próprio.

**O que mantém monetização** ([EarnFacts](https://earnfacts.com/demonetization-2026-ai-rules/), [Vexub](https://vexub.com/blog/ai-generated-video-monetization-policies), [ScaleLab](https://scalelab.com/en/why-youtube-is-cracking-down-on-ai-generated-content-in-2026)):
- **persona nomeada e consistente** com ponto de vista reconhecível no roteiro;
- **variação de formato** entre vídeos;
- **visual com edição real / b-roll de verdade** (nossa regra nova do Diretor — b-roll real de pessoas casando com a fala — é EXATAMENTE o antídoto contra o carimbo de slideshow IA);
- **divulgação de IA quando realista/sintético**: o descumprimento tem escalada de 3 strikes (aviso → 90 dias sem monetização → remoção do YPP), e a divulgação NÃO derruba ranking — RPM de conteúdo IA divulgado é comparável ao não-IA no mesmo nicho ([Vexub](https://vexub.com/blog/ai-generated-video-monetization-policies), [EarnFacts](https://earnfacts.com/demonetization-2026-ai-rules/) — blogs de mercado; a regra oficial de disclosure existe desde 2024, os efeitos numéricos são estimativa deles).

**Leitura minha — nosso posicionamento:** estamos do lado certo POR PROJETO (roteiro original anti-cópia, b-roll real, identidade visual própria, 2–3 vídeos/semana e não 12/dia, valor real = satisfação). O risco residual é a VOZ sintética + cadência regular parecer template para o classificador. Mitigação: variar estrutura de abertura entre vídeos, manter a persona do canal explícita na narração ("aqui no Poder da Mente Sábia..."), preencher o disclosure de conteúdo alterado/sintético no Studio quando aplicável, e nunca publicar dois vídeos com o MESMO esqueleto de roteiro em sequência.

## Como aplicar no próximo vídeo

1. **Calcular o multiplicador do conceito antes de aprovar a pauta**: só produzir conceito com outlier ≥5x confirmado no território (≥10x = prioridade), registrado no pesquisa_semana.json com título/duração/idade/multiplicador.
2. **Checklist anti-slop no crivo final**: persona nomeada presente na narração? estrutura de abertura diferente do vídeo anterior? b-roll real casando com a fala (não slideshow)? Se falhar 1, volta para a fábrica.
3. **Disclosure**: marcar no YouTube Studio a declaração de conteúdo sintético/alterado quando a peça tiver voz/imagem gerada realista — proteção de 3 strikes, sem custo de alcance.
4. **Planejar mid-rolls**: no roteiro de 15–40min, marcar 2–3 pontos naturais de pausa (transição de bloco) para mid-roll — é onde o RPM US$5–9 do nicho vira mais receita sem ferir retenção.
5. **Não assinar ferramenta paga agora**: manter caça manual de outliers (workflow da seção 2); reavaliar TubeLab/1of10 só quando o canal gerar receita.
