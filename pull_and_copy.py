import os
import shutil
from git import Repo

print("GITHUB_TOKEN:", os.getenv("GITHUB_TOKEN"))

repo_path = "/dnt/2024_DS1_Mechelen"
doel_path = "/workdir"
token = os.getenv("GITHUB_TOKEN")
repo_url = f"https://{token}@github.com/oclaerbout/2024_DS1_Mechelen.git" if token else "https://github.com/oclaerbout/2024_DS1_Mechelen.git"
print(f"Repository URL: {repo_url}")

def initialize_repo():
    # Controleer of de map bestaat en maak deze aan indien nodig
    if not os.path.isdir(repo_path):
        os.makedirs(repo_path)
        print(f"map {repo_path} aangemaakt")
    # Controleer of het al een Git-repository is
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        # Initialiseer de repository en voeg de remote 'origin' toe
        repository = Repo.clone_from(repo_url, repo_path)
        print(f"repository gekloond en remote origin toegevoegd")
    else:
        #open de bestaande repository
        repository = Repo(repo_path)
        origin = repository.remotes.origin
        origin.set_url(repo_url)
        print("Bestaande repository geopend en remote URL bijgewerkt.")
    return repository

def pull_repo(repository):
    origin = repository.remotes.origin
    origin.pull()
    print("Repository bijgewerkt met de laatste wijzigingen.")

def copy_files():
        if not os.path.isdir(doel_path):
            os.makedirs(doel_path)
            print(f"map {doel_path} aangemaakt")
        # Kopieer de bestanden van repo_path naar doel_path
        print(f"kopieren bestanden van {repo_path} naar {doel_path}")
        for item in os.listdir(repo_path):
            s = os.path.join(repo_path, item)
            d = os.path.join(doel_path, item)

            if item == ".git":
                print(f"Slaat {s} over (git directory)")
                continue
            if os.path.isdir(s):
                if not os.path.exists(d):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                    print(f"Kopieer map {s} naar {d}")
                else:
                    for root, dirs, files in os.walk(s):
                        # creëer submappen als ze nog niet bestaan in de doellocatie
                        relative_path = os.path.relpath(root, s)
                        dest_dir = os.path.join(d, relative_path)
                        if not os.path.exists(dest_dir):
                            os.makedirs(dest_dir)

                        for file in files:
                            src_file = os.path.join(root, file)
                            dest_file = os.path.join(dest_dir, file)
                            if not os.path.exists(dest_file):
                                shutil.copy2(src_file, dest_file)
                                print(f"Kopieer nieuw bestand {src_file} naar {dest_file}")
                            else:
                                print(f"Overslaat bestaand bestand {dest_file}")

            elif os.path.isfile(s):
                if not os.path.exists(d):
                    shutil.copy2(s, d)
                    print(f"Kopieer {s} naar {d}")
                else:
                    print(f"Overslaat bestaand bestand {d}")
        print("Bestanden succesvol gekopieerd.")


if __name__ == "__main__":
    repo = initialize_repo()
    pull_repo(repo)
    copy_files()