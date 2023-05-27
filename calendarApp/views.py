import json
from google_auth_oauthlib.flow import InstalledAppFlow
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
def GoogleCalendarInitView(request):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        print(settings.BASE_DIR)
        print(settings.SECRET_FILE)
        
    
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.SECRET_FILE,  # Replace with your client secret file path
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=request.build_absolute_uri('/rest/v1/calendar/redirect/')
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        return HttpResponse(json.dumps({'auth_url': auth_url},indent=4), content_type='application/json')


def GoogleCalendarRedirectView(request):
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.SECRET_FILE,  # Replace with your client secret file path
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=request.build_absolute_uri('/rest/v1/calendar/redirect/')
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        access_token = flow.credentials.token
        
        service = build('calendar', 'v3', credentials=flow.credentials)

    # Fetch events from the user's primary calendar
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        print(events)
        finalEvents=[]
        for event in events:
            summary = event['summary']
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            finalEvents.append({
                   'start':start,
                   'end':end,
                   'summary':summary
            })
            
        # Use the access_token to fetch events from the user's calendar
        # Implement the code to fetch events from the calendar here
        return HttpResponse(json.dumps({'events': finalEvents},indent=4), content_type='application/json')
