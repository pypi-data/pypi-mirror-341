"""
Core openemr rest api client functionality.
"""

import requests

from openemr import __version__

_USER_AGENT = "OpenEmrApiClientPython/%s" % __version__

scopes = [
    "openid",
    "offline_access",
    "api:oemr",
    "api:fhir",
    "api:port",
    "user/appointment.read",
    "user/facility.read",
    "user/patient.read",
    "user/practitioner.read",
    "user/Encounter.read",
    "user/Location.read",
]


class Client(object):
    """Performs requests to the OpenEmr rest API."""

    def __init__(
        self,
        username,
        password,
        base_url="https://localhost",
        client_scope=scopes,
        client_id=None,
        client_secret=None,
    ):
        """Base OpenEmr api client."""

        self.base_url = base_url
        self.client_scope = client_scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._login()

    def _login(self):
        """Log in to the OpenEMR API."""

        if "refresh_token" in self.__dict__:
            # Use refresh token to fetch new access token
            payload = {
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            }
        else:
            payload = {
                "grant_type": "password",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": self.username,
                "password": self.password,
                "scope": " ".join(self.client_scope),
                "user_role": "users",
            }

        print(f"Authenticating with {payload['grant_type']} grant type")

        self.session.headers.update(
            {
                "User-Agent": _USER_AGENT,
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

        token_response = self.session.post(
            url=self.base_url + "/oauth2/default/token", data=payload
        )

        self.access_token = token_response.json()["access_token"]
        self.refresh_token = token_response.json()["refresh_token"]

        self.session.headers.update(
            {
                "User-Agent": _USER_AGENT,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.access_token,
            }
        )

        self.api_url = f"{self.base_url}/apis/default/api"

        # test the connection
        try:
            self.api_version = self._get(self.api_url + "/version")
            print(
                f"Connected to OpenEMR API {self.base_url} version: {self.api_version}"
            )
        except Exception as e:
            if "refresh_token" in self.__dict__:
                print(
                    "Failed to connect to OpenEMR API, trying login without refresh token"
                )
                del self.refresh_token
                self._login()
            else:
                raise Exception("Failed to connect to OpenEMR API: " + str(e))

    def _post(self, url, payload=None):
        """Performs HTTP POST with credentials, returning the body as JSON."""

        response = self.session.post(url, data=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.post(url, data=payload)
        try:
            return response.json()
        except:
            return response.text

    def _post_json(self, url, payload=None):
        """Performs HTTP POST with credentials, returning the body as JSON."""

        response = self.session.post(url, json=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.post(url, json=payload)
        try:
            return response.json()
        except:
            return response.text

    def _put(self, url, payload=None):
        """Performs HTTP PUT with credentials, returning the body as JSON."""

        response = self.session.put(url, json=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.put(url, json=payload)
        try:
            return response.json()
        except:
            return response.text

    def _get(self, url, payload=None):
        """Performs HTTP GET with credentials, returning the body as JSON."""

        response = self.session.get(url)
        if response.status_code == 401:
            self._login()
            response = self.session.get(url)
        try:
            return response.json()
        except:
            return response.text

    def _patient(self, pid):
        """Patient info by id"""

        return self._get(self.api_url + "/patient/" + pid)

    def _patient_search(self, **kwargs):
        """lookup patients, if no search terms given returns all patients"""

        # might crash on too many search results, for reliable all patient search use get_patients()
        # use keyword arguments as search terms like lname fname dob etc.
        searchterms = ""
        if kwargs is not None:
            for key, value in kwargs.items():
                searchterms = searchterms + "&%s=%s" % (key, value)
        else:
            searchterms = ""

        return self._get(self.api_url + "/patient" + searchterms)

    def _appointment(self):
        """list al appointments"""

        return self._get(self.api_url + "/appointment")

    def _patient_encounter(self, pid):
        """Patient encounters"""

        return self._get(self.api_url + "/patient/" + pid + "/encounter")

    def _patient_appointment(self, pid):
        """List patient appointments"""

        return self._get(self.api_url + "/patient/" + pid + "/appointment")

    def _get_patient_document(self, pid):
        """Patient document by pid document id"""

        return self._get(self.api_url + "/patient/" + pid + "/document")

    def _patient_message(self, pid):
        """Get a patient message"""

        return self._get(self.api_url + "/patient/" + pid + "/message/1")

    def _new_patient(self, payload=None):
        """Create new patient"""

        # Check required fields
        try:
            city = payload["city"]
            country_code = payload["country_code"]
            dob = payload["dob"]
            ethnicity = payload["ethnicity"]
            fname = payload["fname"]
            lname = payload["lname"]
            mname = payload["mname"]
            phone_contact = payload["phone_contact"]
            postal_code = payload["postal_code"]
            race = payload["race"]
            sex = payload["sex"]
            state = payload["state"]
            street = payload["street"]
            title = payload["title"]
        except:
            print("not all fields are filled!")
            return None

        pid = str(int(self._patient_search()[-1]["pid"]) + 1)
        exists = self._patient(pid=pid)
        if exists:
            print(
                "The pid I suggested already exists, this is strange check openemr class."
            )
            return None

        # on success will return: {'pid': '5970'} use pid with newPid = class._new_patient(payload=payload)['pid']
        return self._post_json(self.api_url + "/patient", payload=payload)

    def get_patients(self) -> list:
        """Get all patients with pagination"""

        page_size = 200
        page = 0
        patients = []

        # page_size - 1 is used to make sure we get page size number of patients
        # otherwise emr returns one more patient
        result_data = self._get(self.api_url + "/patient" + f"?_limit={page_size - 1}")[
            "data"
        ]
        while result_data:
            patients.extend(result_data)
            page += 1
            result_data = self._get(
                self.api_url
                + "/patient"
                + f"?_limit={page_size - 1}&_offset={page * page_size}"
            )["data"]

        return patients
