# Getting the credentials.json file for Google Calendar API

To get the `credentials.json` file for Google Calendar API, follow these steps:

1. **Create a project in the Google API Console:**
   - Go to the [Google API Console](https://console.developers.google.com/).
   - Click on the project drop-down and select `New Project`.
   - Enter a name for your project and click `Create`.

2. **Enable the Google Calendar API:**
   - In the Google API Console, select your new project.
   - Navigate to the "Library" section.
   - Search for "Google Calendar API" and click on it.
   - Click the "Enable" button.

3. **Create credentials for the API:**
   - Navigate to the "Credentials" section in the API Console.
   - Click on the "Create credentials" button and select "Service account".
   - Fill in the required details and click "Create".
   - Assign the "Project" role (e.g., "Editor") to the service account and continue.
   - Click "Done" to finish creating the service account.

4. **Download the credentials file:**
   - In the "Credentials" section, find the service account you created.
   - Click on the email of the service account.
   - Click on the "Keys" tab.
   - Click on "Add Key" and select "JSON".
   - A JSON file containing your credentials will be downloaded. This is the `credentials.json` file.

For more detailed information, you can refer to the [Google API Console documentation](https://console.developers.google.com/).

Once you have the `credentials.json` file, you can place it in the root directory of your project and use it for authenticating with the Google Calendar API.
