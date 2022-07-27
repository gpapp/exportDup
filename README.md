# exportDup
Exporting dup files from https://enterprise-architecture.org/dupcentral.php into various formats


# Purpose
https://enterprise-architecture.org/ provides great resources that can be used as reference when building capability models. They are however in the Essential repository import format, that requires access to an Essential repository. While it is possible to set up such a repo for yourself, it is quite time consuming, especially if you are only interested in the higher level models.

# Pre-requisites
* Python installed and set up, so it can run from the command line.
** Windows users can download a version from the Microsoft Store
** Linux users already have it installed
** iOS users will likely have an older version of Pyton installed, but it should work anyway
* Text editor

# How to use
## Creating exports

1. Download the model you wish to use from https://enterprise-architecture.org/dupcentral.php it is a ZIP file named dup. You will be able to use standard zip extractor after renaming it
1. Extract the dup_import_script.py from the model to a directory of your choice
1. Place the standard_funcions.py from this repository in the directory
1. Replace the imports in the dup_import_script.py with
```
import standardFunctions
from standardFunctions import defineExternalRepository
from standardFunctions import EssentialGetInstance
from standardFunctions import addIfNotThere
from standardFunctions import kb
from standardFunctions import Integer
from standardFunctions import dump_Archi
from standardFunctions import dump_Lucid
```
5. Add the following lines to the end of the file, where __MODELNAME__ is the name of the model. This will be prefix for the export files 
```
dump_Lucid('MODELNAME')
dump_Archi('MODELNAME')
```
6.Navigate to the directory in the command line of your OS
7. Execute the following command and hope for the best!
```
python standard_funcions.py
```
8. The script will create the files `MODELNAMEelements.csv`, `MODELNAMErelations.csv`, `MODELNAMEproperties.csv` to be used in Archi, and , `MODELNAMELucid.csv` for Lucid or other use

## Importing to Archi
1. Create an empty model in Archi
2. Use the menu File->Import->CSV data into selected model... 
3. Select any of the generated `MODELNAMEelements.csv`, `MODELNAMErelations.csv`, `MODELNAMEproperties.csv`
4. Import should generate the corresponding items
There will be no view created during the import, you'd have to do all manually.

## Importing to Lucidcharts as a smartchart
__You will need enterprise licence of Lucid to use this!__

1. Open a Lucidchart canvas
2. From Containers menu on the side create a Smart Container using Import Data
3. Select the first row as header, and the ID column as identifier for the data
3. When selecting fields use 
    * L1 Name for Containers
    * L2 Name for Shape Title
    to create L2 chart, or 
    * L2 Name for Containers
    * L3 Name for Shape title
    Ignore the warning for Blank values
    __It may take long time for Lucid to create the model!__
4. After the data is dumped into the sheet, select the container open the properties on the right side and use "Add New Filter" on the Data sheet
    * For __Item__
    * Show if __Levelis equal to 2__ for L2 or __3__ for L3 chart 
