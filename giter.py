import os, subprocess, colorama, argparse, sys
from github import Github

def get_credentials():
    """
    Prompts inputs to enter username and password for your Github account.
    Returns username and password.
    """
    username = str()
    passwd = str()
    
    #Set Github username
    print(colorama.Fore.YELLOW+"Enter Github username: ", end=" ")
    username = input(colorama.Fore.RESET)
    #Set Github password associated with the given username
    print(colorama.Fore.YELLOW+"Enter Github password: ", end=" ")
    passwd = input(colorama.Fore.RESET)

    return username, passwd

def authenticat_user():
    username, passwd = get_credentials()

    try:
        print(colorama.Fore.YELLOW+"\nAuthenticating user...")
        user = Github(username, passwd).get_user()
        print(colorama.Fore.GREEN+f"User {user.login} has been authenticated!")
        return user
    except Exception as e:
        print(colorama.Fore.RED+repr(e))

def create_repo():
    repo = str()
    user = authenticat_user()
    user
    #Set repo name
    print(colorama.Fore.YELLOW+"\nEnter repository name: ", end=" ")
    repo = input(colorama.Fore.RESET)

    try:
        print(colorama.Fore.YELLOW+f"\nCreating repo {repo}")
        user.create_repo(repo)
        print(colorama.Fore.GREEN+f"Repository {user.get_repo(repo).full_name} has been created")
        #Return username and repo name
        return user.name, repo
    except Exception as e:
        print(colorama.Fore.RED, repr(e))

def git_init(username, repo_name, https=True):
    """
    Initializes a git repo at the path 
    """
    subprocess.run("git init", shell=True)
    subprocess.run("git add *", shell=True)
    subprocess.run("git commit -m \"Initial commit\"", shell=True)
    if https:
        subprocess.run(f"git add origin https://github.com/{username}/{repo_name}", shell=True)
    else:
        subprocess.run(f"git add origin git@github.com:{username}/{repo_name}", shell=True)
    subprocess.run("git push -u origin master", shell=True)


if __name__ == "__main__":
    colorama.init()
    parser = argparse.ArgumentParser(description="Command line application to quickly set up new repositories on Github and add to as origin to your local repo.")
    parser.add_argument("--init", "-i", action="store_true")
    parser.add_argument("--https", action="store_true")
    parser.add_argument("--create", "-c", action="store_true")
    args = parser.parse_args()

    if args.create:
        username, repo_name = create_repo()
    if args.init and args.create:
        git_init(username, repo_name, args.https)
    elif args.init and args.create == False:
        username = input(colorama.Fore.YELLOW+"Enter username: ")
        repo_name = input(colorama.Fore.YELLOW+"Enter repository name: ")
        git_init(username, repo_name, args.https)
