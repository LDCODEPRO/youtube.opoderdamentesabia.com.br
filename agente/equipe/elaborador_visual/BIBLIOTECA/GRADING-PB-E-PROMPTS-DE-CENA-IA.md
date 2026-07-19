# Grading P&B cinematográfico + prompts de imagem IA para cenas
Data: 2026-07-17 · Autor: O Elaborador Visual · Status: guia técnico da estética da marca

Nosso canal é P&B com prata cromada. Este guia junta (a) o workflow de grading preto e branco
que separa "vídeo dessaturado" de "filme", e (b) a gramática de prompt que faz a IA entregar
cena cinematográfica de primeira — nas DUAS frentes do Diretor: b-roll real de pessoas
(padrão) e cena simbólica (só quando a narração nomeia o conceito).

---

## 1. Grading P&B: o workflow certo (ordem importa)

Fonte principal: https://noamkroll.com/how-to-color-grade-a-perfectly-cinematic-black-and-white-look/

1. **Ajustar COR antes de dessaturar.** Mexer nos canais RGB primeiro e só então tirar a
   saturação — dessaturar antes anula o efeito. Empurrar canais emula filtros físicos de
   lente (ex.: filtro amarelo clássico do P&B) e muda drasticamente os tons finais.
2. **Contraste é o prato principal.** Os estoques P&B clássicos eram de contraste alto;
   só dessaturar sem trabalhar contraste dá cara "flat e video-ish" (o erro nº 1).
3. **Pretos: esmagar primeiro, levantar depois.** Para o look vintage: crush nos blacks e
   então um leve lift — levantar pretos sem antes comprimi-los dá imagem "leitosa" e sem
   profundidade (milky blacks).
4. **LUT criativa SEMPRE antes da dessaturação**, para herdar o contraste e os níveis do
   design original da LUT.
5. **Vinheta/power window: quase imperceptível.** Uma vinheta sutil guia o olho; várias
   janelas marcadas dão cara digital. P&B é bom em ESCONDER: usar isso a favor (mistério).
6. **Na captura/geração:** P&B perdoa mais a superexposição do que cor; se houver opção,
   partir de material flat/LOG para ter latitude nas sombras e altas luzes.

**Aplicação direta no pipeline (leitura minha):** nossa cadeia FFmpeg/edição deve fixar essa
ordem — (RGB mix/curvas de canal) → dessaturação → curva de contraste com pretos esmagados →
vinheta sutil → grão. Nunca começar pelo `hue=s=0` seco, que é exatamente o "erro nº 1" da fonte.

## 2. Zona de segurança do nosso P&B (checklist de saída)

- [ ] Pretos assentados (crushed) mas com detalhe onde interessa — nada de cinza leitoso
      (https://noamkroll.com/how-to-color-grade-a-perfectly-cinematic-black-and-white-look/)
- [ ] Altas luzes brilhando (a prata cromada precisa "estourar limpo", não cinza-claro)
- [ ] Vinheta presente porém invisível ao olho consciente (mesma fonte)
- [ ] Grão fino uniforme (assinatura de filme; ver film stocks na seção 3)
- [ ] Mesmo tratamento em TODAS as cenas do vídeo — b-roll real e símbolo têm de parecer
      saídos do MESMO filme (leitura minha; é o que cola a regra "visual casa com a fala")

## 3. Gramática de prompt para cena cinematográfica (IA de imagem)

Fonte principal: https://promptsera.com/midjourney-prompts-cinematic-realism/ (a gramática
vale para qualquer gerador — ChatGPT/ponte, Midjourney etc.; leitura minha).

**Fórmula (nesta ordem, o começo pesa mais):**
`[tamanho de plano + ângulo] + [sujeito] + [ação/emoção] + [ambiente] + [hora/clima] + [iluminação] + [lente + film stock] + [referência de estilo] + [parâmetros]`
— e manter o prompt enxuto (a fonte recomenda <60 palavras).

**Vocabulário que muda o resultado (mesma fonte):**
- Planos: EWS (figura minúscula na paisagem = solidão/imensidão), WS, MS, CU, ECU
  (olho, mão, gota de suor).
