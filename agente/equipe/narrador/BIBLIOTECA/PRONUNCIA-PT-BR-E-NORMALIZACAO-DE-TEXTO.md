# Pronúncia PT-BR e normalização de texto antes do TTS (ciclo 2 — 2026-07-17)

> Guia prático do Narrador, ciclo 2 (aprofundamento). Todo número tem fonte (URL) ao lado. Opinião = "leitura minha". NUNCA estatística inventada.
> Os guias anteriores cuidaram de RITMO (ciclo 1), EMOÇÃO por seção e PAUSAS (ciclo 2). Falta o terceiro pilar da qualidade: **o motor pronunciar CERTO**. Uma frase com ritmo e emoção perfeitos morre se o TTS lê "R$ 1.000" como "erre-cifrão-um-ponto-zero-zero-zero" ou solta "dois mil e vinte e seis" onde era um placar. Este guia é a **normalização determinística do texto** antes de gerar áudio — a etapa que os guias anteriores não cobriram.

## 1. Por que normalizar (e por que não confiar no motor)

- Normalização de texto (TN) é a **primeira etapa** de qualquer pipeline de TTS: converter "palavras não-padrão" (números, datas, moeda, siglas, abreviações) em palavras faladas ANTES da conversão em fonemas (https://beyondwords.io/blog/the-importance-of-text-preprocessing-in-tts/, https://ar5iv.labs.arxiv.org/html/2005.05144).
- Categorias que quebram (exemplos do próprio artigo): **datas** "01/01/2001", **moeda** "$100" → "cem dólares", **unidades** "10m" (dez metros? dez milhões?), **abreviações** "St." → Street/Saint, **siglas** — algumas se leem como palavra (NASA), outras letra a letra (FBI) (https://beyondwords.io/blog/the-importance-of-text-preprocessing-in-tts/).
- **edge-tts (nosso motor atual) NÃO tem `<say-as>`**: o jeito recomendado de resolver número/data lidos errado é **pré-processar em Python e escrever por extenso ANTES** de mandar pro edge-tts (https://github.com/rany2/edge-tts, https://grokipedia.com/page/edge-tts).
- **Leitura minha:** as vozes neurais PT-BR do edge-tts até acertam muito número simples sozinhas — o problema é a INCONSISTÊNCIA. Ela acerta "2026" e erra "2026-2027"; acerta "50%" e gagueja em "R$ 1.499,90"; lê "km" às vezes "quilômetros", às vezes "ka-eme". Em 3 vídeos/semana, "às vezes" é bug garantido. Regra da casa: **o que importa NÃO se deixa ao acaso do motor — normaliza na origem.** Vale para edge-tts, Chatterbox e Sterling igual.

## 2. Onde entra no fluxo

Roteiro final (linhas de respiração) → **[NORMALIZAÇÃO]** → texto pronto para fala → TTS por blocos de 100–150 palavras (ciclo 1) → WAV.

- **Leitura minha:** a normalização é o passo entre o Roteirista e o meu gerador. O ideal é o Roteirista já entregar "falável" (ver seção 7), e eu rodo um passe automático de segurança por cima. Duas redes, nenhum número escapa.

## 3. Receita 1 — números e moeda por extenso (com `num2words`)

`num2words` suporta **`lang='pt_BR'`** e os conversores `cardinal` (padrão), `ordinal`, `ordinal_num`, `year`, **`currency`** (https://pypi.org/project/num2words/, https://github.com/savoirfairelinux/num2words).

```bash
pip install num2words
```

```python
from num2words import num2words

num2words(1000, lang='pt_BR')                    # -> "mil"
num2words(1499.90, to='currency', lang='pt_BR')  # -> reais e centavos por extenso
num2words(2026, to='year', lang='pt_BR')         # -> "vinte e vinte e seis" / "dois mil e vinte e seis"
num2words(1, to='ordinal', lang='pt_BR')         # -> "primeiro"
```
Fonte da API e dos conversores: https://pypi.org/project/num2words/ (exemplo oficial de moeda, em espanhol: `num2words(2.14, to='currency', lang='es')` → "dos euros con catorce céntimos").

- **Sempre CONFERIR a saída no ouvido** antes de fixar a receita: a forma exata (ex.: "e" antes das centenas, centavos) varia — validar com o Diretor uma vez e padronizar.
- **Leitura minha (regras do canal, calibrar no ouvido):**
  - Percentual: escrever **"por cento"** (não "%").
  - Moeda: **"mil quatrocentos e noventa e nove reais e noventa centavos"** — mas em roteiro motivacional, número redondo comunica melhor: prefira "quase mil e quinhentos reais" a um centavo exato, salvo quando o valor é o ponto.
  - Ano: decidir UM padrão ("dois mil e vinte e seis") e manter em todos os vídeos — consistência de marca.
  - Ordinal: "1º" → "primeiro", "3ª" → "terceira".

## 4. Receita 2 — datas, horas e intervalos

Não existe `say-as` no edge-tts; escrever por extenso (https://github.com/rany2/edge-tts). Uma data numérica é ambígua até para humano — "01/01/2001" deveria virar "primeiro de janeiro de dois mil e um" (https://beyondwords.io/blog/the-importance-of-text-preprocessing-in-tts/).

| Escrito | Falável (leitura minha, PT-BR) |
|---|---|
| 17/07/2026 | dezessete de julho de dois mil e vinte e seis |
| 19h / 19:00 | sete da noite *(ou "dezenove horas" — escolher UM padrão)* |
| 10h | dez da manhã |
| 2026–2027 | de dois mil e vinte e seis a dois mil e vinte e sete |
| 90s | noventa segundos |
| 3x/semana | três vezes por semana |

- **Leitura minha:** horário coloquial ("sete da noite") aquece; horário técnico ("dezenove horas") esfria. Canal motivacional → coloquial, exceto quando a precisão é o recado.

## 5. Receita 3 — siglas: palavra vs letra a letra (o erro mais chato em PT-BR)

Sigla é o caso clássico: algumas se leem como palavra (NASA), outras letra a letra (FBI) — e o motor **não adivinha qual** (https://beyondwords.io/blog/the-importance-of-text-preprocessing-in-tts/). Em PT-BR a decisão é nossa.

**Leitura minha — tabela de decisão do canal (validar no ouvido):**

| Sigla | Como o canal fala | Como escrever para o TTS |
|---|---|---|
| IA (inteligência artificial) | letra a letra: "i-á" | `i-á` ou `I.A.` (ver seção 6) |
| ONU | palavra: "ônu" | deixar `ONU` (costuma acertar) — conferir |
| OMS | letras: "ó-eme-esse" | `ó-eme-esse` |
| PIB | palavra: "pib" | deixar `PIB` |
| CEO | letras à inglesa: "cí-í-ôu" | escrever `cêo` ou `C.E.O.` e ouvir; se falhar, "diretor-executivo" |
| USP | letras: "u-esse-pê" | `u-esse-pê` |

- Regra: se a sigla PODE virar palavra estranha na boca do motor, **desmontar em letras com pontos/hífens** (`I.A.`, `ó-eme-esse`) ou **escrever a expansão** ("Organização Mundial da Saúde"). Nunca deixar ambíguo em vídeo publicado.

## 6. Receita 4 — o truque das letras separadas e da grafia fonética

- Para forçar leitura **letra a letra**, separar com pontos ou espaços: `A.B.C.` / `a b c`. É a versão pobre-mas-eficaz do `<say-as interpret-as="characters">` que o edge-tts não tem (https://github.com/rany2/edge-tts).
- Para **estrangeirismo** que o motor PT-BR erra, **reescrever foneticamente em português**: "design" → "dizáin", "insight" → "ínsait", "coach" → "côutch", "hardware" → "rárdwer". Feio no papel, certo no ouvido. (Leitura minha — validar caso a caso.)
- **ElevenLabs v3** aceita **IPA inline** em 70+ idiomas com ~80–90% de consistência (ciclo 1: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) — se um dia formos de Sterling, dá para marcar pronúncia por IPA em vez de reescrever "no chute fonético". edge-tts e Chatterbox: fica o truque da grafia fonética.
- **Homógrafos/heterônimos** (mesma grafia, som diferente) existem e confundem o motor — em inglês "lead" (guiar) × "lead" (metal) (https://beyondwords.io/blog/the-importance-of-text-preprocessing-in-tts/). Em PT-BR o clássico é a vogal aberta/fechada: **"gosto"** (substantivo, ô) × **"gosto"** (verbo, ó); **"sede"** (vontade, ê) × **"sede"** (matriz, é); **"colher"** (verbo) × **"colher"** (talher). Onde o motor errar, reescrever ("eu gósto" → "eu curto"; ou trocar a frase) — *leitura minha, o motor não tem contexto, então tiro a ambiguidade na fonte*.

## 7. Receita 5 — glossário de pronúncia do canal (ativo permanente)

**Leitura minha — criar e versionar um `glossario_pronuncia.md`/JSON** com toda palavra que já deu errado e a grafia falável certa. Vira um passe de "buscar e substituir" antes do TTS:

```
# glossario_pronuncia (exemplo)
"IA"        -> "i-á"
"design"    -> "dizáin"
"R$"        -> "reais"        # + num2words no número
"%"         -> " por cento"
"CEO"       -> "diretor-executivo"
"vs"        -> "versus"
"e.g."      -> "por exemplo"
"km"        -> "quilômetros"
```

- Cresce a cada vídeo (todo erro novo entra no glossário → nunca erra duas vezes).
- É **agnóstico de motor**: serve edge-tts, Chatterbox e Sterling.
- Abreviações precisam ser expandidas ("St." → "Saint/Street") porque o motor não sabe qual (https://beyondwords.io/blog/the-importance-of-text-preprocessing-in-tts/) — o glossário guarda a decisão do canal.

## 8. Ordem de aplicação (pipeline de normalização)

Aplicar nesta ordem (uma etapa pode criar entrada para a próxima):
1. **Glossário** (busca-e-substitui das entradas fixas).
2. **Moeda/percentual** → num2words `currency` + "por cento".
3. **Datas/horas/intervalos** → por extenso (seção 4).
4. **Números soltos** → num2words `cardinal`/`ordinal`/`year` conforme o caso.
5. **Siglas/estrangeirismos** → tabela de decisão + grafia fonética.
6. **Passe de ouvido** no bloco gerado: caçou erro novo → volta pro glossário (passo 1) e regenera.

- **Leitura minha:** automatizar 1–4 (determinístico, num2words resolve) e deixar 5 como semiautomático (glossário cobre o conhecido; o desconhecido o ouvido pega). Com 3 vídeos/semana, o que não for automático não sobrevive — mas siga sempre com o passe de ouvido, porque número por extenso também pode soar pesado ("mil quatrocentos e noventa e nove reais e noventa centavos" cansa) e às vezes o melhor é reescrever o roteiro.

## Como aplicar no próximo vídeo

1. Criar o **`glossario_pronuncia`** (seção 7) já com IA, design, R$, %, km, CEO, vs — e commitá-lo junto do projeto do canal; toda gravação passa por ele.
2. Rodar um **passe automático com `num2words` (lang='pt_BR')** sobre o roteiro final para moeda, ano, ordinais e percentuais ANTES de gerar qualquer áudio, e conferir a saída por extenso no ouvido uma vez para fixar o padrão do canal.
3. Varrer o roteiro atrás de **siglas e estrangeirismos**, aplicar a tabela de decisão (seção 5) e a grafia fonética (seção 6); o que ficar em dúvida, gerar as duas versões e o Diretor escolhe.
4. Padronizar UMA forma para ano ("dois mil e vinte e seis") e para hora ("sete da noite") e manter igual nos três vídeos da semana — consistência de marca vale mais que variar.
5. No **passe de ouvido** de cada bloco, todo erro de pronúncia novo entra no glossário na hora — assim o vídeo de domingo já nasce sabendo o que o de sexta errou (o glossário é o que transforma 3 vídeos/semana em qualidade crescente, não em pressa).
6. Anexar ao handoff do vídeo a lista de substituições aplicadas, para o Legendador escrever a legenda com a grafia CORRETA (visual = "IA", falado = "i-á") — o texto na tela nunca vira a grafia fonética.
