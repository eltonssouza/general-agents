# PT-BR vs EN edition: page numbering, partial translations and gaps

> Executive summary: PGEN (ed. 2.1.450, 2026) and PGBR (ed. 2.1.47, 2024, a translation of an old version written for Git 2.0.0, PGBR p.20) do NOT have the same pagination nor the same content. PGBR PDF page = PGEN PDF page minus 4 to 9 up to Ch. 7, and varies afterwards. PGBR only translates the body up to p.188 (mid-page) and Ch. 10 up to p.434; the rest is in English. Always cite the edition: `(PGEN p.N)` / `(PGBR p.N)`.

## Page convention
- All citations in the package use the PDF page (PAGE N marker of the extracted text). Printed page: PGEN = PDF - 6 (e.g.: Introduction printed 8, PDF 14); PGBR = PDF - 5.
- The EN TOC (PDF 3-6) lists printed pages; add 6. The EN back-of-book index (PDF 499-501) also uses printed pages (PGEN, see `apendices-e-mapa-de-comandos.md`).

## Chapter map (PDF)
| Chapter | PGEN | PGBR |
|---|---|---|
| Introduction | 14 | 10 |
| 1 Getting Started / Começando | 16 | 12 |
| 2 Git Basics / Fundamentos de Git | 32 | 26 |
| 3 Git Branching / Branches no Git | 69 | 61 |
| 4 Git on the Server / Git no servidor | 111 | 102 |
| 5 Distributed Git | 132 | 123 |
| 6 GitHub | 172 | 165 |
| 7 Git Tools | 224 | 217 |
| 8 Customizing Git | 342 | 334 |
| 9 Git and Other Systems | 373 | 365 |
| 10 Git Internals / Funcionamento Interno do Git | 420 | 420 |
| Appendix A | 459 | 460 |
| Appendix B | 472 | 472 |
| Appendix C | 484 | 482 |
| Index | 499-501 | 496-499 |

Source: PGEN p.3-6 (TOC) and PGBR p.10-500; see the detailed tables below.

## Content differences
- PGEN has the section 'Your default branch name' (PGEN p.29, init.defaultBranch); PGBR does not (no occurrence of init.defaultBranch in PGBR).
- PGEN covers git switch/restore (PGEN p.55-56, 66, 76); PGBR mentions neither git switch nor git restore.
- PGEN p.255 recommends git-filter-repo in place of filter-branch; PGBR does not cite filter-repo.
- PGEN Ch. 6 and parts of 4/5 are up to date; PGBR has GitLab (p.117-121) with an old version. [DATED]
- PGBR p.500 is a template text of the translation project, not book content.

## Detail 1: section map of PGBR p.10-250 and comparison with PGEN

Format: PT title (EN title) | PGBR | PGEN | difference (EN - PT). PT titles checked as an isolated line on the page (automatic verification); EN likewise. "(EN in PT)" = title/body in English inside the PT-BR.

