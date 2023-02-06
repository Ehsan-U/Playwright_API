from playwright.async_api import async_playwright
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
from urllib.parse import urlparse
import hashlib
import redis.asyncio as redis


class Request(BaseModel):
    url: str
    wait_until: str | None = None
    timeout: int | None = 30
    wait_for: int | None = None
    images_enabled: bool | None = True
    update_cache: bool | None = False



class Headless_Playwright():
    """ playwright via api """


    def __init__(self, url, wait_until, timeout, wait_for, images_enabled, update_cache):
        self.url = url
        self.wait_until = wait_until
        self.timeout = timeout
        self.wait_for = wait_for
        self.images_enabled = images_enabled
        self.update_cache = update_cache
        self.cache = redis.Redis(host='127.0.0.1', port='6379', db=0)


    async def cache_lookup(self, request):
        response_id = hashlib.md5(request.url.encode()).hexdigest()[:16]
        lookup_result = await self.cache.get(response_id)
        if self.update_cache is True:
            await self.cache.delete(response_id)
            return False
        elif lookup_result:
            return {'response': lookup_result}
        else:
            return False


    async def cache_dump(self, response):
        response_id = hashlib.md5(self.url.encode()).hexdigest()[:16]
        await self.cache.set(response_id, response, ex=86400)


    async def get_page(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            if not self.images_enabled:
                await page.route(f'**{urlparse(self.url).netloc}/*', lambda route: route.abort() if route.request.resource_type == 'image' else route.continue_())
            await page.goto(self.url)
            if self.wait_until:
                await page.wait_for_selector(self.wait_until, timeout=self.timeout)
            if self.wait_for:
                await page.wait_for_timeout(self.wait_for)
            content = await page.content()
            await context.close()
            await self.cache_dump(content)
            return content


    async def start_playing(self):
        try:
            content = await self.get_page()
        except Exception as e:
            response = {'error': e}
        else:
            response = {'response': content}
        return response
        

    @classmethod
    async def from_request(cls, request):
        url = request.url
        wait_until = request.wait_until
        timeout = request.timeout
        wait_for = request.wait_for
        images_enabled = request.images_enabled
        update_cache = request.update_cache
        return cls(url, wait_until, timeout, wait_for, images_enabled, update_cache)


app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.post("/")
async def root(request: Request):
    headless_play = await Headless_Playwright.from_request(request)
    response = await headless_play.cache_lookup(request)
    if response is False:
        response = await headless_play.start_playing()
    return response

