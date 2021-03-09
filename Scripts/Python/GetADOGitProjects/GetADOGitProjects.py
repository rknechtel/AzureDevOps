# ************************************************************************
# Script: GetADOGitProjects.py
# Author: Richard Knechtel
# Date: Create Date 03/08/2021
# Description: This script will allow you to get all the git projects
#              in an Azure DevOps Project,
#
# Note: Must install Python libs: 
#       pip install urllib3 
# 
# LICENSE: 
# This script is in the public domain, free from copyrights or restrictions.
#
#
# EXIT STATUS:
#     Exit codes:
#     0 = Success
#     1 = Error
#
# EXAMPLES:
#   Args format from a DOS Batch file (using either python):
#   call python Drive:\Path\GetADOGitProjects.py MyADOProject MyUserName 1cxcbknj5e2f5z7iserleu6tp3rudjh9hsezp1rk5remeuck3gty
#
#   Args format from a Shell Script (using either python):
#   python /Path/GetADOGitProjects.py MyADOProject MyUserName 1cxcbknj5e2f5z7iserleu6tp3rudjh9hsezp1rk5remeuck3gty
#
#************************************************************************

#---------------------------------------------------------[Imports]------------------------------------------------------

_modules = [
            'argparse',
             'csv',
            'datetime',
            'errno',
            'io',
            'json',
            'logging',
            'os',
            'requests',
            'shutil',
            'sys',
            'time',
            'traceback',
            'urllib3',
           ]

for module in _modules:
  try:
    locals()[module] = __import__(module, {}, {}, [])
  except ImportError:
    print("Error importing %s." % module)

	
# Custom Modules:
from modules import getadogitprojectsconfig as config
from modules import genericfunctions as genfunc

#---------------------------------------------------------[Script Parameters]------------------------------------------------------
print("")
print("Passed Arguments:")
print(sys.argv)
print("")

# Set our Variables:
config.ThisScript = sys.argv[0]
config.AdoProject = sys.argv[1]

#---------------------------------------------------------[Initialisations]--------------------------------------------------------

Username = os.environ["USERNAME"]

# Logger
global GetADOGitProjectsLogger

# This is the JSON data (dictionary) returned from Azure Devops Rest API
global JsonData

# For Info and up logging
config.LogLevel = logging.INFO
# For Debug and up Logging:
#config.LogLevel = logging.DEBUG

# Output Path for Files
config.OutputPath = config.TempDir + "\\ADOFiles"
config.SaveFile = config.AdoProject + "-Repos.csv"

#----------------------------------------------------------[Declarations]----------------------------------------------------------

#Script Version
ScriptVersion = '1.0'

#---------------------------------------------------------[Functions]--------------------------------------------------------

# ###################################################################################
# Function: InitScriptLogging
# Description:  Initialize the Scripts logging
# Parameters: None
#
def InitScriptLogging():
  # Initialize the default logging system:
  config.LogPath = config.TempDir + "\\Log"
  config.LogFile = "GetADOGitProjects.log" 
  #print("Log File Name = " + os.path.join(config.LogPath, config.LogFile))
  
  # Check if Log directory exists, if it doens't create it
  DirExists = os.path.isdir(config.LogPath)
  if DirExists==False:
    try:
      os.mkdir(config.LogPath)
    except OSError:
      print("Creation of the directory %s failed" % config.LogPath)
    else:
      print("Successfully created the directory %s" % config.LogPath) 
  
  # For Debug and up Logging:
  #ScriptLogger = genfunc.CreateLogger(__name__, os.path.join(LogPath, LogFile),logging.DEBUG)
  # For Info and up logging
  GetADOGitProjectsLogger = genfunc.CreateLogger(__name__, os.path.join(config.LogPath, config.LogFile),logging.INFO)

  return GetADOGitProjectsLogger
  
