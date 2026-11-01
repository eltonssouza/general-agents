# Bilingual EN ⇄ PT-BR glossary (Pro Git)

> Sources: PGEN = Pro Git EN (Chacon/Straub, ed. 2.1.450, 2026-05-25, 501 pp.) and PGBR = Pro Git PT-BR (ed. 2.1.47, 2024-10-28, 500 pp.). Page = PDF page (PGEN printed = PDF - 6; PGBR printed = PDF - 5). The two editions do NOT have the same pagination (see `edicao-ptbr-e-numeracao.md`).

## 0. Recommended vocabulary in answers in Portuguese

Agent rule: use the English command term as the main term (it is what you type and what the PT-BR book keeps most often) and give the PT-BR book equivalent in parentheses when one exists. Only attribute a PT term to PGBR if it is in the table below; for Ch. 7, 8, 9 and most of 10 and of the appendices, PGBR is in English (see `edicao-ptbr-e-numeracao.md`). "Usual" equivalents outside the book are [extrapolation].

| Concept | EN term (command) | PGBR PT-BR term | Note |
|---|---|---|---|
| staging area | staging area / index | área de stage (dominant), área de preparo, área de preparação | three forms in PGBR (p.19-20, 26, 61) |
| working directory | working directory / working tree | diretório de trabalho | PGBR mixes in "working directory" (p.28, 48-49) |
| three states | modified, staged, committed | modificado, preparado, committed | PGBR p.19 |
| branching | branch | branch (dominant), ramificação | avoid "filial" (error, p.91) |
| merging | merge | merge / mesclagem / mesclar | also "fusão" |
| rebase | rebase | rebase (also "realocar") | |
| fast-forward | fast-forward | fast-forward (also "avanço rápido") | |
| remote repository | remote | remoto / repositório remoto | |
| plumbing / porcelain | plumbing / porcelain | encanamento / porcelana | PGBR p.420 |
| stash, reflog, bisect, blame, refspec, packfile, cherry-pick | - | no translation in PGBR (English-only terms) | use EN; a PT term would be [extrapolation] |
| interactive rebase | interactive rebase / git rebase -i | only 1 occurrence of "rebase interativo" (PGBR p.143, cross-reference); the section itself (PGBR p.243-244) is in English | use "rebase -i" |
| hook | gancho (hook) | only in GitLab (PGBR p.120); elsewhere, "hooks" | use "hook" |
| submodule | submódulos | 1 passing occurrence (PGBR p.425); section in English (p.292-315) | use "submodule" |

## 1. EN | PT-BR glossary of the book (part 1: PGBR p.10-250)

Convention of the "page" column: first page (or main pages) where the term appears in that form. "KEPT" = the book leaves it in English.

