from playwright.async_api import async_playwright
from fastapi import FastAPI
from pydantic import BaseModel
import traceback
import uvicorn


class Request(BaseModel):
    url: str
    # str | None mean expected values, last None indicate default value 
    wait_until: str | None = None
    timeout: int | None = 30
    wait_for: int | None = None



class Headless_Playwright():
    """ playwright via api """


    def __init__(self, url, wait_until, timeout, wait_for):
        self.url = url
        self.wait_until = wait_until
        self.timeout = timeout
        self.wait_for = wait_for


    async def get_page(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(self.url)
            if self.wait_until:
                await page.wait_for_selector(self.wait_until, timeout=self.timeout)
            if self.wait_for:
                await page.wait_for_timeout(self.wait_for)
            content = await page.content()
            await context.close()
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
    async def from_api(cls, request):
        url = request.url
        wait_until = request.wait_until
        timeout = request.timeout
        wait_for = request.wait_for
        return cls(url, wait_until, timeout, wait_for)


app = FastAPI()

@app.post("/play/")
async def root(request: Request):
    headless_play = await Headless_Playwright.from_api(request)
    response = await headless_play.start_playing()
    return response


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=False,
        port=8000
    )