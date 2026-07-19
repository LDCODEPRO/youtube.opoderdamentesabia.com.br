# Mandato de pesquisa — Legendador

## Varredura ciclo 2 — 2026-07-17
**O que estudei:** aprofundamento ("mais um ciclo de conhecimento", ordem do Diretor). Os 3 temas do mandato do ciclo 2 (palavra-a-palavra vs bloco com efeito medido; estilos virais 2026; karaokê ASS via ffmpeg) já estavam cobertos por 2 guias do início deste ciclo (KARAOKE-VS-BLOCO-DECISAO-POR-DADOS.md e RECEITA-KARAOKE-ASS-FFMPEG.md) — proibido repetir. Empurrei para as 2 fronteiras adjacentes que o ciclo 1 tinha deixado como "próximo estudo": (1) de onde vêm os TEMPOS por palavra (alinhamento forçado) e (2) a camada de MOVIMENTO da legenda (animação, não realce de cor). 5 buscas + leitura de fontes primárias (papers arXiv, GitHub das ferramentas, blogs de fornecedor). Resultado: 2 guias novos.

**Aprendizados-chave:**
- Alinhamento forçado ≠ transcrição: como TEMOS o roteiro, é proibido re-transcrever pra legendar — só calcular os tempos (texto é intocável).
- Precisão medida (só em inglês): MFA erra a fronteira da palavra em ~12,5 ms de mediana; WhisperX ~23,5 ms; MMS ~29,3 ms (arXiv 2406.19363).
- Encaixe do nosso caso: aeneas (DTW+TTS, PT confirmado, sem GPU, sai SRT) no dia a dia; MFA (`portuguese_brazil_mfa`) só na estreia de domingo; WhisperX/stable-ts só quando falta roteiro.
- Tempo REAL por palavra substitui a ESTIMATIVA proporcional da RECEITA e torna exato o adianto de 100 ms do ciclo 2.
- Animação de legenda é camada SOMÁVEL ao realce `\k`: pop/scale, fade, float, focus — feitos com `\t`, `\fscx/\fscy`, `\fad`, `\move`, `\blur` em ASS.
- Nossa raia é "minimal documentary": movimento é luz+escala sutil (100–180 ms); PROIBIDO bounce/rotação/cor de acento (bounce = comédia/meme nas fontes).
- A própria fonte de animação prega "dinâmico só nos momentos-chave, corpo sutil" — validação externa da doutrina da casa.
- Números de retenção de animação (15–30% nos primeiros 10 s) são de blog comercial sem método — hipótese, não verdade; gerar o nosso dado com a cadência 3/semana.

**Fontes principais:**
- https://arxiv.org/html/2406.19363v1 (comparação MFA vs WhisperX vs MMS, com números)
- https://arxiv.org/abs/2606.18466 (estado do alinhamento em 2026, MFA <15 ms)
- https://github.com/readbeyond/aeneas (aeneas: DTW+TTS, PT, saída SRT)
- https://github.com/m-bain/whisperx e https://github.com/jianfch/stable-ts
- https://github.com/MontrealCorpusTools/mfa-models e https://montreal-forced-aligner.readthedocs.io/en/stable/user_guide/models/index.html
- https://www.opus.pro/blog/best-text-animation-packs-captions-titles (catálogo de animação 2026 + regra "sutil no corpo")
- https://reelwords.ai/blog/animated-captions (encaixe de animação por tipo de conteúdo)
- https://aegisub.org/docs/latest/ass_tags/ e https://hhsprings.bitbucket.io/docs/programming/examples/ffmpeg/subtitle/ass.html (tags de animação em ASS/libass)

**Próximo estudo (ciclo 3):** (a) testar aeneas com o áudio real do Narrador + roteiro em PT-BR e MEDIR o erro de fronteira no nosso caso (as tabelas publicadas são só de inglês); (b) como o YouTube renderiza o .srt enviado no player (estilo do CC oficial) para não brigar com a queimada; (c) montar o pipeline único .bat: alinhar → `\k` + animação → frame/tira de conferência, para o custo por vídeo cair a ~2 min na cadência de 3/semana.

## Varredura 2026-07-17
**O que estudei:** estado da arte 2026 de legendas queimadas — estilo/posição/tamanho que aumentam retenção, karaokê vs bloco em vídeo longo, contraste em vídeo P&B (contorno vs caixa), acessibilidade WCAG/W3C e a norma profissional PT-BR (Netflix TTSG pt-BR). 6 buscas + leitura direta das fontes primárias. Resultado: 2 guias novos na BIBLIOTECA (ESTILO-POSICAO-RETENCAO-2026.md e ACESSIBILIDADE-CONTRASTE-NORMA-PTBR.md).

**Aprendizados-chave:**
- 85%+ do vídeo social é visto sem som e legenda eleva watch time ~12% / conclusão até 80% — legenda é âncora de retenção, não enfeite.
- Karaokê palavra-a-palavra vence só no short-form (<60s); para vídeo longo o padrão é BLOCO + ênfase karaokê pontual em palavras-chave (gancho, tese, encerramento).
- Norma PT-BR profissional (Netflix): ≤42 chars/linha, ≤2 linhas, CPS ≤17, evento entre 0,83s e 7s — o CPS é o que estoura com narração rápida; medir sempre.
- Quebra de linha gramatical (antes de conjunção/preposição; nunca artigo|substantivo) é o que separa legenda amadora de profissional.
- Contraste: caixa preta = 21:1, contorno 3–4px ≈ 12:1, contorno 1–2px é frágil — nosso Outline=2 em vídeo P&B falha nos frames brancos; proposta de Outline=3 ou caixa 70–80% levada ao Gerente.
- Zona segura 16:9 em 1080p: manter ~120px do rodapé (controles do player) e fonte renderizada ~24–36px (3–5% da altura).
- Legenda automática NÃO conta como acessível sem revisão (W3C) — subir sempre o NOSSO .srt revisado como faixa oficial.

**Fontes principais:**
- https://partnerhelp.netflixstudios.com/hc/en-us/articles/215600497-Portuguese-Brazil-Timed-Text-Style-Guide
- https://www.w3.org/WAI/media/av/captions/
- https://blitzcutai.com/blog/caption-background-vs-outline-vs-shadow
- https://emax.studio/blog/word-by-word-ai-captions-vs-static-subtitles
- https://www.kapwing.com/resources/subtitle-statistics/
- https://www.captioncut.com/blog/video-captions-seo-engagement-2025/
- https://convertaudiototext.com/blog/subtitle-styling-best-practices
- https://kreatli.com/guides/youtube-shorts-safe-zone

**Próximo estudo:** ferramentas de alinhamento palavra-a-palavra (Whisper word-level timestamps vs forced alignment tipo aeneas/MFA) para automatizar a ênfase karaokê nos momentos-chave; e como o YouTube renderiza o .srt enviado no player (estilo do CC oficial) para não conflitar com a queimada.

## Mandato
SUA ESPECIALIDADE: legibilidade e sincronia.
Pesquisar: estilos de legenda que aumentam retenção (dados, não moda), ferramentas de alinhamento palavra-a-palavra, boas práticas de acessibilidade do YouTube.
## Como registrar o que aprender
Todo achado vira arquivo na sua BIBLIOTECA/ (um tema por arquivo, com fonte e data).
Achado que muda REGRA da produção → avisar o Gerente para atualizar a DOUTRINA e o painel.
Cadência: revisão da função TODA SEMANA junto da varredura de segunda-feira do Pesquisador.