| EN term | canonical PT-BR term used in the book | PGBR page | note |
|---|---|---|---|
| version control | controle de versão (VCS = Version Control System) | 12 | "versionamento" also used (p.27, 61) |
| local VCS / centralized VCS (CVCS) / distributed VCS (DVCS) | Sistemas Locais / Centralizados / Distribuídos de Controle de Versão | 12, 13, 14 | acronyms kept in English |
| snapshot | snapshot (KEPT); "imagem"; "instantâneo" | 16-17 (imagens), 61 (instantâneos), 28+ (snapshot) | title p.16 "Imagens, Não Diferenças" (Snapshots, Not Differences); text p.17 "tira uma foto"; p.61 "snapshots (instantâneos de um momento)". Three forms for the same concept |
| checksum / SHA-1 hash | soma de verificação (checksum); hash SHA-1 | 18 | "checksum" also kept in English (p.18, 37); "soma de verificação" p.99 |
| three states (committed, modified, staged) | committed, modificado (modified), preparado (staged) | 19 | "committed" stays in English; "modificado" and "preparado" translated |
| staging area | área de preparo (p.19-20); área de preparação (staging area) (p.61); área de stage (p.26+) | 19, 61, 26 | INCONSISTENT: three forms; "área de stage" is the dominant one in chs. 2 and 5 (13 occurrences). Also "índice" (index) p.19 |
| stage (verb/state) | "stage" (KEPT): "mandar para o stage", "colocar na área de stage", "preparar" | 30, 34, 128 | "preparado (staged)" p.19, 30; "não-preparado (unstaged)" p.31; "fora do stage" p.33, 38 |
| unstage / unstaged | retirar do stage; não-preparado (unstaged) | 48, 31 | "unstage" kept (p.60 alias) |
| working directory | diretório de trabalho (p.19+, 21 occ.); working directory (p.28, 48-49, 38 occ.); work directory (p.48); cópia de trabalho (p.28, 70) | 19, 48 | INCONSISTENT: PT/EN mix, even on the same page (p.48 "work directory", p.49 "working directory") |
| Git directory | diretório Git | 19 | = .git |
| tracked / untracked | rastreado / não-rastreado | 28 | "monitorar/monitorado" on p.26-27 (start of ch. 2); "rastrear" in the rest |
| clone | clonar / clonagem; git clone | 27 | see p.27 "clone e não checkout" |
| commit (noun and verb) | commit (KEPT); "fazer commit"; "commitar" (p.139); "submeter" (p.44, 56); "confirmar" (p.62, 66); "enviar" (p.30) | 36 | plural: "commits" (p.37+, 187 occ.) AND "commites" (p.127-147, 27 occ.) - INCONSISTENT by chapter |
| commit message | mensagem de commit; "mensagem de confirmação" (p.77) | 37, 77 | |
| amend | --amend (option); "refazer o commit" | 47 | "--ammend" (typo in the book, p.70) |
| author / committer | autor / committer ("commiter" p.44) | 44 | p.44 uses "commiter" and "Committer" |
| log | git log; "retorno do comando log" | 40 | "retorno" = output on several pages |
| diff / patch | diff / patch (KEPT) | 34 | "patch" also = "correção" (p.44, 68-74 hotfix) |
| remote (repositório remoto) | repositório remoto / servidor remoto / remoto | 50 | "referências remotas" p.53, 82 |
| origin | origin (KEPT) / origin(origem) | 50 | "origem" appears in a gloss (p.50, 51, 83) |
| fetch | fetch (KEPT) / buscar | 52 | "obter" also used p.50 ("pulling(obter)") |
| pull | pull (KEPT) / "obter" / "puxar" | 50, 59 | p.50 "pushing(atualizar) e pulling(obter)"; "puxar" p.79, 83, 96 |
| push | push (KEPT) / "enviar" / "empurrar" / "publicar" / "atualizar" | 50, 88, 124 | "Empurrando (Push)" is the title p.88; "publicar (push)" dominant in ch. 5 (31 occ.) |
| tag | tag (KEPT); tag leve / tag anotada | 55-56 | "Leve" and "Anotada" translated; "tipo leve" |
| lightweight tag / annotated tag | tag de tipo leve / tag anotada | 55, 56 | |
| alias | apelido (alias) | 59 | title "Apelidos Git" |
| branch | branch (KEPT, dominant); ramificação; ramo; "filial" (error, p.91) | 52, 61, 91 | ch. 3 title "Branches no Git"; "ramo mestre" p.52; "ramos" p.10, 16, 80, 121; "branches remotos" |
| branching / merging | ramificação (branching) / mesclagem (merging) | 10, 68 | title p.68 "Ramificação (Branch) e Mesclagem (Merge)" |
| topic branch | branch por tópico / branch de tópico | 80 | |
| long-running branch | branch de longa duração | 79 | |
| master | master (KEPT) | 29 | git init "default" (p.62) |
| HEAD | HEAD (KEPT) | 63 | "ponteiro especial" |
| pointer | ponteiro | 61 | |
| checkout / checked out | checkout (KEPT); "check-out" (p.77, 90); "selecionado" (p.69) | 34+, 64 | "mudar para o branch" p.64 |
| merge (verb/noun) | merge (KEPT, 208 occ.) / mesclar / mesclagem / fundir / fusão / combinar | 52, 68, 71 | INCONSISTENT: "mesclar/mesclagem" (ch. 3), "fundi-los" (p.80, 92, 99), "fusão" (p.61, 93-95), "merge" (chs. 5-6) |
| three-way merge | mesclagem de três vias (three-way merge) | 73 | "fusão de três vias" p.79, 92 |
| merge commit | commit de merge | 73 | 0 occ. of "commit de mesclagem" |
| fast-forward | fast-forward (KEPT, 13 occ.); avanço rápido (p.95-96); fusão rápida (p.93-95) | 71, 95 | "non-fast-forward" kept in English p.124, 131 |
| merge conflict | conflito de merge | 74 | |
| unmerged | unmerged ("não mesclado") | 75 | |
| mergetool | git mergetool | 75 | |
| rebase | rebase (KEPT) / "realocar" / "rebasing" / "fazer rebase" / "rebaseando" | 92-93, 94, 144 | "realocar" only on p.94, 96, 99, 144-145; "rebaseando" p.101 |
| cherry-pick | cherry-pick / selecionado a dedo (cherry-pick) | 143 | translation only on the first occurrence |
| squash | squash / "compacta (squash)" / "comprime" | 145, 146 | git merge --squash |
| upstream | upstream (KEPT) / "branch upstream" | 90, 179 | `@{upstream}`, `@{u}` p.91; remote called "upstream" p.181 |
| tracking branch | branch de rastreamento / "tracking branch" | 82, 90 | "branch remoto de rastreamento" p.87-88 (word order varies) |
| remote-tracking branch | branch de rastreamento remoto | 82-83 | form (remoto)/(branch) |
| bare repository | repositório vazio (bare repository) | 102 | from p.107 on only "bare repository" (sections in English) |
| protocols: Local / HTTP (Smart, Dumb) / SSH / Git | Protocolo Local / HTTP "Smart" e "Dumb" / SSH / Git | 102, 104, 106, 107 | |
| hook | gancho (hook) (p.120); hooks | 120, 105 | "Git Hooks" p.105 kept in English |
| GitLab merge request | solicitação de mesclagem / pedido de mesclagem | 121 | 4 + 3 occ. only on p.121; "Os pedidos de mesclagem" |
| fork | fork (KEPT) / bifurcar / bifurcação | 121, 125, 142, 170 | "bifurcação" only p.121 and "bifurcar (fork)" p.125; "dar fork" p.173+; "fazer fork" |
| pull request | Pull Request (KEPT, 149 occ.) | 143, 171 | p.121 GitLab uses "solicitação de mesclagem"; p.143 "pedido"; "requisição" p.143, 179 |
| maintainer | mantenedor (20 occ.) / coordenador (16 occ.) | 127, 124 | "coordenadores" = integration managers in ch. 5; "Integration Manager" kept p.171 |
| Integration-Manager workflow | Fluxo de Trabalho Coordenado | 124 | |
| Dictator and Lieutenants workflow | Fluxo de Trabalho Ditador e Tenentes; "ditador benevolente" | 125 | |
| Centralized workflow | Fluxo de Trabalho Centralizado | 123 | |
| issue | issue (KEPT) / "chamado" / "problema" | 68, 134, 182 | "chamado #53" p.68; "issue #53" p.72; "Issue" p.182 |
| detached HEAD | there is NO section; it only appears in a git log line in English | 47 | incidental use, no definition |
| hunk | NOT translated; only on English pages | 228-229, 233 | "Stage this hunk" |
| stash | stash (KEPT) | 70, 229 | p.70 only mentions "o comando stash"; full section only in English p.229-234 |
| refspec | refspec (KEPT) | 139 | "Isto é chamado de refspec" |
| mbox / format-patch / send-email / imap-send | kept | 147-149 | |
| reset / reflog | kept | 49, 220 | |
| credential cache / credential helper | "credential cache" | 89 | |
| SSH key (public/private) | chave pública SSH / chave privada | 109-110 | |
| namespace | namespace (KEPT) | 119 | |
| two-factor authentication | Autenticação de Dois Fatores (2FA) | 169 | |
| avatar | avatar | 167 | |
| Task List | Task List (KEPT) | 185 | |
| Markdown | Markdown aprimorado do GitHub (p.184); "Markdown melhorado do GitHub" (p.184, 188) | 184 | two translations of "GitHub Flavored Markdown" on the same page |
| code snippet / quoting / emoji / images | Trechos de código / Citando / Emoji / Imagens | 186-188 | |
| commit guidelines | Diretrizes para Fazer Commites | 127 | title uses "Commites" |
| private small team / private managed team | Time Pequeno Privado / Time Privado Gerenciado | 129, 136 | |
| forked public project | Fork de Projeto Público | 142 | |
| public project over email | Projeto Público através de Email | 146 | |
| summary (end of ch.) | Sumário (chs. 1-4: p.25, 60, 101, 122) / Resumo (ch. 5: p.126, 149) | 25 | INCONSISTENT between chapters |
| section | seção / "sessão" (error: p.48, 55) | 30, 48 | |
| git dir terms: Staging/Unstaging via git reset | "retirar do stage" | 48 | |
| word-diff | --word-diff | 173 | |
| upstream (remote) | upstream | 181 | |
| patch email workflow | Projeto Público através de Email | 146 | git format-patch, git send-email |

