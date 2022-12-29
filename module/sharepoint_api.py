import requests

def authen(config):
    """
    Extract config value from config file.
    """
    print(":::loading config:::")
    client_id = config['client_id']
    client_secret = config['client_secret']
    resource = config['resource']
    tenant_ID = config['tenant_ID']

    return client_id, client_secret, resource, tenant_ID

def call_jwt_token(client_id, client_secret, resource, tenant_ID):
    """
    1. get jwt token for sharepoint api.
    """
    url = f"https://accounts.accesscontrol.windows.net/{tenant_ID}/tokens/OAuth/2"

    payload={'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': resource}

    token_response = requests.post(url, data=payload, verify=True)
    token = token_response.json()
    print(":::Received token:::")
    return token['access_token']

def download_files(token, sp_site, src_path, tar_path, file_name):
    """
    2.Download file from sharepoint, using jwt token.
    output = file.csv
    """
    import shutil
    print(f"Try to download file name:{file_name} \nOn directory: {src_path}")
    url = f"{sp_site}/_api/web/GetFolderByServerRelativeUrl('{src_path}')/Files('{file_name}')/$value"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        print(":::Success get files from sharepoint:::")
        # mkdir
        import os
        if not os.path.exists(tar_path):
            # Create folde if not exists
            os.makedirs(tar_path)

        local_savefilename = f"{tar_path}/{file_name}"
        print('local_savefilename:', local_savefilename)

        with requests.get(url, headers=headers, stream=True) as r:
            """
            using stream = download bulk file
            """
            with open(local_savefilename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print('Done download')
        return
    else:
        raise Exception("Sorry, error has occurred, please check filename")

def list_folder(token, sp_site, file_path):
    """
    List folder from sharepoint target directory
    """
    url = f"{sp_site}/_api/web/GetFolderByServerRelativeUrl('{file_path}')/Folders"

    headers = {
    'Content-Type': 'application/json;odata=verbose',
    'Accept': 'application/json;odata=verbose',
    'Authorization': f'Bearer {token}'}

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Sorry, error has occurred")


def list_files(token, sp_site, file_path):
    """
    List file from target directory
    """
    url = f"{sp_site}/_api/web/GetFolderByServerRelativeUrl('{file_path}')/files"

    headers = {
    'Content-Type': 'application/json;odata=verbose',
    'Accept': 'application/json;odata=verbose',
    'Authorization': f'Bearer {token}'}

    response = requests.request("GET", url, headers=headers)
    return response.json()


def main_download(config, local_file_directory):
    """
    Download file using config setting.
    """
    # read config
    sp_site = config['sp_team_site'] # https://domain.sharepoint.com/teams/target_site
    sp_docpath = config['sp_docpath'] # Shared Documents/General/target_folder

    # call jwt token
    client_id, client_secret, resource, tenant_ID = authen(config)
    token = call_jwt_token(client_id, client_secret, resource, tenant_ID)

    # download file
    src_path = f"{sp_docpath}"
    sp = local_file_directory.split('/') #[dir], [filename]
    tar_path = sp[:-1] # withoit filename
    tar_path = '/'.join(tar_path)

    file_name = sp[-1] # extract filename
    print("src_path:", src_path)
    print("tar_path:", tar_path)
    print("file_name:", file_name)
    download_files(token, sp_site, src_path, tar_path, file_name)
