# Ler Curvas de Retenção no Analytics — Manual de Diagnóstico (ciclo 2 — 17/07/2026)

> **Pesquisador · O Poder da Mente Sábia** · Aprofunda (não repete) a seção de retenção do ALGORITMO-2026-SATISFACAO-CTR-RETENCAO.md: lá estão as METAS (65%+ no 1º min, 50–60% de AVD); aqui está COMO LER a curva no YouTube Analytics e o que fazer com cada formato de queda.
> **Honestidade:** fontes são guias de analytics de mercado (não documentação oficial do YouTube); números sempre com a fonte ao lado; interpretação minha marcada como **"leitura minha"**.

---

## 1. Onde olhar no Studio (a receita de leitura)

1. YouTube Studio → Conteúdo → vídeo → **Engajamento** → gráfico "Retenção de público".
2. **Linha azul = seu vídeo; faixa cinza = a faixa típica do SEU canal.** Performance relativa à média do próprio canal importa mais que o número absoluto ([Virvid — Retention Graphs 2026](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026)).
3. O Studio destaca o **"Intro"** (primeiros 30s) como métrica própria — é o primeiro lugar a checar ([Virvid](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026)).
4. **Segmentar "novos × recorrentes"**: se o espectador recorrente completa o vídeo mas o NOVO despenca nos primeiros 30s, o gancho falha para público frio — teto de crescimento, revisar abertura imediatamente ([Virvid](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026)).
5. Diagnóstico nunca é de 1 vídeo só: **padrões repetidos em vários uploads valem mais que a curva de um vídeo isolado** ([TubeAnalytics — Retention Curve Guide](https://www.tubeanalytics.net/blog/youtube-retention-curve-analysis-guide)). Auditar os últimos 10 vídeos procurando pontos de queda repetidos ([OpusClip — Retention Graphs Explained](https://www.opus.pro/blog/youtube-retention-graphs-explained)).

## 2. O dicionário das formas de curva (o que cada desenho significa)

| Forma | O que significa | O que fazer |
|---|---|---|
| **Penhasco inicial** (queda forte nos primeiros 15–30s, depois linha estável) | Gancho falhou; quem sobrevive fica — a maioria morre antes da substância | Refazer abertura: pagar a promessa do título DE IMEDIATO, cortar preâmbulo; alinhar thumb↔abertura ([Virvid](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026), [Humble&Brag — Retention Benchmarks](https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks)) |
| **Declínio gradual** | NORMAL — o que importa é a inclinação: ~5% de perda por minuto no corpo = saudável; ~15%/min = problema estrutural ([Joyspace — Retention Curve Anatomy](https://joyspace.ai/retention-curve-anatomy-viral-video)) | Se a inclinação passa disso: cortar enchimento, variar ritmo/frase/seção ([TubeAnalytics](https://www.tubeanalytics.net/blog/youtube-retention-curve-analysis-guide)) |
| **Penhasco no meio** (queda abrupta num timestamp específico) | Algo NAQUELE momento expulsou gente: tangente, visual parado demais, transição confusa, bloco comercial longo | Dar scrub no timestamp exato e diagnosticar a cena; cortar/reformular o trecho ([OpusClip](https://www.opus.pro/blog/youtube-retention-graphs-explained), [TubeAnalytics](https://www.tubeanalytics.net/blog/youtube-retention-curve-analysis-guide)) |
| **Serrote/picos** (linha sobe em pontos) | OURO: espectador REBOBINOU para rever — é o conteúdo mais valioso do vídeo | Identificar o que tornou o momento forte e repetir o padrão nos próximos ([OpusClip](https://www.opus.pro/blog/youtube-retention-graphs-explained), [Virvid](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026)) |
| **Curva plana** (maioria chega ao fim) | Ideal raro; sinal de alinhamento tema-ritmo perfeito → distribuição ampla | REPLICAR a estrutura desse vídeo nos próximos uploads ([TubeAnalytics](https://www.tubeanalytics.net/blog/youtube-retention-curve-analysis-guide), [Humble&Brag](https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks)) |
| **Trecho plano no meio** | Ali os espectadores PARARAM de sair — objetivo é empurrar esse platô para o início do vídeo | Antecipar o conteúdo que segura ([Virvid](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026)) |

**Régua de queda pontual:** qualquer mergulho que perde **4%+ dos espectadores num ponto** merece scrub e diagnóstico ([Virvid](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026)). Causas típicas: explicação longa sem mudança visual, transição abrupta, trecho de "recado", problema de áudio.

## 3. Benchmarks de retenção POR DURAÇÃO (novo — calibra nosso 5–30min)

Fonte: [Humble&Brag — Audience Retention Benchmarks 2026](https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks):

| Duração | Retenção média saudável |
|---|---|
| < 5 min | 50–70% |
| 5–15 min | 40–55% |
| 15–30 min | 30–45% (**50%+ em vídeo de 15min+ = excepcional**) |
| > 30 min | 25–35% é normal (25% de um vídeo de 40min = 10min assistidos — sinal fortíssimo em minutos absolutos) |

Complementos ([Virvid](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026)): só **16,8%** dos vídeos passam de 50% de retenção; vídeos com **40%+** superam substancialmente a linha de base do algoritmo; +10 pontos de retenção média do canal ≈ **+25% de impressões em 30 dias**.

**Leitura minha — atualização da régua do crivo:** nossa meta única de "50–60% de AVD" estava certa para vídeos de ~10min, mas é IRREAL para 20–30min. Régua nova por faixa: vídeo de 5–15min → aprovado ≥45%, excelente ≥55%; vídeo de 15–30min → aprovado ≥35%, excelente ≥45%. O 1º minuto continua com meta única: 65%+ (já era regra). Um vídeo de 25min com 38% NÃO é reprovado — é normal-bom da faixa dele.

Por tipo de conteúdo ([Humble&Brag](https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks)): tutoriais 45–55% (saem quando acham a resposta); **thought leadership 35–50% com queda inicial íngreme de curiosos** — nosso conteúdo motivacional se comporta como thought leadership. **Leitura minha:** queda um pouco maior no 1º minuto é ESPERADA no nosso formato; o que não pode é penhasco (>40% perdidos no início = gancho réu, [TubeAnalytics](https://www.tubeanalytics.net/blog/youtube-retention-curve-analysis-guide)).

## 4. A receita de conserto (checklist por sintoma)

- **Penhasco inicial** → reescrever os 30 primeiros segundos: entregar a promessa do título na 1ª frase; zero logo/enrolação; conferir se a thumb não promete algo que a abertura não paga ([Humble&Brag](https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks)).
- **Inclinação forte no corpo** → plantar re-ganchos nos marcos de **25% e 65%** da duração; variar comprimento de frase e de seção; casar duração do roteiro com a profundidade do tema ([Virvid](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026)).
- **Penhasco no meio** → cortar o trecho ou movê-lo; recados/blocos "comerciais" só em transição natural de bloco ([TubeAnalytics](https://www.tubeanalytics.net/blog/youtube-retention-curve-analysis-guide)).
- **Sem picos de rewatch** → leitura minha: falta momento "frase-martelo" (conceito dito de forma tão forte que a pessoa volta pra ouvir de novo). Encomendar ao Roteirista 1–2 frases-martelo por vídeo, posicionadas nos minutos do meio.
- **Novos caem, recorrentes ficam** → o gancho fala com quem já nos conhece; reescrever abertura sem pressupor contexto do canal ([Virvid](https://virvid.ai/blog/retention-graphs-how-to-read-youtube-analytics-2026)).

## Como aplicar no próximo vídeo

1. **Ritual pós-publicação (cadência 3/semana):** D+2 de cada vídeo (ter/qui/dom), abrir a curva de retenção e classificar o desenho pelo dicionário da seção 2 — registrar no pesquisa_semana.json: forma da curva, % no 1º minuto, retenção final, timestamps de mergulho ≥4% e de pico.
2. **Régua por duração no crivo:** aplicar a tabela da seção 3 (5–15min ≥45%; 15–30min ≥35%) em vez da meta única — reprovar por retenção só dentro da faixa certa.
3. **Scrub obrigatório:** todo mergulho ≥4% vira nota com timestamp + causa provável + ordem de correção para o próximo roteiro (padrão repetido em 2 vídeos = regra nova para o Gerente).
4. **Segmentar novos × recorrentes** no 1º vídeo de cada semana: se novos caírem >40% no 1º minuto, a abertura do vídeo seguinte (já em produção) é reescrita antes de renderizar.
5. **Colecionar picos:** cada pico de rewatch vira linha no gabarito ("o que fez rebobinar") — o Roteirista recebe a lista na pauta de segunda.
6. **Replicar curva plana:** se um vídeo der curva plana/quase plana, a ESTRUTURA dele (ordem dos blocos, ritmo, duração) vira molde oficial do próximo domingo — o slot de maior audiência.
