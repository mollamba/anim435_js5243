\\## How to use importSave.py ##

Written by Jake Stratton - 10/17/2025

Updated by Jake Stratton - 10/22/2025

Usage : This script is to be run in Gitbash or Terminal. The user inputs a list of names for animations, and it spits out .ma files with your name, project name, and animation name as the filename
[ENVIRONMENT VARIABLES]
export NAME= ~your name here~
export PNAME= ~project name here~


How it works :

You open your terminal and setup 2 ENVIRONMENT VARIABLES named NAME and PNAME. 
then run assignment4.py, or whatever name you would use if its hooked up to an alias. 

The program will ask you for a list of names of animations you are going to make, for example
run
walk
idle
atk1
atk2
atk3
done {finishes the program}

Enter "done" when you are finished entering animation names.

The program will spit out files named: {NAME}_{PNAME}_{animName}.ma onto your desktop.