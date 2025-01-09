import random  # Importer le module random pour générer des nombres aléatoires
import os      # Importer le module os pour gérer les chemins de fichiers

# Définir le chemin du dossier contenant les fichiers
dossier = r"D:\zzEcole\aaPROJET\Étape 1"

# Définir le chemin du fichier d'entrée (testEntree.txt) et du fichier de sortie (testSortie.txt)
fichier_entree = os.path.join(dossier, "testEntree.txt")
fichier_sortie = os.path.join(dossier, "testSortie.txt")

# Vérifier si le fichier d'entrée existe
if not os.path.exists(fichier_entree):  # Si le fichier d'entrée n'existe pas
    print(f"Le fichier d'entrée {fichier_entree} n'existe pas.")  # Afficher un message d'erreur
else:
    try:
        # Lecture du fichier d'entrée
        print(f"Lecture du fichier {fichier_entree}...")  # Afficher que la lecture du fichier commence
        with open(fichier_entree, 'r') as fichier:  # Ouvrir le fichier en mode lecture
            lignes = fichier.readlines()  # Lire toutes les lignes du fichier

        pseudonymes = []  # Créer une liste vide pour stocker les pseudonymes générés

        # Parcourir chaque ligne lue du fichier
        for ligne in lignes:
            try:
                # Découper la ligne en prénom, nom et année de naissance
                prenom, nom, annee_naissance = ligne.strip().split(";")  # Utiliser strip pour enlever les espaces superflus
                annee_naissance = int(annee_naissance)  # Convertir l'année de naissance en entier

                # Calculer l'âge à partir de l'année de naissance
                annee_actuelle = 2025  # Définir l'année actuelle
                age = annee_actuelle - annee_naissance  # Calculer l'âge

                # Générer un pseudonyme
                initiale_prenom = prenom[0].lower()  # Prendre la première lettre du prénom en minuscule
                debut_nom = nom[:3].lower()  # Prendre les trois premières lettres du nom en minuscule
                nombre_aleatoire = random.randint(10, 99)  # Générer un nombre aléatoire entre 10 et 99
                pseudo = f"{initiale_prenom}{debut_nom}{age}{nombre_aleatoire}"  # Créer le pseudonyme

                # Ajouter le pseudonyme généré à la liste des pseudonymes
                pseudonymes.append(pseudo)

            except ValueError:  # Si une erreur se produit lors de la découpe ou de la conversion des données
                print(f"Ligne mal formatée : {ligne.strip()}")  # Afficher un message d'erreur avec la ligne concernée

        # Vérifier si la liste des pseudonymes n'est pas vide
        if pseudonymes:  # Si la liste des pseudonymes contient des éléments
            # Écriture des pseudonymes dans le fichier de sortie
            print(f"Écriture des pseudonymes dans le fichier {fichier_sortie}...")  # Afficher un message pour indiquer que l'écriture commence
            with open(fichier_sortie, 'w') as fichier:  # Ouvrir le fichier de sortie en mode écriture
                for pseudo in pseudonymes:  # Parcourir chaque pseudonyme dans la liste
                    fichier.write(pseudo + "\n")  # Écrire chaque pseudonyme suivi d'une nouvelle ligne

            print(f"Pseudonymes générés et écrits dans {fichier_sortie}")  # Afficher un message de confirmation

        else:  # Si la liste des pseudonymes est vide
            print("Aucun pseudonyme généré, la liste est vide.")  # Afficher un message indiquant que la liste est vide

    except Exception as e:  # Si une exception quelconque se produit pendant le processus
        print(f"Une erreur est survenue : {e}")  # Afficher l'erreur