| PT title (EN title) | PGBR | PGEN | diff |
|---|---|---|---|
| Introdução (Introduction) | 10 | 14 | +4 |
| Começando (Getting Started) [ch. 1] | 12 | 16 | +4 |
| Sobre Controle de Versão (About Version Control) | 12 | 16 | +4 |
| Sistemas Locais de Controle de Versão | 12 | 16 | +4 |
| Sistemas Centralizados de Controle de Versão | 13 | 17 | +4 |
| Sistemas Distribuídos de Controle de Versão | 14 | 18 | +4 |
| Uma Breve História do Git (A Short History of Git) | 16 | 20 | +4 |
| O Básico do Git (What is Git?) | 16 | 20 | +4 |
| Imagens, Não Diferenças (Snapshots, Not Differences) | 16 | 20 | +4 |
| Quase Todas as Operações são Locais (Nearly Every Operation Is Local) | 17 | 21 | +4 |
| Git Tem Integridade (Git Has Integrity) | 18 | 22 | +4 |
| O Git Geralmente Somente Adiciona Dados (Git Generally Only Adds Data) | 18 | 22 | +4 |
| Os Três Estados (The Three States) | 19 | 22 | +3 |
| A Linha de Comando (The Command Line) | 20 | 24 | +4 |
| Instalando o Git (Installing Git) | 20 | 24 | +4 |
| Instalando no Linux / Mac / Windows / da Fonte | 20 / 21 / 22 / 22 | 24 / 25 / 25 / 26 | +4/+4/+3/+4 |
| Configuração Inicial do Git (First-Time Git Setup) | 23 | 27 | +4 |
| Sua Identidade / Seu Editor (Your Identity / Your Editor) | 24 | 28 | +4 |
| (EN: Your default branch name) | ABSENT in PT | 29 | new section in EN; PT does not have it (and does not mention init.defaultBranch, 0 occurrences) |
| Testando Suas Configurações (Checking Your Settings) | 24 | 29 | +5 |
| Pedindo Ajuda (Getting Help) | 25 | 30 | +5 |
| Sumário cap. 1 (Summary) | 25 | 31 | +6 |
| Fundamentos de Git (Git Basics) [ch. 2] | 26 | 32 | +6 |
| Obtendo um Repositório Git (Getting a Git Repository) | 26 | 32 | +6 |
| Gravando Alterações em Seu Repositório (Recording Changes to the Repository) | 28 | 34 | +6 |
| Status Curto (Short Status) | 31 | ~37 | +6 |
| Ignorando Arquivos (Ignoring Files) | 32 | 38 | +6 |
| Visualizando Suas Alterações Dentro e Fora do Stage (Viewing Your Staged and Unstaged Changes) | 33 | ~39 | +6 |
| Fazendo Commit das Suas Alterações (Committing Your Changes) | 36 | ~42 | +6 |
| Pulando a Área de Stage (Skipping the Staging Area) | 37 (end)-38 | ~43 | +6 |
| Removendo Arquivos / Movendo Arquivos | 38 / 39 | ~44 / ~45 | +6 |
| Vendo o histórico de Commits (Viewing the Commit History) | 40 | 46 | +6 |
| Limitando o retorno do comando Log | 45 | ~51 | +6 |
| Desfazendo coisas (Undoing Things) | 47 | 52 | +5 |
| Trabalhando de Forma Remota (Working with Remotes) | 50 | 56 | +6 |
| Criando Tags (Tagging) | 55 | 61 | +6 |
| Apelidos Git (Git Aliases) | 59 | 66 | +7 |
| Sumário cap. 2 | 60 | ~68 | +8 |
| Branches no Git (Git Branching) [ch. 3] | 61 | 69 | +8 |
| Branches em poucas palavras (Branches in a Nutshell) | 61 | 69 | +8 |
| O básico de Ramificação (Branch) e Mesclagem (Basic Branching and Merging) | 68 | 76 | +8 |
| Gestão de Branches (Branch Management) | 77 | 85 | +8 |
| Fluxo de Branches (Branching Workflows) | 79 | 88 | +9 |
| Branches remotos (Remote Branches) | 82 | 91 | +9 |
| Empurrando (Push) / Rastreando Branches / Fazendo o Pull / Removendo Branches remotos | 88 / 90 / 91 / 92 | ~97 / ~99 / ~100 / 100 | +9 |
| Rebase (Rebasing) | 92 | 101 | +9 |
| Os perigos do Rebase (The Perils of Rebasing) | 97 | 106 | +9 |
| Rebase vs. Merge | 101 | ~109 | +8 |
| Sumário cap. 3 | 101 | 110 | +9 |
| Git no servidor (Git on the Server) [ch. 4] | 102 | 111 | +9 |
| Os Protocolos (The Protocols) / Protocolo Local | 102 | 111 | +9 |
| O Protocolo HTTP (HTTP Smart / HTTP Dumb) | 104 | 113 | +9 |
| O Protocolo SSH | 106 | 114 | +8 |
| O Protocolo Git | 107 | 115 | +8 |
| Getting Git on a Server (EN in PT) | 107 | 116 | +9 |
| Putting the Bare Repository on a Server (EN in PT) | 108 | 117 | +9 |
| Small Setups / SSH Access (EN in PT) | 109 | 117-118 | +8/+9 |
| Gerando Sua Chave Pública SSH (PT) | 109 | 118 | +9 |
| Setting Up the Server (EN in PT) | 111 | 119 | +8 |
| Git Daemon (EN in PT) | 113 | 122 | +9 |
| Smart HTTP (EN in PT) | 114 | 123 | +9 |
| GitWeb (EN in PT) | 116 | 125 | +9 |
| GitLab (PT, after the EN intro of GitWeb) | 117 | 127 | +10 |
| Instalação / Administração (GitLab) | 118 | 127 | +9 |
| Usuários / Grupos / Projetos / Ganchos (hooks) | 119 / 119 / 120 / 120 | 127-129 | +9 |
| Uso Básico / Trabalhando juntos (GitLab) | 121 | 129-130 | +8/+9 |
| Third Party Hosted Options (EN in PT) | 122 | 130 | +8 |
| Sumário cap. 4 | 122 | 131 | +9 |
| Distributed Git (title+intro EN) [ch. 5] | 123 | 132 | +9 |
| Fluxos de Trabalho Distribuídos / Centralizado | 123 | 132 | +9 |
| Fluxo de Trabalho Coordenado | 124 | 133 | +9 |
| Fluxo de Trabalho Ditador e Tenentes | 125 | 134 | +9 |
| Padrões para Controlar Branches de Código Fonte | 126 | 134 | +8 |
| Resumo do Fluxo de Trabalho | 126 | 135 | +9 |
| Contribuindo com um Projeto (Contributing to a Project) | 126 | 135 | +9 |
| Diretrizes para Fazer Commites (Commit Guidelines) | 127 | 136 | +9 |
| Time Pequeno Privado (Private Small Team) | 129 | 137 | +8 |
| Time Privado Gerenciado (Private Managed Team) | 136 | 144 | +8 |
| Fork de Projeto Público (Forked Public Project) | 142 | 149 | +7 |
| Projeto Público através de Email (Public Project over Email) | 146 | 153 | +7 |
| Resumo (Summary) | 149 | 156 | +7 |
| Maintaining a Project (EN in PT) to the end of ch. 5 | 149 (end)-164 | 156-171 | +7 |
|   Working in Topic Branches / Applying Patches from Email (apply, am) | 150 / 150 | 157 / 157-158 | +7 |
|   Checking Out Remote Branches / Determining What Is Introduced | 153 / 154 | 160 / 161 | +7 |
|   Integrating Contributed Work / Merging Workflows / Large-Merging Workflows | 155 / 156 / 158 | 162 / 162 / 165 | +7 |
|   Rebasing and Cherry-Picking Workflows / Rerere / Tagging Your Releases | 159 / 161 / 161 | 166 / 168 / 168 | +7 |
|   Generating a Build Number / Preparing a Release / The Shortlog / Summary | 162 / 163 / 163 / 164 | 169 / 170 / 170 / 171 | +7 |
| GitHub [ch. 6] (title+intro+WARNING EN, rest PT) | 165 | 172 | +7 |
| Configurando uma conta (Account Setup and Configuration) | 165 | 172 | +7 |
| Acesso SSH / Seu Avatar / Seus endereços de email / Autenticação de Dois Fatores | 166 / 167 / 169 / 169 | 173 / 174 / 176 / 176 | +7 |
| Contribuindo em um projeto / Fazendo Fork de projetos | 170 | 177 | +7 |
| O fluxo do GitHub (The GitHub Flow) / Criando um Pull Request | 171 | 178 | +7 |
| Interagindo em um Pull Request (Iterating on a Pull Request) | 175 | 182 | +7 |
| Pull Requests Avançados / Pull Requests como Patches / Mantendo-se no Upstream | 179 | 186 | +7 |
| Referências (References) | 182 | 188 | +6 |
| Markdown aprimorado do GitHub (GitHub Flavored Markdown) | 184 | 190 | +6 |
| Task Lists / Trechos de código / Citando / Emoji / Imagens | 185 / 186 / 186 / 187 / 188 | 191 / 192 / 193 / 194 / 195 | +6/+7 |
| Maintaining a Project (GitHub; EN in PT) / Creating a New Repository | 189 | 197 | +8 |
|   Adding Collaborators / Managing Pull Requests / Email Notifications | 191 / 192 / 193 | 198 / 199 / 200 | +7 |
|   Collaborating on the PR / Pull Request Refs / PRs on PRs | 194 / 195 / 197 | 201 / 202 / 204 | +7 |
|   Mentions and Notifications / Notifications Page / Web, Email notif. | 198 / 199 / 200-201 | 205 / 206 / 207-208 | +7 |
|   Special Files (README, CONTRIBUTING) / Project Administration | 201-202 / 202 | 208-209 / 209 | +7 |
|   Changing the Default Branch / Transferring a Project | 203 | 210 | +7 |
|   Managing an organization (Organization Basics, Teams, Audit Log) | 204-206 | 211-213 | +7 |
|   Scripting GitHub (Services and Hooks, GitHub API, Octokit) / Summary | 207-216 | 214-223 | +7 |
| Git Tools (ch. 7; title and body EN) / Revision Selection (Single Revisions, Short SHA-1) | 217 | 224 | +7 |
|   Branch References / RefLog Shortnames / Ancestry References | 219 / 220 / 221 | 226 / 226 / 228 | +7 |
|   Commit Ranges (Double Dot, Multiple Points, Triple Dot) | 222-224 | 230-231 | +8 |
|   Interactive Staging / Staging and Unstaging Files / Staging Patches | 225 / 225 / 228 | 232 / 232 / 234 | +7 |
|   Stashing and Cleaning (Stashing Your Work, Creative Stashing, Branch from Stash, Cleaning) | 229-234 | 236-241 | +7 |
|   Signing Your Work (GPG, Signing Tags, Verifying Tags, Signing Commits, Everyone Must Sign) | 235-239 | 242-246 | +7 |
|   Searching (Git Grep, Git Log Searching, Line Log Search) | 239-242 | 245-248 | +6/+7 |
|   Rewriting History (Changing Last Commit, Multiple Messages, Reordering, Squashing, Splitting, filter-branch) | 243-249 | 249-256 | +6/+7 |
|   Reset Demystified (The Three Trees) | 249 | 257 | +8 |

