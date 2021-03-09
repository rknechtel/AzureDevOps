# ###################################################################################
# Script/module: modules\getadogitprojectsconfig.py
# Author: Richard Knechtel
# Date: 03/08/2021
# Description: This is a module of configurations for GetADOGitProjects.py
#
#
# LICENSE:
# This script is in the public domain, free from copyrights or restrictions.
#
# ###################################################################################


# ---------------------------------------------------------[Imports]------------------------------------------------------

_modules = [
            'datetime',
            'os',
            'sys',
            'time',
           ]

for module in _modules:
  try:
    locals()[module] = __import__(module, {}, {}, [])
  except ImportError:
    print("Error importing %s." % module)

# ---------------------------------------------------------[Initialisations]--------------------------------------------------------

# Get environment variables:
global BASEDIR

# Parameters to Script:
global ThisScript

global TempDir
TempDir = "D:\\Temp"

global AdoProject
global UserName
global Pat

global AdoBase
AdoBase = "https://dev.azure.com/MyCompany/"
global AdoRestUrl
AdoRestUrl = "/_apis/git/repositories?api-version=6.1-preview.1"

global RestAPiUrl

global CsvOutput
global CsvItem1
global CsvItem2
global CsvRowItem

global OutputPath
global SaveFile

# Logging:
global LogPath
global LogFile
global LogLevel

# Errors
global HasError
HasError = False
 

# ---------------------------------------------------------[Functions]----------------------------------------------------


# ###################################################################################
# Function: ShowUsage
# Description:  Shows the Usage if no parameters
# Parameters: None
#
def ShowUsage():
  print("[USAGE]: GetADOGitProjects.bat arg1 arg2 arg3")
  print("arg1 = ADO Project Name (Example: MyADOProject)")
  print("arg1 = ADO User Name (Example: MyUserName)")
  print("arg1 = ADO Personal Access Token (PAT) (Example: 1cxcbknj5e2f5z7iserleu6tp3rudjh9hsezp1rk5remeuck3gty)")
  
  return
 
# This is a Function template:
# ###################################################################################
# Function:
# Description:
# Parameters:
#
def MyFuncation(Param1, Param2):
  print("In MyFuncation():")

  try:
    # Do Something
    print("Doing Something")

  except Exception as e:
    print("Exception Information= ", sys.exc_type, sys.exc_value)

  return