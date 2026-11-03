# FlowAssist v0.4 — couverture du parcours P2

L’énoncé de référence est **P2 · Agent-assist copilot for a fintech (B2B payments)** dans `course/project_proposals.docx`. La v0.4 fait fonctionner le parcours métier dans une démonstration autonome. Elle ne prétend pas remplacer les systèmes de paiement réels.

| Étape du problème | Fonction utilisable dans l’application | Limite explicite |
|---|---|---|
| Réception du ticket | Création d’un dossier, marchand assigné, langue, priorité, recherche et filtres | Données de démonstration ; pas de connexion Zendesk |
| Prélecture du compte | Plan, région, indicateurs KYC/PSD2 et anciens tickets du seul marchand assigné | Fixtures publiques ; le sélecteur n’est pas une authentification serveur |
| Identification du paiement | Extraction de références, montants et devises ; recherche filtrée par marchand | EUR/SEPA et USD/SWIFT, règles déterministes |
| Mauvais rapprochement | Aucun choix par montant seul ; contrôle de référence, devise et montant ; dossier en contexte seul si doute | Pas de score probabiliste ni de garantie d’isolation production |
| Référence ambiguë | Mise en attente, réouverture, saisie d’une référence fournie par le marchand, nouvelle analyse | L’opérateur confirme la provenance de la référence |
| Lecture des sources | Ledger et clearing consultables, identifiants et horodatages, contrôle de cohérence | Horloge de scénario fixée au 2 novembre ; les sources ne deviennent pas fraîches en rechargeant la page |
| Reconstitution | Résumé et chronologie calculés depuis le paiement retenu ; distinction transmission/crédit | Pas de promesse d’arrivée ou de règlement |
| Frais et montant net | Réconciliation en unités monétaires entières ; brut, frais documentés et net affichés séparément | Pas de conversion FX ou de frais devinés |
| Contraintes réglementaires | Indicateurs de compte et routage conformité, litige ou action financière | Aucune règle juridique personnalisée, date de chargeback ou levée de blocage inventée |
| Réponse sourcée | Texte EN/FR/DE généré depuis les faits, citations des sources du même paiement | Gabarits locaux ; pas de modèle génératif connecté |
| Évaluation avant affichage | Porte de contrôle sur identité, cohérence, fraîcheur, montants/statuts et citations | Contrôle par règles, **pas** le modèle évaluateur demandé pour la version cible de P2 |
| Modification et validation | Revue des sources, brouillon éditable, invalidation après modification, protection contre l’écrasement, vérification finale | Les reformulations libres non certifiables passent en revue humaine ; les erreurs monétaires détectées restent bloquées |
| Communication humaine | Copie dans le presse-papiers et enregistrement explicite d’une réponse humaine dans la démo | Aucun message réellement envoyé ; le bouton de clôture ne contacte pas de client |
| Passation | Motif requis, contexte autorisé, destinataire paiements/conformité/litiges ; transfert enregistré localement | Aucune file externe réellement alimentée |
| Suivi et résolution | Statuts ouvert/en attente/transféré/résolu, réouverture et journal des décisions | État local au navigateur ; pas de collaboration multiutilisateur |
| Mesure et qualité | Temps visible par dossier, pause manuelle, arrêt aux états terminaux, tableau de session et exports | Aide au chronométrage, pas une mesure causale d’AHT, de qualité ou d’économie |
| Traçabilité | Reçus JSON, export du journal et CSV de temps ; données stockées dans l’onglet | Journal modifiable côté navigateur, pas un audit serveur immuable |

## Trois parcours de démonstration

1. **Paiement normal :** DEMO-01 → ouvrir les deux sources → vérifier le brouillon → l’insérer → contrôler le texte final → enregistrer la réponse humaine et clôturer → exporter le reçu.
2. **Ambiguïté :** DEMO-02 → mise en attente → réouverture → saisir `INV-A` en confirmant qu’il a été fourni par le marchand → vérifier les deux nouvelles sources → revue et clôture.
3. **Cas sensible :** DEMO-03 ou DEMO-09 → consulter compte/politique → choisir le motif → préparer la passation → vérifier le destinataire → enregistrer le transfert → vérifier le journal et le tableau de session.

Autres cas inclus : paiement échoué en USD, paiement retourné, rapprochement des frais, source périmée et conflit ledger/clearing. Le formulaire peut créer jusqu’à 30 dossiers de démonstration en réutilisant les références des fixtures.

## Périmètre de mise en production restant

Les connecteurs de lecture, l’authentification/autorisation serveur, la persistance partagée, l’audit protégé, le modèle de génération et le modèle évaluateur doivent être intégrés et validés sur des systèmes autorisés. Les résultats de recherche utilisateurs, les 20 labels proposés et le critère de 41,2 % ne deviennent pas validés du fait de cette extension. Le protocole A/B cible reste randomisé par agent ; les temps de cette démo ne le remplacent pas.

L’autonomie client et les actions sur les fonds restent exclues. Les trois MUST et cinq WON’T du livrable S3 restent la décision de périmètre initiale ; la v0.4 étend l’expérience locale sans réintroduire les actions financières, les réponses autonomes ou les conseils sensibles exclus.
