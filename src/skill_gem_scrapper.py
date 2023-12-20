from __future__ import annotations

import json
import os
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor

import console_colors as cc
import requests
from lxml import html
from tqdm import tqdm


class UserInterface:
    @staticmethod
    def display_color_options(skill_gem_colors):
        for key, value in skill_gem_colors.items():
            print(f'{cc.blue_var(key)}: {value}')

    @staticmethod
    def get_user_choice(skill_gem_colors):
        print('Enter the number corresponding to the desired skill gem color: ', end='')
        user_choice = cc.cyan_input()

        while user_choice not in skill_gem_colors:
            print(f'{cc.yellow_warning()} Enter the number corresponding to the desired skill gem color: ', end='')
            user_choice = cc.cyan_input()

        return skill_gem_colors[user_choice]


class SkillGemScraper:
    """Scrape skill gem details from Path of Exile wiki."""

    def __init__(self, skill_gem_color: str = 'all') -> None:
        """Initialize the SkillGemScraper."""
        self.base_url: str = 'https://www.poewiki.net/wiki/'
        self.base_xpath: str = '//*[@id="mw-content-text"]/div[1]'
        self.skill_gems: list[str] = []
        self.skill_gem_color: str = skill_gem_color

    def format_skill_gem_details(self, skill_gem_name, skill_gem_tags, skill_gem_description):
        formatted_tags = ', '.join(skill_gem_tags)
        formatted_description = '\n'.join(skill_gem_description)

        formatted_details = f'{skill_gem_name}:\n' \
                            f'Tags: {formatted_tags}.\n' \
                            f'Description: {formatted_description}'

        return formatted_details

    def get_parsed_tree(self, url: str) -> html.HtmlElement | None:
        """Fetch and parse HTML content."""
        response = requests.get(url)
        if response.status_code == 200:
            return html.fromstring(response.content)

        print(f'{cc.red_error()} Failed to retrieve the webpage. Status code: {response.status_code}')
        return None

    def scrape_skill_gem_names(self) -> None:
        """Scrape skill gem names from different categories."""
        category_xpaths: dict[str, str] = {
            'Red Skill Gems': f'{self.base_xpath}/div[2]/table/tbody/tr[*]/td[1]/span/span/a/text()',
            'Green Skill Gems': f'{self.base_xpath}/div[3]/table/tbody/tr[*]/td[1]/span/span/a/text()',
            'Blue Skill Gems': f'{self.base_xpath}/div[4]/table/tbody/tr[*]/td[1]/span/span/a/text()'
        }

        if self.skill_gem_color == 'All Skill Gems':
            xpaths = category_xpaths.values()
        elif self.skill_gem_color in category_xpaths:
            xpaths = [category_xpaths[self.skill_gem_color]]
        else:
            raise ValueError(f'Invalid color: {self.skill_gem_color}')

        for xpath in xpaths:
            tree = self.get_parsed_tree(self.base_url + 'List_of_skill_gems')
            if tree is not None:
                self.skill_gems.extend(tree.xpath(xpath))

    def get_non_empty_xpath(self, tree, xpaths):
        for xpath in xpaths:
            result = tree.xpath(xpath)
            if result:
                return result
        return None

    def scrape_skill_gem_details(self, skill_gem: str) -> dict[str, list[str]] | None:
        """Scrape details for a given skill gem."""
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
            skill_gem_name = self.get_non_empty_xpath(tree, name_xpaths)
            skill_gem_tags = self.get_non_empty_xpath(tree, tags_xpaths)
            skill_gem_description = self.get_non_empty_xpath(tree, description_xpaths)

            return {
                'Skill Gem': skill_gem_name,
                'Skill Gem Tags': skill_gem_tags,
                'Skill Gem Description': skill_gem_description
            }

        print(f'{cc.red_error()} Failed to retrieve the webpage. Status code: {response.status_code}')
        return None

    def scrape_all_skill_gem_details(self) -> list[dict[str, list[str]]]:
        """Scrape details for all skill gems using multithreading."""
        self.scrape_skill_gem_names()

        with ThreadPoolExecutor() as executor, tqdm(
                total=len(self.skill_gems), desc='Scraping', colour='green'
        ) as pbar:
            results = []

            for skill_gem in self.skill_gems:
                result = self.scrape_skill_gem_details(skill_gem)
                if result:
                    formatted_details = self.format_skill_gem_details(
                        result['Skill Gem'][0],
                        result['Skill Gem Tags'],
                        result['Skill Gem Description']
                    )
                    results.append(formatted_details)
                pbar.update(1)

        return results


def main():
    skill_gem_colors = {
        '1': 'Red Skill Gems',
        '2': 'Green Skill Gems',
        '3': 'Blue Skill Gems',
        '4': 'All Skill Gems'
    }

    UserInterface.display_color_options(skill_gem_colors)
    selected_color = UserInterface.get_user_choice(skill_gem_colors)

    scraper = SkillGemScraper(skill_gem_color=selected_color)
    skill_gem_details = scraper.scrape_all_skill_gem_details()

    result_folder_name = 'skill_gem_data'
    result_json_path = f'{result_folder_name}/skill_gem_details.json'

    # Check if the folder exists, and create it if not
    if not os.path.exists(result_folder_name):
        os.makedirs(result_folder_name)

    with open(result_json_path, 'w', encoding='utf8') as json_file:
        json.dump(skill_gem_details, json_file, indent=2)

    print(f'{cc.green_done()} Scraping completed. Result saved to {cc.blue_var(result_json_path)}')


if __name__ == '__main__':
    main()
