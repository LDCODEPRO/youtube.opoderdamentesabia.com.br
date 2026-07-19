# Métricas objetivas de roteiro PT-BR (medir antes de julgar)
*Pesquisa de 2026-07-17 (ciclo 2) · O Sintetizador · fontes ao lado de cada número*

O ciclo 1 me deu rubrica e checklist. Este guia dá o que faltava: **números que uma máquina
extrai do roteiro sem opinião** — legibilidade calibrada para português, conversão texto→tempo,
densidade de payoff por minuto e razão promessa/entrega. É a camada "mecânica" que alimenta
o score automático (ver guia [SCORE-AUTOMATICO-DE-RETENCAO-NO-PAPEL](SCORE-AUTOMATICO-DE-RETENCAO-NO-PAPEL.md)).

---

## PARTE 1 — Legibilidade em PT-BR (a fórmula certa, não a gringa)

### A pegadinha do +42
A fórmula clássica de Flesch foi feita para INGLÊS. Aplicar a original em texto português dá
resultado errado: a adaptação brasileira (Martins et al., 1996, ICMC-USP São Carlos) mostrou que
textos em português pontuam, na média, **42 pontos abaixo** dos equivalentes em inglês — por isso
a fórmula adaptada soma essa constante ([legibilidade.com](https://legibilidade.com/), [UFRGS — Índices de Leiturabilidade](https://www.ufrgs.br/textecc/acessibilidade/files/%C3%8Dndices-de-Leiturabilidade.pdf)).

### Fórmula oficial da casa — Índice de Legibilidade de Flesch adaptado (Martins et al. 1996)
```
ILF = 248,835 − (1,015 × ASL) − (84,6 × ASW)
ASL = palavras ÷ frases (tamanho médio da frase)
ASW = sílabas ÷ palavras (sílabas médias por palavra)
```
Fonte: [legibilidade.com](https://legibilidade.com/) · [Wikipédia PT — Legibilidade de Flesch](https://pt.wikipedia.org/wiki/Legibilidade_de_Flesch).

Faixas de interpretação (escala 0–100, maior = mais fácil) ([UFRGS — Índices de Legibilidade de Flesch](https://www.ufrgs.br/bioetica/ilfk.htm)):
| ILF | Nível | Tradução prática |
|---|---|---|
| 75–100 | Muito fácil | até 4ª série |
| 50–75 | Fácil | conclusão do fundamental |
| 25–50 | Difícil | ensino médio/universitário |
| 0–25 | Muito difícil | texto acadêmico |

**Meta da casa (leitura minha):** narração falada precisa ser MAIS fácil que texto escrito —
mirar **ILF ≥ 60** no roteiro final; bloco abaixo de 50 = alarme de "dissertação", reescrever
em frase falada. Legibilidade é **guarda-corpo, não troféu**: mede escolaridade exigida, não
interesse — subir o ILF não deixa o texto bom, só remove uma barreira.

### Duas adaptações circulam — escolher UMA e nunca misturar
O site ALT recalibrou a fórmula com corpus próprio e usa `226 − 1,04×ASL − 72×ASW`
([legibilidade.com/sobre](https://legibilidade.com/sobre)) — coeficientes DIFERENTES dos de Martins.
Nenhuma está "errada", mas os números não são comparáveis entre si. **Padrão da casa: Martins 1996**
(é a referência citada pela literatura acadêmica). Se usar o site ALT para conferência rápida,
anotar que a régua é outra.

### Ferramentas prontas (custo zero)
- **ALT** ([legibilidade.com](https://legibilidade.com/)) — web, grátis: calcula 6 índices adaptados ao PT
  (Flesch, Gulpease, Flesch-Kincaid, Gunning Fog com as 5.000 palavras mais frequentes do PT-BR, ARI,
  Coleman-Liau) + nota composta ([sobre](https://legibilidade.com/sobre), [paper arXiv:2203.12135](https://arxiv.org/pdf/2203.12135)). Bom para conferência manual.
- **NILC-Metrix** — o canhão: **200 métricas** de complexidade textual do PT-BR (coesão, coerência,
  psicolinguística), desenvolvidas desde 2008 (evolução do Coh-Metrix-Port/PorSimples), cobre língua
  **escrita E falada**; web + código aberto ([arXiv:2201.03445](https://arxiv.org/abs/2201.03445),
  [github.com/nilc-nlp/nilcmetrix](https://github.com/nilc-nlp/nilcmetrix)). Overkill para o dia a dia;
  ouro para quando formos treinar um modelo próprio de retenção.
- **textstat (Python)**: a documentação NÃO confirma suporte a português
  ([textstat.org](https://textstat.org/), [PyPI](https://pypi.org/project/textstat/)) — não confiar o ILF a ela.
  A fórmula de Martins é 1 linha; o único trabalho real é contar sílabas.

### Receita pronta — ILF em Python (sem dependência duvidosa)
```python
# pip install pyphen  (hifenização Hunspell; tem dicionário pt_BR)
import re, pyphen
dic = pyphen.Pyphen(lang="pt_BR")

def ilf_martins(texto: str) -> float:
    frases = [f for f in re.split(r"[.!?…]+", texto) if f.strip()]
    palavras = re.findall(r"[A-Za-zÀ-ÿ]+", texto)
    silabas = sum(len(dic.inserted(p).split("-")) for p in palavras)
    asl = len(palavras) / max(len(frases), 1)
    asw = silabas / max(len(palavras), 1)
    return 248.835 - (1.015 * asl) - (84.6 * asw)   # Martins et al. 1996
```
Rodar por BLOCO, não só no total: um bloco "dissertação" se esconde na média do roteiro inteiro.

---

## PARTE 2 — Do texto ao tempo: PPM do português falado

Sem converter palavras→minutos, nenhuma métrica "por minuto" existe no papel. Referências:

| Contexto | PPM | Fonte |
|---|---|---|
| Narração de vídeo PT | ~155 | [Dumela — calculadora de tempo de locução](https://dumela.tv/tools/tempo-de-locucao/) |
| Audiobook | 150–160 | [Omni Calculator PT](https://www.omnicalculator.com/pt/dia-a-dia/palavras-por-minuto) |
| YouTubers | 150–160 | [Omni Calculator PT](https://www.omnicalculator.com/pt/dia-a-dia/palavras-por-minuto) |
| Fala média geral PT (pausada) | ~110 | [Omni Calculator PT](https://www.omnicalculator.com/pt/dia-a-dia/palavras-por-minuto) |
| Guias gringos (fala em câmera) | 130–150 | [OutlierKit](https://outlierkit.com/resources/youtube-script-writing/), [Sumera](https://sumera.io/blog/how-to-write-youtube-script-keeps-viewers-watching) |

**Padrão da casa (leitura minha): 140 PPM provisório** — nosso tom é contemplativo, com pausas;
155 é rápido demais para "mente sábia". **REGRA DE CALIBRAÇÃO:** assim que o vídeo de estreia
(hoje, 10h) tiver áudio final, calcular `palavras do roteiro ÷ minutos de narração` = **PPM real da casa**,
e substituir o 140 em TODAS as contas. Chute calibrado uma vez vale mais que média da internet.

Tabela de conversão a 140 PPM (até calibrar):
| Duração alvo | Palavras de roteiro |
|---|---|
| 5 min | ~700 |
| 10 min | ~1.400 |
| 15 min | ~2.100 |
| 20 min | ~2.800 |
| 30 min | ~4.200 |

(Guias gringos estimam 1.300–1.500 palavras para 10 min a 130–150 PPM — [OutlierKit](https://outlierkit.com/resources/youtube-script-writing/), [Sumera](https://sumera.io/blog/how-to-write-youtube-script-keeps-viewers-watching) — coerente com nossa faixa.)

Marcos derivados (a 140 PPM): **linha dos 8s ≈ 19 palavras** · **linha dos 15s ≈ 35 palavras** ·
**minuto 1 ≈ 140 palavras** · **pattern interrupt a cada 60–90s ≈ a cada 140–210 palavras**.

---

## PARTE 3 — Densidade de payoff por minuto

**Definição operacional (leitura minha, formalizando o que o campo descreve):** payoff = momento
em que o espectador RECEBE algo nomeável — insight que ele consegue repetir, loop que fecha,
frase citável, instrução acionável. Densidade = `payoffs ÷ minutos estimados`.

Números do campo:
- **5 a 7 loops setup–tensão–payoff** num vídeo bem estruturado de 10–15 min — "a well-structured
  10 to 15 minute video will have five to seven of these loops"
  ([Humble & Brag](https://humbleandbrag.com/blog/how-to-write-a-youtube-script)). Isso dá **~0,4–0,6 payoffs/min**.
- **3–5 segmentos de valor**, cada um com setup→desenvolvimento→payoff próprio
  ([TubeAI](https://learn.tubeai.app/blog/youtube-script-writing-retention) — já na biblioteca, ciclo 1).
- Pattern interrupts a cada 60–90s → **7–10 re-engajamentos num vídeo de 10 min**
  ([Sumera](https://sumera.io/blog/how-to-write-youtube-script-keeps-viewers-watching)). Interrupt ≠ payoff:
  interrupt segura a atenção, payoff paga a atenção. Contar separado.
- **Escada ascendente**: "if each point is better than the last, they stay" — segunda melhor ideia
  primeiro, a MELHOR por último ([Humble & Brag](https://humbleandbrag.com/blog/how-to-write-a-youtube-script)).
- Densidade vence duração: "a tighter 8-minute video nearly always outperforms a padded 15-minute one"
  ([Humble & Brag](https://humbleandbrag.com/blog/how-to-write-a-youtube-script)). Casa com nossa regra
  "empate → vence o mais curto".

**Piso da casa (leitura minha): densidade ≥ 0,5 payoff/min** (1 payoff a cada ≤2 min), com o 1º payoff
antes da linha dos 15s (valor visível — regra do ciclo 1) e o MAIOR payoff no último bloco (escada).
Trecho de >2,5 min sem payoff = deserto; cortar ou fundir blocos.

### Como medir no papel (ritual de 10 min)
1. Marcar no roteiro final cada payoff com `[P]` e cada interrupt com `[I]`.
2. Converter posição em tempo (contagem de palavras ÷ PPM da casa).
3. Plotar mentalmente (ou na tabela de proveniência): existe deserto >2,5 min? O `[P]` mais forte está no fim?
4. Registrar `densidade = nº de [P] ÷ duração estimada` na tabela do vídeo.

---

## PARTE 4 — Razão promessa/entrega

Prometer e não pagar é o pecado nº 1: "one common mistake is promising something in the hook but
never delivering the payoff" ([StudioBinder](https://www.studiobinder.com/blog/script-writing-on-youtube/));
ferramentas de análise de roteiro checam exatamente o **alinhamento semântico entre o que o gancho
promete e o que o corpo entrega** ([PrePublish](https://prepublish.ai/guides/what-is-youtube-script-analysis)).

**Métrica da casa — RPE (Razão Promessa/Entrega):**
```
RPE = promessas PAGAS ÷ promessas FEITAS        → obrigatório: RPE = 1,0
```
Inventário de promessas (o que conta como promessa):
- o TÍTULO e o que a capa insinua (promessa implícita nº 1);
- a promessa do gancho (frase 1–2);
- toda ponte "daqui a pouco eu mostro…" / "no final você vai…" (cada uma abre uma dívida);
- todo loop aberto (já mapeado no protocolo de fusão — loop órfão é RPE < 1,0).

Regras de ouro:
- **Payoffs se escrevem PRIMEIRO** — "write the payoffs first, not the setups": garante que o vídeo
  TEM o que promete antes de prometer ([Humble & Brag](https://humbleandbrag.com/blog/how-to-write-a-youtube-script)).
  No meu fluxo de fusão: eleger os payoffs vencedores ANTES de eleger o gancho vencedor.
- A promessa central deve ser paga **cedo o bastante para saciar a curiosidade antes de o espectador
  desistir** — não guardar "a única coisa" para o minuto final ([PrePublish](https://prepublish.ai/guides/what-is-youtube-script-analysis)).
  Conciliação com a escada (leitura minha): pagar a promessa do TÍTULO no miolo; guardar para o fim
  um payoff MAIOR que o prometido.
- **Superentrega de 1** (leitura minha): 1 payoff NÃO prometido no último terço = surpresa positiva,
  o espectador sai com mais do que veio buscar. RPE alvo real: paga tudo + entrega 1 extra.

---

## Como aplicar no próximo vídeo
1. **Hoje, pós-estreia:** calcular o PPM real da casa com o áudio do vídeo 1 (`palavras ÷ minutos`) e fixar o número no meu fluxo — todas as contas por minuto passam a usar ele.
2. Rodar `ilf_martins()` por bloco em todo roteiro final: bloco < 50 volta para reescrita falada; meta ≥ 60 (com a cadência de 3/semana, o script roda em segundos e não vira gargalo).
3. Marcar `[P]` e `[I]` no roteiro final montado e registrar a densidade de payoff na tabela de proveniência; piso 0,5/min, deserto máximo 2,5 min.
4. Montar o inventário de promessas (título+capa+gancho+pontes) com o ponto de pagamento de cada uma; liberar só com RPE = 1,0 + 1 superentrega.
5. Inverter meu passo de fusão: eleger payoffs vencedores ANTES do gancho vencedor (payoff primeiro, promessa depois).
6. Ordenar os blocos em escada ascendente (2ª melhor ideia primeiro, melhor por último) — conferir se a fusão não enterrou o melhor payoff no meio.
