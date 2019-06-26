# Google People API

## Steps

### Google Authorization Steps

#### To get contacts saved in account

[Get credentials.json following these steps](https://developers.google.com/people/quickstart/python)

#### To Create Contacts

1. Go to [Google API Console](https://console.developers.google.com) and sign into your account.
2. Create a new project and enable People API
3. Go to Credentials tab and click on Configure Consent Screen Button.
4. Type some Application Name and Save.
5. Then go to Create Credentials and choose OAuth Client ID.
6. Choose other for this project and then download json file and keep it in the same folder as of the project.

### Running the file
We can simply run a flask server to add contact
Just launch-
```http://0.0.0.0:8091/?name={Name}&number={Contact Number}```
It will save the contact if contact doesn't already exist in your Google Account!
