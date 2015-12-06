import requests
from lxml import html as _html
import re
from pymplay.MusicPlayer import MusicPlayer
import io
import os
from downloadsdotnl.config import config
import urllib.request


class Searcher(object):

    def __init__(self):
        self.base_url = 'http://www.downloads-nl.com/results/mp3/{}/{}'
        self.s = requests.Session()
        self.player = MusicPlayer()

    
    def send_request(self, page, query):
        r = self.s.get(
            self.base_url.format(page, query),
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))' 
            },
            allow_redirects=True
        )

        return r

    
    def get_songs(self, page, query):
        doc = _html.fromstring(self.send_request(page, query).text)
        song_urls = doc.xpath(".//a[@class='tl j-lnk']/@href")
        files = []
        
        for url in song_urls:
            full_url = 'http://www.downloads-nl.com/{}&p=1'.format(url)
            
            r = self.s.get(
                full_url,
                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT \
                        9.0; en-US))' 
                },
                allow_redirects=True
            )
            
            try:
                m = re.search("'Play\'.'(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'", r.text).group(1)
                files.append(m)
            except AttributeError:
                pass

        for file in files:
            real_file = '{}/{}'.format(config['download']['dir'], os.path.basename(file))
            print('Saving: {}'.format(real_file))
            
            r = self.s.get(
                file,
                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT \
                        9.0; en-US))' 
                },
                allow_redirects=True,
                stream=True
            )

            with open(real_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)

            self.player.play_audio(real_file)