Summary of the drift: PT = EN - 4 up to ~p.16-30; -6 in ch. 2; -8/-9 in chs. 3-5; -7 in chs. 6-7. To find the equivalent page in EN for a PT page, add ~4 (ch. 1), ~6 (ch. 2), ~8-9 (chs. 3-5), ~7 (chs. 6-7); always confirm by title. The entries marked "~" in PGEN are estimates (I only checked by title those without "~"); PGBR for the whole table was read/confirmed on the pages.


## Detail 2: passages still in English in PGBR (p.10-250)

Method: count of accented letters per page (0 = English) + reading. Intervals within the 10-250 scope:
- p.107 (from "Getting Git on a Server", final part) to mid-p.109 (up to before "Gerando Sua Chave Pública SSH"): Getting Git on a Server, Putting the Bare Repository on a Server, Small Setups, SSH Access.
- p.111-116 in full and top of p.117: Setting Up the Server, Git Daemon, Smart HTTP (git-http-backend), GitWeb (git instaweb). p.117 mixes: GitWeb in English up to "Embora o GitWeb..." and GitLab in PT.
- p.122 (middle): Third Party Hosted Options (in English); the Summary of ch. 4 goes back to PT on the same page.
- p.123 (top): title "Distributed Git" and 2 opening paragraphs of ch. 5 in English; from "Fluxos de Trabalho Distribuídos" it goes back to PT.
- p.149 (end) to p.164 in full: "Maintaining a Project" (ch. 5: Working in Topic Branches, Applying Patches from Email, Checking Out Remote Branches, Determining What Is Introduced, Integrating Contributed Work, Merging Workflows, Large-Merging Workflows, Rebasing and Cherry-Picking Workflows, Rerere, Tagging Your Releases, Generating a Build Number, Preparing a Release, The Shortlog, Summary). There are 16 pages without a single accented letter (150-164).
- p.165 (top): title "GitHub", opening paragraphs and WARNING "Interfaces Change" in English; PT starts at "Configurando uma conta".
- p.189 (end) to p.216: "Maintaining a Project" of GitHub (Creating a New Repository ... Octokit, Summary): 28 pages 190-216 without accents (p.201 has 3 accents only because of a PT figure caption cited).
- p.217-250 (the whole of ch. 7 "Git Tools" read so far): Revision Selection, Commit Ranges, Interactive Staging, Stashing and Cleaning, Signing Your Work, Searching, Rewriting History, Reset Demystified (start). 0 accents in 217-250.
- Out of scope (count only): 251-419 also without accents (English); accented letters reappear in 420-434, 453-455, 458-460, 487, 493, 500 (probably appendices/last pages translated; not verified).
- Small English passages inside PT pages: see 1.2 item 18 (table labels p.44-46, captions p.100/116, title p.52 "Pushing to Your Remotes", xrefs).
- The index itself (p.1-9) was not read (out of scope).


