# PyCompilePackage
Lightweight Python Pre Compiler and Packager (As a single Package)

A Picture is Worth a Thousand Words

![alt UX](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/DeploymentModels.png)

If you're tired of the below aspects of your Python Deployments, **PyCompilePackage** is the right Tool for you;

#### * You Don't want to share the Original Python Source Code, so that there is no or little chance for tampering your source

#### * You would like to Pre compile your Python Source for better performance gains, before deployment

#### * You want your Python Depolyments clean, and would like to package all your source in a single package

# How PyCompilePackage, Works

PyCompilePackge, Helps to make your Python Build/Deployments clean and compact by;

#### 1. Pre-Compile all your python sources to Byte Codes

#### 2. Package those Compiled Files in a Single PYZ Container file, with any associated resources

#### 3. Deployment is as simple as, Copy this single PYZ file to Target Machines and run

This has the below advantages over the traditional python deployments;

##### * Original Python Source code is not shared, hence less chance for tampering

##### * Enjoy performance boosts, due to pre compiled source and faster startup time

##### * Easy and fast (re)deployments, as you don't have to deal with lot of files/folder hierarchies 

##### * Chances for Individual file corruption post deployment is less, Since all files have packaged as a single PYZ file

# How To Use PyCompilePackage

Refer [DemoStandaloneApp](https://github.com/avarghesein/PyCompilePackage/tree/main/DemoStandaloneApp)

In a nutshell, for every new Python Project you have to do the below;

##### 1. Unzip the latest [PyCompilePackage Release](https://github.com/avarghesein/PyCompilePackage/releases/download/Version7/BUILD.zip) to your Source folder (Under BUILD Directory)

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/BuildTemplateFolder.png)

##### 2. Update Your Package Name in "BuildConfig.json" and "RunApp.sh or RunApp.BAT"

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/UpdatePackageName.png)

##### 3. Build/Package your Source using command "\BUILD\BuildPackage.BAT or sh"

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/BuildPackage.png)

##### 4. Run the built package using command "\DIST\OUTPUT\RunApp.BAT or sh"

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/RunPackage.png)

##### 5. Copy "\DIST\OUTPUT" folder contents to your Target/Deployment directory/machines and use "RunApp.BAT or sh" to run the package

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/DeployPackage.png)

# PyCompilePackage, Advanced Options Explained

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/AdvancedOptions.png)

**Embedding External Dependencies**: 
If you include **requirements.txt** file as an **Internal Resource**, The Builder will copy all mentioned dependencies in the
'requirements.txt' file to the final standalone APP file. Though this build process may take a while, 
the Standalone App is now selfcontained, and does not require the dependencies available on the target machines !

e.g.

      "INTERNAL_RESOURCES": [
              ["BUILD/requirements.txt",""],

The below settings will control the pre-compilation of external dependencies. 

      "PRE_COMPILE_REQUIREMENTS" : "NO",
 
"NO" will copy the external packages as is to the final APP file.
"YES" will compile the external packages before copying to the final APP file.


      "EXTRACT_REQUIREMENTS" : "NO",
 
This setting is specific for **Libraries having C/C++ extensions** such as Numpy.
Such Libraries needs to be extracted on target machines before running the APP. (They wont run properly from the ZipApp package)

A "NO" will not extract the external packages to the target machines, instead it will try to load from the APP file itself.

"YES" will first extract the external packages before loading the dependencies.
Required for external libraries having C/C++ extensions.

# Build PyCompilePackage Itself !

**PyCompilePackage** itself built using the same **PyCompilePackage** Build methodology.

Use command **"\BUILD\BuildPackage.BAT or sh"**, and find the Built Package (**PyCompilePackager.pyz**) in "DIST/OUTPUT" folder. 

Or you could directly run **Main.py**, from VSCode to achieve the same result. 

Copy the Contents of the above "DIST/OUTPUT" folder, to "BUILD" folders of target python projects
(for **PyCompilePackage**, these are its Deployment Folders),
Which you want to package using **PyCompilePackage** Build methodology.
