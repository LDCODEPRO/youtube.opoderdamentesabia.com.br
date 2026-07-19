# Prova de conceito — Chatterbox Multilingual PT-BR local vs edge-tts (ciclo 2 — 2026-07-17)

> Guia prático do Narrador, ciclo 2 (aprofundamento). Todo número tem fonte (URL) ao lado. Opinião = "leitura minha". NUNCA estatística inventada.
> Os guias TTS-ESTADO-DA-ARTE-2026.md (ciclo 1) e DIRECAO-EMOCIONAL-POR-SECAO.md (ciclo 2) já DECIDIRAM que o Chatterbox é o candidato a custo-zero de qualidade e deram os knobs por emoção. Aqui é o **manual de mão** para pôr de pé o teste na máquina `conta`: requisitos, instalação, comando que roda, e o protocolo de comparação contra o edge-tts atual. Sem isto, a decisão de trocar o motor fica no "achismo".

## 1. O que estamos comparando (as duas naturezas são MUITO diferentes)

| Eixo | **edge-tts (atual)** | **Chatterbox Multilingual (candidato)** |
|---|---|---|
| Onde roda | Serviço ONLINE da Microsoft Edge — precisa de internet, sem GPU, sem API key, grátis (https://github.com/rany2/edge-tts, https://pypi.org/project/edge-tts/) | LOCAL na máquina — roda offline, usa GPU/CPU da `conta` (https://github.com/resemble-ai/chatterbox) |
| Licença | serviço MS (uso de fato, sem SLA) | **MIT — comercial OK** (canal monetizado liberado) (https://github.com/resemble-ai/chatterbox) |
| Direção de voz | só `--rate`/`--volume`/`--pitch`; sem break/emphasis/say-as/express-as (https://github.com/rany2/edge-tts) | `exaggeration`, `cfg_weight`, `temperature`, clonagem por áudio de referência (https://github.com/resemble-ai/chatterbox) |
| Clonagem de voz | não | sim, ~10 s de referência (ciclo 1, https://www.resemble.ai/learn/models/chatterbox-multilingual) |
| Custo real | zero, mas teto baixo | zero em API, **custo em VRAM/tempo de máquina** |
| Risco | depende de serviço externo que pode mudar/cair | depende do nosso hardware aguentar |

- **Leitura minha:** não é "qual é melhor no absoluto" — é "o ganho de qualidade do Chatterbox paga o custo de GPU e a complexidade de rodar local, para 3 vídeos/semana?". O teste existe para responder ISSO com o ouvido do Diretor, não para eleger campeão em papel.

## 2. Requisitos para rodar o Chatterbox na `conta`

- **Python 3.11.** O pacote foi desenvolvido/testado em Python 3.11 (Debian 11) com dependências pinadas; versões mais novas de Python podem falhar na instalação (https://pypi.org/project/chatterbox-tts/, https://github.com/resemble-ai/chatterbox). → **Usar venv/conda com 3.11, não o Python do sistema.**
- **GPU (recomendado):** NVIDIA com CUDA; o modelo 0.5B usa **~5–7 GB de VRAM**; recomendação prática de **8–12 GB de VRAM** para folga (https://localaimaster.com/blog/chatterbox-tts-setup-guide, https://github.com/devnen/Chatterbox-TTS-Server).
- **Também roda** em AMD (ROCm), Apple Silicon (MPS) e **CPU como fallback** (https://github.com/devnen/Chatterbox-TTS-Server, https://localaimaster.com/blog/chatterbox-tts-setup-guide).
- **CPU-only:** funciona, porém **mais lento que tempo real** — serve para lote noturno, não para iteração ao vivo (https://localaimaster.com/blog/chatterbox-tts-setup-guide).
- **Velocidade com GPU:** modelo original 0.5B tem latência sub-200 ms, tempo real em GPU moderna; variante **Turbo (350M) ~75 ms, ~6× mais rápido que tempo real** (https://localaimaster.com/blog/chatterbox-tts-setup-guide, https://huggingface.co/ResembleAI/chatterbox-turbo).
- Os pesos baixam sozinhos do Hugging Face no primeiro uso (https://localaimaster.com/blog/chatterbox-tts-setup-guide) → primeira execução exige internet e uns minutos.

> **Antes de instalar:** conferir a VRAM real da `conta` (`nvidia-smi`). Se não houver GPU NVIDIA com ~8 GB livres, o caminho realista é (a) CPU em lote noturno, ou (b) rodar na VPS/outra máquina da federação — combinar com o Gerente. Não gastar dinheiro em GPU sem ordem (regra da casa: só avisar antes se gasta $/muda acesso/irreversível).

## 3. Instalação — caminho A (script, mais controle)

```bash
# 1. Ambiente isolado com Python 3.11
python3.11 -m venv chatterbox-env
# Linux/Mac:
source chatterbox-env/bin/activate
# Windows (a nossa conta):
# chatterbox-env\Scripts\activate

# 2. Instalar o pacote (pesos baixam no 1º run)
pip install chatterbox-tts
```

Fonte da receita: https://pypi.org/project/chatterbox-tts/ , https://localaimaster.com/blog/chatterbox-tts-setup-guide

Alternativa a partir do fonte (se quiser a versão mais nova do repo):
```bash
git clone https://github.com/resemble-ai/chatterbox.git
cd chatterbox
pip install -e .
```
Fonte: https://github.com/resemble-ai/chatterbox

## 4. Instalação — caminho B (servidor com Web UI, mais fácil de ouvir/testar)

Para o **teste de ouvido** (gerar o mesmo bloco várias vezes, mexer nos knobs sem escrever código), o self-host **devnen/Chatterbox-TTS-Server** entrega Web UI + API compatível com OpenAI + vozes predefinidas + clonagem + processamento de texto longo (escala audiobook); roda em NVIDIA (CUDA), AMD (ROCm) e CPU (https://github.com/devnen/Chatterbox-TTS-Server).

- **Leitura minha:** para a PROVA DE CONCEITO, o caminho B é melhor — o Diretor abre a Web UI, cola o bloco, escuta, mexe no exaggeration e compara na hora. Para a PRODUÇÃO integrada ao pipeline (roteiro→voz→edição), o caminho A (script) é o que a gente automatiza depois. Começar por B, migrar para A se aprovar.

## 5. O comando que gera PT-BR (receita mínima que roda)

```python
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

# device: "cuda" (NVIDIA), "mps" (Apple), ou "cpu" (fallback)
model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")

texto = "A disciplina começa onde a motivação termina."
wav = model.generate(texto, language_id="pt")     # PT = "pt"
ta.save("saida_pt.wav", wav, model.sr)             # model.sr = taxa de amostragem do modelo
```
Fonte do padrão de código: https://replicate.com/resemble-ai/chatterbox-multilingual/readme , https://chatterboxtts.com/docs/multilingual

### Com clonagem de voz + knobs por emoção (casa com DIRECAO-EMOCIONAL-POR-SECAO.md)
```python
wav = model.generate(
    text="A disciplina começa onde a motivação termina.",
    language_id="pt",
    audio_prompt_path="referencia_10s.wav",  # ~10 s de voz de referência
    exaggeration=0.5,        # 0.25–2.0 · intensidade emocional (0.7+ = dramático)
    cfg_weight=0.5,          # 0.2–1.0 · ritmo (mais baixo ~0.3 = mais lento/deliberado)
    temperature=0.8,         # aleatoriedade da amostragem
    repetition_penalty=2.0
)
```
Fonte dos parâmetros e faixas: https://replicate.com/resemble-ai/chatterbox-multilingual/readme , https://github.com/resemble-ai/chatterbox

- Default `exaggeration=0.5 / cfg_weight=0.5` funciona bem para a maioria dos casos (https://github.com/resemble-ai/chatterbox).
- Referência com fala RÁPIDA → baixar `cfg_weight` para ~0.3 melhora o ritmo (https://github.com/resemble-ai/chatterbox).
- **Existe modelo dedicado de PT-BR** (finetune reportado como `ResembleAI/Chatterbox-Multilingual-pt-br` no self-host) — **verificar o nome exato no Hugging Face antes de usar** e comparar contra o multilíngue genérico com `language_id="pt"` (https://github.com/devnen/Chatterbox-TTS-Server; ciclo 1: https://huggingface.co/ResembleAI/chatterbox). *Leitura minha:* incluir os DOIS no teste de ouvido — o finetune tende a ganhar em sotaque BR, mas quem decide é o ouvido do Diretor.
- Todo áudio sai com watermark neural Perth (imperceptível, rastreável como IA) — não afeta o ouvido (ciclo 1: https://www.resemble.ai/learn/models/chatterbox-multilingual).

## 6. Knobs de partida por seção (herdados do ciclo 2, para não recalibrar do zero)

Da DIRECAO-EMOCIONAL-POR-SECAO.md (calibrar no ouvido — atenção: fontes divergem sobre a direção do `cfg_weight`, então o ouvido manda):

| Seção | exaggeration | cfg_weight | Intenção |
|---|---|---|---|
| GANCHO | 0.65 | 0.4 | tenso, urgência contida |
| LEI/TESE | 0.55 | 0.3 | firme, lento e pesado |
| PRÁTICA | 0.45 | 0.5 | calmo, professor |
| CTA | 0.60 | 0.4 | quente, cúmplice |

Ajustar **um parâmetro por vez**; exaggeration alto + cfg alto atropela a cadência (https://localaimaster.com/blog/chatterbox-tts-setup-guide).

## 7. Protocolo de comparação (o teste de verdade, replicável)

**Objetivo:** decisão do Diretor no cego, sem viés de "o novo é melhor".

1. **Bloco-padrão único** de ~120 palavras contendo as 4 emoções do canal (1 frase de gancho tenso, 1 lei firme, 1 trecho de prática, 1 CTA quente). Mesmo texto para todos os motores.
2. Gerar **3 versões**:
   - A) **edge-tts** `pt-BR-AntonioNeural --rate=+8%` (nosso padrão provado — ciclo 1 / VOZ-HUMANIZADA.md).
   - B) **Chatterbox multilíngue** `language_id="pt"` com os knobs da seção 6.
   - C) **Chatterbox finetune PT-BR** (se o nome do modelo confirmar) com os mesmos knobs.
   - (D opcional) **Sterling/ElevenLabs** se houver crédito na Higgsfield — o teto de qualidade de referência.
3. **Normalizar volume** das 3 (mesmo LUFS aproximado) para o teste não premiar a mais alta.
4. **Nomear os arquivos sem revelar o motor** (v1/v2/v3 embaralhados) → teste cego real.
5. Medir por versão: **WPM real** (contra o alvo 130–140 do ciclo 1), naturalidade das pausas, sotaque BR, artefatos/erros de pronúncia (nomes, números, siglas — ver o guia PRONUNCIA-PT-BR-E-NORMALIZACAO-DE-TEXTO.md), e **tempo de geração** do bloco.
6. Registrar: qual venceu, em quê, e o **custo** (segundos de geração + VRAM). Decisão vira regra só com aprovação do Diretor.

- **Leitura minha:** o critério de aprovação não é "empatou com o Sterling", é "**é bom o bastante para o vídeo monetizado E é confiável para rodar 3×/semana sem babá**". Um motor lindo que trava em produção perde para o edge-tts chato que sempre entrega. Confiabilidade é feature.

## 8. Se aprovar → o que muda na produção (avisar o Gerente)

- Chatterbox vira o **custo-zero de qualidade**; edge-tts recua para **fallback de emergência** (quando faltar GPU/internet).
- Atualizar DOUTRINA + painel do canal (mudança de REGRA de produção — não é decisão minha sozinho).
- Padronizar no pipeline: um bloco de 100–150 palavras por chamada (ciclo 1), WAV por bloco + tempos no handoff para Legendador/Editor, watermark Perth anotado no registro do vídeo.

## Como aplicar no próximo vídeo

1. **Antes de qualquer coisa:** rodar `nvidia-smi` na `conta` e anotar a VRAM livre — decide se o teste roda em GPU (iteração ao vivo) ou só em CPU/lote noturno; se faltar GPU, levar ao Gerente a opção de rodar na federação.
2. Instalar pelo **caminho B (devnen server, Web UI)** num venv Python 3.11 e gerar o **bloco-padrão de 120 palavras** nos 3 motores (edge-tts / Chatterbox multi / Chatterbox PT-BR).
3. Fazer o **teste cego** da seção 7 com o Diretor no vídeo de **quarta 19h** (o slot-experimento do canal), mantendo domingo 10h e sexta 19h na receita provada (edge-tts) até haver veredito.
4. Registrar no handoff do vídeo: motor usado, knobs por seção, WPM real, tempo de geração e erros de pronúncia — para cruzar com a retenção do YouTube Studio quando os dados chegarem (nada de conclusão sem dado).
5. Se o Diretor aprovar o Chatterbox, avisar o Gerente para trocar a REGRA de custo-zero na DOUTRINA e planejar a migração do caminho B (teste) para o caminho A (script no pipeline), começando pelo vídeo de menor risco.
