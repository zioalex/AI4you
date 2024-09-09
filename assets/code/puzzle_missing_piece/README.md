# Setup

python -mvenv .venv 
. .venv/bin/activate
pip install requirements.txt 
pip install -r requirements.txt 

# Usage
. .secrets
(.venv) python main.py 

# Tests
https://replicate.com/p/x0bxz0rc0srgj0cfnwb8r0gmk4


# RUNPOD
https://blog.runpod.io/visual-studio-code-vs-code-remote/

- connect remotely via remote tunnet. Remote Hosts doesn't work. -T option in SSH client call.


## Copy to runpod
Install azcli rsync sudo 

curl -sL https://packages.microsoft.com/keys/microsoft.asc |   gpg --dearmor |   tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null
AZ_REPO=$(lsb_release -cs)
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" |   tee /etc/apt/sources.list.d/azure-cli.list
apt update
apt-get install azure-cli sudo rsync
## AZCopy download
https://aka.ms/downloadazcopy-v10-linux

az login --use-device-code
az account set --subscription f5bc5a63-92f8-4ab6-ad94-84673eeebb56
az ad sp create-for-rbac --name ml-sa-experiment-sp --sdk-auth

{
  "clientId": "aee23cbe-8fd0-4214-b81d-be5e25f9f8cd",
  "clientSecret": "DUMMY_CLIENT_SECRET",
  "subscriptionId": "f5bc5a63-92f8-4ab6-ad94-84673eeebb56",
  "tenantId": "88d74ba7-d9b6-40fc-abea-8f80aa5cedf1",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}

export AZURE_CLIENT_ID=DUMMY_CLIENT_ID
export AZURE_CLIENT_SECRET=DUMMY_CLIENT_SECRET
export AZURE_TENANT_ID=88d74ba7-d9b6-40fc-abea-8f80aa5cedf1
export AZURE_SUBSCRIPTION_ID=f5bc5a63-92f8-4ab6-ad94-84673eeebb56

export AZCOPY_SPA_CLIENT_SECRET=$AZURE_CLIENT_SECRET
azcopy login --service-principal --application-id $AZURE_CLIENT_ID --tenant-id $AZURE_TENANT_ID # Doesn't work

cd ; curl -L  https://aka.ms/downloadazcopy-v10-linux |tar zxvf -; mv azcopy_linux_amd64_10.25.1/azcopy /usr/local/bin/
# Using SAS token

# sync puzzle_missin_piece
azcopy sync puzzle_missing_piece/ "https://aimlexperiment.blob.core.windows.net/runpod/puzzle_missing_piece/?sp=racwdl&st=2024-07-20T21:06:38Z&se=2024-12-31T06:06:38Z&spr=https&sv=2022-11-02&sr=c&sig=jIfZfEPUZUwyhHqsPPnBAL6cFtt08uET0B1Z2J7cqwo%3D" --recursive=true

azcopy sync /workspace/ "https://aimlexperiment.blob.core.windows.net/runpod/workspace/?sp=racwdl&st=2024-07-20T21:06:38Z&se=2024-12-31T06:06:38Z&spr=https&sv=2022-11-02&sr=c&sig=jIfZfEPUZUwyhHqsPPnBAL6cFtt08uET0B1Z2J7cqwo%3D" --recursive=true

PIP in the virtual environment
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
az storage account copy
rsync -avz puzzle_missing_piece root@149.86.66.214 -p 34474

rsync -avz -e "/usr/bin/ssh -p 34474" puzzle_missing_piece root@149.86.66.214:/root
