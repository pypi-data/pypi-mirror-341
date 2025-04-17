import re
import asyncio
import json
import logging
from typing import Dict, Generic, List, Optional, Type, TypeVar, Union

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

# from lmnr.sdk.laminar import Laminar
from pydantic import BaseModel

from browser_use.agent.views import ActionModel, ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.registry.service import Registry
from browser_use.dom.views import DOMElementNode, DOMTextNode
from browser_use.controller.views import (
	ClickElementAction,
	DoneAction,
	GoToUrlAction,
	InputTextAction,
	NoParamsAction,
	OpenTabAction,
	ScrollAction,
	SearchGoogleAction,
	SendKeysAction,
	SwitchTabAction,
)
from browser_use.utils import time_execution_sync

logger = logging.getLogger(__name__)


Context = TypeVar('Context')


class Controller(Generic[Context]):
	def __init__(
		self,
		exclude_actions: list[str] = [],
		output_model: Optional[Type[BaseModel]] = None,
	):
		self.registry = Registry[Context](exclude_actions)
		self.playwright_script: list[str] = []
		self.locator_generator = PlaywrightLocatorGenerator()

		"""Register all default browser actions"""

		if output_model is not None:
			# Create a new model that extends the output model with success parameter
			class ExtendedOutputModel(output_model):  # type: ignore
				success: bool = True

			@self.registry.action(
				'Complete task - with return text and if the task is finished (success=True) or not yet  completly finished (success=False), because last step is reached',
				param_model=ExtendedOutputModel,
			)
			async def done(params: ExtendedOutputModel):
				# Exclude success from the output JSON since it's an internal parameter
				output_dict = params.model_dump(exclude={'success'})
				return ActionResult(is_done=True, success=params.success, extracted_content=json.dumps(output_dict))
		else:

			@self.registry.action(
				'Complete task - with return text and if the task is finished (success=True) or not yet  completly finished (success=False), because last step is reached',
				param_model=DoneAction,
			)
			async def done(params: DoneAction):
				return ActionResult(is_done=True, success=params.success, extracted_content=params.text)

		# Basic Navigation Actions
		@self.registry.action(
			'Search the query in Google in the current tab, the query should be a search query like humans search in Google, concrete and not vague or super long. More the single most important items. ',
			param_model=SearchGoogleAction,
		)
		async def search_google(params: SearchGoogleAction, browser: BrowserContext):
			page = await browser.get_current_page()
			await page.goto(f'https://www.google.com/search?q={params.query}&udm=14')
			await page.wait_for_load_state()
			msg = f'🔍  Searched for "{params.query}" in Google'
			logger.info(msg)
			# Append Playwright commands to script
			self.playwright_script.append(f"await page.goto('https://www.google.com/search?q={params.query}&udm=14')")
			self.playwright_script.append("await page.wait_for_load_state()")
			return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action('Navigate to URL in the current tab', param_model=GoToUrlAction)
		async def go_to_url(params: GoToUrlAction, browser: BrowserContext):
			page = await browser.get_current_page()
			await page.goto(params.url)
			await page.wait_for_load_state()
			msg = f'🔗  Navigated to {params.url}'
			logger.info(msg)
			# Append Playwright commands to script
			self.playwright_script.append(f"await page.goto('{params.url}')")
			self.playwright_script.append("await page.wait_for_load_state()")
			return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action('Go back', param_model=NoParamsAction)
		async def go_back(_: NoParamsAction, browser: BrowserContext):
			await browser.go_back()
			msg = '🔙  Navigated back'
			logger.info(msg)
			# Append Playwright commands to script
			self.playwright_script.append("await page.go_back(timeout=10, wait_until='domcontentloaded')")
			return ActionResult(extracted_content=msg, include_in_memory=True)

		# wait for x seconds
		@self.registry.action('Wait for x seconds default 3')
		async def wait(seconds: int = 3):
			msg = f'🕒  Waiting for {seconds} seconds'
			logger.info(msg)
			await asyncio.sleep(seconds)
			# Append Playwright commands to script
			self.playwright_script.append(f"await page.wait_for_timeout({seconds * 1000})")
			return ActionResult(extracted_content=msg, include_in_memory=True)

		# Element Interaction Actions
		@self.registry.action('Click element', param_model=ClickElementAction)
		async def click_element(params: ClickElementAction, browser: BrowserContext):
			session = await browser.get_session()

			if params.index not in await browser.get_selector_map():
				raise Exception(f'Element with index {params.index} does not exist - retry or use alternative actions')

			element_node = await browser.get_dom_element_by_index(params.index)
			initial_pages = len(session.context.pages)
			simplified_locator = self.get_playwright_locator(element_node)
			# if element has file uploader then dont click
			if await browser.is_file_uploader(element_node):
				msg = f'Index {params.index} - has an element which opens file upload dialog. To upload files please use a specific function to upload files '
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)

			msg = None

			try:
				download_path = await browser._click_element_node(element_node)
				if download_path:
					msg = f'💾  Downloaded file to {download_path}'
				else:
					msg = f'🖱️  Clicked button with index {params.index}: {element_node.get_all_text_till_next_clickable_element(max_depth=2)}'

				logger.info(msg)
				logger.debug(f'Element xpath: {element_node.xpath}')
				if len(session.context.pages) > initial_pages:
					new_tab_msg = 'New tab opened - switching to it'
					msg += f' - {new_tab_msg}'
					logger.info(new_tab_msg)
					await browser.switch_to_tab(-1)
					# Append Playwright commands to script
					self.playwright_script.append(f"# Click element with index {params.index} (xpath: {element_node.xpath})")
					self.playwright_script.append(f"await page.{simplified_locator}.click()")
					self.playwright_script.append("# New tab opened - switching to it")
					self.playwright_script.append("page = context.pages[-1]")
				else:
					# Append Playwright commands to script
					self.playwright_script.append(f"# Click element with index {params.index} (xpath: {element_node.xpath})")
					self.playwright_script.append(f"await page.{simplified_locator}.click()")
				return ActionResult(extracted_content=msg, include_in_memory=True)
			except Exception as e:
				logger.warning(f'Element not clickable with index {params.index} - most likely the page changed')
				return ActionResult(error=str(e))

		@self.registry.action(
			'Input text into a input interactive element',
			param_model=InputTextAction,
		)
		async def input_text(params: InputTextAction, browser: BrowserContext, has_sensitive_data: bool = False):
			if params.index not in await browser.get_selector_map():
				raise Exception(f'Element index {params.index} does not exist - retry or use alternative actions')

			element_node = await browser.get_dom_element_by_index(params.index)
			simplified_locator = self.get_playwright_locator(element_node)
			await browser._input_text_element_node(element_node, params.text)
			if not has_sensitive_data:
				msg = f'⌨️  Input {params.text} into index {params.index}'
			else:
				msg = f'⌨️  Input sensitive data into index {params.index}'
			logger.info(msg)
			logger.debug(f'Element xpath: {element_node.xpath}')
			# Append Playwright commands to script
			self.playwright_script.append(f"# Input text into element with index {params.index} (xpath: {element_node.xpath})")
			self.playwright_script.append(f"await page.{simplified_locator}.fill('{params.text}')")
			return ActionResult(extracted_content=msg, include_in_memory=True)

		# Tab Management Actions
		@self.registry.action('Switch tab', param_model=SwitchTabAction)
		async def switch_tab(params: SwitchTabAction, browser: BrowserContext):
			await browser.switch_to_tab(params.page_id)
			# Wait for tab to be ready
			page = await browser.get_current_page()
			await page.wait_for_load_state()
			msg = f'🔄  Switched to tab {params.page_id}'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action('Open url in new tab', param_model=OpenTabAction)
		async def open_tab(params: OpenTabAction, browser: BrowserContext):
			await browser.create_new_tab(params.url)
			msg = f'🔗  Opened new tab with {params.url}'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		# Content Actions
		@self.registry.action(
			'Extract page content to retrieve specific information from the page, e.g. all company names, a specifc description, all information about, links with companies in structured format or simply links',
		)
		async def extract_content(goal: str, browser: BrowserContext, page_extraction_llm: BaseChatModel):
			page = await browser.get_current_page()
			import markdownify

			content = markdownify.markdownify(await page.content())

			prompt = 'Your task is to extract the content of the page. You will be given a page and a goal and you should extract all relevant information around this goal from the page. If the goal is vague, summarize the page. Respond in json format. Extraction goal: {goal}, Page: {page}'
			template = PromptTemplate(input_variables=['goal', 'page'], template=prompt)
			try:
				output = page_extraction_llm.invoke(template.format(goal=goal, page=content))
				msg = f'📄  Extracted from page\n: {output.content}\n'
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)
			except Exception as e:
				logger.debug(f'Error extracting content: {e}')
				msg = f'📄  Extracted from page\n: {content}\n'
				logger.info(msg)
				return ActionResult(extracted_content=msg)

		@self.registry.action(
			'Scroll down the page by pixel amount - if no amount is specified, scroll down one page',
			param_model=ScrollAction,
		)
		async def scroll_down(params: ScrollAction, browser: BrowserContext):
			page = await browser.get_current_page()
			if params.amount is not None:
				await page.evaluate(f'window.scrollBy(0, {params.amount});')
			else:
				await page.evaluate('window.scrollBy(0, window.innerHeight);')

			amount = f'{params.amount} pixels' if params.amount is not None else 'one page'
			msg = f'🔍  Scrolled down the page by {amount}'
			logger.info(msg)
			# Append Playwright commands to script
			if params.amount is not None:
				self.playwright_script.append(f"# Scroll down by {params.amount} pixels")
				self.playwright_script.append(f"await page.evaluate('window.scrollBy(0, {params.amount})')")
			else:
				self.playwright_script.append("# Scroll down by one page")
				self.playwright_script.append("await page.evaluate('window.scrollBy(0, window.innerHeight)')")
			return ActionResult(
				extracted_content=msg,
				include_in_memory=True,
			)

		# scroll up
		@self.registry.action(
			'Scroll up the page by pixel amount - if no amount is specified, scroll up one page',
			param_model=ScrollAction,
		)
		async def scroll_up(params: ScrollAction, browser: BrowserContext):
			page = await browser.get_current_page()
			if params.amount is not None:
				await page.evaluate(f'window.scrollBy(0, -{params.amount});')
			else:
				await page.evaluate('window.scrollBy(0, -window.innerHeight);')

			amount = f'{params.amount} pixels' if params.amount is not None else 'one page'
			msg = f'🔍  Scrolled up the page by {amount}'
			logger.info(msg)
			# Append Playwright commands to script
			if params.amount is not None:
				self.playwright_script.append(f"# Scroll up by {params.amount} pixels")
				self.playwright_script.append(f"await page.evaluate('window.scrollBy(0, -{params.amount})')")
			else:
				self.playwright_script.append("# Scroll up by one page")
				self.playwright_script.append("await page.evaluate('window.scrollBy(0, -window.innerHeight)')")
			return ActionResult(
				extracted_content=msg,
				include_in_memory=True,
			)

		# send keys
		@self.registry.action(
			'Send strings of special keys like Escape,Backspace, Insert, PageDown, Delete, Enter, Shortcuts such as `Control+o`, `Control+Shift+T` are supported as well. This gets used in keyboard.press. ',
			param_model=SendKeysAction,
		)
		async def send_keys(params: SendKeysAction, browser: BrowserContext):
			page = await browser.get_current_page()

			try:
				await page.keyboard.press(params.keys)
			except Exception as e:
				if 'Unknown key' in str(e):
					# loop over the keys and try to send each one
					for key in params.keys:
						try:
							await page.keyboard.press(key)
						except Exception as e:
							logger.debug(f'Error sending key {key}: {str(e)}')
							raise e
				else:
					raise e
			msg = f'⌨️  Sent keys: {params.keys}'
			logger.info(msg)
			# Append Playwright commands to script
			self.playwright_script.append(f"# Send keys: {params.keys}")
			self.playwright_script.append(f"await page.keyboard.press('{params.keys}')")
			return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action(
			description='If you dont find something which you want to interact with, scroll to it',
		)
		async def scroll_to_text(text: str, browser: BrowserContext):  # type: ignore
			page = await browser.get_current_page()
			try:
				# Try different locator strategies
				locators = [
					page.get_by_text(text, exact=False),
					page.locator(f'text={text}'),
					page.locator(f"//*[contains(text(), '{text}')]"),
				]

				for locator in locators:
					try:
						# First check if element exists and is visible
						if await locator.count() > 0 and await locator.first.is_visible():
							await locator.first.scroll_into_view_if_needed()
							await asyncio.sleep(0.5)  # Wait for scroll to complete
							msg = f'🔍  Scrolled to text: {text}'
							logger.info(msg)
							# Append Playwright commands to script
							self.playwright_script.append(f"# Scroll to text: {text}")
							self.playwright_script.append(f"await page.get_by_text('{text}', exact=False).scroll_into_view_if_needed()")
							self.playwright_script.append("await page.wait_for_timeout(500)")
							return ActionResult(extracted_content=msg, include_in_memory=True)
					except Exception as e:
						logger.debug(f'Locator attempt failed: {str(e)}')
						continue

				msg = f"Text '{text}' not found or not visible on page"
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)

			except Exception as e:
				msg = f"Failed to scroll to text '{text}': {str(e)}"
				logger.error(msg)
				return ActionResult(error=msg, include_in_memory=True)

		@self.registry.action(
			description='Get all options from a native dropdown',
		)
		async def get_dropdown_options(index: int, browser: BrowserContext) -> ActionResult:
			"""Get all options from a native dropdown"""
			page = await browser.get_current_page()
			selector_map = await browser.get_selector_map()
			dom_element = selector_map[index]

			try:
				# Frame-aware approach since we know it works
				all_options = []
				frame_index = 0

				for frame in page.frames:
					try:
						options = await frame.evaluate(
							"""
							(xpath) => {
								const select = document.evaluate(xpath, document, null,
									XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
								if (!select) return null;

								return {
									options: Array.from(select.options).map(opt => ({
										text: opt.text, //do not trim, because we are doing exact match in select_dropdown_option
										value: opt.value,
										index: opt.index
									})),
									id: select.id,
									name: select.name
								};
							}
						""",
							dom_element.xpath,
						)

						if options:
							logger.debug(f'Found dropdown in frame {frame_index}')
							logger.debug(f'Dropdown ID: {options["id"]}, Name: {options["name"]}')

							formatted_options = []
							for opt in options['options']:
								# encoding ensures AI uses the exact string in select_dropdown_option
								encoded_text = json.dumps(opt['text'])
								formatted_options.append(f'{opt["index"]}: text={encoded_text}')

							all_options.extend(formatted_options)

					except Exception as frame_e:
						logger.debug(f'Frame {frame_index} evaluation failed: {str(frame_e)}')

					frame_index += 1

				if all_options:
					msg = '\n'.join(all_options)
					msg += '\nUse the exact text string in select_dropdown_option'
					logger.info(msg)
					return ActionResult(extracted_content=msg, include_in_memory=True)
				else:
					msg = 'No options found in any frame for dropdown'
					logger.info(msg)
					return ActionResult(extracted_content=msg, include_in_memory=True)

			except Exception as e:
				logger.error(f'Failed to get dropdown options: {str(e)}')
				msg = f'Error getting options: {str(e)}'
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action(
			description='Select dropdown option for interactive element index by the text of the option you want to select',
		)
		async def select_dropdown_option(
			index: int,
			text: str,
			browser: BrowserContext,
		) -> ActionResult:
			"""Select dropdown option by the text of the option you want to select"""
			page = await browser.get_current_page()
			selector_map = await browser.get_selector_map()
			dom_element = selector_map[index]

			# Validate that we're working with a select element
			if dom_element.tag_name != 'select':
				logger.error(f'Element is not a select! Tag: {dom_element.tag_name}, Attributes: {dom_element.attributes}')
				msg = f'Cannot select option: Element with index {index} is a {dom_element.tag_name}, not a select'
				return ActionResult(extracted_content=msg, include_in_memory=True)

			logger.debug(f"Attempting to select '{text}' using xpath: {dom_element.xpath}")
			logger.debug(f'Element attributes: {dom_element.attributes}')
			logger.debug(f'Element tag: {dom_element.tag_name}')

			xpath = '//' + dom_element.xpath

			try:
				frame_index = 0
				for frame in page.frames:
					try:
						logger.debug(f'Trying frame {frame_index} URL: {frame.url}')

						# First verify we can find the dropdown in this frame
						find_dropdown_js = """
							(xpath) => {
								try {
									const select = document.evaluate(xpath, document, null,
										XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
									if (!select) return null;
									if (select.tagName.toLowerCase() !== 'select') {
										return {
											error: `Found element but it's a ${select.tagName}, not a SELECT`,
											found: false
										};
									}
									return {
										id: select.id,
										name: select.name,
										found: true,
										tagName: select.tagName,
										optionCount: select.options.length,
										currentValue: select.value,
										availableOptions: Array.from(select.options).map(o => o.text.trim())
									};
								} catch (e) {
									return {error: e.toString(), found: false};
								}
							}
						"""

						dropdown_info = await frame.evaluate(find_dropdown_js, dom_element.xpath)

						if dropdown_info:
							if not dropdown_info.get('found'):
								logger.error(f'Frame {frame_index} error: {dropdown_info.get("error")}')
								continue

							logger.debug(f'Found dropdown in frame {frame_index}: {dropdown_info}')

							# "label" because we are selecting by text
							# nth(0) to disable error thrown by strict mode
							# timeout=1000 because we are already waiting for all network events, therefore ideally we don't need to wait a lot here (default 30s)
							selected_option_values = (
								await frame.locator('//' + dom_element.xpath).nth(0).select_option(label=text, timeout=1000)
							)

							msg = f'selected option {text} with value {selected_option_values}'
							logger.info(msg + f' in frame {frame_index}')

							return ActionResult(extracted_content=msg, include_in_memory=True)

					except Exception as frame_e:
						logger.error(f'Frame {frame_index} attempt failed: {str(frame_e)}')
						logger.error(f'Frame type: {type(frame)}')
						logger.error(f'Frame URL: {frame.url}')

					frame_index += 1

				msg = f"Could not select option '{text}' in any frame"
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)

			except Exception as e:
				msg = f'Selection failed: {str(e)}'
				logger.error(msg)
				return ActionResult(error=msg, include_in_memory=True)

	# Register ---------------------------------------------------------------

	def action(self, description: str, **kwargs):
		"""Decorator for registering custom actions

		@param description: Describe the LLM what the function does (better description == better function calling)
		"""
		return self.registry.action(description, **kwargs)

	# Act --------------------------------------------------------------------

	@time_execution_sync('--act')
	async def act(
		self,
		action: ActionModel,
		browser_context: BrowserContext,
		#
		page_extraction_llm: Optional[BaseChatModel] = None,
		sensitive_data: Optional[Dict[str, str]] = None,
		available_file_paths: Optional[list[str]] = None,
		#
		context: Context | None = None,
	) -> ActionResult:
		"""Execute an action"""

		try:
			for action_name, params in action.model_dump(exclude_unset=True).items():
				if params is not None:
					# with Laminar.start_as_current_span(
					# 	name=action_name,
					# 	input={
					# 		'action': action_name,
					# 		'params': params,
					# 	},
					# 	span_type='TOOL',
					# ):
					result = await self.registry.execute_action(
						action_name,
						params,
						browser=browser_context,
						page_extraction_llm=page_extraction_llm,
						sensitive_data=sensitive_data,
						available_file_paths=available_file_paths,
						context=context,
					)

					# Laminar.set_span_output(result)

					if isinstance(result, str):
						return ActionResult(extracted_content=result)
					elif isinstance(result, ActionResult):
						return result
					elif result is None:
						return ActionResult()
					else:
						raise ValueError(f'Invalid action result type: {type(result)} of {result}')
			return ActionResult()
		except Exception as e:
			raise e
	
	def get_playwright_locator(self, node: DOMElementNode) -> str:
		attrs = node.attributes
		tag = node.tag_name.lower()
		text = node.get_all_text_till_next_clickable_element().strip()
		# split text by newline and keep only the first line
		text = text.split('\n')[0]

		# 1. Try role + name (most reliable)
		if "aria-label" in attrs:
			return f'get_by_role("{tag}", name="{attrs["aria-label"]}")'

		if tag == "button" and text:
			return f'get_by_role("button", name="{text}")'

		if tag == "a" and text:
			return f'get_by_role("link", name="{text}")'
		
		if tag == "img" and "alt" in attrs:
			return f'get_by_alt_text("{attrs["alt"]}")'

		if tag in ["input", "textarea"] and "placeholder" in attrs:
			return f'get_by_placeholder("{attrs["placeholder"]}")'

		if tag == "input" and attrs.get("type") == "search":
			return f'get_by_role("searchbox")'

		# 2. Use unique attributes (more reliable than XPath)
		if "id" in attrs:
			return f'locator("#{attrs["id"]}")'
		
		# check testId or test-id
		if "testId" in attrs:
			return f'locator(\'[data-testid="{attrs["testId"]}"]\')'
		
		if "test-id" in attrs:
			return f'locator(\'[data-testid="{attrs["test-id"]}"]\')'

		if "name" in attrs:
			name = attrs["name"]
			if '\n' in name:
				name = name.split('\n')[0].strip()
				return f'locator(\'[name*="{name}"]\')'  # Use "contains" match
			else:
				name = name.replace('"', '\\"')
				return f'locator(\'[name="{name}"]\')' # Exact match

		# 3. Use text content if unique and stable
		if text:
			return f'get_by_text("{text}", exact=False)'

		# 4. Use tag + type (less specific, but can be useful)
		if "type" in attrs:
			return f'locator(\'{tag}[type="{attrs["type"]}"]\')'

		# 5. Fallback to XPath (least reliable, use sparingly)
		return f'locator("xpath={node.xpath}")'

	def get_playwright_locator_experimental(self, node: DOMElementNode) -> str:
		# TODO: This needed changes in buildDomTree.js
		# When I made it, too many attributes were captured, leading to poor performance of browser-use
		# We can revisit this later
		return self.locator_generator.get_playwright_locator(node)
	
	async def get_playwright_codes(self):
		"""Get the playwright codes for the current playwright script"""
		return self.playwright_script

	async def save_playwright_script(self):
		"""Save the playwright script to a file"""
		script_content = [
			"import asyncio",
			"from playwright.async_api import async_playwright, expect",
			"",
			"async def run():",
			"    async with async_playwright() as p:",
			"        browser = await p.chromium.launch(headless=False)",
			"        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})",
			"        context = browser.contexts[0]",
			"",
			"        # Generated Playwright commands:",
			*[f"        {line}\n        await page.wait_for_timeout(1000)" for line in self.playwright_script],
			"",
			"        await browser.close()",
			"",
			"asyncio.run(run())"
		]
		
		with open('playwright_script.py', 'w') as f:
			f.write('\n'.join(script_content))

