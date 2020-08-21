# Commands
`git clone` : Downloads a local copy of a repository e.g. `git clone https://github.com/mike-colletta/py4DSTEM.git`

`git status` : Shows the status of the local repository

`git branch` : Shows the branches in the repository

`git checkout` : Switch branches ( e.g. `git checkout dev` to switch to the dev branch), create new branches ( e.g. `git checkout -b aNewBranch` to create a new branch called aNewBranch), and access previous commits (e.g. `git checkout [hash]`)

`git log` : Shows previous commits

`git add` : Adds changes in a file/files to the index for a commit. e.g. `git add *` will add all changed files, `git add README.md` only adds the README

`git rm` : Removes a file both from the local repository and from the index. Use when you want to remove a file from the repository. e.g. `git rm README.md`

`git mv` : Moves a file both in the local repository and the index. Use when you want to move or rename a file. e.g. `git mv README.md MEREAD.md` renames README.md to MEREAD.md

`git commit` : Creates a commit with the current state of the index (all changes add-ed, rm-ed, mv-ed). Use the -m flag to add a message, e.g. `git commit -m "Added new subroutine"`

`git push` : Updates the remote (github) with your commits

`git pull` : Updates your local repository with changes from the remote (github).

# Example workflows

## Cloning this repository and switching to the working branch

`git clone https://github.com/mike-colletta/py4DSTEM.git`

`git checkout workingBranch`

## Pulling new changes from github and viewing them
`git pull` : this will give you an output with the hashes for the commits, copy from here, or from `git log`

`git diff [hash]` to inspect changes

## Updating github with your changes
`git add *`

`git commit -m "new changes"`

`git push`


