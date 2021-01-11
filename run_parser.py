from bs4 import BeautifulSoup
import requests
import re
from google_trans_new import google_translator
from db import Session, Apartments


session = Session()


class Logic:
    def __init__(self, appt_blocks):
        self.translator = google_translator()
        self.appt_blocks = appt_blocks

    def translation_data(self, data, lang='en'):
        return self.translator.translate(data, lang_tgt=lang)

    def block_price(self):
        return self.appt_blocks.find('span',
                                     {'class':
                                      'blue font-24 block bold price'
                                      })

    def block_location(self):
        return self.appt_blocks.find_all(
            'a', {'class': 'blue medium'})

    def block_description(self):
        return self.appt_blocks.find_all(
            'span', {'class': 'blue medium'})

    def block_note(self):
        return self.appt_blocks.find_all(
            'span', {'class': 'medium'})

    def block_name(self):
        return self.appt_blocks.find(
            'a', {'class': 'bold font-16 block'})

    def get_price(self, rate=28):
        div = self.block_price()
        if not div:
            return None
        price = re.sub(r'\D', '', div.get_text())
        if price:
            return float(price) / rate
        else:
            None

    def get_district(self):
        try:
            district = str(self.block_location()[0].get_text())
            # Translate
            district = self.translation_data(district)
            return district
        except IndexError:
            return None

    def get_rooms(self):
        try:
            rooms = re.sub(r'\D', '', self.block_location()[1].get_text())
            if rooms:
                return float(rooms)
            else:
                return None
        except IndexError:
            return None

    def get_floor(self):
        try:
            floor = re.sub(r'\D', '', self.block_description()[3].get_text())
            if floor:
                return float(floor)
            else:
                return None
        except IndexError:
            return None

    def get_floors(self):
        try:
            floors = re.sub(r'\D', '', self.block_description()[4].get_text())
            if floors:
                return float(floors)
            else:
                return None
        except IndexError:
            return None

    def get_area(self):
        try:
            area = re.sub(r'\D', '', self.block_description()[5].get_text())
            if area:
                return float(area)
            else:
                return area
        except IndexError:
            return None

    def get_type(self):
        try:
            type_app = str(self.block_description()[6].get_text())
            type_app = self.translation_data(type_app)
            return type_app
        except IndexError:
            return None

    def get_cond(self):
        try:
            cond = str(self.block_description()[7].get_text())
            return cond
        except IndexError:
            return None

    def get_walls(self):
        try:
            walls = str(self.block_description()[8].get_text())
            walls = self.translation_data(walls)
            return walls
        except IndexError:
            return None

    def get_desc(self):
        try:
            desc = str(self.block_note()[9].get_text())
            desc = self.translation_data(desc)
            return desc
        except IndexError:
            return None

    def get_name(self):
        try:
            name = str(' '.join(self.block_name().get_text().split()))
            name = self.translation_data(name)
            return name
        except IndexError:
            return None


def scrape_block(apt_block, rules):
    '''
    define a function which will extract the
    targeted elements from an appatrment block list
    '''

    apt_data = {}
    apt_data['price'] = rules.get_price(rate=28)
    apt_data['district'] = rules.get_district()
    apt_data['rooms'] = rules.get_rooms()
    apt_data['floor'] = rules.get_floor()
    apt_data['floors'] = rules.get_floors()
    apt_data['area'] = rules.get_area()
    apt_data['type'] = rules.get_type()
    apt_data['cond'] = rules.get_cond()
    apt_data['walls'] = rules.get_walls()
    apt_data['desc'] = rules.get_desc()
    apt_data['name'] = rules.get_name()

    # Get Note
    return apt_data


def scrape_apt_page(appt_blocks):
    '''
    function to scrape all appartment blocks within a single search result page
    '''
    page_apt_data = []
    num_blocks = len(appt_blocks)

    for i in range(num_blocks):
        define_rules = Logic(appt_blocks=appt_blocks[i])
        page_apt_data.append(scrape_block(appt_blocks[i], define_rules))

    return page_apt_data


def scrape_this(link, t_count):
    '''
    function to iterate the above function through all
    pages of the search result untill we scrape data for
    the targeted number of appartments
    '''

    base_url = link
    remaining_acount = t_count
    new_page_number = 1
    apt_data = []

    while remaining_acount > 0:
        url = base_url + str(new_page_number)
        source = requests.get(url).text
        r = requests.get(url)
        if r.status_code != 200:
            return apt_data
        source = r.text
        soup = BeautifulSoup(source, 'html.parser')
        appt_blocks = soup.findAll('div', {'class': 'col-md-4'})
        apt_data.extend(scrape_apt_page(appt_blocks))
        new_page_number = new_page_number+1
        remaining_acount = remaining_acount-1
    return apt_data


if __name__ == '__main__':
    base_scraping_link = "https://alexander-n.com/kvartiri?page="
    top_pages = 1  # "How many pages do you want to scrape?"
    apts = scrape_this(base_scraping_link, int(top_pages))

    for i in apts:
        add_data = Apartments(
            Price=i['price'],
            District=i['district'],
            Rooms=i['rooms'],
            Floor=i['floor'],
            Floors=i['floors'],
            Area=i['area'],
            Type=i['type'],
            Walls=i['walls'],
            Desc=i['desc'],
            Name=i['name'],
        )
        session.add(add_data)
    session.commit()
