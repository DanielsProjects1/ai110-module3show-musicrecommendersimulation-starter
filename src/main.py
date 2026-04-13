"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, create_taste_profile, WEIGHTING_STRATEGIES


def print_recommendations(label: str, note: str, recommendations: list) -> None:
    print("\n" + "=" * 60)
    print(f"  PROFILE: {label}")
    print(f"  NOTE: {note}")
    print("=" * 60)
    for i, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"\n  #{i}  {song['title']} by {song['artist']}")
        print(f"       Score: {score:.4f}  |  Genre: {song['genre']}  |  Mood: {song['mood']}")
        print("       Why this song:")
        for reason in reasons:
            print(f"         - {reason}")
        print("  " + "-" * 58)


def main() -> None:
    songs = load_songs("data/songs.csv")

    adversarial_profiles = [

        # ── 1. The Contradiction ─────────────────────────────────────────────
        # High energy + sad mood conflict: which songs satisfy both?
        (
            "The Contradiction — High Energy + Sad Mood",
            "energy=0.9 and mood=['sad'] are semantically opposite; "
            "watch how the ranker handles zero categorical + high numerical scores",
            create_taste_profile(
                genres=["emo", "post-punk"],
                moods=["sad", "melancholic"],
                energy=0.9,
                valence=0.05,
                danceability=0.85,
                acousticness=0.05,
                tempo_bpm=160,
            ),
        ),

        # ── 2. Out-of-Range Tempo ────────────────────────────────────────────
        # tempo_bpm=30 is below the 60 BPM floor used by normalization.
        # Songs far above 60 BPM will produce a negative tempo score because
        # score = 1 - |(30-60)/120 - (song_bpm-60)/120| can exceed 1.0.
        (
            "Out-of-Range Tempo — Negative Score Bug",
            "tempo_bpm=30 breaks the (bpm-60)/120 normalization; "
            "expect tempo scores to go negative for fast songs",
            create_taste_profile(
                genres=["ambient", "drone"],
                moods=["calm"],
                energy=0.05,
                valence=0.3,
                danceability=0.1,
                acousticness=0.9,
                tempo_bpm=30,
            ),
        ),

        # ── 3. Phantom Genre ─────────────────────────────────────────────────
        # No song in the dataset has this genre or mood, so every song scores
        # 0.0 on both categorical features (40% of default weight is dead).
        (
            "Phantom Genre — Silent All-Zero Categories",
            "genres and moods match nothing in the dataset; "
            "40% of weight is permanently zeroed out with no warning",
            create_taste_profile(
                genres=["neo-classical-darkwave-fusion"],
                moods=["transcendent"],
                energy=0.5,
                valence=0.5,
                danceability=0.5,
                acousticness=0.5,
                tempo_bpm=120,
            ),
        ),

        # ── 4. The Tolerance Trap ────────────────────────────────────────────
        # tolerance=0.01 sounds very strict but the field is stored and never
        # read by score_song — it has zero effect on results.
        (
            "The Tolerance Trap — Dead Parameter",
            "tolerance=0.01 vs tolerance=0.99 produces identical output; "
            "score_song never reads user_prefs['tolerance']",
            create_taste_profile(
                genres=["jazz"],
                moods=["relaxed"],
                energy=0.4,
                valence=0.6,
                danceability=0.3,
                acousticness=0.8,
                tempo_bpm=90,
                tolerance=0.01,
            ),
        ),

        # ── 5. Weights Don't Sum to 1.0 ──────────────────────────────────────
        # Weights sum to 0.5 instead of 1.0. Relative ranking still works but
        # all scores are halved and no longer interpretable as 0–1 confidence.
        (
            "Weights Don't Sum to 1.0",
            "weights sum to 0.5; scores will top out around 0.5 "
            "but ranking order is accidentally preserved",
            create_taste_profile(
                genres=["pop"],
                moods=["happy"],
                energy=0.7,
                valence=0.8,
                danceability=0.75,
                acousticness=0.2,
                tempo_bpm=120,
                weights={
                    "genre": 0.10,
                    "mood": 0.10,
                    "energy": 0.075,
                    "valence": 0.075,
                    "danceability": 0.075,
                    "acousticness": 0.05,
                    "tempo_bpm": 0.025,
                },
            ),
        ),

        # ── 6. All-Zero Weights ──────────────────────────────────────────────
        # Every song scores exactly 0.0. sorted() preserves insertion order,
        # so "top 5" is just the first 5 rows of the CSV.
        (
            "All-Zero Weights — Every Song Ties at 0.0",
            "all weights=0.0 means every song scores 0.0; "
            "recommendations are the first 5 rows of the CSV by accident",
            create_taste_profile(
                genres=["rock"],
                moods=["energetic"],
                energy=0.8,
                valence=0.6,
                danceability=0.7,
                acousticness=0.1,
                tempo_bpm=130,
                weights={k: 0.0 for k in [
                    "genre", "mood", "energy", "valence",
                    "danceability", "acousticness", "tempo_bpm"
                ]},
            ),
        ),

        # ── 7. Contradictory Audio Physics ───────────────────────────────────
        # energy=0.95 AND acousticness=0.95 almost never co-occur in real music.
        # The scorer treats them independently so no song can score well on both;
        # results will be mediocre compromises.
        (
            "Contradictory Audio Physics — High Energy + High Acousticness",
            "energy=0.95 and acousticness=0.95 are physically rare together; "
            "watch scores plateau around 0.5 with no clear winner",
            create_taste_profile(
                genres=["folk"],
                moods=["intense"],
                energy=0.95,
                valence=0.5,
                danceability=0.8,
                acousticness=0.95,
                tempo_bpm=160,
                weights=WEIGHTING_STRATEGIES["audio_features_focused"],
            ),
        ),

        # ── 8. The Catch-All ─────────────────────────────────────────────────
        # Every genre and mood in the dataset is listed. All categorical scores
        # are 1.0 for every song, making genre/mood useless for discrimination.
        # Rankings are driven entirely by "closeness to average" (0.5 targets).
        (
            "The Catch-All — Overly Broad Categories",
            "all genres and moods listed so categorical scores are 1.0 everywhere; "
            "rankings reduce to 'closest to perfectly average song'",
            create_taste_profile(
                genres=["pop", "rock", "jazz", "metal", "hip-hop", "indie pop",
                        "country", "classical", "electronic", "folk", "lofi",
                        "ambient", "synthwave", "soul", "alternative", "reggae"],
                moods=["happy", "sad", "calm", "intense", "melancholic",
                       "romantic", "aggressive", "chill", "uplifting", "focused",
                       "playful", "moody", "energetic", "relaxed"],
                energy=0.5,
                valence=0.5,
                danceability=0.5,
                acousticness=0.5,
                tempo_bpm=120,
            ),
        ),
    ]

    for label, note, profile in adversarial_profiles:
        recs = recommend_songs(profile, songs, k=5)
        print_recommendations(label, note, recs)


if __name__ == "__main__":
    main()
