import os
import json
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .logging_config import setup_logger

# Suppress only the single InsecureRequestWarning from urllib3 needed to disable SSL verification warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class DynatraceClient:

    def __init__(self, client_id, client_secret, account_urn, headers={}, log_level='INFO'):
        setup_logger(__name__, log_level)
        self.logger = logging.getLogger(__name__)
        self.headers = headers
        self.baseurl = 'https://api.dynatrace.com'
        self.session = requests.Session()
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_urn = account_urn
        self.account_uuid = account_urn.split(':')[2]

        # Authenticate and get the token
        self.token = self.login()
        self.headers['Authorization'] = f'Bearer {self.token}'
        self.headers['Content-Type'] = 'application/json'

        # Get initial account information
        self.environments = self.get_all_environments()
        self.account_groups = self.get_all_account_groups()
        self.account_policies = self.get_all_account_policies()

    def _setup_logger(self, log_level):
        log_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        log_level = log_levels.get(log_level.upper(), logging.INFO)

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        handler = logging.FileHandler('account_api.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def login(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'account-env-read account-idm-read iam-policies-management',
            'resource': self.account_urn
        }
        headers = self.headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        req = self.session.post('https://sso.dynatrace.com/sso/oauth2/token', data=payload, headers=headers, verify=False)

        if req.status_code < 400:
            return req.json()['access_token']
        else:
            self.logger.error(f"SSO login failed with status code {req.status_code}")
            raise requests.HTTPError(f"SSO login failed with status code {req.status_code}")

    def get_all_environments(self):
        req = self.session.get(f'{self.baseurl}/env/v2/accounts/{self.account_uuid}/environments', headers=self.headers, verify=False)
        if req.status_code == 200:
            return req.json()['data']
        else:
            self.logger.error(f"Failed to get environments with status code {req.status_code}")
            raise requests.HTTPError(f"Failed to get environments with status code {req.status_code}")

    def get_all_account_groups(self):
        req = self.session.get(f'{self.baseurl}/iam/v1/accounts/{self.account_uuid}/groups', headers=self.headers, verify=False)
        if req.status_code == 200:
            return req.json()['items']
        else:
            self.logger.error(f"Failed to get account groups with status code {req.status_code}")
            raise requests.HTTPError(f"Failed to get account groups with status code {req.status_code}")

    def get_all_account_policies(self):
        req = self.session.get(f'{self.baseurl}/iam/v1/repo/account/{self.account_uuid}/policies/aggregate', headers=self.headers, verify=False)
        if req.status_code == 200:
            return req.json()['policyOverviewList']
        else:
            self.logger.error(f"Failed to get account policies with status code {req.status_code}")
            raise requests.HTTPError(f"Failed to get account policies with status code {req.status_code}")

    def get_policy_details(self, level_type, level_id, uuid):
        req = self.session.get(f'{self.baseurl}/iam/v1/repo/{level_type}/{level_id}/policies/{uuid}', headers=self.headers, verify=False)
        if req.status_code == 200:
            return req.json()
        else:
            self.logger.error(f"Failed to get policy details with status code {req.status_code}")
            raise requests.HTTPError(f"Failed to get policy details with status code {req.status_code}")

    def get_policy_bindings(self, level_type, level_id, uuid):
        self.logger.debug(f"Starting request for policy bindings for {uuid}. Level Type: {level_type} | Level ID: {level_id}")
        req = self.session.get(f'{self.baseurl}/iam/v1/repo/{level_type}/{level_id}/bindings/{uuid}', headers=self.headers, verify=False)
        if req.status_code == 200:
            return req.json()
        else:
            self.logger.error(f"Failed to get policy bindings with status code {req.status_code}")
            raise requests.HTTPError(f"Failed to get policy bindings with status code {req.status_code}")