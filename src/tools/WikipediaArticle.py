import requests
import json
import re
from bs4 import BeautifulSoup


class WikipediaArticle:
    sections_to_remove = ["See also", "Notes and references", "Further reading", "External links", "References", "Bibliography"]

    def __init__(self, url):
        self.url = url
        self.title = ""
        self.summary = []
        self.sections = {}

        self.get_page()

    def save(self):
        self.sections["title"] = self.title

        with open(f'./data/{self.title}.json', 'w') as fp:
            json.dump(self.sections, fp)

    def get_page(self):
        # with open('./data/mockHtml.html') as fp:
        #     soup = BeautifulSoup(fp, 'html.parser')
        #     body = soup.find("div", {"id": "mockBody"})
        # To test on mock data comment out the following 3 lines and replace with the above 3 lines
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser').select('body')[0]
        body = soup.find("div", {"id": "mw-content-text"})

        # Set the title
        self.title = soup.find(id="firstHeading").text

        # Set the summary of the article and remove these summary 'p' tags
        # removing the first item after
        body = self.set_summary_and_body(body.find_all())

        # start_idx = 1 because there is a 'meta' tag at the beginning when find_all() is called
        start_idx = 1
        header = body[start_idx].text.replace("[edit]", '')
        header_type = int(body[start_idx].name.replace('h', ''))
        current_section = {header: {"text": []}}

        # Extract the data into the 'sections' dict recursively
        self.sections = self.extract_data(body, current_section, header, header_type, start_idx)

        # Remove redundant sections at the footer of the page
        self.remove_footer_sections()

    def set_summary_and_body(self, body):
        header_pattern = re.compile(r'^h[1-6]$')
        i = 0

        for tag in body:
            if tag.name == 'p':
                self.summary.append(tag.text)

            if header_pattern.match(tag.name):
                # Subtract by 1 to ensure this header tag is not accidentally skipped
                return body[i-1:]

            i += 1

    def extract_data(self, body, current_section, current_header, current_header_type, start):
        header_pattern = re.compile(r'^h[1-6]$')

        # Use of while loop so tags can be skipped when they have been added to 'sections' within inner recursion calls
        i = start
        while i < len(body):
            tag_name = body[i].name
            tag_text = body[i].text.replace("[edit]", '')

            # Check whether the current tag is a header using regex
            if header_pattern.match(tag_name):

                # The tag is a header, lets find out what type of header it is
                next_header_type = int(tag_name.replace('h', ''))

                # If the header type of the next section is the same as the current section we have been inspecting,
                # then continue adding sections to 'current_section'
                if next_header_type == current_header_type:
                    current_section[tag_text] = {'text': []}
                    current_header = tag_text

                # If the next header is a subtitle of the current header, then we want to create a new sub section
                # inside current_section and recursively follow the same procedure
                elif next_header_type > current_header_type:
                    current_section[current_header][tag_text] = {"text": []}

                    # parse 'i' and return 'i' so we can keep track of which tags have been added to 'sections' dict
                    new_section, i = self.extract_data(body, {}, tag_text, next_header_type, i)
                    current_section[current_header].update(new_section)

                # If the next header is a subtitle that is not a subtitle of the current section we are in,
                # and it isn't even the same type of title type, then we are entering a new section.
                # This means we want to save the current sub section and start the recursive loop for this new section
                elif next_header_type < current_header_type:

                    # we parse back i-1 becuase we don't want to skip this header, we want to add this header to
                    # 'sections' when we exit this recursive call
                    return current_section, i-1

            # if we are inspecting a 'p' tag, then we want to simply add the text inside it to the current section
            elif tag_name == 'p':
                current_section[current_header]["text"].append(tag_text)

            i += 1

        # End of recursion return, also avoids the i leaking from this function as we don't need it outside of here
        return current_section

    def remove_footer_sections(self):
        for section in self.sections_to_remove:
            if section in self.sections.keys():
                del self.sections[section]
