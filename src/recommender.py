from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

def create_taste_profile(
    genres: list,
    moods: list,
    energy: float,
    valence: float,
    danceability: float,
    acousticness: float,
    tempo_bpm: int,
    weights: dict = None,
    tolerance: float = 0.2
) -> dict:
    """
    Creates a taste profile dictionary for music recommendation comparisons.
    
    This represents a user's musical preferences across both categorical 
    (genres, moods) and numerical (energy, valence, etc.) song attributes.
    
    Args:
        genres: List of preferred genres (e.g., ["pop", "indie pop"])
        moods: List of preferred moods (e.g., ["happy", "uplifting"])
        energy: Target energy level (0-1 scale, where 0=low, 1=high)
        valence: Target valence/positivity (0-1 scale, where 0=sad, 1=happy)
        danceability: Target danceability (0-1 scale)
        acousticness: Target acousticness (0-1 scale, where 0=electronic, 1=acoustic)
        tempo_bpm: Target tempo in beats per minute (typical range: 60-180)
        weights: Dict of feature importance weights (should sum to ~1.0)
                 If None, uses default equal weighting
        tolerance: Acceptable range for numerical features (0-1 scale)
                   Default 0.2 = 20% tolerance around target values
    
    Returns:
        A dictionary representing the user's taste profile with the following structure:
        {
            "categorical": {"genres": [...], "moods": [...]},
            "numerical": {"energy": ..., "valence": ..., ...},
            "weights": {...},
            "tolerance": ...
        }
    
    Example:
        profile = create_taste_profile(
            genres=["pop", "indie pop"],
            moods=["happy", "uplifting"],
            energy=0.75,
            valence=0.80,
            danceability=0.78,
            acousticness=0.20,
            tempo_bpm=120,
            tolerance=0.15
        )
    """
    default_weights = {
        "genre": 0.20,
        "mood": 0.20,
        "energy": 0.15,
        "valence": 0.15,
        "danceability": 0.15,
        "acousticness": 0.10,
        "tempo_bpm": 0.05
    }
    
    return {
        "categorical": {
            "genres": genres,
            "moods": moods
        },
        "numerical": {
            "energy": energy,
            "valence": valence,
            "danceability": danceability,
            "acousticness": acousticness,
            "tempo_bpm": tempo_bpm
        },
        "weights": weights or default_weights,
        "tolerance": tolerance
    }


# ============================================================================
# POINT WEIGHTING STRATEGIES FOR ATTRIBUTE SCORING
# ============================================================================
# This section defines how each attribute contributes to a song's overall score.
# All individual attribute scores are normalized to 0-1 range, then weighted.
#
# SCORING APPROACH:
# 1. Categorical Features (Genre, Mood):
#    - BINARY MATCH: 1.0 if song's attribute is in user's preferred list
#    - NO MATCH: 0.0 if song's attribute is NOT in user's preferred list
#    - No partial credit (exact match only)
#
# 2. Numerical Features (Energy, Valence, Danceability, Acousticness, Tempo):
#    - PROXIMITY-BASED: Score = 1 - |user_target - song_value|
#    - Range: 0.0 (farthest) to 1.0 (perfect match)
#    - TEMPO NORMALIZATION: Convert BPM to 0-1 scale first
#      * Typical range: 60-180 BPM
#      * normalized_tempo = (tempo_bpm - 60) / (180 - 60) = (tempo_bpm - 60) / 120
#
# 3. Overall Score:
#    - Weighted sum of all attribute scores
#    - final_score = Σ(attribute_score × attribute_weight)
#    - All weights must sum to 1.0 for normalized output
#
# ============================================================================

# PREDEFINED WEIGHTING STRATEGIES
# Choose a strategy based on user profile type or customize your own

