import http.server
import logging
import threading
from tikplay.statics import USAGE
from tikplay import audio


# noinspection PyPep8Naming
class TikplayAPIHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.ap = audio.API()
        http.server.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        path_parts = self.path.split('/')
        if path_parts[1] == 'now_playing':
            self.send_response(200, 'Now playing: ' + self.ap.now_playing())

        elif path_parts[1] == 'queue':
            self.send_response(200, 'Queue: ' + self.ap.now_playing(10))

        elif len(path_parts) < 4:
            self.__get_else(path_parts)

        else:
            self.__error_state()

    def do_POST(self):
        if self.path == '/file':
            self.ap.store(self.rfile)

        else:
            self.__error_state()

    def __get_else(self, path_parts):
        target = path_parts[-1]
        correct_requests = ['song_hash', 'artist', 'title', 'length', 'filename']
        if path_parts[1] == 'find' and path_parts[2] in correct_requests:
            if self.ap.find(target, path_parts[2]):
                self.send_response(302)
            else:
                self.send_response(404)

        elif path_parts[1] == 'play' and path_parts[2] in correct_requests:
            if self.ap.play(target, path_parts[2]):
                self.send_response(200, 'Song is playing')
            else:
                self.send_response(201, 'Song is in the queue')

        else:
            self.__error_state()

    def __error_state(self):
        self.send_response(200, USAGE)


class Server():
    """ Wrapper for HTTPServer and TikplayAPIHandler """
    def __init__(self, host='', port=5000, server_class=http.server.HTTPServer, handler_class=TikplayAPIHandler):
        self.host = host
        self.port = port
        self.server_class = server_class
        self.handler_class = handler_class
        self.__server = self.server_class((self.host, self.port), self.handler_class)
        self.server_thread = threading.Thread(target=self.__server.serve_forever, daemon=True)
        self.logger = logging.getLogger('HTTPServer')

    def start(self):
        """ Start the server and thread """
        self.logger.log(logging.INFO, 'Starting the server')
        self.server_thread.start()

    def stop(self):
        """ Shutdown the server and thread """
        self.logger.log(logging.INFO, 'Stopping the server')
        if self.server_thread.isAlive():
            self.__server.shutdown()
            self.server_thread.join()
            self.logger.log(logging.INFO, 'Stopped')

        else:
            self.logger.log(logging.WARN, 'Already stopped, nothing to do')

    def restart(self):
        """ Unload all the dependencies and stuff from memory, reload and start again """
        # TODO
        pass
