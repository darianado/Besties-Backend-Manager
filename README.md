# seg-backend-manager
Backend Manager Application for SEG Djangoals. 
This application provides an interface to interact with the backend directly for seeding and un-seeding, as well as testing out various backend features without the need of a frontend client.

> **Please note: Seeding and unseeding a large number of users (>100) is *pricey*. Please check [this](https://console.firebase.google.com/project/seg-djangoals/usage) page to see if we are hitting our free daily max.**

## Local setup
In order to use this application, you must setup credentials on your machine and install dependencies. Follow this guide:
1. Open this [link](https://console.firebase.google.com/project/seg-djangoals/settings/serviceaccounts/adminsdk)
2. Click the button called *Generate new private key*, and then click *Generate key* to download a .json file. **Do NOT share this file with anyone else - everyone in the project should make their own file.**
3. Rename the downloaded file to '*serviceAccountKey.json*' and put it in the same directory as '*main.py*'.
4. Open a new terminal window, and navigate to the folder where the '*main.py*' file is located.
5. Run the command `source venv/bin/activate`
6. Run the command `pip install -r requirements.txt`

## Using the application
This application has an easy to use menu interface, which makes it easy to navigate. To start the application, follow this guide:
1. Open a new terminal window, and navigate to the folder where the '*main.py*' file is located.
2. Run the command `source venv/bin/activate`
3. Run the command `python3 main.py`