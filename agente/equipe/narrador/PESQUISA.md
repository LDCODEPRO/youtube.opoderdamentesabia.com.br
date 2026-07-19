# Mandato de pesquisa — Narrador

## Varredura ciclo 2 — 2026-07-17
**O que estudei:** aprofundamento em cima do ciclo 1. Foco em dois vãos ainda abertos da especialidade "voz sintética de qualidade PT-BR": (1) o **manual de mão** para pôr de pé o teste do Chatterbox Multilingual PT-BR local — requisitos reais (Python 3.11, VRAM, GPU/CPU), instalação (script vs servidor com Web UI), o comando que roda PT-BR, e um protocolo de comparação cego contra o edge-tts atual; (2) o **terceiro pilar da qualidade** que nenhum guia cobria — pronúncia e normalização de texto (números, moeda, datas, siglas, estrangeirismos, homógrafos) ANTES do TTS. 6 buscas + leitura das fontes primárias. Resultado: 2 guias novos (PROVA-DE-CONCEITO-CHATTERBOX-PT-BR.md e PRONUNCIA-PT-BR-E-NORMALIZACAO-DE-TEXTO.md). Obs.: emoção-por-seção e pausa dramática/respiração já haviam sido cobertas em DIRECAO-EMOCIONAL-POR-SECAO.md (não repeti).

**Aprendizados-chave:**
- Chatterbox exige **Python 3.11** (versões novas podem falhar na instalação) e usa **~5–7 GB de VRAM**; recomendado NVIDIA 8–12 GB; roda em CUDA/ROCm/MPS/CPU (CPU = mais lento que tempo real, só lote) — fonte pypi + localaimaster + devnen.
- Instalar é `pip install chatterbox-tts` (pesos baixam no 1º run); para o TESTE de ouvido, o self-host devnen (Web UI + API OpenAI-compatível) é o caminho mais rápido; para PRODUÇÃO, o script.
- PT-BR roda com `ChatterboxMultilingualTTS` + `language_id="pt"`; há finetune dedicado de PT-BR (verificar nome exato no HF); knobs `exaggeration`/`cfg_weight` já mapeados por emoção no ciclo 2.
- edge-tts é serviço ONLINE (sem GPU, precisa internet) e não tem `<say-as>` → a forma oficial de corrigir número/data é **pré-processar em Python e escrever por extenso** — mesmo princípio serve pra todo motor.
- Normalização de texto é a 1ª etapa de qualquer TTS: `num2words` (lang='pt_BR', to='currency'/'year'/'ordinal') resolve número/moeda/data de forma determinística; siglas (palavra vs letra a letra) e homógrafos exigem decisão do canal + glossário versionado.
- **Leitura minha:** confiabilidade é feature — um motor bonito que trava perde para o edge-tts chato que sempre entrega; e o glossário de pronúncia é o que transforma 3 vídeos/semana em qualidade CRESCENTE (nunca erra a mesma palavra duas vezes).

**Fontes:** https://pypi.org/project/chatterbox-tts/ · https://github.com/resemble-ai/chatterbox · https://github.com/devnen/Chatterbox-TTS-Server · https://localaimaster.com/blog/chatterbox-tts-setup-guide · https://replicate.com/resemble-ai/chatterbox-multilingual/readme · https://chatterboxtts.com/docs/multilingual · https://huggingface.co/ResembleAI/chatterbox-turbo · https://github.com/rany2/edge-tts · https://grokipedia.com/page/edge-tts · https://pypi.org/project/num2words/ · https://github.com/savoirfairelinux/num2words · https://beyondwords.io/blog/the-importance-of-text-preprocessing-in-tts/ · https://ar5iv.labs.arxiv.org/html/2005.05144

**Próximo estudo:** rodar de fato a prova de conceito na `conta` (conferir VRAM com `nvidia-smi`, gerar o bloco-padrão de 120 palavras nos 3 motores, teste cego com o Diretor no slot de quarta); construir o `glossario_pronuncia` inicial e automatizar o passe num2words no pipeline; medir tempo de geração vs qualidade para decidir se o Chatterbox vira o custo-zero de produção.

## Varredura 2026-07-17
**O que estudei:** estado da arte de voz IA humanizada — ElevenLabs v3 (Audio Tags, configurações, fim do SSML), limites reais do edge-tts, open source 2026 (Chatterbox Multilingual PT-BR, Kokoro, XTTS/Fish e suas licenças), prosódia/pausas/ênfase e ritmo (WPM) para narração longa. 5 buscas + leitura das fontes primárias. Resultado: 2 guias novos na BIBLIOTECA (RITMO-E-PROSODIA-MOTIVACIONAL.md e TTS-ESTADO-DA-ARTE-2026.md).

**Aprendizados-chave:**
- Narração longa vive em 120–150 WPM; acima de 150–160 a retenção cai — nosso alvo: média 130–140, freando na revelação.
- Humanos enfatizam só 5–10% das palavras: marcar 1–2 palavras por frase, nunca mais que 2–3 — uniformidade é o que denuncia o robô.
- Pausa natural = 200–500 ms; silêncio >1–2 s do TTS deve ser cortado na edição; pausa só em ponto de respiração real.
- Gerar em blocos de 100–150 palavras (evita degradação) e conferir emendas contra micro-gaps; em conteúdo longo, respiros audíveis fazem diferença a partir de ~90 s.
- ElevenLabs v3 aboliu SSML: direção agora é Audio Tags + pontuação (… = pausa, MAIÚSCULA = ênfase); stability em Creative/Natural para as tags responderem.
- edge-tts tem teto duro: só rate/pitch/volume, sem `<break>`/`<emphasis>` — toda prosódia tem que vir do texto.
- NOVO CUSTO-ZERO CANDIDATO: Chatterbox Multilingual (MIT, comercial OK) tem finetune dedicado de PT-BR, clona voz com ~10 s e venceu ElevenLabs em teste cego do próprio vendor (65,3% × 24,5%) — testar na máquina `conta`.
- XTTS v2 e Fish Speech estão FORA para nós: licenças não-comerciais barram canal monetizado.

**Fontes:** https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices · https://elevenlabs.io/blog/v3-audiotags · https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/ · https://silentcut.studio/blog/why-ai-voices-sound-unnatural · https://www.voiceovers.com/blog/how-many-words-per-minute-voice-over · https://github.com/rany2/edge-tts · https://www.resemble.ai/learn/models/chatterbox-multilingual · https://huggingface.co/ResembleAI/chatterbox · https://www.tryspeakeasy.io/blog/open-source-text-to-speech-2026 · https://localaimaster.com/blog/best-local-tts-models

**Próximo estudo:** prova de conceito Chatterbox Multilingual PT-BR local (mesmo bloco vs Sterling vs edge-tts, ouvido do Diretor decide); técnicas de inserção de respiros no áudio final; medir WPM real dos nossos vídeos publicados vs retenção.
SUA ESPECIALIDADE: voz sintética de qualidade.
Pesquisar: novos TTS/vozes PT-BR (qualidade vs custo), técnicas de marcação de ênfase/pausa, o que os canais narrados gigantes usam.
## Como registrar o que aprender
Todo achado vira arquivo na sua BIBLIOTECA/ (um tema por arquivo, com fonte e data).
Achado que muda REGRA da produção → avisar o Gerente para atualizar a DOUTRINA e o painel.
Cadência: revisão da função TODA SEMANA junto da varredura de segunda-feira do Pesquisador.
