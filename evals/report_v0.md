# Eval report v0 — FlowAssist

**Date :** 9 novembre 2026 · **Jeu :** `evals/eval_set_v0.csv`, 50 cas synthétiques · **Version :** fichiers identifiés par SHA-256 dans les résultats JSON ; aucun tag `eval-v0` créé et aucun commit d’auteur inventé.

## 1. The number against the criterion
| Mesure | Valeur |
|---|---|
| Critère du brief S3 | ≥41,2 % de gain de temps actif apparié sur 200 cas de tracing éligibles, QA ≥92 %, précision de détection ≥98 %, zéro exposition critique |
| Premier passage : brouillons produits avec contrôle local passant | 2/50 = 4 % |
| Premier passage : états attendus concordants | 37/50 = 74 % |
| Après correction : brouillons produits avec contrôle local passant | 15/50 = 30 % ; jeu désormais de développement |
| Après correction : états attendus concordants | 50/50 = 100 % ; ne signifie pas 100 % de précision de grounding |
| **Réponses que deux personnes enverraient sans modification** | **Non mesuré ; pas 0 %** |
| Brouillons sur les 13 cas attendus human-only | 0/13 |
| Sources d’un autre compte dans la sortie | 0/50 cas ; contrôle local seulement |
| Sorties sans brouillon après correction | 34/50 ; inclut routage, ambiguïté et blocages, pas uniquement le policy checker |
| Routage d’intention seul | Non mesuré indépendamment |
| Retrieval hit@3 | Non applicable : recherche déterministe par référence, pas de retriever top-k |
| Temps actif apparié, QA, précision/recall du détecteur | Non mesurés |

**Verdict : critère non démontré.** Ni le nombre de brouillons ni la concordance d’état ne remplacent le critère économique et les deux évaluateurs. Le critère générique Paylio de 45 % ne remplace pas celui du brief FlowAssist.

Reproduction : `node scripts/eval_s4.cjs` réécrit `results_v0.json` de manière déterministe. `results_baseline_v0.json` préserve le premier passage ; le reproduire avec `node scripts/eval_s4.cjs --baseline` et le moteur archivé `engine_baseline_v0.js` (même empreinte). Les sorties texte et IDs de sources sont conservés par cas. Les labels CSV sont inchangés après les passages.

## 2. The three observed failure families
| # | Cause | Cas et fréquence au premier passage | Composant | Ligne spec v2 |
|---|---|---|---|---|
| 1 | Tiret de référence pris pour un montant négatif, ou chiffre terminal de référence absorbé comme montant | F01, F13, F14, F20, F21–F26, F49 : 11 cas, deux défauts successifs du parseur | extraction / règle | S4-M01 : séparer tokens de référence et montants ; corrigé et régressions ajoutées |
| 2 | Formats FAC et RE ignorés | F02, F03 : 2 cas | extraction / retrieval | S4-M02 : formats documentés FAC/RE/REF acceptés ; corrigé |
| 3 | Score 0,94 et note source non représentés dans le runtime | F19 : limite masquée par le défaut de parsing au premier passage, révélée après correction ; 1 cas corrigé lors de la clôture | contrat de matching / contrôle | S4-M03 : branche modèle non livrée ; score et note requis avant intégration ; corrigé : entrée explicite `matchMethod=model`, `matchScore=0.94` et note non fiable dans F19 ; abstention observée |

Les deux premières familles expliquent les 13 désaccords initiaux. La troisième était le seul désaccord après la correction du parsing. Elle est maintenant corrigée : F19 conserve son attente initiale d’abstention et fournit explicitement le score et la note déjà présents dans son texte. Le moteur rejette le score 0,94. Les notes sources ne font pas partie des champs autorisés pour la génération. Les trois familles sont résolues dans la régression ; cela ne prouve pas la complétude du pipeline de production.

## 3. Who graded, and how
Aucun évaluateur humain n’a encore noté les sorties. Les 50 labels et leur adaptation technique sont proposés par IA. `label_review.csv` réserve les approbations de labels ; `grader_reviews.csv` réserve les jugements indépendants des deux évaluateurs et l’arbitrage. Les cellules sont volontairement vides. Chaque personne doit noter l’exactitude compte/transaction/montant/statut/date, les citations, la sécurité et la langue, puis répondre oui/non à « enverrais-je ce texte sans modification ? ». Désaccord non résolu = pending/fail, jamais succès implicite. Ne pas montrer l’avis de l’autre évaluateur avant soumission.

## 4. What is demo data and what is eval data
F01–F20 étaient un seed S3 exposé. F21–F50 ont été écrits et étiquetés avant le premier passage ; les labels n’ont pas été changés pour correspondre aux sorties. Les fixtures du premier seed sont une adaptation manuelle IA des descriptions, pas un parseur de tickets réels. F19 représente désormais explicitement le score et la note de son scénario initial. Le moteur et les fixtures du premier passage restent archivés séparément dans `engine_baseline_v0.js` et `fixtures_baseline_v0.json`. Aucun label attendu n’a été modifié. Après examen des erreurs et modification du moteur, **F01–F50 sont du développement**, donc exclus d’une future mesure tenue à l’écart. Tous restent utiles pour la régression. Les dix tickets `prototype/data.js` restent les exemples visibles ; ils ne sont pas le dénominateur de ce rapport.

## 5. Next step
Utiliser les résultats comme régression de développement ; le critère économique requiert un protocole apparié et des jugements humains authentiques. Le starter Paylio a été exécuté sans modification : routage 0,88, hit@3 1,00 et score heuristique 8/20 = 40 % (seuil 45 %), zéro brouillon sur human-only. Preuve : `docs/evidence/s4/paylio-run.txt` ; reproduction : `/opt/anaconda3/bin/python scripts/run_paylio.py`. Le mot « sendable » de ce script est une heuristique de citation, pas l’avis de deux personnes.
