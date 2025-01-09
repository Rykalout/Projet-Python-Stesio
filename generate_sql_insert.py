import os  # Module pour gérer les fichiers et répertoires


def list_log_files(directory):
    """
    Liste tous les fichiers log disponibles dans le répertoire donné.
    Retourne une liste des fichiers trouvés.
    """
    try:
        files = [f for f in os.listdir(directory) if f.startswith("log_proxy_") and f.endswith(".txt")]
        if not files:
            print("Aucun fichier log trouvé dans le répertoire spécifié.")
        return files
    except FileNotFoundError:
        print(f"Erreur : Le dossier '{directory}' n'existe pas ou n'est pas accessible.")
        return []


def parse_log_file(filepath):
    """
    Analyse le contenu d'un fichier log et retourne une liste de dictionnaires représentant chaque ligne.
    Format attendu de chaque ligne (exemple) :
    00:10:58 192.168.2.100 PUT https://www.netflix.com 200 [optionnel]
    """
    parsed_data = []
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 5:
                # Trop peu d'éléments, on saute la ligne
                continue

            # On mappe :
            # parts[0] = "00:10:58"
            # parts[1] = "192.168.2.100"
            # parts[2] = "PUT"
            # parts[3] = "https://www.netflix.com"
            # parts[4] = "200" ou "231+2460"
            heure        = parts[0]
            adresse_ip   = parts[1]
            methode_http = parts[2]
            url          = parts[3]
            code_reponse = parts[4]  # ou parts[5] si c'est celui-ci que vous voulez

            parsed_data.append({
                # Pas de date séparée dans votre log => on peut laisser vide
                "date": "",
                "heure": heure,
                "adresse_ip": adresse_ip,
                "url": url,
                "methode_http": methode_http,
                "code_reponse": code_reponse
            })
    return parsed_data


def generate_sql_insert_file(parsed_data, output_filename):
    with open(output_filename, "w") as sql_file:
        sql_file.write("-- Script SQL généré automatiquement\n")
        sql_file.write(f"-- Fichier : {output_filename}\n\n")
        sql_file.write(
            "INSERT INTO journaux_acces (horodatage, adresse_ip_employe, url_consultee, methode_http, code_reponse)\n"
            "VALUES\n"
        )
        
        total = len(parsed_data)
        for i, entry in enumerate(parsed_data):
            horodatage = entry["heure"]
            adresse_ip = entry["adresse_ip"]
            code       = entry["code_reponse"]
            methode    = entry["methode_http"]
            url        = entry["url"]

            # Si ce n'est pas la dernière ligne, on met une virgule à la fin
            if i < total - 1:
                sql_file.write(
                    f"('{horodatage}', '{adresse_ip}', '{code}', '{methode}', '{url}'),\n"
                )
            else:
                # Dernière ligne : pas de virgule
                sql_file.write(
                    f"('{horodatage}', '{adresse_ip}', '{code}', '{methode}', '{url}')\n"
                )

        # Ici, plus besoin de seek()
        sql_file.write(";\n")

    print(f"Fichier SQL généré : {output_filename}")



def main():
    """
    Fonction principale pour exécuter le programme.
    """
    directory = r"C:\Users\esteb\Downloads\Fichiers_logs_proxy\Fichiers_logs_proxy"
    files = list_log_files(directory)
    
    if not files:
        print("Aucun fichier log trouvé ou dossier inaccessible.")
        return

    print("Fichiers logs disponibles :")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

    try:
        choice = int(input("Entrez le numéro du fichier à traiter : ")) - 1
    except ValueError:
        print("Choix invalide. Veuillez entrer un nombre.")
        return
    
    if choice < 0 or choice >= len(files):
        print("Choix invalide.")
        return

    selected_file = files[choice]
    filepath = os.path.join(directory, selected_file)
    print(f"Fichier sélectionné : {selected_file}")

    parsed_data = parse_log_file(filepath)

    # Dans vos noms de fichiers, vous avez un format log_proxy_<quelque_chose>.txt
    # si vous voulez extraire la date (ex: "log_proxy_20250108.txt"), vous pouvez :
    # log_date = selected_file.split("_")[2].split(".")[0]
    # Mais si ce n'est pas pertinent, vous pouvez simplement générer un timestamp
    # ou laisser comme vous préférez.
    log_date = selected_file.split("_")[2].split(".")[0]  # si vos fichiers s'appellent log_proxy_20250108.txt
    output_filename = f"insert_log_{log_date}.sql"
    
    generate_sql_insert_file(parsed_data, output_filename)


if __name__ == "__main__":
    main()
