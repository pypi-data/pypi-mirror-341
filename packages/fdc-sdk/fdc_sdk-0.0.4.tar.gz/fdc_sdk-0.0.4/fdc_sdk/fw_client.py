import requests
import json
import math

class FWClient:
    def __init__(self, url, org, token):
        self.base_url = url.rstrip("/") + "/aggregator/api/v2/sdk"
        self.org = org
        self.token = token
        self.headers = {
            "x-sdk-token": token ,
            "Content-Type": "application/json"
        }

    def list_all_entities(self, layer="BRONZE", q=None, id=None):
        try:
            params ={}
            params["layer"] = layer.upper()
            if q:
                params["q"] = q
            if id:
                params["id"] = id

            print("Calling /entities/ with params:", params)

            response = requests.get(
                f"{self.base_url}/entities/",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            response_json = response.json()

            count = response_json.get("count", 0)
            results = response_json.get("results", [])

            print(f"Fetched {count} entities.")
            return results

        except requests.RequestException as e:
            print(f"Error fetching entity list: {e}")
            return []

    def create_silver_entity(self, entity_name, sql_query):
        try:
            payload = {
                "entity_name": entity_name,
                "sql_query": sql_query
            }

            print("Sending create_silver_entity payload:", json.dumps(payload, indent=2))

            response = requests.post(
                f"{self.base_url}/create-silver-entity/",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            print("Silver entity created successfully.")
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating silver entity: {e}")
            return {"error": str(e)}
    def create_gold_entity(self, entity_name, sql_query):
        try:
            payload = {
                "entity_name": entity_name,
                "sql_query": sql_query
            }

            print("Sending create_gold_entity payload:", json.dumps(payload, indent=2))

            response = requests.post(
                f"{self.base_url}/create-gold-entity/",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            print("Gold entity created successfully.")
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating silver entity: {e}")
            return {"error": str(e)}
    def trigger_event(self, event_payload):
        try:
            print("sending event ",event_payload)
            response = requests.post(
                f"{self.base_url}/trigger-event/",
                headers=self.headers,
                json=event_payload
            )
            response.raise_for_status()
            print("Event triggered successfully.")
            return response.json()
        except requests.RequestException as e:
            print(f"Error triggering event : {e}")
            return {"error": str(e)}
            
