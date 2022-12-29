Download file from sharepoint site using Python Requests.

Need to generate Client_id, Client_secret, Tenent_id, Tenent_name. please find the solution on https://www.youtube.com/watch?v=YMliU4vB_YM 


In thai: 

https://narumitkitiweth-67098.medium.com/how-to-transfer-the-files-with-microsoft-sharepoint-via-rest-api-b0f7318d9f86

1. Config parameter as below:
Config example:

{
"client_id"  : "client_id@Tenant_ID",
"client_secret": "client_secret",
"resource"   : "00000003-0000-0ff1-ce00-000000000000/domain.sharepoint.com@Tenant_ID",
"tenant_ID"  : "Tenant_ID",

"sp_team_site"  : "https://domain.sharepoint.com/teams/target_site",
"sp_docpath" : "Shared Documents/General/target_folder",

"tmp_foldername"  : "download", 
"filename"  : "test.csv"

}

2. run app.py
