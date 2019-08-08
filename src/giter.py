#!/bin/python
"""
    Command line application to quickly set up a new remote repository, initialize a local git repository and add the remote repo.
"""
import os, subprocess, argparse, sys, getpass
from github import Github
from . import giter

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

def authenticat_user(pUsername="", pPasswd=""):
    """ 
    Authenticate the credentials provided and return a Github user object.
    """
    username, passwd = get_credentials()

    if pUsername == "" and pPasswd == "":
        try:
            print(color.BOLD+"\nAuthenticating user...")
            user = Github(username, passwd).get_user()
            print(color.GREEN+f"User {user.login} has been authenticated!"+color.END)
            # Return Github user object
            return user
        except Exception as e:
            print(color.RED+repr(e))
            sys.exit()
    else:
        try:
            user = Github(pUsername, pPasswd).get_user()
            return user
        except Exception as e:
            print(repr(e), file=sys.stderr)

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
        # Return username and repo name
        return user.login, repo
    except Exception as e:
        print(color.RED, repr(e))

def git_init(username, repo_name, https=False):
    """
    Initializes a git repo where this application has been called from.
    """
    print(color.BOLD+color.CYAN+"\n[Setting up git repository]"+color.END)
    
    subprocess.run("git init", shell=True)
    subprocess.run("echo \"# test\" >> README.md", shell=True)
    subprocess.run("git add *", shell=True)
    subprocess.run("git commit -m \"Initial commit\"", shell=True)
    if https:
        subprocess.run(f"git remote add origin https://github.com/{username}/{repo_name}", shell=True)
    else:
        subprocess.run(f"git remote add origin git@github.com:{username}/{repo_name}.git", shell=True)
    subprocess.run("git push -u origin master", shell=True)
    subprocess.run("git branch --set-upstream-to=origin/master master", shell=True)

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
        print(color.BOLD+color.RED+"Both --init and --create have to be used. Only --create can be used alone.")
    elif args.doc:
        help(giter)
    else:
        parser.print_help()