#### 1.1 Terms that PT-BR KEEPS in English (confirmed in the reading)
commit, branch, merge, rebase, fetch, pull, push, stage, snapshot, checkout, HEAD, master, origin, tag, stash, squash, cherry-pick, fast-forward, hook (sometimes), refspec, patch, diff, log, status, tracking branch, upstream, fork, Pull Request, issue, namespace, avatar, Task List, Markdown, checksum, committed, bare repository, hash. Command outputs (e.g. "Changes to be committed", "Untracked files", "nothing to commit") stay in English throughout the text (p.28-31, 38, 48-49, 74-76).

#### 1.2 Terms with inconsistent translation (summary)
1. staging area: área de preparo (p.19-20) / área de preparação (p.61) / área de stage (p.26+) / stage.
2. working directory: diretório de trabalho / working directory / work directory / cópia de trabalho.
3. branch: branch / ramificação / ramo / "filial" (p.91, 2 occ.) / "ramo mestre" (p.52).
4. merge: mesclar / mesclagem / fundir / fusão / merge / combinar.
5. push: enviar / empurrar / publicar / atualizar / push (ch. 5 prefers "publicar").
6. fetch/pull: buscar / obter / baixar / puxar.
7. commit (pl.): commits (chs. 2-3, 6) vs commites (ch. 5, p.127-147).
8. snapshot: snapshot / imagem / instantâneo.
9. rebase: rebase / realocar / rebasear (rebaseando) / fazer rebase.
10. fast-forward: fast-forward / avanço rápido / fusão rápida.
11. fork: fork / bifurcar / bifurcação.
12. pull request: Pull Request / solicitação de mesclagem (GitLab, p.121) / pedido / requisição.
13. section: seção / sessão (p.48, 55).
14. "GitHub Flavored Markdown": Markdown aprimorado / melhorado (p.184).
15. end of chapter: Sumário / Resumo.
16. coordenador vs mantenedor (maintainer / integration manager).
17. example domain: git.ourcompany.com (p.83) vs git.nossaempresa.com (p.85).
18. cross-refs: section titles sometimes in PT ("Fundamentos de Git", "Funcionamento Interno do Git", "Branches no Git", "Desfazendo coisas"), sometimes in EN ("Getting Git on a Server" p.27/51/103/107, "Distributed Git" p.44/82/176, "Credential Storage" p.89/106, "Git Hooks" p.105, "Data Recovery" p.50, "Reset Demystified" p.49, "Stashing and Cleaning" p.70, "Advanced Merging" p.76, "Interactive Staging" p.128, "Rewriting History" p.128/143, "Commit Ranges" p.134, "The Refspec" p.139, "Rebasing and Cherry-Picking Workflows" p.143, "Determining What Is Introduced" p.154/178; "Git Tools" p.165 vs "Ferramentas do Git" p.171). Also table labels in English (p.44 "Useful options for git log --pretty=format"; p.45 "Common options to git log"; p.46 "Options to limit the output of git log"), figure caption in English (p.100 "Rebase on top of force-pushed rebase work."; p.116 "The GitWeb web-based user interface."), and broken xrefs "<< ch01-introdução # ch01-introdução >>" (p.61, 2x).


