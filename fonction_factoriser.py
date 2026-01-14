def demander_montant(message, solde=None):
    while True:
        montant = input(message)
        if not montant.isdigit() or int(montant) <= 0:
            print("Montant invalide, veuillez entrer un montant positif.")
        elif solde is not None and int(montant) > solde:
            print("Solde insuffisant.")
        else:
            return int(montant)

#utilisation avec try/except

def demander_montant(message, solde=None):
    while True:
        try:
            montant = float(input(message))  # Utiliser float pour permettre des montants décimaux
            if montant <= 0:
                raise ValueError("Le montant doit être positif.")
            if solde is not None and montant > solde:
                raise ValueError("Solde insuffisant.")
            return montant
        except ValueError as e:
            print(e)
            print("Veuillez entrer un montant valide.")



def demander_numero(message):
    while True:
        numero = input(message)
        if not numero.isdigit() or len(numero) != 9:
            print("Numéro incorrect, veuillez saisir un numéro à 9 chiffres.")
        else:
            return numero
        
#utilisation avec try except
def demander_numero(message):
    while True:
        try:
            numero = input(message)
            if not numero.isdigit() or len(numero) != 9:
                raise ValueError("Numéro incorrect, veuillez saisir un numéro à 9 chiffres.")
            return numero
        except ValueError as e:
            print(e)

        
#avec try /except appelle des argument sur la fonction

def effectuer_transfert(solde, historique):
    numero = demander_numero("Entrez le numéro du destinataire : ")
    montant = demander_montant("Entrez le montant à transférer : ", solde)

    if not demander_code_secrett():
        return solde, None

    solde -= montant
    historique.append({'type': 'transfert', 'numero': numero, 'montant': montant})
    ecrire_historique(historique)
    print(f"Transfert de {montant} vers {numero} effectué avec succès.")
    print(f"Nouveau solde : {solde}")
    ecrire_solde(solde)
    return solde, montant


# utilisation de try/except 
def demander_montant(message, solde=None):
    while True:
        montant = input(message)
        if not montant.isdigit() or int(montant) <= 0:
            print("Montant invalide, veuillez entrer un montant positif.")
        elif solde is not None and int(montant) > solde:
            print("Solde insuffisant.")
        else:
            return int(montant)

def demander_numero(message):
    while True:
        numero = input(message)
        if not numero.isdigit() or len(numero) != 9:
            print("Numéro incorrect, veuillez saisir un numéro à 9 chiffres.")
        else:
            return numero

def demander_code_secrett():
    code = input("Entrez votre code secret 4 chiffres : ")
    for _ in range(3):  # Offre 3 tentatives
        if code == code_secret:
            return True
        print("Code secret incorrect, essayez à nouveau.")
        code = input("Entrez votre code secret 4 chiffres : ")
    print("Nombre de tentatives dépassé.")
    return False
