# Activer la synchronisation GitHub vers Vercel

À transmettre à Benjamin et Lenny. Le code de synchronisation est prêt et poussé dans le dépôt principal ; ce guide explique l’autorisation à configurer une seule fois.

**L’app est déjà en ligne : [ouvrir FlowAssist](https://deploy-project-product-management.vercel.app).** Le secret ci-dessous sert à publier automatiquement les prochaines modifications de toute l’équipe. Une première synchronisation locale a réussi ; la synchronisation automatique GitHub Actions reste à activer.

Le circuit est : **push sur le dépôt d’équipe → GitHub Actions → copie dans le dépôt de Lenny → déploiement Vercel**.

| Élément | Valeur |
|---|---|
| Dépôt principal, où ajouter le secret | `BenjaminAHS/project-product-management` |
| Dépôt de déploiement, où le jeton autorise l’écriture | `lsantus-mines/deploy-project-product-management` |
| Secret attendu | `DEPLOY_REPO_TOKEN` |
| Workflow | `Sync Vercel deployment repository` |
| Branche concernée | `main` |

## 1. Lenny crée le jeton sur son compte

Le jeton doit être créé avec **le compte `lsantus-mines`**, propriétaire du dépôt de déploiement. Un jeton créé par Benjamin n’a pas automatiquement accès en écriture au dépôt de Lenny.

1. Connecte-toi à GitHub avec `lsantus-mines`, puis ouvre [la création d’un jeton à accès fin](https://github.com/settings/personal-access-tokens/new).
2. Renseigne les paramètres suivants :

   | Champ GitHub | Valeur à choisir |
   |---|---|
   | Token name | `FlowAssist deployment sync` |
   | Expiration | Par exemple 90 jours ; prévoir son renouvellement |
   | Resource owner | `lsantus-mines` |
   | Repository access | **Only select repositories** |
   | Selected repositories | **deploy-project-product-management** uniquement |

3. Dans **Repository permissions**, règle **Contents → Read and write**. **Metadata → Read-only** peut être ajouté automatiquement. Aucun accès Workflows, Administration ou à tous les dépôts n’est nécessaire : le script ne copie pas les définitions de workflows.
4. Clique sur **Generate token**, puis copie la valeur affichée. Elle ne sera plus affichée ensuite.

Conserve cette valeur comme un mot de passe. Elle doit être saisie dans le formulaire de secret GitHub, jamais dans le README, un commit ou cette conversation. Si Benjamin la renseigne, transmets-la par un canal privé sécurisé.

## 2. Benjamin ajoute le secret dans le dépôt principal

Un collaborateur disposant de l’accès nécessaire aux réglages peut également effectuer cette étape : Lenny peut essayer directement, sans transmettre le jeton.

1. Ouvre [les secrets Actions du dépôt principal](https://github.com/BenjaminAHS/project-product-management/settings/secrets/actions).
2. Le chemin dans GitHub est **Settings → Secrets and variables → Actions → Secrets**.
3. Clique sur **New repository secret**.
4. Remplis exactement :

   | Champ | Valeur |
   |---|---|
   | Name | `DEPLOY_REPO_TOKEN` |
   | Secret | La valeur du jeton créé par Lenny à l’étape 1 |

5. Clique sur **Add secret**. Le nom doit ensuite apparaître dans **Repository secrets** ; la valeur restera masquée.

Il faut un **repository secret dans le dépôt principal**, pas une variable Actions, un secret d’environnement ou un secret dans le dépôt de déploiement. Si les réglages ne sont pas accessibles, Benjamin effectue cette étape en tant que propriétaire.

## 3. Lancer la première synchronisation

1. Ouvre [les exécutions du workflow](https://github.com/BenjaminAHS/project-product-management/actions/workflows/sync-deploy.yml).
2. Sélectionne **Run workflow**, choisis `main`, puis confirme **Run workflow**. Le workflow doit déjà être présent sur `main` pour apparaître.
3. Attends la fin de l’exécution et vérifie que l’étape **Synchronize committed files and push safely** est verte.
4. Ouvre [les commits du dépôt de déploiement](https://github.com/lsantus-mines/deploy-project-product-management/commits/main/). Si les fichiers différaient, un commit **Sync primary main at …** doit apparaître. Si tout était déjà identique, le script affiche `0 changed, 0 removed` et ne crée pas de commit.
5. Vérifie dans Vercel que le projet utilise bien `lsantus-mines/deploy-project-product-management`, branche `main`, puis contrôle le déploiement et son URL publique.

Ensuite, chaque push sur `main` du dépôt principal déclenche automatiquement la synchronisation, quel que soit le membre qui pousse. Les exécutions sont sérialisées et copient la dernière version de `main`. Une exécution sans modification de fichiers ne provoque pas de nouveau commit de déploiement.

## Si une étape échoue

| Symptôme | Action |
|---|---|
| Message demandant `DEPLOY_REPO_TOKEN` | Vérifier le nom exact et le dépôt où le secret a été ajouté ; relancer ensuite le workflow |
| `Repository not found`, erreur 403 ou écriture refusée | Vérifier que le jeton vient de `lsantus-mines`, cible le bon dépôt, possède Contents en écriture et n’a pas expiré |
| Refus `fetch first` / non-fast-forward | Quelqu’un a modifié le dépôt de déploiement pendant la synchronisation ; relancer le workflow, sans push forcé |
| Workflow absent dans Actions | Vérifier que `.github/workflows/sync-deploy.yml` est sur `main` du dépôt principal et que GitHub Actions y est activé |
| Synchronisation verte mais aucune nouvelle version dans Vercel | Vérifier le dépôt et la branche liés au projet Vercel ; s’il n’y a aucun changement de fichiers, l’absence de nouveau commit est normale |
| L’URL demande de se connecter à Vercel | Vérifier l’accès public à la production dans Deployment Protection ; partager le domaine de production |

Au renouvellement, crée un nouveau jeton avec les mêmes droits, remplace la valeur de `DEPLOY_REPO_TOKEN`, puis relance le workflow pour vérifier.

Références : [création des jetons GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens), [secrets GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets). Le [guide de déploiement](../prototype/DEPLOYMENT.md) détaille les paramètres Vercel et les contrôles de publication.
