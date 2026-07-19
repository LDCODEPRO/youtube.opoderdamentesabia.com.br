# Protocolo de fusão das 3 versões (montar o campeão sem criar um Frankenstein)
*Pesquisa de 2026-07-17 · O Sintetizador · fontes ao lado de cada afirmação forte*

Minha missão é MONTAR o melhor dos três roteiros, não escolher um. Este guia junta o que a
ciência (fusão de saídas de LLM) e a prática (writers' rooms de TV) sabem sobre juntar versões.

---

## PARTE 1 — A ciência: fusão VENCE escolha

- **LLM-Blender (ACL 2023)** provou o nosso método: primeiro um *PairRanker* compara candidatos
  em pares e ranqueia; depois um *GenFuser* **funde os top-K num texto novo que herda as forças
  e corta as fraquezas de cada um**. Resultado: a fusão "supera significativamente cada LLM
  individual e os métodos de seleção, com margem substancial"
  ([arXiv:2306.02561](https://arxiv.org/abs/2306.02561)).
  Tradução: escolher o melhor roteiro inteiro deixa qualidade na mesa; fundir bem rende mais.
- O survey de *test-time scaling* cataloga as 3 famílias de fusão
  ([arXiv:2503.24235](https://arxiv.org/pdf/2503.24235)):
  1. **Seleção** (best-of-N): pega o melhor e joga o resto fora — o piso.
  2. **Ponderação por verificador**: cada candidato pesa conforme a nota de um avaliador — é o meu ranking por bloco.
  3. **Fusão generativa**: um redator REESCREVE juntando os melhores pedaços — é a minha costura final.
- Lição central do LLM-Blender: a fusão não é recorte-e-cola — o GenFuser **gera texto novo**
  condicionado nos melhores candidatos. Minha costura deve reescrever, não colar.

## PARTE 2 — A prática: como uma writers' room de TV junta versões

Fluxo real ([Michael Jamin, roteirista de TV](https://michaeljamin.substack.com/p/whats-the-rewrite-process-like-in),
[Anton Schettini](https://www.antonschettini.com/post/tv-writers-room-a-day-in-the-life)):

1. A sala inteira quebra a história num **beat sheet** (estrutura antes de texto).
2. UM roteirista escreve o draft (uma voz desde o início).
3. A sala reescreve JUNTA linha a linha → **Table Draft**.
4. Nas comédias, a sala se divide: **sala A** (roteiristas sêniores) conserta HISTÓRIA;
   **sala B** faz punch-up e pitcheia **5–10 alternativas ("alts") por piada** — e só a melhor entra
   ([Anton Schettini](https://www.antonschettini.com/post/tv-writers-room-a-day-in-the-life)).
5. **O showrunner decide o que fica** — muitas mãos contribuem, UMA cabeça arbitra. No nosso time, essa cabeça sou eu.
6. Detector de problema: "é fácil saber quando algo não funciona, porque a energia sai da sala" (Jamin). Achar o CONSERTO é que é difícil — não aceitar o primeiro remendo.
7. **Script doctor** = polir sem mexer no cerne da história ([PremiumBeat](https://www.premiumbeat.com/blog/art-of-movie-script-revision/)). A fase final é polimento, não reforma.

Lições diretas: estrutura se decide ANTES do texto; alternativas se pitcheiam em LOTE por
ponto específico (não "versão inteira contra versão inteira"); e sempre existe UM árbitro final.

## PARTE 3 — O protocolo (7 passos para A, B e C)

**Passo 1 — Julgar às cegas, por bloco.** Rubrica binária + dupla ordem + anti-vieses
(ver guia [JULGAMENTO-CEGO-E-RETENCAO-NO-PAPEL](JULGAMENTO-CEGO-E-RETENCAO-NO-PAPEL.md)).

**Passo 2 — Eleger a ESPINHA DORSAL.** A estrutura vencedora (ordem dos blocos, escada
emocional, arco da promessa) vem INTEIRA de um único roteiro. *Leitura minha:* estrutura
híbrida é a receita nº 1 de Frankenstein — a writers' room decide estrutura em conjunto ANTES,
nunca costurando metades de estruturas prontas.

**Passo 3 — Transplantar ÓRGÃOS, não membros.** Dos outros dois roteiros entram apenas
unidades pequenas e autocontidas: o gancho (se venceu), frases citáveis, um exemplo mais
forte, um payoff melhor. É o modelo das "alts" da sala B: substituição pontual, 1 por 1, no lugar
exato do equivalente mais fraco.

**Passo 4 — Passada de VOZ ÚNICA (meu GenFuser).** Reescrever — não colar: unificar pessoa
gramatical, temperatura emocional, vocabulário e a metáfora-mestra; refazer TODAS as
transições entre blocos de origens diferentes. Regra prática: se dá pra apontar onde termina o
texto de um autor e começa o do outro, a fusão falhou.

**Passo 5 — Teste da energia.** Leitura em voz alta (regra antiga da casa) + pergunta de Jamin:
em que linha "a energia sai da sala"? Marcar e reescrever a LINHA-CAUSA, que costuma estar
1–2 frases antes do ponto morto (*leitura minha*).

**Passo 6 — Scorecard de retenção no roteiro FINAL.** Rodar o checklist "retenção no papel" do
outro guia (zonas 0–8s, 15s, muro do minuto 1, re-hook 40–60%, CTA único). A fusão pode ter
quebrado um loop aberto sem querer — conferir cada loop: onde abre, onde fecha.

**Passo 7 — Registro de proveniência.** Tabela final: bloco → origem (A/B/C) → nota → o que
mudou na costura. Transparência já é regra da casa; também é como o time aprende quem é
forte em quê.

## Anti-padrões (os 5 jeitos de estragar uma fusão)
1. **Colcha de retalhos** — voz muda no meio; espectador sente sem saber por quê.
2. **Estrutura híbrida** — metade da escada de um, metade do outro: escada que não sobe.
3. **"Melhor frase" que quebra o fluxo** — frase citável brilhante no lugar errado vale menos que uma frase comum no lugar certo.
4. **Fusão que INFLA** — juntar os melhores pedaços tende a alongar; é o viés de verbosidade agindo em mim. O roteiro final deve ter tamanho ≤ o da espinha dorsal (*leitura minha, fundada no viés documentado em* [Evidently](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)).
5. **Loop órfão** — transplante remove a resolução de um loop aberto (ou o loop inteiro) e a promessa fica sem pagamento: veneno de retenção e de confiança.

## Como aplicar no próximo vídeo
1. Antes de ler os 3 roteiros, escrever qual estrutura o vídeo PEDE (beat sheet de 1 linha por bloco) — e só então eleger a espinha dorsal que mais casa.
2. Montar a tabela de transplantes: máximo de 1 órgão por bloco vindo de outro roteiro; mais que isso, o bloco perdedor é reescrito, não remendado.
3. Fazer a passada de voz única SEPARADA da montagem (nunca no mesmo passo), caçando toda emenda perceptível entre origens.
4. Mapear loops abertos do roteiro final: cada "abre" com seu "fecha" anotado; loop órfão = corrigir antes de liberar.
5. Medir o tamanho: roteiro final ≤ espinha dorsal; se cresceu, cortar na passada de voz.
6. Entregar ao Gerente o roteiro + tabela de proveniência + posição do re-hook.
