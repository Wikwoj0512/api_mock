import os
import random
import unittest

from main import get_servers
from models.models_file import AppConfiguration
from utils.tools import ReSearching


class FlaskTest(unittest.TestCase):
    config = AppConfiguration.fromFie(os.path.join(os.getcwd(), "config.yaml"))
    servers = get_servers(config)
    apps = [server.setup() for server in servers]

    def test_index(self):
        for app in self.apps:
            tester = app.test_client()
            response = tester.get("/api")
            statuscode = response.status_code
            self.assertEqual(200, statuscode)
            tester = self.apps[1].test_client()
            response = tester.get("/api")
            statuscode = response.status_code
            self.assertEqual(200, statuscode)

    def test_all_endpoints(self):
        for server, app in zip(self.servers, self.apps):
            tester = app.test_client()
            for endpoint in server.endpoints:
                for response in endpoint.responses:
                    route = server.endpoint_prefix + endpoint.endpoint
                    if response.method.value == "GET":
                        app_response = tester.get(route)
                    if response.method.value == "POST":
                        app_response = tester.post(route)
                    if response.method.value == "PUT":
                        app_response = tester.put(route)
                    if response.method.value == "DELETE":
                        app_response = tester.delete(route)

                    self.assertEqual(response.status_code.value, app_response.status_code)
                    self.assertEqual("application/json", app_response.content_type)

    def test_formatting(self):
        config = AppConfiguration.fromDict(
            {'mockoon_file': 'mockoon_files/format_test.json', 'flask_debug': False, 'logging_level': 'INFO',
             'host_addr': '0.0.0.0'})
        servers = get_servers(config)
        apps = [server.setup() for server in servers]
        app = apps[0]
        tester = app.test_client()
        response = tester.get("/api?name=jakiesimie")
        self.assertListEqual(sorted(["hostname", "ip", 'lang', "method", "queryParam", "urlparam"]),
                             sorted(list(eval(response.data).keys())))
        self.assertDictEqual({"hostname": "localhost", "ip": "127.0.0.1", "lang": "localhost", "method": "GET",
                              "queryParam": "jakiesimie", "urlparam": "api"}, eval(response.data))

    def test_var_value(self):
        config = AppConfiguration.fromDict(
            {'mockoon_file': 'mockoon_files/format_test.json', 'flask_debug': False, 'logging_level': 'INFO',
             'host_addr': '0.0.0.0'})
        servers = get_servers(config)
        apps = [server.setup() for server in servers]
        app = apps[0]
        tester = app.test_client()

        allowed_signs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
        for i in range(20):
            value = "".join(random.choices(allowed_signs, k=random.randint(3, 20)))
            print(value)
            response = tester.get(f"urlparam/{value}")
            dict = eval(response.data)
            self.assertEqual(value, dict["urlParam"])

    def test_re_searching_kwargs(self):
        test_cases_working = {"{{ip}}": "ip", "{{hostname      }}": "hostname"}
        for case in test_cases_working:
            self.assertEqual([(case, test_cases_working[case])], ReSearching.search_keywoards(case))
        test_cases_not_working = {"{ {method}}": "method", "hostname": ""}
        for case in test_cases_not_working:
            self.assertListEqual([], ReSearching.search_keywoards(case))

    def test_re_searching_params(self):
        test_cases_working = {"{{urlParam 'var'}}": ["urlParam", "'var'", ''],
                              "{{urlParam   'var'   'siema'}}": ["urlParam", "'var'", "'siema'"]}
        for case in test_cases_working:
            self.assertEqual(
                [(case, test_cases_working[case][0], test_cases_working[case][1], test_cases_working[case][2])],
                ReSearching.search_params(case))
        test_cases_not_working = ["{{urlParam ''var'}}", "method", "{{urlParam }}", "{ {urlParam ''var'}}"]
        for case in test_cases_not_working:
            self.assertListEqual([], ReSearching.search_params(case))

    def test_headers(self):
        config = AppConfiguration.fromDict(
            {'mockoon_file': 'mockoon_files/headers_test.json', 'flask_debug': False, 'logging_level': 'INFO',
             'host_addr': '0.0.0.0'})
        servers = get_servers(config)
        apps = [server.setup() for server in servers]
        app = apps[0]
        tester = app.test_client()
        response = tester.get('/')
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.headers["Accept-Language"], "en-en")
        self.assertEqual(response.headers["Connection"], "keep-alive")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
