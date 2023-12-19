# flask_e2e_project
Final Project for HHA 504

## App Structure

This app displays a patient registry table, showing the patient ID, first name, last name, and date of birth. Users will log into the app through Google Authentication, where they will be redirected to the registry page. On this page will be the table with every current patient entry. Users can use the URL to filter GET requests by any of the parameters. An example of the syntax and its result will be shown in the screenshots. The user info button directs users to see the information that is pulled from the Google login. The table was made in MySQL Workbench and was populated using the populate.py file, which generated 100 fake entries and put them into the table when run.

## Technologies used

This app was built on Google Shell, using Flask as the backend, with HTML and CSS to stylize the front end. The patient registry database is stored on a MySQL Flexible Server hosted by Azure. A SqlLite database is used to store information about users who have logged in, which can be accessed using db_review.py. Logging was performed by Python's built-in logging package. Logs can be viewed under the log folder within the app folder. The app was dockerized and can be accessible through a .tar file, which is stored locally but can be shared with another user for access. The app was deployed through Azure Web Services. I will include a section below dedicated to Azure as there were several issues with it.

## Accessing

Before using this locally or deploying it yourself, you should recreate the .env file. It should contain the following variables: DB_HOST(host link to MySQL database), DB_DATABASE (database name within MySQL database), DB_USERNAME(admin username for MySQL database), DB_PASSWORD(admin password for MySQL database), GOOGLE_CLIENT_SECRET(secret id from google auth page), GOOGLE_CLIENT_ID(google client id from google auth page).

### Local

The app can be run locally by running 'python app.py' in the working directory where the app lives. Note: for the Google authentication to work, the redirect URI must be changed so it matches your URI. This is the URI in line 64 of the app.py file. You must also create a Web application under the Google console credentials, where you can place your local URL as well as the corresponding redirect URL. 

### Docker

After dockerizing the app, I downloaded it as a .tar file, which can be shared with other people who want to download and run it. They can store it in a directory, load it in, and then run it on their device. Alternatively, I could decide to push it into a docker directory, where it can be downloaded remotely and run, however, I did not publish this application.

### Azure

I attempted to deploy this application to Azure. It technically has deployed, the link is here: https://sean504final.azurewebsites.net/

To deploy, install Azure CLI in your terminal and log in using the device code. Once logged in, use az web app up, followed by the app name, resource group name, python version, and sku to upload your working directory as an app.

My website opens, however, I ran into a 401 client error with the Google authentication. I tried changing the redirect URIs and changing my Google endpoints, but I was not able to recreate the authentication process that I had locally, as I would still run into either the 401 client error, or I would log in but it would not store the login information and I would not be granted any access to my table. My / endpoint, as well as my /info endpoint, are accessible, as they do not require Google authentication to access. When trying to access my /patients table without the authentication, it fails and I see my coded logger message saying I do not have access. There seems to be some error with the redirect URI, and using the URI that was provided in Azure documentation allowed for login but nothing was stored, meaning there was no user and nothing could still be accessed. That documentation is here: https://learn.microsoft.com/en-us/azure/app-service/overview-authentication-authorization

I also tried using Azure's built-in credentials system, which I was able to configure correctly so I would log in through Google when the application opened. However, my application uses variables from my coded authentication endpoints, and I am unsure how to retrieve the same variables from Azure's authentication method, meaning I would be missing parts of my application or I would have to re-write it. I also had issues with Google Chrome detecting my application as unsecured, only when I changed the app's URI to interact with my Azure website. 

This was the only major issue I ran into with my application. I was still at least able to partially deploy it and hit the rest of the objectives. I'm curious how this Google OAuth process could be fixed, as I tried several solutions and could not get the feature fully functional on my deployed version.


