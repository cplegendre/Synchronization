# ======================================================================================================================
# Title:  Synchronize two folders
# Author: Cédric Legendre
# Date:   05 Mar 2024
# ======================================================================================================================
import os, shutil
import time
import hashlib
import logging
from glob import glob


######### Logging

LocalTime = time.localtime()

# Set up log file
logfile = "logfile.txt"
if os.path.exists(logfile) and KeepLogFile == 0:
    os.remove(logfile)
logging.basicConfig(
    filename=logfile,
    level=logging.INFO,
    format="%(asctime)s|--> %(name)s| %(levelname)s| %(message)s",
)



######### Variables & paths

# Overwrite the logfile?
KeepLogFile = 0

# Set up paths and files
# InputDir = '/path/to/dir/'
# OutputDir = '/path/to/dir/'

InputDir = './Source/'
OutputDir = './Replica/'

# Synchronization interval:
SyncInterval = 600  # 600s / 10 minutes.
TimeInterval = 10   # Update every 10 seconds.


# Main code
def Backup():
    # Check that both directories exist
    if not os.path.isdir(InputDir):
        print("No source directory")
        logging.info("No source directory")

    else:
        print(f"Source directory {InputDir}")
        logging.info(f"Source directory {InputDir}")
        
    if not os.path.isdir(OutputDir):
        print(f"Creating replica directory {OutputDir}")
        logging.info(f"Creating replica directory {OutputDir}")
        os.makedirs(OutputDir, exist_ok=True)

    else:
        print(f"Replica directory exist: {OutputDir}")
        logging.info(f"Replica directory exist: {OutputDir}")


    # Check the folders in the Source directory
    # For this script, the indentation level was set to one, but can be easily increased.
    # At each level, copy the files from the source to the destination.

    FirstLayerFolders = []
    NbFiles = 0
    layer = 1
    w = os.walk(InputDir)
    for (dirpath, dirnames, filenames) in w:
        if layer == 1:
            FirstLayerFolders.extend(dirnames)
            print(f"Number of subdirectories: {len(FirstLayerFolders)}")
            logging.info(f"Number of subdirectories: {len(FirstLayerFolders)}")

    # Copy files
            for f in filenames:
                FileSource = InputDir+f
                FileDest = OutputDir+f
                NbFiles = NbFiles + len(filenames)
                if glob(FileSource) and glob(FileDest):
                    hash1 = hashlib.md5(open(FileSource,'rb').read()).hexdigest()
                    hash2 = hashlib.md5(open(FileDest,'rb').read()).hexdigest()
                    if hash1 == hash2:
                        continue
                    else:
                        print(f"File {FileSource} modified")
                        logging.info(f"File {FileSource} modified")
                        try:
                            shutil.copy(FileSource,FileDest)
                        except:
                            print(f"Error writing {f}")
                            logging.info(f"Error writing {f}")
                            pass
            


            
           
            for numb in range(0,len(FirstLayerFolders)):
                FirstLayerFoldersTarget = f"{FirstLayerFolders[int(numb)]}"
                FirstLayerFoldersTargetSrc = f"{InputDir}{FirstLayerFolders[int(numb)]}/"
                FirstLayerFoldersTargetDir = f"{OutputDir}{FirstLayerFolders[int(numb)]}/"
                os.makedirs(FirstLayerFoldersTargetDir, exist_ok=True)

                WalkingFiles = os.walk(FirstLayerFoldersTargetSrc)
                for (dirpath, dirnames, filenames) in WalkingFiles:
                    NbFiles = NbFiles + len(filenames)
                    for f in filenames:
                        FileSource = FirstLayerFoldersTargetSrc+f
                        FileDest = FirstLayerFoldersTargetDir+f
                        try:
                            shutil.copy(FileSource,FileDest)
                        except:
                            print(f"Error writing {f}")
                            logging.info(f"Error writing {f}")
                            pass

        layer += 1




# Check that deleted files from sources are also deleted from replica.
    w2 = os.walk(OutputDir)
    for (dirpath, dirnames, filenames) in w2:
            for f in filenames:
                FileSource = InputDir+f
                FileDest = OutputDir+f
                if not glob(FileSource) and glob(FileDest):
                    os.remove(FileDest) 
                    print(f"Deleting {FileDest}")
                    logging.info(f"Deleting {FileDest}")
                    

    print(f"Number of files: {NbFiles}")
    logging.info(f"Number of files: {NbFiles}")



print(f"###################")
print(f"# Team_tesk_task! #")
print(f"###################")
logging.info(f"###################")
logging.info(f"# Team_tesk_task! #")
logging.info(f"###################")


while 0<1:
# Check when was the folder synchronized for the last time
    StartTime = time.time()
    if not os.path.isdir(OutputDir):
        print(f"No backup found, initial backup")
        logging.info(f"No backup found, initial backup")
        Backup()
        EndTime = time.time()
        time.sleep(TimeInterval) 


    

    if os.path.isdir(OutputDir):
        LatestBackup = int(time.time() - os.path.getatime(OutputDir))
        if LatestBackup < SyncInterval:
            print(f"Backup is recent!")
            logging.info(f"Backup is recent!")
            EndTime = time.time()
            time.sleep(TimeInterval) 
        else:
            print(f"Backup is older than {SyncInterval}s!")
            logging.info(f"Backup is older than {SyncInterval}s!")
            Backup()
            EndTime = time.time()
            time.sleep(TimeInterval) 

    

    print(f"###################")
    print(f"#   Completed!   #")
    print(f"###################")
    print("Finished in")
    print(EndTime-StartTime)
    print("seconds")
    logging.info(f"###################")
    logging.info(f"#   Completed!   #")
    logging.info(f"###################")
    logging.info("Finished in")
    logging.info(EndTime-StartTime)
    logging.info("seconds")

