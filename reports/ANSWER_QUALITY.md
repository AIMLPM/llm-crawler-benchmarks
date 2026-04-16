# End-to-End RAG Answer Quality
<!-- style: v2, 2026-04-15 -->

All crawlers produce similar LLM answer quality (4.03-4.53 out of 5). colly+md leads slightly at 4.53; markcrawl ranks 2nd at 4.52 — a 0.3% gap from the best. The gaps are small but consistent.

Each tool's crawled content is chunked, embedded, retrieved (top-10),
and sent to `gpt-4o-mini` to generate an answer. Answers are scored by
`gpt-4o-mini` on correctness, relevance, completeness, and usefulness (1-5 each).

**Scoring scale:** 1 = wrong/irrelevant, 2 = partially relevant, 3 = acceptable, 4 = good, 5 = excellent/complete. Scores are averaged across all queries per tool. An overall score above 4.0 indicates consistently good answers.

## Summary (109 queries across 8 sites)

| Tool | Correctness | Relevance | Completeness | Usefulness | **Overall** | Avg tokens/query |
|---|---|---|---|---|---|---|
| colly+md | 4.64 | 4.60 | 4.36 | 4.54 | **4.53 ±0.19** | 1,659 |
| **markcrawl** | 4.64 | 4.57 | 4.36 | 4.51 | **4.52 ±0.19** | 2,080 |
| crawlee | 4.65 | 4.60 | 4.31 | 4.50 | **4.52 ±0.19** | 1,724 |
| crawl4ai-raw | 4.61 | 4.51 | 4.21 | 4.42 | **4.44 ±0.20** | 1,617 |
| crawl4ai | 4.61 | 4.50 | 4.20 | 4.42 | **4.43 ±0.20** | 1,622 |
| playwright | 4.59 | 4.49 | 4.19 | 4.40 | **4.42 ±0.21** | 1,794 |
| scrapy+md | 4.30 | 4.09 | 3.73 | 4.00 | **4.03 ±0.25** | 1,779 |

> **Column definitions:** All scores are 1-5 averages across queries, judged by `gpt-4o-mini`. **Correctness** = factual accuracy. **Relevance** = answers the question asked. **Completeness** = covers all aspects. **Usefulness** = practical value to the user. **Overall** = mean of the four dimensions (± 95% confidence interval). **Avg tokens/query** = estimated input tokens per query (chunk words x 1.33). Gaps within the ± range are not statistically significant.

## What this means in practice

The quality gap between the best (colly+md, 4.53) and worst (scrapy+md, 4.03) crawler is 0.50 points on a 5-point scale -- 11.0% relative. This gap is real but small.

For most use cases, your choice of crawler will not noticeably affect the quality of LLM-generated answers. All tools produce answers that score above 4.0 ("good") on average, meaning users get helpful, accurate responses regardless of which crawler feeds the pipeline.

