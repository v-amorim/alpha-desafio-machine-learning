from __future__ import annotations

import json
import os
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor

import console_colors as cc
import requests
from lxml import html
from tqdm import tqdm


class UI:
    @staticmethod
    def display_color_options(skill_gem_colors_dict):
        for key, value in skill_gem_colors_dict.items():
            print(f'{cc.blue_var(key)}: {value}')

    @staticmethod
    def get_user_choice(skill_gem_colors_dict):
        print('Enter the number corresponding to the desired skill gem color: ', end='')
        user_choice = cc.cyan_input()

        while user_choice not in skill_gem_colors_dict:
            print(f'{cc.yellow_warning()} Enter the number corresponding to the desired skill gem color: ', end='')
            user_choice = cc.cyan_input()

        return skill_gem_colors_dict[user_choice]


class SkillGemScraper:
    """Scrape skill gem details from Path of Exile wiki."""

    def __init__(self, selected_color: str = 'all') -> None:
        """Initialize the SkillGemScraper."""
        self.base_url: str = 'https://www.poewiki.net/wiki/'
        self.base_xpath: str = '//*[@id="mw-content-text"]/div[1]'
        self.skill_gems: list[str] = []
        self.selected_color: str = selected_color

    def _get_parsed_tree(self, url: str) -> html.HtmlElement | None:
        """Fetch and parse HTML content."""
        response = requests.get(url)
        if response.status_code == 200:
            return html.fromstring(response.content)

        print(f'{cc.red_error()} Failed to retrieve the webpage. Status code: {response.status_code}')
        return None

    def _scrape_skill_gem_names(self) -> None:
        """Scrape skill gem names from different categories."""
        category_xpaths: dict[str, str] = {
            'Red Skill Gems': f'{self.base_xpath}/div[2]/table/tbody/tr[*]/td[1]/span/span/a/text()',
            'Green Skill Gems': f'{self.base_xpath}/div[3]/table/tbody/tr[*]/td[1]/span/span/a/text()',
            'Blue Skill Gems': f'{self.base_xpath}/div[4]/table/tbody/tr[*]/td[1]/span/span/a/text()'
        }

        if self.selected_color == 'All Skill Gems':
            xpaths = category_xpaths.values()
        elif self.selected_color in category_xpaths:
            xpaths = [category_xpaths[self.selected_color]]
        else:
            raise ValueError(f'Invalid color: {self.selected_color}')

        for xpath in xpaths:
            tree = self._get_parsed_tree(self.base_url + 'List_of_skill_gems')
            if tree is not None:
                self.skill_gems.extend(tree.xpath(xpath))

    def _get_non_empty_xpath(self, tree, xpaths):
        for xpath in xpaths:
            result = tree.xpath(xpath)
            if result:
                return result
        return None

    def _scrape_skill_gem_info(self, skill_gem: str) -> dict[str, list[str]] | None:
        """Scrape info of a given skill gem."""
        skill_gem_url: str = self.base_url + skill_gem

        name_xpaths: list[str] = [
            f'{self.base_xpath}/div[1]/span/span[1]/text()',
            f'{self.base_xpath}/div[2]/span[1]/span[1]/text()',
            f'{self.base_xpath}/div[3]/span/span[1]/text()',
            f'{self.base_xpath}/div[3]/span[1]/span[1]/text()',
        ]

        tags_xpaths: list[str] = [
            f'{self.base_xpath}/div[1]/span/span[2]/span[1]/a/text()',
            f'{self.base_xpath}/div[2]/span[1]/span[2]/span[1]/a/text()',
            f'{self.base_xpath}/div[3]/span/span[2]/span[1]/a/text()',
            f'{self.base_xpath}/div[3]/span[1]/span[2]/span[1]/a/text()',
        ]

        description_xpaths: list[str] = [
            f'{self.base_xpath}/div[1]/span/span[2]/span[@class="group tc -gemdesc"]/text()',
            f'{self.base_xpath}/div[2]/span[1]/span[2]/span[@class="group tc -gemdesc"]/text()',
            f'{self.base_xpath}/div[3]/span/span[2]/span[@class="group tc -gemdesc"]/text()',
            f'{self.base_xpath}/div[3]/span[1]/span[2]/span[@class="group tc -gemdesc"]/text()',
        ]

        response = requests.get(skill_gem_url)

        if response.status_code == 200:
            tree = html.fromstring(response.content)
            skill_gem_name = self._get_non_empty_xpath(tree, name_xpaths)
            skill_gem_tags = self._get_non_empty_xpath(tree, tags_xpaths)
            skill_gem_description = self._get_non_empty_xpath(tree, description_xpaths)
            skill_gem_description = [desc.replace('\n', ' ') for desc in skill_gem_description]

            return {
                'Skill Gem': skill_gem_name,
                'Skill Gem Tags': skill_gem_tags,
                'Skill Gem Description': skill_gem_description
            }

        print(f'{cc.red_error()} Failed to retrieve the webpage. Status code: {response.status_code}')
        return None

    def scrape_skill_gems_info(self) -> list[dict[str, list[str]]]:
        """Scrape info of all skill gems using multithreading."""
        self._scrape_skill_gem_names()

        with ThreadPoolExecutor() as executor, tqdm(
                total=len(self.skill_gems), desc='Scraping', colour='green'
        ) as pbar:
            futures = {
                executor.submit(self._scrape_skill_gem_info, skill_gem): skill_gem for skill_gem in self.skill_gems}

            for _ in as_completed(futures):
                pbar.update(1)

            results: list[dict[str, list[str]] | None] = [future.result() for future in futures]

        # Filter out None results (failed requests)
        results = [result for result in results if result is not None]

        return results

    def format_skill_gem_details(self, skill_gem_details: list[dict[str, list[str]]]) -> str:
        """Format skill gem details for the desired output."""
        formatted_output = ''
        for skill_gem_detail in skill_gem_details:
            skill_gem_name = skill_gem_detail.get('Skill Gem', [''])[0]
            skill_gem_tags = ', '.join(skill_gem_detail.get('Skill Gem Tags', []))
            skill_gem_description = skill_gem_detail.get('Skill Gem Description', [''])[0]

            formatted_output += (
                f'Skill Gem: {skill_gem_name}; '
                f'Skill Gem Tags: {skill_gem_tags}; '
                f'Skill Gem Details: {skill_gem_description};\n'
            )

        return formatted_output


