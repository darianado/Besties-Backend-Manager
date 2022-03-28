# besties-backend-manager

**Application title:** Backend Manager Application

**Authors:**
* Nikolaj Banke Jense
* Chukwudalu Esomeju
* Dariana Dorin
* Luca Brown
* Mateusz Adamski
* Jacqueline Ilie
* Petra-Theodora Safta
* Sze Wye Tham
* Yue Yu


Backend Manager Application for the 'Besties' app developed by SEG-Djangoals. 
This application provides an interface to interact with the backend directly for various purposes including seeding and un-seeding and manually testing out various backend features without the need of a frontend client or production environment.

> **Please note: Seeding and unseeding a large number of users (>100) is *pricey*. Please check [this](https://console.firebase.google.com/project/seg-djangoals/usage) page to see if the project is hitting the free daily limit.**

## Developer setup
**This application is intended to work on macOS and Linux only.** 

In order to use this application, you must setup credentials on your machine and install dependencies. Follow this guide:
1. Open this [link](https://console.firebase.google.com/project/seg-djangoals/settings/serviceaccounts/adminsdk).
2. Click the button called *Generate new private key*, and then click *Generate key* to download a .json file. **Do NOT share this file with anyone else as it contains confidential information - everyone in the project should make their own file.**
3. Rename the downloaded file to '*serviceAccountKey.json*' and put it in the same directory as '*main.py*'.
4. Open a new terminal window and navigate to the folder where the '*main.py*' file is located.
5. Run the command `python3 -m venv venv` to create a new virtual environment.
6. Run the command `source venv/bin/activate` to activate the virtual environment.
7. Run the command `pip3 install -r requirements.txt` to install the required dependencies.

## Using the application
To start the application, follow this guide:
1. Open a new terminal window, and navigate to the folder where the '*main.py*' file is located.
2. Run the command `source venv/bin/activate`.
3. Run the command `python3 main.py`.

The application has an easy to use menu interface, which makes it easy to navigate and use.

## Sources
* Code for loading and manipulating json files (`update_settings_field()` in '*utils.py*') has been inspired by [this](https://stackoverflow.com/a/21035861) code snippet written by Stack Overflow user '*falsetru*'.
* Packages and external libraries used in this application are listed in '*requirements.txt*'.