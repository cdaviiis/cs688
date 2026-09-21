"""
3. Write a script to look at the title of each article and count the occurrences
of the three given words. For example, "ai", "compute”, and "invest". Then, create
a word frequency histogram.
Our script satisfies the criteria above by doing the following:
- reads the file produced by scrape_bing_news.py (one title per line)
- strips on-alpha characters from each title
- counts EXACT (whole-word) matches of our three keywords
- plots a word-frequency histogram
"""
import matplotlib.pyplot as plt

input_csv = "search_results_titles.csv"
keywords = ["ai", "invest", "compute"]
output_chart = "keyword_histogram.png"
titles = []
with open(input_csv) as f:
    for line in f:
        titles.append(line.strip())
counts = {}
for keyword in keywords:
    counts[keyword] = 0
for title in titles:
    cleaned_up_title = ""
    for char in title:
        if char.isalpha() or char == " ":
            cleaned_up_title = cleaned_up_title + char
        else:
            cleaned_up_title = cleaned_up_title + " "
    cleaned_up_title = cleaned_up_title.lower()
    words_in_title = cleaned_up_title.split()  # filter for exact words
    for keyword in keywords:
        counts[keyword] = counts[keyword] + words_in_title.count(keyword)  # exact equality match
values = []
for keyword in keywords:
    values.append(counts[keyword])
plt.figure()
plt.bar(keywords, values, color=["green", "blue", "orange"])
plt.title("Keyword Frequency in Article Titles")
plt.xlabel("Keyword")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(output_chart)
