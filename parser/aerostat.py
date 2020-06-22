import os
import glob
import json
import datetime

from lxml import etree
from lxml.html import fromstring, tostring, HTMLParser
from lxml.etree import ParserError


class AerostatFolders():

    def __init__(self, folder_path=None):
        if not folder_path:
            self.folder_path = '/home/vera/work/aerostat/AEROSTATICA/aerostatica.ru/'
        else:
            self.folder_path = folder_path

    def get_all_files(self):
        return glob.glob('{}/20??/??/??/*/index.html'.format(self.folder_path))

    def parse_files(self):
        res = []
        for file in self.get_all_files():
            print(file)
            page = ParsePage(file)
            res.append(page.parse())
        return res


class ParsePage():

    def __init__(self, fpath=None):
        if not fpath:
            self.file_path = '/home/vera/work/aerostat/AEROSTATICA/aerostatica.ru/2019/04/28/728-beltain-flook-2019/index.html'
        else:
            self.file_path = fpath
        with open(self.file_path, 'rb') as f:
            self.soup = fromstring(f.read(), parser=HTMLParser(encoding='utf8'))

    def release_number(self):
        return self.soup.find_class('volume-link')[0].text_content()

    def release_date(self):
        dt_str = self.soup.findall('.//time')[0].attrib['datetime']
        # '2019-04-28T14:10:00+03:00'
        return dt_str.split('T')[0]

    def release_name(self):
        return self.soup.find_class('post-title')[0].text_content()

    def get_audio_url(self):
    #     http://aerostats.getmobileup.com/music/001.mp3
        number = self.release_number()
        return 'http://aerostats.getmobileup.com/music/{}.mp3'.format(number)

    def paragraphs(self):
        post = self.soup.find_class('post-content')[0]
        content = post.find_class("main-content-wrap")[0]
        res = []
        l = {'field_text': ''}
        for child in content.getchildren():
            if child.tag == 'p':
                l['field_text'] = l.get('field_text', '') + tostring(child, method='html', encoding='utf8').decode('utf8')
            elif child.tag == 'ul':
                res.append(l)
                # l = {}
                try:
                    l = {'field_name': child.findall(".//h4")[0].text_content()}
                except IndexError as e:
                    print(str(e))
                    pass
        res.append(l)
        return res

    def parse(self):
        return {
            'title': self.release_name(),
            'field_release_number': self.release_number(),
            'field_release_date': self.release_date(),
            'field_audio_file': self.get_audio_url(),
            'field_paragraphs': self.paragraphs()
        }


if __name__ == "__main__":
    release_page = ParsePage()
    import pdb;pdb.set_trace()
    res = release_page.parse()
    # for p in res:
    #     print('name: {}'.format(p.get('field_name', '')))
    #     print(p['field_text'])
    # with open('txt.txt', 'w') as f:
    #     f.write(json.dumps(res).decode('utf8'))