## 2. Glossary (part 2: PGBR p.217-500)

Convention: "(not translated)" = only the English term exists in PGBR. "(keep EN)" = the PT passage itself keeps the term in English. Page = where I read the term/usage.

#### 2.1 Data concepts and Internals (real PT passages, p.420-434, 453-459)
| EN term | PT-BR term in the book | page | note |
|---|---|---|---|
| plumbing | encanamento ("comandos de encanamento"; "(plumbing)") | 420 | translated; also 458 |
| porcelain | porcelana ("comandos porcelana"; "(porcelain)") | 420 | translated |
| Git Internals | Funcionamento Interno do Git | 420 | title of ch. 10; EN xrefs use the same name (p.219, 287, 356, 412, 495) |
| VCS | VCS (keep EN) | 420 | acronym not expanded |
| content-addressable filesystem | sistema de arquivos de conteúdo endereçável | 420 | translated |
| .git directory | diretório .git | 420 | |
| hooks | hooks (keep EN); "scripts hooks" | 421 | xref "Git Hooks" at 421 stays in English |
| objects | objetos; "diretório objects" | 421 | "Objetos do Git" is a section title |
| key-value store | armazenamento chave-valor; "chave" | 421 | "chave" at 421-423, 434 |
| object database | banco de dados | 421 | also 422, 424, 431 |
| staging area / index | área de stage; index | 421, 424, 425 | "stage" kept EN; "area de staging" does NOT occur |
| hash-object | hash-object | 421 | plumbing command |
| SHA-1 hash / checksum | hash SHA-1; checksum | 422 | "checksum hash de 40 caracteres": synonyms coexist |
| header | cabeçalho | 422, 429 | |
| cat-file | cat-file; "canivete suíço" | 422 | |
| blob | blob; "objeto blob" | 423 | kept EN |
| tree | tree; "árvore" 1x; "objeto tree"; "Objetos Tree" | 423 | "tree (árvore)" only in the definition |
| commit object | objeto commit; "Objetos Commit" | 426, 427 | |
| snapshot | snapshot | 426 | kept EN |
| working directory | diretório de trabalho | 426 | in ch. 7 "Working Directory" (EN) appears 250-251 |
| update-index / --cacheinfo / --add | commands kept; "opção --add" | 424 | |
| write-tree / read-tree --prefix | same | 425 | |
| submodule | submódulos (only in passing) | 425 | valid modes 100644, 100755, 120000 (424-425) |
| symbolic link | link simbólico | 424 | mode 120000 |
| commit-tree | commit-tree | 426, 427 | |
| author / committer | autor/commiter | 427 | spelling "commiter" |
| timestamp | timestamp (keep EN) | 427, 455 | |
| object storage (zlib) | armazenamento de objetos; "comprime com zlib" | 429, 430 | |
| reference / ref | referência(s); refs | 430, 431 | "referências (references) ou refs" (431) |
| update-ref | update-ref | 431 | recommended instead of editing the ref file |
| branch | branch (gender fluctuates: "a branch") | 421, 431 | |
| HEAD / symbolic reference | A HEAD; referência simbólica | 432 | title with feminine article |
| symbolic-ref | symbolic-ref | 432, 433 | |
| tag object | objeto tag; "Tags" | 433 | |
| annotated / lightweight tag | tag anotada / tag leve | 433 | translated |
| remote | remote; "remoto" 1x; "Remotes" | 434 | "remoto" only in the definition |
| push | push (keep EN) | 434 | |
| maintainer | mantenedor | 434 | |
| environment variables | variáveis de ambiente | 453 | title "Variáveis de ambiente" |
| global behavior | Comportamentos globais | 453 | |
| pathspec | pathspec (keep EN) | 454 | title "Pathspecss" (error) |
| wildcards | curingas ("curingas (wildcards)") | 454 | |
| making commits | Fazendo commits | 454 | vs "Fazendo Commit das Suas Alterações" (485) |
| network and Internet | Rede e Internet | 455 | |
| summary | Sumário (458) / Resumo (471) | 458, 471 | INCONSISTENT; EN "Summary" at 269, 333, 364, 386, 419, 465 |
| plumbing commands | comandos de encanamento | 458 | |
| other environments | Git em Outros Ambientes | 460 | title of App. A |