## Detail 3: section map of PGBR p.217-500 and English passages

Chapter start (PGEN = Git-Pro-Git-EN.txt, detected by title on the 1st line of the page):
| Chapter | PGEN p. | PGBR p. | Title in PGBR |
|---|---|---|---|
| 7 Git Tools | 224 | 217 | "Git Tools" (English) |
| 8 Customizing Git | 342 | 334 | "Customizing Git" (English) |
| 9 Git and Other Systems | 373 | 365 | "Git and Other Systems" (English) |
| 10 Git Internals | 420 | 420 | "Funcionamento Interno do Git" (PT) |
| App. A Git in Other Environments | 459 | 460 | "Apêndice A: Git em Outros Ambientes" (PT) |
| App. B Embedding Git in your Applications | 472 | 472 | "Apêndice B: Embedding Git in your Applications" (mixed) |
| App. C Git Commands | 484 | 482 | "Apêndice C: Git Commands" (mixed) |
| Index | - | 496 | "Index" (English, with "Chaves SSH" and "Comandos git push" loose) |
| Translation Notes ("Notas de Tradução") | - | 500 | PT (template text of the translation project, not book content) |
Note: the PGEN-PGBR offset goes from -7 (ch. 7) to -8 (ch. 8/9), 0 (ch. 10) and +1/-2 in the appendices; do not use a fixed offset between the two PDFs.

