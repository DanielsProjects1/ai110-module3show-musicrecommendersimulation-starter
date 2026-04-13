# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  

Content-based song recommendations

- What assumptions does it make about the user  

That the user knows their taste in numerical terms and that they know the catalogs exact genre and mood vocabulary.

- Is this for real users or classroom exploration  

This is for classroom exploration.


---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The genre, mood, energy, valence, danceability, acousticness, and tempo_bpm were the features from each song that I used to help me score the song. The system first creates a user taste profile using the users preference for each feature and compares each song by how close each feature of that song is to their respecitve feature rating of the taste profile and sums them up to get the score of the song.

Scores were raw sums (roughly 0–5.8). Valence and tempo weren't scored at all. The user profile had only four fields: one genre string, one mood string, a single energy target, and a boolean likes_acoustic.

What changed in the current version:

Scoring normalized to 0–1. The raw additive system was replaced with a weighted sum where all feature scores are on a 0–1 scale and weights sum to 1.0, making scores interpretable across different profiles.

Weights made configurable. Every feature now has an explicit weight. Eight named weighting strategies (genre-focused, mood-focused, energy-focused, etc.) let you shift what matters most without changing the profile values.

Profile expanded from 4 fields to 7 features. valence, danceability, acousticness, and tempo_bpm are now all scored. The single-genre and single-mood strings became lists, allowing multiple preferred genres and moods.

Acousticness changed from binary to proximity-based. The original used acousticness >= 0.5 as a yes/no threshold. The current version scores it the same way as energy — 1 - |target - value| — giving partial credit for close matches.

The conditional danceability boost was removed. In the original, danceability only contributed to the score when target_energy >= 0.7. Now it's scored independently with its own weight every time.

Tempo added as a scored feature. The original ignored tempo entirely. The current version normalizes it to 0–1 using the 60–180 BPM window, then scores it by proximity.

Removed the pandas dependency. The starter used pandas to load the CSV. The current version uses the standard library csv module via load_songs().

Explanation style changed. The original explain_recommendation() returned natural language like "matches your favorite genre pop, has a similar energy level." The current score_song() returns data-reporting strings like "Energy: 0.88 (target=0.7, song=0.82)" — more precise, but less human-readable.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 20 songs total.
The genres covered are: pop, indie pop, lofi, rock, electronic, synthwave, ambient, jazz, classical, soul, metal, hip-hop, country, folk, reggae, and alternative. Moods include happy, chill, intense, focused, melancholic, moody, uplifting, relaxed, playful, romantic, aggressive, sad, and energetic.
I didn't add or remove any songs from the original dataset.
There's also a lot missing in terms of what music actually exists. The whole catalog is Western English-language music. There's no K-pop, no Latin genres like cumbia or reggaeton, no Afrobeats, no classical Indian music, nothing in languages other than English.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best when the user's preferences are specific and actually match what's in the catalog. The clearest example from testing was the jazz/relaxed profile — it returned Coffee Shop Stories as the #1 pick with a score of 0.93, and that genuinely is the most jazz, acoustic, low-energy song in the dataset. When the genre and mood match and the numerical features line up, the ranking feels obvious in a good way, like the system did exactly what you'd expect.

The weighted scoring captures a few real patterns correctly. When a user cares a lot about energy level (like a workout profile), the energy-focused weighting strategy pushes high-energy songs to the top even if the genre doesn't match, which makes sense for how people actually use music functionally rather than categorically.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  

Songs whose genre is not in the user's genre list get penalized by up to .4 points no matter how perfectly it matches other dimensions. 

The system disadvantages semantically related content that happens to use a different label.

- Genres or moods that are underrepresented  

Romantic, aggressive, sad, playful, focused, and energetic songs all only have 1 song.

- Cases where the system overfits to one preference  

The 60–180 BPM window assumes Western popular music conventions. Genres like:
Drone / dark ambient: 20–40 BPM
Cumbia / some Afrobeat: 80–100 BPM (fine)
Speedcore / some drum & bass: 180–300 BPM
...are penalized or produce negative scores because the normalization formula wasn't designed for them.

- Ways the scoring might unintentionally favor some users  

A user with genres=["pop", "rock", "electronic"] will match genre on 5 songs (getting +0.20 each). A user with genres=["jazz"] matches 1 song. The categorical weight is 40% of the total score under defaults, so broad-taste users get a larger portion of the score "unlocked" across more songs — they naturally see higher average scores and more variety in top-5.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested 

I tested eight adversarial profiles designed to stress-test the scoring logic rather than represent realistic listeners. These included:

The Contradiction — a user who wants high energy (0.9) but only sad, melancholic moods, to see what the system does when numerical and categorical preferences point in opposite directions
Out-of-Range Tempo — a user targeting 30 BPM, well below the 60–180 BPM range the normalization formula assumes, to see if scores could go negative
Phantom Genre — a user whose listed genre and mood exist in no song in the dataset, to see if the system warns you or silently degrades
The Tolerance Trap — a user with tolerance=0.01 to verify whether that parameter actually affects results
Weights Don't Sum to 1.0 — custom weights that add up to 0.5 instead of 1.0, to see how the final scores behave
All-Zero Weights — every weight set to 0.0, to see what the system recommends when it has no criteria
Contradictory Audio Physics — a user wanting both very high energy and very high acousticness, two features that almost never appear together in real songs
The Catch-All — a user who lists every genre and mood in the dataset, to see what ranking looks like when categorical scoring is meaningless

- What you looked for in the recommendations  

I looked at whether the scores and rankings made intuitive sense given the profile, whether the system gave any indication when something was wrong, and whether the top-5 results were genuinely useful or just the least bad available options. I also compared the actual score values across profiles to see whether they were interpretable as confidence levels.

- What surprised you 

The Phantom Genre and Catch-All profiles returned the same five songs in the same order, just with scores 0.40 points lower across the board for Phantom Genre. This made it clear that 40% of the scoring weight was silently zeroed out. The system never flagged it.

- Any simple tests or comparisons you ran  

The most useful comparison was running the Phantom Genre and Catch-All profiles back to back. Since the Catch-All matches every genre and mood in the dataset and Phantom Genre matches none, they function as a controlled experiment: same numerical targets, same weights, only the categorical match rate changed. The rankings were identical proving the numerical features alone drove all the ordering, and the 0.40-point categorical gap just shifted every score uniformly downward without changing which songs were "better" than others.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I would make the system so that genre's like "indie" and "indie pop" are treated similarly and not penalized for being different genres.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  


I learned that recommender system can be unintentionally biased due to how they compare songs. For example: in my system, the tempo normaliztion is 60-180 BPM which assumes Western Pop conventions meaning genres outside this range will get distorted scores.
Something unexpected that I discovered is that writing the logic for a music recommender app, or in this case simulation, is quite simple.
Now I know that the songs I listen to on spotify also have a danceability attribute.
