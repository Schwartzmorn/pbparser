import json, time, logging
from http.error import HTTPHandlerError
from http.httphandler import DefaultHTTPHandler
from http.config import DEFAULT_TIMEOUT

LOGGER = logging.getLogger('rpcclient')
LOGGER.setLevel(logging.INFO)

class RPCClient(object):
    def __init__(self):
        self.session_id = 0
        self.http_handler = DefaultHTTPHandler()

    def request(self, method, arguments={}):
        query = json.dumps({'method': method, 'arguments': arguments})
        start = time.time()
        http_data = self._http_request(query)
        elapsed = time.time() - start
        LOGGER.info('http request took %.3f s' % (elapsed))
        LOGGER.info(http_data)
        return json.loads(http_data)

    def _http_request(self, query, timeout=None):  
        _session_id = 0
        headers = {'x-transmission-session-id': str(self.session_id)}
        result = '{}'
        request_count = 0

        if timeout == None:
            timeout = DEFAULT_TIMEOUT

        while True:
            try:
                LOGGER.info(json.dumps({
                    'url': self.http_handler.url, 'headers': headers, 
                    'query': query, 'timeout': timeout}, indent=2))
                result = self.http_handler.request(self.http_handler.url, query, headers, timeout)
                break
            except HTTPHandlerError as error:
                if error.code == 409:
                    LOGGER.info('Server responded with 409, trying to set session-id.')
                    if request_count > 1:
                        raise
                    self.session_id = None
                    for key in list(error.headers.keys()):
                        if key.lower() == 'x-transmission-session-id':
                            self.session_id = error.headers[key]
                            headers = {'x-transmission-session-id': str(self.session_id)}
                    if self.session_id is None:
                        raise
                else:
                    raise
        return result
