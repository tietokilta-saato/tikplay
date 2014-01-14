tikplay
=======

New implementation of tikplay. Legacy software contained in the LEGACY directory.

Requirements
============

Apart from what is listed in `requirements.txt` (can be installed with pip), libmp3lame is also required for youtube-dl

Architecture
============

## Client to Server architecture and API

```
+--------+                    +------------------+
| Client |<-HTTP RESTful API->|      Server      |
+--------+                    +~~~~~~~~~~~~~~~~~~+
                              | HTTP API Handler |
                              +------------------+
                              - GET
                                - /now_playing
                                - /queue
                                - /find
                                    - /song_hash
                                    - /filename
                                    - /artist
                                    - /title
                                    - /length
                                - /play
                                    - /song_hash
                             - POST
                                - /file
```

## Server to Audio architecture and Audio API

```
+------------------+           +-------+
| HTTP API Handler |<--------->| Audio |
+------------------+ Control   +~~~~~~~+
                     the music | API   |
                     flow      +-------+
                               - find(keyword, column)
                               - play(song_hash)
                               - store(filepointer)
                               - now_playing(queue_length=1)
```

## Audio architecture

```
                              +-------------+  +=============+
       +----Songcache-------->| PySoundFile |--| HDD Storage |
       |                      +-------------+  +=============+
       |
+------+----+                   +-----------+  +~~~~~~~~~~~~+
| Audio API |<--External Data-->| Retriever |--| Retrievers |
+------+----+                   +-----------+  +~~~~~~~~~~~~+
  ^    |
  |    |                      +-------------+  +===========+
  |    +----Play songs------->| PySoundCard |--| Soundcard |
  |                           +-------------+  +===========+
  |
  |                    +--------------------+
  +------------------->| Database Interface |
   \                   +--------------------+
    Change and store   - add_song_metadata(song_hash,
    song metadata                          filename,
                                           artist=None,
                                           title=None,
                                           length=None,
                                           play_count=1,
                                           date_added=datetime.now(),
                                           last_played=datetime.now())
                       - increment_play_count(song_hash)
                       - set_last_played(song_hash, date=datetime.now())
                       - get_song_metadata(song_hash)
                       - get_song_hashes_by_filename(filename)
                       - get_song_hashes_by_artist(artist)
                       - get_song_hashes_by_title(title)
                       - get_song_hashes_by_length(length)
```

## Database architecture

```
+--------------------+  +------------+  +========+
| Database Interface |--| SQLAlchemy |--| SQLite |
+--------------------+  +------------+  +========+
                                        - Song (table name: songs)
                                            - * song_hash    <String(40)> *
                                            - filename       <Text>
                                            - play_count     <Integer>
                                            - artist         <Text> <nullable>
                                            - title          <Text> <nullable>
                                            - length         <Integer> <nullable>
                                            - last_played    <DateTime> <nullable>
                                            - date_added     <DateTime> <nullable>
```
