import os, subprocess, colorama, argparse, sys, giter
from github import Github

def get_credentials():
    """
    Prompts inputs to enter username and password for your Github account.
    Returns username and password.
    """
    username = str()
    passwd = str()
    
    # Set Github username
    print(colorama.Fore.YELLOW+"Enter Github username: ", end=" ")
    username = input(colorama.Fore.RESET)
    # Set Github password associated with the given username
    print(colorama.Fore.YELLOW+"Enter Github password: ", end=" ")
    passwd = input(colorama.Fore.RESET)

    return username, passwd

def authenticat_user():
    """ 
    Authenticate the credentials provided and return a Github user object.
    """
    username, passwd = get_credentials()

    try:
        print(colorama.Fore.YELLOW+"\nAuthenticating user...")
        user = Github(username, passwd).get_user()
        print(colorama.Fore.GREEN+f"User {user.login} has been authenticated!")
        return user
    except Exception as e:
        print(colorama.Fore.RED+repr(e))

def create_repo():
    """
    Creates a remote repository on Github.com and returns username and repo name.
    """
    repo = str()
    user = authenticat_user()
    # Set repo name
    print(colorama.Fore.YELLOW+"\nEnter repository name: ", end=" ")
    repo = input(colorama.Fore.RESET)

    try:
        print(colorama.Fore.YELLOW+f"\nCreating repo {repo}")
        user.create_repo(repo)
        print(colorama.Fore.GREEN+f"Repository {user.get_repo(repo).full_name} has been created")
        # Return username and repo name
        return user.name, repo
    except Exception as e:
        print(colorama.Fore.RED, repr(e))

def git_init(username, repo_name, https=False):
    """
    Initializes a git repo where this application has been called from!!! 
    """
    print()
    subprocess.run("git init", shell=True)
    subprocess.run("git add *", shell=True)
    subprocess.run("git commit -m \"Initial commit\"", shell=True)
    if https:
        subprocess.run(f"git remote add origin https://github.com/{username}/{repo_name}", shell=True)
    else:
        subprocess.run(f"git remote add origin git@github.com:{username}/{repo_name}.git", shell=True)
    subprocess.run("git push -u origin master", shell=True)


if __name__ == "__main__":
    colorama.init()
    parser = argparse.ArgumentParser(description="Command line application to quickly set up a new remote repository, initialize a local git repository and add the remote repo.")
    parser.add_argument("--init", "-i", action="store_true")
    parser.add_argument("--https", action="store_true")
    parser.add_argument("--create", "-c", action="store_true")
    parser.add_argument("--doc", action="store_true")
    args = parser.parse_args()

    # Create a new repo on Github.com
    if args.create:
        username, repo_name = create_repo()
    # If a new repo on Github.com already has been created also initialize a local git repo
    if args.init and args.create:
        git_init(username, repo_name, args.https)
    # Only initialize a local git repo. User will be prompted to enter his Github.com username and the desired repo name (has to be created already). 
    elif args.init and args.create == False:
        username = input(colorama.Fore.YELLOW+"Enter username: "+colorama.Fore.RESET)
        repo_name = input(colorama.Fore.YELLOW+"Enter repository name: "+colorama.Fore.RESET)
        git_init(username, repo_name, args.https)
    if args.doc:
        help(giter)
