import os
import subprocess
import requests

######################################Clone Client Repo###################################
reponame = input("Enter the full name of git repository: ")
print(reponame)
#directory=reponame.strip('git@github.com:someRepoOwnerrr/')
directory=reponame[15:]
pwd=os.getcwd()
pipe=subprocess.Popen(['git', 'clone', str(reponame), str(pwd +'/'+ directory)])
pipe.wait()
os.chdir(directory)
print('master is cloned to ' + os.getcwd())

def getnamebrances():
        proc = subprocess.Popen(['git', 'branch', '-a'],stdout=subprocess.PIPE)
        text = proc.communicate()[0].decode('utf-8')
        branches = []
        counter = 0
        for i in text.splitlines():
                counter += 1
#               if counter>2:
                branches.append(i[17:])
        return branches

branchList=getnamebrances()
print('total branches = ' + str(len(branchList)))

for branch in branchList:
        pipe=subprocess.Popen(['git', 'checkout', '-b', branch, str('origin/'+ branch) ])
        pipe.wait()
