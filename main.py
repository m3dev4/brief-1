import json
import os
import re

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear') #
    
    
DATA_FILE = "data.json"

try:
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    data = []
    
#Function pour taper le ussd OM #144#
def ussd_code():
    while True:
        number_ussd_code = '#144#'
        while True:
            code = input()
            if code == number_ussd_code:
                menu_om()
                break
            else:
                print("Invalid USSD code. Please try again.")
                
#Function du menu OM
def menu_om():
    print("""""")
    while True:
        choice = input("1.Afficher le solde \n2.Acheter un forfait \n3.Effectuer un transfert \n4.Annuler le dernier transfert \n5.Voir l’historique des transactions \n6.Quitter: ")
        
        match choice:
            case "1":
                display_balance()
            case "2":
                menu_forfait()
            case "3":
                  sending_money()
            case "4":
                pass
            case "5":
                pass
            case "6":
                break
            case _:
                print("Invalid choice. Please try again.")
                
  
#Function pour afficher le solde
def display_balance():
    
    for entry in data:
        while True:
            #On demande son code secret d'abord et on vérifie si il est correct
            secret_code = input("Enter your secret code: ")
            secret_code = int(secret_code)
            back = input("0. Precédent: ")
            if secret_code == entry["secret_code"]:
                print(f"Votre solde est de {entry["balance"]} FcFa.")  
                break 
           
            else:
                print("Invalid secret code. Please try again.")
                continue
             # Retour en arrier
        if back == "0":
                menu_om()

#function pour acheter un forfait
def menu_forfait():
    print("Acheter du forfait")
    choice = input("1. 1000 FcFa pour 1000 minutes \n2. 2000 FcFa pour 2000 minutes \n3. 5000 FcFa pour 5000 minutes \n4. 10000 FcFa pour 10000 minutes \n5. 20000 FcFa pour 20000 minutes \n6. 50000 FcFa pour 50000 minutes \n7. Precédent: ")     
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
                
            
            
#Function acheter forfait
def buy_forfait(prix):
    clearTerminal()
    for entry in data:
        my_solde = entry["balance"]
        while True:
           try:
                #on demande son code secret d'abord et on vérifie si il est correct
                 secret_code = input("Enter your secret code: ") 
                 secret_code = int(secret_code)
                 if secret_code == entry["secret_code"]:
                 #Les validation & controle de saisi
                  if my_solde < prix:
                    print("Votre solde est insuffisant pour acheter ce forfait.")
                    return
                 elif my_solde < 0:
                    print("Le montant ne peut pas être négatif")
                 else:
                    new_solde = my_solde - prix
                    entry["balance"] = new_solde
                    with open(DATA_FILE, 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4)
                    print(f"Le forfait a été acheté avec succès. Votre solde est de {new_solde} FcFa.")
           except ValueError:
                print("Veuillez entrer un nombre entier")
                continue 
                    
#Function pour effectuer un transfert
def sending_money():
    for entry in data:
        my_solde = entry["balance"]

        while True:
            try:
                recipient_number = input("Entrer le numéro de téléphone du bénéficiare: ")

                if not re.match(r'^\d{9}$', recipient_number):
                    print("Numéro de téléphone invalide. Veuillez entrer un numéro de téléphone valide.")
                    continue

                montant = int(input("Entrer le montant à transferer: "))
          

                while True:
                    secret_code = input("Enter your secret code: ")
                    secret_code = int(secret_code)
                    
                    if secret_code == entry["secret_code"]:
                        #validation & controle de saisi
                        if montant < 0:
                            print("Le montant ne peut pas être négatif")
                            continue
                        elif montant > my_solde:
                            print("Votre solde est insuffisant pour effectuer ce transfert.")
                            continue
                        else:
                            new_solde = my_solde - montant
                            entry["balance"] = new_solde
                            entry["transaction"] = montant
                            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                                json.dump(data, file, indent=4)
                            print(f"Le trensfert c'est bien effectué vers ce numéro {recipient_number}.")
                        break
                    else:
                        print("Invalid secret code. Please try again.")
                        continue
            
            except ValueError:
                print("Veuillez entrer un nombre entier")

ussd_code()