WEIGHTING_STRATEGIES = {
    # GENRE-FOCUSED: User cares most about genre match, mood match secondary
    "genre_focused": {
        "genre": 0.35,
        "mood": 0.20,
        "energy": 0.15,
        "valence": 0.10,
        "danceability": 0.10,
        "acousticness": 0.05,
        "tempo_bpm": 0.05,
    },
    
    # MOOD-FOCUSED: User cares most about mood/vibe, genre is secondary
    "mood_focused": {
        "genre": 0.20,
        "mood": 0.35,
        "energy": 0.15,
        "valence": 0.15,
        "danceability": 0.10,
        "acousticness": 0.03,
        "tempo_bpm": 0.02,
    },
    
    # ENERGY-FOCUSED: User wants the right energy level above all else
    # (e.g., workout music, chill study sessions)
    "energy_focused": {
        "genre": 0.15,
        "mood": 0.15,
        "energy": 0.35,
        "valence": 0.10,
        "danceability": 0.15,
        "acousticness": 0.05,
        "tempo_bpm": 0.05,
    },
    
    # AUDIO_FEATURES_FOCUSED: Numerical features matter more than categorical
    # (e.g., user who focuses on feel/sound over genre labels)
    "audio_features_focused": {
        "genre": 0.10,
        "mood": 0.10,
        "energy": 0.20,
        "valence": 0.20,
        "danceability": 0.20,
        "acousticness": 0.15,
        "tempo_bpm": 0.05,
    },
    
    # BALANCED: Equal importance across most features
    "balanced": {
        "genre": 0.18,
        "mood": 0.18,
        "energy": 0.16,
        "valence": 0.16,
        "danceability": 0.16,
        "acousticness": 0.10,
        "tempo_bpm": 0.06,
    },
    
    # STRICT_GENRE_MOOD: User wants their exact genre/mood, flexible on audio
    # (categorical = 60%, numerical = 40%)
    "strict_categorical": {
        "genre": 0.35,
        "mood": 0.25,
        "energy": 0.12,
        "valence": 0.10,
        "danceability": 0.10,
        "acousticness": 0.05,
        "tempo_bpm": 0.03,
    },
    
    # ACOUSTIC_PREFERENCE: User strongly prefers acoustic vs electronic
    "acoustic_focused": {
        "genre": 0.15,
        "mood": 0.15,
        "energy": 0.15,
        "valence": 0.15,
        "danceability": 0.10,
        "acousticness": 0.25,
        "tempo_bpm": 0.05,
    },
    
    # VIBE_FOCUSED: Mood, Energy, Valence matter most (the "feeling" of music)
    "vibe_focused": {
        "genre": 0.08,
        "mood": 0.30,
        "energy": 0.25,
        "valence": 0.20,
        "danceability": 0.10,
        "acousticness": 0.04,
        "tempo_bpm": 0.03,
    },
}

# EXAMPLE USAGE OF STRATEGIES:
# 
# # For a user who cares mostly about genre:
# user_profile = create_taste_profile(
#     genres=["rock", "metal"],
#     moods=["intense", "aggressive"],
#     energy=0.85,
#     valence=0.40,
#     danceability=0.70,
#     acousticness=0.10,
#     tempo_bpm=140,
#     weights=WEIGHTING_STRATEGIES["genre_focused"]
# )
#
# # For a user who wants the right mood/vibe regardless of genre:
# user_profile = create_taste_profile(
#     genres=["pop", "lofi", "ambient"],  # More flexible on genre
#     moods=["relaxed", "chill"],
#     energy=0.35,
#     valence=0.60,
#     danceability=0.40,
#     acousticness=0.70,
#     tempo_bpm=85,
#     weights=WEIGHTING_STRATEGIES["mood_focused"]
# )

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    numerical_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in numerical_fields:
                row[field] = float(row[field])
            songs.append(dict(row))

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    weights = user_prefs["weights"]
    categorical = user_prefs["categorical"]
    numerical = user_prefs["numerical"]

    scores = {}
    reasons = []

    # Categorical: binary match (1.0 = match, 0.0 = no match)
    genre_match = song["genre"] in categorical["genres"]
    scores["genre"] = 1.0 if genre_match else 0.0
    reasons.append(f"Genre {'matched' if genre_match else 'did not match'} ({song['genre']})")

    mood_match = song["mood"] in categorical["moods"]
    scores["mood"] = 1.0 if mood_match else 0.0
    reasons.append(f"Mood {'matched' if mood_match else 'did not match'} ({song['mood']})")

    # Numerical: proximity-based score = 1 - |target - value|
    for feature in ["energy", "valence", "danceability", "acousticness"]:
        target = numerical[feature]
        value = song[feature]
        score = 1.0 - abs(target - value)
        scores[feature] = score
        reasons.append(f"{feature.capitalize()}: {score:.2f} (target={target}, song={value})")

    # Tempo: normalize to 0-1 first, then proximity score
    target_norm = (numerical["tempo_bpm"] - 60) / 120
    song_norm = (song["tempo_bpm"] - 60) / 120
    tempo_score = 1.0 - abs(target_norm - song_norm)
    scores["tempo_bpm"] = tempo_score
    reasons.append(f"Tempo: {tempo_score:.2f} (target={numerical['tempo_bpm']} BPM, song={song['tempo_bpm']} BPM)")

    # Weighted sum: final_score = Σ(attribute_score × weight)
    final_score = sum(scores[attr] * weights[attr] for attr in weights)

    return final_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    top_k = sorted(scored, key=lambda x: x[1], reverse=True)[:k]
    return [(song, score, reasons) for song, score, reasons in top_k]
