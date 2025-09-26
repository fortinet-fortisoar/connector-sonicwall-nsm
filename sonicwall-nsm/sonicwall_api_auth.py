"""
Copyright start
MIT License
Copyright (c) 2025 Fortinet Inc
Copyright end
"""

import requests, json
from connectors.core.connector import get_logger, ConnectorError
from connectors.core.utils import update_connnector_config

logger = get_logger('sonicwall-nsm')


class SonicWallAuth:

    def __init__(self, config):
        url = config.get('server_url', '').strip('/')
        if not url.startswith('https://') and not url.startswith('http://'):
            self.url = 'https://{0}'.format(url)
        else:
            self.url = url
        self.api_key = config.get('api_key')
        self.verify_ssl = config.get('verify_ssl')

    def generate_token(self):
        try:
            token_resp = acquire_token(self)
            token_resp['accessToken'] = token_resp.get("access_token")
            token_resp.pop("access_token")
            return token_resp
        except Exception as err:
            logger.error("{0}".format(err))
            raise ConnectorError("{0}".format(err))

    def validate_token(self, connector_config, connector_info):
        try:
            if not connector_config.get('accessToken'):
                token_resp = self.generate_token()
                connector_config['accessToken'] = token_resp['accessToken']
                update_connnector_config(connector_info['connector_name'], connector_info['connector_version'],
                                         connector_config,
                                         connector_config['config_id'])

                return "{0}".format(connector_config.get('accessToken'))
            else:
                return "{0}".format(connector_config.get('accessToken'))
        except Exception as err:
            logger.error("{0}".format(str(err)))
            raise ConnectorError("{0}".format(str(err)))


def acquire_token(self):
    try:
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

        # Step 1: Get tenants
        response = requests.get(
            'https://api.mysonicwall.com/api/hgms/get-cloud-tenants',
            headers=headers,
            verify=self.verify_ssl
        )
        if not response.ok:
            raise ConnectorError(response.text)

        cloud_tenants = response.json()
        tenant_list = cloud_tenants.get('content', {}).get('arrTenants', [])
        tenant_serial_id, product_group_id = "", ""

        for tenant in tenant_list:
            for cloud in tenant.get("cloudServices", []):
                if cloud.get("tenantSerial"):
                    tenant_serial_id = cloud["tenantSerial"]
                    break
            if tenant_serial_id:
                product_group_id = tenant.get("productGroupID", "")
                break

        # Condition 1: Must have product_group_id and tenant_serial_id
        if not product_group_id or not tenant_serial_id:
            raise ConnectorError("Product Group ID/Tenant Serial ID not present for the tenant.")

        # Step 2: Generate access code
        body = {"tenantId": product_group_id}
        response = requests.post(
            'https://api.mysonicwall.com/api/generate-cscaccesscode',
            headers=headers,
            data=json.dumps(body),
            verify=self.verify_ssl
        )
        if not response.ok:
            raise ConnectorError(response.text)

        resp_access_code = response.json()
        access_code = resp_access_code.get('content', {}).get('accessCode')

        # Condition 2: Must have access_code
        if not access_code:
            raise ConnectorError("Error: Access code not present in response.")

        # Step 3: Get bearer token
        bearer_headers = {'Content-Type': 'application/json'}
        body = {"tenantSerial": tenant_serial_id, "code": access_code}
        response = requests.post(
            '{0}/api/manager/auth/sso'.format(self.url),
            headers=bearer_headers,
            data=json.dumps(body),
            verify=self.verify_ssl
        )
        if not response.ok:
            raise ConnectorError(response.text)

        bearer_token = response.json()
        token = (
            bearer_token.get('status', {})
            .get('info', [{}])[0]
            .get('message')
        )

        # Condition 3: Must have token
        if not token:
            raise ConnectorError("Error: Bearer token not present in response.")

        return {"access_token": token}

    except Exception as err:
        raise ConnectorError(f"Unexpected error: {err}")


def check(config, connector_info):
    try:
        sonic = SonicWallAuth(config)
        if not 'accessToken' in config:
            token_resp = sonic.generate_token()
            config['accessToken'] = token_resp.get('accessToken')
            update_connnector_config(connector_info['connector_name'], connector_info['connector_version'], config,
                                     config['config_id'])
            return True
        else:
            token_resp = sonic.validate_token(config, connector_info)
            return True
    except Exception as err:
        raise ConnectorError(str(err))
