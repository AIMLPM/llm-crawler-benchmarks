# Extraction Quality Comparison
<!-- style: v2, 2026-04-13 -->

**markcrawl** produces the cleanest Markdown for RAG: lowest preamble and highest content signal across all sites.

## Methodology

Four automated quality metrics — no LLM or human review needed:

1. **Junk phrases** — known boilerplate strings (nav, footer, breadcrumbs) found in output
2. **Preamble [2]** — average words per page appearing *before* the first heading.
   Nav chrome (version selectors, language pickers, prev/next links) lives here.
   A tool with a high preamble count is injecting site chrome into every chunk.
3. **Cross-page repeat rate** — fraction of sentences that appear on >50% of pages.
   Real content appears on at most a few pages; nav text repeats everywhere.
   High repeat rate = nav boilerplate polluting every chunk in the RAG index.
4. **Cross-tool consensus** — precision (how much output is agreed real content?)
   and recall (how much agreed content did this tool capture?).

> **Why preamble + repeat rate matter for RAG:** A tool that embeds 200 words of
> nav chrome before each article degrades retrieval in two ways: (1) chunks contain
> irrelevant tokens that dilute semantic similarity, and (2) the same nav sentences
> match queries on every page, flooding results with false positives.

## Summary: RAG readiness at a glance

For RAG pipelines, **clean output matters more than comprehensive output.**
A tool that includes 1,000 words of nav chrome per page pollutes every
chunk in the vector index, degrading retrieval for every query.

| Tool | Content signal [1] | Preamble [2] | Repeat rate [3] | Junk/page [4] | Precision [5] | Recall [5] |
|---|---|---|---|---|---|---|
| **markcrawl** | 99% | 15 | 0% | 0.5 | 99% | 64% |
| crawl4ai | 89% | 311 ⚠ | 1% | 3.2 | 100% | 66% |
| crawl4ai-raw | 89% | 311 ⚠ | 1% | 3.2 | 100% | 66% |
| scrapy+md | 95% | 133 ⚠ | 1% | 2.5 | 100% | 68% |
| crawlee | 66% | 2207 ⚠ | 1% | 3.8 | 94% | 97% |
| colly+md | 68% | 1953 ⚠ | 1% | 3.8 | 99% | 96% |
| playwright | 68% | 2037 ⚠ | 1% | 3.6 | 100% | 97% |
| firecrawl | — | — | — | — | — | — |

> **Column definitions:**
> **[1] Content signal** = (total words - preamble words) ÷ total words, per page average. Higher = cleaner output.
> **[2] Preamble** = avg words per page appearing *before* the first heading (nav chrome, breadcrumbs). Lower is better.
> **[3] Repeat rate** = fraction of sentences appearing on >50% of pages (boilerplate). Lower is better.
> **[4] Junk/page** = known boilerplate phrases (nav, footer, cookie banners) detected per page. Lower is better.
> **[5] Precision/Recall** = cross-tool consensus: precision measures how much output is agreed-upon content; recall measures how much agreed content was captured.


**Key takeaway:** markcrawl achieves 99% content signal with only 15 words of preamble per page — compared to 2207 for crawlee. Its recall is lower (64% vs 97%) because it strips nav, footer, and sponsor content that other tools include. For RAG use cases, this trade-off typically favors cleaner output: fewer junk tokens per chunk means better embedding quality and retrieval precision.


## quotes-toscrape

| Tool | Avg words [6] | Preamble [2] | Repeat rate [3] | Junk found [4] | Headings [7] | Code blocks [8] | Precision [5] | Recall [5] |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 214 | 15 | 0% | 0 | 0.9 | 0.0 | 100% | 100% |
| crawl4ai | 242 | 0 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| crawl4ai-raw | 242 | 0 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| scrapy+md | 242 | 0 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| crawlee | 245 | 3 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| colly+md | 245 | 3 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| playwright | 245 | 3 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| firecrawl | — | — | — | — | — | — | — | — |

> **Column definitions:**
> **[6] Avg words** = mean words per page. **[2] Preamble** = avg words per page before the first heading (nav chrome). **[3] Repeat rate** = fraction of sentences on >50% of pages.
> **[4] Junk found** = total known boilerplate phrases detected across all pages. **[7] Headings** = avg headings per page. **[8] Code blocks** = avg fenced code blocks per page.
> **[5] Precision/Recall** = cross-tool consensus (pages with <2 sentences excluded). **⚠** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

<details>
<summary>Sample output — first 40 lines of <code>quotes.toscrape.com/tag/books/page/1</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
### Viewing tag: [books](/tag/books/page/1/)

“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”
by Jane Austen
[(about)](/author/Jane-Austen)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

“I have always imagined that Paradise will be a kind of library.”
by Jorge Luis Borges
[(about)](/author/Jorge-Luis-Borges)

“You can never get a cup of tea large enough or a book long enough to suit me.”
by C.S. Lewis
[(about)](/author/C-S-Lewis)

“If you only read the books that everyone else is reading, you can only think what everyone else is thinking.”
by Haruki Murakami
[(about)](/author/Haruki-Murakami)

“There is no friend as loyal as a book.”
by Ernest Hemingway
[(about)](/author/Ernest-Hemingway)

“What really knocks me out is a book that, when you're all done reading it, you wish the author that wrote it was a terrific friend of yours and you could call him up on the phone whenever you felt like it. That doesn't happen much, though.”
by J.D. Salinger
[(about)](/author/J-D-Salinger)

“′Classic′ - a book which people praise and don't read.”
by Mark Twain
[(about)](/author/Mark-Twain)

“I declare after all there is no enjoyment like reading! How much sooner one tires of any thing than of a book! -- When I have a house of my own, I shall be miserable if I have not an excellent library.”
by Jane Austen
[(about)](/author/Jane-Austen)

“You have to write the book that wants to be written. And if the book will be too difficult for grown-ups, then you write it for children.”
by Madeleine L'Engle
```

**crawl4ai**
```
#  [Quotes to Scrape](https://quotes.toscrape.com/)
[Login](https://quotes.toscrape.com/login)
### Viewing tag: [books](https://quotes.toscrape.com/tag/books/page/1/)
“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.” by Jane Austen [(about)](https://quotes.toscrape.com/author/Jane-Austen)
Tags: [aliteracy](https://quotes.toscrape.com/tag/aliteracy/page/1/) [books](https://quotes.toscrape.com/tag/books/page/1/) [classic](https://quotes.toscrape.com/tag/classic/page/1/) [humor](https://quotes.toscrape.com/tag/humor/page/1/)
“Good friends, good books, and a sleepy conscience: this is the ideal life.” by Mark Twain [(about)](https://quotes.toscrape.com/author/Mark-Twain)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [contentment](https://quotes.toscrape.com/tag/contentment/page/1/) [friends](https://quotes.toscrape.com/tag/friends/page/1/) [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [life](https://quotes.toscrape.com/tag/life/page/1/)
“I have always imagined that Paradise will be a kind of library.” by Jorge Luis Borges [(about)](https://quotes.toscrape.com/author/Jorge-Luis-Borges)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [library](https://quotes.toscrape.com/tag/library/page/1/)
“You can never get a cup of tea large enough or a book long enough to suit me.” by C.S. Lewis [(about)](https://quotes.toscrape.com/author/C-S-Lewis)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [inspirational](https://quotes.toscrape.com/tag/inspirational/page/1/) [reading](https://quotes.toscrape.com/tag/reading/page/1/) [tea](https://quotes.toscrape.com/tag/tea/page/1/)
“If you only read the books that everyone else is reading, you can only think what everyone else is thinking.” by Haruki Murakami [(about)](https://quotes.toscrape.com/author/Haruki-Murakami)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [thought](https://quotes.toscrape.com/tag/thought/page/1/)
“There is no friend as loyal as a book.” by Ernest Hemingway [(about)](https://quotes.toscrape.com/author/Ernest-Hemingway)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [friends](https://quotes.toscrape.com/tag/friends/page/1/) [novelist-quotes](https://quotes.toscrape.com/tag/novelist-quotes/page/1/)
“What really knocks me out is a book that, when you're all done reading it, you wish the author that wrote it was a terrific friend of yours and you could call him up on the phone whenever you felt like it. That doesn't happen much, though.” by J.D. Salinger [(about)](https://quotes.toscrape.com/author/J-D-Salinger)
Tags: [authors](https://quotes.toscrape.com/tag/authors/page/1/) [books](https://quotes.toscrape.com/tag/books/page/1/) [literature](https://quotes.toscrape.com/tag/literature/page/1/) [reading](https://quotes.toscrape.com/tag/reading/page/1/) [writing](https://quotes.toscrape.com/tag/writing/page/1/)
“′Classic′ - a book which people praise and don't read.” by Mark Twain [(about)](https://quotes.toscrape.com/author/Mark-Twain)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [classic](https://quotes.toscrape.com/tag/classic/page/1/) [reading](https://quotes.toscrape.com/tag/reading/page/1/)
“I declare after all there is no enjoyment like reading! How much sooner one tires of any thing than of a book! -- When I have a house of my own, I shall be miserable if I have not an excellent library.” by Jane Austen [(about)](https://quotes.toscrape.com/author/Jane-Austen)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [library](https://quotes.toscrape.com/tag/library/page/1/) [reading](https://quotes.toscrape.com/tag/reading/page/1/)
“You have to write the book that wants to be written. And if the book will be too difficult for grown-ups, then you write it for children.” by Madeleine L'Engle [(about)](https://quotes.toscrape.com/author/Madeleine-LEngle)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [children](https://quotes.toscrape.com/tag/children/page/1/) [difficult](https://quotes.toscrape.com/tag/difficult/page/1/) [grown-ups](https://quotes.toscrape.com/tag/grown-ups/page/1/) [write](https://quotes.toscrape.com/tag/write/page/1/) [writers](https://quotes.toscrape.com/tag/writers/page/1/) [writing](https://quotes.toscrape.com/tag/writing/page/1/)
  * [Next →](https://quotes.toscrape.com/tag/books/page/2/)


## Top Ten tags
[love](https://quotes.toscrape.com/tag/love/) [inspirational](https://quotes.toscrape.com/tag/inspirational/) [life](https://quotes.toscrape.com/tag/life/) [humor](https://quotes.toscrape.com/tag/humor/) [books](https://quotes.toscrape.com/tag/books/) [reading](https://quotes.toscrape.com/tag/reading/) [friendship](https://quotes.toscrape.com/tag/friendship/) [friends](https://quotes.toscrape.com/tag/friends/) [truth](https://quotes.toscrape.com/tag/truth/) [simile](https://quotes.toscrape.com/tag/simile/)
Quotes by: [GoodReads.com](https://www.goodreads.com/quotes)
Made with ❤ by [Zyte](https://www.zyte.com)
```

**crawl4ai-raw**
```
#  [Quotes to Scrape](https://quotes.toscrape.com/)
[Login](https://quotes.toscrape.com/login)
### Viewing tag: [books](https://quotes.toscrape.com/tag/books/page/1/)
“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.” by Jane Austen [(about)](https://quotes.toscrape.com/author/Jane-Austen)
Tags: [aliteracy](https://quotes.toscrape.com/tag/aliteracy/page/1/) [books](https://quotes.toscrape.com/tag/books/page/1/) [classic](https://quotes.toscrape.com/tag/classic/page/1/) [humor](https://quotes.toscrape.com/tag/humor/page/1/)
“Good friends, good books, and a sleepy conscience: this is the ideal life.” by Mark Twain [(about)](https://quotes.toscrape.com/author/Mark-Twain)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [contentment](https://quotes.toscrape.com/tag/contentment/page/1/) [friends](https://quotes.toscrape.com/tag/friends/page/1/) [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [life](https://quotes.toscrape.com/tag/life/page/1/)
“I have always imagined that Paradise will be a kind of library.” by Jorge Luis Borges [(about)](https://quotes.toscrape.com/author/Jorge-Luis-Borges)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [library](https://quotes.toscrape.com/tag/library/page/1/)
“You can never get a cup of tea large enough or a book long enough to suit me.” by C.S. Lewis [(about)](https://quotes.toscrape.com/author/C-S-Lewis)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [inspirational](https://quotes.toscrape.com/tag/inspirational/page/1/) [reading](https://quotes.toscrape.com/tag/reading/page/1/) [tea](https://quotes.toscrape.com/tag/tea/page/1/)
“If you only read the books that everyone else is reading, you can only think what everyone else is thinking.” by Haruki Murakami [(about)](https://quotes.toscrape.com/author/Haruki-Murakami)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [thought](https://quotes.toscrape.com/tag/thought/page/1/)
“There is no friend as loyal as a book.” by Ernest Hemingway [(about)](https://quotes.toscrape.com/author/Ernest-Hemingway)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [friends](https://quotes.toscrape.com/tag/friends/page/1/) [novelist-quotes](https://quotes.toscrape.com/tag/novelist-quotes/page/1/)
“What really knocks me out is a book that, when you're all done reading it, you wish the author that wrote it was a terrific friend of yours and you could call him up on the phone whenever you felt like it. That doesn't happen much, though.” by J.D. Salinger [(about)](https://quotes.toscrape.com/author/J-D-Salinger)
Tags: [authors](https://quotes.toscrape.com/tag/authors/page/1/) [books](https://quotes.toscrape.com/tag/books/page/1/) [literature](https://quotes.toscrape.com/tag/literature/page/1/) [reading](https://quotes.toscrape.com/tag/reading/page/1/) [writing](https://quotes.toscrape.com/tag/writing/page/1/)
“′Classic′ - a book which people praise and don't read.” by Mark Twain [(about)](https://quotes.toscrape.com/author/Mark-Twain)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [classic](https://quotes.toscrape.com/tag/classic/page/1/) [reading](https://quotes.toscrape.com/tag/reading/page/1/)
“I declare after all there is no enjoyment like reading! How much sooner one tires of any thing than of a book! -- When I have a house of my own, I shall be miserable if I have not an excellent library.” by Jane Austen [(about)](https://quotes.toscrape.com/author/Jane-Austen)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [library](https://quotes.toscrape.com/tag/library/page/1/) [reading](https://quotes.toscrape.com/tag/reading/page/1/)
“You have to write the book that wants to be written. And if the book will be too difficult for grown-ups, then you write it for children.” by Madeleine L'Engle [(about)](https://quotes.toscrape.com/author/Madeleine-LEngle)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [children](https://quotes.toscrape.com/tag/children/page/1/) [difficult](https://quotes.toscrape.com/tag/difficult/page/1/) [grown-ups](https://quotes.toscrape.com/tag/grown-ups/page/1/) [write](https://quotes.toscrape.com/tag/write/page/1/) [writers](https://quotes.toscrape.com/tag/writers/page/1/) [writing](https://quotes.toscrape.com/tag/writing/page/1/)
  * [Next →](https://quotes.toscrape.com/tag/books/page/2/)


## Top Ten tags
[love](https://quotes.toscrape.com/tag/love/) [inspirational](https://quotes.toscrape.com/tag/inspirational/) [life](https://quotes.toscrape.com/tag/life/) [humor](https://quotes.toscrape.com/tag/humor/) [books](https://quotes.toscrape.com/tag/books/) [reading](https://quotes.toscrape.com/tag/reading/) [friendship](https://quotes.toscrape.com/tag/friendship/) [friends](https://quotes.toscrape.com/tag/friends/) [truth](https://quotes.toscrape.com/tag/truth/) [simile](https://quotes.toscrape.com/tag/simile/)
Quotes by: [GoodReads.com](https://www.goodreads.com/quotes)
Made with ❤ by [Zyte](https://www.zyte.com)
```

**scrapy+md**
```
# [Quotes to Scrape](/)

[Login](/login)

### Viewing tag: [books](/tag/books/page/1/)

“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”
by Jane Austen
[(about)](/author/Jane-Austen)

Tags:
[aliteracy](/tag/aliteracy/page/1/)
[books](/tag/books/page/1/)
[classic](/tag/classic/page/1/)
[humor](/tag/humor/page/1/)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

Tags:
[books](/tag/books/page/1/)
[contentment](/tag/contentment/page/1/)
[friends](/tag/friends/page/1/)
[friendship](/tag/friendship/page/1/)
[life](/tag/life/page/1/)

“I have always imagined that Paradise will be a kind of library.”
by Jorge Luis Borges
[(about)](/author/Jorge-Luis-Borges)

Tags:
[books](/tag/books/page/1/)
[library](/tag/library/page/1/)

“You can never get a cup of tea large enough or a book long enough to suit me.”
by C.S. Lewis
[(about)](/author/C-S-Lewis)

Tags:
```

**crawlee**
```
Quotes to Scrape



# [Quotes to Scrape](/)

[Login](/login)

### Viewing tag: [books](/tag/books/page/1/)

“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”
by Jane Austen
[(about)](/author/Jane-Austen)

Tags:
[aliteracy](/tag/aliteracy/page/1/)
[books](/tag/books/page/1/)
[classic](/tag/classic/page/1/)
[humor](/tag/humor/page/1/)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

Tags:
[books](/tag/books/page/1/)
[contentment](/tag/contentment/page/1/)
[friends](/tag/friends/page/1/)
[friendship](/tag/friendship/page/1/)
[life](/tag/life/page/1/)

“I have always imagined that Paradise will be a kind of library.”
by Jorge Luis Borges
[(about)](/author/Jorge-Luis-Borges)

Tags:
[books](/tag/books/page/1/)
[library](/tag/library/page/1/)

“You can never get a cup of tea large enough or a book long enough to suit me.”
```

**colly+md**
```
Quotes to Scrape



# [Quotes to Scrape](/)

[Login](/login)

### Viewing tag: [books](/tag/books/page/1/)

“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”
by Jane Austen
[(about)](/author/Jane-Austen)

Tags:
[aliteracy](/tag/aliteracy/page/1/)
[books](/tag/books/page/1/)
[classic](/tag/classic/page/1/)
[humor](/tag/humor/page/1/)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

Tags:
[books](/tag/books/page/1/)
[contentment](/tag/contentment/page/1/)
[friends](/tag/friends/page/1/)
[friendship](/tag/friendship/page/1/)
[life](/tag/life/page/1/)

“I have always imagined that Paradise will be a kind of library.”
by Jorge Luis Borges
[(about)](/author/Jorge-Luis-Borges)

Tags:
[books](/tag/books/page/1/)
[library](/tag/library/page/1/)

“You can never get a cup of tea large enough or a book long enough to suit me.”
```

**playwright**
```
Quotes to Scrape



# [Quotes to Scrape](/)

[Login](/login)

### Viewing tag: [books](/tag/books/page/1/)

“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”
by Jane Austen
[(about)](/author/Jane-Austen)

Tags:
[aliteracy](/tag/aliteracy/page/1/)
[books](/tag/books/page/1/)
[classic](/tag/classic/page/1/)
[humor](/tag/humor/page/1/)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

Tags:
[books](/tag/books/page/1/)
[contentment](/tag/contentment/page/1/)
[friends](/tag/friends/page/1/)
[friendship](/tag/friendship/page/1/)
[life](/tag/life/page/1/)

“I have always imagined that Paradise will be a kind of library.”
by Jorge Luis Borges
[(about)](/author/Jorge-Luis-Borges)

Tags:
[books](/tag/books/page/1/)
[library](/tag/library/page/1/)

“You can never get a cup of tea large enough or a book long enough to suit me.”
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [2]</summary>

| URL | markcrawl words [6] / preamble [2] | crawl4ai words [6] / preamble [2] | crawl4ai-raw words [6] / preamble [2] | scrapy+md words [6] / preamble [2] | crawlee words [6] / preamble [2] | colly+md words [6] / preamble [2] | playwright words [6] / preamble [2] | firecrawl words [6] / preamble [2] |
|---|---|---|---|---|---|---|---|---|
| quotes.toscrape.com | 212 / 212 | 282 / 0 | 282 / 0 | 282 / 0 | 285 / 3 | 285 / 3 | 285 / 3 | — |
| quotes.toscrape.com/author/Albert-Einstein | 616 / 0 | 629 / 0 | 629 / 0 | 629 / 0 | 632 / 3 | 632 / 3 | 632 / 3 | — |
| quotes.toscrape.com/author/Eleanor-Roosevelt | 237 / 0 | 250 / 0 | 250 / 0 | 250 / 0 | 253 / 3 | 253 / 3 | 253 / 3 | — |
| quotes.toscrape.com/author/Steve-Martin | 134 / 0 | 147 / 0 | 147 / 0 | 147 / 0 | 150 / 3 | 150 / 3 | 150 / 3 | — |
| quotes.toscrape.com/tag/abilities/page/1 | 24 / 0 | 54 / 0 | 54 / 0 | 54 / 0 | 57 / 3 | 57 / 3 | 57 / 3 | — |
| quotes.toscrape.com/tag/aliteracy/page/1 | 27 / 0 | 59 / 0 | 59 / 0 | 59 / 0 | 62 / 3 | 62 / 3 | 62 / 3 | — |
| quotes.toscrape.com/tag/books/page/1 | 262 / 0 | 340 / 0 | 340 / 0 | 340 / 0 | 343 / 3 | 343 / 3 | 343 / 3 | — |
| quotes.toscrape.com/tag/change/page/1 | 29 / 0 | 61 / 0 | 61 / 0 | 61 / 0 | 64 / 3 | 64 / 3 | 64 / 3 | — |
| quotes.toscrape.com/tag/choices/page/1 | 24 / 0 | 54 / 0 | 54 / 0 | 54 / 0 | 57 / 3 | 57 / 3 | 57 / 3 | — |
| quotes.toscrape.com/tag/edison/page/1 | — | 53 / 0 | 53 / 0 | 53 / 0 | 56 / 3 | 56 / 3 | 56 / 3 | — |
| quotes.toscrape.com/tag/friendship | 118 / 0 | 166 / 0 | 166 / 0 | 166 / 0 | 169 / 3 | 169 / 3 | 169 / 3 | — |
| quotes.toscrape.com/tag/life | 434 / 0 | 509 / 0 | 509 / 0 | 509 / 0 | 512 / 3 | 512 / 3 | 512 / 3 | — |
| quotes.toscrape.com/tag/love/page/1 | 619 / 0 | 684 / 0 | 684 / 0 | 684 / 0 | 687 / 3 | 687 / 3 | 687 / 3 | — |
| quotes.toscrape.com/tag/reading | 197 / 0 | 255 / 0 | 255 / 0 | 255 / 0 | 258 / 3 | 258 / 3 | 258 / 3 | — |
| quotes.toscrape.com/tag/thinking/page/1 | 57 / 0 | 93 / 0 | 93 / 0 | 93 / 0 | 96 / 3 | 96 / 3 | 96 / 3 | — |

</details>

## books-toscrape

| Tool | Avg words [6] | Preamble [2] | Repeat rate [3] | Junk found [4] | Headings [7] | Code blocks [8] | Precision [5] | Recall [5] |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 339 | 66 ⚠ | 0% | 0 | 1.8 | 0.0 | 100% | 99% |
| crawl4ai | 493 | 178 ⚠ | 2% | 0 | 10.7 | 0.0 | 100% | 99% |
| crawl4ai-raw | 493 | 178 ⚠ | 2% | 0 | 10.7 | 0.0 | 100% | 99% |
| scrapy+md | 387 | 101 ⚠ | 1% | 0 | 1.8 | 0.0 | 100% | 99% |
| crawlee | 395 | 110 ⚠ | 1% | 0 | 1.8 | 0.0 | 100% | 100% |
| colly+md | 395 | 110 ⚠ | 1% | 0 | 1.8 | 0.0 | 100% | 100% |
| playwright | 395 | 110 ⚠ | 1% | 0 | 1.8 | 0.0 | 100% | 100% |
| firecrawl | — | — | — | — | — | — | — | — |

> **Column definitions:**
> **[6] Avg words** = mean words per page. **[2] Preamble** = avg words per page before the first heading (nav chrome). **[3] Repeat rate** = fraction of sentences on >50% of pages.
> **[4] Junk found** = total known boilerplate phrases detected across all pages. **[7] Headings** = avg headings per page. **[8] Code blocks** = avg fenced code blocks per page.
> **[5] Precision/Recall** = cross-tool consensus (pages with <2 sentences excluded). **⚠** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
The word count gap (339 vs 493 avg words) is largely explained by preamble: 178 words of nav chrome account for ~36% of crawl4ai's output on this site.

<details>
<summary>Sample output — first 40 lines of <code>books.toscrape.com/catalogue/category/books/autobiography_27/index.html</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
# Autobiography


**9** results.

**Warning!** This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.

1. ### [The Argonauts](../../../the-argonauts_837/index.html "The Argonauts")

   £10.93

   In stock

   Add to basket
2. ### [M Train](../../../m-train_598/index.html "M Train")

   £27.18

   In stock

   Add to basket
3. ### [Lab Girl](../../../lab-girl_595/index.html "Lab Girl")

   £40.85

   In stock

   Add to basket
4. ### [Approval Junkie: Adventures in ...](../../../approval-junkie-adventures-in-caring-too-much_363/index.html "Approval Junkie: Adventures in Caring Too Much")

   £58.81

   In stock

   Add to basket
5. ### [Running with Scissors](../../../running-with-scissors_215/index.html "Running with Scissors")

   £12.91

   In stock
```

**crawl4ai**
```
[Books to Scrape](https://books.toscrape.com/index.html) We love being scraped!
  * [Home](https://books.toscrape.com/index.html)
  * [Books](https://books.toscrape.com/catalogue/category/books_1/index.html)
  * Autobiography


  * [ Books ](https://books.toscrape.com/catalogue/category/books_1/index.html)
    * [ Travel ](https://books.toscrape.com/catalogue/category/books/travel_2/index.html)
    * [ Mystery ](https://books.toscrape.com/catalogue/category/books/mystery_3/index.html)
    * [ Historical Fiction ](https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html)
    * [ Sequential Art ](https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html)
    * [ Classics ](https://books.toscrape.com/catalogue/category/books/classics_6/index.html)
    * [ Philosophy ](https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html)
    * [ Romance ](https://books.toscrape.com/catalogue/category/books/romance_8/index.html)
    * [ Womens Fiction ](https://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html)
    * [ Fiction ](https://books.toscrape.com/catalogue/category/books/fiction_10/index.html)
    * [ Childrens ](https://books.toscrape.com/catalogue/category/books/childrens_11/index.html)
    * [ Religion ](https://books.toscrape.com/catalogue/category/books/religion_12/index.html)
    * [ Nonfiction ](https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html)
    * [ Music ](https://books.toscrape.com/catalogue/category/books/music_14/index.html)
    * [ Default ](https://books.toscrape.com/catalogue/category/books/default_15/index.html)
    * [ Science Fiction ](https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html)
    * [ Sports and Games ](https://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html)
    * [ Add a comment ](https://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html)
    * [ Fantasy ](https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html)
    * [ New Adult ](https://books.toscrape.com/catalogue/category/books/new-adult_20/index.html)
    * [ Young Adult ](https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html)
    * [ Science ](https://books.toscrape.com/catalogue/category/books/science_22/index.html)
    * [ Poetry ](https://books.toscrape.com/catalogue/category/books/poetry_23/index.html)
    * [ Paranormal ](https://books.toscrape.com/catalogue/category/books/paranormal_24/index.html)
    * [ Art ](https://books.toscrape.com/catalogue/category/books/art_25/index.html)
    * [ Psychology ](https://books.toscrape.com/catalogue/category/books/psychology_26/index.html)
    * [ **Autobiography** ](https://books.toscrape.com/catalogue/category/books/autobiography_27/index.html)
    * [ Parenting ](https://books.toscrape.com/catalogue/category/books/parenting_28/index.html)
    * [ Adult Fiction ](https://books.toscrape.com/catalogue/category/books/adult-fiction_29/index.html)
    * [ Humor ](https://books.toscrape.com/catalogue/category/books/humor_30/index.html)
    * [ Horror ](https://books.toscrape.com/catalogue/category/books/horror_31/index.html)
    * [ History ](https://books.toscrape.com/catalogue/category/books/history_32/index.html)
    * [ Food and Drink ](https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html)
    * [ Christian Fiction ](https://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html)
```

**crawl4ai-raw**
```
[Books to Scrape](https://books.toscrape.com/index.html) We love being scraped!
  * [Home](https://books.toscrape.com/index.html)
  * [Books](https://books.toscrape.com/catalogue/category/books_1/index.html)
  * Autobiography


  * [ Books ](https://books.toscrape.com/catalogue/category/books_1/index.html)
    * [ Travel ](https://books.toscrape.com/catalogue/category/books/travel_2/index.html)
    * [ Mystery ](https://books.toscrape.com/catalogue/category/books/mystery_3/index.html)
    * [ Historical Fiction ](https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html)
    * [ Sequential Art ](https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html)
    * [ Classics ](https://books.toscrape.com/catalogue/category/books/classics_6/index.html)
    * [ Philosophy ](https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html)
    * [ Romance ](https://books.toscrape.com/catalogue/category/books/romance_8/index.html)
    * [ Womens Fiction ](https://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html)
    * [ Fiction ](https://books.toscrape.com/catalogue/category/books/fiction_10/index.html)
    * [ Childrens ](https://books.toscrape.com/catalogue/category/books/childrens_11/index.html)
    * [ Religion ](https://books.toscrape.com/catalogue/category/books/religion_12/index.html)
    * [ Nonfiction ](https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html)
    * [ Music ](https://books.toscrape.com/catalogue/category/books/music_14/index.html)
    * [ Default ](https://books.toscrape.com/catalogue/category/books/default_15/index.html)
    * [ Science Fiction ](https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html)
    * [ Sports and Games ](https://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html)
    * [ Add a comment ](https://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html)
    * [ Fantasy ](https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html)
    * [ New Adult ](https://books.toscrape.com/catalogue/category/books/new-adult_20/index.html)
    * [ Young Adult ](https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html)
    * [ Science ](https://books.toscrape.com/catalogue/category/books/science_22/index.html)
    * [ Poetry ](https://books.toscrape.com/catalogue/category/books/poetry_23/index.html)
    * [ Paranormal ](https://books.toscrape.com/catalogue/category/books/paranormal_24/index.html)
    * [ Art ](https://books.toscrape.com/catalogue/category/books/art_25/index.html)
    * [ Psychology ](https://books.toscrape.com/catalogue/category/books/psychology_26/index.html)
    * [ **Autobiography** ](https://books.toscrape.com/catalogue/category/books/autobiography_27/index.html)
    * [ Parenting ](https://books.toscrape.com/catalogue/category/books/parenting_28/index.html)
    * [ Adult Fiction ](https://books.toscrape.com/catalogue/category/books/adult-fiction_29/index.html)
    * [ Humor ](https://books.toscrape.com/catalogue/category/books/humor_30/index.html)
    * [ Horror ](https://books.toscrape.com/catalogue/category/books/horror_31/index.html)
    * [ History ](https://books.toscrape.com/catalogue/category/books/history_32/index.html)
    * [ Food and Drink ](https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html)
    * [ Christian Fiction ](https://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html)
```

**scrapy+md**
```
[Books to Scrape](../../../../index.html) We love being scraped!

* [Home](../../../../index.html)
* [Books](../../books_1/index.html)
* Autobiography

* [Books](../../books_1/index.html)
  + [Travel](../travel_2/index.html)
  + [Mystery](../mystery_3/index.html)
  + [Historical Fiction](../historical-fiction_4/index.html)
  + [Sequential Art](../sequential-art_5/index.html)
  + [Classics](../classics_6/index.html)
  + [Philosophy](../philosophy_7/index.html)
  + [Romance](../romance_8/index.html)
  + [Womens Fiction](../womens-fiction_9/index.html)
  + [Fiction](../fiction_10/index.html)
  + [Childrens](../childrens_11/index.html)
  + [Religion](../religion_12/index.html)
  + [Nonfiction](../nonfiction_13/index.html)
  + [Music](../music_14/index.html)
  + [Default](../default_15/index.html)
  + [Science Fiction](../science-fiction_16/index.html)
  + [Sports and Games](../sports-and-games_17/index.html)
  + [Add a comment](../add-a-comment_18/index.html)
  + [Fantasy](../fantasy_19/index.html)
  + [New Adult](../new-adult_20/index.html)
  + [Young Adult](../young-adult_21/index.html)
  + [Science](../science_22/index.html)
  + [Poetry](../poetry_23/index.html)
  + [Paranormal](../paranormal_24/index.html)
  + [Art](../art_25/index.html)
  + [Psychology](../psychology_26/index.html)
  + [**Autobiography**](index.html)
  + [Parenting](../parenting_28/index.html)
  + [Adult Fiction](../adult-fiction_29/index.html)
  + [Humor](../humor_30/index.html)
  + [Horror](../horror_31/index.html)
  + [History](../history_32/index.html)
  + [Food and Drink](../food-and-drink_33/index.html)
  + [Christian Fiction](../christian-fiction_34/index.html)
```

**crawlee**
```
Autobiography |
Books to Scrape - Sandbox




[Books to Scrape](../../../../index.html) We love being scraped!

* [Home](../../../../index.html)
* [Books](../../books_1/index.html)
* Autobiography

* [Books](../../books_1/index.html)
  + [Travel](../travel_2/index.html)
  + [Mystery](../mystery_3/index.html)
  + [Historical Fiction](../historical-fiction_4/index.html)
  + [Sequential Art](../sequential-art_5/index.html)
  + [Classics](../classics_6/index.html)
  + [Philosophy](../philosophy_7/index.html)
  + [Romance](../romance_8/index.html)
  + [Womens Fiction](../womens-fiction_9/index.html)
  + [Fiction](../fiction_10/index.html)
  + [Childrens](../childrens_11/index.html)
  + [Religion](../religion_12/index.html)
  + [Nonfiction](../nonfiction_13/index.html)
  + [Music](../music_14/index.html)
  + [Default](../default_15/index.html)
  + [Science Fiction](../science-fiction_16/index.html)
  + [Sports and Games](../sports-and-games_17/index.html)
  + [Add a comment](../add-a-comment_18/index.html)
  + [Fantasy](../fantasy_19/index.html)
  + [New Adult](../new-adult_20/index.html)
  + [Young Adult](../young-adult_21/index.html)
  + [Science](../science_22/index.html)
  + [Poetry](../poetry_23/index.html)
  + [Paranormal](../paranormal_24/index.html)
  + [Art](../art_25/index.html)
  + [Psychology](../psychology_26/index.html)
  + [**Autobiography**](index.html)
  + [Parenting](../parenting_28/index.html)
```

**colly+md**
```
  


Autobiography |
Books to Scrape - Sandbox




[Books to Scrape](../../../../index.html) We love being scraped!

* [Home](../../../../index.html)
* [Books](../../books_1/index.html)
* Autobiography

* [Books](../../books_1/index.html)
  + [Travel](../travel_2/index.html)
  + [Mystery](../mystery_3/index.html)
  + [Historical Fiction](../historical-fiction_4/index.html)
  + [Sequential Art](../sequential-art_5/index.html)
  + [Classics](../classics_6/index.html)
  + [Philosophy](../philosophy_7/index.html)
  + [Romance](../romance_8/index.html)
  + [Womens Fiction](../womens-fiction_9/index.html)
  + [Fiction](../fiction_10/index.html)
  + [Childrens](../childrens_11/index.html)
  + [Religion](../religion_12/index.html)
  + [Nonfiction](../nonfiction_13/index.html)
  + [Music](../music_14/index.html)
  + [Default](../default_15/index.html)
  + [Science Fiction](../science-fiction_16/index.html)
  + [Sports and Games](../sports-and-games_17/index.html)
  + [Add a comment](../add-a-comment_18/index.html)
  + [Fantasy](../fantasy_19/index.html)
  + [New Adult](../new-adult_20/index.html)
  + [Young Adult](../young-adult_21/index.html)
  + [Science](../science_22/index.html)
  + [Poetry](../poetry_23/index.html)
  + [Paranormal](../paranormal_24/index.html)
  + [Art](../art_25/index.html)
```

**playwright**
```
Autobiography |
Books to Scrape - Sandbox




[Books to Scrape](../../../../index.html) We love being scraped!

* [Home](../../../../index.html)
* [Books](../../books_1/index.html)
* Autobiography

* [Books](../../books_1/index.html)
  + [Travel](../travel_2/index.html)
  + [Mystery](../mystery_3/index.html)
  + [Historical Fiction](../historical-fiction_4/index.html)
  + [Sequential Art](../sequential-art_5/index.html)
  + [Classics](../classics_6/index.html)
  + [Philosophy](../philosophy_7/index.html)
  + [Romance](../romance_8/index.html)
  + [Womens Fiction](../womens-fiction_9/index.html)
  + [Fiction](../fiction_10/index.html)
  + [Childrens](../childrens_11/index.html)
  + [Religion](../religion_12/index.html)
  + [Nonfiction](../nonfiction_13/index.html)
  + [Music](../music_14/index.html)
  + [Default](../default_15/index.html)
  + [Science Fiction](../science-fiction_16/index.html)
  + [Sports and Games](../sports-and-games_17/index.html)
  + [Add a comment](../add-a-comment_18/index.html)
  + [Fantasy](../fantasy_19/index.html)
  + [New Adult](../new-adult_20/index.html)
  + [Young Adult](../young-adult_21/index.html)
  + [Science](../science_22/index.html)
  + [Poetry](../poetry_23/index.html)
  + [Paranormal](../paranormal_24/index.html)
  + [Art](../art_25/index.html)
  + [Psychology](../psychology_26/index.html)
  + [**Autobiography**](index.html)
  + [Parenting](../parenting_28/index.html)
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [2]</summary>

| URL | markcrawl words [6] / preamble [2] | crawl4ai words [6] / preamble [2] | crawl4ai-raw words [6] / preamble [2] | scrapy+md words [6] / preamble [2] | crawlee words [6] / preamble [2] | colly+md words [6] / preamble [2] | playwright words [6] / preamble [2] | firecrawl words [6] / preamble [2] |
|---|---|---|---|---|---|---|---|---|
| books.toscrape.com | 397 / 5 | 702 / 232 | 702 / 232 | 531 / 130 | 539 / 138 | 539 / 138 | 539 / 138 | — |
| books.toscrape.com/catalogue/category/books/academic_40 | 32 / 6 | 282 / 233 | 282 / 233 | 185 / 131 | 192 / 138 | 192 / 138 | 192 / 138 | — |
| books.toscrape.com/catalogue/category/books/add-a-comme | 424 / 8 | 745 / 235 | 745 / 235 | 558 / 133 | 567 / 142 | 567 / 142 | 567 / 142 | — |
| books.toscrape.com/catalogue/category/books/adult-ficti | 34 / 7 | 284 / 234 | 284 / 234 | 187 / 132 | 195 / 140 | 195 / 140 | 195 / 140 | — |
| books.toscrape.com/catalogue/category/books/art_25/inde | 163 / 0 | 422 / 233 | 422 / 233 | 303 / 131 | 310 / 138 | 310 / 138 | 310 / 138 | — |
| books.toscrape.com/catalogue/category/books/autobiograp | 163 / 0 | 412 / 233 | 412 / 233 | 303 / 131 | 310 / 138 | 310 / 138 | 310 / 138 | — |
| books.toscrape.com/catalogue/category/books/biography_3 | 32 / 6 | 410 / 233 | 410 / 233 | 279 / 131 | 286 / 138 | 286 / 138 | 286 / 138 | — |
| books.toscrape.com/catalogue/category/books/business_35 | 290 / 0 | 612 / 233 | 612 / 233 | 430 / 131 | 437 / 138 | 437 / 138 | 437 / 138 | — |
| books.toscrape.com/catalogue/category/books/childrens_1 | 360 / 0 | 642 / 233 | 642 / 233 | 500 / 131 | 507 / 138 | 507 / 138 | 507 / 138 | — |
| books.toscrape.com/catalogue/category/books/christian-f | 140 / 7 | 388 / 234 | 388 / 234 | 274 / 132 | 282 / 140 | 282 / 140 | 282 / 140 | — |
| books.toscrape.com/catalogue/category/books/christian_4 | 32 / 6 | 342 / 233 | 342 / 233 | 230 / 131 | 237 / 138 | 237 / 138 | 237 / 138 | — |
| books.toscrape.com/catalogue/category/books/classics_6/ | 320 / 0 | 593 / 233 | 593 / 233 | 460 / 131 | 467 / 138 | 467 / 138 | 467 / 138 | — |
| books.toscrape.com/catalogue/category/books/contemporar | 78 / 0 | 320 / 233 | 320 / 233 | 218 / 131 | 225 / 138 | 225 / 138 | 225 / 138 | — |
| books.toscrape.com/catalogue/category/books/crime_51/in | 52 / 0 | 296 / 233 | 296 / 233 | 192 / 131 | 199 / 138 | 199 / 138 | 199 / 138 | — |
| books.toscrape.com/catalogue/category/books/cultural_49 | 40 / 0 | 274 / 233 | 274 / 233 | 180 / 131 | 187 / 138 | 187 / 138 | 187 / 138 | — |
| books.toscrape.com/catalogue/category/books/default_15/ | 433 / 0 | 777 / 233 | 777 / 233 | 573 / 131 | 580 / 138 | 580 / 138 | 580 / 138 | — |
| books.toscrape.com/catalogue/category/books/erotica_50/ | 38 / 0 | 271 / 233 | 271 / 233 | 178 / 131 | 185 / 138 | 185 / 138 | 185 / 138 | — |
| books.toscrape.com/catalogue/category/books/fantasy_19/ | 430 / 0 | 764 / 233 | 764 / 233 | 570 / 131 | 577 / 138 | 577 / 138 | 577 / 138 | — |
| books.toscrape.com/catalogue/category/books/fiction_10/ | 359 / 0 | 636 / 233 | 636 / 233 | 499 / 131 | 506 / 138 | 506 / 138 | 506 / 138 | — |
| books.toscrape.com/catalogue/category/books/food-and-dr | 548 / 8 | 978 / 235 | 978 / 235 | 682 / 133 | 691 / 142 | 691 / 142 | 691 / 142 | — |
| books.toscrape.com/catalogue/category/books/health_47/i | 118 / 0 | 384 / 233 | 384 / 233 | 258 / 131 | 265 / 138 | 265 / 138 | 265 / 138 | — |
| books.toscrape.com/catalogue/category/books/historical_ | 69 / 0 | 315 / 233 | 315 / 233 | 209 / 131 | 216 / 138 | 216 / 138 | 216 / 138 | — |
| books.toscrape.com/catalogue/category/books/horror_31/i | 269 / 0 | 524 / 233 | 524 / 233 | 409 / 131 | 416 / 138 | 416 / 138 | 416 / 138 | — |
| books.toscrape.com/catalogue/category/books/humor_30/in | 233 / 0 | 529 / 233 | 529 / 233 | 373 / 131 | 380 / 138 | 380 / 138 | 380 / 138 | — |
| books.toscrape.com/catalogue/category/books/music_14/in | 298 / 0 | 616 / 233 | 616 / 233 | 438 / 131 | 445 / 138 | 445 / 138 | 445 / 138 | — |
| books.toscrape.com/catalogue/category/books/mystery_3/i | 401 / 0 | 710 / 233 | 710 / 233 | 541 / 131 | 548 / 138 | 548 / 138 | 548 / 138 | — |
| books.toscrape.com/catalogue/category/books/new-adult_2 | 130 / 7 | 370 / 234 | 370 / 234 | 264 / 132 | 272 / 140 | 272 / 140 | 272 / 140 | — |
| books.toscrape.com/catalogue/category/books/novels_46/i | 32 / 6 | 286 / 233 | 286 / 233 | 187 / 131 | 194 / 138 | 194 / 138 | 194 / 138 | — |
| books.toscrape.com/catalogue/category/books/parenting_2 | 32 / 6 | 286 / 233 | 286 / 233 | 187 / 131 | 194 / 138 | 194 / 138 | 194 / 138 | — |
| books.toscrape.com/catalogue/category/books/poetry_23/i | 349 / 0 | 642 / 233 | 642 / 233 | 489 / 131 | 496 / 138 | 496 / 138 | 496 / 138 | — |
| books.toscrape.com/catalogue/category/books/politics_48 | 88 / 0 | 340 / 233 | 340 / 233 | 228 / 131 | 235 / 138 | 235 / 138 | 235 / 138 | — |
| books.toscrape.com/catalogue/category/books/psychology_ | 178 / 0 | 460 / 233 | 460 / 233 | 318 / 131 | 325 / 138 | 325 / 138 | 325 / 138 | — |
| books.toscrape.com/catalogue/category/books/science-fic | 322 / 7 | 615 / 234 | 615 / 234 | 456 / 132 | 464 / 140 | 464 / 140 | 464 / 140 | — |
| books.toscrape.com/catalogue/category/books/science_22/ | 344 / 0 | 690 / 233 | 690 / 233 | 484 / 131 | 491 / 138 | 491 / 138 | 491 / 138 | — |
| books.toscrape.com/catalogue/category/books/short-stori | 39 / 0 | 273 / 234 | 273 / 234 | 180 / 132 | 188 / 140 | 188 / 140 | 188 / 140 | — |
| books.toscrape.com/catalogue/category/books/spiritualit | 165 / 0 | 447 / 233 | 447 / 233 | 305 / 131 | 312 / 138 | 312 / 138 | 312 / 138 | — |
| books.toscrape.com/catalogue/category/books/sports-and- | 137 / 8 | 391 / 235 | 391 / 235 | 271 / 133 | 280 / 142 | 280 / 142 | 280 / 142 | — |
| books.toscrape.com/catalogue/category/books/suspense_44 | 46 / 0 | 284 / 233 | 284 / 233 | 186 / 131 | 193 / 138 | 193 / 138 | 193 / 138 | — |
| books.toscrape.com/catalogue/category/books/thriller_37 | 205 / 0 | 465 / 233 | 465 / 233 | 345 / 131 | 352 / 138 | 352 / 138 | 352 / 138 | — |
| books.toscrape.com/catalogue/category/books/travel_2/in | 252 / 0 | 550 / 233 | 550 / 233 | 392 / 131 | 399 / 138 | 399 / 138 | 399 / 138 | — |
| books.toscrape.com/catalogue/category/books/womens-fict | 330 / 7 | 614 / 234 | 614 / 234 | 464 / 132 | 472 / 140 | 472 / 140 | 472 / 140 | — |
| books.toscrape.com/catalogue/category/books/young-adult | 386 / 7 | 676 / 234 | 676 / 234 | 520 / 132 | 528 / 140 | 528 / 140 | 528 / 140 | — |
| books.toscrape.com/catalogue/category/books_1/index.htm | 391 / 0 | 700 / 231 | 700 / 231 | 529 / 129 | 536 / 136 | 536 / 136 | 536 / 136 | — |
| books.toscrape.com/catalogue/its-only-the-himalayas_981 | 667 / 230 | 480 / 22 | 480 / 22 | 463 / 18 | 473 / 28 | 473 / 28 | 473 / 28 | — |
| books.toscrape.com/catalogue/libertarianism-for-beginne | 596 / 195 | 442 / 20 | 442 / 20 | 426 / 17 | 435 / 26 | 435 / 26 | 435 / 26 | — |
| books.toscrape.com/catalogue/olio_984/index.html | 703 / 249 | 491 / 16 | 491 / 16 | 477 / 15 | 484 / 22 | 484 / 22 | 484 / 22 | — |
| books.toscrape.com/catalogue/our-band-could-be-your-lif | 531 / 163 | 419 / 40 | 419 / 40 | 403 / 27 | 422 / 46 | 422 / 46 | 422 / 46 | — |
| books.toscrape.com/catalogue/page-2.html | 413 / 5 | 726 / 232 | 726 / 232 | 547 / 130 | 555 / 138 | 555 / 138 | 555 / 138 | — |
| books.toscrape.com/catalogue/sapiens-a-brief-history-of | 761 / 304 | 481 / 26 | 481 / 26 | 485 / 20 | 497 / 32 | 497 / 32 | 497 / 32 | — |
| books.toscrape.com/catalogue/scott-pilgrims-precious-li | 515 / 148 | 428 / 31 | 428 / 31 | 398 / 23 | 412 / 37 | 412 / 37 | 412 / 37 | — |
| books.toscrape.com/catalogue/set-me-free_988/index.html | 486 / 132 | 411 / 21 | 411 / 21 | 380 / 18 | 389 / 27 | 389 / 27 | 389 / 27 | — |
| books.toscrape.com/catalogue/shakespeares-sonnets_989/i | 509 / 143 | 421 / 18 | 421 / 18 | 390 / 16 | 398 / 24 | 398 / 24 | 398 / 24 | — |
| books.toscrape.com/catalogue/sharp-objects_997/index.ht | 685 / 274 | 427 / 18 | 427 / 18 | 435 / 16 | 443 / 24 | 443 / 24 | 443 / 24 | — |
| books.toscrape.com/catalogue/soumission_998/index.html | 452 / 163 | 304 / 16 | 304 / 16 | 312 / 15 | 319 / 22 | 319 / 22 | 319 / 22 | — |
| books.toscrape.com/catalogue/starving-hearts-triangular | 619 / 196 | 486 / 26 | 486 / 26 | 451 / 20 | 463 / 32 | 463 / 32 | 463 / 32 | — |
| books.toscrape.com/catalogue/the-black-maria_991/index. | 1150 / 464 | 742 / 20 | 742 / 20 | 711 / 17 | 720 / 26 | 720 / 26 | 720 / 26 | — |
| books.toscrape.com/catalogue/the-coming-woman-a-novel-b | 1335 / 568 | 818 / 44 | 818 / 44 | 804 / 29 | 825 / 50 | 825 / 50 | 825 / 50 | — |
| books.toscrape.com/catalogue/the-dirty-little-secrets-o | 757 / 284 | 508 / 32 | 508 / 32 | 504 / 23 | 519 / 38 | 519 / 38 | 519 / 38 | — |
| books.toscrape.com/catalogue/the-requiem-red_995/index. | 509 / 170 | 362 / 21 | 362 / 21 | 365 / 18 | 374 / 27 | 374 / 27 | 374 / 27 | — |
| books.toscrape.com/catalogue/tipping-the-velvet_999/ind | 444 / 165 | 298 / 21 | 298 / 21 | 305 / 18 | 314 / 27 | 314 / 27 | 314 / 27 | — |

</details>

## fastapi-docs

| Tool | Avg words [6] | Preamble [2] | Repeat rate [3] | Junk found [4] | Headings [7] | Code blocks [8] | Precision [5] | Recall [5] |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 2084 | 13 | 0% | 186 | 20.2 | 14.3 | 93% | 68% |
| crawl4ai | 3519 | 1420 ⚠ | 1% | 183 | 20.1 | 14.2 | 100% | 92% |
| crawl4ai-raw | 3521 | 1420 ⚠ | 1% | 183 | 20.1 | 14.2 | 100% | 92% |
| scrapy+md | 2851 | 765 ⚠ | 0% | 328 | 20.2 | 14.3 | 100% | 69% |
| crawlee | 3154 | 1004 ⚠ | 1% | 628 | 20.1 | 14.2 | 100% | 96% |
| colly+md | 3175 | 986 ⚠ | 1% | 632 | 20.2 | 14.3 | 100% | 97% |
| playwright | 3160 | 999 ⚠ | 1% | 632 | 20.1 | 14.3 | 100% | 97% |
| firecrawl | — | — | — | — | — | — | — | — |

> **Column definitions:**
> **[6] Avg words** = mean words per page. **[2] Preamble** = avg words per page before the first heading (nav chrome). **[3] Repeat rate** = fraction of sentences on >50% of pages.
> **[4] Junk found** = total known boilerplate phrases detected across all pages. **[7] Headings** = avg headings per page. **[8] Code blocks** = avg fenced code blocks per page.
> **[5] Precision/Recall** = cross-tool consensus (pages with <2 sentences excluded). **⚠** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
**markcrawl** produces the cleanest output with 13 words of preamble per page, while **crawl4ai-raw** injects 1420 words of nav chrome before content begins. The word count gap (2084 vs 3521 avg words) is largely explained by preamble: 1420 words of nav chrome account for ~40% of crawl4ai-raw's output on this site. markcrawl's lower recall (68% vs 97%) reflects stricter content filtering — the "missed" sentences are predominantly navigation, sponsor links, and footer text that other tools include as content. For RAG, this is typically a net positive: fewer junk tokens per chunk tends to improve embedding quality and retrieval precision.

<details>
<summary>Sample output — first 40 lines of <code>fastapi.tiangolo.com/reference/status</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
*FastAPI framework, high performance, easy to learn, fast to code, ready for production*


# Status Codes[¶](#status-codes "Permanent link")

You can import the `status` module from `fastapi`:

```
from fastapi import status
```

`status` is provided directly by Starlette.

It contains a group of named constants (variables) with integer status codes.

For example:

* 200: `status.HTTP_200_OK`
* 403: `status.HTTP_403_FORBIDDEN`
* etc.

It can be convenient to quickly access HTTP (and WebSocket) status codes in your app, using autocompletion for the name without having to remember the integer status codes by memory.

Read more about it in the [FastAPI docs about Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).

## Example[¶](#example "Permanent link")

```
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

## fastapi.status [¶](#fastapi.status "Permanent link")
```

**crawl4ai**
```
[ Skip to content ](https://fastapi.tiangolo.com/reference/status/#status-codes)
[ **FastAPI Cloud** waiting list 🚀 ](https://fastapicloud.com)
[ Follow **@fastapi** on **X (Twitter)** to stay updated ](https://x.com/fastapi)
[ Follow **FastAPI** on **LinkedIn** to stay updated ](https://www.linkedin.com/company/fastapi)
[ **FastAPI and friends** newsletter 🎉 ](https://fastapi.tiangolo.com/newsletter/)
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/blockbee-banner.png) ](https://blockbee.io?ref=fastapi "BlockBee Cryptocurrency Payment Gateway")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/scalar-banner.svg) ](https://github.com/scalar/scalar/?utm_source=fastapi&utm_medium=website&utm_campaign=top-banner "Scalar: Beautiful Open-Source API References from Swagger/OpenAPI files")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/propelauth-banner.png) ](https://www.propelauth.com/?utm_source=fastapi&utm_campaign=1223&utm_medium=topbanner "Auth, user management and more for your B2B product")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/zuplo-banner.png) ](https://zuplo.link/fastapi-web "Zuplo: Scale, Protect, Document, and Monetize your FastAPI")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/liblab-banner.png) ](https://liblab.com?utm_source=fastapi "liblab - Generate SDKs from FastAPI")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/render-banner.svg) ](https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi "Deploy & scale any full-stack web app on Render. Focus on building apps, not infra.")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/coderabbit-banner.png) ](https://www.coderabbit.ai/?utm_source=fastapi&utm_medium=banner&utm_campaign=fastapi "Cut Code Review Time & Bugs in Half with CodeRabbit")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/subtotal-banner.svg) ](https://subtotal.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=open-source "Making Retail Purchases Actionable for Brands and Developers")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/railway-banner.png) ](https://docs.railway.com/guides/fastapi?utm_medium=integration&utm_source=docs&utm_campaign=fastapi "Deploy enterprise applications at startup speed")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/serpapi-banner.png) ](https://serpapi.com/?utm_source=fastapi_website "SerpApi: Web Search API")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/greptile-banner.png) ](https://www.greptile.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=fastapi_sponsor_page "Greptile: The AI Code Reviewer")
[ ![logo](https://fastapi.tiangolo.com/img/icon-white.svg) ](https://fastapi.tiangolo.com/ "FastAPI")
FastAPI 
Status Codes 
  * [ en - English ](https://fastapi.tiangolo.com/)
  * [ de - Deutsch ](https://fastapi.tiangolo.com/de/)
  * [ es - español ](https://fastapi.tiangolo.com/es/)
  * [ fr - français ](https://fastapi.tiangolo.com/fr/)
  * [ ja - 日本語 ](https://fastapi.tiangolo.com/ja/)
  * [ ko - 한국어 ](https://fastapi.tiangolo.com/ko/)
  * [ pt - português ](https://fastapi.tiangolo.com/pt/)
  * [ ru - русский язык ](https://fastapi.tiangolo.com/ru/)
  * [ tr - Türkçe ](https://fastapi.tiangolo.com/tr/)
  * [ uk - українська мова ](https://fastapi.tiangolo.com/uk/)
  * [ zh - 简体中文 ](https://fastapi.tiangolo.com/zh/)
  * [ zh-hant - 繁體中文 ](https://fastapi.tiangolo.com/zh-hant/)


[ ](https://fastapi.tiangolo.com/reference/status/?q= "Share")
Initializing search 
[ fastapi/fastapi 
  * 0.135.3
  * 97.1k
  * 9.1k
```

**crawl4ai-raw**
```
[ Skip to content ](https://fastapi.tiangolo.com/reference/status/#status-codes)
[ **FastAPI Cloud** waiting list 🚀 ](https://fastapicloud.com)
[ Follow **@fastapi** on **X (Twitter)** to stay updated ](https://x.com/fastapi)
[ Follow **FastAPI** on **LinkedIn** to stay updated ](https://www.linkedin.com/company/fastapi)
[ **FastAPI and friends** newsletter 🎉 ](https://fastapi.tiangolo.com/newsletter/)
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/blockbee-banner.png) ](https://blockbee.io?ref=fastapi "BlockBee Cryptocurrency Payment Gateway")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/scalar-banner.svg) ](https://github.com/scalar/scalar/?utm_source=fastapi&utm_medium=website&utm_campaign=top-banner "Scalar: Beautiful Open-Source API References from Swagger/OpenAPI files")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/propelauth-banner.png) ](https://www.propelauth.com/?utm_source=fastapi&utm_campaign=1223&utm_medium=topbanner "Auth, user management and more for your B2B product")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/zuplo-banner.png) ](https://zuplo.link/fastapi-web "Zuplo: Scale, Protect, Document, and Monetize your FastAPI")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/liblab-banner.png) ](https://liblab.com?utm_source=fastapi "liblab - Generate SDKs from FastAPI")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/render-banner.svg) ](https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi "Deploy & scale any full-stack web app on Render. Focus on building apps, not infra.")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/coderabbit-banner.png) ](https://www.coderabbit.ai/?utm_source=fastapi&utm_medium=banner&utm_campaign=fastapi "Cut Code Review Time & Bugs in Half with CodeRabbit")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/subtotal-banner.svg) ](https://subtotal.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=open-source "Making Retail Purchases Actionable for Brands and Developers")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/railway-banner.png) ](https://docs.railway.com/guides/fastapi?utm_medium=integration&utm_source=docs&utm_campaign=fastapi "Deploy enterprise applications at startup speed")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/serpapi-banner.png) ](https://serpapi.com/?utm_source=fastapi_website "SerpApi: Web Search API")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/greptile-banner.png) ](https://www.greptile.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=fastapi_sponsor_page "Greptile: The AI Code Reviewer")
[ ![logo](https://fastapi.tiangolo.com/img/icon-white.svg) ](https://fastapi.tiangolo.com/ "FastAPI")
FastAPI 
Status Codes 
  * [ en - English ](https://fastapi.tiangolo.com/)
  * [ de - Deutsch ](https://fastapi.tiangolo.com/de/)
  * [ es - español ](https://fastapi.tiangolo.com/es/)
  * [ fr - français ](https://fastapi.tiangolo.com/fr/)
  * [ ja - 日本語 ](https://fastapi.tiangolo.com/ja/)
  * [ ko - 한국어 ](https://fastapi.tiangolo.com/ko/)
  * [ pt - português ](https://fastapi.tiangolo.com/pt/)
  * [ ru - русский язык ](https://fastapi.tiangolo.com/ru/)
  * [ tr - Türkçe ](https://fastapi.tiangolo.com/tr/)
  * [ uk - українська мова ](https://fastapi.tiangolo.com/uk/)
  * [ zh - 简体中文 ](https://fastapi.tiangolo.com/zh/)
  * [ zh-hant - 繁體中文 ](https://fastapi.tiangolo.com/zh-hant/)


[ ](https://fastapi.tiangolo.com/reference/status/?q= "Share")
Type to start searching
[ fastapi/fastapi 
  * 0.135.3
  * 97.1k
  * 9.1k
```

**scrapy+md**
```
FastAPI

[fastapi/fastapi](https://github.com/fastapi/fastapi "Go to repository")

* [FastAPI](../..)
* [Features](../../features/)
* [Learn](../../learn/)

  Learn
  + [Python Types Intro](../../python-types/)
  + [Concurrency and async / await](../../async/)
  + [Environment Variables](../../environment-variables/)
  + [Virtual Environments](../../virtual-environments/)
  + [Tutorial - User Guide](../../tutorial/)

    Tutorial - User Guide
    - [First Steps](../../tutorial/first-steps/)
    - [Path Parameters](../../tutorial/path-params/)
    - [Query Parameters](../../tutorial/query-params/)
    - [Request Body](../../tutorial/body/)
    - [Query Parameters and String Validations](../../tutorial/query-params-str-validations/)
    - [Path Parameters and Numeric Validations](../../tutorial/path-params-numeric-validations/)
    - [Query Parameter Models](../../tutorial/query-param-models/)
    - [Body - Multiple Parameters](../../tutorial/body-multiple-params/)
    - [Body - Fields](../../tutorial/body-fields/)
    - [Body - Nested Models](../../tutorial/body-nested-models/)
    - [Declare Request Example Data](../../tutorial/schema-extra-example/)
    - [Extra Data Types](../../tutorial/extra-data-types/)
    - [Cookie Parameters](../../tutorial/cookie-params/)
    - [Header Parameters](../../tutorial/header-params/)
    - [Cookie Parameter Models](../../tutorial/cookie-param-models/)
    - [Header Parameter Models](../../tutorial/header-param-models/)
    - [Response Model - Return Type](../../tutorial/response-model/)
    - [Extra Models](../../tutorial/extra-models/)
    - [Response Status Code](../../tutorial/response-status-code/)
    - [Form Data](../../tutorial/request-forms/)
    - [Form Models](../../tutorial/request-form-models/)
    - [Request Files](../../tutorial/request-files/)
    - [Request Forms and Files](../../tutorial/request-forms-and-files/)
    - [Handling Errors](../../tutorial/handling-errors/)
```

**crawlee**
```
Status Codes - FastAPI




:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}



\_\_md\_scope=new URL("../..",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}













.grecaptcha-badge {
visibility: hidden;
}





[Skip to content](https://fastapi.tiangolo.com/reference/status/#status-codes)

[Join the **FastAPI Cloud** waiting list 🚀](https://fastapicloud.com)

[Follow **@fastapi** on **X (Twitter)** to stay updated](https://x.com/fastapi)

[Follow **FastAPI** on **LinkedIn** to stay updated](https://www.linkedin.com/company/fastapi)

[Subscribe to the **FastAPI and friends** newsletter 🎉](https://fastapi.tiangolo.com/newsletter/)
```

**colly+md**
```
Status Codes - FastAPI




:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}



\_\_md\_scope=new URL("../..",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}






[Skip to content](#status-codes)

[Join the **FastAPI Cloud** waiting list 🚀](https://fastapicloud.com)

[Follow **@fastapi** on **X (Twitter)** to stay updated](https://x.com/fastapi)

[Follow **FastAPI** on **LinkedIn** to stay updated](https://www.linkedin.com/company/fastapi)

[Subscribe to the **FastAPI and friends** newsletter 🎉](https://fastapi.tiangolo.com/newsletter/)

[sponsor](https://blockbee.io?ref=fastapi "BlockBee Cryptocurrency Payment Gateway")

[sponsor](https://github.com/scalar/scalar/?utm_source=fastapi&utm_medium=website&utm_campaign=top-banner "Scalar: Beautiful Open-Source API References from Swagger/OpenAPI files")

[sponsor](https://www.propelauth.com/?utm_source=fastapi&utm_campaign=1223&utm_medium=topbanner "Auth, user management and more for your B2B product")

[sponsor](https://zuplo.link/fastapi-web "Zuplo: Scale, Protect, Document, and Monetize your FastAPI")

[sponsor](https://liblab.com?utm_source=fastapi "liblab - Generate SDKs from FastAPI")

[sponsor](https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi "Deploy & scale any full-stack web app on Render. Focus on building apps, not infra.")

[sponsor](https://www.coderabbit.ai/?utm_source=fastapi&utm_medium=banner&utm_campaign=fastapi "Cut Code Review Time & Bugs in Half with CodeRabbit")
```

**playwright**
```
Status Codes - FastAPI




:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}



\_\_md\_scope=new URL("../..",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}













.grecaptcha-badge {
visibility: hidden;
}





[Skip to content](https://fastapi.tiangolo.com/reference/status/#status-codes)

[Join the **FastAPI Cloud** waiting list 🚀](https://fastapicloud.com)

[Follow **@fastapi** on **X (Twitter)** to stay updated](https://x.com/fastapi)

[Follow **FastAPI** on **LinkedIn** to stay updated](https://www.linkedin.com/company/fastapi)

[Subscribe to the **FastAPI and friends** newsletter 🎉](https://fastapi.tiangolo.com/newsletter/)
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [2]</summary>

| URL | markcrawl words [6] / preamble [2] | crawl4ai words [6] / preamble [2] | crawl4ai-raw words [6] / preamble [2] | scrapy+md words [6] / preamble [2] | crawlee words [6] / preamble [2] | colly+md words [6] / preamble [2] | playwright words [6] / preamble [2] | firecrawl words [6] / preamble [2] |
|---|---|---|---|---|---|---|---|---|
| fastapi.tiangolo.com | 2243 / 13 | 3991 / 1538 | 3979 / 1526 | 3092 / 839 | 3374 / 1071 | 3404 / 1054 | 3362 / 1059 | — |
| fastapi.tiangolo.com/about | 28 / 13 | 1303 / 1241 | 1303 / 1241 | 677 / 646 | 1015 / 882 | 998 / 863 | 1008 / 875 | — |
| fastapi.tiangolo.com/advanced | 128 / 13 | 1415 / 1261 | 1415 / 1261 | 792 / 661 | 1126 / 901 | 1113 / 882 | 1124 / 899 | — |
| fastapi.tiangolo.com/advanced/additional-responses | 1287 / 13 | 2648 / 1332 | 2650 / 1334 | 2008 / 718 | 2344 / 960 | 2337 / 941 | 2342 / 958 | — |
| fastapi.tiangolo.com/advanced/additional-status-codes | 485 / 13 | 1796 / 1280 | 1794 / 1278 | 1165 / 677 | 1504 / 917 | 1491 / 898 | 1497 / 910 | — |
| fastapi.tiangolo.com/advanced/advanced-dependencies | 2213 / 13 | 3660 / 1434 | 3658 / 1432 | 3012 / 796 | 3328 / 1032 | 3335 / 1015 | 3323 / 1027 | — |
| fastapi.tiangolo.com/advanced/advanced-python-types | 343 / 13 | 1642 / 1266 | 1644 / 1268 | 1015 / 669 | 1355 / 909 | 1340 / 890 | 1348 / 902 | — |
| fastapi.tiangolo.com/advanced/async-tests | 659 / 13 | 1991 / 1308 | 1991 / 1308 | 1354 / 692 | 1684 / 930 | 1678 / 911 | 1682 / 928 | — |
| fastapi.tiangolo.com/advanced/behind-a-proxy | 2231 / 13 | 3672 / 1478 | 3674 / 1480 | 3055 / 821 | 3318 / 1061 | 3378 / 1042 | 3381 / 1054 | — |
| fastapi.tiangolo.com/advanced/custom-response | 2000 / 13 | 3459 / 1450 | 3457 / 1448 | 2782 / 779 | 3097 / 1027 | 3116 / 1008 | 3090 / 1020 | — |
| fastapi.tiangolo.com/advanced/dataclasses | 791 / 13 | 2115 / 1296 | 2117 / 1298 | 1482 / 688 | 1813 / 926 | 1804 / 907 | 1811 / 924 | — |
| fastapi.tiangolo.com/advanced/events | 1513 / 13 | 2886 / 1356 | 2886 / 1356 | 2240 / 724 | 2556 / 962 | 2559 / 943 | 2549 / 955 | — |
| fastapi.tiangolo.com/advanced/generate-clients | 1665 / 13 | 3177 / 1480 | 3177 / 1480 | 2498 / 828 | 2810 / 1066 | 2823 / 1047 | 2803 / 1059 | — |
| fastapi.tiangolo.com/advanced/json-base64-bytes | 756 / 13 | 2096 / 1314 | 2096 / 1314 | 1462 / 703 | 1799 / 947 | 1790 / 928 | 1792 / 940 | — |
| fastapi.tiangolo.com/advanced/middleware | 610 / 13 | 1944 / 1308 | 1942 / 1306 | 1303 / 690 | 1630 / 928 | 1625 / 909 | 1623 / 921 | — |
| fastapi.tiangolo.com/advanced/openapi-callbacks | 1759 / 13 | 3155 / 1376 | 3157 / 1378 | 2510 / 748 | 2831 / 986 | 2832 / 967 | 2829 / 984 | — |
| fastapi.tiangolo.com/advanced/openapi-webhooks | 532 / 13 | 1868 / 1304 | 1870 / 1306 | 1231 / 696 | 1564 / 934 | 1555 / 915 | 1557 / 927 | — |
| fastapi.tiangolo.com/advanced/path-operation-advanced-c | 1336 / 13 | 2727 / 1374 | 2727 / 1374 | 2083 / 744 | 2405 / 984 | 2408 / 967 | 2400 / 979 | — |
| fastapi.tiangolo.com/advanced/response-change-status-co | 305 / 13 | 1612 / 1280 | 1612 / 1280 | 985 / 677 | 1324 / 921 | 1311 / 902 | 1322 / 919 | — |
| fastapi.tiangolo.com/advanced/response-cookies | 389 / 13 | 1706 / 1290 | 1706 / 1290 | 1076 / 684 | 1409 / 922 | 1398 / 903 | 1402 / 915 | — |
| fastapi.tiangolo.com/advanced/response-directly | 750 / 13 | 2099 / 1322 | 2101 / 1324 | 1461 / 708 | 1798 / 950 | 1791 / 931 | 1791 / 943 | — |
| fastapi.tiangolo.com/advanced/response-headers | 364 / 13 | 1680 / 1288 | 1682 / 1290 | 1051 / 684 | 1385 / 922 | 1374 / 903 | 1378 / 915 | — |
| fastapi.tiangolo.com/advanced/security | 103 / 13 | 1395 / 1265 | 1397 / 1267 | 770 / 664 | 1101 / 900 | 1090 / 883 | 1096 / 895 | — |
| fastapi.tiangolo.com/advanced/security/http-basic-auth | 1182 / 13 | 2553 / 1351 | 2553 / 1351 | 1913 / 728 | 2240 / 968 | 2237 / 949 | 2238 / 966 | — |
| fastapi.tiangolo.com/advanced/security/oauth2-scopes | 9002 / 13 | 10454 / 1445 | 10452 / 1443 | 9798 / 793 | 10106 / 1029 | 10119 / 1012 | 10101 / 1024 | — |
| fastapi.tiangolo.com/advanced/settings | 2195 / 13 | 3544 / 1472 | 3544 / 1472 | 3006 / 808 | 3191 / 1048 | 3330 / 1031 | 3317 / 1043 | — |
| fastapi.tiangolo.com/advanced/stream-data | 2736 / 13 | 4109 / 1354 | 4111 / 1356 | 3465 / 726 | 3787 / 964 | 3788 / 945 | 3780 / 957 | — |
| fastapi.tiangolo.com/advanced/strict-content-type | 535 / 13 | 1858 / 1296 | 1860 / 1298 | 1225 / 687 | 1559 / 927 | 1550 / 908 | 1552 / 920 | — |
| fastapi.tiangolo.com/advanced/sub-applications | 476 / 13 | 1829 / 1326 | 1829 / 1326 | 1187 / 708 | 1519 / 950 | 1512 / 931 | 1517 / 948 | — |
| fastapi.tiangolo.com/advanced/templates | 571 / 13 | 1917 / 1328 | 1913 / 1326 | 1281 / 707 | 1601 / 943 | 1599 / 924 | 1598 / 936 | — |
| fastapi.tiangolo.com/advanced/testing-dependencies | 707 / 13 | 2034 / 1296 | 2036 / 1298 | 1400 / 690 | 1740 / 932 | 1729 / 913 | 1733 / 925 | — |
| fastapi.tiangolo.com/advanced/testing-events | 276 / 13 | 1562 / 1253 | 1562 / 1253 | 929 / 650 | 1278 / 898 | 1261 / 879 | 1271 / 891 | — |
| fastapi.tiangolo.com/advanced/testing-websockets | 130 / 13 | 1414 / 1248 | 1414 / 1248 | 783 / 650 | 1125 / 888 | 1108 / 869 | 1118 / 881 | — |
| fastapi.tiangolo.com/advanced/using-request-directly | 370 / 13 | 1692 / 1296 | 1692 / 1296 | 1063 / 690 | 1399 / 932 | 1388 / 913 | 1397 / 930 | — |
| fastapi.tiangolo.com/advanced/vibe | 402 / 13 | 1717 / 1280 | 1719 / 1282 | 1081 / 676 | 1413 / 914 | 1402 / 895 | 1411 / 912 | — |
| fastapi.tiangolo.com/advanced/websockets | 1651 / 13 | 3048 / 1374 | 3046 / 1374 | 2397 / 743 | 2714 / 979 | 2714 / 960 | 2711 / 972 | — |
| fastapi.tiangolo.com/advanced/wsgi | 260 / 13 | 1565 / 1278 | 1565 / 1278 | 937 / 674 | 1276 / 918 | 1265 / 901 | 1276 / 918 | — |
| fastapi.tiangolo.com/alternatives | 3306 / 13 | 4757 / 1458 | 4759 / 1460 | 4087 / 778 | 4383 / 1020 | 4412 / 1001 | 4376 / 1013 | — |
| fastapi.tiangolo.com/async | 3664 / 13 | 5198 / 1484 | 5198 / 1484 | 4478 / 811 | 4782 / 1055 | 4805 / 1036 | 4775 / 1048 | — |
| fastapi.tiangolo.com/benchmarks | 538 / 13 | 1831 / 1256 | 1829 / 1254 | 1202 / 661 | 1537 / 897 | 1522 / 878 | 1530 / 890 | — |
| fastapi.tiangolo.com/contributing | 1612 / 13 | 3118 / 1494 | 3116 / 1494 | 2438 / 823 | 2755 / 1063 | 2765 / 1044 | 2753 / 1056 | — |
| fastapi.tiangolo.com/deployment | 253 / 13 | 1540 / 1257 | 1542 / 1259 | 915 / 659 | 1247 / 895 | 1234 / 876 | 1240 / 888 | — |
| fastapi.tiangolo.com/deployment/cloud | 155 / 13 | 1466 / 1278 | 1466 / 1278 | 833 / 675 | 1176 / 919 | 1163 / 900 | 1169 / 912 | — |
| fastapi.tiangolo.com/deployment/concepts | 3079 / 13 | 4699 / 1606 | 4701 / 1608 | 3988 / 906 | 4276 / 1144 | 4313 / 1125 | 4269 / 1137 | — |
| fastapi.tiangolo.com/deployment/docker | 4170 / 13 | 5537 / 1722 | 5539 / 1724 | 5156 / 983 | 5068 / 1225 | 5488 / 1208 | 5417 / 1220 | — |
| fastapi.tiangolo.com/deployment/fastapicloud | 308 / 13 | 1638 / 1306 | 1637 / 1306 | 1005 / 694 | 1328 / 930 | 1326 / 913 | 1334 / 925 | — |
| fastapi.tiangolo.com/deployment/https | 2106 / 13 | 3541 / 1396 | 3543 / 1398 | 2857 / 748 | 3168 / 986 | 3179 / 967 | 3161 / 979 | — |
| fastapi.tiangolo.com/deployment/manually | 811 / 13 | 2054 / 1332 | 2054 / 1334 | 1528 / 714 | 1736 / 956 | 1852 / 937 | 1814 / 954 | — |
| fastapi.tiangolo.com/deployment/server-workers | 877 / 13 | 2027 / 1296 | 2026 / 1296 | 1564 / 684 | 1725 / 928 | 1898 / 911 | 1798 / 923 | — |
| fastapi.tiangolo.com/deployment/versions | 550 / 13 | 1886 / 1318 | 1886 / 1318 | 1254 / 701 | 1580 / 941 | 1575 / 922 | 1573 / 934 | — |
| fastapi.tiangolo.com/editor-support | 323 / 13 | 1621 / 1274 | 1623 / 1276 | 998 / 672 | 1328 / 910 | 1317 / 891 | 1321 / 903 | — |
| fastapi.tiangolo.com/environment-variables | 1147 / 13 | 2462 / 1326 | 2449 / 1326 | 1862 / 712 | 2150 / 948 | 2185 / 931 | 2222 / 948 | — |
| fastapi.tiangolo.com/external-links | 712 / 13 | 1999 / 1254 | 1999 / 1254 | 1375 / 660 | 1714 / 898 | 1699 / 879 | 1707 / 891 | — |
| fastapi.tiangolo.com/fastapi-cli | 671 / 13 | 1825 / 1296 | 1827 / 1298 | 1364 / 690 | 1523 / 928 | 1684 / 909 | 1621 / 921 | — |
| fastapi.tiangolo.com/fastapi-people | 1447 / 13 | 3349 / 1432 | 3347 / 1430 | 2230 / 780 | 2536 / 1018 | 2551 / 999 | 2529 / 1011 | — |
| fastapi.tiangolo.com/features | 1167 / 13 | 2569 / 1366 | 2571 / 1368 | 1899 / 729 | 2206 / 965 | 2215 / 946 | 2204 / 963 | — |
| fastapi.tiangolo.com/help-fastapi | 1968 / 13 | 3519 / 1564 | 3519 / 1564 | 2842 / 875 | 3141 / 1119 | 3172 / 1100 | 3134 / 1112 | — |
| fastapi.tiangolo.com/history-design-future | 632 / 13 | 1946 / 1296 | 1948 / 1298 | 1315 / 680 | 1645 / 922 | 1640 / 903 | 1638 / 915 | — |
| fastapi.tiangolo.com/how-to | 110 / 13 | 1400 / 1251 | 1400 / 1251 | 764 / 651 | 1112 / 893 | 1095 / 874 | 1105 / 886 | — |
| fastapi.tiangolo.com/how-to/authentication-error-status | 207 / 13 | 1492 / 1254 | 1492 / 1254 | 861 / 651 | 1208 / 899 | 1191 / 880 | 1201 / 892 | — |
| fastapi.tiangolo.com/how-to/conditional-openapi | 393 / 13 | 1713 / 1287 | 1715 / 1289 | 1083 / 687 | 1422 / 925 | 1406 / 906 | 1415 / 918 | — |
| fastapi.tiangolo.com/how-to/configure-swagger-ui | 1577 / 13 | 2923 / 1317 | 2923 / 1317 | 2284 / 704 | 2618 / 944 | 2611 / 925 | 2611 / 937 | — |
| fastapi.tiangolo.com/how-to/custom-docs-ui-assets | 1545 / 13 | 3044 / 1481 | 3044 / 1481 | 2377 / 829 | 2702 / 1075 | 2713 / 1056 | 2700 / 1073 | — |
| fastapi.tiangolo.com/how-to/custom-request-and-route | 1523 / 13 | 2896 / 1355 | 2896 / 1355 | 2262 / 736 | 2592 / 980 | 2587 / 961 | 2585 / 973 | — |
| fastapi.tiangolo.com/how-to/extending-openapi | 772 / 13 | 2145 / 1349 | 2147 / 1351 | 1500 / 725 | 1828 / 963 | 1827 / 944 | 1826 / 961 | — |
| fastapi.tiangolo.com/how-to/general | 366 / 13 | 1806 / 1419 | 1806 / 1419 | 1152 / 783 | 1484 / 1029 | 1487 / 1010 | 1477 / 1022 | — |
| fastapi.tiangolo.com/how-to/graphql | 377 / 13 | 1705 / 1295 | 1707 / 1297 | 1068 / 688 | 1403 / 924 | 1394 / 905 | 1396 / 917 | — |
| fastapi.tiangolo.com/how-to/migrate-from-pydantic-v1-to | 957 / 13 | 2267 / 1369 | 2267 / 1369 | 1698 / 738 | 1955 / 986 | 2031 / 967 | 2025 / 979 | — |
| fastapi.tiangolo.com/how-to/separate-openapi-schemas | 900 / 13 | 2345 / 1411 | 2345 / 1411 | 1679 / 776 | 2014 / 1026 | 2017 / 1009 | 2009 / 1021 | — |
| fastapi.tiangolo.com/how-to/testing-database | 55 / 13 | 1344 / 1252 | 1344 / 1252 | 709 / 651 | 1052 / 889 | 1037 / 872 | 1047 / 884 | — |
| fastapi.tiangolo.com/learn | 48 / 13 | 1322 / 1241 | 1324 / 1243 | 697 / 646 | 1032 / 882 | 1015 / 863 | 1025 / 875 | — |
| fastapi.tiangolo.com/management | 228 / 13 | 1535 / 1280 | 1537 / 1282 | 905 / 674 | 1233 / 912 | 1224 / 893 | 1226 / 905 | — |
| fastapi.tiangolo.com/management-tasks | 1811 / 13 | 3193 / 1370 | 3195 / 1372 | 2553 / 739 | 2871 / 977 | 2876 / 960 | 2871 / 977 | — |
| fastapi.tiangolo.com/newsletter | 23 / 13 | 1299 / 1244 | 1301 / 1246 | 672 / 646 | 1014 / 888 | 997 / 869 | 1012 / 886 | — |
| fastapi.tiangolo.com/project-generation | 266 / 13 | 1568 / 1272 | 1570 / 1274 | 945 / 676 | 1285 / 918 | 1270 / 899 | 1278 / 911 | — |
| fastapi.tiangolo.com/python-types | 1905 / 13 | 3337 / 1422 | 3339 / 1424 | 2671 / 763 | 2978 / 1003 | 2995 / 984 | 2976 / 1001 | — |
| fastapi.tiangolo.com/reference | 57 / 13 | 1334 / 1241 | 1336 / 1243 | 706 / 646 | 1044 / 880 | 1029 / 863 | 1044 / 880 | — |
| fastapi.tiangolo.com/reference/apirouter | 24902 / 13 | 26603 / 1404 | 26605 / 1406 | 25651 / 746 | 25971 / 984 | 25976 / 965 | 25964 / 977 | — |
| fastapi.tiangolo.com/reference/background | 388 / 13 | 1715 / 1298 | 1715 / 1298 | 1079 / 688 | 1418 / 930 | 1403 / 911 | 1416 / 928 | — |
| fastapi.tiangolo.com/reference/dependencies | 1530 / 13 | 2839 / 1280 | 2839 / 1280 | 2206 / 673 | 2548 / 917 | 2535 / 898 | 2541 / 910 | — |
| fastapi.tiangolo.com/reference/encoders | 1130 / 13 | 2415 / 1252 | 2417 / 1254 | 1792 / 659 | 2131 / 897 | 2116 / 880 | 2131 / 897 | — |
| fastapi.tiangolo.com/reference/exceptions | 759 / 13 | 2099 / 1310 | 2097 / 1308 | 1455 / 693 | 1795 / 935 | 1784 / 918 | 1790 / 930 | — |
| fastapi.tiangolo.com/reference/fastapi | 29540 / 13 | 31322 / 1454 | 31322 / 1454 | 30321 / 778 | 30633 / 1016 | 30640 / 997 | 30626 / 1009 | — |
| fastapi.tiangolo.com/reference/httpconnection | 305 / 13 | 1669 / 1334 | 1669 / 1334 | 1022 / 714 | 1358 / 952 | 1341 / 933 | 1351 / 945 | — |
| fastapi.tiangolo.com/reference/middleware | 1043 / 13 | 2490 / 1410 | 2490 / 1410 | 1811 / 765 | 2152 / 1001 | 2135 / 982 | 2145 / 994 | — |
| fastapi.tiangolo.com/reference/openapi | 45 / 13 | 1320 / 1245 | 1322 / 1247 | 696 / 648 | 1028 / 882 | 1013 / 865 | 1023 / 877 | — |
| fastapi.tiangolo.com/reference/openapi/docs | 1770 / 13 | 3076 / 1276 | 3076 / 1276 | 2445 / 672 | 2783 / 912 | 2764 / 891 | 2774 / 903 | — |
| fastapi.tiangolo.com/reference/openapi/models | 3721 / 13 | 7396 / 3188 | 7394 / 3186 | 5672 / 1948 | 6009 / 2186 | 5992 / 2167 | 6007 / 2184 | — |
| fastapi.tiangolo.com/reference/parameters | 12469 / 13 | 13849 / 1286 | 13851 / 1288 | 13154 / 682 | 13489 / 918 | 13474 / 901 | 13484 / 913 | — |
| fastapi.tiangolo.com/reference/request | 693 / 13 | 2122 / 1388 | 2122 / 1388 | 1446 / 750 | 1784 / 988 | 1767 / 969 | 1777 / 981 | — |
| fastapi.tiangolo.com/reference/response | 664 / 13 | 2012 / 1310 | 2012 / 1310 | 1365 / 698 | 1709 / 936 | 1692 / 917 | 1702 / 929 | — |
| fastapi.tiangolo.com/reference/responses | 5521 / 13 | 7509 / 1886 | 7509 / 1886 | 6601 / 1077 | 6947 / 1329 | 6934 / 1310 | 6940 / 1322 | — |
| fastapi.tiangolo.com/reference/security | 8822 / 13 | 10907 / 1922 | 10905 / 1920 | 9911 / 1086 | 10207 / 1324 | 10232 / 1305 | 10200 / 1317 | — |
| fastapi.tiangolo.com/reference/staticfiles | 1000 / 13 | 2365 / 1332 | 2367 / 1334 | 1715 / 712 | 2058 / 954 | 2041 / 935 | 2056 / 952 | — |
| fastapi.tiangolo.com/reference/status | 1009 / 13 | 2768 / 1730 | 2770 / 1732 | 1986 / 974 | 2327 / 1218 | 2306 / 1193 | 2319 / 1210 | — |
| fastapi.tiangolo.com/reference/templating | 636 / 13 | 1974 / 1276 | 1976 / 1278 | 1314 / 675 | 1655 / 913 | 1640 / 896 | 1650 / 908 | — |
| fastapi.tiangolo.com/reference/testclient | 2181 / 13 | 3662 / 1448 | 3662 / 1448 | 2972 / 788 | 3312 / 1028 | 3297 / 1011 | 3312 / 1028 | — |
| fastapi.tiangolo.com/reference/uploadfile | 726 / 13 | 2072 / 1314 | 2070 / 1312 | 1427 / 698 | 1765 / 936 | 1750 / 917 | 1763 / 934 | — |
| fastapi.tiangolo.com/reference/websockets | 1280 / 13 | 2826 / 1466 | 2826 / 1466 | 2086 / 803 | 2419 / 1039 | 2404 / 1020 | 2412 / 1032 | — |
| fastapi.tiangolo.com/release-notes | 52954 / 13 | 59610 / 8426 | 59795 / 8426 | 57519 / 4562 | 56030 / 4800 | 57836 / 4781 | 56208 / 4793 | — |
| fastapi.tiangolo.com/resources | 27 / 13 | 1302 / 1241 | 1302 / 1241 | 676 / 646 | 1014 / 882 | 997 / 863 | 1007 / 875 | — |
| fastapi.tiangolo.com/tutorial | 587 / 13 | 1719 / 1270 | 1717 / 1268 | 1255 / 665 | 1423 / 907 | 1579 / 888 | 1526 / 905 | — |
| fastapi.tiangolo.com/tutorial/background-tasks | 987 / 13 | 2334 / 1325 | 2336 / 1327 | 1695 / 705 | 2021 / 943 | 2018 / 924 | 2014 / 936 | — |
| fastapi.tiangolo.com/tutorial/bigger-applications | 3340 / 13 | 4914 / 1567 | 4912 / 1565 | 4229 / 886 | 4534 / 1130 | 4557 / 1111 | 4532 / 1128 | — |
| fastapi.tiangolo.com/tutorial/body | 1244 / 13 | 2652 / 1381 | 2652 / 1381 | 1994 / 747 | 2314 / 985 | 2317 / 966 | 2307 / 978 | — |
| fastapi.tiangolo.com/tutorial/body-fields | 665 / 13 | 1989 / 1297 | 1989 / 1297 | 1354 / 686 | 1689 / 926 | 1680 / 907 | 1682 / 919 | — |
| fastapi.tiangolo.com/tutorial/body-multiple-params | 1418 / 13 | 2781 / 1341 | 2781 / 1341 | 2142 / 721 | 2473 / 963 | 2468 / 944 | 2466 / 956 | — |
| fastapi.tiangolo.com/tutorial/body-nested-models | 1476 / 13 | 2929 / 1443 | 2927 / 1441 | 2270 / 791 | 2584 / 1031 | 2597 / 1014 | 2579 / 1026 | — |
| fastapi.tiangolo.com/tutorial/body-updates | 1024 / 13 | 2377 / 1333 | 2377 / 1333 | 1743 / 716 | 2068 / 954 | 2065 / 937 | 2063 / 949 | — |
| fastapi.tiangolo.com/tutorial/cookie-param-models | 601 / 13 | 1932 / 1303 | 1932 / 1303 | 1296 / 692 | 1628 / 932 | 1619 / 913 | 1621 / 925 | — |
| fastapi.tiangolo.com/tutorial/cookie-params | 378 / 13 | 1686 / 1281 | 1688 / 1283 | 1058 / 677 | 1388 / 913 | 1379 / 896 | 1383 / 908 | — |
| fastapi.tiangolo.com/tutorial/cors | 765 / 13 | 2109 / 1323 | 2109 / 1323 | 1467 / 699 | 1794 / 941 | 1791 / 922 | 1792 / 939 | — |
| fastapi.tiangolo.com/tutorial/debugging | 393 / 13 | 1735 / 1303 | 1733 / 1301 | 1090 / 694 | 1425 / 930 | 1408 / 911 | 1418 / 923 | — |
| fastapi.tiangolo.com/tutorial/dependencies | 1806 / 13 | 3109 / 1334 | 3111 / 1336 | 2521 / 712 | 2786 / 948 | 2841 / 929 | 2784 / 946 | — |
| fastapi.tiangolo.com/tutorial/dependencies/classes-as-d | 1956 / 13 | 3312 / 1333 | 3312 / 1333 | 2673 / 714 | 2998 / 954 | 2993 / 935 | 2991 / 947 | — |
| fastapi.tiangolo.com/tutorial/dependencies/dependencies | 913 / 13 | 2286 / 1357 | 2286 / 1357 | 1648 / 732 | 1976 / 976 | 1973 / 957 | 1974 / 974 | — |
| fastapi.tiangolo.com/tutorial/dependencies/dependencies | 2593 / 13 | 3819 / 1467 | 3819 / 1467 | 3414 / 818 | 3479 / 1058 | 3735 / 1039 | 3719 / 1051 | — |
| fastapi.tiangolo.com/tutorial/dependencies/global-depen | 295 / 13 | 1603 / 1275 | 1603 / 1275 | 973 / 675 | 1312 / 913 | 1297 / 894 | 1305 / 906 | — |
| fastapi.tiangolo.com/tutorial/dependencies/sub-dependen | 877 / 13 | 2211 / 1319 | 2213 / 1321 | 1586 / 706 | 1903 / 942 | 1908 / 923 | 1913 / 940 | — |
| fastapi.tiangolo.com/tutorial/encoder | 294 / 13 | 1590 / 1265 | 1592 / 1267 | 965 / 668 | 1304 / 908 | 1289 / 889 | 1302 / 906 | — |
| fastapi.tiangolo.com/tutorial/extra-data-types | 726 / 13 | 2028 / 1273 | 2028 / 1273 | 1401 / 672 | 1738 / 912 | 1725 / 893 | 1731 / 905 | — |
| fastapi.tiangolo.com/tutorial/extra-models | 1232 / 13 | 2649 / 1405 | 2649 / 1405 | 1998 / 763 | 2313 / 999 | 2322 / 982 | 2308 / 994 | — |
| fastapi.tiangolo.com/tutorial/first-steps | 1797 / 13 | 3327 / 1589 | 3329 / 1591 | 2693 / 893 | 2816 / 1129 | 3015 / 1112 | 2916 / 1124 | — |
| fastapi.tiangolo.com/tutorial/handling-errors | 1723 / 13 | 3161 / 1421 | 3161 / 1421 | 2503 / 777 | 2819 / 1015 | 2826 / 996 | 2812 / 1008 | — |
| fastapi.tiangolo.com/tutorial/header-param-models | 715 / 13 | 2059 / 1315 | 2059 / 1315 | 1420 / 702 | 1751 / 940 | 1746 / 923 | 1751 / 940 | — |
| fastapi.tiangolo.com/tutorial/header-params | 710 / 13 | 2033 / 1301 | 2033 / 1301 | 1402 / 689 | 1730 / 927 | 1723 / 908 | 1723 / 920 | — |
| fastapi.tiangolo.com/tutorial/metadata | 1185 / 13 | 2563 / 1361 | 2561 / 1359 | 1917 / 729 | 2240 / 971 | 2241 / 952 | 2233 / 964 | — |
| fastapi.tiangolo.com/tutorial/middleware | 611 / 13 | 1951 / 1301 | 1951 / 1301 | 1308 / 694 | 1644 / 930 | 1635 / 911 | 1637 / 923 | — |
| fastapi.tiangolo.com/tutorial/path-operation-configurat | 913 / 13 | 2278 / 1341 | 2278 / 1341 | 1632 / 716 | 1956 / 956 | 1955 / 937 | 1949 / 949 | — |
| fastapi.tiangolo.com/tutorial/path-params | 1556 / 13 | 3029 / 1469 | 3029 / 1469 | 2360 / 801 | 2659 / 1039 | 2680 / 1020 | 2652 / 1032 | — |
| fastapi.tiangolo.com/tutorial/path-params-numeric-valid | 1747 / 13 | 3179 / 1399 | 3179 / 1399 | 2518 / 768 | 2847 / 1012 | 2848 / 993 | 2840 / 1005 | — |
| fastapi.tiangolo.com/tutorial/query-param-models | 551 / 13 | 1887 / 1305 | 1887 / 1305 | 1250 / 696 | 1586 / 936 | 1577 / 917 | 1579 / 929 | — |
| fastapi.tiangolo.com/tutorial/query-params | 876 / 13 | 2208 / 1311 | 2210 / 1313 | 1578 / 699 | 1905 / 937 | 1898 / 918 | 1898 / 930 | — |
| fastapi.tiangolo.com/tutorial/query-params-str-validati | 4084 / 13 | 5684 / 1593 | 5684 / 1593 | 4987 / 900 | 5283 / 1142 | 5316 / 1125 | 5278 / 1137 | — |
| fastapi.tiangolo.com/tutorial/request-files | 1804 / 13 | 3199 / 1373 | 3201 / 1375 | 2548 / 741 | 2867 / 979 | 2870 / 960 | 2865 / 977 | — |
| fastapi.tiangolo.com/tutorial/request-form-models | 458 / 13 | 1782 / 1299 | 1782 / 1299 | 1152 / 691 | 1481 / 929 | 1472 / 910 | 1474 / 922 | — |
| fastapi.tiangolo.com/tutorial/request-forms | 501 / 13 | 1824 / 1293 | 1826 / 1295 | 1189 / 685 | 1519 / 923 | 1510 / 904 | 1512 / 916 | — |
| fastapi.tiangolo.com/tutorial/request-forms-and-files | 401 / 13 | 1723 / 1295 | 1721 / 1293 | 1091 / 687 | 1424 / 927 | 1415 / 910 | 1419 / 922 | — |
| fastapi.tiangolo.com/tutorial/response-model | 3163 / 13 | 4718 / 1555 | 4716 / 1553 | 4040 / 874 | 4346 / 1122 | 4367 / 1099 | 4335 / 1111 | — |
| fastapi.tiangolo.com/tutorial/response-status-code | 639 / 13 | 1964 / 1295 | 1964 / 1295 | 1332 / 690 | 1665 / 930 | 1654 / 911 | 1658 / 923 | — |
| fastapi.tiangolo.com/tutorial/schema-extra-example | 2019 / 13 | 3481 / 1451 | 3483 / 1453 | 2823 / 801 | 3139 / 1043 | 3150 / 1024 | 3132 / 1036 | — |
| fastapi.tiangolo.com/tutorial/security | 700 / 13 | 2010 / 1288 | 2012 / 1290 | 1381 / 678 | 1705 / 914 | 1702 / 895 | 1698 / 907 | — |
| fastapi.tiangolo.com/tutorial/security/first-steps | 1539 / 13 | 2915 / 1355 | 2915 / 1355 | 2263 / 721 | 2588 / 963 | 2587 / 944 | 2581 / 956 | — |
| fastapi.tiangolo.com/tutorial/security/get-current-user | 1550 / 13 | 2913 / 1339 | 2915 / 1341 | 2269 / 716 | 2600 / 956 | 2597 / 937 | 2598 / 954 | — |
| fastapi.tiangolo.com/tutorial/security/oauth2-jwt | 4431 / 13 | 5893 / 1431 | 5893 / 1431 | 5212 / 778 | 5552 / 1030 | 5549 / 1011 | 5550 / 1028 | — |
| fastapi.tiangolo.com/tutorial/security/simple-oauth2 | 3609 / 13 | 5078 / 1455 | 5080 / 1457 | 4405 / 793 | 4726 / 1039 | 4741 / 1020 | 4719 / 1032 | — |
| fastapi.tiangolo.com/tutorial/server-sent-events | 1462 / 13 | 2837 / 1359 | 2837 / 1359 | 2195 / 730 | 2515 / 968 | 2518 / 951 | 2510 / 963 | — |
| fastapi.tiangolo.com/tutorial/sql-databases | 10604 / 13 | 12264 / 1637 | 12262 / 1635 | 11545 / 938 | 11842 / 1176 | 11872 / 1159 | 11837 / 1171 | — |
| fastapi.tiangolo.com/tutorial/static-files | 258 / 13 | 1575 / 1293 | 1575 / 1293 | 944 / 683 | 1274 / 921 | 1265 / 902 | 1267 / 914 | — |
| fastapi.tiangolo.com/tutorial/stream-json-lines | 1227 / 13 | 2544 / 1343 | 2544 / 1343 | 1950 / 720 | 2224 / 958 | 2276 / 941 | 2272 / 953 | — |
| fastapi.tiangolo.com/tutorial/testing | 1498 / 13 | 2853 / 1341 | 2851 / 1339 | 2217 / 716 | 2533 / 952 | 2534 / 933 | 2526 / 945 | — |
| fastapi.tiangolo.com/virtual-environments | 3022 / 13 | 4539 / 1524 | 4528 / 1524 | 3869 / 844 | 4153 / 1082 | 4191 / 1063 | 4264 / 1075 | — |
| fastapi.tiangolo.com/zh-hant | 1139 / 13 | 2714 / 1341 | 2714 / 1341 | 1786 / 637 | 2068 / 869 | 2098 / 852 | 2051 / 852 | — |

</details>

## python-docs

| Tool | Avg words [6] | Preamble [2] | Repeat rate [3] | Junk found [4] | Headings [7] | Code blocks [8] | Precision [5] | Recall [5] |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 3766 | 5 | 0% | 378 | 11.9 | 7.3 | 98% | 82% |
| crawl4ai | 4180 | 50 ⚠ | 0% | 3111 | 19.4 | 7.4 | 100% | 70% |
| crawl4ai-raw | 4180 | 50 ⚠ | 0% | 3111 | 19.4 | 7.4 | 100% | 70% |
| scrapy+md | 4796 | 4 | 0% | 2086 | 22.7 | 9.5 | 100% | 99% |
| crawlee | 4140 | 47 | 0% | 3111 | 19.1 | 7.3 | 100% | 92% |
| colly+md | 4070 | 26 | 0% | 3111 | 19.1 | 7.3 | 100% | 92% |
| playwright | 4140 | 47 | 0% | 3111 | 19.1 | 7.3 | 100% | 92% |
| firecrawl | — | — | — | — | — | — | — | — |

> **Column definitions:**
> **[6] Avg words** = mean words per page. **[2] Preamble** = avg words per page before the first heading (nav chrome). **[3] Repeat rate** = fraction of sentences on >50% of pages.
> **[4] Junk found** = total known boilerplate phrases detected across all pages. **[7] Headings** = avg headings per page. **[8] Code blocks** = avg fenced code blocks per page.
> **[5] Precision/Recall** = cross-tool consensus (pages with <2 sentences excluded). **⚠** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
**scrapy+md** produces the cleanest output with 4 words of preamble per page, while **crawl4ai** injects 50 words of nav chrome before content begins.

<details>
<summary>Sample output — first 40 lines of <code>docs.python.org/3.10/library/pyclbr.html</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
# [`pyclbr`](#module-pyclbr "pyclbr: Supports information extraction for a Python module browser.") — Python module browser support[¶](#module-pyclbr "Permalink to this headline")

**Source code:** [Lib/pyclbr.py](https://github.com/python/cpython/tree/3.10/Lib/pyclbr.py)

---

The [`pyclbr`](#module-pyclbr "pyclbr: Supports information extraction for a Python module browser.") module provides limited information about the
functions, classes, and methods defined in a Python-coded module. The
information is sufficient to implement a module browser. The
information is extracted from the Python source code rather than by
importing the module, so this module is safe to use with untrusted code.
This restriction makes it impossible to use this module with modules not
implemented in Python, including all standard and optional extension
modules.

`pyclbr.``readmodule`(*module*, *path=None*)[¶](#pyclbr.readmodule "Permalink to this definition")
:   Return a dictionary mapping module-level class names to class
    descriptors. If possible, descriptors for imported base classes are
    included. Parameter *module* is a string with the name of the module
    to read; it may be the name of a module within a package. If given,
    *path* is a sequence of directory paths prepended to `sys.path`,
    which is used to locate the module source code.

    This function is the original interface and is only kept for back
    compatibility. It returns a filtered version of the following.

`pyclbr.``readmodule_ex`(*module*, *path=None*)[¶](#pyclbr.readmodule_ex "Permalink to this definition")
:   Return a dictionary-based tree containing a function or class
    descriptors for each function and class defined in the module with a
    `def` or `class` statement. The returned dictionary maps
    module-level function and class names to their descriptors. Nested
    objects are entered into the children dictionary of their parent. As
    with readmodule, *module* names the module to be read and *path* is
    prepended to sys.path. If the module being read is a package, the
    returned dictionary has a key `'__path__'` whose value is a list
    containing the package search path.

New in version 3.7: Descriptors for nested definitions. They are accessed through the
new children attribute. Each has a new parent attribute.
```

**crawl4ai**
```
[ ![Python logo](https://docs.python.org/3.10/_static/py.svg) ](https://www.python.org/) dev (3.15) 3.14 3.13 3.12 3.11 3.10.20 3.9 3.8 3.7 3.6 3.5 3.4 3.3 3.2 3.1 3.0 2.7 2.6
Greek | Ελληνικά English Spanish | español French | français Italian | italiano Japanese | 日本語 Korean | 한국어 Polish | polski Brazilian Portuguese | Português brasileiro Romanian | Românește Turkish | Türkçe Simplified Chinese | 简体中文 Traditional Chinese | 繁體中文
Theme  Auto Light Dark
### [Table of Contents](https://docs.python.org/3.10/contents.html)
  * [`pyclbr` — Python module browser support](https://docs.python.org/3.10/library/pyclbr.html#)
    * [Function Objects](https://docs.python.org/3.10/library/pyclbr.html#function-objects)
    * [Class Objects](https://docs.python.org/3.10/library/pyclbr.html#class-objects)


#### Previous topic
[`tabnanny` — Detection of ambiguous indentation](https://docs.python.org/3.10/library/tabnanny.html "previous chapter")
#### Next topic
[`py_compile` — Compile Python source files](https://docs.python.org/3.10/library/py_compile.html "next chapter")
### This Page
  * [Report a Bug](https://docs.python.org/3.10/bugs.html)
  * [Show Source ](https://github.com/python/cpython/blob/3.10/Doc/library/pyclbr.rst)


### Navigation
  * [index](https://docs.python.org/3.10/genindex.html "General Index")
  * [modules](https://docs.python.org/3.10/py-modindex.html "Python Module Index") |
  * [next](https://docs.python.org/3.10/library/py_compile.html "py_compile — Compile Python source files") |
  * [previous](https://docs.python.org/3.10/library/tabnanny.html "tabnanny — Detection of ambiguous indentation") |
  * ![Python logo](https://docs.python.org/3.10/_static/py.svg)
  * [Python](https://www.python.org/) »
  * Greek | Ελληνικά English Spanish | español French | français Italian | italiano Japanese | 日本語 Korean | 한국어 Polish | polski Brazilian Portuguese | Português brasileiro Romanian | Românește Turkish | Türkçe Simplified Chinese | 简体中文 Traditional Chinese | 繁體中文
dev (3.15) 3.14 3.13 3.12 3.11 3.10.20 3.9 3.8 3.7 3.6 3.5 3.4 3.3 3.2 3.1 3.0 2.7 2.6
  * [3.10.20 Documentation](https://docs.python.org/3.10/index.html) » 
  * [The Python Standard Library](https://docs.python.org/3.10/library/index.html) »
  * [Python Language Services](https://docs.python.org/3.10/library/language.html) »
  * [`pyclbr` — Python module browser support](https://docs.python.org/3.10/library/pyclbr.html)
  * | 
  * Theme  Auto Light Dark |


#  [`pyclbr`](https://docs.python.org/3.10/library/pyclbr.html#module-pyclbr "pyclbr: Supports information extraction for a Python module browser.") — Python module browser support[¶](https://docs.python.org/3.10/library/pyclbr.html#module-pyclbr "Permalink to this headline")
**Source code:** [Lib/pyclbr.py](https://github.com/python/cpython/tree/3.10/Lib/pyclbr.py)
* * *
The [`pyclbr`](https://docs.python.org/3.10/library/pyclbr.html#module-pyclbr "pyclbr: Supports information extraction for a Python module browser.") module provides limited information about the functions, classes, and methods defined in a Python-coded module. The information is sufficient to implement a module browser. The information is extracted from the Python source code rather than by importing the module, so this module is safe to use with untrusted code. This restriction makes it impossible to use this module with modules not implemented in Python, including all standard and optional extension modules. 
```

**crawl4ai-raw**
```
[ ![Python logo](https://docs.python.org/3.10/_static/py.svg) ](https://www.python.org/) dev (3.15) 3.14 3.13 3.12 3.11 3.10.20 3.9 3.8 3.7 3.6 3.5 3.4 3.3 3.2 3.1 3.0 2.7 2.6
Greek | Ελληνικά English Spanish | español French | français Italian | italiano Japanese | 日本語 Korean | 한국어 Polish | polski Brazilian Portuguese | Português brasileiro Romanian | Românește Turkish | Türkçe Simplified Chinese | 简体中文 Traditional Chinese | 繁體中文
Theme  Auto Light Dark
### [Table of Contents](https://docs.python.org/3.10/contents.html)
  * [`pyclbr` — Python module browser support](https://docs.python.org/3.10/library/pyclbr.html#)
    * [Function Objects](https://docs.python.org/3.10/library/pyclbr.html#function-objects)
    * [Class Objects](https://docs.python.org/3.10/library/pyclbr.html#class-objects)


#### Previous topic
[`tabnanny` — Detection of ambiguous indentation](https://docs.python.org/3.10/library/tabnanny.html "previous chapter")
#### Next topic
[`py_compile` — Compile Python source files](https://docs.python.org/3.10/library/py_compile.html "next chapter")
### This Page
  * [Report a Bug](https://docs.python.org/3.10/bugs.html)
  * [Show Source ](https://github.com/python/cpython/blob/3.10/Doc/library/pyclbr.rst)


### Navigation
  * [index](https://docs.python.org/3.10/genindex.html "General Index")
  * [modules](https://docs.python.org/3.10/py-modindex.html "Python Module Index") |
  * [next](https://docs.python.org/3.10/library/py_compile.html "py_compile — Compile Python source files") |
  * [previous](https://docs.python.org/3.10/library/tabnanny.html "tabnanny — Detection of ambiguous indentation") |
  * ![Python logo](https://docs.python.org/3.10/_static/py.svg)
  * [Python](https://www.python.org/) »
  * Greek | Ελληνικά English Spanish | español French | français Italian | italiano Japanese | 日本語 Korean | 한국어 Polish | polski Brazilian Portuguese | Português brasileiro Romanian | Românește Turkish | Türkçe Simplified Chinese | 简体中文 Traditional Chinese | 繁體中文
dev (3.15) 3.14 3.13 3.12 3.11 3.10.20 3.9 3.8 3.7 3.6 3.5 3.4 3.3 3.2 3.1 3.0 2.7 2.6
  * [3.10.20 Documentation](https://docs.python.org/3.10/index.html) » 
  * [The Python Standard Library](https://docs.python.org/3.10/library/index.html) »
  * [Python Language Services](https://docs.python.org/3.10/library/language.html) »
  * [`pyclbr` — Python module browser support](https://docs.python.org/3.10/library/pyclbr.html)
  * | 
  * Theme  Auto Light Dark |


#  [`pyclbr`](https://docs.python.org/3.10/library/pyclbr.html#module-pyclbr "pyclbr: Supports information extraction for a Python module browser.") — Python module browser support[¶](https://docs.python.org/3.10/library/pyclbr.html#module-pyclbr "Permalink to this headline")
**Source code:** [Lib/pyclbr.py](https://github.com/python/cpython/tree/3.10/Lib/pyclbr.py)
* * *
The [`pyclbr`](https://docs.python.org/3.10/library/pyclbr.html#module-pyclbr "pyclbr: Supports information extraction for a Python module browser.") module provides limited information about the functions, classes, and methods defined in a Python-coded module. The information is sufficient to implement a module browser. The information is extracted from the Python source code rather than by importing the module, so this module is safe to use with untrusted code. This restriction makes it impossible to use this module with modules not implemented in Python, including all standard and optional extension modules. 
```

**scrapy+md**
```
Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [`pyclbr` — Python module browser support](#)
  + [Function Objects](#function-objects)
  + [Class Objects](#class-objects)

#### Previous topic

[`tabnanny` — Detection of ambiguous indentation](tabnanny.html "previous chapter")

#### Next topic

[`py_compile` — Compile Python source files](py_compile.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/3.10/Doc/library/pyclbr.rst)

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](py_compile.html "py_compile — Compile Python source files") |
* [previous](tabnanny.html "tabnanny — Detection of ambiguous indentation") |
* [Python](https://www.python.org/) »

* [3.10.20 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [Python Language Services](language.html) »
* `pyclbr` — Python module browser support
* |
* Theme
  Auto
  Light
```

**crawlee**
```
pyclbr — Python module browser support — Python 3.10.20 documentation

















@media only screen {
table.full-width-table {
width: 100%;
}
}



dev (3.15)3.143.133.123.113.10.203.93.83.73.63.53.43.33.23.13.02.72.6

Greek | ΕλληνικάEnglishSpanish | españolFrench | françaisItalian | italianoJapanese | 日本語Korean | 한국어Polish | polskiBrazilian Portuguese | Português brasileiroRomanian | RomâneșteTurkish | TürkçeSimplified Chinese | 简体中文Traditional Chinese | 繁體中文

Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [`pyclbr` — Python module browser support](#)
  + [Function Objects](#function-objects)
  + [Class Objects](#class-objects)
```

**colly+md**
```
pyclbr — Python module browser support — Python 3.10.20 documentation

















@media only screen {
table.full-width-table {
width: 100%;
}
}



Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [`pyclbr` — Python module browser support](#)
  + [Function Objects](#function-objects)
  + [Class Objects](#class-objects)

#### Previous topic

[`tabnanny` — Detection of ambiguous indentation](tabnanny.html "previous chapter")
```

**playwright**
```
pyclbr — Python module browser support — Python 3.10.20 documentation

















@media only screen {
table.full-width-table {
width: 100%;
}
}



dev (3.15)3.143.133.123.113.10.203.93.83.73.63.53.43.33.23.13.02.72.6

Greek | ΕλληνικάEnglishSpanish | españolFrench | françaisItalian | italianoJapanese | 日本語Korean | 한국어Polish | polskiBrazilian Portuguese | Português brasileiroRomanian | RomâneșteTurkish | TürkçeSimplified Chinese | 简体中文Traditional Chinese | 繁體中文

Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [`pyclbr` — Python module browser support](#)
  + [Function Objects](#function-objects)
  + [Class Objects](#class-objects)
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [2]</summary>

| URL | markcrawl words [6] / preamble [2] | crawl4ai words [6] / preamble [2] | crawl4ai-raw words [6] / preamble [2] | scrapy+md words [6] / preamble [2] | crawlee words [6] / preamble [2] | colly+md words [6] / preamble [2] | playwright words [6] / preamble [2] | firecrawl words [6] / preamble [2] |
|---|---|---|---|---|---|---|---|---|
| docs.python.org/2.6 | 189 / 0 | 323 / 0 | 323 / 0 | — | 349 / 20 | 349 / 20 | 349 / 20 | — |
| docs.python.org/2.7 | 186 / 0 | 320 / 28 | 320 / 28 | — | 315 / 30 | 309 / 30 | 315 / 30 | — |
| docs.python.org/2.7/about.html | 179 / 0 | 352 / 28 | 352 / 28 | — | 343 / 34 | 337 / 34 | 343 / 34 | — |
| docs.python.org/2.7/bugs.html | 604 / 0 | 787 / 28 | 787 / 28 | — | 779 / 33 | 773 / 33 | 779 / 33 | — |
| docs.python.org/2.7/c-api/index.html | 276 / 0 | 447 / 28 | 447 / 28 | — | 439 / 35 | 433 / 35 | 439 / 35 | — |
| docs.python.org/2.7/contents.html | 12899 / 0 | 13051 / 28 | 13051 / 28 | — | 13041 / 34 | 13035 / 34 | 13041 / 34 | — |
| docs.python.org/2.7/download.html | 246 / 0 | 384 / 28 | 384 / 28 | — | 357 / 32 | 351 / 32 | 357 / 32 | — |
| docs.python.org/2.7/extending/index.html | 394 / 0 | 574 / 28 | 574 / 28 | — | 568 / 37 | 562 / 37 | 568 / 37 | — |
| docs.python.org/2.7/glossary.html | 5184 / 0 | 5287 / 28 | 5287 / 28 | — | 5356 / 32 | 5350 / 32 | 5356 / 32 | — |
| docs.python.org/2.7/howto/index.html | 52 / 0 | 304 / 28 | 304 / 28 | — | 294 / 33 | 288 / 33 | 294 / 33 | — |
| docs.python.org/2.7/installing/index.html | 1143 / 0 | 1421 / 28 | 1421 / 28 | — | 1413 / 34 | 1407 / 34 | 1413 / 34 | — |
| docs.python.org/2.7/library/index.html | 2969 / 0 | 3138 / 28 | 3138 / 28 | — | 3129 / 35 | 3123 / 35 | 3129 / 35 | — |
| docs.python.org/2.7/license.html | 6376 / 0 | 6656 / 28 | 6656 / 28 | — | 6647 / 34 | 6641 / 34 | 6647 / 34 | — |
| docs.python.org/2.7/py-modindex.html | 5398 / 0 | 5580 / 28 | 5580 / 28 | — | 5565 / 37 | 5559 / 37 | 5565 / 37 | — |
| docs.python.org/2.7/reference/index.html | 380 / 0 | 554 / 28 | 554 / 28 | — | 546 / 35 | 540 / 35 | 546 / 35 | — |
| docs.python.org/2.7/tutorial/index.html | 928 / 0 | 1105 / 28 | 1105 / 28 | — | 1096 / 34 | 1090 / 34 | 1096 / 34 | — |
| docs.python.org/2.7/using/index.html | 248 / 0 | 419 / 28 | 419 / 28 | — | 411 / 35 | 405 / 35 | 411 / 35 | — |
| docs.python.org/2.7/whatsnew/2.7.html | 16861 / 0 | 17267 / 28 | 17267 / 28 | — | 17275 / 36 | 17269 / 36 | 17275 / 36 | — |
| docs.python.org/2.7/whatsnew/index.html | 823 / 0 | 997 / 28 | 997 / 28 | — | 989 / 35 | 983 / 35 | 989 / 35 | — |
| docs.python.org/3.0 | 183 / 0 | 281 / 0 | 281 / 0 | — | 307 / 20 | 307 / 20 | 307 / 20 | — |
| docs.python.org/3.0/about.html | 878 / 0 | 1003 / 0 | 1003 / 0 | — | 1021 / 22 | 1021 / 22 | 1021 / 22 | — |
| docs.python.org/3.0/bugs.html | 459 / 0 | 531 / 0 | 531 / 0 | — | 553 / 23 | 553 / 23 | 553 / 23 | — |
| docs.python.org/3.0/c-api/index.html | 288 / 0 | 363 / 0 | 363 / 0 | — | 386 / 23 | 386 / 23 | 386 / 23 | — |
| docs.python.org/3.0/contents.html | 8408 / 0 | 8477 / 0 | 8477 / 0 | — | 8495 / 22 | 8495 / 22 | 8495 / 22 | — |
| docs.python.org/3.0/copyright.html | 94 / 0 | 176 / 0 | 176 / 0 | — | 191 / 20 | 191 / 20 | 191 / 20 | — |
| docs.python.org/3.0/distutils/index.html | 632 / 0 | 711 / 0 | 711 / 0 | — | 733 / 22 | 733 / 22 | 733 / 22 | — |
| docs.python.org/3.0/documenting/index.html | 240 / 0 | 314 / 0 | 314 / 0 | — | 332 / 21 | 332 / 21 | 332 / 21 | — |
| docs.python.org/3.0/download.html | 243 / 0 | 297 / 0 | 297 / 0 | — | 314 / 20 | 314 / 20 | 314 / 20 | — |
| docs.python.org/3.0/extending/index.html | 375 / 0 | 454 / 0 | 454 / 0 | — | 479 / 25 | 479 / 25 | 479 / 25 | — |
| docs.python.org/3.0/genindex.html | 91 / 0 | 198 / 0 | 198 / 0 | — | 211 / 20 | 211 / 20 | 211 / 20 | — |
| docs.python.org/3.0/glossary.html | 3770 / 0 | 3791 / 0 | 3791 / 0 | — | 3871 / 20 | 3871 / 20 | 3871 / 20 | — |
| docs.python.org/3.0/howto/index.html | 141 / 0 | 223 / 0 | 223 / 0 | — | 241 / 21 | 241 / 21 | 241 / 21 | — |
| docs.python.org/3.0/install/index.html | 6166 / 0 | 6261 / 0 | 6261 / 0 | — | 6259 / 22 | 6259 / 22 | 6259 / 22 | — |
| docs.python.org/3.0/library/index.html | 2022 / 0 | 2093 / 0 | 2093 / 0 | — | 2116 / 23 | 2116 / 23 | 2116 / 23 | — |
| docs.python.org/3.0/license.html | 4649 / 0 | 4803 / 0 | 4803 / 0 | — | 4822 / 22 | 4822 / 22 | 4822 / 22 | — |
| docs.python.org/3.0/modindex.html | 3599 / 0 | 3667 / 0 | 3667 / 0 | — | 3669 / 25 | 3669 / 25 | 3669 / 25 | — |
| docs.python.org/3.0/reference/index.html | 357 / 0 | 432 / 0 | 432 / 0 | — | 455 / 23 | 455 / 23 | 455 / 23 | — |
| docs.python.org/3.0/search.html | 51 / 0 | 105 / 0 | 105 / 0 | — | 122 / 20 | 122 / 20 | 122 / 20 | — |
| docs.python.org/3.0/tutorial/index.html | 840 / 0 | 919 / 0 | 919 / 0 | — | 941 / 22 | 941 / 22 | 941 / 22 | — |
| docs.python.org/3.0/using/index.html | 240 / 0 | 326 / 0 | 326 / 0 | — | 344 / 21 | 344 / 21 | 344 / 21 | — |
| docs.python.org/3.0/whatsnew/3.0.html | 5433 / 0 | 5676 / 0 | 5676 / 0 | — | 5689 / 24 | 5689 / 24 | 5689 / 24 | — |
| docs.python.org/3.0/whatsnew/index.html | 836 / 0 | 919 / 0 | 919 / 0 | — | 938 / 23 | 938 / 23 | 938 / 23 | — |
| docs.python.org/3.1 | 191 / 0 | 315 / 0 | 315 / 0 | — | 341 / 20 | 341 / 20 | 341 / 20 | — |
| docs.python.org/3.1/about.html | 881 / 0 | 1016 / 0 | 1016 / 0 | — | 1035 / 22 | 1035 / 22 | 1035 / 22 | — |
| docs.python.org/3.1/bugs.html | 538 / 0 | 676 / 0 | 676 / 0 | — | 696 / 21 | 696 / 21 | 696 / 21 | — |
| docs.python.org/3.1/c-api/index.html | 328 / 0 | 418 / 0 | 418 / 0 | — | 441 / 23 | 441 / 23 | 441 / 23 | — |
| docs.python.org/3.1/contents.html | 11438 / 0 | 11520 / 0 | 11520 / 0 | — | 11538 / 22 | 11538 / 22 | 11538 / 22 | — |
| docs.python.org/3.1/copyright.html | 96 / 0 | 187 / 0 | 187 / 0 | — | 202 / 20 | 202 / 20 | 202 / 20 | — |
| docs.python.org/3.1/distutils/index.html | 736 / 0 | 830 / 0 | 830 / 0 | — | 852 / 22 | 852 / 22 | 852 / 22 | — |
| docs.python.org/3.1/documenting/index.html | 188 / 0 | 277 / 0 | 277 / 0 | — | 295 / 21 | 295 / 21 | 295 / 21 | — |
| docs.python.org/3.1/download.html | 243 / 0 | 310 / 0 | 310 / 0 | — | 327 / 20 | 327 / 20 | 327 / 20 | — |
| docs.python.org/3.1/extending/index.html | 410 / 0 | 506 / 0 | 506 / 0 | — | 531 / 25 | 531 / 25 | 531 / 25 | — |
| docs.python.org/3.1/faq/index.html | 29 / 29 | 204 / 0 | 204 / 0 | — | 227 / 23 | 227 / 23 | 227 / 23 | — |
| docs.python.org/3.1/genindex.html | 104 / 0 | 211 / 0 | 211 / 0 | — | 228 / 20 | 228 / 20 | 228 / 20 | — |
| docs.python.org/3.1/glossary.html | 4196 / 0 | 4228 / 0 | 4228 / 0 | — | 4314 / 20 | 4314 / 20 | 4314 / 20 | — |
| docs.python.org/3.1/howto/index.html | 152 / 0 | 245 / 0 | 245 / 0 | — | 263 / 21 | 263 / 21 | 263 / 21 | — |
| docs.python.org/3.1/install/index.html | 6226 / 0 | 6339 / 0 | 6339 / 0 | — | 6334 / 22 | 6334 / 22 | 6334 / 22 | — |
| docs.python.org/3.1/library/index.html | 2300 / 0 | 2388 / 0 | 2388 / 0 | — | 2411 / 23 | 2411 / 23 | 2411 / 23 | — |
| docs.python.org/3.1/license.html | 6281 / 0 | 6464 / 0 | 6464 / 0 | — | 6481 / 22 | 6481 / 22 | 6481 / 22 | — |
| docs.python.org/3.1/modindex.html | 3649 / 0 | 3731 / 0 | 3731 / 0 | — | 3738 / 25 | 3738 / 25 | 3738 / 25 | — |
| docs.python.org/3.1/reference/index.html | 429 / 0 | 521 / 0 | 521 / 0 | — | 544 / 23 | 544 / 23 | 544 / 23 | — |
| docs.python.org/3.1/search.html | 51 / 0 | 118 / 0 | 118 / 0 | — | 135 / 20 | 135 / 20 | 135 / 20 | — |
| docs.python.org/3.1/tutorial/index.html | 968 / 0 | 1062 / 0 | 1062 / 0 | — | 1084 / 22 | 1084 / 22 | 1084 / 22 | — |
| docs.python.org/3.1/using/index.html | 250 / 0 | 398 / 0 | 398 / 0 | — | 418 / 23 | 418 / 23 | 418 / 23 | — |
| docs.python.org/3.1/whatsnew/3.1.html | 2974 / 0 | 3167 / 0 | 3167 / 0 | — | 3194 / 24 | 3194 / 24 | 3194 / 24 | — |
| docs.python.org/3.1/whatsnew/index.html | 858 / 0 | 954 / 0 | 954 / 0 | — | 973 / 23 | 973 / 23 | 973 / 23 | — |
| docs.python.org/3.10 | 190 / 0 | 711 / 68 | 711 / 68 | 521 / 4 | 629 / 47 | 533 / 16 | 629 / 47 | — |
| docs.python.org/3.10/about.html | 180 / 0 | 604 / 68 | 604 / 68 | 407 / 4 | 520 / 52 | 424 / 21 | 520 / 52 | — |
| docs.python.org/3.10/bugs.html | 666 / 0 | 1104 / 68 | 1104 / 68 | 913 / 4 | 1026 / 52 | 930 / 21 | 1026 / 52 | — |
| docs.python.org/3.10/c-api/apiabiversion.html | 240 / 0 | 656 / 68 | 656 / 68 | 465 / 4 | 579 / 53 | 483 / 22 | 579 / 53 | — |
| docs.python.org/3.10/c-api/arg.html | 4786 / 0 | 5210 / 68 | 5210 / 68 | 5075 / 4 | 5190 / 54 | 5094 / 23 | 5190 / 54 | — |
| docs.python.org/3.10/c-api/bytes.html | 1173 / 0 | 1584 / 68 | 1584 / 68 | 1400 / 4 | 1512 / 51 | 1416 / 20 | 1512 / 51 | — |
| docs.python.org/3.10/c-api/call.html | 2257 / 0 | 2751 / 68 | 2751 / 68 | 2536 / 4 | 2648 / 51 | 2552 / 20 | 2648 / 51 | — |
| docs.python.org/3.10/c-api/cell.html | 341 / 0 | 755 / 68 | 755 / 68 | 564 / 4 | 676 / 51 | 580 / 20 | 676 / 51 | — |
| docs.python.org/3.10/c-api/code.html | 399 / 0 | 838 / 68 | 838 / 68 | 618 / 4 | 730 / 51 | 634 / 20 | 730 / 51 | — |
| docs.python.org/3.10/c-api/codec.html | 899 / 0 | 1338 / 68 | 1338 / 68 | 1164 / 4 | 1279 / 54 | 1183 / 23 | 1279 / 54 | — |
| docs.python.org/3.10/c-api/datetime.html | 1262 / 0 | 1676 / 68 | 1676 / 68 | 1493 / 4 | 1605 / 51 | 1509 / 20 | 1605 / 51 | — |
| docs.python.org/3.10/c-api/dict.html | 1461 / 0 | 1865 / 68 | 1865 / 68 | 1680 / 4 | 1792 / 51 | 1696 / 20 | 1792 / 51 | — |
| docs.python.org/3.10/c-api/exceptions.html | 6000 / 0 | 6509 / 68 | 6509 / 68 | 6295 / 4 | 6407 / 51 | 6311 / 20 | 6407 / 51 | — |
| docs.python.org/3.10/c-api/gcsupport.html | 1284 / 0 | 1728 / 68 | 1728 / 68 | 1545 / 4 | 1659 / 53 | 1563 / 22 | 1659 / 53 | — |
| docs.python.org/3.10/c-api/import.html | 2010 / 0 | 2412 / 68 | 2412 / 68 | 2233 / 4 | 2345 / 51 | 2249 / 20 | 2345 / 51 | — |
| docs.python.org/3.10/c-api/index.html | 427 / 0 | 837 / 68 | 837 / 68 | 640 / 4 | 754 / 53 | 658 / 22 | 754 / 53 | — |
| docs.python.org/3.10/c-api/init.html | 9920 / 0 | 10601 / 68 | 10601 / 68 | 10501 / 4 | 10615 / 53 | 10519 / 22 | 10615 / 53 | — |
| docs.python.org/3.10/c-api/init_config.html | 5810 / 0 | 6237 / 68 | 6237 / 68 | 6123 / 4 | 6236 / 52 | 6140 / 21 | 6236 / 52 | — |
| docs.python.org/3.10/c-api/intro.html | 4747 / 0 | 5225 / 68 | 5225 / 68 | 5042 / 4 | 5153 / 50 | 5057 / 19 | 5153 / 50 | — |
| docs.python.org/3.10/c-api/iter.html | 331 / 0 | 742 / 68 | 742 / 68 | 550 / 4 | 662 / 51 | 566 / 20 | 662 / 51 | — |
| docs.python.org/3.10/c-api/list.html | 809 / 0 | 1219 / 68 | 1219 / 68 | 1028 / 4 | 1140 / 51 | 1044 / 20 | 1140 / 51 | — |
| docs.python.org/3.10/c-api/long.html | 1626 / 0 | 2018 / 68 | 2018 / 68 | 1849 / 4 | 1961 / 51 | 1865 / 20 | 1961 / 51 | — |
| docs.python.org/3.10/c-api/module.html | 3388 / 0 | 3833 / 68 | 3833 / 68 | 3663 / 4 | 3775 / 51 | 3679 / 20 | 3775 / 51 | — |
| docs.python.org/3.10/c-api/number.html | 2106 / 0 | 2495 / 68 | 2495 / 68 | 2325 / 4 | 2437 / 51 | 2341 / 20 | 2437 / 51 | — |
| docs.python.org/3.10/c-api/refcounting.html | 719 / 0 | 1130 / 68 | 1130 / 68 | 940 / 4 | 1052 / 51 | 956 / 20 | 1052 / 51 | — |
| docs.python.org/3.10/c-api/reflection.html | 357 / 0 | 775 / 68 | 775 / 68 | 590 / 4 | 701 / 50 | 605 / 19 | 701 / 50 | — |
| docs.python.org/3.10/c-api/set.html | 1013 / 0 | 1411 / 68 | 1411 / 68 | 1232 / 4 | 1344 / 51 | 1248 / 20 | 1344 / 51 | — |
| docs.python.org/3.10/c-api/stable.html | 980 / 0 | 3894 / 68 | 3894 / 68 | 3695 / 4 | 3808 / 52 | 3712 / 21 | 3808 / 52 | — |
| docs.python.org/3.10/c-api/structures.html | 2619 / 0 | 3074 / 68 | 3074 / 68 | 2902 / 4 | 3015 / 52 | 2919 / 21 | 3015 / 52 | — |
| docs.python.org/3.10/c-api/tuple.html | 1271 / 0 | 1708 / 68 | 1708 / 68 | 1520 / 4 | 1632 / 51 | 1536 / 20 | 1632 / 51 | — |
| docs.python.org/3.10/c-api/type.html | 1541 / 0 | 1945 / 68 | 1945 / 68 | 1790 / 4 | 1902 / 51 | 1806 / 20 | 1902 / 51 | — |
| docs.python.org/3.10/c-api/typeobj.html | 12666 / 0 | 14124 / 68 | 14124 / 68 | 13963 / 4 | 14075 / 51 | 13979 / 20 | 14075 / 51 | — |
| docs.python.org/3.10/c-api/unicode.html | 10151 / 0 | 10726 / 68 | 10726 / 68 | 10552 / 4 | 10666 / 53 | 10570 / 22 | 10666 / 53 | — |
| docs.python.org/3.10/c-api/veryhigh.html | 2443 / 0 | 2891 / 68 | 2891 / 68 | 2662 / 4 | 2777 / 54 | 2681 / 23 | 2777 / 54 | — |
| docs.python.org/3.10/contents.html | 19401 / 0 | 19782 / 68 | 19782 / 68 | 19584 / 4 | 19697 / 52 | 19601 / 21 | 19697 / 52 | — |
| docs.python.org/3.10/copyright.html | 58 / 0 | 460 / 68 | 460 / 68 | 261 / 4 | 372 / 50 | 276 / 19 | 372 / 50 | — |
| docs.python.org/3.10/distributing/index.html | 976 / 0 | 1481 / 68 | 1481 / 68 | 1285 / 4 | 1402 / 52 | 1306 / 21 | 1402 / 52 | — |
| docs.python.org/3.10/download.html | 277 / 0 | 599 / 68 | 599 / 68 | 404 / 4 | 515 / 50 | 419 / 19 | 515 / 50 | — |
| docs.python.org/3.10/extending/index.html | 578 / 0 | 1108 / 68 | 1108 / 68 | 912 / 4 | 1028 / 55 | 932 / 24 | 1028 / 55 | — |
| docs.python.org/3.10/faq/index.html | 65 / 65 | 454 / 68 | 454 / 68 | 257 / 4 | 371 / 53 | 275 / 22 | 371 / 53 | — |
| docs.python.org/3.10/genindex.html | 65 / 65 | 391 / 68 | 391 / 68 | 196 / 4 | 307 / 50 | 211 / 19 | 307 / 50 | — |
| docs.python.org/3.10/glossary.html | 7963 / 0 | 8264 / 68 | 8264 / 68 | 8186 / 4 | 8302 / 50 | 8201 / 19 | 8302 / 50 | — |
| docs.python.org/3.10/howto/annotations.html | 1520 / 0 | 1908 / 68 | 1908 / 68 | 1853 / 4 | 1966 / 52 | 1870 / 21 | 1966 / 52 | — |
| docs.python.org/3.10/howto/index.html | 52 / 0 | 553 / 68 | 553 / 68 | 356 / 4 | 468 / 51 | 372 / 20 | 468 / 51 | — |
| docs.python.org/3.10/installing/index.html | 1207 / 0 | 1808 / 68 | 1808 / 68 | 1612 / 4 | 1725 / 52 | 1629 / 21 | 1725 / 52 | — |
| docs.python.org/3.10/library/__main__.html | 1810 / 0 | 2311 / 68 | 2311 / 68 | 2127 / 4 | 2247 / 54 | 2146 / 23 | 2247 / 54 | — |
| docs.python.org/3.10/library/_thread.html | 1141 / 0 | 1569 / 68 | 1569 / 68 | 1380 / 4 | 1495 / 54 | 1399 / 23 | 1495 / 54 | — |
| docs.python.org/3.10/library/abc.html | 1594 / 0 | 2031 / 68 | 2031 / 68 | 1843 / 4 | 1958 / 54 | 1862 / 23 | 1958 / 54 | — |
| docs.python.org/3.10/library/array.html | 1450 / 0 | 1874 / 68 | 1874 / 68 | 1697 / 4 | 1814 / 56 | 1718 / 25 | 1814 / 56 | — |
| docs.python.org/3.10/library/ast.html | 8584 / 0 | 9114 / 68 | 9114 / 68 | 8945 / 4 | 9112 / 54 | 8964 / 23 | 9112 / 54 | — |
| docs.python.org/3.10/library/asynchat.html | 1060 / 0 | 1543 / 68 | 1543 / 68 | 1353 / 4 | 1469 / 55 | 1373 / 24 | 1469 / 55 | — |
| docs.python.org/3.10/library/asyncio-api-index.html | 591 / 0 | 1049 / 68 | 1049 / 68 | 870 / 4 | 983 / 52 | 887 / 21 | 983 / 52 | — |
| docs.python.org/3.10/library/asyncio-task.html | 4157 / 0 | 4762 / 68 | 4762 / 68 | 4544 / 4 | 4659 / 52 | 4561 / 21 | 4659 / 52 | — |
| docs.python.org/3.10/library/asyncio.html | 223 / 0 | 724 / 68 | 724 / 68 | 524 / 4 | 639 / 53 | 542 / 22 | 639 / 53 | — |
| docs.python.org/3.10/library/atexit.html | 579 / 0 | 1062 / 68 | 1062 / 68 | 862 / 4 | 976 / 53 | 880 / 22 | 976 / 53 | — |
| docs.python.org/3.10/library/audioop.html | 1616 / 0 | 2082 / 68 | 2082 / 68 | 1869 / 4 | 1985 / 55 | 1889 / 24 | 1985 / 55 | — |
| docs.python.org/3.10/library/base64.html | 1616 / 0 | 2126 / 68 | 2126 / 68 | 1919 / 4 | 2038 / 57 | 1941 / 26 | 2038 / 57 | — |
| docs.python.org/3.10/library/bdb.html | 2171 / 0 | 2599 / 68 | 2599 / 68 | 2414 / 4 | 2528 / 53 | 2432 / 22 | 2528 / 53 | — |
| docs.python.org/3.10/library/binary.html | 98 / 0 | 677 / 68 | 677 / 68 | 480 / 4 | 593 / 52 | 497 / 21 | 593 / 52 | — |
| docs.python.org/3.10/library/bisect.html | 1347 / 0 | 1876 / 68 | 1876 / 68 | 1640 / 4 | 1758 / 54 | 1659 / 23 | 1758 / 54 | — |
| docs.python.org/3.10/library/builtins.html | 200 / 0 | 658 / 68 | 658 / 68 | 459 / 4 | 573 / 53 | 477 / 22 | 573 / 53 | — |
| docs.python.org/3.10/library/bz2.html | 1666 / 0 | 2187 / 68 | 2187 / 68 | 1981 / 4 | 2100 / 55 | 2001 / 24 | 2100 / 55 | — |
| docs.python.org/3.10/library/cgi.html | 3396 / 0 | 3961 / 68 | 3961 / 68 | 3759 / 4 | 3875 / 55 | 3779 / 24 | 3875 / 55 | — |
| docs.python.org/3.10/library/cgitb.html | 568 / 0 | 1031 / 68 | 1031 / 68 | 827 / 4 | 944 / 56 | 848 / 25 | 944 / 56 | — |
| docs.python.org/3.10/library/cmd.html | 1926 / 0 | 2402 / 68 | 2402 / 68 | 2209 / 4 | 2326 / 56 | 2230 / 25 | 2326 / 56 | — |
| docs.python.org/3.10/library/code.html | 1097 / 0 | 1575 / 68 | 1575 / 68 | 1374 / 4 | 1489 / 54 | 1393 / 23 | 1489 / 54 | — |
| docs.python.org/3.10/library/codecs.html | 8089 / 0 | 8731 / 68 | 8731 / 68 | 8530 / 4 | 8648 / 56 | 8551 / 25 | 8648 / 56 | — |
| docs.python.org/3.10/library/collections.abc.html | 1989 / 0 | 2453 / 68 | 2453 / 68 | 2294 / 4 | 2414 / 56 | 2315 / 25 | 2414 / 56 | — |
| docs.python.org/3.10/library/collections.html | 7020 / 0 | 7592 / 68 | 7592 / 68 | 7389 / 4 | 7533 / 53 | 7407 / 22 | 7533 / 53 | — |
| docs.python.org/3.10/library/colorsys.html | 256 / 0 | 717 / 68 | 717 / 68 | 511 / 4 | 628 / 55 | 531 / 24 | 628 / 55 | — |
| docs.python.org/3.10/library/constants.html | 572 / 0 | 999 / 68 | 999 / 68 | 809 / 4 | 921 / 51 | 825 / 20 | 921 / 51 | — |
| docs.python.org/3.10/library/contextlib.html | 4524 / 0 | 5056 / 68 | 5056 / 68 | 4915 / 4 | 5038 / 55 | 4935 / 24 | 5038 / 55 | — |
| docs.python.org/3.10/library/ctypes.html | 13276 / 0 | 13960 / 68 | 13960 / 68 | 13819 / 4 | 14006 / 57 | 13841 / 26 | 14006 / 57 | — |
| docs.python.org/3.10/library/curses.html | 9380 / 0 | 9874 / 68 | 9874 / 68 | 9702 / 4 | 9819 / 56 | 9723 / 25 | 9819 / 56 | — |
| docs.python.org/3.10/library/dataclasses.html | 4336 / 0 | 4833 / 68 | 4833 / 68 | 4671 / 4 | 4785 / 53 | 4689 / 22 | 4785 / 53 | — |
| docs.python.org/3.10/library/datetime.html | 14043 / 0 | 14623 / 68 | 14623 / 68 | 14458 / 4 | 14601 / 56 | 14479 / 25 | 14601 / 56 | — |
| docs.python.org/3.10/library/debug.html | 261 / 0 | 693 / 68 | 693 / 68 | 496 / 4 | 609 / 52 | 513 / 21 | 609 / 52 | — |
| docs.python.org/3.10/library/decimal.html | 10530 / 0 | 11095 / 68 | 11095 / 68 | 10905 / 4 | 11070 / 58 | 10928 / 27 | 11070 / 58 | — |
| docs.python.org/3.10/library/difflib.html | 4304 / 0 | 4881 / 68 | 4881 / 68 | 4617 / 4 | 4753 / 55 | 4637 / 24 | 4753 / 55 | — |
| docs.python.org/3.10/library/distribution.html | 50 / 0 | 580 / 68 | 580 / 68 | 383 / 4 | 497 / 53 | 401 / 22 | 497 / 53 | — |
| docs.python.org/3.10/library/distutils.html | 323 / 0 | 779 / 68 | 779 / 68 | 578 / 4 | 695 / 56 | 599 / 25 | 695 / 56 | — |
| docs.python.org/3.10/library/email.generator.html | 1903 / 0 | 2374 / 68 | 2374 / 68 | 2158 / 4 | 2272 / 53 | 2176 / 22 | 2272 / 53 | — |
| docs.python.org/3.10/library/email.html | 1130 / 0 | 1660 / 68 | 1660 / 68 | 1467 / 4 | 1585 / 57 | 1489 / 26 | 1585 / 57 | — |
| docs.python.org/3.10/library/email.policy.html | 3961 / 0 | 4388 / 68 | 4388 / 68 | 4222 / 4 | 4339 / 52 | 4239 / 21 | 4339 / 52 | — |
| docs.python.org/3.10/library/email.utils.html | 1462 / 0 | 1908 / 68 | 1908 / 68 | 1703 / 4 | 1816 / 52 | 1720 / 21 | 1816 / 52 | — |
| docs.python.org/3.10/library/ensurepip.html | 718 / 0 | 1220 / 68 | 1220 / 68 | 1019 / 4 | 1135 / 55 | 1039 / 24 | 1135 / 55 | — |
| docs.python.org/3.10/library/enum.html | 5317 / 0 | 6130 / 68 | 6130 / 68 | 5890 / 4 | 6062 / 54 | 5909 / 23 | 6062 / 54 | — |
| docs.python.org/3.10/library/errno.html | 1472 / 0 | 1825 / 68 | 1825 / 68 | 1749 / 4 | 1865 / 55 | 1769 / 24 | 1865 / 55 | — |
| docs.python.org/3.10/library/exceptions.html | 4688 / 0 | 5004 / 68 | 5004 / 68 | 4959 / 4 | 5071 / 51 | 4975 / 20 | 5071 / 51 | — |
| docs.python.org/3.10/library/faulthandler.html | 940 / 0 | 1470 / 68 | 1470 / 68 | 1269 / 4 | 1385 / 55 | 1289 / 24 | 1385 / 55 | — |
| docs.python.org/3.10/library/fileinput.html | 1371 / 0 | 1842 / 68 | 1842 / 68 | 1630 / 4 | 1749 / 58 | 1653 / 27 | 1749 / 58 | — |
| docs.python.org/3.10/library/fractions.html | 785 / 0 | 1238 / 68 | 1238 / 68 | 1050 / 4 | 1168 / 53 | 1068 / 22 | 1168 / 53 | — |
| docs.python.org/3.10/library/frameworks.html | 224 / 0 | 646 / 68 | 646 / 68 | 449 / 4 | 561 / 51 | 465 / 20 | 561 / 51 | — |
| docs.python.org/3.10/library/functions.html | 11862 / 0 | 12437 / 68 | 12437 / 68 | 12219 / 4 | 12350 / 51 | 12235 / 20 | 12350 / 51 | — |
| docs.python.org/3.10/library/gc.html | 1628 / 0 | 2049 / 68 | 2049 / 68 | 1877 / 4 | 1994 / 54 | 1896 / 23 | 1994 / 54 | — |
| docs.python.org/3.10/library/glob.html | 666 / 0 | 1141 / 68 | 1141 / 68 | 933 / 4 | 1052 / 56 | 954 / 25 | 1052 / 56 | — |
| docs.python.org/3.10/library/graphlib.html | 1203 / 0 | 1674 / 68 | 1674 / 68 | 1482 / 4 | 1602 / 57 | 1504 / 26 | 1602 / 57 | — |
| docs.python.org/3.10/library/grp.html | 335 / 0 | 782 / 68 | 782 / 68 | 588 / 4 | 703 / 54 | 607 / 23 | 703 / 54 | — |
| docs.python.org/3.10/library/gzip.html | 1449 / 0 | 1965 / 68 | 1965 / 68 | 1756 / 4 | 1872 / 55 | 1776 / 24 | 1872 / 55 | — |
| docs.python.org/3.10/library/hashlib.html | 3609 / 0 | 4195 / 68 | 4195 / 68 | 3960 / 4 | 4093 / 56 | 3981 / 25 | 4093 / 56 | — |
| docs.python.org/3.10/library/html.html | 193 / 0 | 651 / 68 | 651 / 68 | 450 / 4 | 566 / 55 | 470 / 24 | 566 / 55 | — |
| docs.python.org/3.10/library/html.parser.html | 1522 / 0 | 2027 / 68 | 2027 / 68 | 1833 / 4 | 1957 / 56 | 1854 / 25 | 1957 / 56 | — |
| docs.python.org/3.10/library/http.client.html | 2920 / 0 | 3389 / 68 | 3389 / 68 | 3209 / 4 | 3330 / 54 | 3228 / 23 | 3330 / 54 | — |
| docs.python.org/3.10/library/http.server.html | 2802 / 0 | 3255 / 68 | 3255 / 68 | 3083 / 4 | 3197 / 53 | 3101 / 22 | 3197 / 53 | — |
| docs.python.org/3.10/library/idle.html | 6334 / 0 | 6990 / 68 | 6990 / 68 | 6857 / 4 | 6969 / 50 | 6872 / 19 | 6969 / 50 | — |
| docs.python.org/3.10/library/imghdr.html | 396 / 0 | 862 / 68 | 862 / 68 | 661 / 4 | 780 / 57 | 683 / 26 | 780 / 57 | — |
| docs.python.org/3.10/library/imp.html | 2270 / 0 | 2743 / 68 | 2743 / 68 | 2557 / 4 | 2673 / 55 | 2577 / 24 | 2673 / 55 | — |
| docs.python.org/3.10/library/importlib.html | 9157 / 0 | 9668 / 68 | 9668 / 68 | 9577 / 4 | 9694 / 55 | 9597 / 24 | 9694 / 55 | — |
| docs.python.org/3.10/library/importlib.metadata.html | 1419 / 0 | 1948 / 68 | 1948 / 68 | 1730 / 4 | 1863 / 51 | 1746 / 20 | 1863 / 51 | — |
| docs.python.org/3.10/library/index.html | 2282 / 0 | 2684 / 68 | 2684 / 68 | 2487 / 4 | 2601 / 53 | 2505 / 22 | 2601 / 53 | — |
| docs.python.org/3.10/library/inspect.html | 7199 / 0 | 7738 / 68 | 7738 / 68 | 7554 / 4 | 7678 / 54 | 7573 / 23 | 7678 / 54 | — |
| docs.python.org/3.10/library/io.html | 6375 / 0 | 6949 / 68 | 6949 / 68 | 6766 / 4 | 6885 / 57 | 6788 / 26 | 6885 / 57 | — |
| docs.python.org/3.10/library/itertools.html | 5234 / 0 | 5746 / 68 | 5746 / 68 | 5535 / 4 | 5655 / 57 | 5557 / 26 | 5655 / 57 | — |
| docs.python.org/3.10/library/json.html | 3807 / 0 | 4419 / 68 | 4419 / 68 | 4166 / 4 | 4291 / 55 | 4186 / 24 | 4291 / 55 | — |
| docs.python.org/3.10/library/language.html | 38 / 0 | 636 / 68 | 636 / 68 | 439 / 4 | 552 / 52 | 456 / 21 | 552 / 52 | — |
| docs.python.org/3.10/library/logging.config.html | 5080 / 0 | 5655 / 68 | 5655 / 68 | 5461 / 4 | 5575 / 53 | 5479 / 22 | 5575 / 53 | — |
| docs.python.org/3.10/library/logging.handlers.html | 6934 / 0 | 7443 / 68 | 7443 / 68 | 7281 / 4 | 7395 / 53 | 7299 / 22 | 7395 / 53 | — |
| docs.python.org/3.10/library/logging.html | 9093 / 0 | 9665 / 68 | 9665 / 68 | 9481 / 4 | 9597 / 55 | 9501 / 24 | 9597 / 55 | — |
| docs.python.org/3.10/library/lzma.html | 2417 / 0 | 2960 / 68 | 2960 / 68 | 2748 / 4 | 2865 / 56 | 2769 / 25 | 2865 / 56 | — |
| docs.python.org/3.10/library/mailcap.html | 683 / 0 | 1151 / 68 | 1151 / 68 | 946 / 4 | 1062 / 54 | 965 / 23 | 1062 / 54 | — |
| docs.python.org/3.10/library/markup.html | 360 / 0 | 810 / 68 | 810 / 68 | 613 / 4 | 727 / 53 | 631 / 22 | 727 / 53 | — |
| docs.python.org/3.10/library/mm.html | 37 / 0 | 496 / 68 | 496 / 68 | 299 / 4 | 411 / 51 | 315 / 20 | 411 / 51 | — |
| docs.python.org/3.10/library/mmap.html | 2045 / 0 | 2521 / 68 | 2521 / 68 | 2328 / 4 | 2443 / 54 | 2347 / 23 | 2443 / 54 | — |
| docs.python.org/3.10/library/modulefinder.html | 388 / 0 | 883 / 68 | 883 / 68 | 685 / 4 | 803 / 57 | 707 / 26 | 803 / 57 | — |
| docs.python.org/3.10/library/modules.html | 38 / 0 | 619 / 68 | 619 / 68 | 422 / 4 | 534 / 51 | 438 / 20 | 534 / 51 | — |
| docs.python.org/3.10/library/msilib.html | 2265 / 0 | 2951 / 68 | 2951 / 68 | 2675 / 4 | 2793 / 57 | 2697 / 26 | 2793 / 57 | — |
| docs.python.org/3.10/library/netdata.html | 261 / 0 | 705 / 68 | 705 / 68 | 508 / 4 | 621 / 52 | 525 / 21 | 621 / 52 | — |
| docs.python.org/3.10/library/nntplib.html | 3114 / 0 | 3636 / 68 | 3636 / 68 | 3421 / 4 | 3546 / 54 | 3440 / 23 | 3546 / 54 | — |
| docs.python.org/3.10/library/numbers.html | 1026 / 0 | 1503 / 68 | 1503 / 68 | 1331 / 4 | 1447 / 55 | 1351 / 24 | 1447 / 55 | — |
| docs.python.org/3.10/library/operator.html | 2403 / 0 | 2949 / 68 | 2949 / 68 | 2704 / 4 | 2824 / 55 | 2724 / 24 | 2824 / 55 | — |
| docs.python.org/3.10/library/optparse.html | 10934 / 0 | 11683 / 68 | 11683 / 68 | 11559 / 4 | 11677 / 56 | 11580 / 25 | 11677 / 56 | — |
| docs.python.org/3.10/library/os.html | 24682 / 0 | 25322 / 68 | 25322 / 68 | 25098 / 4 | 25215 / 55 | 25118 / 24 | 25215 / 55 | — |
| docs.python.org/3.10/library/os.path.html | 2744 / 0 | 3193 / 68 | 3193 / 68 | 3011 / 4 | 3132 / 54 | 3030 / 23 | 3132 / 54 | — |
| docs.python.org/3.10/library/pathlib.html | 4727 / 0 | 5624 / 68 | 5624 / 68 | 5380 / 4 | 5569 / 54 | 5399 / 23 | 5569 / 54 | — |
| docs.python.org/3.10/library/pdb.html | 3220 / 0 | 3677 / 68 | 3677 / 68 | 3491 / 4 | 3608 / 54 | 3510 / 23 | 3608 / 54 | — |
| docs.python.org/3.10/library/pickle.html | 7266 / 0 | 7872 / 68 | 7872 / 68 | 7667 / 4 | 7785 / 54 | 7686 / 23 | 7785 / 54 | — |
| docs.python.org/3.10/library/pipes.html | 438 / 0 | 915 / 68 | 915 / 68 | 719 / 4 | 836 / 55 | 739 / 24 | 836 / 55 | — |
| docs.python.org/3.10/library/pkgutil.html | 1566 / 0 | 2034 / 68 | 2034 / 68 | 1833 / 4 | 1948 / 54 | 1852 / 23 | 1948 / 54 | — |
| docs.python.org/3.10/library/platform.html | 1359 / 0 | 1891 / 68 | 1891 / 68 | 1694 / 4 | 1812 / 57 | 1716 / 26 | 1812 / 57 | — |
| docs.python.org/3.10/library/pprint.html | 1887 / 0 | 2411 / 68 | 2411 / 68 | 2172 / 4 | 2295 / 54 | 2191 / 23 | 2295 / 54 | — |
| docs.python.org/3.10/library/py_compile.html | 976 / 0 | 1455 / 68 | 1455 / 68 | 1259 / 4 | 1375 / 55 | 1279 / 24 | 1375 / 55 | — |
| docs.python.org/3.10/library/pyclbr.html | 681 / 0 | 1160 / 68 | 1160 / 68 | 974 / 4 | 1090 / 55 | 994 / 24 | 1090 / 55 | — |
| docs.python.org/3.10/library/queue.html | 1520 / 0 | 1985 / 68 | 1985 / 68 | 1795 / 4 | 1911 / 55 | 1815 / 24 | 1911 / 55 | — |
| docs.python.org/3.10/library/random.html | 3281 / 0 | 3806 / 68 | 3806 / 68 | 3606 / 4 | 3724 / 54 | 3625 / 23 | 3724 / 54 | — |
| docs.python.org/3.10/library/rlcompleter.html | 349 / 0 | 825 / 68 | 825 / 68 | 624 / 4 | 742 / 56 | 645 / 25 | 742 / 56 | — |
| docs.python.org/3.10/library/runpy.html | 1239 / 0 | 1707 / 68 | 1707 / 68 | 1506 / 4 | 1623 / 56 | 1527 / 25 | 1623 / 56 | — |
| docs.python.org/3.10/library/select.html | 3079 / 0 | 3578 / 68 | 3578 / 68 | 3404 / 4 | 3520 / 55 | 3424 / 24 | 3520 / 55 | — |
| docs.python.org/3.10/library/shelve.html | 1303 / 0 | 1792 / 68 | 1792 / 68 | 1586 / 4 | 1701 / 54 | 1605 / 23 | 1701 / 54 | — |
| docs.python.org/3.10/library/shutil.html | 4501 / 0 | 5083 / 68 | 5083 / 68 | 4838 / 4 | 4956 / 54 | 4857 / 23 | 4956 / 54 | — |
| docs.python.org/3.10/library/signal.html | 3708 / 0 | 4214 / 68 | 4214 / 68 | 4045 / 4 | 4162 / 56 | 4066 / 25 | 4162 / 56 | — |
| docs.python.org/3.10/library/sndhdr.html | 308 / 0 | 757 / 68 | 757 / 68 | 559 / 4 | 676 / 56 | 580 / 25 | 676 / 56 | — |
| docs.python.org/3.10/library/socket.html | 11142 / 0 | 11663 / 68 | 11663 / 68 | 11493 / 4 | 11610 / 54 | 11512 / 23 | 11610 / 54 | — |
| docs.python.org/3.10/library/socketserver.html | 3148 / 0 | 3651 / 68 | 3651 / 68 | 3479 / 4 | 3596 / 56 | 3500 / 25 | 3596 / 56 | — |
| docs.python.org/3.10/library/sqlite3.html | 8282 / 0 | 9053 / 68 | 9053 / 68 | 8886 / 4 | 9019 / 57 | 8908 / 26 | 9019 / 57 | — |
| docs.python.org/3.10/library/ssl.html | 14127 / 0 | 14692 / 68 | 14692 / 68 | 14602 / 4 | 14739 / 56 | 14623 / 25 | 14739 / 56 | — |
| docs.python.org/3.10/library/stat.html | 1676 / 0 | 2080 / 68 | 2080 / 68 | 1947 / 4 | 2062 / 54 | 1966 / 23 | 2062 / 54 | — |
| docs.python.org/3.10/library/statistics.html | 4959 / 0 | 5509 / 68 | 5509 / 68 | 5284 / 4 | 5437 / 54 | 5303 / 23 | 5437 / 54 | — |
| docs.python.org/3.10/library/stdtypes.html | 27083 / 0 | 28128 / 68 | 28128 / 68 | 27914 / 4 | 28140 / 51 | 27930 / 20 | 28140 / 51 | — |
| docs.python.org/3.10/library/string.html | 4993 / 0 | 5531 / 68 | 5531 / 68 | 5311 / 4 | 5439 / 54 | 5330 / 23 | 5439 / 54 | — |
| docs.python.org/3.10/library/struct.html | 3237 / 0 | 3793 / 68 | 3793 / 68 | 3574 / 4 | 3702 / 57 | 3596 / 26 | 3702 / 57 | — |
| docs.python.org/3.10/library/subprocess.html | 8197 / 0 | 8859 / 68 | 8859 / 68 | 8676 / 4 | 8795 / 53 | 8694 / 22 | 8795 / 53 | — |
| docs.python.org/3.10/library/superseded.html | 531 / 0 | 981 / 68 | 981 / 68 | 784 / 4 | 896 / 51 | 800 / 20 | 896 / 51 | — |
| docs.python.org/3.10/library/symtable.html | 821 / 0 | 1292 / 68 | 1292 / 68 | 1130 / 4 | 1249 / 57 | 1152 / 26 | 1249 / 57 | — |
| docs.python.org/3.10/library/sys.html | 9831 / 0 | 10228 / 68 | 10228 / 68 | 10086 / 4 | 10204 / 55 | 10106 / 24 | 10204 / 55 | — |
| docs.python.org/3.10/library/sysconfig.html | 1372 / 0 | 1884 / 68 | 1884 / 68 | 1683 / 4 | 1802 / 57 | 1705 / 26 | 1802 / 57 | — |
| docs.python.org/3.10/library/tarfile.html | 6635 / 0 | 7156 / 68 | 7156 / 68 | 7002 / 4 | 7120 / 57 | 7024 / 26 | 7120 / 57 | — |
| docs.python.org/3.10/library/telnetlib.html | 1179 / 0 | 1662 / 68 | 1662 / 68 | 1474 / 4 | 1589 / 53 | 1492 / 22 | 1589 / 53 | — |
| docs.python.org/3.10/library/tempfile.html | 2306 / 0 | 2856 / 68 | 2856 / 68 | 2611 / 4 | 2730 / 56 | 2632 / 25 | 2730 / 56 | — |
| docs.python.org/3.10/library/termios.html | 529 / 0 | 1005 / 68 | 1005 / 68 | 806 / 4 | 922 / 55 | 826 / 24 | 922 / 55 | — |
| docs.python.org/3.10/library/textwrap.html | 1542 / 0 | 2016 / 68 | 2016 / 68 | 1793 / 4 | 1912 / 55 | 1813 / 24 | 1912 / 55 | — |
| docs.python.org/3.10/library/threading.html | 6512 / 0 | 7008 / 68 | 7008 / 68 | 6839 / 4 | 6953 / 53 | 6857 / 22 | 6953 / 53 | — |
| docs.python.org/3.10/library/time.html | 4751 / 0 | 5234 / 68 | 5234 / 68 | 5072 / 4 | 5192 / 55 | 5092 / 24 | 5192 / 55 | — |
| docs.python.org/3.10/library/tkinter.colorchooser.html | 120 / 0 | 577 / 68 | 577 / 68 | 377 / 4 | 492 / 54 | 396 / 23 | 492 / 54 | — |
| docs.python.org/3.10/library/tkinter.html | 6333 / 0 | 6895 / 68 | 6895 / 68 | 6766 / 4 | 6883 / 55 | 6786 / 24 | 6883 / 55 | — |
| docs.python.org/3.10/library/tkinter.messagebox.html | 161 / 0 | 626 / 68 | 626 / 68 | 402 / 4 | 517 / 54 | 421 / 23 | 517 / 54 | — |
| docs.python.org/3.10/library/tkinter.scrolledtext.html | 168 / 0 | 622 / 68 | 622 / 68 | 425 / 4 | 540 / 54 | 444 / 23 | 540 / 54 | — |
| docs.python.org/3.10/library/traceback.html | 2518 / 0 | 3039 / 68 | 3039 / 68 | 2819 / 4 | 2939 / 57 | 2841 / 26 | 2939 / 57 | — |
| docs.python.org/3.10/library/tracemalloc.html | 3466 / 0 | 4008 / 68 | 4008 / 68 | 3849 / 4 | 3964 / 54 | 3868 / 23 | 3964 / 54 | — |
| docs.python.org/3.10/library/tty.html | 159 / 0 | 608 / 68 | 608 / 68 | 408 / 4 | 523 / 54 | 427 / 23 | 523 / 54 | — |
| docs.python.org/3.10/library/types.html | 2140 / 0 | 2633 / 68 | 2633 / 68 | 2467 / 4 | 2588 / 59 | 2491 / 28 | 2588 / 59 | — |
| docs.python.org/3.10/library/typing.html | 10829 / 0 | 11365 / 68 | 11365 / 68 | 11300 / 4 | 11420 / 55 | 11320 / 24 | 11420 / 55 | — |
| docs.python.org/3.10/library/unicodedata.html | 813 / 0 | 1249 / 68 | 1249 / 68 | 1064 / 4 | 1179 / 53 | 1082 / 22 | 1179 / 53 | — |
| docs.python.org/3.10/library/unittest.html | 12854 / 0 | 13518 / 68 | 13518 / 68 | 13265 / 4 | 13382 / 54 | 13284 / 23 | 13382 / 54 | — |
| docs.python.org/3.10/library/unittest.mock-examples.htm | 6546 / 0 | 7369 / 68 | 7369 / 68 | 7099 / 4 | 7287 / 53 | 7117 / 22 | 7287 / 53 | — |
| docs.python.org/3.10/library/urllib.parse.html | 4143 / 0 | 4711 / 68 | 4711 / 68 | 4472 / 4 | 4594 / 55 | 4492 / 24 | 4594 / 55 | — |
| docs.python.org/3.10/library/urllib.robotparser.html | 401 / 0 | 847 / 68 | 847 / 68 | 656 / 4 | 772 / 54 | 675 / 23 | 772 / 54 | — |
| docs.python.org/3.10/library/venv.html | 3268 / 0 | 3798 / 68 | 3798 / 68 | 3598 / 4 | 3714 / 55 | 3618 / 24 | 3714 / 55 | — |
| docs.python.org/3.10/library/winreg.html | 3520 / 0 | 4028 / 68 | 4028 / 68 | 3851 / 4 | 3967 / 54 | 3870 / 23 | 3967 / 54 | — |
| docs.python.org/3.10/library/xdrlib.html | 1244 / 0 | 1700 / 68 | 1700 / 68 | 1531 / 4 | 1648 / 56 | 1552 / 25 | 1648 / 56 | — |
| docs.python.org/3.10/library/xml.sax.handler.html | 2295 / 0 | 2771 / 68 | 2771 / 68 | 2604 / 4 | 2721 / 56 | 2625 / 25 | 2721 / 56 | — |
| docs.python.org/3.10/library/xml.sax.html | 1025 / 0 | 1524 / 68 | 1524 / 68 | 1326 / 4 | 1442 / 55 | 1346 / 24 | 1442 / 55 | — |
| docs.python.org/3.10/library/xmlrpc.client.html | 2693 / 0 | 3224 / 68 | 3224 / 68 | 3038 / 4 | 3153 / 54 | 3057 / 23 | 3153 / 54 | — |
| docs.python.org/3.10/library/xmlrpc.html | 81 / 0 | 541 / 68 | 541 / 68 | 344 / 4 | 461 / 56 | 365 / 25 | 461 / 56 | — |
| docs.python.org/3.10/library/xmlrpc.server.html | 2007 / 0 | 2509 / 68 | 2509 / 68 | 2312 / 4 | 2427 / 54 | 2331 / 23 | 2427 / 54 | — |
| docs.python.org/3.10/library/zipimport.html | 959 / 0 | 1416 / 68 | 1416 / 68 | 1232 / 4 | 1349 / 56 | 1253 / 25 | 1349 / 56 | — |
| docs.python.org/3.10/library/zlib.html | 2078 / 0 | 2527 / 68 | 2527 / 68 | 2331 / 4 | 2447 / 55 | 2351 / 24 | 2447 / 55 | — |
| docs.python.org/3.10/license.html | 6986 / 0 | 7625 / 68 | 7625 / 68 | 7445 / 4 | 7558 / 52 | 7462 / 21 | 7558 / 52 | — |
| docs.python.org/3.10/py-modindex.html | 4026 / 0 | 4420 / 68 | 4420 / 68 | 4208 / 4 | 4324 / 55 | 4228 / 24 | 4324 / 55 | — |
| docs.python.org/3.10/reference/compound_stmts.html | 7246 / 0 | 7950 / 68 | 7950 / 68 | 7742 / 4 | 7859 / 52 | 7759 / 21 | 7859 / 52 | — |
| docs.python.org/3.10/reference/datamodel.html | 16528 / 0 | 17235 / 68 | 17235 / 68 | 17101 / 4 | 17220 / 52 | 17118 / 21 | 17220 / 52 | — |
| docs.python.org/3.10/reference/expressions.html | 10437 / 0 | 11184 / 68 | 11184 / 68 | 10976 / 4 | 11090 / 51 | 10992 / 20 | 11090 / 51 | — |
| docs.python.org/3.10/reference/grammar.html | 1881 / 0 | 2303 / 68 | 2303 / 68 | 2106 / 4 | 2220 / 53 | 2124 / 22 | 2220 / 53 | — |
| docs.python.org/3.10/reference/index.html | 438 / 0 | 844 / 68 | 844 / 68 | 647 / 4 | 761 / 53 | 665 / 22 | 761 / 53 | — |
| docs.python.org/3.10/reference/lexical_analysis.html | 5123 / 0 | 5797 / 68 | 5797 / 68 | 5564 / 4 | 5681 / 52 | 5581 / 21 | 5681 / 52 | — |
| docs.python.org/3.10/search.html | 21 / 0 | 340 / 68 | 340 / 68 | 145 / 4 | 390 / 184 | 294 / 153 | 390 / 184 | — |
| docs.python.org/3.10/tutorial/appendix.html | 693 / 0 | 1187 / 68 | 1187 / 68 | 990 / 4 | 1103 / 51 | 1006 / 20 | 1103 / 51 | — |
| docs.python.org/3.10/tutorial/index.html | 982 / 0 | 1382 / 68 | 1382 / 68 | 1185 / 4 | 1298 / 52 | 1202 / 21 | 1298 / 52 | — |
| docs.python.org/3.10/using/cmdline.html | 4940 / 0 | 5393 / 68 | 5393 / 68 | 5264 / 4 | 5379 / 54 | 5283 / 23 | 5379 / 54 | — |
| docs.python.org/3.10/using/configure.html | 3330 / 0 | 3873 / 68 | 3873 / 68 | 3757 / 4 | 3872 / 52 | 3774 / 21 | 3872 / 52 | — |
| docs.python.org/3.10/using/editors.html | 46 / 0 | 480 / 68 | 480 / 68 | 283 / 4 | 397 / 53 | 301 / 22 | 397 / 53 | — |
| docs.python.org/3.10/using/index.html | 460 / 0 | 870 / 68 | 870 / 68 | 673 / 4 | 787 / 53 | 691 / 22 | 787 / 53 | — |
| docs.python.org/3.10/using/mac.html | 963 / 0 | 1524 / 68 | 1524 / 68 | 1328 / 4 | 1444 / 55 | 1348 / 24 | 1444 / 55 | — |
| docs.python.org/3.10/using/unix.html | 685 / 0 | 1235 / 68 | 1235 / 68 | 1044 / 4 | 1160 / 55 | 1064 / 24 | 1160 / 55 | — |
| docs.python.org/3.10/using/windows.html | 7057 / 0 | 7873 / 68 | 7873 / 68 | 7690 / 4 | 7806 / 54 | 7709 / 23 | 7806 / 54 | — |
| docs.python.org/3.10/whatsnew/2.0.html | 9031 / 0 | 9636 / 68 | 9636 / 68 | 9440 / 4 | 9556 / 54 | 9459 / 23 | 9556 / 54 | — |
| docs.python.org/3.10/whatsnew/2.1.html | 5603 / 0 | 6202 / 68 | 6202 / 68 | 6016 / 4 | 6133 / 54 | 6035 / 23 | 6133 / 54 | — |
| docs.python.org/3.10/whatsnew/2.2.html | 8889 / 0 | 9506 / 68 | 9506 / 68 | 9306 / 4 | 9429 / 54 | 9325 / 23 | 9429 / 54 | — |
| docs.python.org/3.10/whatsnew/2.3.html | 13061 / 0 | 13822 / 68 | 13822 / 68 | 13604 / 4 | 13752 / 54 | 13623 / 23 | 13752 / 54 | — |
| docs.python.org/3.10/whatsnew/2.4.html | 9193 / 0 | 9879 / 68 | 9879 / 68 | 9664 / 4 | 9806 / 54 | 9683 / 23 | 9806 / 54 | — |
| docs.python.org/3.10/whatsnew/2.5.html | 14271 / 0 | 14998 / 68 | 14998 / 68 | 14804 / 4 | 14927 / 54 | 14823 / 23 | 14927 / 54 | — |
| docs.python.org/3.10/whatsnew/2.6.html | 18020 / 0 | 18895 / 68 | 18895 / 68 | 18673 / 4 | 18827 / 54 | 18692 / 23 | 18827 / 54 | — |
| docs.python.org/3.10/whatsnew/2.7.html | 16678 / 0 | 17596 / 68 | 17596 / 68 | 17381 / 4 | 17529 / 54 | 17400 / 23 | 17529 / 54 | — |
| docs.python.org/3.10/whatsnew/3.0.html | 5654 / 0 | 6289 / 68 | 6289 / 68 | 6095 / 4 | 6210 / 54 | 6114 / 23 | 6210 / 54 | — |
| docs.python.org/3.10/whatsnew/3.1.html | 2814 / 0 | 3356 / 68 | 3356 / 68 | 3149 / 4 | 3278 / 54 | 3168 / 23 | 3278 / 54 | — |
| docs.python.org/3.10/whatsnew/3.10.html | 12579 / 0 | 13749 / 68 | 13749 / 68 | 13627 / 4 | 13773 / 54 | 13646 / 23 | 13773 / 54 | — |
| docs.python.org/3.10/whatsnew/3.2.html | 14445 / 0 | 15360 / 68 | 15360 / 68 | 15093 / 4 | 15268 / 54 | 15112 / 23 | 15268 / 54 | — |
| docs.python.org/3.10/whatsnew/3.3.html | 13058 / 0 | 14601 / 68 | 14601 / 68 | 14419 / 4 | 14550 / 54 | 14438 / 23 | 14550 / 54 | — |
| docs.python.org/3.10/whatsnew/3.4.html | 15521 / 0 | 16605 / 68 | 16605 / 68 | 16408 / 4 | 16528 / 54 | 16427 / 23 | 16528 / 54 | — |
| docs.python.org/3.10/whatsnew/3.5.html | 12043 / 0 | 13260 / 68 | 13260 / 68 | 13052 / 4 | 13191 / 54 | 13071 / 23 | 13191 / 54 | — |
| docs.python.org/3.10/whatsnew/3.6.html | 12378 / 0 | 13727 / 68 | 13727 / 68 | 13533 / 4 | 13656 / 54 | 13552 / 23 | 13656 / 54 | — |
| docs.python.org/3.10/whatsnew/3.7.html | 13451 / 0 | 14690 / 68 | 14690 / 68 | 14509 / 4 | 14624 / 54 | 14528 / 23 | 14624 / 54 | — |
| docs.python.org/3.10/whatsnew/3.8.html | 11745 / 0 | 12704 / 68 | 12704 / 68 | 12486 / 4 | 12619 / 54 | 12505 / 23 | 12619 / 54 | — |
| docs.python.org/3.10/whatsnew/3.9.html | 8718 / 0 | 9585 / 68 | 9585 / 68 | 9408 / 4 | 9526 / 54 | 9427 / 23 | 9526 / 54 | — |
| docs.python.org/3.10/whatsnew/changelog.html | 183653 / 0 | 188265 / 68 | 188265 / 68 | 188054 / 4 | 188169 / 50 | 188069 / 19 | 188169 / 50 | — |
| docs.python.org/3.10/whatsnew/index.html | 2172 / 0 | 2587 / 68 | 2587 / 68 | 2389 / 4 | 2503 / 53 | 2407 / 22 | 2503 / 53 | — |
| docs.python.org/3.11 | 188 / 0 | 711 / 68 | 711 / 68 | 522 / 4 | 629 / 47 | 534 / 16 | 629 / 47 | — |
| docs.python.org/3.11/about.html | 207 / 27 | 606 / 68 | 606 / 68 | 410 / 4 | 522 / 52 | 427 / 21 | 522 / 52 | — |
| docs.python.org/3.11/bugs.html | 698 / 32 | 1106 / 68 | 1106 / 68 | 916 / 4 | 1028 / 52 | 933 / 21 | 1028 / 52 | — |
| docs.python.org/3.11/c-api/index.html | 463 / 33 | 842 / 68 | 842 / 68 | 646 / 4 | 759 / 53 | 664 / 22 | 759 / 53 | — |
| docs.python.org/3.11/contents.html | 20504 / 31 | 20856 / 68 | 20856 / 68 | 20659 / 4 | 20771 / 52 | 20676 / 21 | 20771 / 52 | — |
| docs.python.org/3.11/copyright.html | 85 / 27 | 462 / 68 | 462 / 68 | 264 / 4 | 374 / 50 | 279 / 19 | 374 / 50 | — |
| docs.python.org/3.11/distributing/index.html | 34 / 0 | 384 / 68 | 384 / 68 | 188 / 4 | 300 / 52 | 205 / 21 | 300 / 52 | — |
| docs.python.org/3.11/download.html | 261 / 0 | 585 / 68 | 585 / 68 | 391 / 4 | 501 / 50 | 406 / 19 | 501 / 50 | — |
| docs.python.org/3.11/extending/index.html | 613 / 35 | 1110 / 68 | 1110 / 68 | 915 / 4 | 1030 / 55 | 935 / 24 | 1030 / 55 | — |
| docs.python.org/3.11/faq/index.html | 97 / 97 | 456 / 68 | 456 / 68 | 260 / 4 | 373 / 53 | 278 / 22 | 373 / 53 | — |
| docs.python.org/3.11/glossary.html | 8486 / 32 | 8760 / 68 | 8760 / 68 | 8680 / 4 | 8795 / 50 | 8695 / 19 | 8795 / 50 | — |
| docs.python.org/3.11/howto/index.html | 82 / 30 | 556 / 68 | 556 / 68 | 360 / 4 | 471 / 51 | 376 / 20 | 471 / 51 | — |
| docs.python.org/3.11/installing/index.html | 1236 / 27 | 1816 / 68 | 1816 / 68 | 1621 / 4 | 1733 / 52 | 1638 / 21 | 1733 / 52 | — |
| docs.python.org/3.11/library/index.html | 2332 / 29 | 2707 / 68 | 2707 / 68 | 2511 / 4 | 2624 / 53 | 2529 / 22 | 2624 / 53 | — |
| docs.python.org/3.11/license.html | 7696 / 32 | 8309 / 68 | 8309 / 68 | 8130 / 4 | 8242 / 52 | 8147 / 21 | 8242 / 52 | — |
| docs.python.org/3.11/py-modindex.html | 4102 / 0 | 4498 / 68 | 4498 / 68 | 4287 / 4 | 4402 / 55 | 4307 / 24 | 4402 / 55 | — |
| docs.python.org/3.11/reference/index.html | 471 / 33 | 846 / 68 | 846 / 68 | 650 / 4 | 763 / 53 | 668 / 22 | 763 / 53 | — |
| docs.python.org/3.11/search.html | 13 / 0 | 334 / 68 | 334 / 68 | 147 / 4 | 437 / 230 | 342 / 199 | 437 / 230 | — |
| docs.python.org/3.11/tutorial/index.html | 1024 / 28 | 1398 / 68 | 1398 / 68 | 1202 / 4 | 1314 / 52 | 1219 / 21 | 1314 / 52 | — |
| docs.python.org/3.11/using/index.html | 508 / 32 | 888 / 68 | 888 / 68 | 692 / 4 | 805 / 53 | 710 / 22 | 805 / 53 | — |
| docs.python.org/3.11/whatsnew/3.11.html | 13307 / 32 | 14517 / 68 | 14517 / 68 | 14330 / 4 | 14445 / 54 | 14349 / 23 | 14445 / 54 | — |
| docs.python.org/3.11/whatsnew/index.html | 2390 / 34 | 2773 / 68 | 2773 / 68 | 2576 / 4 | 2689 / 53 | 2594 / 22 | 2689 / 53 | — |
| docs.python.org/3.12 | 195 / 4 | 712 / 68 | 712 / 68 | 525 / 4 | 632 / 47 | 537 / 16 | 632 / 47 | — |
| docs.python.org/3.12/about.html | 211 / 26 | 609 / 68 | 609 / 68 | 415 / 4 | 527 / 52 | 432 / 21 | 527 / 52 | — |
| docs.python.org/3.12/bugs.html | 724 / 32 | 1130 / 68 | 1130 / 68 | 942 / 4 | 1054 / 52 | 959 / 21 | 1054 / 52 | — |
| docs.python.org/3.12/c-api/index.html | 447 / 33 | 824 / 68 | 824 / 68 | 630 / 4 | 743 / 53 | 648 / 22 | 743 / 53 | — |
| docs.python.org/3.12/contents.html | 19884 / 30 | 20235 / 68 | 20235 / 68 | 20040 / 4 | 20152 / 52 | 20057 / 21 | 20152 / 52 | — |
| docs.python.org/3.12/deprecations/index.html | 2635 / 28 | 3378 / 68 | 3378 / 68 | 3182 / 4 | 3292 / 50 | 3197 / 19 | 3292 / 50 | — |
| docs.python.org/3.12/download.html | 267 / 3 | 586 / 68 | 586 / 68 | 394 / 4 | 504 / 50 | 409 / 19 | 504 / 50 | — |
| docs.python.org/3.12/extending/index.html | 607 / 35 | 1102 / 68 | 1102 / 68 | 909 / 4 | 1024 / 55 | 929 / 24 | 1024 / 55 | — |
| docs.python.org/3.12/glossary.html | 8740 / 29 | 8999 / 68 | 8999 / 68 | 8909 / 4 | 9039 / 50 | 8924 / 19 | 9039 / 50 | — |
| docs.python.org/3.12/howto/index.html | 177 / 29 | 562 / 68 | 562 / 68 | 368 / 4 | 479 / 51 | 384 / 20 | 479 / 51 | — |
| docs.python.org/3.12/installing/index.html | 1233 / 27 | 1811 / 68 | 1811 / 68 | 1618 / 4 | 1730 / 52 | 1635 / 21 | 1730 / 52 | — |
| docs.python.org/3.12/library/index.html | 2316 / 29 | 2689 / 68 | 2689 / 68 | 2495 / 4 | 2608 / 53 | 2513 / 22 | 2608 / 53 | — |
| docs.python.org/3.12/license.html | 7747 / 32 | 8320 / 68 | 8320 / 68 | 8143 / 4 | 8255 / 52 | 8160 / 21 | 8255 / 52 | — |
| docs.python.org/3.12/py-modindex.html | 3602 / 0 | 3996 / 68 | 3996 / 68 | 3787 / 4 | 3902 / 55 | 3807 / 24 | 3902 / 55 | — |
| docs.python.org/3.12/reference/index.html | 481 / 33 | 854 / 68 | 854 / 68 | 660 / 4 | 773 / 53 | 678 / 22 | 773 / 53 | — |
| docs.python.org/3.12/tutorial/index.html | 1023 / 28 | 1395 / 68 | 1395 / 68 | 1201 / 4 | 1313 / 52 | 1218 / 21 | 1313 / 52 | — |
| docs.python.org/3.12/using/index.html | 534 / 32 | 912 / 68 | 912 / 68 | 718 / 4 | 831 / 53 | 736 / 22 | 831 / 53 | — |
| docs.python.org/3.12/whatsnew/3.12.html | 15327 / 33 | 16742 / 68 | 16742 / 68 | 16524 / 4 | 16660 / 54 | 16543 / 23 | 16660 / 54 | — |
| docs.python.org/3.12/whatsnew/index.html | 2498 / 34 | 2879 / 68 | 2879 / 68 | 2684 / 4 | 2797 / 53 | 2702 / 22 | 2797 / 53 | — |
| docs.python.org/3.13 | 195 / 4 | 712 / 68 | 712 / 68 | 525 / 4 | 632 / 47 | 537 / 16 | 632 / 47 | — |
| docs.python.org/3.13/about.html | 211 / 26 | 609 / 68 | 609 / 68 | 415 / 4 | 527 / 52 | 432 / 21 | 527 / 52 | — |
| docs.python.org/3.13/c-api/index.html | 496 / 33 | 873 / 68 | 873 / 68 | 679 / 4 | 792 / 53 | 697 / 22 | 792 / 53 | — |
| docs.python.org/3.13/contents.html | 20979 / 27 | 21333 / 68 | 21333 / 68 | 21138 / 4 | 21250 / 52 | 21155 / 21 | 21250 / 52 | — |
| docs.python.org/3.13/copyright.html | 85 / 27 | 460 / 68 | 460 / 68 | 264 / 4 | 374 / 50 | 279 / 19 | 374 / 50 | — |
| docs.python.org/3.13/deprecations/index.html | 2811 / 28 | 3671 / 68 | 3671 / 68 | 3475 / 4 | 3585 / 50 | 3490 / 19 | 3585 / 50 | — |
| docs.python.org/3.13/download.html | 152 / 3 | 471 / 68 | 471 / 68 | 279 / 4 | 389 / 50 | 294 / 19 | 389 / 50 | — |
| docs.python.org/3.13/extending/index.html | 566 / 35 | 1062 / 68 | 1062 / 68 | 868 / 4 | 983 / 55 | 888 / 24 | 983 / 55 | — |
| docs.python.org/3.13/glossary.html | 10616 / 29 | 10850 / 68 | 10850 / 68 | 10785 / 4 | 10916 / 50 | 10800 / 19 | 10916 / 50 | — |
| docs.python.org/3.13/howto/index.html | 203 / 29 | 584 / 68 | 584 / 68 | 390 / 4 | 501 / 51 | 406 / 20 | 501 / 51 | — |
| docs.python.org/3.13/installing/index.html | 1010 / 31 | 1548 / 68 | 1548 / 68 | 1353 / 4 | 1465 / 52 | 1370 / 21 | 1465 / 52 | — |
| docs.python.org/3.13/library/index.html | 2153 / 29 | 2526 / 68 | 2526 / 68 | 2332 / 4 | 2445 / 53 | 2350 / 22 | 2445 / 53 | — |
| docs.python.org/3.13/license.html | 7923 / 32 | 8523 / 68 | 8523 / 68 | 8329 / 4 | 8441 / 52 | 8346 / 21 | 8441 / 52 | — |
| docs.python.org/3.13/py-modindex.html | 3489 / 0 | 3883 / 68 | 3883 / 68 | 3674 / 4 | 3789 / 55 | 3694 / 24 | 3789 / 55 | — |
| docs.python.org/3.13/tutorial/index.html | 1057 / 28 | 1429 / 68 | 1429 / 68 | 1235 / 4 | 1347 / 52 | 1252 / 21 | 1347 / 52 | — |
| docs.python.org/3.13/using/index.html | 313 / 32 | 691 / 68 | 691 / 68 | 497 / 4 | 610 / 53 | 515 / 22 | 610 / 53 | — |
| docs.python.org/3.13/whatsnew/3.13.html | 16950 / 33 | 18380 / 68 | 18380 / 68 | 18181 / 4 | 18302 / 54 | 18200 / 23 | 18302 / 54 | — |
| docs.python.org/3.13/whatsnew/index.html | 2572 / 34 | 2953 / 68 | 2953 / 68 | 2758 / 4 | 2871 / 53 | 2776 / 22 | 2871 / 53 | — |
| docs.python.org/3.14 | 195 / 4 | 712 / 68 | 712 / 68 | 525 / 4 | 632 / 47 | 537 / 16 | 632 / 47 | — |
| docs.python.org/3.14/about.html | 211 / 26 | 617 / 68 | 617 / 68 | 495 / 4 | 607 / 52 | 512 / 21 | 607 / 52 | — |
| docs.python.org/3.14/c-api/index.html | 589 / 33 | 974 / 68 | 974 / 68 | 852 / 4 | 965 / 53 | 870 / 22 | 965 / 53 | — |
| docs.python.org/3.14/contents.html | 22218 / 30 | 22582 / 68 | 22582 / 68 | 22454 / 4 | 22566 / 52 | 22471 / 21 | 22566 / 52 | — |
| docs.python.org/3.14/copyright.html | 86 / 28 | 468 / 68 | 468 / 68 | 344 / 4 | 454 / 50 | 359 / 19 | 454 / 50 | — |
| docs.python.org/3.14/deprecations/index.html | 3109 / 30 | 3782 / 68 | 3782 / 68 | 3659 / 4 | 3770 / 50 | 3674 / 19 | 3770 / 50 | — |
| docs.python.org/3.14/download.html | 132 / 3 | 451 / 68 | 451 / 68 | 259 / 4 | 369 / 50 | 274 / 19 | 369 / 50 | — |
| docs.python.org/3.14/extending/index.html | 566 / 35 | 1070 / 68 | 1070 / 68 | 948 / 4 | 1063 / 55 | 968 / 24 | 1063 / 55 | — |
| docs.python.org/3.14/glossary.html | 11351 / 29 | 11582 / 68 | 11582 / 68 | 11600 / 4 | 11731 / 50 | 11615 / 19 | 11731 / 50 | — |
| docs.python.org/3.14/howto/index.html | 207 / 29 | 596 / 68 | 596 / 68 | 474 / 4 | 585 / 51 | 490 / 20 | 585 / 51 | — |
| docs.python.org/3.14/library/index.html | 2236 / 29 | 2617 / 68 | 2617 / 68 | 2495 / 4 | 2608 / 53 | 2513 / 22 | 2608 / 53 | — |
| docs.python.org/3.14/py-modindex.html | 3551 / 0 | 3948 / 68 | 3948 / 68 | 3736 / 4 | 3851 / 55 | 3756 / 24 | 3851 / 55 | — |
| docs.python.org/3.14/reference/index.html | 498 / 33 | 879 / 68 | 879 / 68 | 757 / 4 | 870 / 53 | 775 / 22 | 870 / 53 | — |
| docs.python.org/3.14/tutorial/index.html | 1057 / 28 | 1437 / 68 | 1437 / 68 | 1315 / 4 | 1427 / 52 | 1332 / 21 | 1427 / 52 | — |
| docs.python.org/3.14/using/index.html | 317 / 32 | 703 / 68 | 703 / 68 | 581 / 4 | 694 / 53 | 599 / 22 | 694 / 53 | — |
| docs.python.org/3.14/whatsnew/3.14.html | 19724 / 33 | 21273 / 68 | 21273 / 68 | 21115 / 4 | 21256 / 54 | 21134 / 23 | 21256 / 54 | — |
| docs.python.org/3.14/whatsnew/index.html | 2617 / 34 | 3006 / 68 | 3006 / 68 | 2883 / 4 | 2996 / 53 | 2901 / 22 | 2996 / 53 | — |
| docs.python.org/3.15 | 195 / 4 | 709 / 67 | 709 / 67 | 525 / 4 | 629 / 46 | 537 / 16 | 629 / 46 | — |
| docs.python.org/3.15/about.html | 209 / 26 | 612 / 67 | 612 / 67 | 493 / 4 | 602 / 51 | 510 / 21 | 602 / 51 | — |
| docs.python.org/3.15/bugs.html | 682 / 32 | 1093 / 67 | 1093 / 67 | 980 / 4 | 1089 / 51 | 997 / 21 | 1089 / 51 | — |
| docs.python.org/3.15/c-api/index.html | 595 / 33 | 973 / 67 | 973 / 67 | 854 / 4 | 964 / 52 | 872 / 22 | 964 / 52 | — |
| docs.python.org/3.15/contents.html | 22640 / 32 | 23003 / 67 | 23003 / 67 | 22874 / 4 | 22983 / 51 | 22891 / 21 | 22983 / 51 | — |
| docs.python.org/3.15/deprecations/index.html | 3667 / 30 | 4385 / 67 | 4385 / 67 | 4265 / 4 | 4373 / 49 | 4280 / 19 | 4373 / 49 | — |
| docs.python.org/3.15/download.html | 132 / 3 | 448 / 67 | 448 / 67 | 259 / 4 | 366 / 49 | 274 / 19 | 366 / 49 | — |
| docs.python.org/3.15/extending/index.html | 642 / 35 | 1098 / 67 | 1098 / 67 | 979 / 4 | 1091 / 54 | 999 / 24 | 1091 / 54 | — |
| docs.python.org/3.15/howto/index.html | 208 / 29 | 594 / 67 | 594 / 67 | 475 / 4 | 583 / 50 | 491 / 20 | 583 / 50 | — |
| docs.python.org/3.15/library/index.html | 2256 / 29 | 2634 / 67 | 2634 / 67 | 2515 / 4 | 2625 / 52 | 2533 / 22 | 2625 / 52 | — |
| docs.python.org/3.15/license.html | 8612 / 32 | 9235 / 67 | 9235 / 67 | 9116 / 4 | 9225 / 51 | 9133 / 21 | 9225 / 51 | — |
| docs.python.org/3.15/py-modindex.html | 3588 / 0 | 3984 / 67 | 3984 / 67 | 3773 / 4 | 3885 / 54 | 3793 / 24 | 3885 / 54 | — |
| docs.python.org/3.15/tutorial/index.html | 1065 / 28 | 1442 / 67 | 1442 / 67 | 1323 / 4 | 1432 / 51 | 1340 / 21 | 1432 / 51 | — |
| docs.python.org/3.15/whatsnew/3.15.html | 12088 / 31 | 13352 / 67 | 13352 / 67 | 13197 / 4 | 13326 / 53 | 13216 / 23 | 13326 / 53 | — |
| docs.python.org/3.15/whatsnew/index.html | 2641 / 34 | 3027 / 67 | 3027 / 67 | 2907 / 4 | 3017 / 52 | 2925 / 22 | 3017 / 52 | — |
| docs.python.org/3.2 | 185 / 0 | 298 / 0 | 298 / 0 | — | 324 / 20 | 323 / 20 | 324 / 20 | — |
| docs.python.org/3.3 | 185 / 0 | 298 / 0 | 298 / 0 | — | 324 / 20 | 323 / 20 | 324 / 20 | — |
| docs.python.org/3.3/about.html | 179 / 0 | 319 / 0 | 319 / 0 | — | 338 / 22 | 337 / 22 | 338 / 22 | — |
| docs.python.org/3.3/bugs.html | 596 / 0 | 746 / 0 | 746 / 0 | — | 766 / 21 | 765 / 21 | 766 / 21 | — |
| docs.python.org/3.3/c-api/index.html | 318 / 0 | 416 / 0 | 416 / 0 | — | 436 / 23 | 435 / 23 | 436 / 23 | — |
| docs.python.org/3.3/contents.html | 14428 / 0 | 14515 / 0 | 14515 / 0 | — | 14533 / 22 | 14532 / 22 | 14533 / 22 | — |
| docs.python.org/3.3/copyright.html | 96 / 0 | 192 / 0 | 192 / 0 | — | 207 / 20 | 206 / 20 | 207 / 20 | — |
| docs.python.org/3.3/distutils/index.html | 772 / 0 | 871 / 0 | 871 / 0 | — | 893 / 22 | 892 / 22 | 893 / 22 | — |
| docs.python.org/3.3/download.html | 270 / 0 | 344 / 0 | 344 / 0 | — | 361 / 20 | 360 / 20 | 361 / 20 | — |
| docs.python.org/3.3/extending/index.html | 437 / 0 | 541 / 0 | 541 / 0 | — | 563 / 25 | 562 / 25 | 563 / 25 | — |
| docs.python.org/3.3/faq/index.html | 29 / 29 | 192 / 0 | 192 / 0 | — | 212 / 23 | 211 / 23 | 212 / 23 | — |
| docs.python.org/3.3/genindex.html | 104 / 0 | 216 / 0 | 216 / 0 | — | 233 / 20 | 232 / 20 | 233 / 20 | — |
| docs.python.org/3.3/glossary.html | 5590 / 0 | 5615 / 0 | 5615 / 0 | — | 5717 / 20 | 5712 / 20 | 5717 / 20 | — |
| docs.python.org/3.3/howto/index.html | 95 / 0 | 274 / 0 | 274 / 0 | — | 292 / 21 | 291 / 21 | 292 / 21 | — |
| docs.python.org/3.3/install/index.html | 6793 / 0 | 6931 / 0 | 6931 / 0 | — | 6906 / 22 | 6905 / 22 | 6906 / 22 | — |
| docs.python.org/3.3/library/index.html | 2435 / 0 | 2531 / 0 | 2531 / 0 | — | 2551 / 23 | 2550 / 23 | 2551 / 23 | — |
| docs.python.org/3.3/license.html | 6243 / 0 | 6431 / 0 | 6431 / 0 | — | 6450 / 22 | 6449 / 22 | 6450 / 22 | — |
| docs.python.org/3.3/py-modindex.html | 3758 / 0 | 3897 / 0 | 3897 / 0 | — | 3903 / 25 | 3902 / 25 | 3903 / 25 | — |
| docs.python.org/3.3/reference/index.html | 446 / 0 | 544 / 0 | 544 / 0 | — | 564 / 23 | 563 / 23 | 564 / 23 | — |
| docs.python.org/3.3/search.html | 51 / 0 | 123 / 0 | 123 / 0 | — | 144 / 24 | 143 / 24 | 144 / 24 | — |
| docs.python.org/3.3/tutorial/index.html | 951 / 0 | 1045 / 0 | 1045 / 0 | — | 1064 / 22 | 1063 / 22 | 1064 / 22 | — |
| docs.python.org/3.3/using/index.html | 320 / 0 | 473 / 0 | 473 / 0 | — | 493 / 23 | 492 / 23 | 493 / 23 | — |
| docs.python.org/3.3/whatsnew/3.3.html | 13595 / 0 | 14113 / 0 | 14113 / 0 | — | 14166 / 24 | 14150 / 24 | 14166 / 24 | — |
| docs.python.org/3.3/whatsnew/index.html | 1205 / 0 | 1430 / 0 | 1430 / 0 | — | 1449 / 23 | 1448 / 23 | 1449 / 23 | — |
| docs.python.org/3.4 | 191 / 0 | 336 / 28 | 336 / 28 | — | 361 / 47 | 360 / 47 | 361 / 47 | — |
| docs.python.org/3.4/about.html | 179 / 0 | 347 / 28 | 347 / 28 | — | 365 / 49 | 364 / 49 | 365 / 49 | — |
| docs.python.org/3.4/bugs.html | 596 / 0 | 774 / 28 | 774 / 28 | — | 793 / 48 | 792 / 48 | 793 / 48 | — |
| docs.python.org/3.4/c-api/index.html | 334 / 0 | 460 / 28 | 460 / 28 | — | 479 / 50 | 478 / 50 | 479 / 50 | — |
| docs.python.org/3.4/contents.html | 15636 / 0 | 15751 / 28 | 15751 / 28 | — | 15768 / 49 | 15767 / 49 | 15768 / 49 | — |
| docs.python.org/3.4/copyright.html | 96 / 0 | 220 / 28 | 220 / 28 | — | 234 / 47 | 233 / 47 | 234 / 47 | — |
| docs.python.org/3.4/distributing/index.html | 978 / 0 | 1190 / 28 | 1190 / 28 | — | 1214 / 49 | 1213 / 49 | 1214 / 49 | — |
| docs.python.org/3.4/download.html | 266 / 0 | 368 / 28 | 368 / 28 | — | 384 / 47 | 383 / 47 | 384 / 47 | — |
| docs.python.org/3.4/extending/index.html | 507 / 0 | 758 / 28 | 758 / 28 | — | 780 / 52 | 779 / 52 | 780 / 52 | — |
| docs.python.org/3.4/faq/index.html | 27 / 27 | 211 / 28 | 211 / 28 | — | 230 / 50 | 229 / 50 | 230 / 50 | — |
| docs.python.org/3.4/genindex.html | 27 / 27 | 244 / 28 | 244 / 28 | — | 260 / 47 | 259 / 47 | 260 / 47 | — |
| docs.python.org/3.4/glossary.html | 5774 / 0 | 5818 / 28 | 5818 / 28 | — | 5928 / 47 | 5923 / 47 | 5928 / 47 | — |
| docs.python.org/3.4/howto/index.html | 95 / 0 | 306 / 28 | 306 / 28 | — | 323 / 48 | 322 / 48 | 323 / 48 | — |
| docs.python.org/3.4/installing/index.html | 1136 / 0 | 1404 / 28 | 1404 / 28 | — | 1425 / 49 | 1424 / 49 | 1425 / 49 | — |
| docs.python.org/3.4/library/index.html | 2498 / 0 | 2622 / 28 | 2622 / 28 | — | 2641 / 50 | 2640 / 50 | 2641 / 50 | — |
| docs.python.org/3.4/license.html | 6644 / 0 | 6890 / 28 | 6890 / 28 | — | 6908 / 49 | 6907 / 49 | 6908 / 49 | — |
| docs.python.org/3.4/py-modindex.html | 3846 / 0 | 4013 / 28 | 4013 / 28 | — | 4018 / 52 | 4017 / 52 | 4018 / 52 | — |
| docs.python.org/3.4/reference/index.html | 458 / 0 | 584 / 28 | 584 / 28 | — | 603 / 50 | 602 / 50 | 603 / 50 | — |
| docs.python.org/3.4/search.html | 51 / 0 | 151 / 28 | 151 / 28 | — | 171 / 51 | 170 / 51 | 171 / 51 | — |
| docs.python.org/3.4/tutorial/index.html | 979 / 0 | 1101 / 28 | 1101 / 28 | — | 1119 / 49 | 1118 / 49 | 1119 / 49 | — |
| docs.python.org/3.4/using/index.html | 360 / 0 | 486 / 28 | 486 / 28 | — | 505 / 50 | 504 / 50 | 505 / 50 | — |
| docs.python.org/3.4/whatsnew/3.4.html | 16183 / 0 | 16323 / 28 | 16323 / 28 | — | 16350 / 51 | 16344 / 51 | 16350 / 51 | — |
| docs.python.org/3.4/whatsnew/index.html | 1464 / 0 | 1593 / 28 | 1593 / 28 | — | 1611 / 50 | 1610 / 50 | 1611 / 50 | — |
| docs.python.org/3.5 | 186 / 0 | 371 / 28 | 371 / 28 | — | 353 / 29 | 324 / 29 | 353 / 29 | — |
| docs.python.org/3.5/about.html | 180 / 0 | 397 / 28 | 397 / 28 | — | 374 / 34 | 345 / 34 | 374 / 34 | — |
| docs.python.org/3.5/bugs.html | 631 / 0 | 856 / 28 | 856 / 28 | — | 835 / 34 | 806 / 34 | 835 / 34 | — |
| docs.python.org/3.5/c-api/index.html | 323 / 0 | 535 / 28 | 535 / 28 | — | 513 / 35 | 484 / 35 | 513 / 35 | — |
| docs.python.org/3.5/contents.html | 16248 / 0 | 16441 / 28 | 16441 / 28 | — | 16417 / 34 | 16388 / 34 | 16417 / 34 | — |
| docs.python.org/3.5/copyright.html | 58 / 0 | 269 / 28 | 269 / 28 | — | 242 / 32 | 213 / 32 | 242 / 32 | — |
| docs.python.org/3.5/distributing/index.html | 978 / 0 | 1236 / 28 | 1236 / 28 | — | 1219 / 34 | 1190 / 34 | 1219 / 34 | — |
| docs.python.org/3.5/download.html | 255 / 0 | 413 / 28 | 413 / 28 | — | 389 / 32 | 360 / 32 | 389 / 32 | — |
| docs.python.org/3.5/extending/index.html | 514 / 0 | 811 / 28 | 811 / 28 | — | 792 / 37 | 763 / 37 | 792 / 37 | — |
| docs.python.org/3.5/glossary.html | 6315 / 0 | 6440 / 28 | 6440 / 28 | — | 6518 / 32 | 6485 / 32 | 6518 / 32 | — |
| docs.python.org/3.5/howto/index.html | 52 / 0 | 345 / 28 | 345 / 28 | — | 321 / 33 | 292 / 33 | 321 / 33 | — |
| docs.python.org/3.5/installing/index.html | 1166 / 0 | 1479 / 28 | 1479 / 28 | — | 1459 / 34 | 1430 / 34 | 1459 / 34 | — |
| docs.python.org/3.5/library/index.html | 2476 / 0 | 2685 / 28 | 2685 / 28 | — | 2663 / 35 | 2634 / 35 | 2663 / 35 | — |
| docs.python.org/3.5/license.html | 6671 / 0 | 6993 / 28 | 6993 / 28 | — | 6970 / 34 | 6941 / 34 | 6970 / 34 | — |
| docs.python.org/3.5/py-modindex.html | 3873 / 0 | 4099 / 28 | 4099 / 28 | — | 4063 / 37 | 4034 / 37 | 4063 / 37 | — |
| docs.python.org/3.5/using/index.html | 351 / 0 | 563 / 28 | 563 / 28 | — | 541 / 35 | 512 / 35 | 541 / 35 | — |
| docs.python.org/3.5/whatsnew/3.5.html | 11914 / 0 | 12519 / 28 | 12519 / 28 | — | 12513 / 36 | 12460 / 36 | 12513 / 36 | — |
| docs.python.org/3.5/whatsnew/index.html | 1490 / 0 | 1706 / 28 | 1706 / 28 | — | 1683 / 35 | 1654 / 35 | 1683 / 35 | — |
| docs.python.org/3.6 | 186 / 0 | 371 / 28 | 371 / 28 | — | 353 / 29 | 324 / 29 | 353 / 29 | — |
| docs.python.org/3.6/about.html | 180 / 0 | 397 / 28 | 397 / 28 | — | 374 / 34 | 345 / 34 | 374 / 34 | — |
| docs.python.org/3.6/bugs.html | 631 / 0 | 856 / 28 | 856 / 28 | — | 835 / 34 | 806 / 34 | 835 / 34 | — |
| docs.python.org/3.6/c-api/index.html | 325 / 0 | 537 / 28 | 537 / 28 | — | 515 / 35 | 486 / 35 | 515 / 35 | — |
| docs.python.org/3.6/contents.html | 17414 / 0 | 17607 / 28 | 17607 / 28 | — | 17583 / 34 | 17554 / 34 | 17583 / 34 | — |
| docs.python.org/3.6/copyright.html | 58 / 0 | 269 / 28 | 269 / 28 | — | 242 / 32 | 213 / 32 | 242 / 32 | — |
| docs.python.org/3.6/distributing/index.html | 968 / 0 | 1228 / 28 | 1228 / 28 | — | 1209 / 34 | 1180 / 34 | 1209 / 34 | — |
| docs.python.org/3.6/download.html | 255 / 0 | 413 / 28 | 413 / 28 | — | 389 / 32 | 360 / 32 | 389 / 32 | — |
| docs.python.org/3.6/extending/index.html | 578 / 0 | 875 / 28 | 875 / 28 | — | 856 / 37 | 827 / 37 | 856 / 37 | — |
| docs.python.org/3.6/glossary.html | 7083 / 0 | 7198 / 28 | 7198 / 28 | — | 7286 / 32 | 7253 / 32 | 7286 / 32 | — |
| docs.python.org/3.6/howto/index.html | 52 / 0 | 352 / 28 | 352 / 28 | — | 328 / 33 | 299 / 33 | 328 / 33 | — |
| docs.python.org/3.6/installing/index.html | 1237 / 0 | 1567 / 28 | 1567 / 28 | — | 1545 / 34 | 1516 / 34 | 1545 / 34 | — |
| docs.python.org/3.6/library/index.html | 2487 / 0 | 2696 / 28 | 2696 / 28 | — | 2674 / 35 | 2645 / 35 | 2674 / 35 | — |
| docs.python.org/3.6/license.html | 6672 / 0 | 6994 / 28 | 6994 / 28 | — | 6971 / 34 | 6942 / 34 | 6971 / 34 | — |
| docs.python.org/3.6/py-modindex.html | 3882 / 0 | 4108 / 28 | 4108 / 28 | — | 4072 / 37 | 4043 / 37 | 4072 / 37 | — |
| docs.python.org/3.6/reference/index.html | 428 / 0 | 643 / 28 | 643 / 28 | — | 621 / 35 | 592 / 35 | 621 / 35 | — |
| docs.python.org/3.6/search.html | 51 / 0 | 205 / 28 | 205 / 28 | — | 180 / 32 | 151 / 32 | 180 / 32 | — |
| docs.python.org/3.6/tutorial/index.html | 935 / 0 | 1141 / 28 | 1141 / 28 | — | 1118 / 34 | 1089 / 34 | 1118 / 34 | — |
| docs.python.org/3.6/using/index.html | 346 / 0 | 558 / 28 | 558 / 28 | — | 536 / 35 | 507 / 35 | 536 / 35 | — |
| docs.python.org/3.6/whatsnew/3.6.html | 12608 / 0 | 13340 / 28 | 13340 / 28 | — | 13330 / 36 | 13293 / 36 | 13330 / 36 | — |
| docs.python.org/3.6/whatsnew/index.html | 1657 / 0 | 1873 / 28 | 1873 / 28 | — | 1850 / 35 | 1821 / 35 | 1850 / 35 | — |
| docs.python.org/3.7 | 186 / 0 | 371 / 28 | 371 / 28 | — | 363 / 39 | 334 / 39 | 363 / 39 | — |
| docs.python.org/3.7/about.html | 180 / 0 | 397 / 28 | 397 / 28 | — | 384 / 44 | 355 / 44 | 384 / 44 | — |
| docs.python.org/3.7/bugs.html | 599 / 0 | 824 / 28 | 824 / 28 | — | 813 / 44 | 784 / 44 | 813 / 44 | — |
| docs.python.org/3.7/c-api/index.html | 352 / 0 | 564 / 28 | 564 / 28 | — | 552 / 45 | 523 / 45 | 552 / 45 | — |
| docs.python.org/3.7/contents.html | 16858 / 0 | 17051 / 28 | 17051 / 28 | — | 17037 / 44 | 17008 / 44 | 17037 / 44 | — |
| docs.python.org/3.7/distributing/index.html | 973 / 0 | 1236 / 28 | 1236 / 28 | — | 1227 / 44 | 1198 / 44 | 1227 / 44 | — |
| docs.python.org/3.7/download.html | 241 / 0 | 399 / 28 | 399 / 28 | — | 385 / 42 | 356 / 42 | 385 / 42 | — |
| docs.python.org/3.7/extending/index.html | 578 / 0 | 872 / 28 | 872 / 28 | — | 863 / 47 | 834 / 47 | 863 / 47 | — |
| docs.python.org/3.7/glossary.html | 7203 / 0 | 7317 / 28 | 7317 / 28 | — | 7417 / 42 | 7383 / 42 | 7417 / 42 | — |
| docs.python.org/3.7/installing/index.html | 1237 / 0 | 1567 / 28 | 1567 / 28 | — | 1555 / 44 | 1526 / 44 | 1555 / 44 | — |
| docs.python.org/3.7/library/index.html | 2214 / 0 | 2420 / 28 | 2420 / 28 | — | 2408 / 45 | 2379 / 45 | 2408 / 45 | — |
| docs.python.org/3.7/license.html | 6325 / 0 | 6642 / 28 | 6642 / 28 | — | 6629 / 44 | 6600 / 44 | 6629 / 44 | — |
| docs.python.org/3.7/py-modindex.html | 3898 / 0 | 4124 / 28 | 4124 / 28 | — | 4098 / 47 | 4069 / 47 | 4098 / 47 | — |
| docs.python.org/3.7/reference/index.html | 433 / 0 | 642 / 28 | 642 / 28 | — | 630 / 45 | 601 / 45 | 630 / 45 | — |
| docs.python.org/3.7/tutorial/index.html | 951 / 0 | 1157 / 28 | 1157 / 28 | — | 1144 / 44 | 1115 / 44 | 1144 / 44 | — |
| docs.python.org/3.7/using/index.html | 359 / 0 | 571 / 28 | 571 / 28 | — | 559 / 45 | 530 / 45 | 559 / 45 | — |
| docs.python.org/3.7/whatsnew/3.7.html | 13820 / 0 | 14487 / 28 | 14487 / 28 | — | 14486 / 46 | 14457 / 46 | 14486 / 46 | — |
| docs.python.org/3.7/whatsnew/index.html | 1896 / 0 | 2112 / 28 | 2112 / 28 | — | 2099 / 45 | 2070 / 45 | 2099 / 45 | — |
| docs.python.org/3.8 | 189 / 0 | 551 / 56 | 551 / 56 | — | 484 / 39 | 400 / 12 | 484 / 39 | — |
| docs.python.org/3.9 | 190 / 0 | 580 / 63 | 580 / 63 | — | 504 / 43 | 408 / 12 | 504 / 43 | — |
| docs.python.org/3/bugs.html | — | — | — | 980 / 4 | — | 997 / 21 | — | — |
| docs.python.org/3/license.html | — | — | — | 8679 / 4 | — | 8696 / 21 | — | — |
| docs.python.org/bugs.html | 682 / 32 | 1096 / 68 | 1096 / 68 | — | 1092 / 52 | — | 1092 / 52 | — |
| docs.python.org/license.html | 8187 / 32 | 8801 / 68 | 8801 / 68 | — | 8791 / 52 | — | 8791 / 52 | — |

</details>

## react-dev

| Tool | Avg words [6] | Preamble [2] | Repeat rate [3] | Junk found [4] | Headings [7] | Code blocks [8] | Precision [5] | Recall [5] |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 1559 | 13 | 0% | 136 | 15.4 | 9.9 | 100% | 44% |
| crawl4ai | 2277 | 12 | 0% | 142 | 19.8 | 9.8 | 100% | 37% |
| crawl4ai-raw | 2279 | 12 | 0% | 142 | 19.8 | 9.8 | 100% | 37% |
| scrapy+md | 1601 | 6 | 0% | 137 | 15.4 | 9.9 | 100% | 44% |
| crawlee | 4370 | 368 ⚠ | 0% | 144 | 21.6 | 9.8 | 99% | 98% |
| colly+md | 4292 | 289 ⚠ | 0% | 144 | 21.6 | 9.9 | 98% | 100% |
| playwright | 4292 | 289 ⚠ | 0% | 144 | 21.6 | 9.9 | 100% | 98% |
| firecrawl | — | — | — | — | — | — | — | — |

> **Column definitions:**
> **[6] Avg words** = mean words per page. **[2] Preamble** = avg words per page before the first heading (nav chrome). **[3] Repeat rate** = fraction of sentences on >50% of pages.
> **[4] Junk found** = total known boilerplate phrases detected across all pages. **[7] Headings** = avg headings per page. **[8] Code blocks** = avg fenced code blocks per page.
> **[5] Precision/Recall** = cross-tool consensus (pages with <2 sentences excluded). **⚠** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
**scrapy+md** produces the cleanest output with 6 words of preamble per page, while **crawlee** injects 368 words of nav chrome before content begins. The word count gap (1559 vs 4370 avg words) is largely explained by preamble: 368 words of nav chrome account for ~8% of crawlee's output on this site. scrapy+md's lower recall (44% vs 100%) reflects stricter content filtering — the "missed" sentences are predominantly navigation, sponsor links, and footer text that other tools include as content. For RAG, this is typically a net positive: fewer junk tokens per chunk tends to improve embedding quality and retrieval precision.

<details>
<summary>Sample output — first 40 lines of <code>react.dev/learn/separating-events-from-effects</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
*The library for web and native user interfaces*


[Learn React](/learn)

[Escape Hatches](/learn/escape-hatches)

Copy pageCopy

# Separating Events from Effects

Event handlers only re-run when you perform the same interaction again. Unlike event handlers, Effects re-synchronize if some value they read, like a prop or a state variable, is different from what it was during the last render. Sometimes, you also want a mix of both behaviors: an Effect that re-runs in response to some values but not others. This page will teach you how to do that.

### You will learn

* How to choose between an event handler and an Effect
* Why Effects are reactive, and event handlers are not
* What to do when you want a part of your Effect’s code to not be reactive
* What Effect Events are, and how to extract them from your Effects
* How to read the latest props and state from Effects using Effect Events

## Choosing between event handlers and Effects

First, let’s recap the difference between event handlers and Effects.

Imagine you’re implementing a chat room component. Your requirements look like this:

1. Your component should automatically connect to the selected chat room.
2. When you click the “Send” button, it should send a message to the chat.

Let’s say you’ve already implemented the code for them, but you’re not sure where to put it. Should you use event handlers or Effects? Every time you need to answer this question, consider [*why* the code needs to run.](/learn/synchronizing-with-effects#what-are-effects-and-how-are-they-different-from-events)

### Event handlers run in response to specific interactions

From the user’s perspective, sending a message should happen *because* the particular “Send” button was clicked. The user will get rather upset if you send their message at any other time or for any other reason. This is why sending a message should be an event handler. Event handlers let you handle specific interactions:

```
function ChatRoom({ roomId }) {

```

**crawl4ai**
```
[![logo by @sawaratsuki1004](https://react.dev/_next/image?url=%2Fimages%2Fuwu.png&w=128&q=75)](https://react.dev/)
[React](https://react.dev/)
[v19.2](https://react.dev/versions)
`⌘``Ctrl``K`
[Learn](https://react.dev/learn)
[Reference](https://react.dev/reference/react)
[Community](https://react.dev/community)
[Blog](https://react.dev/blog)
[](https://react.dev/community/translations)
[](https://github.com/facebook/react/releases)
### GET STARTED
  * [Quick Start ](https://react.dev/learn "Quick Start")
    * [Tutorial: Tic-Tac-Toe ](https://react.dev/learn/tutorial-tic-tac-toe "Tutorial: Tic-Tac-Toe")
    * [Thinking in React ](https://react.dev/learn/thinking-in-react "Thinking in React")
  * [Installation ](https://react.dev/learn/installation "Installation")
    * [Creating a React App ](https://react.dev/learn/creating-a-react-app "Creating a React App")
    * [Build a React App from Scratch ](https://react.dev/learn/build-a-react-app-from-scratch "Build a React App from Scratch")
    * [Add React to an Existing Project ](https://react.dev/learn/add-react-to-an-existing-project "Add React to an Existing Project")
  * [Setup ](https://react.dev/learn/setup "Setup")
    * [Editor Setup ](https://react.dev/learn/editor-setup "Editor Setup")
    * [Using TypeScript ](https://react.dev/learn/typescript "Using TypeScript")
    * [React Developer Tools ](https://react.dev/learn/react-developer-tools "React Developer Tools")
  * [React Compiler ](https://react.dev/learn/react-compiler "React Compiler")
    * [Introduction ](https://react.dev/learn/react-compiler/introduction "Introduction")
    * [Installation ](https://react.dev/learn/react-compiler/installation "Installation")
    * [Incremental Adoption ](https://react.dev/learn/react-compiler/incremental-adoption "Incremental Adoption")
    * [Debugging and Troubleshooting ](https://react.dev/learn/react-compiler/debugging "Debugging and Troubleshooting")
### LEARN REACT
  * [Describing the UI ](https://react.dev/learn/describing-the-ui "Describing the UI")
    * [Your First Component ](https://react.dev/learn/your-first-component "Your First Component")
    * [Importing and Exporting Components ](https://react.dev/learn/importing-and-exporting-components "Importing and Exporting Components")
    * [Writing Markup with JSX ](https://react.dev/learn/writing-markup-with-jsx "Writing Markup with JSX")
    * [JavaScript in JSX with Curly Braces ](https://react.dev/learn/javascript-in-jsx-with-curly-braces "JavaScript in JSX with Curly Braces")
    * [Passing Props to a Component ](https://react.dev/learn/passing-props-to-a-component "Passing Props to a Component")
    * [Conditional Rendering ](https://react.dev/learn/conditional-rendering "Conditional Rendering")
    * [Rendering Lists ](https://react.dev/learn/rendering-lists "Rendering Lists")
    * [Keeping Components Pure ](https://react.dev/learn/keeping-components-pure "Keeping Components Pure")
    * [Your UI as a Tree ](https://react.dev/learn/understanding-your-ui-as-a-tree "Your UI as a Tree")
  * [Adding Interactivity ](https://react.dev/learn/adding-interactivity "Adding Interactivity")
    * [Responding to Events ](https://react.dev/learn/responding-to-events "Responding to Events")
```

**crawl4ai-raw**
```
[![logo by @sawaratsuki1004](https://react.dev/_next/image?url=%2Fimages%2Fuwu.png&w=128&q=75)](https://react.dev/)
[React](https://react.dev/)
[v19.2](https://react.dev/versions)
`⌘``Ctrl``K`
[Learn](https://react.dev/learn)
[Reference](https://react.dev/reference/react)
[Community](https://react.dev/community)
[Blog](https://react.dev/blog)
[](https://react.dev/community/translations)
[](https://github.com/facebook/react/releases)
### GET STARTED
  * [Quick Start ](https://react.dev/learn "Quick Start")
    * [Tutorial: Tic-Tac-Toe ](https://react.dev/learn/tutorial-tic-tac-toe "Tutorial: Tic-Tac-Toe")
    * [Thinking in React ](https://react.dev/learn/thinking-in-react "Thinking in React")
  * [Installation ](https://react.dev/learn/installation "Installation")
    * [Creating a React App ](https://react.dev/learn/creating-a-react-app "Creating a React App")
    * [Build a React App from Scratch ](https://react.dev/learn/build-a-react-app-from-scratch "Build a React App from Scratch")
    * [Add React to an Existing Project ](https://react.dev/learn/add-react-to-an-existing-project "Add React to an Existing Project")
  * [Setup ](https://react.dev/learn/setup "Setup")
    * [Editor Setup ](https://react.dev/learn/editor-setup "Editor Setup")
    * [Using TypeScript ](https://react.dev/learn/typescript "Using TypeScript")
    * [React Developer Tools ](https://react.dev/learn/react-developer-tools "React Developer Tools")
  * [React Compiler ](https://react.dev/learn/react-compiler "React Compiler")
    * [Introduction ](https://react.dev/learn/react-compiler/introduction "Introduction")
    * [Installation ](https://react.dev/learn/react-compiler/installation "Installation")
    * [Incremental Adoption ](https://react.dev/learn/react-compiler/incremental-adoption "Incremental Adoption")
    * [Debugging and Troubleshooting ](https://react.dev/learn/react-compiler/debugging "Debugging and Troubleshooting")
### LEARN REACT
  * [Describing the UI ](https://react.dev/learn/describing-the-ui "Describing the UI")
    * [Your First Component ](https://react.dev/learn/your-first-component "Your First Component")
    * [Importing and Exporting Components ](https://react.dev/learn/importing-and-exporting-components "Importing and Exporting Components")
    * [Writing Markup with JSX ](https://react.dev/learn/writing-markup-with-jsx "Writing Markup with JSX")
    * [JavaScript in JSX with Curly Braces ](https://react.dev/learn/javascript-in-jsx-with-curly-braces "JavaScript in JSX with Curly Braces")
    * [Passing Props to a Component ](https://react.dev/learn/passing-props-to-a-component "Passing Props to a Component")
    * [Conditional Rendering ](https://react.dev/learn/conditional-rendering "Conditional Rendering")
    * [Rendering Lists ](https://react.dev/learn/rendering-lists "Rendering Lists")
    * [Keeping Components Pure ](https://react.dev/learn/keeping-components-pure "Keeping Components Pure")
    * [Your UI as a Tree ](https://react.dev/learn/understanding-your-ui-as-a-tree "Your UI as a Tree")
  * [Adding Interactivity ](https://react.dev/learn/adding-interactivity "Adding Interactivity")
    * [Responding to Events ](https://react.dev/learn/responding-to-events "Responding to Events")
```

**scrapy+md**
```
[Learn React](/learn)

[Escape Hatches](/learn/escape-hatches)

 Copy pageCopy

# Separating Events from Effects

Event handlers only re-run when you perform the same interaction again. Unlike event handlers, Effects re-synchronize if some value they read, like a prop or a state variable, is different from what it was during the last render. Sometimes, you also want a mix of both behaviors: an Effect that re-runs in response to some values but not others. This page will teach you how to do that.

### You will learn

* How to choose between an event handler and an Effect
* Why Effects are reactive, and event handlers are not
* What to do when you want a part of your Effect’s code to not be reactive
* What Effect Events are, and how to extract them from your Effects
* How to read the latest props and state from Effects using Effect Events

## Choosing between event handlers and Effects

First, let’s recap the difference between event handlers and Effects.

Imagine you’re implementing a chat room component. Your requirements look like this:

1. Your component should automatically connect to the selected chat room.
2. When you click the “Send” button, it should send a message to the chat.

Let’s say you’ve already implemented the code for them, but you’re not sure where to put it. Should you use event handlers or Effects? Every time you need to answer this question, consider [*why* the code needs to run.](/learn/synchronizing-with-effects#what-are-effects-and-how-are-they-different-from-events)

### Event handlers run in response to specific interactions

From the user’s perspective, sending a message should happen *because* the particular “Send” button was clicked. The user will get rather upset if you send their message at any other time or for any other reason. This is why sending a message should be an event handler. Event handlers let you handle specific interactions:

```
function ChatRoom({ roomId }) {



const [message, setMessage] = useState('');
```

**crawlee**
```
Separating Events from Effects – Reactwindow.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-B1E83PJ3RT');
(function () {
try {
let logShown = false;
function setUwu(isUwu) {
try {
if (isUwu) {
localStorage.setItem('uwu', true);
document.documentElement.classList.add('uwu');
if (!logShown) {
console.log('uwu mode! turn off with ?uwu=0');
console.log('logo credit to @sawaratsuki1004 via https://github.com/SAWARATSUKI/KawaiiLogos');
logShown = true;
}
} else {
localStorage.removeItem('uwu');
document.documentElement.classList.remove('uwu');
console.log('uwu mode off. turn on with ?uwu');
}
} catch (err) { }
}
window.\_\_setUwu = setUwu;
function checkQueryParam() {
const params = new URLSearchParams(window.location.search);
const value = params.get('uwu');
switch(value) {
case '':
case 'true':
case '1':
return true;
case 'false':
case '0':
return false;
default:
return null;
}
}
function checkLocalStorage() {
try {
return localStorage.getItem('uwu') === 'true';
```

**colly+md**
```
Separating Events from Effects – Reactwindow.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-B1E83PJ3RT');
(function () {
try {
let logShown = false;
function setUwu(isUwu) {
try {
if (isUwu) {
localStorage.setItem('uwu', true);
document.documentElement.classList.add('uwu');
if (!logShown) {
console.log('uwu mode! turn off with ?uwu=0');
console.log('logo credit to @sawaratsuki1004 via https://github.com/SAWARATSUKI/KawaiiLogos');
logShown = true;
}
} else {
localStorage.removeItem('uwu');
document.documentElement.classList.remove('uwu');
console.log('uwu mode off. turn on with ?uwu');
}
} catch (err) { }
}
window.\_\_setUwu = setUwu;
function checkQueryParam() {
const params = new URLSearchParams(window.location.search);
const value = params.get('uwu');
switch(value) {
case '':
case 'true':
case '1':
return true;
case 'false':
case '0':
return false;
default:
return null;
}
}
function checkLocalStorage() {
try {
return localStorage.getItem('uwu') === 'true';
```

**playwright**
```
Separating Events from Effects – Reactwindow.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-B1E83PJ3RT');
(function () {
try {
let logShown = false;
function setUwu(isUwu) {
try {
if (isUwu) {
localStorage.setItem('uwu', true);
document.documentElement.classList.add('uwu');
if (!logShown) {
console.log('uwu mode! turn off with ?uwu=0');
console.log('logo credit to @sawaratsuki1004 via https://github.com/SAWARATSUKI/KawaiiLogos');
logShown = true;
}
} else {
localStorage.removeItem('uwu');
document.documentElement.classList.remove('uwu');
console.log('uwu mode off. turn on with ?uwu');
}
} catch (err) { }
}
window.\_\_setUwu = setUwu;
function checkQueryParam() {
const params = new URLSearchParams(window.location.search);
const value = params.get('uwu');
switch(value) {
case '':
case 'true':
case '1':
return true;
case 'false':
case '0':
return false;
default:
return null;
}
}
function checkLocalStorage() {
try {
return localStorage.getItem('uwu') === 'true';
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [2]</summary>

| URL | markcrawl words [6] / preamble [2] | crawl4ai words [6] / preamble [2] | crawl4ai-raw words [6] / preamble [2] | scrapy+md words [6] / preamble [2] | crawlee words [6] / preamble [2] | colly+md words [6] / preamble [2] | playwright words [6] / preamble [2] | firecrawl words [6] / preamble [2] |
|---|---|---|---|---|---|---|---|---|
| 18.react.dev/reference/react-dom/findDOMNode | — | — | — | 1202 / 3 | — | 3363 / 278 | — | — |
| 18.react.dev/reference/react-dom/hydrate | — | — | — | 906 / 3 | — | 2599 / 278 | — | — |
| 18.react.dev/reference/react-dom/render | — | — | — | 852 / 3 | — | 2522 / 278 | — | — |
| 18.react.dev/reference/react-dom/server/renderToNodeStr | — | — | — | 411 / 4 | — | 1582 / 278 | — | — |
| 18.react.dev/reference/react-dom/server/renderToStaticN | — | — | — | 414 / 4 | — | 1587 / 278 | — | — |
| 18.react.dev/reference/react-dom/unmountComponentAtNode | — | — | — | 342 / 3 | — | 1464 / 278 | — | — |
| 18.react.dev/reference/react/createFactory | — | — | — | 784 / 5 | — | 2263 / 278 | — | — |
| legacy.reactjs.org/blog/2020/09/22/introducing-the-new- | — | — | — | 2059 / 299 | — | 3992 / 2232 | — | — |
| react.dev | 1227 / 38 | 1335 / 15 | 1335 / 15 | 1258 / 0 | 1535 / 276 | 1535 / 276 | 1535 / 276 | — |
| react.dev/blog | 1278 / 11 | 1356 / 15 | 1356 / 15 | 1318 / 3 | 2752 / 282 | 2752 / 282 | 2752 / 282 | — |
| react.dev/blog/2020/12/21/data-fetching-with-react-serv | 235 / 11 | 303 / 15 | 303 / 15 | 275 / 3 | 808 / 285 | 808 / 285 | 808 / 285 | — |
| react.dev/blog/2021/06/08/the-plan-for-react-18 | 892 / 11 | 1015 / 15 | 1015 / 15 | 932 / 3 | 2188 / 285 | 2188 / 285 | 2188 / 285 | — |
| react.dev/blog/2021/12/17/react-conf-2021-recap | 1194 / 11 | 1331 / 15 | 1331 / 15 | 1234 / 3 | 2866 / 284 | 2866 / 284 | 2866 / 284 | — |
| react.dev/blog/2022/03/08/react-18-upgrade-guide | 2586 / 11 | 2755 / 15 | 2755 / 15 | 2626 / 3 | 5411 / 286 | 5411 / 286 | 5411 / 286 | — |
| react.dev/blog/2022/03/29/react-v18 | 3736 / 11 | 3978 / 15 | 3978 / 15 | 3776 / 3 | 8014 / 282 | 8014 / 282 | 8014 / 282 | — |
| react.dev/blog/2022/06/15/react-labs-what-we-have-been- | 1493 / 11 | 1605 / 15 | 1605 / 15 | 1533 / 3 | 3418 / 290 | 3418 / 290 | 3418 / 290 | — |
| react.dev/blog/2023/03/16/introducing-react-dev | 2292 / 11 | 2672 / 15 | 2672 / 15 | 2337 / 3 | 5530 / 282 | 5530 / 282 | 5530 / 282 | — |
| react.dev/blog/2023/03/22/react-labs-what-we-have-been- | 2311 / 11 | 2419 / 15 | 2419 / 15 | 2351 / 3 | 4989 / 290 | 4989 / 290 | 4989 / 290 | — |
| react.dev/blog/2023/05/03/react-canaries | 1709 / 11 | 1859 / 15 | 1859 / 15 | 1749 / 3 | 3796 / 288 | 3796 / 288 | 3796 / 288 | — |
| react.dev/blog/2024/02/15/react-labs-what-we-have-been- | 1897 / 11 | 2009 / 15 | 2009 / 15 | 1937 / 3 | 4134 / 290 | 4134 / 290 | 4134 / 290 | — |
| react.dev/blog/2024/04/25/react-19-upgrade-guide | 3284 / 11 | 3716 / 15 | 3716 / 15 | 3324 / 3 | 6769 / 284 | 6769 / 284 | 6769 / 284 | — |
| react.dev/blog/2024/05/22/react-conf-2024-recap | 1177 / 11 | 1274 / 15 | 1274 / 15 | 1217 / 3 | 2810 / 284 | 2810 / 284 | 2810 / 284 | — |
| react.dev/blog/2024/10/21/react-compiler-beta-release | 1449 / 11 | 1593 / 15 | 1593 / 15 | 1491 / 3 | 3241 / 284 | 3241 / 284 | 3241 / 284 | — |
| react.dev/blog/2024/12/05/react-19 | 4261 / 11 | 4550 / 15 | 4550 / 15 | 4301 / 3 | 8673 / 282 | 8673 / 282 | 8673 / 282 | — |
| react.dev/blog/2025/02/14/sunsetting-create-react-app | 2576 / 11 | 2737 / 15 | 2737 / 15 | 2616 / 3 | 5497 / 284 | 5497 / 284 | 5497 / 284 | — |
| react.dev/blog/2025/04/23/react-labs-view-transitions-a | 5425 / 11 | 5662 / 15 | 5662 / 15 | 5465 / 3 | 39955 / 287 | 39955 / 287 | 39955 / 287 | — |
| react.dev/blog/2025/10/01/react-19-2 | 1924 / 11 | 2334 / 15 | 2334 / 15 | 1964 / 3 | 4098 / 282 | 4098 / 282 | 4098 / 282 | — |
| react.dev/blog/2025/10/07/introducing-the-react-foundat | 513 / 11 | 603 / 15 | 603 / 15 | 553 / 3 | 1348 / 284 | 1348 / 284 | 1348 / 284 | — |
| react.dev/blog/2025/10/07/react-compiler-1 | 1788 / 11 | 1932 / 15 | 1932 / 15 | 1828 / 3 | 3862 / 283 | 3862 / 283 | 3862 / 283 | — |
| react.dev/blog/2025/10/16/react-conf-2025-recap | 1127 / 11 | 1237 / 15 | 1237 / 15 | 1167 / 3 | 2689 / 284 | 2689 / 284 | 2689 / 284 | — |
| react.dev/blog/2025/12/03/critical-security-vulnerabili | 990 / 11 | 1162 / 15 | 1162 / 15 | 1030 / 3 | 2254 / 287 | 2254 / 287 | 2254 / 287 | — |
| react.dev/blog/2025/12/11/denial-of-service-and-source- | 1190 / 11 | 1384 / 15 | 1384 / 15 | 1230 / 3 | 2698 / 291 | 2698 / 291 | 2698 / 291 | — |
| react.dev/blog/2026/02/24/the-react-foundation | 366 / 11 | 469 / 15 | 469 / 15 | 406 / 3 | 1046 / 293 | 1046 / 293 | 1046 / 293 | — |
| react.dev/community | 211 / 11 | 374 / 12 | 374 / 12 | 251 / 3 | 800 / 279 | 800 / 279 | 800 / 279 | — |
| react.dev/community/acknowledgements | 316 / 11 | 459 / 12 | 459 / 12 | 356 / 3 | 1002 / 278 | 1002 / 278 | 1002 / 278 | — |
| react.dev/community/conferences | 3287 / 11 | 5796 / 12 | 5796 / 12 | 3327 / 3 | 8873 / 279 | 8873 / 279 | 8873 / 279 | — |
| react.dev/community/docs-contributors | 191 / 11 | 338 / 12 | 338 / 12 | 231 / 3 | 753 / 279 | 753 / 279 | 753 / 279 | — |
| react.dev/community/meetups | 509 / 11 | 952 / 12 | 952 / 12 | 549 / 3 | 1456 / 279 | 1456 / 279 | 1456 / 279 | — |
| react.dev/community/team | 1399 / 11 | 1774 / 12 | 1774 / 12 | 1439 / 3 | 3102 / 280 | 3102 / 280 | 3102 / 280 | — |
| react.dev/community/translations | 339 / 11 | 504 / 12 | 504 / 12 | 379 / 3 | 859 / 278 | 859 / 278 | 859 / 278 | — |
| react.dev/community/versioning-policy | 2226 / 11 | 2519 / 12 | 2519 / 12 | 2266 / 3 | 4817 / 279 | 4817 / 279 | 4817 / 279 | — |
| react.dev/community/videos | 926 / 11 | 1390 / 12 | 1390 / 12 | 966 / 3 | 2497 / 279 | 2497 / 279 | 2497 / 279 | — |
| react.dev/learn | 2033 / 12 | 2975 / 12 | 2985 / 12 | 2073 / 4 | 5354 / 802 | 4815 / 279 | 4815 / 279 | — |
| react.dev/learn/add-react-to-an-existing-project | 1029 / 13 | 1679 / 12 | 1679 / 12 | 1069 / 5 | 2867 / 283 | 2867 / 283 | 2867 / 283 | — |
| react.dev/learn/adding-interactivity | 1813 / 12 | 2520 / 12 | 2531 / 12 | 1858 / 4 | 6066 / 1111 | 5232 / 279 | 5232 / 279 | — |
| react.dev/learn/build-a-react-app-from-scratch | 1679 / 13 | 2331 / 12 | 2331 / 12 | 1719 / 5 | 4100 / 283 | 4100 / 283 | 4100 / 283 | — |
| react.dev/learn/choosing-the-state-structure | 3914 / 14 | 4529 / 12 | 4529 / 12 | 3954 / 6 | 11907 / 281 | 11907 / 281 | 11907 / 281 | — |
| react.dev/learn/conditional-rendering | 1839 / 15 | 2466 / 12 | 2482 / 12 | 1879 / 7 | 5375 / 802 | 4827 / 279 | 4827 / 279 | — |
| react.dev/learn/creating-a-react-app | 929 / 13 | 1553 / 12 | 1553 / 12 | 969 / 5 | 2599 / 281 | 2599 / 281 | 2599 / 281 | — |
| react.dev/learn/describing-the-ui | 1584 / 12 | 2527 / 12 | 2527 / 12 | 1624 / 4 | 4574 / 803 | 4062 / 280 | 4062 / 280 | — |
| react.dev/learn/editor-setup | 543 / 13 | 1128 / 12 | 1128 / 12 | 584 / 5 | 1813 / 279 | 1813 / 279 | 1813 / 279 | — |
| react.dev/learn/escape-hatches | 2534 / 12 | 3198 / 12 | 3198 / 12 | 2574 / 4 | 6659 / 802 | 6150 / 279 | 6150 / 279 | — |
| react.dev/learn/extracting-state-logic-into-a-reducer | 2818 / 14 | 3476 / 12 | 3476 / 12 | 2858 / 6 | 10808 / 1115 | 10006 / 283 | 10006 / 283 | — |
| react.dev/learn/importing-and-exporting-components | 1316 / 15 | 1939 / 12 | 1941 / 12 | 1356 / 7 | 4290 / 1113 | 3444 / 281 | 3444 / 281 | — |
| react.dev/learn/installation | 331 / 12 | 954 / 12 | 954 / 12 | 371 / 4 | 1936 / 801 | 1406 / 278 | 1406 / 278 | — |
| react.dev/learn/javascript-in-jsx-with-curly-braces | 1064 / 15 | 1709 / 12 | 1721 / 12 | 1104 / 7 | 4409 / 1204 | 3472 / 283 | 3472 / 283 | — |
| react.dev/learn/keeping-components-pure | 1876 / 15 | 2529 / 12 | 2529 / 12 | 1921 / 7 | 6375 / 803 | 5846 / 280 | 5846 / 280 | — |
| react.dev/learn/lifecycle-of-reactive-effects | 4739 / 14 | 5524 / 12 | 5534 / 12 | 4779 / 6 | 14227 / 281 | 14227 / 281 | 14227 / 281 | — |
| react.dev/learn/managing-state | 2050 / 12 | 2688 / 12 | 2706 / 12 | 2090 / 4 | 6248 / 1111 | 5485 / 279 | 5485 / 279 | — |
| react.dev/learn/manipulating-the-dom-with-refs | 2811 / 14 | 3453 / 12 | 3471 / 12 | 2851 / 6 | 7724 / 805 | 7183 / 282 | 7183 / 282 | — |
| react.dev/learn/passing-data-deeply-with-context | 2655 / 14 | 3773 / 12 | 3789 / 12 | 2695 / 6 | 7893 / 805 | 7379 / 282 | 7379 / 282 | — |
| react.dev/learn/passing-props-to-a-component | 1681 / 15 | 2390 / 12 | 2400 / 12 | 1726 / 7 | 6000 / 805 | 5460 / 282 | 5460 / 282 | — |
| react.dev/learn/preserving-and-resetting-state | 3454 / 14 | 6010 / 12 | 6010 / 12 | 3494 / 6 | 11574 / 1113 | 10750 / 281 | 10750 / 281 | — |
| react.dev/learn/queueing-a-series-of-state-updates | 1733 / 14 | 2435 / 12 | 2435 / 12 | 1778 / 6 | 5279 / 806 | 4752 / 283 | 4752 / 283 | — |
| react.dev/learn/react-compiler | 183 / 12 | 781 / 12 | 781 / 12 | 223 / 4 | 1105 / 279 | 1105 / 279 | 1105 / 279 | — |
| react.dev/learn/react-compiler/debugging | 660 / 14 | 1321 / 12 | 1321 / 12 | 700 / 6 | 2047 / 280 | 2047 / 280 | 2047 / 280 | — |
| react.dev/learn/react-compiler/incremental-adoption | 898 / 14 | 1620 / 12 | 1620 / 12 | 938 / 6 | 2515 / 279 | 2515 / 279 | 2515 / 279 | — |
| react.dev/learn/react-compiler/installation | 916 / 14 | 1628 / 12 | 1628 / 12 | 956 / 6 | 2496 / 278 | 2496 / 278 | 2496 / 278 | — |
| react.dev/learn/react-compiler/introduction | 1299 / 14 | 1993 / 12 | 1993 / 12 | 1339 / 6 | 3318 / 278 | 3318 / 278 | 3318 / 278 | — |
| react.dev/learn/react-developer-tools | 255 / 13 | 837 / 12 | 837 / 12 | 295 / 5 | 1238 / 280 | 1238 / 280 | 1238 / 280 | — |
| react.dev/learn/reacting-to-input-with-state | 2413 / 14 | 3306 / 12 | 3318 / 12 | 2468 / 6 | 7702 / 805 | 7229 / 282 | 7229 / 282 | — |
| react.dev/learn/referencing-values-with-refs | 1959 / 14 | 2619 / 12 | 2619 / 12 | 2004 / 6 | 5456 / 281 | 5456 / 281 | 5456 / 281 | — |
| react.dev/learn/removing-effect-dependencies | 5495 / 14 | 6279 / 12 | 6293 / 12 | 5535 / 6 | 15774 / 803 | 15217 / 280 | 15217 / 280 | — |
| react.dev/learn/render-and-commit | 1011 / 14 | 1758 / 12 | 1764 / 12 | 1066 / 6 | 2896 / 280 | 2896 / 280 | 2896 / 280 | — |
| react.dev/learn/rendering-lists | 1774 / 15 | 2398 / 12 | 2406 / 12 | 1814 / 7 | 6245 / 279 | 6257 / 279 | 6257 / 279 | — |
| react.dev/learn/responding-to-events | 2459 / 14 | 3125 / 12 | 3120 / 12 | 2499 / 6 | 6825 / 1201 | 5916 / 280 | 5916 / 280 | — |
| react.dev/learn/reusing-logic-with-custom-hooks | 5388 / 14 | 6114 / 12 | 6114 / 12 | 5428 / 6 | 15181 / 1114 | 14376 / 282 | 14376 / 282 | — |
| react.dev/learn/scaling-up-with-reducer-and-context | 1965 / 14 | 2512 / 12 | 2512 / 12 | 2005 / 6 | 6702 / 1115 | 5964 / 283 | 5964 / 283 | — |
| react.dev/learn/separating-events-from-effects | 3891 / 14 | 4615 / 12 | 4615 / 12 | 3931 / 6 | 11074 / 281 | 11074 / 281 | 11074 / 281 | — |
| react.dev/learn/setup | 154 / 12 | 744 / 12 | 744 / 12 | 194 / 4 | 1044 / 278 | 1044 / 278 | 1044 / 278 | — |
| react.dev/learn/sharing-state-between-components | 1810 / 14 | 2825 / 12 | 2825 / 12 | 1850 / 6 | 5689 / 804 | 5135 / 281 | 5135 / 281 | — |
| react.dev/learn/state-a-components-memory | 3004 / 14 | 3675 / 12 | 3675 / 12 | 3044 / 6 | 12653 / 804 | 12110 / 281 | 12110 / 281 | — |
| react.dev/learn/state-as-a-snapshot | 1686 / 14 | 2320 / 12 | 2320 / 12 | 1736 / 6 | 5042 / 1113 | 4201 / 281 | 4201 / 281 | — |
| react.dev/learn/synchronizing-with-effects | 6392 / 14 | 7223 / 12 | 7223 / 12 | 6432 / 6 | 15138 / 280 | 15138 / 280 | 15138 / 280 | — |
| react.dev/learn/thinking-in-react | 2922 / 14 | 3604 / 12 | 3604 / 12 | 2962 / 6 | 6502 / 280 | 6502 / 280 | 6502 / 280 | — |
| react.dev/learn/tutorial-tic-tac-toe | 10694 / 14 | 11326 / 12 | 11326 / 12 | 10734 / 6 | 22668 / 802 | 22356 / 279 | 22356 / 279 | — |
| react.dev/learn/typescript | 2426 / 13 | 3087 / 12 | 3087 / 12 | 2466 / 5 | 5460 / 279 | 5460 / 279 | 5460 / 279 | — |
| react.dev/learn/understanding-your-ui-as-a-tree | 1242 / 15 | 2422 / 12 | 2422 / 12 | 1282 / 7 | 4269 / 806 | 3731 / 283 | 3731 / 283 | — |
| react.dev/learn/updating-arrays-in-state | 3069 / 14 | 3711 / 12 | 3733 / 12 | 3109 / 6 | 8923 / 281 | 8923 / 281 | 8923 / 281 | — |
| react.dev/learn/updating-objects-in-state | 2812 / 14 | 3445 / 12 | 3454 / 12 | 2852 / 6 | 7665 / 281 | 7665 / 281 | 7665 / 281 | — |
| react.dev/learn/writing-markup-with-jsx | 1142 / 15 | 2044 / 12 | 2044 / 12 | 1182 / 7 | 3168 / 281 | 3168 / 281 | 3168 / 281 | — |
| react.dev/learn/you-might-not-need-an-effect | 5807 / 14 | 6565 / 12 | 6565 / 12 | 5847 / 6 | 14324 / 283 | 14324 / 283 | 14324 / 283 | — |
| react.dev/learn/your-first-component | 1344 / 15 | 2002 / 12 | 2008 / 12 | 1384 / 7 | 3690 / 280 | 3690 / 280 | 3690 / 280 | — |
| react.dev/link/new-jsx-transform | 1740 / 88 | 1754 / 20 | 1754 / 20 | — | 4141 / 2381 | — | 3992 / 2232 | — |
| react.dev/reference/dev-tools/react-performance-tracks | 1065 / 12 | 1901 / 12 | 1901 / 12 | 1105 / 4 | 2942 / 280 | 2942 / 280 | 2942 / 280 | — |
| react.dev/reference/eslint-plugin-react-hooks | 391 / 12 | 1110 / 12 | 1110 / 12 | 441 / 4 | 1571 / 278 | 1571 / 278 | 1571 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/com | 268 / 13 | 1021 / 12 | 1021 / 12 | 308 / 5 | 1334 / 278 | 1334 / 278 | 1334 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/con | 235 / 13 | 988 / 12 | 988 / 12 | 275 / 5 | 1276 / 278 | 1276 / 278 | 1276 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/err | 268 / 13 | 1024 / 12 | 1024 / 12 | 308 / 5 | 1366 / 278 | 1366 / 278 | 1366 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/exh | 581 / 13 | 1372 / 12 | 1372 / 12 | 621 / 5 | 1933 / 278 | 1933 / 278 | 1933 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/gat | 184 / 13 | 913 / 12 | 913 / 12 | 224 / 5 | 1168 / 278 | 1168 / 278 | 1168 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/glo | 270 / 13 | 999 / 12 | 999 / 12 | 310 / 5 | 1331 / 278 | 1331 / 278 | 1331 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/imm | 434 / 13 | 1221 / 12 | 1221 / 12 | 474 / 5 | 1680 / 278 | 1680 / 278 | 1680 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/inc | 706 / 13 | 1443 / 12 | 1443 / 12 | 746 / 5 | 2184 / 278 | 2184 / 278 | 2184 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/pre | 322 / 13 | 1077 / 12 | 1077 / 12 | 362 / 5 | 1449 / 278 | 1449 / 278 | 1449 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/pur | 276 / 13 | 1043 / 12 | 1043 / 12 | 316 / 5 | 1360 / 278 | 1360 / 278 | 1360 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/ref | 463 / 13 | 1239 / 12 | 1239 / 12 | 503 / 5 | 1732 / 278 | 1732 / 278 | 1732 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/rul | 614 / 13 | 1414 / 12 | 1414 / 12 | 654 / 5 | 1996 / 278 | 1996 / 278 | 1996 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/set | 458 / 13 | 1197 / 12 | 1197 / 12 | 498 / 5 | 1707 / 278 | 1707 / 278 | 1707 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/set | 404 / 13 | 1173 / 12 | 1173 / 12 | 444 / 5 | 1621 / 278 | 1621 / 278 | 1621 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/sta | 338 / 13 | 1093 / 12 | 1093 / 12 | 378 / 5 | 1481 / 278 | 1481 / 278 | 1481 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/uns | 335 / 13 | 1088 / 12 | 1088 / 12 | 375 / 5 | 1470 / 278 | 1470 / 278 | 1470 / 278 | — |
| react.dev/reference/eslint-plugin-react-hooks/lints/use | 307 / 13 | 1066 / 12 | 1066 / 12 | 347 / 5 | 1429 / 278 | 1429 / 278 | 1429 / 278 | — |
| react.dev/reference/react | 415 / 12 | 1180 / 12 | 1180 / 12 | 455 / 4 | 1633 / 280 | 1633 / 280 | 1633 / 280 | — |
| react.dev/reference/react-compiler/compilationMode | 620 / 13 | 1464 / 12 | 1464 / 12 | 660 / 5 | 1969 / 278 | 1969 / 278 | 1969 / 278 | — |
| react.dev/reference/react-compiler/compiling-libraries | 505 / 12 | 1363 / 12 | 1363 / 12 | 545 / 4 | 1791 / 279 | 1791 / 279 | 1791 / 279 | — |
| react.dev/reference/react-compiler/configuration | 374 / 12 | 1177 / 12 | 1177 / 12 | 414 / 4 | 1535 / 278 | 1535 / 278 | 1535 / 278 | — |
| react.dev/reference/react-compiler/directives | 697 / 12 | 1591 / 12 | 1591 / 12 | 737 / 4 | 2095 / 278 | 2095 / 278 | 2095 / 278 | — |
| react.dev/reference/react-compiler/directives/use-memo | 721 / 13 | 1567 / 12 | 1567 / 12 | 761 / 5 | 2186 / 280 | 2186 / 280 | 2186 / 280 | — |
| react.dev/reference/react-compiler/directives/use-no-me | 637 / 13 | 1469 / 12 | 1469 / 12 | 677 / 5 | 2032 / 281 | 2032 / 281 | 2032 / 281 | — |
| react.dev/reference/react-compiler/gating | 366 / 13 | 1173 / 12 | 1173 / 12 | 406 / 5 | 1481 / 278 | 1481 / 278 | 1481 / 278 | — |
| react.dev/reference/react-compiler/logger | 264 / 13 | 1049 / 12 | 1049 / 12 | 304 / 5 | 1300 / 278 | 1300 / 278 | 1300 / 278 | — |
| react.dev/reference/react-compiler/panicThreshold | 246 / 13 | 1024 / 12 | 1024 / 12 | 286 / 5 | 1260 / 278 | 1260 / 278 | 1260 / 278 | — |
| react.dev/reference/react-compiler/target | 453 / 13 | 1297 / 12 | 1297 / 12 | 493 / 5 | 1641 / 278 | 1641 / 278 | 1641 / 278 | — |
| react.dev/reference/react-dom | 336 / 12 | 1085 / 12 | 1085 / 12 | 376 / 4 | 1477 / 280 | 1477 / 280 | 1477 / 280 | — |
| react.dev/reference/react-dom/client | 137 / 12 | 864 / 12 | 864 / 12 | 177 / 4 | 1093 / 281 | 1093 / 281 | 1093 / 281 | — |
| react.dev/reference/react-dom/client/createRoot | 2325 / 14 | 3345 / 12 | 3345 / 12 | 2365 / 6 | 5614 / 278 | 5614 / 278 | 5614 / 278 | — |
| react.dev/reference/react-dom/client/hydrateRoot | 1958 / 14 | 2892 / 12 | 2896 / 12 | 1998 / 6 | 4912 / 278 | 4912 / 278 | 4912 / 278 | — |
| react.dev/reference/react-dom/components | 959 / 12 | 1753 / 12 | 1757 / 12 | 999 / 4 | 2753 / 280 | 2753 / 280 | 2753 / 280 | — |
| react.dev/reference/react-dom/components/common | 6375 / 13 | 7530 / 12 | 7544 / 12 | 6415 / 5 | 13359 / 281 | 13359 / 281 | 13359 / 281 | — |
| react.dev/reference/react-dom/components/form | 1537 / 13 | 2386 / 12 | 2398 / 12 | 1577 / 5 | 3869 / 278 | 3869 / 278 | 3869 / 278 | — |
| react.dev/reference/react-dom/components/input | 2956 / 13 | 3940 / 12 | 3940 / 12 | 2996 / 5 | 6637 / 278 | 6637 / 278 | 6637 / 278 | — |
| react.dev/reference/react-dom/components/link | 1465 / 13 | 2286 / 12 | 2294 / 12 | 1505 / 5 | 3643 / 278 | 3643 / 278 | 3643 / 278 | — |
| react.dev/reference/react-dom/components/meta | 539 / 13 | 1325 / 12 | 1325 / 12 | 579 / 5 | 1863 / 278 | 1863 / 278 | 1863 / 278 | — |
| react.dev/reference/react-dom/components/option | 272 / 13 | 1035 / 12 | 1035 / 12 | 312 / 5 | 1341 / 278 | 1341 / 278 | 1341 / 278 | — |
| react.dev/reference/react-dom/components/progress | 212 / 13 | 964 / 12 | 966 / 12 | 252 / 5 | 1759 / 801 | 1224 / 278 | 1224 / 278 | — |
| react.dev/reference/react-dom/components/script | 784 / 13 | 1550 / 12 | 1554 / 12 | 824 / 5 | 2315 / 278 | 2315 / 278 | 2315 / 278 | — |
| react.dev/reference/react-dom/components/select | 1674 / 13 | 2529 / 12 | 2529 / 12 | 1714 / 5 | 4112 / 278 | 4112 / 278 | 4112 / 278 | — |
| react.dev/reference/react-dom/components/style | 605 / 13 | 1364 / 12 | 1366 / 12 | 645 / 5 | 1981 / 278 | 1981 / 278 | 1981 / 278 | — |
| react.dev/reference/react-dom/components/textarea | 1966 / 13 | 2918 / 12 | 2918 / 12 | 2006 / 5 | 4775 / 278 | 4775 / 278 | 4775 / 278 | — |
| react.dev/reference/react-dom/components/title | 483 / 13 | 1259 / 12 | 1259 / 12 | 523 / 5 | 1752 / 278 | 1752 / 278 | 1752 / 278 | — |
| react.dev/reference/react-dom/createPortal | 1324 / 13 | 2161 / 12 | 2161 / 12 | 1364 / 5 | 3695 / 278 | 3695 / 278 | 3695 / 278 | — |
| react.dev/reference/react-dom/findDOMNode | 1162 / 11 | 2018 / 12 | 2018 / 12 | — | 3363 / 278 | — | 3363 / 278 | — |
| react.dev/reference/react-dom/flushSync | 905 / 13 | 1704 / 12 | 1704 / 12 | 945 / 5 | 2550 / 278 | 2550 / 278 | 2550 / 278 | — |
| react.dev/reference/react-dom/hooks | 175 / 12 | 888 / 12 | 888 / 12 | 215 / 4 | 1162 / 281 | 1162 / 281 | 1162 / 281 | — |
| react.dev/reference/react-dom/hooks/useFormStatus | 812 / 13 | 1623 / 12 | 1623 / 12 | 852 / 5 | 2439 / 278 | 2445 / 278 | 2445 / 278 | — |
| react.dev/reference/react-dom/hydrate | 866 / 11 | 1677 / 12 | 1677 / 12 | — | 2599 / 278 | — | 2599 / 278 | — |
| react.dev/reference/react-dom/preconnect | 393 / 13 | 1172 / 12 | 1172 / 12 | 433 / 5 | 1565 / 278 | 1565 / 278 | 1565 / 278 | — |
| react.dev/reference/react-dom/prefetchDNS | 431 / 13 | 1214 / 12 | 1214 / 12 | 471 / 5 | 1641 / 278 | 1641 / 278 | 1641 / 278 | — |
| react.dev/reference/react-dom/preinit | 586 / 13 | 1374 / 12 | 1374 / 12 | 626 / 5 | 1987 / 278 | 1987 / 278 | 1987 / 278 | — |
| react.dev/reference/react-dom/preinitModule | 482 / 13 | 1260 / 12 | 1260 / 12 | 522 / 5 | 1740 / 278 | 1740 / 278 | 1740 / 278 | — |
| react.dev/reference/react-dom/preload | 642 / 13 | 1430 / 12 | 1430 / 12 | 682 / 5 | 2172 / 278 | 2172 / 278 | 2172 / 278 | — |
| react.dev/reference/react-dom/preloadModule | 456 / 13 | 1234 / 12 | 1234 / 12 | 496 / 5 | 1687 / 278 | 1687 / 278 | 1687 / 278 | — |
| react.dev/reference/react-dom/render | 812 / 11 | 1620 / 12 | 1620 / 12 | — | 2522 / 278 | — | 2522 / 278 | — |
| react.dev/reference/react-dom/server | 225 / 12 | 982 / 12 | 982 / 12 | 265 / 4 | 1290 / 281 | 1290 / 281 | 1290 / 281 | — |
| react.dev/reference/react-dom/server/renderToNodeStream | 371 / 12 | 1158 / 12 | 1158 / 12 | — | 1582 / 278 | — | 1582 / 278 | — |
| react.dev/reference/react-dom/server/renderToPipeableSt | 3134 / 14 | 4098 / 12 | 4098 / 12 | 3174 / 6 | 6938 / 278 | 6938 / 278 | 6938 / 278 | — |
| react.dev/reference/react-dom/server/renderToReadableSt | 3189 / 14 | 4155 / 12 | 4155 / 12 | 3229 / 6 | 7064 / 278 | 7064 / 278 | 7064 / 278 | — |
| react.dev/reference/react-dom/server/renderToStaticMark | 341 / 14 | 1116 / 12 | 1116 / 12 | 381 / 6 | 1465 / 278 | 1465 / 278 | 1465 / 278 | — |
| react.dev/reference/react-dom/server/renderToStaticNode | 374 / 12 | 1163 / 12 | 1163 / 12 | — | 1587 / 278 | — | 1587 / 278 | — |
| react.dev/reference/react-dom/server/renderToString | 769 / 14 | 1643 / 12 | 1643 / 12 | 809 / 6 | 2319 / 278 | 2319 / 278 | 2319 / 278 | — |
| react.dev/reference/react-dom/server/resume | 842 / 14 | 1611 / 12 | 1611 / 12 | 882 / 6 | 2544 / 278 | 2544 / 278 | 2544 / 278 | — |
| react.dev/reference/react-dom/server/resumeToPipeableSt | 561 / 14 | 1319 / 12 | 1319 / 12 | 601 / 6 | 1902 / 278 | 1902 / 278 | 1902 / 278 | — |
| react.dev/reference/react-dom/static | 184 / 12 | 919 / 12 | 919 / 12 | 224 / 4 | 1203 / 281 | 1203 / 281 | 1203 / 281 | — |
| react.dev/reference/react-dom/static/prerender | 1767 / 14 | 2650 / 12 | 2650 / 12 | 1807 / 6 | 4266 / 278 | 4266 / 278 | 4266 / 278 | — |
| react.dev/reference/react-dom/static/prerenderToNodeStr | 1772 / 14 | 2655 / 12 | 2655 / 12 | 1812 / 6 | 4275 / 278 | 4275 / 278 | 4275 / 278 | — |
| react.dev/reference/react-dom/static/resumeAndPrerender | 524 / 14 | 1287 / 12 | 1287 / 12 | 564 / 6 | 1827 / 278 | 1827 / 278 | 1827 / 278 | — |
| react.dev/reference/react-dom/static/resumeAndPrerender | 520 / 14 | 1281 / 12 | 1281 / 12 | 560 / 6 | 1819 / 278 | 1819 / 278 | 1819 / 278 | — |
| react.dev/reference/react-dom/unmountComponentAtNode | 302 / 11 | 1077 / 12 | 1077 / 12 | — | 1464 / 278 | — | 1464 / 278 | — |
| react.dev/reference/react/Activity | 3001 / 13 | 3876 / 12 | 3876 / 12 | 3041 / 5 | 7622 / 278 | 7622 / 278 | 7622 / 278 | — |
| react.dev/reference/react/Children | 2697 / 15 | 3704 / 12 | 3704 / 12 | 2737 / 7 | 6467 / 278 | 6467 / 278 | 6467 / 278 | — |
| react.dev/reference/react/Component | 8044 / 15 | 9404 / 12 | 9404 / 12 | 8084 / 7 | 16797 / 278 | 16797 / 278 | 16797 / 278 | — |
| react.dev/reference/react/Fragment | 1452 / 13 | 2247 / 12 | 2247 / 12 | 1492 / 5 | 3592 / 279 | 3592 / 279 | 3592 / 279 | — |
| react.dev/reference/react/Profiler | 676 / 13 | 1471 / 12 | 1471 / 12 | 716 / 5 | 2109 / 278 | 2109 / 278 | 2109 / 278 | — |
| react.dev/reference/react/PureComponent | 707 / 15 | 1474 / 12 | 1474 / 12 | 747 / 7 | 2176 / 278 | 2176 / 278 | 2176 / 278 | — |
| react.dev/reference/react/StrictMode | 3167 / 13 | 4040 / 12 | 4040 / 12 | 3207 / 5 | 7997 / 278 | 7997 / 278 | 7997 / 278 | — |
| react.dev/reference/react/Suspense | 2848 / 13 | 3792 / 12 | 3792 / 12 | 2888 / 5 | 9480 / 278 | 9480 / 278 | 9480 / 278 | — |
| react.dev/reference/react/ViewTransition | 4885 / 13 | 5948 / 12 | 5948 / 12 | 4937 / 5 | 12800 / 278 | 12800 / 278 | 12800 / 278 | — |
| react.dev/reference/react/act | 796 / 13 | 1606 / 12 | 1606 / 12 | 836 / 5 | 2373 / 278 | 2373 / 278 | 2373 / 278 | — |
| react.dev/reference/react/addTransitionType | 553 / 13 | 1384 / 12 | 1384 / 12 | 605 / 5 | 1889 / 278 | 1889 / 278 | 1889 / 278 | — |
| react.dev/reference/react/apis | 205 / 12 | 922 / 12 | 922 / 12 | 245 / 4 | 1213 / 280 | 1213 / 280 | 1213 / 280 | — |
| react.dev/reference/react/cache | 2378 / 13 | 3258 / 12 | 3258 / 12 | 2418 / 5 | 5451 / 278 | 5451 / 278 | 5451 / 278 | — |
| react.dev/reference/react/cacheSignal | 444 / 13 | 1225 / 12 | 1225 / 12 | 484 / 5 | 1662 / 278 | 1662 / 278 | 1662 / 278 | — |
| react.dev/reference/react/captureOwnerStack | 878 / 13 | 1668 / 12 | 1674 / 12 | 918 / 5 | 2713 / 278 | 2713 / 278 | 2713 / 278 | — |
| react.dev/reference/react/cloneElement | 1516 / 15 | 2338 / 12 | 2338 / 12 | 1556 / 7 | 4130 / 278 | 4130 / 278 | 4130 / 278 | — |
| react.dev/reference/react/components | 116 / 12 | 845 / 12 | 845 / 12 | 156 / 4 | 1045 / 280 | 1045 / 280 | 1045 / 280 | — |
| react.dev/reference/react/createContext | 892 / 13 | 1738 / 12 | 1738 / 12 | 932 / 5 | 2534 / 278 | 2534 / 278 | 2534 / 278 | — |
| react.dev/reference/react/createElement | 937 / 15 | 1705 / 12 | 1705 / 12 | 977 / 7 | 2649 / 278 | 2649 / 278 | 2649 / 278 | — |
| react.dev/reference/react/createFactory | 744 / 13 | 1565 / 12 | 1565 / 12 | — | 2266 / 278 | — | 2263 / 278 | — |
| react.dev/reference/react/createRef | 544 / 15 | 1334 / 12 | 1334 / 12 | 584 / 7 | 1836 / 278 | 1836 / 278 | 1836 / 278 | — |
| react.dev/reference/react/experimental_taintObjectRefer | 800 / 13 | 1585 / 12 | 1585 / 12 | 852 / 5 | 2356 / 278 | 2356 / 278 | 2356 / 278 | — |
| react.dev/reference/react/experimental_taintUniqueValue | 1132 / 13 | 1915 / 12 | 1915 / 12 | 1184 / 5 | 3003 / 278 | 3003 / 278 | 3003 / 278 | — |
| react.dev/reference/react/forwardRef | 1529 / 15 | 2406 / 12 | 2406 / 12 | 1569 / 7 | 4038 / 278 | 4038 / 278 | 4038 / 278 | — |
| react.dev/reference/react/hooks | 741 / 12 | 1530 / 12 | 1530 / 12 | 781 / 4 | 2258 / 280 | 2258 / 280 | 2258 / 280 | — |
| react.dev/reference/react/isValidElement | 541 / 15 | 1313 / 12 | 1313 / 12 | 581 / 7 | 1816 / 278 | 1816 / 278 | 1816 / 278 | — |
| react.dev/reference/react/lazy | 698 / 13 | 1501 / 12 | 1503 / 12 | 738 / 5 | 2225 / 278 | 2225 / 278 | 2225 / 278 | — |
| react.dev/reference/react/legacy | 229 / 12 | 954 / 12 | 954 / 12 | 269 / 4 | 1266 / 280 | 1266 / 280 | 1266 / 280 | — |
| react.dev/reference/react/memo | 2529 / 13 | 3432 / 12 | 3432 / 12 | 2569 / 5 | 5766 / 278 | 5766 / 278 | 5766 / 278 | — |
| react.dev/reference/react/startTransition | 588 / 13 | 1358 / 12 | 1358 / 12 | 628 / 5 | 1953 / 278 | 1953 / 278 | 1953 / 278 | — |
| react.dev/reference/react/use | 1624 / 13 | 2467 / 12 | 2473 / 12 | 1664 / 5 | 4226 / 278 | 4226 / 278 | 4226 / 278 | — |
| react.dev/reference/react/useActionState | 3623 / 13 | 4623 / 12 | 4637 / 12 | 3663 / 5 | 8971 / 278 | 8971 / 278 | 8971 / 278 | — |
| react.dev/reference/react/useCallback | 3356 / 13 | 4247 / 12 | 4249 / 12 | 3396 / 5 | 8134 / 278 | 8134 / 278 | 8134 / 278 | — |
| react.dev/reference/react/useContext | 2052 / 13 | 2968 / 12 | 2976 / 12 | 2092 / 5 | 6457 / 278 | 6457 / 278 | 6457 / 278 | — |
| react.dev/reference/react/useDebugValue | 444 / 13 | 1234 / 12 | 1234 / 12 | 484 / 5 | 1707 / 278 | 1710 / 278 | 1710 / 278 | — |
| react.dev/reference/react/useDeferredValue | 2155 / 13 | 2994 / 12 | 2994 / 12 | 2195 / 5 | 6131 / 278 | 6131 / 278 | 6131 / 278 | — |
| react.dev/reference/react/useEffect | 5842 / 13 | 6940 / 12 | 6958 / 12 | 5882 / 5 | 14263 / 278 | 14263 / 278 | 14263 / 278 | — |
| react.dev/reference/react/useEffectEvent | 2070 / 13 | 3057 / 12 | 3065 / 12 | 2110 / 5 | 5008 / 278 | 5008 / 278 | 5008 / 278 | — |
| react.dev/reference/react/useId | 1106 / 13 | 1944 / 12 | 1950 / 12 | 1146 / 5 | 3025 / 278 | 3025 / 278 | 3025 / 278 | — |
| react.dev/reference/react/useImperativeHandle | 832 / 13 | 1610 / 12 | 1614 / 12 | 872 / 5 | 2609 / 278 | 2609 / 278 | 2609 / 278 | — |
| react.dev/reference/react/useInsertionEffect | 838 / 13 | 1614 / 12 | 1614 / 12 | 878 / 5 | 2422 / 278 | 2422 / 278 | 2422 / 278 | — |
| react.dev/reference/react/useLayoutEffect | 1627 / 13 | 2431 / 12 | 2431 / 12 | 1667 / 5 | 5044 / 278 | 5044 / 278 | 5044 / 278 | — |
| react.dev/reference/react/useMemo | 4699 / 13 | 5666 / 12 | 5666 / 12 | 4739 / 5 | 11685 / 278 | 11685 / 278 | 11685 / 278 | — |
| react.dev/reference/react/useOptimistic | 3556 / 13 | 4589 / 12 | 4589 / 12 | 3596 / 5 | 8265 / 278 | 8265 / 278 | 8265 / 278 | — |
| react.dev/reference/react/useReducer | 2779 / 13 | 3806 / 12 | 3806 / 12 | 2819 / 5 | 7153 / 278 | 7153 / 278 | 7153 / 278 | — |
| react.dev/reference/react/useRef | 1648 / 13 | 2522 / 12 | 2522 / 12 | 1688 / 5 | 4456 / 278 | 4456 / 278 | 4456 / 278 | — |
| react.dev/reference/react/useState | 3803 / 13 | 4903 / 12 | 4903 / 12 | 3843 / 5 | 9355 / 278 | 9355 / 278 | 9355 / 278 | — |
| react.dev/reference/react/useSyncExternalStore | 2049 / 13 | 2916 / 12 | 2916 / 12 | 2089 / 5 | 4896 / 278 | 4896 / 278 | 4896 / 278 | — |
| react.dev/reference/react/useTransition | 3428 / 13 | 4447 / 12 | 4447 / 12 | 3468 / 5 | 10017 / 278 | 10017 / 278 | 10017 / 278 | — |
| react.dev/reference/rsc/directives | 70 / 12 | 787 / 12 | 787 / 12 | 110 / 4 | 949 / 278 | 949 / 278 | 949 / 278 | — |
| react.dev/reference/rsc/server-components | 1387 / 12 | 2173 / 12 | 2173 / 12 | 1427 / 4 | 3489 / 279 | 3489 / 279 | 3489 / 279 | — |
| react.dev/reference/rsc/server-functions | 923 / 12 | 1736 / 12 | 1736 / 12 | 963 / 4 | 2704 / 279 | 2704 / 279 | 2704 / 279 | — |
| react.dev/reference/rsc/use-client | 2216 / 13 | 3466 / 12 | 3466 / 12 | 2256 / 5 | 5420 / 280 | 5420 / 280 | 5420 / 280 | — |
| react.dev/reference/rsc/use-server | 1101 / 13 | 1901 / 12 | 1901 / 12 | 1141 / 5 | 2954 / 280 | 2954 / 280 | 2954 / 280 | — |
| react.dev/reference/rules | 585 / 12 | 1341 / 12 | 1341 / 12 | 625 / 4 | 1964 / 280 | 1964 / 280 | 1964 / 280 | — |
| react.dev/reference/rules/components-and-hooks-must-be- | 2568 / 13 | 3479 / 12 | 3479 / 12 | 2608 / 5 | 5854 / 283 | 5854 / 283 | 5854 / 283 | — |
| react.dev/reference/rules/react-calls-components-and-ho | 767 / 13 | 1545 / 12 | 1545 / 12 | 807 / 5 | 2318 / 282 | 2318 / 282 | 2318 / 282 | — |
| react.dev/reference/rules/rules-of-hooks | 609 / 13 | 1352 / 12 | 1352 / 12 | 649 / 5 | 1985 / 280 | 1985 / 280 | 1985 / 280 | — |
| react.dev/versions | 1111 / 12 | 1458 / 12 | 1458 / 12 | 1151 / 4 | 2681 / 279 | 2681 / 279 | 2681 / 279 | — |
| react.dev/warnings/react-dom-test-utils | 192 / 12 | 447 / 12 | 447 / 12 | 232 / 4 | 770 / 280 | 770 / 280 | 770 / 280 | — |

</details>

## wikipedia-python

| Tool | Avg words [6] | Preamble [2] | Repeat rate [3] | Junk found [4] | Headings [7] | Code blocks [8] | Precision [5] | Recall [5] |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 3417 | 0 | 0% | 16 | 15.2 | 3.0 | 100% | 64% |
| crawl4ai | 5106 | 252 ⚠ | 0% | 211 | 14.9 | 3.0 | 100% | 41% |
| crawl4ai-raw | 5106 | 252 ⚠ | 0% | 211 | 14.9 | 3.0 | 100% | 41% |
| scrapy+md | 4925 | 4 | 0% | 67 | 15.2 | 3.0 | 99% | 77% |
| crawlee | 10493 | 5245 ⚠ | 3% | 162 | 16.1 | 3.0 | 52% | 89% |
| colly+md | 5446 | 270 ⚠ | 0% | 162 | 16.1 | 3.0 | 100% | 91% |
| playwright | 5249 | 387 ⚠ | 1% | 140 | 15.4 | 3.6 | 100% | 98% |
| firecrawl | — | — | — | — | — | — | — | — |

> **Column definitions:**
> **[6] Avg words** = mean words per page. **[2] Preamble** = avg words per page before the first heading (nav chrome). **[3] Repeat rate** = fraction of sentences on >50% of pages.
> **[4] Junk found** = total known boilerplate phrases detected across all pages. **[7] Headings** = avg headings per page. **[8] Code blocks** = avg fenced code blocks per page.
> **[5] Precision/Recall** = cross-tool consensus (pages with <2 sentences excluded). **⚠** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
**markcrawl** produces the cleanest output with 0 word of preamble per page, while **crawlee** injects 5245 words of nav chrome before content begins. The word count gap (3417 vs 10493 avg words) is largely explained by preamble: 5245 words of nav chrome account for ~50% of crawlee's output on this site. markcrawl's lower recall (64% vs 98%) reflects stricter content filtering — the "missed" sentences are predominantly navigation, sponsor links, and footer text that other tools include as content. For RAG, this is typically a net positive: fewer junk tokens per chunk tends to improve embedding quality and retrieval precision.

<details>
<summary>Sample output — first 40 lines of <code>en.wikipedia.org/wiki/Common_Language_Runtime</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
# Common Language Runtime

* [العربية](https://ar.wikipedia.org/wiki/%D9%88%D9%82%D8%AA_%D8%A7%D9%84%D8%AA%D9%86%D9%81%D9%8A%D8%B0_%D8%A7%D9%84%D9%85%D8%B4%D8%AA%D8%B1%D9%83_%D9%84%D9%84%D8%BA%D8%A7%D8%AA "وقت التنفيذ المشترك للغات – Arabic")
* [Català](https://ca.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Catalan")
* [Dansk](https://da.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Danish")
* [Deutsch](https://de.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – German")
* [Español](https://es.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Spanish")
* [Eesti](https://et.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Estonian")
* [Euskara](https://eu.wikipedia.org/wiki/CLR "CLR – Basque")
* [فارسی](https://fa.wikipedia.org/wiki/%D8%B2%D9%85%D8%A7%D9%86_%D8%A7%D8%AC%D8%B1%D8%A7%DB%8C_%D8%B2%D8%A8%D8%A7%D9%86_%D9%85%D8%B4%D8%AA%D8%B1%DA%A9 "زمان اجرای زبان مشترک – Persian")
* [Suomi](https://fi.wikipedia.org/wiki/CLR_(tietotekniikka) "CLR (tietotekniikka) – Finnish")
* [Français](https://fr.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – French")
* [עברית](https://he.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Hebrew")
* [Magyar](https://hu.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Hungarian")
* [Bahasa Indonesia](https://id.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Indonesian")
* [Italiano](https://it.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Italian")
* [日本語](https://ja.wikipedia.org/wiki/%E5%85%B1%E9%80%9A%E8%A8%80%E8%AA%9E%E3%83%A9%E3%83%B3%E3%82%BF%E3%82%A4%E3%83%A0 "共通言語ランタイム – Japanese")
* [한국어](https://ko.wikipedia.org/wiki/%EA%B3%B5%ED%86%B5_%EC%96%B8%EC%96%B4_%EB%9F%B0%ED%83%80%EC%9E%84 "공통 언어 런타임 – Korean")
* [Nederlands](https://nl.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Dutch")
* [Polski](https://pl.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Polish")
* [Português](https://pt.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Portuguese")
* [Русский](https://ru.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Russian")
* [Slovenščina](https://sl.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Slovenian")
* [Српски / srpski](https://sr.wikipedia.org/wiki/CLR "CLR – Serbian")
* [Svenska](https://sv.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Swedish")
* [ไทย](https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%84%E0%B8%97%E0%B8%A1%E0%B9%8C%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2%E0%B8%A3%E0%B9%88%E0%B8%A7%E0%B8%A1 "รันไทม์ภาษาร่วม – Thai")
* [Türkçe](https://tr.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Turkish")
* [Українська](https://uk.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Ukrainian")
* [中文](https://zh.wikipedia.org/wiki/%E9%80%9A%E7%94%A8%E8%AA%9E%E8%A8%80%E9%81%8B%E8%A1%8C%E5%BA%AB "通用語言運行庫 – Chinese")

[Edit links](https://www.wikidata.org/wiki/Special:EntityPage/Q733134#sitelinks-wikipedia "Edit interlanguage links")

From Wikipedia, the free encyclopedia

Virtual machine component of Microsoft's .NET framework

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | **This article has multiple issues.** Please help **[improve it](/wiki/Special:EditPage/Common_Language_Runtime "Special:EditPage/Common Language Runtime")** or discuss these issues on the **[talk page](/wiki/Talk:Common_Language_Runtime "Talk:Common Language Runtime")**. *([Learn how and when to remove these messages](/wiki/Help:Maintenance_template_removal "Help:Maintenance template removal"))* |  |  | | --- | --- | |  | This article **may rely excessively on sources [too closely associated with the subject](/wiki/Wikipedia:NIS "Wikipedia:NIS")**, potentially preventing the article from being [verifiable](/wiki/Wikipedia:Verifiability "Wikipedia:Verifiability") and [neutral](/wiki/Wikipedia:Neutral_point_of_view "Wikipedia:Neutral point of view"). Please help [improve it](https://en.wikipedia.org/w/index.php?title=Common_Language_Runtime&action=edit) by replacing them with more appropriate [citations](/wiki/Wikipedia:Citing_sources "Wikipedia:Citing sources") to [reliable, independent sources](/wiki/Wikipedia:Independent_sources "Wikipedia:Independent sources"). *(March 2019)* *([Learn how and when to remove this message](/wiki/Help:Maintenance_template_removal "Help:Maintenance template removal"))* |  |  |  | | --- | --- | |  | This article **needs additional citations for [verification](/wiki/Wikipedia:Verifiability "Wikipedia:Verifiability")**. Please help [improve this article](/wiki/Special:EditPage/Common_Language_Runtime "Special:EditPage/Common Language Runtime") by [adding citations to reliable sources](/wiki/Help:Referencing_for_beginners "Help:Referencing for beginners"). Unsourced material may be challenged and removed. *Find sources:* ["Common Language Runtime"](https://www.google.com/search?as_eq=wikipedia&q=%22Common+Language+Runtime%22) – [news](https://www.google.com/search?tbm=nws&q=%22Common+Language+Runtime%22+-wikipedia&tbs=ar:1) **·** [newspapers](https://www.google.com/search?&q=%22Common+Language+Runtime%22&tbs=bkt:s&tbm=bks) **·** [books](https://www.google.com/search?tbs=bks:1&q=%22Common+Language+Runtime%22+-wikipedia) **·** [scholar](https://scholar.google.com/scholar?q=%22Common+Language+Runtime%22) **·** [JSTOR](https://www.jstor.org/action/doBasicSearch?Query=%22Common+Language+Runtime%22&acc=on&wc=on) *(September 2014)* *([Learn how and when to remove this message](/wiki/Help:Maintenance_template_removal "Help:Maintenance template removal"))* |  *([Learn how and when to remove this message](/wiki/Help:Maintenance_template_removal "Help:Maintenance template removal"))* |
```

**crawl4ai**
```
[Jump to content](https://en.wikipedia.org/wiki/Common_Language_Runtime#bodyContent)
Main menu
Main menu
move to sidebar hide
Navigation 
  * [Main page](https://en.wikipedia.org/wiki/Main_Page "Visit the main page \[ctrl-option-z\]")
  * [Contents](https://en.wikipedia.org/wiki/Wikipedia:Contents "Guides to browsing Wikipedia")
  * [Current events](https://en.wikipedia.org/wiki/Portal:Current_events "Articles related to current events")
  * [Random article](https://en.wikipedia.org/wiki/Special:Random "Visit a randomly selected article \[ctrl-option-x\]")
  * [About Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:About "Learn about Wikipedia and how it works")
  * [Contact us](https://en.wikipedia.org/wiki/Wikipedia:Contact_us "How to contact Wikipedia")


Contribute 
  * [Help](https://en.wikipedia.org/wiki/Help:Contents "Guidance on how to use and edit Wikipedia")
  * [Learn to edit](https://en.wikipedia.org/wiki/Help:Introduction "Learn how to edit Wikipedia")
  * [Community portal](https://en.wikipedia.org/wiki/Wikipedia:Community_portal "The hub for editors")
  * [Recent changes](https://en.wikipedia.org/wiki/Special:RecentChanges "A list of recent changes to Wikipedia \[ctrl-option-r\]")
  * [Upload file](https://en.wikipedia.org/wiki/Wikipedia:File_upload_wizard "Add images or other media for use on Wikipedia")
  * [Special pages](https://en.wikipedia.org/wiki/Special:SpecialPages "A list of all special pages \[ctrl-option-q\]")


[ ![](https://en.wikipedia.org/static/images/icons/enwiki-25.svg) ![Wikipedia](https://en.wikipedia.org/static/images/mobile/copyright/wikipedia-wordmark-en-25.svg) ![The Free Encyclopedia](https://en.wikipedia.org/static/images/mobile/copyright/wikipedia-tagline-en-25.svg) ](https://en.wikipedia.org/wiki/Main_Page)
[Search ](https://en.wikipedia.org/wiki/Special:Search "Search Wikipedia \[ctrl-option-f\]")
Search
Appearance
Appearance
move to sidebar hide
Text
  * Small
Standard
Large

This page always uses small font size
Width
  * Standard
Wide

The content is as wide as possible for your browser window.
Color (beta)
```

**crawl4ai-raw**
```
[Jump to content](https://en.wikipedia.org/wiki/Common_Language_Runtime#bodyContent)
Main menu
Main menu
move to sidebar hide
Navigation 
  * [Main page](https://en.wikipedia.org/wiki/Main_Page "Visit the main page \[ctrl-option-z\]")
  * [Contents](https://en.wikipedia.org/wiki/Wikipedia:Contents "Guides to browsing Wikipedia")
  * [Current events](https://en.wikipedia.org/wiki/Portal:Current_events "Articles related to current events")
  * [Random article](https://en.wikipedia.org/wiki/Special:Random "Visit a randomly selected article \[ctrl-option-x\]")
  * [About Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:About "Learn about Wikipedia and how it works")
  * [Contact us](https://en.wikipedia.org/wiki/Wikipedia:Contact_us "How to contact Wikipedia")


Contribute 
  * [Help](https://en.wikipedia.org/wiki/Help:Contents "Guidance on how to use and edit Wikipedia")
  * [Learn to edit](https://en.wikipedia.org/wiki/Help:Introduction "Learn how to edit Wikipedia")
  * [Community portal](https://en.wikipedia.org/wiki/Wikipedia:Community_portal "The hub for editors")
  * [Recent changes](https://en.wikipedia.org/wiki/Special:RecentChanges "A list of recent changes to Wikipedia \[ctrl-option-r\]")
  * [Upload file](https://en.wikipedia.org/wiki/Wikipedia:File_upload_wizard "Add images or other media for use on Wikipedia")
  * [Special pages](https://en.wikipedia.org/wiki/Special:SpecialPages "A list of all special pages \[ctrl-option-q\]")


[ ![](https://en.wikipedia.org/static/images/icons/enwiki-25.svg) ![Wikipedia](https://en.wikipedia.org/static/images/mobile/copyright/wikipedia-wordmark-en-25.svg) ![The Free Encyclopedia](https://en.wikipedia.org/static/images/mobile/copyright/wikipedia-tagline-en-25.svg) ](https://en.wikipedia.org/wiki/Main_Page)
[Search ](https://en.wikipedia.org/wiki/Special:Search "Search Wikipedia \[ctrl-option-f\]")
Search
Appearance
Appearance
move to sidebar hide
Text
  * Small
Standard
Large

This page always uses small font size
Width
  * Standard
Wide

The content is as wide as possible for your browser window.
Color (beta)
```

**scrapy+md**
```
Toggle the table of contents

# Common Language Runtime

27 languages

* [العربية](https://ar.wikipedia.org/wiki/%D9%88%D9%82%D8%AA_%D8%A7%D9%84%D8%AA%D9%86%D9%81%D9%8A%D8%B0_%D8%A7%D9%84%D9%85%D8%B4%D8%AA%D8%B1%D9%83_%D9%84%D9%84%D8%BA%D8%A7%D8%AA "وقت التنفيذ المشترك للغات – Arabic")
* [Català](https://ca.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Catalan")
* [Dansk](https://da.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Danish")
* [Deutsch](https://de.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – German")
* [Español](https://es.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Spanish")
* [Eesti](https://et.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Estonian")
* [Euskara](https://eu.wikipedia.org/wiki/CLR "CLR – Basque")
* [فارسی](https://fa.wikipedia.org/wiki/%D8%B2%D9%85%D8%A7%D9%86_%D8%A7%D8%AC%D8%B1%D8%A7%DB%8C_%D8%B2%D8%A8%D8%A7%D9%86_%D9%85%D8%B4%D8%AA%D8%B1%DA%A9 "زمان اجرای زبان مشترک – Persian")
* [Suomi](https://fi.wikipedia.org/wiki/CLR_(tietotekniikka) "CLR (tietotekniikka) – Finnish")
* [Français](https://fr.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – French")
* [עברית](https://he.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Hebrew")
* [Magyar](https://hu.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Hungarian")
* [Bahasa Indonesia](https://id.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Indonesian")
* [Italiano](https://it.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Italian")
* [日本語](https://ja.wikipedia.org/wiki/%E5%85%B1%E9%80%9A%E8%A8%80%E8%AA%9E%E3%83%A9%E3%83%B3%E3%82%BF%E3%82%A4%E3%83%A0 "共通言語ランタイム – Japanese")
* [한국어](https://ko.wikipedia.org/wiki/%EA%B3%B5%ED%86%B5_%EC%96%B8%EC%96%B4_%EB%9F%B0%ED%83%80%EC%9E%84 "공통 언어 런타임 – Korean")
* [Nederlands](https://nl.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Dutch")
* [Polski](https://pl.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Polish")
* [Português](https://pt.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Portuguese")
* [Русский](https://ru.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Russian")
* [Slovenščina](https://sl.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Slovenian")
* [Српски / srpski](https://sr.wikipedia.org/wiki/CLR "CLR – Serbian")
* [Svenska](https://sv.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Swedish")
* [ไทย](https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%84%E0%B8%97%E0%B8%A1%E0%B9%8C%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2%E0%B8%A3%E0%B9%88%E0%B8%A7%E0%B8%A1 "รันไทม์ภาษาร่วม – Thai")
* [Türkçe](https://tr.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Turkish")
* [Українська](https://uk.wikipedia.org/wiki/Common_Language_Runtime "Common Language Runtime – Ukrainian")
* [中文](https://zh.wikipedia.org/wiki/%E9%80%9A%E7%94%A8%E8%AA%9E%E8%A8%80%E9%81%8B%E8%A1%8C%E5%BA%AB "通用語言運行庫 – Chinese")

[Edit links](https://www.wikidata.org/wiki/Special:EntityPage/Q733134#sitelinks-wikipedia "Edit interlanguage links")

* [Article](/wiki/Common_Language_Runtime "View the content page [c]")
* [Talk](/wiki/Talk:Common_Language_Runtime "Discuss improvements to the content page [t]")

English
```

**crawlee**
```
Common Language Runtime - Wikipedia
(function(){var className="client-js vector-feature-language-in-header-enabled vector-feature-language-in-main-menu-disabled vector-feature-language-in-main-page-header-disabled vector-feature-page-tools-pinned-disabled vector-feature-toc-pinned-clientpref-1 vector-feature-main-menu-pinned-disabled vector-feature-limited-width-clientpref-1 vector-feature-limited-width-content-enabled vector-feature-custom-font-size-clientpref-1 vector-feature-appearance-pinned-clientpref-1 skin-theme-clientpref-day vector-sticky-header-enabled vector-toc-available skin-theme-clientpref-thumb-standard";var cookie=document.cookie.match(/(?:^|; )enwikimwclientpreferences=([^;]+)/);if(cookie){cookie[1].split('%2C').forEach(function(pref){className=className.replace(new RegExp('(^| )'+pref.replace(/-clientpref-\w+$|[^\w-]+/g,'')+'-clientpref-\\w+( |$)'),'$1'+pref+'$2');});}document.documentElement.className=className;}());RLCONF={"wgBreakFrames":false,"wgSeparatorTransformTable":["",""],"wgDigitTransformTable":["",""],"wgDefaultDateFormat":"dmy","wgMonthNames":["","January","February","March","April","May","June","July","August","September","October","November","December"],"wgRequestId":"5db3c8d3-dd97-4df7-944c-ddf94314b59a","wgCanonicalNamespace":"","wgCanonicalSpecialPageName":false,"wgNamespaceNumber":0,"wgPageName":"Common\_Language\_Runtime","wgTitle":"Common Language Runtime","wgCurRevisionId":1317322509,"wgRevisionId":1317322509,"wgArticleId":46003,"wgIsArticle":true,"wgIsRedirect":false,"wgAction":"view","wgUserName":null,"wgUserGroups":["\*"],"wgCategories":["Articles with short description","Short description matches Wikidata","Articles lacking reliable references from March 2019","All articles lacking reliable references","Articles needing additional references from September 2014","All articles needing additional references","Articles with multiple maintenance issues",".NET Framework terminology","Stack-based virtual machines"],"wgPageViewLanguage":"en","wgPageContentLanguage":"en","wgPageContentModel":"wikitext","wgRelevantPageName":"Common\_Language\_Runtime","wgRelevantArticleId":46003,"wgTempUserName":null,"wgIsProbablyEditable":true,"wgRelevantPageIsProbablyEditable":true,"wgRestrictionEdit":[],"wgRestrictionMove":[],"wgNoticeProject":"wikipedia","wgFlaggedRevsParams":{"tags":{"status":{"levels":1}}},"wgConfirmEditCaptchaNeededForGenericEdit":"hcaptcha","wgConfirmEditHCaptchaVisualEditorOnLoadIntegrationEnabled":false,"wgConfirmEditHCaptchaSiteKey":"5d0c670e-a5f4-4258-ad16-1f42792c9c62","wgMediaViewerOnClick":true,"wgMediaViewerEnabledByDefault":true,"wgPopupsFlags":0,"wgVisualEditor":{"pageLanguageCode":"en","pageLanguageDir":"ltr","pageVariantFallbacks":"en"},"wgMFDisplayWikibaseDescriptions":{"search":true,"watchlist":true,"tagline":false,"nearby":true},"wgWMESchemaEditAttemptStepOversample":false,"wgWMEPageLength":4000,"wgEditSubmitButtonLabelPublish":true,"wgVisualEditorPageIsDisambiguation":false,"wgULSPosition":"interlanguage","wgULSisCompactLinksEnabled":false,"wgVector2022LanguageInHeader":true,"wgULSisLanguageSelectorEmpty":false,"wgWikibaseItemId":"Q733134","wgCheckUserClientHintsHeadersJsApi":["brands","architecture","bitness","fullVersionList","mobile","model","platform","platformVersion"],"GEHomepageSuggestedEditsEnableTopics":true,"wgGESuggestedEditsTaskTypes":{"taskTypes":["copyedit","link-recommendation"],"unavailableTaskTypes":[]},"wgGETopicsMatchModeEnabled":false,"wgGELevelingUpEnabledForUser":false,"wgTestKitchenUserExperiments":{"overrides":[],"enrolled":[],"assigned":[],"subject\_ids":[]}};
RLSTATE={"ext.globalCssJs.user.styles":"ready","site.styles":"ready","user.styles":"ready","ext.globalCssJs.user":"ready","user":"ready","user.options":"loading","ext.wikimediamessages.styles":"ready","ext.cite.styles":"ready","skins.vector.search.codex.styles":"ready","skins.vector.styles":"ready","skins.vector.icons":"ready","jquery.makeCollapsible.styles":"ready","ext.visualEditor.desktopArticleTarget.noscript":"ready","ext.uls.interlanguage":"ready","wikibase.client.init":"ready"};RLPAGEMODULES=["ext.parsermigration.survey","ext.cite.ux-enhancements","site","mediawiki.page.ready","jquery.makeCollapsible","skins.vector.js","ext.centralNotice.geoIP","ext.centralNotice.startUp","ext.gadget.ReferenceTooltips","ext.gadget.switcher","ext.urlShortener.toolbar","ext.centralauth.centralautologin","mmv.bootstrap","ext.popups","ext.visualEditor.desktopArticleTarget.init","ext.echo.centralauth","ext.eventLogging","ext.wikimediaEvents","ext.navigationTiming","ext.uls.interface","ext.cx.eventlogging.campaigns","ext.cx.uls.quick.actions","wikibase.client.vector-2022","wikibase.databox.fromWikidata","ext.checkUser.clientHints","ext.quicksurveys.init","ext.growthExperiments.SuggestedEditSession","ext.testKitchen"];
(RLQ=window.RLQ||[]).push(function(){mw.loader.impl(function(){return["user.options@12s5i",function($,jQuery,require,module){mw.user.tokens.set({"patrolToken":"+\\","watchToken":"+\\","csrfToken":"+\\"});
}];});});



.mw-spinner{position:relative; }.mw-spinner > .mw-spinner-container{transform-origin:0 0}.mw-spinner-small{width:20px;height:20px}.mw-spinner-small > .mw-spinner-container{transform:scale(0.3125)}.mw-spinner-large{width:32px;height:32px}.mw-spinner-large > .mw-spinner-container{transform:scale(0.5)}.mw-spinner-block{display:block;width:100%;text-align:center}.mw-spinner-block > .mw-spinner-container{display:inline-block;vertical-align:top}.mw-spinner-block.mw-spinner-small > .mw-spinner-container{min-width:20px}.mw-spinner-block.mw-spinner-large > .mw-spinner-container{min-width:32px}.mw-spinner-inline{display:inline-block;vertical-align:middle}.mw-spinner-container > div{transform-origin:32px 32px;animation:mw-spinner 1.2s linear infinite}.mw-spinner-container > div::after{content:' ';display:block;position:absolute;top:3px; left:29px;width:5px;height:14px;border-radius:20%;background:var(--color-base,#202122)}.mw-spinner-container > div:nth-child(1){transform:rotate(0deg);animation-delay:-1.1s}.mw-spinner-container > div:nth-child(2){transform:rotate(30deg);animation-delay:-1s}.mw-spinner-container > div:nth-child(3){transform:rotate(60deg);animation-delay:-0.9s}.mw-spinner-container > div:nth-child(4){transform:rotate(90deg);animation-delay:-0.8s}.mw-spinner-container > div:nth-child(5){transform:rotate(120deg);animation-delay:-0.7s}.mw-spinner-container > div:nth-child(6){transform:rotate(150deg);animation-delay:-0.6s}.mw-spinner-container > div:nth-child(7){transform:rotate(180deg);animation-delay:-0.5s}.mw-spinner-container > div:nth-child(8){transform:rotate(210deg);animation-delay:-0.4s}.mw-spinner-container > div:nth-child(9){transform:rotate(240deg);animation-delay:-0.3s}.mw-spinner-container > div:nth-child(10){transform:rotate(270deg);animation-delay:-0.2s}.mw-spinner-container > div:nth-child(11){transform:rotate(300deg);animation-delay:-0.1s}.mw-spinner-container > div:nth-child(12){transform:rotate(330deg);animation-delay:0s}@keyframes mw-spinner{0%{opacity:1}100%{opacity:0}}
.mw-editfont-monospace{font-family:monospace,monospace}.mw-editfont-sans-serif{font-family:sans-serif}.mw-editfont-serif{font-family:serif} .mw-editfont-monospace,.mw-editfont-sans-serif,.mw-editfont-serif{font-size:0.8125rem; -moz-tab-size:4;tab-size:4; }.mw-editfont-monospace.oo-ui-textInputWidget,.mw-editfont-sans-serif.oo-ui-textInputWidget,.mw-editfont-serif.oo-ui-textInputWidget{font-size:inherit}.mw-editfont-monospace.oo-ui-textInputWidget > .oo-ui-inputWidget-input,.mw-editfont-sans-serif.oo-ui-textInputWidget > .oo-ui-inputWidget-input,.mw-editfont-serif.oo-ui-textInputWidget > .oo-ui-inputWidget-input{font-size:0.8125rem}.mw-editfont-monospace.oo-ui-textInputWidget > input.oo-ui-inputWidget-input,.mw-editfont-sans-serif.oo-ui-textInputWidget > input.oo-ui-inputWidget-input,.mw-editfont-serif.oo-ui-textInputWidget > input.oo-ui-inputWidget-input{min-height:32px}
.vector-icon.mw-ui-icon-wikimedia-appearance{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=appearance&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=appearance&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-appearance-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=appearance&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=appearance&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-appearance-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=appearance&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=appearance&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-speechBubbleAdd{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbleAdd&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbleAdd&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-speechBubbleAdd-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbleAdd&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbleAdd&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-speechBubbleAdd-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbleAdd&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbleAdd&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-speechBubbles{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbles&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbles&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-speechBubbles-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbles&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbles&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-speechBubbles-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbles&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=speechBubbles&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-article{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=article&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=article&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-article-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=article&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=article&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-article-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=article&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=article&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-history{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=history&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=history&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-history-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=history&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=history&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-history-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=history&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=history&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-wikiText{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=wikiText&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=wikiText&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-wikiText-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=wikiText&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=wikiText&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-wikiText-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=wikiText&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=wikiText&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-edit{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=edit&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=edit&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-edit-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=edit&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=edit&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-edit-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=edit&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=edit&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-editLock{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=editLock&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=editLock&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-editLock-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=editLock&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=editLock&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-editLock-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=editLock&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=editLock&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-exitFullscreen{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=exitFullscreen&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=exitFullscreen&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-exitFullscreen-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=exitFullscreen&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=exitFullscreen&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-exitFullscreen-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=exitFullscreen&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=exitFullscreen&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-fullScreen{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=fullScreen&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=fullScreen&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-fullScreen-invert{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=fullScreen&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=fullScreen&variant=invert&format=original&lang=en&skin=vector-2022&version=8l5k3)}.vector-icon.mw-ui-icon-wikimedia-fullScreen-progressive{-webkit-mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=fullScreen&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3);mask-image:url(https://en.wikipedia.org/w/load.php?modules=skins.vector.icons.js&image=fullScreen&variant=progressive&format=original&lang=en&skin=vector-2022&version=8l5k3)}
.cite-accessibility-label{ top:-99999px;clip:rect(1px,1px,1px,1px); position:absolute !important;padding:0 !important;border:0 !important;height:1px !important;width:1px !important; overflow:hidden}:target .mw-cite-targeted-backlink{font-weight:bold}.mw-cite-up-arrow-backlink{display:none}:target .mw-cite-up-arrow-backlink{display:inline}:target .mw-cite-up-arrow{display:none}
.ext-urlshortener-result-dialog{font-size:0.90909em}.ext-urlshortener-result-dialog a{word-wrap:break-word}.ext-urlshortener-qrcode{text-align:center}.ext-urlshortener-qrcode img{width:320px}
.cdx-button{display:inline-flex;align-items:center;justify-content:center;gap:6px;box-sizing:border-box;min-height:32px;max-width:28rem;margin:0;border-width:1px;border-style:solid;border-radius:2px;padding-right:11px;padding-left:11px;font-family:inherit;font-size:var(--font-size-medium,1rem);font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-transform:none;transition-property:background-color,color,border-color,box-shadow;transition-duration:.1s}.cdx-button--size-small{gap:4px;min-height:1.5rem;padding-right:5px;padding-left:5px}.cdx-button--size-large{min-height:44px;padding-right:15px;padding-left:15px}.cdx-button--icon-only{min-width:32px;padding-right:0;padding-left:0}.cdx-button--icon-only.cdx-button--size-small{min-width:1.5rem}.cdx-button--icon-only.cdx-button--size-large{min-width:44px}.cdx-button::-moz-focus-inner{border:0;padding:0}.cdx-button .cdx-button\_\_icon,.cdx-button .cdx-icon{vertical-align:middle}.cdx-button .cdx-icon{color:inherit}.cdx-button--fake-button,.cdx-button--fake-button:hover,.cdx-button--fake-button:focus{text-decoration:none}.cdx-button:enabled,.cdx-button.cdx-button--fake-button--enabled{background-color:var(--background-color-interactive-subtle,#f8f9fa);color:var(--color-neutral,#404244);border-color:var(--border-color-interactive,#72777d)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled .cdx-button\_\_icon{background-color:var(--color-neutral,#404244)}}.cdx-button:enabled:hover,.cdx-button.cdx-button--fake-button--enabled:hover{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);border-color:var(--border-color-interactive--hover,#27292d);cursor:pointer}.cdx-button:enabled:active,.cdx-button.cdx-button--fake-button--enabled:active,.cdx-button:enabled.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--is-active{background-color:var(--background-color-interactive-subtle--active,#dadde3);border-color:var(--border-color-interactive--active,#202122)}.cdx-button:enabled:focus,.cdx-button.cdx-button--fake-button--enabled:focus{outline:1px solid transparent}.cdx-button:enabled:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c)}.cdx-button:enabled.cdx-button--action-progressive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive{background-color:var(--background-color-progressive-subtle,#e8eeff);color:var(--color-progressive,#36c);border-color:var(--border-color-progressive,#6485d1)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-progressive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive .cdx-button\_\_icon{background-color:var(--color-progressive,#36c)}}.cdx-button:enabled.cdx-button--action-progressive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:hover{background-color:var(--background-color-progressive-subtle--hover,#d9e2ff);color:var(--color-progressive--hover,#3056a9);border-color:var(--border-color-progressive--hover,#3056a9)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-progressive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:hover .cdx-button\_\_icon{background-color:var(--color-progressive--hover,#3056a9)}}.cdx-button:enabled.cdx-button--action-progressive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:active,.cdx-button:enabled.cdx-button--action-progressive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive.cdx-button--is-active{background-color:var(--background-color-progressive-subtle--active,#b6d4fb);color:var(--color-progressive--active,#233566);border-color:var(--border-color-progressive--active,#233566)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-progressive--active,#233566)}}.cdx-button:enabled.cdx-button--action-destructive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive{background-color:var(--background-color-destructive-subtle,#ffe9e5);color:var(--color-destructive,#bf3c2c);border-color:var(--border-color-destructive,#f54739)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-destructive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive .cdx-button\_\_icon{background-color:var(--color-destructive,#bf3c2c)}}.cdx-button:enabled.cdx-button--action-destructive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:hover{background-color:var(--background-color-destructive-subtle--hover,#ffdad3);color:var(--color-destructive--hover,#9f3526);border-color:var(--border-color-destructive--hover,#9f3526)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-destructive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:hover .cdx-button\_\_icon{background-color:var(--color-destructive--hover,#9f3526)}}.cdx-button:enabled.cdx-button--action-destructive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:active,.cdx-button:enabled.cdx-button--action-destructive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive.cdx-button--is-active{background-color:var(--background-color-destructive-subtle--active,#ffc8bd);color:var(--color-destructive--active,#612419);border-color:var(--border-color-destructive--active,#612419)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-destructive--active,#612419)}}.cdx-button:enabled.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-destructive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-destructive--focus,#36c)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive{background-color:var(--background-color-progressive,#36c);color:var(--color-inverted-fixed,#fff);border-color:var(--border-color-transparent,transparent)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive:hover{background-color:var(--background-color-progressive--hover,#3056a9)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive:active,.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive.cdx-button--is-active{background-color:var(--background-color-progressive--active,#233566)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c),inset 0 0 0 2px var(--box-shadow-color-inverted,#fff)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive .cdx-button\_\_icon{background-color:var(--color-inverted-fixed,#fff)}}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive{background-color:var(--background-color-destructive,#bf3c2c);color:var(--color-inverted-fixed,#fff);border-color:var(--border-color-transparent,transparent)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive:hover{background-color:var(--background-color-destructive--hover,#9f3526)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive:active,.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive.cdx-button--is-active{background-color:var(--background-color-destructive--active,#612419)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-destructive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-destructive--focus,#36c),inset 0 0 0 2px var(--box-shadow-color-inverted,#fff)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive .cdx-button\_\_icon{background-color:var(--color-inverted-fixed,#fff)}}.cdx-button:enabled.cdx-button--weight-quiet,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet{background-color:var(--background-color-transparent,transparent);border-color:var(--border-color-transparent,transparent)}.cdx-button:enabled.cdx-button--weight-quiet:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet:hover{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);mix-blend-mode:var(--mix-blend-mode-blend,multiply)}.cdx-button:enabled.cdx-button--weight-quiet:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet:active,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--is-active{background-color:var(--background-color-interactive-subtle--active,#dadde3)}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive{color:var(--color-progressive,#36c)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive .cdx-button\_\_icon{background-color:var(--color-progressive,#36c)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover{background-color:var(--background-color-progressive-subtle--hover,#d9e2ff);color:var(--color-progressive--hover,#3056a9);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover .cdx-button\_\_icon{background-color:var(--color-progressive--hover,#3056a9)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active{background-color:var(--background-color-progressive-subtle--active,#b6d4fb);color:var(--color-progressive--active,#233566);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-progressive--active,#233566)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c)}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive{color:var(--color-destructive,#bf3c2c)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive .cdx-button\_\_icon{background-color:var(--color-destructive,#bf3c2c)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover{background-color:var(--background-color-destructive-subtle--hover,#ffdad3);color:var(--color-destructive--hover,#9f3526);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover .cdx-button\_\_icon{background-color:var(--color-destructive--hover,#9f3526)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active{background-color:var(--background-color-destructive-subtle--active,#ffc8bd);color:var(--color-destructive--active,#612419);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-destructive--active,#612419)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-destructive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-destructive--focus,#36c)}.cdx-button:disabled,.cdx-button.cdx-button--fake-button--disabled{background-color:var(--background-color-disabled,#dadde3);color:var(--color-disabled-emphasized,#a2a9b1);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:disabled .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--disabled .cdx-button\_\_icon{background-color:var(--color-inverted,#fff)}}.cdx-button:disabled.cdx-button--weight-quiet,.cdx-button.cdx-button--fake-button--disabled.cdx-button--weight-quiet{background-color:var(--background-color-transparent,transparent);color:var(--color-disabled,#a2a9b1)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:disabled.cdx-button--weight-quiet .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--disabled.cdx-button--weight-quiet .cdx-button\_\_icon{background-color:var(--color-disabled,#a2a9b1)}}.cdx-icon{color:var(--color-base,#202122);display:inline-flex;align-items:center;justify-content:center;vertical-align:text-bottom}.cdx-icon svg{fill:currentcolor;width:100%;height:100%}.cdx-icon--x-small{min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) - 4px);height:calc(var(--font-size-medium,1rem) - 4px)}.cdx-icon--small{min-width:14px;min-height:14px;width:var(--font-size-medium,1rem);height:var(--font-size-medium,1rem)}.cdx-icon--medium{min-width:18px;min-height:18px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px)}.cdx-icon--flipped svg{transform:scaleX(-1)}.cdx-dialog-backdrop{background-color:var(--background-color-backdrop-light,rgba(255,255,255,.65));display:flex;align-items:center;justify-content:center;position:fixed;top:0;left:0;z-index:400;min-height:100%;width:100vw;height:100vh;height:-webkit-fill-available}.cdx-dialog{background-color:var(--background-color-base,#fff);display:flex;flex-direction:column;box-sizing:border-box;width:100%;height:100%}@media (min-width:640px){.cdx-dialog{width:calc(100% - 2rem);height:unset;max-width:32rem;max-height:calc(100vh - 2.5rem);border:1px solid var(--border-color-base,#a2a9b1);border-radius:2px;box-shadow:0 4px 8px 0 var(--box-shadow-color-alpha-base,rgba(0,0,0,.06)),0 0 16px 0 var(--box-shadow-color-alpha-base,rgba(0,0,0,.06))}}.cdx-dialog\_\_header{padding:16px 24px 8px}.cdx-dialog\_\_header--default{display:flex;align-items:baseline;justify-content:flex-end;box-sizing:border-box;width:100%}.cdx-dialog\_\_header\_\_title-group{display:flex;flex-grow:1;flex-direction:column}.cdx-dialog\_\_header .cdx-dialog\_\_header\_\_title{margin:0;border:0;padding:0;font-family:inherit;font-size:var(--font-size-x-large,1.25rem);font-weight:700;line-height:var(--line-height-x-large,1.875rem)}.cdx-dialog\_\_header .cdx-dialog\_\_header\_\_subtitle{color:var(--color-subtle,#54595d);margin:0;padding:0;font-size:var(--font-size-medium,1rem);line-height:var(--line-height-small,1.375rem)}.cdx-dialog\_\_header\_\_close-button.cdx-button{margin-right:-8px}@media (min-width:640px){.cdx-dialog\_\_header--no-close-button .cdx-dialog\_\_header\_\_close-button{display:none}}.cdx-dialog--dividers .cdx-dialog\_\_header{border-bottom:1px solid var(--border-color-subtle,#c8ccd1)}.cdx-dialog\_\_body{padding:8px 24px;overflow-y:auto;font-family:sans-serif;font-size:var(--font-size-medium,1rem);font-weight:400;line-height:var(--line-height-medium,1.625rem)}.cdx-dialog\_\_body--no-footer{padding-bottom:24px}.cdx-dialog\_\_body>\*:first-child{margin-top:0;padding-top:0}.cdx-dialog\_\_body>\*:last-child{margin-bottom:0;padding-bottom:0}.cdx-dialog\_\_footer{margin-top:auto;padding:16px 24px 24px}.cdx-dialog--dividers .cdx-dialog\_\_footer{border-top:1px solid var(--border-color-subtle,#c8ccd1)}.cdx-dialog\_\_footer--default{display:flex;align-items:baseline;flex-wrap:wrap;justify-content:space-between;gap:12px}.cdx-dialog\_\_footer .cdx-dialog\_\_footer\_\_text{color:var(--color-subtle,#54595d);flex:1 0 auto;width:100%;margin:0;font-size:var(--font-size-small,.875rem);line-height:var(--line-height-small,1.375rem)}.cdx-dialog\_\_footer\_\_actions{display:flex;flex-grow:1;flex-direction:row-reverse;gap:12px}@media (max-width:639px){.cdx-dialog\_\_footer\_\_actions{flex-direction:column;width:100%}.cdx-dialog\_\_footer\_\_actions .cdx-button{max-width:none}}.cdx-dialog--vertical-actions .cdx-dialog\_\_footer\_\_actions{flex-direction:column;width:100%}.cdx-dialog--vertical-actions .cdx-dialog\_\_footer\_\_actions .cdx-button{max-width:none}.cdx-dialog-focus-trap{position:absolute}.cdx-dialog-focus-trap:focus{outline:0}.cdx-dialog-fade-enter-active,.cdx-dialog-fade-leave-active{transition-property:opacity;transition-duration:.25s;transition-timing-function:ease}.cdx-dialog-fade-enter-from,.cdx-dialog-fade-leave-to{opacity:0}body.cdx-dialog-open{overflow:hidden}.cdx-progress-bar{box-sizing:border-box;overflow-x:hidden}.cdx-progress-bar\_\_bar{width:33.33%;height:100%}.cdx-progress-bar:not(.cdx-progress-bar--inline){position:relative;z-index:1;height:1rem;max-width:none;border-radius:9999px;box-shadow:0 0 0 1px var(--box-shadow-color-base,#a2a9b1)}.cdx-progress-bar--inline{width:100%;height:.25rem}.cdx-progress-bar:not(.cdx-progress-bar--disabled) .cdx-progress-bar\_\_bar{background-color:var(--background-color-progressive,#36c);animation-name:cdx-animation-progress-bar\_\_bar;animation-duration:1.6s;animation-timing-function:linear;animation-iteration-count:infinite}.cdx-progress-bar:not(.cdx-progress-bar--disabled).cdx-progress-bar--block{background-color:var(--background-color-base,#fff)}.cdx-progress-bar--disabled .cdx-progress-bar\_\_bar{background-color:var(--background-color-disabled,#dadde3)}.cdx-progress-bar--disabled:not(.cdx-progress-bar--inline){background-color:var(--background-color-disabled-subtle,#eaecf0)}@keyframes cdx-animation-progress-bar\_\_bar{0%{transform:translate(-100%)}to{transform:translate(300%)}}.cdx-thumbnail{display:inline-flex}.cdx-thumbnail\_\_placeholder,.cdx-thumbnail\_\_image{background-position:center;background-repeat:no-repeat;background-size:cover;flex-shrink:0;box-sizing:border-box;min-width:40px;min-height:40px;width:2.5rem;height:2.5rem;border:1px solid var(--border-color-subtle,#c8ccd1);border-radius:2px}.cdx-thumbnail\_\_image{background-color:var(--background-color-base-fixed,#fff);display:inline-block}.cdx-thumbnail\_\_image-enter-active{transition-property:opacity;transition-duration:.1s}.cdx-thumbnail\_\_image-enter-from{opacity:0}.cdx-thumbnail\_\_placeholder{background-color:var(--background-color-interactive-subtle,#f8f9fa);display:inline-flex;align-items:center;justify-content:center}.cdx-thumbnail\_\_placeholder\_\_icon{min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not (((-webkit-mask-image:none) or (mask-image:none))){.cdx-thumbnail\_\_placeholder\_\_icon{background-position:center;background-repeat:no-repeat;background-size:max(calc(var(--font-size-medium,1rem) + 4px),10px)}}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-thumbnail\_\_placeholder\_\_icon{-webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:max(calc(var(--font-size-medium,1rem) + 4px),10px);mask-size:max(calc(var(--font-size-medium,1rem) + 4px),10px)}}@supports not (((-webkit-mask-image:none) or (mask-image:none))){.cdx-thumbnail\_\_placeholder\_\_icon{background-image:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="%23000"><path d="M19 3H1v14h18zM3 14l3.5-4.5 2.5 3L12.5 8l4.5 6z"/><path d="M19 5H1V3h18zm0 12H1v-2h18z"/></svg>');filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,.87)}}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-thumbnail\_\_placeholder\_\_icon{-webkit-mask-image:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="%23000"><path d="M19 3H1v14h18zM3 14l3.5-4.5 2.5 3L12.5 8l4.5 6z"/><path d="M19 5H1V3h18zm0 12H1v-2h18z"/></svg>');mask-image:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="%23000"><path d="M19 3H1v14h18zM3 14l3.5-4.5 2.5 3L12.5 8l4.5 6z"/><path d="M19 5H1V3h18zm0 12H1v-2h18z"/></svg>');background-color:var(--color-placeholder,#72777d)}}.cdx-thumbnail\_\_placeholder\_\_icon--vue.cdx-icon{color:var(--color-placeholder,#72777d)}.cdx-search-result-title{display:inline-block;max-width:100%;font-weight:700}.cdx-search-result-title\_\_match{font-weight:400}.cdx-menu-item{list-style:none;position:relative;padding:8px 12px;font-size:var(--font-size-medium,1rem);line-height:var(--line-height-small,1.375rem);transition-property:background-color,color,border-color,box-shadow;transition-duration:.1s}.cdx-menu-item\_\_content{display:flex;align-items:center;word-wrap:break-word}@supports (word-break:break-word){.cdx-menu-item\_\_content{word-wrap:unset;word-break:break-word}}@supports (overflow-wrap:anywhere){.cdx-menu-item\_\_content{word-break:normal;overflow-wrap:anywhere}}.cdx-menu-item\_\_content:lang(de),.cdx-menu-item\_\_content:lang(de-AT),.cdx-menu-item\_\_content:lang(de-CH),.cdx-menu-item\_\_content:lang(de-DE),.cdx-menu-item\_\_content:lang(de-LI),.cdx-menu-item\_\_content:lang(de-LU),.cdx-menu-item\_\_content:lang(de-x-formal){-webkit-hyphens:auto;hyphens:auto}.cdx-menu-item\_\_content,.cdx-menu-item\_\_content:hover{text-decoration:none}.cdx-menu-item--has-description .cdx-menu-item\_\_content{align-items:flex-start}.cdx-menu-item\_\_text{max-width:100%}.cdx-menu-item\_\_text\_\_description{display:block}.cdx-menu-item\_\_thumbnail.cdx-thumbnail{margin-right:8px}.cdx-menu-item\_\_icon{height:var(--line-height-small,1.375rem);margin-right:8px}.cdx-menu-item\_\_icon.cdx-icon{color:var(--color-subtle,#54595d)}.cdx-menu-item\_\_selected-icon{height:var(--line-height-small,1.375rem);margin-left:auto}.cdx-menu-item\_\_selected-icon.cdx-icon{color:inherit}.cdx-menu-item--bold-label .cdx-menu-item\_\_text\_\_label{font-weight:700}.cdx-menu-item--hide-description-overflow .cdx-menu-item\_\_text{overflow:hidden}.cdx-menu-item--hide-description-overflow .cdx-menu-item\_\_text\_\_description{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.cdx-menu-item--enabled,.cdx-menu-item--enabled .cdx-menu-item\_\_content{color:var(--color-base,#202122)}.cdx-menu-item--enabled .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--enabled .cdx-menu-item\_\_text\_\_description{color:var(--color-subtle,#54595d)}.cdx-menu-item--enabled.cdx-menu-item--highlighted{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);cursor:pointer}.cdx-menu-item--enabled.cdx-menu-item--active{background-color:var(--background-color-interactive-subtle--active,#dadde3)}.cdx-menu-item--enabled.cdx-menu-item--selected{background-color:var(--background-color-progressive-subtle,#e8eeff);color:var(--color-progressive,#36c)}.cdx-menu-item--enabled.cdx-menu-item--selected .cdx-menu-item\_\_content,.cdx-menu-item--enabled.cdx-menu-item--selected .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--enabled.cdx-menu-item--selected .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--enabled.cdx-menu-item--selected .cdx-menu-item\_\_icon{color:var(--color-progressive,#36c)}.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--highlighted{background-color:var(--background-color-progressive-subtle--hover,#d9e2ff)}.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--highlighted .cdx-menu-item\_\_content,.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--highlighted .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--highlighted .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--highlighted .cdx-menu-item\_\_icon{color:var(--color-progressive--hover,#3056a9)}.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--active{background-color:var(--background-color-progressive-subtle--active,#b6d4fb)}.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--active .cdx-menu-item\_\_content,.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--active .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--active .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--enabled.cdx-menu-item--selected.cdx-menu-item--active .cdx-menu-item\_\_icon{color:var(--color-progressive--active,#233566)}.cdx-menu-item--disabled{color:var(--color-disabled,#a2a9b1);cursor:default}.cdx-menu-item--disabled .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--disabled .cdx-menu-item\_\_icon{color:inherit}.cdx-menu-item--destructive .cdx-menu-item\_\_content,.cdx-menu-item--destructive .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--destructive .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--destructive .cdx-menu-item\_\_icon{color:var(--color-destructive,#bf3c2c)}.cdx-menu-item--destructive.cdx-menu-item--highlighted{background-color:var(--background-color-destructive-subtle--hover,#ffdad3)}.cdx-menu-item--destructive.cdx-menu-item--highlighted .cdx-menu-item\_\_content,.cdx-menu-item--destructive.cdx-menu-item--highlighted .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--destructive.cdx-menu-item--highlighted .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--destructive.cdx-menu-item--highlighted .cdx-menu-item\_\_icon{color:var(--color-destructive--hover,#9f3526)}.cdx-menu-item--destructive.cdx-menu-item--active{background-color:var(--background-color-destructive-subtle--active,#ffc8bd)}.cdx-menu-item--destructive.cdx-menu-item--active .cdx-menu-item\_\_content,.cdx-menu-item--destructive.cdx-menu-item--active .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--destructive.cdx-menu-item--active .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--destructive.cdx-menu-item--active .cdx-menu-item\_\_icon{color:var(--color-destructive--active,#612419)}.cdx-menu-item--destructive.cdx-menu-item--selected{background-color:var(--background-color-destructive-subtle,#ffe9e5);color:var(--color-destructive,#bf3c2c)}.cdx-menu-item--destructive.cdx-menu-item--selected .cdx-menu-item\_\_content,.cdx-menu-item--destructive.cdx-menu-item--selected .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--destructive.cdx-menu-item--selected .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--destructive.cdx-menu-item--selected .cdx-menu-item\_\_icon{color:var(--color-destructive,#bf3c2c)}.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--highlighted{background-color:var(--background-color-destructive-subtle--hover,#ffdad3)}.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--highlighted .cdx-menu-item\_\_content,.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--highlighted .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--highlighted .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--highlighted .cdx-menu-item\_\_icon{color:var(--color-destructive--hover,#9f3526)}.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--active{background-color:var(--background-color-destructive-subtle--active,#ffc8bd)}.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--active .cdx-menu-item\_\_content,.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--active .cdx-menu-item\_\_text\_\_supporting-text,.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--active .cdx-menu-item\_\_text\_\_description,.cdx-menu-item--destructive.cdx-menu-item--selected.cdx-menu-item--active .cdx-menu-item\_\_icon{color:var(--color-destructive--active,#612419)}.cdx-menu{background-color:var(--background-color-base,#fff);display:flex;flex-direction:column;position:absolute;left:0;z-index:50;box-sizing:border-box;width:100%;border:1px solid var(--border-color-base,#a2a9b1);border-radius:2px;box-shadow:0 4px 4px 0 var(--box-shadow-color-alpha-base,rgba(0,0,0,.06)),0 0 8px 0 var(--box-shadow-color-alpha-base,rgba(0,0,0,.06));font-size:var(--font-size-medium,1rem);line-height:var(--line-height-small,1.375rem)}.cdx-menu\_\_progress-bar.cdx-progress-bar{position:absolute;top:0}.cdx-menu\_\_listbox,.cdx-menu\_\_group{margin:0;padding:0}.cdx-menu\_\_listbox{overflow-y:auto}.cdx-menu\_\_group{display:flex;flex-direction:column}.cdx-menu\_\_group\_\_meta{display:flex;gap:8px;padding:8px 12px 6px}.cdx-menu\_\_group\_\_meta\_\_text{display:flex;flex-direction:column;font-size:var(--font-size-medium,1rem);line-height:var(--line-height-small,1.375rem)}.cdx-menu\_\_group\_\_icon{height:var(--line-height-small,1.375rem)}.cdx-menu\_\_group\_\_label{font-weight:700}.cdx-menu\_\_group\_\_description{color:var(--color-subtle,#54595d);font-size:var(--font-size-small,.875rem);line-height:var(--line-height-small,1.375rem)}.cdx-menu\_\_group-wrapper--hide-label .cdx-menu\_\_group\_\_meta{display:block;clip:rect(1px,1px,1px,1px);position:absolute!important;width:1px;height:1px;margin:-1px;border:0;padding:0;overflow:hidden}.cdx-menu\_\_group-wrapper+.cdx-menu-item,.cdx-menu-item+.cdx-menu\_\_group-wrapper,.cdx-menu\_\_group-wrapper--hide-label,.cdx-menu\_\_group-wrapper--hide-label+.cdx-menu\_\_group-wrapper{border-top:1px solid var(--border-color-muted,#dadde3)}.cdx-menu--has-footer .cdx-menu\_\_listbox>.cdx-menu-item:last-of-type{position:absolute;bottom:0;box-sizing:border-box;width:100%}.cdx-menu--has-footer .cdx-menu\_\_listbox>.cdx-menu-item:last-of-type:not(:first-of-type){border-top:1px solid var(--border-color-subtle,#c8ccd1)}.cdx-select{align-content:center;box-sizing:border-box;min-width:256px;min-height:32px;border-width:1px;border-style:solid;border-radius:2px;padding-top:4px;padding-bottom:4px;padding-left:8px;padding-right:calc(8px + 8px + calc(var(--font-size-medium,1rem) + 4px));font-size:var(--font-size-medium,1rem);line-height:1;-webkit-appearance:none;appearance:none;background-position:center right 12px;background-repeat:no-repeat;background-size:max(calc(var(--font-size-medium,1rem) - 4px),10px)}.cdx-select:disabled{background-color:var(--background-color-disabled-subtle,#eaecf0);color:var(--color-disabled,#a2a9b1);border-color:var(--border-color-disabled,#c8ccd1);background-image:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="%23a2a9b1"><path d="m17.5 4.75-7.5 7.5-7.5-7.5L1 6.25l9 9 9-9z"/></svg>');opacity:1}.cdx-select:enabled{background-color:var(--background-color-interactive-subtle,#f8f9fa);color:var(--color-subtle,#54595d);border-color:var(--border-color-interactive,#72777d);transition-property:background-color,color,border-color,box-shadow;transition-duration:.1s;background-image:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="%23202122"><path d="m17.5 4.75-7.5 7.5-7.5-7.5L1 6.25l9 9 9-9z"/></svg>')}.cdx-select:enabled:hover{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);border-color:var(--border-color-interactive--hover,#27292d);cursor:pointer}.cdx-select:enabled:active{background-color:var(--background-color-interactive-subtle--active,#dadde3);border-color:var(--border-color-interactive--active,#202122)}.cdx-select:enabled:focus:not(:active){background-color:var(--background-color-base,#fff);border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c);outline:1px solid transparent}.cdx-select-vue{display:inline-block;position:relative}.cdx-select-vue\_\_handle{align-content:center;box-sizing:border-box;min-width:256px;min-height:32px;border-width:1px;border-style:solid;border-radius:2px;padding-top:4px;padding-bottom:4px;padding-left:8px;padding-right:calc(8px + 8px + calc(var(--font-size-medium,1rem) + 4px));font-size:var(--font-size-medium,1rem);line-height:1;position:relative;width:100%}.cdx-select-vue--has-start-icon .cdx-select-vue\_\_handle{padding-left:calc(8px + 12px + calc(var(--font-size-medium,1rem) + 4px))}.cdx-select-vue\_\_start-icon.cdx-icon{color:var(--color-subtle,#54595d);position:absolute;top:50%;min-width:18px;min-height:18px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);transition-property:color;transition-duration:.1s;left:12px;transform:translateY(-50%)}.cdx-select-vue\_\_indicator.cdx-icon{color:var(--color-base,#202122);position:absolute;top:50%;min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) - 4px);height:calc(var(--font-size-medium,1rem) - 4px);transition-property:color;transition-duration:.1s;right:12px;transform:translateY(-50%)}.cdx-select-vue--enabled .cdx-select-vue\_\_handle{background-color:var(--background-color-interactive-subtle,#f8f9fa);color:var(--color-subtle,#54595d);border-color:var(--border-color-interactive,#72777d);transition-property:background-color,color,border-color,box-shadow;transition-duration:.1s}.cdx-select-vue--enabled .cdx-select-vue\_\_handle:hover{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);border-color:var(--border-color-interactive--hover,#27292d);cursor:pointer}.cdx-select-vue--enabled .cdx-select-vue\_\_handle:active{background-color:var(--background-color-interactive-subtle--active,#dadde3);border-color:var(--border-color-interactive--active,#202122)}.cdx-select-vue--enabled .cdx-select-vue\_\_handle:focus:not(:active){background-color:var(--background-color-base,#fff);border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c);outline:1px solid transparent}.cdx-select-vue--enabled.cdx-select-vue--value-selected .cdx-select-vue\_\_handle{color:var(--color-base,#202122)}.cdx-select-vue--enabled.cdx-select-vue--expanded .cdx-select-vue\_\_handle{background-color:var(--background-color-base,#fff)}.cdx-select-vue--disabled .cdx-select-vue\_\_handle{background-color:var(--background-color-disabled-subtle,#eaecf0);color:var(--color-disabled,#a2a9b1);border-color:var(--border-color-disabled,#c8ccd1);cursor:default}.cdx-select-vue--disabled .cdx-select-vue\_\_indicator,.cdx-select-vue--disabled .cdx-select-vue\_\_start-icon{color:var(--color-disabled,#a2a9b1)}.cdx-select-vue--status-error.cdx-select-vue--enabled .cdx-select-vue\_\_handle{background-color:var(--background-color-error-subtle,#ffe9e5);color:var(--color-error,#bf3c2c);border-color:var(--border-color-error,#f54739)}.cdx-select-vue--status-error.cdx-select-vue--enabled .cdx-select-vue\_\_handle .cdx-select-vue\_\_start-icon{color:var(--color-error,#bf3c2c)}.cdx-select-vue--status-error.cdx-select-vue--enabled .cdx-select-vue\_\_handle:hover:not(:focus){background-color:var(--background-color-error-subtle--hover,#ffdad3);color:var(--color-error--hover,#9f3526);border-color:var(--border-color-error--hover,#9f3526)}.cdx-select-vue--status-error.cdx-select-vue--enabled .cdx-select-vue\_\_handle:hover:not(:focus) .cdx-select-vue\_\_start-icon{color:var(--color-error--hover,#9f3526)}.cdx-select-vue--status-error.cdx-select-vue--enabled .cdx-select-vue\_\_handle:active{background-color:var(--background-color-error-subtle--active,#ffc8bd);color:var(--color-error--active,#612419);border-color:var(--border-color-error--active,#612419)}.cdx-select-vue--status-error.cdx-select-vue--enabled .cdx-select-vue\_\_handle:active .cdx-select-vue\_\_start-icon{color:var(--color-error--active,#612419)}.cdx-select-vue--status-error.cdx-select-vue--enabled .cdx-select-vue\_\_handle:focus:not(:active){color:var(--color-subtle,#54595d)}.cdx-select-vue--status-error.cdx-select-vue--enabled.cdx-select-vue--value-selected .cdx-select-vue\_\_handle:focus:not(:active){color:var(--color-base,#202122)}.cdx-select-vue--status-error.cdx-select-vue--enabled.cdx-select-vue--value-selected .cdx-select-vue\_\_handle:focus:not(:active) .cdx-select-vue\_\_start-icon{color:var(--color-base,#202122)}.cdx-scrollable-container .cdx-select-vue{position:static}.cdx-tab[aria-hidden=true]{display:none}.cdx-tab:focus{outline:1px solid transparent}.cdx-tabs\_\_header{display:flex;align-items:flex-end;position:relative}.cdx-tabs\_\_prev-scroller,.cdx-tabs\_\_next-scroller{background-color:inherit;position:absolute;top:0;bottom:0}.cdx-tabs\_\_prev-scroller{left:0}.cdx-tabs\_\_next-scroller{right:0}.cdx-tabs\_\_prev-scroller:after,.cdx-tabs\_\_next-scroller:before{content:"";position:absolute;top:0;z-index:1;width:1.5rem;height:100%;pointer-events:none}.cdx-tabs\_\_prev-scroller:after{left:100%}.cdx-tabs\_\_next-scroller:before{right:100%}.cdx-tabs\_\_scroll-button.cdx-button{height:100%}.cdx-tabs\_\_list{display:flex;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}.cdx-tabs\_\_list::-webkit-scrollbar{-webkit-appearance:none;display:none}.cdx-tabs\_\_list\_\_item{background-color:var(--background-color-transparent,transparent);display:block;flex:0 0 auto;max-width:16rem;border-width:0;border-top-left-radius:2px;border-top-right-radius:2px;padding:4px 12px;font-size:var(--font-size-medium,1rem);font-weight:700;line-height:var(--line-height-small,1.375rem);text-decoration:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;transition-property:background-color,color,border-color,box-shadow;transition-duration:.1s}.cdx-tabs\_\_list\_\_item:hover{cursor:pointer}.cdx-tabs\_\_list\_\_item[aria-selected=true]{cursor:default}.cdx-tabs>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item+.cdx-tabs\_\_list\_\_item{margin-left:0}.cdx-tabs--framed>.cdx-tabs\_\_header{background-color:var(--background-color-interactive,#eaecf0)}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_prev-scroller:after{background-image:linear-gradient(to right,var(--background-color-interactive,#eaecf0) 0,var(--background-color-transparent,transparent) 100%)}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_next-scroller:before{background-image:linear-gradient(to left,var(--background-color-interactive,#eaecf0) 0,var(--background-color-transparent,transparent) 100%)}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item{color:var(--color-base,#202122);margin:8px 4px 0 8px}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:enabled{overflow:hidden}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:enabled:hover{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);color:var(--color-base,#202122);mix-blend-mode:var(--mix-blend-mode-blend,multiply)}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:enabled:active{background-color:var(--background-color-interactive-subtle--active,#dadde3);color:var(--color-base,#202122)}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item[aria-selected=true],.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item[aria-selected=true]:hover{background-color:var(--background-color-base,#fff);color:var(--color-base,#202122);mix-blend-mode:var(--mix-blend-mode-base,normal)}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:disabled{background-color:var(--background-color-interactive,#eaecf0);color:var(--color-disabled,#a2a9b1);cursor:default}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:last-child{margin-right:8px}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header{background-color:var(--background-color-base,#fff);margin:0 4px;border-bottom:1px solid var(--border-color-base,#a2a9b1)}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_prev-scroller:after{background-image:linear-gradient(to right,var(--background-color-base,#fff) 0,var(--background-color-transparent,transparent) 100%)}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_next-scroller:before{background-image:linear-gradient(to left,var(--background-color-base,#fff) 0,var(--background-color-transparent,transparent) 100%)}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item{margin:0 2px}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:enabled{color:var(--color-base,#202122)}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:enabled:hover:not([aria-selected="true"]){color:var(--color-progressive--hover,#3056a9);box-shadow:inset 0 -2px 0 0 var(--box-shadow-color-progressive-selected--hover,#3056a9)}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:enabled:active:not([aria-selected="true"]){color:var(--color-progressive--active,#233566);box-shadow:inset 0 -2px 0 0 var(--box-shadow-color-progressive-selected--active,#233566)}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item[aria-selected=true]{color:var(--color-progressive,#36c);box-shadow:inset 0 -2px 0 0 var(--box-shadow-color-progressive-selected,#36c)}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item[aria-selected=true]:hover{color:var(--color-progressive,#36c)}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:disabled{color:var(--color-disabled,#a2a9b1);cursor:default}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:first-child{margin-left:0}.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:last-child{margin-right:0}.cdx-tabs--framed>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:focus-visible,.cdx-tabs:not(.cdx-tabs--framed)>.cdx-tabs\_\_header .cdx-tabs\_\_list\_\_item:focus-visible{box-shadow:inset 0 0 0 2px var(--border-color-progressive,#6485d1);outline:1px solid transparent;overflow:hidden}.cdx-text-input{position:relative;box-sizing:border-box;min-width:256px;border-radius:2px;overflow:hidden}.cdx-text-input .cdx-text-input\_\_start-icon{position:absolute;top:50%;min-width:18px;min-height:18px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);transition-property:color;transition-duration:.1s;left:9px;transform:translateY(-50%)}.cdx-text-input\_\_icon.cdx-text-input\_\_end-icon{min-width:10px;min-height:10px;width:var(--font-size-medium,1rem);height:var(--font-size-medium,1rem)}@supports not (((-webkit-mask-image:none) or (mask-image:none))){.cdx-text-input\_\_icon.cdx-text-input\_\_end-icon{background-position:center;background-repeat:no-repeat;background-size:max(var(--font-size-medium,1rem),10px)}}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-text-input\_\_icon.cdx-text-input\_\_end-icon{-webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:max(var(--font-size-medium,1rem),10px);mask-size:max(var(--font-size-medium,1rem),10px)}}.cdx-text-input\_\_clear-icon.cdx-icon,.cdx-text-input .cdx-text-input\_\_end-icon{position:absolute;top:50%;min-width:14px;min-height:14px;width:var(--font-size-medium,1rem);height:var(--font-size-medium,1rem);transition-property:color;transition-duration:.1s;right:9px;transform:translateY(-50%)}.cdx-text-input\_\_clear-icon.cdx-icon:hover{cursor:pointer}.cdx-text-input\_\_end-icon.cdx-icon+.cdx-text-input\_\_clear-icon.cdx-icon{right:calc(calc(8px \* 2 + var(--font-size-medium,1rem)) + 1px)}.cdx-text-input\_\_input{display:block;box-sizing:border-box;min-height:32px;width:100%;max-height:2rem;margin:0;border-width:1px;border-style:solid;border-radius:0;padding:4px 8px;font-family:inherit;font-size:var(--font-size-medium,1rem);line-height:var(--line-height-small,1.375rem)}.cdx-text-input\_\_input:enabled{background-color:var(--background-color-base,#fff);color:var(--color-base,#202122);border-color:var(--border-color-interactive,#72777d);box-shadow:inset 0 0 0 1px var(--box-shadow-color-transparent,transparent);transition-property:background-color,color,border-color,box-shadow;transition-duration:.25s}.cdx-text-input\_\_input:enabled~.cdx-text-input\_\_icon-vue{color:var(--color-placeholder,#72777d)}.cdx-text-input\_\_input:enabled~.cdx-text-input\_\_icon{opacity:var(--opacity-icon-placeholder,.51)}.cdx-text-input\_\_input:enabled:hover{border-color:var(--border-color-interactive--hover,#27292d)}.cdx-text-input\_\_input:enabled:focus~.cdx-text-input\_\_icon-vue,.cdx-text-input\_\_input:enabled.cdx-text-input\_\_input--has-value~.cdx-text-input\_\_icon-vue{color:var(--color-subtle,#54595d)}.cdx-text-input\_\_input:enabled:focus~.cdx-text-input\_\_clear-icon,.cdx-text-input\_\_input:enabled.cdx-text-input\_\_input--has-value~.cdx-text-input\_\_clear-icon{color:var(--color-base,#202122)}.cdx-text-input\_\_input:enabled:focus~.cdx-text-input\_\_icon,.cdx-text-input\_\_input:enabled.cdx-text-input\_\_input--has-value~.cdx-text-input\_\_icon{opacity:1}.cdx-text-input\_\_input:enabled:focus{border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c);outline:1px solid transparent}.cdx-text-input\_\_input:enabled:read-only{background-color:var(--background-color-neutral-subtle,#f8f9fa);border-color:var(--border-color-base,#a2a9b1)}.cdx-text-input\_\_input:disabled{background-color:var(--background-color-disabled-subtle,#eaecf0);color:var(--color-disabled,#a2a9b1);-webkit-text-fill-color:var(--color-disabled,#a2a9b1);border-color:var(--border-color-disabled,#c8ccd1)}.cdx-text-input\_\_input:disabled~.cdx-text-input\_\_icon-vue{color:var(--color-disabled,#a2a9b1);pointer-events:none}.cdx-text-input\_\_input:disabled~.cdx-text-input\_\_icon{opacity:var(--opacity-icon-base--disabled,.51)}.cdx-text-input\_\_input::placeholder{color:var(--color-placeholder,#72777d);opacity:1}.cdx-text-input\_\_input[type=search]{-webkit-appearance:none;-moz-appearance:textfield}.cdx-text-input\_\_input[type=search]::-webkit-search-decoration,.cdx-text-input\_\_input[type=search]::-webkit-search-cancel-button{display:none}.cdx-text-input--has-start-icon .cdx-text-input\_\_input{padding-left:calc(8px + 8px + calc(var(--font-size-medium,1rem) + 4px))}.cdx-text-input--has-end-icon .cdx-text-input\_\_input,.cdx-text-input--clearable .cdx-text-input\_\_input{padding-right:calc(8px + 8px + var(--font-size-medium,1rem))}.cdx-text-input--has-end-icon.cdx-text-input--clearable .cdx-text-input\_\_input{padding-right:calc(8px + calc(8px \* 2 + var(--font-size-medium,1rem)) + var(--font-size-medium,1rem))}.cdx-text-input--status-error .cdx-text-input\_\_input:enabled:not(:read-only):not(:focus){background-color:var(--background-color-error-subtle,#ffe9e5);color:var(--color-error,#bf3c2c);border-color:var(--border-color-error,#f54739)}.cdx-text-input--status-error .cdx-text-input\_\_input:enabled:not(:read-only):not(:focus)::placeholder,.cdx-text-input--status-error .cdx-text-input\_\_input:enabled:not(:read-only):not(:focus)~.cdx-text-input\_\_start-icon,.cdx-text-input--status-error .cdx-text-input\_\_input:enabled:not(:read-only):not(:focus)~.cdx-text-input\_\_end-icon{color:var(--color-error,#bf3c2c)}.cdx-text-input--status-error .cdx-text-input\_\_input:enabled:not(:read-only):not(:focus):hover{background-color:var(--background-color-error-subtle--hover,#ffdad3);color:var(--color-error--hover,#9f3526);border-color:var(--border-color-error--hover,#9f3526)}.cdx-text-input--status-error .cdx-text-input\_\_input:enabled:not(:read-only):not(:focus):hover::placeholder,.cdx-text-input--status-error .cdx-text-input\_\_input:enabled:not(:read-only):not(:focus):hover~.cdx-text-input\_\_start-icon,.cdx-text-input--status-error .cdx-text-input\_\_input:enabled:not(:read-only):not(:focus):hover~.cdx-text-input\_\_end-icon{color:var(--color-error--hover,#9f3526)}
.ve-init-mw-progressBarWidget{height:1em;overflow:hidden;margin:0 25%}.ve-init-mw-progressBarWidget-bar{height:1em;width:0} .ve-init-mw-progressBarWidget{background-color:#fff;box-sizing:border-box;height:0.875em;border:1px solid #36c;border-radius:0.875em;box-shadow:0 1px 1px rgba(0,0,0,0.15)}.ve-init-mw-progressBarWidget-bar{background-color:#36c;height:0.875em}
.rt-overlay{position:absolute;width:100%;font-size:calc(var(--font-size-medium,1rem) \* (13 / 14));line-height:1.5em; z-index:800; top:0} .skin-vector-legacy .rt-overlay{font-size:13px}.skin-monobook .rt-overlay{font-size:12.7px}.rt-tooltip{position:absolute;max-width:27em;background:var(--background-color-base,#fff);color:var(--color-base,#202122);border:1px solid var(--border-color-subtle,#c8ccd1);border-radius:2px;box-shadow:0 20px 48px 0 rgba(0,0,0,0.2)}html.skin-theme-clientpref-night .rt-tooltip{box-shadow:0 20px 48px 0 rgba(0,0,0,1)} .rt-tooltip-above .rt-hoverArea{margin-bottom:-0.6em;padding-bottom:0.6em}.rt-tooltip-below .rt-hoverArea{margin-top:-0.7em;padding-top:0.7em}.rt-scroll{overflow-x:auto}.rt-content{padding:0.7em 0.9em;overflow-wrap:break-word}.rt-tail{ background:linear-gradient(to top right,var(--border-color-subtle,#c8ccd1) 48%,rgba(0,0,0,0) 48%);--tail-left:19px;--tail-side-width:13px}.rt-tail,.rt-tail:after{position:absolute; z-index:-1;width:var(--tail-side-width);height:var(--tail-side-width)}.rt-tail:after{content:'';background:var(--background-color-base,#fff);bottom:1px;left:1px}.rt-tooltip-above .rt-tail{transform:rotate(-45deg);transform-origin:100% 100%;bottom:0;left:var(--tail-left)}.rt-tooltip-below .rt-tail{transform:rotate(135deg);transform-origin:0 0;top:0;left:calc(var(--tail-left) + var(--tail-side-width))}.rt-settingsLink{background-image:url(data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2024%22%3E%0D%0A%20%20%20%20%3Cpath%20fill%3D%22%2354595d%22%20d%3D%22M20%2014.5v-2.9l-1.8-.3c-.1-.4-.3-.8-.6-1.4l1.1-1.5-2.1-2.1-1.5%201.1c-.5-.3-1-.5-1.4-.6L13.5%205h-2.9l-.3%201.8c-.5.1-.9.3-1.4.6L7.4%206.3%205.3%208.4l1%201.5c-.3.5-.4.9-.6%201.4l-1.7.2v2.9l1.8.3c.1.5.3.9.6%201.4l-1%201.5%202.1%202.1%201.5-1c.4.2.9.4%201.4.6l.3%201.8h3l.3-1.8c.5-.1.9-.3%201.4-.6l1.5%201.1%202.1-2.1-1.1-1.5c.3-.5.5-1%20.6-1.4l1.5-.3zM12%2016c-1.7%200-3-1.3-3-3s1.3-3%203-3%203%201.3%203%203-1.3%203-3%203z%22%2F%3E%0D%0A%3C%2Fsvg%3E);float:right;margin:-0.5em -0.5em 0 0.5em;box-sizing:border-box;height:32px;width:32px;border:1px solid transparent;border-radius:2px;background-position:center center;background-repeat:no-repeat;background-size:24px 24px}html.skin-theme-clientpref-night .rt-settingsLink{background-image:url(data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2024%22%3E%0D%0A%20%20%20%20%3Cpath%20fill%3D%22%23c8ccd1%22%20d%3D%22M20%2014.5v-2.9l-1.8-.3c-.1-.4-.3-.8-.6-1.4l1.1-1.5-2.1-2.1-1.5%201.1c-.5-.3-1-.5-1.4-.6L13.5%205h-2.9l-.3%201.8c-.5.1-.9.3-1.4.6L7.4%206.3%205.3%208.4l1%201.5c-.3.5-.4.9-.6%201.4l-1.7.2v2.9l1.8.3c.1.5.3.9.6%201.4l-1%201.5%202.1%202.1%201.5-1c.4.2.9.4%201.4.6l.3%201.8h3l.3-1.8c.5-.1.9-.3%201.4-.6l1.5%201.1%202.1-2.1-1.1-1.5c.3-.5.5-1%20.6-1.4l1.5-.3zM12%2016c-1.7%200-3-1.3-3-3s1.3-3%203-3%203%201.3%203%203-1.3%203-3%203z%22%2F%3E%0D%0A%3C%2Fsvg%3E)}.rt-settingsLink:hover,.rt-settingsLink:active{background-color:var(--background-color-interactive,#eaecf0)}.rt-settingsLink:active{border-color:var(--border-color-interactive,#72777d)}.rt-settingsLink:focus{outline:1px solid transparent}.rt-settingsLink:focus:not(:active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c)}.rt-target{background-color:var(--background-color-progressive-subtle,#eaf3ff)}.rt-enableField{font-weight:bold;margin-bottom:1.25em}.rt-numberInput.rt-numberInput{width:10em}.rt-tooltipsForCommentsField.rt-tooltipsForCommentsField.rt-tooltipsForCommentsField{margin-top:1.25em}.rt-disabledHelp{border-collapse:collapse}.rt-disabledHelp td{padding:0}.rt-disabledNote.rt-disabledNote{vertical-align:bottom;padding-left:0.36em;font-weight:bold}@keyframes rt-fade-in-up{0%{opacity:0;transform:translate(0,20px)}100%{opacity:1;transform:translate(0,0)}}@keyframes rt-fade-in-down{0%{opacity:0;transform:translate(0,-20px)}100%{opacity:1;transform:translate(0,0)}}@keyframes rt-fade-out-down{0%{opacity:1;transform:translate(0,0)}100%{opacity:0;transform:translate(0,20px)}}@keyframes rt-fade-out-up{0%{opacity:1;transform:translate(0,0)}100%{opacity:0;transform:translate(0,-20px)}}.rt-fade-in-up{animation:rt-fade-in-up 0.2s ease forwards}.rt-fade-in-down{animation:rt-fade-in-down 0.2s ease forwards}.rt-fade-out-down{animation:rt-fade-out-down 0.2s ease forwards}.rt-fade-out-up{animation:rt-fade-out-up 0.2s ease forwards}
.mw-collapsible-toggle{float:right;-webkit-user-select:none;-moz-user-select:none;user-select:none}.mw-collapsible-toggle-default{-webkit-appearance:none;-moz-appearance:none;appearance:none;background:none;margin:0;padding:0;border:0;font:inherit}.mw-collapsible-toggle-default .mw-collapsible-text{color:var(--color-progressive,#36c);border-radius:2px;text-decoration:none; }.mw-collapsible-toggle-default .mw-collapsible-text:visited{color:var(--color-visited,#6a60b0)}.mw-collapsible-toggle-default .mw-collapsible-text:visited:hover{color:var(--color-visited--hover,#534fa3)}.mw-collapsible-toggle-default .mw-collapsible-text:visited:active{color:var(--color-visited--active,#353262)}.mw-collapsible-toggle-default .mw-collapsible-text:hover{color:var(--color-progressive--hover,#3056a9);text-decoration:underline}.mw-collapsible-toggle-default .mw-collapsible-text:active{color:var(--color-progressive--active,#233566);text-decoration:underline}.mw-collapsible-toggle-default .mw-collapsible-text:focus-visible{outline:solid 2px var(--outline-color-progressive--focus,#36c)}@supports not selector(:focus-visible){.mw-collapsible-toggle-default .mw-collapsible-text:focus{outline:solid 2px var(--outline-color-progressive--focus,#36c)}}.mw-collapsible-toggle-default .mw-collapsible-text .cdx-icon:not(.cdx-thumbnail\_\_placeholder\_\_icon--vue):last-child{min-width:10px;min-height:10px;width:var(--font-size-medium,1rem);height:var(--font-size-medium,1rem);padding-left:4px;vertical-align:middle}.mw-underline-always .mw-collapsible-toggle-default .mw-collapsible-text{text-decoration:underline}.mw-underline-never .mw-collapsible-toggle-default .mw-collapsible-text{text-decoration:none}.mw-collapsible-toggle-default::before{content:'['}.mw-collapsible-toggle-default::after{content:']'}.mw-customtoggle,.mw-collapsible-toggle{cursor:pointer} caption .mw-collapsible-toggle,.mw-content-ltr caption .mw-collapsible-toggle,.mw-content-rtl caption .mw-collapsible-toggle,.mw-content-rtl .mw-content-ltr caption .mw-collapsible-toggle,.mw-content-ltr .mw-content-rtl caption .mw-collapsible-toggle{float:none}.mw-collapsible[hidden='until-found'],.mw-collapsible [hidden='until-found']{display:block;position:absolute; width:0 !important;height:0 !important;overflow:hidden !important;padding:0 !important;margin:0 !important;border:0 !important; }.wikitable.mw-collapsed{border:0}
@keyframes centralAuthPPersonalAnimation{0%{opacity:0;transform:translateY(-20px)}100%{opacity:1;transform:translateY(0)}}.centralAuthPPersonalAnimation{animation-duration:1s;animation-fill-mode:both;animation-name:centralAuthPPersonalAnimation}
.mw-file-element:not([srcset]),.mw-file-element--updated{object-fit:scale-down} #mw-teleport-target{position:absolute;z-index:450} #mw-teleport-target{font-size:var(--font-size-small,0.875rem)}
#vector-appearance form{font-size:0.875rem;padding:6px 0}#vector-appearance a.skin-theme-beta-notice-success{color:var(--color-success,#177860);pointer-events:none}#vector-appearance .vector-icon.vector-icon--heart{ min-width:10px;min-height:10px;width:var(--font-size-medium,1rem);height:var(--font-size-medium,1rem);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){#vector-appearance .vector-icon.vector-icon--heart{background-position:center;background-repeat:no-repeat; background-size:calc(max(var(--font-size-medium,1rem),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){#vector-appearance .vector-icon.vector-icon--heart{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(var(--font-size-medium,1rem),10px));mask-size:calc(max(var(--font-size-medium,1rem),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){#vector-appearance .vector-icon.vector-icon--heart{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M14.75 1A5.24 5.24 0 0010 4 5.24 5.24 0 000 6.25C0 11.75 10 19 10 19s10-7.25 10-12.75A5.25 5.25 0 0014.75 1\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){#vector-appearance .vector-icon.vector-icon--heart{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M14.75 1A5.24 5.24 0 0010 4 5.24 5.24 0 000 6.25C0 11.75 10 19 10 19s10-7.25 10-12.75A5.25 5.25 0 0014.75 1\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M14.75 1A5.24 5.24 0 0010 4 5.24 5.24 0 000 6.25C0 11.75 10 19 10 19s10-7.25 10-12.75A5.25 5.25 0 0014.75 1\"/></svg>");background-color:var(--color-success,#177860)}}#skin-theme-beta-notice{display:none}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os #skin-theme-beta-notice{display:block}}html.skin-theme-clientpref-night #skin-theme-beta-notice{display:block}
.uls-menu{border-radius:2px; font-size:medium}.uls-search,.uls-language-settings-close-block{border-top-right-radius:2px;border-top-left-radius:2px}.uls-language-list{border-bottom-right-radius:2px;border-bottom-left-radius:2px}.uls-menu.callout::before,.uls-menu.callout::after{border-top:10px solid var(--border-color-transparent,transparent);border-bottom:10px solid var(--border-color-transparent,transparent);display:inline-block; top:17px;position:absolute;content:''}.uls-menu.callout.selector-right::before{ border-left:10px solid var(--border-color-subtle,#c8ccd1); right:-11px}.uls-menu.callout.selector-right::after{ border-left:10px solid var(--border-color-inverted,#fff); right:-10px}.uls-menu.callout.selector-left::before{ border-right:10px solid var(--border-color-subtle,#c8ccd1); left:-11px}.uls-menu.callout.selector-left::after{ border-right:10px solid var(--border-color-inverted,#fff); left:-10px}.uls-ui-languages button{margin:5px 15px 5px 0;white-space:nowrap;overflow:hidden}.uls-search-wrapper-wrapper{position:relative;padding-left:40px;margin-top:5px;margin-bottom:5px}.uls-icon-back{background:transparent url(/w/extensions/UniversalLanguageSelector/resources/images/back-grey-ltr.svg?c9c25) no-repeat scroll center center;background-size:28px;height:32px;width:40px;display:block;position:absolute;left:0;border-right:1px solid var(--border-color-subtle,#c8ccd1);opacity:var(--opacity-icon-base,0.87)}.uls-icon-back:hover{opacity:1;cursor:pointer}.uls-menu .uls-no-results-view .uls-no-found-more{background-color:var(--background-color-base,#fff)}.uls-menu .uls-no-results-view h3{padding:0 28px;margin:0;color:var(--color-subtle,#54595d);font-size:1em;font-weight:normal} .skin-vector .uls-menu{border-color:var(--border-color-subtle,#c8ccd1);box-shadow:0 4px 4px 0 var(--box-shadow-color-alpha-base,rgba(0,0,0,0.06)),0 0 8px 0 var(--box-shadow-color-alpha-base,rgba(0,0,0,0.06));font-size:0.875em;z-index:50}.skin-vector .uls-search{border-bottom-color:var(--border-color-subtle,#c8ccd1)}.skin-vector .uls-search-label{opacity:var(--opacity-icon-placeholder,0.51);transition:opacity 250ms}.skin-vector .uls-search-wrapper:hover .uls-search-label{opacity:var(--opacity-icon-base,0.87)}.skin-vector .uls-languagefilter,.skin-vector .uls-lcd-region-title{color:var(--color-subtle,#54595d)}.skin-vector .uls-filtersuggestion{color:var(--color-placeholder,#72777d)}
#parsermigration-survey-placeholder .ext-quick-survey-panel{width:100%;clear:both;float:none;margin:50px auto 0}
@media print{#centralNotice{display:none}}.cn-closeButton{display:inline-block;background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUBAMAAAB/pwA+AAAAElBMVEUAAAAQEBDPz88AAABAQEDv7+9oe1vvAAAABnRSTlMA3rLe3rJS22KzAAAARElEQVQI12PAAUIUQCSTK5BwFgIxFU1AhKECUFAYKAAioXwwBeZChMGCEGGQIFQYJohgIhQgtCEMQ7ECYTHCOciOxA4AADgJTXIb9s8AAAAASUVORK5CYII=) no-repeat;width:20px;height:20px;text-indent:20px;white-space:nowrap;overflow:hidden}
#uls-settings-block{background-color:#fcfcfc}#uls-settings-block.uls-settings-block--vector-2022{display:flex;justify-content:space-between;padding:8px 12px}#uls-settings-block.uls-settings-block--vector-2022.row::before,#uls-settings-block.uls-settings-block--vector-2022.row::after{content:none}#uls-settings-block.uls-settings-block--vector-2022.uls-settings-block--with-add-languages{background-color:#f8f9fa;border-top:1px solid var(--border-color-subtle,#c8ccd1)}#uls-settings-block.uls-settings-block--vector-2022 > button.uls-add-languages-button{background:transparent url(/w/extensions/UniversalLanguageSelector/resources/images/add.svg?3165e) no-repeat left center;margin-right:32px;padding-left:32px}#uls-settings-block.uls-settings-block--vector-2022 > button.uls-language-settings-button{background:transparent url(/w/extensions/UniversalLanguageSelector/resources/images/cog.svg?ce0b4) no-repeat center;margin-left:auto;border:0;min-height:20px;min-width:20px}#uls-settings-block:not(.uls-settings-block--vector-2022){background-color:#f8f9fa;border-top:1px solid var(--border-color-subtle,#c8ccd1);padding-left:10px;line-height:1.2em;border-radius:0 0 2px 2px}#uls-settings-block:not(.uls-settings-block--vector-2022) > button{background:left top transparent no-repeat;background-size:20px auto;color:var(--color-subtle,#54595d);display:inline-block;margin:8px 15px;border:0;padding:0 0 0 26px;font-size:medium;cursor:pointer}#uls-settings-block:not(.uls-settings-block--vector-2022) > button:hover{color:#202122}#uls-settings-block:not(.uls-settings-block--vector-2022) > button.display-settings-block{background-image:url(/w/extensions/UniversalLanguageSelector/resources/images/display.svg?9fd85)}#uls-settings-block:not(.uls-settings-block--vector-2022) > button.input-settings-block{background-image:url(/w/extensions/UniversalLanguageSelector/resources/images/input.svg?60384)}.uls-tipsy.uls-tipsy{z-index:1000}.uls-empty-state{padding:28px}.uls-empty-state .uls-empty-state\_\_header,.uls-empty-state .uls-empty-state\_\_desc{color:var(--color-subtle,#54595d)}.uls-empty-state .uls-language-action-items{list-style:none;margin:1em 0}.empty-language-selector\_\_language-settings-button{margin:12px} .uls-menu.uls-language-actions-dialog{min-width:248px}.uls-menu.uls-language-actions-dialog .uls-language-actions-title{border-bottom:1px solid var(--border-color-subtle,#c8ccd1);display:flex;align-items:center;height:32px;padding:5px 0}.uls-menu.uls-language-actions-dialog .uls-language-actions-title .uls-language-actions-close{min-width:unset;width:44px;background:transparent url(/w/extensions/UniversalLanguageSelector/resources/images/arrow-previous-ltr.svg?279af) no-repeat center}.uls-menu.uls-language-actions-dialog .uls-language-action-items .uls-language-action.oo-ui-widget{margin:0;padding:12px 8px;display:block}.uls-menu.uls-language-actions-dialog .uls-language-action-items .uls-language-action.oo-ui-widget .oo-ui-buttonElement-button{padding-left:36px}.cdx-button{display:inline-flex;align-items:center;justify-content:center;gap:6px;box-sizing:border-box;min-height:32px;max-width:28rem;margin:0;border-width:1px;border-style:solid;border-radius:2px;padding-right:11px;padding-left:11px;font-family:inherit;font-size:var(--font-size-medium,1rem);font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-transform:none;transition-property:background-color,color,border-color,box-shadow;transition-duration:.1s}.cdx-button--size-small{gap:4px;min-height:1.5rem;padding-right:5px;padding-left:5px}.cdx-button--size-large{min-height:44px;padding-right:15px;padding-left:15px}.cdx-button--icon-only{min-width:32px;padding-right:0;padding-left:0}.cdx-button--icon-only.cdx-button--size-small{min-width:1.5rem}.cdx-button--icon-only.cdx-button--size-large{min-width:44px}.cdx-button::-moz-focus-inner{border:0;padding:0}.cdx-button .cdx-button\_\_icon,.cdx-button .cdx-icon{vertical-align:middle}.cdx-button .cdx-icon{color:inherit}.cdx-button--fake-button,.cdx-button--fake-button:hover,.cdx-button--fake-button:focus{text-decoration:none}.cdx-button:enabled,.cdx-button.cdx-button--fake-button--enabled{background-color:var(--background-color-interactive-subtle,#f8f9fa);color:var(--color-neutral,#404244);border-color:var(--border-color-interactive,#72777d)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled .cdx-button\_\_icon{background-color:var(--color-neutral,#404244)}}.cdx-button:enabled:hover,.cdx-button.cdx-button--fake-button--enabled:hover{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);border-color:var(--border-color-interactive--hover,#27292d);cursor:pointer}.cdx-button:enabled:active,.cdx-button.cdx-button--fake-button--enabled:active,.cdx-button:enabled.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--is-active{background-color:var(--background-color-interactive-subtle--active,#dadde3);border-color:var(--border-color-interactive--active,#202122)}.cdx-button:enabled:focus,.cdx-button.cdx-button--fake-button--enabled:focus{outline:1px solid transparent}.cdx-button:enabled:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c)}.cdx-button:enabled.cdx-button--action-progressive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive{background-color:var(--background-color-progressive-subtle,#e8eeff);color:var(--color-progressive,#36c);border-color:var(--border-color-progressive,#6485d1)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-progressive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive .cdx-button\_\_icon{background-color:var(--color-progressive,#36c)}}.cdx-button:enabled.cdx-button--action-progressive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:hover{background-color:var(--background-color-progressive-subtle--hover,#d9e2ff);color:var(--color-progressive--hover,#3056a9);border-color:var(--border-color-progressive--hover,#3056a9)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-progressive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:hover .cdx-button\_\_icon{background-color:var(--color-progressive--hover,#3056a9)}}.cdx-button:enabled.cdx-button--action-progressive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:active,.cdx-button:enabled.cdx-button--action-progressive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive.cdx-button--is-active{background-color:var(--background-color-progressive-subtle--active,#b6d4fb);color:var(--color-progressive--active,#233566);border-color:var(--border-color-progressive--active,#233566)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-progressive--active,#233566)}}.cdx-button:enabled.cdx-button--action-destructive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive{background-color:var(--background-color-destructive-subtle,#ffe9e5);color:var(--color-destructive,#bf3c2c);border-color:var(--border-color-destructive,#f54739)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-destructive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive .cdx-button\_\_icon{background-color:var(--color-destructive,#bf3c2c)}}.cdx-button:enabled.cdx-button--action-destructive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:hover{background-color:var(--background-color-destructive-subtle--hover,#ffdad3);color:var(--color-destructive--hover,#9f3526);border-color:var(--border-color-destructive--hover,#9f3526)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-destructive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:hover .cdx-button\_\_icon{background-color:var(--color-destructive--hover,#9f3526)}}.cdx-button:enabled.cdx-button--action-destructive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:active,.cdx-button:enabled.cdx-button--action-destructive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive.cdx-button--is-active{background-color:var(--background-color-destructive-subtle--active,#ffc8bd);color:var(--color-destructive--active,#612419);border-color:var(--border-color-destructive--active,#612419)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-destructive--active,#612419)}}.cdx-button:enabled.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-destructive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-destructive--focus,#36c)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive{background-color:var(--background-color-progressive,#36c);color:var(--color-inverted-fixed,#fff);border-color:var(--border-color-transparent,transparent)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive:hover{background-color:var(--background-color-progressive--hover,#3056a9)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive:active,.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive.cdx-button--is-active{background-color:var(--background-color-progressive--active,#233566)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c),inset 0 0 0 2px var(--box-shadow-color-inverted,#fff)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive .cdx-button\_\_icon{background-color:var(--color-inverted-fixed,#fff)}}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive{background-color:var(--background-color-destructive,#bf3c2c);color:var(--color-inverted-fixed,#fff);border-color:var(--border-color-transparent,transparent)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive:hover{background-color:var(--background-color-destructive--hover,#9f3526)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive:active,.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive.cdx-button--is-active{background-color:var(--background-color-destructive--active,#612419)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-destructive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-destructive--focus,#36c),inset 0 0 0 2px var(--box-shadow-color-inverted,#fff)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive .cdx-button\_\_icon{background-color:var(--color-inverted-fixed,#fff)}}.cdx-button:enabled.cdx-button--weight-quiet,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet{background-color:var(--background-color-transparent,transparent);border-color:var(--border-color-transparent,transparent)}.cdx-button:enabled.cdx-button--weight-quiet:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet:hover{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);mix-blend-mode:var(--mix-blend-mode-blend,multiply)}.cdx-button:enabled.cdx-button--weight-quiet:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet:active,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--is-active{background-color:var(--background-color-interactive-subtle--active,#dadde3)}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive{color:var(--color-progressive,#36c)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive .cdx-button\_\_icon{background-color:var(--color-progressive,#36c)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover{background-color:var(--background-color-progressive-subtle--hover,#d9e2ff);color:var(--color-progressive--hover,#3056a9);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover .cdx-button\_\_icon{background-color:var(--color-progressive--hover,#3056a9)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active{background-color:var(--background-color-progressive-subtle--active,#b6d4fb);color:var(--color-progressive--active,#233566);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-progressive--active,#233566)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c)}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive{color:var(--color-destructive,#bf3c2c)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive .cdx-button\_\_icon{background-color:var(--color-destructive,#bf3c2c)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover{background-color:var(--background-color-destructive-subtle--hover,#ffdad3);color:var(--color-destructive--hover,#9f3526);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover .cdx-button\_\_icon{background-color:var(--color-destructive--hover,#9f3526)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active{background-color:var(--background-color-destructive-subtle--active,#ffc8bd);color:var(--color-destructive--active,#612419);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-destructive--active,#612419)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-destructive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-destructive--focus,#36c)}.cdx-button:disabled,.cdx-button.cdx-button--fake-button--disabled{background-color:var(--background-color-disabled,#dadde3);color:var(--color-disabled-emphasized,#a2a9b1);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:disabled .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--disabled .cdx-button\_\_icon{background-color:var(--color-inverted,#fff)}}.cdx-button:disabled.cdx-button--weight-quiet,.cdx-button.cdx-button--fake-button--disabled.cdx-button--weight-quiet{background-color:var(--background-color-transparent,transparent);color:var(--color-disabled,#a2a9b1)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:disabled.cdx-button--weight-quiet .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--disabled.cdx-button--weight-quiet .cdx-button\_\_icon{background-color:var(--color-disabled,#a2a9b1)}}.mw-interlanguage-selector-disabled #p-lang-btn-sticky-header{display:none}
.mw-ui-icon-wikimedia-expand{ width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) - 4px);height:calc(var(--font-size-medium,1rem) - 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.mw-ui-icon-wikimedia-expand{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.mw-ui-icon-wikimedia-expand{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.mw-ui-icon-wikimedia-expand{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"m17.5 4.75-7.5 7.5-7.5-7.5L1 6.25l9 9 9-9z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.mw-ui-icon-wikimedia-expand{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"m17.5 4.75-7.5 7.5-7.5-7.5L1 6.25l9 9 9-9z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"m17.5 4.75-7.5 7.5-7.5-7.5L1 6.25l9 9 9-9z\"/></svg>");background-color:var(--color-base,#202122)}}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.mw-ui-icon-wikimedia-expand{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) - 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.mw-ui-icon-wikimedia-expand{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) - 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) - 4px),10px)); }}.vector-popup-notification{font-size:var(--font-size-small,0.875rem)}.vector-popup-notification p{margin:0}.vector-popup-notification p:last-child{padding-bottom:0} .vector-sticky-header-container{position:fixed;top:0;left:0;right:0;z-index:3;transition:transform 250ms linear;display:none;transform:translateY(-100%);opacity:0}.vector-sticky-header{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--background-color-interactive,#eaecf0)}.vector-sticky-header-start,.vector-sticky-header-end,.vector-sticky-header-icons,.vector-sticky-header-buttons,.vector-sticky-header-context-bar{display:flex;align-items:center}.vector-sticky-header-start{flex-grow:1;min-width:0}.vector-sticky-header-context-bar-primary,.vector-sticky-header-end{white-space:nowrap}.vector-sticky-header-icon-start{border-right:1px solid var(--border-color-subtle,#c8ccd1);margin-right:calc(20px - 8px);padding-right:20px}.vector-sticky-header-context-bar{min-width:0}.vector-sticky-header-context-bar > \*{padding-left:8px}.vector-sticky-header-context-bar > .vector-sticky-header-context-bar-primary{padding:0 8px}.vector-sticky-header .vector-sticky-header-toc{ margin:0 !important}.vector-sticky-header-context-bar-primary{overflow:hidden;font-family:'Linux Libertine','Georgia','Times','Source Serif 4',serif;font-size:1.5em;text-overflow:ellipsis}.vector-sticky-header-context-bar-primary wbr{display:none}.vector-sticky-header-buttons{font-size:0.875em}.vector-sticky-header-icons,.vector-sticky-header-buttons{column-gap:8px}.vector-sticky-header .vector-search-box{display:none}.vector-sticky-header.vector-header-search-toggled .vector-sticky-header-icon-start,.vector-sticky-header.vector-header-search-toggled .vector-sticky-header-context-bar{display:none}.vector-sticky-header.vector-header-search-toggled .vector-search-box{display:block;margin-left:4px}.vector-sticky-header.vector-header-search-toggled .vector-search-box-show-thumbnail{margin-left:-9px}@media (min-width:1120px){.client-js.vector-sticky-header-enabled .vector-sticky-header-container{display:flex}.client-js.vector-sticky-header-enabled .vector-sticky-header-visible .vector-sticky-header-container{opacity:1;transform:translateY(0)}.client-js.vector-sticky-header-enabled .vector-sticky-pinned-container{top:calc(3.125rem + 24px);max-height:calc(100vh - 3.125rem - (24px \* 2))}.client-js.vector-sticky-header-enabled .mw-sticky-header-element,.client-js.vector-sticky-header-enabled .charts-stickyhead th{ top:3.125rem !important}} .client-js .mw-portlet-dock-bottom,.client-js .vector-settings{display:block;position:fixed;bottom:8px;right:8px;z-index:1}.client-js .mw-portlet-dock-bottom ul,.client-js .vector-settings ul{padding:0;list-style:none;display:flex;flex-direction:column-reverse;align-items:center;gap:8px 8px}
.mw-mmv-overlay{position:fixed;top:0;left:0;right:0;bottom:0;z-index:1000;background-color:#000;display:flex;justify-items:center;align-items:center;align-content:center;justify-content:center}.mw-mmv-overlay .cdx-progress-bar{max-width:80vw;min-width:20vw;width:20rem}.mw-mmv-overlay.mw-mmv-overlay--beta{--color-base:#eaecf0;--color-base--hover:#f8f9fa;--color-emphasized:#f8f9fa;--color-neutral:#c8ccd1;--color-subtle:#a2a9b1;--color-disabled:#54595d;--color-disabled-emphasized:#72777d;--color-inverted:#101418;--color-progressive:#88a3e8; --color-progressive--hover:#a6bbf5;--color-progressive--active:#b6d4fb;--color-destructive:#fd7865; --color-destructive--hover:#fea898;--color-destructive--active:#ffc8bd;--color-visited:#a799cd; --color-visited--hover:#c5b9dd;--color-visited--active:#d9d0e9;--color-destructive--visited:#c99391; --color-destructive--visited--hover:#dcb5b3;--color-destructive--visited--active:#e8cecd;--color-error:#fd7865;--color-error--hover:#fea898;--color-error--active:#ffc8bd;--color-warning:#ca982e;--color-success:#2cb491;--color-notice:#a2a9b1;--color-content-added:#80cdb3;--color-content-removed:#fd7865;--color-base--subtle:#a2a9b1;--box-shadow-color-base:#72777d;--box-shadow-color-progressive--focus:#6485d1;--box-shadow-color-progressive-selected:#88a3e8;--box-shadow-color-progressive-selected--hover:#a6bbf5;--box-shadow-color-progressive-selected--active:#b6d4fb;--box-shadow-color-destructive--focus:#6485d1;--box-shadow-color-inverted:#000;--box-shadow-color-alpha-base:rgba(0,0,0,0.87);--mix-blend-mode-blend:screen;--background-color-base:#101418; --background-color-neutral:#27292d;--background-color-neutral-subtle:#202122;--background-color-interactive:#27292d;--background-color-interactive--hover:#404244;--background-color-interactive--active:#54595d;--background-color-interactive-subtle:#202122;--background-color-interactive-subtle--hover:#27292d;--background-color-interactive-subtle--active:#404244;--background-color-disabled:#404244; --background-color-disabled-subtle:#27292d; --background-color-inverted:#f8f9fa;--background-color-progressive--focus:#6485d1;--background-color-progressive-subtle:#1b223d;--background-color-progressive-subtle--hover:#233566;--background-color-progressive-subtle--active:#3056a9;--background-color-destructive--focus:#6485d1;--background-color-destructive-subtle:#3c1a13;--background-color-destructive-subtle--hover:#612419;--background-color-destructive-subtle--active:#9f3526;--background-color-error-subtle:#3c1a13;--background-color-error-subtle--hover:#612419;--background-color-error-subtle--active:#9f3526;--background-color-warning-subtle:#2d2212;--background-color-success-subtle:#132821;--background-color-notice-subtle:#27292d;--background-color-content-added:#233566;--background-color-content-removed:#453217;--background-color-target-text:#572c19;--background-color-backdrop-light:rgba(0,0,0,0.65); --background-color-backdrop-dark:rgba(255,255,255,0.65);--border-color-base:#72777d;--border-color-emphasized:#eaecf0;--border-color-subtle:#54595d;--border-color-muted:#404244;--border-color-interactive--hover:#a2a9b1;--border-color-interactive--active:#c8ccd1;--border-color-disabled:#54595d;--border-color-inverted:#101418;--border-color-progressive--hover:#88a3e8;--border-color-progressive--active:#a6bbf5;--border-color-progressive--focus:#6485d1;--border-color-destructive--hover:#fd7865;--border-color-destructive--active:#fea898;--border-color-destructive--focus:#6485d1;--border-color-error--hover:#fd7865;--border-color-error--active:#fea898;--border-color-warning--hover:#ca982e;--border-color-warning--active:#edb537;--border-color-content-added:#233566;--border-color-content-removed:#987027;background-color:var(--background-color-interactive-subtle,#f8f9fa)}body.mw-mmv-lightbox-open{overflow-y:auto;background-color:#000}body.mw-mmv-lightbox-open > \*:not(.mw-notification-area-overlay){display:none}body.mw-mmv-lightbox-open > .mw-mmv-overlay{display:flex}body.mw-mmv-lightbox-open > .mw-mmv-wrapper{display:block}.mw-mmv-view-expanded .cdx-button\_\_icon{ min-width:10px;min-height:10px;width:var(--font-size-medium,1rem);height:var(--font-size-medium,1rem);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.mw-mmv-view-expanded .cdx-button\_\_icon{background-position:center;background-repeat:no-repeat; background-size:calc(max(var(--font-size-medium,1rem),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.mw-mmv-view-expanded .cdx-button\_\_icon{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(var(--font-size-medium,1rem),10px));mask-size:calc(max(var(--font-size-medium,1rem),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.mw-mmv-view-expanded .cdx-button\_\_icon{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M3 5a2 2 0 00-2 2v10a2 2 0 002 2h14a2 2 0 002-2V7a2 2 0 00-2-2zm0 11 3.5-4.5 2.5 3 3.5-4.5 4.5 6zM16 2a2 2 0 012 2H2a2 2 0 012-2z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}.cdx-button:not(.cdx-button--weight-quiet):disabled .mw-mmv-view-expanded .cdx-button\_\_icon,.cdx-button--weight-primary.cdx-button--action-progressive .mw-mmv-view-expanded .cdx-button\_\_icon,.cdx-button--weight-primary.cdx-button--action-destructive .mw-mmv-view-expanded .cdx-button\_\_icon{filter:invert(var(--filter-invert-primary-button-icon,1))}}@supports (-webkit-mask-image:none) or (mask-image:none){.mw-mmv-view-expanded .cdx-button\_\_icon{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M3 5a2 2 0 00-2 2v10a2 2 0 002 2h14a2 2 0 002-2V7a2 2 0 00-2-2zm0 11 3.5-4.5 2.5 3 3.5-4.5 4.5 6zM16 2a2 2 0 012 2H2a2 2 0 012-2z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M3 5a2 2 0 00-2 2v10a2 2 0 002 2h14a2 2 0 002-2V7a2 2 0 00-2-2zm0 11 3.5-4.5 2.5 3 3.5-4.5 4.5 6zM16 2a2 2 0 012 2H2a2 2 0 012-2z\"/></svg>");transition-property:background-color;transition-duration:100ms}}
.ve-init-mw-tempWikitextEditorWidget{border:0;padding:0;color:inherit;line-height:1.5em;width:100%;-moz-tab-size:4;tab-size:4; }.ve-init-mw-tempWikitextEditorWidget:focus{outline:0;padding:0}.ve-init-mw-tempWikitextEditorWidget::selection{background:rgba(109,169,247,0.5)}
.ext-quick-survey-panel,.ext-qs-loader-bar{width:auto;background-color:var(--background-color-neutral,#eaecf0)} .ext-qs-loader-bar{height:100px;margin-left:1.4em;clear:right;float:right;background-color:var(--background-color-neutral,#eaecf0);display:flex;justify-content:center;align-items:center}.ext-qs-loader-bar .mw-spinner-container{transform:scale(0.5);transform-origin:center;width:25%;height:75%}.ext-quick-survey-panel{overflow-wrap:anywhere}@media all and (min-width:640px){.ext-qs-loader-bar,.ext-quick-survey-panel{margin-left:1.4em;width:300px;clear:right;float:right}}.mw-body > .content .panel.ext-quick-survey-panel{text-align:initial}.mw-body > .content .panel.ext-quick-survey-panel .image{background-position:center 80%;background-repeat:no-repeat;background-size:auto 5em}@media print{.ext-quick-survey-panel{display:none}}
.oo-ui-icon-edit,.mw-ui-icon-edit:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E edit %3C/title%3E%3Cpath d=%22m16.77 8 1.94-2a1 1 0 0 0 0-1.41l-3.34-3.3a1 1 0 0 0-1.41 0L12 3.23zM1 14.25V19h4.75l9.96-9.96-4.75-4.75z%22/%3E%3C/svg%3E")}.oo-ui-image-invert.oo-ui-icon-edit,.mw-ui-icon-edit-invert:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E edit %3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22m16.77 8 1.94-2a1 1 0 0 0 0-1.41l-3.34-3.3a1 1 0 0 0-1.41 0L12 3.23zM1 14.25V19h4.75l9.96-9.96-4.75-4.75z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-progressive.oo-ui-icon-edit,.mw-ui-icon-edit-progressive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E edit %3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22m16.77 8 1.94-2a1 1 0 0 0 0-1.41l-3.34-3.3a1 1 0 0 0-1.41 0L12 3.23zM1 14.25V19h4.75l9.96-9.96-4.75-4.75z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-icon-editLock,.mw-ui-icon-editLock:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E edit lock %3C/title%3E%3Cpath d=%22M12 12a2 2 0 0 1-2-2V5.25l-9 9V19h4.75l7-7zm7-8h-.5V2.5a2.5 2.5 0 0 0-5 0V4H13a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1m-3 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1m1.5-4h-3V2.75C14.5 2 14.5 1 16 1s1.5 1 1.5 1.75z%22/%3E%3C/svg%3E")}.oo-ui-image-invert.oo-ui-icon-editLock,.mw-ui-icon-editLock-invert:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E edit lock %3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22M12 12a2 2 0 0 1-2-2V5.25l-9 9V19h4.75l7-7zm7-8h-.5V2.5a2.5 2.5 0 0 0-5 0V4H13a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1m-3 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1m1.5-4h-3V2.75C14.5 2 14.5 1 16 1s1.5 1 1.5 1.75z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-progressive.oo-ui-icon-editLock,.mw-ui-icon-editLock-progressive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E edit lock %3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22M12 12a2 2 0 0 1-2-2V5.25l-9 9V19h4.75l7-7zm7-8h-.5V2.5a2.5 2.5 0 0 0-5 0V4H13a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1m-3 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1m1.5-4h-3V2.75C14.5 2 14.5 1 16 1s1.5 1 1.5 1.75z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-icon-editUndo,.mw-ui-icon-editUndo:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E undo edit %3C/title%3E%3Cpath d=%22M1 14.25V19h4.75l8.33-8.33-5.27-4.23zM13 2.86V0L8 4l5 4V5h.86c2.29 0 4 1.43 4 4.29H20a6.51 6.51 0 0 0-6.14-6.43z%22/%3E%3C/svg%3E")}.oo-ui-image-invert.oo-ui-icon-editUndo,.mw-ui-icon-editUndo-invert:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E undo edit %3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22M1 14.25V19h4.75l8.33-8.33-5.27-4.23zM13 2.86V0L8 4l5 4V5h.86c2.29 0 4 1.43 4 4.29H20a6.51 6.51 0 0 0-6.14-6.43z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-progressive.oo-ui-icon-editUndo,.mw-ui-icon-editUndo-progressive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E undo edit %3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22M1 14.25V19h4.75l8.33-8.33-5.27-4.23zM13 2.86V0L8 4l5 4V5h.86c2.29 0 4 1.43 4 4.29H20a6.51 6.51 0 0 0-6.14-6.43z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-icon-link,.mw-ui-icon-link:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E link %3C/title%3E%3Cpath d=%22M4.83 15h2.91a4.9 4.9 0 0 1-1.55-2H5a3 3 0 1 1 0-6h3a3 3 0 0 1 2.82 4h2.1a5 5 0 0 0 .08-.83v-.34A4.83 4.83 0 0 0 8.17 5H4.83A4.83 4.83 0 0 0 0 9.83v.34A4.83 4.83 0 0 0 4.83 15%22/%3E%3Cpath d=%22M15.17 5h-2.91a4.9 4.9 0 0 1 1.55 2H15a3 3 0 1 1 0 6h-3a3 3 0 0 1-2.82-4h-2.1a5 5 0 0 0-.08.83v.34A4.83 4.83 0 0 0 11.83 15h3.34A4.83 4.83 0 0 0 20 10.17v-.34A4.83 4.83 0 0 0 15.17 5%22/%3E%3C/svg%3E")}.oo-ui-image-invert.oo-ui-icon-link,.mw-ui-icon-link-invert:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E link %3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22M4.83 15h2.91a4.9 4.9 0 0 1-1.55-2H5a3 3 0 1 1 0-6h3a3 3 0 0 1 2.82 4h2.1a5 5 0 0 0 .08-.83v-.34A4.83 4.83 0 0 0 8.17 5H4.83A4.83 4.83 0 0 0 0 9.83v.34A4.83 4.83 0 0 0 4.83 15%22/%3E%3Cpath d=%22M15.17 5h-2.91a4.9 4.9 0 0 1 1.55 2H15a3 3 0 1 1 0 6h-3a3 3 0 0 1-2.82-4h-2.1a5 5 0 0 0-.08.83v.34A4.83 4.83 0 0 0 11.83 15h3.34A4.83 4.83 0 0 0 20 10.17v-.34A4.83 4.83 0 0 0 15.17 5%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-progressive.oo-ui-icon-link,.mw-ui-icon-link-progressive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E link %3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22M4.83 15h2.91a4.9 4.9 0 0 1-1.55-2H5a3 3 0 1 1 0-6h3a3 3 0 0 1 2.82 4h2.1a5 5 0 0 0 .08-.83v-.34A4.83 4.83 0 0 0 8.17 5H4.83A4.83 4.83 0 0 0 0 9.83v.34A4.83 4.83 0 0 0 4.83 15%22/%3E%3Cpath d=%22M15.17 5h-2.91a4.9 4.9 0 0 1 1.55 2H15a3 3 0 1 1 0 6h-3a3 3 0 0 1-2.82-4h-2.1a5 5 0 0 0-.08.83v.34A4.83 4.83 0 0 0 11.83 15h3.34A4.83 4.83 0 0 0 20 10.17v-.34A4.83 4.83 0 0 0 15.17 5%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-icon-unLink,.mw-ui-icon-unLink:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E unlink %3C/title%3E%3Cpath d=%22M4.83 5A4.83 4.83 0 0 0 0 9.83v.34A4.83 4.83 0 0 0 4.83 15h2.91a4.9 4.9 0 0 1-1.55-2H5c-4 0-4-6 0-6h3q.113.002.225.012L6.215 5zm7.43 0a4.9 4.9 0 0 1 1.55 2H15c3.179.003 4.17 4.3 1.314 5.695l1.508 1.508A4.83 4.83 0 0 0 20 10.17v-.34A4.83 4.83 0 0 0 15.17 5zm-3.612.03 4.329 4.327A4.83 4.83 0 0 0 8.648 5.03M7.227 8.411C7.17 8.595 7.08 9 7.08 9c-.045.273-.08.584-.08.83v.34A4.83 4.83 0 0 0 11.83 15h3.34q.475 0 .941-.094L14.205 13H12c-2.067-.006-3.51-2.051-2.82-4zm3.755 1.36A3 3 0 0 1 10.82 11h1.389z%22/%3E%3Cpath d=%22M1.22 0 0 1.22 18.8 20l1.2-1.22z%22/%3E%3C/svg%3E")}.oo-ui-image-invert.oo-ui-icon-unLink,.mw-ui-icon-unLink-invert:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E unlink %3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22M4.83 5A4.83 4.83 0 0 0 0 9.83v.34A4.83 4.83 0 0 0 4.83 15h2.91a4.9 4.9 0 0 1-1.55-2H5c-4 0-4-6 0-6h3q.113.002.225.012L6.215 5zm7.43 0a4.9 4.9 0 0 1 1.55 2H15c3.179.003 4.17 4.3 1.314 5.695l1.508 1.508A4.83 4.83 0 0 0 20 10.17v-.34A4.83 4.83 0 0 0 15.17 5zm-3.612.03 4.329 4.327A4.83 4.83 0 0 0 8.648 5.03M7.227 8.411C7.17 8.595 7.08 9 7.08 9c-.045.273-.08.584-.08.83v.34A4.83 4.83 0 0 0 11.83 15h3.34q.475 0 .941-.094L14.205 13H12c-2.067-.006-3.51-2.051-2.82-4zm3.755 1.36A3 3 0 0 1 10.82 11h1.389z%22/%3E%3Cpath d=%22M1.22 0 0 1.22 18.8 20l1.2-1.22z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-progressive.oo-ui-icon-unLink,.mw-ui-icon-unLink-progressive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E unlink %3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22M4.83 5A4.83 4.83 0 0 0 0 9.83v.34A4.83 4.83 0 0 0 4.83 15h2.91a4.9 4.9 0 0 1-1.55-2H5c-4 0-4-6 0-6h3q.113.002.225.012L6.215 5zm7.43 0a4.9 4.9 0 0 1 1.55 2H15c3.179.003 4.17 4.3 1.314 5.695l1.508 1.508A4.83 4.83 0 0 0 20 10.17v-.34A4.83 4.83 0 0 0 15.17 5zm-3.612.03 4.329 4.327A4.83 4.83 0 0 0 8.648 5.03M7.227 8.411C7.17 8.595 7.08 9 7.08 9c-.045.273-.08.584-.08.83v.34A4.83 4.83 0 0 0 11.83 15h3.34q.475 0 .941-.094L14.205 13H12c-2.067-.006-3.51-2.051-2.82-4zm3.755 1.36A3 3 0 0 1 10.82 11h1.389z%22/%3E%3Cpath d=%22M1.22 0 0 1.22 18.8 20l1.2-1.22z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-destructive.oo-ui-icon-unLink,.mw-ui-icon-unLink-destructive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E unlink %3C/title%3E%3Cg fill=%22%23d73333%22%3E%3Cpath d=%22M4.83 5A4.83 4.83 0 0 0 0 9.83v.34A4.83 4.83 0 0 0 4.83 15h2.91a4.9 4.9 0 0 1-1.55-2H5c-4 0-4-6 0-6h3q.113.002.225.012L6.215 5zm7.43 0a4.9 4.9 0 0 1 1.55 2H15c3.179.003 4.17 4.3 1.314 5.695l1.508 1.508A4.83 4.83 0 0 0 20 10.17v-.34A4.83 4.83 0 0 0 15.17 5zm-3.612.03 4.329 4.327A4.83 4.83 0 0 0 8.648 5.03M7.227 8.411C7.17 8.595 7.08 9 7.08 9c-.045.273-.08.584-.08.83v.34A4.83 4.83 0 0 0 11.83 15h3.34q.475 0 .941-.094L14.205 13H12c-2.067-.006-3.51-2.051-2.82-4zm3.755 1.36A3 3 0 0 1 10.82 11h1.389z%22/%3E%3Cpath d=%22M1.22 0 0 1.22 18.8 20l1.2-1.22z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-icon-linkExternal,.mw-ui-icon-linkExternal:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E external link %3C/title%3E%3Cpath d=%22M19 1h-8l3.286 3.286L6 12l1.371 1.472 8.332-7.77.007.008L19 9zM2 5h4v2H3v10h10v-4.004h2V18a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1%22/%3E%3C/svg%3E")}.oo-ui-image-invert.oo-ui-icon-linkExternal,.mw-ui-icon-linkExternal-invert:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E external link %3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22M19 1h-8l3.286 3.286L6 12l1.371 1.472 8.332-7.77.007.008L19 9zM2 5h4v2H3v10h10v-4.004h2V18a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-progressive.oo-ui-icon-linkExternal,.mw-ui-icon-linkExternal-progressive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E external link %3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22M19 1h-8l3.286 3.286L6 12l1.371 1.472 8.332-7.77.007.008L19 9zM2 5h4v2H3v10h10v-4.004h2V18a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-icon-linkSecure,.mw-ui-icon-linkSecure:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E secure link %3C/title%3E%3Cpath d=%22M16.07 8H15V5s0-5-5-5-5 5-5 5v3H3.93A1.93 1.93 0 0 0 2 9.93v8.15A1.93 1.93 0 0 0 3.93 20h12.14A1.93 1.93 0 0 0 18 18.07V9.93A1.93 1.93 0 0 0 16.07 8M7 5.5C7 4 7 2 10 2s3 2 3 3.5V8H7zM10 16a2 2 0 1 1 2-2 2 2 0 0 1-2 2%22/%3E%3C/svg%3E")}.oo-ui-image-invert.oo-ui-icon-linkSecure,.mw-ui-icon-linkSecure-invert:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E secure link %3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22M16.07 8H15V5s0-5-5-5-5 5-5 5v3H3.93A1.93 1.93 0 0 0 2 9.93v8.15A1.93 1.93 0 0 0 3.93 20h12.14A1.93 1.93 0 0 0 18 18.07V9.93A1.93 1.93 0 0 0 16.07 8M7 5.5C7 4 7 2 10 2s3 2 3 3.5V8H7zM10 16a2 2 0 1 1 2-2 2 2 0 0 1-2 2%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-progressive.oo-ui-icon-linkSecure,.mw-ui-icon-linkSecure-progressive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E secure link %3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22M16.07 8H15V5s0-5-5-5-5 5-5 5v3H3.93A1.93 1.93 0 0 0 2 9.93v8.15A1.93 1.93 0 0 0 3.93 20h12.14A1.93 1.93 0 0 0 18 18.07V9.93A1.93 1.93 0 0 0 16.07 8M7 5.5C7 4 7 2 10 2s3 2 3 3.5V8H7zM10 16a2 2 0 1 1 2-2 2 2 0 0 1-2 2%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-icon-redo,.mw-ui-icon-redo:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E redo %3C/title%3E%3Cpath d=%22M19 8.5 12 3v11zM12 7v3h-1c-4 0-7 2-7 6v1H1v-1c0-6 5-9 10-9z%22/%3E%3C/svg%3E")}.oo-ui-image-invert.oo-ui-icon-redo,.mw-ui-icon-redo-invert:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E redo %3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22M19 8.5 12 3v11zM12 7v3h-1c-4 0-7 2-7 6v1H1v-1c0-6 5-9 10-9z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-progressive.oo-ui-icon-redo,.mw-ui-icon-redo-progressive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E redo %3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22M19 8.5 12 3v11zM12 7v3h-1c-4 0-7 2-7 6v1H1v-1c0-6 5-9 10-9z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-icon-undo,.mw-ui-icon-undo:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E undo %3C/title%3E%3Cpath d=%22M1 8.5 8 14v-4h1c4 0 7 2 7 6v1h3v-1c0-6-5-9-10-9H8V3z%22/%3E%3C/svg%3E")}.oo-ui-image-invert.oo-ui-icon-undo,.mw-ui-icon-undo-invert:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E undo %3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22M1 8.5 8 14v-4h1c4 0 7 2 7 6v1h3v-1c0-6-5-9-10-9H8V3z%22/%3E%3C/g%3E%3C/svg%3E")}.oo-ui-image-progressive.oo-ui-icon-undo,.mw-ui-icon-undo-progressive:before{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3E undo %3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22M1 8.5 8 14v-4h1c4 0 7 2 7 6v1h3v-1c0-6-5-9-10-9H8V3z%22/%3E%3C/g%3E%3C/svg%3E")}
@keyframes mwe-popups-fade-in-up{0%{opacity:0;transform:translate(0,20px)}100%{opacity:1;transform:translate(0,0)}}@keyframes mwe-popups-fade-in-down{0%{opacity:0;transform:translate(0,-20px)}100%{opacity:1;transform:translate(0,0)}}@keyframes mwe-popups-fade-out-down{0%{opacity:1;transform:translate(0,0)}100%{opacity:0;transform:translate(0,20px)}}@keyframes mwe-popups-fade-out-up{0%{opacity:1;transform:translate(0,0)}100%{opacity:0;transform:translate(0,-20px)}}.mwe-popups-fade-in-up{animation:mwe-popups-fade-in-up 0.2s ease forwards}.mwe-popups-fade-in-down{animation:mwe-popups-fade-in-down 0.2s ease forwards}.mwe-popups-fade-out-down{animation:mwe-popups-fade-out-down 0.2s ease forwards}.mwe-popups-fade-out-up{animation:mwe-popups-fade-out-up 0.2s ease forwards}.popups-icon--settings{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--settings{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--settings{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--settings{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><g xmlns:xlink=\"http://www.w3.org/1999/xlink\" transform=\"translate(10 10)\"><path id=\"cdx-icon-settings-a\" d=\"M1.5-10h-3l-1 6.5h5m0 7h-5l1 6.5h3\"/><use xlink:href=\"%23cdx-icon-settings-a\" transform=\"rotate(45)\"/><use xlink:href=\"%23cdx-icon-settings-a\" transform=\"rotate(90)\"/><use xlink:href=\"%23cdx-icon-settings-a\" transform=\"rotate(135)\"/></g><path d=\"M10 2.5a7.5 7.5 0 000 15 7.5 7.5 0 000-15v4a3.5 3.5 0 010 7 3.5 3.5 0 010-7\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--settings{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><g xmlns:xlink=\"http://www.w3.org/1999/xlink\" transform=\"translate(10 10)\"><path id=\"cdx-icon-settings-a\" d=\"M1.5-10h-3l-1 6.5h5m0 7h-5l1 6.5h3\"/><use xlink:href=\"%23cdx-icon-settings-a\" transform=\"rotate(45)\"/><use xlink:href=\"%23cdx-icon-settings-a\" transform=\"rotate(90)\"/><use xlink:href=\"%23cdx-icon-settings-a\" transform=\"rotate(135)\"/></g><path d=\"M10 2.5a7.5 7.5 0 000 15 7.5 7.5 0 000-15v4a3.5 3.5 0 010 7 3.5 3.5 0 010-7\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><g xmlns:xlink=\"http://www.w3.org/1999/xlink\" transform=\"translate(10 10)\"><path id=\"cdx-icon-settings-a\" d=\"M1.5-10h-3l-1 6.5h5m0 7h-5l1 6.5h3\"/><use xlink:href=\"%23cdx-icon-settings-a\" transform=\"rotate(45)\"/><use xlink:href=\"%23cdx-icon-settings-a\" transform=\"rotate(90)\"/><use xlink:href=\"%23cdx-icon-settings-a\" transform=\"rotate(135)\"/></g><path d=\"M10 2.5a7.5 7.5 0 000 15 7.5 7.5 0 000-15v4a3.5 3.5 0 010 7 3.5 3.5 0 010-7\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--infoFilled{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--infoFilled{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--infoFilled{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--infoFilled{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0M9 5h2v2H9zm0 4h2v6H9z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--infoFilled{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0M9 5h2v2H9zm0 4h2v6H9z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0M9 5h2v2H9zm0 4h2v6H9z\"/></svg>");background-color:var(--color-base,#202122)}}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--infoFilled:lang(ar){background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M8 19a1 1 0 001 1h2a1 1 0 001-1v-1H8zm9-12a7 7 0 10-12 4.9S7 14 7 15v1a1 1 0 001 1h4a1 1 0 001-1v-1c0-1 2-3.1 2-3.1A7 7 0 0017 7\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--infoFilled:lang(ar){ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M8 19a1 1 0 001 1h2a1 1 0 001-1v-1H8zm9-12a7 7 0 10-12 4.9S7 14 7 15v1a1 1 0 001 1h4a1 1 0 001-1v-1c0-1 2-3.1 2-3.1A7 7 0 0017 7\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M8 19a1 1 0 001 1h2a1 1 0 001-1v-1H8zm9-12a7 7 0 10-12 4.9S7 14 7 15v1a1 1 0 001 1h4a1 1 0 001-1v-1c0-1 2-3.1 2-3.1A7 7 0 0017 7\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--close{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--close{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--close{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--close{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"m4.34 2.93 12.73 12.73-1.41 1.41L2.93 4.35z\"/><path d=\"M17.07 4.34 4.34 17.07l-1.41-1.41L15.66 2.93z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--close{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"m4.34 2.93 12.73 12.73-1.41 1.41L2.93 4.35z\"/><path d=\"M17.07 4.34 4.34 17.07l-1.41-1.41L15.66 2.93z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"m4.34 2.93 12.73 12.73-1.41 1.41L2.93 4.35z\"/><path d=\"M17.07 4.34 4.34 17.07l-1.41-1.41L15.66 2.93z\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--footer{background-image:url(/w/extensions/Popups/src/ui/icons/footer-ltr.svg?9d590)}.popups-icon--preview-generic{mask-image:url(/w/extensions/Popups/src/ui/icons/sad-face-ltr.svg?d9aab);background-color:var(--color-base,#202122)}#mwe-popups-settings{z-index:1000;background-color:var(--background-color-base,#fff);width:420px;border:1px solid var(--border-color-base,#a2a9b1);box-shadow:0 4px 4px 0 var(--box-shadow-color-alpha-base,rgba(0,0,0,0.06)),0 0 8px 0 var(--box-shadow-color-alpha-base,rgba(0,0,0,0.06));border-radius:2px;font-size:var(--font-size-small,0.875rem)}#mwe-popups-settings header{box-sizing:border-box;border-bottom:1px solid var(--border-color-subtle,#c8ccd1);position:relative;display:table;width:100%;padding:5px 7px}#mwe-popups-settings header > div{display:table-cell;width:calc(calc(var(--font-size-medium,1rem) + 4px) + (2 \* 1em));vertical-align:middle;cursor:pointer}#mwe-popups-settings header h1{margin-bottom:0.6em;padding-top:0.5em;border:0;width:100%;font-family:sans-serif;font-size:var(--font-size-large,1.125rem);font-weight:bold;text-align:center}#mwe-popups-settings main#mwe-popups-settings-form{display:block;width:350px;padding:32px 0 24px;margin:0 auto}#mwe-popups-settings main#mwe-popups-settings-form p{color:var(--color-subtle,#54595d);font-size:var(--font-size-small,0.875rem);margin:16px 0 0}#mwe-popups-settings main#mwe-popups-settings-form p:first-child{margin-top:0}#mwe-popups-settings main#mwe-popups-settings-form form img{margin-right:60px}#mwe-popups-settings main#mwe-popups-settings-form form label{font-size:var(--font-size-small,0.875rem);line-height:16px;width:300px;margin-left:10px;flex-direction:column}#mwe-popups-settings main#mwe-popups-settings-form form label > span{color:var(--color-emphasized,#101418);font-size:var(--font-size-small,0.875rem);font-weight:700;display:block;margin-bottom:5px}#mwe-popups-settings main#mwe-popups-settings-form form label::before{top:0.78125em !important}.mwe-popups-settings-help{font-size:var(--font-size-small,0.875rem);font-weight:700;margin:40px;position:relative}.mwe-popups-settings-help .popups-icon{background-size:contain;width:180px;max-width:none;height:140px;margin:0;padding:0}.mwe-popups-settings-help p{left:180px;bottom:20px;position:absolute}.mwe-popups{background:var(--background-color-base,#fff);position:absolute;z-index:110;box-shadow:0 30px 90px -20px rgba(0,0,0,0.3),0 0 0 1px var(--background-color-neutral,#eaecf0);padding:0;display:none;font-size:var(--font-size-small,0.875rem);line-height:20px;min-width:300px;border-radius:2px; }.mwe-popups .mwe-popups-container{color:var(--color-base,#202122);text-decoration:none}.mwe-popups .mwe-popups-container footer{padding:0 16px 16px;margin:0;position:absolute;bottom:0;pointer-events:none}.mwe-popups .mwe-popups-container footer a{pointer-events:auto}.mwe-popups .mwe-popups-settings-button{float:right;pointer-events:auto; min-width:32px !important;min-height:32px !important}.mwe-popups .mwe-popups-extract{margin:16px;display:block;color:var(--color-base,#202122);text-decoration:none;position:relative;padding-bottom:4px}.mwe-popups .mwe-popups-extract:hover{text-decoration:none;color:inherit}.mwe-popups .mwe-popups-extract::after{content:' ';position:absolute;bottom:0;width:25%;height:20px;background-color:transparent;pointer-events:none}.mwe-popups .mwe-popups-extract[dir='ltr']::after{ right:0; background-image:linear-gradient(to right,rgba(255,255,255,0),#ffffff 50%)}.mwe-popups .mwe-popups-extract[dir='rtl']::after{ left:0; background-image:linear-gradient(to left,rgba(255,255,255,0),#ffffff 50%)}.mwe-popups .mwe-popups-extract p{margin:0}.mwe-popups .mwe-popups-extract ul,.mwe-popups .mwe-popups-extract ol,.mwe-popups .mwe-popups-extract li,.mwe-popups .mwe-popups-extract dl,.mwe-popups .mwe-popups-extract dd,.mwe-popups .mwe-popups-extract dt{margin-top:0;margin-bottom:0}.mwe-popups .mwe-popups-extract blockquote{margin:0;padding:0 20px}.mwe-popups svg{overflow:hidden}.mwe-popups.mwe-popups-is-tall{width:450px}.mwe-popups.mwe-popups-is-tall > div > a > svg{vertical-align:middle}.mwe-popups.mwe-popups-is-tall .mwe-popups-extract{width:215px;height:176px;overflow:hidden;float:left}.mwe-popups.mwe-popups-is-tall footer{left:0;right:203px}.mwe-popups.mwe-popups-is-not-tall{width:320px}.mwe-popups.mwe-popups-is-not-tall .mwe-popups-extract{min-height:50px;max-height:136px;overflow:hidden;margin-bottom:50px}.mwe-popups.mwe-popups-is-not-tall footer{left:0;right:0}.mwe-popups.mwe-popups-no-image-pointer::before{content:'';position:absolute;border:8px solid var(--border-color-transparent,transparent);border-top:0;border-bottom:8px solid rgba(0,0,0,0.07000000000000001);top:-8px;left:10px}.mwe-popups.mwe-popups-no-image-pointer::after{content:'';position:absolute;border:11px solid var(--border-color-transparent,transparent);border-top:0;border-bottom:11px solid var(--background-color-base,#fff);top:-7px;left:7px}.mwe-popups.flipped-x.mwe-popups-no-image-pointer::before{left:auto;right:10px}.mwe-popups.flipped-x.mwe-popups-no-image-pointer::after{left:auto;right:7px}.mwe-popups.mwe-popups-image-pointer::before{content:'';position:absolute;border:9px solid var(--border-color-transparent,transparent);border-top:0;border-bottom:9px solid var(--border-color-base,#a2a9b1);top:-9px;left:9px;z-index:111}.mwe-popups.mwe-popups-image-pointer::after{content:'';position:absolute;border:12px solid var(--border-color-transparent,transparent);border-top:0;border-bottom:12px solid var(--background-color-base,#fff);top:-8px;left:6px;z-index:112}.mwe-popups.mwe-popups-image-pointer.flipped-x::before{content:'';position:absolute;border:9px solid var(--border-color-transparent,transparent);border-top:0;border-bottom:9px solid var(--border-color-base,#a2a9b1);top:-9px;left:293px}.mwe-popups.mwe-popups-image-pointer.flipped-x::after{content:'';position:absolute;border:12px solid var(--border-color-transparent,transparent);border-top:0;border-bottom:12px solid var(--background-color-base,#fff);top:-8px;left:290px}.mwe-popups.mwe-popups-image-pointer > div > a > svg{margin-top:-8px;position:absolute;z-index:113;left:0}.mwe-popups.flipped-x.mwe-popups-is-tall{min-height:242px}.mwe-popups.flipped-x.mwe-popups-is-tall::before{content:'';position:absolute;border:9px solid var(--border-color-transparent,transparent);border-top:0;border-bottom:9px solid var(--border-color-base,#a2a9b1);top:-9px;left:420px;z-index:111}.mwe-popups.flipped-x.mwe-popups-is-tall > div > a > svg{margin:0;margin-top:-8px;margin-bottom:-7px;position:absolute;z-index:113;right:0}.mwe-popups.flipped-x-y::before{content:'';position:absolute;border:9px solid var(--border-color-transparent,transparent);border-bottom:0;border-top:9px solid var(--border-color-base,#a2a9b1);bottom:-9px;left:293px;z-index:111}.mwe-popups.flipped-x-y::after{content:'';position:absolute;border:12px solid var(--border-color-transparent,transparent);border-bottom:0;border-top:12px solid var(--background-color-base,#fff);bottom:-8px;left:290px;z-index:112}.mwe-popups.flipped-x-y.mwe-popups-is-tall{min-height:242px}.mwe-popups.flipped-x-y.mwe-popups-is-tall::before{content:'';position:absolute;border:9px solid var(--border-color-transparent,transparent);border-bottom:0;border-top:9px solid var(--border-color-base,#a2a9b1);bottom:-9px;left:420px}.mwe-popups.flipped-x-y.mwe-popups-is-tall::after{content:'';position:absolute;border:12px solid var(--border-color-transparent,transparent);border-bottom:0;border-top:12px solid var(--background-color-base,#fff);bottom:-8px;left:417px}.mwe-popups.flipped-x-y.mwe-popups-is-tall > div > a > svg{margin:0;margin-bottom:-9px;position:absolute;z-index:113;right:0}.mwe-popups.flipped-y::before{content:'';position:absolute;border:8px solid var(--border-color-transparent,transparent);border-bottom:0;border-top:8px solid var(--border-color-base,#a2a9b1);bottom:-8px;left:10px}.mwe-popups.flipped-y::after{content:'';position:absolute;border:11px solid var(--border-color-transparent,transparent);border-bottom:0;border-top:11px solid var(--background-color-base,#fff);bottom:-7px;left:7px}.mwe-popups-is-tall polyline{transform:translate(0,0)}.mwe-popups-is-tall.flipped-x-y polyline{transform:translate(0,-8px)}.mwe-popups-is-tall.flipped-x polyline{transform:translate(0,8px)}.rtl .mwe-popups-is-tall polyline{transform:translate(-100%,0)}.rtl .mwe-popups-is-tall.flipped-x-y polyline{transform:translate(-100%,-8px)}.rtl .mwe-popups-is-tall.flipped-x polyline{transform:translate(-100%,8px)}@supports (clip-path:polygon(1px 1px)){.mwe-popups .mwe-popups-thumbnail{display:block;object-fit:cover;outline:1px solid rgba(0,0,0,0.1)}.mwe-popups.flipped-y .mwe-popups-container,.mwe-popups.flipped-x-y .mwe-popups-container{--y1:100%;--y2:calc(100% - var(--pointer-height));--y3:calc(100% - var(--pointer-height) - var(--pseudo-radius));--y4:var(--pseudo-radius);--y5:0;margin-bottom:calc(var(--pointer-height) \* -1);padding-bottom:var(--pointer-height)}.mwe-popups:not(.flipped-y):not(.flipped-x-y) .mwe-popups-container{margin-top:calc(var(--pointer-height) \* -1);padding-top:var(--pointer-height)}.mwe-popups .mwe-popups-discreet{margin-top:calc(var(--pointer-height) \* -1)}.mwe-popups.mwe-popups-is-tall.flipped-y .mwe-popups-discreet,.mwe-popups.mwe-popups-is-tall.flipped-x-y .mwe-popups-discreet{margin-top:0;margin-bottom:calc(var(--pointer-height) \* -1)}.mwe-popups .mwe-popups-container{--x1:0;--x2:var(--pseudo-radius);--x3:calc(var(--pointer-offset) - (var(--pointer-width) / 2));--x4:var(--pointer-offset);--x5:calc(var(--pointer-offset) + (var(--pointer-width) / 2));--x6:calc(100% - var(--pseudo-radius));--x7:100%;--y1:0;--y2:var(--pointer-height);--y3:calc(var(--pointer-height) + var(--pseudo-radius));--y4:calc(100% - var(--pseudo-radius));--y5:100%;padding-top:0;display:flex;background:var(--background-color-base,#fff);--pseudo-radius:2px;--pointer-height:8px;--pointer-width:16px;--pointer-offset:26px;clip-path:polygon(var(--x2) var(--y2),var(--x3) var(--y2),var(--x4) var(--y1),var(--x5) var(--y2),var(--x6) var(--y2),var(--x7) var(--y3),var(--x7) var(--y4),var(--x6) var(--y5),var(--x2) var(--y5),var(--x1) var(--y4),var(--x1) var(--y3))}.mwe-popups.mwe-popups-is-tall{flex-direction:row}.mwe-popups.mwe-popups-is-tall .mwe-popups-discreet{order:1}.mwe-popups.mwe-popups-is-tall .mwe-popups-discreet .mwe-popups-thumbnail{width:203px;box-sizing:border-box;height:250px}.mwe-popups.mwe-popups-is-not-tall .mwe-popups-thumbnail{width:320px;height:192px}.mwe-popups.mwe-popups-is-not-tall .mwe-popups-container{flex-direction:column}.mwe-popups::before{display:none}.mwe-popups::after{display:none}body.ltr .mwe-popups.flipped-x .mwe-popups-container,body.ltr .mwe-popups.flipped-x-y .mwe-popups-container,body.rtl .mwe-popups:not(.flipped-x):not(.flipped-x-y) .mwe-popups-container{--x3:calc(100% - var(--pointer-offset) - (var(--pointer-width) / 2));--x4:calc(100% - var(--pointer-offset));--x5:calc(100% - var(--pointer-offset) + (var(--pointer-width) / 2))}}@media screen{html.skin-theme-clientpref-night .mwe-popups.mwe-popups-no-image-pointer::before{content:'';position:absolute;border:8px solid var(--border-color-transparent,transparent);border-top:0;border-bottom:8px solid rgba(255,255,255,0.07000000000000001);top:-8px;left:10px}html.skin-theme-clientpref-night .mwe-popups-extract[dir='ltr']::after{ background-image:linear-gradient(to right,transparent,var(--background-color-base,#fff) 50%)}html.skin-theme-clientpref-night .mwe-popups-extract[dir='rtl']::after{ background-image:linear-gradient(to left,transparent,var(--background-color-base,#fff) 50%)}@supports (clip-path:polygon(1px 1px)){html.skin-theme-clientpref-night .mwe-popups .mwe-popups-thumbnail{background-color:#c8ccd1}}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mwe-popups.mwe-popups-no-image-pointer::before{content:'';position:absolute;border:8px solid var(--border-color-transparent,transparent);border-top:0;border-bottom:8px solid rgba(255,255,255,0.07000000000000001);top:-8px;left:10px}html.skin-theme-clientpref-os .mwe-popups-extract[dir='ltr']::after{ background-image:linear-gradient(to right,transparent,var(--background-color-base,#fff) 50%)}html.skin-theme-clientpref-os .mwe-popups-extract[dir='rtl']::after{ background-image:linear-gradient(to left,transparent,var(--background-color-base,#fff) 50%)}@supports (clip-path:polygon(1px 1px)){html.skin-theme-clientpref-os .mwe-popups .mwe-popups-thumbnail{background-color:#c8ccd1}}}.mwe-popups .mwe-popups-title{display:block;margin-bottom:12px}.mwe-popups-type-generic.mwe-popups .mwe-popups-title{font-weight:normal;margin:0}.mwe-popups .mwe-popups-title .popups-icon,.mwe-popups .mw-parser-output .popups-icon{margin:0 8px 0 0}.mwe-popups.mwe-popups-type-generic .mwe-popups-extract,.mwe-popups.mwe-popups-type-disambiguation .mwe-popups-extract{min-height:auto}.mwe-popups.mwe-popups-type-generic .mwe-popups-read-link,.mwe-popups.mwe-popups-type-disambiguation .mwe-popups-read-link{font-weight:bold;font-size:var(--font-size-x-small,0.75rem);text-decoration:none}.mwe-popups.mwe-popups-type-generic .mwe-popups-extract:hover + footer .mwe-popups-read-link,.mwe-popups.mwe-popups-type-disambiguation .mwe-popups-extract:hover + footer .mwe-popups-read-link,.mwe-popups.mwe-popups-type-generic .mwe-popups-read-link:hover,.mwe-popups.mwe-popups-type-disambiguation .mwe-popups-read-link:hover{text-decoration:underline}.mwe-popups-overlay{background-color:var(--background-color-backdrop-light,rgba(255,255,255,0.65));z-index:999;position:fixed;height:100%;width:100%;top:0;bottom:0;left:0;right:0;display:flex;justify-content:center;align-items:center}#mwe-popups-svg{position:absolute;top:-1000px}.popups-icon{min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}.popups-icon--size-small{min-width:10px;min-height:10px;width:var(--font-size-medium,1rem);height:var(--font-size-medium,1rem)}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--size-small{background-position:center;background-repeat:no-repeat; background-size:calc(max(var(--font-size-medium,1rem),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--size-small{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(var(--font-size-medium,1rem),10px));mask-size:calc(max(var(--font-size-medium,1rem),10px)); }}.mwe-popups-overlay .cdx-button.cdx-button--icon-only span + span,.mwe-popups .cdx-button.cdx-button--icon-only span + span{display:block;position:absolute !important; clip:rect(1px,1px,1px,1px);width:1px;height:1px;margin:-1px;border:0;padding:0;overflow:hidden}.cdx-button{display:inline-flex;align-items:center;justify-content:center;gap:6px;box-sizing:border-box;min-height:32px;max-width:28rem;margin:0;border-width:1px;border-style:solid;border-radius:2px;padding-right:11px;padding-left:11px;font-family:inherit;font-size:var(--font-size-medium,1rem);font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-transform:none;transition-property:background-color,color,border-color,box-shadow;transition-duration:.1s}.cdx-button--size-small{gap:4px;min-height:1.5rem;padding-right:5px;padding-left:5px}.cdx-button--size-large{min-height:44px;padding-right:15px;padding-left:15px}.cdx-button--icon-only{min-width:32px;padding-right:0;padding-left:0}.cdx-button--icon-only.cdx-button--size-small{min-width:1.5rem}.cdx-button--icon-only.cdx-button--size-large{min-width:44px}.cdx-button::-moz-focus-inner{border:0;padding:0}.cdx-button .cdx-button\_\_icon,.cdx-button .cdx-icon{vertical-align:middle}.cdx-button .cdx-icon{color:inherit}.cdx-button--fake-button,.cdx-button--fake-button:hover,.cdx-button--fake-button:focus{text-decoration:none}.cdx-button:enabled,.cdx-button.cdx-button--fake-button--enabled{background-color:var(--background-color-interactive-subtle,#f8f9fa);color:var(--color-neutral,#404244);border-color:var(--border-color-interactive,#72777d)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled .cdx-button\_\_icon{background-color:var(--color-neutral,#404244)}}.cdx-button:enabled:hover,.cdx-button.cdx-button--fake-button--enabled:hover{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);border-color:var(--border-color-interactive--hover,#27292d);cursor:pointer}.cdx-button:enabled:active,.cdx-button.cdx-button--fake-button--enabled:active,.cdx-button:enabled.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--is-active{background-color:var(--background-color-interactive-subtle--active,#dadde3);border-color:var(--border-color-interactive--active,#202122)}.cdx-button:enabled:focus,.cdx-button.cdx-button--fake-button--enabled:focus{outline:1px solid transparent}.cdx-button:enabled:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c)}.cdx-button:enabled.cdx-button--action-progressive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive{background-color:var(--background-color-progressive-subtle,#e8eeff);color:var(--color-progressive,#36c);border-color:var(--border-color-progressive,#6485d1)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-progressive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive .cdx-button\_\_icon{background-color:var(--color-progressive,#36c)}}.cdx-button:enabled.cdx-button--action-progressive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:hover{background-color:var(--background-color-progressive-subtle--hover,#d9e2ff);color:var(--color-progressive--hover,#3056a9);border-color:var(--border-color-progressive--hover,#3056a9)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-progressive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:hover .cdx-button\_\_icon{background-color:var(--color-progressive--hover,#3056a9)}}.cdx-button:enabled.cdx-button--action-progressive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:active,.cdx-button:enabled.cdx-button--action-progressive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive.cdx-button--is-active{background-color:var(--background-color-progressive-subtle--active,#b6d4fb);color:var(--color-progressive--active,#233566);border-color:var(--border-color-progressive--active,#233566)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-progressive--active,#233566)}}.cdx-button:enabled.cdx-button--action-destructive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive{background-color:var(--background-color-destructive-subtle,#ffe9e5);color:var(--color-destructive,#bf3c2c);border-color:var(--border-color-destructive,#f54739)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-destructive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive .cdx-button\_\_icon{background-color:var(--color-destructive,#bf3c2c)}}.cdx-button:enabled.cdx-button--action-destructive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:hover{background-color:var(--background-color-destructive-subtle--hover,#ffdad3);color:var(--color-destructive--hover,#9f3526);border-color:var(--border-color-destructive--hover,#9f3526)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-destructive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:hover .cdx-button\_\_icon{background-color:var(--color-destructive--hover,#9f3526)}}.cdx-button:enabled.cdx-button--action-destructive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:active,.cdx-button:enabled.cdx-button--action-destructive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive.cdx-button--is-active{background-color:var(--background-color-destructive-subtle--active,#ffc8bd);color:var(--color-destructive--active,#612419);border-color:var(--border-color-destructive--active,#612419)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-destructive--active,#612419)}}.cdx-button:enabled.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-destructive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-destructive--focus,#36c)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive{background-color:var(--background-color-progressive,#36c);color:var(--color-inverted-fixed,#fff);border-color:var(--border-color-transparent,transparent)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive:hover{background-color:var(--background-color-progressive--hover,#3056a9)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive:active,.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive.cdx-button--is-active{background-color:var(--background-color-progressive--active,#233566)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c),inset 0 0 0 2px var(--box-shadow-color-inverted,#fff)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-progressive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-progressive .cdx-button\_\_icon{background-color:var(--color-inverted-fixed,#fff)}}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive{background-color:var(--background-color-destructive,#bf3c2c);color:var(--color-inverted-fixed,#fff);border-color:var(--border-color-transparent,transparent)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive:hover{background-color:var(--background-color-destructive--hover,#9f3526)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive:active,.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive.cdx-button--is-active{background-color:var(--background-color-destructive--active,#612419)}.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-destructive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-destructive--focus,#36c),inset 0 0 0 2px var(--box-shadow-color-inverted,#fff)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-primary.cdx-button--action-destructive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-primary.cdx-button--action-destructive .cdx-button\_\_icon{background-color:var(--color-inverted-fixed,#fff)}}.cdx-button:enabled.cdx-button--weight-quiet,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet{background-color:var(--background-color-transparent,transparent);border-color:var(--border-color-transparent,transparent)}.cdx-button:enabled.cdx-button--weight-quiet:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet:hover{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);mix-blend-mode:var(--mix-blend-mode-blend,multiply)}.cdx-button:enabled.cdx-button--weight-quiet:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet:active,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--is-active{background-color:var(--background-color-interactive-subtle--active,#dadde3)}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive{color:var(--color-progressive,#36c)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive .cdx-button\_\_icon{background-color:var(--color-progressive,#36c)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover{background-color:var(--background-color-progressive-subtle--hover,#d9e2ff);color:var(--color-progressive--hover,#3056a9);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:hover .cdx-button\_\_icon{background-color:var(--color-progressive--hover,#3056a9)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active{background-color:var(--background-color-progressive-subtle--active,#b6d4fb);color:var(--color-progressive--active,#233566);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-progressive--active,#233566)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-progressive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c)}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive{color:var(--color-destructive,#bf3c2c)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive .cdx-button\_\_icon{background-color:var(--color-destructive,#bf3c2c)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover{background-color:var(--background-color-destructive-subtle--hover,#ffdad3);color:var(--color-destructive--hover,#9f3526);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:hover .cdx-button\_\_icon{background-color:var(--color-destructive--hover,#9f3526)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active{background-color:var(--background-color-destructive-subtle--active,#ffc8bd);color:var(--color-destructive--active,#612419);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:active .cdx-button\_\_icon,.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive.cdx-button--is-active .cdx-button\_\_icon{background-color:var(--color-destructive--active,#612419)}}.cdx-button:enabled.cdx-button--weight-quiet.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active),.cdx-button.cdx-button--fake-button--enabled.cdx-button--weight-quiet.cdx-button--action-destructive:focus:not(:active):not(.cdx-button--is-active){border-color:var(--border-color-destructive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-destructive--focus,#36c)}.cdx-button:disabled,.cdx-button.cdx-button--fake-button--disabled{background-color:var(--background-color-disabled,#dadde3);color:var(--color-disabled-emphasized,#a2a9b1);border-color:var(--border-color-transparent,transparent)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:disabled .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--disabled .cdx-button\_\_icon{background-color:var(--color-inverted,#fff)}}.cdx-button:disabled.cdx-button--weight-quiet,.cdx-button.cdx-button--fake-button--disabled.cdx-button--weight-quiet{background-color:var(--background-color-transparent,transparent);color:var(--color-disabled,#a2a9b1)}@supports ((-webkit-mask-image:none) or (mask-image:none)){.cdx-button:disabled.cdx-button--weight-quiet .cdx-button\_\_icon,.cdx-button.cdx-button--fake-button--disabled.cdx-button--weight-quiet .cdx-button\_\_icon{background-color:var(--color-disabled,#a2a9b1)}}.cdx-icon{color:var(--color-base,#202122);display:inline-flex;align-items:center;justify-content:center;vertical-align:text-bottom}.cdx-icon svg{fill:currentcolor;width:100%;height:100%}.cdx-icon--x-small{min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) - 4px);height:calc(var(--font-size-medium,1rem) - 4px)}.cdx-icon--small{min-width:14px;min-height:14px;width:var(--font-size-medium,1rem);height:var(--font-size-medium,1rem)}.cdx-icon--medium{min-width:18px;min-height:18px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px)}.cdx-icon--flipped svg{transform:scaleX(-1)}.cdx-label{display:flex;flex-direction:column;font-size:var(--font-size-medium,1rem);line-height:var(--line-height-small,1.375rem)}.cdx-label\_\_label\_\_icon.cdx-icon{color:var(--color-subtle,#54595d);margin-right:4px}.cdx-label\_\_label\_\_text{font-weight:700}legend.cdx-label{padding:0}fieldset label.cdx-label\_\_label .cdx-label\_\_label\_\_text{font-weight:400}.cdx-label:not(.cdx-label--disabled) .cdx-label\_\_label\_\_optional-flag,.cdx-label:not(.cdx-label--disabled) .cdx-label\_\_description{color:var(--color-subtle,#54595d)}.cdx-label--disabled,.cdx-label--disabled .cdx-label\_\_label\_\_icon{color:var(--color-disabled,#a2a9b1)}.cdx-label--visually-hidden{display:block;clip:rect(1px,1px,1px,1px);position:absolute!important;width:1px;height:1px;margin:-1px;border:0;padding:0;overflow:hidden}.cdx-label:not(.cdx-label--visually-hidden){padding-bottom:4px}.cdx-checkbox{position:relative;min-width:20px;min-height:20px}.cdx-checkbox\_\_wrapper{display:flex}.cdx-checkbox:not(.cdx-checkbox--inline){display:flex;flex-direction:column;margin-bottom:6px}.cdx-checkbox:not(.cdx-checkbox--inline):last-child{margin-bottom:0}.cdx-checkbox--inline{display:inline-flex;margin-right:16px;white-space:nowrap}.cdx-checkbox--inline:last-child{margin-right:0}.cdx-checkbox\_\_label,.cdx-checkbox\_\_label.cdx-label{display:inline-flex;position:relative;z-index:0;padding-left:calc(var(--font-size-medium,1rem) + 10px)}.cdx-checkbox\_\_label.cdx-label{padding-bottom:0}.cdx-checkbox\_\_label.cdx-label .cdx-label\_\_label\_\_text{font-weight:400}.cdx-checkbox--inline .cdx-checkbox\_\_label{display:inline}.cdx-checkbox\_\_icon{background-color:var(--background-color-base-fixed,#fff);position:absolute;left:0;box-sizing:border-box;min-width:18px;min-height:18px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);margin-top:1px;border-width:1px;border-style:solid;transition-property:background-color,color,border-color,box-shadow;transition-duration:.1s}.cdx-checkbox\_\_input{opacity:0;position:absolute;left:0;z-index:1;min-width:20px;min-height:20px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);margin:1px 0 0;font-size:var(--font-size-medium,1rem);cursor:inherit}.cdx-checkbox\_\_wrapper:hover>.cdx-checkbox\_\_input:enabled,.cdx-checkbox\_\_wrapper:hover>.cdx-checkbox\_\_input:enabled~.cdx-label .cdx-label\_\_label,.cdx-checkbox\_\_wrapper:hover>.cdx-checkbox\_\_input:enabled~.cdx-checkbox\_\_label:not(.cdx-label){cursor:pointer}.cdx-checkbox\_\_custom-input:not(.cdx-checkbox\_\_custom-input--inline){padding-top:6px;padding-left:calc(var(--font-size-medium,1rem) + 10px)}.cdx-checkbox\_\_icon{border-radius:2px}.cdx-checkbox\_\_input:indeterminate+.cdx-checkbox\_\_icon:before{content:" ";background-color:var(--background-color-base-fixed,#fff);position:absolute;top:calc(50% - .5px);right:3px;left:3px;height:2px}.cdx-checkbox\_\_input:checked:not(:indeterminate)+.cdx-checkbox\_\_icon:before{content:" ";display:block;width:.25rem;height:calc(100% - 6px);margin:0 auto 4px;border-right-width:2px;border-right-style:solid;border-bottom-width:2px;border-bottom-style:solid;transform:rotate(45deg)}.cdx-checkbox\_\_input:enabled+.cdx-checkbox\_\_icon{background-color:var(--background-color-base,#fff);border-color:var(--border-color-interactive,#72777d)}.cdx-checkbox\_\_input:enabled:hover+.cdx-checkbox\_\_icon{background-color:var(--background-color-interactive-subtle--hover,#eaecf0);border-color:var(--border-color-interactive--hover,#27292d)}.cdx-checkbox\_\_input:enabled:focus:not(:active)+.cdx-checkbox\_\_icon{border-color:var(--border-color-progressive--focus,#36c);box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c);outline:1px solid transparent}.cdx-checkbox\_\_input:enabled:active+.cdx-checkbox\_\_icon{background-color:var(--background-color-interactive-subtle--active,#dadde3);border-color:var(--border-color-interactive--active,#202122)}.cdx-checkbox\_\_input:enabled:checked+.cdx-checkbox\_\_icon,.cdx-checkbox\_\_input:enabled:indeterminate+.cdx-checkbox\_\_icon{background-color:var(--background-color-progressive,#36c);border-color:var(--border-color-transparent,transparent)}.cdx-checkbox\_\_input:enabled:checked:hover+.cdx-checkbox\_\_icon,.cdx-checkbox\_\_input:enabled:indeterminate:hover+.cdx-checkbox\_\_icon{background-color:var(--background-color-progressive--hover,#3056a9)}.cdx-checkbox\_\_input:enabled:checked:focus:not(:active):not(:hover)+.cdx-checkbox\_\_icon,.cdx-checkbox\_\_input:enabled:indeterminate:focus:not(:active):not(:hover)+.cdx-checkbox\_\_icon{background-color:var(--background-color-progressive,#36c)}.cdx-checkbox\_\_input:enabled:checked:focus:not(:active)+.cdx-checkbox\_\_icon,.cdx-checkbox\_\_input:enabled:indeterminate:focus:not(:active)+.cdx-checkbox\_\_icon{box-shadow:inset 0 0 0 1px var(--box-shadow-color-progressive--focus,#36c),inset 0 0 0 2px var(--box-shadow-color-inverted,#fff)}.cdx-checkbox\_\_input:enabled:checked:active+.cdx-checkbox\_\_icon,.cdx-checkbox\_\_input:enabled:indeterminate:active+.cdx-checkbox\_\_icon{background-color:var(--background-color-progressive--active,#233566)}.cdx-checkbox\_\_input:enabled:checked:not(:indeterminate)+.cdx-checkbox\_\_icon:before{border-color:var(--border-color-inverted-fixed,#fff)}.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled~.cdx-checkbox\_\_label{color:var(--color-error,#bf3c2c)}.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled+.cdx-checkbox\_\_icon{background-color:var(--background-color-error-subtle,#ffe9e5);border-color:var(--border-color-error,#f54739)}.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:hover+.cdx-checkbox\_\_icon{background-color:var(--background-color-error-subtle--hover,#ffdad3);border-color:var(--border-color-error--hover,#9f3526)}.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:focus+.cdx-checkbox\_\_icon{border-color:var(--border-color-progressive--focus,#36c)}.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:active+.cdx-checkbox\_\_icon{background-color:var(--background-color-error-subtle--active,#ffc8bd);border-color:var(--border-color-error--active,#612419)}.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:checked+.cdx-checkbox\_\_icon,.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:indeterminate+.cdx-checkbox\_\_icon{background-color:var(--background-color-error,#f54739);border-color:var(--border-color-transparent,transparent)}.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:checked:hover+.cdx-checkbox\_\_icon,.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:indeterminate:hover+.cdx-checkbox\_\_icon{background-color:var(--background-color-error--hover,#d74032)}.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:checked:active+.cdx-checkbox\_\_icon,.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:indeterminate:active+.cdx-checkbox\_\_icon{background-color:var(--background-color-error--active,#bf3c2c)}.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:checked:focus:not(:active)+.cdx-checkbox\_\_icon,.cdx-checkbox--status-error .cdx-checkbox\_\_input:enabled:indeterminate:focus:not(:active)+.cdx-checkbox\_\_icon{background-color:var(--background-color-error,#f54739);border-color:var(--border-color-progressive--focus,#36c)}.cdx-checkbox\_\_input:disabled+.cdx-checkbox\_\_icon{background-color:var(--background-color-disabled-subtle,#eaecf0);border-color:var(--border-color-disabled,#c8ccd1)}.cdx-checkbox\_\_input:disabled:checked+.cdx-checkbox\_\_icon,.cdx-checkbox\_\_input:disabled:indeterminate+.cdx-checkbox\_\_icon{background-color:var(--background-color-disabled,#dadde3);border-color:var(--border-color-transparent,transparent)}.cdx-checkbox\_\_input:disabled:checked:not(:indeterminate)+.cdx-checkbox\_\_icon:before{border-right-color:var(--color-disabled,#a2a9b1);border-bottom-color:var(--color-disabled,#a2a9b1)}.cdx-checkbox\_\_input:disabled:indeterminate+.cdx-checkbox\_\_icon:before{background-color:var(--color-disabled-emphasized,#a2a9b1)}.cdx-checkbox\_\_input:disabled~.cdx-checkbox\_\_label,.cdx-checkbox\_\_input:disabled~.cdx-checkbox\_\_label.cdx-label{color:var(--color-disabled,#a2a9b1)}
.ve-active .ve-init-mw-desktopArticleTarget-targetContainer #siteNotice,.ve-active .mw-indicators,.ve-active #t-print,.ve-active #t-permalink,.ve-active #p-coll-print\_export,.ve-active #t-cite,.ve-active .ve-init-mw-desktopArticleTarget-editableContent,.ve-active .ve-init-mw-tempWikitextEditorWidget{display:none}.ve-deactivating .ve-ui-surface{display:none}.ve-activating{ }.ve-activating .ve-ui-surface{height:0;padding:0 !important; overflow:hidden} .ve-loading .ve-init-mw-desktopArticleTarget-targetContainer > :not(.ve-init-mw-desktopArticleTarget-toolbarPlaceholder):not(.ve-init-mw-desktopArticleTarget),.ve-loading .ve-init-mw-desktopArticleTarget-originalContent,.ve-activated:not(.ve-loading) .ve-init-mw-desktopArticleTarget-uneditableContent{pointer-events:none;-webkit-user-select:none;-moz-user-select:none;user-select:none;opacity:0.5}.ve-activated .ve-init-mw-desktopArticleTarget-targetContainer #firstHeading{ -webkit-user-select:text;-moz-user-select:text;user-select:text;pointer-events:auto;cursor:text}.ve-activated .ve-init-mw-desktopArticleTarget-targetContainer #firstHeading a{ pointer-events:none}.ve-activated .ve-init-mw-desktopArticleTarget-originalContent #catlinks{cursor:pointer}.ve-activated .ve-init-mw-desktopArticleTarget-originalContent #catlinks:hover{ background:rgba(109,169,247,0.15)}.ve-activated .ve-init-mw-desktopArticleTarget-originalContent #catlinks a{opacity:1} .ve-init-mw-desktopArticleTarget-loading-overlay{z-index:2;position:absolute;width:100%;top:1em}.ve-init-mw-desktopArticleTarget-toolbarPlaceholder{-webkit-position:sticky;position:sticky;top:0;z-index:2;overflow:hidden;transition:height 250ms ease;height:0;padding-bottom:2px; }.ve-init-mw-desktopArticleTarget-toolbarPlaceholder-bar{background:var(--background-color-base,#fff);transform:translateY(-100%);transition:transform 250ms ease}.ve-init-mw-desktopArticleTarget-toolbarPlaceholder-open .ve-init-mw-desktopArticleTarget-toolbarPlaceholder-bar{transform:translateY(0)} .oo-ui-element-hidden{display:none !important; } .ve-init-mw-desktopArticleTarget-categoryEdit{float:right;margin-top:1ex} .ve-init-mw-desktopArticleTarget-toolbarPlaceholder-bar{height:42px;border-bottom:1px solid #c8ccd1;box-shadow:0 1px 1px 0 rgba(0,0,0,0.1)}.ve-init-mw-desktopArticleTarget-toolbarPlaceholder-open{height:42px} .ve-activated .vector-toc,.ve-activated .vector-page-titlebar-toc{display:none}.ve-init-mw-desktopArticleTarget-toolbar,.ve-init-mw-desktopArticleTarget-toolbarPlaceholder,.ve-ui-overlay-local,.ve-ui-overlay-global,.ve-ui-sidebarDialogWindowManager,.ve-ce-surface-interface{font-size:0.875rem}.ve-ce-surface-interface{font-family:sans-serif}.ve-init-mw-desktopArticleTarget-toolbarPlaceholder-bar,.ve-init-mw-desktopArticleTarget-toolbar.ve-ui-toolbar > .oo-ui-toolbar-bar{box-shadow:0 2px 1px -1px rgba(0,0,0,0.1)}.ve-ui-mwSaveDialog-preview .mw-body{ }.ve-ui-mwSaveDialog-preview .mw-body .firstHeading{grid-area:titlebar}.ve-ui-mwSaveDialog-preview .mw-body .mw-body-content{grid-area:content;font-size:var(--font-size-medium);line-height:var(--line-height-content)}.ve-ui-mwSaveDialog-preview .mw-content-container{max-width:960px;margin:0 auto}.ve-init-mw-desktopArticleTarget .ve-init-mw-target-surface > .ve-ce-surface .ve-ce-attachedRootNode{min-height:15em}.ve-init-mw-desktopArticleTarget-toolbar .ve-ui-toolbarDialog-position-above.ve-ui-toolbarDialog-padded .oo-ui-window-body,.ve-init-mw-desktopArticleTarget-toolbar .ve-ui-toolbarDialog-position-below.ve-ui-toolbarDialog-padded .oo-ui-window-body{padding-left:0;padding-right:0}.ve-init-mw-desktopArticleTarget-toolbar .ve-ui-toolbarDialog-position-side.ve-ui-toolbarDialog-padded .oo-ui-window-body{padding-right:0}
.popups-icon--reference-generic{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-generic{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-generic{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-generic{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"m15 10-2.78-2.78L9.44 10V1H5a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V3a2 2 0 00-2-2z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-generic{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"m15 10-2.78-2.78L9.44 10V1H5a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V3a2 2 0 00-2-2z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"m15 10-2.78-2.78L9.44 10V1H5a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V3a2 2 0 00-2-2z\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--reference-book{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-book{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-book{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-book{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M15 2a7.65 7.65 0 00-5 2 7.65 7.65 0 00-5-2H1v15h4a7.65 7.65 0 015 2 7.65 7.65 0 015-2h4V2zm2.5 13.5H14a4.38 4.38 0 00-3 1V5s1-1.5 4-1.5h2.5z\"/><path d=\"M9 3.5h2v1H9z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-book{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M15 2a7.65 7.65 0 00-5 2 7.65 7.65 0 00-5-2H1v15h4a7.65 7.65 0 015 2 7.65 7.65 0 015-2h4V2zm2.5 13.5H14a4.38 4.38 0 00-3 1V5s1-1.5 4-1.5h2.5z\"/><path d=\"M9 3.5h2v1H9z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M15 2a7.65 7.65 0 00-5 2 7.65 7.65 0 00-5-2H1v15h4a7.65 7.65 0 015 2 7.65 7.65 0 015-2h4V2zm2.5 13.5H14a4.38 4.38 0 00-3 1V5s1-1.5 4-1.5h2.5z\"/><path d=\"M9 3.5h2v1H9z\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--reference-book[dir='rtl'],html[dir='rtl'] .popups-icon--reference-book:not([dir='ltr']){transform:scaleX(-1)}.popups-icon--reference-journal{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-journal{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-journal{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-journal{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M2 18.5A1.5 1.5 0 003.5 20H5V0H3.5A1.5 1.5 0 002 1.5zM6 0v20h10a2 2 0 002-2V2a2 2 0 00-2-2zm7 8H8V7h5zm3-2H8V5h8z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-journal{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M2 18.5A1.5 1.5 0 003.5 20H5V0H3.5A1.5 1.5 0 002 1.5zM6 0v20h10a2 2 0 002-2V2a2 2 0 00-2-2zm7 8H8V7h5zm3-2H8V5h8z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M2 18.5A1.5 1.5 0 003.5 20H5V0H3.5A1.5 1.5 0 002 1.5zM6 0v20h10a2 2 0 002-2V2a2 2 0 00-2-2zm7 8H8V7h5zm3-2H8V5h8z\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--reference-journal[dir='rtl'],html[dir='rtl'] .popups-icon--reference-journal:not([dir='ltr']){transform:scaleX(-1)}.popups-icon--reference-news{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-news{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-news{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-news{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M5 2a2 2 0 00-2 2v12a1 1 0 01-1-1V5h-.5A1.5 1.5 0 000 6.5v10A1.5 1.5 0 001.5 18H18a2 2 0 002-2V4a2 2 0 00-2-2zm1 2h11v4H6zm0 6h6v1H6zm0 2h6v1H6zm0 2h6v1H6zm7-4h4v5h-4z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-news{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M5 2a2 2 0 00-2 2v12a1 1 0 01-1-1V5h-.5A1.5 1.5 0 000 6.5v10A1.5 1.5 0 001.5 18H18a2 2 0 002-2V4a2 2 0 00-2-2zm1 2h11v4H6zm0 6h6v1H6zm0 2h6v1H6zm0 2h6v1H6zm7-4h4v5h-4z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M5 2a2 2 0 00-2 2v12a1 1 0 01-1-1V5h-.5A1.5 1.5 0 000 6.5v10A1.5 1.5 0 001.5 18H18a2 2 0 002-2V4a2 2 0 00-2-2zm1 2h11v4H6zm0 6h6v1H6zm0 2h6v1H6zm0 2h6v1H6zm7-4h4v5h-4z\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--reference-news[dir='rtl'],html[dir='rtl'] .popups-icon--reference-news:not([dir='ltr']){transform:scaleX(-1)}.popups-icon--reference-map{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-map{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-map{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-map{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M13 3 7 1 1 3v16l6-2 6 2 6-2V1zM7 14.89l-4 1.36V4.35L7 3zm10 .75L13 17V5.1l4-1.36z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-map{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M13 3 7 1 1 3v16l6-2 6 2 6-2V1zM7 14.89l-4 1.36V4.35L7 3zm10 .75L13 17V5.1l4-1.36z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M13 3 7 1 1 3v16l6-2 6 2 6-2V1zM7 14.89l-4 1.36V4.35L7 3zm10 .75L13 17V5.1l4-1.36z\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--reference-map[dir='rtl'],html[dir='rtl'] .popups-icon--reference-map:not([dir='ltr']){transform:scaleX(-1)}.popups-icon--reference-web{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-web{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-web{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--reference-web{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M2 2a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V4a2 2 0 00-2-2zm2 1.5A1.5 1.5 0 112.5 5 1.5 1.5 0 014 3.5M18 16H2V8h16z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--reference-web{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M2 2a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V4a2 2 0 00-2-2zm2 1.5A1.5 1.5 0 112.5 5 1.5 1.5 0 014 3.5M18 16H2V8h16z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M2 2a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V4a2 2 0 00-2-2zm2 1.5A1.5 1.5 0 112.5 5 1.5 1.5 0 014 3.5M18 16H2V8h16z\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--reference-web[dir='rtl'],html[dir='rtl'] .popups-icon--reference-web:not([dir='ltr']){transform:scaleX(-1)}.popups-icon--preview-disambiguation{ min-width:10px;min-height:10px;width:calc(var(--font-size-medium,1rem) + 4px);height:calc(var(--font-size-medium,1rem) + 4px);display:inline-block;vertical-align:text-bottom}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--preview-disambiguation{background-position:center;background-repeat:no-repeat; background-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px))}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--preview-disambiguation{ -webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px));mask-size:calc(max(calc(var(--font-size-medium,1rem) + 4px),10px)); }}@supports not ((-webkit-mask-image:none) or (mask-image:none)){.popups-icon--preview-disambiguation{background-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M7 0a2 2 0 00-2 2h9a2 2 0 012 2v12a2 2 0 002-2V2a2 2 0 00-2-2z\"/><path d=\"M13 20a2 2 0 002-2V5a2 2 0 00-2-2H4a2 2 0 00-2 2v13a2 2 0 002 2zM9 5h4v5H9zM4 5h4v1H4zm0 2h4v1H4zm0 2h4v1H4zm0 2h9v1H4zm0 2h9v1H4zm0 2h9v1H4z\"/></svg>");filter:invert(var(--filter-invert-icon,0));opacity:var(--opacity-icon-base,0.87)}}@supports (-webkit-mask-image:none) or (mask-image:none){.popups-icon--preview-disambiguation{ -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M7 0a2 2 0 00-2 2h9a2 2 0 012 2v12a2 2 0 002-2V2a2 2 0 00-2-2z\"/><path d=\"M13 20a2 2 0 002-2V5a2 2 0 00-2-2H4a2 2 0 00-2 2v13a2 2 0 002 2zM9 5h4v5H9zM4 5h4v1H4zm0 2h4v1H4zm0 2h4v1H4zm0 2h9v1H4zm0 2h9v1H4zm0 2h9v1H4z\"/></svg>"); mask-image:url("data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"%23000\"><path d=\"M7 0a2 2 0 00-2 2h9a2 2 0 012 2v12a2 2 0 002-2V2a2 2 0 00-2-2z\"/><path d=\"M13 20a2 2 0 002-2V5a2 2 0 00-2-2H4a2 2 0 00-2 2v13a2 2 0 002 2zM9 5h4v5H9zM4 5h4v1H4zm0 2h4v1H4zm0 2h4v1H4zm0 2h9v1H4zm0 2h9v1H4zm0 2h9v1H4z\"/></svg>");background-color:var(--color-base,#202122)}}.popups-icon--preview-disambiguation[dir='rtl'],html[dir='rtl'] .popups-icon--preview-disambiguation:not([dir='ltr']){transform:scaleX(-1)} #mw-content-text .reference a[href\*='#'] \*{pointer-events:none}.mwe-popups.mwe-popups-type-reference .mwe-popups-container .mwe-popups-title .popups-icon--reference-note{display:none}.mwe-popups.mwe-popups-type-reference .mwe-popups-container .mwe-popups-extract{margin-right:0;max-height:inherit}.mwe-popups.mwe-popups-type-reference .mwe-popups-container .mwe-popups-extract .mwe-popups-scroll{max-height:343px;overflow:auto;padding-right:16px}.mwe-popups.mwe-popups-type-reference .mwe-popups-container .mwe-popups-extract .mw-parser-output{overflow-wrap:break-word}.mwe-popups.mwe-popups-type-reference .mwe-popups-container .mwe-popups-extract::after{display:none}.mwe-popups.mwe-popups-type-reference .mwe-popups-container .mwe-popups-extract .mwe-popups-fade{position:absolute;width:100%;height:20px;background-color:transparent;background-image:linear-gradient(rgba(255,255,255,0),#ffffff);opacity:0;pointer-events:none;transition:opacity 250ms ease}.mwe-popups.mwe-popups-type-reference .mwe-popups-container .mwe-popups-extract.mwe-popups-fade-out .mwe-popups-fade{opacity:1}.mwe-popups.mwe-popups-type-reference .mwe-popups-container .mwe-collapsible-placeholder{font-weight:bold;margin:1em 0;position:relative}.mwe-popups.mwe-popups-type-reference .mwe-popups-container .mw-reference-previews-parent{margin-bottom:1em}

[Jump to content](#bodyContent)

Main menu

Main menu

move to sidebar
```

**colly+md**
```
Common Language Runtime - Wikipedia
(function(){var className="client-js vector-feature-language-in-header-enabled vector-feature-language-in-main-menu-disabled vector-feature-language-in-main-page-header-disabled vector-feature-page-tools-pinned-disabled vector-feature-toc-pinned-clientpref-1 vector-feature-main-menu-pinned-disabled vector-feature-limited-width-clientpref-1 vector-feature-limited-width-content-enabled vector-feature-custom-font-size-clientpref-1 vector-feature-appearance-pinned-clientpref-1 skin-theme-clientpref-day vector-sticky-header-enabled vector-toc-available skin-theme-clientpref-thumb-standard";var cookie=document.cookie.match(/(?:^|; )enwikimwclientpreferences=([^;]+)/);if(cookie){cookie[1].split('%2C').forEach(function(pref){className=className.replace(new RegExp('(^| )'+pref.replace(/-clientpref-\w+$|[^\w-]+/g,'')+'-clientpref-\\w+( |$)'),'$1'+pref+'$2');});}document.documentElement.className=className;}());RLCONF={"wgBreakFrames":false,"wgSeparatorTransformTable":["",""],"wgDigitTransformTable":["",""],"wgDefaultDateFormat":"dmy","wgMonthNames":["","January","February","March","April","May","June","July","August","September","October","November","December"],"wgRequestId":"5db3c8d3-dd97-4df7-944c-ddf94314b59a","wgCanonicalNamespace":"","wgCanonicalSpecialPageName":false,"wgNamespaceNumber":0,"wgPageName":"Common\_Language\_Runtime","wgTitle":"Common Language Runtime","wgCurRevisionId":1317322509,"wgRevisionId":1317322509,"wgArticleId":46003,"wgIsArticle":true,"wgIsRedirect":false,"wgAction":"view","wgUserName":null,"wgUserGroups":["\*"],"wgCategories":["Articles with short description","Short description matches Wikidata","Articles lacking reliable references from March 2019","All articles lacking reliable references","Articles needing additional references from September 2014","All articles needing additional references","Articles with multiple maintenance issues",".NET Framework terminology","Stack-based virtual machines"],"wgPageViewLanguage":"en","wgPageContentLanguage":"en","wgPageContentModel":"wikitext","wgRelevantPageName":"Common\_Language\_Runtime","wgRelevantArticleId":46003,"wgTempUserName":null,"wgIsProbablyEditable":true,"wgRelevantPageIsProbablyEditable":true,"wgRestrictionEdit":[],"wgRestrictionMove":[],"wgNoticeProject":"wikipedia","wgFlaggedRevsParams":{"tags":{"status":{"levels":1}}},"wgConfirmEditCaptchaNeededForGenericEdit":"hcaptcha","wgConfirmEditHCaptchaVisualEditorOnLoadIntegrationEnabled":false,"wgConfirmEditHCaptchaSiteKey":"5d0c670e-a5f4-4258-ad16-1f42792c9c62","wgMediaViewerOnClick":true,"wgMediaViewerEnabledByDefault":true,"wgPopupsFlags":0,"wgVisualEditor":{"pageLanguageCode":"en","pageLanguageDir":"ltr","pageVariantFallbacks":"en"},"wgMFDisplayWikibaseDescriptions":{"search":true,"watchlist":true,"tagline":false,"nearby":true},"wgWMESchemaEditAttemptStepOversample":false,"wgWMEPageLength":4000,"wgEditSubmitButtonLabelPublish":true,"wgVisualEditorPageIsDisambiguation":false,"wgULSPosition":"interlanguage","wgULSisCompactLinksEnabled":false,"wgVector2022LanguageInHeader":true,"wgULSisLanguageSelectorEmpty":false,"wgWikibaseItemId":"Q733134","wgCheckUserClientHintsHeadersJsApi":["brands","architecture","bitness","fullVersionList","mobile","model","platform","platformVersion"],"GEHomepageSuggestedEditsEnableTopics":true,"wgGESuggestedEditsTaskTypes":{"taskTypes":["copyedit","link-recommendation"],"unavailableTaskTypes":[]},"wgGETopicsMatchModeEnabled":false,"wgGELevelingUpEnabledForUser":false,"wgTestKitchenUserExperiments":{"overrides":[],"enrolled":[],"assigned":[],"subject\_ids":[]}};
RLSTATE={"ext.globalCssJs.user.styles":"ready","site.styles":"ready","user.styles":"ready","ext.globalCssJs.user":"ready","user":"ready","user.options":"loading","ext.wikimediamessages.styles":"ready","ext.cite.styles":"ready","skins.vector.search.codex.styles":"ready","skins.vector.styles":"ready","skins.vector.icons":"ready","jquery.makeCollapsible.styles":"ready","ext.visualEditor.desktopArticleTarget.noscript":"ready","ext.uls.interlanguage":"ready","wikibase.client.init":"ready"};RLPAGEMODULES=["ext.parsermigration.survey","ext.cite.ux-enhancements","site","mediawiki.page.ready","jquery.makeCollapsible","skins.vector.js","ext.centralNotice.geoIP","ext.centralNotice.startUp","ext.gadget.ReferenceTooltips","ext.gadget.switcher","ext.urlShortener.toolbar","ext.centralauth.centralautologin","mmv.bootstrap","ext.popups","ext.visualEditor.desktopArticleTarget.init","ext.echo.centralauth","ext.eventLogging","ext.wikimediaEvents","ext.navigationTiming","ext.uls.interface","ext.cx.eventlogging.campaigns","ext.cx.uls.quick.actions","wikibase.client.vector-2022","wikibase.databox.fromWikidata","ext.checkUser.clientHints","ext.quicksurveys.init","ext.growthExperiments.SuggestedEditSession","ext.testKitchen"];
(RLQ=window.RLQ||[]).push(function(){mw.loader.impl(function(){return["user.options@12s5i",function($,jQuery,require,module){mw.user.tokens.set({"patrolToken":"+\\","watchToken":"+\\","csrfToken":"+\\"});
}];});});

[Jump to content](#bodyContent)

Main menu

Main menu

move to sidebar
hide

Navigation

* [Main page](/wiki/Main_Page "Visit the main page [z]")
* [Contents](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia")
* [Current events](/wiki/Portal:Current_events "Articles related to current events")
* [Random article](/wiki/Special:Random "Visit a randomly selected article [x]")
* [About Wikipedia](/wiki/Wikipedia:About "Learn about Wikipedia and how it works")
* [Contact us](//en.wikipedia.org/wiki/Wikipedia:Contact_us "How to contact Wikipedia")

Contribute

* [Help](/wiki/Help:Contents "Guidance on how to use and edit Wikipedia")
* [Learn to edit](/wiki/Help:Introduction "Learn how to edit Wikipedia")
* [Community portal](/wiki/Wikipedia:Community_portal "The hub for editors")
* [Recent changes](/wiki/Special:RecentChanges "A list of recent changes to Wikipedia [r]")
* [Upload file](/wiki/Wikipedia:File_upload_wizard "Add images or other media for use on Wikipedia")
* [Special pages](/wiki/Special:SpecialPages "A list of all special pages [q]")

[Search](/wiki/Special:Search "Search Wikipedia [f]")

Search

Appearance

* [Donate](https://donate.wikimedia.org/?wmf_source=donate&wmf_medium=sidebar&wmf_campaign=en.wikipedia.org&uselang=en)
```

**playwright**
```
Common Language Runtime - Wikipedia
(function(){var className="client-js vector-feature-language-in-header-enabled vector-feature-language-in-main-menu-disabled vector-feature-language-in-main-page-header-disabled vector-feature-page-tools-pinned-disabled vector-feature-toc-pinned-clientpref-1 vector-feature-main-menu-pinned-disabled vector-feature-limited-width-clientpref-1 vector-feature-limited-width-content-enabled vector-feature-custom-font-size-clientpref-1 vector-feature-appearance-pinned-clientpref-1 skin-theme-clientpref-day vector-sticky-header-enabled vector-toc-available skin-theme-clientpref-thumb-standard";var cookie=document.cookie.match(/(?:^|; )enwikimwclientpreferences=([^;]+)/);if(cookie){cookie[1].split('%2C').forEach(function(pref){className=className.replace(new RegExp('(^| )'+pref.replace(/-clientpref-\w+$|[^\w-]+/g,'')+'-clientpref-\\w+( |$)'),'$1'+pref+'$2');});}document.documentElement.className=className;}());RLCONF={"wgBreakFrames":false,"wgSeparatorTransformTable":["",""],"wgDigitTransformTable":["",""],"wgDefaultDateFormat":"dmy","wgMonthNames":["","January","February","March","April","May","June","July","August","September","October","November","December"],"wgRequestId":"5db3c8d3-dd97-4df7-944c-ddf94314b59a","wgCanonicalNamespace":"","wgCanonicalSpecialPageName":false,"wgNamespaceNumber":0,"wgPageName":"Common\_Language\_Runtime","wgTitle":"Common Language Runtime","wgCurRevisionId":1317322509,"wgRevisionId":1317322509,"wgArticleId":46003,"wgIsArticle":true,"wgIsRedirect":false,"wgAction":"view","wgUserName":null,"wgUserGroups":["\*"],"wgCategories":["Articles with short description","Short description matches Wikidata","Articles lacking reliable references from March 2019","All articles lacking reliable references","Articles needing additional references from September 2014","All articles needing additional references","Articles with multiple maintenance issues",".NET Framework terminology","Stack-based virtual machines"],"wgPageViewLanguage":"en","wgPageContentLanguage":"en","wgPageContentModel":"wikitext","wgRelevantPageName":"Common\_Language\_Runtime","wgRelevantArticleId":46003,"wgTempUserName":null,"wgIsProbablyEditable":true,"wgRelevantPageIsProbablyEditable":true,"wgRestrictionEdit":[],"wgRestrictionMove":[],"wgNoticeProject":"wikipedia","wgFlaggedRevsParams":{"tags":{"status":{"levels":1}}},"wgConfirmEditCaptchaNeededForGenericEdit":"hcaptcha","wgConfirmEditHCaptchaVisualEditorOnLoadIntegrationEnabled":false,"wgConfirmEditHCaptchaSiteKey":"5d0c670e-a5f4-4258-ad16-1f42792c9c62","wgMediaViewerOnClick":true,"wgMediaViewerEnabledByDefault":true,"wgPopupsFlags":0,"wgVisualEditor":{"pageLanguageCode":"en","pageLanguageDir":"ltr","pageVariantFallbacks":"en"},"wgMFDisplayWikibaseDescriptions":{"search":true,"watchlist":true,"tagline":false,"nearby":true},"wgWMESchemaEditAttemptStepOversample":false,"wgWMEPageLength":4000,"wgEditSubmitButtonLabelPublish":true,"wgVisualEditorPageIsDisambiguation":false,"wgULSPosition":"interlanguage","wgULSisCompactLinksEnabled":false,"wgVector2022LanguageInHeader":true,"wgULSisLanguageSelectorEmpty":false,"wgWikibaseItemId":"Q733134","wgCheckUserClientHintsHeadersJsApi":["brands","architecture","bitness","fullVersionList","mobile","model","platform","platformVersion"],"GEHomepageSuggestedEditsEnableTopics":true,"wgGESuggestedEditsTaskTypes":{"taskTypes":["copyedit","link-recommendation"],"unavailableTaskTypes":[]},"wgGETopicsMatchModeEnabled":false,"wgGELevelingUpEnabledForUser":false,"wgTestKitchenUserExperiments":{"overrides":[],"enrolled":[],"assigned":[],"subject\_ids":[]}};
RLSTATE={"ext.globalCssJs.user.styles":"ready","site.styles":"ready","user.styles":"ready","ext.globalCssJs.user":"ready","user":"ready","user.options":"loading","ext.wikimediamessages.styles":"ready","ext.cite.styles":"ready","skins.vector.search.codex.styles":"ready","skins.vector.styles":"ready","skins.vector.icons":"ready","jquery.makeCollapsible.styles":"ready","ext.visualEditor.desktopArticleTarget.noscript":"ready","ext.uls.interlanguage":"ready","wikibase.client.init":"ready"};RLPAGEMODULES=["ext.parsermigration.survey","ext.cite.ux-enhancements","site","mediawiki.page.ready","jquery.makeCollapsible","skins.vector.js","ext.centralNotice.geoIP","ext.centralNotice.startUp","ext.gadget.ReferenceTooltips","ext.gadget.switcher","ext.urlShortener.toolbar","ext.centralauth.centralautologin","mmv.bootstrap","ext.popups","ext.visualEditor.desktopArticleTarget.init","ext.echo.centralauth","ext.eventLogging","ext.wikimediaEvents","ext.navigationTiming","ext.uls.interface","ext.cx.eventlogging.campaigns","ext.cx.uls.quick.actions","wikibase.client.vector-2022","wikibase.databox.fromWikidata","ext.checkUser.clientHints","ext.quicksurveys.init","ext.growthExperiments.SuggestedEditSession","ext.testKitchen"];
(RLQ=window.RLQ||[]).push(function(){mw.loader.impl(function(){return["user.options@12s5i",function($,jQuery,require,module){mw.user.tokens.set({"patrolToken":"+\\","watchToken":"+\\","csrfToken":"+\\"});
}];});});

[Jump to content](#bodyContent)

Main menu

Main menu

move to sidebar
hide

Navigation

* [Main page](/wiki/Main_Page "Visit the main page [z]")
* [Contents](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia")
* [Current events](/wiki/Portal:Current_events "Articles related to current events")
* [Random article](/wiki/Special:Random "Visit a randomly selected article [x]")
* [About Wikipedia](/wiki/Wikipedia:About "Learn about Wikipedia and how it works")
* [Contact us](//en.wikipedia.org/wiki/Wikipedia:Contact_us "How to contact Wikipedia")

Contribute

* [Help](/wiki/Help:Contents "Guidance on how to use and edit Wikipedia")
* [Learn to edit](/wiki/Help:Introduction "Learn how to edit Wikipedia")
* [Community portal](/wiki/Wikipedia:Community_portal "The hub for editors")
* [Recent changes](/wiki/Special:RecentChanges "A list of recent changes to Wikipedia [r]")
* [Upload file](/wiki/Wikipedia:File_upload_wizard "Add images or other media for use on Wikipedia")
* [Special pages](/wiki/Special:SpecialPages "A list of all special pages [q]")

[Search](/wiki/Special:Search "Search Wikipedia [f]")

Search

Appearance

* [Donate](https://donate.wikimedia.org/?wmf_source=donate&wmf_medium=sidebar&wmf_campaign=en.wikipedia.org&uselang=en)
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [2]</summary>

| URL | markcrawl words [6] / preamble [2] | crawl4ai words [6] / preamble [2] | crawl4ai-raw words [6] / preamble [2] | scrapy+md words [6] / preamble [2] | crawlee words [6] / preamble [2] | colly+md words [6] / preamble [2] | playwright words [6] / preamble [2] | firecrawl words [6] / preamble [2] |
|---|---|---|---|---|---|---|---|---|
| en.wikipedia.org/wiki/Apple_M1 | 4487 / 0 | 8663 / 252 | 8663 / 252 | 8636 / 5 | 14242 / 5200 | 9175 / 242 | 9175 / 242 | — |
| en.wikipedia.org/wiki/Assertion_(programming) | 3295 / 0 | 3972 / 252 | 3972 / 252 | 3557 / 5 | 8996 / 5168 | 4052 / 247 | 4052 / 247 | — |
| en.wikipedia.org/wiki/Beta_release | 3616 / 0 | 4673 / 252 | 4673 / 252 | 4525 / 5 | 10093 / 5231 | 5076 / 273 | 5076 / 273 | — |
| en.wikipedia.org/wiki/Bibcode_(identifier) | 1225 / 0 | 1847 / 252 | 1847 / 252 | 1540 / 5 | 6909 / 5162 | 1981 / 247 | 1981 / 247 | — |
| en.wikipedia.org/wiki/Byte | 9524 / 0 | 10535 / 252 | 10535 / 252 | 10626 / 5 | 16342 / 5250 | 11165 / 286 | 11165 / 286 | — |
| en.wikipedia.org/wiki/Category:All_articles_with_specif | 2540 / 0 | 3296 / 254 | 3296 / 254 | 3141 / 0 | 8403 / 5089 | 3576 / 268 | — | — |
| en.wikipedia.org/wiki/Category:Dynamically_typed_progra | 784 / 0 | 1317 / 254 | 1317 / 254 | 940 / 0 | 6068 / 5009 | 1284 / 231 | 1284 / 231 | — |
| en.wikipedia.org/wiki/Cobra_(programming_language) | 819 / 0 | 1765 / 252 | 1765 / 252 | 1686 / 5 | 7120 / 5209 | 2127 / 245 | 2127 / 245 | — |
| en.wikipedia.org/wiki/Common_Language_Runtime | 998 / 0 | 2604 / 252 | 2604 / 252 | 2705 / 5 | 8131 / 5213 | 3151 / 259 | 3151 / 259 | — |
| en.wikipedia.org/wiki/Conditional_(computer_programming | 5722 / 0 | 6499 / 252 | 6499 / 252 | 6080 / 5 | 11623 / 5212 | 6665 / 291 | 6665 / 291 | — |
| en.wikipedia.org/wiki/Cycle_detection | 5400 / 0 | 6297 / 252 | 6297 / 252 | 5719 / 5 | 11296 / 5179 | 6312 / 257 | 6312 / 257 | — |
| en.wikipedia.org/wiki/ECMAScript | 2183 / 0 | 6192 / 252 | 6192 / 252 | 6116 / 5 | 11631 / 5230 | 6602 / 266 | 11631 / 5180 | — |
| en.wikipedia.org/wiki/Eclipse_(software) | 7509 / 0 | 11744 / 252 | 11744 / 252 | 11511 / 5 | 17322 / 5305 | 12110 / 347 | 12110 / 347 | — |
| en.wikipedia.org/wiki/File:Wikibooks-logo.svg | 1536 / 0 | 2088 / 254 | 2088 / 254 | 1688 / 0 | 5395 / 3659 | 1948 / 221 | — | — |
| en.wikipedia.org/wiki/File:Wikiversity_logo_2017.svg | 1319 / 0 | 1846 / 254 | 1846 / 254 | 1460 / 0 | 5173 / 3663 | 1726 / 225 | — | — |
| en.wikipedia.org/wiki/Free-software_license | 7978 / 0 | 10329 / 252 | 10329 / 252 | 10497 / 5 | 16245 / 5263 | 11106 / 305 | 11106 / 305 | — |
| en.wikipedia.org/wiki/Free_and_open-source_software | 10558 / 0 | 13068 / 252 | 13068 / 252 | 12806 / 5 | 19842 / 5993 | 13877 / 326 | — | — |
| en.wikipedia.org/wiki/Gmsh | 645 / 0 | 1462 / 252 | 1462 / 252 | 1395 / 5 | 6827 / 5222 | 1849 / 264 | 1849 / 264 | — |
| en.wikipedia.org/wiki/Google_App_Engine | 2273 / 0 | 9301 / 252 | 9301 / 252 | 9330 / 5 | 14864 / 5241 | 9826 / 277 | 9826 / 277 | — |
| en.wikipedia.org/wiki/Help:Category | 4638 / 0 | 7564 / 252 | 7564 / 252 | 7446 / 5 | 17859 / 10102 | 7973 / 233 | 7973 / 233 | — |
| en.wikipedia.org/wiki/If-then-else | 5726 / 0 | 6503 / 252 | 6503 / 252 | 6084 / 5 | 11627 / 5212 | 6669 / 291 | 6669 / 291 | — |
| en.wikipedia.org/wiki/Infix_notation | 649 / 0 | 1313 / 252 | 1313 / 252 | 1223 / 5 | 6568 / 5146 | 1650 / 231 | 1650 / 231 | — |
| en.wikipedia.org/wiki/List_comprehensions | 3329 / 0 | 4867 / 252 | 4867 / 252 | 4601 / 5 | 10128 / 5234 | 5136 / 270 | 5136 / 270 | — |
| en.wikipedia.org/wiki/List_of_formerly_open-source_or_f | 2004 / 0 | 3398 / 252 | 3398 / 252 | 3278 / 5 | 8794 / 5240 | 3751 / 286 | 3751 / 286 | — |
| en.wikipedia.org/wiki/List_of_free_and_open-source_web_ | 1754 / 0 | 3085 / 252 | 3085 / 252 | 3055 / 5 | 8475 / 5213 | 3501 / 259 | 3501 / 259 | — |
| en.wikipedia.org/wiki/List_of_open-source_bioinformatic | 2188 / 0 | 2783 / 252 | 2783 / 252 | 2441 / 5 | 7797 / 5158 | 2871 / 247 | 2871 / 247 | — |
| en.wikipedia.org/wiki/MedCalc | 1201 / 0 | 2119 / 247 | 2119 / 247 | 2190 / 0 | 7604 / 5225 | 2620 / 276 | 2620 / 276 | — |
| en.wikipedia.org/wiki/Memory_management | 3862 / 0 | 5094 / 252 | 5094 / 252 | 5045 / 5 | 10751 / 5219 | 5726 / 254 | — | — |
| en.wikipedia.org/wiki/Metaprogramming | 2555 / 0 | 4103 / 252 | 4103 / 252 | 4033 / 5 | 9563 / 5250 | 4555 / 286 | 4555 / 286 | — |
| en.wikipedia.org/wiki/MindSpore | 1196 / 0 | 5299 / 252 | 5299 / 252 | 5515 / 5 | 10994 / 5241 | 5987 / 283 | 5987 / 283 | — |
| en.wikipedia.org/wiki/NumPy | 3426 / 0 | 5053 / 252 | 5053 / 252 | 4955 / 5 | 10643 / 5262 | 5596 / 297 | 5596 / 297 | — |
| en.wikipedia.org/wiki/Numba | 785 / 0 | 1388 / 252 | 1388 / 252 | 1131 / 5 | 5584 / 4253 | 1575 / 251 | 1575 / 251 | — |
| en.wikipedia.org/wiki/Plotly | 2844 / 0 | 4275 / 252 | 4275 / 252 | 3191 / 5 | 8697 / 5189 | 3678 / 274 | — | — |
| en.wikipedia.org/wiki/PyS60 | 1029 / 0 | 3058 / 252 | 3058 / 252 | 3189 / 5 | 8657 / 5252 | 3680 / 294 | 3680 / 294 | — |
| en.wikipedia.org/wiki/Python_(programming_language) | 14538 / 0 | 18625 / 252 | 18625 / 252 | 18193 / 5 | 24732 / 5341 | 19322 / 376 | 19322 / 376 | — |
| en.wikipedia.org/wiki/Python_Software_Foundation | 1430 / 0 | 2274 / 252 | 2274 / 252 | 2229 / 5 | 7696 / 5227 | 2699 / 269 | 2699 / 269 | — |
| en.wikipedia.org/wiki/Python_Tools_for_Visual_Studio | 415 / 0 | 3062 / 252 | 3062 / 252 | 3035 / 5 | 8447 / 5209 | 3478 / 255 | 3478 / 255 | — |
| en.wikipedia.org/wiki/RPyC | 1052 / 0 | 1678 / 252 | 1678 / 252 | 1443 / 5 | 6822 / 5175 | 1896 / 254 | 1896 / 254 | — |
| en.wikipedia.org/wiki/SETL | 1256 / 0 | 1936 / 252 | 1936 / 252 | 1778 / 5 | 7218 / 5200 | 2211 / 242 | 2211 / 242 | — |
| en.wikipedia.org/wiki/SQLAlchemy | 951 / 0 | 1600 / 252 | 1600 / 252 | 1271 / 5 | 6646 / 5159 | 1711 / 238 | 1711 / 238 | — |
| en.wikipedia.org/wiki/Software_license | 5237 / 0 | 6533 / 252 | 6533 / 252 | 6328 / 5 | 12194 / 5233 | 7051 / 274 | 7051 / 274 | — |
| en.wikipedia.org/wiki/Software_release_life_cycle | 3610 / 0 | 4667 / 252 | 4667 / 252 | 4519 / 5 | 10088 / 5232 | 5071 / 274 | 5071 / 274 | — |
| en.wikipedia.org/wiki/Source-available_software | 2844 / 0 | 4689 / 252 | 4689 / 252 | 4500 / 5 | 10082 / 5207 | 5018 / 248 | 5018 / 248 | — |
| en.wikipedia.org/wiki/Standard_library | 1262 / 0 | 1841 / 252 | 1841 / 252 | 1495 / 5 | 6876 / 5189 | 1956 / 274 | 1956 / 274 | — |
| en.wikipedia.org/wiki/Strongly_typed | 4285 / 0 | 5176 / 252 | 5176 / 252 | 5000 / 5 | 10491 / 5166 | 5522 / 245 | 5522 / 245 | — |
| en.wikipedia.org/wiki/Unicode | 16362 / 0 | 20752 / 252 | 20752 / 252 | 20547 / 5 | 26515 / 5283 | 21234 / 325 | — | — |
| en.wikipedia.org/wiki/Unix-like | 2636 / 0 | 4735 / 252 | 4735 / 252 | 4620 / 5 | 10116 / 5221 | 5101 / 263 | — | — |
| en.wikipedia.org/wiki/Wolfram_Mathematica | 3014 / 0 | 5990 / 252 | 5990 / 252 | 5945 / 5 | 11576 / 5294 | 6490 / 336 | 6490 / 336 | — |
| en.wikipedia.org/wiki/World_Programming_System | 1606 / 0 | 2250 / 252 | 2250 / 252 | 1941 / 5 | 7363 / 5181 | 2402 / 266 | 2402 / 266 | — |
| en.wikipedia.org/wiki/Zlib_License | 768 / 0 | 2117 / 252 | 2117 / 252 | 2093 / 5 | 7513 / 5215 | 2538 / 257 | 2538 / 257 | — |

</details>

## stripe-docs

| Tool | Avg words [6] | Preamble [2] | Repeat rate [3] | Junk found [4] | Headings [7] | Code blocks [8] | Precision [5] | Recall [5] |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 1165 | 13 | 0% | 35 | 10.3 | 2.2 | 98% | 22% |
| crawl4ai | 1372 | 174 ⚠ | 0% | 819 | 12.0 | 2.2 | 100% | 18% |
| crawl4ai-raw | 1369 | 174 ⚠ | 0% | 785 | 12.0 | 2.2 | 100% | 18% |
| scrapy+md | 1360 | 171 ⚠ | 0% | 552 | 10.3 | 2.2 | 100% | 22% |
| crawlee | 18095 | 8955 ⚠ | 1% | 1254 | 10.6 | 2.2 | 98% | 100% |
| colly+md | 16950 | 8867 ⚠ | 1% | 977 | 10.1 | 2.0 | 98% | 94% |
| playwright | 18073 | 8955 ⚠ | 1% | 999 | 10.6 | 2.2 | 98% | 95% |
| firecrawl | — | — | — | — | — | — | — | — |

> **Column definitions:**
> **[6] Avg words** = mean words per page. **[2] Preamble** = avg words per page before the first heading (nav chrome). **[3] Repeat rate** = fraction of sentences on >50% of pages.
> **[4] Junk found** = total known boilerplate phrases detected across all pages. **[7] Headings** = avg headings per page. **[8] Code blocks** = avg fenced code blocks per page.
> **[5] Precision/Recall** = cross-tool consensus (pages with <2 sentences excluded). **⚠** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
**markcrawl** produces the cleanest output with 13 words of preamble per page, while **playwright** injects 8955 words of nav chrome before content begins. The word count gap (1165 vs 18095 avg words) is largely explained by preamble: 8955 words of nav chrome account for ~49% of crawlee's output on this site. markcrawl's lower recall (22% vs 100%) reflects stricter content filtering — the "missed" sentences are predominantly navigation, sponsor links, and footer text that other tools include as content. For RAG, this is typically a net positive: fewer junk tokens per chunk tends to improve embedding quality and retrieval precision.

<details>
<summary>Sample output — first 40 lines of <code>docs.stripe.com/payment-authentication/writing-queries</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
*Use Stripe Sigma to retrieve information about authentication, conversion, and the SCA exemptions used.*


# Querying authentication conversion

## Use Stripe Sigma to retrieve information about authentication, conversion, and the SCA exemptions used.

Ask about this page

Copy for LLMView as Markdown

See the `authentication_report_attempts` table under the **Analytics Tables** section of the Sigma schema. Each row within the `authentication_report_attempts` table represents data about an individual attempt object. Our [full-page documentation](https://dashboard.stripe.com/stripe-schema?tableName=authentication_report_attempts) also shows the schema in a split-view format.

## Attempt conversion information

You can get a report for every attempt, with each [PaymentIntent](/api/payment_intents) or [SetupIntent](/api/payment_intents) having possibly more than one attempt.

#### Note

In some cases there are multiple attempts for a single transaction, such as when a payment is declined and then retried. To filter to a specific transaction, use the `is_final_attempt` column. This column is eventually consist after a few days.

The following example query uses the `authentication_report_attempts` table to retrieve a list of PaymentIntents that were successfully authenticated using the challenge flow.

```
select
  attempt_id,
  intent_id,
  payment_method,
  threeds_reason as step_up_reason,
  charge_outcome
from authentication_report_attempts
where intent_type = 'payment'
  and threeds_outcome_result = 'authenticated'
  and authentication_flow = 'challenge'
  and is_final_attempt
limit 5
```

| attempt_id | intent_id | payment_method | step_up_reason | charge_outcome |
| --- | --- | --- | --- | --- |
```

**crawl4ai**
```
[Skip to content](https://docs.stripe.com/payment-authentication/writing-queries#main-content)
Writing queries
[Create account](https://dashboard.stripe.com/register) or [Sign in](https://dashboard.stripe.com/login?redirect=https%3A%2F%2Fdocs.stripe.com%2Fpayment-authentication%2Fwriting-queries)
[The Stripe Docs logo](https://docs.stripe.com/)
Search `/`Ask AI
[Create account](https://dashboard.stripe.com/register)[Sign in](https://dashboard.stripe.com/login?redirect=https%3A%2F%2Fdocs.stripe.com%2Fpayment-authentication%2Fwriting-queries)
[Get started ](https://docs.stripe.com/get-started)
[Payments ](https://docs.stripe.com/payments)
[Revenue ](https://docs.stripe.com/revenue)
[Platforms and marketplaces ](https://docs.stripe.com/connect)
[Money management ](https://docs.stripe.com/money-management)
APIs & SDKsHelp
[Overview](https://docs.stripe.com/payments)[Accept a payment](https://docs.stripe.com/payments/accept-a-payment)[Upgrade your integration](https://docs.stripe.com/payments/upgrades)
Online payments
[Overview](https://docs.stripe.com/payments/online-payments)[Find your use case](https://docs.stripe.com/payments/use-cases/get-started)
Use Payment Links
Build a payments page
Build a custom integration with Elements
Build an in-app integration
Use Managed Payments
[Recurring payments](https://docs.stripe.com/recurring-payments)
In-person payments
Terminal
Payment methods
Add payment methods
Manage payment methods
Faster checkout with Link
Payment operations
Analytics
[Balances and settlement time](https://docs.stripe.com/payments/balances)
Compliance and security
[3D Secure authentication](https://docs.stripe.com/payments/3d-secure)
[Authenticate with 3D Secure](https://docs.stripe.com/payments/3d-secure/authentication-flow)
[SCA exemptions](https://docs.stripe.com/payments/3d-secure/strong-customer-authentication-exemptions)
[Standalone 3D Secure](https://docs.stripe.com/payments/3d-secure/standalone-three-d-secure)
[Import 3D Secure results](https://docs.stripe.com/payments/payment-intents/three-d-secure-import)
Writing queries
[SCA readiness](https://docs.stripe.com/strong-customer-authentication)
[India recurring payments](https://docs.stripe.com/india-recurring-payments)
```

**crawl4ai-raw**
```
[Skip to content](https://docs.stripe.com/payment-authentication/writing-queries#main-content)
Writing queries
[Create account](https://dashboard.stripe.com/register) or [Sign in](https://dashboard.stripe.com/login?redirect=https%3A%2F%2Fdocs.stripe.com%2Fpayment-authentication%2Fwriting-queries)
[The Stripe Docs logo](https://docs.stripe.com/)
Search `/`Ask AI
[Create account](https://dashboard.stripe.com/register)[Sign in](https://dashboard.stripe.com/login?redirect=https%3A%2F%2Fdocs.stripe.com%2Fpayment-authentication%2Fwriting-queries)
[Get started ](https://docs.stripe.com/get-started)
[Payments ](https://docs.stripe.com/payments)
[Revenue ](https://docs.stripe.com/revenue)
[Platforms and marketplaces ](https://docs.stripe.com/connect)
[Money management ](https://docs.stripe.com/money-management)
APIs & SDKsHelp
[Overview](https://docs.stripe.com/payments)[Accept a payment](https://docs.stripe.com/payments/accept-a-payment)[Upgrade your integration](https://docs.stripe.com/payments/upgrades)
Online payments
[Overview](https://docs.stripe.com/payments/online-payments)[Find your use case](https://docs.stripe.com/payments/use-cases/get-started)
Use Payment Links
Build a payments page
Build a custom integration with Elements
Build an in-app integration
Use Managed Payments
[Recurring payments](https://docs.stripe.com/recurring-payments)
In-person payments
Terminal
Payment methods
Add payment methods
Manage payment methods
Faster checkout with Link
Payment operations
Analytics
[Balances and settlement time](https://docs.stripe.com/payments/balances)
Compliance and security
[3D Secure authentication](https://docs.stripe.com/payments/3d-secure)
[Authenticate with 3D Secure](https://docs.stripe.com/payments/3d-secure/authentication-flow)
[SCA exemptions](https://docs.stripe.com/payments/3d-secure/strong-customer-authentication-exemptions)
[Standalone 3D Secure](https://docs.stripe.com/payments/3d-secure/standalone-three-d-secure)
[Import 3D Secure results](https://docs.stripe.com/payments/payment-intents/three-d-secure-import)
Writing queries
[SCA readiness](https://docs.stripe.com/strong-customer-authentication)
[India recurring payments](https://docs.stripe.com/india-recurring-payments)
```

**scrapy+md**
```
[Skip to content](#main-content)

Writing queries

[Create account](https://dashboard.stripe.com/register) or [Sign in](https://dashboard.stripe.com/login?redirect=https%3A%2F%2Fdocs.stripe.com%2Fpayment-authentication%2Fwriting-queries)

[The Stripe Docs logo](/)

Search

`/`Ask AI

[Create account](https://dashboard.stripe.com/register)[Sign in](https://dashboard.stripe.com/login?redirect=https%3A%2F%2Fdocs.stripe.com%2Fpayment-authentication%2Fwriting-queries)

[Get started](/get-started)

[Payments](/payments)

[Revenue](/revenue)

[Platforms and marketplaces](/connect)

[Money management](/money-management)

[Developer resources](/development)

APIs & SDKsHelp

[Overview](/payments)[Accept a payment](/payments/accept-a-payment)[Upgrade your integration](/payments/upgrades)

Online payments

[Overview](/payments/online-payments)[Find your use case](/payments/use-cases/get-started)

Use Payment Links

Build a payments page

Build a custom integration with Elements
```

**crawlee**
```
Querying authentication conversion | Stripe Documentation




#​ .sn-1q4qxi9 { --jybopzu-hue-gray0: #ffffff; --jybopzu-hue-gray50: #f6f8fa; --jybopzu-hue-gray100: #ebeef1; --jybopzu-hue-gray150: #d5dbe1; --jybopzu-hue-gray200: #c0c8d2; --jybopzu-hue-gray300: #a3acba; --jybopzu-hue-gray400: #87909f; --jybopzu-hue-gray500: #687385; --jybopzu-hue-gray600: #545969; --jybopzu-hue-gray700: #414552; --jybopzu-hue-gray800: #30313d; --jybopzu-hue-gray900: #1a1b25; --jybopzu-hue-gray950: #10111a; --jybopzu-hue-blue50: #ddfffe; --jybopzu-hue-blue100: #cff5f6; --jybopzu-hue-blue150: #a2e5ef; --jybopzu-hue-blue200: #75d5e8; --jybopzu-hue-blue300: #06b9ef; --jybopzu-hue-blue400: #0096eb; --jybopzu-hue-blue500: #0570de; --jybopzu-hue-blue600: #0055bc; --jybopzu-hue-blue700: #04438c; --jybopzu-hue-blue800: #003262; --jybopzu-hue-blue900: #011c3a; --jybopzu-hue-green50: #ecfed7; --jybopzu-hue-green100: #d7f7c2; --jybopzu-hue-green150: #a6eb84; --jybopzu-hue-green200: #76df47; --jybopzu-hue-green300: #48c404; --jybopzu-hue-green400: #3fa40d; --jybopzu-hue-green500: #228403; --jybopzu-hue-green600: #006908; --jybopzu-hue-green700: #0b5019; --jybopzu-hue-green800: #043b15; --jybopzu-hue-green900: #02220d; --jybopzu-hue-orange50: #fef9da; --jybopzu-hue-orange100: #fcedb9; --jybopzu-hue-orange150: #fcd579; --jybopzu-hue-orange200: #fcbd3a; --jybopzu-hue-orange300: #ff8f0e; --jybopzu-hue-orange400: #ed6704; --jybopzu-hue-orange500: #c84801; --jybopzu-hue-orange600: #a82c00; --jybopzu-hue-orange700: #842106; --jybopzu-hue-orange800: #5f1a05; --jybopzu-hue-orange900: #331302; --jybopzu-hue-red50: #fff5fa; --jybopzu-hue-red100: #ffe7f2; --jybopzu-hue-red150: #ffccdf; --jybopzu-hue-red200: #ffb1cd; --jybopzu-hue-red300: #fe87a1; --jybopzu-hue-red400: #fc526a; --jybopzu-hue-red500: #df1b41; --jybopzu-hue-red600: #b3093c; --jybopzu-hue-red700: #890d37; --jybopzu-hue-red800: #68052b; --jybopzu-hue-red900: #3e021a; --jybopzu-hue-purple50: #f9f7ff; --jybopzu-hue-purple100: #f2ebff; --jybopzu-hue-purple150: #dfd3fc; --jybopzu-hue-purple200: #d1befe; --jybopzu-hue-purple300: #b49cfc; --jybopzu-hue-purple400: #8d7ffa; --jybopzu-hue-purple500: #625afa; --jybopzu-hue-purple600: #513dd9; --jybopzu-hue-purple700: #3f32a1; --jybopzu-hue-purple800: #302476; --jybopzu-hue-purple900: #14134e; --jybopzu-color-neutral0: var(--jybopzu-hue-gray0); --jybopzu-color-neutral50: var(--jybopzu-hue-gray50); --jybopzu-color-neutral100: var(--jybopzu-hue-gray100); --jybopzu-color-neutral150: var(--jybopzu-hue-gray150); --jybopzu-color-neutral200: var(--jybopzu-hue-gray200); --jybopzu-color-neutral300: var(--jybopzu-hue-gray300); --jybopzu-color-neutral400: var(--jybopzu-hue-gray400); --jybopzu-color-neutral500: var(--jybopzu-hue-gray500); --jybopzu-color-neutral600: var(--jybopzu-hue-gray600); --jybopzu-color-neutral700: var(--jybopzu-hue-gray700); --jybopzu-color-neutral800: var(--jybopzu-hue-gray800); --jybopzu-color-neutral900: var(--jybopzu-hue-gray900); --jybopzu-color-neutral950: var(--jybopzu-hue-gray950); --jybopzu-color-brand50: var(--jybopzu-hue-purple50); --jybopzu-color-brand100: var(--jybopzu-hue-purple100); --jybopzu-color-brand200: var(--jybopzu-hue-purple200); --jybopzu-color-brand300: var(--jybopzu-hue-purple300); --jybopzu-color-brand400: var(--jybopzu-hue-purple400); --jybopzu-color-brand500: var(--jybopzu-hue-purple500); --jybopzu-color-brand600: var(--jybopzu-hue-purple600); --jybopzu-color-brand700: var(--jybopzu-hue-purple700); --jybopzu-color-brand800: var(--jybopzu-hue-purple800); --jybopzu-color-brand900: var(--jybopzu-hue-purple900); --jybopzu-color-info50: var(--jybopzu-hue-blue50); --jybopzu-color-info100: var(--jybopzu-hue-blue100); --jybopzu-color-info150: var(--jybopzu-hue-blue150); --jybopzu-color-info200: var(--jybopzu-hue-blue200); --jybopzu-color-info300: var(--jybopzu-hue-blue300); --jybopzu-color-info400: var(--jybopzu-hue-blue400); --jybopzu-color-info500: var(--jybopzu-hue-blue500); --jybopzu-color-info600: var(--jybopzu-hue-blue600); --jybopzu-color-info700: var(--jybopzu-hue-blue700); --jybopzu-color-info800: var(--jybopzu-hue-blue800); --jybopzu-color-info900: var(--jybopzu-hue-blue900); --jybopzu-color-success50: var(--jybopzu-hue-green50); --jybopzu-color-success100: var(--jybopzu-hue-green100); --jybopzu-color-success150: var(--jybopzu-hue-green150); --jybopzu-color-success200: var(--jybopzu-hue-green200); --jybopzu-color-success300: var(--jybopzu-hue-green300); --jybopzu-color-success400: var(--jybopzu-hue-green400); --jybopzu-color-success500: var(--jybopzu-hue-green500); --jybopzu-color-success600: var(--jybopzu-hue-green600); --jybopzu-color-success700: var(--jybopzu-hue-green700); --jybopzu-color-success800: var(--jybopzu-hue-green800); --jybopzu-color-success900: var(--jybopzu-hue-green900); --jybopzu-color-attention50: var(--jybopzu-hue-orange50); --jybopzu-color-attention100: var(--jybopzu-hue-orange100); --jybopzu-color-attention150: var(--jybopzu-hue-orange150); --jybopzu-color-attention200: var(--jybopzu-hue-orange200); --jybopzu-color-attention300: var(--jybopzu-hue-orange300); --jybopzu-color-attention400: var(--jybopzu-hue-orange400); --jybopzu-color-attention500: var(--jybopzu-hue-orange500); --jybopzu-color-attention600: var(--jybopzu-hue-orange600); --jybopzu-color-attention700: var(--jybopzu-hue-orange700); --jybopzu-color-attention800: var(--jybopzu-hue-orange800); --jybopzu-color-attention900: var(--jybopzu-hue-orange900); --jybopzu-color-critical50: var(--jybopzu-hue-red50); --jybopzu-color-critical100: var(--jybopzu-hue-red100); --jybopzu-color-critical150: var(--jybopzu-hue-red150); --jybopzu-color-critical200: var(--jybopzu-hue-red200); --jybopzu-color-critical300: var(--jybopzu-hue-red300); --jybopzu-color-critical400: var(--jybopzu-hue-red400); --jybopzu-color-critical500: var(--jybopzu-hue-red500); --jybopzu-color-critical600: var(--jybopzu-hue-red600); --jybopzu-color-critical700: var(--jybopzu-hue-red700); --jybopzu-color-critical800: var(--jybopzu-hue-red800); --jybopzu-color-critical900: var(--jybopzu-hue-red900); --jybopzu-backgroundColor-surface: var(--jybopzu-color-neutral0); --jybopzu-backgroundColor-container: var(--jybopzu-color-neutral50); --jybopzu-borderColor-neutral: var(--jybopzu-color-neutral150); --jybopzu-borderColor-critical: var(--jybopzu-color-critical500); --jybopzu-iconColor-primary: var(--jybopzu-color-neutral600); --jybopzu-iconColor-secondary: var(--jybopzu-color-neutral400); --jybopzu-iconColor-disabled: var(--jybopzu-color-neutral200); --jybopzu-iconColor-brand: var(--jybopzu-color-brand400); --jybopzu-iconColor-info: var(--jybopzu-color-info400); --jybopzu-iconColor-success: var(--jybopzu-color-success400); --jybopzu-iconColor-attention: var(--jybopzu-color-attention400); --jybopzu-iconColor-critical: var(--jybopzu-color-critical400); --jybopzu-textColor-primary: var(--jybopzu-color-neutral700); --jybopzu-textColor-secondary: var(--jybopzu-color-neutral500); --jybopzu-textColor-disabled: var(--jybopzu-color-neutral300); --jybopzu-textColor-brand: var(--jybopzu-color-brand500); --jybopzu-textColor-info: var(--jybopzu-color-info500); --jybopzu-textColor-success: var(--jybopzu-color-success500); --jybopzu-textColor-attention: var(--jybopzu-color-attention500); --jybopzu-textColor-critical: var(--jybopzu-color-critical500); --jybopzu-overflow-hidden: hidden; --jybopzu-radius-none: none; --jybopzu-radius-xsmall: 4px; --jybopzu-radius-small: 4px; --jybopzu-radius-medium: 8px; --jybopzu-radius-large: 10px; --jybopzu-radius-rounded: 999em; --jybopzu-shadow-none: none; --jybopzu-shadow-top: rgb(0 0 0 / 12%) 0px 1px 1px 0px; --jybopzu-shadow-base: rgb(64 68 82 / 8%) 0px 2px 5px 0px, 0 0 0 0 transparent; --jybopzu-shadow-hover: rgb(64 68 82 / 8%) 0px 2px 5px 0px, rgb(64 68 82 / 8%) 0px 3px 9px 0px; --jybopzu-shadow-focus: 0 0 0 4px rgb(1 150 237 / 36%); --jybopzu-size-0: 0px; --jybopzu-size-1: var(--jybopzu-space-1); --jybopzu-size-25: var(--jybopzu-space-25); --jybopzu-size-50: var(--jybopzu-space-50); --jybopzu-size-75: var(--jybopzu-space-75); --jybopzu-size-100: var(--jybopzu-space-100); --jybopzu-size-150: var(--jybopzu-space-150); --jybopzu-size-200: var(--jybopzu-space-200); --jybopzu-size-250: var(--jybopzu-space-250); --jybopzu-size-300: var(--jybopzu-space-300); --jybopzu-size-350: var(--jybopzu-space-350); --jybopzu-size-400: var(--jybopzu-space-400); --jybopzu-size-500: var(--jybopzu-space-500); --jybopzu-size-600: var(--jybopzu-space-600); --jybopzu-size-fill: 100%; --jybopzu-size-min: min-content; --jybopzu-size-max: max-content; --jybopzu-size-fit: fit-content; --jybopzu-size-1\/2: 50%; --jybopzu-size-1\/3: 33.3333%; --jybopzu-size-2\/3: 66.6667%; --jybopzu-size-1\/4: 25%; --jybopzu-size-2\/4: 50%; --jybopzu-size-3\/4: 75%; --jybopzu-size-1\/5: 20%; --jybopzu-size-2\/5: 40%; --jybopzu-size-3\/5: 60%; --jybopzu-size-4\/5: 80%; --jybopzu-size-1\/6: 16.6667%; --jybopzu-size-2\/6: 33.3333%; --jybopzu-size-3\/6: 50%; --jybopzu-size-4\/6: 66.6667%; --jybopzu-size-5\/6: 83.3333%; --jybopzu-size-1\/12: 8.3333%; --jybopzu-size-2\/12: 16.6667%; --jybopzu-size-3\/12: 25%; --jybopzu-size-4\/12: 33.3333%; --jybopzu-size-5\/12: 41.6667%; --jybopzu-size-6\/12: 50%; --jybopzu-size-7\/12: 58.3333%; --jybopzu-size-8\/12: 66.6667%; --jybopzu-size-9\/12: 75%; --jybopzu-size-10\/12: 83.3333%; --jybopzu-size-11\/12: 91.6667%; --jybopzu-space-0: 0px; --jybopzu-space-1: 1px; --jybopzu-space-25: 2px; --jybopzu-space-50: 4px; --jybopzu-space-75: 6px; --jybopzu-space-100: 8px; --jybopzu-space-150: 12px; --jybopzu-space-200: 16px; --jybopzu-space-250: 20px; --jybopzu-space-300: 24px; --jybopzu-space-350: 28px; --jybopzu-space-400: 32px; --jybopzu-space-500: 40px; --jybopzu-space-600: 48px; --jybopzu-space-xxsmall: var(--jybopzu-space-25); --jybopzu-space-xsmall: var(--jybopzu-space-50); --jybopzu-space-small: var(--jybopzu-space-100); --jybopzu-space-medium: var(--jybopzu-space-200); --jybopzu-space-large: var(--jybopzu-space-300); --jybopzu-space-xlarge: var(--jybopzu-space-400); --jybopzu-space-xxlarge: var(--jybopzu-space-600); --jybopzu-typeface-ui: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; --jybopzu-typeface-monospace: 'Source Code Pro', Menlo, Monaco, monospace; --jybopzu-weight-regular: 400; --jybopzu-weight-semibold: 600; --jybopzu-weight-bold: 700; --jybopzu-zIndex-overlay: 299; --jybopzu-zIndex-partial: 400; }#​#​ .rs-3::before {
content: var(--s--baseline-alignment-content);user-select: none;align-self: baseline;margin-right: calc(-1 \* var(--s--column-gap));
}
#​#​ .rs-8[aria-invalid="true"] {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .sail-table-row:not(:hover) .row-actions-trigger {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-4 {
display: var(--s--display-block);
}
#​#​ .rs-2 {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-6:active:not([aria-disabled="true"]) {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .sail-table-row:hover .row-actions-trigger {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-5:hover:not(:active):not([aria-disabled="true"]) {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-7:focus {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .sn-d7kp2a { --distribute-x: initial; --distribute-y: initial; --align-x: initial; --align-y: initial; }
#​#​ .sn-d7kp2a > \* { --align-self-x: initial; --align-self-y: initial; --flex-x: 1 1 auto; --flex-y: 1 1 auto; }
#​#​ .sn-1fnc4mz { --row-gap: normal; --column-gap: normal; gap: var(--row-gap) var(--column-gap); }
#​#​ .sn-1c37ise { --padding-top: 0; --padding-right: 0; --padding-bottom: 0; --padding-left: 0; padding: var(--padding-top) var(--padding-right) var(--padding-bottom) var(--padding-left); }
.\_\_sn-sheet-order { --order: '\_1rkm1cp,\_88mn99,\_5olop,\_16pds2j,\_1wna6e6,\_kskd3k,\_5vzub4,\_lzay40,\_1d9aqya'; }#​#​#​#​#​ .sn-182o7r0 { font-family: var(--jybopzu-typeface-ui); color: var(--jybopzu-textColor-primary); fill: var(--jybopzu-iconColor-primary); -webkit-font-smoothing: antialiased; }#​#​#​#​#​#​#​:root, :host #​#​#​#​#​#​#​, #​#​#​#​#​#​#​ .sn-token-provider {
--s-806179: var(--s-1ipujfj);--qyckuc: 200ms;--s-1xyzpq3: 0ms;--ch7862: 50ms;--s-5jzhfa: 100ms;--s-12b75vv: 150ms;--rsnfo1: 300ms;--s-12ljnrj: 400ms;--s-10dnt5v: cubic-bezier(0, .09, .4, 1);--s-12oyqav: ease-in-out;--im41o8: ease-out;--s-1fdsmh8: ease-in;--s-1pzb1xw: 120;--s-6429u6: 14;--dutg7l: 300;--rjlba6: 20;--s-117eyx7: 400;--slm412: 10;--s-1pt58bw: 30ms;--pu6lsa: 50ms;--s-1ca225m: 80ms;--h9q5hc: 0.95;--s-1308p7c: 0.99;--s-1paplcg: 0.98;--s-19omtc6: 1.02;--eef79q: #ffffff;--s-8qwlk1: #F4F7FA;--o3gs5n: #ECF1F6;--hyhghw: #D4DEE9;--s-1b58r1w: #BAC8DA;--ovqch4: #95A4BA;--ggantb: #7D8BA4;--s-1a8u6zz: #667691;--k08wfi: #50617A;--s-169hr3v: #3C4F69;--ymu9b7: #273951;--ny99wq: #1A2C44;--s-1nmzh8w: #ffffff;--s-421sqo: #e2fbfe;--s-4qj11w: #cbf5fd;--s-1u1nr1c: #a7e7fc;--dj5edy: #6dc9fc;--s-3blua0: #3babfd;--s-172n6d2: #088ef9;--s-1l3w4rb: #0072e9;--s-1yzoj9a: #045ad0;--kvmyi1: #0b46ad;--s-1ah8y8v: #0d3485;--s-1v7mjmv: #0a2156;--s-1cbef47: #ffffff;--ncitdb: #eafcdd;--khndpt: #d1fab3;--fcix74: #a8f170;--s-1jt7b3q: #7cd548;--rz6g85: #58ba27;--s-10in11e: #3da00b;--jet5ih: #2b8700;--s-11ws3zn: #217005;--mkuc60: #1c5a0d;--s-5vneq4: #184310;--s-1ybzlmc: #112a0d;--s-1idvp5s: #ffffff;--s-1ronw4t: #fdf8c9;--een7nd: #fceeb5;--s-1j3zdk7: #fbd992;--bpq42r: #fcaf4f;--d5srfd: #f7870f;--s-7gt7xl: #e46602;--s-1bt4nax: #cc4b00;--s-1m90cr3: #b13600;--s-105rx08: #922700;--s-3csqoi: #701b01;--s-1x99otv: #4a0f02;--s-18rmc6q: #ffffff;--m4edry: #fef4f6;--pfpugw: #fde9ee;--s-1at7tzv: #fbd3dc;--s-8ik67: #faa9b8;--s-1brqpgc: #fa7e91;--s-1k4y65: #fa4a67;--s-1t7w85x: #e61947;--j769ku: #c0123c;--s-105k9ow: #9b0c36;--s-1bradsh: #76072f;--s-17cbcf1: #4e0322;--s-1m3ejd7: #ffffff;--wclsxb: #f7f5fd;--s-1nuetr3: #efecfc;--s-1rgwov0: #e0d9fb;--d427sf: #c3b6fb;--s-1gm5hwl: #a497fc;--d7ng6f: #857afe;--s-1wqs2n2: #675dff;--s-1rqwfiu: #533afd;--cb9l9o: #4e11e2;--b00e2n: #44139f;--yvasq2: #2f0e63;--s-35hf94: hsla(0, 0%, 100%, 0.2);--s-13ypoy8: var(--eef79q);--s-114rdv4: var(--s-8qwlk1);--s-1bcqfda: var(--o3gs5n);--s-1kkti1r: var(--hyhghw);--s-16pqfer: var(--s-1b58r1w);--s-1kmer3i: var(--ovqch4);--s-13py8ob: var(--ggantb);--s-1wdog5l: var(--s-1a8u6zz);--jkp57b: var(--k08wfi);--s-1xkgkxo: var(--s-169hr3v);--s-1egalvn: var(--ymu9b7);--v2y5bm: var(--ny99wq);--s-1ona342: var(--s-1m3ejd7);--s-1xikbvo: var(--wclsxb);--ek860z: var(--s-1nuetr3);--s-3qadn4: var(--s-1rgwov0);--nl7ypg: var(--d427sf);--hm37ax: var(--s-1gm5hwl);--s-142x5wh: var(--d7ng6f);--s-1nbkq3e: var(--s-1wqs2n2);--s-1b0l18k: var(--s-1rqwfiu);--s-1y0ta6r: var(--cb9l9o);--pxx34h: var(--b00e2n);--xp2k2: var(--yvasq2);--s-13od8gw: var(--s-1idvp5s);--fox699: var(--s-1ronw4t);--p5cdic: var(--een7nd);--s-1jh7fp5: var(--s-1j3zdk7);--lsye2d: var(--bpq42r);--t3987n: var(--d5srfd);--s-1vcezov: var(--s-7gt7xl);--s-1qk1a9q: var(--s-1bt4nax);--s-1ipujfj: var(--s-1m90cr3);--s-1vhr1m: var(--s-105rx08);--s-1oqa1l5: var(--s-3csqoi);--kubwak: var(--s-1x99otv);--whf9po: var(--s-18rmc6q);--gqp7g1: var(--m4edry);--s-1j0j6fb: var(--pfpugw);--o1xbta: var(--s-1at7tzv);--vyde9h: var(--s-8ik67);--s-875rxv: var(--s-1brqpgc);--s-1xn82ef: var(--s-1k4y65);--xi7x09: var(--s-1t7w85x);--uk4ts2: var(--j769ku);--s-9ukgu0: var(--s-105k9ow);--s-15yycft: var(--s-1bradsh);--s-1v6ybst: var(--s-17cbcf1);--s-1f39zfp: var(--s-1nmzh8w);--s-1bf76tl: var(--s-421sqo);--s-1sypgcr: var(--s-4qj11w);--u7pgeo: var(--s-1u1nr1c);--qev2nh: var(--dj5edy);--rqlrpr: var(--s-3blua0);--s-8vaodq: var(--s-172n6d2);--s-1m519r1: var(--s-1l3w4rb);--r3g89x: var(--s-1yzoj9a);--n0umvo: var(--kvmyi1);--c0109p: var(--s-1ah8y8v);--s-26e45o: var(--s-1v7mjmv);--s-1a4o86t: var(--s-1cbef47);--nxbwn6: var(--ncitdb);--s-18tv9xz: var(--khndpt);--s-660zz9: var(--fcix74);--s-5y9ijm: var(--s-1jt7b3q);--s-1gwptpc: var(--rz6g85);--t5jail: var(--s-10in11e);--qcdf10: var(--jet5ih);--s-1o92vf6: var(--s-11ws3zn);--s-1spzwnv: var(--mkuc60);--s-35q6a2: var(--s-5vneq4);--axxngb: var(--s-1ybzlmc);--s-1hj7tfd: var(--s-18rmc6q);--s-1xf1h3f: var(--m4edry);--aqxmtx: var(--pfpugw);--s-1um7fco: var(--s-1at7tzv);--d2i300: var(--s-8ik67);--cae9kd: var(--s-1brqpgc);--s-1a4c91b: var(--s-1k4y65);--s-1jvllvw: var(--s-1t7w85x);--x379qy: var(--j769ku);--s-1owp6iv: var(--s-105k9ow);--m26qys: var(--s-1bradsh);--s-3rumb4: var(--s-17cbcf1);--s-5tm7hx: var(--s-1cbef47);--h22sh6: var(--ncitdb);--s-11rdejd: var(--khndpt);--s-1g2t37u: var(--fcix74);--wesn6: var(--s-1jt7b3q);--s-1hhq31p: var(--rz6g85);--yji28s: var(--s-10in11e);--s-169ogke: var(--jet5ih);--hr7syg: var(--s-11ws3zn);--s-14wylcr: var(--mkuc60);--s-289q66: var(--s-5vneq4);--v27jy: var(--s-1ybzlmc);--s-1hldvhn: #9966FF;--s-1xwen3a: #0055BC;--hxpspa: #00A1C2;--s-5ghlc9: #ED6804;--nap71a: #B3063D;--s-1sz15nh: var(--mkuc60);--mygevb: var(--s-1k4y65);--nrw914: var(--s-105rx08);--bu79cc: var(--s-10in11e);--s-1rfvf0n: var(--s-114rdv4);--s-9fypy8: var(--s-13ypoy8);--s-8muhy8: var(--s-35hf94);--s-153sf3j: rgba(186, 200, 218, 0.7);--s-1mkjmgu: var(--s-1b0l18k);--s-9u3gcm: var(--s-1b0l18k);--s-1pk4mhu: var(--s-1y0ta6r);--s-1wze59r: var(--s-1b0l18k);--s-1gzyq0k: var(--s-1b0l18k);--s-1eg71kz: var(--s-9fypy8);--uftl0g: var(--s-9fypy8);--s-1wj6iyq: var(--s-114rdv4);--s-1jrjwpv: var(--s-9fypy8);--b5b0q1: var(--s-9fypy8);--jix8n1: var(--xi7x09);--s-1isx4n7: var(--xi7x09);--s-1owgngi: var(--uk4ts2);--s-1tqa4ka: var(--xi7x09);--s-1dl2eq8: var(--xi7x09);--s-14a2tiz: var(--s-13ypoy8);--s-1b3o71a: var(--s-1nbkq3e);--qkwke3: var(--s-1nbkq3e);--s-1afrigr: var(--s-1b0l18k);--s-1orf6yv: var(--s-1nbkq3e);--s-18eec8a: var(--s-1kkti1r);--rfaik3: var(--s-13ypoy8);--s-1xn7irg: var(--s-1bcqfda);--s-1x4qw9u: var(--s-13ypoy8);--s-4m5wr6: var(--s-1bcqfda);--s-1mbtsu2: var(--s-13ypoy8);--s-1im6yhz: var(--s-13ypoy8);--syi4h: var(--s-13ypoy8);--a37hit: var(--s-13ypoy8);--s-2av06t: var(--s-114rdv4);--s-1pjx0uz: var(--s-1bcqfda);--s-175jw0u: var(--s-114rdv4);--pz1vgx: var(--s-1wdog5l);--s-6j56kn: var(--s-1egalvn);--jg0c26: var(--s-1sypgcr);--s-1g3vynh: var(--s-1bf76tl);--lg8mcu: var(--s-1m519r1);--s-12izfvv: var(--s-18tv9xz);--s-1t53zya: var(--nxbwn6);--zuu90a: var(--qcdf10);--s-414lsb: var(--p5cdic);--ulpd63: var(--fox699);--s-15wlbw2: var(--s-1qk1a9q);--s-1dn6rk: var(--s-1j0j6fb);--s-1k641wx: var(--gqp7g1);--aw0phz: var(--xi7x09);--s-15xulsv: var(--s-1kkti1r);--w22o9l: var(--s-1b0l18k);--s-8c655s: var(--pxx34h);--s-1ok36r9: var(--pxx34h);--s-158s5xz: var(--s-1b0l18k);--xw6qjn: var(--s-1b0l18k);--s-4lkz9i: var(--s-15xulsv);--s-1amkzr1: var(--s-1kmer3i);--s-17kovyh: var(--s-15xulsv);--s-125pidq: var(--s-15xulsv);--s-8to5ry: var(--s-15xulsv);--s-17n5yam: var(--xi7x09);--eyrjow: var(--s-9ukgu0);--s-1u2do9: var(--s-9ukgu0);--qzxx9l: var(--xi7x09);--s-1draesn: var(--xi7x09);--s-17tmi4r: var(--s-1kkti1r);--b7ifjk: var(--xi7x09);--s-6o7nrw: var(--uk4ts2);--s-73zwar: var(--xi7x09);--d3be3c: var(--xi7x09);--npx6zl: var(--xi7x09);--wt6h1z: var(--s-1nbkq3e);--s-19hm5u2: var(--s-1b0l18k);--s-1ki2h5s: var(--s-1b0l18k);--s-1upode3: var(--s-1nbkq3e);--e619vt: var(--s-1kkti1r);--h29g9m: var(--s-1kmer3i);--o26ijo: var(--s-1kkti1r);--s-1fqa73g: var(--s-1kkti1r);--s-1t2fj50: var(--s-1kkti1r);--s-1p5fyku: var(--s-1kkti1r);--s-7st1q: var(--s-1kkti1r);--s-177yrws: var(--s-1wdog5l);--s-1x5q6fw: var(--s-1egalvn);--s-1cn97xm: var(--u7pgeo);--s-9nkfwt: var(--u7pgeo);--s-7pqyn6: var(--s-1m519r1);--s-9bkbz: var(--s-660zz9);--s-1qd49a9: var(--s-660zz9);--s-17mlsdr: var(--qcdf10);--s-1ow1a4n: var(--s-1jh7fp5);--s-1mnr65s: var(--s-1jh7fp5);--s-1yfj4t4: var(--s-1qk1a9q);--fg7f6q: var(--o1xbta);--d8waz0: var(--o1xbta);--s-8cc9re: var(--xi7x09);--s-13hmetb: var(--v2y5bm);--oiv4a4: var(--s-1b0l18k);--s-6obdb0: var(--s-1y0ta6r);--s-17yrw5r: var(--pxx34h);--s-1o9jit1: var(--s-1b0l18k);--s-17snam4: var(--s-13py8ob);--s-1xyyyk2: var(--s-1egalvn);--s-1ui80l2: var(--v2y5bm);--jus5c7: var(--v2y5bm);--s-184ljp4: var(--s-1egalvn);--eb4u9z: var(--jkp57b);--o8bs57: var(--uk4ts2);--s-10w80od: var(--s-9ukgu0);--s-1c9sq9t: var(--s-15yycft);--ruipx: var(--uk4ts2);--s-1wer54: var(--s-13py8ob);--uvjldp: var(--s-13ypoy8);--rygqjm: var(--s-13ypoy8);--s-3zsim4: var(--s-3qadn4);--nqzz7a: var(--s-13ypoy8);--fmcfok: var(--s-13ypoy8);--s-13dhk1f: var(--s-1egalvn);--s-97x5jr: var(--s-1egalvn);--s-148oer1: var(--s-1xkgkxo);--qzwqpe: var(--s-1egalvn);--s-9i3k0u: var(--s-1egalvn);--s-87wktm: var(--s-13ypoy8);--s-13hlbvk: var(--s-13ypoy8);--s-114300b: var(--o1xbta);--l5jmjk: var(--s-13ypoy8);--oalgln: var(--s-13ypoy8);--wukrzp: var(--s-1egalvn);--fa9lug: var(--s-1wdog5l);--s-1oi81m8: var(--s-1egalvn);--x0orno: var(--s-1egalvn);--s-1pxcz58: var(--s-1egalvn);--p0bjsc: var(--s-13py8ob);--u320f7: var(--r3g89x);--s-1iv5nq8: var(--r3g89x);--uj52u9: var(--n0umvo);--s-6v1wws: var(--s-1o92vf6);--s-1tqfmwd: var(--s-1o92vf6);--g8y80y: var(--s-1spzwnv);--uflrw: var(--s-1ipujfj);--jg0bei: var(--s-1ipujfj);--s-1kdpopy: var(--s-1vhr1m);--ibollp: var(--uk4ts2);--evfcf2: var(--uk4ts2);--qj0juw: var(--s-9ukgu0);--s-1u9outy: var(--jkp57b);--s-18brxby: var(--jkp57b);--s-5wyt2d: var(--s-13ypoy8);--s-15m6t6b: var(--s-13ypoy8);--nph474: var(--r3g89x);--s-9j04rl: var(--r3g89x);--s-18eqkid: var(--s-13ypoy8);--k9sgh3: var(--s-1o92vf6);--s-679qlr: var(--s-1o92vf6);--s-1gxwr4: var(--s-13ypoy8);--i7djdz: var(--s-1ipujfj);--s-1yqvg4v: var(--s-13ypoy8);--s-1uywv9f: var(--uk4ts2);--xfgvhn: var(--uk4ts2);--s-1l3ikln: var(--s-13ypoy8);--s-1hknj82: var(--v2y5bm);--xd9t29: var(--v2y5bm);--s-1qz4hey: var(--s-1xkgkxo);--s-13mj3ey: var(--s-1nbkq3e);--yfq5jb: var(--s-1b0l18k);--s-1d5tn5g: var(--s-1y0ta6r);--s-1ts3wnp: var(--s-1nbkq3e);--mtnc2e: var(--s-1kmer3i);--s-1ggs8se: var(--s-1xkgkxo);--s-1983a3r: var(--s-1egalvn);--s-1rbj8zq: var(--v2y5bm);--s-12x7xov: var(--s-1xkgkxo);--q5xz4t: var(--s-1wdog5l);--s-2ojt3v: var(--xi7x09);--s-1c4musi: var(--uk4ts2);--rwzmwu: var(--s-9ukgu0);--s-1k156kb: var(--xi7x09);--s-1njcrbd: var(--s-1kmer3i);--s-1auir75: var(--s-13ypoy8);--tipuka: var(--s-13ypoy8);--s-1myp5o1: var(--s-3qadn4);--s-5didwj: var(--s-13ypoy8);--s-1wf2wvi: var(--s-13ypoy8);--s-15w0yfc: var(--s-1qz4hey);--fc8g0t: var(--s-1qz4hey);--s-17uj1m3: var(--jkp57b);--g8dxu4: var(--s-1qz4hey);--s-2e4gj5: var(--s-1qz4hey);--s-1xsl5v6: var(--s-13ypoy8);--s-1vjzvov: var(--s-13ypoy8);--s-1n46b59: var(--o1xbta);--u90thq: var(--s-13ypoy8);--s-19o7zaa: var(--s-13ypoy8);--s-10q3p1o: var(--s-1xkgkxo);--s-8jpmhq: var(--s-1xkgkxo);--s-1nuytc0: var(--s-1xkgkxo);--s-1vua7kb: var(--s-1xkgkxo);--brnaxe: var(--s-1kmer3i);--s-1ufxgw0: var(--s-13ypoy8);--qth5g3: var(--s-13ypoy8);--s-1hd7tld: var(--s-13ypoy8);--s-40ljxg: var(--s-13ypoy8);--s-1aln5xz: var(--s-114rdv4);--s-49rsbu: var(--s-1m519r1);--xsdaas: var(--s-1m519r1);--mglbt2: var(--r3g89x);--rtvqux: var(--qcdf10);--ko7qd: var(--qcdf10);--s-50f0qm: var(--s-1o92vf6);--eu61bi: var(--s-1qk1a9q);--y7jsf0: var(--s-1qk1a9q);--s-1ac7lwk: var(--s-1ipujfj);--s-9k5091: var(--xi7x09);--ruhzmh: var(--xi7x09);--s-2xp72p: var(--uk4ts2);--s-17iqe5q: var(--s-1wdog5l);--s-1253b2y: var(--s-1wdog5l);--s-1piwg9i: var(--s-13ypoy8);--s-7oniqh: var(--s-13ypoy8);--s-6ucdv7: var(--s-1m519r1);--s-1jcoye7: var(--s-1m519r1);--hnqjk9: var(--s-13ypoy8);--pgimab: var(--qcdf10);--xntlbj: var(--qcdf10);--s-14mlsvd: var(--s-13ypoy8);--s-1exie7f: var(--s-1qk1a9q);--yqmt02: var(--s-1qk1a9q);--s-17qjsgp: var(--s-13ypoy8);--e6rr02: var(--xi7x09);--qwe25a: var(--xi7x09);--s-1cx6227: var(--s-13ypoy8);--s-1o2c3h9: var(--s-1wdog5l);--s-6gs83q: var(--s-1egalvn);--ahgtyg: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';--dilwm: 2048;--s-6omq4: 1980;--nsaztv: 1443;--s-1ixv1ks: 1078;--s-1biv3ye: -432;--s-1te2tup: 0;--cdmbir: 300;--s-1mnxhel: 400;--s-1nt3wam: 600;--s-1ocxf4e: 700;--s-1vpgvqc: 'Source Code Pro', Menlo, Monaco, monospace;--s-1y398ge: 2048;--j5b9ko: 1556;--s-17c3qcu: 1493;--s-6zqpne: 1120;--s-1jib5q0: -492;--s-75pjiv: 410;--s-780oqg: var(--ahgtyg);--s-1c2w534: var(--dilwm);--s-4imvpn: var(--s-6omq4);--s-1ph4673: var(--nsaztv);--s-14qchrt: var(--s-1ixv1ks);--s-174cqiz: var(--s-1biv3ye);--s-1rnjjay: var(--s-1te2tup);--bwm4no: var(--s-1mnxhel);--s-1bfvuc2: var(--s-1i82044);--s-1vo01ya: var(--s-1db3chc);--s-1nrhtfr: var(--tk0isw);--s-1xlut57: var(--s-1lhqll2);--s-10rtirn: var(--s-11v0pqn);--s-1gj0nto: var(--s-6cbmuf);--z8c3ww: var(--yplwvi);--s-1itdcoa: var(--s-1m30mdf);--s-1e47fbj: var(--cd4zwn);--s-1i82044: var(--s-780oqg);--s-1db3chc: var(--s-1c2w534);--tk0isw: var(--s-4imvpn);--s-1lhqll2: var(--s-1ph4673);--s-11v0pqn: var(--s-14qchrt);--s-6cbmuf: var(--s-174cqiz);--yplwvi: var(--s-1rnjjay);--s-1m30mdf: 56px;--cd4zwn: 64px;--s-1fgn2x1: var(--s-1ocxf4e);--g8k6lo: var(--s-1mnxhel);--simh7g: var(--wsbs66);--s-11tag5s: var(--s-1cfwdq);--egn7v3: var(--s-18ll6fg);--s-1rfbcod: var(--s-13spi5k);--s-1luqrck: var(--s-15fn66i);--s-27iqeg: var(--d5drjy);--s-18wcjw: var(--s-1rsg6td);--s-1u9zl82: var(--n6jam8);--miv9l: var(--lq97ov);--wsbs66: var(--s-780oqg);--s-1cfwdq: var(--s-1c2w534);--s-18ll6fg: var(--s-4imvpn);--s-13spi5k: var(--s-1ph4673);--s-15fn66i: var(--s-14qchrt);--d5drjy: var(--s-174cqiz);--s-1rsg6td: var(--s-1rnjjay);--n6jam8: 48px;--lq97ov: 56px;--s-1ucmgz7: var(--s-1ocxf4e);--s-17ghi8h: var(--s-1mnxhel);--hbk0oo: var(--s-1wwy80b);--s-2dbb2a: var(--s-160c6gg);--yxaojm: var(--s-1npqh71);--nm1xrx: var(--s-68sjx3);--s-1ivbjtl: var(--wejrbv);--s-8vhotc: var(--si2vzf);--pakukh: var(--s-7035h);--icmlh7: var(--ad7wce);--s-8mv65e: var(--s-12zbgfl);--s-1wwy80b: var(--s-780oqg);--s-160c6gg: var(--s-1c2w534);--s-1npqh71: var(--s-4imvpn);--s-68sjx3: var(--s-1ph4673);--wejrbv: var(--s-14qchrt);--si2vzf: var(--s-174cqiz);--s-7035h: var(--s-1rnjjay);--ad7wce: 40px;--s-12zbgfl: 48px;--s-1xgajx6: var(--s-1ocxf4e);--s-1mb7r8p: var(--s-1mnxhel);--s-1jtr8l0: var(--dx0zsf);--bzblmh: var(--s-1s7fwor);--s-13z63vp: var(--s-1z08gqp);--s-1noeuap: var(--fdri1y);--s-1iotv3v: var(--s-1ktva78);--s-18s8xzd: var(--jrvk1a);--s-1xijmep: var(--s-62671d);--s-1nph8pw: var(--s-1eryk2b);--s-5jpu2o: var(--s-1rvvcgm);--dx0zsf: var(--s-780oqg);--s-1s7fwor: var(--s-1c2w534);--s-1z08gqp: var(--s-4imvpn);--fdri1y: var(--s-1ph4673);--s-1ktva78: var(--s-14qchrt);--jrvk1a: var(--s-174cqiz);--s-62671d: var(--s-1rnjjay);--s-1eryk2b: 32px;--s-1rvvcgm: 40px;--nusmm3: var(--s-1ocxf4e);--xcedj6: var(--ahgtyg);--s-14xlm6o: var(--dilwm);--msg65c: var(--s-6omq4);--s-1ywnfza: var(--nsaztv);--zjva6a: var(--s-1ixv1ks);--s-15n3uo5: var(--s-1biv3ye);--i6u0ap: var(--s-1te2tup);--xb6tkh: var(--s-1mnxhel);--s-1xmxn4q: var(--s-71ssjp);--s-1xgixpx: var(--db0w5x);--s-1k35674: var(--jed2z7);--s-12k91a7: var(--tv79ff);--s-1s0wyj4: var(--s-1x8so7v);--ig6ly8: var(--s-1j7acn3);--s-8l4ca5: var(--s-38ks7n);--s-1svi9x0: var(--x65r8g);--d7hr4e: var(--s-14j81vx);--s-1ylzxkj: var(--oq2dkr);--s-71ssjp: var(--xcedj6);--db0w5x: var(--s-14xlm6o);--jed2z7: var(--msg65c);--tv79ff: var(--s-1ywnfza);--s-1x8so7v: var(--zjva6a);--s-1j7acn3: var(--s-15n3uo5);--s-38ks7n: var(--i6u0ap);--x65r8g: 28px;--s-14j81vx: 36px;--s-1n4fl4h: var(--s-1ocxf4e);--oq2dkr: none;--f4w18u: var(--s-1mnxhel);--s-1rpa4qr: var(--jdmia2);--v1v838: var(--ts1hpc);--vn27bl: var(--s-187zl0b);--s-1vnqflb: var(--s-12s5kmm);--s-1n4dokk: var(--s-4fox1q);--wb62lm: var(--j3z1dw);--s-1f8ywlh: var(--s-1jvq51g);--s-1uud5hl: var(--s-1joebgy);--s-1qj9g61: var(--s-19hh4gw);--s-1bvu74j: var(--hdrt9t);--jdmia2: var(--xcedj6);--ts1hpc: var(--s-14xlm6o);--s-187zl0b: var(--msg65c);--s-12s5kmm: var(--s-1ywnfza);--s-4fox1q: var(--zjva6a);--j3z1dw: var(--s-15n3uo5);--s-1jvq51g: var(--i6u0ap);--s-1joebgy: 24px;--s-19hh4gw: 32px;--g65i9c: var(--s-1ocxf4e);--hdrt9t: none;--wpt2ge: var(--s-1mnxhel);--w4jvxk: var(--s-1bq9l67);--s-1mflgki: var(--s-1xsxprz);--s-1517qlh: var(--qfwzw4);--sdtaur: var(--o2sqss);--s-6qvd4o: var(--xxsoub);--y4gv3: var(--s-1hw9qk9);--s-193lww5: var(--s-9rewa3);--yem2xc: var(--s-1k0d4db);--s-1uz67ki: var(--syp0fc);--b4hhf7: var(--s-18pg62i);--s-1bq9l67: var(--xcedj6);--s-1xsxprz: var(--s-14xlm6o);--qfwzw4: var(--msg65c);--o2sqss: var(--s-1ywnfza);--xxsoub: var(--zjva6a);--s-1hw9qk9: var(--s-15n3uo5);--s-9rewa3: var(--i6u0ap);--s-1k0d4db: 20px;--syp0fc: 28px;--s-1vfd5li: var(--s-1ocxf4e);--s-18pg62i: none;--s-1p87an6: var(--s-1mnxhel);--gbhvil: var(--s-1tckhn5);--s-2wlxzm: var(--s-1bnzo0w);--s-1lhh5an: var(--ub00w8);--b57bg4: var(--vayv2j);--s-10pihpx: var(--s-1bg5wjj);--s-1de7swi: var(--ofc8t8);--p0d0ra: var(--s-1myygfh);--rdvhzd: var(--s-1vrlxop);--wxjtoa: var(--s-1fjdblk);--s-14i6ex0: var(--s-176iwse);--s-1tckhn5: var(--xcedj6);--s-1bnzo0w: var(--s-14xlm6o);--ub00w8: var(--msg65c);--vayv2j: var(--s-1ywnfza);--s-1bg5wjj: var(--zjva6a);--ofc8t8: var(--s-15n3uo5);--s-1myygfh: var(--i6u0ap);--s-1vrlxop: 16px;--s-1fjdblk: 24px;--s-15lxxlk: var(--s-1ocxf4e);--s-176iwse: none;--ihun98: var(--s-1mnxhel);--lzkj6b: var(--s-1fz1zwb);--s-19gq58y: var(--s-1e9sg5q);--s-1fndoqe: var(--s-1xty0l1);--s-1ozmd2v: var(--s-1c9087t);--s-1itf6ev: var(--njr6lf);--lqlo87: var(--wvavyz);--s-15g638a: var(--s-1bdp00y);--s-101nale: var(--s-1rv6t4);--rpuu4f: var(--onmy4p);--s-1x2ggh5: var(--s-135hi2l);--s-1fz1zwb: var(--xcedj6);--s-1e9sg5q: var(--s-14xlm6o);--s-1xty0l1: var(--msg65c);--s-1c9087t: var(--s-1ywnfza);--njr6lf: var(--zjva6a);--wvavyz: var(--s-15n3uo5);--s-1bdp00y: var(--i6u0ap);--s-1rv6t4: 12px;--onmy4p: 20px;--s-4yu78: var(--s-1ocxf4e);--s-135hi2l: none;--qsps49: var(--ahgtyg);--s-1m5o6xs: var(--dilwm);--s-1sl6m46: var(--s-6omq4);--s-1tlryov: var(--nsaztv);--kidu0o: var(--s-1ixv1ks);--l2fksn: var(--s-1biv3ye);--s-16fd3c8: var(--s-1te2tup);--s-1n41s7u: var(--s-1nt3wam);--njb836: var(--s-108w7yg);--s-18nbbqu: var(--s-6mvx34);--b9ogvo: var(--s-1pbhbhw);--h3wc70: var(--z5eq11);--u4c2q6: var(--e1e86);--s-1oj6z6t: var(--uik06i);--s-1qtuyvq: var(--s-1eah8e8);--l28r8y: var(--h7f28h);--fcsdep: var(--s-1vvlcgn);--s-1ikrpfx: var(--s-36ddn3);--s-108w7yg: var(--qsps49);--s-6mvx34: var(--s-1m5o6xs);--s-1pbhbhw: var(--s-1sl6m46);--z5eq11: var(--s-1tlryov);--e1e86: var(--kidu0o);--uik06i: var(--l2fksn);--s-1eah8e8: var(--s-16fd3c8);--h7f28h: 18px;--s-1vvlcgn: 28px;--s-5hgyej: var(--s-1mnxhel);--s-36ddn3: none;--p1b3a1: var(--s-1nt3wam);--s-10jfra1: var(--wtyf0o);--s-1m1wff1: var(--s-167pe37);--s-1savn4h: var(--s-10fnwqi);--s-1gygsl6: var(--s-1sdpwmi);--li3rbu: var(--s-1prlirw);--s-9cy93t: var(--s-1oay49k);--s-11a5wqu: var(--b7x093);--s-17qz9cg: var(--s-1nk8z4c);--s-1pqj9m0: var(--s-1adv7ix);--s-1ctdufq: var(--s-2vga1d);--wtyf0o: var(--qsps49);--s-167pe37: var(--s-1m5o6xs);--s-10fnwqi: var(--s-1sl6m46);--s-1sdpwmi: var(--s-1tlryov);--s-1prlirw: var(--kidu0o);--s-1oay49k: var(--l2fksn);--b7x093: var(--s-16fd3c8);--s-1nk8z4c: 16px;--s-1adv7ix: 24px;--e9j7zt: var(--s-1mnxhel);--s-2vga1d: none;--s-1e6wgok: var(--s-1nt3wam);--s-5twc1q: var(--iv638n);--s-13v453w: var(--zzbkbv);--q47ujb: var(--cw4443);--s-4fq1f8: var(--sf9nah);--s-8kvr39: var(--s-1lduq5c);--t9sogg: var(--s-49369g);--s-6dkjzu: var(--s-195juhb);--s-1wizgxe: var(--eoafo5);--s-7ih227: var(--s-7paqqe);--be5p7j: var(--pz3gk9);--iv638n: var(--qsps49);--zzbkbv: var(--s-1m5o6xs);--cw4443: var(--s-1sl6m46);--sf9nah: var(--s-1tlryov);--s-1lduq5c: var(--kidu0o);--s-49369g: var(--l2fksn);--s-195juhb: var(--s-16fd3c8);--eoafo5: 14px;--s-7paqqe: 20px;--x5dpqz: var(--s-1mnxhel);--pz3gk9: none;--pyk6k1: var(--ahgtyg);--s-1verpm8: var(--dilwm);--rd4b92: var(--s-6omq4);--s-1i90hyx: var(--nsaztv);--y96hdk: var(--s-1ixv1ks);--qkji3r: var(--s-1biv3ye);--s-1kwoc9c: var(--s-1te2tup);--s-1qv548f: var(--s-1nt3wam);--s-1tq5jkt: var(--v43x2t);--s-3uli8c: var(--tcmtp2);--s-10wdlk9: var(--g77870);--s-1iqa1pt: var(--s-1xy9kgq);--vxd1ew: var(--wqx1if);--w2b5wa: var(--s-1fysgfv);--s-16ck0e3: var(--s-18527no);--okauee: var(--s-1rxtcbb);--s-1fhkvft: var(--s-1a3m0xe);--hj8sur: var(--ayuh76);--v43x2t: var(--pyk6k1);--tcmtp2: var(--s-1verpm8);--g77870: var(--rd4b92);--s-1xy9kgq: var(--s-1i90hyx);--wqx1if: var(--y96hdk);--s-1fysgfv: var(--qkji3r);--s-18527no: var(--s-1kwoc9c);--s-1rxtcbb: 16px;--s-1a3m0xe: 24px;--s-5y4pqp: var(--s-1mnxhel);--ayuh76: none;--ep1e0f: var(--s-1nt3wam);--s-6vkd26: var(--huplq6);--s-1h9quwx: var(--l1gcj7);--t2iyzt: var(--s-3mrwm8);--s-1xn3ax7: var(--l6yv66);--s-15oh72s: var(--s-1k1xktp);--s-1ohirt0: var(--s-3dxl6s);--juchqv: var(--s7es0h);--s-1g9cdsy: var(--tlxlq6);--yfph9h: var(--s-432ttp);--r31u81: var(--s-59wabm);--huplq6: var(--pyk6k1);--l1gcj7: var(--s-1verpm8);--s-3mrwm8: var(--rd4b92);--l6yv66: var(--s-1i90hyx);--s-1k1xktp: var(--y96hdk);--s-3dxl6s: var(--qkji3r);--s7es0h: var(--s-1kwoc9c);--tlxlq6: 14px;--s-432ttp: 20px;--s-1htz8iq: var(--s-1mnxhel);--s-59wabm: none;--ereqaf: var(--s-1nt3wam);--yiyhsh: var(--ft4em7);--sodrin: var(--ngt1c6);--bfuocu: var(--s-1vj0i13);--s-2nir93: var(--c3yjur);--s-1jh3kwa: var(--r99a4f);--hfec15: var(--s-19xhaty);--s-16ewvzx: var(--ctnn8n);--zzbsa1: var(--mae4h0);--ki0zdj: var(--s-1kc6i1b);--s-12qaksx: var(--s-1k0dbzs);--ft4em7: var(--pyk6k1);--ngt1c6: var(--s-1verpm8);--s-1vj0i13: var(--rd4b92);--c3yjur: var(--s-1i90hyx);--r99a4f: var(--y96hdk);--s-19xhaty: var(--qkji3r);--ctnn8n: var(--s-1kwoc9c);--mae4h0: 12px;--s-1kc6i1b: 16px;--s-10ubhie: var(--s-1mnxhel);--s-1k0dbzs: none;--l5cirb: var(--s-1camloi);--s-3ab8ub: var(--s-1fverle);--s-15f02i8: var(--s-2c6wsx);--s-1f29tr2: var(--s-19hyq79);--s-18tqzme: var(--s-1wum1rt);--s-1s3tcwv: var(--s-1p07rxq);--s-1sr9szs: var(--s-18ns0of);--s-72fzvy: 0px;--s-1n66wtu: 1px;--s-1camloi: 2px;--s-1fverle: 4px;--s-1eo1l6l: 6px;--s-2c6wsx: 8px;--s-14t02z3: 10px;--s-1cn5k4b: 12px;--s-10yt1e6: 14px;--s-19hyq79: 16px;--zmqxvl: 18px;--s-16s2r5d: 20px;--s-1wum1rt: 24px;--s-11p7nl: 28px;--s-1p07rxq: 32px;--s-18g2og9: 36px;--x3ux79: 40px;--s-18ns0of: 48px;--s-7dpk8n: 56px;--s-1ubl41v: 64px;--s-12tsswl: 72px;--s-1e1s3yj: 80px;--s-1c4fwdw: var(--s-282tnx);--jpxxql: var(--s-282tnx);--u4yslg: none;--s-1l4o7cj: 4px;--s-282tnx: 6px;--s-9fb64w: 8px;--s-721m59: 12px;--eazveb: 16px;--s-1pfp217: 9999em;--s-11c5ftm: solid;--s-5oekti: dashed;--s-12pesem: 1px;--s-1p3l5ml: 2px;--f0gr6w: 4px;--li639m: 100%;--s-18ciw8m: min-content;--s-15qxt3g: max-content;--s-22nfqw: fit-content;--cvc234: 50%;--bcipp6: 33.3333%;--s-1990hu4: 66.6667%;--hrim1e: 25%;--ys322a: 50%;--s-2hrodg: 75%;--ywypcv: 20%;--s-1j1r695: 40%;--s-3qcouv: 60%;--s-1c433cn: 80%;--s-1o6hvkt: 16.6667%;--v94vw1: 33.3333%;--ncjl8c: 50%;--s-14apa3: 66.6667%;--kcudzm: 83.3333%;--s-1sq848d: 8.3333%;--k9vhhg: 16.6667%;--s-1m2eq9s: 25%;--s-1hfpugt: 33.3333%;--s-12j0rnv: 41.6667%;--s-1ce5jho: 50%;--yca82r: 58.3333%;--s-1bb34n7: 66.6667%;--x6iu4: 75%;--s-1qjxzud: 83.3333%;--d52z5c: 91.6667%;--s-1qqjf1s: 0px 1px 1px 0px rgba(0, 0, 0, 0.12), 0px 2px 5px 0px rgba(48, 49, 61, 0.08);--s29i93: 0px 3px 6px 0px rgba(0, 0, 0, 0.12), 0px 7px 14px 0px rgba(48, 49, 61, 0.08);--s-144bgvr: 0px 5px 15px 0px rgba(0, 0, 0, 0.12), 0px 15px 35px 0px rgba(48, 49, 61, 0.08);--qbcnik: 0px 5px 15px 0px rgba(0, 0, 0, 0.12), 0px 15px 35px 0px rgba(48, 49, 61, 0.08), 0px 50px 100px 0px rgba(48, 49, 61, 0.08);--s-46hi4m: var(--s-144bgvr);--s-4fcpev: 0px 0px 15px 0px rgba(0, 0, 0, 0.12), 0px 0px 35px 0px rgba(48, 49, 61, 0.08);--s-8kdpya: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-1q5y78: 0px -1px 1px 0px rgba(20, 19, 78, 0.32);--s-1kgpzka: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-186fre1: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-1fb3eog: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-1ibn4id: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--s-1l32yqd: 0px -1px 1px 0px rgba(16, 17, 26, 0.16);--wq0k6h: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--fur145: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--s-1fecqxp: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--ytuq2g: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--k2t3ri: 0px -1px 1px 0px rgba(62, 2, 26, 0.32);--s-1fc7ea9: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--s-8p4pnm: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--s-1s9evt6: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--pga66p: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--s-7nyne0: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--s-1p8nnzk: 0px -1px 1px 0px rgba(1, 28, 58, 0.16);--s-4fmi5d: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--s-1mw80b4: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--s-1mp6cz9: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--o68lqt: 0px 1px 1px 0px rgba(62, 2, 26, .16);--s-1srjzen: 0px -1px 1px 0px rgba(62, 2, 26, .16);--s-5cda5b: 0px 1px 1px 0px rgba(62, 2, 26, .16);--uojav1: 0px 1px 1px 0px rgba(62, 2, 26, .16);--s-1xpb9p2: 0px 1px 1px 0px rgba(62, 2, 26, .16);--s-1atvbio: 0px -1px 1px 0px rgba(16, 17, 26, 0.16);--s-9l041r: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--fcko44: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--zh5azq: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--tnw4uh: 490px;--p6z4q9: 768px;--s-1tolf8z: 1040px;--s-13qggw6: 1440px;--s-1oz5pfq: 0;--s-52qljy: 490px;--m9yfsr: 768px;--s-1gz3jh8: 1040px;--s-1ad545m: 1440px;--s-1xy6qjm: 0 0 0 4px rgba(1, 150, 237, .36);
}
#​#​#​#​#​#​#​ .tooltip-trigger-isolate {
```

**colly+md**
```
Querying authentication conversion | Stripe Documentation




#​ .sn-1q4qxi9 { --jybopzu-hue-gray0: #ffffff; --jybopzu-hue-gray50: #f6f8fa; --jybopzu-hue-gray100: #ebeef1; --jybopzu-hue-gray150: #d5dbe1; --jybopzu-hue-gray200: #c0c8d2; --jybopzu-hue-gray300: #a3acba; --jybopzu-hue-gray400: #87909f; --jybopzu-hue-gray500: #687385; --jybopzu-hue-gray600: #545969; --jybopzu-hue-gray700: #414552; --jybopzu-hue-gray800: #30313d; --jybopzu-hue-gray900: #1a1b25; --jybopzu-hue-gray950: #10111a; --jybopzu-hue-blue50: #ddfffe; --jybopzu-hue-blue100: #cff5f6; --jybopzu-hue-blue150: #a2e5ef; --jybopzu-hue-blue200: #75d5e8; --jybopzu-hue-blue300: #06b9ef; --jybopzu-hue-blue400: #0096eb; --jybopzu-hue-blue500: #0570de; --jybopzu-hue-blue600: #0055bc; --jybopzu-hue-blue700: #04438c; --jybopzu-hue-blue800: #003262; --jybopzu-hue-blue900: #011c3a; --jybopzu-hue-green50: #ecfed7; --jybopzu-hue-green100: #d7f7c2; --jybopzu-hue-green150: #a6eb84; --jybopzu-hue-green200: #76df47; --jybopzu-hue-green300: #48c404; --jybopzu-hue-green400: #3fa40d; --jybopzu-hue-green500: #228403; --jybopzu-hue-green600: #006908; --jybopzu-hue-green700: #0b5019; --jybopzu-hue-green800: #043b15; --jybopzu-hue-green900: #02220d; --jybopzu-hue-orange50: #fef9da; --jybopzu-hue-orange100: #fcedb9; --jybopzu-hue-orange150: #fcd579; --jybopzu-hue-orange200: #fcbd3a; --jybopzu-hue-orange300: #ff8f0e; --jybopzu-hue-orange400: #ed6704; --jybopzu-hue-orange500: #c84801; --jybopzu-hue-orange600: #a82c00; --jybopzu-hue-orange700: #842106; --jybopzu-hue-orange800: #5f1a05; --jybopzu-hue-orange900: #331302; --jybopzu-hue-red50: #fff5fa; --jybopzu-hue-red100: #ffe7f2; --jybopzu-hue-red150: #ffccdf; --jybopzu-hue-red200: #ffb1cd; --jybopzu-hue-red300: #fe87a1; --jybopzu-hue-red400: #fc526a; --jybopzu-hue-red500: #df1b41; --jybopzu-hue-red600: #b3093c; --jybopzu-hue-red700: #890d37; --jybopzu-hue-red800: #68052b; --jybopzu-hue-red900: #3e021a; --jybopzu-hue-purple50: #f9f7ff; --jybopzu-hue-purple100: #f2ebff; --jybopzu-hue-purple150: #dfd3fc; --jybopzu-hue-purple200: #d1befe; --jybopzu-hue-purple300: #b49cfc; --jybopzu-hue-purple400: #8d7ffa; --jybopzu-hue-purple500: #625afa; --jybopzu-hue-purple600: #513dd9; --jybopzu-hue-purple700: #3f32a1; --jybopzu-hue-purple800: #302476; --jybopzu-hue-purple900: #14134e; --jybopzu-color-neutral0: var(--jybopzu-hue-gray0); --jybopzu-color-neutral50: var(--jybopzu-hue-gray50); --jybopzu-color-neutral100: var(--jybopzu-hue-gray100); --jybopzu-color-neutral150: var(--jybopzu-hue-gray150); --jybopzu-color-neutral200: var(--jybopzu-hue-gray200); --jybopzu-color-neutral300: var(--jybopzu-hue-gray300); --jybopzu-color-neutral400: var(--jybopzu-hue-gray400); --jybopzu-color-neutral500: var(--jybopzu-hue-gray500); --jybopzu-color-neutral600: var(--jybopzu-hue-gray600); --jybopzu-color-neutral700: var(--jybopzu-hue-gray700); --jybopzu-color-neutral800: var(--jybopzu-hue-gray800); --jybopzu-color-neutral900: var(--jybopzu-hue-gray900); --jybopzu-color-neutral950: var(--jybopzu-hue-gray950); --jybopzu-color-brand50: var(--jybopzu-hue-purple50); --jybopzu-color-brand100: var(--jybopzu-hue-purple100); --jybopzu-color-brand200: var(--jybopzu-hue-purple200); --jybopzu-color-brand300: var(--jybopzu-hue-purple300); --jybopzu-color-brand400: var(--jybopzu-hue-purple400); --jybopzu-color-brand500: var(--jybopzu-hue-purple500); --jybopzu-color-brand600: var(--jybopzu-hue-purple600); --jybopzu-color-brand700: var(--jybopzu-hue-purple700); --jybopzu-color-brand800: var(--jybopzu-hue-purple800); --jybopzu-color-brand900: var(--jybopzu-hue-purple900); --jybopzu-color-info50: var(--jybopzu-hue-blue50); --jybopzu-color-info100: var(--jybopzu-hue-blue100); --jybopzu-color-info150: var(--jybopzu-hue-blue150); --jybopzu-color-info200: var(--jybopzu-hue-blue200); --jybopzu-color-info300: var(--jybopzu-hue-blue300); --jybopzu-color-info400: var(--jybopzu-hue-blue400); --jybopzu-color-info500: var(--jybopzu-hue-blue500); --jybopzu-color-info600: var(--jybopzu-hue-blue600); --jybopzu-color-info700: var(--jybopzu-hue-blue700); --jybopzu-color-info800: var(--jybopzu-hue-blue800); --jybopzu-color-info900: var(--jybopzu-hue-blue900); --jybopzu-color-success50: var(--jybopzu-hue-green50); --jybopzu-color-success100: var(--jybopzu-hue-green100); --jybopzu-color-success150: var(--jybopzu-hue-green150); --jybopzu-color-success200: var(--jybopzu-hue-green200); --jybopzu-color-success300: var(--jybopzu-hue-green300); --jybopzu-color-success400: var(--jybopzu-hue-green400); --jybopzu-color-success500: var(--jybopzu-hue-green500); --jybopzu-color-success600: var(--jybopzu-hue-green600); --jybopzu-color-success700: var(--jybopzu-hue-green700); --jybopzu-color-success800: var(--jybopzu-hue-green800); --jybopzu-color-success900: var(--jybopzu-hue-green900); --jybopzu-color-attention50: var(--jybopzu-hue-orange50); --jybopzu-color-attention100: var(--jybopzu-hue-orange100); --jybopzu-color-attention150: var(--jybopzu-hue-orange150); --jybopzu-color-attention200: var(--jybopzu-hue-orange200); --jybopzu-color-attention300: var(--jybopzu-hue-orange300); --jybopzu-color-attention400: var(--jybopzu-hue-orange400); --jybopzu-color-attention500: var(--jybopzu-hue-orange500); --jybopzu-color-attention600: var(--jybopzu-hue-orange600); --jybopzu-color-attention700: var(--jybopzu-hue-orange700); --jybopzu-color-attention800: var(--jybopzu-hue-orange800); --jybopzu-color-attention900: var(--jybopzu-hue-orange900); --jybopzu-color-critical50: var(--jybopzu-hue-red50); --jybopzu-color-critical100: var(--jybopzu-hue-red100); --jybopzu-color-critical150: var(--jybopzu-hue-red150); --jybopzu-color-critical200: var(--jybopzu-hue-red200); --jybopzu-color-critical300: var(--jybopzu-hue-red300); --jybopzu-color-critical400: var(--jybopzu-hue-red400); --jybopzu-color-critical500: var(--jybopzu-hue-red500); --jybopzu-color-critical600: var(--jybopzu-hue-red600); --jybopzu-color-critical700: var(--jybopzu-hue-red700); --jybopzu-color-critical800: var(--jybopzu-hue-red800); --jybopzu-color-critical900: var(--jybopzu-hue-red900); --jybopzu-backgroundColor-surface: var(--jybopzu-color-neutral0); --jybopzu-backgroundColor-container: var(--jybopzu-color-neutral50); --jybopzu-borderColor-neutral: var(--jybopzu-color-neutral150); --jybopzu-borderColor-critical: var(--jybopzu-color-critical500); --jybopzu-iconColor-primary: var(--jybopzu-color-neutral600); --jybopzu-iconColor-secondary: var(--jybopzu-color-neutral400); --jybopzu-iconColor-disabled: var(--jybopzu-color-neutral200); --jybopzu-iconColor-brand: var(--jybopzu-color-brand400); --jybopzu-iconColor-info: var(--jybopzu-color-info400); --jybopzu-iconColor-success: var(--jybopzu-color-success400); --jybopzu-iconColor-attention: var(--jybopzu-color-attention400); --jybopzu-iconColor-critical: var(--jybopzu-color-critical400); --jybopzu-textColor-primary: var(--jybopzu-color-neutral700); --jybopzu-textColor-secondary: var(--jybopzu-color-neutral500); --jybopzu-textColor-disabled: var(--jybopzu-color-neutral300); --jybopzu-textColor-brand: var(--jybopzu-color-brand500); --jybopzu-textColor-info: var(--jybopzu-color-info500); --jybopzu-textColor-success: var(--jybopzu-color-success500); --jybopzu-textColor-attention: var(--jybopzu-color-attention500); --jybopzu-textColor-critical: var(--jybopzu-color-critical500); --jybopzu-overflow-hidden: hidden; --jybopzu-radius-none: none; --jybopzu-radius-xsmall: 4px; --jybopzu-radius-small: 4px; --jybopzu-radius-medium: 8px; --jybopzu-radius-large: 10px; --jybopzu-radius-rounded: 999em; --jybopzu-shadow-none: none; --jybopzu-shadow-top: rgb(0 0 0 / 12%) 0px 1px 1px 0px; --jybopzu-shadow-base: rgb(64 68 82 / 8%) 0px 2px 5px 0px, 0 0 0 0 transparent; --jybopzu-shadow-hover: rgb(64 68 82 / 8%) 0px 2px 5px 0px, rgb(64 68 82 / 8%) 0px 3px 9px 0px; --jybopzu-shadow-focus: 0 0 0 4px rgb(1 150 237 / 36%); --jybopzu-size-0: 0px; --jybopzu-size-1: var(--jybopzu-space-1); --jybopzu-size-25: var(--jybopzu-space-25); --jybopzu-size-50: var(--jybopzu-space-50); --jybopzu-size-75: var(--jybopzu-space-75); --jybopzu-size-100: var(--jybopzu-space-100); --jybopzu-size-150: var(--jybopzu-space-150); --jybopzu-size-200: var(--jybopzu-space-200); --jybopzu-size-250: var(--jybopzu-space-250); --jybopzu-size-300: var(--jybopzu-space-300); --jybopzu-size-350: var(--jybopzu-space-350); --jybopzu-size-400: var(--jybopzu-space-400); --jybopzu-size-500: var(--jybopzu-space-500); --jybopzu-size-600: var(--jybopzu-space-600); --jybopzu-size-fill: 100%; --jybopzu-size-min: min-content; --jybopzu-size-max: max-content; --jybopzu-size-fit: fit-content; --jybopzu-size-1\/2: 50%; --jybopzu-size-1\/3: 33.3333%; --jybopzu-size-2\/3: 66.6667%; --jybopzu-size-1\/4: 25%; --jybopzu-size-2\/4: 50%; --jybopzu-size-3\/4: 75%; --jybopzu-size-1\/5: 20%; --jybopzu-size-2\/5: 40%; --jybopzu-size-3\/5: 60%; --jybopzu-size-4\/5: 80%; --jybopzu-size-1\/6: 16.6667%; --jybopzu-size-2\/6: 33.3333%; --jybopzu-size-3\/6: 50%; --jybopzu-size-4\/6: 66.6667%; --jybopzu-size-5\/6: 83.3333%; --jybopzu-size-1\/12: 8.3333%; --jybopzu-size-2\/12: 16.6667%; --jybopzu-size-3\/12: 25%; --jybopzu-size-4\/12: 33.3333%; --jybopzu-size-5\/12: 41.6667%; --jybopzu-size-6\/12: 50%; --jybopzu-size-7\/12: 58.3333%; --jybopzu-size-8\/12: 66.6667%; --jybopzu-size-9\/12: 75%; --jybopzu-size-10\/12: 83.3333%; --jybopzu-size-11\/12: 91.6667%; --jybopzu-space-0: 0px; --jybopzu-space-1: 1px; --jybopzu-space-25: 2px; --jybopzu-space-50: 4px; --jybopzu-space-75: 6px; --jybopzu-space-100: 8px; --jybopzu-space-150: 12px; --jybopzu-space-200: 16px; --jybopzu-space-250: 20px; --jybopzu-space-300: 24px; --jybopzu-space-350: 28px; --jybopzu-space-400: 32px; --jybopzu-space-500: 40px; --jybopzu-space-600: 48px; --jybopzu-space-xxsmall: var(--jybopzu-space-25); --jybopzu-space-xsmall: var(--jybopzu-space-50); --jybopzu-space-small: var(--jybopzu-space-100); --jybopzu-space-medium: var(--jybopzu-space-200); --jybopzu-space-large: var(--jybopzu-space-300); --jybopzu-space-xlarge: var(--jybopzu-space-400); --jybopzu-space-xxlarge: var(--jybopzu-space-600); --jybopzu-typeface-ui: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; --jybopzu-typeface-monospace: 'Source Code Pro', Menlo, Monaco, monospace; --jybopzu-weight-regular: 400; --jybopzu-weight-semibold: 600; --jybopzu-weight-bold: 700; --jybopzu-zIndex-overlay: 299; --jybopzu-zIndex-partial: 400; }#​#​ .rs-3::before {
content: var(--s--baseline-alignment-content);user-select: none;align-self: baseline;margin-right: calc(-1 \* var(--s--column-gap));
}
#​#​ .rs-8[aria-invalid="true"] {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .sail-table-row:not(:hover) .row-actions-trigger {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-4 {
display: var(--s--display-block);
}
#​#​ .rs-2 {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-6:active:not([aria-disabled="true"]) {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .sail-table-row:hover .row-actions-trigger {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-5:hover:not(:active):not([aria-disabled="true"]) {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-7:focus {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .sn-d7kp2a { --distribute-x: initial; --distribute-y: initial; --align-x: initial; --align-y: initial; }
#​#​ .sn-d7kp2a > \* { --align-self-x: initial; --align-self-y: initial; --flex-x: 1 1 auto; --flex-y: 1 1 auto; }
#​#​ .sn-1fnc4mz { --row-gap: normal; --column-gap: normal; gap: var(--row-gap) var(--column-gap); }
#​#​ .sn-1c37ise { --padding-top: 0; --padding-right: 0; --padding-bottom: 0; --padding-left: 0; padding: var(--padding-top) var(--padding-right) var(--padding-bottom) var(--padding-left); }
.\_\_sn-sheet-order { --order: '\_1rkm1cp,\_88mn99,\_5olop,\_16pds2j,\_1wna6e6,\_kskd3k,\_5vzub4,\_lzay40,\_1d9aqya'; }#​#​#​#​#​ .sn-182o7r0 { font-family: var(--jybopzu-typeface-ui); color: var(--jybopzu-textColor-primary); fill: var(--jybopzu-iconColor-primary); -webkit-font-smoothing: antialiased; }#​#​#​#​#​#​#​:root, :host #​#​#​#​#​#​#​, #​#​#​#​#​#​#​ .sn-token-provider {
--s-806179: var(--s-1ipujfj);--qyckuc: 200ms;--s-1xyzpq3: 0ms;--ch7862: 50ms;--s-5jzhfa: 100ms;--s-12b75vv: 150ms;--rsnfo1: 300ms;--s-12ljnrj: 400ms;--s-10dnt5v: cubic-bezier(0, .09, .4, 1);--s-12oyqav: ease-in-out;--im41o8: ease-out;--s-1fdsmh8: ease-in;--s-1pzb1xw: 120;--s-6429u6: 14;--dutg7l: 300;--rjlba6: 20;--s-117eyx7: 400;--slm412: 10;--s-1pt58bw: 30ms;--pu6lsa: 50ms;--s-1ca225m: 80ms;--h9q5hc: 0.95;--s-1308p7c: 0.99;--s-1paplcg: 0.98;--s-19omtc6: 1.02;--eef79q: #ffffff;--s-8qwlk1: #F4F7FA;--o3gs5n: #ECF1F6;--hyhghw: #D4DEE9;--s-1b58r1w: #BAC8DA;--ovqch4: #95A4BA;--ggantb: #7D8BA4;--s-1a8u6zz: #667691;--k08wfi: #50617A;--s-169hr3v: #3C4F69;--ymu9b7: #273951;--ny99wq: #1A2C44;--s-1nmzh8w: #ffffff;--s-421sqo: #e2fbfe;--s-4qj11w: #cbf5fd;--s-1u1nr1c: #a7e7fc;--dj5edy: #6dc9fc;--s-3blua0: #3babfd;--s-172n6d2: #088ef9;--s-1l3w4rb: #0072e9;--s-1yzoj9a: #045ad0;--kvmyi1: #0b46ad;--s-1ah8y8v: #0d3485;--s-1v7mjmv: #0a2156;--s-1cbef47: #ffffff;--ncitdb: #eafcdd;--khndpt: #d1fab3;--fcix74: #a8f170;--s-1jt7b3q: #7cd548;--rz6g85: #58ba27;--s-10in11e: #3da00b;--jet5ih: #2b8700;--s-11ws3zn: #217005;--mkuc60: #1c5a0d;--s-5vneq4: #184310;--s-1ybzlmc: #112a0d;--s-1idvp5s: #ffffff;--s-1ronw4t: #fdf8c9;--een7nd: #fceeb5;--s-1j3zdk7: #fbd992;--bpq42r: #fcaf4f;--d5srfd: #f7870f;--s-7gt7xl: #e46602;--s-1bt4nax: #cc4b00;--s-1m90cr3: #b13600;--s-105rx08: #922700;--s-3csqoi: #701b01;--s-1x99otv: #4a0f02;--s-18rmc6q: #ffffff;--m4edry: #fef4f6;--pfpugw: #fde9ee;--s-1at7tzv: #fbd3dc;--s-8ik67: #faa9b8;--s-1brqpgc: #fa7e91;--s-1k4y65: #fa4a67;--s-1t7w85x: #e61947;--j769ku: #c0123c;--s-105k9ow: #9b0c36;--s-1bradsh: #76072f;--s-17cbcf1: #4e0322;--s-1m3ejd7: #ffffff;--wclsxb: #f7f5fd;--s-1nuetr3: #efecfc;--s-1rgwov0: #e0d9fb;--d427sf: #c3b6fb;--s-1gm5hwl: #a497fc;--d7ng6f: #857afe;--s-1wqs2n2: #675dff;--s-1rqwfiu: #533afd;--cb9l9o: #4e11e2;--b00e2n: #44139f;--yvasq2: #2f0e63;--s-35hf94: hsla(0, 0%, 100%, 0.2);--s-13ypoy8: var(--eef79q);--s-114rdv4: var(--s-8qwlk1);--s-1bcqfda: var(--o3gs5n);--s-1kkti1r: var(--hyhghw);--s-16pqfer: var(--s-1b58r1w);--s-1kmer3i: var(--ovqch4);--s-13py8ob: var(--ggantb);--s-1wdog5l: var(--s-1a8u6zz);--jkp57b: var(--k08wfi);--s-1xkgkxo: var(--s-169hr3v);--s-1egalvn: var(--ymu9b7);--v2y5bm: var(--ny99wq);--s-1ona342: var(--s-1m3ejd7);--s-1xikbvo: var(--wclsxb);--ek860z: var(--s-1nuetr3);--s-3qadn4: var(--s-1rgwov0);--nl7ypg: var(--d427sf);--hm37ax: var(--s-1gm5hwl);--s-142x5wh: var(--d7ng6f);--s-1nbkq3e: var(--s-1wqs2n2);--s-1b0l18k: var(--s-1rqwfiu);--s-1y0ta6r: var(--cb9l9o);--pxx34h: var(--b00e2n);--xp2k2: var(--yvasq2);--s-13od8gw: var(--s-1idvp5s);--fox699: var(--s-1ronw4t);--p5cdic: var(--een7nd);--s-1jh7fp5: var(--s-1j3zdk7);--lsye2d: var(--bpq42r);--t3987n: var(--d5srfd);--s-1vcezov: var(--s-7gt7xl);--s-1qk1a9q: var(--s-1bt4nax);--s-1ipujfj: var(--s-1m90cr3);--s-1vhr1m: var(--s-105rx08);--s-1oqa1l5: var(--s-3csqoi);--kubwak: var(--s-1x99otv);--whf9po: var(--s-18rmc6q);--gqp7g1: var(--m4edry);--s-1j0j6fb: var(--pfpugw);--o1xbta: var(--s-1at7tzv);--vyde9h: var(--s-8ik67);--s-875rxv: var(--s-1brqpgc);--s-1xn82ef: var(--s-1k4y65);--xi7x09: var(--s-1t7w85x);--uk4ts2: var(--j769ku);--s-9ukgu0: var(--s-105k9ow);--s-15yycft: var(--s-1bradsh);--s-1v6ybst: var(--s-17cbcf1);--s-1f39zfp: var(--s-1nmzh8w);--s-1bf76tl: var(--s-421sqo);--s-1sypgcr: var(--s-4qj11w);--u7pgeo: var(--s-1u1nr1c);--qev2nh: var(--dj5edy);--rqlrpr: var(--s-3blua0);--s-8vaodq: var(--s-172n6d2);--s-1m519r1: var(--s-1l3w4rb);--r3g89x: var(--s-1yzoj9a);--n0umvo: var(--kvmyi1);--c0109p: var(--s-1ah8y8v);--s-26e45o: var(--s-1v7mjmv);--s-1a4o86t: var(--s-1cbef47);--nxbwn6: var(--ncitdb);--s-18tv9xz: var(--khndpt);--s-660zz9: var(--fcix74);--s-5y9ijm: var(--s-1jt7b3q);--s-1gwptpc: var(--rz6g85);--t5jail: var(--s-10in11e);--qcdf10: var(--jet5ih);--s-1o92vf6: var(--s-11ws3zn);--s-1spzwnv: var(--mkuc60);--s-35q6a2: var(--s-5vneq4);--axxngb: var(--s-1ybzlmc);--s-1hj7tfd: var(--s-18rmc6q);--s-1xf1h3f: var(--m4edry);--aqxmtx: var(--pfpugw);--s-1um7fco: var(--s-1at7tzv);--d2i300: var(--s-8ik67);--cae9kd: var(--s-1brqpgc);--s-1a4c91b: var(--s-1k4y65);--s-1jvllvw: var(--s-1t7w85x);--x379qy: var(--j769ku);--s-1owp6iv: var(--s-105k9ow);--m26qys: var(--s-1bradsh);--s-3rumb4: var(--s-17cbcf1);--s-5tm7hx: var(--s-1cbef47);--h22sh6: var(--ncitdb);--s-11rdejd: var(--khndpt);--s-1g2t37u: var(--fcix74);--wesn6: var(--s-1jt7b3q);--s-1hhq31p: var(--rz6g85);--yji28s: var(--s-10in11e);--s-169ogke: var(--jet5ih);--hr7syg: var(--s-11ws3zn);--s-14wylcr: var(--mkuc60);--s-289q66: var(--s-5vneq4);--v27jy: var(--s-1ybzlmc);--s-1hldvhn: #9966FF;--s-1xwen3a: #0055BC;--hxpspa: #00A1C2;--s-5ghlc9: #ED6804;--nap71a: #B3063D;--s-1sz15nh: var(--mkuc60);--mygevb: var(--s-1k4y65);--nrw914: var(--s-105rx08);--bu79cc: var(--s-10in11e);--s-1rfvf0n: var(--s-114rdv4);--s-9fypy8: var(--s-13ypoy8);--s-8muhy8: var(--s-35hf94);--s-153sf3j: rgba(186, 200, 218, 0.7);--s-1mkjmgu: var(--s-1b0l18k);--s-9u3gcm: var(--s-1b0l18k);--s-1pk4mhu: var(--s-1y0ta6r);--s-1wze59r: var(--s-1b0l18k);--s-1gzyq0k: var(--s-1b0l18k);--s-1eg71kz: var(--s-9fypy8);--uftl0g: var(--s-9fypy8);--s-1wj6iyq: var(--s-114rdv4);--s-1jrjwpv: var(--s-9fypy8);--b5b0q1: var(--s-9fypy8);--jix8n1: var(--xi7x09);--s-1isx4n7: var(--xi7x09);--s-1owgngi: var(--uk4ts2);--s-1tqa4ka: var(--xi7x09);--s-1dl2eq8: var(--xi7x09);--s-14a2tiz: var(--s-13ypoy8);--s-1b3o71a: var(--s-1nbkq3e);--qkwke3: var(--s-1nbkq3e);--s-1afrigr: var(--s-1b0l18k);--s-1orf6yv: var(--s-1nbkq3e);--s-18eec8a: var(--s-1kkti1r);--rfaik3: var(--s-13ypoy8);--s-1xn7irg: var(--s-1bcqfda);--s-1x4qw9u: var(--s-13ypoy8);--s-4m5wr6: var(--s-1bcqfda);--s-1mbtsu2: var(--s-13ypoy8);--s-1im6yhz: var(--s-13ypoy8);--syi4h: var(--s-13ypoy8);--a37hit: var(--s-13ypoy8);--s-2av06t: var(--s-114rdv4);--s-1pjx0uz: var(--s-1bcqfda);--s-175jw0u: var(--s-114rdv4);--pz1vgx: var(--s-1wdog5l);--s-6j56kn: var(--s-1egalvn);--jg0c26: var(--s-1sypgcr);--s-1g3vynh: var(--s-1bf76tl);--lg8mcu: var(--s-1m519r1);--s-12izfvv: var(--s-18tv9xz);--s-1t53zya: var(--nxbwn6);--zuu90a: var(--qcdf10);--s-414lsb: var(--p5cdic);--ulpd63: var(--fox699);--s-15wlbw2: var(--s-1qk1a9q);--s-1dn6rk: var(--s-1j0j6fb);--s-1k641wx: var(--gqp7g1);--aw0phz: var(--xi7x09);--s-15xulsv: var(--s-1kkti1r);--w22o9l: var(--s-1b0l18k);--s-8c655s: var(--pxx34h);--s-1ok36r9: var(--pxx34h);--s-158s5xz: var(--s-1b0l18k);--xw6qjn: var(--s-1b0l18k);--s-4lkz9i: var(--s-15xulsv);--s-1amkzr1: var(--s-1kmer3i);--s-17kovyh: var(--s-15xulsv);--s-125pidq: var(--s-15xulsv);--s-8to5ry: var(--s-15xulsv);--s-17n5yam: var(--xi7x09);--eyrjow: var(--s-9ukgu0);--s-1u2do9: var(--s-9ukgu0);--qzxx9l: var(--xi7x09);--s-1draesn: var(--xi7x09);--s-17tmi4r: var(--s-1kkti1r);--b7ifjk: var(--xi7x09);--s-6o7nrw: var(--uk4ts2);--s-73zwar: var(--xi7x09);--d3be3c: var(--xi7x09);--npx6zl: var(--xi7x09);--wt6h1z: var(--s-1nbkq3e);--s-19hm5u2: var(--s-1b0l18k);--s-1ki2h5s: var(--s-1b0l18k);--s-1upode3: var(--s-1nbkq3e);--e619vt: var(--s-1kkti1r);--h29g9m: var(--s-1kmer3i);--o26ijo: var(--s-1kkti1r);--s-1fqa73g: var(--s-1kkti1r);--s-1t2fj50: var(--s-1kkti1r);--s-1p5fyku: var(--s-1kkti1r);--s-7st1q: var(--s-1kkti1r);--s-177yrws: var(--s-1wdog5l);--s-1x5q6fw: var(--s-1egalvn);--s-1cn97xm: var(--u7pgeo);--s-9nkfwt: var(--u7pgeo);--s-7pqyn6: var(--s-1m519r1);--s-9bkbz: var(--s-660zz9);--s-1qd49a9: var(--s-660zz9);--s-17mlsdr: var(--qcdf10);--s-1ow1a4n: var(--s-1jh7fp5);--s-1mnr65s: var(--s-1jh7fp5);--s-1yfj4t4: var(--s-1qk1a9q);--fg7f6q: var(--o1xbta);--d8waz0: var(--o1xbta);--s-8cc9re: var(--xi7x09);--s-13hmetb: var(--v2y5bm);--oiv4a4: var(--s-1b0l18k);--s-6obdb0: var(--s-1y0ta6r);--s-17yrw5r: var(--pxx34h);--s-1o9jit1: var(--s-1b0l18k);--s-17snam4: var(--s-13py8ob);--s-1xyyyk2: var(--s-1egalvn);--s-1ui80l2: var(--v2y5bm);--jus5c7: var(--v2y5bm);--s-184ljp4: var(--s-1egalvn);--eb4u9z: var(--jkp57b);--o8bs57: var(--uk4ts2);--s-10w80od: var(--s-9ukgu0);--s-1c9sq9t: var(--s-15yycft);--ruipx: var(--uk4ts2);--s-1wer54: var(--s-13py8ob);--uvjldp: var(--s-13ypoy8);--rygqjm: var(--s-13ypoy8);--s-3zsim4: var(--s-3qadn4);--nqzz7a: var(--s-13ypoy8);--fmcfok: var(--s-13ypoy8);--s-13dhk1f: var(--s-1egalvn);--s-97x5jr: var(--s-1egalvn);--s-148oer1: var(--s-1xkgkxo);--qzwqpe: var(--s-1egalvn);--s-9i3k0u: var(--s-1egalvn);--s-87wktm: var(--s-13ypoy8);--s-13hlbvk: var(--s-13ypoy8);--s-114300b: var(--o1xbta);--l5jmjk: var(--s-13ypoy8);--oalgln: var(--s-13ypoy8);--wukrzp: var(--s-1egalvn);--fa9lug: var(--s-1wdog5l);--s-1oi81m8: var(--s-1egalvn);--x0orno: var(--s-1egalvn);--s-1pxcz58: var(--s-1egalvn);--p0bjsc: var(--s-13py8ob);--u320f7: var(--r3g89x);--s-1iv5nq8: var(--r3g89x);--uj52u9: var(--n0umvo);--s-6v1wws: var(--s-1o92vf6);--s-1tqfmwd: var(--s-1o92vf6);--g8y80y: var(--s-1spzwnv);--uflrw: var(--s-1ipujfj);--jg0bei: var(--s-1ipujfj);--s-1kdpopy: var(--s-1vhr1m);--ibollp: var(--uk4ts2);--evfcf2: var(--uk4ts2);--qj0juw: var(--s-9ukgu0);--s-1u9outy: var(--jkp57b);--s-18brxby: var(--jkp57b);--s-5wyt2d: var(--s-13ypoy8);--s-15m6t6b: var(--s-13ypoy8);--nph474: var(--r3g89x);--s-9j04rl: var(--r3g89x);--s-18eqkid: var(--s-13ypoy8);--k9sgh3: var(--s-1o92vf6);--s-679qlr: var(--s-1o92vf6);--s-1gxwr4: var(--s-13ypoy8);--i7djdz: var(--s-1ipujfj);--s-1yqvg4v: var(--s-13ypoy8);--s-1uywv9f: var(--uk4ts2);--xfgvhn: var(--uk4ts2);--s-1l3ikln: var(--s-13ypoy8);--s-1hknj82: var(--v2y5bm);--xd9t29: var(--v2y5bm);--s-1qz4hey: var(--s-1xkgkxo);--s-13mj3ey: var(--s-1nbkq3e);--yfq5jb: var(--s-1b0l18k);--s-1d5tn5g: var(--s-1y0ta6r);--s-1ts3wnp: var(--s-1nbkq3e);--mtnc2e: var(--s-1kmer3i);--s-1ggs8se: var(--s-1xkgkxo);--s-1983a3r: var(--s-1egalvn);--s-1rbj8zq: var(--v2y5bm);--s-12x7xov: var(--s-1xkgkxo);--q5xz4t: var(--s-1wdog5l);--s-2ojt3v: var(--xi7x09);--s-1c4musi: var(--uk4ts2);--rwzmwu: var(--s-9ukgu0);--s-1k156kb: var(--xi7x09);--s-1njcrbd: var(--s-1kmer3i);--s-1auir75: var(--s-13ypoy8);--tipuka: var(--s-13ypoy8);--s-1myp5o1: var(--s-3qadn4);--s-5didwj: var(--s-13ypoy8);--s-1wf2wvi: var(--s-13ypoy8);--s-15w0yfc: var(--s-1qz4hey);--fc8g0t: var(--s-1qz4hey);--s-17uj1m3: var(--jkp57b);--g8dxu4: var(--s-1qz4hey);--s-2e4gj5: var(--s-1qz4hey);--s-1xsl5v6: var(--s-13ypoy8);--s-1vjzvov: var(--s-13ypoy8);--s-1n46b59: var(--o1xbta);--u90thq: var(--s-13ypoy8);--s-19o7zaa: var(--s-13ypoy8);--s-10q3p1o: var(--s-1xkgkxo);--s-8jpmhq: var(--s-1xkgkxo);--s-1nuytc0: var(--s-1xkgkxo);--s-1vua7kb: var(--s-1xkgkxo);--brnaxe: var(--s-1kmer3i);--s-1ufxgw0: var(--s-13ypoy8);--qth5g3: var(--s-13ypoy8);--s-1hd7tld: var(--s-13ypoy8);--s-40ljxg: var(--s-13ypoy8);--s-1aln5xz: var(--s-114rdv4);--s-49rsbu: var(--s-1m519r1);--xsdaas: var(--s-1m519r1);--mglbt2: var(--r3g89x);--rtvqux: var(--qcdf10);--ko7qd: var(--qcdf10);--s-50f0qm: var(--s-1o92vf6);--eu61bi: var(--s-1qk1a9q);--y7jsf0: var(--s-1qk1a9q);--s-1ac7lwk: var(--s-1ipujfj);--s-9k5091: var(--xi7x09);--ruhzmh: var(--xi7x09);--s-2xp72p: var(--uk4ts2);--s-17iqe5q: var(--s-1wdog5l);--s-1253b2y: var(--s-1wdog5l);--s-1piwg9i: var(--s-13ypoy8);--s-7oniqh: var(--s-13ypoy8);--s-6ucdv7: var(--s-1m519r1);--s-1jcoye7: var(--s-1m519r1);--hnqjk9: var(--s-13ypoy8);--pgimab: var(--qcdf10);--xntlbj: var(--qcdf10);--s-14mlsvd: var(--s-13ypoy8);--s-1exie7f: var(--s-1qk1a9q);--yqmt02: var(--s-1qk1a9q);--s-17qjsgp: var(--s-13ypoy8);--e6rr02: var(--xi7x09);--qwe25a: var(--xi7x09);--s-1cx6227: var(--s-13ypoy8);--s-1o2c3h9: var(--s-1wdog5l);--s-6gs83q: var(--s-1egalvn);--ahgtyg: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';--dilwm: 2048;--s-6omq4: 1980;--nsaztv: 1443;--s-1ixv1ks: 1078;--s-1biv3ye: -432;--s-1te2tup: 0;--cdmbir: 300;--s-1mnxhel: 400;--s-1nt3wam: 600;--s-1ocxf4e: 700;--s-1vpgvqc: 'Source Code Pro', Menlo, Monaco, monospace;--s-1y398ge: 2048;--j5b9ko: 1556;--s-17c3qcu: 1493;--s-6zqpne: 1120;--s-1jib5q0: -492;--s-75pjiv: 410;--s-780oqg: var(--ahgtyg);--s-1c2w534: var(--dilwm);--s-4imvpn: var(--s-6omq4);--s-1ph4673: var(--nsaztv);--s-14qchrt: var(--s-1ixv1ks);--s-174cqiz: var(--s-1biv3ye);--s-1rnjjay: var(--s-1te2tup);--bwm4no: var(--s-1mnxhel);--s-1bfvuc2: var(--s-1i82044);--s-1vo01ya: var(--s-1db3chc);--s-1nrhtfr: var(--tk0isw);--s-1xlut57: var(--s-1lhqll2);--s-10rtirn: var(--s-11v0pqn);--s-1gj0nto: var(--s-6cbmuf);--z8c3ww: var(--yplwvi);--s-1itdcoa: var(--s-1m30mdf);--s-1e47fbj: var(--cd4zwn);--s-1i82044: var(--s-780oqg);--s-1db3chc: var(--s-1c2w534);--tk0isw: var(--s-4imvpn);--s-1lhqll2: var(--s-1ph4673);--s-11v0pqn: var(--s-14qchrt);--s-6cbmuf: var(--s-174cqiz);--yplwvi: var(--s-1rnjjay);--s-1m30mdf: 56px;--cd4zwn: 64px;--s-1fgn2x1: var(--s-1ocxf4e);--g8k6lo: var(--s-1mnxhel);--simh7g: var(--wsbs66);--s-11tag5s: var(--s-1cfwdq);--egn7v3: var(--s-18ll6fg);--s-1rfbcod: var(--s-13spi5k);--s-1luqrck: var(--s-15fn66i);--s-27iqeg: var(--d5drjy);--s-18wcjw: var(--s-1rsg6td);--s-1u9zl82: var(--n6jam8);--miv9l: var(--lq97ov);--wsbs66: var(--s-780oqg);--s-1cfwdq: var(--s-1c2w534);--s-18ll6fg: var(--s-4imvpn);--s-13spi5k: var(--s-1ph4673);--s-15fn66i: var(--s-14qchrt);--d5drjy: var(--s-174cqiz);--s-1rsg6td: var(--s-1rnjjay);--n6jam8: 48px;--lq97ov: 56px;--s-1ucmgz7: var(--s-1ocxf4e);--s-17ghi8h: var(--s-1mnxhel);--hbk0oo: var(--s-1wwy80b);--s-2dbb2a: var(--s-160c6gg);--yxaojm: var(--s-1npqh71);--nm1xrx: var(--s-68sjx3);--s-1ivbjtl: var(--wejrbv);--s-8vhotc: var(--si2vzf);--pakukh: var(--s-7035h);--icmlh7: var(--ad7wce);--s-8mv65e: var(--s-12zbgfl);--s-1wwy80b: var(--s-780oqg);--s-160c6gg: var(--s-1c2w534);--s-1npqh71: var(--s-4imvpn);--s-68sjx3: var(--s-1ph4673);--wejrbv: var(--s-14qchrt);--si2vzf: var(--s-174cqiz);--s-7035h: var(--s-1rnjjay);--ad7wce: 40px;--s-12zbgfl: 48px;--s-1xgajx6: var(--s-1ocxf4e);--s-1mb7r8p: var(--s-1mnxhel);--s-1jtr8l0: var(--dx0zsf);--bzblmh: var(--s-1s7fwor);--s-13z63vp: var(--s-1z08gqp);--s-1noeuap: var(--fdri1y);--s-1iotv3v: var(--s-1ktva78);--s-18s8xzd: var(--jrvk1a);--s-1xijmep: var(--s-62671d);--s-1nph8pw: var(--s-1eryk2b);--s-5jpu2o: var(--s-1rvvcgm);--dx0zsf: var(--s-780oqg);--s-1s7fwor: var(--s-1c2w534);--s-1z08gqp: var(--s-4imvpn);--fdri1y: var(--s-1ph4673);--s-1ktva78: var(--s-14qchrt);--jrvk1a: var(--s-174cqiz);--s-62671d: var(--s-1rnjjay);--s-1eryk2b: 32px;--s-1rvvcgm: 40px;--nusmm3: var(--s-1ocxf4e);--xcedj6: var(--ahgtyg);--s-14xlm6o: var(--dilwm);--msg65c: var(--s-6omq4);--s-1ywnfza: var(--nsaztv);--zjva6a: var(--s-1ixv1ks);--s-15n3uo5: var(--s-1biv3ye);--i6u0ap: var(--s-1te2tup);--xb6tkh: var(--s-1mnxhel);--s-1xmxn4q: var(--s-71ssjp);--s-1xgixpx: var(--db0w5x);--s-1k35674: var(--jed2z7);--s-12k91a7: var(--tv79ff);--s-1s0wyj4: var(--s-1x8so7v);--ig6ly8: var(--s-1j7acn3);--s-8l4ca5: var(--s-38ks7n);--s-1svi9x0: var(--x65r8g);--d7hr4e: var(--s-14j81vx);--s-1ylzxkj: var(--oq2dkr);--s-71ssjp: var(--xcedj6);--db0w5x: var(--s-14xlm6o);--jed2z7: var(--msg65c);--tv79ff: var(--s-1ywnfza);--s-1x8so7v: var(--zjva6a);--s-1j7acn3: var(--s-15n3uo5);--s-38ks7n: var(--i6u0ap);--x65r8g: 28px;--s-14j81vx: 36px;--s-1n4fl4h: var(--s-1ocxf4e);--oq2dkr: none;--f4w18u: var(--s-1mnxhel);--s-1rpa4qr: var(--jdmia2);--v1v838: var(--ts1hpc);--vn27bl: var(--s-187zl0b);--s-1vnqflb: var(--s-12s5kmm);--s-1n4dokk: var(--s-4fox1q);--wb62lm: var(--j3z1dw);--s-1f8ywlh: var(--s-1jvq51g);--s-1uud5hl: var(--s-1joebgy);--s-1qj9g61: var(--s-19hh4gw);--s-1bvu74j: var(--hdrt9t);--jdmia2: var(--xcedj6);--ts1hpc: var(--s-14xlm6o);--s-187zl0b: var(--msg65c);--s-12s5kmm: var(--s-1ywnfza);--s-4fox1q: var(--zjva6a);--j3z1dw: var(--s-15n3uo5);--s-1jvq51g: var(--i6u0ap);--s-1joebgy: 24px;--s-19hh4gw: 32px;--g65i9c: var(--s-1ocxf4e);--hdrt9t: none;--wpt2ge: var(--s-1mnxhel);--w4jvxk: var(--s-1bq9l67);--s-1mflgki: var(--s-1xsxprz);--s-1517qlh: var(--qfwzw4);--sdtaur: var(--o2sqss);--s-6qvd4o: var(--xxsoub);--y4gv3: var(--s-1hw9qk9);--s-193lww5: var(--s-9rewa3);--yem2xc: var(--s-1k0d4db);--s-1uz67ki: var(--syp0fc);--b4hhf7: var(--s-18pg62i);--s-1bq9l67: var(--xcedj6);--s-1xsxprz: var(--s-14xlm6o);--qfwzw4: var(--msg65c);--o2sqss: var(--s-1ywnfza);--xxsoub: var(--zjva6a);--s-1hw9qk9: var(--s-15n3uo5);--s-9rewa3: var(--i6u0ap);--s-1k0d4db: 20px;--syp0fc: 28px;--s-1vfd5li: var(--s-1ocxf4e);--s-18pg62i: none;--s-1p87an6: var(--s-1mnxhel);--gbhvil: var(--s-1tckhn5);--s-2wlxzm: var(--s-1bnzo0w);--s-1lhh5an: var(--ub00w8);--b57bg4: var(--vayv2j);--s-10pihpx: var(--s-1bg5wjj);--s-1de7swi: var(--ofc8t8);--p0d0ra: var(--s-1myygfh);--rdvhzd: var(--s-1vrlxop);--wxjtoa: var(--s-1fjdblk);--s-14i6ex0: var(--s-176iwse);--s-1tckhn5: var(--xcedj6);--s-1bnzo0w: var(--s-14xlm6o);--ub00w8: var(--msg65c);--vayv2j: var(--s-1ywnfza);--s-1bg5wjj: var(--zjva6a);--ofc8t8: var(--s-15n3uo5);--s-1myygfh: var(--i6u0ap);--s-1vrlxop: 16px;--s-1fjdblk: 24px;--s-15lxxlk: var(--s-1ocxf4e);--s-176iwse: none;--ihun98: var(--s-1mnxhel);--lzkj6b: var(--s-1fz1zwb);--s-19gq58y: var(--s-1e9sg5q);--s-1fndoqe: var(--s-1xty0l1);--s-1ozmd2v: var(--s-1c9087t);--s-1itf6ev: var(--njr6lf);--lqlo87: var(--wvavyz);--s-15g638a: var(--s-1bdp00y);--s-101nale: var(--s-1rv6t4);--rpuu4f: var(--onmy4p);--s-1x2ggh5: var(--s-135hi2l);--s-1fz1zwb: var(--xcedj6);--s-1e9sg5q: var(--s-14xlm6o);--s-1xty0l1: var(--msg65c);--s-1c9087t: var(--s-1ywnfza);--njr6lf: var(--zjva6a);--wvavyz: var(--s-15n3uo5);--s-1bdp00y: var(--i6u0ap);--s-1rv6t4: 12px;--onmy4p: 20px;--s-4yu78: var(--s-1ocxf4e);--s-135hi2l: none;--qsps49: var(--ahgtyg);--s-1m5o6xs: var(--dilwm);--s-1sl6m46: var(--s-6omq4);--s-1tlryov: var(--nsaztv);--kidu0o: var(--s-1ixv1ks);--l2fksn: var(--s-1biv3ye);--s-16fd3c8: var(--s-1te2tup);--s-1n41s7u: var(--s-1nt3wam);--njb836: var(--s-108w7yg);--s-18nbbqu: var(--s-6mvx34);--b9ogvo: var(--s-1pbhbhw);--h3wc70: var(--z5eq11);--u4c2q6: var(--e1e86);--s-1oj6z6t: var(--uik06i);--s-1qtuyvq: var(--s-1eah8e8);--l28r8y: var(--h7f28h);--fcsdep: var(--s-1vvlcgn);--s-1ikrpfx: var(--s-36ddn3);--s-108w7yg: var(--qsps49);--s-6mvx34: var(--s-1m5o6xs);--s-1pbhbhw: var(--s-1sl6m46);--z5eq11: var(--s-1tlryov);--e1e86: var(--kidu0o);--uik06i: var(--l2fksn);--s-1eah8e8: var(--s-16fd3c8);--h7f28h: 18px;--s-1vvlcgn: 28px;--s-5hgyej: var(--s-1mnxhel);--s-36ddn3: none;--p1b3a1: var(--s-1nt3wam);--s-10jfra1: var(--wtyf0o);--s-1m1wff1: var(--s-167pe37);--s-1savn4h: var(--s-10fnwqi);--s-1gygsl6: var(--s-1sdpwmi);--li3rbu: var(--s-1prlirw);--s-9cy93t: var(--s-1oay49k);--s-11a5wqu: var(--b7x093);--s-17qz9cg: var(--s-1nk8z4c);--s-1pqj9m0: var(--s-1adv7ix);--s-1ctdufq: var(--s-2vga1d);--wtyf0o: var(--qsps49);--s-167pe37: var(--s-1m5o6xs);--s-10fnwqi: var(--s-1sl6m46);--s-1sdpwmi: var(--s-1tlryov);--s-1prlirw: var(--kidu0o);--s-1oay49k: var(--l2fksn);--b7x093: var(--s-16fd3c8);--s-1nk8z4c: 16px;--s-1adv7ix: 24px;--e9j7zt: var(--s-1mnxhel);--s-2vga1d: none;--s-1e6wgok: var(--s-1nt3wam);--s-5twc1q: var(--iv638n);--s-13v453w: var(--zzbkbv);--q47ujb: var(--cw4443);--s-4fq1f8: var(--sf9nah);--s-8kvr39: var(--s-1lduq5c);--t9sogg: var(--s-49369g);--s-6dkjzu: var(--s-195juhb);--s-1wizgxe: var(--eoafo5);--s-7ih227: var(--s-7paqqe);--be5p7j: var(--pz3gk9);--iv638n: var(--qsps49);--zzbkbv: var(--s-1m5o6xs);--cw4443: var(--s-1sl6m46);--sf9nah: var(--s-1tlryov);--s-1lduq5c: var(--kidu0o);--s-49369g: var(--l2fksn);--s-195juhb: var(--s-16fd3c8);--eoafo5: 14px;--s-7paqqe: 20px;--x5dpqz: var(--s-1mnxhel);--pz3gk9: none;--pyk6k1: var(--ahgtyg);--s-1verpm8: var(--dilwm);--rd4b92: var(--s-6omq4);--s-1i90hyx: var(--nsaztv);--y96hdk: var(--s-1ixv1ks);--qkji3r: var(--s-1biv3ye);--s-1kwoc9c: var(--s-1te2tup);--s-1qv548f: var(--s-1nt3wam);--s-1tq5jkt: var(--v43x2t);--s-3uli8c: var(--tcmtp2);--s-10wdlk9: var(--g77870);--s-1iqa1pt: var(--s-1xy9kgq);--vxd1ew: var(--wqx1if);--w2b5wa: var(--s-1fysgfv);--s-16ck0e3: var(--s-18527no);--okauee: var(--s-1rxtcbb);--s-1fhkvft: var(--s-1a3m0xe);--hj8sur: var(--ayuh76);--v43x2t: var(--pyk6k1);--tcmtp2: var(--s-1verpm8);--g77870: var(--rd4b92);--s-1xy9kgq: var(--s-1i90hyx);--wqx1if: var(--y96hdk);--s-1fysgfv: var(--qkji3r);--s-18527no: var(--s-1kwoc9c);--s-1rxtcbb: 16px;--s-1a3m0xe: 24px;--s-5y4pqp: var(--s-1mnxhel);--ayuh76: none;--ep1e0f: var(--s-1nt3wam);--s-6vkd26: var(--huplq6);--s-1h9quwx: var(--l1gcj7);--t2iyzt: var(--s-3mrwm8);--s-1xn3ax7: var(--l6yv66);--s-15oh72s: var(--s-1k1xktp);--s-1ohirt0: var(--s-3dxl6s);--juchqv: var(--s7es0h);--s-1g9cdsy: var(--tlxlq6);--yfph9h: var(--s-432ttp);--r31u81: var(--s-59wabm);--huplq6: var(--pyk6k1);--l1gcj7: var(--s-1verpm8);--s-3mrwm8: var(--rd4b92);--l6yv66: var(--s-1i90hyx);--s-1k1xktp: var(--y96hdk);--s-3dxl6s: var(--qkji3r);--s7es0h: var(--s-1kwoc9c);--tlxlq6: 14px;--s-432ttp: 20px;--s-1htz8iq: var(--s-1mnxhel);--s-59wabm: none;--ereqaf: var(--s-1nt3wam);--yiyhsh: var(--ft4em7);--sodrin: var(--ngt1c6);--bfuocu: var(--s-1vj0i13);--s-2nir93: var(--c3yjur);--s-1jh3kwa: var(--r99a4f);--hfec15: var(--s-19xhaty);--s-16ewvzx: var(--ctnn8n);--zzbsa1: var(--mae4h0);--ki0zdj: var(--s-1kc6i1b);--s-12qaksx: var(--s-1k0dbzs);--ft4em7: var(--pyk6k1);--ngt1c6: var(--s-1verpm8);--s-1vj0i13: var(--rd4b92);--c3yjur: var(--s-1i90hyx);--r99a4f: var(--y96hdk);--s-19xhaty: var(--qkji3r);--ctnn8n: var(--s-1kwoc9c);--mae4h0: 12px;--s-1kc6i1b: 16px;--s-10ubhie: var(--s-1mnxhel);--s-1k0dbzs: none;--l5cirb: var(--s-1camloi);--s-3ab8ub: var(--s-1fverle);--s-15f02i8: var(--s-2c6wsx);--s-1f29tr2: var(--s-19hyq79);--s-18tqzme: var(--s-1wum1rt);--s-1s3tcwv: var(--s-1p07rxq);--s-1sr9szs: var(--s-18ns0of);--s-72fzvy: 0px;--s-1n66wtu: 1px;--s-1camloi: 2px;--s-1fverle: 4px;--s-1eo1l6l: 6px;--s-2c6wsx: 8px;--s-14t02z3: 10px;--s-1cn5k4b: 12px;--s-10yt1e6: 14px;--s-19hyq79: 16px;--zmqxvl: 18px;--s-16s2r5d: 20px;--s-1wum1rt: 24px;--s-11p7nl: 28px;--s-1p07rxq: 32px;--s-18g2og9: 36px;--x3ux79: 40px;--s-18ns0of: 48px;--s-7dpk8n: 56px;--s-1ubl41v: 64px;--s-12tsswl: 72px;--s-1e1s3yj: 80px;--s-1c4fwdw: var(--s-282tnx);--jpxxql: var(--s-282tnx);--u4yslg: none;--s-1l4o7cj: 4px;--s-282tnx: 6px;--s-9fb64w: 8px;--s-721m59: 12px;--eazveb: 16px;--s-1pfp217: 9999em;--s-11c5ftm: solid;--s-5oekti: dashed;--s-12pesem: 1px;--s-1p3l5ml: 2px;--f0gr6w: 4px;--li639m: 100%;--s-18ciw8m: min-content;--s-15qxt3g: max-content;--s-22nfqw: fit-content;--cvc234: 50%;--bcipp6: 33.3333%;--s-1990hu4: 66.6667%;--hrim1e: 25%;--ys322a: 50%;--s-2hrodg: 75%;--ywypcv: 20%;--s-1j1r695: 40%;--s-3qcouv: 60%;--s-1c433cn: 80%;--s-1o6hvkt: 16.6667%;--v94vw1: 33.3333%;--ncjl8c: 50%;--s-14apa3: 66.6667%;--kcudzm: 83.3333%;--s-1sq848d: 8.3333%;--k9vhhg: 16.6667%;--s-1m2eq9s: 25%;--s-1hfpugt: 33.3333%;--s-12j0rnv: 41.6667%;--s-1ce5jho: 50%;--yca82r: 58.3333%;--s-1bb34n7: 66.6667%;--x6iu4: 75%;--s-1qjxzud: 83.3333%;--d52z5c: 91.6667%;--s-1qqjf1s: 0px 1px 1px 0px rgba(0, 0, 0, 0.12), 0px 2px 5px 0px rgba(48, 49, 61, 0.08);--s29i93: 0px 3px 6px 0px rgba(0, 0, 0, 0.12), 0px 7px 14px 0px rgba(48, 49, 61, 0.08);--s-144bgvr: 0px 5px 15px 0px rgba(0, 0, 0, 0.12), 0px 15px 35px 0px rgba(48, 49, 61, 0.08);--qbcnik: 0px 5px 15px 0px rgba(0, 0, 0, 0.12), 0px 15px 35px 0px rgba(48, 49, 61, 0.08), 0px 50px 100px 0px rgba(48, 49, 61, 0.08);--s-46hi4m: var(--s-144bgvr);--s-4fcpev: 0px 0px 15px 0px rgba(0, 0, 0, 0.12), 0px 0px 35px 0px rgba(48, 49, 61, 0.08);--s-8kdpya: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-1q5y78: 0px -1px 1px 0px rgba(20, 19, 78, 0.32);--s-1kgpzka: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-186fre1: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-1fb3eog: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-1ibn4id: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--s-1l32yqd: 0px -1px 1px 0px rgba(16, 17, 26, 0.16);--wq0k6h: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--fur145: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--s-1fecqxp: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--ytuq2g: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--k2t3ri: 0px -1px 1px 0px rgba(62, 2, 26, 0.32);--s-1fc7ea9: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--s-8p4pnm: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--s-1s9evt6: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--pga66p: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--s-7nyne0: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--s-1p8nnzk: 0px -1px 1px 0px rgba(1, 28, 58, 0.16);--s-4fmi5d: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--s-1mw80b4: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--s-1mp6cz9: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--o68lqt: 0px 1px 1px 0px rgba(62, 2, 26, .16);--s-1srjzen: 0px -1px 1px 0px rgba(62, 2, 26, .16);--s-5cda5b: 0px 1px 1px 0px rgba(62, 2, 26, .16);--uojav1: 0px 1px 1px 0px rgba(62, 2, 26, .16);--s-1xpb9p2: 0px 1px 1px 0px rgba(62, 2, 26, .16);--s-1atvbio: 0px -1px 1px 0px rgba(16, 17, 26, 0.16);--s-9l041r: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--fcko44: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--zh5azq: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--tnw4uh: 490px;--p6z4q9: 768px;--s-1tolf8z: 1040px;--s-13qggw6: 1440px;--s-1oz5pfq: 0;--s-52qljy: 490px;--m9yfsr: 768px;--s-1gz3jh8: 1040px;--s-1ad545m: 1440px;--s-1xy6qjm: 0 0 0 4px rgba(1, 150, 237, .36);
}
#​#​#​#​#​#​#​ .tooltip-trigger-isolate {
```

**playwright**
```
Querying authentication conversion | Stripe Documentation




#​ .sn-1q4qxi9 { --jybopzu-hue-gray0: #ffffff; --jybopzu-hue-gray50: #f6f8fa; --jybopzu-hue-gray100: #ebeef1; --jybopzu-hue-gray150: #d5dbe1; --jybopzu-hue-gray200: #c0c8d2; --jybopzu-hue-gray300: #a3acba; --jybopzu-hue-gray400: #87909f; --jybopzu-hue-gray500: #687385; --jybopzu-hue-gray600: #545969; --jybopzu-hue-gray700: #414552; --jybopzu-hue-gray800: #30313d; --jybopzu-hue-gray900: #1a1b25; --jybopzu-hue-gray950: #10111a; --jybopzu-hue-blue50: #ddfffe; --jybopzu-hue-blue100: #cff5f6; --jybopzu-hue-blue150: #a2e5ef; --jybopzu-hue-blue200: #75d5e8; --jybopzu-hue-blue300: #06b9ef; --jybopzu-hue-blue400: #0096eb; --jybopzu-hue-blue500: #0570de; --jybopzu-hue-blue600: #0055bc; --jybopzu-hue-blue700: #04438c; --jybopzu-hue-blue800: #003262; --jybopzu-hue-blue900: #011c3a; --jybopzu-hue-green50: #ecfed7; --jybopzu-hue-green100: #d7f7c2; --jybopzu-hue-green150: #a6eb84; --jybopzu-hue-green200: #76df47; --jybopzu-hue-green300: #48c404; --jybopzu-hue-green400: #3fa40d; --jybopzu-hue-green500: #228403; --jybopzu-hue-green600: #006908; --jybopzu-hue-green700: #0b5019; --jybopzu-hue-green800: #043b15; --jybopzu-hue-green900: #02220d; --jybopzu-hue-orange50: #fef9da; --jybopzu-hue-orange100: #fcedb9; --jybopzu-hue-orange150: #fcd579; --jybopzu-hue-orange200: #fcbd3a; --jybopzu-hue-orange300: #ff8f0e; --jybopzu-hue-orange400: #ed6704; --jybopzu-hue-orange500: #c84801; --jybopzu-hue-orange600: #a82c00; --jybopzu-hue-orange700: #842106; --jybopzu-hue-orange800: #5f1a05; --jybopzu-hue-orange900: #331302; --jybopzu-hue-red50: #fff5fa; --jybopzu-hue-red100: #ffe7f2; --jybopzu-hue-red150: #ffccdf; --jybopzu-hue-red200: #ffb1cd; --jybopzu-hue-red300: #fe87a1; --jybopzu-hue-red400: #fc526a; --jybopzu-hue-red500: #df1b41; --jybopzu-hue-red600: #b3093c; --jybopzu-hue-red700: #890d37; --jybopzu-hue-red800: #68052b; --jybopzu-hue-red900: #3e021a; --jybopzu-hue-purple50: #f9f7ff; --jybopzu-hue-purple100: #f2ebff; --jybopzu-hue-purple150: #dfd3fc; --jybopzu-hue-purple200: #d1befe; --jybopzu-hue-purple300: #b49cfc; --jybopzu-hue-purple400: #8d7ffa; --jybopzu-hue-purple500: #625afa; --jybopzu-hue-purple600: #513dd9; --jybopzu-hue-purple700: #3f32a1; --jybopzu-hue-purple800: #302476; --jybopzu-hue-purple900: #14134e; --jybopzu-color-neutral0: var(--jybopzu-hue-gray0); --jybopzu-color-neutral50: var(--jybopzu-hue-gray50); --jybopzu-color-neutral100: var(--jybopzu-hue-gray100); --jybopzu-color-neutral150: var(--jybopzu-hue-gray150); --jybopzu-color-neutral200: var(--jybopzu-hue-gray200); --jybopzu-color-neutral300: var(--jybopzu-hue-gray300); --jybopzu-color-neutral400: var(--jybopzu-hue-gray400); --jybopzu-color-neutral500: var(--jybopzu-hue-gray500); --jybopzu-color-neutral600: var(--jybopzu-hue-gray600); --jybopzu-color-neutral700: var(--jybopzu-hue-gray700); --jybopzu-color-neutral800: var(--jybopzu-hue-gray800); --jybopzu-color-neutral900: var(--jybopzu-hue-gray900); --jybopzu-color-neutral950: var(--jybopzu-hue-gray950); --jybopzu-color-brand50: var(--jybopzu-hue-purple50); --jybopzu-color-brand100: var(--jybopzu-hue-purple100); --jybopzu-color-brand200: var(--jybopzu-hue-purple200); --jybopzu-color-brand300: var(--jybopzu-hue-purple300); --jybopzu-color-brand400: var(--jybopzu-hue-purple400); --jybopzu-color-brand500: var(--jybopzu-hue-purple500); --jybopzu-color-brand600: var(--jybopzu-hue-purple600); --jybopzu-color-brand700: var(--jybopzu-hue-purple700); --jybopzu-color-brand800: var(--jybopzu-hue-purple800); --jybopzu-color-brand900: var(--jybopzu-hue-purple900); --jybopzu-color-info50: var(--jybopzu-hue-blue50); --jybopzu-color-info100: var(--jybopzu-hue-blue100); --jybopzu-color-info150: var(--jybopzu-hue-blue150); --jybopzu-color-info200: var(--jybopzu-hue-blue200); --jybopzu-color-info300: var(--jybopzu-hue-blue300); --jybopzu-color-info400: var(--jybopzu-hue-blue400); --jybopzu-color-info500: var(--jybopzu-hue-blue500); --jybopzu-color-info600: var(--jybopzu-hue-blue600); --jybopzu-color-info700: var(--jybopzu-hue-blue700); --jybopzu-color-info800: var(--jybopzu-hue-blue800); --jybopzu-color-info900: var(--jybopzu-hue-blue900); --jybopzu-color-success50: var(--jybopzu-hue-green50); --jybopzu-color-success100: var(--jybopzu-hue-green100); --jybopzu-color-success150: var(--jybopzu-hue-green150); --jybopzu-color-success200: var(--jybopzu-hue-green200); --jybopzu-color-success300: var(--jybopzu-hue-green300); --jybopzu-color-success400: var(--jybopzu-hue-green400); --jybopzu-color-success500: var(--jybopzu-hue-green500); --jybopzu-color-success600: var(--jybopzu-hue-green600); --jybopzu-color-success700: var(--jybopzu-hue-green700); --jybopzu-color-success800: var(--jybopzu-hue-green800); --jybopzu-color-success900: var(--jybopzu-hue-green900); --jybopzu-color-attention50: var(--jybopzu-hue-orange50); --jybopzu-color-attention100: var(--jybopzu-hue-orange100); --jybopzu-color-attention150: var(--jybopzu-hue-orange150); --jybopzu-color-attention200: var(--jybopzu-hue-orange200); --jybopzu-color-attention300: var(--jybopzu-hue-orange300); --jybopzu-color-attention400: var(--jybopzu-hue-orange400); --jybopzu-color-attention500: var(--jybopzu-hue-orange500); --jybopzu-color-attention600: var(--jybopzu-hue-orange600); --jybopzu-color-attention700: var(--jybopzu-hue-orange700); --jybopzu-color-attention800: var(--jybopzu-hue-orange800); --jybopzu-color-attention900: var(--jybopzu-hue-orange900); --jybopzu-color-critical50: var(--jybopzu-hue-red50); --jybopzu-color-critical100: var(--jybopzu-hue-red100); --jybopzu-color-critical150: var(--jybopzu-hue-red150); --jybopzu-color-critical200: var(--jybopzu-hue-red200); --jybopzu-color-critical300: var(--jybopzu-hue-red300); --jybopzu-color-critical400: var(--jybopzu-hue-red400); --jybopzu-color-critical500: var(--jybopzu-hue-red500); --jybopzu-color-critical600: var(--jybopzu-hue-red600); --jybopzu-color-critical700: var(--jybopzu-hue-red700); --jybopzu-color-critical800: var(--jybopzu-hue-red800); --jybopzu-color-critical900: var(--jybopzu-hue-red900); --jybopzu-backgroundColor-surface: var(--jybopzu-color-neutral0); --jybopzu-backgroundColor-container: var(--jybopzu-color-neutral50); --jybopzu-borderColor-neutral: var(--jybopzu-color-neutral150); --jybopzu-borderColor-critical: var(--jybopzu-color-critical500); --jybopzu-iconColor-primary: var(--jybopzu-color-neutral600); --jybopzu-iconColor-secondary: var(--jybopzu-color-neutral400); --jybopzu-iconColor-disabled: var(--jybopzu-color-neutral200); --jybopzu-iconColor-brand: var(--jybopzu-color-brand400); --jybopzu-iconColor-info: var(--jybopzu-color-info400); --jybopzu-iconColor-success: var(--jybopzu-color-success400); --jybopzu-iconColor-attention: var(--jybopzu-color-attention400); --jybopzu-iconColor-critical: var(--jybopzu-color-critical400); --jybopzu-textColor-primary: var(--jybopzu-color-neutral700); --jybopzu-textColor-secondary: var(--jybopzu-color-neutral500); --jybopzu-textColor-disabled: var(--jybopzu-color-neutral300); --jybopzu-textColor-brand: var(--jybopzu-color-brand500); --jybopzu-textColor-info: var(--jybopzu-color-info500); --jybopzu-textColor-success: var(--jybopzu-color-success500); --jybopzu-textColor-attention: var(--jybopzu-color-attention500); --jybopzu-textColor-critical: var(--jybopzu-color-critical500); --jybopzu-overflow-hidden: hidden; --jybopzu-radius-none: none; --jybopzu-radius-xsmall: 4px; --jybopzu-radius-small: 4px; --jybopzu-radius-medium: 8px; --jybopzu-radius-large: 10px; --jybopzu-radius-rounded: 999em; --jybopzu-shadow-none: none; --jybopzu-shadow-top: rgb(0 0 0 / 12%) 0px 1px 1px 0px; --jybopzu-shadow-base: rgb(64 68 82 / 8%) 0px 2px 5px 0px, 0 0 0 0 transparent; --jybopzu-shadow-hover: rgb(64 68 82 / 8%) 0px 2px 5px 0px, rgb(64 68 82 / 8%) 0px 3px 9px 0px; --jybopzu-shadow-focus: 0 0 0 4px rgb(1 150 237 / 36%); --jybopzu-size-0: 0px; --jybopzu-size-1: var(--jybopzu-space-1); --jybopzu-size-25: var(--jybopzu-space-25); --jybopzu-size-50: var(--jybopzu-space-50); --jybopzu-size-75: var(--jybopzu-space-75); --jybopzu-size-100: var(--jybopzu-space-100); --jybopzu-size-150: var(--jybopzu-space-150); --jybopzu-size-200: var(--jybopzu-space-200); --jybopzu-size-250: var(--jybopzu-space-250); --jybopzu-size-300: var(--jybopzu-space-300); --jybopzu-size-350: var(--jybopzu-space-350); --jybopzu-size-400: var(--jybopzu-space-400); --jybopzu-size-500: var(--jybopzu-space-500); --jybopzu-size-600: var(--jybopzu-space-600); --jybopzu-size-fill: 100%; --jybopzu-size-min: min-content; --jybopzu-size-max: max-content; --jybopzu-size-fit: fit-content; --jybopzu-size-1\/2: 50%; --jybopzu-size-1\/3: 33.3333%; --jybopzu-size-2\/3: 66.6667%; --jybopzu-size-1\/4: 25%; --jybopzu-size-2\/4: 50%; --jybopzu-size-3\/4: 75%; --jybopzu-size-1\/5: 20%; --jybopzu-size-2\/5: 40%; --jybopzu-size-3\/5: 60%; --jybopzu-size-4\/5: 80%; --jybopzu-size-1\/6: 16.6667%; --jybopzu-size-2\/6: 33.3333%; --jybopzu-size-3\/6: 50%; --jybopzu-size-4\/6: 66.6667%; --jybopzu-size-5\/6: 83.3333%; --jybopzu-size-1\/12: 8.3333%; --jybopzu-size-2\/12: 16.6667%; --jybopzu-size-3\/12: 25%; --jybopzu-size-4\/12: 33.3333%; --jybopzu-size-5\/12: 41.6667%; --jybopzu-size-6\/12: 50%; --jybopzu-size-7\/12: 58.3333%; --jybopzu-size-8\/12: 66.6667%; --jybopzu-size-9\/12: 75%; --jybopzu-size-10\/12: 83.3333%; --jybopzu-size-11\/12: 91.6667%; --jybopzu-space-0: 0px; --jybopzu-space-1: 1px; --jybopzu-space-25: 2px; --jybopzu-space-50: 4px; --jybopzu-space-75: 6px; --jybopzu-space-100: 8px; --jybopzu-space-150: 12px; --jybopzu-space-200: 16px; --jybopzu-space-250: 20px; --jybopzu-space-300: 24px; --jybopzu-space-350: 28px; --jybopzu-space-400: 32px; --jybopzu-space-500: 40px; --jybopzu-space-600: 48px; --jybopzu-space-xxsmall: var(--jybopzu-space-25); --jybopzu-space-xsmall: var(--jybopzu-space-50); --jybopzu-space-small: var(--jybopzu-space-100); --jybopzu-space-medium: var(--jybopzu-space-200); --jybopzu-space-large: var(--jybopzu-space-300); --jybopzu-space-xlarge: var(--jybopzu-space-400); --jybopzu-space-xxlarge: var(--jybopzu-space-600); --jybopzu-typeface-ui: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; --jybopzu-typeface-monospace: 'Source Code Pro', Menlo, Monaco, monospace; --jybopzu-weight-regular: 400; --jybopzu-weight-semibold: 600; --jybopzu-weight-bold: 700; --jybopzu-zIndex-overlay: 299; --jybopzu-zIndex-partial: 400; }#​#​ .rs-3::before {
content: var(--s--baseline-alignment-content);user-select: none;align-self: baseline;margin-right: calc(-1 \* var(--s--column-gap));
}
#​#​ .rs-8[aria-invalid="true"] {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .sail-table-row:not(:hover) .row-actions-trigger {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-4 {
display: var(--s--display-block);
}
#​#​ .rs-2 {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-6:active:not([aria-disabled="true"]) {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .sail-table-row:hover .row-actions-trigger {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-5:hover:not(:active):not([aria-disabled="true"]) {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .rs-7:focus {
box-shadow: var(--s--top-shadow), var(--s--keyline) 0 0 0 var(--s--keyline-width), var(--s--focus-ring), var(--s--box-shadow);
}
#​#​ .sn-d7kp2a { --distribute-x: initial; --distribute-y: initial; --align-x: initial; --align-y: initial; }
#​#​ .sn-d7kp2a > \* { --align-self-x: initial; --align-self-y: initial; --flex-x: 1 1 auto; --flex-y: 1 1 auto; }
#​#​ .sn-1fnc4mz { --row-gap: normal; --column-gap: normal; gap: var(--row-gap) var(--column-gap); }
#​#​ .sn-1c37ise { --padding-top: 0; --padding-right: 0; --padding-bottom: 0; --padding-left: 0; padding: var(--padding-top) var(--padding-right) var(--padding-bottom) var(--padding-left); }
.\_\_sn-sheet-order { --order: '\_1rkm1cp,\_88mn99,\_5olop,\_16pds2j,\_1wna6e6,\_kskd3k,\_5vzub4,\_lzay40,\_1d9aqya'; }#​#​#​#​#​ .sn-182o7r0 { font-family: var(--jybopzu-typeface-ui); color: var(--jybopzu-textColor-primary); fill: var(--jybopzu-iconColor-primary); -webkit-font-smoothing: antialiased; }#​#​#​#​#​#​#​:root, :host #​#​#​#​#​#​#​, #​#​#​#​#​#​#​ .sn-token-provider {
--s-806179: var(--s-1ipujfj);--qyckuc: 200ms;--s-1xyzpq3: 0ms;--ch7862: 50ms;--s-5jzhfa: 100ms;--s-12b75vv: 150ms;--rsnfo1: 300ms;--s-12ljnrj: 400ms;--s-10dnt5v: cubic-bezier(0, .09, .4, 1);--s-12oyqav: ease-in-out;--im41o8: ease-out;--s-1fdsmh8: ease-in;--s-1pzb1xw: 120;--s-6429u6: 14;--dutg7l: 300;--rjlba6: 20;--s-117eyx7: 400;--slm412: 10;--s-1pt58bw: 30ms;--pu6lsa: 50ms;--s-1ca225m: 80ms;--h9q5hc: 0.95;--s-1308p7c: 0.99;--s-1paplcg: 0.98;--s-19omtc6: 1.02;--eef79q: #ffffff;--s-8qwlk1: #F4F7FA;--o3gs5n: #ECF1F6;--hyhghw: #D4DEE9;--s-1b58r1w: #BAC8DA;--ovqch4: #95A4BA;--ggantb: #7D8BA4;--s-1a8u6zz: #667691;--k08wfi: #50617A;--s-169hr3v: #3C4F69;--ymu9b7: #273951;--ny99wq: #1A2C44;--s-1nmzh8w: #ffffff;--s-421sqo: #e2fbfe;--s-4qj11w: #cbf5fd;--s-1u1nr1c: #a7e7fc;--dj5edy: #6dc9fc;--s-3blua0: #3babfd;--s-172n6d2: #088ef9;--s-1l3w4rb: #0072e9;--s-1yzoj9a: #045ad0;--kvmyi1: #0b46ad;--s-1ah8y8v: #0d3485;--s-1v7mjmv: #0a2156;--s-1cbef47: #ffffff;--ncitdb: #eafcdd;--khndpt: #d1fab3;--fcix74: #a8f170;--s-1jt7b3q: #7cd548;--rz6g85: #58ba27;--s-10in11e: #3da00b;--jet5ih: #2b8700;--s-11ws3zn: #217005;--mkuc60: #1c5a0d;--s-5vneq4: #184310;--s-1ybzlmc: #112a0d;--s-1idvp5s: #ffffff;--s-1ronw4t: #fdf8c9;--een7nd: #fceeb5;--s-1j3zdk7: #fbd992;--bpq42r: #fcaf4f;--d5srfd: #f7870f;--s-7gt7xl: #e46602;--s-1bt4nax: #cc4b00;--s-1m90cr3: #b13600;--s-105rx08: #922700;--s-3csqoi: #701b01;--s-1x99otv: #4a0f02;--s-18rmc6q: #ffffff;--m4edry: #fef4f6;--pfpugw: #fde9ee;--s-1at7tzv: #fbd3dc;--s-8ik67: #faa9b8;--s-1brqpgc: #fa7e91;--s-1k4y65: #fa4a67;--s-1t7w85x: #e61947;--j769ku: #c0123c;--s-105k9ow: #9b0c36;--s-1bradsh: #76072f;--s-17cbcf1: #4e0322;--s-1m3ejd7: #ffffff;--wclsxb: #f7f5fd;--s-1nuetr3: #efecfc;--s-1rgwov0: #e0d9fb;--d427sf: #c3b6fb;--s-1gm5hwl: #a497fc;--d7ng6f: #857afe;--s-1wqs2n2: #675dff;--s-1rqwfiu: #533afd;--cb9l9o: #4e11e2;--b00e2n: #44139f;--yvasq2: #2f0e63;--s-35hf94: hsla(0, 0%, 100%, 0.2);--s-13ypoy8: var(--eef79q);--s-114rdv4: var(--s-8qwlk1);--s-1bcqfda: var(--o3gs5n);--s-1kkti1r: var(--hyhghw);--s-16pqfer: var(--s-1b58r1w);--s-1kmer3i: var(--ovqch4);--s-13py8ob: var(--ggantb);--s-1wdog5l: var(--s-1a8u6zz);--jkp57b: var(--k08wfi);--s-1xkgkxo: var(--s-169hr3v);--s-1egalvn: var(--ymu9b7);--v2y5bm: var(--ny99wq);--s-1ona342: var(--s-1m3ejd7);--s-1xikbvo: var(--wclsxb);--ek860z: var(--s-1nuetr3);--s-3qadn4: var(--s-1rgwov0);--nl7ypg: var(--d427sf);--hm37ax: var(--s-1gm5hwl);--s-142x5wh: var(--d7ng6f);--s-1nbkq3e: var(--s-1wqs2n2);--s-1b0l18k: var(--s-1rqwfiu);--s-1y0ta6r: var(--cb9l9o);--pxx34h: var(--b00e2n);--xp2k2: var(--yvasq2);--s-13od8gw: var(--s-1idvp5s);--fox699: var(--s-1ronw4t);--p5cdic: var(--een7nd);--s-1jh7fp5: var(--s-1j3zdk7);--lsye2d: var(--bpq42r);--t3987n: var(--d5srfd);--s-1vcezov: var(--s-7gt7xl);--s-1qk1a9q: var(--s-1bt4nax);--s-1ipujfj: var(--s-1m90cr3);--s-1vhr1m: var(--s-105rx08);--s-1oqa1l5: var(--s-3csqoi);--kubwak: var(--s-1x99otv);--whf9po: var(--s-18rmc6q);--gqp7g1: var(--m4edry);--s-1j0j6fb: var(--pfpugw);--o1xbta: var(--s-1at7tzv);--vyde9h: var(--s-8ik67);--s-875rxv: var(--s-1brqpgc);--s-1xn82ef: var(--s-1k4y65);--xi7x09: var(--s-1t7w85x);--uk4ts2: var(--j769ku);--s-9ukgu0: var(--s-105k9ow);--s-15yycft: var(--s-1bradsh);--s-1v6ybst: var(--s-17cbcf1);--s-1f39zfp: var(--s-1nmzh8w);--s-1bf76tl: var(--s-421sqo);--s-1sypgcr: var(--s-4qj11w);--u7pgeo: var(--s-1u1nr1c);--qev2nh: var(--dj5edy);--rqlrpr: var(--s-3blua0);--s-8vaodq: var(--s-172n6d2);--s-1m519r1: var(--s-1l3w4rb);--r3g89x: var(--s-1yzoj9a);--n0umvo: var(--kvmyi1);--c0109p: var(--s-1ah8y8v);--s-26e45o: var(--s-1v7mjmv);--s-1a4o86t: var(--s-1cbef47);--nxbwn6: var(--ncitdb);--s-18tv9xz: var(--khndpt);--s-660zz9: var(--fcix74);--s-5y9ijm: var(--s-1jt7b3q);--s-1gwptpc: var(--rz6g85);--t5jail: var(--s-10in11e);--qcdf10: var(--jet5ih);--s-1o92vf6: var(--s-11ws3zn);--s-1spzwnv: var(--mkuc60);--s-35q6a2: var(--s-5vneq4);--axxngb: var(--s-1ybzlmc);--s-1hj7tfd: var(--s-18rmc6q);--s-1xf1h3f: var(--m4edry);--aqxmtx: var(--pfpugw);--s-1um7fco: var(--s-1at7tzv);--d2i300: var(--s-8ik67);--cae9kd: var(--s-1brqpgc);--s-1a4c91b: var(--s-1k4y65);--s-1jvllvw: var(--s-1t7w85x);--x379qy: var(--j769ku);--s-1owp6iv: var(--s-105k9ow);--m26qys: var(--s-1bradsh);--s-3rumb4: var(--s-17cbcf1);--s-5tm7hx: var(--s-1cbef47);--h22sh6: var(--ncitdb);--s-11rdejd: var(--khndpt);--s-1g2t37u: var(--fcix74);--wesn6: var(--s-1jt7b3q);--s-1hhq31p: var(--rz6g85);--yji28s: var(--s-10in11e);--s-169ogke: var(--jet5ih);--hr7syg: var(--s-11ws3zn);--s-14wylcr: var(--mkuc60);--s-289q66: var(--s-5vneq4);--v27jy: var(--s-1ybzlmc);--s-1hldvhn: #9966FF;--s-1xwen3a: #0055BC;--hxpspa: #00A1C2;--s-5ghlc9: #ED6804;--nap71a: #B3063D;--s-1sz15nh: var(--mkuc60);--mygevb: var(--s-1k4y65);--nrw914: var(--s-105rx08);--bu79cc: var(--s-10in11e);--s-1rfvf0n: var(--s-114rdv4);--s-9fypy8: var(--s-13ypoy8);--s-8muhy8: var(--s-35hf94);--s-153sf3j: rgba(186, 200, 218, 0.7);--s-1mkjmgu: var(--s-1b0l18k);--s-9u3gcm: var(--s-1b0l18k);--s-1pk4mhu: var(--s-1y0ta6r);--s-1wze59r: var(--s-1b0l18k);--s-1gzyq0k: var(--s-1b0l18k);--s-1eg71kz: var(--s-9fypy8);--uftl0g: var(--s-9fypy8);--s-1wj6iyq: var(--s-114rdv4);--s-1jrjwpv: var(--s-9fypy8);--b5b0q1: var(--s-9fypy8);--jix8n1: var(--xi7x09);--s-1isx4n7: var(--xi7x09);--s-1owgngi: var(--uk4ts2);--s-1tqa4ka: var(--xi7x09);--s-1dl2eq8: var(--xi7x09);--s-14a2tiz: var(--s-13ypoy8);--s-1b3o71a: var(--s-1nbkq3e);--qkwke3: var(--s-1nbkq3e);--s-1afrigr: var(--s-1b0l18k);--s-1orf6yv: var(--s-1nbkq3e);--s-18eec8a: var(--s-1kkti1r);--rfaik3: var(--s-13ypoy8);--s-1xn7irg: var(--s-1bcqfda);--s-1x4qw9u: var(--s-13ypoy8);--s-4m5wr6: var(--s-1bcqfda);--s-1mbtsu2: var(--s-13ypoy8);--s-1im6yhz: var(--s-13ypoy8);--syi4h: var(--s-13ypoy8);--a37hit: var(--s-13ypoy8);--s-2av06t: var(--s-114rdv4);--s-1pjx0uz: var(--s-1bcqfda);--s-175jw0u: var(--s-114rdv4);--pz1vgx: var(--s-1wdog5l);--s-6j56kn: var(--s-1egalvn);--jg0c26: var(--s-1sypgcr);--s-1g3vynh: var(--s-1bf76tl);--lg8mcu: var(--s-1m519r1);--s-12izfvv: var(--s-18tv9xz);--s-1t53zya: var(--nxbwn6);--zuu90a: var(--qcdf10);--s-414lsb: var(--p5cdic);--ulpd63: var(--fox699);--s-15wlbw2: var(--s-1qk1a9q);--s-1dn6rk: var(--s-1j0j6fb);--s-1k641wx: var(--gqp7g1);--aw0phz: var(--xi7x09);--s-15xulsv: var(--s-1kkti1r);--w22o9l: var(--s-1b0l18k);--s-8c655s: var(--pxx34h);--s-1ok36r9: var(--pxx34h);--s-158s5xz: var(--s-1b0l18k);--xw6qjn: var(--s-1b0l18k);--s-4lkz9i: var(--s-15xulsv);--s-1amkzr1: var(--s-1kmer3i);--s-17kovyh: var(--s-15xulsv);--s-125pidq: var(--s-15xulsv);--s-8to5ry: var(--s-15xulsv);--s-17n5yam: var(--xi7x09);--eyrjow: var(--s-9ukgu0);--s-1u2do9: var(--s-9ukgu0);--qzxx9l: var(--xi7x09);--s-1draesn: var(--xi7x09);--s-17tmi4r: var(--s-1kkti1r);--b7ifjk: var(--xi7x09);--s-6o7nrw: var(--uk4ts2);--s-73zwar: var(--xi7x09);--d3be3c: var(--xi7x09);--npx6zl: var(--xi7x09);--wt6h1z: var(--s-1nbkq3e);--s-19hm5u2: var(--s-1b0l18k);--s-1ki2h5s: var(--s-1b0l18k);--s-1upode3: var(--s-1nbkq3e);--e619vt: var(--s-1kkti1r);--h29g9m: var(--s-1kmer3i);--o26ijo: var(--s-1kkti1r);--s-1fqa73g: var(--s-1kkti1r);--s-1t2fj50: var(--s-1kkti1r);--s-1p5fyku: var(--s-1kkti1r);--s-7st1q: var(--s-1kkti1r);--s-177yrws: var(--s-1wdog5l);--s-1x5q6fw: var(--s-1egalvn);--s-1cn97xm: var(--u7pgeo);--s-9nkfwt: var(--u7pgeo);--s-7pqyn6: var(--s-1m519r1);--s-9bkbz: var(--s-660zz9);--s-1qd49a9: var(--s-660zz9);--s-17mlsdr: var(--qcdf10);--s-1ow1a4n: var(--s-1jh7fp5);--s-1mnr65s: var(--s-1jh7fp5);--s-1yfj4t4: var(--s-1qk1a9q);--fg7f6q: var(--o1xbta);--d8waz0: var(--o1xbta);--s-8cc9re: var(--xi7x09);--s-13hmetb: var(--v2y5bm);--oiv4a4: var(--s-1b0l18k);--s-6obdb0: var(--s-1y0ta6r);--s-17yrw5r: var(--pxx34h);--s-1o9jit1: var(--s-1b0l18k);--s-17snam4: var(--s-13py8ob);--s-1xyyyk2: var(--s-1egalvn);--s-1ui80l2: var(--v2y5bm);--jus5c7: var(--v2y5bm);--s-184ljp4: var(--s-1egalvn);--eb4u9z: var(--jkp57b);--o8bs57: var(--uk4ts2);--s-10w80od: var(--s-9ukgu0);--s-1c9sq9t: var(--s-15yycft);--ruipx: var(--uk4ts2);--s-1wer54: var(--s-13py8ob);--uvjldp: var(--s-13ypoy8);--rygqjm: var(--s-13ypoy8);--s-3zsim4: var(--s-3qadn4);--nqzz7a: var(--s-13ypoy8);--fmcfok: var(--s-13ypoy8);--s-13dhk1f: var(--s-1egalvn);--s-97x5jr: var(--s-1egalvn);--s-148oer1: var(--s-1xkgkxo);--qzwqpe: var(--s-1egalvn);--s-9i3k0u: var(--s-1egalvn);--s-87wktm: var(--s-13ypoy8);--s-13hlbvk: var(--s-13ypoy8);--s-114300b: var(--o1xbta);--l5jmjk: var(--s-13ypoy8);--oalgln: var(--s-13ypoy8);--wukrzp: var(--s-1egalvn);--fa9lug: var(--s-1wdog5l);--s-1oi81m8: var(--s-1egalvn);--x0orno: var(--s-1egalvn);--s-1pxcz58: var(--s-1egalvn);--p0bjsc: var(--s-13py8ob);--u320f7: var(--r3g89x);--s-1iv5nq8: var(--r3g89x);--uj52u9: var(--n0umvo);--s-6v1wws: var(--s-1o92vf6);--s-1tqfmwd: var(--s-1o92vf6);--g8y80y: var(--s-1spzwnv);--uflrw: var(--s-1ipujfj);--jg0bei: var(--s-1ipujfj);--s-1kdpopy: var(--s-1vhr1m);--ibollp: var(--uk4ts2);--evfcf2: var(--uk4ts2);--qj0juw: var(--s-9ukgu0);--s-1u9outy: var(--jkp57b);--s-18brxby: var(--jkp57b);--s-5wyt2d: var(--s-13ypoy8);--s-15m6t6b: var(--s-13ypoy8);--nph474: var(--r3g89x);--s-9j04rl: var(--r3g89x);--s-18eqkid: var(--s-13ypoy8);--k9sgh3: var(--s-1o92vf6);--s-679qlr: var(--s-1o92vf6);--s-1gxwr4: var(--s-13ypoy8);--i7djdz: var(--s-1ipujfj);--s-1yqvg4v: var(--s-13ypoy8);--s-1uywv9f: var(--uk4ts2);--xfgvhn: var(--uk4ts2);--s-1l3ikln: var(--s-13ypoy8);--s-1hknj82: var(--v2y5bm);--xd9t29: var(--v2y5bm);--s-1qz4hey: var(--s-1xkgkxo);--s-13mj3ey: var(--s-1nbkq3e);--yfq5jb: var(--s-1b0l18k);--s-1d5tn5g: var(--s-1y0ta6r);--s-1ts3wnp: var(--s-1nbkq3e);--mtnc2e: var(--s-1kmer3i);--s-1ggs8se: var(--s-1xkgkxo);--s-1983a3r: var(--s-1egalvn);--s-1rbj8zq: var(--v2y5bm);--s-12x7xov: var(--s-1xkgkxo);--q5xz4t: var(--s-1wdog5l);--s-2ojt3v: var(--xi7x09);--s-1c4musi: var(--uk4ts2);--rwzmwu: var(--s-9ukgu0);--s-1k156kb: var(--xi7x09);--s-1njcrbd: var(--s-1kmer3i);--s-1auir75: var(--s-13ypoy8);--tipuka: var(--s-13ypoy8);--s-1myp5o1: var(--s-3qadn4);--s-5didwj: var(--s-13ypoy8);--s-1wf2wvi: var(--s-13ypoy8);--s-15w0yfc: var(--s-1qz4hey);--fc8g0t: var(--s-1qz4hey);--s-17uj1m3: var(--jkp57b);--g8dxu4: var(--s-1qz4hey);--s-2e4gj5: var(--s-1qz4hey);--s-1xsl5v6: var(--s-13ypoy8);--s-1vjzvov: var(--s-13ypoy8);--s-1n46b59: var(--o1xbta);--u90thq: var(--s-13ypoy8);--s-19o7zaa: var(--s-13ypoy8);--s-10q3p1o: var(--s-1xkgkxo);--s-8jpmhq: var(--s-1xkgkxo);--s-1nuytc0: var(--s-1xkgkxo);--s-1vua7kb: var(--s-1xkgkxo);--brnaxe: var(--s-1kmer3i);--s-1ufxgw0: var(--s-13ypoy8);--qth5g3: var(--s-13ypoy8);--s-1hd7tld: var(--s-13ypoy8);--s-40ljxg: var(--s-13ypoy8);--s-1aln5xz: var(--s-114rdv4);--s-49rsbu: var(--s-1m519r1);--xsdaas: var(--s-1m519r1);--mglbt2: var(--r3g89x);--rtvqux: var(--qcdf10);--ko7qd: var(--qcdf10);--s-50f0qm: var(--s-1o92vf6);--eu61bi: var(--s-1qk1a9q);--y7jsf0: var(--s-1qk1a9q);--s-1ac7lwk: var(--s-1ipujfj);--s-9k5091: var(--xi7x09);--ruhzmh: var(--xi7x09);--s-2xp72p: var(--uk4ts2);--s-17iqe5q: var(--s-1wdog5l);--s-1253b2y: var(--s-1wdog5l);--s-1piwg9i: var(--s-13ypoy8);--s-7oniqh: var(--s-13ypoy8);--s-6ucdv7: var(--s-1m519r1);--s-1jcoye7: var(--s-1m519r1);--hnqjk9: var(--s-13ypoy8);--pgimab: var(--qcdf10);--xntlbj: var(--qcdf10);--s-14mlsvd: var(--s-13ypoy8);--s-1exie7f: var(--s-1qk1a9q);--yqmt02: var(--s-1qk1a9q);--s-17qjsgp: var(--s-13ypoy8);--e6rr02: var(--xi7x09);--qwe25a: var(--xi7x09);--s-1cx6227: var(--s-13ypoy8);--s-1o2c3h9: var(--s-1wdog5l);--s-6gs83q: var(--s-1egalvn);--ahgtyg: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';--dilwm: 2048;--s-6omq4: 1980;--nsaztv: 1443;--s-1ixv1ks: 1078;--s-1biv3ye: -432;--s-1te2tup: 0;--cdmbir: 300;--s-1mnxhel: 400;--s-1nt3wam: 600;--s-1ocxf4e: 700;--s-1vpgvqc: 'Source Code Pro', Menlo, Monaco, monospace;--s-1y398ge: 2048;--j5b9ko: 1556;--s-17c3qcu: 1493;--s-6zqpne: 1120;--s-1jib5q0: -492;--s-75pjiv: 410;--s-780oqg: var(--ahgtyg);--s-1c2w534: var(--dilwm);--s-4imvpn: var(--s-6omq4);--s-1ph4673: var(--nsaztv);--s-14qchrt: var(--s-1ixv1ks);--s-174cqiz: var(--s-1biv3ye);--s-1rnjjay: var(--s-1te2tup);--bwm4no: var(--s-1mnxhel);--s-1bfvuc2: var(--s-1i82044);--s-1vo01ya: var(--s-1db3chc);--s-1nrhtfr: var(--tk0isw);--s-1xlut57: var(--s-1lhqll2);--s-10rtirn: var(--s-11v0pqn);--s-1gj0nto: var(--s-6cbmuf);--z8c3ww: var(--yplwvi);--s-1itdcoa: var(--s-1m30mdf);--s-1e47fbj: var(--cd4zwn);--s-1i82044: var(--s-780oqg);--s-1db3chc: var(--s-1c2w534);--tk0isw: var(--s-4imvpn);--s-1lhqll2: var(--s-1ph4673);--s-11v0pqn: var(--s-14qchrt);--s-6cbmuf: var(--s-174cqiz);--yplwvi: var(--s-1rnjjay);--s-1m30mdf: 56px;--cd4zwn: 64px;--s-1fgn2x1: var(--s-1ocxf4e);--g8k6lo: var(--s-1mnxhel);--simh7g: var(--wsbs66);--s-11tag5s: var(--s-1cfwdq);--egn7v3: var(--s-18ll6fg);--s-1rfbcod: var(--s-13spi5k);--s-1luqrck: var(--s-15fn66i);--s-27iqeg: var(--d5drjy);--s-18wcjw: var(--s-1rsg6td);--s-1u9zl82: var(--n6jam8);--miv9l: var(--lq97ov);--wsbs66: var(--s-780oqg);--s-1cfwdq: var(--s-1c2w534);--s-18ll6fg: var(--s-4imvpn);--s-13spi5k: var(--s-1ph4673);--s-15fn66i: var(--s-14qchrt);--d5drjy: var(--s-174cqiz);--s-1rsg6td: var(--s-1rnjjay);--n6jam8: 48px;--lq97ov: 56px;--s-1ucmgz7: var(--s-1ocxf4e);--s-17ghi8h: var(--s-1mnxhel);--hbk0oo: var(--s-1wwy80b);--s-2dbb2a: var(--s-160c6gg);--yxaojm: var(--s-1npqh71);--nm1xrx: var(--s-68sjx3);--s-1ivbjtl: var(--wejrbv);--s-8vhotc: var(--si2vzf);--pakukh: var(--s-7035h);--icmlh7: var(--ad7wce);--s-8mv65e: var(--s-12zbgfl);--s-1wwy80b: var(--s-780oqg);--s-160c6gg: var(--s-1c2w534);--s-1npqh71: var(--s-4imvpn);--s-68sjx3: var(--s-1ph4673);--wejrbv: var(--s-14qchrt);--si2vzf: var(--s-174cqiz);--s-7035h: var(--s-1rnjjay);--ad7wce: 40px;--s-12zbgfl: 48px;--s-1xgajx6: var(--s-1ocxf4e);--s-1mb7r8p: var(--s-1mnxhel);--s-1jtr8l0: var(--dx0zsf);--bzblmh: var(--s-1s7fwor);--s-13z63vp: var(--s-1z08gqp);--s-1noeuap: var(--fdri1y);--s-1iotv3v: var(--s-1ktva78);--s-18s8xzd: var(--jrvk1a);--s-1xijmep: var(--s-62671d);--s-1nph8pw: var(--s-1eryk2b);--s-5jpu2o: var(--s-1rvvcgm);--dx0zsf: var(--s-780oqg);--s-1s7fwor: var(--s-1c2w534);--s-1z08gqp: var(--s-4imvpn);--fdri1y: var(--s-1ph4673);--s-1ktva78: var(--s-14qchrt);--jrvk1a: var(--s-174cqiz);--s-62671d: var(--s-1rnjjay);--s-1eryk2b: 32px;--s-1rvvcgm: 40px;--nusmm3: var(--s-1ocxf4e);--xcedj6: var(--ahgtyg);--s-14xlm6o: var(--dilwm);--msg65c: var(--s-6omq4);--s-1ywnfza: var(--nsaztv);--zjva6a: var(--s-1ixv1ks);--s-15n3uo5: var(--s-1biv3ye);--i6u0ap: var(--s-1te2tup);--xb6tkh: var(--s-1mnxhel);--s-1xmxn4q: var(--s-71ssjp);--s-1xgixpx: var(--db0w5x);--s-1k35674: var(--jed2z7);--s-12k91a7: var(--tv79ff);--s-1s0wyj4: var(--s-1x8so7v);--ig6ly8: var(--s-1j7acn3);--s-8l4ca5: var(--s-38ks7n);--s-1svi9x0: var(--x65r8g);--d7hr4e: var(--s-14j81vx);--s-1ylzxkj: var(--oq2dkr);--s-71ssjp: var(--xcedj6);--db0w5x: var(--s-14xlm6o);--jed2z7: var(--msg65c);--tv79ff: var(--s-1ywnfza);--s-1x8so7v: var(--zjva6a);--s-1j7acn3: var(--s-15n3uo5);--s-38ks7n: var(--i6u0ap);--x65r8g: 28px;--s-14j81vx: 36px;--s-1n4fl4h: var(--s-1ocxf4e);--oq2dkr: none;--f4w18u: var(--s-1mnxhel);--s-1rpa4qr: var(--jdmia2);--v1v838: var(--ts1hpc);--vn27bl: var(--s-187zl0b);--s-1vnqflb: var(--s-12s5kmm);--s-1n4dokk: var(--s-4fox1q);--wb62lm: var(--j3z1dw);--s-1f8ywlh: var(--s-1jvq51g);--s-1uud5hl: var(--s-1joebgy);--s-1qj9g61: var(--s-19hh4gw);--s-1bvu74j: var(--hdrt9t);--jdmia2: var(--xcedj6);--ts1hpc: var(--s-14xlm6o);--s-187zl0b: var(--msg65c);--s-12s5kmm: var(--s-1ywnfza);--s-4fox1q: var(--zjva6a);--j3z1dw: var(--s-15n3uo5);--s-1jvq51g: var(--i6u0ap);--s-1joebgy: 24px;--s-19hh4gw: 32px;--g65i9c: var(--s-1ocxf4e);--hdrt9t: none;--wpt2ge: var(--s-1mnxhel);--w4jvxk: var(--s-1bq9l67);--s-1mflgki: var(--s-1xsxprz);--s-1517qlh: var(--qfwzw4);--sdtaur: var(--o2sqss);--s-6qvd4o: var(--xxsoub);--y4gv3: var(--s-1hw9qk9);--s-193lww5: var(--s-9rewa3);--yem2xc: var(--s-1k0d4db);--s-1uz67ki: var(--syp0fc);--b4hhf7: var(--s-18pg62i);--s-1bq9l67: var(--xcedj6);--s-1xsxprz: var(--s-14xlm6o);--qfwzw4: var(--msg65c);--o2sqss: var(--s-1ywnfza);--xxsoub: var(--zjva6a);--s-1hw9qk9: var(--s-15n3uo5);--s-9rewa3: var(--i6u0ap);--s-1k0d4db: 20px;--syp0fc: 28px;--s-1vfd5li: var(--s-1ocxf4e);--s-18pg62i: none;--s-1p87an6: var(--s-1mnxhel);--gbhvil: var(--s-1tckhn5);--s-2wlxzm: var(--s-1bnzo0w);--s-1lhh5an: var(--ub00w8);--b57bg4: var(--vayv2j);--s-10pihpx: var(--s-1bg5wjj);--s-1de7swi: var(--ofc8t8);--p0d0ra: var(--s-1myygfh);--rdvhzd: var(--s-1vrlxop);--wxjtoa: var(--s-1fjdblk);--s-14i6ex0: var(--s-176iwse);--s-1tckhn5: var(--xcedj6);--s-1bnzo0w: var(--s-14xlm6o);--ub00w8: var(--msg65c);--vayv2j: var(--s-1ywnfza);--s-1bg5wjj: var(--zjva6a);--ofc8t8: var(--s-15n3uo5);--s-1myygfh: var(--i6u0ap);--s-1vrlxop: 16px;--s-1fjdblk: 24px;--s-15lxxlk: var(--s-1ocxf4e);--s-176iwse: none;--ihun98: var(--s-1mnxhel);--lzkj6b: var(--s-1fz1zwb);--s-19gq58y: var(--s-1e9sg5q);--s-1fndoqe: var(--s-1xty0l1);--s-1ozmd2v: var(--s-1c9087t);--s-1itf6ev: var(--njr6lf);--lqlo87: var(--wvavyz);--s-15g638a: var(--s-1bdp00y);--s-101nale: var(--s-1rv6t4);--rpuu4f: var(--onmy4p);--s-1x2ggh5: var(--s-135hi2l);--s-1fz1zwb: var(--xcedj6);--s-1e9sg5q: var(--s-14xlm6o);--s-1xty0l1: var(--msg65c);--s-1c9087t: var(--s-1ywnfza);--njr6lf: var(--zjva6a);--wvavyz: var(--s-15n3uo5);--s-1bdp00y: var(--i6u0ap);--s-1rv6t4: 12px;--onmy4p: 20px;--s-4yu78: var(--s-1ocxf4e);--s-135hi2l: none;--qsps49: var(--ahgtyg);--s-1m5o6xs: var(--dilwm);--s-1sl6m46: var(--s-6omq4);--s-1tlryov: var(--nsaztv);--kidu0o: var(--s-1ixv1ks);--l2fksn: var(--s-1biv3ye);--s-16fd3c8: var(--s-1te2tup);--s-1n41s7u: var(--s-1nt3wam);--njb836: var(--s-108w7yg);--s-18nbbqu: var(--s-6mvx34);--b9ogvo: var(--s-1pbhbhw);--h3wc70: var(--z5eq11);--u4c2q6: var(--e1e86);--s-1oj6z6t: var(--uik06i);--s-1qtuyvq: var(--s-1eah8e8);--l28r8y: var(--h7f28h);--fcsdep: var(--s-1vvlcgn);--s-1ikrpfx: var(--s-36ddn3);--s-108w7yg: var(--qsps49);--s-6mvx34: var(--s-1m5o6xs);--s-1pbhbhw: var(--s-1sl6m46);--z5eq11: var(--s-1tlryov);--e1e86: var(--kidu0o);--uik06i: var(--l2fksn);--s-1eah8e8: var(--s-16fd3c8);--h7f28h: 18px;--s-1vvlcgn: 28px;--s-5hgyej: var(--s-1mnxhel);--s-36ddn3: none;--p1b3a1: var(--s-1nt3wam);--s-10jfra1: var(--wtyf0o);--s-1m1wff1: var(--s-167pe37);--s-1savn4h: var(--s-10fnwqi);--s-1gygsl6: var(--s-1sdpwmi);--li3rbu: var(--s-1prlirw);--s-9cy93t: var(--s-1oay49k);--s-11a5wqu: var(--b7x093);--s-17qz9cg: var(--s-1nk8z4c);--s-1pqj9m0: var(--s-1adv7ix);--s-1ctdufq: var(--s-2vga1d);--wtyf0o: var(--qsps49);--s-167pe37: var(--s-1m5o6xs);--s-10fnwqi: var(--s-1sl6m46);--s-1sdpwmi: var(--s-1tlryov);--s-1prlirw: var(--kidu0o);--s-1oay49k: var(--l2fksn);--b7x093: var(--s-16fd3c8);--s-1nk8z4c: 16px;--s-1adv7ix: 24px;--e9j7zt: var(--s-1mnxhel);--s-2vga1d: none;--s-1e6wgok: var(--s-1nt3wam);--s-5twc1q: var(--iv638n);--s-13v453w: var(--zzbkbv);--q47ujb: var(--cw4443);--s-4fq1f8: var(--sf9nah);--s-8kvr39: var(--s-1lduq5c);--t9sogg: var(--s-49369g);--s-6dkjzu: var(--s-195juhb);--s-1wizgxe: var(--eoafo5);--s-7ih227: var(--s-7paqqe);--be5p7j: var(--pz3gk9);--iv638n: var(--qsps49);--zzbkbv: var(--s-1m5o6xs);--cw4443: var(--s-1sl6m46);--sf9nah: var(--s-1tlryov);--s-1lduq5c: var(--kidu0o);--s-49369g: var(--l2fksn);--s-195juhb: var(--s-16fd3c8);--eoafo5: 14px;--s-7paqqe: 20px;--x5dpqz: var(--s-1mnxhel);--pz3gk9: none;--pyk6k1: var(--ahgtyg);--s-1verpm8: var(--dilwm);--rd4b92: var(--s-6omq4);--s-1i90hyx: var(--nsaztv);--y96hdk: var(--s-1ixv1ks);--qkji3r: var(--s-1biv3ye);--s-1kwoc9c: var(--s-1te2tup);--s-1qv548f: var(--s-1nt3wam);--s-1tq5jkt: var(--v43x2t);--s-3uli8c: var(--tcmtp2);--s-10wdlk9: var(--g77870);--s-1iqa1pt: var(--s-1xy9kgq);--vxd1ew: var(--wqx1if);--w2b5wa: var(--s-1fysgfv);--s-16ck0e3: var(--s-18527no);--okauee: var(--s-1rxtcbb);--s-1fhkvft: var(--s-1a3m0xe);--hj8sur: var(--ayuh76);--v43x2t: var(--pyk6k1);--tcmtp2: var(--s-1verpm8);--g77870: var(--rd4b92);--s-1xy9kgq: var(--s-1i90hyx);--wqx1if: var(--y96hdk);--s-1fysgfv: var(--qkji3r);--s-18527no: var(--s-1kwoc9c);--s-1rxtcbb: 16px;--s-1a3m0xe: 24px;--s-5y4pqp: var(--s-1mnxhel);--ayuh76: none;--ep1e0f: var(--s-1nt3wam);--s-6vkd26: var(--huplq6);--s-1h9quwx: var(--l1gcj7);--t2iyzt: var(--s-3mrwm8);--s-1xn3ax7: var(--l6yv66);--s-15oh72s: var(--s-1k1xktp);--s-1ohirt0: var(--s-3dxl6s);--juchqv: var(--s7es0h);--s-1g9cdsy: var(--tlxlq6);--yfph9h: var(--s-432ttp);--r31u81: var(--s-59wabm);--huplq6: var(--pyk6k1);--l1gcj7: var(--s-1verpm8);--s-3mrwm8: var(--rd4b92);--l6yv66: var(--s-1i90hyx);--s-1k1xktp: var(--y96hdk);--s-3dxl6s: var(--qkji3r);--s7es0h: var(--s-1kwoc9c);--tlxlq6: 14px;--s-432ttp: 20px;--s-1htz8iq: var(--s-1mnxhel);--s-59wabm: none;--ereqaf: var(--s-1nt3wam);--yiyhsh: var(--ft4em7);--sodrin: var(--ngt1c6);--bfuocu: var(--s-1vj0i13);--s-2nir93: var(--c3yjur);--s-1jh3kwa: var(--r99a4f);--hfec15: var(--s-19xhaty);--s-16ewvzx: var(--ctnn8n);--zzbsa1: var(--mae4h0);--ki0zdj: var(--s-1kc6i1b);--s-12qaksx: var(--s-1k0dbzs);--ft4em7: var(--pyk6k1);--ngt1c6: var(--s-1verpm8);--s-1vj0i13: var(--rd4b92);--c3yjur: var(--s-1i90hyx);--r99a4f: var(--y96hdk);--s-19xhaty: var(--qkji3r);--ctnn8n: var(--s-1kwoc9c);--mae4h0: 12px;--s-1kc6i1b: 16px;--s-10ubhie: var(--s-1mnxhel);--s-1k0dbzs: none;--l5cirb: var(--s-1camloi);--s-3ab8ub: var(--s-1fverle);--s-15f02i8: var(--s-2c6wsx);--s-1f29tr2: var(--s-19hyq79);--s-18tqzme: var(--s-1wum1rt);--s-1s3tcwv: var(--s-1p07rxq);--s-1sr9szs: var(--s-18ns0of);--s-72fzvy: 0px;--s-1n66wtu: 1px;--s-1camloi: 2px;--s-1fverle: 4px;--s-1eo1l6l: 6px;--s-2c6wsx: 8px;--s-14t02z3: 10px;--s-1cn5k4b: 12px;--s-10yt1e6: 14px;--s-19hyq79: 16px;--zmqxvl: 18px;--s-16s2r5d: 20px;--s-1wum1rt: 24px;--s-11p7nl: 28px;--s-1p07rxq: 32px;--s-18g2og9: 36px;--x3ux79: 40px;--s-18ns0of: 48px;--s-7dpk8n: 56px;--s-1ubl41v: 64px;--s-12tsswl: 72px;--s-1e1s3yj: 80px;--s-1c4fwdw: var(--s-282tnx);--jpxxql: var(--s-282tnx);--u4yslg: none;--s-1l4o7cj: 4px;--s-282tnx: 6px;--s-9fb64w: 8px;--s-721m59: 12px;--eazveb: 16px;--s-1pfp217: 9999em;--s-11c5ftm: solid;--s-5oekti: dashed;--s-12pesem: 1px;--s-1p3l5ml: 2px;--f0gr6w: 4px;--li639m: 100%;--s-18ciw8m: min-content;--s-15qxt3g: max-content;--s-22nfqw: fit-content;--cvc234: 50%;--bcipp6: 33.3333%;--s-1990hu4: 66.6667%;--hrim1e: 25%;--ys322a: 50%;--s-2hrodg: 75%;--ywypcv: 20%;--s-1j1r695: 40%;--s-3qcouv: 60%;--s-1c433cn: 80%;--s-1o6hvkt: 16.6667%;--v94vw1: 33.3333%;--ncjl8c: 50%;--s-14apa3: 66.6667%;--kcudzm: 83.3333%;--s-1sq848d: 8.3333%;--k9vhhg: 16.6667%;--s-1m2eq9s: 25%;--s-1hfpugt: 33.3333%;--s-12j0rnv: 41.6667%;--s-1ce5jho: 50%;--yca82r: 58.3333%;--s-1bb34n7: 66.6667%;--x6iu4: 75%;--s-1qjxzud: 83.3333%;--d52z5c: 91.6667%;--s-1qqjf1s: 0px 1px 1px 0px rgba(0, 0, 0, 0.12), 0px 2px 5px 0px rgba(48, 49, 61, 0.08);--s29i93: 0px 3px 6px 0px rgba(0, 0, 0, 0.12), 0px 7px 14px 0px rgba(48, 49, 61, 0.08);--s-144bgvr: 0px 5px 15px 0px rgba(0, 0, 0, 0.12), 0px 15px 35px 0px rgba(48, 49, 61, 0.08);--qbcnik: 0px 5px 15px 0px rgba(0, 0, 0, 0.12), 0px 15px 35px 0px rgba(48, 49, 61, 0.08), 0px 50px 100px 0px rgba(48, 49, 61, 0.08);--s-46hi4m: var(--s-144bgvr);--s-4fcpev: 0px 0px 15px 0px rgba(0, 0, 0, 0.12), 0px 0px 35px 0px rgba(48, 49, 61, 0.08);--s-8kdpya: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-1q5y78: 0px -1px 1px 0px rgba(20, 19, 78, 0.32);--s-1kgpzka: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-186fre1: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-1fb3eog: 0px 1px 1px 0px rgba(20, 19, 78, 0.32);--s-1ibn4id: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--s-1l32yqd: 0px -1px 1px 0px rgba(16, 17, 26, 0.16);--wq0k6h: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--fur145: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--s-1fecqxp: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--ytuq2g: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--k2t3ri: 0px -1px 1px 0px rgba(62, 2, 26, 0.32);--s-1fc7ea9: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--s-8p4pnm: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--s-1s9evt6: 0px 1px 1px 0px rgba(62, 2, 26, 0.32);--pga66p: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--s-7nyne0: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--s-1p8nnzk: 0px -1px 1px 0px rgba(1, 28, 58, 0.16);--s-4fmi5d: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--s-1mw80b4: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--s-1mp6cz9: 0px 1px 1px 0px rgba(1, 28, 58, 0.16);--o68lqt: 0px 1px 1px 0px rgba(62, 2, 26, .16);--s-1srjzen: 0px -1px 1px 0px rgba(62, 2, 26, .16);--s-5cda5b: 0px 1px 1px 0px rgba(62, 2, 26, .16);--uojav1: 0px 1px 1px 0px rgba(62, 2, 26, .16);--s-1xpb9p2: 0px 1px 1px 0px rgba(62, 2, 26, .16);--s-1atvbio: 0px -1px 1px 0px rgba(16, 17, 26, 0.16);--s-9l041r: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--fcko44: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--zh5azq: 0px 1px 1px 0px rgba(16, 17, 26, 0.16);--tnw4uh: 490px;--p6z4q9: 768px;--s-1tolf8z: 1040px;--s-13qggw6: 1440px;--s-1oz5pfq: 0;--s-52qljy: 490px;--m9yfsr: 768px;--s-1gz3jh8: 1040px;--s-1ad545m: 1440px;--s-1xy6qjm: 0 0 0 4px rgba(1, 150, 237, .36);
}
#​#​#​#​#​#​#​ .tooltip-trigger-isolate {
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [2]</summary>

| URL | markcrawl words [6] / preamble [2] | crawl4ai words [6] / preamble [2] | crawl4ai-raw words [6] / preamble [2] | scrapy+md words [6] / preamble [2] | crawlee words [6] / preamble [2] | colly+md words [6] / preamble [2] | playwright words [6] / preamble [2] | firecrawl words [6] / preamble [2] |
|---|---|---|---|---|---|---|---|---|
| docs.stripe.com/acceptable-verification-documents | 968 / 27 | 1378 / 144 | 1378 / 144 | 1116 / 141 | 16329 / 7825 | 16196 / 7771 | 16326 / 7843 | — |
| docs.stripe.com/ach-deprecated | 2399 / 13 | 2558 / 36 | 2558 / 36 | 2453 / 33 | 30600 / 10574 | 30430 / 10511 | 30561 / 10556 | — |
| docs.stripe.com/agentic-commerce | 236 / 8 | 437 / 150 | 437 / 150 | 409 / 147 | 10210 / 7775 | 10135 / 7721 | 10189 / 7775 | — |
| docs.stripe.com/agentic-commerce/apps | 357 / 11 | 561 / 159 | 561 / 159 | 536 / 156 | 10523 / 7903 | 10445 / 7858 | 10502 / 7903 | — |
| docs.stripe.com/agentic-commerce/apps/accept-payment | 957 / 7 | 1243 / 163 | 1243 / 163 | 1144 / 160 | 16562 / 10765 | 16405 / 10711 | 16536 / 10765 | — |
| docs.stripe.com/agentic-commerce/concepts | 385 / 8 | 628 / 162 | 628 / 162 | 570 / 159 | 10675 / 7938 | 10541 / 7866 | 10645 / 7929 | — |
| docs.stripe.com/agentic-commerce/concepts/shared-paymen | 477 / 7 | 749 / 166 | 749 / 166 | 667 / 163 | 11053 / 8161 | 10922 / 8116 | 11050 / 8179 | — |
| docs.stripe.com/agentic-commerce/enable-in-context-sell | 1007 / 11 | 1375 / 158 | 1375 / 158 | 1188 / 155 | 14487 / 8159 | 14244 / 8105 | 14457 / 8150 | — |
| docs.stripe.com/agentic-commerce/product-feed | 742 / 15 | 1010 / 165 | 989 / 165 | 923 / 162 | 13813 / 7923 | 13674 / 7869 | 13801 / 7932 | — |
| docs.stripe.com/agentic-commerce/protocol | 595 / 11 | 848 / 169 | 827 / 169 | 784 / 166 | 11096 / 7948 | 10960 / 7876 | 11048 / 7921 | — |
| docs.stripe.com/agentic-commerce/protocol/specification | 4075 / 7 | 4439 / 173 | 4439 / 173 | 4272 / 170 | 17362 / 8329 | 17198 / 8284 | 17350 / 8338 | — |
| docs.stripe.com/agents | 306 / 17 | 490 / 132 | 490 / 132 | 452 / 129 | 18983 / 10762 | 18887 / 10708 | 18962 / 10762 | — |
| docs.stripe.com/agents-billing-workflows | 726 / 11 | 925 / 124 | 904 / 124 | 870 / 121 | 16206 / 7549 | 16102 / 7504 | 16212 / 7576 | — |
| docs.stripe.com/api-includable-response-values | 612 / 20 | 808 / 170 | 808 / 170 | 793 / 167 | 20265 / 10700 | 20192 / 10646 | 20244 / 10700 | — |
| docs.stripe.com/api-v2-overview | 1660 / 18 | 1970 / 165 | 1970 / 165 | 1838 / 162 | 21832 / 10922 | 21644 / 10868 | 21829 / 10940 | — |
| docs.stripe.com/apis | 292 / 21 | 485 / 160 | 464 / 160 | 462 / 157 | 15046 / 7335 | 14971 / 7281 | 15025 / 7335 | — |
| docs.stripe.com/apple-pay | 2390 / 16 | 2838 / 266 | 2838 / 266 | 2674 / 263 | 22059 / 11491 | 21860 / 11437 | 22038 / 11491 | — |
| docs.stripe.com/apple-pay/apple-pay-recurring | 1071 / 13 | 1454 / 271 | 1454 / 271 | 1360 / 268 | 15327 / 11115 | 15157 / 11043 | 15297 / 11106 | — |
| docs.stripe.com/apple-pay/best-practices | 1296 / 16 | 1708 / 269 | 1708 / 269 | 1580 / 266 | 12612 / 7958 | 12418 / 7895 | 12573 / 7940 | — |
| docs.stripe.com/apple-pay/cartes-bancaires | 275 / 16 | 620 / 272 | 599 / 272 | 563 / 269 | 13511 / 10816 | 13396 / 10762 | 13490 / 10816 | — |
| docs.stripe.com/apple-pay/disputes-refunds | 222 / 14 | 546 / 274 | 546 / 274 | 513 / 271 | 10271 / 7805 | 10162 / 7733 | 10232 / 7787 | — |
| docs.stripe.com/apple-pay/merchant-tokens | 609 / 14 | 942 / 271 | 942 / 271 | 897 / 268 | 11502 / 8069 | 11419 / 8033 | 11490 / 8078 | — |
| docs.stripe.com/atlas | 513 / 22 | 737 / 191 | 737 / 191 | 717 / 188 | 10603 / 7664 | 10531 / 7610 | 10582 / 7664 | — |
| docs.stripe.com/atlas/83b-election | 1179 / 23 | 1455 / 193 | 1455 / 193 | 1380 / 190 | 12204 / 7860 | 12089 / 7824 | 12192 / 7869 | — |
| docs.stripe.com/atlas/83b-elections-non-us-founders | 280 / 19 | 503 / 194 | 503 / 194 | 486 / 191 | 10164 / 7683 | 10089 / 7629 | 10143 / 7683 | — |
| docs.stripe.com/atlas/accept-payments | 402 / 27 | 639 / 194 | 639 / 194 | 600 / 191 | 10488 / 7711 | 10382 / 7648 | 10467 / 7711 | — |
| docs.stripe.com/atlas/business-taxes | 1190 / 22 | 1472 / 192 | 1472 / 192 | 1391 / 189 | 12836 / 8021 | 12719 / 7985 | 12815 / 8021 | — |
| docs.stripe.com/atlas/company-types | 313 / 21 | 569 / 192 | 569 / 192 | 521 / 189 | 10405 / 7698 | 10301 / 7644 | 10384 / 7698 | — |
| docs.stripe.com/atlas/equity-terms | 714 / 19 | 973 / 193 | 973 / 193 | 919 / 190 | 11196 / 7860 | 11109 / 7824 | 11193 / 7878 | — |
| docs.stripe.com/atlas/fundraise-with-safes | 758 / 18 | 1025 / 193 | 1004 / 193 | 964 / 190 | 11308 / 7700 | 11218 / 7673 | 11287 / 7700 | — |
| docs.stripe.com/atlas/incorporation-documents | 665 / 18 | 887 / 192 | 866 / 192 | 870 / 189 | 11032 / 7745 | 10957 / 7691 | 11011 / 7745 | — |
| docs.stripe.com/atlas/indian-founder-guide | 1511 / 22 | 1779 / 197 | 1779 / 197 | 1719 / 194 | 12636 / 7717 | 12538 / 7672 | 12615 / 7717 | — |
| docs.stripe.com/atlas/payments-business-bank | 320 / 18 | 551 / 193 | 551 / 193 | 526 / 190 | 10253 / 7700 | 10188 / 7664 | 10250 / 7718 | — |
| docs.stripe.com/atlas/signup | 1884 / 19 | 2224 / 195 | 2224 / 195 | 2096 / 192 | 14053 / 8266 | 13868 / 8212 | 14041 / 8275 | — |
| docs.stripe.com/atlas/singapore-founder-guide | 1803 / 76 | 2067 / 196 | 2067 / 196 | 1958 / 193 | 13390 / 7945 | 13260 / 7900 | 13369 / 7945 | — |
| docs.stripe.com/atlas/stripe-treasury-offer | 198 / 27 | 255 / 36 | 255 / 36 | 238 / 33 | 20709 / 7014 | 20634 / 6960 | 20688 / 7014 | — |
| docs.stripe.com/automated-testing | 650 / 14 | 865 / 162 | 865 / 162 | 829 / 159 | 19790 / 10826 | 19696 / 10772 | 19769 / 10826 | — |
| docs.stripe.com/batch-api | 2786 / 10 | 3191 / 161 | 3191 / 161 | 2968 / 158 | 20916 / 8179 | 20645 / 8125 | 20886 / 8170 | — |
| docs.stripe.com/billing | 557 / 16 | 710 / 108 | 689 / 108 | 682 / 105 | 9630 / 7663 | 9555 / 7609 | 9609 / 7663 | — |
| docs.stripe.com/billing/automation-recipes | 565 / 25 | 750 / 116 | 750 / 116 | 687 / 113 | 9682 / 7598 | 9552 / 7535 | 9670 / 7607 | — |
| docs.stripe.com/billing/automations | 1254 / 38 | 1418 / 117 | 1418 / 117 | 1364 / 114 | 11533 / 8041 | 11414 / 7987 | 11503 / 8032 | — |
| docs.stripe.com/billing/billing-apis | 867 / 18 | 1119 / 111 | 1119 / 111 | 1002 / 108 | 10793 / 7896 | 10618 / 7842 | 10772 / 7896 | — |
| docs.stripe.com/billing/collection-method | 1345 / 21 | 1687 / 217 | 1666 / 217 | 1572 / 214 | 12394 / 8307 | 12230 / 8262 | 12391 / 8325 | — |
| docs.stripe.com/billing/customer | 1462 / 10 | 1758 / 152 | 1758 / 152 | 1635 / 149 | 12794 / 7878 | 12608 / 7815 | 12746 / 7851 | — |
| docs.stripe.com/billing/customer/balance | 1181 / 8 | 1448 / 154 | 1448 / 154 | 1358 / 151 | 15278 / 11166 | 15129 / 11094 | 15257 / 11166 | — |
| docs.stripe.com/billing/customer/tax-ids | 3597 / 14 | 2920 / 217 | 2920 / 217 | 3831 / 214 | 13864 / 8231 | 13724 / 8177 | 13843 / 8231 | — |
| docs.stripe.com/billing/entitlements | 559 / 17 | 852 / 215 | 852 / 215 | 788 / 212 | 11664 / 7771 | 11530 / 7717 | 11643 / 7771 | — |
| docs.stripe.com/billing/invoices/subscription | 2215 / 18 | 2699 / 216 | 2699 / 216 | 2444 / 213 | 19350 / 11411 | 19050 / 11366 | 19320 / 11402 | — |
| docs.stripe.com/billing/multi-entity-business | 620 / 20 | 849 / 124 | 828 / 124 | 765 / 121 | 10063 / 7657 | 9921 / 7603 | 10051 / 7666 | — |
| docs.stripe.com/billing/revenue-recovery | 440 / 12 | 610 / 120 | 610 / 120 | 579 / 117 | 10132 / 8220 | 10052 / 8175 | 10111 / 8220 | — |
| docs.stripe.com/billing/revenue-recovery/customer-email | 955 / 18 | 1166 / 122 | 1166 / 122 | 1090 / 119 | 10649 / 7635 | 10514 / 7581 | 10646 / 7653 | — |
| docs.stripe.com/billing/revenue-recovery/recovery-analy | 594 / 24 | 779 / 121 | 779 / 121 | 722 / 118 | 9907 / 7764 | 9783 / 7701 | 9895 / 7773 | — |
| docs.stripe.com/billing/revenue-recovery/smart-retries | 1175 / 11 | 1366 / 122 | 1366 / 122 | 1317 / 119 | 11985 / 8222 | 11887 / 8177 | 11964 / 8222 | — |
| docs.stripe.com/billing/subscriptions/acss-debit | 1901 / 13 | 2315 / 270 | 2315 / 270 | 2192 / 267 | 19309 / 11332 | 19104 / 11260 | 19288 / 11332 | — |
| docs.stripe.com/billing/subscriptions/analytics | 780 / 11 | 1101 / 216 | 1101 / 216 | 1016 / 213 | 12235 / 8132 | 12107 / 8087 | 12223 / 8141 | — |
| docs.stripe.com/billing/subscriptions/au-becs-debit | 2466 / 13 | 2879 / 271 | 2879 / 271 | 2758 / 268 | 22599 / 11373 | 22422 / 11328 | 22578 / 11373 | — |
| docs.stripe.com/billing/subscriptions/backdating | 1193 / 18 | 1491 / 216 | 1470 / 216 | 1422 / 213 | 15231 / 11087 | 15109 / 11033 | 15201 / 11078 | — |
| docs.stripe.com/billing/subscriptions/bank-transfer | 378 / 12 | 718 / 268 | 718 / 268 | 665 / 265 | 14016 / 11049 | 13894 / 10986 | 13995 / 11049 | — |
| docs.stripe.com/billing/subscriptions/billing-cycle | 1951 / 19 | 2289 / 217 | 2289 / 217 | 2192 / 214 | 19255 / 11068 | 19100 / 11014 | 19234 / 11068 | — |
| docs.stripe.com/billing/subscriptions/billing-mode | 1157 / 20 | 1477 / 223 | 1477 / 223 | 1392 / 220 | 17873 / 11105 | 17742 / 11060 | 17861 / 11114 | — |
| docs.stripe.com/billing/subscriptions/billing-mode/comp | 1986 / 29 | 2429 / 230 | 2429 / 230 | 2218 / 227 | 13111 / 8184 | 12815 / 8103 | 13072 / 8166 | — |
| docs.stripe.com/billing/subscriptions/build-subscriptio | 2225 / 18 | 2602 / 237 | 2602 / 237 | 2486 / 234 | 102890 / 12139 | 102717 / 12085 | 102854 / 12139 | — |
| docs.stripe.com/billing/subscriptions/build-subscriptio | 2748 / 18 | 3159 / 237 | 3159 / 237 | 3004 / 234 | 103447 / 12141 | — | 103415 / 12141 | — |
| docs.stripe.com/billing/subscriptions/build-subscriptio | 3526 / 18 | 4054 / 237 | 4054 / 237 | 3783 / 234 | 104371 / 12171 | 103237 / 12087 | 104348 / 12171 | — |
| docs.stripe.com/billing/subscriptions/build-subscriptio | 1807 / 18 | 2168 / 237 | 2168 / 237 | 2064 / 234 | 102764 / 12451 | 102607 / 12397 | 102743 / 12451 | — |
| docs.stripe.com/billing/subscriptions/build-subscriptio | 3126 / 18 | 3676 / 237 | 3676 / 237 | 3383 / 234 | 103395 / 11574 | — | 103372 / 11574 | — |
| docs.stripe.com/billing/subscriptions/build-subscriptio | 3220 / 18 | 3785 / 237 | 3785 / 237 | 3477 / 234 | 103511 / 11580 | — | 103488 / 11580 | — |
| docs.stripe.com/billing/subscriptions/build-subscriptio | 3487 / 18 | 4062 / 237 | 4062 / 237 | 3744 / 234 | 103782 / 11574 | 103049 / 11520 | 103759 / 11574 | — |
| docs.stripe.com/billing/subscriptions/cancel | 1754 / 23 | 2098 / 216 | 2098 / 216 | 1981 / 213 | 17380 / 11280 | 17208 / 11235 | 17350 / 11271 | — |
| docs.stripe.com/billing/subscriptions/change | 351 / 39 | 591 / 223 | 591 / 223 | 566 / 220 | 9570 / 7919 | 9478 / 7856 | 9531 / 7901 | — |
| docs.stripe.com/billing/subscriptions/change-price | 1197 / 20 | 1518 / 226 | 1518 / 226 | 1434 / 223 | 16938 / 11308 | 16778 / 11236 | 16926 / 11317 | — |
| docs.stripe.com/billing/subscriptions/coupons | 2997 / 21 | 3392 / 216 | 3392 / 216 | 3223 / 213 | 22006 / 11622 | 21786 / 11568 | 21985 / 11622 | — |
| docs.stripe.com/billing/subscriptions/deferred-payment | 591 / 19 | 868 / 217 | 868 / 217 | 821 / 214 | 10384 / 8164 | 10284 / 8101 | 10345 / 8146 | — |
| docs.stripe.com/billing/subscriptions/design-an-integra | 1763 / 17 | 2107 / 217 | 2107 / 217 | 2000 / 214 | 12775 / 8323 | 12654 / 8269 | 12745 / 8314 | — |
| docs.stripe.com/billing/subscriptions/migrate-subscript | 360 / 19 | 645 / 228 | 645 / 228 | 601 / 225 | 9604 / 7906 | 9527 / 7870 | 9601 / 7924 | — |
| docs.stripe.com/billing/subscriptions/mixed-interval | 1213 / 16 | 1530 / 218 | 1530 / 218 | 1447 / 215 | 14331 / 8206 | 14199 / 8161 | 14292 / 8188 | — |
| docs.stripe.com/billing/subscriptions/overview | 2035 / 16 | 2384 / 217 | 2384 / 217 | 2273 / 214 | 13900 / 8120 | 13751 / 8084 | 13888 / 8129 | — |
| docs.stripe.com/billing/subscriptions/pause | 745 / 16 | 1047 / 216 | 1047 / 216 | 976 / 213 | 13791 / 11309 | 13635 / 11228 | 13761 / 11300 | — |
| docs.stripe.com/billing/subscriptions/pause-payment | 900 / 20 | 1208 / 217 | 1208 / 217 | 1128 / 214 | 15506 / 11109 | 15368 / 11055 | 15485 / 11109 | — |
| docs.stripe.com/billing/subscriptions/payment-methods-s | 667 / 18 | 998 / 265 | 998 / 265 | 945 / 262 | 13457 / 10793 | 13334 / 10730 | 13436 / 10793 | — |
| docs.stripe.com/billing/subscriptions/paypal | 1184 / 11 | 1577 / 267 | 1577 / 267 | 1472 / 264 | 29187 / 11300 | 29020 / 11246 | 29166 / 11300 | — |
| docs.stripe.com/billing/subscriptions/pending-updates | 904 / 21 | 1216 / 227 | 1216 / 227 | 1141 / 224 | 14471 / 11224 | 14326 / 11161 | 14450 / 11224 | — |
| docs.stripe.com/billing/subscriptions/prebilling | 676 / 13 | 943 / 218 | 943 / 218 | 912 / 215 | 10738 / 7907 | 10649 / 7853 | 10735 / 7925 | — |
| docs.stripe.com/billing/subscriptions/prorations | 2584 / 16 | 2962 / 226 | 2962 / 226 | 2825 / 223 | 20656 / 11202 | 20471 / 11157 | 20642 / 11220 | — |
| docs.stripe.com/billing/subscriptions/quantities | 1594 / 19 | 1744 / 36 | 1744 / 36 | 1646 / 33 | 30459 / 10798 | 30285 / 10726 | 30429 / 10789 | — |
| docs.stripe.com/billing/subscriptions/sales-led-billing | 1844 / 18 | 2052 / 36 | 2052 / 36 | 1893 / 33 | 25419 / 7976 | 25176 / 7895 | 25380 / 7958 | — |
| docs.stripe.com/billing/subscriptions/stablecoins | 1057 / 16 | 1448 / 267 | 1448 / 267 | 1351 / 264 | 21316 / 11388 | 21168 / 11334 | 21295 / 11388 | — |
| docs.stripe.com/billing/subscriptions/subscription-sche | 3113 / 13 | 3463 / 216 | 3463 / 216 | 3347 / 213 | 34875 / 11163 | 34705 / 11109 | 34854 / 11163 | — |
| docs.stripe.com/billing/subscriptions/third-party-payme | 2400 / 13 | 2826 / 219 | 2826 / 219 | 2640 / 216 | 28755 / 11029 | 28514 / 10975 | 28731 / 11029 | — |
| docs.stripe.com/billing/subscriptions/trials | 2365 / 5 | 2905 / 228 | 2905 / 228 | 2635 / 225 | 25744 / 11417 | 25428 / 11372 | 25732 / 11426 | — |
| docs.stripe.com/billing/subscriptions/trials/free-trial | 2111 / 6 | 2615 / 233 | 2615 / 233 | 2369 / 230 | 22217 / 11233 | 21902 / 11170 | 22178 / 11215 | — |
| docs.stripe.com/billing/subscriptions/trials/manage-tri | 672 / 11 | 1014 / 236 | 1014 / 236 | 928 / 233 | 10280 / 7937 | 10130 / 7874 | 10259 / 7937 | — |
| docs.stripe.com/billing/subscriptions/usage-based | 139 / 12 | 320 / 134 | 320 / 134 | 296 / 131 | 8807 / 7620 | 8732 / 7566 | 8786 / 7620 | — |
| docs.stripe.com/billing/subscriptions/usage-based-legac | 810 / 3 | 945 / 36 | 945 / 36 | 877 / 33 | 30252 / 7627 | 30133 / 7573 | 30231 / 7627 | — |
| docs.stripe.com/billing/subscriptions/usage-based-legac | 984 / 10 | 1094 / 36 | 1094 / 36 | 1041 / 33 | 30932 / 10423 | 30830 / 10378 | 30920 / 10432 | — |
| docs.stripe.com/billing/subscriptions/usage-based-legac | 1417 / 8 | 1534 / 36 | 1534 / 36 | 1488 / 33 | 31902 / 10840 | 31803 / 10786 | 31881 / 10840 | — |
| docs.stripe.com/billing/subscriptions/usage-based-legac | 649 / 10 | 749 / 36 | 749 / 36 | 711 / 33 | 25580 / 10468 | 25484 / 10414 | 25559 / 10468 | — |
| docs.stripe.com/billing/subscriptions/usage-based-v1/us | 118 / 8 | 304 / 146 | 304 / 146 | 287 / 143 | 8838 / 7666 | 8763 / 7612 | 8817 / 7666 | — |
| docs.stripe.com/billing/subscriptions/usage-based-v1/us | 1596 / 15 | 1868 / 151 | 1847 / 151 | 1769 / 148 | 16921 / 8109 | 16791 / 8064 | 16909 / 8118 | — |
| docs.stripe.com/billing/subscriptions/usage-based-v2/ov | 77 / 10 | 267 / 120 | 267 / 120 | 218 / 117 | 8896 / 7776 | 8790 / 7722 | 8875 / 7776 | — |
| docs.stripe.com/billing/subscriptions/usage-based/advan | 8806 / 18 | 3137 / 124 | 3137 / 124 | 8943 / 121 | 25713 / 11406 | 25491 / 11334 | 25674 / 11388 | — |
| docs.stripe.com/billing/subscriptions/usage-based/advan | 1963 / 18 | 1299 / 136 | 1299 / 136 | 2112 / 133 | 13561 / 8672 | 13353 / 8636 | 13558 / 8690 | — |
| docs.stripe.com/billing/subscriptions/usage-based/alert | 563 / 8 | 777 / 139 | 777 / 139 | 737 / 136 | 14415 / 10889 | 14330 / 10844 | 14394 / 10889 | — |
| docs.stripe.com/billing/subscriptions/usage-based/analy | 1057 / 9 | 1235 / 36 | 1235 / 36 | 1115 / 33 | 13597 / 10565 | 13392 / 10484 | 13558 / 10547 | — |
| docs.stripe.com/billing/subscriptions/usage-based/billi | 1503 / 52 | 1791 / 140 | 1770 / 140 | 1622 / 137 | 11983 / 7980 | 11782 / 7935 | 11971 / 7989 | — |
| docs.stripe.com/billing/subscriptions/usage-based/billi | 502 / 11 | 759 / 145 | 738 / 145 | 667 / 142 | 12789 / 8029 | 12641 / 7966 | 12768 / 8029 | — |
| docs.stripe.com/billing/subscriptions/usage-based/confi | 666 / 11 | 901 / 163 | 901 / 163 | 849 / 160 | 10364 / 8102 | 10239 / 8030 | 10343 / 8102 | — |
| docs.stripe.com/billing/subscriptions/usage-based/how-i | 525 / 11 | 733 / 137 | 733 / 137 | 687 / 134 | 10083 / 7969 | 9988 / 7924 | 10053 / 7960 | — |
| docs.stripe.com/billing/subscriptions/usage-based/imple | 1296 / 11 | 1571 / 151 | 1571 / 151 | 1473 / 148 | 15012 / 8285 | 14869 / 8231 | 14982 / 8276 | — |
| docs.stripe.com/billing/subscriptions/usage-based/manag | 1036 / 28 | 1212 / 137 | 1212 / 137 | 1176 / 134 | 15637 / 10805 | 15534 / 10742 | 15634 / 10823 | — |
| docs.stripe.com/billing/subscriptions/usage-based/meter | 843 / 8 | 1082 / 165 | 1082 / 165 | 1036 / 162 | 14440 / 10912 | 14328 / 10840 | 14401 / 10894 | — |
| docs.stripe.com/billing/subscriptions/usage-based/monit | 397 / 11 | 574 / 137 | 574 / 137 | 554 / 134 | 9396 / 7701 | 9321 / 7647 | 9375 / 7701 | — |
| docs.stripe.com/billing/subscriptions/usage-based/prici | 3573 / 9 | 2844 / 121 | 2844 / 121 | 3727 / 118 | 32279 / 11538 | 32094 / 11475 | 32240 / 11520 | — |
| docs.stripe.com/billing/subscriptions/usage-based/recor | 1880 / 14 | 2172 / 164 | 2172 / 164 | 2061 / 161 | 16487 / 11210 | 16329 / 11156 | 16466 / 11210 | — |
| docs.stripe.com/billing/subscriptions/usage-based/recor | 537 / 16 | 784 / 165 | 784 / 165 | 717 / 162 | 9867 / 7937 | 9725 / 7856 | 9819 / 7910 | — |
| docs.stripe.com/billing/subscriptions/usage-based/thres | 1094 / 9 | 1319 / 139 | 1319 / 139 | 1267 / 136 | 13908 / 10866 | 13798 / 10812 | 13896 / 10875 | — |
| docs.stripe.com/billing/subscriptions/usage-based/use-c | 1864 / 5 | 2203 / 150 | 2203 / 150 | 2042 / 147 | 20570 / 8108 | 20368 / 8045 | 20558 / 8117 | — |
| docs.stripe.com/billing/subscriptions/use-cases | 172 / 17 | 245 / 36 | 224 / 36 | 222 / 33 | 20513 / 6863 | 20438 / 6809 | 20492 / 6863 | — |
| docs.stripe.com/billing/subscriptions/webhooks | 4033 / 18 | 3355 / 217 | 3355 / 217 | 4263 / 214 | 16959 / 8470 | 16819 / 8425 | 16947 / 8479 | — |
| docs.stripe.com/billing/taxes/collect-taxes | 1561 / 10 | 1925 / 218 | 1925 / 218 | 1801 / 215 | 24076 / 11283 | 23890 / 11229 | 24055 / 11283 | — |
| docs.stripe.com/billing/taxes/migration | 1773 / 9 | 2136 / 219 | 2136 / 219 | 2014 / 216 | 20395 / 11135 | 20218 / 11081 | 20374 / 11135 | — |
| docs.stripe.com/billing/taxes/tax-rates | 2749 / 11 | 3125 / 216 | 3125 / 216 | 2985 / 213 | 17762 / 11189 | 17582 / 11153 | 17759 / 11207 | — |
| docs.stripe.com/billing/testing | 3648 / 20 | 2970 / 125 | 2970 / 125 | 3796 / 122 | 17316 / 8372 | 17094 / 8327 | 17304 / 8381 | — |
| docs.stripe.com/billing/testing/test-clocks | 173 / 8 | 348 / 129 | 348 / 129 | 325 / 126 | 8535 / 7282 | 8460 / 7228 | 8514 / 7282 | — |
| docs.stripe.com/billing/testing/test-clocks/api-advance | 2251 / 12 | 2520 / 134 | 2520 / 134 | 2404 / 131 | 24394 / 10886 | 24205 / 10823 | 24355 / 10868 | — |
| docs.stripe.com/billing/testing/test-clocks/simulate-su | 295 / 8 | 467 / 132 | 467 / 132 | 450 / 129 | 9115 / 7589 | 9040 / 7535 | 9094 / 7589 | — |
| docs.stripe.com/billing/token-billing | 595 / 20 | 756 / 36 | 735 / 36 | 642 / 33 | 9898 / 7635 | 9731 / 7581 | 9859 / 7617 | — |
| docs.stripe.com/building-extensions | 1054 / 11 | 1428 / 249 | 1428 / 249 | 1323 / 246 | 20688 / 10981 | 20525 / 10927 | 20667 / 10981 | — |
| docs.stripe.com/building-plugins | 1317 / 12 | 1614 / 170 | 1614 / 170 | 1506 / 167 | 21873 / 11144 | 21698 / 11081 | 21852 / 11144 | — |
| docs.stripe.com/capital/api-integration | 1802 / 10 | 2081 / 115 | 2081 / 115 | 1938 / 112 | 15830 / 11578 | 15629 / 11524 | 15800 / 11569 | — |
| docs.stripe.com/capital/embedded-component-integration | 1813 / 14 | 2085 / 118 | 2085 / 118 | 1955 / 115 | 13341 / 8705 | 13144 / 8633 | 13320 / 8705 | — |
| docs.stripe.com/capital/getting-started | 1482 / 12 | 1655 / 108 | 1655 / 108 | 1609 / 105 | 12135 / 8373 | 12029 / 8310 | 12114 / 8373 | — |
| docs.stripe.com/capital/how-capital-for-platforms-works | 2389 / 8 | 2670 / 98 | 2670 / 98 | 2514 / 95 | 15186 / 8397 | 14986 / 8343 | 15165 / 8397 | — |
| docs.stripe.com/capital/how-stripe-capital-works | 2216 / 29 | 2429 / 76 | 2408 / 76 | 2301 / 73 | 18269 / 7924 | 18095 / 7870 | 18248 / 7924 | — |
| docs.stripe.com/capital/import-non-stripe-data | 1756 / 14 | 1946 / 99 | 1946 / 99 | 1872 / 96 | 12781 / 8465 | 12615 / 8384 | 12751 / 8456 | — |
| docs.stripe.com/capital/marketing | 3330 / 5 | 3569 / 94 | 3569 / 94 | 3452 / 91 | 18593 / 8426 | 18432 / 8390 | 18581 / 8435 | — |
| docs.stripe.com/capital/mca-marketing-guidelines | 2226 / 9 | 2389 / 36 | 2389 / 36 | 2284 / 33 | 13077 / 8121 | 12933 / 8058 | 13047 / 8112 | — |
| docs.stripe.com/capital/no-code-integration | 1107 / 12 | 1375 / 111 | 1375 / 111 | 1238 / 108 | 11194 / 8133 | 10999 / 8079 | 11173 / 8133 | — |
| docs.stripe.com/capital/overview | 568 / 12 | 693 / 74 | 672 / 74 | 665 / 71 | 9390 / 7756 | 9315 / 7702 | 9369 / 7756 | — |
| docs.stripe.com/capital/promotional-tile | 840 / 11 | 1075 / 103 | 1075 / 103 | 968 / 100 | 14395 / 11299 | 14229 / 11227 | 14356 / 11281 | — |
| docs.stripe.com/capital/refills | 652 / 9 | 853 / 118 | 832 / 118 | 792 / 115 | 10100 / 8117 | 9963 / 8045 | 10061 / 8099 | — |
| docs.stripe.com/capital/regulatory-compliance | 2036 / 9 | 2219 / 95 | 2219 / 95 | 2153 / 92 | 13298 / 8579 | 13188 / 8534 | 13286 / 8588 | — |
| docs.stripe.com/capital/replacements | 764 / 7 | 951 / 118 | 951 / 118 | 906 / 115 | 10323 / 8129 | 10196 / 8057 | 10293 / 8120 | — |
| docs.stripe.com/changelog/2014-08-20/disputes-provide-s | 145 / 0 | 433 / 232 | 433 / 232 | 408 / 229 | 15833 / 7879 | 15732 / 7807 | 15812 / 7879 | — |
| docs.stripe.com/changelog/2014-09-08/bank-accounts-incl | 149 / 0 | 437 / 232 | 437 / 232 | 412 / 229 | 15842 / 7875 | 15777 / 7839 | 15830 / 7884 | — |
| docs.stripe.com/changelog/2014-10-07/create-card-bank-a | 159 / 0 | 447 / 232 | 447 / 232 | 422 / 229 | 15870 / 7879 | 15787 / 7825 | 15849 / 7879 | — |
| docs.stripe.com/changelog/2014-10-07/no-longer-retrieve | 134 / 0 | 422 / 232 | 422 / 232 | 397 / 229 | 15808 / 7873 | 15734 / 7828 | 15778 / 7864 | — |
| docs.stripe.com/changelog/2014-11-05/renames-charge-acc | 143 / 0 | 431 / 232 | 431 / 232 | 406 / 229 | 15835 / 7882 | 15743 / 7819 | 15823 / 7891 | — |
| docs.stripe.com/changelog/2014-11-20/disputes-reported- | 166 / 0 | 454 / 232 | 454 / 232 | 429 / 229 | 15869 / 7867 | 15804 / 7831 | 15875 / 7894 | — |
| docs.stripe.com/changelog/2014-11-20/invoice-items-refl | 177 / 0 | 465 / 232 | 465 / 232 | 440 / 229 | 15911 / 7886 | 15819 / 7823 | 15902 / 7877 | — |
| docs.stripe.com/changelog/2014-12-17/creating-accounts- | 144 / 0 | 432 / 232 | 432 / 232 | 407 / 229 | 15832 / 7875 | 15758 / 7830 | 15802 / 7866 | — |
| docs.stripe.com/changelog/2014-12-17/introduces-stateme | 203 / 0 | 491 / 232 | 491 / 232 | 466 / 229 | 15960 / 7880 | 15886 / 7835 | 15939 / 7880 | — |
| docs.stripe.com/changelog/2014-12-22/cards-use-unchecke | 198 / 0 | 486 / 232 | 486 / 232 | 461 / 229 | 15963 / 7891 | 15880 / 7837 | 15951 / 7900 | — |
| docs.stripe.com/changelog/2014-12-22/tokens-cards-no-lo | 155 / 0 | 443 / 232 | 443 / 232 | 418 / 229 | 15859 / 7882 | 15776 / 7828 | 15829 / 7873 | — |
| docs.stripe.com/changelog/2015-01-11/file-uploads-descr | 168 / 0 | 456 / 232 | 456 / 232 | 431 / 229 | 15875 / 7868 | 15801 / 7823 | 15872 / 7886 | — |
| docs.stripe.com/changelog/2015-01-26/subscriptions-repo | 182 / 0 | 470 / 232 | 470 / 232 | 445 / 229 | 15918 / 7880 | 15826 / 7817 | 15888 / 7871 | — |
| docs.stripe.com/changelog/2015-02-16/renames-transfer-c | 136 / 0 | 424 / 232 | 424 / 232 | 399 / 229 | 15826 / 7889 | 15743 / 7835 | 15787 / 7871 | — |
| docs.stripe.com/changelog/2015-02-18/charges-have-sourc | 176 / 0 | 464 / 232 | 464 / 232 | 439 / 229 | 15889 / 7867 | 15815 / 7822 | 15877 / 7876 | — |
| docs.stripe.com/changelog/2015-02-18/charges-succeed-ha | 149 / 0 | 437 / 232 | 437 / 232 | 412 / 229 | 15845 / 7881 | 15762 / 7827 | 15824 / 7881 | — |
| docs.stripe.com/changelog/2015-02-18/customers-have-sou | 190 / 0 | 478 / 232 | 478 / 232 | 453 / 229 | 15936 / 7881 | 15871 / 7845 | 15915 / 7881 | — |
| docs.stripe.com/changelog/2015-03-24/coupons-no-longer- | 173 / 0 | 461 / 232 | 461 / 232 | 436 / 229 | 15892 / 7876 | 15800 / 7813 | 15871 / 7876 | — |
| docs.stripe.com/changelog/2019-02-11/renames-allowed-so | 150 / 0 | 438 / 232 | 417 / 232 | 413 / 229 | 15847 / 7881 | 15773 / 7836 | 15826 / 7881 | — |
| docs.stripe.com/changelog/2019-02-11/renames-authorize- | 143 / 0 | 431 / 232 | 410 / 232 | 406 / 229 | 15817 / 7864 | 15743 / 7819 | 15796 / 7864 | — |
| docs.stripe.com/changelog/2019-02-11/renames-next-sourc | 156 / 0 | 444 / 232 | 444 / 232 | 419 / 229 | 15843 / 7864 | 15769 / 7819 | 15831 / 7873 | — |
| docs.stripe.com/changelog/2019-02-11/renames-save-sourc | 153 / 0 | 441 / 232 | 441 / 232 | 416 / 229 | 15853 / 7881 | 15752 / 7809 | 15832 / 7881 | — |
| docs.stripe.com/changelog/2019-02-19/accounts-no-longer | 190 / 0 | 478 / 232 | 478 / 232 | 453 / 229 | 15997 / 7893 | 15914 / 7839 | 15976 / 7893 | — |
| docs.stripe.com/changelog/2019-02-19/accounts-us-requir | 177 / 0 | 465 / 232 | 465 / 232 | 440 / 229 | 15926 / 7884 | 15834 / 7821 | 15887 / 7866 | — |
| docs.stripe.com/changelog/2019-02-19/business-details-m | 177 / 0 | 465 / 232 | 465 / 232 | 440 / 229 | 15902 / 7877 | 15810 / 7814 | 15881 / 7877 | — |
| docs.stripe.com/changelog/2019-02-19/changes-statement- | 259 / 0 | 548 / 232 | 527 / 232 | 522 / 229 | 16086 / 7865 | 16021 / 7829 | 16074 / 7874 | — |
| docs.stripe.com/changelog/2019-02-19/renames-business-i | 166 / 0 | 454 / 232 | 454 / 232 | 429 / 229 | 15865 / 7865 | 15809 / 7838 | 15862 / 7883 | — |
| docs.stripe.com/changelog/2019-02-19/several-fields-acc | 310 / 0 | 598 / 232 | 598 / 232 | 573 / 229 | 16165 / 7891 | 16082 / 7837 | 16135 / 7882 | — |
| docs.stripe.com/changelog/2019-02-19/verification-accou | 185 / 0 | 473 / 232 | 473 / 232 | 448 / 229 | 15923 / 7886 | 15840 / 7832 | 15884 / 7868 | — |
| docs.stripe.com/changelog/2019-08-14/accounts-many-coun | 220 / 0 | 508 / 232 | 508 / 232 | 483 / 229 | 16001 / 7888 | 15927 / 7843 | 15980 / 7888 | — |
| docs.stripe.com/changelog/2019-08-14/configuring-person | 213 / 0 | 501 / 232 | 501 / 232 | 476 / 229 | 15978 / 7881 | 15904 / 7836 | 15966 / 7890 | — |
| docs.stripe.com/changelog/2019-09-09/2019-09-09-1 | 201 / 0 | 489 / 232 | 489 / 232 | 464 / 229 | 15983 / 7893 | 15891 / 7830 | 15944 / 7875 | — |
| docs.stripe.com/changelog/2019-09-09/adds-detail-code-p | 154 / 0 | 442 / 232 | 421 / 232 | 417 / 229 | 15846 / 7872 | 15772 / 7827 | 15825 / 7872 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/affirm-tran | 250 / 0 | 437 / 132 | 437 / 132 | 413 / 129 | 16553 / 8376 | 16457 / 8313 | 16523 / 8367 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/billing-ale | 219 / 0 | 408 / 132 | 408 / 132 | 382 / 129 | 16502 / 8359 | 16422 / 8314 | 16508 / 8386 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/billing-ale | 224 / 0 | 413 / 132 | 413 / 132 | 387 / 129 | 16538 / 8378 | 16449 / 8324 | 16499 / 8360 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/billing-ale | 245 / 0 | 434 / 132 | 434 / 132 | 408 / 129 | 16469 / 8308 | 16398 / 8272 | 16457 / 8317 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/billing-due | 199 / 0 | 386 / 132 | 386 / 132 | 362 / 129 | 16437 / 8381 | 16350 / 8327 | 16425 / 8390 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/billing-mut | 198 / 0 | 385 / 132 | 385 / 132 | 361 / 129 | 16578 / 8525 | 16482 / 8462 | 16548 / 8516 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/checkout-up | 174 / 0 | 356 / 132 | 335 / 132 | 337 / 129 | 16456 / 8488 | 16373 / 8434 | 16426 / 8479 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/disputes-ca | 190 / 0 | 375 / 132 | 375 / 132 | 353 / 129 | 16684 / 8674 | 16599 / 8620 | 16675 / 8665 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/identity-ve | 217 / 0 | 402 / 132 | 402 / 132 | 380 / 129 | 16743 / 8681 | 16649 / 8618 | 16713 / 8672 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/issuing-add | 246 / 0 | 434 / 132 | 434 / 132 | 409 / 129 | 16963 / 8833 | 16856 / 8761 | 16933 / 8824 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/issuing-web | 258 / 0 | 447 / 132 | 447 / 132 | 421 / 129 | 16987 / 8824 | 16889 / 8761 | 16975 / 8833 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/support-cus | 280 / 0 | 469 / 132 | 469 / 132 | 443 / 129 | 17062 / 8829 | 16973 / 8775 | 17041 / 8829 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/support-pay | 191 / 0 | 376 / 132 | 376 / 132 | 354 / 129 | 16699 / 8674 | 16605 / 8611 | 16669 / 8665 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/tax-registr | 262 / 0 | 451 / 132 | 451 / 132 | 425 / 129 | 17036 / 8819 | 16947 / 8765 | 17024 / 8828 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/terminal-of | 235 / 0 | 421 / 132 | 421 / 132 | 398 / 129 | 16633 / 8515 | 16564 / 8479 | 16612 / 8515 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/terminal-re | 198 / 0 | 385 / 132 | 385 / 132 | 361 / 129 | 16441 / 8380 | 16354 / 8326 | 16429 / 8389 | — |
| docs.stripe.com/changelog/acacia/2024-09-30/twint-suppo | 200 / 0 | 387 / 132 | 387 / 132 | 363 / 129 | 16412 / 8367 | 16316 / 8304 | 16400 / 8376 | — |
| docs.stripe.com/connect/supported-embedded-components/c | 129 / 6 | 388 / 201 | 367 / 201 | 355 / 198 | 9004 / 7945 | 8922 / 7900 | 8983 / 7945 | — |
| docs.stripe.com/connect/supported-embedded-components/c | 766 / 12 | 1026 / 121 | 1026 / 121 | 911 / 118 | 14279 / 11419 | 14103 / 11365 | 14224 / 11410 | — |
| docs.stripe.com/connect/supported-embedded-components/c | 1070 / 8 | 1343 / 121 | 1343 / 121 | 1219 / 118 | 15187 / 11401 | 15003 / 11347 | 15141 / 11401 | — |
| docs.stripe.com/connect/supported-embedded-components/c | 1139 / 15 | 1403 / 121 | 1403 / 121 | 1281 / 118 | 15386 / 11392 | 15222 / 11356 | 15383 / 11410 | — |
| docs.stripe.com/connect/use-accounts-as-customers | 1626 / 13 | 1832 / 137 | 1832 / 137 | 1781 / 134 | 16265 / 11133 | 16142 / 11088 | 16271 / 11160 | — |
| docs.stripe.com/context | 337 / 17 | 588 / 162 | 588 / 162 | 513 / 159 | 15908 / 7925 | 15775 / 7871 | 15887 / 7925 | — |
| docs.stripe.com/customer-management | 2258 / 59 | 2410 / 152 | 2410 / 152 | 2386 / 149 | 12850 / 7706 | 12775 / 7652 | 12829 / 7706 | — |
| docs.stripe.com/customer-management/activate-no-code-cu | 294 / 9 | 513 / 157 | 513 / 157 | 474 / 154 | 9161 / 7512 | 9063 / 7458 | 9140 / 7512 | — |
| docs.stripe.com/customer-management/cancellation-page | 412 / 11 | 637 / 159 | 637 / 159 | 591 / 156 | 9564 / 7683 | 9461 / 7629 | 9561 / 7701 | — |
| docs.stripe.com/customer-management/configure-portal | 1115 / 10 | 1357 / 155 | 1336 / 155 | 1291 / 152 | 11121 / 8086 | 11005 / 8041 | 11109 / 8095 | — |
| docs.stripe.com/customer-management/integrate-customer- | 1723 / 80 | 1927 / 159 | 1927 / 159 | 1837 / 156 | 17472 / 11238 | 17318 / 11175 | 17469 / 11256 | — |
| docs.stripe.com/customer-management/portal-deep-links | 803 / 9 | 1040 / 159 | 1040 / 159 | 984 / 156 | 16408 / 11101 | 16312 / 11047 | 16387 / 11101 | — |
| docs.stripe.com/error-codes | 5429 / 23 | 4618 / 161 | 4618 / 161 | 5600 / 158 | 24870 / 8051 | 24795 / 7997 | 24849 / 8051 | — |
| docs.stripe.com/error-handling | 3009 / 14 | 3354 / 164 | 3354 / 164 | 3192 / 161 | 51915 / 11199 | 51742 / 11136 | 51868 / 11181 | — |
| docs.stripe.com/error-low-level | 1769 / 14 | 2029 / 168 | 2029 / 168 | 1954 / 165 | 22147 / 11024 | 21994 / 10943 | 22108 / 11006 | — |
| docs.stripe.com/file-upload | 1219 / 16 | 1400 / 120 | 1400 / 120 | 1354 / 117 | 20875 / 10973 | 20753 / 10901 | 20854 / 10973 | — |
| docs.stripe.com/get-started/account | 256 / 9 | 446 / 142 | 446 / 142 | 423 / 139 | 8284 / 7317 | 8209 / 7263 | 8263 / 7317 | — |
| docs.stripe.com/get-started/account/activate | 799 / 13 | 1025 / 144 | 1004 / 144 | 978 / 141 | 10190 / 7983 | 10091 / 7929 | 10187 / 8001 | — |
| docs.stripe.com/get-started/account/add-funds | 1003 / 39 | 1214 / 146 | 1193 / 146 | 1141 / 143 | 10810 / 8283 | 10688 / 8238 | 10807 / 8301 | — |
| docs.stripe.com/get-started/account/checklist | 748 / 9 | 958 / 143 | 958 / 143 | 941 / 140 | 10291 / 7983 | 10216 / 7929 | 10270 / 7983 | — |
| docs.stripe.com/get-started/account/linked-external-acc | 1318 / 5 | 1563 / 144 | 1563 / 144 | 1488 / 141 | 10971 / 7811 | 10864 / 7775 | 10968 / 7829 | — |
| docs.stripe.com/get-started/account/multiple-accounts | 407 / 10 | 608 / 144 | 587 / 144 | 587 / 141 | 9202 / 7811 | 9127 / 7757 | 9181 / 7811 | — |
| docs.stripe.com/get-started/account/orgs | 400 / 8 | 637 / 159 | 637 / 159 | 605 / 156 | 9287 / 7855 | 9212 / 7801 | 9266 / 7855 | — |
| docs.stripe.com/get-started/account/orgs/build | 673 / 7 | 952 / 163 | 952 / 163 | 871 / 160 | 9827 / 7878 | 9678 / 7824 | 9806 / 7878 | — |
| docs.stripe.com/get-started/account/orgs/setup | 441 / 11 | 976 / 162 | 976 / 162 | 623 / 159 | 9888 / 7669 | 9480 / 7615 | 9885 / 7687 | — |
| docs.stripe.com/get-started/account/orgs/sharing/custom | 1400 / 25 | 1866 / 165 | 1866 / 165 | 1584 / 162 | 12001 / 8252 | 11652 / 8189 | 11904 / 8243 | — |
| docs.stripe.com/get-started/account/orgs/team | 1131 / 10 | 1416 / 165 | 1395 / 165 | 1321 / 162 | 10528 / 7698 | 10372 / 7653 | 10489 / 7680 | — |
| docs.stripe.com/get-started/account/statement-descripto | 1191 / 5 | 1439 / 143 | 1439 / 143 | 1364 / 140 | 14915 / 11053 | 14773 / 10990 | 14885 / 11044 | — |
| docs.stripe.com/get-started/account/teams | 472 / 9 | 691 / 146 | 691 / 146 | 655 / 143 | 9460 / 7831 | 9345 / 7759 | 9430 / 7822 | — |
| docs.stripe.com/get-started/account/teams/roles | 4610 / 21 | 4792 / 149 | 4792 / 149 | 4769 / 146 | 13437 / 8277 | 13362 / 8223 | 13416 / 8277 | — |
| docs.stripe.com/get-started/data-migrations/export-file | 6738 / 23 | 1990 / 140 | 1990 / 140 | 6886 / 137 | 16129 / 8168 | 15978 / 8114 | 16090 / 8150 | — |
| docs.stripe.com/get-started/data-migrations/map-payment | 283 / 34 | 455 / 128 | 455 / 128 | 408 / 125 | 9097 / 8077 | 9022 / 8041 | 9076 / 8077 | — |
| docs.stripe.com/get-started/data-migrations/pan-copy-se | 2587 / 9 | 2889 / 128 | 2889 / 128 | 2745 / 125 | 15156 / 7852 | 14968 / 7807 | 15144 / 7861 | — |
| docs.stripe.com/get-started/data-migrations/pan-export | 426 / 5 | 605 / 136 | 605 / 136 | 588 / 133 | 8975 / 7643 | 8900 / 7589 | 8954 / 7643 | — |
| docs.stripe.com/get-started/data-migrations/pan-import | 2580 / 29 | 2877 / 124 | 2877 / 124 | 2724 / 121 | 14759 / 8292 | 14567 / 8247 | 14747 / 8301 | — |
| docs.stripe.com/get-started/data-migrations/payment-met | 1570 / 17 | 1847 / 129 | 1847 / 129 | 1724 / 126 | 16484 / 7995 | 16316 / 7941 | 16463 / 7995 | — |
| docs.stripe.com/get-started/data-migrations/supplementa | 519 / 20 | 692 / 128 | 671 / 128 | 663 / 125 | 9351 / 7825 | 9246 / 7753 | 9321 / 7816 | — |
| docs.stripe.com/ips | 617 / 14 | 842 / 163 | 842 / 163 | 797 / 160 | 16098 / 7876 | 15979 / 7804 | 16059 / 7858 | — |
| docs.stripe.com/issuing/customer-support | 1669 / 10 | 1998 / 268 | 1998 / 268 | 1961 / 265 | 12479 / 8022 | 12393 / 7977 | 12485 / 8049 | — |
| docs.stripe.com/issuing/integration-guides | 123 / 13 | 431 / 267 | 410 / 267 | 408 / 264 | 8231 / 7420 | 8156 / 7366 | 8210 / 7420 | — |
| docs.stripe.com/issuing/integration-guides/b2b-payments | 790 / 7 | 1149 / 270 | 1149 / 270 | 1085 / 267 | 15354 / 10967 | 15241 / 10922 | 15324 / 10958 | — |
| docs.stripe.com/issuing/integration-guides/embedded-fin | 2398 / 12 | 2817 / 270 | 2817 / 270 | 2690 / 267 | 27685 / 11323 | 27488 / 11260 | 27664 / 11323 | — |
| docs.stripe.com/issuing/integration-guides/fleet | 1852 / 8 | 2275 / 269 | 2275 / 269 | 2146 / 266 | 24143 / 11186 | 23951 / 11132 | 24113 / 11177 | — |
| docs.stripe.com/issuing/onboarding-overview | 1092 / 4 | 1475 / 262 | 1475 / 262 | 1381 / 259 | 12408 / 7883 | 12260 / 7829 | 12387 / 7883 | — |
| docs.stripe.com/issuing/sample-app | 515 / 26 | 910 / 262 | 910 / 262 | 789 / 259 | 11976 / 8100 | 11812 / 8046 | 11955 / 8100 | — |
| docs.stripe.com/keys | 3569 / 16 | 3906 / 168 | 3906 / 168 | 3779 / 165 | 26073 / 11248 | 25833 / 11194 | 26079 / 11275 | — |
| docs.stripe.com/keys-best-practices | 1189 / 15 | 1515 / 173 | 1515 / 173 | 1380 / 170 | 20838 / 10852 | 20651 / 10798 | 20817 / 10852 | — |
| docs.stripe.com/keys/restricted-api-keys | 1704 / 14 | 2154 / 172 | 2133 / 172 | 1909 / 169 | 18912 / 7936 | 18603 / 7882 | 18909 / 7954 | — |
| docs.stripe.com/metadata | 1593 / 15 | 1887 / 162 | 1887 / 162 | 1771 / 159 | 24044 / 11205 | 23863 / 11142 | 24005 / 11187 | — |
| docs.stripe.com/metadata/use-cases | 2122 / 15 | 2423 / 165 | 2423 / 165 | 2303 / 162 | 29287 / 11010 | 29127 / 10974 | 29266 / 11010 | — |
| docs.stripe.com/money-management | 181 / 23 | 277 / 64 | 277 / 64 | 253 / 61 | 7973 / 7077 | 7898 / 7023 | 7952 / 7077 | — |
| docs.stripe.com/payment-authentication/writing-queries | 624 / 14 | 845 / 169 | 845 / 169 | 810 / 166 | 11052 / 8089 | 10959 / 8035 | 11040 / 8098 | — |
| docs.stripe.com/payments/checkout/pricing-table | 2244 / 19 | 2656 / 218 | 2656 / 218 | 2483 / 215 | 18011 / 11340 | 17797 / 11295 | 17972 / 11322 | — |
| docs.stripe.com/products | 20 / 20 | 243 / 100 | 243 / 100 | 219 / 97 | 7849 / 7213 | 7774 / 7159 | 7828 / 7213 | — |
| docs.stripe.com/products-prices/manage-prices | 3915 / 21 | 4169 / 139 | 4169 / 139 | 4073 / 136 | 28420 / 10821 | 28225 / 10767 | 28390 / 10812 | — |
| docs.stripe.com/products-prices/overview | 133 / 19 | 306 / 134 | 306 / 134 | 283 / 131 | 8020 / 7275 | 7945 / 7221 | 7999 / 7275 | — |
| docs.stripe.com/products-prices/pricing-models | 262 / 17 | 544 / 241 | 544 / 241 | 527 / 238 | 9560 / 8014 | 9485 / 7960 | 9539 / 8014 | — |
| docs.stripe.com/rate-limits | 1647 / 14 | 1891 / 161 | 1870 / 161 | 1825 / 158 | 21539 / 10847 | 21399 / 10775 | 21518 / 10847 | — |
| docs.stripe.com/saas | 978 / 19 | 1127 / 36 | 1127 / 36 | 1032 / 33 | 23789 / 7905 | 23656 / 7851 | 23795 / 7932 | — |
| docs.stripe.com/subscriptions/pricing-models/flat-rate- | 316 / 8 | 608 / 243 | 608 / 243 | 582 / 240 | 11033 / 7836 | 10958 / 7782 | 11012 / 7836 | — |
| docs.stripe.com/subscriptions/pricing-models/per-seat-p | 323 / 7 | 609 / 242 | 609 / 242 | 589 / 239 | 10651 / 7834 | 10576 / 7780 | 10630 / 7834 | — |
| docs.stripe.com/subscriptions/pricing-models/tiered-pri | 1111 / 7 | 1418 / 242 | 1418 / 242 | 1379 / 239 | 12664 / 8010 | 12573 / 7956 | 12634 / 8001 | — |
| docs.stripe.com/upgrades | 7660 / 17 | 7884 / 122 | 7884 / 122 | 7811 / 119 | 30109 / 7926 | 29957 / 7863 | 30097 / 7935 | — |
| docs.stripe.com/upgrades/manage-payment-methods | 788 / 17 | 1041 / 197 | 1041 / 197 | 999 / 194 | 17424 / 10586 | 17324 / 10532 | 17403 / 10586 | — |

</details>

## blog-engineering

| Tool | Avg words [6] | Preamble [2] | Repeat rate [3] | Junk found [4] | Headings [7] | Code blocks [8] | Precision [5] | Recall [5] |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 667 | 36 | 0% | 1 | 14.3 | 0.4 | 100% | 33% |
| crawl4ai | 2301 | 697 ⚠ | 2% | 201 | 20.3 | 0.4 | 100% | 72% |
| crawl4ai-raw | 2301 | 697 ⚠ | 2% | 201 | 20.3 | 0.4 | 100% | 72% |
| scrapy+md | 659 | 8 | 0% | 1 | 14.3 | 0.4 | 100% | 33% |
| crawlee | 3576 | 1923 ⚠ | 3% | 228 | 20.3 | 0.4 | 100% | 98% |
| colly+md | 3048 | 1526 ⚠ | 4% | 141 | 20.3 | 0.3 | 99% | 93% |
| playwright | 3584 | 1930 ⚠ | 3% | 231 | 20.3 | 0.4 | 99% | 98% |
| firecrawl | — | — | — | — | — | — | — | — |

> **Column definitions:**
> **[6] Avg words** = mean words per page. **[2] Preamble** = avg words per page before the first heading (nav chrome). **[3] Repeat rate** = fraction of sentences on >50% of pages.
> **[4] Junk found** = total known boilerplate phrases detected across all pages. **[7] Headings** = avg headings per page. **[8] Code blocks** = avg fenced code blocks per page.
> **[5] Precision/Recall** = cross-tool consensus (pages with <2 sentences excluded). **⚠** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
**scrapy+md** produces the cleanest output with 8 words of preamble per page, while **playwright** injects 1930 words of nav chrome before content begins. The word count gap (659 vs 3584 avg words) is largely explained by preamble: 1930 words of nav chrome account for ~54% of playwright's output on this site. scrapy+md's lower recall (33% vs 98%) reflects stricter content filtering — the "missed" sentences are predominantly navigation, sponsor links, and footer text that other tools include as content. For RAG, this is typically a net positive: fewer junk tokens per chunk tends to improve embedding quality and retrieval precision.

<details>
<summary>Sample output — first 40 lines of <code>github.blog/news-insights/the-library/tasty-tidbits</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
*Chris Wanstrath of Err the Blog (hey that’s me!) just posted an article covering some tasty GitHub tidbits. Range highlighting, key shortcuts, keeping dotfiles in git, and the GitHub gem…*


[Home](https://github.blog/) / [News & insights](https://github.blog/news-insights/) / [The library](https://github.blog/news-insights/the-library/)

# Tasty Tidbits

Chris Wanstrath of Err the Blog (hey that’s me!) just posted an article covering some tasty GitHub tidbits. Range highlighting, key shortcuts, keeping dotfiles in git, and the GitHub gem…

[Chris Wanstrath](https://github.blog/author/defunkt/ "Posts by Chris Wanstrath")·[@defunkt](https://github.com/defunkt)

May 11, 2008
|

Updated January 4, 2019

* Share:

Chris Wanstrath of Err the Blog (hey that’s me!) just posted an article covering some [tasty GitHub tidbits](http://errtheblog.com/posts/89-huba-huba). Range highlighting, key shortcuts, keeping dotfiles in git, and the [GitHub gem](http://github.com/defunkt/github-gem) are covered.

Enjoy.

## Written by

### [Chris Wanstrath](https://github.blog/author/defunkt/)

[@defunkt](https://github.com/defunkt)

## Related posts

[Company news](https://github.blog/news-insights/company-news/)

### [GitHub availability report: March 2026](https://github.blog/news-insights/company-news/github-availability-report-march-2026/)

In March, we experienced four incidents that resulted in degraded performance across GitHub services.

[Company news](https://github.blog/news-insights/company-news/)

### [GitHub Universe is back: We want you to take the stage](https://github.blog/news-insights/company-news/github-universe-is-back-we-want-you-to-take-the-stage/)
```

**crawl4ai**
```
[ Skip to content ](https://github.blog/news-insights/the-library/tasty-tidbits/#start-of-content) [ Skip to sidebar ](https://github.blog/news-insights/the-library/tasty-tidbits/#sidebar)
[ ](https://github.com) / [ Blog](https://github.blog/)
  * [Changelog](https://github.blog/changelog/)
  * [Docs](https://docs.github.com/)
  * [Customer stories](https://github.com/customer-stories)


[ Try GitHub Copilot  ](https://github.com/features/copilot?utm_source=blog-tap-nav&utm_medium=blog&utm_campaign=universe25) [ See what's new  ](https://github.com/events/universe/recap?utm_source=k2k-blog-tap-nav&utm_medium=blog&utm_campaign=universe25)
  * [AI & ML](https://github.blog/ai-and-ml/)
    * [AI & ML](https://github.blog/ai-and-ml/)
Learn about artificial intelligence and machine learning across the GitHub ecosystem and the wider industry.
      * [Generative AI](https://github.blog/ai-and-ml/generative-ai/)
Learn how to build with generative AI.
      * [GitHub Copilot](https://github.blog/ai-and-ml/github-copilot/)
Change how you work with GitHub Copilot.
      * [LLMs](https://github.blog/ai-and-ml/llms/)
Everything developers need to know about LLMs.
      * [Machine learning](https://github.blog/ai-and-ml/machine-learning/)
Machine learning tips, tricks, and best practices.
    * ![](https://github.blog/wp-content/uploads/2024/06/AI-DarkMode-4.png?resize=800%2C425)
[How AI code generation works](https://github.blog/ai-and-ml/generative-ai/how-ai-code-generation-works/)
Explore the capabilities and benefits of AI code generation and how it can improve your developer experience.
Learn more
  * [Developer skills](https://github.blog/developer-skills/)
    * [Developer skills](https://github.blog/developer-skills/)
Resources for developers to grow in their skills and careers.
      * [Application development](https://github.blog/developer-skills/application-development/)
Insights and best practices for building apps.
      * [Career growth](https://github.blog/developer-skills/career-growth/)
Tips & tricks to grow as a professional developer.
      * [GitHub](https://github.blog/developer-skills/github/)
Improve how you use GitHub at work.
      * [GitHub Education](https://github.blog/developer-skills/github-education/)
Learn how to move into your first professional role.
      * [Programming languages & frameworks](https://github.blog/developer-skills/programming-languages-and-frameworks/)
Stay current on what’s new (or new again).
    * ![](https://github.blog/wp-content/uploads/2024/05/Enterprise-DarkMode-3.png?resize=800%2C425)
[Get started with GitHub documentation](https://docs.github.com/en/get-started)
Learn how to start building, shipping, and maintaining software with GitHub.
Learn more
```

**crawl4ai-raw**
```
[ Skip to content ](https://github.blog/news-insights/the-library/tasty-tidbits/#start-of-content) [ Skip to sidebar ](https://github.blog/news-insights/the-library/tasty-tidbits/#sidebar)
[ ](https://github.com) / [ Blog](https://github.blog/)
  * [Changelog](https://github.blog/changelog/)
  * [Docs](https://docs.github.com/)
  * [Customer stories](https://github.com/customer-stories)


[ Try GitHub Copilot  ](https://github.com/features/copilot?utm_source=blog-tap-nav&utm_medium=blog&utm_campaign=universe25) [ See what's new  ](https://github.com/events/universe/recap?utm_source=k2k-blog-tap-nav&utm_medium=blog&utm_campaign=universe25)
  * [AI & ML](https://github.blog/ai-and-ml/)
    * [AI & ML](https://github.blog/ai-and-ml/)
Learn about artificial intelligence and machine learning across the GitHub ecosystem and the wider industry.
      * [Generative AI](https://github.blog/ai-and-ml/generative-ai/)
Learn how to build with generative AI.
      * [GitHub Copilot](https://github.blog/ai-and-ml/github-copilot/)
Change how you work with GitHub Copilot.
      * [LLMs](https://github.blog/ai-and-ml/llms/)
Everything developers need to know about LLMs.
      * [Machine learning](https://github.blog/ai-and-ml/machine-learning/)
Machine learning tips, tricks, and best practices.
    * ![](https://github.blog/wp-content/uploads/2024/06/AI-DarkMode-4.png?resize=800%2C425)
[How AI code generation works](https://github.blog/ai-and-ml/generative-ai/how-ai-code-generation-works/)
Explore the capabilities and benefits of AI code generation and how it can improve your developer experience.
Learn more
  * [Developer skills](https://github.blog/developer-skills/)
    * [Developer skills](https://github.blog/developer-skills/)
Resources for developers to grow in their skills and careers.
      * [Application development](https://github.blog/developer-skills/application-development/)
Insights and best practices for building apps.
      * [Career growth](https://github.blog/developer-skills/career-growth/)
Tips & tricks to grow as a professional developer.
      * [GitHub](https://github.blog/developer-skills/github/)
Improve how you use GitHub at work.
      * [GitHub Education](https://github.blog/developer-skills/github-education/)
Learn how to move into your first professional role.
      * [Programming languages & frameworks](https://github.blog/developer-skills/programming-languages-and-frameworks/)
Stay current on what’s new (or new again).
    * ![](https://github.blog/wp-content/uploads/2024/05/Enterprise-DarkMode-3.png?resize=800%2C425)
[Get started with GitHub documentation](https://docs.github.com/en/get-started)
Learn how to start building, shipping, and maintaining software with GitHub.
Learn more
```

**scrapy+md**
```
[Home](https://github.blog/) / [News & insights](https://github.blog/news-insights/) / [The library](https://github.blog/news-insights/the-library/)

# Tasty Tidbits

Chris Wanstrath of Err the Blog (hey that’s me!) just posted an article covering some tasty GitHub tidbits. Range highlighting, key shortcuts, keeping dotfiles in git, and the GitHub gem…

[Chris Wanstrath](https://github.blog/author/defunkt/ "Posts by Chris Wanstrath")·[@defunkt](https://github.com/defunkt)

May 11, 2008 
|

Updated January 4, 2019

* Share:

Chris Wanstrath of Err the Blog (hey that’s me!) just posted an article covering some [tasty GitHub tidbits](http://errtheblog.com/posts/89-huba-huba). Range highlighting, key shortcuts, keeping dotfiles in git, and the [GitHub gem](http://github.com/defunkt/github-gem) are covered.

Enjoy.

## Written by

### [Chris Wanstrath](https://github.blog/author/defunkt/)

[@defunkt](https://github.com/defunkt)

## Related posts

[Company news](https://github.blog/news-insights/company-news/)

### [GitHub availability report: March 2026](https://github.blog/news-insights/company-news/github-availability-report-march-2026/)

In March, we experienced four incidents that resulted in degraded performance across GitHub services.

[Jakub Oleksy](https://github.blog/author/jakuboleksy/ "Posts by Jakub Oleksy")

[Company news](https://github.blog/news-insights/company-news/)

### [GitHub Universe is back: We want you to take the stage](https://github.blog/news-insights/company-news/github-universe-is-back-we-want-you-to-take-the-stage/)

Get inspired by five of the most memorable, magical, and quirky Universe sessions to date.
```

**crawlee**
```
Tasty Tidbits - The GitHub Blog













{"@context":"https:\/\/schema.org","headline":"Tasty Tidbits","author":{"@type":"Person","name":"Chris Wanstrath"},"datePublished":"2008-05-11T04:22:37-07:00","abstract":"Chris Wanstrath of Err the Blog (hey that&#8217;s me!) just posted an article covering some tasty GitHub tidbits. Range highlighting, key shortcuts, keeping dotfiles in git, and the GitHub gem&hellip;","mainEntityOfPage":{"@type":"WebPage","@id":"https:\/\/github.blog\/news-insights\/the-library\/tasty-tidbits\/"},"@type":"TechArticle"}
{"@context":"https:\/\/schema.org","headline":"Tasty Tidbits","author":{"@type":"Person","name":"Chris Wanstrath"},"datePublished":"2008-05-11T04:22:37-07:00","abstract":"Chris Wanstrath of Err the Blog (hey that&#8217;s me!) just posted an article covering some tasty GitHub tidbits. Range highlighting, key shortcuts, keeping dotfiles in git, and the GitHub gem&hellip;","mainEntityOfPage":{"@type":"WebPage","@id":"https:\/\/github.blog\/news-insights\/the-library\/tasty-tidbits\/"},"@type":"BlogPosting"}
{"@context":"https:\/\/schema.org","@graph":[{"@type":"Article","@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/#article","isPartOf":{"@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/"},"author":[{"@id":"https:\/\/github.blog\/#\/schema\/person\/159f1a6ddb285af554ae75915884730d"}],"headline":"Tasty Tidbits","datePublished":"2008-05-11T11:22:37+00:00","dateModified":"2019-01-04T16:41:06+00:00","mainEntityOfPage":{"@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/"},"wordCount":36,"articleSection":["News &amp; insights","The library"],"inLanguage":"en-US"},{"@type":"WebPage","@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/","url":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/","name":"Tasty Tidbits - The GitHub Blog","isPartOf":{"@id":"https:\/\/github.blog\/#website"},"datePublished":"2008-05-11T11:22:37+00:00","dateModified":"2019-01-04T16:41:06+00:00","author":{"@id":"https:\/\/github.blog\/#\/schema\/person\/159f1a6ddb285af554ae75915884730d"},"breadcrumb":{"@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/#breadcrumb"},"inLanguage":"en-US","potentialAction":[{"@type":"ReadAction","target":["https:\/\/github.blog\/news-insights\/tasty-tidbits\/"]}]},{"@type":"BreadcrumbList","@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https:\/\/github.blog\/"},{"@type":"ListItem","position":2,"name":"News &amp; insights","item":"https:\/\/github.blog\/news-insights\/"},{"@type":"ListItem","position":3,"name":"The library","item":"https:\/\/github.blog\/news-insights\/the-library\/"},{"@type":"ListItem","position":4,"name":"Tasty Tidbits"}]},{"@type":"WebSite","@id":"https:\/\/github.blog\/#website","url":"https:\/\/github.blog\/","name":"The GitHub Blog","description":"Updates, ideas, and inspiration from GitHub to help developers build and design software.","potentialAction":[{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":"https:\/\/github.blog\/?s={search\_term\_string}"},"query-input":{"@type":"PropertyValueSpecification","valueRequired":true,"valueName":"search\_term\_string"}}],"inLanguage":"en-US"},{"@type":"Person","@id":"https:\/\/github.blog\/#\/schema\/person\/159f1a6ddb285af554ae75915884730d","name":"Chris Wanstrath","image":{"@type":"ImageObject","inLanguage":"en-US","@id":"https:\/\/secure.gravatar.com\/avatar\/33666dec44de96b88e8c117b8c17efe29a62dacd06c4abf72cf969a74775381a?s=96&d=mm&r=g289c11bc82a60609a31604c4517156a7","url":"https:\/\/secure.gravatar.com\/avatar\/33666dec44de96b88e8c117b8c17efe29a62dacd06c4abf72cf969a74775381a?s=96&d=mm&r=g","contentUrl":"https:\/\/secure.gravatar.com\/avatar\/33666dec44de96b88e8c117b8c17efe29a62dacd06c4abf72cf969a74775381a?s=96&d=mm&r=g","caption":"Chris Wanstrath"},"sameAs":["http:\/\/chriswanstrath.com\/"],"url":"https:\/\/github.blog\/author\/defunkt\/"}]}












img:is([sizes=auto i],[sizes^="auto," i]){contain-intrinsic-size:3000px 1500px}
/\*# sourceURL=wp-img-auto-sizes-contain-inline-css \*/

img.wp-smiley, img.emoji {
display: inline !important;
border: none !important;
box-shadow: none !important;
height: 1em !important;
width: 1em !important;
margin: 0 0.07em !important;
vertical-align: -0.1em !important;
```

**colly+md**
```
Tasty Tidbits - The GitHub Blog













{"@context":"https:\/\/schema.org","headline":"Tasty Tidbits","author":{"@type":"Person","name":"Chris Wanstrath"},"datePublished":"2008-05-11T04:22:37-07:00","abstract":"Chris Wanstrath of Err the Blog (hey that&#8217;s me!) just posted an article covering some tasty GitHub tidbits. Range highlighting, key shortcuts, keeping dotfiles in git, and the GitHub gem&hellip;","mainEntityOfPage":{"@type":"WebPage","@id":"https:\/\/github.blog\/news-insights\/the-library\/tasty-tidbits\/"},"@type":"TechArticle"}
{"@context":"https:\/\/schema.org","headline":"Tasty Tidbits","author":{"@type":"Person","name":"Chris Wanstrath"},"datePublished":"2008-05-11T04:22:37-07:00","abstract":"Chris Wanstrath of Err the Blog (hey that&#8217;s me!) just posted an article covering some tasty GitHub tidbits. Range highlighting, key shortcuts, keeping dotfiles in git, and the GitHub gem&hellip;","mainEntityOfPage":{"@type":"WebPage","@id":"https:\/\/github.blog\/news-insights\/the-library\/tasty-tidbits\/"},"@type":"BlogPosting"}
{"@context":"https:\/\/schema.org","@graph":[{"@type":"Article","@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/#article","isPartOf":{"@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/"},"author":[{"@id":"https:\/\/github.blog\/#\/schema\/person\/159f1a6ddb285af554ae75915884730d"}],"headline":"Tasty Tidbits","datePublished":"2008-05-11T11:22:37+00:00","dateModified":"2019-01-04T16:41:06+00:00","mainEntityOfPage":{"@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/"},"wordCount":36,"articleSection":["News &amp; insights","The library"],"inLanguage":"en-US"},{"@type":"WebPage","@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/","url":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/","name":"Tasty Tidbits - The GitHub Blog","isPartOf":{"@id":"https:\/\/github.blog\/#website"},"datePublished":"2008-05-11T11:22:37+00:00","dateModified":"2019-01-04T16:41:06+00:00","author":{"@id":"https:\/\/github.blog\/#\/schema\/person\/159f1a6ddb285af554ae75915884730d"},"breadcrumb":{"@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/#breadcrumb"},"inLanguage":"en-US","potentialAction":[{"@type":"ReadAction","target":["https:\/\/github.blog\/news-insights\/tasty-tidbits\/"]}]},{"@type":"BreadcrumbList","@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https:\/\/github.blog\/"},{"@type":"ListItem","position":2,"name":"News &amp; insights","item":"https:\/\/github.blog\/news-insights\/"},{"@type":"ListItem","position":3,"name":"The library","item":"https:\/\/github.blog\/news-insights\/the-library\/"},{"@type":"ListItem","position":4,"name":"Tasty Tidbits"}]},{"@type":"WebSite","@id":"https:\/\/github.blog\/#website","url":"https:\/\/github.blog\/","name":"The GitHub Blog","description":"Updates, ideas, and inspiration from GitHub to help developers build and design software.","potentialAction":[{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":"https:\/\/github.blog\/?s={search\_term\_string}"},"query-input":{"@type":"PropertyValueSpecification","valueRequired":true,"valueName":"search\_term\_string"}}],"inLanguage":"en-US"},{"@type":"Person","@id":"https:\/\/github.blog\/#\/schema\/person\/159f1a6ddb285af554ae75915884730d","name":"Chris Wanstrath","image":{"@type":"ImageObject","inLanguage":"en-US","@id":"https:\/\/secure.gravatar.com\/avatar\/33666dec44de96b88e8c117b8c17efe29a62dacd06c4abf72cf969a74775381a?s=96&d=mm&r=g289c11bc82a60609a31604c4517156a7","url":"https:\/\/secure.gravatar.com\/avatar\/33666dec44de96b88e8c117b8c17efe29a62dacd06c4abf72cf969a74775381a?s=96&d=mm&r=g","contentUrl":"https:\/\/secure.gravatar.com\/avatar\/33666dec44de96b88e8c117b8c17efe29a62dacd06c4abf72cf969a74775381a?s=96&d=mm&r=g","caption":"Chris Wanstrath"},"sameAs":["http:\/\/chriswanstrath.com\/"],"url":"https:\/\/github.blog\/author\/defunkt\/"}]}












img:is([sizes=auto i],[sizes^="auto," i]){contain-intrinsic-size:3000px 1500px}
/\*# sourceURL=wp-img-auto-sizes-contain-inline-css \*/

img.wp-smiley, img.emoji {
display: inline !important;
border: none !important;
box-shadow: none !important;
height: 1em !important;
width: 1em !important;
margin: 0 0.07em !important;
vertical-align: -0.1em !important;
```

**playwright**
```
Tasty Tidbits - The GitHub Blog













{"@context":"https:\/\/schema.org","headline":"Tasty Tidbits","author":{"@type":"Person","name":"Chris Wanstrath"},"datePublished":"2008-05-11T04:22:37-07:00","abstract":"Chris Wanstrath of Err the Blog (hey that&#8217;s me!) just posted an article covering some tasty GitHub tidbits. Range highlighting, key shortcuts, keeping dotfiles in git, and the GitHub gem&hellip;","mainEntityOfPage":{"@type":"WebPage","@id":"https:\/\/github.blog\/news-insights\/the-library\/tasty-tidbits\/"},"@type":"TechArticle"}
{"@context":"https:\/\/schema.org","headline":"Tasty Tidbits","author":{"@type":"Person","name":"Chris Wanstrath"},"datePublished":"2008-05-11T04:22:37-07:00","abstract":"Chris Wanstrath of Err the Blog (hey that&#8217;s me!) just posted an article covering some tasty GitHub tidbits. Range highlighting, key shortcuts, keeping dotfiles in git, and the GitHub gem&hellip;","mainEntityOfPage":{"@type":"WebPage","@id":"https:\/\/github.blog\/news-insights\/the-library\/tasty-tidbits\/"},"@type":"BlogPosting"}
{"@context":"https:\/\/schema.org","@graph":[{"@type":"Article","@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/#article","isPartOf":{"@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/"},"author":[{"@id":"https:\/\/github.blog\/#\/schema\/person\/159f1a6ddb285af554ae75915884730d"}],"headline":"Tasty Tidbits","datePublished":"2008-05-11T11:22:37+00:00","dateModified":"2019-01-04T16:41:06+00:00","mainEntityOfPage":{"@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/"},"wordCount":36,"articleSection":["News &amp; insights","The library"],"inLanguage":"en-US"},{"@type":"WebPage","@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/","url":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/","name":"Tasty Tidbits - The GitHub Blog","isPartOf":{"@id":"https:\/\/github.blog\/#website"},"datePublished":"2008-05-11T11:22:37+00:00","dateModified":"2019-01-04T16:41:06+00:00","author":{"@id":"https:\/\/github.blog\/#\/schema\/person\/159f1a6ddb285af554ae75915884730d"},"breadcrumb":{"@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/#breadcrumb"},"inLanguage":"en-US","potentialAction":[{"@type":"ReadAction","target":["https:\/\/github.blog\/news-insights\/tasty-tidbits\/"]}]},{"@type":"BreadcrumbList","@id":"https:\/\/github.blog\/news-insights\/tasty-tidbits\/#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https:\/\/github.blog\/"},{"@type":"ListItem","position":2,"name":"News &amp; insights","item":"https:\/\/github.blog\/news-insights\/"},{"@type":"ListItem","position":3,"name":"The library","item":"https:\/\/github.blog\/news-insights\/the-library\/"},{"@type":"ListItem","position":4,"name":"Tasty Tidbits"}]},{"@type":"WebSite","@id":"https:\/\/github.blog\/#website","url":"https:\/\/github.blog\/","name":"The GitHub Blog","description":"Updates, ideas, and inspiration from GitHub to help developers build and design software.","potentialAction":[{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":"https:\/\/github.blog\/?s={search\_term\_string}"},"query-input":{"@type":"PropertyValueSpecification","valueRequired":true,"valueName":"search\_term\_string"}}],"inLanguage":"en-US"},{"@type":"Person","@id":"https:\/\/github.blog\/#\/schema\/person\/159f1a6ddb285af554ae75915884730d","name":"Chris Wanstrath","image":{"@type":"ImageObject","inLanguage":"en-US","@id":"https:\/\/secure.gravatar.com\/avatar\/33666dec44de96b88e8c117b8c17efe29a62dacd06c4abf72cf969a74775381a?s=96&d=mm&r=g289c11bc82a60609a31604c4517156a7","url":"https:\/\/secure.gravatar.com\/avatar\/33666dec44de96b88e8c117b8c17efe29a62dacd06c4abf72cf969a74775381a?s=96&d=mm&r=g","contentUrl":"https:\/\/secure.gravatar.com\/avatar\/33666dec44de96b88e8c117b8c17efe29a62dacd06c4abf72cf969a74775381a?s=96&d=mm&r=g","caption":"Chris Wanstrath"},"sameAs":["http:\/\/chriswanstrath.com\/"],"url":"https:\/\/github.blog\/author\/defunkt\/"}]}












img:is([sizes=auto i],[sizes^="auto," i]){contain-intrinsic-size:3000px 1500px}
/\*# sourceURL=wp-img-auto-sizes-contain-inline-css \*/

img.wp-smiley, img.emoji {
display: inline !important;
border: none !important;
box-shadow: none !important;
height: 1em !important;
width: 1em !important;
margin: 0 0.07em !important;
vertical-align: -0.1em !important;
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [2]</summary>

| URL | markcrawl words [6] / preamble [2] | crawl4ai words [6] / preamble [2] | crawl4ai-raw words [6] / preamble [2] | scrapy+md words [6] / preamble [2] | crawlee words [6] / preamble [2] | colly+md words [6] / preamble [2] | playwright words [6] / preamble [2] | firecrawl words [6] / preamble [2] |
|---|---|---|---|---|---|---|---|---|
| github.blog/engineering/architecture-optimization/intro | 2215 / 37 | 3900 / 697 | 3900 / 697 | 2211 / 7 | 5052 / 1847 | 4563 / 1449 | 5052 / 1847 | — |
| github.blog/engineering/engineering-principles/move-fas | 4027 / 36 | 5717 / 697 | 5717 / 697 | 4023 / 6 | 7390 / 2372 | — | 6882 / 1865 | — |
| github.blog/engineering/engineering-principles/scripts- | 777 / 36 | 2445 / 697 | 2445 / 697 | 773 / 6 | 3628 / 1861 | 3139 / 1463 | 4136 / 2368 | — |
| github.blog/engineering/infrastructure/building-resilie | 3235 / 35 | 4913 / 697 | 4913 / 697 | 3231 / 5 | 6080 / 1855 | 5591 / 1457 | 6080 / 1855 | — |
| github.blog/engineering/infrastructure/context-aware-my | 2584 / 35 | 4260 / 697 | 4260 / 697 | 2580 / 5 | 5439 / 1865 | — | 5439 / 1865 | — |
| github.blog/engineering/infrastructure/evolution-of-our | 1487 / 35 | 3159 / 697 | 3159 / 697 | 1483 / 5 | 4337 / 1860 | 4356 / 1969 | 4337 / 1860 | — |
| github.blog/engineering/infrastructure/githubs-metal-cl | 1727 / 35 | 3407 / 697 | 3407 / 697 | 1723 / 5 | 4593 / 1876 | 4104 / 1478 | 4593 / 1876 | — |
| github.blog/engineering/infrastructure/glb-director-ope | 3858 / 35 | 5601 / 697 | 5601 / 697 | 3854 / 5 | 7221 / 2372 | 6224 / 1467 | 6713 / 1865 | — |
| github.blog/engineering/infrastructure/kubernetes-at-gi | 3034 / 35 | 4735 / 697 | 4735 / 697 | 3030 / 5 | 5874 / 1850 | — | 6382 / 2357 | — |
| github.blog/engineering/infrastructure/orchestrator-git | 2752 / 35 | 4436 / 697 | 4436 / 697 | 2748 / 5 | 5590 / 1848 | — | 5590 / 1848 | — |
| github.blog/engineering/infrastructure/transit-and-peer | 1508 / 35 | 3185 / 697 | 3185 / 697 | 1504 / 5 | 4381 / 1883 | — | 4381 / 1883 | — |
| github.blog/engineering/platform-security/soft-u2f | 675 / 36 | 2346 / 697 | 2346 / 697 | 671 / 6 | 3508 / 1843 | 3019 / 1445 | 3508 / 1843 | — |
| github.blog/engineering/platform-security/syn-flood-mit | 1876 / 36 | 3558 / 697 | 3558 / 697 | 1872 / 6 | 4729 / 1863 | 4240 / 1465 | 5237 / 2370 | — |
| github.blog/engineering/user-experience/like-injection | 1054 / 36 | 2721 / 697 | 2721 / 697 | 1050 / 6 | 3887 / 1843 | — | 3887 / 1843 | — |
| github.blog/engineering/user-experience/topics | 2946 / 36 | 4620 / 697 | 4620 / 697 | 2943 / 6 | 5804 / 1867 | 5315 / 1469 | 6312 / 2374 | — |
| github.blog/latest | 808 / 16 | 2942 / 692 | 2942 / 692 | 1039 / 3 | 4325 / 2295 | 3329 / 1390 | 3817 / 1788 | — |
| github.blog/news-insights/company-news/ddos-incident-re | 991 / 38 | 2629 / 697 | 2629 / 697 | 980 / 8 | 3839 / 1865 | — | 3839 / 1865 | — |
| github.blog/news-insights/company-news/gh-ost-github-s- | 3138 / 38 | 4761 / 697 | 4761 / 697 | 3127 / 8 | 6006 / 1885 | — | 6006 / 1885 | — |
| github.blog/news-insights/company-news/sha-1-collision- | 1193 / 38 | 2815 / 697 | 2815 / 697 | 1182 / 8 | 4041 / 1865 | — | 4549 / 2372 | — |
| github.blog/news-insights/policy-news-and-insights/work | 670 / 37 | 2292 / 697 | 2292 / 697 | 659 / 7 | 3531 / 1878 | 3042 / 1480 | 3531 / 1878 | — |
| github.blog/news-insights/product-news/recover-accounts | 1274 / 37 | 2903 / 697 | 2903 / 697 | 1263 / 7 | 4132 / 1875 | 3643 / 1477 | 4640 / 2382 | — |
| github.blog/news-insights/the-library/a-few-words-on-th | 578 / 38 | 2200 / 697 | 2200 / 697 | 567 / 8 | 3438 / 1877 | — | 3438 / 1877 | — |
| github.blog/news-insights/the-library/a-note-on-the-rec | 869 / 38 | 2491 / 697 | 2491 / 697 | 858 / 8 | 3723 / 1871 | 3234 / 1473 | 3723 / 1871 | — |
| github.blog/news-insights/the-library/adhearsion-moves- | 396 / 38 | 2020 / 697 | 2020 / 697 | 385 / 8 | 3238 / 1859 | 2749 / 1461 | 3238 / 1859 | — |
| github.blog/news-insights/the-library/annotated-downloa | 500 / 38 | 2122 / 697 | 2122 / 697 | 489 / 8 | 3330 / 1847 | 2841 / 1449 | 3330 / 1847 | — |
| github.blog/news-insights/the-library/announcing-ernie- | 1160 / 38 | 2782 / 697 | 2782 / 697 | 1149 / 8 | 4008 / 1865 | 3519 / 1467 | 4008 / 1865 | — |
| github.blog/news-insights/the-library/api-forum-grand-o | 361 / 38 | 1985 / 697 | 1985 / 697 | 350 / 8 | 3203 / 1859 | 2714 / 1461 | 3203 / 1859 | — |
| github.blog/news-insights/the-library/basic-auth-post-r | 322 / 27 | 1957 / 697 | 1957 / 697 | 322 / 8 | 3147 / 1831 | 2658 / 1433 | 3147 / 1831 | — |
| github.blog/news-insights/the-library/benchmarking-gith | 1973 / 38 | 3660 / 697 | 3660 / 697 | 1962 / 8 | 4809 / 1853 | 4320 / 1455 | 4809 / 1853 | — |
| github.blog/news-insights/the-library/branch-lists | 777 / 38 | 2399 / 697 | 2399 / 697 | 766 / 8 | 3607 / 1847 | — | 3607 / 1847 | — |
| github.blog/news-insights/the-library/brubeck | 1696 / 38 | 3327 / 697 | 3327 / 697 | 1685 / 8 | 4550 / 1871 | 4061 / 1473 | 4550 / 1871 | — |
| github.blog/news-insights/the-library/cheat-git-chit | 426 / 38 | 2050 / 697 | 2050 / 697 | 415 / 8 | 3274 / 1865 | 2785 / 1467 | 3274 / 1865 | — |
| github.blog/news-insights/the-library/check-your-usage | 369 / 38 | 1993 / 697 | 1993 / 697 | 358 / 8 | 3205 / 1853 | 2716 / 1455 | 3205 / 1853 | — |
| github.blog/news-insights/the-library/cleaning-house | 407 / 38 | 2031 / 697 | 2031 / 697 | 396 / 8 | 3237 / 1847 | 2748 / 1449 | 3237 / 1847 | — |
| github.blog/news-insights/the-library/closing-issues-wi | 364 / 38 | 1988 / 697 | 1988 / 697 | 353 / 8 | 3206 / 1859 | 2717 / 1461 | 3206 / 1859 | — |
| github.blog/news-insights/the-library/code-in-the-open | 402 / 38 | 2026 / 697 | 2026 / 697 | 391 / 8 | 3244 / 1859 | — | 3244 / 1859 | — |
| github.blog/news-insights/the-library/code-search-on-va | 329 / 29 | 1962 / 697 | 1962 / 697 | 327 / 8 | 3162 / 1841 | — | 3670 / 2348 | — |
| github.blog/news-insights/the-library/committing-like-c | 431 / 38 | 2053 / 697 | 2053 / 697 | 420 / 8 | 3267 / 1853 | — | 3775 / 2360 | — |
| github.blog/news-insights/the-library/control-git-with- | 359 / 38 | 1983 / 697 | 1983 / 697 | 348 / 8 | 3201 / 1859 | — | 3201 / 1859 | — |
| github.blog/news-insights/the-library/cross-platform-ui | 1673 / 38 | 3306 / 697 | 3306 / 697 | 1662 / 8 | 4524 / 1868 | — | 4524 / 1868 | — |
| github.blog/news-insights/the-library/cyber-monday-25-o | 454 / 38 | 2078 / 697 | 2078 / 697 | 443 / 8 | 3308 / 1871 | 3327 / 1980 | 3308 / 1871 | — |
| github.blog/news-insights/the-library/dashboard-for-ipa | 346 / 35 | 1973 / 697 | 1973 / 697 | 338 / 8 | 3687 / 2354 | 2690 / 1449 | 3179 / 1847 | — |
| github.blog/news-insights/the-library/deploying-without | 350 / 36 | 1976 / 697 | 1976 / 697 | 341 / 8 | 3190 / 1855 | — | 3190 / 1855 | — |
| github.blog/news-insights/the-library/developing-with-s | 359 / 38 | 1983 / 697 | 1983 / 697 | 348 / 8 | 3195 / 1853 | — | 3703 / 2360 | — |
| github.blog/news-insights/the-library/diff-your-gist | 366 / 38 | 1990 / 697 | 1990 / 697 | 355 / 8 | 3202 / 1853 | 2713 / 1455 | 3202 / 1853 | — |
| github.blog/news-insights/the-library/dj-god | 299 / 20 | 1941 / 697 | 1941 / 697 | 306 / 8 | 3613 / 2312 | 2616 / 1407 | 3105 / 1805 | — |
| github.blog/news-insights/the-library/downtime-tonight | 354 / 38 | 1978 / 697 | 1978 / 697 | 343 / 8 | 3184 / 1847 | 3203 / 1956 | 3184 / 1847 | — |
| github.blog/news-insights/the-library/easily-share-ubiq | 329 / 29 | 1964 / 697 | 1964 / 697 | 327 / 8 | 3162 / 1841 | — | 3670 / 2348 | — |
| github.blog/news-insights/the-library/easy-peezy-capist | 356 / 38 | 1980 / 697 | 1980 / 697 | 345 / 8 | 3198 / 1859 | — | 3198 / 1859 | — |
| github.blog/news-insights/the-library/enhanced-ubiquity | 310 / 23 | 1949 / 697 | 1949 / 697 | 314 / 8 | 3131 / 1823 | 3150 / 1932 | 3131 / 1823 | — |
| github.blog/news-insights/the-library/european-training | 403 / 38 | 2028 / 697 | 2028 / 697 | 392 / 8 | 3233 / 1847 | — | 3233 / 1847 | — |
| github.blog/news-insights/the-library/exception-monitor | 1550 / 38 | 3197 / 697 | 3197 / 697 | 1539 / 8 | 4901 / 2367 | — | 4393 / 1860 | — |
| github.blog/news-insights/the-library/facebook-s-memcac | 408 / 38 | 2032 / 697 | 2032 / 697 | 397 / 8 | 3250 / 1859 | — | 3250 / 1859 | — |
| github.blog/news-insights/the-library/flash-in-javascri | 363 / 38 | 1987 / 697 | 1987 / 697 | 352 / 8 | 3199 / 1853 | — | 3199 / 1853 | — |
| github.blog/news-insights/the-library/fork-you-india-2 | 317 / 25 | 1954 / 697 | 1954 / 697 | 319 / 8 | 3146 / 1833 | 2657 / 1435 | 3146 / 1833 | — |
| github.blog/news-insights/the-library/fork-you-on-the-t | 271 / 9 | 1926 / 697 | 1926 / 697 | 289 / 8 | 3604 / 2320 | — | 3096 / 1813 | — |
| github.blog/news-insights/the-library/fork-you-sighting | 306 / 21 | 1947 / 697 | 1947 / 697 | 312 / 8 | 3137 / 1831 | — | 3137 / 1831 | — |
| github.blog/news-insights/the-library/fork-you-sighting | 269 / 9 | 1924 / 697 | 1924 / 697 | 287 / 8 | 3082 / 1801 | — | 3082 / 1801 | — |
| github.blog/news-insights/the-library/fork-you-the-perf | 334 / 30 | 1968 / 697 | 1968 / 697 | 331 / 8 | 3180 / 1855 | — | 3180 / 1855 | — |
| github.blog/news-insights/the-library/get-ready-to-rail | 411 / 38 | 2037 / 697 | 2037 / 697 | 400 / 8 | 3259 / 1865 | 3278 / 1974 | 3259 / 1865 | — |
| github.blog/news-insights/the-library/ghc-haskell-movin | 413 / 38 | 2037 / 697 | 2037 / 697 | 402 / 8 | 3261 / 1865 | 2772 / 1467 | 3261 / 1865 | — |
| github.blog/news-insights/the-library/gist-support-for- | 428 / 38 | 2052 / 697 | 2052 / 697 | 417 / 8 | 3270 / 1859 | 2781 / 1461 | 3270 / 1859 | — |
| github.blog/news-insights/the-library/gist-vim-and-gist | 398 / 38 | 2024 / 697 | 2024 / 697 | 387 / 8 | 3234 / 1853 | 2745 / 1455 | 3234 / 1853 | — |
| github.blog/news-insights/the-library/git-concurrency-i | 1686 / 38 | 3317 / 697 | 3317 / 697 | 1675 / 8 | 4534 / 1865 | — | 4534 / 1865 | — |
| github.blog/news-insights/the-library/git-down-speaker- | 381 / 38 | 2008 / 697 | 2008 / 697 | 370 / 8 | 3223 / 1859 | 2734 / 1461 | 3223 / 1859 | — |
| github.blog/news-insights/the-library/git-helps-people- | 378 / 38 | 2002 / 697 | 2002 / 697 | 367 / 8 | 3226 / 1865 | — | 3226 / 1865 | — |
| github.blog/news-insights/the-library/git-in-haskell | 328 / 29 | 1961 / 697 | 1961 / 697 | 326 / 8 | 3155 / 1835 | 2666 / 1437 | 3155 / 1835 | — |
| github.blog/news-insights/the-library/git-on-windows-ag | 308 / 22 | 1950 / 697 | 1950 / 697 | 313 / 8 | 3134 / 1827 | 3153 / 1936 | 3134 / 1827 | — |
| github.blog/news-insights/the-library/git-over-bonjour | 384 / 38 | 2008 / 697 | 2008 / 697 | 373 / 8 | 3220 / 1853 | 2731 / 1455 | 3220 / 1853 | — |
| github.blog/news-insights/the-library/git-remote-branch | 379 / 38 | 2003 / 697 | 2003 / 697 | 368 / 8 | 3203 / 1841 | — | 3203 / 1841 | — |
| github.blog/news-insights/the-library/git-training | 354 / 38 | 1980 / 697 | 1980 / 697 | 343 / 8 | 3184 / 1847 | 3203 / 1956 | 3184 / 1847 | — |
| github.blog/news-insights/the-library/git-tricks | 383 / 38 | 2008 / 697 | 2008 / 697 | 372 / 8 | 3213 / 1847 | — | 3213 / 1847 | — |
| github.blog/news-insights/the-library/github-at-posscon | 393 / 38 | 2017 / 697 | 2017 / 697 | 382 / 8 | 3229 / 1853 | 2740 / 1455 | 3229 / 1853 | — |
| github.blog/news-insights/the-library/github-at-railsco | 560 / 38 | 2182 / 697 | 2182 / 697 | 549 / 8 | 3396 / 1853 | — | 3396 / 1853 | — |
| github.blog/news-insights/the-library/github-at-zendcon | 360 / 38 | 1984 / 697 | 1984 / 697 | 349 / 8 | 3196 / 1853 | 2707 / 1455 | 3196 / 1853 | — |
| github.blog/news-insights/the-library/github-bookmarkle | 362 / 38 | 1986 / 697 | 1986 / 697 | 351 / 8 | 3192 / 1847 | — | 3192 / 1847 | — |
| github.blog/news-insights/the-library/github-debug | 505 / 38 | 2135 / 697 | 2135 / 697 | 494 / 8 | 3336 / 1848 | 3355 / 1957 | 3336 / 1848 | — |
| github.blog/news-insights/the-library/github-disaster-g | 458 / 38 | 2080 / 697 | 2080 / 697 | 447 / 8 | 3294 / 1853 | — | 3294 / 1853 | — |
| github.blog/news-insights/the-library/github-for-the-re | 375 / 38 | 1999 / 697 | 1999 / 697 | 364 / 8 | 3235 / 1877 | 2746 / 1479 | 3235 / 1877 | — |
| github.blog/news-insights/the-library/github-free-for-o | 492 / 38 | 2114 / 697 | 2114 / 697 | 481 / 8 | 3340 / 1865 | 2851 / 1467 | 3340 / 1865 | — |
| github.blog/news-insights/the-library/github-google-gro | 331 / 30 | 1964 / 697 | 1964 / 697 | 328 / 8 | 3159 / 1837 | 2670 / 1439 | 3159 / 1837 | — |
| github.blog/news-insights/the-library/github-in-your-la | 521 / 38 | 2143 / 697 | 2143 / 697 | 510 / 8 | 3363 / 1859 | 2874 / 1461 | 3363 / 1859 | — |
| github.blog/news-insights/the-library/github-is-about-p | 374 / 38 | 1998 / 697 | 1998 / 697 | 363 / 8 | 3216 / 1859 | 2727 / 1461 | 3216 / 1859 | — |
| github.blog/news-insights/the-library/github-is-hiring | 304 / 21 | 1945 / 697 | 1945 / 697 | 310 / 8 | 3631 / 2326 | 2634 / 1421 | 3631 / 2326 | — |
| github.blog/news-insights/the-library/github-languages | 410 / 38 | 2035 / 697 | 2035 / 697 | 399 / 8 | 3240 / 1847 | 2751 / 1449 | 3240 / 1847 | — |
| github.blog/news-insights/the-library/github-loves-ruby | 456 / 38 | 2078 / 697 | 2078 / 697 | 445 / 8 | 3298 / 1859 | 2809 / 1461 | 3298 / 1859 | — |
| github.blog/news-insights/the-library/github-meetup-bou | 398 / 38 | 2023 / 697 | 2023 / 697 | 387 / 8 | 3252 / 1871 | — | 3760 / 2378 | — |
| github.blog/news-insights/the-library/github-meetup-rio | 369 / 38 | 1993 / 697 | 1993 / 697 | 358 / 8 | 3217 / 1865 | — | 3217 / 1865 | — |
| github.blog/news-insights/the-library/github-meetup-sf- | 384 / 38 | 2009 / 697 | 2009 / 697 | 373 / 8 | 3226 / 1859 | — | 3226 / 1859 | — |
| github.blog/news-insights/the-library/github-meetup-sf- | 411 / 38 | 2038 / 697 | 2038 / 697 | 400 / 8 | 3253 / 1859 | 2764 / 1461 | 3253 / 1859 | — |
| github.blog/news-insights/the-library/github-rebase-1 | 316 / 25 | 1955 / 697 | 1955 / 697 | 318 / 8 | 3139 / 1827 | 2650 / 1429 | 3139 / 1827 | — |
| github.blog/news-insights/the-library/github-rebase-3 | 579 / 38 | 2203 / 697 | 2203 / 697 | 568 / 8 | 3415 / 1853 | — | 3415 / 1853 | — |
| github.blog/news-insights/the-library/github-rebase-33 | 780 / 38 | 2403 / 697 | 2403 / 697 | 769 / 8 | 3616 / 1853 | — | 3616 / 1853 | — |
| github.blog/news-insights/the-library/github-rebase-34 | 830 / 38 | 2453 / 697 | 2453 / 697 | 819 / 8 | 3666 / 1853 | 3177 / 1455 | 3666 / 1853 | — |
| github.blog/news-insights/the-library/github-rebase-35 | 843 / 38 | 2466 / 697 | 2466 / 697 | 832 / 8 | 4187 / 2360 | 3190 / 1455 | 3679 / 1853 | — |
| github.blog/news-insights/the-library/github-rebase-36 | 724 / 38 | 2347 / 697 | 2347 / 697 | 713 / 8 | 3560 / 1853 | — | 3560 / 1853 | — |
| github.blog/news-insights/the-library/github-rebase-4 | 630 / 38 | 2253 / 697 | 2253 / 697 | 619 / 8 | 3464 / 1853 | — | 3466 / 1853 | — |
| github.blog/news-insights/the-library/github-rebase-5 | 775 / 38 | 2398 / 697 | 2398 / 697 | 764 / 8 | 3611 / 1853 | 3122 / 1455 | 3611 / 1853 | — |
| github.blog/news-insights/the-library/github-rebase-6 | 807 / 38 | 2429 / 697 | 2429 / 697 | 796 / 8 | 3643 / 1853 | — | 3643 / 1853 | — |
| github.blog/news-insights/the-library/github-rebase-7 | 886 / 38 | 2509 / 697 | 2509 / 697 | 875 / 8 | 3722 / 1853 | 3233 / 1455 | 3722 / 1853 | — |
| github.blog/news-insights/the-library/github-rebase-8 | 797 / 38 | 2419 / 697 | 2419 / 697 | 786 / 8 | 3633 / 1853 | — | 3633 / 1853 | — |
| github.blog/news-insights/the-library/github-services-i | 407 / 38 | 2031 / 697 | 2031 / 697 | 396 / 8 | 3243 / 1853 | 2754 / 1455 | 3243 / 1853 | — |
| github.blog/news-insights/the-library/github-support | 360 / 38 | 1986 / 697 | 1986 / 697 | 349 / 8 | 3190 / 1847 | — | 3190 / 1847 | — |
| github.blog/news-insights/the-library/github-supports-o | 614 / 38 | 2237 / 697 | 2237 / 697 | 603 / 8 | 3492 / 1895 | 3003 / 1497 | 3492 / 1895 | — |
| github.blog/news-insights/the-library/github-textmate-b | 364 / 38 | 1988 / 697 | 1988 / 697 | 353 / 8 | 3200 / 1853 | 2711 / 1455 | 3200 / 1853 | — |
| github.blog/news-insights/the-library/github-turns-one | 474 / 38 | 2096 / 697 | 2096 / 697 | 463 / 8 | 3310 / 1853 | — | 3310 / 1853 | — |
| github.blog/news-insights/the-library/github-userscript | 359 / 38 | 1985 / 697 | 1985 / 697 | 348 / 8 | 3697 / 2354 | 2700 / 1449 | 3189 / 1847 | — |
| github.blog/news-insights/the-library/github-wiki-upgra | 566 / 38 | 2190 / 697 | 2190 / 697 | 555 / 8 | 3414 / 1865 | 2925 / 1467 | 3414 / 1865 | — |
| github.blog/news-insights/the-library/githubbin-from-wo | 400 / 38 | 2024 / 697 | 2024 / 697 | 389 / 8 | 3744 / 2360 | 2747 / 1455 | 3236 / 1853 | — |
| github.blog/news-insights/the-library/grailscrowd | 344 / 35 | 1973 / 697 | 1973 / 697 | 336 / 8 | 3673 / 2342 | — | 3673 / 2342 | — |
| github.blog/news-insights/the-library/has-my-gem-built- | 324 / 27 | 1961 / 697 | 1961 / 697 | 324 / 8 | 3161 / 1843 | — | 3161 / 1843 | — |
| github.blog/news-insights/the-library/hello-world | 388 / 38 | 2012 / 697 | 2012 / 697 | 377 / 8 | 3218 / 1847 | — | 3726 / 2354 | — |
| github.blog/news-insights/the-library/hot-ruby-projects | 376 / 38 | 2000 / 697 | 2000 / 697 | 365 / 8 | 3224 / 1865 | 2735 / 1467 | 3224 / 1865 | — |
| github.blog/news-insights/the-library/how-to-run-a-goog | 1385 / 38 | 3007 / 697 | 3007 / 697 | 1374 / 8 | 4269 / 1901 | 3780 / 1503 | 4269 / 1901 | — |
| github.blog/news-insights/the-library/http-cloning | 407 / 38 | 2031 / 697 | 2031 / 697 | 396 / 8 | 3237 / 1847 | 3256 / 1956 | 3237 / 1847 | — |
| github.blog/news-insights/the-library/it-s-a-mirror | 411 / 38 | 2035 / 697 | 2035 / 697 | 400 / 8 | 3755 / 2360 | 2758 / 1455 | 3755 / 2360 | — |
| github.blog/news-insights/the-library/janky | 326 / 29 | 1961 / 697 | 1961 / 697 | 324 / 8 | 3141 / 1823 | 3160 / 1932 | 3649 / 2330 | — |
| github.blog/news-insights/the-library/janky-5 | 326 / 29 | 1961 / 697 | 1961 / 697 | 324 / 8 | 3141 / 1823 | 3160 / 1932 | 3141 / 1823 | — |
| github.blog/news-insights/the-library/join-virtual-clas | 721 / 38 | 2345 / 697 | 2345 / 697 | 710 / 8 | 3587 / 1883 | — | 3587 / 1883 | — |
| github.blog/news-insights/the-library/kindle-winner | 270 / 10 | 1924 / 697 | 1924 / 697 | 287 / 8 | 3072 / 1791 | 2583 / 1393 | 3072 / 1791 | — |
| github.blog/news-insights/the-library/local-github-conf | 456 / 38 | 2078 / 697 | 2078 / 697 | 445 / 8 | 3292 / 1853 | 2803 / 1455 | 3292 / 1853 | — |
| github.blog/news-insights/the-library/maintenance-video | 389 / 38 | 2013 / 697 | 2013 / 697 | 378 / 8 | 3219 / 1847 | — | 3219 / 1847 | — |
| github.blog/news-insights/the-library/maven-enabled-pro | 400 / 38 | 2024 / 697 | 2024 / 697 | 389 / 8 | 3236 / 1853 | 2747 / 1455 | 3236 / 1853 | — |
| github.blog/news-insights/the-library/more-db-optimizat | 356 / 38 | 1980 / 697 | 1980 / 697 | 345 / 8 | 3700 / 2360 | — | 3700 / 2360 | — |
| github.blog/news-insights/the-library/more-github-gem-g | 376 / 38 | 2000 / 697 | 2000 / 697 | 365 / 8 | 3218 / 1859 | 3237 / 1968 | 3218 / 1859 | — |
| github.blog/news-insights/the-library/more-javascript-g | 356 / 38 | 1980 / 697 | 1980 / 697 | 345 / 8 | 3198 / 1859 | 2709 / 1461 | 3198 / 1859 | — |
| github.blog/news-insights/the-library/more-slowness-era | 325 / 28 | 1959 / 697 | 1959 / 697 | 324 / 8 | 3151 / 1833 | 2662 / 1435 | 3151 / 1833 | — |
| github.blog/news-insights/the-library/more-textmate-bun | 377 / 38 | 2001 / 697 | 2001 / 697 | 366 / 8 | 3219 / 1859 | 3238 / 1968 | 3219 / 1859 | — |
| github.blog/news-insights/the-library/myspace-for-hacke | 411 / 38 | 2035 / 697 | 2035 / 697 | 400 / 8 | 3247 / 1853 | — | 3755 / 2360 | — |
| github.blog/news-insights/the-library/ncsa-mosaic-on-gi | 356 / 38 | 1980 / 697 | 1980 / 697 | 345 / 8 | 3198 / 1859 | — | 3198 / 1859 | — |
| github.blog/news-insights/the-library/net-neutrality-up | 1100 / 42 | 2718 / 697 | 2718 / 697 | 1085 / 8 | 4051 / 1972 | 3562 / 1574 | 4051 / 1972 | — |
| github.blog/news-insights/the-library/new-languages-hig | 458 / 38 | 2080 / 697 | 2080 / 697 | 447 / 8 | 3802 / 2360 | 2805 / 1455 | 3294 / 1853 | — |
| github.blog/news-insights/the-library/new-post-receive- | 312 / 23 | 1951 / 697 | 1951 / 697 | 316 / 8 | 3653 / 2342 | 2656 / 1437 | 3653 / 2342 | — |
| github.blog/news-insights/the-library/new-to-git | 437 / 38 | 2060 / 697 | 2060 / 697 | 426 / 8 | 3781 / 2360 | 2784 / 1455 | 3781 / 2360 | — |
| github.blog/news-insights/the-library/new-to-git-cheat | 412 / 38 | 2036 / 697 | 2036 / 697 | 401 / 8 | 3254 / 1859 | — | 3254 / 1859 | — |
| github.blog/news-insights/the-library/new-year-new-comp | 424 / 38 | 2048 / 697 | 2048 / 697 | 413 / 8 | 3774 / 2366 | — | 3266 / 1859 | — |
| github.blog/news-insights/the-library/not-just-code | 386 / 38 | 2010 / 697 | 2010 / 697 | 375 / 8 | 3222 / 1853 | — | 3222 / 1853 | — |
| github.blog/news-insights/the-library/nu-and-io-on-gith | 562 / 38 | 2184 / 697 | 2184 / 697 | 551 / 8 | 3410 / 1865 | 3429 / 1974 | 3410 / 1865 | — |
| github.blog/news-insights/the-library/octocatalog-diff- | 1387 / 38 | 3015 / 697 | 3015 / 697 | 1376 / 8 | 4757 / 2386 | — | 4249 / 1879 | — |
| github.blog/news-insights/the-library/one-more-thing | 362 / 38 | 1990 / 697 | 1990 / 697 | 351 / 8 | 3198 / 1853 | 2709 / 1455 | 3198 / 1853 | — |
| github.blog/news-insights/the-library/open-source-proje | 400 / 38 | 2024 / 697 | 2024 / 697 | 389 / 8 | 3248 / 1865 | 2759 / 1467 | 3248 / 1865 | — |
| github.blog/news-insights/the-library/open-sourcing-our | 516 / 38 | 2138 / 697 | 2138 / 697 | 505 / 8 | 3376 / 1877 | 2887 / 1479 | 3376 / 1877 | — |
| github.blog/news-insights/the-library/our-rubygem-build | 366 / 38 | 1990 / 697 | 1990 / 697 | 355 / 8 | 3232 / 1883 | 2743 / 1485 | 3232 / 1883 | — |
| github.blog/news-insights/the-library/pages-jekyll-to-v | 372 / 38 | 1996 / 697 | 1996 / 697 | 361 / 8 | 3226 / 1871 | 2737 / 1473 | 3226 / 1871 | — |
| github.blog/news-insights/the-library/palm-goes-github | 371 / 38 | 1996 / 697 | 1996 / 697 | 360 / 8 | 3207 / 1853 | 2718 / 1455 | 3207 / 1853 | — |
| github.blog/news-insights/the-library/paris-git-trainin | 365 / 38 | 1989 / 697 | 1989 / 697 | 354 / 8 | 3201 / 1853 | 2712 / 1455 | 3201 / 1853 | — |
| github.blog/news-insights/the-library/participation-gra | 465 / 38 | 2087 / 697 | 2087 / 697 | 454 / 8 | 3307 / 1859 | 2818 / 1461 | 3307 / 1859 | — |
| github.blog/news-insights/the-library/pearhub | 376 / 38 | 2000 / 697 | 2000 / 697 | 365 / 8 | 3200 / 1841 | — | 3200 / 1841 | — |
| github.blog/news-insights/the-library/philadelphia-coha | 376 / 38 | 1999 / 697 | 1999 / 697 | 365 / 8 | 3212 / 1853 | — | 3212 / 1853 | — |
| github.blog/news-insights/the-library/pimp-your-prototy | 473 / 38 | 2094 / 697 | 2094 / 697 | 462 / 8 | 3315 / 1859 | — | 3823 / 2366 | — |
| github.blog/news-insights/the-library/postmortem-of-las | 691 / 38 | 2312 / 697 | 2312 / 697 | 680 / 8 | 3541 / 1867 | 3052 / 1469 | 3541 / 1867 | — |
| github.blog/news-insights/the-library/pro-git-bloggin | 395 / 38 | 2020 / 697 | 2020 / 697 | 384 / 8 | 3231 / 1853 | 2742 / 1455 | 3231 / 1853 | — |
| github.blog/news-insights/the-library/profitable-progra | 382 / 38 | 2006 / 697 | 2006 / 697 | 371 / 8 | 3732 / 2366 | — | 3732 / 2366 | — |
| github.blog/news-insights/the-library/pushes | 393 / 38 | 2017 / 697 | 2017 / 697 | 382 / 8 | 3725 / 2348 | 2728 / 1443 | 3725 / 2348 | — |
| github.blog/news-insights/the-library/pushing-and-pulli | 358 / 38 | 1982 / 697 | 1982 / 697 | 347 / 8 | 3194 / 1853 | — | 3194 / 1853 | — |
| github.blog/news-insights/the-library/rails-moving-to-g | 415 / 38 | 2040 / 697 | 2040 / 697 | 404 / 8 | 3257 / 1859 | 2768 / 1461 | 3765 / 2366 | — |
| github.blog/news-insights/the-library/random-repo | 369 / 38 | 1993 / 697 | 1993 / 697 | 358 / 8 | 3199 / 1847 | 2710 / 1449 | 3199 / 1847 | — |
| github.blog/news-insights/the-library/removing-oobgc | 1034 / 38 | 2669 / 697 | 2669 / 697 | 1023 / 8 | 3882 / 1865 | 3901 / 1974 | 3882 / 1865 | — |
| github.blog/news-insights/the-library/rolling-with-engi | 395 / 38 | 2019 / 697 | 2019 / 697 | 384 / 8 | 3237 / 1859 | — | 3237 / 1859 | — |
| github.blog/news-insights/the-library/runnable-document | 1618 / 38 | 3240 / 697 | 3240 / 697 | 1607 / 8 | 4466 / 1865 | 3977 / 1467 | 4466 / 1865 | — |
| github.blog/news-insights/the-library/scala-projects-cl | 432 / 38 | 2056 / 697 | 2056 / 697 | 421 / 8 | 3274 / 1859 | 2785 / 1461 | 3274 / 1859 | — |
| github.blog/news-insights/the-library/scheduled-db-main | 386 / 38 | 2010 / 697 | 2010 / 697 | 375 / 8 | 3754 / 2384 | 2757 / 1479 | 3754 / 2384 | — |
| github.blog/news-insights/the-library/scheduled-fileser | 374 / 38 | 1998 / 697 | 1998 / 697 | 363 / 8 | 3234 / 1877 | — | 3234 / 1877 | — |
| github.blog/news-insights/the-library/services-galore | 447 / 38 | 2069 / 697 | 2069 / 697 | 436 / 8 | 3277 / 1847 | 2788 / 1449 | 3277 / 1847 | — |
| github.blog/news-insights/the-library/side-projects-the | 369 / 38 | 1993 / 697 | 1993 / 697 | 358 / 8 | 3211 / 1859 | 2722 / 1461 | 3211 / 1859 | — |
| github.blog/news-insights/the-library/smart-http-suppor | 604 / 38 | 2226 / 697 | 2226 / 697 | 593 / 8 | 3440 / 1853 | 2951 / 1455 | 3440 / 1853 | — |
| github.blog/news-insights/the-library/smooth-support-lo | 356 / 38 | 1982 / 697 | 1982 / 697 | 345 / 8 | 3700 / 2360 | 2703 / 1455 | 3700 / 2360 | — |
| github.blog/news-insights/the-library/sound-in-the-clou | 323 / 27 | 1960 / 697 | 1960 / 697 | 323 / 8 | 3154 / 1837 | 2665 / 1439 | 3154 / 1837 | — |
| github.blog/news-insights/the-library/speedy-queries | 370 / 38 | 1994 / 697 | 1994 / 697 | 359 / 8 | 3200 / 1847 | 2711 / 1449 | 3200 / 1847 | — |
| github.blog/news-insights/the-library/ssh-keys-generate | 536 / 38 | 2156 / 697 | 2156 / 697 | 525 / 8 | 3390 / 1871 | 2901 / 1473 | 3390 / 1871 | — |
| github.blog/news-insights/the-library/submodule-display | 382 / 38 | 2006 / 697 | 2006 / 697 | 371 / 8 | 3720 / 2354 | — | 3720 / 2354 | — |
| github.blog/news-insights/the-library/supercharged-git- | 618 / 38 | 2240 / 697 | 2240 / 697 | 607 / 8 | 3448 / 1847 | 2959 / 1449 | 3448 / 1847 | — |
| github.blog/news-insights/the-library/tasty-tidbits | 357 / 38 | 1981 / 697 | 1981 / 697 | 346 / 8 | 3187 / 1847 | 2698 / 1449 | 3187 / 1847 | — |
| github.blog/news-insights/the-library/the-api | 374 / 38 | 1998 / 697 | 1998 / 697 | 363 / 8 | 3712 / 2354 | 2715 / 1449 | 3712 / 2354 | — |
| github.blog/news-insights/the-library/the-blog-arrives | 391 / 38 | 2015 / 697 | 2015 / 697 | 380 / 8 | 3735 / 2360 | 2738 / 1455 | 3735 / 2360 | — |
| github.blog/news-insights/the-library/the-future-of-cod | 451 / 38 | 2073 / 697 | 2073 / 697 | 440 / 8 | 3293 / 1859 | 2804 / 1461 | 3293 / 1859 | — |
| github.blog/news-insights/the-library/the-git-user-s-su | 409 / 38 | 2035 / 697 | 2035 / 697 | 398 / 8 | 3251 / 1859 | — | 3251 / 1859 | — |
| github.blog/news-insights/the-library/the-github-podcas | 389 / 38 | 2013 / 697 | 2013 / 697 | 378 / 8 | 3225 / 1853 | — | 3225 / 1853 | — |
| github.blog/news-insights/the-library/the-new-queue | 1052 / 38 | 2674 / 697 | 2674 / 697 | 1041 / 8 | 3890 / 1853 | — | 3890 / 1853 | — |
| github.blog/news-insights/the-library/the-pricing-plans | 371 / 38 | 1995 / 697 | 1995 / 697 | 360 / 8 | 3207 / 1853 | 2718 / 1455 | 3207 / 1853 | — |
| github.blog/news-insights/the-library/the-status-blog | 360 / 38 | 1984 / 697 | 1984 / 697 | 349 / 8 | 3196 / 1853 | 2707 / 1455 | 3196 / 1853 | — |
| github.blog/news-insights/the-library/the-tree-slider | 529 / 38 | 2151 / 697 | 2151 / 697 | 518 / 8 | 3365 / 1853 | — | 3365 / 1853 | — |
| github.blog/news-insights/the-library/tinymce-on-github | 364 / 38 | 1988 / 697 | 1988 / 697 | 353 / 8 | 3200 / 1853 | 3219 / 1962 | 3708 / 2360 | — |
| github.blog/news-insights/the-library/tortoisegit-chall | 575 / 38 | 2197 / 697 | 2197 / 697 | 564 / 8 | 3405 / 1847 | 2916 / 1449 | 3405 / 1847 | — |
| github.blog/news-insights/the-library/twitter-s-on-gith | 392 / 38 | 2017 / 697 | 2017 / 697 | 381 / 8 | 3228 / 1853 | — | 3228 / 1853 | — |
| github.blog/news-insights/the-library/use-bit-ly-to-nam | 385 / 38 | 2010 / 697 | 2010 / 697 | 374 / 8 | 3233 / 1865 | 2744 / 1467 | 3233 / 1865 | — |
| github.blog/news-insights/the-library/use-github-as-you | 492 / 38 | 2114 / 697 | 2114 / 697 | 481 / 8 | 3340 / 1865 | 2851 / 1467 | 3340 / 1865 | — |
| github.blog/news-insights/the-library/using-git-in-ruby | 507 / 38 | 2129 / 697 | 2129 / 697 | 496 / 8 | 3355 / 1865 | — | 3355 / 1865 | — |
| github.blog/news-insights/the-library/vote-for-github | 386 / 38 | 2012 / 697 | 2012 / 697 | 375 / 8 | 3222 / 1853 | 2733 / 1455 | 3222 / 1853 | — |
| github.blog/news-insights/the-library/we-re-web-2-0 | 365 / 38 | 1989 / 697 | 1989 / 697 | 354 / 8 | 3201 / 1853 | 2712 / 1455 | 3201 / 1853 | — |
| github.blog/news-insights/the-library/webpulp-tv-interv | 396 / 38 | 2020 / 697 | 2020 / 697 | 385 / 8 | 3244 / 1865 | 2755 / 1467 | 3244 / 1865 | — |
| github.blog/news-insights/the-library/when-limits-are-e | 385 / 38 | 2009 / 697 | 2009 / 697 | 374 / 8 | 3227 / 1859 | — | 3227 / 1859 | — |
| github.blog/news-insights/the-library/wiki-preview | 267 / 9 | 1920 / 697 | 1920 / 697 | 285 / 8 | 3068 / 1789 | — | 3068 / 1789 | — |
| github.blog/news-insights/the-library/yesterday-s-outag | 500 / 38 | 2122 / 697 | 2122 / 697 | 489 / 8 | 3330 / 1847 | — | 3330 / 1847 | — |
| github.blog/news-insights/the-library/yui-examples | 356 / 38 | 1980 / 697 | 1980 / 697 | 345 / 8 | 3186 / 1847 | 2697 / 1449 | 3186 / 1847 | — |
| github.blog/news-insights/the-library/yui-on-github | 377 / 38 | 2003 / 697 | 2003 / 697 | 366 / 8 | 3213 / 1853 | — | 3213 / 1853 | — |
| github.blog/news-insights/the-library/zendcon-2008-pics | 283 / 14 | 1931 / 697 | 1931 / 697 | 296 / 8 | 3095 / 1805 | 2606 / 1407 | 3095 / 1805 | — |
| github.blog/open-source/git/git-2-13-has-been-released | 2003 / 36 | 3677 / 697 | 3677 / 697 | 2003 / 6 | 4858 / 1861 | — | 4858 / 1861 | — |
| github.blog/open-source/improving-your-oss-dependency-w | 1383 / 34 | 3056 / 697 | 3056 / 697 | 1383 / 4 | 4758 / 2380 | 3761 / 1475 | 4250 / 1873 | — |
| github.blog/security/subresource-integrity | 829 / 33 | 2498 / 697 | 2498 / 697 | 818 / 3 | 3653 / 1841 | 3672 / 1950 | 3653 / 1841 | — |

</details>

## See also

- [RETRIEVAL_COMPARISON.md](RETRIEVAL_COMPARISON.md) — does cleaner Markdown improve retrieval?
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup and fairness decisions
