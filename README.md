# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

In my system, each song will use the following features: energy, valence, genre, mood, danceability, tempo_bpm, and acousticness.

My `Recommender` will computer the score of each song by taking each the abosulte value of each rating of each attribute of the song minus the users preferred rating for that attribute, and subtracting that value from 1 to get the songs score for that attribute. This way, the closer the song's attribute is rating wise to the user's preferred attribute rating, the higher a score it will receive for that rating. then we take the scores for all those attributes and divide multiply each of them by a weight based on how important that attribute is to the user, and then take the average score of all these attributes and assign that to the overall score.

We will use this score to determine which songs get recommended to the user.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

The biggest thing I learned is that a recommender isn't really "smart" — it's just math applied to assumptions. Every feature gets a number, every number gets compared to a target, and the song with the smallest total gap wins. What makes it feel intelligent is that when the assumptions are reasonable and the data is representative, the output looks like genuine taste-matching. But once you stress-test it — like asking for high energy and sad mood at the same time, or setting all weights to zero — you see that the system has no actual understanding of music. It's pattern-matching against whatever structure you gave it, and if that structure is wrong or incomplete, it fails silently and confidently.

The bias stuff was the more surprising part. Going in I expected bias to mean something obvious, like the system explicitly favoring one group. What I actually found is that most of it is invisible and structural. A user who writes "indie" instead of "indie pop" loses 20% of their score with no warning. A user who likes jazz gets one real candidate in the whole catalog while a lofi fan gets three, so their recommendations are just worse by default. The tempo formula quietly assumes no one listens to music outside 60–180 BPM, which rules out entire global genres. None of that is intentional — it's just that every design decision (what labels to use, how many songs per genre to include, what BPM range to normalize against) quietly encodes assumptions about whose taste is "normal." The system treats everyone the same mathematically, but the people whose taste matches those hidden assumptions get noticeably better results.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

Default Output
![Music Recommender Default output 1](<Music Recommender Default output 1.png>)
![Music Recommender Default output 2](<Music Recommender Default output 2.png>)

Phase 4 Pictures
![Pic 1](<Phase 4 pic 1.png>) ![Pic 2](<Phase 4 pic 2.png>) ![Pic 3](<Phase 4 pic 3.png>)![Pic 4](<phase 4 pic 4.png>) 


