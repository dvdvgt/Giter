#!/bin/python
"""
    Command line application to quickly set up a new remote repository, initialize a local git repository and add the remote repo.
"""
import os, subprocess, argparse, sys, getpass, giter, requests, time
from github import Github
from bs4 import BeautifulSoup

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def get_credentials():
    """
    Prompts inputs to enter username and password for your Github account.
    Returns username and password.
    """
    username = str()
    passwd = str()
    print(color.BOLD+color.CYAN+"[Authentication]"+color.END)
    # Set Github username
    username = input(color.BOLD+"Enter Github username ➜ "+color.END)
    # Set Github password associated with the given username
    passwd = getpass.getpass(color.BOLD+"Enter password ➜ "+color.END)

    return username, passwd

def authenticat_user():
    """ 
    Authenticate the credentials provided and return a Github user object.
    """
    username, passwd = get_credentials()
    try:
        print(color.BOLD+"\nAuthenticating user...")
        user = Github(username, passwd).get_user()
        print(color.GREEN+f"User {user.login} has been authenticated!"+color.END)
        # Return Github user object
        return user
    except Exception as e:
        print(color.RED+repr(e))
        sys.exit()

def create_repo():
    """
    Creates a remote repository on Github.com and returns username and repo name.
    """
    user = authenticat_user()
    print(color.BOLD+color.CYAN+"\n[Repository creation]"+color.END)
    # Set repo name
    repo = input(color.BOLD+"Enter repository name ➜ "+color.END)
    # Set repo description
    description = input(color.BOLD+"Enter repository description ➜ "+color.END)
    # Whether you want the repo to be private
    private = input(color.BOLD+"Private repository (y/n)? ➜ "+color.END)
    private = True if private == "y" else False

    try:
        print(color.BOLD+f"\nCreating repo {repo}", color.END)
        user.create_repo(repo, description=description, private=private)
        print(color.BOLD+color.GREEN+f"Repository {user.get_repo(repo).full_name} has been created"+color.END)
        time.sleep(1)
        # Add a license
        add_license(user, repo)
        # Return username and repo name
        return user.login, repo
    except Exception as e:
        print(color.RED, repr(e))

def add_license(user, repo_name):
    GPL_3 = r"https://www.gnu.org/licenses/gpl-3.0.txt"
    GPL_3_text = requests.get(GPL_3).text

    apache = r"https://www.apache.org/licenses/LICENSE-2.0.txt"
    apache_text = requests.get(apache).text

    mit = r"https://choosealicense.com/licenses/mit/"
    mit_req = requests.get(mit)
    mit_soup = BeautifulSoup(mit_req.text, "html.parser")
    mit_text = mit_soup.select("pre")[0].text

    selection = input(color.BOLD+"\nSelect a license:\n[1] GNU GPL v3\n[2] MIT\n[3] Apache\n[4] None\n➜ ")
    repo = user.get_repo(repo_name)

    if selection == "1":
        repo.create_file("LICENSE.txt", "Initial commit", GPL_3_text)
    elif selection == "2":
        repo.create_file("LICENSE.txt", "Initial commit", mit_text)
    elif selection == "3":
        repo.create_file("LICENSE.txt", "Initial commit", apache_text)
    elif selection == "4":
        pass
    else:
        print(color.BOLD+color.RED+"Wrong Input! No license has been created."+color.END)

def git_init(username, repo_name, https=False):
    """
    Initializes a git repo where this application has been called from.
    """
    print(color.BOLD+color.CYAN+"\n[Setting up git repository]"+color.END)
    
    subprocess.run("git init", shell=True)
    subprocess.run(f"echo \"# {repo_name}\" >> README.md", shell=True)
    subprocess.run("git add *", shell=True)
    subprocess.run("git commit -m \"Initial commit\"", shell=True)
    if https:
        subprocess.run(f"git remote add origin https://github.com/{username}/{repo_name}", shell=True)
    else:
        subprocess.run(f"git remote add origin git@github.com:{username}/{repo_name}.git", shell=True)
    subprocess.run("git pull origin master:master", shell=True)
    subprocess.run("git rebase origin/master", shell=True)
    subprocess.run("git push -u origin master", shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command line application to quickly set up a new remote repository, initialize a local git repository and add the remote repo.")
    parser.add_argument("--init", "-i", action="store_true")
    parser.add_argument("--https", action="store_true")
    parser.add_argument("--create", "-c", action="store_true")
    parser.add_argument("--doc", action="store_true")
    args = parser.parse_args()

    # Create a new repo on Github.com
    if args.init == False and args.create:
        username, repo_name = create_repo()
    # Create a new repo on github.com, initialize a local git repo and add the remote repo
    elif args.init and args.create:
        username, repo_name = create_repo()
        git_init(username, repo_name, args.https)
    # Only initialize a local git repo and add a already created remote github repo.
    elif args.init and args.create == False:
        user = input(color.BOLD+"Github username ➜ "+color.END)
        repo_name = input(color.BOLD+"Repository name ➜ "+color.END)
        git_init(user, repo_name)
    elif args.doc:
        help(giter)
    else:
        parser.print_help()