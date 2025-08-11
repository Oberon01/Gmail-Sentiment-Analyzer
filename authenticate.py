from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import google.auth.exceptions
import pickle, os, pathlib
from textblob import TextBlob
import time, traceback, logging
from dotenv import load_dotenv, dotenv_values
import base64, email, html, re


env = dotenv_values()
LABEL_ID_REVIEW = env["LABEL_ID_REVIEW"]
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
TOKEN = pathlib.Path("token.pickle")

def get_service():
	creds = None
	if TOKEN.exists():
		creds = pickle.loads(TOKEN.read_bytes())
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
			creds = flow.run_local_server(port=0)
		TOKEN.write_bytes(pickle.dumps(creds))
	return build("gmail", "v1", credentials=creds)

if __name__ == "__main__":
     get_service()