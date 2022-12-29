import os
import json
from module.sharepoint_api import *

if __name__ == '__main__':
    """
    Setting config
    """
    with open(f"config.json") as f:
        config = json.load(f)

    file_name = config['filename']
    tmp_foldername = config['tmp_foldername'] 
    local_file_directory = f"./{tmp_foldername}/{file_name}"
    print("Save tmp file on:", local_file_directory)

    if not os.path.exists(local_file_directory):
        # downloadfile if not exists
        main_download(config,  local_file_directory)
    else:
        print(f"The file for this path {local_file_directory} has been exists.")
        pass

    print("Done run phone api")






    
