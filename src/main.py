"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Define multiple user profiles for stress testing
    profiles = {
        "Pop/Happy (default)": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4},
        "Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
        "Conflicting (adversarial)": {"genre": "pop", "mood": "sad", "energy": 0.9},
    }

    # Run recommender for each profile (set run_all_profiles=True for full stress test)
    run_all_profiles = True
    profiles_to_run = list(profiles.items()) if run_all_profiles else [("Pop/Happy (default)", profiles["Pop/Happy (default)"])]

    for profile_name, user_prefs in profiles_to_run:
        print(f"Profile: {profile_name}\n")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print("Top recommendations:\n")
        for i, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            print(f"  {i}. {song['title']} — {song['artist']}")
            print(f"     Score: {score:.2f}")
            print(f"     Because: {explanation}")
            print()
        if run_all_profiles:
            print("-" * 50)


if __name__ == "__main__":
    main()
