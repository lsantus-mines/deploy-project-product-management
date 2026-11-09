# FlowAssist — Payment tracing copilot for specialists

**Course:** Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04) · Albert School / Mines Paris-PSL · shared project with Agentic Workflows

**Cohort:** M2-INTER-1

**Site Vercel : [ouvrir FlowAssist](https://deploy-project-product-management.vercel.app)**

## Team

| Name | Git handle | Also in the Agentic Workflows team? |
|---|---|---|
| Lenny Santus | @lsantus-mines | no |
| Anthony Rascle | @antotototototo18 | no |
| Antoine Rabeau | @antorabo75 | no |
| Benjamin Caujolle | @BenjaminAHS | no |
| Colin Sibieude | @csib-wq | no |

## Our agent

- **Starting point:** P2 — Agent-assist copilot for a fintech (B2B payments). FlowAssist adapts the supplied proposal; `00_pitch.md` records the adaptation rather than a separate custom proposal.
- **The company:** PayFlow B2B, a European B2B payments fintech: 800 enterprise/marketplace merchant accounts, 12,000 support tickets per month and an assumed team of 18 Tier-1 specialists. These are educational scenario/planning figures, not observed company measurements.
- **The job, in one sentence:** When a merchant submits a payment-tracing request, FlowAssist matches a transaction within the assigned merchant’s synthetic records and prepares a cited EN/FR/DE status reply, producing an editable draft for the specialist’s approval and local recording.
- **Trust level per step:** L1 intent/entity suggestions → L3 scoped local read-only lookup with explicit source inspection and human match review → L2 draft and policy checks → person-only final approval and local response/handover recording. The local journal is application metadata, not authenticated L4 production auditing. The production design retains person-only customer sending. Model confidence never authorizes access; the runtime uses rules/templates and makes no live model, bank or Zendesk call.
- **One thing it must never do:** Send an autonomous customer reply, execute/refund/release funds, write a ledger, or expose a payment outside the assigned merchant and verified transaction. Missing/ambiguous identity, invalid evidence or sensitive intent suppresses drafting and returns the case to a person.

## Repository structure

One numbered file per session. Every member authors commits in at least four of the numbered files. This is the course requirement, not a certification of contributions.

| File | Session | Status |
|---|---|---|
| `00_pitch.md` | before S3 — only if you bring your own idea | Present: optional adaptation of supplied P2, not a separate custom proposal |
| `01_problem_statement.md` | S1–S2 — Assignment 1 | Documented: quantified scenario, causes, AI choice, hypotheses and baseline |
| `governance.md` | created for Assignment 1, one line added every session | Updated through S4: source boundaries, data, human checkpoints and manual override |
| `02_sizing.xlsx` | S2 — Assignment 2 | Editable three-scenario model; financial limitations explained in the memo |
| `02_investment_memo.md` | S2 — Assignment 2 | Updated: conditional GO, named alternative and 41.2% flip threshold |
| `03_product_brief.md` | S3 | Brief v2 present; supporting process/design record and archived v1 |
| `04_architecture.md` | S4 | Implemented workflow, diagram, components, checkpoints, fallbacks and data |
| `05_metrics.md` | S5 | Future session deliverable; not yet present |
| `06_ab_protocol.md` | S6 | Future session deliverable; not yet present |
| `07_operations.md` | S7 | Future session deliverable; not yet present |
| `08_launch_memo.md` | S8 | Future session deliverable; not yet present |
| `spec.md`, `product_brief.md` | final | `spec.md` v2 present; consolidated final `product_brief.md` not yet present |
| `/prototype`, `/evals` | from S4 | Executable local workflow, 32 tests, 50 development cases and before/after reports |

Supporting S3 files: [AI Lean Canvas](03_ai_lean_canvas.md), [design details](03_design_details.md), [needs/design record](03_user_research.md), [prototype link](03_prototype_link.md) and [delivery matrix](03_s3_delivery.md). S4: [report](evals/report_v0.md), [delivery matrix](04_s4_delivery.md) and [evaluation guide](evals/README_eval_set.md). [Cross-session evidence audit](docs/DELIVERY_AUDIT.md).

## Rules

- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.

## Version actuelle · 9 novembre 2026

Le prototype local implémente le parcours complet : création de ticket, contexte du compte, recherche limitée au compte, clarification de référence, réponse citée, inspection des sources, validation, traitement manuel et transfert local. Le moteur utilise des règles et des gabarits ; il n’appelle aucun modèle, système bancaire ou Zendesk. Aucun message client ni mouvement de fonds n’est exécuté.

- **32 tests domaine/interface passent.**
- **50/50 états attendus concordent** sur les cas de développement ; 15 brouillons, zéro brouillon sur les cas human-only et aucune source étrangère observée.
- Les corrections couvrent les références et montants, ainsi que l’abstention sur une correspondance déclarée comme issue d’un modèle avec score absent, invalide ou inférieur à 0,95. Le score ne remplace aucun contrôle d’identité ou de source.
- Le starter Paylio original a été exécuté : routage 0,88, hit@3 1,00, score heuristique 8/20 = 40 % pour un seuil de 45 %. Cette heuristique ne constitue pas une notation humaine.

Les 50 cas ont été examinés pendant le développement : ces résultats servent à la régression, pas à revendiquer une performance sur un benchmark tenu à l’écart. Le critère métier reste ≥41,2 % de gain de temps actif apparié sur les cas éligibles, QA ≥92 %, précision de détection ≥98 % et zéro exposition critique. Les résultats automatiques ne démontrent pas ce critère.

[Architecture](04_architecture.md) · [Rapport d’évaluation](evals/report_v0.md) · [Livraison S4](04_s4_delivery.md) · [Audit des séances](docs/DELIVERY_AUDIT.md) · [Couverture produit](docs/PRODUCT_COVERAGE.md).

## Utiliser le prototype

Ouvrir [prototype/index.html](prototype/index.html), ou lancer depuis la racine :

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Puis accéder à `http://127.0.0.1:8000/prototype/`. Aucun compte, installation npm ou clé API n’est nécessaire. Les brouillons et actions sont enregistrés dans le sessionStorage de l’onglet ; seules des données synthétiques doivent être saisies.

[Adresse de la démonstration hébergée](https://deploy-project-product-management.vercel.app). Le dernier contrôle HTTP réussi date du 3 novembre ; la copie Git de publication a été vérifiée synchronisée avec la livraison S4 le 9 novembre. Le nouveau déploiement HTTP n’a pas pu être confirmé à cause d’une erreur DNS. [État de publication et procédure](prototype/DEPLOYMENT.md).

## Vérifier et reproduire

Python et Node.js suffisent aux vérifications FlowAssist :

```sh
python3 scripts/verify_s3.py
python3 scripts/verify_s4.py
```

Le premier contrôle les artefacts, liens et 32 scénarios domaine/interface. Le second vérifie les 50 cas, les grilles de revue et les empreintes, puis reproduit les passages initial et courant. Pour ne relancer que le moteur :

```sh
node scripts/eval_s4.cjs
node scripts/eval_s4.cjs --baseline
```

Le starter Paylio requiert pandas et scikit-learn. Dans l’environnement local où ils sont installés :

```sh
/opt/anaconda3/bin/python scripts/run_paylio.py
```

Sur une autre machine, utiliser un interpréteur Python disposant de ces dépendances. [Instructions runtime](prototype/README.md) · [Preuves et limites des vérifications](prototype/verification.md) · [Historique des changements](prototype/CHANGELOG.md).

## Assignment PDFs and sources

- [Assignment 1 — Team, agent and problem](Assignments/Assignment_1_Team_Agent_Problem.pdf) · 4 pages.
- [Assignment 2 — Sizing and investment memo](Assignments/Assignment_2_Sizing_Investment_Memo.pdf) · 6 pages.
- [Assignment 3 — MVP brief and design loop](Assignments/Assignment_3_MVP_Brief_and_Design_Loop.pdf) · 7 pages.
- [Assignment 4 — Prototype and architecture](Assignments/Assignment_4_Prototype_and_Architecture.pdf) · 4 pages · [original-format sources](Assignments/Sources/Assignment_4_sources.zip).

[Package notes and reproduction](Assignments/README.md). S1–S3 PDFs and archives retain their 6 November edition, including the historical 20-case S3 index; the current CSV has 50 development cases. The current Markdown documents describe the S4 code and results. Original instructions remain in `course/`, `S3_templates/` and `S4_templates/`.

The documents distinguish automated checks, assumptions and human validation. They do not certify real conversations, independent judgements or individual contributions beyond the available evidence. Future deliverables in the template remain visible as future work rather than being omitted or described as completed.

## Source et publication

Développer dans [BenjaminAHS/project-product-management](https://github.com/BenjaminAHS/project-product-management), branche `main`. Vercel utilise la copie [lsantus-mines/deploy-project-product-management](https://github.com/lsantus-mines/deploy-project-product-management), avec un historique séparé. Après chaque push primaire réussi, exécuter `python3 scripts/sync_deploy.py` et confirmer le résultat ; préserver les workflows de destination et ne jamais forcer le push. [Instructions du dépôt](AGENTS.md) · [Guide de synchronisation](docs/ACTIVER_SYNC_GITHUB.md).

La livraison PDF S4 `60267d0` a été poussée et sa copie de publication comparée sans différence. La synchronisation Git ne constitue pas une vérification HTTP du site ; les preuves datées sont conservées dans [le guide de déploiement](prototype/DEPLOYMENT.md).
