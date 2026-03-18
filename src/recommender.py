from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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

def _song_to_dict(song: Song) -> Dict:
    """Convert Song dataclass to dict for score_song."""
    return {"genre": song.genre, "mood": song.mood, "energy": song.energy}


def _user_to_prefs(user: UserProfile) -> Dict:
    """Convert UserProfile to preference dict for score_song."""
    return {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy}


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Rank all songs by score and return the top k."""
        prefs = _user_to_prefs(user)
        scored = [(s, score_song(prefs, _song_to_dict(s))[0]) for s in self.songs]
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)
        return [s for s, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return human-readable explanation of why this song was recommended."""
        prefs = _user_to_prefs(user)
        _, explanation = score_song(prefs, _song_to_dict(song))
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dictionaries with proper type conversion.
    Numerical values (energy, tempo_bpm, valence, etc.) are converted to floats/ints for scoring.
    """
    import csv
    import os
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, csv_path) if not os.path.isabs(csv_path) else csv_path
    songs = []
    numeric_float = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            song["id"] = int(song.get("id", 0) or 0)
            for col in numeric_float:
                if col in song and song[col]:
                    song[col] = float(song[col])
                else:
                    song[col] = 0.0
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song against user preferences. Returns (score, explanation).
    Algorithm: +2.0 genre match, +1.0 mood match, up to 2.0 for energy similarity.
    """
    score = 0.0
    reasons = []
    genre = str(user_prefs.get("genre", "")).strip().lower()
    mood = str(user_prefs.get("mood", "")).strip().lower()
    target_energy = float(user_prefs.get("energy", 0.5))
    song_genre = str(song.get("genre", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    song_energy = float(song.get("energy", 0.5))
    if genre and song_genre == genre:
        score += 2.0
        reasons.append("genre match (+2.0)")
    if mood and song_mood == mood:
        score += 1.0
        reasons.append("mood match (+1.0)")
    energy_diff = abs(song_energy - target_energy)
    energy_score = max(0.0, 2.0 * (1.0 - energy_diff))
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")
    explanation = "; ".join(reasons) if reasons else "no match"
    return (score, explanation)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores all songs, ranks by score descending, and returns the top k with explanations.
    Uses score_song as the judge for each song; sorted() preserves the original list.
    """
    scored = [(s, *score_song(user_prefs, s)) for s in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, explanation) for song, score, explanation in ranked[:k]]
