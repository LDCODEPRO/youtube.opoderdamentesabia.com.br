# Score automático de retenção-no-papel (nota única, montada de métricas objetivas)
*Pesquisa de 2026-07-17 (ciclo 2) · O Sintetizador · fontes ao lado de cada número*

Os guias anteriores me deram as **peças** (rubrica binária, checklist de retenção, ILF, PPM, densidade
de payoff, RPE). Este guia junta as peças num **número só, reproduzível, que qualquer máquina calcula
igual** — o "score de retenção-no-papel". Ele NÃO substitui meu julgamento; ele é o pré-filtro que
diz *onde olhar* e o portão que impede um roteiro fraco de passar por descuido. Fecha a referência
pendente do guia [METRICAS-OBJETIVAS-DE-ROTEIRO-PT-BR](METRICAS-OBJETIVAS-DE-ROTEIRO-PT-BR.md).

> **Aviso honesto (leitura minha):** os PESOS abaixo são *provisórios e arbitrados por mim* com base
> na literatura. Score não vira ciência enquanto não for **calibrado contra retenção real** — ver o
> guia [CALIBRACAO-DO-SCORE-COM-RETENCAO-REAL](CALIBRACAO-DO-SCORE-COM-RETENCAO-REAL.md). Até lá, use o
> score como **guarda-corpo e comparador**, nunca como oráculo.

---

## PARTE 1 — O molde científico (existe um jeito certo de montar score)

