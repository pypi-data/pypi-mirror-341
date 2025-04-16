# Project Name - ReadMe

This file contains user's information on how to navigate the project's structure.

Each directory included in this repository provides a README.md file with detailed
information about the purpose and scope of the directory.

Some directory are empty and are supposed to remain as such. For instance, the *data*
and *models* directories exist but no content except for the README.md file will be
taken into account by Git. 
This is to enforce the standard of not versioning any dataset or binary file.

## Directories 

Below a quick description of the directory in this structure:
- **config** contains configuration files and dependency files (e.g. Conda)
- **data** it is supposed to contain datasets for input and output, but without versioning them in Git
- **docs** contains the Technical Report and the Operational Manual for the project
- **models** it is supposed to contained trained models as binary files, but without versioning them into Git
- **notebooks** contains all the Jypiter Notebooks used during development and perhaps containing useful snippets of code and rendering of insightful charts
- **src** contains a directory structure to organize the source code of the project

## Scripts

At the top level of this repository, there are 3 main scripts which represent the 
entry points for the overall project:
- **setup.sh** contains all the necessary code which is needed to install the software solution the first time. This include the possibility of creations of Virtual Environments or the building or container's images, etc...
- **train.sh** contains the necessary code to run the project and train a Machine Learning algorithm on data. The code to be run will be available under a specific path in the *src* directory and the data to be used will be available in the *data* directory, persisting the model in the *models* directory as suggested by the structure above. Some projects might not involve a ML algorithm and therefore no training will be required: in such case this direcrtory will be empty and only the scoring will be necessary.
- **score.sh** contains the necessary code to run the project and score newly available data using a previously trained model. The code to be run will be available under a specific path in the *src* directory, the data to score will be available in the *data* directory and the model, if necessary, will be stored in the *models* directory. 

The scripts described above are listed as *Shell/Bash* script to be executed in a Linux environment. However, in the presence of a Windows environment the same scripts will be available under a different file extension (.bat) for *Windows Batch* files.

## Scripts blueprints

In the **docs > Scripts_blueprints** folder you can find the blueprints to follow for both **R** and **Python** scripts, respectively. 
For both there are summary text documents **Summary.md** which you should read to know what it takes for you to be compliant with the **Code Quality** standards defined by the dedicated DX working stream. 
If you use **VS Code** as you IDE you can install those standards (guideline in the **Summary.md** files) and have VS Code enforce them on your scripts automatically. Should you be using for R or Python different IDE, it is your responsibility to comply with those standards. 
Not complying to those Code Quality standards results in risking that your code will not be committed to **GitHub**, as GitHub will be requiring those standards to be followed upon commit.