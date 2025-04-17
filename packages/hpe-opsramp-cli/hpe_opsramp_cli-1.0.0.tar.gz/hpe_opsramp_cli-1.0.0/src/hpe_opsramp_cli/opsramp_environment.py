import inspect
import json
import os
import sys
from typing import Any

import requests
import yaml
import yaml.scanner
from rich import print

from opentelemetry.instrumentation.requests import RequestsInstrumentor


from hpe_opsramp_cli.singleton_logger import SingletonLogger

try:
    from . import settings as s
except ImportError:
    try:
        sys.path.append()
        from hpe_opsramp_cli import settings as s
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

logger = SingletonLogger().get_logger()


class OpsRampEnvironment:

    OPS_ALERT_SEARCH_ATTRIBUTES = [
        "states",
        "startDate",
        "endDate",
        "priority",
        "uniqueId",
        "deviceStatus",
        "resourceType",
        "resourceIds",
        "actions",
        "alertTypes",
        "metrics",
        "duration",
        "alertTimeBase",
        "clientIds",
        "ticketId",
        "apps",
    ]

    def __init__(self, envname, envfile="environments.yml", isSecure=True):
        self.get_environment(envname, envfile)

        logger.debug("Invoking RequestsInstrumentor().instrument")
        RequestsInstrumentor().instrument(
            request_hook=self.request_hook, response_hook=self.response_hook
        )

        self.isSecure = True
        if isinstance(isSecure, str) and (
            isSecure.lower() == "false" or isSecure.lower() == "no" or isSecure == "0"
        ):
            self.isSecure = False

    def get_token(self):
        url = self.env["url"] + "/tenancy/auth/oauth/token"

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.env["client_id"],
            "client_secret": self.env["client_secret"],
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=self.isSecure
        )
        if response.ok:
            return response.json()["access_token"]
        else:
            logger.error("Invalid key and secret in the environment file")
            sys.exit(1)

    def get_environment(self, envname="", envfile=""):
        if hasattr(self, "env"):
            return self.env
        try:
            envstream = open(envfile, "r")
        except FileNotFoundError:
            logger.error(f"{s.ENV_FILE_NOT_FOUND_ERROR_MESSAGE}")
            # print(s.ENV_FILE_NOT_FOUND_ERROR_MESSAGE % (envfile, os.getcwd()))
            sys.exit(1)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        else:
            try:
                envs = yaml.safe_load(envstream)
                filtered_envs = filter(lambda x: (x["name"] == envname), envs)
                self.env = next(filtered_envs)
                return self.env
            except StopIteration:
                logger.error(f"{s.ENV_NAME_NOT_FOUND_ERROR_MESSAGE}")
                # print(s.ENV_NAME_NOT_FOUND_ERROR_MESSAGE % (envname, envfile))
                sys.exit(1)
            except yaml.scanner.ScannerError:
                print(s.INVALID_ENV_FILE_ERROR_MESSAGE % (envfile))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    def get_json_from_file(self, file):
        jsonarray: Any = None
        try:
            with open(file) as f:
                jsonarray = json.load(f)
        except json.JSONDecodeError:
            # rich.print("The json file %s is not a valid json file" % (file))
            logger.error(f"The json file: {file} is not a valid json file")
            """
            print(type(error))    # the exception type
            print(error.args)     # arguments stored in .args
            print(error)
            """
            sys.exit(1)
        except FileNotFoundError:
            pass
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        """
        Looking into current folder
        """
        json_file_abs_path: str
        current_dir = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        json_file_abs_path = os.path.join(current_dir, file)

        try:
            with open(json_file_abs_path) as f:
                jsonarray = json.load(f)
        except FileNotFoundError:
            # rich.print("The json file %s is not found" % (file))
            logger.error(f"The json file: {file} is not found")
            sys.exit(1)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            """
            debug notes
            jsonarray={dict:5 } {'fields': ['id'], 'filterCriteria': 'tags.name = "Managed By"  AND tags.value = "Alert" ', 'objectType': 'resource', 'pageNo': 1, 'pageSize': 500}
            """
            return jsonarray

    def do_post(self, input_payload, api_name: str, client_id=None) -> Any:
        """

        :param input_payload: input payload
        :param api_name: name of API to be invoked; example - opsql
        :return: results from response payload
        """

        logger.debug("locals() %s " % locals())

        endpoints = {
            "opsql": "/opsql/api/v3/tenants/" + self.env["tenant"] + "/queries",
            "resource_unmanage": "/api/v2/tenants/"
            + self.env["tenant"]
            + "/resources/action/unmanage",
        }

        if client_id:
            endpoints.update(
                {
                    "resource_unmanage_partner": "/api/v2/tenants/"
                    + client_id
                    + "/resources/action/unmanage"
                }
            )

        url = self.env["url"] + endpoints[api_name]

        token = self.get_token()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + token,
        }
        # print("Posting the below payload to URL: %s" % (url))
        # print_json(json.dumps(input_payload))
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=json.dumps(input_payload),
            verify=self.isSecure,
        )

        unmanage_api_names = {"resource_unmanage", "resource_unmanage_partner"}
        if api_name in unmanage_api_names:
            """
            unmanage returns nothing so ok to get JSONDecodeError('Expecting value: line 1 column 1 (char 0)')
            """
            logger.debug("unmanage API completed")
            return None
        elif not response.ok and api_name not in unmanage_api_names:
            try:
                responseobj = response.json()
            except Exception:
                # rich.print(repr(response))
                logger.error(f"{repr(response)}")
                sys.exit(1)
            except:
                # print("Unexpected error:", sys.exc_info()[0])
                logger.error(f"Unexpected error: {sys.exc_info()[0]}")
                raise
        elif response.ok and api_name not in unmanage_api_names:
            try:
                responseobj = response.json()
            except Exception:
                logger.error(f"Unexpected error Exiting:{sys.exc_info()[0]}")
                raise
                sys.exit(1)
            try:
                if "results" in responseobj:
                    results = responseobj["results"]
                else:
                    results = responseobj
                    """
                Fixed as per if "nextPage" in responseobj and responseobj['nextPage'] == True:
                E712 Avoid equality comparisons to `True`; use `if responseobj['nextPage']:` for truth checks
                """
                if responseobj["nextPage"]:
                    # print("Got %i %s from %s, proceeding to page %i" % (len(results), obtype, self.env['name'], responseobj['nextPageNo']))
                    pageNo = input_payload["pageNo"]
                    pageNo = pageNo + 1
                    input_payload["pageNo"] = pageNo
                    """
                    To Fix
                    getting below error 
                    TypeError: json must be str. Did you mean print_json(data={'results': [{'id': '7f72389f-99bf-4390-90c5-74b5f1adf24d', 'name': 'DC142', 'type': 'Other'}, {'id': '99cf1edb-d2d5-4feb-ae81-842c365ee8b2', 'name': 'DC134', 'type': 'Other'}, {'id': 'bef80628-9bde-4712-88df-dc7545906d65', 'name': 'DC143', 'type': 'Other'}, {'id': '17fa026c-cb50-4048-b40b-19531a2fc452', 'name': 'Windows', 'type': 'Server'}, {'id': '553d817c-69e8-4df1-bd62-632d6318ac22', 'name': 'DC155', 'type': 'Other'}], 'pageNo': 1, 'pageSize': 5, 'nextPage': True, 'descendingOrder': False}) ?
                    print("OpsQL query:\n")
                    print_json(json.dumps(opsql_query))
                    print("Results:\n")
                    print_json((response.json()))
                    """

                    return results + self.do_post(input_payload, api_name)
                else:
                    # print("OpsQL query: %s \nresults %s" % (json.dumps(opsql_query), response.json()))
                    return results
            except Exception:
                logger.error(f"Unexpected error Exiting:{sys.exc_info()[0]}")
                raise
                sys.exit(1)

        return response.json()

    def get_objects(
        self,
        obtype,
        page=1,
        queryString=None,
        searchQuery=None,
        countonly=False,
        attrId=None,
    ):

        endpoints = {
            "clients": self.env["partner"] + "/clients/" + self.env["tenant"],
            "incidentCustomFields": self.env["tenant"] + "/customFields/INCIDENT",
            "deviceGroups": self.env["tenant"] + "/deviceGroups/minimal",
            "userGroups": self.env["tenant"] + "/userGroups",
            "urgencies": self.env["tenant"] + "/incidents/urgencies",
            "customAttributes": self.env["tenant"] + "/customAttributes/search",
            "resources": self.env["tenant"] + "/resources/search",
            "resourcesNewSearch": self.env["tenant"] + "/query/execute",
            "assignedAttributeEntities": self.env["tenant"]
            + "/customAttributes/"
            + str(attrId)
            + "/assignedEntities/search",
        }

        url = self.env["url"] + "/api/v2/tenants/" + endpoints[obtype]
        token = self.get_token()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + token,
        }

        params = {"pageSize": 500, "pageNo": page}

        if countonly:
            params["pageSize"] = 1

        if queryString:
            params["queryString"] = queryString

        if searchQuery:
            params["searchQuery"] = searchQuery
            params["type"] = "resources"

        if obtype == "userGroups":
            params["pageSize"] = 100

        response = requests.request(
            "GET", url, headers=headers, verify=self.isSecure, params=params
        )
        try:
            responseobj = response.json()
        except Exception:
            logger.error(f"{repr(response)}")
            sys.exit(1)
        except:
            logger.error(f"Unexpected error: {sys.exc_info()[0]}")
            raise

        if countonly:
            return int(responseobj["totalResults"])

        if "results" in responseobj:
            results = responseobj["results"]
        else:
            results = responseobj

        if "nextPage" in responseobj and responseobj["nextPage"]:
            # print("Got %i %s from %s, proceeding to page %i" % (len(results), obtype, self.env['name'], responseobj['nextPageNo']))
            return results + self.get_objects(
                obtype=obtype,
                page=responseobj["nextPageNo"],
                queryString=queryString,
                searchQuery=searchQuery,
                attrId=attrId,
            )
        else:
            return results

    # `request_obj` is an instance of requests.PreparedRequest
    def request_hook(self, span, request_obj):

        if span is not None:
            span.set_attribute("http.custom_attribute", "custom_value")
            # print(f"Custom hook: {request.method} {request.url}")
            logger.debug(
                "span: %s request.method: %s request.url: %s request.body %s"
                % (span, request_obj.method, request_obj.url, request_obj.body)
            )
        pass

    # `request_obj` is an instance of requests.PreparedRequest
    # `response` is an instance of requests.Response
    def response_hook(self, span, request_obj, response):
        if span is not None:
            logger.debug(
                "span: %s request.method: %s request.url: %s request.body %s response: %s"
                % (
                    span,
                    request_obj.method,
                    request_obj.url,
                    request_obj.body,
                    response,
                )
            )
        pass
