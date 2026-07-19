# Ler o Painel Inteiro — Além da Curva de Retenção (ciclo 2 — 17/07/2026)

> **Pesquisador · O Poder da Mente Sábia** · Companheiro do LER-CURVAS-DE-RETENCAO-NO-ANALYTICS.md (aquele lê SÓ o gráfico de retenção). Aqui está o resto do Studio: o **funil de Alcance** (impressões→CTR→views→watch time), a **aba Público** (novo/casual/regular, inscrito×não inscrito) e o relatório de **horários** para travar nossos 3 slots da semana. NÃO repete a leitura de curva.
> **Honestidade:** as definições marcadas "oficial" vêm do YouTube Ajuda; o resto são guias de analytics de mercado — números sempre com a fonte ao lado; interpretação minha marcada como **"leitura minha"**.

---

## 1. O painel tem 5 abas — cada pergunta mora numa aba

Um erro comum é olhar só "Visão geral" e a curva de retenção. As decisões moram espalhadas:

- **Visão geral** → o placar (views, watch time, inscritos) — bom para tendência, ruim para diagnóstico.
- **Conteúdo / Alcance (Reach)** → *por que o vídeo foi ou não descoberto* (impressões, CTR, fontes de tráfego).
- **Público (Audience)** → *quem assiste e quando* (novo/casual/regular, inscrito×não, horários).
- **Receita** → RPM/CPM/mid-rolls (números do nosso mercado estão no OUTLIERS-RECENTES-BROWSE-CLUSTERS-E-RPM-BR.md — não repito aqui).
- **Retenção** (dentro de Engajamento) → coberta no guia companheiro.

**Leitura minha:** o crivo do Pesquisador precisa ler Alcance + Público JUNTO com a curva. A curva diz *se seguraram*; o Alcance diz *se clicaram*; o Público diz *se voltam*. Julgar vídeo só pela curva é meio diagnóstico.

## 2. O funil de Alcance — impressões → CTR → views → watch time

