import json
import time
import hashlib
from git import Repo
from pathlib import Path


# Returns a list of all non-hidden, non virtualenv, file paths
def get_paths():
    result = list()

    p = Path('.')
    # Create a list of all directories
    directories = list(p.glob("**"))
    # Now convert these to strings
    directories = list(map(lambda x: str(x), directories))
    # Now remove any that start with . (hidden directories)
    # and any that start with env (our virtualenv)
    directories = list(filter(lambda x: x[0] != '.' and x[0:3] != 'env',
                                                directories))

    # Add the current directory to directories
    directories.append('.')
    for directory in directories:
        p = Path(directory)
        # Select all strings in this path
        files = list(p.glob('*.*'))
        # Now convert these to strings again
        files = list(map(lambda x: str(x), files))
        # Now remove any that start with . (hidden files)
        files = list(filter(lambda x: x[0] != '.', files))
        # Now append
        result.extend(files)
    return result

# Gets an MD5 hash of all files in the tree
def get_md5():
    md5 = hashlib.md5()
    for filename in get_paths():
        file = open(filename, "r")
        while True:
            data = file.read(32)
            if not data:
                break
            md5.update(data.encode("utf-8"))
    return md5.hexdigest()


if(__name__ == "__main__"):
    config = dict()
    print("""HOW TO USE:
This simply sets up config.json with a hash of updater.py and more.
At the end, it also runs an equivalent of the following with GitPython:
$ git add .
$ git commit -m "Update to version <new version>"
$ git push origin master

SHORTCOMING: If you add a new file to here, you'll need to make sure to git
add it prior to running this script.

This program assumes you've already written a new program to update.py
AND that there is a repository in the current directory.

Also, THIS WAS DONE FOR TIME'S SAKE! -- DO NOT USE IN PRODUCTION!
Ideally, we would be using a server that's not literally just raw github.
But so I could focus on code instead of writing a server for just getting
files, I stuck with this. 
    """)

    config["version"] = input("Input a version: ")
    # Make sure our version is a number
    if len(config["version"]) == 0 or not config["version"].replace(".","").isdigit():
        raise Exception("Version must be in the format x.x.x..., where x is an integer")

    config["notes"] = input("Add any release notes: ")
    config["date"] = int(time.time())
    config["hash"] = get_md5()
    
    file = open("config.json", "w")
    json.dump(config, file)
    file.close()

    try:
        print("Initializing git...", end="")
        repo = Repo(".git")
        print("done.")
        repo.git.add(update=True)        
        repo.index.commit("Update to version {0}".format(config["version"]))
        print("Committed")
        print("Pushing...")
        repo.git.push("origin", "master")
        print("done.")
    except:
        print("Something failed with git. Try pushing manually.")