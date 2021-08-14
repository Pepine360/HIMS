import requests

class Test:
    @classmethod
    def testGet(self):
        pass
        # data = requests.get("127.0.0.1:5000/api/v1/getProduct")

    @classmethod
    def testPost(self, payload):
        data = requests.post("http://127.0.0.1:5000/api/v1/createProduct", data=payload)
        return data.json()

    @classmethod
    def testPut(self):
        pass

    @classmethod
    def testDelete(self):
        pass
