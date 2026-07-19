# Karaokê vs bloco: a decisão por dados (ciclo 2 — aprofundamento)

> Varredura ciclo 2, 2026-07-17. Aprofunda o que a ESTILO-POSICAO-RETENCAO-2026.md abriu: agora com efeito MEDIDO, timing fino e a matriz de decisão por trecho de vídeo. Todo número tem fonte ao lado; opinião marcada como "leitura minha". Atenção: a maioria dos números vem de blogs de fornecedores de ferramenta (não é estudo revisado por pares) — usar como direção, não como verdade absoluta.
> Contexto do canal: vídeo LONGO (5–30 min) motivacional PT-BR, P&B prata, b-roll que casa com a fala, 3 vídeos/semana.

## 1. O efeito medido (o que há de número em 2026)

- Legenda bem estilizada melhora o watch time em **23–40%** vs texto estático/mal estilizado (blog da Opus — https://www.opus.pro/blog/best-caption-presets-styles-boost-retention).
- Palavra-a-palavra tem "as maiores taxas de retenção para conteúdo educacional"; **~70% dos top criadores educacionais** usam o estilo (mesma fonte Opus — https://www.opus.pro/blog/best-caption-presets-styles-boost-retention).
- Compreensão sobe até **56%** quando áudio e texto chegam juntos (dual-coding; mesma fonte Opus — https://www.opus.pro/blog/best-caption-presets-styles-boost-retention).
- Presets com identidade de marca consistente: retenção **+10–18%** em espectador recorrente (mesma fonte Opus — https://www.opus.pro/blog/best-caption-presets-styles-boost-retention). Leitura minha: é o nosso caso — 3 vídeos/semana com a MESMA legenda prata cria reconhecimento.
- Segmentos curtos de legenda melhoram velocidade de leitura e compreensão vs legendas longas (estudo acadêmico Kruger et al. 2013, citado em https://www.contentfries.com/blog/the-science-of-video-captions-how-they-impact-audience-retention — original: https://dl.acm.org/doi/abs/10.1145/2509315.2509331).
- Texto pequeno demais reduz engajamento; razão texto-para-conteúdo ideal na tela: **20–30%** (Journal of Computer-Assisted Learning, citado em https://www.contentfries.com/blog/the-science-of-video-captions-how-they-impact-audience-retention).
- Palavra-a-palavra supera legenda de frase inteira em completion rate "na maioria dos estudos de TikTok" — sem número publicado (https://blitzcutai.com/blog/best-caption-style-tiktok).
- Leitura minha sobre o conjunto: NENHUMA fonte mediu karaokê contínuo em vídeo de 10–30 min. Todos os dados fortes são de short-form ou educacional segmentado. A regra da casa (bloco no corpo + ênfase pontual) continua de pé — o que muda agora é o COMO (timing e estilo abaixo).

## 2. Timing fino (o detalhe que ninguém da casa sabia)

- A legenda deve ENTRAR **100–200 ms ANTES** do áudio da frase (https://www.opus.pro/blog/best-caption-presets-styles-boost-retention).
- No karaokê, a palavra deve acender **50–100 ms ANTES** de ser falada (mesma fonte). Mecanismo: cria "micro-loop de antecipação" — o olho chega junto com a voz, nunca atrasado.
- Precisão primeiro: karaokê com timing desalinhado é PIOR que bloco simples (https://www.vocallab.ai/blog/word-highlighting-subtitles).
- Leitura minha: isso pede alinhamento por ferramenta (whisperX dá ±50 ms por palavra — ver RECEITA-KARAOKE-ASS-FFMPEG.md), não chute manual. Regra prática: gerar timestamps por palavra e adiantar o SRT/ASS inteiro em 100 ms na entrega final.

## 3. Quando usar cada um — matriz de decisão por trecho

| Trecho do vídeo | Estilo | Por quê |
|---|---|---|
| Gancho (0–30s) | Karaokê palavra-a-palavra | 60–70% do drop-off é nos primeiros segundos; movimento segura o olho (https://www.vocallab.ai/blog/word-highlighting-subtitles) |
| Corpo (narração sobre b-roll) | BLOCO 1–2 linhas, ~5 palavras | Padrão da casa; bloco deixa o olho descansar em vídeo longo (ciclo 1) e "minimal clean" é o preset indicado para conteúdo com muito b-roll (https://www.opus.pro/blog/best-caption-presets-styles-boost-retention) |
| Frase-tese de cada capítulo | Bloco com 1 palavra em destaque | "Bold statement": cada linha vira manchete, 5–8 palavras (https://www.opus.pro/blog/best-caption-presets-styles-boost-retention) |
| Momentos de tela "cheia" (arte 3D, letreiro) | SEM ênfase, bloco discreto ou nada | Destaque + tela congestionada = sobrecarga visual (https://www.vocallab.ai/blog/word-highlighting-subtitles) |
| Chamada final (inscrição/próximo vídeo) | Karaokê com varredura (\kf) | Fechamento com energia; varredura é o efeito clássico de karaokê (https://aegisub.org/docs/latest/ass_tags/) |

- Limite duro em qualquer estilo: **8–12 palavras por evento** no máximo (https://www.opus.pro/blog/best-caption-presets-styles-boost-retention); nosso padrão ~5 já respeita.

## 4. O estilo dos virais motivacionais em 2026 — e a tradução P&B

O que os virais usam (todas as fontes abaixo são de short-form; adaptar, não copiar):
- **Bold Highlight**: texto branco EM CAIXA ALTA + 1 palavra-chave destacada em amarelo/vermelho/laranja por frase (https://blitzcutai.com/blog/best-caption-style-tiktok).
- **Word Pop**: palavra-a-palavra com animação sutil (escala/fade), sem caixa de fundo — o indicado para conteúdo motivacional/alta energia (https://blitzcutai.com/blog/best-caption-style-tiktok).
- Amarelo **#f7c204** é a cor de destaque mais comum; branco+contorno preto segue sendo o contraste mais seguro (síntese de https://blitzcutai.com/blog/best-caption-fonts-tiktok e https://sendshort.ai/guides/style-captions/).
- Fontes dominantes: Montserrat Bold, Proxima Nova Bold, Impact — bold sans-serif de x-height alta (https://blitzcutai.com/blog/best-caption-fonts-reels-2026).
- CAIXA ALTA aumenta ênfase/urgência percebida em conteúdo motivacional (https://blitzcutai.com/blog/best-caption-style-tiktok).
- 1 cor de acento no máximo; animação pesada e multicor perdem para simples+contraste no celular (https://www.vocallab.ai/blog/word-highlighting-subtitles).

**Tradução para a nossa marca P&B prata (leitura minha — precisa de aval do Gerente porque toca a LEGENDA-DA-MARCA):**
- Amarelo quebraria o P&B. O destaque da casa deve ser MONOCROMÁTICO: palavra-chave acende de cinza-prata (&H00A0A0A0) para BRANCO PURO via karaokê — testado e funciona (ver receita). O "pop" vem da luz, não da cor.
- Alternativa de ênfase sem cor: +10% de escala na palavra-chave (`\fscx110\fscy110`) — sutil, elegante, dentro da estética "melhorar ≠ aumentar".
- CAIXA ALTA: usar só nas frases-tese e chamada final, nunca no corpo (caixa alta contínua por 20 min cansa — leitura minha).
- Arial Bold continua (norma da casa + referência Netflix do ciclo 1); Montserrat Bold fica anotada como candidata SE o Diretor um dia quiser repaginar — decisão dele, não minha.

## 5. O que ainda não tem dado (honestidade de pesquisa)

- Não achei NENHUM estudo com número para karaokê em vídeo >90s no YouTube. O mais próximo: recomendação de bloco + ênfase a cada 8–10s (ciclo 1, https://emax.studio/blog/word-by-word-ai-captions-vs-static-subtitles).
- Os percentuais da Opus (23–40% etc.) são de blog comercial sem metodologia aberta (https://www.opus.pro/blog/best-caption-presets-styles-boost-retention). Tratar como hipótese de trabalho.
- Conclusão (leitura minha): o canal deve gerar o PRÓPRIO dado — com 3 vídeos/semana, em 1 mês temos 12+ vídeos para comparar retenção real no YouTube Studio entre vídeos com e sem ênfase karaokê nos momentos-chave.

## Como aplicar no próximo vídeo

1. Aplicar a matriz da seção 3 no roteiro ANTES da queima: marcar gancho (karaokê), 3–5 frases-tese (bloco+destaque) e chamada final (\kf) — 10 min de trabalho por vídeo, cabe na cadência de 3/semana.
2. Adiantar a legenda em ~100–200 ms em relação ao áudio na entrega final (seção 2) e, no karaokê, acender a palavra 50–100 ms antes da voz.
3. Implementar o destaque monocromático prata→branco (seção 4) num trecho de teste e levar o frame ao Gerente junto com a proposta de contraste do ciclo 1 (Outline=3 vs caixa) — uma decisão só, de uma vez.
4. Manter corpo em bloco ~5 palavras; conferir que nenhum evento passa de 12 palavras (limite da seção 3).
5. Abrir uma planilha simples de retenção por vídeo (YouTube Studio: retenção aos 30s e média) anotando qual estilo de ênfase cada vídeo usou — em 4 semanas (12 vídeos) teremos o NOSSO dado de karaokê vs bloco.
6. Nos vídeos de domingo 10h (maior audiência de estreia), usar sempre a versão mais validada; testar variação nova só em quarta/sexta (leitura minha: proteger o horário nobre).
