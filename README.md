# PyCompilePackage
Lightweight Python Pre Compiler and Packager (As a single Package)

A Picture is Worth a Thousand Words

![alt UX](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/DeploymentModels.png)

If you're tired of the below aspects of your Python Deployments, **PyCompilePackage** is the right Tool for you;

#### * You Don't want to share the Original Python Source Code, so that there is no orlittle chance for tampering your source

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

Refer [DemoStandaloneApp](https://github.com/avarghesein/PyCompilePackage/tree/main/DemoStandaloneApp), to get a feel of it !

In a nutshell, for every new Python Project you have to do the below;

##### 1. Unzip the latest [PyCompilePackage Release](https://github.com/avarghesein/PyCompilePackage/releases/download/Version1/BUILD.zip) to your Source folder (Under BUILD Directory)

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/BuildTemplateFolder.png)

##### 2. Update Your Package Name in "BuildConfig.json" and "RunApp.sh or RunApp.BAT"

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/UpdatePackageName.png)

##### 3. Build/Package your Source using command "\BUILD\BuildPackage.BAT or sh"

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/BuildPackage.png)

##### 4. Run the built package using command "\DIST\RunApp.BAT or sh"

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/RunPackage.png)

##### 5. Copy "\DIST" folder contents to your Target/Deployment directory/machines and use "RunApp.BAT or sh" to run the package

![](https://github.com/avarghesein/PyCompilePackage/blob/main/Docs/DeployPackage.png)


