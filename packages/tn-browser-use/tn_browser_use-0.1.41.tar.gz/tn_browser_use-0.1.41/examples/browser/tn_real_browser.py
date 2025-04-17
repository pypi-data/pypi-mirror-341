import os
import sys
from pathlib import Path

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

browser = Browser(
	config=BrowserConfig(
		# NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
		# chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		disable_security=False,
	)
)

def get_llm(model: str = 'gemini'):
	if model == 'gemini':
		return ChatGoogleGenerativeAI(model='gemini-2.0-flash')
	
	if model == 'openai':
		return ChatOpenAI(model='gpt-4o')
	else:
		raise ValueError(f'Invalid model: {model}')

async def main():
	agent = Agent(
		# task='Go to flipkart.com and search for iphone 15, and click on the first product listed',
		task="Go to styleseat.com/m and click on braids product card. choose location as san francisco",
		llm=get_llm(),
		browser=browser,
	)

	await agent.run()
	await browser.close()

	playwright_codes = await agent.controller.get_playwright_codes()
	print("Playwright codes: ", playwright_codes)
	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
