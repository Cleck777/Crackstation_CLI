import requests
from requests.exceptions import RequestException, ConnectionError, HTTPError

from urllib3.exceptions import InsecureRequestWarning
import requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class APIHandler:
    def __init__(self, base_url="https://192.168.56.101:443"):
        self.base_url = base_url

    def call_api(self, endpoint, method="GET", data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            # Choose the request method based on the 'method' parameter
            if method == "GET":
                response = requests.get(url, params=params, verify=False)
            elif method == "POST":
                print(data)
                response = requests.post(url, json=data, verify=False)
            elif method == "PUT":
                response = requests.put(url, json=data, verify=False)
            elif method == "DELETE":
                response = requests.delete(url, json=data, verify=False)
            elif method == "PATCH":
                response = requests.patch(url, json=data, verify=False)
            else:
                raise ValueError("Invalid HTTP method")

            # Check for HTTP errors
            response.raise_for_status()
            return response.json()

        except HTTPError as e:
            return f"HTTP error occurred: {str(e)}"
        except ConnectionError as e:
            return f"Connection error occurred: {str(e)}"
        except RequestException as e:
            return f"Request error occurred: {str(e)}"
        except ValueError as e:
            return f"Error: {str(e)}"


    def admin_operations(self, user_id=None, data=None, method="GET"):
        if user_id:
            return self.call_api(f"/api/admin/{user_id}", method, data)
        return self.call_api("/api/admin/", method, data)

    def profile_operations(self, data=None, method="GET"):
        return self.call_api("/api/profile/", method, data)

    def benchmark_operations(self, data=None, method="GET"):
        return self.call_api("/api/benchmark/", method, data)

    def authentication_operations(self, operation, data=None, method="POST"):
        operations = {
            "login": "/api/login",
            "sso": "/api/sso",
            "logout": "/api/logout"
        }
        return self.call_api(operations[operation], method, data)

    def option_operations(self):
        return self.call_api("/api/options", "GET")

    def queuing_operations(self, job_id, data=None, method="GET"):
        return self.call_api(f"/api/queuing/{job_id}", method, data)

    def report_operations(self, data=None, method="GET"):
        return self.call_api("/api/reports", method, data)

    def task_template_operations(self, temp_id=None, data=None, method="GET"):
        if temp_id:
            return self.call_api(f"/api/tasks/templates/{temp_id}", method, data)
        return self.call_api("/api/tasks/templates", method, data)

    def task_operations(self, task_id=None, data=None, method="GET"):
        if task_id:
            return self.call_api(f"/api/tasks/{task_id}", method, data)
        return self.call_api("/api/tasks", method, data)
