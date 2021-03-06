from http import rpcclient
import webapp2, logging
import json, traceback

RPC_CLIENT = rpcclient.RPCClient()

class PBProxy (webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        res = None
        try:
            method = self.request.get("method")
            args = self.request.get("args")
            url = self.request.get("url")
            user = self.request.get("user")
            password = self.request.get("password")
            if url and user and password:
                RPC_CLIENT.http_handler.set_authentication(url, user, password)
                logging.info("Using request's authentication.")
            logging.info(method)
            logging.info(args)
            res = RPC_CLIENT.request(method, json.loads(args))
        except:
            logging.info("### Invalid Args ###")
            logging.info(traceback.format_exc())
        self.response.write(json.dumps(res))