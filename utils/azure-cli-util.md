## Create Instructions

1. **Login to Azure (if not already done)**
   ```bash
   az login
   ```

2. **Get your Azure Tenant ID**
   ```bash
   az account show --query tenantId -o tsv
   ```
   Save this as your `AZURE_TENANT_ID`.

3. **Create a Service Principal**
   ```bash
   az ad sp create-for-rbac --name "PolarisServicePrincipal" --role "Storage Blob Data Contributor" --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/$YOUR_RESOURCE_GROUP/providers/Microsoft.Storage/storageAccounts/$YOUR_STORAGE_ACCOUNT_NAME
   ```
   Replace:
   - `YOUR_RESOURCE_GROUP`: The resource group containing your storage account
   - `YOUR_STORAGE_ACCOUNT_NAME`: Your storage account name

4. **Output & Environment Variables**
   The command above will output JSON similar to:
   ```json
   {
     "appId": "00000000-0000-0000-0000-000000000000",
     "displayName": "PolarisServicePrincipal",
     "password": "YOUR-GENERATED-PASSWORD",
     "tenant": "00000000-0000-0000-0000-000000000000"
   }
   ```

   Map these values to your environment variables:
   - `AZURE_CLIENT_ID` = the `appId` value
   - `AZURE_CLIENT_SECRET` = the `password` value
   - `AZURE_TENANT_ID` = the `tenant` value

5. **Verify Permissions** (optional)
   ```bash
   az role assignment list --assignee [AZURE_CLIENT_ID]
   ```


## Cleanup Instructions

1. **Find Your Service Principal ID**

   If you don't remember your service principal's ID (the client ID/appId), you can find it by name:
   ```bash
   az ad sp list --display-name "PolarisServicePrincipal" --query "[].appId" -o tsv
   ```
   This returns the application ID (client ID) of your service principal.

2. **Remove Role Assignments**

   Before deleting the service principal, remove its role assignments:
   ```bash
   az role assignment delete --assignee "<CLIENT_ID>" --scope "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/<YOUR_RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<YOUR_STORAGE_ACCOUNT_NAME>"
   ```
   Replace:
   - `<CLIENT_ID>` with your service principal's appId
   - `<YOUR_RESOURCE_GROUP>` with your resource group name
   - `<YOUR_STORAGE_ACCOUNT_NAME>` with your storage account name

3. **Delete the Service Principal**

   Delete the service principal itself:
   ```bash
   az ad sp delete --id "<CLIENT_ID>"
   ```

4. **Delete the Associated App Registration** (Optional)

   In some cases, you might also want to delete the associated app registration:
   ```bash
   az ad app delete --id "<CLIENT_ID>"
   ```

5. **Verify Removal** (Optional)

   Confirm the service principal no longer exists:
   ```bash
   az ad sp show --id "<CLIENT_ID>"
   ```
   This should return an error if the service principal was successfully deleted.
