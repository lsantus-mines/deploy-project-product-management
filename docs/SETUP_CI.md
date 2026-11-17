# Mise en place CI/CD et API — guide pour Benjamin

**Pour qui :** Benjamin, admin du repo principal `BenjaminAHS/project-product-management`. Seule l'étape 2 demande l'accès au projet Vercel, qui est sur le compte de Lenny (`lsantus-mines`) : demande-lui de t'ajouter au projet, ou faites-la ensemble.
**Durée :** ~20 min. **Coût :** 0 € (GitHub Actions et Vercel Hobby gratuits ; aucun service d'analytics externe).
**Contexte :** la PR `anthony/production-hardening` ajoute une API FastAPI (guardrails côté serveur), une CI, un déploiement conditionné à la CI, un interrupteur global et un suivi des métriques **en local**. Rien ne change pour la démo tant que la PR n'est pas mergée.

Ordre conseillé : **1 → 2 → merge de la PR → 3**.

---

## 1. GitHub — la CI (sur ton repo)

La CI tourne sur ton repo, donc sur les minutes GitHub Actions de ton compte (illimitées si le repo est public, 2 000 min/mois sinon ; un run dure ~30 s).

1. **Vérifier que les Actions sont actives :** *Settings → Actions → General → Allow all actions*.
2. **Rendre la CI obligatoire avant tout merge sur `main`** : *Settings → Branches → Add branch protection rule* (ou *Rules → Rulesets*) :
   - Branch name pattern : `main`
   - ☑ *Require a pull request before merging*
   - ☑ *Require status checks to pass* → cocher **`lint, tests, evals, attacks`** (le check existe déjà, il a tourné sur la PR #1)
   - Laisse la possibilité de bypass aux admins si tu veux garder un bouton d'urgence.
3. **Secret optionnel pour le juge LLM** : *Settings → Secrets and variables → Actions → New repository secret* → `OPENAI_API_KEY` (le juge utilise `gpt-6-luna`). Le workflow *LLM judge (manual)* ne tourne qu'à la main (*Actions → LLM judge → Run workflow*) et coûte quelques centimes. Chacun peut aussi le lancer en local avec `make judge` et sa clé dans `.env`.
4. Le secret existant `DEPLOY_REPO_TOKEN` ne change pas.

**Ce que fait la CI** (`.github/workflows/ci.yml`, identique à `make ci` en local) : lint Python, données front/serveur synchronisées, tests Python (dont parité moteur JS ↔ Python, API et suivi des métriques), 39 tests d'interface, régression des 50 cas, **set d'attaques : un seul raté bloque la PR**.

**Ce qui change pour le déploiement** (`.github/workflows/sync-deploy.yml`) : la synchro vers le repo Vercel ne part plus à chaque push, mais **après une CI verte sur `main`**, puis lance un smoke test sur la prod. Si le smoke échoue, le run est rouge avec la marche à suivre (rollback).

## 2. Vercel — l'API Python (accès au projet de Lenny)

`vercel.json` déclare maintenant la fonction `api/index.py` (FastAPI, détectée grâce à `requirements.txt`) et la règle `/api/* → api/index`. Le front statique ne change pas.

Dans *Vercel → projet `deploy-project-product-management` → Settings → Environment Variables*, ajouter (environnement **Production**) :

| Variable | Valeur | Rôle |
|---|---|---|
| `ASSIST_MODE` | `on` | **l'interrupteur global** : `on` / `suggest_only` / `off` |
| `FLOWASSIST_ENV` | `demo` | tague les traces et événements comme démo |

Puis *Deployments → … → Redeploy* (les variables ne s'appliquent qu'aux nouveaux déploiements).

**Vérifier après le déploiement :**
- `https://deploy-project-product-management.vercel.app/api/health` → `{"status":"ok","engine_version":"0.6.0"}`
- `…/api/config` → `assist_mode` vaut `on`
- Onglet *Logs* : une ligne JSON par requête (`"type":"trace"`) et par événement (`"type":"event"`), sans aucun texte de ticket.
- En local : `make smoke URL=https://deploy-project-product-management.vercel.app` → 6 × `ok`.

> ⚠️ Ne jamais mettre de clé OpenAI ou Anthropic sur Vercel : le juge ne tourne pas en production.

**Utiliser l'interrupteur (rollback sans toucher au code) :** changer `ASSIST_MODE` en `suggest_only` (brouillons visibles, plus d'insertion) ou `off` (mode humains seuls), puis **Redeploy** (~1 min). Toute autre valeur met le serveur en `suggest_only` par sécurité. Qui peut le faire : Head of Payment Ops le jour, l'ingénieur d'astreinte la nuit (voir `governance.md`).

## 3. Après le merge — checklist de validation

- [ ] La CI de la PR est verte (*Pull request → Checks*).
- [ ] Après le merge : *Actions* montre **CI** puis **Sync Vercel deployment repository**, les deux verts.
- [ ] `/api/health` renvoie `engine_version` = `0.6.0`.
- [ ] La démo affiche dans le bandeau « Assistant on · you approve every reply ».
- [ ] Test de l'interrupteur : `ASSIST_MODE=suggest_only` + Redeploy → le bandeau passe en « suggest-only » et « Use draft » est désactivé → remettre `on`. **Noter la date du test dans `governance.md`** (exigé par le plan de rollback).

## Les métriques avant lancement (en local, pas de setup)

Chaque membre peut produire les métriques sur sa machine :
```sh
make install      # une fois
make dev          # API + démo sur http://127.0.0.1:8000 ; les événements vont dans metrics/events.jsonl
# … utiliser la démo (ouvrir des tickets, inspecter les sources, enregistrer des réponses) …
make metrics      # → metrics/report.md : funnel, blocages, temps de traitement par segment, escalade, infra
```
`metrics/` est ignoré par Git : les données restent sur la machine. Le détail des événements est dans `docs/TRACKING_PLAN.md`. Pour la prod, on peut exporter les logs Vercel (lignes JSON) et lancer `python scripts/eval/metrics_report.py export.jsonl`.

## En cas de problème

| Symptôme | Cause probable | Action |
|---|---|---|
| Bandeau « Assistant server unavailable » | `/api/*` ne répond pas (fonction non déployée ou erreur) | *Vercel → Logs*. Le front est volontairement fermé (fail-closed) : la démo reste utilisable en manuel. |
| Bandeau « suggest-only » alors que rien n'a été changé | `ASSIST_MODE` absent ou mal orthographié sur Vercel | corriger la variable puis Redeploy |
| Le run *Sync Vercel* ne part pas | la CI a échoué, ou le workflow n'est pas encore sur `main` | corriger la CI ; *Run workflow* manuel possible |
| Smoke test rouge après déploiement | régression en prod | revert du commit sur `main` (la CI repasse et redéploie) **ou** `ASSIST_MODE=off` + Redeploy |

Commandes locales utiles : `make help`, `make install`, `make dev`, `make ci`, `make metrics`, `make judge`, `make smoke URL=…`.