Um paper de 2025 fez exatamente o que eu preciso: um **rubric-based scorer** que lê um vídeo, dá nota
0–10 a poucos fatores e funde num score único de "viralidade" — e depois PROVA que o score prevê
engajamento real ([*Understanding Virality: A Rubric-based VLM Framework*, arXiv:2512.21402](https://arxiv.org/html/2512.21402)).
Três lições que copio direto:

1. **Poucos fatores, não muitos.** Eles extraem 20+ features e ficam só com os **top-5 mais
   influentes** (via análise SHAP) ([arXiv:2512.21402](https://arxiv.org/html/2512.21402)). *Leitura minha:*
   score com 15 critérios vira ruído; concentro peso nos poucos que movem a agulha.
2. **A fórmula é média ponderada normalizada:**
   ```
   S = 10 × Σ(wᵢ · sᵢ) / Σ(wᵢ)        (i = 1..N fatores)
   ```
   onde `wᵢ` = peso do fator e `sᵢ` = nota 0–10 do fator ([arXiv:2512.21402](https://arxiv.org/html/2512.21402)).
   Simples de propósito — dá pra auditar cada parcela.
3. **O teto realista de um bom score é ~0,71.** O deles correlaciona **Spearman ρ = 0,71** com o
   engajamento real (Kendall τ = 0,51; acurácia de ranking par-a-par 76,3%)
   ([arXiv:2512.21402](https://arxiv.org/html/2512.21402)). *Leitura minha:* isso me vacina contra
   arrogância — nenhum score de papel acerta 100%; a meta é **ordenar bem**, não adivinhar o número.

Outro paper reforça a régua de avaliação: combine ranking + linearidade num índice
`0,6 × SROCC + 0,4 × PLCC` (Spearman + Pearson) ([*Engagement Prediction of Short Videos*, arXiv:2508.02516](https://arxiv.org/pdf/2508.02516)).
Guardo para a fase de calibração.

---

## PARTE 2 — As 7 dimensões do score da casa

Cada dimensão vira nota **0–10** e tem um **peso provisório**. Escolhi 7 (não 15) seguindo a regra
"poucos fatores". Todas as metas vêm de guias já na biblioteca — este score só as **agrega**.

| # | Dimensão | Peso | Nota 10 = | Fonte da meta |
|---|---|---|---|---|
| 1 | **Muro do 1º minuto** | 22 | Tensão+promessa em ≤8s, valor concreto ≤15s, promessa do título confirmada | [Retention Rabbit — 55% somem no 1º min; valor em 15s = +18% retenção](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report) |
| 2 | **Densidade de payoff** | 18 | ≥0,5 payoff/min, nenhum deserto >2,5 min, maior payoff no fim (escada) | [METRICAS-OBJETIVAS](METRICAS-OBJETIVAS-DE-ROTEIRO-PT-BR.md) · [Humble & Brag — 5–7 loops/vídeo](https://humbleandbrag.com/blog/how-to-write-a-youtube-script) |
| 3 | **Promessa/entrega (RPE)** | 16 | RPE = 1,0 (toda promessa paga) + 1 superentrega | [StudioBinder — não pagar o gancho é o erro nº 1](https://www.studiobinder.com/blog/script-writing-on-youtube/) |
| 4 | **Retenção de meio** (re-hook + interrupts) | 14 | Re-hook escrito em 40–60%; interrupt a cada 60–90s | [Retention Rabbit — êxodo secundário 55–65%](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report) · [TubeAI](https://learn.tubeai.app/blog/youtube-script-writing-retention) |
| 5 | **Legibilidade falada (ILF)** | 12 | ILF ≥ 60 por bloco (Flesch-Martins), nenhum bloco < 50 | [METRICAS-OBJETIVAS](METRICAS-OBJETIVAS-DE-ROTEIRO-PT-BR.md) · [Martins et al. 1996 / UFRGS](https://www.ufrgs.br/bioetica/ilfk.htm) |
| 6 | **Humanidade / anti-robô** (burstiness) | 12 | Desvio-padrão de tamanho de frase alto; zero frase de IA | [Retention Rabbit — conteúdo "IA" = 70% menos retenção](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report) · burstiness (Parte 3) |
| 7 | **CTA + fecho de loop** | 6 | 1 CTA único, semente antes dos últimos 10s, loop do gancho fechado | [Retention Rabbit — só 16% chegam aos últimos 10s](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report) · [TubeAI](https://learn.tubeai.app/blog/youtube-script-writing-retention) |

Soma dos pesos = 100 (facilita ler `S` como "quase-porcentagem"). **Por que o Muro pesa mais que
tudo:** 55%+ do público some antes de 60s ([Retention Rabbit](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report)) —
nenhuma outra parte do roteiro decide tanto. *Leitura minha:* dimensão 1 é a única com **poder de veto**
(ver Parte 5).

### Como cada nota 0–10 sai de SIM/NÃO (herda a rubrica binária)
Nunca dou nota "no olho" (viés documentado — [Evidently AI](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)).
Cada dimensão é um punhado de perguntas SIM/NÃO; a nota é `(SIMs ÷ total) × 10`. Exemplo do **Muro (dim 1)**:
- [ ] 1ª frase tem TENSÃO?
- [ ] 1ª frase tem PROMESSA concreta?
- [ ] Valor visível/nomeável antes de ~35 palavras (≈15s)?
- [ ] Promessa do título aparece antes do fim do 1º minuto (≈140 palavras)?
- [ ] Zero "olá, bem-vindos ao canal" / aquecimento morto?

5 perguntas → cada SIM vale 2 pontos. Isso torna o score **reproduzível**: outro juiz responde as
mesmas caixas e chega no mesmo número.

---

## PARTE 3 — A dimensão traiçoeira: humanidade medida por burstiness

Nossa maior ameaça tem número: conteúdo percebido como IA teve **70% menos retenção** e narração IA
perdeu **35% dos espectadores nos primeiros 45s** ([Retention Rabbit](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report)).
Dá pra medir "cara de robô" **objetivamente** com **burstiness** = o quanto o tamanho das frases VARIA.

**Como se calcula** ([write-humanly, deep-dive — fonte de fornecedor, tratar como direcional](https://www.write-humanly.com/blog/burstiness-perplexity-deep-dive)):
> "Conte as palavras de cada frase. Calcule o desvio-padrão dessas contagens. Esse é seu score de burstiness."

Faixas que os detectores usam ([write-humanly — vendor, direcional](https://www.write-humanly.com/blog/burstiness-perplexity-deep-dive)):

| Desvio-padrão do tamanho das frases | Leitura |
|---|---|
| 0,5 a 3 | típico de **IA** (frases todas do mesmo tamanho) |
| 5 a 20 | típico de **humano** |
| < 4 | **alarme de robô** |

> ⚠️ **Advertência de honestidade:** esses cortes vêm de sites que VENDEM "humanização de IA", não de
> literatura revisada — uso como **sinal direcional**, não como lei. E burstiness **alto não garante
> texto bom**; só remove uma assinatura de robô. É guarda-corpo, igual ao ILF.

**Receita pronta — burstiness em Python:**
```python
import re, statistics
def burstiness(texto: str) -> float:
    frases = [f for f in re.split(r"[.!?…]+", texto) if f.strip()]
    tamanhos = [len(re.findall(r"[A-Za-zÀ-ÿ]+", f)) for f in frases]
    return statistics.pstdev(tamanhos) if len(tamanhos) > 1 else 0.0
# leitura da casa: < 4 = reescrever variando o comprimento; alvo ≥ 6
```

**Nota 10 na dimensão 6** = burstiness ≥ 6 **E** passa no teste anti-robô qualitativo (ler em voz alta,
caçar lista simétrica demais, "é importante ressaltar", conclusão redonda — regra do ciclo 1).
*Reforço opcional:* rodar **TTR/MATTR** (diversidade de vocabulário) pelo NILC-Metrix, que já traz TTR
pronto para PT-BR ([NILC-Metrix, arXiv:2201.03445](https://arxiv.org/abs/2201.03445)); preferir **MATTR**
a TTR cru porque TTR despenca com o tamanho do texto ([Sketch Engine — TTR é sensível ao comprimento](https://www.sketchengine.eu/glossary/type-token-ratio-ttr/)).
*Leitura minha:* burstiness é o sinal barato e forte; TTR fica como conferência de 2ª ordem, não entra no peso ainda.

---

## PARTE 4 — Score por BLOCO, não só total (o mapa de calor do papel)

O total esconde o buraco. Um bloco "dissertação" no minuto 6 morre na média de um roteiro de nota 82.
Por isso calculo o score **duas vezes**:

- **S_global** — as 7 dimensões no roteiro inteiro → o número do portão (Parte 5).
- **S_bloco** — para cada bloco, as dimensões que se aplicam a ele (payoff, ILF, burstiness, interrupt),
  convertendo a posição em tempo pelo **PPM da casa** (140 provisório até calibrar — [METRICAS-OBJETIVAS](METRICAS-OBJETIVAS-DE-ROTEIRO-PT-BR.md)).

O S_bloco vira um **mini-mapa de retenção previsto**: bloco vermelho = onde eu *aposto* que a curva real
vai cair. Isso é exatamente o que a Parte de calibração vai testar contra a curva do YouTube Studio
([CALIBRACAO-DO-SCORE-COM-RETENCAO-REAL](CALIBRACAO-DO-SCORE-COM-RETENCAO-REAL.md)).

---

## PARTE 5 — O portão: números que liberam ou barram

**Regras de veto (leitura minha, ancoradas nos benchmarks):** score alto NÃO compra um Muro fraco.

| Condição | Ação |
|---|---|
| Dimensão 1 (Muro) < 6 | **BARRADO** — reescreve o 1º minuto, ponto. (55%+ some ali — [Retention Rabbit](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report)) |
| RPE < 1,0 (loop órfão / promessa não paga) | **BARRADO** — nenhum score compensa promessa quebrada |
| Qualquer bloco com ILF < 50 | **volta pra reescrita falada** daquele bloco |
| S_global < 70 | **CONSIDER** — precisa de passada de fusão/punch-up antes de liberar |
| S_global 70–84, sem veto | **APROVADO** — segue o fluxo normal |
| S_global ≥ 85, sem veto | **RECOMMEND** — candidato a destaque |

Os 3 rótulos (Barrado→Consider→Recommend) espelham o veredito de 3 níveis do *script coverage* de
Hollywood, que evita nota fina no veredito global ([Wikipedia — script coverage](https://en.wikipedia.org/wiki/Script_coverage)).
A nota fina (S) serve para **comparar e localizar**, não para "carimbar".

**Regra de desempate mantida:** dois roteiros com S dentro de 3 pontos = empate técnico → vence o mais
CURTO (antídoto ao viés de verbosidade — [Evidently AI](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)).

---

## PARTE 6 — Esqueleto do calculador (junta tudo o que já temos)

```python
# depende das receitas do guia METRICAS-OBJETIVAS: ilf_martins(), e da burstiness() acima
PESOS = {"muro":22,"payoff":18,"rpe":16,"meio":14,"ilf":12,"humanidade":12,"cta":6}

def nota_por_sim_nao(respostas: list[bool]) -> float:
    return (sum(respostas) / len(respostas)) * 10   # 0..10

def score_global(notas: dict) -> float:
    # notas = {"muro":8.0,"payoff":6.7,...} já em 0..10
    num = sum(PESOS[k] * notas[k] for k in PESOS)
    return num / sum(PESOS.values()) * 10            # 0..100  (S = 10·Σw·s/Σw)

def portao(notas: dict, rpe: float, ilf_min_bloco: float, s: float) -> str:
    if notas["muro"] < 6:            return "BARRADO: reescrever 1º minuto"
    if rpe < 1.0:                    return "BARRADO: promessa não paga / loop órfão"
    if ilf_min_bloco < 50:           return "REVISAR bloco: ILF<50"
    if s < 70:                       return "CONSIDER: punch-up antes de liberar"
    if s >= 85:                      return "RECOMMEND"
    return "APROVADO"
```
Fórmula `S = 10·Σ(w·s)/Σw` copiada de [arXiv:2512.21402](https://arxiv.org/html/2512.21402). Roda em
segundos — cabe folgado na cadência de 3 vídeos/semana.

---

## Como aplicar no próximo vídeo
1. **Calcular S_global e S_bloco** do roteiro final montado (fusão dos 3) e anexar os dois números à
   tabela de proveniência que já entrego ao Gerente — vira o "raio-x" do vídeo.
2. **Aplicar o portão antes de liberar:** Muro < 6 ou RPE < 1,0 = devolve pra reescrita, sem exceção,
   por mais bonito que seja o resto.
3. **Rodar `burstiness()` no roteiro inteiro e por bloco:** qualquer trecho < 4 vira tarefa de variar
   o comprimento das frases (a dimensão 6 é a nossa defesa nº 1 contra os 70% de penalidade de "IA").
4. **Marcar o bloco de pior S_bloco** como "onde a curva deve cair" e avisar o Gerente para conferir
   contra o YouTube Studio quando os dados chegarem (semente da calibração).
5. **Guardar S de TODO vídeo publicado** (planilha simples: título, S_global, S por dimensão) — com
   3 vídeos/semana, em ~3 semanas há amostra pra começar a calibrar os pesos (guia de calibração).
6. **Nunca anunciar o S como verdade:** ele ordena e alerta; a palavra final continua sendo meu
   julgamento cego + a curva real. Score é bússola, não juiz.
