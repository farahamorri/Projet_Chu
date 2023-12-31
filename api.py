from google.oauth2 import service_account
import googleapiclient.discovery

# Charge le fichier JSON des clés d'authentification
credentials = service_account.Credentials.from_service_account_file(
    '/Users/farahamorri/Desktop/Centrale/ProjetG1G2/chu2/client_secret_223705720317-k1b855r74pi1qg6a6kqsis9d4fhivavh.apps.googleusercontent.com.json', scopes=['https://www.googleapis.com/auth/calendar']
)

# Initialise le client Google Calendar
service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
