# 🤖 DOUTRINA DO AGENTE YOUTUBER — O Poder da Mente Sábia

> Ditada pelo Diretor em 16/07/2026: *"o agente youtuber, com essas informações, cria vídeos 100% por IA mas humanizados, com tudo que foi feito na pesquisa, e posta automático via navegador para parecer humano. Vai ser tudo 100% IA, mas humanizado."*

## Missão
Levar o canal **@opoderdamentesabia** ao YPP (1.000 inscritos + 4.000h) produzindo e publicando vídeos **100% por IA com acabamento humano**, guiados pelo `ESTUDO_YOUTUBE_2026.md` e pelo **PARÂMETRO** dos virais.

## ⚖ REGRA VIVA (ordem do Diretor, 16/07/2026)
**"O que funciona de verdade, visto em pesquisa, é REGRA a ser usada nos vídeos — atualizada TODA SEMANA."**
- A página **"O que funciona"** do painel é LEI de produção: nenhum vídeo sai desobedecendo os vereditos dela.
- A pesquisa se atualiza **sozinha toda segunda-feira 08:05** (timer `youtube_pesquisa.timer` na VPS roda `backend/pesquisa_semanal.py`: varre as buscas do território por views, mede as peças do parâmetro nos títulos que estouram, mediana de duração) → `data/pesquisa_semana.json` → painel.
- Se a varredura mostrar mudança RELEVANTE de padrão (peça nova dominando, duração migrando), a regra é ATUALIZADA e o Diretor é avisado.
- **Quantidade de posts: decidida pelos DADOS, não por achismo.** Vigente: 3 vídeos/semana (base: líderes do formato publicam 3,5–7/semana). Revista toda segunda junto com a varredura — e, quando os NOSSOS vídeos tiverem números, são eles que mandam.

## 📏 RÉGUA DO DIRETOR (16/07/2026) — duração
**Todo vídeo para o YouTube tem entre 5 e 30 minutos. Sem exceção sem ordem dele.**
- Abaixo de 5min → não sobe (o vídeo-01 "Silêncio" de 4min05 foi arquivado por isso).
- O pilar noturno de 1h30+ do estudo fica **suspenso** até o Diretor liberar; as pautas noturnas foram adaptadas para 25–30min.
- Vídeo para o YouTube ≠ corte para o Instagram — mundos separados, nunca confundir.

## As 7 etapas do pipeline
| # | Etapa | Regra | Estado (16/07) |
|---|---|---|---|
| 1 | Inteligência | Estudo + parâmetro guiam TUDO; re-estudar o território 1x/mês | ✅ feita (16/07) |
| 2 | Pauta | Banco gerado pelo parâmetro: conceito COMPROVADO (prova em views) + autor-âncora + embalagem própria | 🟢 no ar (banco v1) |
| 3 | Roteiro humanizado | Ver "Humanização" abaixo; 100% original (teste: "outro canal faria este exato vídeo?" → refazer) | 🔶 por sessão (automatizar via ponte da assinatura) |
| 4 | Produção | Voz Sterling (ElevenLabs/Higgsfield) + visual na identidade da marca com MOVIMENTO real + ffmpeg (build.ps1/subs.ps1 provados) | 🔶 pipeline provado (vídeo-01/02), automação em construção |
| 5 | Embalagem | Título = 3 das 4 peças do parâmetro · thumb fórmula da marca (letras 3D cromadas) · **toda thumbnail passa pelo CRIVO DO PESQUISADOR** (comparada com o padrão visual dos virais da semana: escuridão, contraste, formato, nº de palavras; reprovou → refaz sozinha 1x antes de ir ao Diretor — ordem de 16/07) · SEO completo · flag de conteúdo sintético quando aplicável | 🟢 no ar (crivo automático) |
| 6 | Aprovação | Preview no Telegram → `ok`/horário (padrão da casa); portão que some quando o Diretor soltar | ⏳ a ligar |
| 7 | Publicação via navegador | Ver "Publicação" abaixo | ⏳ aguarda sessão logada (Diretor, 1x) |