#### Ch. 7 Git Tools (PGBR p.217-333; ALL in English)
Revision Selection 217 > Single Revisions 217 > Short SHA-1 217 > Branch References 219 > RefLog Shortnames 220 > Ancestry References 221 > Commit Ranges 222 > Double Dot 223 > Multiple Points 224 > Triple Dot 224.
Interactive Staging 225 > Staging and Unstaging Files 225 > Staging Patches 228.
Stashing and Cleaning 229 > Stashing Your Work 230 > Creative Stashing 232 > Creating a Branch from a Stash 233 > Cleaning your Working Directory 234.
Signing Your Work 235 > GPG Introduction 235 > Signing Tags 235 > Verifying Tags 236 > Signing Commits 237 > Everyone Must Sign 239.
Searching 239 > Git Grep 239 > Git Log Searching 241 > Line Log Search 242.
Rewriting History 243 > Changing the Last Commit 243 > Changing Multiple Commit Messages 243 > Reordering Commits 245 > Squashing Commits 246 > Splitting a Commit 247 > The Nuclear Option: filter-branch 248 > Removing a File from Every Commit 248 > Making a Subdirectory the New Root 248 > Changing Email Addresses Globally 249.
Reset Demystified 249 > The Three Trees 249 > The HEAD 250 > The Index 250 > The Working Directory 251 > The Workflow 251 > The Role of Reset 257 > Step 1: Move HEAD 258 > Step 2 (--mixed) 259 > Step 3 (--hard) 260 > Recap 261 > Reset With a Path 262 > Squashing 264 > Check It Out 267 > Summary (table) 269.
Advanced Merging 269 > Merge Conflicts 270 > Aborting a Merge 272 > Ignoring Whitespace 273 > Manual File Re-merging 273 > Checking Out Conflicts 276 > Merge Log 278 > Combined Diff Format 279 > Undoing Merges 281 > Other Types of Merges 284 > Our or Theirs Preference 284 > Subtree Merging 286 > Rerere 288.
Debugging with Git 294 > File Annotation 294 > Binary Search 295.
Submodules 297 > Starting with Submodules 297 > Cloning a Project with Submodules 299 > Working on a Project with Submodules 301 > Pulling in Upstream Changes 301 > Working on a Submodule 305 > Publishing Submodule Changes 308 > Merging Submodule Changes 309 > Submodule Tips 311 > Submodule Foreach 311 > Useful Aliases 313 > Issues with Submodules 314.
Bundling 316 > Replace 320 > Credential Storage 328 > Under the Hood 329 > A Custom Credential Cache 331 > Summary 333.

