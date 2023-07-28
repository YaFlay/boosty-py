import aiohttp
from utils import target
class API:
    URI = "https://api.boosty.to/v1"
    async def init(self, token: str, cookie: str, user: str):
        """Standart API class.

        Args:
            token (str): User`s token, getting from Authorization row in F11 Developer menu -> Network -> /api -> connect
            cookie (str): Like token, but a little below in row Cookie
        """
        self.bearer = token
        self.cookie = cookie
        self.header = {
            "Authorization": f"Bearer {token}"
        }
        self.user = user
        self.session = aiohttp.ClientSession(headers=self.header,cookie=self.cookie)  # creates session
        
        async with self.session.get(f"{self.URI}/ws/connect") as resp:  # gets token
            if resp.status == 200:
                self.token = await resp.json()["token"]
            else:
                raise Exception(
                    f"Error! API not worked... Status code: {resp.status}"
                )
    
    async def __get(self, url, *, to_json: bool = True, **args) -> dict | aiohttp.ClientResponse:
            async with self.session.get(f"{self.URI}{url}", kwargs=args) as resp:
                if resp.status == 200:
                    if to_json:
                        return await resp.json()
                    else:
                        return resp
                else:
                    raise aiohttp.ServerConnectionError(f"Error in __get function. Status: {resp.status}")

    async def __post(self, url, *, data, to_json: bool = True, **kwargs) -> dict | aiohttp.ClientResponse:
            async with self.session.post(f"{self.URI}{url}", data=data, kwargs=kwargs) as resp:
                if resp.status == 200:
                    if to_json:
                        return await resp.json()
                    else:
                        return resp
                else:
                    raise aiohttp.ServerConnectionError(f"Error in __get function. Status: {resp.status}")
    async def get_target(self, post_name: str) -> target.target | list[target.target]:
        """Return target on specific post or list of target

        Args:
            post_name (str): Name of post`s

        Returns:
            target.target | list[target.target]: target or targets to money or any
        """
        json = await self.__get(f"/target/{post_name}/?", to_json=True)
        if len(json.get("data")) == 0:
            return "Not Found"
        elif len(json.get("data")) == 1:
            return target.target(json.get("data"))
        else:
            target_list: list[target.target] = []
            for i in json.get("data"):
                target_list.append(target.target(i))
            return target_list
    
    async def get_post(self, post_id: str, post_author: str) -> dict:
        return await self.__get(f"/blog/{post_author}/post/{post_id}/")
    async def get_user(self, user: str) -> dict:
        """Get ur user

        Args:
            user (str): ur nickname 

        Returns:
            dict: all data with ur user
        """
        self.user = user
        return await self.__get(f"/blog/{user}")
    @property
    async def events(self) -> dict:
        """Return all events

        Returns:
            dict: dict with all events
        """
        return await self.__get(f"/notification/standalone/event/")