- Ângulos: low angle = herói/dominante · high angle = vulnerável/isolado · dutch angle =
  desconforto · over-the-shoulder = intimidade.
- Lentes: 35mm = "padrão cinema" natural · 50mm = retrato limpo · 85–135mm = fundo comprimido
  e íntimo · anamórfica = flare horizontal e bokeh oval. Sempre parear com abertura
  (f/1.4 = fundo derretido).
- Iluminação (nomear a técnica, não o adjetivo): chiaroscuro (contraste extremo, nosso DNA),
  Rembrandt (triângulo de luz no rosto), rim lighting (silhueta recortada — perfeito para
  prata sobre preto), volumetric fog (feixes visíveis).
- Film stock: para o nosso P&B, **Kodak Tri-X 400** = alto contraste, grão marcado, film noir
  (mesma fonte). É o nome que mais aproxima a IA do nosso look.
- Anti-plástico: pedir explicitamente a EXCLUSÃO de "3d render, CGI, smooth skin, plastic,
  airbrushed, cartoon, watermark" (a fonte traz a lista de negativos completa).

## 4. Receitas prontas do canal (adaptação nossa — leitura minha, gramática da fonte acima)

**B-roll REAL (padrão novo do Diretor):**
> "Wide shot, low angle, homem de moletom subindo escadaria da cidade no amanhecer, névoa,
> rim lighting recortando a silhueta, black and white, Kodak Tri-X 400, 35mm f/2, chiaroscuro,
> photorealistic — sem marca d'água, sem texto"
(+ marca inline MENTE_SABIA no pedido à ponte, SEMPRE — regra da casa.)

**Cena simbólica (só quando a fala nomeia o conceito):**
> "Extreme close-up, cérebro cromado prateado girando lento sobre fundo preto cósmico #05060A,
> partículas de poeira iluminadas, volumetric light, chiaroscuro, black and white com prata
> metálica, 85mm f/1.4, photorealistic — sem rostos, sem marca d'água"

Regras fixas nas duas receitas:
- 1 ideia por imagem; prompt <60 palavras (https://promptsera.com/midjourney-prompts-cinematic-realism/).
- Não pedir contradição física (ex.: fundo desfocado + lente ultra-wide — mesma fonte).
- Base ≥4608 px para o zoom liso anti-tremor (doutrina interna provada — ver
  CENAS-SIMBOLICAS-DA-MARCA.md).
- NUNCA imagem parada no vídeo final: zoom liso, overlay de motion (blend screen) ou microvídeo.

## 5. Consistência entre cenas (o vídeo como UM filme)

- Repetir o MESMO bloco final do prompt (iluminação + lente + film stock + estilo) em todas as
  cenas do vídeo = identidade coesa; mudar só plano/sujeito/ação (leitura minha; princípio da
  priorização sequencial da fonte de prompts).
- Se o gerador suportar referência de imagem/personagem (ex.: `--oref` no Midjourney), usar a
  mesma referência para manter o "protagonista" do vídeo consistente entre cenas
  (https://promptsera.com/midjourney-prompts-cinematic-realism/).
- O grading da seção 1 é o unificador final: mesmo que as gerações variem, a mesma curva de
  contraste + grão + vinheta cola tudo (leitura minha).

## Como aplicar no próximo vídeo

1. Refazer a cadeia de grading do pipeline na ordem certa: canais RGB → dessaturar → contraste
   com pretos esmagados → vinheta sutil → grão fino (nunca só dessaturar).
2. Adotar o bloco-assinatura de prompt do canal: "black and white, Kodak Tri-X 400,
   chiaroscuro, photorealistic" + lista de negativos anti-plástico em TODOS os pedidos.
3. Gerar o b-roll real com a receita da seção 4 (pessoas em ação casando com a fala) e
   reservar a receita simbólica só para as frases que nomeiam o conceito.
4. Padronizar lente por função: 35mm para ação/ambiente, 85mm f/1.4 para close emocional e
   símbolo — e manter nas cenas do mesmo bloco.
5. Conferir o vídeo exportado contra o checklist da seção 2 (pretos, altas luzes, vinheta,
   grão, coesão) antes de subir para aprovação.
