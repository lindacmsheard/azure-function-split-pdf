# Provision required infrastructure with the Azure Cli

> Note: these steps can be executed locally or from an [Azure cloud shell](https://docs.microsoft.com/en-gb/azure/cloud-shell/quickstart).

Start by defining names in an environment file called `.env`. (This file is gitignored, and so won't be in the repo and needs to be created locally. It can therefore be used to hold sensitive information such as keys and connection strings. See the [.env.sample](../.env.sample) provided in the root of the repo.)

```
LOCATION=uksouth
RG=<resource-group-name>
STORAGE_ACCOUNT=<storageaccountname>
FUNCTION_APP_NAME = <functionappname>

```

Source the file in the shell and verify that the environment variables have been read:
```sh
source .env
echo $RG
```

### Resource Group
Create a resource group
```sh
az group create -n $RG --location $LOCATION
```

Set some basic azure cli defaults, to avoid having to pass these parameters into the following commands. (note: the defaults are persisted within the current folder in a `.azure` directory, so it makes sense to execute this command at the root of the repo.)

```sh
cd <project root>  # do the default configuration at the root of the repo
az config set --local defaults.group=$RG defaults.location=$LOCATION
```


> 👉 TIP: Verify that the `.gitignore` file of the repo lists environmet variable files (`.env*`) and any local azure cli configuration (`.azure`). 

### Storage Account
Create storage account
```sh
az storage account create -n $STORAGE_ACCOUNT --sku Standard_LRS
```

Make the account key available as an environment variable (optional). Note this uses the cli defaults set earlier, meaning we do not need to specify the resource group for example.
```sh
echo -e '\r\nSTORAGE_ACCOUNT_KEY='$(az storage account keys list --account-name $STORAGE_ACCOUNT --query [0].value -o tsv) >> .env
echo -e '\r\nSTORAGE_CONN_STR='$(az storage account show-connection-string --account-name $STORAGE_ACCOUNT -o tsv) >> .env

source .env
```

Create blob storage container within the storage account 
```sh
az storage container create -n documents --account-name $STORAGE_ACCOUNT --account-key $STORAGE_ACCOUNT_KEY

```
### Azure Function App resource

> ℹ️ see also: https://docs.microsoft.com/en-us/azure/azure-functions/scripts/functions-cli-create-serverless


az functionapp create \
  --name $FUNCTION_APP_NAME \
  --storage-account $STORAGE_ACCOUNT \
  --consumption-plan-location $LOCATION \
  --functions-version 2

az functionapp create \
  --name $FUNCTION_APP_NAME \
  --consumption-plan-location $LOCATION \
  --storage-account $STORAGE_ACCOUNT \
  --runtime python \
  --runtime-version 3.8 \
  --functions-version 3 \
  --os-type linux



# Cleanup

delete the resource group to clean up:

```
az group delete <resource group name> --no-wait
```