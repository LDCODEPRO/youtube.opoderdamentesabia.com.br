# Alinhamento forçado: timestamps por PALAVRA de verdade (ciclo 2 — o motor da sincronia)

> Varredura ciclo 2, 2026-07-17. Fecha o "próximo estudo" que o ciclo 1 deixou em aberto e o item da seção 4 da RECEITA-KARAOKE-ASS-FFMPEG.md (lá os tempos por palavra eram ESTIMADOS pelo tamanho da palavra; aqui aprendemos a MEDIR de verdade). Todo número tem fonte ao lado; opinião marcada como "leitura minha"; nada de estatística inventada.
> NÃO repete a RECEITA (que ensina a QUEIMAR o karaokê): este guia ensina de onde vêm os TEMPOS que alimentam a queima.
> Contexto: vídeo LONGO motivacional PT-BR, 3 vídeos/semana. Detalhe de ouro do nosso caso: **nós já temos o TEXTO exato** (o roteiro do Roteirista). Isso muda tudo — ver seção 1.

## 1. Duas coisas diferentes: transcrever vs ALINHAR (a virada de chave)

- **Transcrição (ASR):** o computador ouve o áudio e ADIVINHA o texto. Erra palavra, erra acento, e os tempos saem ~±500 ms no Whisper puro (https://localaimaster.com/blog/whisperx-guide).
- **Alinhamento forçado (forced alignment):** você dá o áudio **E o texto já conhecido**; o computador só precisa descobrir QUANDO cada palavra é dita. "Toma uma transcrição ortográfica de um áudio e gera uma versão alinhada no tempo, usando um dicionário de pronúncia para achar os fones de cada palavra" (https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/index.html).
- **Leitura minha — a regra da casa daqui pra frente:** como temos o roteiro, é PROIBIDO re-transcrever para legendar. Re-transcrever reintroduz erro de palavra e de acento que o Roteirista já tinha resolvido. Nós ALINHAMOS. O texto é sagrado; só os tempos são calculados.

## 2. Quem alinha melhor — os números (com fonte)

Estudo acadêmico comparando alinhadores em fala em inglês (TIMIT/Buckeye), MFA vs WhisperX vs MMS — fonte de todos os números deste bloco: https://arxiv.org/html/2406.19363v1

Acerto do início/fim da PALAVRA dentro da tolerância (TIMIT, nível palavra):

| Tolerância | MFA | WhisperX | MMS |
|---|---|---|---|
| ≤25 ms | 72,8% | 52,7% | 43,5% |
| ≤50 ms | **89,4%** | 82,4% | 75,7% |
| ≤100 ms | 97,4% | 94,2% | 94,7% |

Erro de fronteira da palavra (quanto o tempo "escorrega", em ms — menor é melhor):

| Ferramenta | Média | Mediana |
|---|---|---|
| **MFA** | 21,9 ms | **12,5 ms** |
| WhisperX | 34,3 ms | 23,5 ms |
| MMS | 68,5 ms | 29,3 ms |

- Em fala conversacional longa (Buckeye), a mediana do MFA se manteve em **12,9 ms** contra 23,7 ms do WhisperX (mesma fonte). Ou seja: quanto mais longo/solto o áudio, mais o MFA abre vantagem — e o nosso é vídeo LONGO.
- Por que o MFA ganha: usa arquitetura GMM-HMM com resolução de quadro de **10 ms**; WhisperX/MMS são transformers ponta-a-ponta que operam em trechos maiores, com resolução temporal mais grosseira (mesma fonte).
- Um segundo estudo, focado no estado da arte em 2026, reporta erro médio de fronteira **abaixo de 15 ms** para o MFA 3.0 em vários idiomas (https://arxiv.org/abs/2606.18466 — li a listagem/resumo, não o texto completo; tratar como direção, não como número cravado).
- **Honestidade de pesquisa:** a tabela acima foi medida SÓ em inglês; o próprio paper marca a falta de testes multilíngues como lacuna (https://arxiv.org/html/2406.19363v1). Não existe garantia publicada do mesmo desempenho em PT-BR. Leitura minha: a ordem de mérito (MFA > WhisperX > MMS) deve se manter, mas o número exato pode mudar em português.

## 3. As 4 ferramentas — qual usar em cada caso

### aeneas — o encaixe natural do nosso pipeline (leitura minha)
- Não usa ASR: sintetiza a fala do texto com TTS (eSpeak) e casa com o áudio real via MFCC + DTW (dynamic time warping) (https://github.com/readbeyond/aeneas).
- **PT confirmado:** "Confirmed working on 38 languages", incluindo POR (mesma fonte). Já foi usado para alinhar os corpora ALIP e TEDx em português (https://arxiv.org/pdf/2406.19363v1 cita o uso; ver também a prática em corpora BP).
- Granularidade flexível: palavra, subfrase, frase, parágrafo — e alinhamento multinível (mesma fonte). É exatamente o que precisamos: dá pra pedir **1 palavra por vez**.
- Sai direto em SRT/VTT/JSON e mais 12 formatos (mesma fonte) — não precisa de conversor de TextGrid.
- Instala leve, sem GPU: `pip install numpy` e depois `pip install aeneas`; precisa de ffmpeg + eSpeak no sistema (mesma fonte).
- **Leitura minha:** para o nosso caso (texto conhecido + PT + sem GPU + saída SRT direta), aeneas é o caminho padrão. Precisão menor que MFA, mas suficiente para ênfase pontual, e MUITO mais simples de rodar 3x/semana.

### Montreal Forced Aligner (MFA) — quando quiser a máxima precisão
- Campeão de precisão (seção 2). Modelos e dicionários PT-BR prontos para baixar: `mfa model download acoustic portuguese_brazil_mfa` e `mfa model download dictionary portuguese_brazil_mfa` (padrão de nome `<idioma>_mfa`; confirmar o sufixo exato com `mfa model download acoustic` sem argumento, que lista os disponíveis — https://github.com/MontrealCorpusTools/mfa-models e https://montreal-forced-aligner.readthedocs.io/en/stable/user_guide/models/index.html).
- Custo: instala por conda, é mais pesado e sai em **TextGrid** (precisa converter pra SRT). Leitura minha: reservar para quando um vídeo-âncora (ex.: estreia de domingo) pedir sincronia cirúrgica, não para o dia a dia.

### WhisperX — quando NÃO temos o texto
- Word-level via alinhamento wav2vec2 (https://github.com/m-bain/whisperx). Instala com `pip install whisperx`; gera SRT com a palavra corrente destacada via `whisperx audio.wav --highlight_words True` (mesma fonte).
- PORÉM re-transcreve (adivinha o texto) — e PT não está na lista de modelos padrão `{en, fr, de, es, it}`, só via Hugging Face (mesma fonte). Leitura minha: é plano B, para quando alguém entregar áudio SEM roteiro. Tendo roteiro, aeneas/MFA ganham.

### stable-ts — alternativa Whisper com função `align`
- `pip install stable-ts`; tem `stable_whisper.align(audio, texto)` que aceita o texto conhecido (é alinhamento, não só transcrição) e devolve tempos por palavra (https://github.com/jianfch/stable-ts). Precisão fica entre Whisper puro e WhisperX conforme a discussão da própria comunidade (https://github.com/jianfch/stable-ts/discussions/376). Leitura minha: bom para quem já tem Whisper montado e quer palavra-a-palavra sem instalar aeneas.

**Resumo da decisão (leitura minha):** temos roteiro → **aeneas** no dia a dia; vídeo-âncora que exige perfeição → **MFA**; sem roteiro → **WhisperX/stable-ts**.

## 4. Receita aeneas: do áudio + roteiro aos tempos por palavra

O truque para tempo por PALAVRA no aeneas: entregar o texto com **uma palavra por linha** — cada linha vira um "fragmento" alinhado.

### Passo A — quebrar o roteiro em uma palavra por linha
```python
# quebra_palavras.py  -> python quebra_palavras.py roteiro.txt palavras.txt
import sys, re
txt = open(sys.argv[1], encoding="utf-8").read()
palavras = re.findall(r"\S+", txt)                 # mantém pontuação colada à palavra
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(palavras) + "\n")
```

### Passo B — alinhar (sem GPU, PT-BR)
```
python -m aeneas.tools.execute_task ^
  narracao.wav palavras.txt ^
  "task_language=por|is_text_type=plain|os_task_file_format=json" ^
  tempos.json
```
(`task_language=por` = português; `is_text_type=plain` = uma linha = um fragmento; saída JSON com begin/end de CADA palavra. Sintaxe do execute_task: https://github.com/readbeyond/aeneas)

### Passo C — transformar os tempos reais nos `\k` do ASS (substitui a ESTIMATIVA da RECEITA)
O `tempos.json` do aeneas traz `fragments` com `begin`/`end` por palavra. Em vez de distribuir `\k` por tamanho da palavra (jeito antigo, RECEITA seção 4), usamos a duração MEDIDA:
```python
# tempos2k.py -> gera os \k em centissegundos a partir do JSON do aeneas
import json, sys
frg = json.load(open(sys.argv[1], encoding="utf-8"))["fragments"]
for f in frg:
    ini = float(f["begin"]); fim = float(f["end"])
    k = max(int(round((fim - ini) * 100)), 1)      # centissegundos, mínimo 1
    print(f'{{\\k{k}}}{f["lines"][0]}', end=" ")
```
A partir daqui, montar o Dialogue e queimar seguem a RECEITA-KARAOKE-ASS-FFMPEG.md (não repito aqui). O ganho: o "acender" cai EXATAMENTE na voz, não numa média.

### Passo D — aplicar o adianto de 100 ms (regra do ciclo 2)
O ciclo 2 (KARAOKE-VS-BLOCO-DECISAO-POR-DADOS.md, seção 2) manda a legenda entrar 100–200 ms antes da voz e a palavra acender 50–100 ms antes (https://www.opus.pro/blog/best-caption-presets-styles-boost-retention). Com tempo REAL em mãos, o adianto vira uma subtração exata: tirar 0,10 s de cada `begin` antes de gerar o `\k`. Antes (com estimativa) isso era chute; agora é preciso.

## 5. Pegadinhas de PT-BR no alinhamento (leitura minha, do que li)

- **Números e siglas:** "1º", "3km", "R$", "Dr." confundem tanto o TTS do aeneas quanto o dicionário do MFA. Escrever o roteiro por extenso onde a fala é por extenso ("primeiro", "três quilômetros") reduz erro de fronteira — casa com a regra de números do TTSG pt-BR já anotada em ACESSIBILIDADE-CONTRASTE-NORMA-PTBR.md.
- **Áudio limpo alinha melhor:** trilha/efeito por cima do MFCC piora o DTW. Se der, alinhar pela faixa SÓ do Narrador (stem de voz), depois casar com a mixagem — leitura minha.
- **Confiar, mas conferir:** nenhum alinhador acerta 100%. Rodar SEMPRE o frame de conferência da RECEITA (Passo D de lá) num trecho de fala rápida antes do render longo.

## Como aplicar no próximo vídeo

1. Instalar aeneas (`pip install numpy && pip install aeneas`, + ffmpeg/eSpeak) e rodar o fluxo A→B→C num trecho de 30 s do gancho do vídeo de quarta 19h, comparando o "acender" com a versão por estimativa da RECEITA — se a diferença for visível, adotar o alinhado como padrão.
2. Pedir ao Roteirista/Narrador o roteiro em .txt e, se possível, o stem de voz separado — os dois insumos derrubam o erro de fronteira antes de qualquer ajuste.
3. Padronizar o adianto exato de 0,10 s no `begin` (Passo D) dentro do script, para o timing de karaokê parar de ser chute.
4. Reservar o MFA (com `portuguese_brazil_mfa`) só para o vídeo de estreia de domingo 10h, onde a sincronia perfeita paga o custo de instalação; quarta e sexta seguem no aeneas para caber na cadência.
5. Levar ao Gerente uma nota curta para a LEGENDA-DA-MARCA: "tempos de palavra vêm de alinhamento forçado (aeneas/MFA), nunca de re-transcrição; texto do roteiro é intocável".
6. Guardar `quebra_palavras.py` e `tempos2k.py` na pasta de ferramentas da equipe, ao lado do `srt2ass_karaoke.py` da RECEITA (pedir ao Gerente o local oficial).
