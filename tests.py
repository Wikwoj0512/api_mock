try:
    from main import main
    import unittest
except Exception as e:
    print(e)

servers, apps = main()
app = apps[0]


class FlaskTest(unittest.TestCase):
    # check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/")
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/api/")
        self.assertEqual(response.content_type, "application/json")

    def test_all_endpoints(self):
        tester = app.test_client(self)
        endpoints = ["/api/", '/api/test1', "api/test2"]
        for endpoint in endpoints:
            response = tester.get(endpoint)
            self.assertEqual(200, response.status_code)

    def test_all_endpoints_content(self):
        tester = app.test_client(self)
        endpoints = ["/api/", '/api/test1', "api/test2"]
        for endpoint in endpoints:
            response = tester.get(endpoint)
            self.assertEqual("application/json", response.content_type)
