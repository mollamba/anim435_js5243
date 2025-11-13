# Assignment 5 
## Animation File Creator
### Jacob Stratton : Last revised 11/13/2025
# Summary
This script asks the user to enter a set of names for animation file names from a user. This script will also grab environment variables from bash.

## How to use it
To start in bash, initialize 2 environment variables before running the script:
```
$ export NAME=jacob
$ export PNAME=doublin
```

NAME is your name, and PNAME is the name of the project you're working in.
The filename output will look something like this
```
jacob_doublin_[animationNameHere].ma
```

Then run the script. It will prompt you to enter animation file names. A logger Info will print, prompting the user that they must ender a file name that starts with a letter.

If the user does not, they will get warnings for every input that does not start with a letter, until the user does. 

Lastly, if the script cannot find a directory it will log Error to the user. 

When the user has entered all the animation names, they type `done` and all the files will be created at the user's desktop, this directory can be changed. 