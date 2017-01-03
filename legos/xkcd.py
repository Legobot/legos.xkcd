from Legobot.Lego import Lego
import requests
import re
import logging

logger = logging.getLogger(__name__)


class XKCD(Lego):
    def listening_for(self, message):
        return message['text'].split()[0] == '!xkcd'
        logger.debug('xkcd lego triggered')

    def handle(self, message):
        logger.debug('Handling message...')
        opts = self._handle_opts(message)
        # Set a default return_val in case we can't handle our crap
        return_val = '¯\_(ツ)_/¯'

        comic_id = self._parse_args(message)

        url = self._build_url(comic_id)

        logger.info('Retrieving URL: %s' % url)
        webpage = requests.get(url)
        if webpage.status_code == requests.codes.ok:
            return_val = self._parse_for_comic(webpage)
        else:
            logger.error('Requests encountered an error.')
            logger.error('HTTP GET response code: %s' % webpage.status_code)
            webpage.raise_for_status()

        self.reply(message, return_val, opts)

    def _parse_args(self, message):
        comic_id = None
        try:
            comic_id = message['text'].split()[1]
            logger.debug('Found an argument: %s' % str(id))
        except IndexError:
            comic_id = None
            logger.debug('No args provided. Setting "id" to None')
        logger.debug('_parse_args comic_id: %s' % comic_id)
        return comic_id

    def _handle_opts(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except IndexError:
            opts = None
            logger.error('Could not identify message source in message: %s'
                         % str(message))
        return opts

    def _build_url(self, comic_id):
        if comic_id is not None:
            if comic_id == 'r' or comic_id == 'random':
                logger.debug('Random comic requested...')
                url = 'http://dynamic.xkcd.com/random/comic'
            else:
                logger.debug('User requested comic by id: %s' % str(comic_id))
                url = 'http://xkcd.com/%s' % str(comic_id)
        else:
            url = 'http://xkcd.com/'
        return url

    def _parse_for_comic(self, r):
        content = r.text
        comic_regex = r'<div id="comic".*?\n?.*?(//im.+?)".+?\s?title="(.+?)"'
        comic = re.search(comic_regex, content)
        if comic:
            altText = comic.group(2).replace("&#39;", "'")
            response = "%s %s" % (altText, "http:" + comic.group(1))
        else:
            logger.error('Unable to find comic')
            response = "Unable to find a comic"
        return response

    def get_name(self):
        return 'xkcd'

    def get_help(self):
        return 'Fetch an xkcd. Usage: !xkcd [r|random|number]'
