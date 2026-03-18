# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This recommender suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration—to understand how content-based recommenders work—and is not intended for real users or production use. It assumes users can articulate preferences as genre, mood, and energy targets.

---

## 3. How the Model Works

The model uses three features per song: *genre*, *mood*, and *energy* (0.0–1.0). The user provides a favorite genre, favorite mood, and target energy. Each song is scored by how well it matches these preferences. A genre match adds 2.0 points, a mood match adds 1.0 points, and energy similarity adds up to 2.0 points based on how close the song's energy is to the target (closer = higher). All songs are then sorted by score and the top K are returned with explanations of why each was suggested.

---

## 4. Data

- **Catalog size:** 10 songs in `data/songs.csv`.
- **Genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop.
- **Moods:** happy, chill, intense, relaxed, moody, focused.
- The dataset favors lofi (3 songs) and pop (2 songs); rock, ambient, jazz, synthwave, and indie pop have one song each. No lyrics, semantic understanding, or user listening history.

---

## 5. Strengths

- Works well when user preferences clearly align with a subset of the catalog (e.g., Pop/Happy, Chill Lofi, Intense Rock).
- Transparent: every recommendation includes the reasons (genre match, mood match, energy similarity).
- Simple and interpretable—no black box; easy to adjust weights or add features.
- Clear separation between "Gym Hero" (pop + intense) and "Sunrise City" (pop + happy) for users who care about mood.

---

## 6. Limitations and Bias

- **Genre dominance:** Genre is weighted highest (2.0 points). A great mood/energy match in another genre may lose to a weaker genre match.
- **Filter bubbles:** The system tends to over-prioritize pop and lofi because they appear more often in the catalog.
- **Narrow profiles:** Users with conflicting preferences (e.g., pop + sad + high energy) get partial matches that may feel inconsistent.
- **Ignores:** Lyrics, tempo nuance, acousticness, danceability in scoring; collaborative signals; diversity or serendipity.

---

## 7. Evaluation

Tested with four profiles: Pop/Happy (default), Chill Lofi, Intense Rock, and an adversarial profile (pop + sad + high energy). Results aligned with expectations for coherent profiles (Pop/Happy → Sunrise City first; Chill Lofi → Midnight Coding, Library Rain). The adversarial profile surfaced songs that partially matched, showing how the scoring trades off. Ran pytest for the Recommender OOP interface. No numeric accuracy metric; evaluation was qualitative: do the top results feel right for the profile?

---

## 8. Future Work

- Add tempo range and valence to scoring for finer "vibe" control.
- Introduce diversity constraints so the top K are not all from the same genre.
- Support multiple users and "group vibe" recommendations.
- Experiment with soft genre/mood matching (e.g., "indie pop" partially matching "pop").

---

## 9. Personal Reflection

Building this showed how a small set of rules can produce recommendations that feel intentional. Real recommenders rely on much more data and nuance, but the core idea—turn preferences and content attributes into scores, then rank—is the same. The biggest learning was how bias sneaks in: genre weight, catalog balance, and a single scoring rule all shape who gets served well. AI tools helped quickly prototype and iterate; double-checking the scoring math and edge cases (empty preferences, missing fields) was essential.
