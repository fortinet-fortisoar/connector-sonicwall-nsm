"""
Copyright start
MIT License
Copyright (c) 2025 Fortinet Inc
Copyright end
"""

import requests
from connectors.core.connector import get_logger, ConnectorError
from .constants import *

logger = get_logger('sonicwall-nsm')


class SonicWallNSM(object):

    def __init__(self, config):
        url = config.get('server_url', '').strip('/')
        if not url.startswith('https://') and not url.startswith('http://'):
            self.url = 'https://{0}/api/manager/'.format(url)
        else:
            self.url = url + '/api/manager/'
        self.api_key = config.get('api_key')
        self.verify_ssl = config.get('verify_ssl', False)
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-KEY': self.api_key
        }

    def make_api_call(self, endpoint, method='POST', payload=None, params=None):
        service_endpoint = self.url + endpoint
        try:
            response = requests.request(method, service_endpoint, json=payload,
                                        headers=self.headers, params=params,
                                        verify=self.verify_ssl)
            logger.debug('API Service Endpoint: {0}'.format(service_endpoint))
            logger.debug('API Payload: {0}'.format(payload))
            logger.debug('API Response Status code: {0}'.format(response.status_code))
            logger.debug('API Response: {0}'.format(response.text))
            if response.ok or response.status_code == 204:
                logger.info('Successfully got response for url {0}'.format(service_endpoint))
                if 'json' in str(response.headers):
                    return response.json()
                else:
                    return response
            else:
                logger.error("{0}".format(response.status_code))
                raise ConnectorError("{0}:{1}".format(response.status_code, response.text))
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError(
                'The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid Credentials')
        except Exception as err:
            raise ConnectorError(str(err))


def check_payload(payload):
    updated_payload = {}
    for key, value in payload.items():
        if isinstance(value, dict):
            nested = check_payload(value)
            if len(nested.keys()) > 0:
                updated_payload[key] = nested
        elif value != '' and value is not None:
            updated_payload[key] = value
    return updated_payload


def commit_changes(config):
    nsm = SonicWallNSM(config)
    endpoint = "commits/pending"
    resp = nsm.make_api_call(endpoint, method='POST')
    status = resp.get('status', {}).get('success')
    if status:
        logger.info("All changes successfully committed")
    else:
        logger.error("Failed to commit changes")


def get_access_rules(config, params):
    nsm = SonicWallNSM(config)
    endpoint = "graph/accessrules"
    limit = params.get('limit')
    query_parameters = {
        "filterType": int(FILTER_TYPE.get(params.get('filterType'))),
        "from": params.get('from'),
        "to": params.get('to'),
        "serialnum": params.get('serialnum'),
        "ruleType": RULE_TYPE.get(params.get('ruleType')),
        "limit": limit
    }
    limit_count = params.get('limitCount')
    children_obj_types = params.get('childrenObjTypes')
    if limit and limit_count is not None:
        query_parameters["limitCount"] = limit_count
    if children_obj_types:
        query_parameters["childrenObjTypes"] = children_obj_types
    query_parameters = check_payload(query_parameters)
    return nsm.make_api_call(endpoint, method='GET', params=query_parameters)


def create_address_object(config, params):
    nsm = SonicWallNSM(config)
    endpoint = "graph/addressobject"
    query_parameters = {
        "serialnum": params.get('serialnum')
    }
    query_parameters = check_payload(query_parameters)
    object_type = OBJECT_TYPE.get(params.get('object_type'))
    payload = {
        "name": params.get('name'),
        "description": params.get('description'),
        "zone": params.get('zone'),
        "type": object_type
    }
    if object_type == "host":
        payload["ip"] = params["ip"]
    elif object_type == "network":
        payload["ip"] = params["ip"]
        payload["netmask"] = params["netmask"]
    elif object_type == "range":
        payload["start_ip"] = params["start_ip"]
        payload["end_ip"] = params["end_ip"]
    elif object_type == "fqdn":
        payload["fqdn"] = params["fqdn"]
    elif object_type == "mac":
        payload["mac"] = params["mac"]
    body = {
        "in_addr_info": payload
    }
    body = check_payload(body)
    resp = nsm.make_api_call(endpoint, method='POST', params=query_parameters, payload=body)
    commit_changes(config)
    return resp


def get_address_objects(config, params):
    nsm = SonicWallNSM(config)
    endpoint = "graph/addressobject"
    query_parameter = check_payload(params)
    return nsm.make_api_call(endpoint, method='GET', params=query_parameter)


def update_address_object(config, params):
    nsm = SonicWallNSM(config)
    endpoint = "graph/addressobject"
    query_parameters = {
        "serialnum": params.get('serialnum'),
        "name": params.get('name'),
        "uuid": params.get('uuid')
    }
    query_parameters = check_payload(query_parameters)
    object_type = OBJECT_TYPE.get(params.get('object_type'))
    payload = {
        "name": params.get('new_name'),
        "zone": params.get('zone'),
        "type": object_type
    }
    if object_type == "host":
        payload["ip"] = params["ip"]
    elif object_type == "network":
        payload["ip"] = params["ip"]
        payload["netmask"] = params["netmask"]
    elif object_type == "range":
        payload["start_ip"] = params["start_ip"]
        payload["end_ip"] = params["end_ip"]
    elif object_type == "fqdn":
        payload["fqdn"] = params["fqdn"]
    elif object_type == "mac":
        payload["mac"] = params["mac"]
    body = {
        "in_addr_info": payload
    }
    body = check_payload(body)
    resp = nsm.make_api_call(endpoint, method='PUT', params=query_parameters, payload=body)
    commit_changes(config)
    return resp


def execute_an_api_call(config, params):
    try:
        nsm = SonicWallNSM(config)
        endpoint = params.get("endpoint")
        http_method = params.get("method")
        query_params = params.get("query_params") if params.get("query_params") else {}
        payload = params.get("payload") if params.get("payload") else {}
        logger.debug("Payload: {0}".format(payload))
        response = nsm.make_api_call(endpoint, method=http_method, params=query_params, payload=payload)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_all_tenants(config, params):
    nsm = SonicWallNSM(config)
    endpoint = "tenants?size=1"
    query_parameter = check_payload(params)
    resp = nsm.make_api_call(endpoint, method="GET", params=query_parameter)
    return resp


def _check_health(config):
    try:
        resp = get_all_tenants(config, params={})
        if resp["status"]["success"]:
            return True
        else:
            response = resp["status"]["info"][0]["message"]
            raise ConnectorError("Message : {0}".format(response))
    except Exception as err:
        logger.info(str(err))
        raise ConnectorError(str(err))


operations = {
    'get_access_rules': get_access_rules,
    'create_address_object': create_address_object,
    'get_address_objects': get_address_objects,
    'update_address_object': update_address_object,
    'execute_an_api_call': execute_an_api_call
}
