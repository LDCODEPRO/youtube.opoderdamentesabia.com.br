# Calibração do score com retenção real (o júri que confere a realidade)
*Pesquisa de 2026-07-17 (ciclo 2) · O Sintetizador · fontes ao lado de cada número*

Escrevi um score de retenção-no-papel ([SCORE-AUTOMATICO-DE-RETENCAO-NO-PAPEL](SCORE-AUTOMATICO-DE-RETENCAO-NO-PAPEL.md))
com pesos que **eu chutei** a partir da literatura. Um juiz que nunca é conferido **deriva** — anotei
isso duas vezes já. Este guia é o antídoto: o **laço de calibração** que transforma o score de "palpite
educado" em "instrumento medido", usando a curva de retenção real do YouTube Studio. É o *próximo
estudo* que ficou pendente no meu PESQUISA.md desde o ciclo 1.

---

## PARTE 1 — Ler o instrumento certo (o que o YouTube Studio realmente diz)

Antes de comparar qualquer coisa, preciso ler a retenção como ela é definida **oficialmente**, não como
os blogs resumem ([YouTube Help — *Measure key moments for audience retention*](https://support.google.com/youtube/answer/9314415)):

| Termo oficial | O que é (definição do YouTube) | Como uso |
|---|---|---|
| **Intro** | "% da audiência que ainda assistia após os **primeiros 30 segundos**" | Nota real da minha **dimensão 1 (Muro)** |
| **Top moments** | "momentos onde quase ninguém saiu enquanto assistia" | Confirma meus `[P]` (payoffs) e o re-hook |
| **Spikes** | "momentos **reassistidos ou compartilhados**" | Frases citáveis que funcionaram → aprender o padrão |
| **Dips** | "momentos **pulados** ou onde o espectador **parou de vez**" | Meus blocos de pior S_bloco deveriam cair AQUI |
| **Linha plana** | público assistiu "do início ao fim" daquela parte | O padrão-ouro; queda gradual = perda de interesse |

**Condições pra o relatório existir** ([YouTube Help](https://support.google.com/youtube/answer/9314415)):
vídeo com **≥ 60 s** e **≥ 100 visualizações**; dados levam **1–2 dias** pra processar. Ou seja: cada
vídeo nosso só entra na calibração ~2 dias depois de publicado e depois de bater 100 views.

**Absoluta vs Relativa** — as duas importam por motivos diferentes:
- **Absoluta** = a curva do nosso vídeo. É o que eu comparo com meu S_bloco.
- **Relativa** = desempenho contra outros vídeos de **duração parecida** ([YouTube Help](https://support.google.com/youtube/answer/9314415)).
  *Leitura minha:* uso a relativa pra saber se uma queda é problema NOSSO ou comportamento normal
  daquela duração — impede eu "consertar" um bloco que na verdade está na média.

**Âncora de campo pra o Muro:** vídeos onde **>65% passam do 1º minuto** têm **+58% de duração média**
no resto ([Retention Rabbit, mai/2025](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report)).
Meta operacional: **Intro (30s) ≥ 65%**. Abaixo disso, minha dimensão 1 errou e reescrevo a abertura.

---

## PARTE 2 — Alinhar papel e realidade (traduzir bloco em segundo)

A curva do YouTube é em **tempo**; meu score é em **blocos de texto**. A ponte é o **PPM da casa**:

1. Pegar o **PPM real** = `palavras do roteiro ÷ minutos de narração` do áudio final (regra do
   [METRICAS-OBJETIVAS](METRICAS-OBJETIVAS-DE-ROTEIRO-PT-BR.md); 140 é só provisório).
2. Para cada bloco, `tempo_início = palavras_antes_do_bloco ÷ PPM`.
3. Ler na curva a **retenção % naquele intervalo** = o "resultado real" do bloco.

Fica uma tabela por vídeo:

| Bloco | S_bloco (papel, 0–100) | Intervalo (s) | Retenção real média (%) | Δ (real − esperado) |
|---|---|---|---|---|
| 1 (gancho) | 88 | 0–30 | Intro = 61% | ⚠ paper otimista |
| 2 | 74 | 30–95 | 55% | ok |
| 3 | 41 | 95–150 | 58% | ⚠ paper pessimista |
| … | | | | |

A coluna Δ é ouro: onde **papel e realidade discordam**, ou minha rubrica está errada, ou o problema
não é o texto (é edição, b-roll, thumbnail). É a conversa que levo pro Gerente.

---

## PARTE 3 — A conta que diz se o score presta (Spearman)

A pergunta central: **a ORDEM dos meus blocos por S_bloco bate com a ORDEM deles por retenção real?**
Isso é correlação de postos = **Spearman (ρ)** — a mesma métrica que o paper de rubrica usou pra provar
seu score ([arXiv:2512.21402 reporta ρ = 0,71](https://arxiv.org/html/2512.21402)).

**Interpretação dos valores** (faixas usuais em validação; [tandfonline 2022, teste robusto de permutação](https://www.tandfonline.com/doi/full/10.1080/03610926.2022.2121144)):

| ρ (Spearman) | Leitura | O que faço |
|---|---|---|
| > 0,7 | forte | score confiável — mantenho pesos |
| 0,3 – 0,7 | moderado | útil, mas ajusto pesos das dimensões que erram |
| < 0,3 | fraco | rubrica está vaga/errada — simplificar e reformular |

**Meta da casa (leitura minha):** mirar **ρ ≥ 0,5** entre S_bloco e retenção real por bloco; e, no
nível do vídeo inteiro, **S_global × duração média real** também ≥ 0,5. Não miro 0,71 de cara — aquele
foi treinado com muitos vídeos; começo humilde.

**Receita pronta:**
```python
from scipy.stats import spearmanr   # pip install scipy
# s_blocos e ret_real na MESMA ordem de blocos, do mesmo vídeo (ou empilhando vários)
rho, p = spearmanr(s_blocos, ret_real)
# rho = concordância de ordem; p = chance de ser sorte (ver Parte 4)
```

Refinamento pra depois (quando houver dados): índice composto `0,6 × Spearman + 0,4 × Pearson` —
mistura "acertei a ordem" com "acertei a distância" ([arXiv:2508.02516](https://arxiv.org/pdf/2508.02516)).

---

## PARTE 4 — O perigo do "poucos vídeos" (não me enganar com sorte)

Calibrar com 3 vídeos é ruído, não sinal. Cuidados obrigatórios:

- **Spearman com amostra pequena engana** — o teste padrão vai mal com poucos dados; usar **teste de
  permutação** para o p-valor ([tandfonline 2022](https://www.tandfonline.com/doi/full/10.1080/03610926.2022.2121144)).
  *Regra prática:* não mexer em peso nenhum com **p > 0,05** ou com **menos de ~15 pares** bloco-retenção.
- **Dispersão mínima:** Spearman "produz resultado enganoso quando uma variável está concentrada num
  só valor" ([Statistics By Jim — Spearman](https://statisticsbyjim.com/basics/spearmans-correlation/)).
  Se todos os S_bloco derem ~80, não há o que correlacionar — a rubrica precisa **espalhar** as notas.
- **A cadência é minha aliada:** 3 vídeos/semana = **~12/mês**. Com ~4–6 blocos cada, chego a **50–70
  pares bloco-retenção por mês** — amostra decente para o 1º ciclo sério de calibração em ~3–4 semanas.
- **Confundidores:** retenção sofre de thumbnail, título, edição, b-roll, não só do roteiro. Por isso
  calibro **por bloco interno** (onde thumbnail/título já agiram igual para todos os blocos) e trato o
  **Intro** como o sinal mais limpo do texto de abertura.

---

## PARTE 5 — Reaprender os pesos (virar os chutes em números medidos)

Assim que houver amostra, os pesos provisórios do score dão lugar a pesos **aprendidos** — foi
exatamente assim que o paper achou que "energia de áudio" pesa 12,4%, "variância de quadro" 10,7% etc.,
via importância SHAP ([arXiv:2512.21402](https://arxiv.org/html/2512.21402)). Minha versão enxuta:

1. Montar a tabela: uma linha por **bloco publicado**, colunas = as 7 notas de dimensão + a **retenção
   real** do bloco.
2. Rodar uma regressão simples (retenção ~ dimensões) ou correlacionar **cada dimensão** com a retenção
   isoladamente (Spearman por dimensão) — a dimensão que mais correlaciona **merece mais peso**.
   ("Validação de rubrica por Spearman identifica quais critérios mais predizem o resultado" —
   [princípio de validade preditiva](https://statisticsbyjim.com/basics/spearmans-correlation/)).
3. **Substituir** os pesos da tabela do score (22/18/16/14/12/12/6) pelos proporcionais à importância
   medida. Registrar a data e o ρ atingido — versionar o score, nunca sobrescrever calado.
4. Repetir a cada ~15 vídeos novos. Score é organismo vivo, não pedra.

> **Guarda-corpo (leitura minha):** só troco peso com evidência (p < 0,05, amostra suficiente). Entre
> calibrações, os pesos ficam **congelados** — mexer a cada vídeo é perseguir ruído e é como eu *volto*
> a derivar. Disciplina de instrumento: medir muito, ajustar pouco.

---

## PARTE 6 — Ritual de calibração (o que roda a cada vídeo e a cada mês)

**A cada vídeo publicado (~2 dias depois, com ≥100 views):**
- [ ] Puxar do YouTube Studio: **Intro %**, curva de retenção absoluta, Top moments, Dips.
- [ ] Calcular o **PPM real** e alinhar blocos → segundos (Parte 2).
- [ ] Preencher a linha do vídeo: S_bloco previsto × retenção real; marcar os Δ grandes.
- [ ] Conferir: **os Dips caíram nos meus piores S_bloco?** Se sim, score acertou; se não, investigar.
- [ ] Intro < 65%? → dimensão Muro falhou naquele vídeo: dissecar por que meu papel achou o gancho forte.

**A cada ~15 vídeos (mensal, na cadência de 3/semana):**
- [ ] Rodar Spearman S_bloco × retenção (Parte 3) e por dimensão (Parte 5).
- [ ] Se ρ ≥ 0,5 e p < 0,05: reaprender pesos e versionar o score.
- [ ] Se ρ < 0,3: a rubrica está vaga — simplificar perguntas SIM/NÃO, aumentar dispersão das notas.
- [ ] Levar ao Gerente 1 aprendizado que vira REGRA de produção (ex.: "gancho de pergunta bate gancho
      de afirmação em Intro" — só depois de comprovado).

---

## Como aplicar no próximo vídeo
1. **Já no vídeo de estreia (hoje, 10h):** ~2 dias depois, puxar Intro % e a curva, e registrar o
   **primeiro par** "S_bloco previsto × retenção real" — a calibração começa com o vídeo 1, não espera.
2. **Fixar o PPM real** com o áudio de estreia e usá-lo pra alinhar blocos→segundos em toda calibração
   (fim do 140 provisório).
3. **Criar a planilha-mãe** (1 linha por bloco publicado: 7 notas + retenção real) e alimentá-la a cada
   um dos 3 vídeos/semana — é o combustível do Spearman.
4. **Regra de ouro anti-deriva:** não mexer em peso nenhum antes de ~15 pares e p < 0,05; até lá o score
   fica congelado e serve só de bússola.
5. **Todo mês, 1 número ao Gerente:** o ρ atual do score (o "quanto meu papel prevê a realidade"), pra
   o painel mostrar se o júri está calibrado ou derivando.
6. **Caçar o Δ, não o elogio:** o valor está nos blocos onde papel e realidade DISCORDAM — é ali que a
   rubrica aprende. Concordância confortável não ensina nada.
