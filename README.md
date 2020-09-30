# Simple-asyncio-Python-parser {It is amazing!}
Simple parser I've written to practice in async 3.5 Python code. This can be used for simple tasks like downloading a specific set of images, or a static html website.
#Requirements
Python 3.5

aiohttp 0.21.2


beautifulsoup4 4.4.1




#Examples
In the code are:
 - most popular user-agents to bypass some simple filtering, with usage like

 ```python
 aiohttp.get(url, headers=user_agent())
 ```
 - page count find example with BeautifulSoup4
 - link extracting from a page with BS4
 - Binary file saving
 - Random string generator
 - Async page loading
 - List of links async page loading
The code is fully functional right after downloading, all functions are commented, the hardest thing to understand in the code is list comprehension.

If my code helped you, I'm pleased :)
