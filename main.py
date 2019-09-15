## Imports
import git
import re
from git import Repo
from datetime import datetime

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
print("\t",len(stats.files))
list=[]
for item in stats.files:
    if(item.rsplit("/",1)[0]) not in list:
        list.append(item.rsplit("/",1)[0])
print("---Number of Directories Changed---")
print("\t",len(list))
print("---Number of Lines Deleted (With Comments & Blank Lines)---")
print("\t",stats.total['deletions'])
print("---Number of Lines Inserted (With Comments & Blank Lines)---")
print("\t",stats.total['insertions'])
commit_changes=repo.git.show(fix_commit)
comment_D=0;
comment_A=0;
for line in commit_changes.splitlines():
    if line:
        if (line[0] == '-'):
            if (len(line) < 2 or re.match('^(\/\/)|^(\/\*)|^#|^\*',line[1:].strip())):
                comment_D = comment_D + 1
        elif (line[0] == '+'):
            if (len(line) < 2 or re.match('^(\/\/)|^(\/\*)|^#|^\*',line[1:].strip())):
                comment_A = comment_A + 1
print("---Number of Lines Deleted (Without Comments & Blank Lines)---")
print ("\t",stats.total['deletions']-comment_D)
print("---Number of Lines Inserted (Without Comments & Blank Lines)---")
print ("\t",stats.total['insertions']-comment_A)
print("---Time between the Fixing Commit and the Previous Commit for each File---")
for item in stats.files:
    print("\t--"+item+"--")
    dateone=datetime.strptime(repo.git.log(fix_commit,'--',item,n=1,format="%cd"),'%a %b %d %H:%M:%S %Y %z')
    if (repo.git.log(item,n=1,skip=1,format="%cd")is not ""):
        datetwo=datetime.strptime(repo.git.log(fix_commit,'--',item,n=1,skip=1,format="%cd"),'%a %b %d %H:%M:%S %Y %z')
        print("\t\t",dateone-datetwo)
    else:
        print("\t\tThis file does not have any prior commits")
print("---Number of Modifications for each File---")
for item in stats.files:
    print("\t--"+item+"--")
    list=repo.git.log(fix_commit,'--',item,format="%cd").splitlines()
    print("\t\t",(len(list)))
print("---Developers which have made Modifications to a File---")
for item in stats.files:
    print("\t--"+item+"--")
    list=[]
    listnum=[]
    authors=repo.git.log(fix_commit,"--",item,format="%an").split("\n")
    for author in authors:
        if (author.casefold() not in list):
            list.append(author.casefold())
            listnum.append(author.casefold())
        elif (author.casefold() in list):
            listnum.append(author.casefold())
    for name in list:
        print("\t\tAuthor: ",name.casefold())
        print("\t\t\tNumber of Changes: ",listnum.count(name.casefold()))