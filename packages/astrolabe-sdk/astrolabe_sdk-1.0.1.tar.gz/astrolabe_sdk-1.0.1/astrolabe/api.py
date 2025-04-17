"""
Provides access to the OKAPI:Astrolabe API.
"""

import csv
import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from urllib.parse import quote

import requests
from dotenv import find_dotenv, load_dotenv

from astrolabe.error import AuthenticationError, ClientError, ServerError, SetupError
from astrolabe.utils import get_now_utc, parse_bool, parse_float, parse_int, sanitize_datetime


class AstrolabeAPI:
    """
    Provides access to the OKAPI:Astrolabe API, covering those endpoints
    that are most useful for automating processes.

    The constructor takes an optional instance argument.
    By defaul it connects you to the production API.
    If you want to test your scripts first, use AstrolabeAPI("staging").

    Before sending requests, you need to log in.
    This requires the following credentials as environment variables:

      * ASTROLABE_AUTH0_USERNAME
      * ASTROLABE_AUTH0_PASSWORD
      * ASTROLABE_AUTH0_CLIENT_ID
      * ASTROLABE_AUTH0_DOMAIN
      * ASTROLABE_AUTH0_AUDIENCE
    """

    def __init__(self, instance: str = "production"):
        self.base_url: str = self._api_base_url(instance)
        self.access_token: Optional[str] = None
        self.organization_id: Optional[str] = None

    def login(self, organization_id: str):
        """
        Log in. This requires your Auth0 credentials being defined in the environment,
        as well the ID of the organization you are member of.
        """
        # Load the environment.
        load_dotenv()
        load_dotenv(find_dotenv(usecwd=True))

        # Check that it contains what we need.
        for env_var in [
            "ASTROLABE_AUTH0_USERNAME",
            "ASTROLABE_AUTH0_PASSWORD",
            "ASTROLABE_AUTH0_CLIENT_ID",
            "ASTROLABE_AUTH0_DOMAIN",
            "ASTROLABE_AUTH0_AUDIENCE"
        ]:
            if os.getenv(env_var) is None:
                raise SetupError(f"Environment variable {env_var} is not set.")

        # Authenticate against Auth0.
        print("Logging in to OKAPI:Astrolabe...")
        self.access_token = self._get_access_token_from_auth0()
        self.organization_id = organization_id
        print("Authentication succeeded. You are ready to go.")

    def switch_organization(self, organization_id: str):
        """
        Switch the organization with which you are logged in.
        This will not re-authenticate you, so it will only work
        if you are also member of the given other organization.
        If you want to switch user accounts, use `login` instead.
        """
        self.organization_id = organization_id

    def get(self, path, return_raw_response=False) -> Any:
        """
        Send a GET request to the specified path.
        Returns the response data as dictionary.
        If you want the full raw response, set the `return_raw_response` parameter to `True`.
        If the response status is 4xx, it raises a ClientError;
        if the response status is 5xx, it raises a ServerError.
        """
        if path.startswith("/"):
            path = path[1:]

        response = requests.get(self.base_url + "/" + path, headers=self._headers(), timeout=60)
        self._check_for_errors(response)

        return self._response_data(response, return_raw_response)

    def post(self, path, data, return_raw_response=False) -> Any:
        """
        Send a POST request to the specified path with the given data as body.
        Expects the request data as a dictionary and also returns the response data as dictionary.
        If you want the full raw response, set the `return_raw_response` parameter to `True`.
        If you want to upload a file, use the upload_ephemerides or
        upload_maneuver_plan methods instead.
        If the response status is 4xx, it raises a ClientError;
        if the response status is 5xx, it raises a ServerError.
        """
        if path.startswith("/"):
            path = path[1:]

        response = requests.post(
            self.base_url + "/" + path, headers=self._headers(), json=data, timeout=30
        )
        self._check_for_errors(response)

        return self._response_data(response, return_raw_response)

    def patch(self, path, data, return_raw_response=False) -> Any:
        """
        Send a PATCH request to the specified path with the given data as body.
        Expects the request data as a dictionary and also returns the response data as dictionary.
        If you want the full raw response, set the `return_raw_response` parameter to `True`.
        If the response status is 4xx, it raises a ClientError;
        if the response status is 5xx, it raises a ServerError.
        """
        if path.startswith("/"):
            path = path[1:]

        response = requests.patch(
            self.base_url + "/" + path, headers=self._headers(), json=data, timeout=10
        )
        self._check_for_errors(response)

        return self._response_data(response, return_raw_response)

    def put(self, path, data, return_raw_response=False) -> Any:
        """
        Send a PUT request to the specified path with the given data as body.
        Expects the request data as a dictionary and also returns the response data as dictionary.
        If you want the full raw response, set the `return_raw_response` parameter to `True`.
        If the response status is 4xx, it raises a ClientError;
        if the response status is 5xx, it raises a ServerError.
        """
        if path.startswith("/"):
            path = path[1:]

        response = requests.put(
            self.base_url + "/" + path, headers=self._headers(), json=data, timeout=10
        )
        self._check_for_errors(response)

        return self._response_data(response, return_raw_response)

    def delete(self, path, return_raw_response=False) -> Any:
        """
        Send a DELETE request to the specified path.
        Returns the response data as dictionary.
        If you want the full raw response, set the `return_raw_response` parameter to `True`.
        If the response status is 4xx, it raises a ClientError;
        if the response status is 5xx, it raises a ServerError.
        """
        if path.startswith("/"):
            path = path[1:]

        response = requests.delete(self.base_url + "/" + path, headers=self._headers(), timeout=10)

        self._check_for_errors(response)

        return self._response_data(response, return_raw_response)

    def upload_ephemerides(self, datatype, dataformat, filepath, case_id=None):
        """
        Convenience method for uploading an ephemerides file, either in the
        context of a specific conjunction event (if a case_id is given),
        or independent of any event.
        Raises an exception if there was an error, otherwise returns the
        response data, which contains the document ID of the uploaded file.
        """
        url = (
            f"{self.base_url}/ephemerides"
            if case_id is None
            else f"{self.base_url}/cases/{case_id}/ephemerides"
        )
        response = requests.post(
            url,
            headers=self._headers_without_content_type(),
            files={"file": open(filepath, "rb")},
            data={"ccsds_type": datatype, "format": dataformat},
            timeout=60,
        )

        self._check_for_errors(response)

        return response.json()

    def upload_maneuver_plan(self, datatype, dataformat, filepath, name, case_id):
        """
        Convenience method for uploading a maneuver plan file in the
        context of a specific conjunction even.
        Raises an exception if there was an error, otherwise returns the
        response data, which contains the document ID of the uploaded file.
        """
        response = requests.post(
            f"{self.base_url}/cases/{case_id}/maneuvers",
            headers=self._headers_without_content_type(),
            files={"file": open(filepath, "rb")},
            data={"ccsds_type": datatype, "format": dataformat, "name": name},
            timeout=60,
        )

        self._check_for_errors(response)

        return response.json()

    def get_cdms(self, data_format: str, filters: Optional[dict] = None, latest=False) -> list:
        """
        Fetch CDMs.

        Returns a list of CDM documents in the specified format, or raises an error.

        :param str data_format: The format in which CDMs should be returned ('kvn', 'xml', or 'json').
        :param Optional[dict[str, Any]] filters: The filters that should be applied.
            Can have the following fields, which are all optional:
            {
                "originator": str,
                "object1_name": str,
                "object2_name": str,
                "object1_norad_id": int,
                "object2_norad_id": int,
                "object1_cospar_id": str,
                "object2_cospar_id": str,
                "operator2_name": str,
                "collision_probability": number | Comparison[number],
                "miss_distance": number | Comparison[number],
                "radial_distance": number | Comparison[number],
                "time_to_tca": str | Comparison[str] (with str being a duration like '1d12h'),
                "created_after": str (ISO timestamp, e.g. '2025-01-01T09:30Z')
            }
            Where Comparison[<type>] is a dictionary of the following form:
                {
                    "operator": str ('=', '<', '<=', '>', '>='),
                    "value": <type>
                }
        :param bool latest: Whether only the latest CDM matching the filters should be returned.
        """
        # Build query string for URL.
        query = f"format={data_format.lower()}"

        if filters is None:
            filters = {}

        # Add filters.
        if "originator" in filters:
            query = query + f"&originator={quote(filters['originator'])}"

        if "object1_name" in filters:
            query = query + f"&object1_name={quote(filters['object1_name'])}"
        if "object2_name" in filters:
            query = query + f"&object2_name={quote(filters['object2_name'])}"

        if "object1_norad_id" in filters:
            query = query + f"&object1_norad_id={filters['object1_norad_id']}"
        if "object2_norad_id" in filters:
            query = query + f"&object2_norad_id={filters['object2_norad_id']}"

        if "object1_cospar_id" in filters:
            query = query + f"&object1_cospar_id={filters['object1_cospar_id']}"
        if "object2_cospar_id" in filters:
            query = query + f"&object2_cospar_id={filters['object2_cospar_id']}"

        if "operator2_name" in filters:
            query = query + f"&operator2_name={quote(filters['operator2_name'])}"

        if "collision_probability" in filters:
            query = (
                query
                + "&"
                + self._numeric_comparison_filter_to_query_string(
                    "collision_probability", filters["collision_probability"]
                )
            )

        if "miss_distance" in filters:
            query = (
                query
                + "&"
                + self._numeric_comparison_filter_to_query_string(
                    "miss_distance", filters["miss_distance"]
                )
            )

        if "radial_distance" in filters:
            query = (
                query
                + "&"
                + self._numeric_comparison_filter_to_query_string(
                    "radial_distance", filters["radial_distance"]
                )
            )

        if "time_to_tca" in filters:
            query = (
                query
                + "&"
                + self._duration_comparison_filter_to_query_string(
                    "time_to_tca", filters["time_to_tca"]
                )
            )

        if "created_after" in filters:
            filters["created_after"] = sanitize_datetime(filters["created_after"])
            query = query + f"&created_after={quote(filters['created_after'])}"

        if latest:
            # Request will return only one CDM (the latest), so we don't need pagination.
            print("Fetching latest CDM...")
            return self._get_elements(f"cdms?{query}&latest=true")
        else:
            # In all other cases, we collect paginated results until there are no more.
            print("Fetching CDMs...", end="", flush=True)
            cdms: list[dict] = []
            page = 1
            has_more = True
            while has_more:
                print("...", sep="", end="", flush=True)
                more_cdms = self._get_elements(f"cdms?{query}&page={page}&limit=100")
                cdms = cdms + more_cdms
                has_more = len(more_cdms) > 0
                page += 1
            print("")
            print(f"Got {len(cdms)}")
            return cdms

    def get_ephemerides(self, format_: str, filters: Optional[dict] = None, latest=False) -> list:
        """
        Fetch ephemerides.

        Returns a list of OEM and OPM documents in the specified format, or raises an error.
        Note that this includes ephemerides of other operators only if they agreed to share data with you.

        :param str format_: The format in which CDMs should be returned ('kvn', 'xml', or 'json').
        :param Optional[dict[str, Any]] filters: The filters that should be applied.
            Can have the following fields, which are all optional:
            {
                "object_name": str,
                "object_id": str | number,
                "originator": str,
                "operational": bool,
                "uploaded_after": str (ISO timestamp, e.g. '2025-01-01T09:30Z')
            }
        :param bool latest: Whether only the latest OEM and OPM matching the filters should be returned.
        """
        # Build query string for URL.
        query = f"format={format_.lower()}"

        if filters is None:
            filters = {}

        # Add filters.
        if "object_name" in filters:
            query = query + f"&object_name={quote(filters['object_name'])}"
        if "object_id" in filters:
            query = query + f"&object_id={quote(filters['object_id'])}"
        if "originator" in filters:
            query = query + f"&originator={quote(filters['originator'])}"

        if "operational" in filters:
            query = query + f"&operational={str(filters['operational']).lower()}"

        if "uploaded_after" in filters:
            filters["uploaded_after"] = sanitize_datetime(filters["uploaded_after"])
            query = query + f"&uploaded_after={filters['uploaded_after']}"

        if latest:
            query = query + "&latest=true"

        return self._get_elements(f"ephemerides?{query}")

    def get_cases(
        self,
        include_uncritical: bool = False,
        only_upcoming: bool = True,
        object_name: Optional[str] = None,
        conjunction_partner: Optional[str] = None,
    ) -> list:
        """
        Fetch all open cases for the logged in organization.
        By default, only cases with TCA still in the future are fetched,
        and uncritical cases are filtered out.
        Returns a list of cases ordered by TCA (closest first),
        or raises an exception if something went wrong.
        """
        coordination_cases: list = []

        # Build query parameters.
        query_parameters = []
        # Filter for TCA in the future.
        if only_upcoming:
            now = sanitize_datetime(get_now_utc())
            query_parameters.append(f"newest_cdm.relative_metadata[tca][$gte]={now}")
        # Filter for criticality.
        criticality = "newest_risk_estimation.criticality=critical%2Cobserve"
        if include_uncritical:
            criticality += "%2Cnon_critical"
        query_parameters.append(criticality)
        # Filter for object name.
        if object_name is not None:
            query_parameters.append(f"q={quote(object_name)}")
        # Filter for conjunction partner.
        if conjunction_partner is not None:
            query_parameters.append(
                f"newest_cdm.object2_metadata[operator_organization]={quote(conjunction_partner)}"
            )

        page = 1
        more = True

        while more:
            parameters = "&".join(query_parameters + ["limit=100", f"page={page}"])
            response_data = self.get(f"cases?{parameters}")
            coordination_cases = coordination_cases + response_data["elements"]
            if "has_more" in response_data and response_data["has_more"]:
                page += 1
            else:
                more = False

        return coordination_cases

    def get_tickets(self, case_id) -> list:
        """
        Fetch all tickets for the logged in organization in a given case.
        Returns a list of tickets, or raises an exception if something went wrong.
        """
        return self._get_elements(f"cases/{case_id}/tickets")

    def get_notifications(self) -> list:
        """
        Fetch all notifications for the logged in organization.
        Returns a list of notifications, or raises an exception
        if something went wrong.
        """
        return self._get_elements(f"organizations/{self.organization_id}/notifications")

    def get_satellites(self) -> list:
        """
        Fetch all satellites of the logged in organization.
        Returns a list of satellite. If something goes wrong,
        the response is logged and an empty list is returned.
        """
        return self._get_elements("satellites")

    def get_protocols(
        self, protocol_type: Optional[str] = None, protocol_status: Optional[str] = None
    ) -> list:
        """
        Fetch all protocols availabe for the logged in organization,
        optionally filtering by type (baseline, global, bilateral) or
        status (active, inactive, draft).
        Returns a list of protocols, or raises an exception
        if something went wrong.
        """
        path = "protocols"
        if protocol_type is not None and protocol_status is not None:
            path = path + f"?type={protocol_type}&status={protocol_status}"
        elif protocol_type is not None:
            path = path + f"?type={protocol_type}"
        elif protocol_status is not None:
            path = path + f"?status={protocol_status}"

        return self._get_elements(path)

    def get_subscriptions(self) -> list:
        """
        Fetch all subscriptions of the logged in organization.
        Returns a list of subscriptions, or raises an exception
        if something went wrong.
        """
        return self._get_elements("subscriptions")

    def get_chats(self) -> list:
        """
        Fetch all chats of the currently set organization.
        Returns a list of chats. If something goes wrong,
        the response is logged and an empty list is returned.
        """
        return self._get_elements(f"organizations/{self.organization_id}/chats")

    def get_chat_messages(self, chat_id: str):
        """
        Fetch all chat messages of a given chat of the logged in organization.
        Returns a list of messages, or raises an exception if something went wrong.
        """
        return self._get_elements(f"organizations/{self.organization_id}/chats/{chat_id}/messages")

    def send_chat_message(self, case_id: str, message: str):
        """
        Send a chat message to your conjunction partner in a specific coordination case.
        """
        # Check whether a chat for the given case already exists.
        chat_id = None
        for chat in self._get_elements(f"organizations/{self.organization_id}/chats"):
            if chat["case_id"] == case_id:
                chat_id = chat["chat_id"]
                break

        if chat_id is not None:
            # If there is already a chat for the case, simply post a new message.
            response = self.post(
                f"organizations/{self.organization_id}/chats/{chat_id}/messages",
                {"text": message},
            )
            self._check_for_errors(response)
        else:
            # Otherwise create a new chat.
            response = self.post(
                f"organizations/{self.organization_id}/chats",
                {"case_id": case_id, "text": message},
            )
            self._check_for_errors(response)

    def set_up_satellite(self, satellite_definition: dict):
        """
        Creates or updates a satellite according to the given satellite definition.
        Returns the API response data.
        """
        satellite = satellite_definition.copy()

        satellite_id = None
        satellites = self.get_satellites()
        for existing_satellite in satellites:
            if "norad_id" in satellite and satellite["norad_id"] == existing_satellite["norad_id"]:
                satellite_id = existing_satellite["spacecraft_id"]
                break
            if (
                "cospar_id" in satellite
                and satellite["cospar_id"] == existing_satellite["cospar_id"]
            ):
                satellite_id = existing_satellite["spacecraft_id"]
                break
            if "name" in satellite and satellite["name"] == existing_satellite["name"]:
                satellite_id = existing_satellite["spacecraft_id"]
                break

        if satellite_id is not None:
            print(f"Satellite {satellite['name']} already exists, updating it...")
            del satellite["name"]
            del satellite["norad_id"]
            del satellite["cospar_id"]
            return self.patch(f"satellites/{satellite_id}", satellite)
        else:
            print(f"Creating satellite {satellite['name']}...")
            return self.post("satellites", satellite)

    def upload_satellites_from_csv(self, csv_filename: os.PathLike):
        """
        Creates or updates the satellites defined in the CSV.
        Returns a list with the responses for each satellite entry.
        """
        csv_path = Path(csv_filename)
        if not csv_path.exists():
            raise FileNotFoundError(f"{csv_path} does not exist.")

        responses = []

        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            for i, line in enumerate(csv_reader):
                dictline: dict[str, Any] = defaultdict(lambda: None)

                # remove empty fields so it takes Nones instead
                dictline.update(**{k: v for k, v in zip(header, line) if v != ""})

                sat = {
                    "name": dictline["name"],
                    "norad_id": parse_int(dictline["norad_id"]),
                    "cospar_id": dictline["cospar_id"],
                    "operator_name": dictline["operator_name"],
                    "operator_country_code": dictline["active"],
                    "active": parse_bool(dictline["active"]),
                    "size": dictline["size"],
                    "cross_section": parse_float(dictline["cross_section"]),
                    "hard_body_radius": parse_float(dictline["hard_body_radius"]),
                    "mass": parse_float(dictline["mass"]),
                    "dry_mass": parse_float(dictline["dry_mass"]),
                    "volume": parse_float(dictline["volume"]),
                    "launch_date": dictline["launch_date"],
                    "maneuverability": dictline["maneuverability"],
                    "mission_type": dictline["mission_type"],
                    "mission_phase": dictline["mission_phase"],
                    "is_part_of_constellation": parse_bool(dictline["is_part_of_constellation"]),
                    "constellation_size": parse_int(dictline["constellation_size"]),
                    "orbital_regime": dictline["orbital_regime"],
                    "orbit_category": dictline["orbit_category"],
                    "perigee": parse_float(dictline["perigee"]),
                    "apogee": parse_float(dictline["apogee"]),
                    "inclination": parse_float(dictline["inclination"]),
                    "semi_major_axis": parse_float(dictline["semi_major_axis"]),
                }

                # do not send the Nones, so it takes the default values in the API
                sat = {k: v for k, v in sat.items() if v is not None}

                print(f"Setting up satellite '{dictline['name']}' in line {i + 1}")
                responses.append(self.set_up_satellite(sat))

        return responses

    def delete_satellite(self, satellite_id: str):
        """
        Deletes the satellite with the given ID.
        Does not return anything.
        """
        self.delete(f"satellites/{satellite_id}", return_raw_response=True)

    def download_report(self, case_id: str, output_filepath: str):
        """
        Downloads the coordination case report as PDF
        and stores it in the given file path.
        """
        if not output_filepath.endswith(".pdf"):
            output_filepath += ".pdf"

        if Path(output_filepath).exists():
            timestamp = int(datetime.now().timestamp())
            output_filepath = output_filepath.replace(".pdf", f"-{timestamp}.pdf")

        response = self.get(f"cases/{case_id}/report", return_raw_response=True)
        with open(output_filepath, "wb") as f:
            f.write(response.content)

    def _api_base_url(self, instance: str) -> str:
        match instance:
            case "test":
                return "https://api-astrolabe-test.okapiorbits.com"
            case "staging":
                return "https://api-astrolabe-staging.okapiorbits.com"
            case "demo":
                return "https://api-astrolabe-demo.okapiorbits.com"
            case "production":
                return "https://api-astrolabe.okapiorbits.com"
            case _:
                raise SetupError("Unknown instance: " + instance)

    def _headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token,  # type: ignore
            "X-Organization-Id": self.organization_id,  # type: ignore
        }

    def _headers_without_content_type(self) -> dict:
        return {
            "Authorization": "Bearer " + self.access_token,  # type: ignore
            "X-Organization-Id": self.organization_id,  # type: ignore
        }

    def _get_elements(self, path) -> list:
        """
        For a list endpoint, fetch all elements of the response.
        Returns the list of elements. If something goes wrong,
        the response is logged and an empty list is returned.
        """
        response_data = self.get(path)
        if response_data is not None and "elements" in response_data:
            return response_data["elements"]
        else:
            print(f"Returning empty list because response data is: {response_data}")
            return []

    def _get_access_token_from_auth0(self) -> str:
        auth0_url = f"{os.getenv('ASTROLABE_AUTH0_DOMAIN')}/oauth/token"
        audience = os.getenv("ASTROLABE_AUTH0_AUDIENCE")
        username = os.getenv("ASTROLABE_AUTH0_USERNAME")
        password = os.getenv("ASTROLABE_AUTH0_PASSWORD")
        client_id = os.getenv("ASTROLABE_AUTH0_CLIENT_ID")

        headers = {"Content-type": "application/json"}
        body = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "audience": audience,
            "scope": "openid profile email offline_access",
            "client_id": client_id,
        }

        r = requests.post(auth0_url, headers=headers, data=json.dumps(body), timeout=4)

        if r.status_code == 200:
            response = r.json()
            return response["access_token"]
        else:
            raise AuthenticationError(f"Auth0 returned {str(r.status_code)} {r.json()}")

    def _check_for_errors(self, response: requests.Response):
        """
        Checks an HTTP response. If there was a client or server problem,
        it raises an according exception; in all other cases it does nothing.
        """
        status_code = response.status_code
        try:
            response_str = str(response.json())
        except requests.exceptions.JSONDecodeError:
            response_str = str(response)

        if 400 <= status_code < 500:
            raise ClientError(status_code, response_str)

        if 500 <= status_code < 600:
            raise ServerError(status_code, response_str)

    def _response_data(self, response: requests.Response, return_raw_response: bool):
        if return_raw_response:
            return response
        # Otherwise try to return the parsed response body, unless the response is empty.
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return None

    def _numeric_comparison_filter_to_query_string(self, key: str, comparison: Any) -> str:
        if isinstance(comparison, int) or isinstance(comparison, float):
            return f"{key}={comparison}"

        if "value" not in comparison:
            raise ClientError(400, "'value' is missing")

        if not isinstance(comparison["value"], int) and not isinstance(comparison["value"], float):
            raise ClientError(400, "'value' is not a number")

        operator = "="
        if "operator" in comparison:
            if comparison["operator"] not in ["=", "<", "<=", ">", ">="]:
                raise ClientError(400, f"Invalid operator: {comparison['operator']}")

            operator = comparison["operator"]

        if operator == "=":
            return f"{key}={comparison['value']}"

        operator_string = {"<": "$lt", "<=": "$lte", ">": "$gt", ">=": "$gte"}[operator]

        return f"{key}[{operator_string}]={comparison['value']}"

    def _duration_comparison_filter_to_query_string(self, key: str, comparison: Any) -> str:
        if isinstance(comparison, str):
            return f"{key}={comparison}"

        if "value" not in comparison:
            raise ClientError(400, "'value' is missing")

        operator = "="
        if "operator" in comparison:
            if comparison["operator"] not in ["=", "<", "<=", ">", ">="]:
                raise ClientError(400, f"Invalid operator: {comparison['operator']}")

            operator = comparison["operator"]

        if operator == "=":
            return f"{key}={comparison['value']}"

        operator_string = {"<": "$lt", "<=": "$lte", ">": "$gt", ">=": "$gte"}[operator]

        return f"{key}[{operator_string}]={comparison['value']}"
