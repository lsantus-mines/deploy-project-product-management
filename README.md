# FlowAssist — Payment operations copilot

**Site Vercel : [ouvrir FlowAssist](https://deploy-project-product-management.vercel.app)**

Projet **P2 · PayFlow B2B** — Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04), Albert School / Mines Paris-PSL · M2-INTER-1.

FlowAssist aide un spécialiste support à tracer un paiement, vérifier ses sources et préparer une réponse EN/FR/DE avec validation humaine. PayFlow est un scénario pédagogique ; les comptes, tickets et paiements de l’application sont synthétiques.

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

## Documents du projet

| Séance | Livrables | État documentaire |
|---|---|---|
| S1 | [Pitch](00_pitch.md), [problème](01_problem_statement.md), [gouvernance](governance.md) | Diagnostic, hypothèses, sources et limites du scénario |
| S2 | [Modèle Excel](02_sizing.xlsx), [mémo](02_investment_memo.md) | Trois scénarios, coûts, alternative nommée, seuil de 41,2 % ; réserves financières explicites |
| S3 | [Brief v2](03_product_brief.md), [détails de conception](03_design_details.md), [Lean Canvas](03_ai_lean_canvas.md), [analyse des besoins](03_user_research.md), [prototype](03_prototype_link.md), [matrice de livraison](03_s3_delivery.md) | Synthèse de conception ; brief v1 archivé dans `research/` |
| S3–S4 | [Spec v2](spec.md), [architecture](04_architecture.md), [gouvernance](governance.md) | Contrats, contrôles humains, mode manuel, corrections S4-M01–M03 et périmètre réel |
| S4 | [50 cas CSV](evals/eval_set_v0.csv), [guide](evals/README_eval_set.md), [rapport](evals/report_v0.md), [livraison](04_s4_delivery.md) | Labels proposés, fixtures exécutables, résultats avant/après et grilles de revue |

Le [PDF Assignment 4 — Prototype & Architecture](Assignments/Assignment_4_Prototype_and_Architecture.pdf) fournit une synthèse de quatre pages, accompagnée de [ses sources](Assignments/Sources/Assignment_4_sources.zip). Les versions PDF S1–S3 et leurs archives datées du 6 novembre sont accessibles dans [Assignments](Assignments/README.md). Leur index de 20 cas reflète le seed S3 ; le CSV courant en contient 50. Les fichiers Markdown courants décrivent les évolutions S4. Les consignes et modèles originaux restent dans `course/`, `S3_templates/` et `S4_templates/`.

Les documents distinguent preuves automatiques, hypothèses et validations humaines ; ils ne certifient pas des entretiens, des jugements indépendants ou des contributions personnelles non établis. Les séances ultérieures ne sont pas présentées comme livrées sur la base de simples titres prévisionnels.

## Team

| Membre | GitHub | Également dans l’équipe Agentic Workflows ? |
|---|---|---|
| Lenny Santus | @lsantus-mines | non |
| Anthony Rascle | @antotototototo18 | non |
| Antoine Rabeau | @antorabo75 | non |
| Benjamin Caujolle | @BenjaminAHS | non |
| Colin Sibieude | @csib-wq | non |

## Repository structure

### Source et publication

Développer dans [BenjaminAHS/project-product-management](https://github.com/BenjaminAHS/project-product-management), branche `main`. Vercel utilise la copie [lsantus-mines/deploy-project-product-management](https://github.com/lsantus-mines/deploy-project-product-management), avec un historique séparé. Après chaque push primaire réussi, exécuter `python3 scripts/sync_deploy.py` et confirmer le résultat ; préserver les workflows de destination et ne jamais forcer le push. [Instructions du dépôt](AGENTS.md) · [Guide de synchronisation](docs/ACTIVER_SYNC_GITHUB.md).

La dernière livraison technique est le commit primaire `034267c`, copié dans le commit de publication `8a8a2cf`. Le contrôle local a confirmé zéro fichier modifié ou supprimé entre ces snapshots ; cette vérification Git ne prouve pas la disponibilité du site.

Chaque membre doit utiliser son propre compte Git. La version finale sera taguée `v1.0` avant le premier oral de la cohorte ; aucun commit après le début de cet oral.
