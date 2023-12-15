from __future__ import annotations

from functools import cache

import requests
from lxml import html

# URL to scrape
main_url = 'https://www.poewiki.net/wiki/'
list_of_skill_gems_url = main_url + 'List_of_skill_gems'

# Dictionary of XPaths for skill gem names in different tables
xpaths = {
    'Red Skill Gems': '//*[@id="mw-content-text"]/div[1]/div[2]/table/tbody/tr[*]/td[1]/span/span/a/text()',
    'Green Skill Gems': '//*[@id="mw-content-text"]/div[1]/div[3]/table/tbody/tr[*]/td[1]/span/span/a/text()',
    'Blue Skill Gems': '//*[@id="mw-content-text"]/div[1]/div[4]/table/tbody/tr[*]/td[1]/span/span/a/text()'
}

# List to store all skill gem names
skill_gems = []


@cache
def get_parsed_tree(url):
    # Define a caching decorator for the function that fetches and parses the HTML content
    url_response = requests.get(url)
    if url_response.status_code == 200:
        return html.fromstring(url_response.content)

    print(f'Failed to retrieve the webpage. Status code: {url_response.status_code}')
    return None


# Iterate through each entry in the dictionary
for category, xpath in xpaths.items():
    # Use the cached function to get the parsed HTML tree
    tree = get_parsed_tree(list_of_skill_gems_url)

    if tree is not None:
        # Extract skill gem names using the current XPath and extend the list
        skill_gems.extend(tree.xpath(xpath))

# Print the list of all skill gem names
print('Skill Gems:', skill_gems)


# URL to scrape
for skill_gem in skill_gems:
    skill_gem_url = main_url + skill_gem

    # XPath for the desired main text
    skill_gem_description_xpath = '//*[@id="mw-content-text"]/div[1]/p[1]/span/span[1]/span[2]/span[3]/text()'

    # XPath for the desired titles (all <a> elements)
    skill_gem_tags_xpath = '//*[@id="mw-content-text"]/div[1]/p[1]/span/span[1]/span[2]/span[1]/a/text()'

    # XPath for additional text
    skill_gem_name_xpath = '//*[@id="mw-content-text"]/div[1]/p[1]/span/span[1]/span[1]/text()'

    # Send a GET request to the URL
    response = requests.get(skill_gem_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        tree = html.fromstring(response.content)

        # Extract the main text using XPath
        skill_gem_description = tree.xpath(skill_gem_description_xpath)

        # Extract all titles using XPath and store them in a list
        skill_gem_tags = tree.xpath(skill_gem_tags_xpath)

        # Extract additional text using XPath
        skill_gem_name = tree.xpath(skill_gem_name_xpath)

        # Print the extracted main text, titles, and additional text
        print('Skill Gem:', skill_gem_name)
        print('Skill Gem Tags:', skill_gem_tags)
        print('Skill Gem Description:', skill_gem_description)

    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
