from models import User, Song, UserSongs, Playlist, session
from sqlalchemy.exc import IntegrityError

def add_user(name, favorite_artist, preferred_genres):
    existing_user = session.query(User).filter_by(name=name).first()
    if existing_user:
        print(f"User '{name}' already exists!")
        return

    new_user = User(name=name, favorite_artist=favorite_artist, preferred_genres=preferred_genres)
    session.add(new_user)

    try:
        session.commit()
        print(f"User '{name}' added successfully!")
        check_user = session.query(User).filter_by(name=name).first()
        if check_user:
            print(f" User '{check_user.name}' exists in database!")
        else:
            print("User does not exist!")
    except IntegrityError:
        session.rollback()
        print(f"Error: User '{name}' already exists in the database.")

def add_song(title, artist, genre, user_name):
    """Adds a new song and assigns it to the user who added it."""
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print(f"User '{user_name}' not found. Please add the user first.")
        return

    song = session.query(Song).filter_by(title=title, artist=artist).first()
    if song:
        print(f"Song '{title}' by {artist} already exists.")
    else:
        song = Song(title=title, artist=artist, genre=genre)
        session.add(song)
        try:
            session.commit()
            print(f"Song '{title}' by {artist} added!")
        except Exception as e:
            session.rollback()
            print(f"Error adding song '{title}': {str(e)}")

    user_song = UserSongs(user_id=user.id, song_id=song.id)
    session.add(user_song)
    session.commit()
    print(f"User '{user_name}' has added '{title}' to their library.")

def rate_song(user_name, song_title, rating):
    """Allows a user to rate a song (1-5 stars)."""
    user = session.query(User).filter_by(name=user_name).first()
    song = session.query(Song).filter_by(title=song_title).first()

    if not user:
        print(f"User '{user_name}' not found.")
        return

    if not song:
        print(f"Song '{song_title}' not found.")
        return

    if rating < 1 or rating > 5:
        print("Rating must be between 1 and 5.")
        return

    user_song = session.query(UserSongs).filter_by(user_id=user.id, song_id=song.id).first()
    if user_song:
        user_song.rating = rating
    else:
        user_song = UserSongs(user_id=user.id, song_id=song.id, rating=rating)
        session.add(user_song)

    session.commit()
    print(f"⭐ User '{user_name}' rated '{song_title}' with {rating}/5.")

def recommend_songs(user_name):
    """Recommends songs based on ratings and user preferences."""
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    recommended_songs = session.query(Song).filter(
        (Song.artist == user.favorite_artist) | (Song.genre == user.preferred_genres)
    ).all()

    try:
        top_rated_songs = session.query(Song).join(UserSongs).filter(UserSongs.rating >= 4).all()
    except AttributeError:
        print("Error: UserSongs.rating does not exist! Check your database structure.")
        return

    all_recommendations = list(set(recommended_songs + top_rated_songs))

    if all_recommendations:
        print(f"\n🎶 Recommended Songs for {user_name}:")
        for song in all_recommendations:
            print(f"- {song.title} by {song.artist} ({song.genre})")
    else:
        print("No recommendations found.")

def search_songs(title):
    """Searches for a song by title."""
    song = session.query(Song).filter_by(title=title).first()
    if song:
        print(f"Song Found: {song.title}")
    else:
        print("Song not found.")

def create_playlist(user_name, playlist_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print(f"User '{user_name}' not found.")
        return

    playlist = Playlist(name=playlist_name, user_id=user.id)  # Assuming Playlist has user_id
    session.add(playlist)
    session.commit()
    print(f"Playlist '{playlist_name}' created for user '{user_name}'.")

def add_song_to_playlist(user_name, playlist_name, song_title):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print(f"User '{user_name}' not found.")
        return

    playlist = session.query(Playlist).filter_by(name=playlist_name, user_id=user.id).first()
    if not playlist:
        print(f"Playlist '{playlist_name}' not found for user '{user_name}'.")
        return

    song = session.query(Song).filter_by(title=song_title).first()
    if not song:
        print(f"Song '{song_title}' not found.")
        return

    playlist.add_song(song)  # Using the add_song method from the Playlist class
    session.commit()

def remove_song_from_playlist(user_name, playlist_name, song_title):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print(f"User '{user_name}' not found.")
        return

    playlist = session.query(Playlist).filter_by(name=playlist_name, user_id=user.id).first()
    if not playlist:
        print(f"Playlist '{playlist_name}' not found for user '{user_name}'.")
        return

    song = session.query(Song).filter_by(title=song_title).first()
    if not song:
        print(f"Song '{song_title}' not found.")
        return

    playlist.remove_song(song)  # Using the remove_song method from the Playlist class
    session.commit()
# functionality.py

def get_playlist(playlist_name):
    
    playlist = session.query(Playlist).filter_by(name=playlist_name).first()
    if playlist:
        print(f"Playlist '{playlist_name}' contains the following songs:")
        for song in playlist.songs:
            print(f"- {song.title} by {song.artist}")
    else:
        print(f"Playlist '{playlist_name}' not found.")

def clear_data():
    session.query(User).delete()
    session.query(Song).delete()
    session.query(UserSongs).delete()
    session.query(Playlist).delete()
    session.commit()
    print("All data cleared!")
