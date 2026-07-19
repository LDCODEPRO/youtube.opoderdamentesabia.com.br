# Animação de legenda em 2026: a camada de MOVIMENTO (pop, fade, float) em ASS + ffmpeg

> Varredura ciclo 2, 2026-07-17. Aprofunda "estilos que os virais usam em 2026" por outro ângulo que os guias irmãos NÃO cobrem: eles tratam do REALCE DE COR palavra-a-palavra (`\k`, prata→branco). Este trata do MOVIMENTO — como a palavra entra, cresce e sai — que é uma camada diferente e somável. Todo número tem fonte; opinião marcada como "leitura minha"; nada inventado.
> Não repete a RECEITA-KARAOKE-ASS-FFMPEG.md (realce `\k`) nem o KARAOKE-VS-BLOCO (matriz de decisão): aqui é só a técnica de animação e sua tradução para o P&B.

## 1. O que os virais fazem em 2026 — catálogo com fonte

Estilos de animação de legenda/título que dominam short-form e conteúdo educacional em 2026 (fonte: https://www.opus.pro/blog/best-text-animation-packs-captions-titles):

- **Pop / Scale (escala):** a palavra surge maior e assenta — "micro-momentos de interesse visual que disparam mecanismos de atenção" (mesma fonte).
- **Bounce / Spring (quicar):** entrada elástica; alta energia.
- **Typewriter (máquina de escrever):** revela letra a letra.
- **Fade + realce de cor:** aparece suave destacando a frase-chave.
- **Word-by-word reveal:** cada palavra entra no ritmo da fala.

Encaixe por tipo de conteúdo (fonte: https://reelwords.ai/blog/animated-captions — blog comercial da ReelWords, tratar como direção):

| Animação | Boa para |
|---|---|
| Pop/scale | ganchos, afirmações fortes, "punchline" |
| Word-by-word highlight | explicativo, educacional, talking-head |
| Bounce | comédia, entretenimento, meme |
| Typewriter | narrativa, desabafo |
| Slide-in (terço inferior) | entrevista, comentário |
| **Minimal documentary** | **estilo premium, lifestyle, marca sóbria** |

- **Leitura minha — a nossa raia:** somos "minimal documentary". Bounce/spring é rotulado como comédia/meme na própria tabela acima — briga com a estética P&B prata e com "melhorar ≠ aumentar". A nossa animação tem que ser LUZ e ESCALA sutil, nunca elástico saltitante.

## 2. Os números (e o cuidado com eles)

- "Texto animado costuma aumentar a retenção em **15 a 30%** nos primeiros 10 segundos" (https://www.opus.pro/blog/best-text-animation-packs-captions-titles — blog COMERCIAL de fornecedor, sem metodologia aberta; hipótese de trabalho, não verdade).
- 85%+ dos vídeos sociais são vistos SEM som (já ancorado no ciclo 1: https://www.kapwing.com/resources/subtitle-statistics/) — reforça que o movimento é o que segura o olho no mudo.
- **A regra de ouro, da própria fonte de animação:** "Use animações estrategicamente... Reserve as mais dinâmicas para momentos-chave como títulos e chamadas; use efeitos sutis para legenda de corpo. Animações amontoadas criam caos visual" (https://www.opus.pro/blog/best-text-animation-packs-captions-titles). Leitura minha: isso é literalmente a política da casa (ênfase pontual, corpo calmo) dita por uma fonte externa. Fortalece a nossa doutrina.
- Ferramentas de mercado que popularizaram isso (referência, não pra copiar): Submagic anuncia "35+ templates que destacam, quicam e aparecem palavra por palavra em sincronia" (https://www.submagic.co/ai-caption). Nós fazemos o mesmo efeito à mão em ASS, sem depender de ferramenta paga nem quebrar o P&B.

## 3. As tags de MOVIMENTO em ASS (o que cada uma faz)

Fontes desta seção: https://aegisub.org/docs/latest/ass_tags/ , https://hhsprings.bitbucket.io/docs/programming/examples/ffmpeg/subtitle/ass.html e https://note.com/ron444/n/n3f5ec5869db0

- **`\t(t1,t2,accel,transformações)`** — anima QUALQUER propriedade (escala, cor, blur...) de t1 a t2 (em ms desde o início do evento). O `accel` é a curva:
  - `accel < 1` → começa rápido e desacelera (ease-out) — o "assentar" natural de um pop.
  - `accel = 1` → linear.
  - `accel > 1` → começa devagar e acelera (ease-in).
  - (comportamento do coeficiente confirmado nos exemplos 0.5/1/2 de https://hhsprings.bitbucket.io/docs/programming/examples/ffmpeg/subtitle/ass.html)
- **`\fscx` / `\fscy`** — escala horizontal/vertical em % (100 = tamanho normal). Base do efeito pop.
- **`\fad(entrada,saída)`** — fade-in e fade-out em ms (ex.: `\fad(120,80)`).
- **`\fade(a1,a2,a3,t1,t2,t3,t4)`** — fade com controle fino de alpha em etapas (quando `\fad` simples não basta).
- **`\move(x1,y1,x2,y2,t1,t2)`** — desliza o texto de um ponto a outro no intervalo dado. Base do "float-in".
- **`\blur`** — desfoque gaussiano da borda; animado com `\t` faz o texto "entrar em foco".
- **`\pos(x,y)`** — posição fixa; **`\frz`** — rotação no eixo Z (existe, mas **não usamos**: gira legenda = clima de meme, contra a marca).

**Pegadinha do libass (confirmada):** com `BorderStyle=3/4` (caixa), o motor pode reaproveitar `Outline`/`Shadow` como cor de fundo em vez de contorno — testar sempre que combinar caixa com animação (https://hhsprings.bitbucket.io/docs/programming/examples/ffmpeg/subtitle/ass.html). Casa com a decisão de contraste ainda aberta com o Gerente (ACESSIBILIDADE-CONTRASTE-NORMA-PTBR.md, seção 2).

## 4. Receita P&B: 3 animações sóbrias, prontas para colar

Usam o mesmo header/estilo `Marca` e a mesma queima (`ffmpeg -vf "ass=legendas.ass"`) da RECEITA-KARAOKE-ASS-FFMPEG.md — não repito o cabeçalho aqui. Só o campo Text do Dialogue muda.

### a) Pop de ênfase (para a palavra-chave da frase-tese)
A palavra nasce 15% maior e ASSENTA em 120 ms — o "pop" premium, sem cor, sem quicar:
```
{\fscx115\fscy115\t(0,120,0.6,\fscx100\fscy100)}MENTE
```
Leitura minha: 115% já lê como ênfase; passar de 120% vira "grito". `accel=0.6` dá o assentar elegante. Combina com o realce prata→branco do `\k` da RECEITA na MESMA palavra (movimento + luz juntos).

### b) Float-in do gancho (bloco de abertura, primeiros segundos)
O bloco sobe 12 px e aparece em 140 ms — entra "flutuando", sem corte seco:
```
{\move(960,558,960,546,0,140)\fad(140,0)}{\k...}Sua mente é o campo
```
(x=960 = centro em 1920; y sobe de 558 para 546. Ajustar ao MarginV real do estilo.) O `\fad(140,0)` casa com a regra do ciclo 2 de a legenda entrar ~140 ms antes da voz.

### c) Focus-in documentário (encerramento / frase de impacto)
O texto entra levemente desfocado e vem a foco em 160 ms — clima "premium documentary":
```
{\blur6\t(0,160,\blur0)\fad(120,120)}O primeiro passo é decidir
```

**Duração é tudo (leitura minha):** manter TODA animação entre **100 e 180 ms**. Abaixo de 100 ms ninguém percebe; acima de ~200 ms vira movimento chamativo e cansa em vídeo de 10–30 min. Rápido o bastante para ler como acabamento, não como efeito.

## 5. Onde aplicar (amarra com a matriz da casa, sem repeti-la)

Seguir a matriz de trecho do KARAOKE-VS-BLOCO-DECISAO-POR-DADOS.md e só ESCOLHER a animação certa por trecho:
- Gancho (0–30 s) → **float-in (b)** no bloco + `\k` prata→branco.
- Corpo → **NADA de animação**; bloco estático, só o `\k` quando houver ênfase. (regra "sutil no corpo", https://www.opus.pro/blog/best-text-animation-packs-captions-titles)
- Frase-tese de capítulo → **pop de ênfase (a)** na palavra-chave.
- Chamada final → **focus-in (c)** ou o `\kf` de varredura da RECEITA.
- Tela cheia de arte 3D → nada (sobrecarga visual — ciclo 2).

Limite duro: no máximo UMA animação por evento. Duas animações competindo na mesma tela = o "caos visual" que a própria fonte alerta (mesma fonte acima).

## 6. Conferir o movimento (não dá pra ver num frame só)

Animação não aparece num print único — precisa de tira de frames. Exportar 3 quadros dentro da janela da animação:
```
ffmpeg -y -i video.mp4 -vf "ass=legendas.ass" -ss 00:00:05.00 -frames:v 1 a_000.png
ffmpeg -y -i video.mp4 -vf "ass=legendas.ass" -ss 00:00:05.06 -frames:v 1 b_060.png
ffmpeg -y -i video.mp4 -vf "ass=legendas.ass" -ss 00:00:05.12 -frames:v 1 c_120.png
```
Se entre 000 e 120 ms a letra encolhe/entra e em 120 já está assentada e legível, a animação está no ponto. Leitura minha: essa tira de 3 frames deve ir junto do frame-teste de contraste da RECEITA na entrega ao Gerente.

## Como aplicar no próximo vídeo

1. No vídeo de quarta 19h, aplicar SÓ a animação (a) "pop de ênfase" em 3–5 palavras-tese, deixar o corpo 100% estático, e mostrar a tira de 3 frames ao Gerente antes de animar o vídeo inteiro.
2. No gancho da estreia de domingo 10h, testar o float-in (b) casado com o `\k` da RECEITA — é o trecho onde 15–30% de retenção nos primeiros 10 s (fonte comercial, hipótese) mais paga.
3. Travar a duração de qualquer animação em 100–180 ms no template e nunca colocar mais de uma animação por evento (regra anti-caos da seção 5).
4. Guardar os 3 snippets da seção 4 como "presets" de texto na pasta de ferramentas da equipe, ao lado do `srt2ass_karaoke.py`, para o custo por vídeo ser copiar-e-colar (cabe na cadência 3/semana).
5. Levar ao Gerente a nota para a LEGENDA-DA-MARCA: "animação permitida = pop/float/focus sutil (100–180 ms), monocromática; PROIBIDO bounce, rotação e cor de acento" — fecha a estética antes que vire bagunça.
6. Abrir 1 linha na planilha de retenção (a mesma do ciclo 2) marcando quais vídeos usaram animação de entrada, para em 4 semanas termos o NOSSO dado — os 15–30% são de blog comercial, não nossos.