class PlaywrightLocatorGenerator:
	def get_playwright_locator(self, node: DOMElementNode) -> str:
		"""
		Generate the most reliable Playwright locator for a DOM element.
		Prioritizes accessibility, unique attributes, and visible text.
		"""
		tag = node.tag_name.lower()
		attrs = node.attributes

		# Get clean text content
		text = self._get_visible_text(node)

		# Check if this is an interactive element that should be selected differently
		if self._is_hidden(node):
			return self._get_fallback_locator(node)

		# ---------------------------
		# Priority 1: Test IDs (most stable across app changes)
		# ---------------------------
		test_id_result = self._get_test_id(node)
		if test_id_result:
			if len(test_id_result) == 2:
				attr_name, value = test_id_result
				return f'locator("[{attr_name}=\\"{self._escape_quotes(value)}\\"]")'
			else:
				attr_name, value, child_node = test_id_result
				tag = node.tag_name.lower()
				child_tag = child_node.tag_name.lower()
				return f'locator("{tag} > {child_tag}[{attr_name}=\\"{self._escape_quotes(value)}\\"]")'

		# ---------------------------
		# Priority 2: Accessibility attributes
		# ---------------------------
		a11y_locator = self._get_accessibility_locator(node, tag, attrs, text)
		if a11y_locator:
			return a11y_locator

		# ---------------------------
		# Priority 3: Unique stable attributes
		# ---------------------------
		if "id" in attrs and self._is_likely_stable_id(attrs["id"]):
			return f'locator("#{self._escape_quotes(attrs["id"])}")'

		if "name" in attrs and attrs["name"].strip():
			return f'locator("[name=\\"{self._escape_quotes(attrs["name"])}\\"]")'

		# ---------------------------
		# Priority 4: Text content locators
		# ---------------------------
		if text and len(text) <= 100 and not self._is_generic_text(text):
			# For short, non-generic text that isn't likely to change
			if tag in ["button", "a", "label", "h1", "h2", "h3", "h4", "th", "td"]:
				return f'get_by_text("{self._escape_quotes(text)}", exact=False)'

		# ---------------------------
		# Priority 5: CSS selectors with multiple attributes
		# ---------------------------
		# css_selector = self._build_css_selector(node)
		# if css_selector:
		# 	return f'locator("{self._escape_quotes(css_selector)}")'

		# ---------------------------
		# Priority 6: Structural locators (nth-child, etc.)
		# ---------------------------
		if node.xpath:
			# XPath as last resort since it's brittle to structure changes
			return f'locator("xpath={self._escape_quotes(node.xpath)}")'

		# Ultimate fallback
		return f'locator("{tag}")'

	def _escape_quotes(self, s: str) -> str:
		"""Escape quotes for string literals."""
		if not s:
			return ""
		return s.replace('"', '\\"').replace("'", "\\'")

	def _is_hidden(self, node: DOMElementNode) -> bool:
		"""Check if element is likely hidden."""
		attrs = node.attributes
		return (
			attrs.get("hidden") == "true" or
			attrs.get("aria-hidden") == "true" or
			"display:none" in attrs.get("style", "") or
			"visibility:hidden" in attrs.get("style", "")
		)

	def _get_test_id(self, node: DOMElementNode) -> Optional[tuple]:
		"""
		Extract test ID attributes which are stable across renders.
		Recursively checks children if the current node doesn't have test IDs.
		"""
		test_id_attrs = ["data-testid", "data-test-id", "data-test", "data-cy", "data-automation-id"]
		
		# First check the current node
		for key in node.attributes:
			key_lower = key.lower()
			if key_lower in test_id_attrs and node.attributes[key].strip():
				logger.info(f">>>> test id found on current node, {node.attributes[key]}")
				return (key, node.attributes[key])
		
		# If no test ID found on current node, recursively check children
		# Prioritize direct children first (breadth-first approach)
		for child in node.children:
			if isinstance(child, DOMElementNode):
				child_test_id = self._get_test_id_from_attrs(child.attributes)
				if child_test_id:
					# Return test ID from child with a more specific selector
					attr_name, value = child_test_id
					return (attr_name, value, child)
		
		# If still not found, do a deeper search
		for child in node.children:
			if isinstance(child, DOMElementNode) and child.children:
				deep_test_id = self._get_test_id(child)
				if deep_test_id:
					return deep_test_id
		
		return None

	def _get_test_id_from_attrs(self, attrs: Dict[str, str]) -> Optional[tuple]:
		"""Helper method to check attributes for test IDs."""
		test_id_attrs = ["data-testid", "data-test-id", "data-test", "data-cy", "data-automation-id"]
		for key in attrs:
			key_lower = key.lower()
			if key_lower in test_id_attrs and attrs[key].strip():
				return (key, attrs[key])
		return None


	def _is_likely_stable_id(self, id_value: str) -> bool:
		"""Check if ID appears to be stable, not dynamically generated."""
		if re.match(r'^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$', id_value, re.I):
			return False
		if re.match(r'^[0-9]+$', id_value):
			return False
		return True

	def _is_generic_text(self, text: str) -> bool:
		"""Check if text is too generic to be a reliable locator."""
		generic_terms = ["click", "submit", "cancel", "ok", "yes", "no", "button",
						"continue", "next", "previous", "back", "more"]
		return text.lower() in generic_terms

	def _get_accessibility_locator(self, node: DOMElementNode, tag: str, attrs: Dict[str, str], text: str) -> Optional[str]:
		"""Get locator based on accessibility attributes."""
		if "aria-label" in attrs and attrs["aria-label"].strip():
			aria_role = attrs.get("role") or self._get_implicit_role(tag)
			if aria_role:
				return f'get_by_role("{aria_role}", name="{self._escape_quotes(attrs["aria-label"])}")'
			return f'locator("[aria-label=\\"{self._escape_quotes(attrs["aria-label"])}\\"]")'

		if tag == "button":
			if text:
				return f'get_by_role("button", name="{self._escape_quotes(text)}")'
			if "title" in attrs:
				return f'get_by_role("button", name="{self._escape_quotes(attrs["title"])}")'

		if tag == "a" and text:
			return f'get_by_role("link", name="{self._escape_quotes(text)}")'

		if tag == "img" and "alt" in attrs and attrs["alt"].strip():
			return f'get_by_alt_text("{self._escape_quotes(attrs["alt"])}")'

		if tag in ["input", "textarea"]:
			input_type = attrs.get("type", "text").lower()
			if input_type == "checkbox":
				return f'get_by_role("checkbox")'
			elif input_type == "radio":
				label_text = self._find_associated_label_text(node)
				if label_text:
					return f'get_by_role("radio", name="{self._escape_quotes(label_text)}")'
			elif input_type == "search":
				return f'get_by_role("searchbox")'

			label_text = self._find_associated_label_text(node)
			if label_text:
				if tag == "input":
					role = self._get_input_role(input_type)
					return f'get_by_role("{role}", name="{self._escape_quotes(label_text)}")'
				return f'get_by_label("{self._escape_quotes(label_text)}")'

			if "placeholder" in attrs and attrs["placeholder"].strip():
				return f'get_by_placeholder("{self._escape_quotes(attrs["placeholder"])}")'

		if tag == "select":
			label_text = self._find_associated_label_text(node)
			if label_text:
				return f'get_by_role("combobox", name="{self._escape_quotes(label_text)}")'

		return None

	def _get_implicit_role(self, tag: str) -> Optional[str]:
		"""Map HTML elements to their implicit ARIA roles."""
		role_map = {
			"button": "button",
			"a": "link",
			"input": "textbox",
			"select": "combobox",
			"textarea": "textbox",
			"img": "img",
			"h1": "heading",
			"h2": "heading",
			"h3": "heading",
			"h4": "heading",
			"h5": "heading",
			"h6": "heading",
			"ul": "list",
			"ol": "list",
			"li": "listitem",
			"table": "table",
			"tr": "row",
			"td": "cell",
			"th": "columnheader",
		}
		return role_map.get(tag)

	def _get_input_role(self, input_type: str) -> str:
		"""Get the appropriate role for input elements based on type."""
		input_role_map = {
			"text": "textbox",
			"email": "textbox",
			"password": "textbox",
			"number": "spinbutton",
			"checkbox": "checkbox",
			"radio": "radio",
			"search": "searchbox",
			"submit": "button",
			"button": "button",
			"tel": "textbox",
			"url": "textbox",
			"date": "textbox",
			"time": "textbox",
			"file": "button"
		}
		return input_role_map.get(input_type, "textbox")

	def _find_associated_label_text(self, node: DOMElementNode) -> Optional[str]:
		return None

	def _build_css_selector(self, node: DOMElementNode) -> Optional[str]:
		"""Build a CSS selector combining multiple attributes for more specificity."""
		tag = node.tag_name.lower()
		attrs = node.attributes

		selector_parts = [tag]

		if "class" in attrs and self._is_stable_class(attrs["class"]):
			class_names = attrs["class"].split()
			for class_name in class_names:
				if class_name and not self._looks_like_dynamic_class(class_name):
					selector_parts.append(f".{class_name}")
					break

		for attr_name in ["type", "role", "name"]:
			if attr_name in attrs and attrs[attr_name].strip():
				selector_parts.append(f'[{attr_name}="{self._escape_quotes(attrs[attr_name])}"]')

		if len(selector_parts) > 1:
			return "".join(selector_parts)
		return None

	def _is_stable_class(self, class_str: str) -> bool:
		"""Check if class string contains stable (non-utility) classes."""
		if not class_str:
			return False

		utility_patterns = [
			r'^(mt|mb|ml|mr|pt|pb|pl|pr|m|p|text)-\d+$',
			r'^(d|bg|text|font|border|flex|grid|col|row)-',
		]

		classes = class_str.split()
		for cls in classes:
			if any(re.match(pattern, cls) for pattern in utility_patterns):
				continue
			if self._looks_like_dynamic_class(cls):
				continue
			return True
		return False

	def _looks_like_dynamic_class(self, class_name: str) -> bool:
		return (
			bool(re.match(r'^[a-z0-9]{8,}$', class_name)) or
			bool(re.match(r'^jsx-\d+$', class_name)) or
			bool(re.match(r'^v-[a-z0-9]+$', class_name)) or
			bool(re.match(r'^svelte-[a-z0-9]+$', class_name))
		)

	def _get_fallback_locator(self, node: DOMElementNode) -> str:
		if node.xpath:
			return f'locator("xpath={self._escape_quotes(node.xpath)}")'
		return f'locator("{node.tag_name.lower()}")'

	def _get_visible_text(self, node: DOMElementNode) -> str:
		all_text_nodes = self._collect_text_nodes(node)
		joined_text = " ".join(text for text in all_text_nodes if text.strip())
		normalized_text = re.sub(r'\s+', ' ', joined_text).strip()
		max_length = 100
		if len(normalized_text) <= max_length:
			return normalized_text
		truncate_point = normalized_text.rfind(' ', 0, max_length - 3)
		if truncate_point == -1:
			truncate_point = max_length - 3
		return normalized_text[:truncate_point] + "..."

	def _collect_text_nodes(self, node: Union[DOMElementNode, DOMTextNode]) -> List[str]:
		texts = []

		if isinstance(node, DOMTextNode):
			text = node.text.strip()
			if text:
				texts.append(text)
		elif isinstance(node, DOMElementNode):
			important_texts = self._extract_important_text(node)
			if important_texts:
				return important_texts
			for child in node.children:
				if isinstance(child, DOMTextNode):
					texts.extend(self._collect_text_nodes(child))

		return texts

	def _extract_important_text(self, node: DOMElementNode) -> List[str]:
		important_tags = ["h1", "h2", "h3", "h4", "strong", "b", "em", "label"]

		if node.tag_name.lower() in important_tags:
			texts = []
			for child in node.children:
				if isinstance(child, DOMTextNode):
					texts.extend(self._collect_text_nodes(child))
			return texts

		for child in node.children:
			if isinstance(child, DOMElementNode) and child.tag_name.lower() in important_tags:
				return self._collect_text_nodes(child)

		return []