#### Ch. 8 Customizing Git (PGBR p.334-364; ALL in English)
Git Configuration 334 > Basic Client Configuration 334 > Colors in Git 337 > External Merge and Diff Tools 338 > Formatting and Whitespace 341 > Server Configuration 343.
Git Attributes 344 > Binary Files 344 > Identifying Binary Files 344 > Diffing Binary Files 345 > Keyword Expansion 347 > Exporting Your Repository 350 > Merge Strategies 352.
Git Hooks 352 > Installing a Hook 352 > Client-Side Hooks 353 > Committing-Workflow Hooks 353 > Email Workflow Hooks 353 > Other Client Hooks 354 > Server-Side Hooks 354.
An Example Git-Enforced Policy 355 > Server-Side Hook 355 > Enforcing a Specific Commit-Message Format 356 > Enforcing a User-Based ACL System 357 > Testing It Out 360 > Client-Side Hooks 361 > Summary 364.

#### Ch. 9 Git and Other Systems (PGBR p.365-419; ALL in English)
Git as a Client 365 > Git and Subversion 365 > Setting Up 366 > Getting Started 366 > Committing Back to Subversion 368 > Pulling in New Changes 369 > Git Branching Issues 371 > Subversion Branching 372 > Creating a New SVN Branch 372 > Switching Active Branches 373 > Subversion Commands 373 > SVN Style History 373 > SVN Annotation 374 > SVN Server Information 374 > Ignoring What Subversion Ignores 375.
Git and Mercurial 376 > Getting Started 376 > Workflow 378 > Branches and Bookmarks 380 > Mercurial Summary 383.
Git and Bazaar 383 > Bazaar branches 384 > Caveats 385 > Summary 386.
Git and Perforce 386 > Git Fusion 386 > Setting Up 386 > Fusion Configuration 388 > Workflow 390 > Git-Fusion Summary 393 > Git-p4 394 > Setting Up 394 > Getting Started 394 > Workflow 395 > Branching 400 > Git and Perforce Summary 401.
Migrating to Git 402 > Subversion 402 > Mercurial 404 > Bazaar 407 > Perforce 410 (Perforce Git Fusion 410; Git-p4 410) > A Custom Importer 411 > Summary 419.

#### Ch. 10 Funcionamento Interno do Git (PGBR p.420-459; PT up to p.434, then mixed)
Encanamento e Porcelana 420 > Objetos do Git 421 > Objetos Tree 423 > Objetos Commit 426 > Armazenamento de Objetos 429 > Referências do Git 430 > A HEAD 432 > Tags 433 > Remotes 434 > Packfiles 435 (title and body EN) > The Refspec 438 > Pushing Refspecs 440 > Deleting References 441 > Transfer Protocols 441 > The Dumb Protocol 441 > The Smart Protocol 443 > Uploading Data 443 > Downloading Data 445 > Protocols Summary 446 > Maintenance and Data Recovery 446 > Maintenance 446 > Data Recovery 447 > Removing Objects 449 > Variáveis de ambiente 453 (PT) > Comportamentos globais 453 (PT) > Repository Locations 453 (EN) > Pathspecss 454 (PT, typo) > Fazendo commits 454 (PT) > Rede e Internet 455 (PT) > Diffing and Merging 455 (EN) > Debugging 456 (EN) > Miscellaneous 458 (EN) > Sumário 458 (PT, ends on p.459).

#### Appendix A Git em Outros Ambientes (PGBR p.460-471)
Apêndice A + introductory paragraph 460 (PT) > Graphical Interfaces 460 > gitk and git-gui 460 > GitHub for Mac and Windows 462 > Installation 464 > Recommended Workflow 464 > Summary 465 > Other GUIs 465 > Git in Visual Studio 465 > Git in Eclipse 467 > Git in Bash 467 > Git in Zsh 468 > Git in Powershell 470 > Resumo 471 (PT).

