# Ritmo e prosódia da narração motivacional (varredura 2026-07-17)

> Guia prático do Narrador. Todo número tem fonte ao lado. Opinião pessoal = marcada como "leitura minha".

## 1. Velocidade-alvo (WPM = palavras por minuto)

| Tipo de conteúdo | WPM | Fonte |
|---|---|---|
| Narração (clareza e compreensão) | 120–150 | https://www.voiceovers.com/blog/how-many-words-per-minute-voice-over |
| E-learning (retenção + engajamento) | 140–160 | https://www.voiceovers.com/blog/how-many-words-per-minute-voice-over |
| Audiobook (conforto de escuta) | 150–160 | https://www.voiceovers.com/blog/how-many-words-per-minute-voice-over |
| Comerciais (atenção rápida) | 160–180 | https://www.voiceovers.com/blog/how-many-words-per-minute-voice-over |
| Explicativo médio no YouTube | ~145 | https://lettercounter.org/blog/video-script-word-count/ |
| Documentário / conteúdo calmo | ~120 | https://lettercounter.org/blog/video-script-word-count/ |

- Acima de 160 WPM o conteúdo fica difícil de acompanhar; acima de 150 WPM já se perde tempo de processamento do público e cai a retenção (https://thespeakerlab.com/blog/average-words-per-minute-speaking/, https://www.voiceovers.com/blog/how-many-words-per-minute-voice-over).
- Abaixo de 120 WPM soa arrastado (https://thespeakerlab.com/blog/average-words-per-minute-speaking/).

**Regra do canal (leitura minha):** nosso vídeo motivacional 5–30min vive entre o documentário e o e-learning. Alvo: **média 130–140 WPM**, caindo para ~115–120 nos momentos de revelação/frase-tese e subindo para ~150 nos trechos de tensão/build-up. Isso também dá a conta do roteiro: **um vídeo de 10min ≈ 1.300–1.400 palavras** — número para passar ao Roteirista.

## 2. Pausas: onde, quanto e o perigo do excesso

- Pausa natural de fala: **200–500 ms**; silêncios acima de 1–2 s soam anormais e devem ser cortados na edição (https://silentcut.studio/blog/why-ai-voices-sound-unnatural).
- Pausas devem cair em pontos de respiração reais: fim de frase, momento dramático, transição de tópico. Excesso de pausa deixa a fala picotada e artificial — e muitas tags de pausa podem gerar artefatos de áudio (https://clippie.ai/blog/fix-ai-voiceover-no-pauses).
- A cadência constante é o que entrega o robô: humano acelera e desacelera; IA mantém ritmo estável demais (https://silentcut.studio/blog/why-ai-voices-sound-unnatural).

**Mapa de pausas do canal (leitura minha, calibrar no ouvido):**
- Entre frases do mesmo pensamento: pausa curta (a vírgula/ponto já resolve).
- Entre blocos de ideia (novo parágrafo do roteiro): ~0,8–1,2 s — espaço para o Editor trocar o b-roll.
- Antes da frase-tese ("a revelação"): pausa mais longa + queda de ritmo. Uma só por bloco, senão vira maneirismo.

## 3. Ênfase: menos é mais (o erro nº 1 do TTS)

- Humanos enfatizam só **5–10% das palavras**; a IA sem direção lê tudo com o mesmo peso — e essa uniformidade é o que denuncia a voz artificial (https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/).
- Regra prática: **1–2 palavras importantes por frase**, nunca mais que 2–3; ênfase forte só em ponto crítico ou punchline (https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/).
- Truque que já usamos e a pesquisa confirma: reescrever a frase para a palavra-chave cair no FIM ("o que muda tudo é a CONSISTÊNCIA") — a posição final ganha ênfase natural sem marcação nenhuma (guia VOZ-HUMANIZADA.md + leitura minha).

## 4. Formato do roteiro = direção de prosódia

O jeito mais barato de humanizar não é ferramenta: é FORMATAÇÃO do texto antes do TTS.

- Reescrever como **linhas de respiração**: uma ideia por linha; se a linha não cabe numa respiração, divida; se tem duas ideias, divida (https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/).
- Pontuação é direção: reticências (…) criam pausa e peso; MAIÚSCULA adiciona ênfase; pontuação padrão dá o ritmo base (https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).
- Gerar por partes, nunca o roteiro inteiro de uma vez: blocos de **100–150 palavras** mantêm a "atenção" do modelo e evitam degradação no final (https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/). Atenção ao risco oposto: emendas de segmentos criam micro-gaps — conferir as junções na edição (https://silentcut.studio/blog/why-ai-voices-sound-unnatural).
- Respiração audível importa em conteúdo longo: sem som de respiro, mesmo uma voz bem ritmada começa a soar sintética por volta dos **90 segundos**; inserir respiros curtos e baixos antes de frases longas engana o ouvido na direção certa (https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/).

## 5. Pós-processamento mínimo (para o Editor)

- Detectar e encurtar silêncios acima de 1–2 s deixados pelo TTS (https://silentcut.studio/blog/why-ai-voices-sound-unnatural).
- Vozes de IA costumam ter médios-agudos ardidos/nasais: corte leve de EQ nessa faixa + compressão soft-knee para nivelar volume e tirar a cara de "API crua" (https://echovox.in/blog/how-to-make-ai-voiceovers-sound-human-2026/).
- Nossa regra da casa continua: música ≥18 dB abaixo da voz (regra do Diretor, doutrina do canal).

## 6. O arco de ritmo do vídeo motivacional (leitura minha, sintetizando as fontes)

1. **Gancho (0–30s):** ritmo médio-alto (~145–150 WPM), frases curtas, zero pausa longa — não dar desculpa para sair.
2. **Desenvolvimento:** ritmo médio (130–140), pausas de bloco marcando as trocas de ideia (e de b-roll).
3. **Tensão/build-up:** acelera gradualmente, frases encurtando.
4. **Revelação/tese:** freia forte (~115–120), pausa longa ANTES da frase-chave, palavra-chave no fim da frase.
5. **Fechamento/CTA:** volta ao médio, tom firme e caloroso, sem pressa.

## Como aplicar no próximo vídeo

1. Formatar o roteiro final em linhas de respiração (uma ideia por linha) ANTES de gerar qualquer áudio — pedir ao Roteirista que já entregue assim.
2. Gerar a narração em blocos de 100–150 palavras, um wav por bloco (já é nossa saída padrão), e conferir as emendas contra micro-gaps.
3. Marcar no roteiro no máximo 1–2 palavras de ênfase por frase e reescrever as frases-tese com a palavra-chave no fim.
4. Cronometrar o resultado: se a média sair de 130–140 WPM (fora gancho/revelação), regenerar ajustando rate/velocidade.
5. Passar ao Editor a lista de silêncios >1s para encurtar e pedir o EQ leve + compressão na voz.
6. Testar 1 vídeo com respiros curtos inseridos antes das frases longas e comparar retenção com o anterior.
