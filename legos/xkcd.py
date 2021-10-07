import logging
import random
import re

from Legobot.Lego import Lego
import requests

logger = logging.getLogger(__name__)


class XKCD(Lego):
    def listening_for(self, message):
        text = message.get('text')

        if text and text.startswith('!xkcd'):
            return True

        return False

    def handle(self, message):
        text = message['text']
        logger.debug(f'Handling message:\n{text}')
        comic_id = self._get_comic_id(text)
        response = self._get_comic(comic_id)

        if response:
            opts = self.build_reply_opts(message)
            self.reply(message, response, opts)

    def _call_xkcd_api(self, comic_id=None):
        if comic_id:
            url = f'https://xkcd.com/{comic_id}/info.0.json'
        else:
            url = 'https://xkcd.com/info.0.json'

        call = requests.get(url)

        if call.status_code == 200:
            return call.json()
        else:
            logger.error(
                f'Error on GET {url}: {call.status_code}: {call.text}')

            return None

    def _get_comic(self, comic_id):
        response = None
        comic = self._call_xkcd_api(comic_id)

        if comic:
            response = 'xkcd #{}: {} {}'.format(
                comic['num'],
                comic['alt'],
                comic['img']
            )

        return response

    def _get_comic_id(self, text):
        comic_id = None
        params = re.split(r'\s+', text)

        if len(params) > 1:
            comic_id = params[1]

        if comic_id in ('r', 'random'):
            comic_id = self._get_random_comic_id()

        return comic_id

    def _get_random_comic_id(self):
        comic_id = 1337
        latest = self._call_xkcd_api()

        if latest:
            latest_id = latest['num']
            comic_id = random.randint(1, latest_id)  # nosec

        return comic_id

    def get_name(self):
        return 'xkcd'

    def get_help(self):
        return 'Fetch an xkcd. Usage: !xkcd [r|random|<int>]'
