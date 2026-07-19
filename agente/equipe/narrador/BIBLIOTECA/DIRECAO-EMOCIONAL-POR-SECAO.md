# Direção emocional por seção + pausa dramática e respiração (ciclo 2 — 2026-07-17)

> Guia prático do Narrador, ciclo 2 (aprofundamento). Todo número tem fonte ao lado. Opinião = "leitura minha".
> O ciclo 1 (RITMO-E-PROSODIA-MOTIVACIONAL.md) deu o ritmo BASE. Este guia dá a CAMADA EMOCIONAL: qual emoção em qual seção, e como dirigir isso em cada motor de voz.

## 1. Por que emoção por seção (o custo da voz chapada)

- Os "matadores de retenção" na narração são exatamente: nenhuma variação de pitch, nenhuma pausa de ênfase e ritmo uniforme independente da intensidade do assunto — dano maior justamente em canais educacionais/documentais como o nosso (https://narrationbox.com/blog/why-viewers-drop-off-after-30-seconds-youtube).
- Voz de IA robótica reduz o engajamento emocional; queda precoce citada na faixa de 28–35% nos primeiros segundos (número observacional do próprio artigo, não estudo controlado — tomar como direção, não como lei) (https://narrationbox.com/blog/why-viewers-drop-off-after-30-seconds-youtube).
- O espectador precisa entender o VALOR do vídeo em até ~20 segundos (https://narrationbox.com/blog/why-viewers-drop-off-after-30-seconds-youtube).
- A queda mais íngreme de retenção acontece entre os segundos 10 e 20, com inflexão por volta do segundo 15 (https://prepublish.ai/guides/first-30-seconds) — ou seja: a emoção do GANCHO decide o vídeo inteiro.
- **Leitura minha:** o ciclo 1 provou que variar VELOCIDADE humaniza. Este ciclo prova que variar EMOÇÃO retém. São duas alavancas diferentes: WPM é o corpo, emoção é a alma. As duas andam juntas por seção.

## 2. O mapa de retenção que sustenta o arco (beat sheet)

Estrutura de 7 batidas para vídeo que segura (https://www.overseeros.com/blog/youtube-retention-architecture-2026):

| Batida | Tempo | Função |
|---|---|---|
| Cold open | 0–5 s | capturar com a tensão central |
| Promessa | 5–15 s | benefício explícito para o espectador |
| Stakes | 15–25 s | por que isso importa |
| Roadmap | 25–30 s | caminho visível do vídeo |
| Corpo (batidas 1–6) | 30%–80% | mini-recompensas a cada 2–3 minutos |
| Clímax | 80–90% | revelação/payoff mais forte |
| CTA | final | próximo passo claro |

- Primeiros 30 s em 3 fases: interrupção de padrão (0–5 s) → promessa específica (5–15 s) → gancho de compromisso (15–30 s) (https://prepublish.ai/guides/first-30-seconds).
- Quedas no meio do vídeo = repetição ou transição confusa; remédio = "frases-ponte" que dizem por que a próxima seção importa (ex.: "agora começa o perigo de verdade…") (https://www.overseeros.com/blog/youtube-retention-architecture-2026).
- Tom por fase: abertura desafia o senso comum (dúvida produtiva) → meio constrói competência com provas → fechamento empodera com ação (https://www.overseeros.com/blog/youtube-retention-architecture-2026).

## 3. A TABELA-MESTRA do canal: emoção × seção (leitura minha, sintetizando as fontes + ciclo 1)

Nosso vídeo motivacional tem 4 emoções-base, uma por tipo de seção:

| Seção | Emoção | WPM (ciclo 1) | Voz | Pausas |
|---|---|---|---|---|
| **GANCHO** | TENSO — urgência contida, quase sussurro de alerta | 145–150 | frases curtas, pergunta direta, zero enfeite | NENHUMA pausa longa |
| **LEI/TESE** ("a lei") | FIRME — autoridade calma, peso em cada palavra | 115–120 | afirmações, sem hedging, palavra-chave no FIM | pausa dramática ANTES da lei |
| **PRÁTICA** | CALMO — professor paciente, próximo | 130–140 | segunda pessoa ("você faz assim"), passos numerados | pausas de bloco normais (~0,8–1,2 s) |
| **CTA** | QUENTE — caloroso, cúmplice, empoderador | 130–135 | narrativo, 1 ação só | curta antes da ação pedida |

- CTA narrativo cria conexão emocional: fechar a HISTÓRIA com a chamada, não colar um anúncio no fim (https://www.capcut.com/pt-br/resource/best-cta-videos).
- Não revelar tudo de uma vez: mini-mistérios/cliffhangers dentro da história seguram atenção — a tensão narrativa é atraso proposital da resolução (https://www.clipshort.co/blog/youtube-video-scripts).
- **Leitura minha:** a transição de emoção NUNCA é brusca — entre TENSO e FIRME existe meia frase de ponte; entre FIRME e CALMO existe uma expiração. Emoção que muda sem ponte soa como troca de locutor.

## 4. Como dirigir cada emoção em cada motor

### 4a. ElevenLabs v3 (Sterling, quando há crédito) — Audio Tags por seção
- Tags = palavras entre colchetes que dirigem a performance: estados emocionais ([excited], [nervous], [calm], [sorrowful]), entrega ([whispers], [shouts]), reações ([sighs], [laughs]), batidas cognitivas ([pauses], [hesitates]) (https://elevenlabs.io/blog/v3-audiotags, https://jonathanmast.com/elevenlabs-v3-audio-tags-user-guide-mastering-emotional-voice-control/).
- Tags podem ser combinadas ou SEQUENCIADAS para arcos emocionais mais ricos (https://jonathanmast.com/elevenlabs-v3-audio-tags-user-guide-mastering-emotional-voice-control/).
- Stability: Creative (mais emoção, pode alucinar) ou Natural (fiel à voz) para as tags responderem; Robust ignora direção (https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).
- A tag tem que ser compatível com a voz: voz gritando + [whispering] não funciona (https://jonathanmast.com/elevenlabs-v3-audio-tags-user-guide-mastering-emotional-voice-control/).
- **Receita do canal (leitura minha):** GANCHO = [serious] (ou nada + pontuação tensa); LEI = [pauses] antes da tese + MAIÚSCULA na palavra-lei; PRÁTICA = [calm]; CTA = tom quente via texto (nada de [excited] forte — nosso canal é prata P&B, não circo). Máximo 1 tag por bloco, como no ciclo 1.

### 4b. Chatterbox Multilingual (custo-zero em teste) — knobs numéricos por seção
- `exaggeration` (default 0.5) controla a intensidade emocional; ~0.7+ para fala dramática (https://github.com/resemble-ai/chatterbox).
- `cfg_weight` (default 0.5): valores menores (~0.3) dão ritmo mais lento e deliberado; exaggeration alto tende a ACELERAR a fala — compensar baixando cfg_weight (https://github.com/resemble-ai/chatterbox). Atenção: há fonte secundária dizendo o oposto (que cfg baixo acelera — https://localaimaster.com/blog/chatterbox-tts-setup-guide); vale o repo oficial + ouvido no teste.
- Ajustar UM parâmetro por vez; exaggeration alto + cfg alto atropela a cadência (https://localaimaster.com/blog/chatterbox-tts-setup-guide).
- **Receita de partida para o teste (leitura minha, calibrar no ouvido):** GANCHO exaggeration 0.65 / cfg 0.4 · LEI 0.55 / 0.3 (lento e firme) · PRÁTICA 0.45 / 0.5 (neutro-calmo) · CTA 0.6 / 0.4 (quente).

### 4c. edge-tts (fallback) — emoção só pelo texto
- Teto conhecido do ciclo 1: só rate/pitch/volume, sem break/emphasis/express-as (https://github.com/rany2/edge-tts).
- **Receita (leitura minha):** gerar POR SEÇÃO com rate diferente — GANCHO `--rate=+12%`, LEI `--rate=-2%`, PRÁTICA `--rate=+8%` (nosso padrão), CTA `--rate=+5%` — e deixar o resto para pontuação e frases curtas. É pouco, mas já quebra a uniformidade que denuncia o robô.

## 5. Pausa dramática e respiração (o toque PT-BR)

### Pausa dramática
- Pausa deliberada que deixa a plateia em suspenso, respirando junto; permite ABSORVER a mensagem e cria ritmo menos ansioso — na tradição teatral brasileira, "o importante não é como se fala, mas como se faz as pausas" (https://www.gazetadopovo.com.br/vida-e-cidadania/colunistas/marleth-silva/a-fabulosa-descoberta-da-pausa-dramatica-8ihmscpl5zoe1tic3z8c2xd8u/).
- O efeito vem da DÚVIDA ("acabou? vem mais?") — por isso ela só funciona rara: virou hábito, virou tique (fonte acima + leitura minha).
- **Regra do canal (consolidando ciclo 1 + 2):** UMA pausa dramática por bloco, sempre ANTES da frase-lei, nunca depois; duração acima da pausa normal mas abaixo do limite de corte de 1–2 s do ciclo 1 (https://silentcut.studio/blog/why-ai-voices-sound-unnatural) — alvo ~0,9–1,4 s, o Editor NÃO corta essa (marcar no handoff como PAUSA-LEI para o corte de silêncio pular ela).

### Respiração aplicada a roteiro de TTS
- Técnica de locução: ler o texto identificando onde se respiraria naturalmente e frasear por respiração — frase que não cabe numa expiração enfraquece no final (https://www.escoladeradio.com.br/post/t%C3%A9cnicas-de-locu%C3%A7%C3%A3o-a-import%C3%A2ncia-da-respira%C3%A7%C3%A3o).
- Recursos vocais que geram sentido: pausa, ênfase, ritmo, cadência, entonação — a pausa é recurso EXPRESSIVO, não só fisiológico (https://revistas.gel.org.br/rg/article/download/120/100/239).
- **Tradução para o nosso fluxo (leitura minha):** o locutor humano respira; o nosso "respiro" é a QUEBRA DE LINHA do roteiro. Linha = uma expiração. O mapa de respiração do locutor vira formatação do texto antes do TTS (linhas de respiração do ciclo 1). E o respiro audível inserido na edição (ciclo 1, a partir de ~90 s) deve cair exatamente nesses pontos — nunca no meio de uma linha.

## 6. Bloco de marcação padrão (entregável para o Roteirista)

**Leitura minha — proposta de notação** no topo de cada seção do roteiro final, para eu gerar sem adivinhar:

```
[SECAO: GANCHO | EMOCAO: TENSO | WPM: 148 | PAUSA-LEI: nao]
[SECAO: LEI    | EMOCAO: FIRME | WPM: 118 | PAUSA-LEI: antes da frase 3]
[SECAO: PRATICA| EMOCAO: CALMO | WPM: 135 | PAUSA-LEI: nao]
[SECAO: CTA    | EMOCAO: QUENTE| WPM: 132 | PAUSA-LEI: nao]
```

Se o Roteirista adotar, a marcação vira contrato entre roteiro→voz→edição (o Editor lê PAUSA-LEI e protege o silêncio). Mudança de REGRA de produção → avisar o Gerente para a DOUTRINA.

## Como aplicar no próximo vídeo

1. Aplicar a TABELA-MESTRA (seção 3) no roteiro do vídeo de quarta 19h: marcar cada seção com o bloco de notação da seção 6 antes de gerar qualquer áudio.
2. Gerar o GANCHO com atenção dupla: tensão + valor claro em até 20 s e as 3 fases dos primeiros 30 s (interrupção→promessa→compromisso) — é onde o vídeo vive ou morre.
3. Inserir UMA pausa dramática de ~0,9–1,4 s antes da frase-lei de cada bloco e marcar PAUSA-LEI no handoff para o Editor não cortar.
4. Pedir ao Roteirista frases-ponte nas trocas de seção ("agora vem a parte que ninguém te conta…") — transição de emoção sem ponte soa troca de locutor.
5. Com a cadência 3/semana, padronizar: domingo 10h e sexta 19h usam a mesma tabela; testar variação de emoção SÓ no vídeo de quarta (1 experimento por semana, o resto na receita provada).
6. Registrar no fim de cada vídeo qual receita emocional foi usada, para cruzar com a retenção real do YouTube Studio quando os dados chegarem (nada de conclusão sem dado).
