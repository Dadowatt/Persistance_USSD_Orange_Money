import json
code_secret = "1236"

def afficher_menu_principal():
    print("\n----- ORANGE MONEY -----")
    print("1. Consulter le solde")
    print("2. Acheter du crédit")
    print("3. Effectuer un transfert")
    print("4. Acheter un forfait Internet")
    print("5. Annuler le dernier transfert")
    print("6. Afficher l'historique des transferts")
    print("7. Quitter")

def lire_solde():
    try:
        with open('solde.json', 'r') as f:
            data = json.load(f)
            return data['solde'] #retourne la valeur du solde
    except (FileNotFoundError, json.JSONDecodeError):
        return 10000  #valeur par defaut

def ecrire_solde(solde):
    with open('solde.json', 'w') as f:
        json.dump({'solde': solde}, f)  #ecrire sous forme de dictionnaire

def ecrire_historique(historique):
    with open('historique.json', 'w') as f:
        json.dump(historique, f) #stock l'historique sous forme de liste de dictionnaire

def lire_historique():
    try:
        with open('historique.json', 'r') as f:
            return json.load(f) #retourne une liste de transactions
    except (FileNotFoundError, json.JSONDecodeError):
        return [] #retourne une liste vide si le fichier n'existe pas 

def consulter_solde(solde):
    print(f"Votre solde est de {solde} FCFA")


def acheter_credit(solde):
    montant = input("Entrez le montant du crédit : ")
    if not montant.isdigit():
        print("Montant invalide")
        return solde
    montant = int(montant)
    if montant <= 0:
        print("Le montant doit être positif")
    elif montant > solde:
        print("Solde insuffisant")
    else:
        solde -= montant
        print(f"Achat effectué avec succès! Nouveau solde : {solde}")
        ecrire_solde(solde)  #mettre à jour le fichier
    return solde


def effectuer_transfert(solde, historique):
    numero = input("Entrez le numéro du destinataire : ")
    if not numero.isdigit() or len(numero) != 9:
        print("Numéro incorrect, veuillez saisir un numéro à 9 chiffres")
        return solde, None
    montant = input("Entrez le montant à transférer : ")
    if not montant.isdigit():
        print("Montant invalide")
        return solde, None
    montant = int(montant)
    if montant <= 0:
        print("Le montant doit être positif")
    elif montant > solde:
        print("Solde insuffisant")
        return solde, None
    code = input("Entrez votre code secret 4 chiffres : ")
    while code != code_secret:
        print("Code secret incorrect")
        code = input("Entrez votre code secret 4 chiffres : ")
    solde -= montant
    historique.append({
        'type': 'transfert',
        'numero': numero,
        'montant': montant
        })  #ajout du transfert dans l'historique
    ecrire_historique(historique) #cette fonction écrira l'historique dans json
    print(f"Transfert de {montant} vers {numero} effectué avec succès")
    print(f"Nouveau solde : {solde}")
    ecrire_solde(solde)  #mettre à jour le fichier
    return solde, montant


def acheter_forfait(solde):
    print("\n--- FORFAITS INTERNET ---")
    print("1. Pass 100 Mo - 500 F")
    print("2. Pass 500 Mo - 1000 F")
    print("3. Pass 1 Go  - 2000 F")

    choix = input("Choisissez un forfait : ")

    forfaits = {
        "1": 500,
        "2": 1000,          
        "3": 2000
    }
    if choix not in forfaits:
        print("Choix invalide")         
        return solde
    prix = forfaits[choix]       
    
    if prix > solde:
        print("Solde insuffisant")     
        return solde
    code = input("Entrez votre code secret 4 chiffres : ")
    while code != code_secret:
        print("Code secret incorrect")
        code = input("Entrez votre code secret 4 chiffres : ")
    solde -= prix      
    print("Forfait activé avec succès!")
    print(f"Nouveau solde : {solde}")
    ecrire_solde(solde)  #mettre à jour le fichier
    return solde        


def annuler_transfert(solde, dernier_transfert):    
    if dernier_transfert is None:           
        print("Aucun transfert à annuler") 
        return solde, None             
    print(f"Dernier transfert : {dernier_transfert} FCFA")         
    confirmation = input("Confirmer l'annulation (O/N) : ").upper()      
    if confirmation != "O":
        print("Annulation annulée")
        return solde, dernier_transfert
    code = input("Entrez votre code secret 4 chiffres : ")
    while code != code_secret:             
        print("Code secret incorrect")
        code = input("Entrez votre code secret 4 chiffres : ")
    solde += dernier_transfert           
    print("Transfert annulé avec succès")
    print(f"Nouveau solde : {solde}")
    ecrire_solde(solde)  #mettre à jour le fichier
    return solde, None         


def afficher_historique(historique):
    if not historique:
        print("Aucun transfert effectué")
        return
    print("\n" + "="*20 + " Historique des transferts " + "="*20)
    print()
    for h in historique:
        numero = h['numero'],
        montant = h['montant']
        print(f"Transfert de {montant} FCFA vers {numero}")


def service_ussd():
    code_ussd = "#144#"
    saisie = input("Composez le code USSD : ")
    while saisie != code_ussd:
        print("Code invalide")
        saisie = input("Composez le code USSD : ")
    dernier_transfert = None
    solde = lire_solde()  #lire le solde à partir du fichier
    historique = lire_historique()  #charger l'historique au démarrage
    print("Bienvenue sur Orange Money")
    choix = ""
    while choix != "7":
        afficher_menu_principal()
        choix = input("Choisissez une option : ")
        if choix == "1":
            consulter_solde(solde)
        elif choix == "2":
            solde = acheter_credit(solde)
        elif choix == "3":
            solde, dernier_transfert = effectuer_transfert(solde, historique) #passer l'historique
        elif choix == "4":
            solde = acheter_forfait(solde)
        elif choix == "5":
            solde, dernier_transfert = annuler_transfert(solde, dernier_transfert)
        elif choix == "6":
            afficher_historique(historique)
        elif choix == "7":
            print("Merci d'avoir utilisé Orange Money")
        else:
            print("Choix invalide")

service_ussd()