def main():
    skill_gem_colors_dict = {
        '1': 'Red Skill Gems',
        '2': 'Green Skill Gems',
        '3': 'Blue Skill Gems',
        '4': 'All Skill Gems'
    }

    UI.display_color_options(skill_gem_colors_dict)
    selected_color = UI.get_user_choice(skill_gem_colors_dict)

    scraper = SkillGemScraper(selected_color)
    skill_gem_info_raw = scraper.scrape_skill_gems_info()
    skill_gem_info_treated = scraper.format_skill_gem_details(skill_gem_info_raw)

    folder_name = 'skill_gem_data'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    raw_json_path = f'{folder_name}/skill_gem_info_raw.json'
    with open(raw_json_path, 'w', encoding='utf8') as json_file:
        raw_json = json.dumps(skill_gem_info_raw, indent=2)
        json_file.write(raw_json + '\n')
        print(f'{cc.green_done()} Raw data saved to {cc.blue_var(raw_json_path)}')

    treated_file_path = f'{folder_name}/skill_gem_info_treated.txt'
    with open(treated_file_path, 'w', encoding='utf8') as text_file:
        text_file.write(skill_gem_info_treated)
        print(f'{cc.green_done()} Formatted data saved to {cc.blue_var(treated_file_path)}')


if __name__ == '__main__':
    main()
