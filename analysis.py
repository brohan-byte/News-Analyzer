import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
import matplotlib.pyplot as plt
from collections import Counter

df = pd.read_csv("dist/headlines--08182025.csv") 


df["title"] = df["title"].astype(str).str.lower()

teams = ["arsenal", "man utd", "chelsea", "liverpool"]
df["team"] = df["title"].apply(lambda x: [t for t in teams if t in x])

team_counts = df.explode("team")["team"].value_counts()
print("Team counts:\n", team_counts)


nltk.download("vader_lexicon")
sid = SentimentIntensityAnalyzer()

df["sentiment"] = df["title"].apply(lambda x: sid.polarity_scores(x)["compound"])

avg_sentiment = df.explode("team").groupby("team")["sentiment"].mean()
print("\nAverage sentiment by team:\n", avg_sentiment)


nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

df["entities"] = df["title"].apply(extract_entities)

entity_counts = Counter([e[1] for ents in df["entities"] for e in ents])
print("\nEntity counts:\n", entity_counts)


sports = {
    "football": ["arsenal", "man utd", "chelsea"],
    "tennis": ["swiatek", "rybakina"],
    "cricket": ["buttler", "livingstone"],
    "boxing": ["usyk", "whyte"]
}

def detect_sport(title):
    for sport, words in sports.items():
        if any(w in title for w in words):
            return sport
    return "other"

df["sport"] = df["title"].apply(detect_sport)

sport_counts = df["sport"].value_counts()
print("\nSport counts:\n", sport_counts)


sport_counts.plot(kind="bar", title="News coverage by sport")
plt.show()

text = " ".join(df["title"])
