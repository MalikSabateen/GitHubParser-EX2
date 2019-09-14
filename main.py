## Imports
import git
from git import Repo
choice=input("If you have the GitHub Repo already downloaded please enter 'yes', if you would like to download it please enter 'no'.\n")
if choice == "yes":
    repo_link=input("Please enter the location of the GitHub Repo you would like to analyse.\n")
    repo = git.Repo(repo_link)
elif choice == "no":
    repo_link=input("Please enter the URL of the GitHub Repo.\n")
    repo_location=input("Please enter the folder name for this Repo.\n")
    print("Please note this may take some time...")
    repo = Repo.clone_from(repo_link,repo_location)
    print("Repo has been downloaded successfully.")
commit_id=input("Please enter the GitHub Fixing Commit you would like to analyse.\n")
print("---TITLE & COMMENT---")
fix_commit=repo.commit(commit_id)
print(fix_commit.message)
stats=fix_commit.stats
print("---Number of Files Changed---")
print(len(stats.files))
list=[]
for item in stats.files:
    if(item.rsplit("/",1)[0]) not in list:
        list.append(item.rsplit("/",1)[0])
print("---Number of Directories Changed---")
print(len(list))
