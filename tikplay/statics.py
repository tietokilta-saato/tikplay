USAGE = """This stinking pile of duct-tape offers a RESTful API.
           Usage is the following:
               GET /find/song_hash/<song_hash>
               GET /find/filename/<filename>
               GET /find/title/<title>
               GET /find/artist/<artist>
               GET /find/length/<length>
               GET /now_playing
               GET /play/<"song_hash"|"filename">/<song_hash|filename>
               POST /file
        """


INTERNAL_ERROR = """Internal error occured! Please contact an administrator, or
                    if you are one, please consult the server logs for more information.
                    
                    If this isn't the first time this error occurs, please
                    consider submitting an issue ticket to:
                    https://github.com/tietokilta-saato/tikplay/issues
                 """
