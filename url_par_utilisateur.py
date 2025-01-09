import os
from collections import defaultdict
import re

def list_log_files(directory):
    """List all log files in the specified directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.startswith('log_proxy_') and f.endswith('.txt')]

def display_menu(files):
    """Display the menu of available log files for selection."""
    # Affiche la liste des fichiers de journal disponibles
    print("Fichiers journaux disponibles :")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    
    while True:
        try:
            # Demande à l'utilisateur de saisir le numéro du fichier à analyser
            choice = int(input("Entrez le numéro du fichier à analyser : ")) - 1
            if 0 <= choice < len(files):
                return files[choice]
            else:
                # Indique un choix invalide
                print("Choix invalide. Veuillez sélectionner un numéro valide.")
        except ValueError:
            # Indique que l'utilisateur doit saisir un numéro
            print("Veuillez entrer un numéro.")

def parse_log_file(filepath):
    """Parse the log file and extract user activity data."""
    # Dictionnaire pour suivre l'activité des utilisateurs
    user_activity = defaultdict(lambda: defaultdict(int))  # {IP: {URL: count}}
    url_pattern = re.compile(r'^https?://[\w\.-]+(?:/[^\s]*)?$')  # Regex améliorée pour capturer des URLs valides

    with open(filepath, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            parts = line.strip().split()
            if len(parts) >= 6:
                ip_address = parts[1]
                url = parts[4]
                # Vérifie si l'URL correspond au pattern
                if url_pattern.match(url):
                    user_activity[ip_address][url] += 1
                else:
                    # Affiche un message de débogage si l'URL est invalide
                    print(f"[DEBUG] URL invalide à la ligne {line_number}: {url}")
            else:
                # Affiche un message de débogage si la ligne est mal formée
                print(f"[DEBUG] Ligne mal formée ignorée à la ligne {line_number}: {line.strip()}")
    return user_activity

def analyze_user_activity(user_activity):
    """Analyze user activity to find the most visited URL for each user."""
    # Prépare un dictionnaire pour stocker les résultats
    results = {}
    for user, urls in user_activity.items():
        if urls:
            # Trouve l'URL la plus visitée
            most_visited_url = max(urls, key=urls.get)
            results[user] = (most_visited_url, urls[most_visited_url])
        else:
            # Affiche un message de débogage s'il n'y a pas d'URL valide
            print(f"[DEBUG] Aucune URL valide trouvée pour l'utilisateur {user}")
    return results

def display_results(results):
    """Display the analysis results."""
    # Affiche les résultats de l'analyse
    print("\nRésultats de l'analyse :")
    if not results:
        # Indique qu'aucune URL valide n'a été trouvée
        print("Aucune URL valide n'a été trouvée dans le fichier de journal.")
    else:
        # Affiche l'URL la plus visitée pour chaque utilisateur
        for user, (url, count) in results.items():
            print(f"Utilisateur {user} - URL la plus visitée : {url} ({count} visites)")

if __name__ == "__main__":
    # Spécifie le chemin du répertoire contenant les fichiers de journal
    log_directory = r"D:\\zzEcole\\aaPROJET\\\Étape 5\\Fichiers_logs_proxy"

    # Vérifie si le répertoire existe
    if not os.path.isdir(log_directory):
        print("Répertoire invalide. Veuillez vérifier que le chemin existe.")
    else:
        log_files = list_log_files(log_directory)

        # Vérifie s'il y a des fichiers de journal dans le répertoire
        if not log_files:
            print("Aucun fichier de journal trouvé dans le répertoire spécifié.")
        else:
            selected_file = display_menu(log_files)
            file_path = os.path.join(log_directory, selected_file)
            user_activity = parse_log_file(file_path)
            results = analyze_user_activity(user_activity)
            display_results(results)
