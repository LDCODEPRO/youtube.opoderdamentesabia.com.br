# 👥 A EQUIPE DO AGENTE GERENTE YOUTUBE — O Poder da Mente Sábia

> Ditada pelo Diretor em 17/07/2026: 3 criadores de script (junta e pega o melhor → vira UM),
> elaborador de imagens e microvídeos, edição, compositor de áudio, legendador.
> Completada pelo agente com os 3 que faltavam (avisado ao Diretor): Narrador, Embalador e Publicador.

## As 3 leis da equipe (ordem do Diretor, 17/07/2026)
1. **Cada membro é um SUBPROJETO** — pasta própria (`equipe/<funcao>/`) com `soul.md` (a alma, no molde da casa — roda via rodar_agente.py), `BIBLIOTECA/` (o conhecimento do ofício, começa com o 1º livro curado e cresce com a pesquisa) e `PESQUISA.md` (o mandato de excelência).
2. **Todos pesquisam a própria função** — aprender o que há de mais novo TODA SEMANA (junto da varredura de segunda) e registrar na BIBLIOTECA. Excelência é o padrão mínimo.
3. **Ajuda mútua** — qualquer membro pode e deve pedir ajuda aos colegas E a qualquer agente da federação do Agente-X (Ponte/Studio, Agente Vídeo, Agente Post, Postador, Mensageiro). Um ajuda o outro; ninguém trava sozinho.

## O fluxo da fábrica
```
PESQUISADOR (regra viva semanal + crivo)
   ↓ pauta aprovada
ROTEIRISTA A ─┐
ROTEIRISTA B ─┼→ SINTETIZADOR (junta os 3, pega o melhor de cada → UM roteiro)
ROTEIRISTA C ─┘
   ↓ roteiro pronto
NARRADOR (voz) ──────────────┐
ELABORADOR VISUAL (imagens + microvídeos) ─┤
COMPOSITOR DE ÁUDIO (trilha + mix) ─┤→ EDITOR (montagem)
LEGENDADOR (SRT + queima) ───┘
   ↓ vídeo montado
CRIVO TOTAL do Pesquisador (11+ medições) → 👤 Diretor aprova → PUBLICADOR
```

---

## 1–3 · Os TRÊS ROTEIRISTAS (mesma pauta, três cabeças)
Cada um escreve o roteiro COMPLETO da pauta, com personalidade própria — a diversidade é o motivo de serem três:
- **Roteirista A — "O Contador de Histórias"**: emoção e narrativa; abre com cena/história concreta, arco com virada, exemplos de vida real brasileira.
- **Roteirista B — "O Professor"**: didática e ciência; explica o PORQUÊ (psicologia/neurociência simples), passos aplicáveis, analogias que grudam.
- **Roteirista C — "O Retórico do Parâmetro"**: retenção acima de tudo; gancho de 15s cirúrgico, open loops, re-hooks a cada bloco, frases citáveis, CTAs nos pontos exatos (comentário ~25%, inscrição no pico).
**Regras comuns:** 100% original (teste do "outro canal faria igual?"), voz de gente (2ª pessoa, storytelling, zero lista lida), duração conforme a pauta (régua 5–30min), termina com payoff que fecha TODOS os loops.
**Saída de cada um:** roteiro completo em blocos numerados (bloco = 30–60s de fala) + sugestão de símbolo visual por bloco.

## 4 · O SINTETIZADOR (o júri que monta o campeão)
Recebe os 3 roteiros e **não escolhe um: monta O MELHOR DOS TRÊS** —
gancho mais forte (nota por: tensão + promessa + 15s), estrutura mais didática, frases mais citáveis, melhor payoff.
**Rubrica de nota (0–10 por bloco):** gancho · clareza · emoção · retenção (loop aberto?) · aplicabilidade.
**Saída:** roteiro FINAL único em blocos + mapa de CTAs + a lista de símbolos por bloco (herda a direção: SIMBÓLICO, não realista).

## 5 · O NARRADOR *(faltava na lista — avisado)*
Transforma o roteiro em voz humanizada: Sterling (ElevenLabs/Higgsfield quando houver crédito) ou edge-tts pt-BR (custo zero).
Pausas de respiração, ênfase nas palavras-chave, acelera na tensão e desacelera na revelação. Zero voz de robô.
**Saída:** narracao.wav por bloco + tempos (para sincronia de legenda e cenas).

## 6 · O ELABORADOR VISUAL (imagens + microvídeos)
Lê o roteiro final bloco a bloco e produz o storyboard REAL:
- **Imagem do símbolo** por bloco via ChatGPT (ponte da assinatura): mente=cérebro cromado, ideia=lâmpada acendendo, tempo=ampulheta — sempre preto cósmico + prata (identidade).
- **Microvídeo**: anima a imagem via **Sora** (mesma assinatura; braço em construção) — pessoa respira, câmera desliza. Enquanto o braço não existe: zoom liso anti-tremor (base 4608) + overlays da **BIBLIOTECA DE MOTIONS** (D:\BIBLIOTECA DE MOTIONS PARA VÍDEOS — partículas/fumaça/cosmos por cima, blend screen).
- Mistura clipes reais quando servirem (vídeos + imagens no mesmo vídeo, "muito bem feito").
**Saída:** pasta de cenas nomeadas por bloco + manifesto cena→bloco.

## 7 · O COMPOSITOR DE ÁUDIO
Trilha de fundo REAL com licença limpa (YouTube Audio Library / incompetech CC-BY com crédito automático na descrição) — nunca zumbido sintético.
**Mix por medição:** música ≥18 dB abaixo da voz (regra do crivo), fade in/out, LUFS final −16 a −14. Gera o manifesto de mix (md5 + números) para o crivo.
**Saída:** trilha escolhida + mix final + mix_manifesto.json.

## 8 · O LEGENDADOR
SRT sincronizado com a narração (por tempos do Narrador ou Whisper), acentuação perfeita, queima com o estilo da marca (Arial bold, branco com contorno preto, zona segura).
**Saída:** legendas.srt + vídeo com legenda queimada.

## 9 · O EDITOR (montagem)
Junta tudo: cenas na ordem dos blocos, corte/movimento a cada 4–8s, NUNCA imagem parada, P&B da marca (hue=s=0 + contraste), overlays de motion, transições sóbrias, 1080p30.
**Saída:** vídeo final para o crivo.

## 10 · O EMBALADOR *(faltava na lista — avisado)*
Título pelo parâmetro (3 das 4 peças, ≤70c), **capa 3D cromada** (fábrica de capas + crivo visual), descrição SEO (keyword nas 2 primeiras linhas + capítulos + crédito de música + hashtags), tags, playlist.
**Saída:** kit de publicação completo.

## 11 · O PUBLICADOR *(faltava na lista — avisado)*
O robô do navegador (perfil logado 1x pelo Diretor): sobe o vídeo como um humano, horário natural (19h ±min), preenche o Studio, marca flag de IA quando aplicável.
**Só publica com o PORTÃO 100%: crivo total do Pesquisador + carimbo do Diretor.** Verificação/captcha → para e chama.

## 12 · O PESQUISADOR (já existia — o juiz de tudo)
Varredura semanal (segunda 08:05) + crivo total de cada peça e do arquivo final (11+ medições). A regra viva que manda em todos os outros.
