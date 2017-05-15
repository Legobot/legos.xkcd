from Legobot.Lego import Lego
import requests
import logging
import json
import random

logger = logging.getLogger(__name__)


class XKCD(Lego):
    def listening_for(self, message):
        if message['text'] is not None:
            try:
                return message['text'].split()[0] == '!xkcd'
            except Exception as e:
                logger.error('''XKCD lego failed to check message text:
                            {}'''.format(e))
                return False

    def handle(self, message):
        logger.debug('Handling message...')
        opts = self._handle_opts(message)
        # Set a default return_val in case we can't handle our crap
        return_val = '¯\_(ツ)_/¯'

        comic_id = self._parse_args(message)

        url = self._build_url(comic_id)

        logger.info('Retrieving URL: {}'.format(url))
        webpage = requests.get(url)
        if webpage.status_code == requests.codes.ok:
            return_val = self._parse_for_comic(webpage)
        else:
            logger.error('Requests encountered an error.')
            logger.error('''HTTP GET response code:
                        {}'''.format(webpage.status_code))
            webpage.raise_for_status()

        self.reply(message, return_val, opts)

    def _parse_args(self, message):
        comic_id = None
        try:
            comic_id = message['text'].split()[1]
            logger.debug('Found an argument: {}'.format(str(comic_id)))
        except IndexError:
            comic_id = None
            logger.debug('No args provided. Setting "comic_id" to None')
        logger.debug('_parse_args comic_id: {}'.format(comic_id))
        return comic_id

    def _handle_opts(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except IndexError:
            opts = None
            logger.error('''Could not identify message source in message:
                        {}'''.format(str(message)))
        return opts

    def _build_url(self, comic_id):
        if comic_id is not None:
            if comic_id == 'r' or comic_id == 'random':
                logger.debug('Random comic requested...')
                comic_id = self._get_random_comic_id()
            else:
                logger.debug('''User requested comic by id:
                            {}'''.format(str(comic_id)))
            url = 'http://xkcd.com/{}/info.0.json'.format(str(comic_id))
        else:
            url = 'http://xkcd.com/info.0.json'
        return url

    def _get_random_comic_id(self):
        latest = requests.get('http://xkcd.com/info.0.json')
        if latest.status_code == requests.codes.ok:
            latest_json = latest.text
            latest_json = json.loads(latest_json)
            comic_id = random.randint(1, latest_json['num'])  # nosec
        else:
            logger.error('Requests encountered an error.')
            logger.error('''HTTP GET response code:
                        {}'''.format(latest.status_code))
            latest.raise_for_status()
            comic_id = 1337
        return comic_id

    def _parse_for_comic(self, r):
        comic = json.loads(r.text)
        if comic:
            response = 'xkcd #{}: {} {}'.format(
                        comic['num'], comic['alt'], comic['img'])
        else:
            logger.error('Unable to find comic')
            response = 'Unable to find a comic'
        return response

    def get_name(self):
        return 'xkcd'

    def get_help(self):
        return 'Fetch an xkcd. Usage: !xkcd [r|random|number]'
