# TTS estado da arte 2026 — ferramentas, tags e o plano do canal (varredura 2026-07-17)

> Guia prático do Narrador. Todo número tem fonte ao lado. Opinião pessoal = marcada como "leitura minha".

## 1. Panorama: quem manda em PT-BR hoje

- **ElevenLabs** segue líder em naturalidade/emoção em PT, com entonação e nuance acima dos concorrentes em comparações de qualidade (https://siteladom.com.br/ferramentas-de-text-to-speech-com-ia/, https://blog.pareto.io/en/elevenlabs-alternatives/). É a nossa voz Sterling via Higgsfield — quando há crédito.
- **A novidade de 2026: o open source alcançou.** Em estudo cego da própria Resemble AI, **65,3% dos ouvintes preferiram o Chatterbox** contra 24,5% que preferiram ElevenLabs (fonte é o vendor — tomar com sal; https://findskill.ai/blog/best-open-source-tts-2026/, https://www.resemble.ai/learn/models/chatterbox).
- Alternativas comerciais (Murf, Play.ht, Speechify, Google TTS) atendem nichos corporativos/podcast/escala — nenhuma bate ElevenLabs em emoção para narração (https://siteladom.com.br/ferramentas-de-text-to-speech-com-ia/).

## 2. ElevenLabs v3: Audio Tags (o que mudou na direção de voz)

- Audio Tags = palavras entre colchetes no próprio texto que dirigem a performance: emoção (`[sad]`, `[excited]`, `[happily]`), entrega (`[whispers]`, `[shouts]`), reações humanas (`[laughs]`, `[sighs]`, `[clears throat]`) (https://elevenlabs.io/blog/v3-audiotags).
- **v3 NÃO suporta SSML** (`<break>` etc.). Pausa e ritmo no v3 = tags + pontuação + estrutura do texto: reticências (…) dão pausa e peso, MAIÚSCULA dá ênfase (https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).
- Nos modelos v2 ainda vale `<break time="1.0s" />` com máximo de 3 s (https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).
- Configuração v3: o slider de stability é o principal — **Creative** (mais expressivo, pode alucinar), **Natural** (fiel à voz base), **Robust** (estável, responde pouco às tags). Para tags funcionarem: Creative ou Natural (https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).
- A eficácia das tags DEPENDE da voz escolhida e do material de treino dela; clones profissionais (PVC) ainda não estão otimizados para v3 (https://elevenlabs.io/blog/v3-audiotags, https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).
- Pronúncia: v3 aceita IPA inline em 70+ idiomas com 80–90% de consistência; parâmetro de velocidade vai de 0.7 a 1.2 (padrão 1.0) (https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).
- **Leitura minha:** para nosso tom motivacional, as tags úteis são poucas e sóbrias — algo como [pause], tom sério/caloroso e um raro [sighs] em história pessoal. Tag demais vira teatro; o v3 recompensa quem marca pouco e certo.

## 3. edge-tts (nosso custo zero atual): teto conhecido

- O serviço do Edge só aceita SSML mínimo: **1 tag `<voice>` com 1 `<prosody>`** — apenas rate, pitch e volume. **`<break>`, `<emphasis>`, `<say-as>` e `<mstts:express-as>` NÃO funcionam** (https://github.com/rany2/edge-tts, https://grokipedia.com/page/edge-tts).
- Ou seja: no edge-tts a ÚNICA direção de prosódia é o texto em si — pontuação, frases curtas, blocos separados. Confirma nossa prática do institucional (pt-BR-AntonioNeural, rate +8%).
- **Leitura minha:** edge-tts continua ok para rascunho e institucional, mas é teto baixo para vídeo monetizável — sem pausa dirigida, sem ênfase, sem emoção.

## 4. Open source que interessa ao canal (roda na nossa máquina, custo zero)

| Modelo | Licença | PT-BR? | Destaque | Fonte |
|---|---|---|---|---|
| **Chatterbox Multilingual (Resemble)** | MIT (comercial OK) | **SIM — finetune dedicado de PT-BR** | 0.5B params; 23 idiomas; clona voz com ~10 s de referência; controle de "emotion exaggeration"; preferido sobre ElevenLabs em teste cego do vendor | https://huggingface.co/ResembleAI/chatterbox, https://www.resemble.ai/learn/models/chatterbox-multilingual |
| Kokoro-82M | Apache 2.0 | sim (voz preset) | levíssimo: roda em 2–3 GB VRAM ou até CPU | https://localaimaster.com/blog/best-local-tts-models |
| XTTS v2 | CPML (NÃO comercial) | sim | padrão-ouro de clonagem zero-shot (6 s de referência, 17 idiomas), mas licença barra uso monetizado | https://www.tryspeakeasy.io/blog/open-source-text-to-speech-2026 |
| Fish Speech | CC-BY-NC-SA (NÃO comercial) | sim | boa qualidade, licença barra canal monetizado | https://www.tryspeakeasy.io/blog/open-source-text-to-speech-2026 |

- Atenção: todo áudio do Chatterbox sai com watermark neural imperceptível (Perth) com ~100% de detecção — não afeta o ouvido, mas é rastreável como IA (https://www.resemble.ai/learn/models/chatterbox-multilingual).
- **Leitura minha:** como o canal é monetizado, XTTS v2 e Fish Speech estão FORA (licença). O caminho é: Sterling/ElevenLabs quando houver crédito → **testar Chatterbox Multilingual PT-BR como novo custo-zero de qualidade** → edge-tts só como fallback de emergência. Se o Chatterbox local aprovar no ouvido do Diretor, muda a REGRA de produção (avisar o Gerente).

## 5. Checklist anti-robô (síntese das fontes + casa)

1. Voz certa = 60% do caminho: narrador calmo, confiante, ritmo médio (https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/).
2. Texto formatado em linhas de respiração, blocos de 100–150 palavras (https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/).
3. Ênfase em 1–2 palavras por frase, nunca mais que 2–3 (https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/).
4. Pausas só em ponto de respiração real; curtas e consistentes; excesso = artefato (https://clippie.ai/blog/fix-ai-voiceover-no-pauses).
5. Pós: encurtar silêncios >1–2 s, EQ leve nos médios-agudos, compressão soft-knee (https://silentcut.studio/blog/why-ai-voices-sound-unnatural, https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/).
6. Ouvir SEMPRE antes de aprovar — tag e configuração se comportam diferente por voz (https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).

## Como aplicar no próximo vídeo

1. Checar balance da Higgsfield; com crédito, gerar com Sterling usando pontuação como direção (reticências para pausa de peso, MAIÚSCULA só na palavra-tese de cada bloco).
2. Se usar v3/tags: manter stability em Natural, no máximo 1 tag sóbria por bloco, e ouvir bloco a bloco antes de aprovar.
3. Montar prova de conceito do Chatterbox Multilingual PT-BR na máquina `conta` (MIT, custo zero): gerar o MESMO bloco de teste em Chatterbox vs edge-tts vs Sterling e levar ao ouvido do Diretor.
4. Se o Chatterbox aprovar, avisar o Gerente: muda a regra de produção do custo-zero (edge-tts vira só emergência) e atualizar DOUTRINA + painel.
5. Registrar no handoff dos blocos (para Legendador/Editor) os tempos + lista de silêncios >1 s para corte.
