# Orange Money USSD Simulator

Une simulation d'application Orange Money en ligne de commande qui permet de gérer un compte mobile money via le code USSD `#144#`
## Fonctionnalités
- **Afficher le solde** : Consulter le solde de votre compte avec code secret
- **Acheter un forfait** : Acheter des minutes d'appel (de 1000 à 50000 FCFA)
- **Effectuer un transfert** : Envoyer de l'argent vers un numéro de téléphone à 9 chiffres
- **Annuler le dernier transfert** : Récupérer l'argent du dernier transfert effectué
- **Historique des transactions** : Voir toutes les transactions effectuées avec leurs détails (ID, date, bénéficiaire, montant)

  ## Structure du fichier data.json

```json
[
    {
        "balance": 50000,
        "secret_code": 1234,
        "transaction": 0,
        "last_transaction": 0,
        "transaction_history": []
    }
]

````
# Fait Mouhamed Lo
