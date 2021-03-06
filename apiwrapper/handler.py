import os
import json
import requests
import json
from apiwrapper.scriptcreator import LoadScriptGenerator
from jmxextractor.extractor import Extractor
from apiwrapper import exceptions


class JMXHandler(object):

    def __init__(self, jmx_file_path):
        self.token = os.environ.get('LOAD_IMPACT_TOKEN', '')
        with open('apiwrapper/config.json', 'rb') as config_file:
            self.data = Extractor(jmx_file_path, json.load(config_file)).data

    def create_scenario(self):
        payload = json.dumps(
            dict(
                load_script=LoadScriptGenerator(
                    self.data['domain'], self.data['targets']
                ).script,
                name="test_scenario"
            )
        )
        resp = requests.post(
            'https://api.loadimpact.com/v2/user-scenarios',
            data=payload,
            headers={"Content-Type": "application/json"},
            auth=(self.token, '')
        )
        if resp.status_code == 400:
            raise exceptions.BadRequestException(
                "Could not create scenario. Bad payload."
            )
        elif resp.status_code == 401:
            raise exceptions.MissingAPITokenException(
                "Could not create scenario. Missing or invalid API token."
                "Make sure LOAD_IMPACT_TOKEN env var is set."
            )
        resp.raise_for_status()
        return resp.json()['id']

    def create_test_config(self, scenario_id):
        payload = {
            'name': self.data['test_plan_name'],
            'url': 'http://%s/' % self.data['domain'],
            'config': {
                "user_type": "sbu",
                "load_schedule": [{"users": 10, "duration": 10}],
                "tracks": [{
                    "clips": [{
                        "user_scenario_id": scenario_id,
                        "percent": 100
                    }],
                    "loadzone": "amazon:us:ashburn"
                }]
            }
        }
        resp = requests.post(
            url='https://api.loadimpact.com/v2/test-configs',
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            auth=(self.token, '')
        )
        resp.raise_for_status()
        return resp.json()['id']
