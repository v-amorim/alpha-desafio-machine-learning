from __future__ import annotations

import json
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor

import requests
from lxml import html
from tqdm import tqdm


class SkillGemScraper:
    """Scrape skill gem details from Path of Exile wiki."""

    def __init__(self) -> None:
        """Initialize the SkillGemScraper."""
        self.base_url: str = 'https://www.poewiki.net/wiki/'
        self.base_xpath: str = '//*[@id="mw-content-text"]/div[1]'
        self.skill_gems: list[str] = []

    def get_parsed_tree(self, url: str) -> html.HtmlElement | None:
        """Fetch and parse HTML content."""
        response = requests.get(url)
        if response.status_code == 200:
            return html.fromstring(response.content)

        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
        return None

    def scrape_skill_gem_names(self) -> None:
        """Scrape skill gem names from different categories."""
        category_xpaths: dict[str, str] = {
            'Red Skill Gems': f'{self.base_xpath}/div[2]/table/tbody/tr[*]/td[1]/span/span/a/text()',
            'Green Skill Gems': f'{self.base_xpath}/div[3]/table/tbody/tr[*]/td[1]/span/span/a/text()',
            'Blue Skill Gems': f'{self.base_xpath}/div[4]/table/tbody/tr[*]/td[1]/span/span/a/text()'
        }

        for xpath in category_xpaths.values():
            tree = self.get_parsed_tree(self.base_url + 'List_of_skill_gems')
            if tree is not None:
                self.skill_gems.extend(tree.xpath(xpath))

    def scrape_skill_gem_details(self, skill_gem: str) -> dict[str, list[str]] | None:
        """Scrape details for a given skill gem."""
        skill_gem_url: str = self.base_url + skill_gem
        name_xpath: str = f'{self.base_xpath}/p[1]/span/span[1]/span[1]/text()'
        tags_xpath: str = f'{self.base_xpath}/p[1]/span/span[1]/span[2]/span[1]/a/text()'
        description_xpath: str = f'{self.base_xpath}/p[1]/span/span[1]/span[2]/span[@class="group tc -gemdesc"]/text()'

        response = requests.get(skill_gem_url)

        if response.status_code == 200:
            tree = html.fromstring(response.content)
            description: list[str] = tree.xpath(description_xpath)
            tags: list[str] = tree.xpath(tags_xpath)
            name: list[str] = tree.xpath(name_xpath)

            return {
                'Skill Gem': name,
                'Skill Gem Tags': tags,
                'Skill Gem Description': description
            }

        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
        return None

    def scrape_all_skill_gem_details(self) -> list[dict[str, list[str]]]:
        """Scrape details for all skill gems using multithreading."""
        self.scrape_skill_gem_names()

        with ThreadPoolExecutor() as executor, tqdm(
                total=len(self.skill_gems), desc='Scraping'
        ) as pbar:
            futures = {
                executor.submit(self.scrape_skill_gem_details, skill_gem): skill_gem for skill_gem in self.skill_gems}

            for _ in as_completed(futures):
                pbar.update(1)

            results: list[dict[str, list[str]] | None] = [future.result() for future in futures]

        # Filter out None results (failed requests)
        results = [result for result in results if result is not None]

        return results


if __name__ == '__main__':
    # Create an instance of the class and perform the scraping
    scraper: SkillGemScraper = SkillGemScraper()
    skill_gem_details: list[dict[str, list[str]]] = scraper.scrape_all_skill_gem_details()

    # Convert the result to JSON
    result_json: str = json.dumps(skill_gem_details, indent=2)

    # Save the JSON to a file
    with open('skill_gem_details.json', 'w', encoding='utf8') as json_file:
        json_file.write(result_json + '\n')

    print("Scraping completed. Result saved to 'skill_gem_details.json'")
