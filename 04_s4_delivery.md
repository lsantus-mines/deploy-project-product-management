# Session 4 — état de livraison au 9 novembre 2026

Référence : `S4_templates/README_S4.md` et Assignment 4 (remise 15 novembre, 23:59).

| Exigence | Livrable / état |
|---|---|
| Prototype exécutable, quatre décisions | `prototype/engine.js` : classify → règles analyze → sourceRecords/makeDraft → evaluateDraft ; interface avec revue et mode manuel |
| 50 cas étiquetés avant passage | CSV 50 lignes, labels IA proposés ; F21–F50 écrits avant exécution, seed S3 déjà exposé ; validation humaine encore requise |
| Exécution et nombre contre le critère | `node scripts/eval_s4.cjs`, résultats avant/après et `evals/report_v0.md` ; critère métier non démontré |
| Deux évaluateurs indépendants | Grille `evals/grader_reviews.csv` prête ; à remplir par deux personnes, aucune attestation simulée |
| Trois causes / spec v2 | Rapport et S4-M01–M03 ; trois familles corrigées ; aucun désaccord d’état sur les 50 cas de développement |
| Architecture conforme au réel | `04_architecture.md`, neuf sections, checkpoints ⊘ et switch ⏻ |
| Gouvernance S4 | `governance.md`, contrôle humain, propriétaire/portée du switch et stockage |
| Quatre commits, quatre auteurs propres | À réaliser par les membres avec leurs comptes. L’assistant ne peut pas fabriquer les contributions ni réécrire l’historique pour satisfaire cette règle |
| Exécuter le starter Paylio une fois | Réalisé sans modifier le starter via `/opt/anaconda3/bin/python scripts/run_paylio.py`. Routage 0,88 ; hit@3 1,00 ; heuristique 8/20 = 40 % (seuil 45 %) ; human-only 0. Preuve : `docs/evidence/s4/paylio-run.txt`. |
| S3 : trois conversations et brief v2 | Les documents existent ; les conversations humaines ne peuvent pas être attestées par une modification automatique |

Les 50 cas ont été consommés pour développement après analyse : remplacer le benchmark avant une mesure indépendante. Pas de faux verdict de succès, de gain de temps ou de validation par des personnes.

Vérifications locales : `python3 scripts/verify_s3.py` (32 scénarios domaine/interface) ; `python3 scripts/verify_s4.py` (alignement des 50 cas, grilles, empreintes et réexécution avant/après). Le harnais DOM n’est pas une preuve visuelle navigateur. Aucune nouvelle publication en ligne n’est revendiquée.

Clôture technique : F19 résolu, 50/50 états attendus, 15 brouillons, 0 brouillon sur human-only ; 32 tests. Les vrais entretiens, jugements et contributions personnelles ne sont jamais remplacés par une simulation IA.
