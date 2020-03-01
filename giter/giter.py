#!/usr/bin/env python3
"""
    Command line application to quickly set up a new remote repository, initialize a local git repository and add the remote repo.
"""
# Standard libaries
import os
import subprocess
import argparse
import sys
import getpass
import requests
import time
import re
# Third party
from github import Github
from github import GithubObject
# Local
from giter import giter
from giter.colors import color

def authenticate_user(username, passwd):
    """
    Authenticate the credentials provided and return a Github user object.
    """
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
    print(color.BOLD+color.CYAN+"[Authentication]"+color.END)
    # Set Github username
    username = input(color.BOLD+"Enter Github username ➜ "+color.END)
    # Set Github password associated with the given username
    passwd = getpass.getpass(color.BOLD+"Enter password ➜ "+color.END)
    
    # Try to login with provided credentials and return github user object
    user = authenticate_user(username, passwd)
    
    print(color.BOLD+color.CYAN+"\n[Repository creation]"+color.END)
    # Set repo name
    repo = input(color.BOLD+"Enter repository name ➜ "+color.END)
    # Set repo description
    description = input(color.BOLD+"Enter repository description ➜ "+color.END)
    # Whether you want the repo to be private
    private = input(color.BOLD+"Private repository (y/n)? ➜ "+color.END)
    private = True if private == "y" else False

    try:
        gitignore_template = add_gitignore()
        print(color.BOLD+f"\nCreating repo {repo}", color.END)
        user.create_repo(repo, description=description, private=private, gitignore_template=gitignore_template)
        print(color.BOLD+color.GREEN+f"Repository {user.get_repo(repo).full_name} has been created"+color.END)
        time.sleep(1)
        # Add a license
        add_license(Github(username, passwd), repo)
        # Return username and repo name
        return user.login, repo
    except Exception as e:
        print(color.RED, repr(e))

def add_gitignore():
    """
    Adds a .gitignore to the repo.
    """
    # check if .gitignore already exists in root directory
    if (os.path.isfile('.gitignore')):
        # Do not add a new gitignore, use the current one
        return GithubObject.NotSet

    selection = input(color.BOLD+"\nSelect a .gitignore:\n[1] C\n[2] C++\n[3] Java\n[4] Node\n[5] Python\n[6] Other\n[7] None\n➜ ")
    if selection == '1':
        return 'C'
    elif selection == '2':
        return 'C++'
    elif selection == '3':
        return 'Java'
    elif selection == '4':
        return 'Node'
    elif selection == '5':
        return 'Python'
    elif selection == '6':
        try:
            print("Downloading list of .gitignore files...")
            response = requests.get("https://api.github.com/gitignore/templates")
            if response.status_code == 200:
                responseJSON = response.json()
                for idx, opt in enumerate(responseJSON):
                    print(f"[{idx}] {opt}")
                selection = int(input(color.BOLD+"Select your .gitignore file ➜ "))
                if selection >= 0 and selection < len(responseJSON):
                    return responseJSON[selection]
                else:
                    return GithubObject.NotSet
            else:
                print("Error in gitignore fetch: status_code = ", response.status_code)
                return GithubObject.NotSet

        except Exception as e:
            print("Error in gitignore fetch: ", str(e))
            return GithubObject.NotSet
    else:
        return GithubObject.NotSet

def add_license(github_obj, repo_name):
    """
    Adds a license to the repo.
    """
    selection = input(color.BOLD+"\nSelect a license:\n[1] GNU GPL v3\n[2] MIT\n[3] Apache\n[4] Unlicense\n[5] None\n➜ ")
    repo = github_obj.get_user().get_repo(repo_name)

    if selection == "1":
        repo.create_file("LICENSE.txt", "Initial commit", github_obj.get_license('gpl-3.0').body)
    elif selection == "2":
        repo.create_file("LICENSE.txt", "Initial commit", github_obj.get_license('mit').body)
    elif selection == "3":
        repo.create_file("LICENSE.txt", "Initial commit", github_obj.get_license('apache-2.0').body)
    elif selection == "4":
        repo.create_file("LICENSE.txt", "Initial commit", github_obj.get_license('unlicense').body)
    elif selection == "5":
        pass
    else:
        print(color.BOLD+color.RED+"Wrong Input! No license has been created."+color.END)

def add_readme(repo_name):
    """
    Replaces existing or creates a new README file
    """
    # Check for existing README
    files = os.listdir(".")
    regex = re.compile("readme*")
    matches = [file for file in files if re.match(regex, file.lower())]

    print(color.BOLD+"Looking for existing README..."+color.END)
    # README already exists
    if len(matches) > 0:
        print(color.BOLD+color.YELLOW+"README file already exists!"+color.END)
        # Replace README file by creating a new one
        if input(color.BOLD+"Replace existing README and REMOVE old README (y/n)? "+color.END).lower() == "y":
            # Remove old README
            os.remove(matches[0])
            # Create new README
            with open("README.md", "w") as file:
                file.write(f"# {repo_name}")
                file.close()
    # No existing README found
    else:
        print(color.BOLD+"No README found."+color.END)
        if input(color.BOLD+"Create README (y/n)? "+color.END) == "y":
            with open("README.md", "w") as file:
                    file.write(f"# {repo_name}")
                    file.close()

def git_init(username, repo_name, https=False):
    """
    Initializes a git repo where this application has been called from.
    """
    print(color.BOLD+color.CYAN+"\n[Setting up git repository]"+color.END)
    
    # Replace existing README or create a new one
    add_readme(repo_name)

    subprocess.run(["git", "init"])
    subprocess.run(["git", "add", "*"])
    subprocess.run(["git", "commit", "-m", "Initial commit"])
    if https:
        subprocess.run(["git", "remote", "add", "origin", f"https://github.com/{username}/{repo_name}"])
    else:
        subprocess.run(["git", "remote", "add", "origin", f"git@github.com:{username}/{repo_name}.git"])
    subprocess.run(["git", "pull", "origin", "master:master"])
    subprocess.run(["git", "rebase", "origin/master"])
    subprocess.run(["git", "push", "-u", "origin", "master"])

def main():
    parser = argparse.ArgumentParser(description="Command line application to quickly set up a new remote repository, initialize a local git repository and add the remote repo.")
    parser.add_argument("--init", "-i", action="store_true", help="Initialize a local git repository and add an EXISTING repository as remote.")
    parser.add_argument("--https", action="store_true", help="Use https instead of ssh.")
    parser.add_argument("--create", "-c", action="store_true", help="Create a repository on Github.com.")
    parser.add_argument("--doc", action="store_true")
    args = parser.parse_args()

    try:
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
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
