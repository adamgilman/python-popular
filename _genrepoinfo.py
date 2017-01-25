from time import sleep
import subprocess
import os

packages = open('package.list', 'r').read().split("\n")
completed = os.listdir("./datastore/")
remaining = list( set(packages) - set(completed) )
try:
    remaining.remove("")
except ValueError:
    pass

for p in remaining:
    command = ['luigi', '--module', 'luigi_getinfo', 'GetRepoRequirements', '--package', p]
    print command
    out = subprocess.check_output(command)
    print out