O relatório-chave chama-se "Impressões e como elas levaram ao tempo de exibição" e mostra o funil inteiro numa tela ([Jeff Bullas — Impressions Funnel](https://www.jeffbullas.com/thread/what-is-the-impressions-funnel-in-youtube-analytics-and-how-do-i-improve-it/); [Improvado — YouTube Analytics Guide](https://improvado.io/blog/youtube-analytics-guide)).

**Definições oficiais** ([YouTube Ajuda — Impressões e tempo de exibição](https://support.google.com/youtube/answer/9314486)):
- **Impressão** = "quantas vezes suas miniaturas foram exibidas para espectadores no YouTube". Só conta se a miniatura ficar **mais de 1 segundo na tela com ao menos 50% visível** (oficial).
- **Taxa de cliques das impressões (CTR)** = "com que frequência os espectadores assistiram a um vídeo depois de ver uma miniatura".
- CTR = cliques ÷ impressões × 100.

**A tabela de diagnóstico do funil** (onde o funil "vaza" diz o que consertar):

| Sintoma | Onde vaza | Significado | Ação |
|---|---|---|---|
| **Muitas impressões + CTR baixo** | impressão→clique | embalagem fraca: a Home mostra, mas a capa/título não convence ([Jeff Bullas](https://www.jeffbullas.com/thread/what-is-the-impressions-funnel-in-youtube-analytics-and-how-do-i-improve-it/), [Subscribr — Reach Tab](https://subscribr.ai/p/youtube-analytics-reach-tab-explained)) | refazer capa/título; testar em miniatura pequena |
| **CTR bom + watch time baixo** | clique→retenção | o vídeo NÃO pagou a promessa da capa/título ([Jeff Bullas](https://www.jeffbullas.com/thread/what-is-the-impressions-funnel-in-youtube-analytics-and-how-do-i-improve-it/)) | consertar abertura (ver guia da curva) — nunca mexer na capa que já converte |
| **Poucas impressões** | antes do funil | o algoritmo ainda não achou o cluster / relevância fraca / hiato de upload | consistência + título de busca + ganho de informação (ver OUTLIERS) |

**Ordem de conserto (regra do funil):** **conserta o CTR PRIMEIRO**; só depois de o CTR estar forte é que faz sentido atacar o watch time ([Jeff Bullas](https://www.jeffbullas.com/thread/what-is-the-impressions-funnel-in-youtube-analytics-and-how-do-i-improve-it/)). **Leitura minha:** faz sentido — não adianta segurar melhor quem nem entrou. Mas atenção ao nosso caso: capa boa + retenção ruim é o pior cenário (queima impressão cara), então no crivo os dois andam juntos.

Régua de CTR para ler o número (já detalhada no ALGORITMO-2026, resumo): a maioria dos canais vive entre **2% e 10%**, e canais novos/pequenos às vezes veem CTR mais alto por público inicial mais qualificado ([Subscribr — Reach Tab](https://subscribr.ai/p/youtube-analytics-reach-tab-explained)). **Sempre ler o CTR por FONTE de tráfego** (Browse 2–5% já é bom) — não repito a tabela, está no ALGORITMO-2026.

## 3. As primeiras 24–48h — o protocolo de decisão por janela de tempo

O algoritmo distribui em fases; o que você faz em cada fase muda o resultado.

- **Janela de teste = 24–48h.** O YouTube mostra o vídeo a um pool inicial e, se CTR + retenção + satisfação forem fortes, expande para públicos maiores nos **7–14 dias** seguintes ([dataslayer — YouTube Algorithm 2026](https://www.dataslayer.ai/blog/youtube-algorithm-2025-how-to-get-your-videos-recommended); [EarnifyHub — Algorithm 2026](https://earnifyhub.com/creator-economy/youtube-algorithm-guide-2026)).
- **Pool inicial é pequeno para canal pequeno:** um canal novo pode receber só **100–500 impressões** nas primeiras horas; um de 100k inscritos, 10.000–50.000 ([EarnifyHub](https://earnifyhub.com/creator-economy/youtube-algorithm-guide-2026) — números de mercado). **Leitura minha:** como somos novos, CTR das primeiras horas oscila MUITO (base minúscula) — não tirar conclusão de embalagem antes de ~500–1.000 impressões acumuladas.
- **CTR decai com o tempo naturalmente** (inscritos veem primeiro): CTR caindo COM impressões subindo = o vídeo alcançou público frio = **sucesso**, não falha ([dataslayer](https://www.dataslayer.ai/blog/youtube-algorithm-2025-how-to-get-your-videos-recommended)).

**Protocolo do crivo por janela:**
1. **0–48h:** NÃO mexer em capa/título (a base é pequena demais e o algoritmo ainda está testando). Só observar.
2. **D+2 a D+7:** ler o funil com impressões já acumuladas. CTR <3% por fonte Browse com boas impressões = candidato a re-embalagem.
3. **D+7 a D+30:** se retenção dentro da faixa (ver guia da curva) mas CTR baixo → trocar capa/título (a alavanca do Tim Gabe: 40x views diárias só de capa, ver ALGORITMO-2026). Se CTR bom mas retenção baixa → lição para o roteiro do próximo, não conserto do vídeo velho.

## 4. Aba Público — quem assiste e se volta (o motor de longo prazo)

O YouTube trocou o antigo "recorrentes" por **três segmentos** ([YouTube Ajuda — Novos, casuais e regulares](https://support.google.com/youtube/answer/13615784); [fluxnote — Audience Analytics 2026](https://fluxnote.io/guides/youtube-audience-analytics-2026)):

- **Novos:** "espectadores que assistiram ao seu canal pela primeira vez no período selecionado" (oficial).
- **Casuais:** "assistem ao seu canal ocasionalmente" (oficial) — assistiram 1 a 5 meses no último ano.
- **Regulares:** "vêm assistindo ao seu canal de forma consistente por muito tempo. São seus membros mais fiéis" (oficial) — 6+ meses no último ano.

Por que importa para o ranqueamento: **inscritos assistem cerca de 2x mais vídeo que não inscritos**, e canal com forte base de regulares é favorecido pela recomendação ([YouTube Ajuda](https://support.google.com/youtube/answer/13615784)). O relatório **"Tempo de exibição de inscritos × não inscritos"** (aba Público) mostra a fatia de cada um ([improvado](https://improvado.io/blog/youtube-analytics-guide)).

**O que o YouTube recomenda oficialmente para virar novo→regular** ([YouTube Ajuda](https://support.google.com/youtube/answer/13615784)):
- produzir conteúdo **consistente em tema/formato**;
- desenvolver **séries** a partir de temas comprovados;
- responder comentários / engajar a comunidade.

**Leitura minha (o que a aba Público exige de nós):**
- Canal muito novo terá quase só "novos" — normal. O KPI de saúde de médio prazo é a fatia de **casuais** subindo mês a mês (prova de que a cadência 3/semana está criando hábito).
- A recomendação oficial de "séries a partir de temas comprovados" bate 100% com a estratégia de clusters (OUTLIERS) e de contribuição de sessão (ALGORITMO). É a MESMA alavanca vista de três ângulos: **fazer séries nomeadas com end screen para o próximo**.
- Meta de leitura mensal: fatia de watch time de inscritos subindo. Se 90% do watch time vem de não inscritos por meses, o conteúdo atrai mas não fideliza — revisar CTA de inscrição e coerência de tema.

## 5. O relatório de horários e os 3 slots da semana (dom 10h · qua 19h · sex 19h)

Ferramenta: **YouTube Studio → Público → "Quando seus espectadores estão no YouTube"** — um mapa de calor por dia/hora; blocos mais escuros = mais gente online ([tubeanalytics — Publish Timing](https://www.tubeanalytics.net/blog/analytics-optimize-video-publish-timing-peak-views)).

**Regra de publicação:** subir o vídeo **1 a 4 horas ANTES do pico** — o buffer dá tempo de o YouTube processar HD/4K, rodar checagem de monetização e gerar legendas, e o algoritmo usa a **primeira hora de resposta** para decidir a largura da distribuição ([tubeanalytics](https://www.tubeanalytics.net/blog/analytics-optimize-video-publish-timing-peak-views) diz 1–2h; [Digitalways — Best Time 2026](https://www.digitalways.org/best-time-to-upload-to-youtube-peak-publishing-hours-based-on-audience-behavior-in-2026/) diz 2–4h).

**Benchmarks de horário para o Brasil** (referência de partida, horário de Brasília — sempre validar no NOSSO mapa de calor):
- Janela geral forte: **14h–17h em dias úteis**; quarta ~16h aparece como pico ([Mundo da Música — Melhores dias/horários](https://mundodamusicamm.com.br/youtube-melhores-dias-horarios/)).
- Fim de semana: **9h–11h** (rotina relaxada de sáb/dom) ([Mundo da Música](https://mundodamusicamm.com.br/youtube-melhores-dias-horarios/)).
- Educação/profissional rende mais **de manhã em dia útil**; entretenimento/vlog rende **à tarde e à noite** ([Mundo da Música](https://mundodamusicamm.com.br/youtube-melhores-dias-horarios/)).

**Cruzando com nossos 3 slots — leitura minha:**
- **Domingo 10h** ✅ casa direto com a janela de fim de semana 9h–11h. Bom slot para o vídeo-âncora da semana (o de maior audiência).
- **Quarta 19h** e **Sexta 19h** ⚠️ o pico "geral" citado é 14h–17h, mas conteúdo motivacional/reflexivo se comporta mais como entretenimento noturno (público consome à noite, para "ouvir antes de dormir" — nosso próprio viral de 10M é "ouça dormindo"). Publicar 19h mira o consumo de fim de tarde/noite. **Validar com dados reais:** depois de ~8 vídeos, abrir o mapa de calor e o teste de slot (seção 6) para confirmar se 19h ou 17h rende mais.

## 6. Teste de slot com método (para a cadência 3/semana)

Não decidir horário no "achismo". Rodar teste estruturado ([tubeanalytics](https://www.tubeanalytics.net/blog/analytics-optimize-video-publish-timing-peak-views)):
- 30 dias, 2–3 slots candidatos, **ao menos 4 vídeos por slot**;
- medir por slot: **CTR de 24h, retenção (50%+ é forte sinal), watch time, conversão de inscritos**;
- comparar a MÉDIA dos vídeos do slot, nunca o vídeo campeão isolado;
- **regra de decisão:** vence o slot com resultado CONSISTENTE, não o que teve o único vídeo mais alto.
- Referência de "slot forte" na fonte: CTR 24h **6,5%–8,2%**, views 24h **1.100–1.450**, conversão de inscritos **0,6%–1,1%** ([tubeanalytics](https://www.tubeanalytics.net/blog/analytics-optimize-video-publish-timing-peak-views) — números do estudo deles, tratar como direção). **Leitura minha:** esses números são de canal já rodado; para nós, o valor é o MÉTODO (média por slot, consistência), não bater a marca de views deles nas primeiras semanas.

## Como aplicar no próximo vídeo

1. **Ritual de leitura do funil (D+7 de cada vídeo, ter/sex/seg conforme os 3 slots):** anotar no pesquisa_semana.json impressões, CTR por fonte, e classificar o vazamento (embalagem × promessa × alcance) pela tabela da seção 2 — a ação sai pronta da tabela.
2. **Trava anti-pânico 0–48h:** proibido trocar capa/título de vídeo com menos de 48h ou <~1.000 impressões; a re-embalagem só entra na janela D+7–D+30, e só quando retenção estiver na faixa e o CTR Browse <3%.
3. **KPI mensal de fidelização:** medir a fatia de watch time de inscritos e a fatia de "casuais" subindo — se ficar preso em quase-só-"novos" por 4+ semanas, o próximo bloco de vídeos vira SÉRIE nomeada com end screen para o próximo (recomendação oficial do YouTube).
4. **Travar os 3 slots com dado:** rodar o teste de slot da seção 6 (4 vídeos por horário candidato ao longo de ~3 semanas) comparando qua 17h × 19h e confirmando dom 10h; decidir pela média consistente, não pelo campeão.
5. **Publicar 1–4h antes do pico do NOSSO mapa de calor:** abrir "Quando seus espectadores estão no YouTube" antes de agendar cada um dos 3 vídeos e ajustar o horário de subida ao pico real, não à tabela genérica.
6. **Ler o funil e o público JUNTO com a curva no crivo:** nenhum veredito de vídeo fecha só com a curva de retenção — anexar CTR por fonte + segmento de público ao veredito.
