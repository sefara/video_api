import json
import re

import requests


class RestClientException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RestClient:

    def __init__(
            self,
            api_url: str,
            soko_api_key: str
    ):
        if not api_url:
            raise RestClientException("api_url is required")
        if not soko_api_key:
            raise RestClientException("soko_api_key is required")

        # Check if the url and key are valid
        if not re.match(r"^(https?)://.+", api_url):
            raise RestClientException("Invalid URL")

        # Check if the key is a valid JWT
        if not re.match(
                r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$", soko_api_key
        ):
            raise RestClientException("Invalid API key")

        self.api_url = api_url
        self.soko_api_key = soko_api_key
        self.access_token = None
        self.user_api_key = None
        self.refresh_token = None
        self.current_user = None

        # options.headers.update(self._get_auth_headers())

        self.rest_url: str = f"{api_url}/rest/v1"
        self.auth_url: str = f"{api_url}/auth/v1"

    def raw_get(self, table,columns,query):

        res = requests.get("{}/{}?{}".format(self.rest_url, table, "select={"+columns+"}&"+query), headers={
            'apiKey': self.soko_api_key,
            "userApiKey": self.user_api_key,
            'Authorization': 'Bearer {}'.format(self.access_token if self.access_token else self.soko_api_key)
        })

        try:
            return res.json()
        except:
            return None

    def raw_post(self, table, payload):
        res = requests.post("{}/{}".format(self.rest_url, table), headers={
            'apiKey': self.soko_api_key,
            "userApiKey": self.user_api_key,
            'Authorization': 'Bearer {}'.format(self.access_token if self.access_token else self.soko_api_key)
        }, json=payload)

        try:
            return res.json()
        except:
            return None


    def raw_patch(self, table, query, payload):
        res = requests.patch("{}/{}?{}".format(self.rest_url, table, query), headers={
            'apiKey': self.soko_api_key,
            "userApiKey": self.user_api_key,
            'Authorization': 'Bearer {}'.format(self.access_token if self.access_token else self.soko_api_key)
        }, json=payload)
        print(res)
        try:
            return res.json()
        except:
            return None

    def get_current_user(self):
        api_key = self.get_api_key()
        if api_key:
            user = {
                **{k: v for k, v in api_key.get('user').items() if v is not None and k != "apiKey"},
                "apiKey": api_key
            }
            return user
        else:
            return None

    def get_api_key(self):
        API_KEY_QUERY = """
           *,
           user:users(
             *
           )
        """.replace("\n", "").replace(" ", "")

        headers = {
            'apiKey': self.soko_api_key
        }

        if self.user_api_key:
            headers['userApiKey'] = self.user_api_key
        elif self.access_token:
            headers['Authorization'] = 'Bearer {}'.format(self.access_token)

        res = requests.get(
            "{}/apiKeys?select={}".format(self.rest_url, API_KEY_QUERY), headers=headers)

        try:
            data = res.json()
            return data and data[0]
        except:
            return None

    def sign_up(
            self, email: str, password: str, data: dict
    ):
        signin_request = requests.post("{}/signup".format(self.auth_url), json={
            "email": email,
            "password": password,
            "data": data
        }, headers={
            'apiKey': self.soko_api_key
        })

        signin_response = None
        if signin_request.status_code == 200:
            signin_response = json.loads(signin_request.content)
        else:
            signin_response = json.loads(signin_request.content)

        return signin_response

    def sign_in_with_password(
            self, email: str, password: str
    ):
        login_request = requests.post("{}/token?grant_type=password".format(self.auth_url), json={
            "email": email,
            "password": password
        }, headers={
            'apiKey': self.soko_api_key,
            'Authorization': 'Bearer {}'.format(self.soko_api_key)
        })

        login_response = None
        if login_request.status_code == 200:
            login_response = json.loads(login_request.content)
            self.access_token = login_response.get('access_token')
            self.refresh_token = login_response.get('refresh_token')
            self.current_user = login_response.get('user')

        return login_response

    def sign_in_with_jwt(
            self, jwt: str
    ):
        user_request = requests.get("{}/user".format(self.auth_url), headers={
            'apiKey': self.soko_api_key,
            'Authorization': 'Bearer {}'.format(jwt)
        })

        user_response = None
        if user_request.status_code == 200:
            user_response = json.loads(user_request.content)
            self.access_token = jwt
            # one time login without refresh function
            # self.refresh_token = login_response.get('refresh_token')
            self.current_user = user_response

        return user_response

    def sign_in_with_api_key(
            self, api_key: str
    ):
        # use User Personal API KEY

        self.user_api_key = api_key

        user_response = None
        # if user_request.status_code == 200:
        #     user_response = json.loads(user_request.content)
        #     # self.access_token = jwt
        #     self.user_api_key = api_key
        #     self.current_user = user_response

        return user_response