from functionality import add_user, add_song, recommend_songs, rate_song, search_songs, create_playlist, add_song_to_playlist, remove_song_from_playlist, get_playlist, clear_data

def main():
    while True:
        print(" Music Recommendation App")
        print("1. Add User")
        print("2. Add Song")
        print("3. Rate a Song")
        print("4. Get Song Recommendations")
        print("5. Search for a Song")
        print("6. Create a playlist")
        print("7. Add a song to a playlist")
        print("8. Remove a song from a playlist")
        print("9. Get a playlist")
        print("10. Clear app data")
        print("11. Exit")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                print("Adding a User...")
                name = input("Enter your name: ")
                favorite_artist = input("Favorite artist: ")
                preferred_genres = input("Preferred genres (comma-separated): ")
                add_user(name, favorite_artist, preferred_genres)

            elif choice == "2":
                print("Adding a Song...")
                user_name = input("Enter your name: ")  # Associate song with user
                title = input("Enter song title: ")
                artist = input("Enter artist: ")
                genre = input("Enter genre: ")
                add_song(title, artist, genre, user_name)  # Associate song with user

            elif choice == "3":
                print("Rating a Song...")
                user_name = input("Enter your name: ")
                song_title = input("Enter the song title to rate: ")
                rating = int(input("Rate the song (1-5): "))
                rate_song(user_name, song_title, rating)

            elif choice == "4":
                print("Getting Song Recommendations...")
                user_name = input("Enter your name: ")
                recommend_songs(user_name)

            elif choice == "5":
                print("Searching for a Song...")
                song_title = input("Enter the song title to search: ")
                search_songs(song_title)

            elif choice == "6":
                print("Creating a Playlist...")
                user_name = input("Enter your name: ")
                playlist_name = input("Enter the playlist name: ")
                create_playlist(user_name, playlist_name)

            elif choice == "7":
                print("Adding a Song to a Playlist...")
                user_name = input("Enter your name: ")
                playlist_name = input("Enter the playlist name: ")
                song_title = input("Enter the song title to add: ")
                add_song_to_playlist(user_name, playlist_name, song_title)

            elif choice == "8":
                print("Removing a Song from a Playlist...")
                user_name = input("Enter your name: ")
                playlist_name = input("Enter the playlist name: ")
                song_title = input("Enter the song title to remove: ")
                remove_song_from_playlist(user_name, playlist_name, song_title)

            elif choice == "9":
                print("Getting a Playlist...")
                user_name = input("Enter your name: ")
                playlist_name = input("Enter the playlist name: ")
                get_playlist(user_name, playlist_name)

            elif choice == "10":
                print("Clearing App Data...")
                clear_data()

            elif choice == "11":
                print("Exiting the App")
                print("Catch you on the next track! ciao!")
                break

            else:
                print("Invalid choice. Please try again.")
        
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()
