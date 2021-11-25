"""Scan all link in webpage."""
import urllib.error
import urllib.request
import sys
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_links(url: str):
    """Find all links on page at the given url.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    link_url = []
    all_tag_a = driver.find_elements(By.TAG_NAME, "a")
    for link in all_tag_a:
        page_url = link.get_attribute('href')
        if(page_url is not None):
            if('#' in page_url):
                page_url = page_url.split('#')[0]
                link_url.append(page_url)
            elif('?' in page_url):
                page_url = page_url.split('?')[0]
                link_url.append(page_url)
    return link_url


def is_valid_url(url: str):
    """Check the link is valid and reachable or not.

    Returns:
        True if the URL is OK.
        False if otherwise or the URL has invalid syntax.
    """
    try:
        urllib.request.urlopen(url)
        return True
    except urllib.error.HTTPError as e:
        if(e.code == 403):
            return True
        else:
            return False


def invalid_urls(urllist: List[str]) -> List[str]:
    """Validate the urls in urllist.

    Returns:
        a new list containing the invalid or unreachable urls.
    """
    invalid_url = []
    for link in urllist:
        if is_valid_url(link) is False:
            invalid_url.append(link)
    return invalid_url


if __name__ == '__main__':
    try:
        url = sys.argv[1]
        list_link = get_links(url)
        invalid_link = invalid_urls(list_link)
        for url in list_link:
            print(url)
        print()
        print('Bad Links:')
        for bad_links in invalid_link:
            print(bad_links)
    except IndexError:
        print("Usage:  python3 link_scan.py url")
        print()
        print("Test all hyperlinks on the given url.")
