class AsyncRequest():
    def __init__(
        self,
        client=None,
        method=None,
        params=None,
        payload=None,
        retries = False
        ):
        self.client = client
        self.method = method
        self.params = params
        self.payload = payload
        self.retries = retries
    
    def _buildReq(self):
        url = self.client.url
        id = self.client.id
        assert type(id) == int
        assert len(url) != 0
        