from asyncio import Lock

from aiohttp import ClientSession, ClientResponse


class RemoteLogger(object):
    def __init__(self, base_url: str, token: str):
        self.base_url: str = base_url
        self.token: str = token
        self.session: ClientSession = None
        self.lock = Lock()

    async def login(self):
        self.session: ClientSession = ClientSession(headers=dict(Authorization=self.token))

    async def login_if_required(self):
        if self.session is None:
            async with self.lock:
                if self.session is None:
                    await  self.login()
        return self.session

    async def verify(self):
        await self.login_if_required()
        return await self.get('api/verify')

    async def log(self, template, **kwargs):
        await self.login_if_required()
        return await self.post(f'api/logs/{template}', data=kwargs)

    async def get(self, url):
        async with self.session.get(self.base_url + '/' + url + '/') as resp:
            resp: ClientResponse = resp
            resp.raise_for_status()
            return await resp.json()

    async def post(self, url, data):
        async with self.session.post(self.base_url + '/' + url + '/', data=data) as resp:
            resp: ClientResponse = resp
            resp.raise_for_status()
            return await resp.json()
