import json
import time
import hashlib
from git import Repo

def get_md5(filename):
    md5 = hashlib.md5()
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
This program assumes you've already written a new program to update.py
AND that there is a repository in the current directory.

Please make sure your origin is set as https://github.com/NoahFiner/groove-remote.git

This simply sets up config.json and also runs an equivalent of the following with GitPython:
$ git add -A
$ git commit -m "Update to version <new version>"
$ git push origin master
    """)

    config["version"] = input("Input a version: ")
    # Make sure our version is a number
    if len(config["version"]) == 0 or not config["version"].replace(".","").isdigit():
        raise Exception("Version must be in the format x.x.x..., where x is an integer")

    config["notes"] = input("Add any release notes: ")
    config["date"] = int(time.time())
    config["hash"] = get_md5("updater.py")
    
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
        print("Pushing...", end="")
        repo.git.push("origin", "master")
        print("done.")
    except:
        print("Something failed with git. Try pushing manually.")