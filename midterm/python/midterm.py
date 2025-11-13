'''
Jacob Stratton Midterm
Import Reference Version Script

This script can import, swap, and unload references
via dropdown options.

It automatically loads files from the 'mb' folder in a given directory.
You should set the directory yourself, and then just shovel
files in there when you need to. 

'''

import maya.cmds as cmds
import os
from functools import partial

#dir of model versions
modelDir = r"E:\anim435\repo\anim435_js5243\anim-435-2025-js5243\midterm\mb"

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def findModels():
    '''
    find and return the unique model names from modelDir
    '''
    
    models = set()
    for files in os.listdir(modelDir):
        modelName = files.split(".model.")[0]
        models.add(modelName)
            
    return sorted(models)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def getVersions(name):
    '''
    return the full filenames for each unique model
    '''
    ver = []
    for files in os.listdir(modelDir):
        if files.startswith(name + ".model"):
            ver.append(files)
        
    ver.sort()
    return ver
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def importReferences(*args):
    """
    func for importing swapping and unloading depending on dropdown option
    """
    models = findModels()
    
    for m in models:
        dropdown = f"{m}_dropdown"
        sel = cmds.optionMenu(dropdown, query=True, value=True)
        nameSpace = m
        refNode = f"{nameSpace}RN"
        
        #none - unload from scene
        if sel == "None":
            if cmds.objExists(refNode):
                try:
                    cmds.file(unloadReference=refNode)
                    print(f"Unloaded reference for {m}")
                except Exception as e:
                    print(f"Failed to unload reference for {m}>{e}")
            continue

        #path to correct version
        filePath = os.path.join(modelDir, sel).replace("\\", "/")

        #swap
        if cmds.objExists(refNode):
            try:
                cmds.file(filePath, loadReference=refNode)
                print(f"Swapped reference for {m} > {sel}")
            except Exception as e:
                print(f"Failed to swap reference for {m}> {e}")

        #first reference
        #this will always run first before swap or unload
        else:
            try:
                cmds.file(filePath, reference=True, namespace=nameSpace)
                print(f"Created new reference for {m} > {sel}")
            except Exception as e:
                print(f"Failed to create reference for {m}>{e}")


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def printWindow():
    """
    prints the main window
    handles dropdown logic from gotVersions() and findModels()
    """
    winName = "ImportReferencesWin"
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
        
    cmds.window(winName, title="Model Reference Importer", widthHeight=(500, 250))
    colLayout = cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    myText = cmds.text(label="Select Model Versions to Reference")
    cmds.separator(height=10)

    models = findModels()

    for m in models:
        
        cmds.text(label=m.capitalize())
        optMenu = cmds.optionMenu(f"{m}_dropdown", width=250)
        #{m}_dropdown so each optionMenu item is unique
        cmds.menuItem(label="None")

        for fileName in getVersions(m):
            cmds.menuItem(label=fileName)

        cmds.separator(height=5)

    
    cmds.button(label="Load References", height=40, command = partial(importReferences))
    
    cmds.showWindow(winName)
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

printWindow()