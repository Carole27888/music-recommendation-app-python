from faker import Faker
from sqlalchemy.orm import sessionmaker
from models import Base, User, Song, Artist, UserSongs, engine
import random

fake = Faker()

Session = sessionmaker(bind=engine)
session = Session()

genres = ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Classical', 'Electronic', 'Reggae', 'RnB', 'Country', 'Metal']

artists = [Artist(name=fake.name()) for _ in range(10)]
session.add_all(artists)
session.commit()
print("Artists created successfully!")

users = [User(name=fake.name()) for _ in range(10)]
session.add_all(users)
session.commit()
print("Users created successfully!")

songs = [
    Song(
        title=fake.sentence(nb_words=3).replace(".", ""),
        genre=random.choice(genres),
        artist_id=random.choice(artists).id
    )
    for _ in range(10)
]
session.add_all(songs)
session.commit()
print("Songs created successfully!")

for user in users:
    assigned_songs = random.sample(songs, random.randint(1, 3))
    for song in assigned_songs:
        user_song = UserSongs(user_id=user.id, song_id=song.id, rating=random.randint(1, 5))
        session.add(user_song)

session.commit()


session.close()

