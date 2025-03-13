from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///database.db')


Session = sessionmaker(bind=engine)
session = Session()

# User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    favorite_artist = Column(String, nullable=True)
    preferred_genres = Column(String, nullable=True)

    songs = relationship("Song", secondary="user_songs", back_populates="users")

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    songs = relationship("Song", back_populates="artist")

# UserSongs Model- many-to-many relationship
class UserSongs(Base):
    __tablename__ = 'user_songs'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True)
    rating = Column(Integer, nullable=True)

class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Associate playlist with a user

    songs = relationship("Song", secondary="playlist_songs", back_populates="playlists")

    def add_song(self, song):
        if song not in self.songs:
            self.songs.append(song)
            session.commit()
            print(f"Song '{song.title}' added to playlist '{self.name}'")
        else:
            print(f"Song '{song.title}' is already in playlist '{self.name}'")

    def remove_song(self, song):
        if song in self.songs:
            self.songs.remove(song)
            session.commit()
            print(f"Song '{song.title}' removed from playlist '{self.name}'")
        else:
            print(f"Song '{song.title}' is not in playlist '{self.name}'")

    def get_songs(self):
        if self.songs:
            print(f"Songs in playlist '{self.name}':")
            for song in self.songs:
                print(f"- {song.title} by {song.artist}")
        else:
            print(f"No songs in playlist '{self.name}'")

class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'))

    artist = relationship("Artist", back_populates="songs")

    playlists = relationship("Playlist", secondary="playlist_songs", back_populates="songs")
    users = relationship("User", secondary="user_songs", back_populates="songs")

class PlaylistSongs(Base):
    __tablename__ = 'playlist_songs'
    playlist_id = Column(Integer, ForeignKey('playlists.id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True)


Base.metadata.create_all(engine)
print("Database and tables created successfully!")
