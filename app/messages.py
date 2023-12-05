# app/glific_api.py
"""Handles message related API requests (Create + Send for now)."""

import json
import requests

class MsgManager:
    """Message Manager."""

    SEND_MSG_URL = "https://api.staging.tides.coloredcow.com/api"

    def __init__(self, auth_manager):
        self.auth_manager = auth_manager

    def send_message(self, contact_id, message):
        """Create + Send a Message."""
        payload= json.dumps({
            "query": """
                mutation createAndSendMessage($input: MessageInput!) {
                createAndSendMessage(input: $input) {
                    message {
                    id
                    body
                    receiver {
                        id
                        name
                    }
                    }
                    errors {
                    key
                    message
                    }
                }
                }
                """,
            "variables": {
                "input": {
                    "body": message.body,
                    "flow": "OUTBOUND",
                    # "isHSM": False,
                    # "mediaId": 2,
                    # "params": [],
                    # "templateId": 4,
                    # "type": "TEXT",
                    # TODO: What should values here be?
                    "senderId": contact_id,
                    "receiverId": contact_id,
                }
            }
        })


        # TODO: Confirm this access token == auth token used in api description.
        headers = {
            'authorization': self.auth_manager.access_token,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.SEND_MSG_URL, headers=headers, data=payload)

        print(response.text)

        # TODO: Confirm no data members need to be modified when message sent
        if response.status_code == 200:
            return True
        return False
