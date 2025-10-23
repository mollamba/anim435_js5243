'''
Batch Import n Save Script 
Jake Stratton

written on October 17th, 2025
v1

This script asks a user to enter their name, project name, and 
'''

import os
import argparse
import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds

parser = argparse.ArgumentParser()
#parser.add_argument('-n', '--name', help="Enter you name, handle, or Company")
#parser.add_argument('-p', '--proj', help="Enter the name of your project or production")
parser.add_argument('-a', '--anim', help="Enter a list of animation names")
args = parser.parse_args()

from functools import partial


def importSave():
    
    animList = []
    anim = ''
    
    
    #get name
    '''
    if not args.name:
        name = input('YOUR NAME: ')
    else:
        name = args.name
        
    #get proj
    if not args.proj:
        proj = input('PROJECT NAME: ')
    else:
        proj = args.proj
    '''
    while (anim !=0):
        
        #get anims
        if not args.anim:
            anim = input('NAME OF ANIMATION: ')
        else:
            anim = args.anim
        
        if (anim.casefold() == 'done'):
            break
        else:
            animList.append(anim)
            
    plugins = ["fbxmaya", "mtoa"]  # add any other needed plugins
    for plugin in plugins:
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            cmds.loadPlugin(plugin)
    
    name = os.getenv("NAME")
    proj = os.getenv("PNAME")
    #import_path = r"E:\P4\js5243_DIGM490_Writer'sBlock\DesignFiles\MayaFiles\rigging\protag\ma\js5243_HumanRig.ma"
    #cmds.file(import_path, i=True)
    
    for animation in animList:
        home = os.path.expanduser("~")
        filename = f"{name}_{proj}_{animation}.ma"
        out_path = os.path.join(home, "Desktop", filename)
        cmds.file(rename=out_path)
        cmds.file(save=True, force= True)
    
    print("Animation Scenes Saved")
    
######################
importSave()
    
    