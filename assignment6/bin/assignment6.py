'''
Batch Import n Save Script 
Jake Stratton


Last Revised on November 20th, 2025     v3

Changlist
v2: Inclusion of environment variables for naming files
v3: export metadata to json file
'''

import os
import argparse
import logging
import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds
from functools import partial

#new imports changelist
import json
from datetime import datetime

# logging 
logger = logging.getLogger(__name__)
FORMAT = "[%(asctime)s][%(filename)s][%(levelname)s] %(message)s"
logging.basicConfig(filename='batch_import_log.txt',
                    level=logging.INFO, 
                    format=FORMAT)

# arg parse
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--anim', help="Enter a list of animation names")
args = parser.parse_args()

# main 
def importSave():
    animList = []
    anim = ''
    
    while True:
        # get anims
        if not args.anim:
            logger.info("File name must start with a letter")
            anim = input('NAME OF ANIMATION (or type "done" to finish): ')
        else:
            anim = args.anim
        
        if anim.lower() == 'done':
            break
        
        # validation: must start with a letter, filenames cant start with anything other than letter right?
        if not anim or not anim[0].isalpha():
            logger.warning(f"Invalid input '{anim}' — must start with a letter.")
            print("X Invalid input. Please start the name with a letter.")
            continue
        else:
            logger.info(f"Valid animation name entered: {anim}")
            animList.append(anim)
        
        # if called with argument, break after first input
        if args.anim:
            break
    

    # load plugins
    plugins = ["fbxmaya", "mtoa"]
    for plugin in plugins:
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            cmds.loadPlugin(plugin)
            logger.info(f"Loaded plugin: {plugin}")
        else:
            logger.info(f"Plugin already loaded: {plugin}")
    
    name = os.getenv("NAME") or "UnknownUser"
    proj = os.getenv("PNAME") or "UntitledProject"
    
    exportMetadata = []
    
    # save animation files
    for animation in animList:
        home = os.path.expanduser("~")
        filename = f"{name}_{proj}_{animation}.ma"
        out_path = os.path.join(home, "Desktop", filename)

        # directory check
        dir_path = os.path.dirname(out_path)
        if not os.path.exists(dir_path):
            logger.error(f"Directory not found: {dir_path}")
            print(f"X Directory not found: {dir_path}")
            continue
        
        try:
            cmds.file(rename=out_path)
            cmds.file(save=True, force=True)
            logger.info(f"Successfully saved: {out_path}")
        except Exception as e:
            logger.error(f"Failed to save {out_path}: {str(e)}")
            print(f"!!! Failed to save {out_path}")
            continue 
    
    #metadata export
        metadata = {
            "expAnimName": animation,
            "expTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #year, month, day, hour:minute:second
            "expPath": out_path,
            "envVar": { #this was annoying to figure out
                "envNAME": os.getenv("NAME"), #this is a good quality user check, to see whoever is using the tool, is actually using it right by making environment variables
                 "envPNAME": os.getenv("PNAME") #if user is not using env variables, it will default to "Unknown user / Unknown project, which is no bueno
                }
            }
        
    #apends export metadata to list
        exportMetadata.append(metadata)
        
        
        #write to json file
        if exportMetadata:
            jsonPath = os.path.join(os.path.expanduser("~"), "Desktop", "a6_metadata.json")

        try:
            with open(jsonPath, "w") as json_file: #writing
                json.dump(exportMetadata, json_file, indent=4) 

            logger.info(f"Metadata exported to {jsonPath}")
            print(f"Metadata exported to: {jsonPath}")

        except Exception as e:
            logger.error(f"Failed to write metadata JSON: {str(e)}")
            print("!!! Failed to write metadata JSON")

    print("Animation Scenes Saved")

#--------------------------------------------------
if __name__ == "__main__":
    importSave()
