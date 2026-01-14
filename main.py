import json
import os
import re
from datetime import date
import uuid

dateTransaction = str(date.today())


def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")  #


DATA_FILE = "data.json"

try:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    data = []


# Function pour taper le ussd OM #144#
def ussd_code():
    print("Taper le ussd OM #144#")
    while True:
        number_ussd_code = "#144#"
        while True:
            code = input()
            if code == number_ussd_code:
                menu_om()
                break
            else:
                print("Invalid USSD code. Please try again.")
                continue
        break


# Function du menu OM
def menu_om():
    clearTerminal()
    print(
        """ 
   
   ..|''||                                               '||    ||'                                   
.|'     ||  ... ..   ....   .. ...     ... .   ....      |||  |||    ...   .. ...     ....  .... ... 
||      ||  ||' '' '' .||   ||  ||   || ||  .|...||     |'|..'||  .|  '|.  ||  ||  .|...||  '|.  |  
'|.     ||  ||     .|' ||   ||  ||    |''   ||          | '|' ||  ||   ||  ||  ||  ||        '|.|   
 ''|...|'  .||.    '|..'|' .||. ||.  '||||.  '|...'    .|. | .||.  '|..|' .||. ||.  '|...'    '|    
                                    .|....'                                                .. |     
                                                                                            ''      """
    )
    while True:
        choice = input(
            "1.Afficher le solde \n2.Acheter un forfait \n3.Effectuer un transfert \n4.Annuler le dernier transfert \n5.Voir l’historique des transactions \n6.Quitter: "
        )

        match choice:
            case "1":
                display_balance()
            case "2":
                menu_forfait()
            case "3":
                sending_money()
            case "4":
                cancel_transfer()
            case "5":
                transaction_history()
            case "6":
                print("Merci d'avoir utiliser nos services")
                break
            case _:
                print("Invalid choice. Please try again.")
                continue
        break


# Function pour afficher le solde
def display_balance():
    clearTerminal()
    for entry in data:
        while True:
            # On demande son code secret d'abord et on vérifie si il est correct
            secret_code = input("Enter your secret code: ")
            secret_code = int(secret_code)
            if secret_code == entry["secret_code"]:
                print(f"Votre solde est de {entry["balance"]} FcFa.")
                break

            else:
                print("Invalid secret code. Please try again.")
                continue


# function pour acheter un forfait
def menu_forfait():
    clearTerminal()
    print("Acheter du forfait")
    while True:
        choice = input(
            "1. 1000 FcFa pour 1000 minutes \n2. 2000 FcFa pour 2000 minutes \n3. 5000 FcFa pour 5000 minutes \n4. 10000 FcFa pour 10000 minutes \n5. 20000 FcFa pour 20000 minutes \n6. 50000 FcFa pour 50000 minutes \n7. Precédent: "
        )
        match choice:
            case "1":
                buy_forfait(1000)
            case "2":
                buy_forfait(2000)
            case "3":
                buy_forfait(5000)
            case "4":
                buy_forfait(10000)
            case "5":
                buy_forfait(20000)
            case "6":
                buy_forfait(50000)
            case "7":
                menu_om()
            case _:
                print("Invalid choice. Please try again.")
                continue


# Function acheter forfait
def buy_forfait(prix):
    clearTerminal()
    for entry in data:
        while True:
            try:
                # on demande son code secret d'abord et on vérifie si il est correct
                secret_code = input("Enter your secret code: ")
                secret_code = int(secret_code)
                if secret_code == entry["secret_code"]:
                    # Les validation & controle de saisi
                    if entry["balance"] < prix:
                        print("Votre solde est insuffisant pour acheter ce forfait.")
                        return
                    elif entry["balance"] < 0:
                        print("Le montant ne peut pas être négatif")
                    else:
                        new_solde = entry["balance"] - prix
                        entry["balance"] = new_solde
                        with open(DATA_FILE, "w", encoding="utf-8") as file:
                            json.dump(data, file, indent=4)
                        print(
                            f"Le forfait a été acheté avec succès. Votre solde est de {new_solde} FcFa."
                        )
                        return
                    break
            except ValueError:
                print("Veuillez entrer un nombre entier")

                continue


# Function pour effectuer un transfert
def sending_money():
    clearTerminal()
    transaction_id = str(uuid.uuid4())
    for entry in data:
        while True:
            try:
                recipient_number = input(
                    "Entrer le numéro de téléphone du bénéficiaire: "
                )

                if not re.match(r"^\d{9}$", recipient_number):
                    print("Numéro de téléphone invalide.")
                    continue

                montant = int(input("Entrer le montant à transférer: "))

                if montant <= 0:
                    print("Le montant doit être supérieur à 0.")
                    continue

                secret_code = int(input("Entrer votre code secret: "))

                if secret_code != entry["secret_code"]:
                    print("Code secret incorrect.")
                    continue

                if montant > entry["balance"]:
                    print("Solde insuffisant.")
                    continue

                entry["balance"] -= montant
                entry["transaction"] += montant
                entry["last_transaction"] = montant
                entry["transaction_history"].append(
                    {
                        "id": transaction_id,
                        "date": dateTransaction,
                        "recipient": recipient_number,
                        "montant": montant,
                    }
                )

                with open(DATA_FILE, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)

                print(f"Transfert réussi vers {recipient_number}.")
                print(f"Nouveau solde : {entry['balance']}")

                return

            except ValueError:
                print("Veuillez entrer un nombre valide.")


# Function d'annulation transfert
def cancel_transfer():
    clearTerminal()
    for entry in data:
        transfert = entry.get("last_transaction")
        if not transfert or transfert == 0:
            print("Aucun transfert n'a été éffectuer")
            return

    message = "Vous êtes sur le point d'annuler un transfert d'argent. \n1. Confirmer \n2. Annuler\nchoix:"
    while True:
        try:
            code_secret = int(input("Veuillez entrer votre code secret: "))
            if code_secret != entry["secret_code"]:
                print("Code incorrect ! Veuillez réessayer.")
                continue
            if input(message) == "1":
                for entry in data:
                    my_solde = entry["balance"]
                    montant_transfert = entry.get("last_transaction", 0)
                    new_solde = my_solde + montant_transfert
                    entry["balance"] = new_solde
                    entry["last_transaction"] = 0
                    print(entry)
                    with open(DATA_FILE, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4)
                    print(
                        f"Le transfert a été annulé avec succes. Votre solde est de {new_solde} FCFA."
                    )
                    return
            elif input(message) == "2":
                print("Annulation du transfert annulée.")
                return
            break
        except ValueError:
            print("Veuillez entrer un nombre entier")
            continue


# Historique des transactions
def transaction_history():
    clearTerminal()
    for entry in data:
        # Verification s'il existe deja de la trasaction
        if not entry["transaction_history"]:
            print("Aucune transaction disponible")

        print("Historique des transactions:")
        for transaction, element in enumerate(entry["transaction_history"], start=1):
            print(
                f"{transaction}. Date: {element['date']}, Beneficiaire: {element['recipient']}, Montant: {element['montant']} FcFa"
            )
            


ussd_code()