**Executive takeaway:** Switching crawlers purely to improve answer quality is unlikely to justify the migration effort. The cost and speed differences between tools are far more impactful on your bottom line -- see [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar-level analysis.

## quotes-toscrape

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 4.62 | 4.38 | 3.88 | 4.38 | 4.31 ±0.80 |
| crawl4ai-raw | 4.62 | 4.38 | 3.88 | 4.38 | 4.31 ±0.80 |
| colly+md | 4.62 | 4.38 | 3.88 | 4.38 | 4.31 ±0.80 |
| crawlee | 4.62 | 4.38 | 3.75 | 4.25 | 4.25 ±0.79 |
| playwright | 4.62 | 4.38 | 3.75 | 4.25 | 4.25 ±0.79 |
| **markcrawl** | 4.25 | 3.88 | 3.50 | 3.88 | 3.88 ±1.03 |
| scrapy+md | 4.12 | 3.62 | 3.25 | 3.62 | 3.66 ±1.02 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for quotes-toscrape</summary>

**Q1: What did Albert Einstein say about thinking and the world?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Albert Einstein said, “The world as we have created it is a process of our thinking. It cannot be ch... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: Which quotes are tagged with 'change'?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| colly+md | 5 | 5 | 4 | 5 | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| crawlee | 5 | 5 | 3 | 4 | 4.2 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| playwright | 5 | 5 | 3 | 4 | 4.2 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q3: What did Steve Martin say about sunshine?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Steve Martin said, “A day without sunshine is like, you know, night.”... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | “A day without sunshine is like, you know, night.” by Steve Martin.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | “A day without sunshine is like, you know, night.” by Steve Martin.... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |

**Q4: What quotes are about thinking deeply?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 4 | 5 | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | The quote about thinking deeply is: “The world as we have created it is a process of our thinking. I... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | The quote about thinking deeply is: “The world as we have created it is a process of our thinking. I... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | The quote about thinking deeply is: “The world as we have created it is a process of our thinking. I... |
| colly+md | 5 | 5 | 4 | 5 | 4.8 | The quote about thinking deeply is:   “The world as we have created it is a process of our thinking.... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | The quote about thinking deeply is:   “The world as we have created it is a process of our thinking.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: What did Eleanor Roosevelt say about life?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| colly+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: Which quotes are tagged about choices and abilities?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The quote tagged about choices and abilities is: “It is our choices, Harry, that show what we truly ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The quote tagged about choices and abilities is: “It is our choices, Harry, that show what we truly ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The quote tagged about choices and abilities is:   “It is our choices, Harry, that show what we trul... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The quote tagged about choices and abilities is:   “It is our choices, Harry, that show what we trul... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The quote tagged about choices and abilities is:   “It is our choices, Harry, that show what we trul... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: What quotes are about friendship?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The quotes about friendship are:  1. "This life is what you make it. No matter what, you're going to... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The quotes about friendship are:  1. “Good friends, good books, and a sleepy conscience: this is the... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The quotes about friendship are:  1. “This life is what you make it. No matter what, you're going to... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The quotes about friendship are:  1. “It takes a great deal of bravery to stand up to our enemies, b... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The quotes about friendship are:  1. “Good friends, good books, and a sleepy conscience: this is the... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The quotes about friendship are:  1. "Good friends, good books, and a sleepy conscience: this is the... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The quotes about friendship are:  1. “Good friends, good books, and a sleepy conscience: this is the... |

**Q8: What are the quotes about love?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | 1. “The opposite of love is not hate, it's indifference.” - Elie Wiesel 2. “It is not a lack of love... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | 1. “It is not a lack of love, but a lack of friendship that makes unhappy marriages.” - Friedrich Ni... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## books-toscrape

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawlee | 4.80 | 5.00 | 4.80 | 4.90 | 4.88 ±0.20 |
| playwright | 4.80 | 5.00 | 4.80 | 4.90 | 4.88 ±0.20 |
| colly+md | 4.80 | 4.90 | 4.80 | 4.90 | 4.85 ±0.24 |
| **markcrawl** | 4.60 | 4.70 | 4.50 | 4.50 | 4.58 ±0.56 |
| crawl4ai-raw | 4.30 | 4.20 | 3.80 | 4.00 | 4.08 ±0.73 |
| crawl4ai | 4.10 | 4.30 | 3.70 | 3.90 | 4.00 ±0.70 |
| scrapy+md | 3.20 | 2.80 | 1.80 | 2.40 | 2.55 ±0.53 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for books-toscrape</summary>

**Q1: What mystery and thriller books are in the catalog?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The mystery books in the catalog are:  1. Sharp Objects - £47.82 2. In a Dark, Dark Wood - £19.63 3.... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | **Mystery Books:** 1. Sharp Objects - £47.82 2. In a Dark, Dark Wood - £19.63 3. The Past Never Ends... |
| colly+md | 5 | 5 | 4 | 5 | 4.8 | **Mystery Books:** 1. Sharp Objects - £47.82 2. In a Dark, Dark Wood - £19.63 3. The Past Never Ends... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | **Mystery Books:** 1. Sharp Objects - £47.82 2. In a Dark, Dark Wood - £19.63 3. The Past Never Ends... |
| crawl4ai | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What science fiction books are available?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The available science fiction books are:  1. Mesaerion: The Best Science Fiction Stories 1800-1849 -... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The available science fiction books are:  1. [Mesaerion: The Best Science Fiction Stories 1800-1849]... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The available science fiction books are:  1. Mesaerion: The Best Science Fiction Stories 1800-1849 -... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The available science fiction books are:  1. Mesaerion: The Best Science Fiction Stories 1800-1849 -... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The available science fiction books are:  1. Mesaerion: The Best Science Fiction Stories 1800-1849 -... |
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | The available science fiction books are:  1. [Mesaerion: The Best Science Fiction Stories 1800-1849]... |
| scrapy+md | 2 | 3 | 2 | 2 | 2.2 | The available science fiction book is "Mesaerion: The Best Science Fiction Stories 1800-1849," price... |

**Q3: What is the book Sharp Objects about?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Sharp Objects follows reporter Camille Preaker, who returns to her hometown to cover the murders of ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Sharp Objects follows reporter Camille Preaker, who returns to her hometown to cover the murders of ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Sharp Objects follows reporter Camille Preaker, who returns to her hometown to cover the murders of ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Sharp Objects follows reporter Camille Preaker, who returns to her hometown to cover the murders of ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Sharp Objects follows reporter Camille Preaker, who returns to her hometown to cover the murders of ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Sharp Objects follows reporter Camille Preaker, who returns to her hometown to cover the murders of ... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: What biography books are in the catalog?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The biography books in the catalog are:  1. Louisa: The Extraordinary Life of Mrs. Adams - £16.85 2.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The biography books in the catalog are:  1. Louisa: The Extraordinary Life of Mrs. Adams - £16.85 2.... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The biography books in the catalog are:  1. Louisa: The Extraordinary Life of Mrs. Adams - £16.85 2.... |
| markcrawl | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| scrapy+md | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q5: What horror books are in the catalog?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The horror books in the catalog are:  1. Security - £39.25 2. Follow You Home - £21.36 3. The Loney ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The horror books in the catalog are:  1. Security - £39.25 2. Follow You Home - £21.36 3. The Loney ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The horror books in the catalog are:  1. Security - £39.25 2. Follow You Home - £21.36 3. The Loney ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The horror books in the catalog are:  1. Security - £39.25 2. Follow You Home - £21.36 3. The Loney ... |
| crawl4ai-raw | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |

**Q6: What poetry books can I find?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. The Black Maria - £52.... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. Quarter Life Poetry: P... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. Quarter Life Poetry: P... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. The Black Maria - £52.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. The Black Maria - £52.... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. The Black Maria - £52.... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | You can find the following poetry books:  1. **You can't bury them all: Poems** - £33.63 2. **Shakes... |

**Q7: What fantasy books are in the bookstore?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The fantasy books in the bookstore are:  1. King's Folly (The Kinsman Chronicles #1) - £39.61 2. Uni... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The fantasy books in the bookstore are:  1. The Bane Chronicles (The Bane Chronicles #1-11) - £44.73... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The fantasy books in the bookstore are:  1. The Bane Chronicles (The Bane Chronicles #1-11) - £44.73... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The fantasy books in the bookstore are:  1. King's Folly (The Kinsman Chronicles #1) - £39.61 2. Uni... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The fantasy books in the bookstore are:  1. King's Folly (The Kinsman Chronicles #1) - £39.61 2. Uni... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The fantasy books in the bookstore are:  1. King's Folly (The Kinsman Chronicles #1) - £39.61 2. Uni... |
| scrapy+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |

**Q8: What philosophy books are available to read?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | The available philosophy books are:  1. [At The Existentialist Café: Freedom, Being, and apricot coc... |
| crawl4ai | 4 | 5 | 4 | 4 | 4.2 | The available philosophy books are:  1. [At The Existentialist Café: Freedom, Being, and apricot coc... |
| crawlee | 3 | 5 | 4 | 4 | 4.0 | The available philosophy books are:  1. Sophie's World - £15.94 2. The Death of Humanity: and the Ca... |
| playwright | 3 | 5 | 4 | 4 | 4.0 | The available philosophy books are:  1. Sophie's World - £15.94 2. The Death of Humanity: and the Ca... |
| colly+md | 3 | 4 | 4 | 4 | 3.8 | The available philosophy books are:  1. Sophie's World - £15.94 2. The Death of Humanity: and the Ca... |
| markcrawl | 2 | 4 | 3 | 3 | 3.0 | The available philosophy books are:  1. **Libertarianism for Beginners** - £51.33 2. **Why the Right... |
| scrapy+md | 2 | 3 | 2 | 2 | 2.2 | The available philosophy book to read is "Sophie’s World."... |

**Q9: What is the book Sapiens about?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The book "Sapiens" by Dr. Yuval Noah Harari explores humanity's creation and evolution, integrating ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The book "Sapiens: A Brief History of Humankind" by Dr. Yuval Noah Harari explores humanity's creati... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The book "Sapiens: A Brief History of Humankind" by Dr. Yuval Noah Harari explores humanity's creati... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The book "Sapiens: A Brief History of Humankind" by Dr. Yuval Noah Harari explores the creation and ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The book "Sapiens: A Brief History of Humankind" by Dr. Yuval Noah Harari explores the creation and ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The book "Sapiens: A Brief History of Humankind" by Dr. Yuval Noah Harari explores the creation and ... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q10: What romance novels are available?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The available romance novels are:  1. Chase Me (Paris Nights #2) - £25.27 2. Black Dust - £34.53 3. ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The available romance novels are:  1. Chase Me (Paris Nights #2) - £25.27 2. Black Dust - £34.53 3. ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The available romance novels are:  1. Chase Me (Paris Nights #2) - £25.27 2. Black Dust - £34.53 3. ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The available romance novels are:  1. Chase Me (Paris Nights #2) - £25.27 2. Black Dust - £34.53 3. ... |
| crawl4ai | 3 | 4 | 3 | 4 | 3.5 | The available romance novels are:  1. [Chase Me (Paris Nights #2)](https://books.toscrape.com/catalo... |
| crawl4ai-raw | 3 | 4 | 3 | 4 | 3.5 | The available romance novels are:  1. [Chase Me (Paris Nights #2)](https://books.toscrape.com/catalo... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## fastapi-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 4.80 | 4.95 | 4.75 | 4.90 | 4.85 ±0.18 |
| crawl4ai | 4.85 | 4.90 | 4.60 | 4.80 | 4.79 ±0.26 |
| crawl4ai-raw | 4.85 | 4.85 | 4.55 | 4.80 | 4.76 ±0.30 |
| playwright | 4.75 | 4.85 | 4.70 | 4.75 | 4.76 ±0.28 |
| crawlee | 4.70 | 4.90 | 4.70 | 4.70 | 4.75 ±0.27 |
| scrapy+md | 4.60 | 4.85 | 4.60 | 4.70 | 4.69 ±0.28 |
| colly+md | 4.60 | 4.85 | 4.60 | 4.70 | 4.69 ±0.28 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for fastapi-docs</summary>

**Q1: How do I add authentication to a FastAPI endpoint?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To add authentication to a FastAPI endpoint, you can use the security utilities provided by FastAPI,... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To add authentication to a FastAPI endpoint, you can use the `OAuth2PasswordBearer` class from the `... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To add authentication to a FastAPI endpoint, you can use the `OAuth2PasswordBearer` class from the `... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To add authentication to a FastAPI endpoint, you can use the `HTTPBasic` security scheme. Here’s a c... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To add authentication to a FastAPI endpoint, you can use the `HTTPBasic` security scheme. Here’s how... |
| scrapy+md | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do I define query parameters in the FastAPI reference?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can define query parameters in FastAPI by declaring them in a function signature, either as indi... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You define query parameters in FastAPI by declaring them as function parameters in your endpoint fun... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You define query parameters in FastAPI by declaring them as function parameters in your endpoint fun... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To define query parameters in FastAPI, you can declare them as part of a Pydantic model and use the ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can define query parameters in FastAPI by declaring them as function parameters in your endpoint... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can define query parameters in FastAPI by declaring them as function parameters in your route ha... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can define query parameters in FastAPI by declaring them as function parameters in your endpoint... |

**Q3: How does FastAPI handle JSON encoding and base64 bytes?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | FastAPI handles JSON encoding by using Pydantic models to serialize data into JSON format. For binar... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | FastAPI handles JSON encoding by using Pydantic to serialize data to JSON. When binary data needs to... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | FastAPI handles JSON encoding by using Pydantic to serialize data to JSON. When binary data needs to... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | FastAPI handles JSON encoding by using Pydantic models to serialize data to JSON. When binary data i... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | FastAPI handles JSON encoding by using Pydantic to serialize data to JSON. When binary data needs to... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | FastAPI handles JSON encoding by using Pydantic models to serialize data to JSON. When binary data i... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | FastAPI handles JSON encoding by using Pydantic to serialize data to JSON. When binary data needs to... |

**Q4: How do I use OAuth2 with password flow in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use OAuth2 with password flow in FastAPI, follow these steps:  1. **Import Required Classes**:   ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use OAuth2 with password flow in FastAPI, follow these steps:  1. **Import Required Classes**:   ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use OAuth2 with password flow in FastAPI, follow these steps:  1. **Frontend Input**: The user en... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use OAuth2 with password flow in FastAPI, follow these steps:  1. **Import Required Classes**:   ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use OAuth2 with password flow in FastAPI, follow these steps:  1. **Frontend Input**: The user en... |
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | To use OAuth2 with password flow in FastAPI, follow these steps:  1. Import the necessary modules:  ... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | To use OAuth2 with password flow in FastAPI, you can follow these steps:  1. Import the necessary mo... |

**Q5: How do I use WebSockets in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |

**Q6: How do I define nested Pydantic models for request bodies?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can define nested Pydantic models for request bodies by creating Pydantic classes where each att... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To define nested Pydantic models for request bodies, you create Pydantic classes where each attribut... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can define nested Pydantic models for request bodies by creating a Pydantic model where each att... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To define nested Pydantic models for request bodies, you create Pydantic classes where each attribut... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can define nested Pydantic models for request bodies by creating a Pydantic model where each att... |
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | You can define nested Pydantic models for request bodies by declaring each attribute of a Pydantic m... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | You can define nested Pydantic models for request bodies by declaring each attribute of a Pydantic m... |

**Q7: How do I use middleware in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use middleware in FastAPI, you can add it to your application using the `app.add_middleware()` me... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use middleware in FastAPI, you can add it to your application using the `@app.middleware("http")`... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use middleware in FastAPI, you can add it to your application using the `@app.middleware("http")`... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use middleware in FastAPI, you can add it to your application using the `app.add_middleware()` me... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use middleware in FastAPI, you can add it to your application using the `app.add_middleware()` me... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use middleware in FastAPI, you can add it to your application using the `app.add_middleware()` me... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use middleware in FastAPI, you can add it to your application using the `app.add_middleware()` me... |

**Q8: How do I deploy FastAPI to the cloud?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 4 | 5 | 4 | 4 | 4.2 | You can deploy FastAPI to the cloud by using **FastAPI Cloud** with one command: `fastapi deploy`. A... |
| markcrawl | 4 | 5 | 3 | 4 | 4.0 | You can deploy FastAPI to the cloud by following your cloud provider's guides. Alternatively, you ca... |
| crawl4ai | 4 | 5 | 3 | 4 | 4.0 | You can deploy FastAPI to the cloud by using FastAPI Cloud with **one command** or by following your... |
| crawl4ai-raw | 4 | 5 | 3 | 4 | 4.0 | You can deploy FastAPI to the cloud by using FastAPI Cloud with **one command** or by following your... |
| scrapy+md | 4 | 5 | 3 | 4 | 4.0 | You can deploy FastAPI apps to any cloud provider you choose by following your cloud provider's guid... |
| colly+md | 4 | 5 | 3 | 4 | 4.0 | You can deploy FastAPI apps to any cloud provider by following your cloud provider's guides. Alterna... |
| playwright | 4 | 5 | 3 | 4 | 4.0 | You can deploy FastAPI to the cloud by using FastAPI Cloud with one command, or by following your ch... |

**Q9: How do I handle file uploads in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle file uploads in FastAPI, you can define a path operation function that accepts files as pa... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle file uploads in FastAPI, you can define a file parameter in your path operation function u... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle file uploads in FastAPI, you can define a file parameter in your path operation function u... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To handle file uploads in FastAPI, you can define a path operation function parameter of type `Uploa... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle file uploads in FastAPI, you can use the `UploadFile` class along with the `File` function... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle file uploads in FastAPI, you can define a path operation function parameter of type `Uploa... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To handle file uploads in FastAPI, you can use the `UploadFile` class along with the `File` function... |

**Q10: How do I write async tests for FastAPI applications?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To write async tests for FastAPI applications, you can use the `pytest.mark.anyio` decorator to mark... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To write async tests for FastAPI applications, you can use the `AsyncClient` from the `httpx` librar... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To write async tests for FastAPI applications, you can use the `AsyncClient` from the `httpx` librar... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To write async tests for FastAPI applications, you can use the `AsyncClient` from HTTPX along with p... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To write async tests for FastAPI applications, you can use the `AsyncClient` from HTTPX along with p... |
| scrapy+md | 4 | 5 | 4 | 4 | 4.2 | To write async tests for FastAPI applications, you can use the `TestClient` directly with HTTPX, as ... |
| colly+md | 4 | 5 | 4 | 4 | 4.2 | To write async tests for FastAPI applications, you can use the `TestClient` directly with HTTPX, as ... |

**Q11: How do I use Jinja2 templates in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can use Jinja2 templates in FastAPI by utilizing the `Jinja2Templates` class. First, import it f... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can use Jinja2 templates in FastAPI by utilizing the `Jinja2Templates` class. First, import it f... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |

**Q12: How do I use dependency injection in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use dependency injection in FastAPI, you can declare dependencies in your path operation function... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use dependency injection in FastAPI, you can declare dependencies in your path operation function... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use dependency injection in FastAPI, you can declare dependencies in your path operation function... |
| crawl4ai | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q13: How do I return custom response classes in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can return custom response classes in FastAPI by creating an instance of the desired response cl... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can return custom response classes in FastAPI by creating an instance of the desired response cl... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can return custom response classes in FastAPI by creating an instance of the desired response cl... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can return custom response classes in FastAPI by creating an instance of the desired response cl... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can return custom response classes in FastAPI by creating an instance of the desired response cl... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can return custom response classes in FastAPI by creating an instance of the desired response cl... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can return custom response classes in FastAPI by creating an instance of the desired response cl... |

**Q14: How do I configure CORS in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To configure CORS in FastAPI, you need to use the `CORSMiddleware`. Here are the steps:  1. Import `... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can configure CORS in FastAPI using the `CORSMiddleware`. Here are the steps:  1. Import `CORSMi... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To configure CORS in FastAPI, you need to use the `CORSMiddleware`. Here are the steps:  1. Import `... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To configure CORS in FastAPI, you need to:  1. Import `CORSMiddleware`. 2. Create a list of allowed ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can configure CORS in FastAPI by using the `CORSMiddleware`. Here are the steps:  1. Import `COR... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To configure CORS in FastAPI, you need to use the `CORSMiddleware`. Here are the steps:  1. Import `... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can configure CORS in FastAPI by using the `CORSMiddleware`. Here are the steps:  1. Import `COR... |

**Q15: How do I use path parameters in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can use path parameters in FastAPI by declaring them in the route path using curly braces `{}` a... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can use path parameters in FastAPI by declaring them in the route path using curly braces `{}`. ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can use path parameters in FastAPI by declaring them in the route path using curly braces `{}`. ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use path parameters in FastAPI, you declare them in the route path using curly braces `{}` and de... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can use path parameters in FastAPI by declaring them in the route path using curly braces `{}`. ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use path parameters in FastAPI, you declare them in the route path using curly braces `{}` and de... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can use path parameters in FastAPI by declaring them in the route path using curly braces `{}`. ... |

**Q16: How do I run FastAPI with Docker?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | To run FastAPI with Docker, you can use the following command after building your Docker image:  ```... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | To run FastAPI with Docker, you can use the following command after building your Docker image:  ```... |
| crawlee | 3 | 5 | 4 | 4 | 4.0 | To run FastAPI with Docker, you need to build a Docker image using a Dockerfile that specifies the n... |
| playwright | 3 | 4 | 4 | 4 | 3.8 | To run FastAPI with Docker, you need to build a Docker image using a Dockerfile. Here’s a basic outl... |
| markcrawl | 3 | 4 | 3 | 4 | 3.5 | To run FastAPI with Docker, you can use the following command in your Dockerfile:  ``` CMD ["fastapi... |
| scrapy+md | 2 | 4 | 3 | 3 | 3.0 | To run FastAPI with Docker, you can use the following command in your Dockerfile:  ``` CMD ["fastapi... |
| colly+md | 2 | 4 | 3 | 3 | 3.0 | To run FastAPI with Docker, you can use the following command in your Dockerfile:  ``` CMD ["fastapi... |

**Q17: How do I configure FastAPI application settings?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can configure FastAPI application settings by creating a class that inherits from `BaseSettings`... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can configure FastAPI application settings by creating a subclass of `BaseSettings` from the `py... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can configure FastAPI application settings by creating a subclass of `BaseSettings` from the `py... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can configure FastAPI application settings by creating a class that inherits from `BaseSettings`... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can configure FastAPI application settings by creating a subclass of `BaseSettings` from `pydant... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can configure FastAPI application settings by creating a class that inherits from `BaseSettings`... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can configure FastAPI application settings by creating a subclass of `BaseSettings` from `pydant... |

**Q18: How do I use background tasks in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use background tasks in FastAPI, you need to import `BackgroundTasks` and define a parameter of t... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can use background tasks in FastAPI by declaring a parameter in a path operation function or dep... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can use background tasks in FastAPI by declaring a parameter in a path operation function or dep... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use background tasks in FastAPI, follow these steps:  1. Import `BackgroundTasks` from `fastapi`.... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use background tasks in FastAPI, you need to follow these steps:  1. Import `BackgroundTasks` fro... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use background tasks in FastAPI, follow these steps:  1. Import `BackgroundTasks` from `fastapi`.... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use background tasks in FastAPI, you need to follow these steps:  1. Import `BackgroundTasks` fro... |

**Q19: What are the first steps to create a FastAPI application?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The first steps to create a FastAPI application are:  1. Import `FastAPI`:    ```python    from fast... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The first steps to create a FastAPI application are:  1. Import `FastAPI`:    ```python    from fast... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | 1. Import `FastAPI` by adding `from fastapi import FastAPI`. 2. Create a FastAPI instance with `app ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The first steps to create a FastAPI application are:  1. **Install FastAPI**: Create a virtual envir... |
| markcrawl | 4 | 5 | 4 | 5 | 4.5 | The first steps to create a FastAPI application are:  1. Install FastAPI using pip:    ```    $ pip ... |
| scrapy+md | 4 | 5 | 4 | 5 | 4.5 | The first steps to create a FastAPI application are:  1. Install FastAPI using pip:    ```    $ pip ... |
| colly+md | 4 | 5 | 4 | 5 | 4.5 | 1. Install FastAPI using pip: `pip install "fastapi[standard]"`. 2. Create a directory for your app ... |

**Q20: How do I handle errors and exceptions in FastAPI?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle errors and exceptions in FastAPI, you can use the `exception_handler` decorator to add cus... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | In FastAPI, you can handle errors and exceptions by using the built-in `HTTPException` to show error... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | In FastAPI, you can handle errors and exceptions by using the built-in `HTTPException` to raise erro... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | In FastAPI, you can handle errors and exceptions by using exception handlers. You can add an excepti... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In FastAPI, you can handle errors and exceptions by using exception handlers. You can add an excepti... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | In FastAPI, you can handle errors and exceptions by using the `HTTPException` class to raise excepti... |
| crawlee | 4 | 5 | 4 | 4 | 4.2 | In FastAPI, you can handle errors and exceptions by using the `HTTPException` class to raise excepti... |

</details>

## python-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 4.68 | 4.53 | 4.37 | 4.53 | 4.53 ±0.51 |
| crawl4ai | 4.68 | 4.53 | 4.37 | 4.53 | 4.53 ±0.51 |
| crawl4ai-raw | 4.63 | 4.58 | 4.37 | 4.47 | 4.51 ±0.48 |
| crawlee | 4.58 | 4.37 | 4.16 | 4.37 | 4.37 ±0.57 |
| scrapy+md | 4.47 | 4.26 | 4.00 | 4.21 | 4.24 ±0.58 |
| playwright | 4.47 | 4.26 | 4.00 | 4.21 | 4.24 ±0.59 |
| colly+md | 4.37 | 4.11 | 3.84 | 4.05 | 4.09 ±0.62 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for python-docs</summary>

**Q1: What new features were added in Python 3.10?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Python 3.10 introduced several new features, including:  1. Parenthesized context managers. 2. Bette... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | New features added in Python 3.10 include:  - Parenthesized context managers - Better error messages... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | New features added in Python 3.10 include:  - Parenthesized context managers - Better error messages... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | New features added in Python 3.10 include:  - Parenthesized context managers - Better error messages... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | New features added in Python 3.10 include:  - Parenthesized context managers - Better error messages... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | New features added in Python 3.10 include:  - Parenthesized context managers - Better error messages... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | New features added in Python 3.10 include:  - Parenthesized context managers - Better error messages... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What does the term 'decorator' mean in Python?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In Python, a 'decorator' is a function that returns another function, usually applied as a function ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | A decorator in Python is a function that returns another function, usually applied as a function tra... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | A decorator in Python is a function that returns another function, usually applied as a transformati... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | In Python, a 'decorator' is a function that returns another function, typically used to modify or en... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In Python, a 'decorator' is a function that modifies or enhances another function or method. It allo... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In Python, a 'decorator' is a function that modifies or enhances another function or method. It is a... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | In Python, a 'decorator' is a function that modifies or enhances another function or method. It allo... |

**Q3: How do I report a bug in Python?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To report a bug in Python, follow these steps:  1. **Check if the bug has already been reported**: U... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To report a bug in Python, submit an issue via the GitHub issues tracker at [https://github.com/pyth... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To report a bug in Python, submit an issue via the GitHub issues tracker at [https://github.com/pyth... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To report a bug in Python, use the issue tracker at <https://github.com/python/cpython/issues>.... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To report a bug in Python, submit an issue via the GitHub issues tracker at <https://github.com/pyth... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To report a bug in Python, follow these steps:  1. Check if the problem has already been reported by... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To report a bug in Python, submit an issue via the GitHub issues tracker at <https://github.com/pyth... |

**Q4: What is Python's glossary definition of a generator?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | A generator is a function which returns an iterator. It looks like a normal function except that val... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| colly+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q5: What is the Python module index?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The Python module index is a structured list of modules, classes, and functions available in Python,... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The Python module index is a list of Python modules that can be accessed through the documentation, ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The Python module index is a list of Python modules that can be accessed through the documentation, ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The Python module index is a section in the documentation that lists all the available Python module... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The Python module index is a list of Python modules that are available for use, providing a way to n... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The Python module index is a section of the Python documentation that provides an organized list of ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The Python module index is a list of Python modules that are available in the Python Standard Librar... |

**Q6: What does the term 'iterable' mean in Python?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In Python, an 'iterable' is an object capable of returning its members one at a time. Examples inclu... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | An 'iterable' in Python is an object capable of returning its members one at a time. Examples includ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | In Python, an 'iterable' is an object capable of returning its members one at a time. Examples inclu... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | An 'iterable' in Python is an object capable of returning its members one at a time. Examples includ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | An 'iterable' in Python is an object capable of returning its members one at a time. Examples includ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | An 'iterable' in Python is an object capable of returning its members one at a time. Examples includ... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: How do I install and configure Python on my system?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| colly+md | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: How do I use the os module for file and directory operations?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the `os` module for file and directory operations, you can follow these steps:  1. **Change D... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `os` module for file and directory operations, you can utilize various functions provided... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `os` module for file and directory operations, you can utilize various functions provided... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `os` module for file and directory operations, you can utilize various functions provided... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `os` module for file and directory operations, you can follow these guidelines:  1. **Rea... |
| crawl4ai-raw | 4 | 5 | 4 | 4 | 4.2 | To use the `os` module for file and directory operations, you can utilize various functions provided... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q9: How do I use pathlib for filesystem paths in Python?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use `pathlib` for filesystem paths in Python, you can follow these steps:  1. **Import the module... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use `pathlib` for filesystem paths in Python, you can follow these basic steps:  1. **Import the ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use `pathlib` for filesystem paths in Python, you can follow these basic steps:  1. **Import the ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can use the `pathlib` module in Python to work with filesystem paths by importing it and creatin... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use `pathlib` for filesystem paths in Python, you can follow these steps:  1. **Import the `pathl... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use `pathlib` for filesystem paths in Python, you can follow these steps:  1. **Import the module... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use `pathlib` for filesystem paths in Python, you can instantiate `Path` objects, which represent... |

**Q10: How do I parse and generate JSON in Python?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To parse and generate JSON in Python, you can use the `json` module.   To generate (encode) JSON fro... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To parse and generate JSON in Python, you can use the `json` module.   To generate JSON (serialize),... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To parse and generate JSON in Python, you can use the `json` module.   To generate JSON (serialize),... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To parse and generate JSON in Python, you can use the `json` module.   To generate (encode) JSON fro... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To parse and generate JSON in Python, you can use the `json` module. To generate JSON, use `json.dum... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To parse JSON in Python, you can use the `json.loads()` function for strings or `json.load()` for fi... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To parse and generate JSON in Python, you can use the `json` module. To generate JSON, use `json.dum... |

**Q11: How do I use asyncio for async programming in Python?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use `asyncio` for asynchronous programming in Python, you can follow these steps:  1. **Define an... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use asyncio for async programming in Python, you can follow these steps:  1. **Define Coroutines*... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use asyncio for async programming in Python, you can follow these steps:  1. **Define Coroutines*... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use asyncio for async programming in Python, you can follow these steps:  1. **Define Coroutines*... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use asyncio for async programming in Python, you can follow these steps:  1. **Define Coroutines*... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use `asyncio` for asynchronous programming in Python, you can follow these steps:  1. **Import th... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use asyncio for async programming in Python, you can follow these steps:  1. **Define Coroutines*... |

**Q12: How do I use type hints and the typing module in Python?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use type hints and the `typing` module in Python, you can annotate function parameters and return... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use type hints in Python, you can annotate function parameters and return types with the expected... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use type hints in Python, you can annotate function parameters and return types with specific typ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use type hints in Python, you can annotate function parameters and return types with the expected... |
| crawl4ai-raw | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q13: How do I work with dates and times using the datetime module?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To work with dates and times using the `datetime` module, you can use the following classes and meth... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To work with dates and times using the `datetime` module, you can utilize its classes and methods fo... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To work with dates and times using the `datetime` module, you can utilize its classes and methods fo... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To work with dates and times using the `datetime` module, you can follow these steps:  1. **Import t... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To work with dates and times using the `datetime` module, you can utilize its classes for manipulati... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To work with dates and times using the `datetime` module, you can use the following classes and meth... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The `datetime` module provides classes for manipulating dates and times, supporting date and time ar... |

**Q14: How do I use Python's logging module?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use Python's logging module, you can follow these basic steps:  1. **Import the logging module**:... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use Python's logging module, you can follow these steps:  1. **Import the logging module**: Start... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use Python's logging module, you can follow these steps:  1. **Import the logging module**: Start... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use Python's logging module, you can follow these steps:  1. **Import the logging module**: Start... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q15: How do I write unit tests with the unittest module?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To write unit tests with the `unittest` module, follow these steps:  1. **Import the module**: Start... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To write unit tests with the `unittest` module, follow these guidelines:  1. **Naming Conventions**:... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To write unit tests with the `unittest` module, follow these guidelines:  1. **Naming Conventions**:... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To write unit tests with the `unittest` module, follow these guidelines:  1. **Naming**: Name your t... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To write unit tests with the `unittest` module, follow these steps:  1. **Create a Test Case Class**... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To write unit tests with the `unittest` module, follow these guidelines:  1. **Naming**: Name the te... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To write unit tests with the `unittest` module, follow these steps:  1. **Create a Test Case**: Subc... |

**Q16: How do I use Python dataclasses?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use Python dataclasses, you can follow these steps:  1. Import the `dataclass` decorator from the... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use Python dataclasses, you can follow these steps:  1. Import the `dataclass` decorator from the... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q17: How do I use itertools for efficient iteration in Python?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can use the `itertools` module in Python, which provides a set of fast, memory-efficient tools f... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can use the `itertools` module in Python, which provides a set of fast, memory-efficient tools f... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q18: How does Python's data model work with special methods?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Python's data model allows classes to implement certain operations through special methods, enabling... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Python's data model allows classes to implement certain operations through special methods, enabling... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Python's data model allows classes to implement certain operations through special methods, enabling... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Python's data model allows classes to implement certain operations through special methods, enabling... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q19: What are Python's compound statements like if, for, and with?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Python's compound statements include structures that can contain other statements, such as `if`, `fo... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Python's compound statements, such as `if`, `for`, and `with`, are constructs that contain groups of... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Python's compound statements, such as `if`, `for`, and `with`, are constructs that contain groups of... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Python's compound statements, such as `if`, `for`, and `with`, consist of one or more clauses that c... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Python's compound statements include constructs such as `if_stmt`, `for_stmt`, `with_stmt`, `functio... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Python's compound statements include `if`, `for`, and `with`, which control the execution of other s... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | Python's compound statements include `if`, `for`, `with`, `function_def`, `class_def`, `try_stmt`, a... |

</details>

## react-dev

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawlee | 5.00 | 5.00 | 4.94 | 5.00 | 4.98 ±0.03 |
| playwright | 5.00 | 5.00 | 4.94 | 5.00 | 4.98 ±0.03 |
| scrapy+md | 4.88 | 4.81 | 4.75 | 4.81 | 4.81 ±0.37 |
| colly+md | 4.88 | 4.81 | 4.69 | 4.81 | 4.80 ±0.37 |
| crawl4ai | 4.69 | 4.62 | 4.31 | 4.56 | 4.55 ±0.50 |
| crawl4ai-raw | 4.69 | 4.62 | 4.31 | 4.56 | 4.55 ±0.50 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for react-dev</summary>

**Q1: How do I manage state in a React component?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You manage state in a React component by using the `useState` Hook. This Hook allows you to declare ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can manage state in a React component by using the `useState` Hook. This Hook allows you to decl... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In a React component, you manage state by using the `useState` hook to create state variables. You c... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can manage state in a React component by using the `useState` Hook. This Hook allows you to decl... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How does the useEffect hook work in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |

**Q3: How do I create and use context in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |

**Q4: What is JSX and how does React use it?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup inside Jav... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup inside a J... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within a J... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |

**Q5: How do I render lists and use keys in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use the `map()` function to transform an array of data into an arr... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript's `map()` method to transform an array of data into... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript's `map()` method to transform an array of data into... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use the `map()` function to transform an array of data into an arr... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use the JavaScript `map()` function to transform an array of data ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |

**Q6: How do I use the useRef hook in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, you can follow these steps:  1. Import `useRef` from React. 2. Ca... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, you can follow these steps:  1. Import the `useRef` hook from Rea... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, call it at the top level of your component to declare a ref. For ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |

**Q7: How do I pass props between React components?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You pass props between React components by giving them as attributes to the child component in the p... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You pass props between React components by giving them as attributes to the child component in the p... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You pass props between React components by giving them as attributes in the JSX of the parent compon... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You pass props between React components by giving them as attributes in the JSX of the parent compon... |
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | React components use _props_ to communicate with each other. A parent component can pass information... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | React components use _props_ to communicate with each other. A parent component can pass information... |
| colly+md | 5 | 5 | 4 | 5 | 4.8 | React components use *props* to communicate with each other. A parent component can pass information... |

**Q8: How do I conditionally render content in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax like `if` statements, the con... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax like `if` statements, the con... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax like `if` statements, the con... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |

**Q9: What is the useMemo hook for in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is for caching the result of a calculation between re-renders, allowing ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is for caching the result of a calculation between re-renders, allowing ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |

**Q10: How do I use the useState hook in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, call it at the top level of your component to declare a state v... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, you can follow this syntax:  ```javascript const [state, setSta... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, you can follow this syntax:  ```javascript const [state, setSta... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, call it at the top level of your component to declare a state v... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, call it at the top level of your component to declare a state v... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, you can follow this syntax:  ```javascript const [state, setSta... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, call it at the top level of your component to declare a state v... |

**Q11: How do I use the useCallback hook in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow this syntax:  ```javascript const cachedFn = ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow this syntax:  ```javascript const cachedFn = ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow this syntax:  ```javascript const cachedFn = ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow this syntax:  ```javascript const cachedFn = ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow this syntax:  ```javascript const cachedFn = ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow these steps:  1. Import `useCallback` from Re... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow this syntax:  ```javascript const cachedFn = ... |

**Q12: How do I use the useReducer hook in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. Import `useReducer` from React. 2. De... |

**Q13: How do I handle events like clicks in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Declare an event handler ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can handle events like clicks in React by declaring event handler functions inside your componen... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can handle events like clicks in React by declaring event handler functions inside your componen... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Declare an event handler ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Define an event handler f... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In React, you handle events like clicks by defining an event handler function inside your component ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Define an event handler f... |

**Q14: What is the Suspense component in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows developers to declaratively specify the loading state for par... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to declaratively specify a loading state for a part of th... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to declaratively specify a loading state for a part of th... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows developers to declaratively specify the loading state for par... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows developers to declaratively specify the loading state for par... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to declaratively specify the loading state for a part of ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows developers to declaratively specify the loading state for par... |

**Q15: How do I add interactivity to React components?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can add interactivity to React components by using state to manage data that changes over time a... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To add interactivity to React components, you can use state, which allows components to update in re... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can add interactivity to React components by using state, which allows components to update thei... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can add interactivity to React components by using state to manage data that changes over time a... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can add interactivity to React components by using state to manage data that changes over time a... |
| crawl4ai | 4 | 5 | 3 | 4 | 4.0 | You can add interactivity to React components by passing new data in response to user interactions, ... |
| crawl4ai-raw | 4 | 5 | 3 | 4 | 4.0 | You can add interactivity to React components by passing new data in response to user interactions, ... |

**Q16: How do I install and set up a new React project?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, follow these steps:  1. **Install React and React DOM**: ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, follow these steps:  1. **Install React and ReactDOM**:  ... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | To install and set up a new React project, you can follow these steps:  1. **Install React and React... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | To install and set up a new React project, you can follow these steps:  1. **Install React and React... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## wikipedia-python

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawlee | 4.40 | 4.10 | 3.80 | 4.10 | 4.10 ±0.90 |
| crawl4ai-raw | 4.20 | 3.90 | 3.40 | 3.80 | 3.83 ±0.91 |
| crawl4ai | 4.20 | 3.80 | 3.40 | 3.80 | 3.80 ±0.93 |
| **markcrawl** | 4.00 | 3.50 | 3.00 | 3.50 | 3.50 ±0.98 |
| scrapy+md | 3.80 | 3.20 | 2.60 | 3.20 | 3.20 ±0.96 |
| playwright | 3.80 | 3.20 | 2.60 | 3.20 | 3.20 ±0.96 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for wikipedia-python</summary>

**Q1: Who created the Python programming language?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Guido van Rossum created the Python programming language.... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The Python programming language was created by Guido van Rossum.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The Python programming language was created by Guido van Rossum.... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The Python programming language was created by Guido van Rossum.... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The Python programming language was created by Guido van Rossum.... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The Python programming language was created by Guido van Rossum.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What is the Python Software Foundation?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The Python Software Foundation is an organization that supports the development of the Python progra... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization established on March 6, 2... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization established on March 6, 2... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization established on March 6, 2... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The Python Software Foundation is the organization that supports the development and maintenance of ... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: Who is Guido van Rossum?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Guido van Rossum is the designer of Python and was the lead developer of the language until July 201... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Guido van Rossum is a Dutch programmer, born on 31 January 1956, known for creating the Python progr... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Guido van Rossum is a Dutch programmer, born on 31 January 1956, known for creating the Python progr... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Guido van Rossum is the designer of Python and was the lead developer of the language until July 201... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Guido van Rossum is a Dutch programmer, born on 31 January 1956, known for creating the Python progr... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Guido van Rossum is the designer of Python and was involved in its development at Centrum Wiskunde &... |

**Q4: What is CPython and how does it work?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | CPython is the reference implementation of Python, written in C and compliant with the C11 standard ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into an... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into an... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into in... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into an... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | CPython is the reference implementation of the Python programming language, written in C and Python.... |

**Q5: How does Python compare to other programming languages?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: What is NumPy and what is it used for?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | NumPy is a library for the Python programming language that adds support for large, multi-dimensiona... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | NumPy is a library for Python that provides support for large, multi-dimensional arrays and matrices... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | NumPy is a library in Python that provides support for large, multi-dimensional arrays and matrices,... |
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | NumPy is a third-party library in Python that is frequently used for scientific scripting, particula... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | NumPy is a third-party library in Python that is frequently used for scientific scripting, particula... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: What is SQLAlchemy and how is it used with Python?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: What is metaprogramming in computer science?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Metaprogramming in computer science is the practice of writing programs that write or manipulate oth... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Metaprogramming in computer science is the practice of writing programs that write or manipulate oth... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Metaprogramming in computer science is the practice of writing programs that write or manipulate oth... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q9: What are list comprehensions in programming?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q10: How does memory management work in programming?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Memory management in programming involves dynamically allocating portions of memory to programs as r... |
| crawl4ai-raw | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## stripe-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 4.89 | 4.83 | 4.78 | 4.83 | 4.83 ±0.33 |
| crawl4ai-raw | 4.89 | 4.83 | 4.78 | 4.83 | 4.83 ±0.33 |
| **markcrawl** | 4.72 | 4.67 | 4.50 | 4.67 | 4.64 ±0.43 |
| colly+md | 4.72 | 4.67 | 4.44 | 4.61 | 4.61 ±0.45 |
| playwright | 4.61 | 4.56 | 4.28 | 4.44 | 4.47 ±0.50 |
| crawlee | 4.61 | 4.50 | 4.11 | 4.44 | 4.42 ±0.52 |
| scrapy+md | 4.33 | 4.00 | 3.67 | 4.00 | 4.00 ±0.66 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for stripe-docs</summary>

**Q1: How do I create a payment intent with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you need to make a request to the Stripe API. Here’s a basic ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you need to make a request to the Stripe API. Here’s a basic ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you can use the following cURL command:  ``` curl https://api... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you can use the following cURL command:  ``` curl https://api... |
| markcrawl | 5 | 5 | 4 | 5 | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | To create a PaymentIntent with Stripe, you can use the following cURL command:  ``` curl https://api... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do I handle webhooks from Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. Set up an HTTP handler in your application t... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. **Create a Webhook Endpoint**: Set up an end... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. **Create a webhook endpoint** on your server... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, you need to create a webhook endpoint that receives POST requests wi... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. Create a webhook endpoint on your server to ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. **Create a webhook endpoint** on your server... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. Create a webhook endpoint on your server to ... |

**Q3: How do I set up Stripe subscriptions?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To set up Stripe subscriptions, you need to:  1. Create a [Product](https://api/products) to define ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To set up Stripe subscriptions, follow these steps:  1. Install the Stripe client of your choice (e.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To set up Stripe subscriptions, follow these steps:  1. Install the Stripe client of your choice (e.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: How do I authenticate with the Stripe API?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You authenticate with the Stripe API by using your account’s API keys. Ensure that your request incl... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To authenticate with the Stripe API, you need to use API keys. You can view and manage your API keys... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To authenticate with the Stripe API, you need to use API keys. You can view and manage your API keys... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To authenticate with the Stripe API, log in to your Stripe user account using the command `stripe lo... |
| crawlee | 4 | 5 | 4 | 4 | 4.2 | To authenticate with the Stripe API, log in and authenticate your Stripe user account using the comm... |
| colly+md | 4 | 5 | 4 | 4 | 4.2 | To authenticate with the Stripe API, log in to your Stripe user account to generate a set of restric... |
| playwright | 4 | 5 | 4 | 4 | 4.2 | To authenticate with the Stripe API, log in and authenticate your Stripe user account using the comm... |

**Q5: How do I handle errors in the Stripe API?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should implement exception handling in your code. Use the St... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should:  1. Write code that gracefully handles all possible ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should:  1. Write code that gracefully handles all possible ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should check for immediate errors returned by Stripe.js, suc... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should:  1. **Understand HTTP Response Codes**: Use the `2xx... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should check for errors returned by Stripe.js, which will pr... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: How do I process refunds with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you need to report the refund after the original payment is successf... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can use the Stripe API or Dashboard. For API refunds, you need t... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can use the Stripe API or Dashboard. For API refunds, you need t... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can use the API to create a refund by sending a request to the r... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, go to the Payments page in the Stripe Dashboard, select the payments... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can issue a refund through the Dashboard or API. The customer mu... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, go to the Payments page in the Stripe Dashboard. Select the payments... |

**Q7: How do I use Stripe checkout for payments?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, you can redirect to a Stripe-hosted payment page using the Chec... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, you can redirect to a Stripe-hosted payment page using the Chec... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, you can build a low-code payment form and embed it on your site... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: How do I test Stripe payments in development?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can test Stripe payments in development by using test cards, test clocks, and the Stripe CLI to ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, use the following steps:  1. Utilize the sandbox environment... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, use the following steps:  1. Utilize the sandbox environment... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following methods:  1. **Sandbox Testing**: ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following steps:  1. Set up your development... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, use a sandbox environment to simulate real-world conditions.... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following steps:  1. Set up your development... |

**Q9: What are Stripe Connect and platform payments?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to manage payments and facilitate... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to manage payments and facilitate... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to route payments between themsel... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to route payments between themsel... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to route payments between themsel... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q10: How do I set up usage-based billing with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To set up usage-based billing with Stripe, you need to follow these major components:  1. **Ingestio... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To set up usage-based billing with Stripe, follow these steps:  1. **Create a Product**: Go to the P... |
| colly+md | 5 | 5 | 4 | 5 | 4.8 | To set up usage-based billing with Stripe, you can follow the guide on setting up usage-based billin... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q11: How do I manage Stripe API keys?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Never put secret API keys in source co... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Access Management**: If you can't view... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Access Management**: If you can't view... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys safely, treat secret keys and restricted API keys as sensitive and do not ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Never put secret API keys in source co... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Never put secret API keys in source co... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Never put secret API keys in source co... |

**Q12: How do I handle Stripe rate limits?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle Stripe rate limits, watch for `429` status codes and implement a retry mechanism. Retry th... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle Stripe rate limits, make your requests less frequently if you begin to receive `429` HTTP ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle Stripe rate limits, make your requests less frequently if you begin to receive `429` HTTP ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To handle Stripe rate limits, you should:  1. Reduce the frequency of your requests if you receive `... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle Stripe rate limits, if you begin to receive `429` HTTP errors in your testing environments... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | To handle Stripe rate limits, if you begin to receive `429` HTTP errors in your testing environments... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | To handle Stripe rate limits, if you begin to receive `429` HTTP errors in your testing environments... |

**Q13: How do I use metadata with Stripe objects?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects to store additional information as key-value pairs. This al... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value pairs to updateable objects such as ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value pairs to updateable objects such as ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value pairs to the object during requests,... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by adding it to common requests, such as processing payment... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value data to updateable objects such as A... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value data to updateable objects such as A... |

**Q14: How do I set up Apple Pay with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. Create a Stripe account. 2. Register for an... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. Create a Stripe account. 2. Register for an... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. Enroll in the Apple Developer Program. 2. S... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q15: How do I issue cards with Stripe Issuing?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, follow these steps:  1. Sign up for a Stripe account and activat... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, you first need to create a cardholder using the Stripe Issuing A... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, you can use the Stripe Issuing API. Specifically, you need to re... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, reference the cardholder ID and use the Stripe Issuing API. You ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, use the Stripe Issuing API to create a card for a cardholder by ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, reference the cardholder ID and use the Stripe Issuing API. You ... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q16: How do I recover failed subscription payments?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you can set up a webhook endpoint to listen for the `custom... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, set up a webhook endpoint to listen for the `customer.subsc... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, set up a webhook endpoint to listen for the `customer.subsc... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can recover failed subscription payments using Stripe's revenue recovery features, which include... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, set up a webhook endpoint to listen for the `customer.subsc... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you can enable notifications to inform customers when their... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, set up a webhook endpoint to listen for the `customer.subsc... |

**Q17: How does Stripe handle tax calculation for billing?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing through two main options: Stripe Tax and tax rates.   1. ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing by automatically determining the customer's location and ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing by automatically determining the customer's location and ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing through its Stripe Tax product, which automatically calcu... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Stripe automatically calculates and collects the correct amount of tax at checkout based on the cust... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Stripe calculates tax on transactions by applying tax rates based on each customer’s location and th... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Stripe automatically calculates and collects the correct amount of tax at checkout based on the cust... |

**Q18: How do I migrate data to Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, follow these steps:  1. Review Stripe’s migration documentation. 2. Conta... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, follow these steps:  1. Review Stripe’s migration documentation. 2. Conta... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, you should develop a data migration plan starting with new customers, the... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, you should develop a data migration plan starting with new customers, aim... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | To migrate data to Stripe, you should develop a data migration plan starting with new customers, aim... |
| markcrawl | 4 | 5 | 4 | 5 | 4.5 | To migrate data to Stripe, you need to follow these steps:  1. **Contact Stripe**: Start the migrati... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## blog-engineering

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 4.50 | 4.50 | 4.12 | 4.12 | 4.31 ±0.75 |
| colly+md | 4.50 | 4.38 | 4.12 | 4.25 | 4.31 ±0.89 |
| crawlee | 4.25 | 4.12 | 3.50 | 3.75 | 3.91 ±0.81 |
| playwright | 4.25 | 4.00 | 3.38 | 3.75 | 3.84 ±0.88 |
| crawl4ai-raw | 4.12 | 3.88 | 3.38 | 3.50 | 3.72 ±0.96 |
| scrapy+md | 4.12 | 3.75 | 3.38 | 3.50 | 3.69 ±0.98 |
| crawl4ai | 4.12 | 3.75 | 3.25 | 3.50 | 3.66 ±1.01 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for blog-engineering</summary>

**Q1: How does GitHub handle Kubernetes at scale?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | GitHub handles Kubernetes at scale by deploying the code that powers `github.com` and `api.github.co... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | GitHub handles Kubernetes at scale by using a multi-cluster, multi-region topology as the base layer... |
| crawl4ai | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| scrapy+md | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| crawlee | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How does GitHub protect against DDoS attacks?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | GitHub protects against DDoS attacks by investigating the use of automated intervention through thei... |
| crawl4ai-raw | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How does GitHub handle MySQL database operations?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | GitHub uses MySQL as its main datastore for metadata, including Issues, Pull Requests, and Comments.... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | GitHub uses MySQL to store vast amounts of relational data and has implemented automation for schema... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | GitHub uses MySQL to store vast amounts of relational data and has implemented automation for schema... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | GitHub uses MySQL as its main datastore to store metadata, including Issues, Pull Requests, and Comm... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | GitHub uses MySQL to store vast amounts of relational data and has implemented automation for schema... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | GitHub handles MySQL database operations by automating schema migrations through a combination of to... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | GitHub uses MySQL to store vast amounts of relational data and has implemented automation for schema... |

**Q4: How does GitHub handle load balancing?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | GitHub handles load balancing using GLB, a scalable load balancing solution that operates as a Layer... |
| crawl4ai | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |

**Q5: What is GitHub's approach to platform security?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | GitHub's approach to platform security involves integrating engineering and security teams to defend... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | GitHub's approach to platform security involves integrating engineering and security teams to defend... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | GitHub's approach to platform security includes supporting strong authentication options, evaluating... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | GitHub's approach to platform security includes bringing engineering and security teams together, im... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | GitHub's approach to platform security involves bringing together engineering and security teams to ... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | GitHub's approach to platform security involves bringing together engineering and security teams to ... |
| markcrawl | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |

**Q6: How does GitHub optimize its architecture?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | GitHub optimizes its architecture by investing in physical infrastructure to improve redundancy and ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | GitHub optimizes its architecture by migrating infrastructure to Azure for scalability, breaking apa... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | GitHub optimizes its architecture by migrating infrastructure to Azure for scalability, breaking apa... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | GitHub optimizes its architecture through various methods, including improving the speed of diff pag... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | GitHub optimizes its architecture by migrating infrastructure to Azure for scalability, breaking apa... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | GitHub optimizes its architecture by using GraphQL for mobile applications to reduce over-fetching a... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | GitHub optimizes its architecture by migrating infrastructure to Azure for scalability, breaking apa... |

**Q7: What engineering principles does GitHub follow?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 5 | 5 | 5 | 5 | 5.0 | GitHub follows engineering principles that include making informed, inclusive, and scalable decision... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | GitHub follows engineering principles that emphasize collaboration, informed decision-making, inclus... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | GitHub follows engineering principles that include making informed, inclusive, and scalable decision... |
| markcrawl | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: How does GitHub improve user experience?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | GitHub improves user experience by enhancing accessibility for users of assistive technology, provid... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | GitHub improves user experience by enhancing accessibility for users of assistive technology, provid... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | GitHub improves user experience by incorporating user feedback to release new features and improveme... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | GitHub improves user experience by making enhancements to the way users of assistive technology can ... |
| markcrawl | 4 | 5 | 4 | 4 | 4.2 | GitHub improves user experience by automatically logging users into the support site, creating an ac... |
| crawlee | 4 | 4 | 3 | 4 | 3.8 | GitHub improves user experience by enhancing navigation in its mobile app, as indicated by the smoot... |
| playwright | 4 | 4 | 3 | 4 | 3.8 | GitHub improves user experience by enhancing navigation in its mobile app, as indicated by the smoot... |

</details>

## Methodology

- **Answer generation:** `gpt-4o-mini` with temperature=0, max_tokens=500
- **Answer judging:** `gpt-4o-mini` scores correctness, relevance, completeness, usefulness (1-5)
- **Retrieval:** Top-10 chunks by cosine similarity (same as retrieval benchmark)
- **Chunking:** Markdown-aware, 400 word max, 50 word overlap
- **Embedding:** `text-embedding-3-small`
- **Same pipeline for all tools** — only crawler output quality varies

## See also

- [RETRIEVAL_COMPARISON.md](RETRIEVAL_COMPARISON.md) — retrieval doesn't differ much, but answers do
- [COST_AT_SCALE.md](COST_AT_SCALE.md) — what the quality gap costs at scale
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup and fairness decisions