# ###################################################################################
# Function: ProcessParams
# Description:  This will process any parameters to the Script
# Parameters: Param1      - Does
#             Param2         - Does
#
def ProcessParams(argv):
  # Set our Variables:

  # Check the total number of args passed - make sure we get 5 (4 + the script name that is passed by default).
  if(len(sys.argv) == 4):
    genfunc.ShowParams()
    config.ThisScript = sys.argv[0]
    config.AdoProject = sys.argv[1]
    config.UserName = sys.argv[2]
    config.Pat = sys.argv[3]

    # Verify we got values for parameters:
    if config.AdoProject is None:
      GetADOGitProjectsLogger.error("Paramater Azure DevOps Project is empty.")
      config.HasError = True
    else:
      config.HasError = False

    if config.UserName is None:
      GetADOGitProjectsLogger.error("Paramater Azure DevOps Username is empty.")
      config.HasError = True
    else:
      config.HasError = False

    if config.Pat is None:
      GetADOGitProjectsLogger.error("Paramater Azure DevOps Personal Access Token (PAT) is empty.")
      config.HasError = True
    else:
      config.HasError = False

    if config.HasError==True:
      config.ShowUsage()
      sys.exit(1)

  else:
    config.ShowUsage()
    sys.exit(1)

  return

####################################################################################
# Function: GetJSONFromURL
# Description: Will get JSON data from a URL 
# Parameters: JSON URL
# Example Call:
# GetJSONFromURL(URL)
#
def GetJSONFromURL(pUrl):
  JsonResponse = ''
  try:
    # Using urllib3:
    # conretry = urllib3.util.Retry(total=10, read=10, connect=10, backoff_factor=1)
    # Retry Params:
    # Number of Retries
    # How many times to retry on read errors
    # How many connection-related errors to retry on
    # A backoff factor to apply between attempts after the second try (how long to sleep)
    # Ref: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html
    # contimeout = urllib3.util.Timeout(connect=2.0, read=4.0)
    # Timeout Params:
    # The maximum amount of time (in seconds) to wait for a connection attempt to a server to succeed.
    # The maximum amount of time (in seconds) to wait between consecutive read operations for a response from the server. 
    # Ref: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html
    # Http = urllib3.PoolManager(retry=conretry, timeout=contimeout, maxsize=1)
    Http = urllib3.PoolManager()

    # Add Basic Auth for Auzre DevOps REST API Authentication
    basicauth = config.UserName + ':' + config.Pat
    baheaders = urllib3.make_headers(basic_auth=basicauth)

    JsonResponse = Http.request('GET', pUrl, headers=baheaders, retries=30)
    GetADOGitProjectsLogger.info("GetJSONFromURL - JsonResponse = " + str(JsonResponse.data.decode('utf-8-sig')))
    config.HasError = False

  except urllib3.exceptions.NewConnectionError as nce:
    config.HasError = True
    GetADOGitProjectsLogger.error("GetJSONFromURL Connection Error (Connection Refused or Get Address Information Error) - Exception Information = " + traceback.format_exc())
  except urllib3.exceptions.MaxRetryError as mre:
    config.HasError = True
    GetADOGitProjectsLogger.error("GetJSONFromURL Max Retries hit - Exception Information = " + traceback.format_exc())
  except Exception as e:
    config.HasError = True
    GetADOGitProjectsLogger.error("GetJSONFromURL - Exception Information = " + traceback.format_exc())

  return JsonResponse

#-----------------------------------------------------------[Execution]------------------------------------------------------------

# ************************************
# Main Script Execution
# ************************************