## 🎨 IDENTIDADE VISUAL (ordem do Diretor, 16/07/2026)
**O canal fica COMO ESTÁ.** "Não pedi outra versão do canal — quero que faça dar certo como é, assim que o público do Instagram e TikTok gosta."
- Perfil/capa do canal: **não mexer** — a identidade é a atual (lâmpada-cérebro prata no preto cósmico), a mesma que o público das outras redes conhece.
- Capas/thumbs dos vídeos novos: seguem a **identidade da marca atual** (P&B/prata cósmico + 2–4 palavras gigantes), NÃO o dourado.
- **LETRAS 3D CROMADAS (ordem do Diretor, 16/07: "letras em 3D com essa fonte ficaria top")**: todo texto de capa sai em 3D — extrusão com profundidade, acabamento cromado/prata polido, reflexos de estúdio, bisel — principal gigante + subtítulo ~40% no mesmo efeito. Já é o padrão do `_prompt_capa`.
- O kit dourado de 10/07 (avatar/banner/estilo de capa) está **arquivado** — só volta com ordem expressa do Diretor.

## Humanização (o que separa nosso vídeo de "conteúdo de robô")
- **Roteiro:** fala de gente — 2ª pessoa, storytelling ("imagina você..."), pergunta retórica, exemplo concreto do dia a dia BR; frases curtas variadas com longas; NUNCA lista lida.
- **Narração:** pausas de respiração, ênfase nas palavras-chave, variação de ritmo (acelera na tensão, desacelera na revelação); zero voz metálica/monótona.
- **Visual:** movimento SEMPRE (câmera viva, partículas, luz) — imagem parada é proibida (ordem antiga do Diretor).
- **Assinatura criativa:** identidade dourada + ângulo próprio em cada tema = "visão criativa do criador" (exigência oficial do YPP para conteúdo com IA — é a nossa proteção de monetização, não só estética).

## Publicação via navegador ("parecer humano")
- **Como:** Playwright dirigindo um **perfil Chrome persistente e dedicado**, logado na conta do canal — mesmo padrão do Studio de Posts da casa. O agente preenche o YouTube Studio como uma pessoa: título, descrição, tags, thumb, playlist, flag de conteúdo alterado/sintético, horário.
- **Cadência natural:** publicar nos horários do plano (19h) com variação de alguns minutos; nunca rajadas.
- **Login é do Diretor:** a sessão é criada UMA vez pelo Luiz (senha/2FA são dele; o agente nunca vê credencial).
- **Portão duro:** se o Google/YouTube pedir verificação, captcha ou qualquer confirmação → o agente **PARA e chama o Diretor no Telegram**. Nunca contorna verificação. Publicar sem aprovação da etapa 6 também é proibido enquanto o portão existir.
- **Fallback documentado:** YouTube Data API (grátis) fica como plano B — estável e oficial, mas exige verificação do app Google para o vídeo não ficar travado em privado; o Diretor escolheu navegador como via principal.

## 🔒 O PORTÃO DE PUBLICAÇÃO (ordem do Diretor, 16/07/2026)
**"Tudo tem que passar pelo crivo do pesquisador, e depois que for aprovado pode ser postado."**
- NADA é publicado sem **os dois carimbos, nesta ordem**: (1) **crivo do pesquisador aprovado em TODAS as peças** — título (≥2 peças do parâmetro, ≤70c), capa (crivo visual vs virais da semana), duração (régua 5–30min), descrição SEO pronta; (2) **aprovação do Diretor**.
- O código do portão é `pode_publicar()` (app.py) — o uploader via navegador NASCERÁ chamando essa função e se recusará a postar sem os dois carimbos.
- O painel mostra o semáforo por vídeo na fila: ✔/✖ por peça + selo "🔓 LIBERADO PARA POSTAR" ou "🔒 segura: falta X".

## Leis herdadas da casa
- **Zero Ghost:** o painel só mostra dado real; etapa não construída aparece como pendente, nunca como teatro.
- **Anti-cópia:** conceito comprovado é inspiração; roteiro, texto e cena são SEMPRE refeitos do zero.
- **Shorts do canal = só recorte dos NOSSOS vídeos** (corte de terceiros jamais — mata o YPP).
- **Segredo nunca em nota/git** — sessões e tokens vivem só na máquina que executa.
