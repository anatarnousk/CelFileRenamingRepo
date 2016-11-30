import csv
import os
import os.path
import requests
from datetime import datetime

# @author: Anastasiya Tarnouskaya
# November 30, 2016
#
# d is the file path with all of your folders that have cel
# files downloaded from NIH. The path that I used was:
# "C:\\Users\\Anastasiya\\Documents\\OVCelData"
#
# Note that you need two backwards slashes because
# '\' is special in python. 

def rename_cel_files_to_case_uuids(d):
    # Time to see how long script takes
    startTime = datetime.now()

    # Note that you need two backwards slashes because '\' is special in python. 
    d = "C:\\Users\\Anastasiya\\Documents\\OVCelData"

    # Obtain all the uuids from the names of downloaded folders 
    dirs = list(filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)]))

    # We just want the last part of the path 
    uuids = ["\\".join(path.split('\\')[-1:]) for path in dirs]

    # Map all the uuids to the case uuids and store them in dictionary
    id_map = {}
    for uuid in uuids:
        r = requests.get('https://gdc-api.nci.nih.gov/v0/legacy/files/{}?expand=metadata_files&fields=associated_entities.case_id'.format(uuid))
        case_id = r.json()['data']['associated_entities'][0]['case_id']
        id_map[uuid] = case_id

    # Let's get started!
    num_file_names_changed = 0
    for subdir in dirs:
        for file in os.listdir(subdir):
            if file.endswith(".CEL"):
                # get the uuid of a particular case 
                uuid = ("\\".join(subdir.split('\\')[-1:]))
                case_uuid = id_map[uuid] + '.CEL'

                #variables for renaming process
                oldPath = os.path.join(subdir, file)
                newPath = os.path.join(subdir, case_uuid)

                #rename the files if need be!
                if oldPath != newPath:
                    os.rename(oldPath, newPath)
                    num_file_names_changed += 1

    time_taken = str(datetime.now() - startTime)
    print('done! ' + str(num_file_names_changed) + ' file names changed in ' + time_taken + ' amount of time!')
