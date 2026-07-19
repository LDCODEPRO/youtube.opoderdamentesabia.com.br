# Julgamento cego e retenção no papel
*Pesquisa de 2026-07-17 · O Sintetizador · fontes ao lado de cada número*

Este guia responde duas perguntas que definem meu trabalho de júri:
1. **Como dar nota sem me enganar** (o que a ciência de "LLM como juiz" e a indústria de cinema já sabem sobre avaliar texto).
2. **Como prever retenção lendo o roteiro** — antes de existir vídeo.

---

## PARTE 1 — O que a indústria de cinema usa (script coverage)

O *script coverage* de Hollywood é a rubrica de roteiro mais testada do mundo. Critérios padrão
([Wikipedia](https://en.wikipedia.org/wiki/Script_coverage), [Greenlight Coverage](https://glcoverage.com/2025/08/11/script-coverage-ratings-explained/)):

| Critério deles | Tradução para nosso canal |
|---|---|
| Conceito (originalidade + apelo) | A ideia do vídeo tem ângulo próprio ou é o 500º "disciplina é liberdade"? |
| Estrutura | Blocos com começo-desenvolvimento-payoff, escada emocional que sobe |
| Personagem | No nosso caso: o ESPECTADOR é o personagem — ele se vê na história? |
| Diálogo | Narração: frases faladas, não escritas; travou a língua = reescreve |
| Ritmo (pacing) | Variação de energia; nenhum bloco parado |
| Mercado | Título/capa/gancho casam com o que o público do território clica |

Veredito final deles é de 3 níveis — **Pass / Consider / Recommend** — não nota fina.
Lição: profissional experiente evita escala granular no veredito global; a nota fina serve
para comparar blocos, não para "aprovar".

## PARTE 2 — O que a ciência de "LLM como juiz" manda (e eu SOU um LLM juiz)

Fonte principal: [guia Evidently AI](https://www.evidentlyai.com/llm-guide/llm-as-a-judge) + estudos de viés
([Medium/J. Lee](https://medium.com/@jiminlee-ai/understanding-llm-as-a-judge-benefits-biases-and-best-practices-4b4d5cc3cbcd)).

### Os 4 vieses que me atacam quando julgo A, B e C
1. **Viés de posição** — o juiz tende a favorecer o texto lido primeiro.
   *Antídoto:* comparar A-vs-B **e depois B-vs-A**; só vale o veredito se as duas ordens concordarem. Divergiu = empate técnico.
2. **Viés de verbosidade** — juiz prefere o texto mais LONGO mesmo quando não é melhor.
   *Antídoto:* nossa regra "empate → vence o mais curto" já é o antídoto certo (agora com fundamento).
3. **Viés de autopreferência** — juiz favorece texto que "soa como ele".
   *Antídoto:* julgar ÀS CEGAS — apagar os rótulos A/B/C antes de ler. A rubrica antiga já dizia "julgue pelo texto, não pelo autor"; agora é protocolo: embaralhar e esconder autoria.
4. **Viés de autoridade** — texto confiante vence texto honesto que hesita.
   *Antídoto:* checar afirmações fortes contra a pesquisa do Pesquisador antes de premiá-las.

### Regras de rubrica que aumentam a confiabilidade
- **Binário > escala 0–10.** "Avaliações binárias tendem a ser mais confiáveis e consistentes" ([Evidently](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)). Upgrade da minha rubrica: cada critério vira 2–4 perguntas SIM/NÃO e a "nota" do bloco é a soma. Ex.: GANCHO = (tem tensão em 1 frase? + promessa concreta? + dá pra visualizar? + evitável de pular?).
- **Um critério por passada.** Não julgar gancho+clareza+emoção de uma vez; ler o roteiro 5 vezes, uma lente por vez.
- **Justificativa escrita junto de cada nota** — melhora a qualidade do julgamento e deixa auditável.
- **Consistência:** julgar 2 vezes; se as notas dançarem muito, a rubrica está vaga demais — simplificar.
- **Calibrar contra a realidade:** quando o vídeo publicar, comparar meu ranking dos blocos com a curva de retenção real no YouTube Studio. Juiz que nunca é conferido deriva. (Pareamento bem feito atinge 80%+ de acordo com humanos — [Evidently](https://www.evidentlyai.com/llm-guide/llm-as-a-judge); a meta é eu concordar com a CURVA.)

## PARTE 3 — Retenção no papel: os números do campo de batalha

Benchmarks 2025 ([Retention Rabbit, 10.000+ vídeos, Q1/2024–Q1/2025](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report)):

- Retenção média de um vídeo no YouTube: **23,7%**. Só 1 em 6 vídeos passa de 50%.
- **55%+ dos espectadores somem no 1º minuto**; a "janela de decisão" é de **8 segundos**.
- **Muro do 1º Minuto:** menos de 45% passam do minuto 1, independente da duração.
- Pico de retenção por duração: vídeos de **5–10 min (31,5%)** — nossa faixa 5–30min começa no ponto doce.
- Nicho educacional/como-fazer: **42,1%** de retenção média (o melhor nicho) — nosso território motivacional-educacional joga na divisão de cima.
- Valor claro nos **primeiros 15s** → **18% mais retenção** no marco de 60s.
- Vídeos >10 min sofrem um **êxodo secundário entre 55–65% do vídeo** → é ali que entra o re-hook.
- Últimos 10 segundos: só **16%** ainda estão lá → CTA final não pode morar só no fim.
- ⚠️ **ALERTA DE CASA:** conteúdo percebido como IA teve **70% menos retenção** que conteúdo com rosto humano, e narração IA perdeu **35% dos espectadores nos primeiros 45s** (mesma fonte). Para nosso canal 100% IA, a ordem "humanizado" não é estética — é sobrevivência. O roteiro precisa soar gente: contrações, hesitação calculada, história pessoal plausível, zero frase de robô.
- Open loops: ganho de watch time é **direcional, sem número confiável** — a própria fonte admite que "os valores exatos variam por fonte" ([YouTubers Hub](https://youtubershub.com/blog/how-to-write-a-video-script-and-hook)). NUNCA citar "+32%" como fato.
- Benchmarks por duração citados em guias de 2026 (não conferi a metodologia primária — usar como direcional): forte = 50–60% (5–10min), 40–50% (10–15min), 35–45% (15–30min) ([Humble & Brag](https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks), [PrePublish](https://prepublish.ai/blog/youtube-retention-benchmarks-2026)).

### Mapa de queda — o que o roteiro DEVE ter em cada zona
| Zona do vídeo | O que acontece | O roteiro precisa ter |
|---|---|---|
| 0–8s | Janela de decisão | Tensão + promessa na 1ª frase; nada de "olá, bem-vindos" |
| 8–60s | Muro do 1º minuto (55% somem) | Valor visível até 15s; primeiro loop aberto; confirmação da promessa do título |
| Cada 60–90s | Atenção derrete | Pattern interrupt: pergunta direta, número, virada de tom (TubeAI sugere 30–45s; [YouTubers Hub](https://youtubershub.com/blog/how-to-write-a-video-script-and-hook) 60–90s — leitura minha: no nosso ritmo contemplativo, 60–90s) |
| 40–60% do vídeo | Êxodo secundário (>10min) | RE-HOOK explícito: "a parte que quase ninguém aplica vem agora" ([TubeAI](https://learn.tubeai.app/blog/youtube-script-writing-retention)) |
| Últimos 60–90s | Só os fiéis | Payoff que fecha o loop do gancho + UM único CTA ([TubeAI](https://learn.tubeai.app/blog/youtube-script-writing-retention)) |

### Checklist "retenção no papel" (rodar no roteiro FINAL montado)
- [ ] 1ª frase tem tensão E promessa? (critério de 8 segundos)
- [ ] Valor concreto aparece antes da linha ~15s?
- [ ] Existe pelo menos 1 loop aberto ATIVO em qualquer ponto do roteiro?
- [ ] 3–5 blocos, cada um com setup→desenvolvimento→payoff próprio ([TubeAI](https://learn.tubeai.app/blog/youtube-script-writing-retention))?
- [ ] Re-hook escrito entre 40–60% do texto?
- [ ] Pattern interrupt a cada ~60–90s de narração (≈150–220 palavras em PT falado — leitura minha)?
- [ ] CTA único, e a semente dele plantada antes dos últimos 10s?
- [ ] Passa no teste anti-robô? (ler em voz alta: alguma frase que humano nunca falaria?)

## Como aplicar no próximo vídeo
1. Julgar os 3 roteiros ÀS CEGAS (apagar rótulos A/B/C) e em DUPLA ORDEM nas comparações; divergiu = empate → vence o mais curto.
2. Converter os 5 critérios da rubrica em perguntas SIM/NÃO por bloco e somar (abandonar nota 0–10 "no olho").
3. Rodar o checklist "retenção no papel" no roteiro final e não liberar com item vermelho nas zonas 0–8s e 8–60s.
4. Marcar no roteiro final a posição do re-hook (40–60%) e dos pattern interrupts (a cada 150–220 palavras).
5. Passada anti-robô dedicada: caçar frases de IA (listas simétricas demais, "é importante ressaltar", conclusões redondas) — os 70%/35% de penalidade são a nossa maior ameaça.
6. Depois que o vídeo publicar, pedir ao Gerente a curva de retenção e comparar com minhas notas por bloco — calibração do júri.
