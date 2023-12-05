# app/auth.py
"""Handles all auth related APIs."""

import datetime
import json
import requests

class AuthManager:
    """Authorization Manager."""

    LOGIN_URL = "https://api.staging.tides.coloredcow.com/api/v1/session"
    RENEW_URL = "https://api.staging.tides.coloredcow.com/api/v1/session/renew"

    def __init__(self):
        self.access_token = None
        self.renewal_token = None
        self.expiry_time = None

    def login(self):
        """Create a new session for an existing user."""

        payload = json.dumps({
            "user": {
                "phone": "917834811114",
                "password": "secret1234"
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", self.LOGIN_URL, headers=headers, data=payload)

        print(response.text)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access_token')
            self.renewal_token = data.get('renewal_token')
            self.expiry_time = (datetime.datetime.now() +
            datetime.timedelta(seconds=data.get('token_expiry_time')))
            return True
        return False

    def renew_token(self):
        """Renew an existing session."""

        payload = json.dumps({
            "data": {
                "data": {
                    "access_token": self.access_token,
                    "renewal_token": self.renewal_token,
                }
            }
        })

        # TODO: Confirm if this = 'Authorization key which includes the renew token.'
        # Seems like this is expected according to api.docs/includes/_auth.md line 120.

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.access_token,
        }

        response = requests.request("POST", self.RENEW_URL, headers=headers, data=payload)

        print(response.text)

        # TODO: Found format of respnse returned in api.docs/includes/_auth.md,
        #       glific api docs (https://api.glific.com/#23b77640-b818-459b-88e0-3437665bf7ad)
        #       say no response returned

        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access_token')
            self.renewal_token = data.get('renewal_token')
            self.expiry_time = datetime.datetime.now() + datetime.timedelta(
                               seconds=data.get('token_expiry_time'))
            return True
        return False

    def is_token_expired(self):
        """Check if the token has expired"""
        return datetime.datetime.now() >= self.expiry_time
