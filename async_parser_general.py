import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
from time import sleep
import random
import time
import string


def user_agent():
    '''
    Popular user agents, randomized
    :return: {'User-Agent':'some_agent'}
    '''
    headers = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
               'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               ]
    return {'User-Agent': headers[random.randrange(0, len(headers))]}


def find_pages_count(binary_page, url):
    '''
    Example method to find pages count
    :param binary_page: loaded html page in binary format
    :param url: It's URL
    :return: Url's to all pages
    '''
    soup = BeautifulSoup(binary_page, 'lxml')
    page_div = soup.body.findAll('td', {"onclick": "document.location=this.firstChild.href"})
    pages = [i.find('a').text for i in page_div]
    max_page = 0
    for j in pages:
        try:
            if max_page < int(j):
                max_page = int(j)
        except:
            pass
    all_pages = [url + '?p=' + str(i) for i in range(1, max_page)]
    return all_pages


def parse_single_page(page_binary):
    '''
    Example single page parse method
    :param page_binary:
    :return: URL's found in this page
    '''
    soup = BeautifulSoup(page_binary, 'lxml')
    picture_div = soup.body.findAll('div', {"class": "gdtm"})
    links = [i.find('a')['href'] for i in picture_div]
    return links


def save_file(file, name, path, file_format):
    '''
    Example method to save a file in binary
    :param file: File in binary
    :param name: Filename
    :param path: Folder to save the file in
    :param file_format: File format - like '.jpg' or '.png'
    :return: Path to saved file
    '''
    # print('Saving file '+name)
    if not os.path.exists(path):
        os.makedirs(path)
    f = open(os.path.join(path, name) + file_format, 'wb')
    f.write(file)
    f.close()
    return path


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    '''
    Random string generator
    :param size: size of generated string, default=6
    :param chars: Chars to include,default = ASCII uppercase + digits
    :return: Random string
    '''
    return ''.join(random.choice(chars) for _ in range(size))


@asyncio.coroutine
def load_page(url, max_time=7, max_retries=10):
    '''
    Example method for use with file you wish to save - e.g. images,audios,etc.
    :param url: URL of the object
    :param max_time: Maximum time for download
    :param max_retries: Maximum retry count
    :return: None if fails, path to saved file if succeeded
    '''
    start = time.time()
    success = False
    retries = 0
    print('Loading page at url\t' + url)
    while not success and not time.time() - start > max_time and not retries > max_retries:
        retries += 1
        try:
            with (yield from sem):
                response = yield from aiohttp.get(url, headers=user_agent())
                status = response.status
                if status == 200:
                    page = yield from response.read()
                    # name=id_generator(10) - generate name for the file
                    # saved_path=save_file(page,name,os.getcwd(),'.jpg') - we can also save the file here
                    success = True
                    print('Page with url\t' + url + '\n finished loading in ' +
                          "{0:.4f}".format(time.time() - start)
                          + ' seconds and with ' + str(retries - 1) + ' retries')
                    return page, url
                else:
                    sleep(0.01)
        except:
            sleep(0.01)
    return None


def load_all_pages(page_links, loop):
    '''
    Example method to load multiple pages
    :param page_links:
    :param loop: asyncio event loop
    :return:
    '''
    load_tasks = [load_page(d) for d in page_links]
    load_results = loop.run_until_complete(asyncio.gather(*load_tasks))
    return load_results


if __name__ == "__main__":
    sem = asyncio.Semaphore(5)  # Setup asycio semaphore

    loop = asyncio.get_event_loop()  # Get the event loop

    links = ['http://google.com', 'http://facebook.com']  # Example links

    pages = load_all_pages(links, loop)  # Get pages binaries

    # links_extra = [find_pages_count(page, url) for page, url in pages]  # Get all extra links
    # pages_extra = [loop.run_until_complete(  # Get all extra pages binaries
    #     asyncio.gather(
    #         *[load_page(url) for page, url in links_extra]
    #     )
    # )]

    paths = [save_file(page, url[url.rfind('/') + 1:] + '_' + id_generator(), os.getcwd(), '.html') for page, url in
             pages]  # Save all pages to files

    loop.close()  # Close the loop

    print('Finished, saved ' + str(len(paths)) + ' files')