#### 2.2 Ch. 10 terms that stay in English (p.435-452)
| EN term | PT term in the book | page | note |
|---|---|---|---|
| packfile | (not translated) | 435-437 | "packfile" 436 |
| loose object | (not translated) | 436 | |
| delta | (not translated) | 436 | |
| git gc | (not translated) | 436, 446 | gc = garbage collect (446) |
| dangling | (not translated) | 437 | blobs without a commit (437, 449) |
| verify-pack | (not translated) | 437 | |
| refspec | (not translated) | 438-441 | "The Refspec" 438; "Pushing Refspecs" 440 |
| dumb / smart protocol | (not translated) | 441, 443 | |
| send-pack / receive-pack / fetch-pack / upload-pack | (not translated) | 443, 445 | |
| auto gc | (not translated) | 446 | |
| packed-refs | (not translated) | 447 | |
| reflog | (not translated) | 448 | "git reflog", "git log -g" |
| git fsck | (not translated) | 449 | |
| git prune / count-objects | (not translated) | 452, 453 | |

#### 2.3 Ch. 7 Git Tools (entirely in English; no PT term)
| EN term | PT term in the book | page | note |
|---|---|---|---|
| Revision Selection / short SHA-1 | (not translated) | 217 | minimum 4 characters |
| reflog / RefLog Shortnames | (not translated) | 220 | HEAD@{n} |
| ancestry (^ and ~) | (not translated) | 221 | |
| commit ranges (double/triple dot) | (not translated) | 222-224 | --left-right 224 |
| interactive staging | (not translated) | 225 | git add -i / --interactive |
| hunk / staging patches | (not translated) | 228, 229 | git add -p |
| stash | (not translated) | 229-234 | "git stash save" 230; --patch 233 |
| git clean | (not translated) | 234 | |
| signing / GPG | (not translated) | 235-239 | user.signingkey 235 |
| git grep | (not translated) | 239 | |
| pickaxe / line log | (not translated; "pickaxe" does NOT appear) | 241, 242 | -S and -L |
| amend | (not translated) | 243 | |
| interactive rebase | (body not translated; "rebase interativo" only in a cross-reference, PGBR p.143) | 244 | git rebase -i |
| squash / fixup / reorder / split | (not translated) | 244-247 | |
| filter-branch | (not translated) | 248 | |
| reset (soft/mixed/hard) | (not translated) | 249, 258-261 | "Reset Demystified" |
| three trees | (not translated) | 249-251 | HEAD, Index, Working Directory |
| merge conflict | (not translated) | 270 | PT xref "Conflitos Básicos de Merge" |
| ours / theirs | (not translated) | 275, 278, 284-285 | -Xours/-Xtheirs 285 |
| rerere | (not translated) | 288 | |
| subtree merge | (not translated) | 286 | |
| blame | (not translated) | 294 | "File Annotation" |
| bisect | (not translated) | 295 | "Binary Search" |
| submodule | (not translated) | 297 | |
| detached HEAD | (not translated) | 305 | |
| bundle | (not translated) | 316 | |
| replace | (not translated) | 320, 326 | |
| credential helper | (not translated) | 328-331 | |