# Will only run if this file is called as primary file 
if __name__ == '__main__':
  
  # Intialize variables:
  JsonResponse = ""

	# Initialize Logging:
  GetADOGitProjectsLogger = InitScriptLogging()

  # Proccess Parameters
  ProcessParams(sys.argv)

  GetADOGitProjectsLogger.info("Starting  GetADOGitProjects script at " + genfunc.GetCurrentDateTime() + ".")
  # Show parameters - mask PAT
  GetADOGitProjectsLogger.info("Parameters = " + str(sys.argv[0]) + " " + str(sys.argv[1]) + " " + str(sys.argv[2]) + " **********")
  
  try:

    # Call Azure DevOps Rest API
    print("Call ADo REST API to get list of Git Repos in Project " + config.AdoProject)
    config.RestAPiUrl = config.AdoBase + config.AdoProject + config.AdoRestUrl
    GetADOGitProjectsLogger.info("RestAPiUrl = " + config.RestAPiUrl)

    try:
      GetJSONFromURL(config.RestAPiUrl)
      JsonResponse = GetJSONFromURL(config.RestAPiUrl)
      JsonData = json.loads(JsonResponse.data.decode('utf-8-sig'))

    except Exception as e:
      GetADOGitProjectsLogger.error("GET URL Execution failed.")
      GetADOGitProjectsLogger.error("Exception Information = " + traceback.format_exc())
      config.HasError = True

    try:

      if not config.HasError:
        # Get JSON Data
        Data = json.dumps(JsonData)
        GetADOGitProjectsLogger.info("Data = " + Data)
        
        # Check if OUptut directory exists, if it doens't create it
        DirExists = os.path.isdir(config.OutputPath)
        if DirExists==False:
          try:
            os.mkdir(config.OutputPath)
          except OSError:
            GetADOGitProjectsLogger.error("Creation of the directory %s failed" % config.OutputPath)
          else:
            GetADOGitProjectsLogger.error("Successfully created the directory %s" % config.OutputPath) 

        # Setup CSV File Writer  
        outputcsvfile = config.OutputPath + "\\" + config.SaveFile
        GetADOGitProjectsLogger.info("outputcsvfile = " + outputcsvfile)

        GetADOGitProjectsLogger.info("Opening " + outputcsvfile)
        config.CsvOutput = open(outputcsvfile,'w', newline='')
        GetADOGitProjectsLogger.info("Creating csvwriter")
        csvwriter = csv.writer(config.CsvOutput)

        # Write Header Row
        GetADOGitProjectsLogger.info("Writing Header Row")
        csvfields = ['RepoUrl', 'ProjectName']
        #csvwriter.writerow("RepoUrl,ProjectName")
        csvwriter.writerow(csvfields)

        # Loop over "values" Array and crating CSV file
        GetADOGitProjectsLogger.info("Pasrsng JSON")   

        for key,value in JsonData.items():
          for item in value:
            subitems = item.items()
            for key,value in subitems:
              # Need to get 'name' and 'webUrl'
              if key == 'name':
                GetADOGitProjectsLogger.info("key = " + str(key))
                GetADOGitProjectsLogger.info("value = " + str(value))  
                config.CsvItem1 = str(value)
              if key == 'webUrl':
                GetADOGitProjectsLogger.info("key = " + str(key))
                GetADOGitProjectsLogger.info("value = " + str(value))
                config.CsvItem2 = str(value)
                
                # Write Row to CSV file then clear variables for next item
                config.CsvRowItem = [config.CsvItem1, config.CsvItem2]
                csvwriter.writerow(config.CsvRowItem)
                config.CsvItem1 = ""
                config.CsvItem2 = ""
                config.CsvRowItem = ""

 
    except TypeError as te:
      # Note: End of JSON will have an entry like: "count": 64
      #       Need to figure out how to skip it.
      GetADOGitProjectsLogger.error("Hit end of JSON")
      # Note: Setting to false so we complete successfully for now
      config.HasError = False

    except Exception as e:
      GetADOGitProjectsLogger.error("Exception =", e)
      config.HasError = True

    finally:
      GetADOGitProjectsLogger.info("Closing CsvOutput")
      config.CsvOutput.flush()
      config.CsvOutput.close()

  except Exception as e:
    GetADOGitProjectsLogger.info(" GetADOGitProjects script Ended at " + genfunc.GetCurrentDateTime() + ".")
    GetADOGitProjectsLogger.error("Execution failed.")
    GetADOGitProjectsLogger.error("Exception Information = " + traceback.format_exc())
    GetADOGitProjectsLogger.error("")
    GetADOGitProjectsLogger.error(" GetADOGitProjects.py completed unsuccessfully at " + genfunc.GetCurrentDateTime() + ".")
    config.HasError = True
    sys.exit(1)

  if not config.HasError:
    # All Went well - exiting!
    End_Time = time.time()
    GetADOGitProjectsLogger.info(" GetADOGitProjects script Ended at " + genfunc.GetCurrentDateTime() + ".")
    GetADOGitProjectsLogger.info("")
    GetADOGitProjectsLogger.info(" GetADOGitProjects.py completed successfully at " + genfunc.GetCurrentDateTime() + ".")
    GetADOGitProjectsLogger.info("")
    GetADOGitProjectsLogger.info("========================================================")
    GetADOGitProjectsLogger.info("")
    config.HasError = False
    sys.exit(0)
