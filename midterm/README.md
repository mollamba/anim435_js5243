# Jacob Stratton Midterm                  
### Last Revision: *October 31st, 2025* 
## "What does it do?"
>**TLDR**: Interface that allows user to import, swap, and unload references from pre-existing files in a directory

Opening and running the script in `Maya` creates an interface with dropdown menus depending on how many unique model asset files you have stored in a preset directory. If you have 3 unique models, 3 dropdowns will appear, and from each dropdown you can select which version to import as reference to the scene. From there, just click the `Load References` button.

## "How does it work?"
>**TLDR**: just read it

### Step 1 )
Lets start from the top.

`Create` or `Locate` a folder for you to dump your assets and their versions in.
>Make sure your naming convention follows: `ASSETNAME.model.VERSION.mb`

**For example:** 

![Here](md.png)

Copy the this folder directory to your clipboard.

### Step 2 )

Open up `Maya`, and open *`midterm.py`* in the script editor. 

```
On line 19, paste your directory to the following variable

modelDir = r"PASTE HERE"

Make sure the last folder on that directory is the name of the folder containing your models
```

### Step 3 )

Now we'll go through each function to understand what they really do.

>`def findModels():` Looks through the `modelDir` and splits each filename into just the first name, and adding it to a set list `modelName`. This list only contains unique names of models, so no matter how many versions of a model you may have in the folder, it will only store 1 of its name. 
For example: `quadball.model.001.mb` will just be stored as *`Quadball`*


>`def getVersions(name):` Returns a list of a parsed model version's full filenames. This function is called inside a nested loop in the `printWindow():` function, so each model from `findModels():` is parsed into `getVersions(name):` as `name` and creates optionItems in the interface for the user to select.

>`def importReferences(*args):` This function is the meat and potatoes of the script, and is broken down into 3 main sections. 

The First section:
```
models = findModels()    #get unique model names as list

    for m in models:
        dropdown = f"{m}_dropdown"
        sel = cmds.optionMenu(dropdown, query=True, value=True)
        nameSpace = m
        refNode = f"{nameSpace}RN"      #initialize new reference node name

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
```
This first chunk deals with getting the model names, and registering if the user selected `None` on the dropdown menu. Finally, it joins the filepath of the given directory with the selected option from the dropdown. 

The Second section:
```
    #swap
    if cmds.objExists(refNode):
        try:
            cmds.file(filePath, loadReference=refNode)
            print(f"Swapped reference for {m} > {sel}")
        except Exception as e:
            print(f"Failed to swap reference for {m}> {e}")
```
This one is pretty self explanatory. If the node exists, swap it via the filepath selected in the dropdown menu. `else` is run in the last section.

The Last section:
```
    #first reference
    #this will always run first before swap or unload
    else:
        try:
            cmds.file(filePath, reference=True, namespace=nameSpace)
            print(f"Created new reference for {m} > {sel}")
        except Exception as e:
            print(f"Failed to create reference for {m}>{e}")
```

This one is also self explanatory. This is the `else` to the second sections `if`, and imports a new reference for the first time. 

### Step 4 )

Run the script in the script editor, select your dropdown options and click `Load References`.

![](tool.png)



-Jake