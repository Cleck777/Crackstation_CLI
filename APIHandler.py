import requests
from requests.exceptions import RequestException, ConnectionError, HTTPError
from urllib3.exceptions import InsecureRequestWarning

# Disable the insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class APIHandler:
    def __init__(self, base_url="https://localhost:443"):
        self.base_url = base_url
        self.session = requests.Session()  # Use session to maintain state, including headers
        self.csrf_token = self.pull_csrf_token()  # Pull CSRF token at initialization
        self.proxies = {
            'http': 'http://localhost:1337',
            'https': 'http://localhost:1337',
        }
        self.session.proxies.update(self.proxies)

    def pull_csrf_token(self):
        """ Pull the CSRF token using OPTIONS request and store it in the session headers """
        response = self.session.options(f"{self.base_url}/api/login", verify=False)
        response.raise_for_status()  # Check for HTTP errors
        # Extract CSRF token from cookies
        csrf_token = self.session.cookies.get('csrftoken', '')
        if csrf_token:
            # Update session headers to include the CSRF token for subsequent requests
            self.session.headers.update({
                'Referer': f"{self.base_url}/login"
            })
        return csrf_token
    def call_api(self, endpoint, method="GET", data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            print(f"URL: {url}")
            print(f"Method: {method}")
            print(f"Headers: {self.session.headers}")
            if data:
                print(f"Body: {data}")
            # Use the session object which contains the CSRF token in headers
            if method == "GET":
                response = self.session.get(url, params=params, verify=False)
            elif method == "POST":
                
                response = self.session.post(url, json=data, verify=False)
                
                

            elif method == "PUT":
                response = self.session.put(url, json=data, verify=False)
            elif method == "DELETE":
                response = self.session.delete(url, json=data, verify=False)
            elif method == "PATCH":
                response = self.session.patch(url, json=data, verify=False)
            elif method == "OPTIONS":
                response = self.session.options(url, verify=False)
            else:
                raise ValueError("Invalid HTTP method")

            response.raise_for_status()  # Check for HTTP errors
            return response.json()

        except HTTPError as e:
            return f"HTTP error occurred: {str(e)}"
        except ConnectionError as e:
            return f"Connection error occurred: {str(e)}"
        except RequestException as e:
            return f"Request error occurred: {str(e)}"
        except ValueError as e:
            return f"Error: {str(e)}"
        # Print response details
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        if response.text:
            print(f"Response Body: {response.text}")

        response.raise_for_status()  # Check for HTTP errors
        return response.json()


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
   # def pull_csrf_token(self):
    #    response = self.call_api("/api/login", "OPTIONS")
     #   csrf_token = response.headers['X-CSRF-Token']
    

    def task_template_operations(self, temp_id=None, data=None, method="GET"):
        if temp_id:
            return self.call_api(f"/api/tasks/templates/{temp_id}", method, data)
        return self.call_api("/api/tasks/templates", method, data)

    def task_operations(self, task_id=None, data=None, method="GET"):
        if task_id:
            return self.call_api(f"/api/tasks/{task_id}", method, data)
        return self.call_api("/api/tasks", method, data)
