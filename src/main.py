"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, create_taste_profile


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Create a user's taste profile using the create_taste_profile function
    user_profile = create_taste_profile(
        genres=["pop", "indie pop"],
        moods=["happy", "uplifting"], 
        energy=0.75,
        valence=0.80,
        danceability=0.78,
        acousticness=0.20,
        tempo_bpm=120,
        tolerance=0.15
    )

    recommendations = recommend_songs(user_profile, songs, k=5)

    print("\n" + "=" * 50)
    print("       TOP SONG RECOMMENDATIONS")
    print("=" * 50)

    for i, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f}  |  Genre: {song['genre']}  |  Mood: {song['mood']}")
        print("    Why this song:")
        for reason in reasons:
            print(f"      - {reason}")
        print("-" * 50)


if __name__ == "__main__":
    main()