#### Appendix B Embedding Git in your Applications (PGBR p.472-481; EN)
Command-line Git 472 > Libgit2 472 > Advanced Functionality 475 > Other Bindings 476 > LibGit2Sharp 476 > Further Reading 477 > JGit 477 > Getting Set Up 477 > Plumbing 478 > Porcelain 480 > Further Reading 481. (There is no PT "Resumo" in this appendix.)

#### Appendix C Git Commands (PGBR p.482-495; EN)
Setup and Config 482 > Getting and Creating Projects 483 > Basic Snapshotting 484 > Branching and Merging 486 > Sharing and Updating Projects 488 > Inspection and Comparison 490 > Debugging 491 > Patching 491 > Email 492 > External Systems 493 > Administration 494 > Plumbing Commands 495. Index 496-499. Translation Notes ("Notas de Tradução") 500.


- 189-419: contiguous, ALL in English (rest of ch. 6 from "Maintaining a Project" 189; ch. 7 217-333; ch. 8 334-364; ch. 9 365-419). Tiny exceptions: labels "Figura N.", label "NOTA", and xrefs with PT titles (195, 201, 219, 270, 287, 323, 334, 356, 359, 412).
- 435-452: entirely English inside ch. 10 (Packfiles to Removing Objects). Exact cut in the middle of the chapter: 420-434 PT, 435-452 EN.
- 453 (after Variáveis de ambiente/Comportamentos globais comes "Repository Locations" EN), 454 (top EN; PT in "Pathspecss" and "Fazendo commits"), 455 (PT at the top; EN in "Diffing and Merging"), 456-457 (EN: Debugging/GIT_TRACE), 458 (EN in "Miscellaneous"; PT in "Sumário"), 459 (PT).
- 460 (PT only in the opening paragraph; "Graphical Interfaces" onwards EN), 461-470 (EN; captions "Figura 152-164" labeled in PT), 471 (1 EN paragraph at the top, "Resumo" PT).
- 472-495 (App. B and C: EN; xrefs with PT titles in 482-489, 493, 495), 496-499 (EN index with "Chaves SSH" and "Comandos git"), 500 (PT, template text).
- Mixed titles: "Apêndice B: Embedding Git in your Applications" (472), "Apêndice C: Git Commands" (482).
- Real PT proportion in 251-500: ~15 full pages (420-434) + ~8 half pages (453, 454, 455, 458, 459, 460, 471, 500): less than 10% of the interval.


## Detail 4: dated data in PGBR

- No use of git switch / git restore in 217-500 (0 occurrences): the book uses "git checkout -- <file>" (230, 231, 233, 277, 293, 303, 348) and "git reset HEAD <file>" (230, 231, 233) [DATED: modern Git offers restore/switch; the book does not mention them].
- "git stash save" (230) [DATED: old form of "git stash push"].
- Hash only SHA-1; SHA-256 does not appear (0 occurrences) [DATED]; "A SHORT NOTE ABOUT SHA-1" 219.
- Default branch "master" (118 pages of the interval).
- Google Code svn URL (375), Git Fusion (386), git-p4 (394), git-remote-hg/bzr (376, 384), GitHub for Mac/Windows (462-464) [DATED: old tools/services].


- There is no git switch nor git restore (0 occurrences); switching branches and undoing use git checkout (p.49, 64) [DATED: the book is from 2014; "git switch/restore" exist since Git 2.23].
- There is no init.defaultBranch nor "main" as the git init default: the book says the default is master (p.29, 62) [DATED]. "main" appears 8x, only in unrelated context.
- There is no SHA-256 (0 occurrences): the hash is a 40-character SHA-1 (p.18) [DATED: the current EN also covers SHA-256].
- There is no --force-with-lease: only git push --force/-f (p.98, 145) [DATED; current practice prefers --force-with-lease].
- The EN section "Your default branch name" (PGEN p.29) does not exist in PT.
- "detached HEAD" is not explained (only a git log line in p.47); "hunk" only appears in English pages (228-229, 233); stash is only explained in English (229-234).
- Installation: Ubuntu 14/yum/Chocolatey/Mavericks, GitHub for Mac/Windows, freenode (p.20-25, 118) [DATED].
- git daemon + Upstart (p.113), GitLab 2016 (p.117-121), msysGit (p.22), "GitHub for Windows" - [DATED].
- Private key: -o option of ssh-keygen (p.110); period dsa/rsa keys [DATED].