#### 2.4 Ch. 8, 9 and appendices
| EN term | PT term in the book | page | note |
|---|---|---|---|
| git config | (not translated); xref "Começando" | 334 | |
| git attributes / smudge / clean filters | (not translated) | 344, 348 | |
| export-ignore / export-subst | (not translated) | 350, 351 | |
| merge strategies | (not translated) | 352 | |
| hooks (client/server) | (not translated) | 352-364 | pre-commit 353; pre-receive and update 355 |
| git svn / dcommit | (not translated) | 366-370 | |
| remote helper | (not translated) | 376, 384 | |
| Git Fusion | (not translated) | 386 | |
| git-p4 | (not translated) | 394 | |
| fast-import | (not translated) | 405, 412 | |
| gitk / git-gui | (not translated) | 460 | "Graphical Interfaces" EN |
| Libgit2, JGit | (not translated) | 472, 477 | |
| Setup and Config ... Plumbing Commands | (not translated) | 482-495 | |
| "Chaves SSH" in the index | loose PT in the EN index ("SSH keys" at 498) | 496 | inconsistency |


## 3. Translation inconsistencies and errors recorded in PGBR (part 2)

1. "Sumário" (458) vs "Resumo" (471) for "Summary"; in the other chapters the title stays "Summary".
2. "Pathspecss" (454, title with a doubled s).
3. "Commites" in "Diretrizes para Fazer Commites" (484, xref); "Fazendo commits" (454) vs "Fazendo Commit das Suas Alterações" (485).
4. "Rebase quando vocês faz Rebase" (489, xref with an agreement error).
5. Stage: "área de stage" (421, 424, 425) / "index" (424, 425) / "Stage" in "Dentro e Fora do Stage" (484, 485); in ch. 7 EN uses "staging area" (217, 225, 228, 243, 250).
6. Working dir: "diretório de trabalho" (426) vs "Working Directory" (EN, 250-251).
7. Gender fluctuates: "a branch" (421) and "a HEAD" (432).
8. hash/checksum/chave/SHA-1 used as synonyms (422).
9. Typos in the PT body: "esteriótipo" (420), "trẽs" (421), "armazendo" (422), "sitema" (423), "exitem" (433), "apotar" and "commando" (434), "prórprias" and "a um baixo mais nível" (458), "cotidiando" (471).
10. Translated labels with EN caption: "Figura 151. Git directory objects..." (432); "Figura 152-164" (461-470); "NOTA" with EN body.
11. p.421 cites "Git Hooks" with an EN title in a PT sentence.
12. Titles: "Objetos Tree"/"Objetos Commit" (PT noun + EN type), "Tags"/"Remotes" (EN) vs "A HEAD" (PT).
13. Index (496-499): "Chaves SSH" in loose PT among EN entries.
14. The extracted text is intact in UTF-8 (accents correct); accent loss only occurs if the Windows terminal decodes as cp1252.
15. "Notas de Tradução" (500) is boilerplate text of the translation repository, not Pro Git content.

