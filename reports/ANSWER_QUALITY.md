# End-to-End RAG Answer Quality
<!-- style: v2, 2026-04-13 -->

All crawlers produce similar LLM answer quality (4.26-4.41 out of 5). scrapy+md leads slightly at 4.41; markcrawl ranks 5th at 4.30 — a 2.5% gap from the best. The gaps are small but consistent.

Each tool's crawled content is chunked, embedded, retrieved (top-10),
and sent to `gpt-4o-mini` to generate an answer. Answers are scored by
`gpt-4o-mini` on correctness, relevance, completeness, and usefulness (1-5 each).

**Scoring scale:** 1 = wrong/irrelevant, 2 = partially relevant, 3 = acceptable, 4 = good, 5 = excellent/complete. Scores are averaged across all queries per tool. An overall score above 4.0 indicates consistently good answers.

## Summary (93 queries across 8 sites)

| Tool | Correctness | Relevance | Completeness | Usefulness | **Overall** | Avg tokens/query |
|---|---|---|---|---|---|---|
| **markcrawl** | 4.47 | 4.39 | 4.09 | 4.24 | **4.30** | 2,336 |
| crawl4ai | 4.45 | 4.34 | 4.01 | 4.25 | **4.26** | 2,153 |
| crawl4ai-raw | 4.48 | 4.40 | 4.09 | 4.28 | **4.31** | 2,156 |
| scrapy+md | 4.58 | 4.48 | 4.19 | 4.39 | **4.41** | 2,295 |
| crawlee | 4.52 | 4.42 | 4.10 | 4.29 | **4.33** | 2,296 |
| colly+md | 4.49 | 4.38 | 4.03 | 4.26 | **4.29** | 2,339 |
| playwright | 4.56 | 4.46 | 4.15 | 4.34 | **4.38** | 2,294 |

> **Column definitions:** All scores are 1-5 averages across queries, judged by `gpt-4o-mini`. **Correctness** = factual accuracy. **Relevance** = answers the question asked. **Completeness** = covers all aspects. **Usefulness** = practical value to the user. **Overall** = mean of the four dimensions. **Avg tokens/query** = estimated input tokens per query (chunk words x 1.33).

## quotes-toscrape

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 4.58 | 4.33 | 3.83 | 4.17 | 4.23 |
| crawl4ai | 4.67 | 4.83 | 4.42 | 4.58 | 4.62 |
| crawl4ai-raw | 4.58 | 4.75 | 4.42 | 4.58 | 4.58 |
| scrapy+md | 4.83 | 4.75 | 4.42 | 4.75 | 4.69 |
| crawlee | 4.50 | 4.67 | 4.08 | 4.50 | 4.44 |
| colly+md | 4.50 | 4.75 | 4.17 | 4.50 | 4.48 |
| playwright | 4.58 | 4.75 | 4.08 | 4.58 | 4.50 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for quotes-toscrape</summary>

**Q1: What did Albert Einstein say about thinking and the world?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| crawl4ai | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| crawl4ai-raw | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| scrapy+md | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| crawlee | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| colly+md | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |
| playwright | 5.0 | Albert Einstein said, "The world as we have created it is a process of our thinking. It cannot be ch... |

**Q2: Which quotes are tagged with 'change'?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai | 3.2 | The quotes tagged with 'inspirational' are:  1. “There are only two ways to live your life. One is a... |
| crawl4ai-raw | 3.2 | The quotes tagged with 'inspirational' are:  1. “There are only two ways to live your life. One is a... |
| scrapy+md | 5.0 | The quotes tagged with 'inspirational' are:  1. “There are only two ways to live your life. One is a... |
| crawlee | 3.0 | The quotes tagged with 'inspirational' are:  1. “There are only two ways to live your life. One is a... |
| colly+md | 3.2 | The quotes tagged with 'inspirational' are:  1. “There are only two ways to live your life. One is a... |
| playwright | 3.2 | The quotes tagged with 'inspirational' are:  1. “There are only two ways to live your life. One is a... |

**Q3: What did Steve Martin say about sunshine?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Jane Austen said, “The person, be it gentleman or lady, who has not pleasure in a good novel, must b... |
| crawl4ai | 5.0 | Jane Austen said, “The person, be it gentleman or lady, who has not pleasure in a good novel, must b... |
| crawl4ai-raw | 5.0 | Jane Austen said, “The person, be it gentleman or lady, who has not pleasure in a good novel, must b... |
| scrapy+md | 5.0 | Jane Austen said, “The person, be it gentleman or lady, who has not pleasure in a good novel, must b... |
| crawlee | 5.0 | Jane Austen said, “The person, be it gentleman or lady, who has not pleasure in a good novel, must b... |
| colly+md | 5.0 | Jane Austen said, “The person, be it gentleman or lady, who has not pleasure in a good novel, must b... |
| playwright | 5.0 | Jane Austen said, “The person, be it gentleman or lady, who has not pleasure in a good novel, must b... |

**Q4: What quotes are about thinking deeply?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.2 | I cannot answer this based on the provided context.... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.2 | I cannot answer this based on the provided context.... |
| playwright | 2.0 | I cannot answer this based on the provided context.... |

**Q5: What did Eleanor Roosevelt say about life?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai | 5.0 | The quotes about humor and being funny are:  1. “A day without sunshine is like, you know, night.” b... |
| crawl4ai-raw | 5.0 | The quotes about humor and being funny are:  1. “A day without sunshine is like, you know, night.” b... |
| scrapy+md | 5.0 | The quotes about humor and being funny are:  1. “A day without sunshine is like, you know, night.” b... |
| crawlee | 4.2 | The quotes about humor and being funny are:  1. “A day without sunshine is like, you know, night.” b... |
| colly+md | 4.2 | The quotes about humor and being funny are:  1. “A day without sunshine is like, you know, night.” b... |
| playwright | 4.8 | The quotes about humor and being funny are:  1. “A day without sunshine is like, you know, night.” b... |

**Q6: Which quotes are tagged about choices and abilities?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | J.K. Rowling said, “It is our choices, Harry, that show what we truly are, far more than our abiliti... |
| crawl4ai | 5.0 | J.K. Rowling said, “It is our choices, Harry, that show what we truly are, far more than our abiliti... |
| crawl4ai-raw | 5.0 | J.K. Rowling said, “It is our choices, Harry, that show what we truly are, far more than our abiliti... |
| scrapy+md | 5.0 | J.K. Rowling said, “It is our choices, Harry, that show what we truly are, far more than our abiliti... |
| crawlee | 5.0 | J.K. Rowling said, “It is our choices, Harry, that show what we truly are, far more than our abiliti... |
| colly+md | 5.0 | J.K. Rowling said, “It is our choices, Harry, that show what we truly are, far more than our abiliti... |
| playwright | 5.0 | J.K. Rowling said, “It is our choices, Harry, that show what we truly are, far more than our abiliti... |

**Q7: What quotes are about friendship?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 4.2 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| crawl4ai | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| crawl4ai-raw | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| scrapy+md | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| crawlee | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| colly+md | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |
| playwright | 4.8 | “The world as we have created it is a process of our thinking. It cannot be changed without changing... |

**Q8: What are the quotes about love?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |
| crawl4ai | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |
| crawl4ai-raw | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |
| scrapy+md | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |
| crawlee | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |
| colly+md | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |
| playwright | 5.0 | Steve Martin said, "A day without sunshine is like, you know, night."... |

</details>

## books-toscrape

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 4.00 | 4.31 | 3.77 | 3.85 | 3.98 |
| crawl4ai | 4.08 | 3.62 | 3.00 | 3.54 | 3.56 |
| crawl4ai-raw | 4.00 | 3.69 | 3.00 | 3.38 | 3.52 |
| scrapy+md | 4.46 | 4.15 | 3.85 | 4.08 | 4.13 |
| crawlee | 4.38 | 4.15 | 3.77 | 4.00 | 4.08 |
| colly+md | 4.46 | 4.15 | 3.77 | 4.08 | 4.12 |
| playwright | 4.54 | 4.23 | 3.92 | 4.08 | 4.19 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for books-toscrape</summary>

**Q1: What mystery and thriller books are in the catalog?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 4.0 | The following books are available for under 20 pounds:  1. **Starving Hearts (Triangular Trade Trilo... |
| crawl4ai | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 5.0 | The following books are available for under 20 pounds:  1. **Starving Hearts (Triangular Trade Trilo... |
| crawlee | 5.0 | 1. [Starving Hearts (Triangular Trade Trilogy, #1)](../../../starving-hearts-triangular-trade-trilog... |
| colly+md | 5.0 | The following books are available for under 20 pounds:  1. [Starving Hearts (Triangular Trade Trilog... |
| playwright | 5.0 | The following books are available for under 20 pounds:  1. [Starving Hearts (Triangular Trade Trilog... |

**Q2: What science fiction books are available?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | The catalog includes the following mystery books:  1. Sharp Objects - £47.82 2. In a Dark, Dark Wood... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 4.8 | **Mystery Books:** 1. Sharp Objects - £47.82 2. In a Dark, Dark Wood - £19.63 3. The Past Never Ends... |
| crawlee | 4.8 | **Mystery Books:** 1. Sharp Objects - £47.82 2. In a Dark, Dark Wood - £19.63 3. The Past Never Ends... |
| colly+md | 4.8 | **Mystery Books:** 1. Sharp Objects - £47.82 2. In a Dark, Dark Wood - £19.63 3. The Past Never Ends... |
| playwright | 4.8 | **Mystery Books:** 1. Sharp Objects - £47.82 2. In a Dark, Dark Wood - £19.63 3. The Past Never Ends... |

**Q3: What is the book Sharp Objects about?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.2 | I cannot answer this based on the provided context.... |
| crawlee | 2.2 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.2 | I cannot answer this based on the provided context.... |

**Q4: What biography books are in the catalog?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | The available science fiction books are:  1. Mesaerion: The Best Science Fiction Stories 1800-1849 -... |
| crawl4ai | 4.8 | The available science fiction books are:  1. [Mesaerion: The Best Science Fiction Stories 1800-1849]... |
| crawl4ai-raw | 4.8 | The available science fiction books are:  1. [Mesaerion: The Best Science Fiction Stories 1800-1849]... |
| scrapy+md | 5.0 | The available science fiction books are:  1. Mesaerion: The Best Science Fiction Stories 1800-1849 -... |
| crawlee | 5.0 | The available science fiction books are:  1. Mesaerion: The Best Science Fiction Stories 1800-1849 -... |
| colly+md | 5.0 | The available science fiction books are:  1. Mesaerion: The Best Science Fiction Stories 1800-1849 -... |
| playwright | 5.0 | The available science fiction books are:  1. Mesaerion: The Best Science Fiction Stories 1800-1849 -... |

**Q5: What horror books are in the catalog?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | The horror books in the catalog are:  1. Security - £39.25 2. Follow You Home - £21.36 3. The Loney ... |
| crawl4ai | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 5.0 | The horror books in the catalog are:  1. Security - £39.25 2. Follow You Home - £21.36 3. The Loney ... |
| crawlee | 5.0 | The horror books in the catalog are:  1. Security - £39.25 2. Follow You Home - £21.36 3. The Loney ... |
| colly+md | 5.0 | The horror books in the catalog are:  1. Security - £39.25 2. Follow You Home - £21.36 3. The Loney ... |
| playwright | 5.0 | The horror books in the catalog are:  1. Security - £39.25 2. Follow You Home - £21.36 3. The Loney ... |

**Q6: What poetry books can I find?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. The Black Maria - £52.... |
| crawl4ai | 5.0 | You can find the following poetry books:  1. [A Light in the Attic](https://books.toscrape.com/catal... |
| crawl4ai-raw | 5.0 | You can find the following poetry books:  1. **You can't bury them all: Poems** - £33.63 2. **Quarte... |
| scrapy+md | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. The Black Maria - £52.... |
| crawlee | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. The Black Maria - £52.... |
| colly+md | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. The Black Maria - £52.... |
| playwright | 5.0 | You can find the following poetry books:  1. A Light in the Attic - £51.77 2. The Black Maria - £52.... |

**Q7: What fantasy books are in the bookstore?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai | 4.8 | The available romance novels are:  1. [Modern Romance](https://books.toscrape.com/catalogue/modern-r... |
| crawl4ai-raw | 4.8 | The available romance novels are:  1. [Modern Romance](https://books.toscrape.com/catalogue/modern-r... |
| scrapy+md | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.8 | I cannot answer this based on the provided context.... |

**Q8: What philosophy books are available to read?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 3.0 | The history books in the collection are:  1. **Sapiens: A Brief History of Humankind** by Yuval Noah... |
| crawl4ai | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.8 | I cannot answer this based on the provided context.... |
| crawlee | 2.8 | I cannot answer this based on the provided context.... |
| colly+md | 2.8 | I cannot answer this based on the provided context.... |
| playwright | 2.8 | I cannot answer this based on the provided context.... |

**Q9: What is the book Sapiens about?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.8 | The available philosophy books are:  1. **Libertarianism for Beginners** - £51.33 2. **Why the Right... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.0 | I cannot answer this based on the provided context.... |

**Q10: What romance novels are available?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 4.2 | The humor and comedy books available are:  1. **The Long Haul (Diary of a Wimpy Kid #9)** - £44.07 2... |
| crawl4ai | 5.0 | The humor and comedy books you can find include:  1. [The Long Haul (Diary of a Wimpy Kid #9)](https... |
| crawl4ai-raw | 5.0 | The humor and comedy books you can find include:  1. [The Long Haul (Diary of a Wimpy Kid #9)](https... |
| scrapy+md | 5.0 | You can find the following humor and comedy books:  1. **The Long Haul (Diary of a Wimpy Kid #9)** -... |
| crawlee | 4.2 | The humor and comedy books you can find are:  1. The Long Haul (Diary of a Wimpy Kid #9) - £44.07 2.... |
| colly+md | 5.0 | You can find the following humor and comedy books:  1. **The Long Haul (Diary of a Wimpy Kid #9)** -... |
| playwright | 5.0 | The humor and comedy books you can find are:  1. **The Long Haul (Diary of a Wimpy Kid #9)** - £44.0... |

</details>

## fastapi-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 4.69 | 4.62 | 4.50 | 4.56 | 4.59 |
| crawl4ai | 4.62 | 4.56 | 4.44 | 4.56 | 4.55 |
| crawl4ai-raw | 4.62 | 4.56 | 4.44 | 4.56 | 4.55 |
| scrapy+md | 4.62 | 4.62 | 4.31 | 4.50 | 4.52 |
| crawlee | 4.81 | 4.81 | 4.75 | 4.75 | 4.78 |
| colly+md | 4.62 | 4.62 | 4.38 | 4.50 | 4.53 |
| playwright | 4.81 | 4.81 | 4.75 | 4.75 | 4.78 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for fastapi-docs</summary>

**Q1: How do I add authentication to a FastAPI endpoint?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To add authentication to a FastAPI endpoint, you can use the security utilities provided by FastAPI,... |
| crawl4ai | 5.0 | To add authentication to a FastAPI endpoint, you can use the `OAuth2PasswordBearer` class from the `... |
| crawl4ai-raw | 5.0 | To add authentication to a FastAPI endpoint, you can use the `OAuth2PasswordBearer` class from the `... |
| scrapy+md | 5.0 | To add authentication to a FastAPI endpoint, you can use the security utilities provided by FastAPI,... |
| crawlee | 5.0 | To add authentication to a FastAPI endpoint, you can use the `HTTPBasic` security scheme. Here’s a c... |
| colly+md | 5.0 | To add authentication to a FastAPI endpoint, you can use the security utilities provided by FastAPI,... |
| playwright | 5.0 | To add authentication to a FastAPI endpoint, you can use the `HTTPBasic` security scheme. Here’s a c... |

**Q2: How do I define query parameters in the FastAPI reference?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 5.0 | The default response status code in FastAPI is 200.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 5.0 | The default response status code in FastAPI is 200.... |

**Q3: How does FastAPI handle JSON encoding and base64 bytes?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | You can define query parameters in FastAPI by declaring them as function parameters in your endpoint... |
| crawl4ai | 5.0 | You can define query parameters in FastAPI by declaring them as function parameters in your endpoint... |
| crawl4ai-raw | 5.0 | You can define query parameters in FastAPI by declaring them as function parameters in your endpoint... |
| scrapy+md | 5.0 | To define query parameters in FastAPI, you can declare them as function parameters in your route han... |
| crawlee | 5.0 | You can define query parameters in FastAPI by declaring them as function parameters in your route ha... |
| colly+md | 5.0 | You can define query parameters in FastAPI by declaring them as function parameters in your route ha... |
| playwright | 5.0 | You can define query parameters in FastAPI by declaring them as function parameters in your route ha... |

**Q4: How do I use OAuth2 with password flow in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | FastAPI handles JSON encoding and base64 bytes by using Pydantic models configured with `val_json_by... |
| crawl4ai | 5.0 | FastAPI handles JSON encoding and base64 bytes by allowing binary data to be encoded as base64 when ... |
| crawl4ai-raw | 5.0 | FastAPI handles JSON encoding and base64 bytes by allowing binary data to be encoded as base64 when ... |
| scrapy+md | 5.0 | FastAPI handles JSON encoding and base64 bytes by using Pydantic models configured with `val_json_by... |
| crawlee | 5.0 | FastAPI handles JSON encoding by using Pydantic models to serialize data into JSON format. When bina... |
| colly+md | 5.0 | FastAPI handles JSON encoding by using Pydantic models to serialize data to JSON. When a model inclu... |
| playwright | 5.0 | FastAPI handles JSON encoding by using Pydantic models to serialize data into JSON format. When bina... |

**Q5: How do I use WebSockets in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.2 | I cannot answer this based on the provided context.... |
| crawlee | 2.2 | I cannot answer this based on the provided context.... |
| colly+md | 2.2 | I cannot answer this based on the provided context.... |
| playwright | 2.2 | I cannot answer this based on the provided context.... |

**Q6: How do I define nested Pydantic models for request bodies?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To use OAuth2 with password flow in FastAPI, you can follow these steps:  1. **Import Required Class... |
| crawl4ai | 5.0 | To use OAuth2 with password flow in FastAPI, you can follow these steps:  1. **Import Required Class... |
| crawl4ai-raw | 5.0 | To use OAuth2 with password flow in FastAPI, you can follow these steps:  1. **Import Required Class... |
| scrapy+md | 4.8 | To use OAuth2 with password flow in FastAPI, you can follow these steps:  1. **Import Required Class... |
| crawlee | 5.0 | To use OAuth2 with password flow in FastAPI, follow these steps:  1. **Import Required Classes**: Im... |
| colly+md | 5.0 | To use OAuth2 with password flow in FastAPI, you can follow these steps:  1. **Import Required Class... |
| playwright | 5.0 | To use OAuth2 with password flow in FastAPI, follow these steps:  1. **Import Required Classes**: Im... |

**Q7: How do I use middleware in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| crawl4ai | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your application. Here’s a ... |
| crawl4ai-raw | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| scrapy+md | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| crawlee | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| colly+md | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your FastAPI application. H... |
| playwright | 5.0 | To use WebSockets in FastAPI, you need to create a WebSocket endpoint in your application. Here’s a ... |

**Q8: How do I deploy FastAPI to the cloud?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To stream data responses in FastAPI, you can use the `StreamingResponse` class. In your path operati... |
| crawl4ai | 5.0 | To stream data responses in FastAPI, you can use the `StreamingResponse` class. You define a path op... |
| crawl4ai-raw | 5.0 | To stream data responses in FastAPI, you can use the `StreamingResponse` class. You define a path op... |
| scrapy+md | 5.0 | To stream data responses in FastAPI, you can use the `StreamingResponse` class. In your path operati... |
| crawlee | 5.0 | To stream data responses in FastAPI, you can use the `StreamingResponse` class. You can declare a pa... |
| colly+md | 5.0 | To stream data responses in FastAPI, you can use the `StreamingResponse` class. In your path operati... |
| playwright | 5.0 | To stream data responses in FastAPI, you can use the `StreamingResponse` class. You can declare a pa... |

**Q9: How do I handle file uploads in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | You can return additional response types in FastAPI by using the `responses` parameter in the path o... |
| crawl4ai | 5.0 | You can return additional response types in FastAPI by declaring them in the `responses` parameter o... |
| crawl4ai-raw | 5.0 | You can return additional response types in FastAPI by declaring them in the `responses` parameter o... |
| scrapy+md | 5.0 | You can return additional response types in FastAPI by using the `responses` parameter in the path o... |
| crawlee | 5.0 | You can return additional response types in FastAPI by using the `responses` parameter in the path o... |
| colly+md | 5.0 | You can return additional response types in FastAPI by using the `responses` parameter in the path o... |
| playwright | 5.0 | You can return additional response types in FastAPI by using the `responses` parameter in the path o... |

**Q10: How do I write async tests for FastAPI applications?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To write async tests for FastAPI applications, you can use the `TestClient` directly with synchronou... |
| crawl4ai | 5.0 | To write async tests for FastAPI applications, you can use the `AsyncClient` from the `httpx` librar... |
| crawl4ai-raw | 5.0 | To write async tests for FastAPI applications, you can use the `AsyncClient` from the `httpx` librar... |
| scrapy+md | 4.2 | To write async tests for FastAPI applications, you cannot use the `TestClient` directly within async... |
| crawlee | 5.0 | To write async tests for FastAPI applications, you can use the `AsyncClient` from the `httpx` librar... |
| colly+md | 4.2 | To write async tests for FastAPI applications, you cannot use the `TestClient` directly inside async... |
| playwright | 5.0 | To write async tests for FastAPI applications, you can use the `AsyncClient` from the `httpx` librar... |

**Q11: How do I use Jinja2 templates in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To define nested Pydantic models for request bodies, you create Pydantic classes where each attribut... |
| crawl4ai | 5.0 | To define nested Pydantic models for request bodies, you create Pydantic models where each attribute... |
| crawl4ai-raw | 5.0 | To define nested Pydantic models for request bodies, you can create Pydantic models where each attri... |
| scrapy+md | 5.0 | To define nested Pydantic models for request bodies, you create Pydantic models where each attribute... |
| crawlee | 5.0 | You can define nested Pydantic models for request bodies by creating classes that inherit from `Base... |
| colly+md | 5.0 | To define nested Pydantic models for request bodies, you create Pydantic classes where each attribut... |
| playwright | 5.0 | To define nested Pydantic models for request bodies, you can create a Pydantic model where one of it... |

**Q12: How do I use dependency injection in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | You can handle startup and shutdown events in FastAPI using the `lifespan` parameter of the FastAPI ... |
| crawl4ai | 5.0 | In FastAPI, you can handle startup and shutdown events by using the `@app.on_event("startup")` and `... |
| crawl4ai-raw | 5.0 | In FastAPI, you can handle startup and shutdown events by using the `@app.on_event("startup")` and `... |
| scrapy+md | 5.0 | You can handle startup and shutdown events in FastAPI using the `lifespan` parameter of the FastAPI ... |
| crawlee | 5.0 | In FastAPI, you can handle startup and shutdown events by using the `@app.on_event("startup")` and `... |
| colly+md | 5.0 | You can handle startup and shutdown events in FastAPI by using the `@app.on_event("startup")` and `@... |
| playwright | 5.0 | In FastAPI, you can handle startup and shutdown events by using the `@app.on_event("startup")` and `... |

**Q13: How do I return custom response classes in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To use middleware in FastAPI, you can add it to your application using the `app.add_middleware()` me... |
| crawl4ai | 5.0 | To use middleware in FastAPI, you can add it to your application using the `@app.middleware("http")`... |
| crawl4ai-raw | 5.0 | To use middleware in FastAPI, you can add it to your application using the `@app.middleware("http")`... |
| scrapy+md | 5.0 | To use middleware in FastAPI, you can add it to your application using the `app.add_middleware()` me... |
| crawlee | 5.0 | To use middleware in FastAPI, you can add it to your application using the `@app.middleware("http")`... |
| colly+md | 5.0 | To use middleware in FastAPI, you can add it to your application using the `app.add_middleware()` me... |
| playwright | 5.0 | To use middleware in FastAPI, you can add it to your application using the `@app.middleware("http")`... |

**Q14: How do I configure CORS in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| crawl4ai | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| crawl4ai-raw | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| scrapy+md | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| crawlee | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| colly+md | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |
| playwright | 5.0 | To use Jinja2 templates in FastAPI, follow these steps:  1. Import `Jinja2Templates` from `fastapi.t... |

**Q15: How do I use path parameters in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 4.2 | You can deploy FastAPI apps to any cloud provider you choose by following your cloud provider's guid... |
| crawl4ai | 3.5 | You can deploy FastAPI to the cloud by using **FastAPI Cloud** with one command: `fastapi deploy`. A... |
| crawl4ai-raw | 3.5 | You can deploy FastAPI to the cloud by using **FastAPI Cloud** with one command: `fastapi deploy`. A... |
| scrapy+md | 4.0 | You can deploy FastAPI apps to any cloud provider by following their specific guides. Alternatively,... |
| crawlee | 4.2 | You can deploy your FastAPI app to the cloud using **FastAPI Cloud** with one command: `fastapi depl... |
| colly+md | 4.0 | You can deploy FastAPI apps to any cloud provider by following your cloud provider's guides. Alterna... |
| playwright | 4.2 | You can deploy your FastAPI app to the cloud using **FastAPI Cloud** with one command: `fastapi depl... |

**Q16: How do I run FastAPI with Docker?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To handle file uploads in FastAPI, you can define a path operation function parameter of type `Uploa... |
| crawl4ai | 5.0 | To handle file uploads in FastAPI, you can use the `File` and `UploadFile` classes. Here's a basic o... |
| crawl4ai-raw | 5.0 | To handle file uploads in FastAPI, you can use the `File` and `UploadFile` classes. Here's a basic e... |
| scrapy+md | 5.0 | To handle file uploads in FastAPI, you can use the `UploadFile` class. You define a path operation f... |
| crawlee | 5.0 | To handle file uploads in FastAPI, you can use the `File` and `UploadFile` classes from the `fastapi... |
| colly+md | 5.0 | To handle file uploads in FastAPI, you can use the `UploadFile` class. You define a path operation f... |
| playwright | 5.0 | To handle file uploads in FastAPI, you can use the `File` and `UploadFile` classes from the `fastapi... |

**Q17: How do I configure FastAPI application settings?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q18: How do I use background tasks in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q19: What are the first steps to create a FastAPI application?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q20: How do I handle errors and exceptions in FastAPI?**

| Tool | Score | Answer (truncated) |
|---|---|---|

</details>

## python-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 4.50 | 4.33 | 4.25 | 4.33 | 4.35 |
| crawl4ai | 4.58 | 4.58 | 4.33 | 4.50 | 4.50 |
| crawl4ai-raw | 4.58 | 4.58 | 4.33 | 4.50 | 4.50 |
| scrapy+md | 4.83 | 4.75 | 4.67 | 4.75 | 4.75 |
| crawlee | 4.58 | 4.33 | 4.08 | 4.25 | 4.31 |
| colly+md | 4.67 | 4.50 | 4.33 | 4.50 | 4.50 |
| playwright | 4.67 | 4.58 | 4.42 | 4.50 | 4.54 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for python-docs</summary>

**Q1: What new features were added in Python 3.10?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Python 3.10 introduced several new features, including:  1. Parenthesized context managers. 2. Bette... |
| crawl4ai | 5.0 | Python 3.10 introduced several new features, including:  1. Parenthesized context managers 2. Better... |
| crawl4ai-raw | 5.0 | Python 3.10 introduced several new features, including:  1. Parenthesized context managers 2. Better... |
| scrapy+md | 5.0 | Python 3.10 introduced several new features, including:  1. Parenthesized context managers 2. Better... |
| crawlee | 5.0 | Python 3.10 introduced several new features, including:  1. Parenthesized context managers 2. Better... |
| colly+md | 5.0 | Python 3.10 introduced several new features, including:  1. Parenthesized context managers 2. Better... |
| playwright | 5.0 | Python 3.10 introduced several new features, including:  1. Parenthesized context managers 2. Better... |

**Q2: What does the term 'decorator' mean in Python?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | A decorator in Python is a function that returns another function, usually applied as a function tra... |
| crawl4ai | 5.0 | In Python, a 'decorator' is a function that returns another function, usually applied as a function ... |
| crawl4ai-raw | 5.0 | In Python, a 'decorator' is a function that returns another function, usually applied as a function ... |
| scrapy+md | 5.0 | In Python, a 'decorator' is a function that returns another function, usually applied as a function ... |
| crawlee | 5.0 | A decorator in Python is a function that returns another function, usually applied as a function tra... |
| colly+md | 5.0 | In Python, a 'decorator' is a function that returns another function, usually applied as a function ... |
| playwright | 5.0 | A decorator in Python is a function that returns another function, usually applied as a function tra... |

**Q3: How do I report a bug in Python?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To report a bug in Python, follow these steps:  1. Go to the Python Bug Tracker at <http://bugs.pyth... |
| crawl4ai | 5.0 | To report a bug in Python, follow these steps:  1. Go to the Python Bug Tracker at <http://bugs.pyth... |
| crawl4ai-raw | 5.0 | To report a bug in Python, follow these steps:  1. Go to the Python Bug Tracker at <http://bugs.pyth... |
| scrapy+md | 5.0 | To report a bug in Python, submit an issue via the GitHub issues tracker at <https://github.com/pyth... |
| crawlee | 5.0 | To report a bug in Python, follow these steps:  1. Visit the Python Bug Tracker at <http://bugs.pyth... |
| colly+md | 5.0 | To report a bug in Python, follow these steps:  1. Go to the Python Bug Tracker at <http://bugs.pyth... |
| playwright | 5.0 | To report a bug in Python, follow these steps:  1. Visit the Python Bug Tracker at <http://bugs.pyth... |

**Q4: What is Python's glossary definition of a generator?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Structural pattern matching in Python is a feature that allows programs to extract information from ... |
| crawl4ai | 5.0 | Structural pattern matching in Python is a feature that allows programs to extract information from ... |
| crawl4ai-raw | 5.0 | Structural pattern matching in Python is a feature that allows programs to extract information from ... |
| scrapy+md | 5.0 | Structural pattern matching in Python is a feature that allows programs to extract information from ... |
| crawlee | 5.0 | Structural pattern matching in Python is a feature that allows programs to extract information from ... |
| colly+md | 5.0 | Structural pattern matching in Python is a feature that allows programs to extract information from ... |
| playwright | 5.0 | Structural pattern matching in Python is a feature that allows programs to extract information from ... |

**Q5: What is the Python module index?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| crawl4ai | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| crawl4ai-raw | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| scrapy+md | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| crawlee | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| colly+md | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |
| playwright | 5.0 | A generator is a function which returns a generator iterator. It looks like a normal function except... |

**Q6: What does the term 'iterable' mean in Python?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | The Python HOWTOs are documents that cover specific topics in-depth, providing detailed information ... |
| crawl4ai | 5.0 | The Python HOWTOs are documents that cover specific topics in-depth, aiming to provide detailed docu... |
| crawl4ai-raw | 5.0 | The Python HOWTOs are documents that cover specific topics in-depth, aiming to provide detailed docu... |
| scrapy+md | 5.0 | The Python how-to guides are documents that cover specific topics in-depth, providing more detailed ... |
| crawlee | 5.0 | The Python HOWTOs are documents that cover specific topics in-depth, providing detailed information ... |
| colly+md | 5.0 | The Python HOWTOs are documents that cover specific topics in-depth, providing detailed information ... |
| playwright | 5.0 | The Python HOWTOs are documents that cover specific topics in-depth, providing detailed information ... |

**Q7: How do I install and configure Python on my system?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai | 5.0 | The Python module index is a list of all the modules available in a specific version of Python docum... |
| crawl4ai-raw | 5.0 | The Python module index is a list of modules available in a specific version of Python documentation... |
| scrapy+md | 5.0 | The Python module index is a list or directory of Python modules that are available for use, typical... |
| crawlee | 2.8 | I cannot answer this based on the provided context.... |
| colly+md | 5.0 | The Python module index is a list or directory of Python modules that are available for use in Pytho... |
| playwright | 2.5 | I cannot answer this based on the provided context.... |

**Q8: How do I use the os module for file and directory operations?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | The Python tutorial covers the basic concepts and features of the Python language and system, includ... |
| crawl4ai | 5.0 | The Python tutorial topics available include:  1. Whetting Your Appetite 2. Using the Python Interpr... |
| crawl4ai-raw | 5.0 | The Python tutorial topics available include:  1. Whetting Your Appetite 2. Using the Python Interpr... |
| scrapy+md | 5.0 | The available Python tutorial topics include:  1. Whetting Your Appetite 2. Using the Python Interpr... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 5.0 | The Python tutorial covers the basic concepts and features of the Python language and system, includ... |

**Q9: How do I use pathlib for filesystem paths in Python?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | The Python software and documentation are licensed under the Python Software Foundation License Vers... |
| crawl4ai | 4.8 | Python software and documentation are licensed under the Python Software Foundation License Version ... |
| crawl4ai-raw | 4.8 | Python software and documentation are licensed under the Python Software Foundation License Version ... |
| scrapy+md | 5.0 | The Python software and documentation are licensed under the Python Software Foundation License Vers... |
| crawlee | 5.0 | The Python software and documentation are licensed under the Python Software Foundation License Vers... |
| colly+md | 5.0 | The Python software and documentation are licensed under the Python Software Foundation License Vers... |
| playwright | 5.0 | The Python software and documentation are licensed under the Python Software Foundation License Vers... |

**Q10: How do I parse and generate JSON in Python?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.2 | The table of contents for Python 3.10 documentation includes:  - About these documents   - Contribut... |
| crawl4ai-raw | 2.2 | The table of contents for Python 3.10 documentation includes:  - About these documents   - Contribut... |
| scrapy+md | 5.0 | The table of contents for Python 3.10 documentation includes:  - About this documentation - Contribu... |
| crawlee | 5.0 | The table of contents for Python 3.10 documentation includes:  - About this documentation   - Contri... |
| colly+md | 5.0 | The table of contents for Python 3.10 documentation includes:  - About these documents   - Contribut... |
| playwright | 5.0 | The table of contents for Python 3.10 documentation includes:  - About these documents   - Contribut... |

**Q11: How do I use asyncio for async programming in Python?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | An 'iterable' in Python is an object capable of returning its members one at a time. Examples includ... |
| crawl4ai | 5.0 | An iterable in Python is an object capable of returning its members one at a time. Examples include ... |
| crawl4ai-raw | 5.0 | An 'iterable' in Python is an object capable of returning its members one at a time. Examples includ... |
| scrapy+md | 5.0 | In Python, an 'iterable' is an object capable of returning its members one at a time. Examples of it... |
| crawlee | 5.0 | In Python, an 'iterable' is an object capable of returning its members one at a time. Examples inclu... |
| colly+md | 5.0 | In Python, an 'iterable' is an object capable of returning its members one at a time. Examples inclu... |
| playwright | 5.0 | In Python, an 'iterable' is an object capable of returning its members one at a time. Examples inclu... |

**Q12: How do I use type hints and the typing module in Python?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.0 | I cannot answer this based on the provided context.... |

**Q13: How do I work with dates and times using the datetime module?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q14: How do I use Python's logging module?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q15: How do I write unit tests with the unittest module?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q16: How do I use Python dataclasses?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q17: How do I use itertools for efficient iteration in Python?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q18: How does Python's data model work with special methods?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q19: What are Python's compound statements like if, for, and with?**

| Tool | Score | Answer (truncated) |
|---|---|---|

</details>

## react-dev

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawl4ai | 4.83 | 4.75 | 4.67 | 4.75 | 4.75 |
| crawl4ai-raw | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| scrapy+md | 4.83 | 4.75 | 4.67 | 4.75 | 4.75 |
| crawlee | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| colly+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| playwright | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for react-dev</summary>

**Q1: How do I manage state in a React component?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | You manage state in a React component by using the `useState` Hook. This Hook allows you to declare ... |
| crawl4ai | 5.0 | To manage state in a React component, you should:  1. **Isolate State**: Understand that state is sp... |
| crawl4ai-raw | 5.0 | To manage state in a React component, you should:  1. **Isolate State**: Ensure that state is specif... |
| scrapy+md | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 5.0 | You manage state in a React component by using the `useState` Hook. This Hook allows you to declare ... |
| colly+md | 5.0 | You can manage state in a React component by using the `useState` Hook. This Hook allows you to decl... |
| playwright | 5.0 | You manage state in a React component by using the `useState` Hook. This Hook allows you to declare ... |

**Q2: How does the useEffect hook work in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | React hooks are special functions that allow you to use different React features in your components.... |
| crawl4ai | 5.0 | React hooks are special functions that start with `use` and allow you to "hook into" different React... |
| crawl4ai-raw | 5.0 | React hooks are special functions that start with `use` and allow you to "hook into" different React... |
| scrapy+md | 5.0 | React hooks are special functions that allow you to use different React features in your components.... |
| crawlee | 5.0 | React hooks are special functions that allow you to use different React features within your compone... |
| colly+md | 5.0 | React hooks are special functions that allow you to use different React features within your compone... |
| playwright | 5.0 | React hooks are special functions that allow you to use different React features within your compone... |

**Q3: How do I create and use context in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| crawl4ai | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| crawl4ai-raw | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| scrapy+md | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| crawlee | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| colly+md | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| playwright | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |

**Q4: What is JSX and how does React use it?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | In React, you handle forms and user input by using controlled components, which means you manage the... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 5.0 | To handle forms and user input in React, you should:  1. **Use a `<form>` element**: Wrap your input... |
| scrapy+md | 5.0 | In React, you handle forms and user input by using controlled components, which means you manage the... |
| crawlee | 5.0 | To handle forms and user input in React, you should use controlled components. This involves:  1. **... |
| colly+md | 5.0 | In React, you handle forms and user input by using controlled components, which means you manage the... |
| playwright | 5.0 | In React, you handle forms and user input by using controlled components, which means you manage the... |

**Q5: How do I render lists and use keys in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| crawl4ai | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |
| crawl4ai-raw | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |
| scrapy+md | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| crawlee | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| colly+md | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |
| playwright | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |

**Q6: How do I use the useRef hook in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Declare an event handler ... |
| crawl4ai | 5.0 | In React, you handle events like clicks by defining an event handler function inside your component ... |
| crawl4ai-raw | 5.0 | In React, you handle events like clicks by defining an event handler function inside your component ... |
| scrapy+md | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Declare an event handler ... |
| crawlee | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Define an event handler f... |
| colly+md | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Define an event handler f... |
| playwright | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Define an event handler f... |

**Q7: How do I pass props between React components?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| crawl4ai | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| crawl4ai-raw | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| scrapy+md | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| crawlee | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| colly+md | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within a J... |
| playwright | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |

**Q8: How do I conditionally render content in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To render lists in React, you can use the `map()` function to transform an array of data into an arr... |
| crawl4ai | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |
| crawl4ai-raw | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |
| scrapy+md | 5.0 | To render lists in React, you can use the JavaScript `map()` function to transform an array of data ... |
| crawlee | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |
| colly+md | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |
| playwright | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |

**Q9: What is the useMemo hook for in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| crawl4ai | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| crawl4ai-raw | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| scrapy+md | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| crawlee | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| colly+md | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| playwright | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |

**Q10: How do I use the useState hook in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | You pass props between React components by giving them as attributes to the child component in the p... |
| crawl4ai | 5.0 | You pass props between React components by having a parent component provide information to its chil... |
| crawl4ai-raw | 5.0 | You pass props between React components by having a parent component provide information to its chil... |
| scrapy+md | 5.0 | You pass props between React components by giving them as attributes to the child component in the p... |
| crawlee | 5.0 | You pass props between React components by giving them as attributes in the JSX of the parent compon... |
| colly+md | 5.0 | You pass props between React components by giving them as attributes in the JSX of the parent compon... |
| playwright | 5.0 | You pass props between React components by giving them as attributes in the JSX of the parent compon... |

**Q11: How do I use the useCallback hook in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | In React, you can conditionally render content using JavaScript syntax like `if` statements, the con... |
| crawl4ai | 5.0 | In React, you can conditionally render content using JavaScript syntax like `if` statements, the con... |
| crawl4ai-raw | 5.0 | In React, you can conditionally render content using JavaScript syntax like `if` statements, the con... |
| scrapy+md | 5.0 | In React, you can conditionally render content using JavaScript syntax like `if` statements, the con... |
| crawlee | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| colly+md | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| playwright | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |

**Q12: How do I use the useReducer hook in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| crawl4ai | 5.0 | The `useMemo` hook in React is for caching the result of a calculation between re-renders, allowing ... |
| crawl4ai-raw | 5.0 | The `useMemo` hook in React is for caching the result of a calculation between re-renders, allowing ... |
| scrapy+md | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| crawlee | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| colly+md | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| playwright | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |

**Q13: How do I handle events like clicks in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q14: What is the Suspense component in React?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q15: How do I add interactivity to React components?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q16: How do I install and set up a new React project?**

| Tool | Score | Answer (truncated) |
|---|---|---|

</details>

## wikipedia-python

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 4.60 | 4.40 | 4.20 | 4.40 | 4.40 |
| crawl4ai | 4.80 | 4.70 | 4.50 | 4.70 | 4.67 |
| crawl4ai-raw | 4.80 | 4.70 | 4.50 | 4.70 | 4.67 |
| scrapy+md | 4.80 | 4.70 | 4.50 | 4.70 | 4.67 |
| crawlee | 4.80 | 4.70 | 4.50 | 4.70 | 4.67 |
| colly+md | 4.80 | 4.70 | 4.50 | 4.70 | 4.67 |
| playwright | 4.80 | 4.70 | 4.50 | 4.70 | 4.67 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for wikipedia-python</summary>

**Q1: Who created the Python programming language?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Guido van Rossum created the Python programming language.... |
| crawl4ai | 5.0 | The Python programming language was created by Guido van Rossum.... |
| crawl4ai-raw | 5.0 | The Python programming language was created by Guido van Rossum.... |
| scrapy+md | 5.0 | The Python programming language was created by Guido van Rossum.... |
| crawlee | 5.0 | Guido van Rossum created the Python programming language.... |
| colly+md | 5.0 | The Python programming language was created by Guido van Rossum.... |
| playwright | 5.0 | Guido van Rossum created the Python programming language.... |

**Q2: What is the Python Software Foundation?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) i... |
| crawl4ai | 5.0 | Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) i... |
| crawl4ai-raw | 5.0 | Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) i... |
| scrapy+md | 5.0 | Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) i... |
| crawlee | 5.0 | Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) i... |
| colly+md | 5.0 | Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) i... |
| playwright | 5.0 | Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) i... |

**Q3: Who is Guido van Rossum?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Python supports multiple programming paradigms, including object-oriented programming, procedural pr... |
| crawl4ai | 5.0 | Python supports multiple programming paradigms, including object-oriented programming, procedural pr... |
| crawl4ai-raw | 5.0 | Python supports multiple programming paradigms, including object-oriented programming, procedural pr... |
| scrapy+md | 5.0 | Python supports multiple programming paradigms, including object-oriented, procedural (imperative), ... |
| crawlee | 5.0 | Python supports multiple programming paradigms, including object-oriented, procedural (imperative), ... |
| colly+md | 5.0 | Python supports multiple programming paradigms, including object-oriented, procedural (imperative), ... |
| playwright | 5.0 | Python supports multiple programming paradigms, including object-oriented, procedural (imperative), ... |

**Q4: What is CPython and how does it work?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization devoted to the Python pro... |
| crawl4ai | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization established on March 6, 2... |
| crawl4ai-raw | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization established on March 6, 2... |
| scrapy+md | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization established on March 6, 2... |
| crawlee | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization established on March 6, 2... |
| colly+md | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization established on March 6, 2... |
| playwright | 5.0 | The Python Software Foundation (PSF) is an American nonprofit organization established on March 6, 2... |

**Q5: How does Python compare to other programming languages?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Python's design philosophy emphasizes code readability, simplicity, and ease of writing, often using... |
| crawl4ai | 5.0 | Python's syntax is designed to be easily readable, using significant indentation instead of curly br... |
| crawl4ai-raw | 5.0 | Python's syntax is designed to be easily readable, using significant indentation instead of curly br... |
| scrapy+md | 5.0 | Python's syntax is designed to be easily readable, using significant indentation and English keyword... |
| crawlee | 5.0 | Python's syntax is designed to be easily readable, using significant indentation and English keyword... |
| colly+md | 5.0 | Python's syntax is designed to be easily readable, using significant indentation and English keyword... |
| playwright | 5.0 | Python's syntax is designed to be easily readable, using significant indentation and English keyword... |

**Q6: What is NumPy and what is it used for?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 4.8 | Python's standard library includes modules for creating graphical user interfaces, connecting to rel... |
| crawl4ai-raw | 4.8 | Python's standard library includes modules for creating graphical user interfaces, connecting to rel... |
| scrapy+md | 4.8 | Python's standard library includes modules for creating graphical user interfaces, connecting to rel... |
| crawlee | 4.8 | Python's standard library includes modules for creating graphical user interfaces, connecting to rel... |
| colly+md | 4.8 | Python's standard library includes modules for creating graphical user interfaces, connecting to rel... |
| playwright | 4.8 | Python's standard library includes modules for creating graphical user interfaces, connecting to rel... |

**Q7: What is SQLAlchemy and how is it used with Python?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Guido van Rossum is the designer of Python and was the lead developer of the language until July 12,... |
| crawl4ai | 5.0 | Guido van Rossum is the creator of the Python programming language and was the lead developer of the... |
| crawl4ai-raw | 5.0 | Guido van Rossum is the creator of the Python programming language and was the lead developer of the... |
| scrapy+md | 5.0 | Guido van Rossum is the designer of Python and was the lead developer of the language until July 201... |
| crawlee | 5.0 | Guido van Rossum is the designer of Python and was the lead developer of the language until July 12,... |
| colly+md | 5.0 | Guido van Rossum is the designer of Python and was the lead developer of the language until July 201... |
| playwright | 5.0 | Guido van Rossum is the designer of Python and was the lead developer of the language until July 201... |

**Q8: What is metaprogramming in computer science?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into in... |
| crawl4ai | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into an... |
| crawl4ai-raw | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into an... |
| scrapy+md | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into in... |
| crawlee | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into in... |
| colly+md | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into an... |
| playwright | 5.0 | CPython is the reference implementation of Python, written in C. It compiles Python programs into in... |

**Q9: What are list comprehensions in programming?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.0 | I cannot answer this based on the provided context.... |

**Q10: How does memory management work in programming?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | Python Enhancement Proposals (PEPs) are the primary mechanism for proposing major new features, coll... |
| crawl4ai | 5.0 | Python Enhancement Proposals (PEPs) are the primary mechanism for proposing major new features, coll... |
| crawl4ai-raw | 5.0 | Python Enhancement Proposals (PEPs) are the primary mechanism for proposing major new features, coll... |
| scrapy+md | 5.0 | Python Enhancement Proposals (PEPs) are the primary mechanism for proposing major new features, coll... |
| crawlee | 5.0 | Python Enhancement Proposals (PEPs) are the primary mechanism for proposing major new features, coll... |
| colly+md | 5.0 | Python Enhancement Proposals (PEPs) are the primary mechanism for proposing major new features, coll... |
| playwright | 5.0 | Python Enhancement Proposals (PEPs) are the primary mechanism for proposing major new features, coll... |

</details>

## stripe-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 4.70 | 4.70 | 4.50 | 4.60 | 4.62 |
| crawl4ai | 4.60 | 4.40 | 4.10 | 4.40 | 4.38 |
| crawl4ai-raw | 4.80 | 4.70 | 4.60 | 4.70 | 4.70 |
| scrapy+md | 4.50 | 4.50 | 4.00 | 4.30 | 4.33 |
| crawlee | 4.40 | 4.10 | 3.70 | 4.10 | 4.08 |
| colly+md | 4.40 | 4.10 | 3.70 | 4.00 | 4.05 |
| playwright | 4.40 | 4.10 | 3.60 | 4.10 | 4.05 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for stripe-docs</summary>

**Q1: How do I create a payment intent with Stripe?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| crawl4ai | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| crawl4ai-raw | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| scrapy+md | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| crawlee | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| colly+md | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| playwright | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |

**Q2: How do I handle webhooks from Stripe?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To handle webhooks from Stripe, follow these steps:  1. Set up a webhook endpoint in your applicatio... |
| crawl4ai | 5.0 | To handle webhooks from Stripe, set up an HTTP handler to accept POST requests containing the webhoo... |
| crawl4ai-raw | 5.0 | To handle webhooks from Stripe, set up an HTTP handler to accept POST requests containing the webhoo... |
| scrapy+md | 5.0 | To handle webhooks from Stripe, follow these steps:  1. **Set Up a Webhook Endpoint**: Create an HTT... |
| crawlee | 5.0 | To handle webhooks from Stripe, set up an HTTP handler in your application to accept a POST request ... |
| colly+md | 5.0 | To handle webhooks from Stripe, follow these steps:  1. **Set Up a Webhook Endpoint**: Create an HTT... |
| playwright | 5.0 | To handle webhooks from Stripe, set up an HTTP handler in your application to accept a POST request ... |

**Q3: How do I set up Stripe subscriptions?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To set up Stripe subscriptions, you need to:  1. Create a [Product](/api/products) to define what yo... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 5.0 | To set up Stripe subscriptions, you need to install the Stripe client of your choice (e.g., Ruby, Py... |
| scrapy+md | 5.0 | To set up Stripe subscriptions, you need to:  1. Create a [Product](https://api.stripe.com/docs/prod... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.0 | I cannot answer this based on the provided context.... |

**Q4: How do I authenticate with the Stripe API?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | You authenticate with the Stripe API using your account’s API keys. Ensure that your request include... |
| crawl4ai | 5.0 | To authenticate with the Stripe API, use your account’s API keys. Include a valid API key in your re... |
| crawl4ai-raw | 5.0 | To authenticate with the Stripe API, use your account’s API keys. Include a valid API key in your re... |
| scrapy+md | 4.8 | Authenticate requests with secret and restricted API keys.... |
| crawlee | 4.8 | Authenticate requests with secret and restricted API keys.... |
| colly+md | 4.5 | Authenticate requests with secret and restricted API keys.... |
| playwright | 4.8 | Authenticate requests with secret and restricted API keys.... |

**Q5: How do I handle errors in the Stripe API?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To handle errors in the Stripe API, you should:  1. Use client libraries that raise exceptions for n... |
| crawl4ai | 5.0 | To handle errors in the Stripe API, you should use exception handling in your code. In the Stripe Ru... |
| crawl4ai-raw | 5.0 | To handle errors in the Stripe API, you should use exception handling in your code. In the Stripe Ru... |
| scrapy+md | 5.0 | To handle errors in the Stripe API, you should use exception handling in your code. In the Stripe Ru... |
| crawlee | 5.0 | To handle errors in the Stripe API, you can use exception handling in your code. In the Stripe Ruby ... |
| colly+md | 5.0 | To handle errors in the Stripe API, you should use exception handling in your code. In the Stripe Ru... |
| playwright | 5.0 | To handle errors in the Stripe API, you should use exception handling in your code. In the Stripe Ru... |

**Q6: How do I process refunds with Stripe?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To create a customer in Stripe, go to the Customers page in the Stripe Dashboard and click **Add cus... |
| crawl4ai | 5.0 | To create a customer in Stripe, you can use the following cURL command:  ```bash curl https://api.st... |
| crawl4ai-raw | 5.0 | To create a customer in Stripe, you can use the following cURL command:  ```bash curl https://api.st... |
| scrapy+md | 5.0 | To create a customer in Stripe, you can use the Stripe Dashboard or the API.   1. **Using the Dashbo... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.0 | I cannot answer this based on the provided context.... |

**Q7: How do I use Stripe checkout for payments?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 4.2 | To process refunds with Stripe, you need to report the refund after the original payment is successf... |
| crawl4ai | 5.0 | To process refunds with Stripe, you need to report the refund after the original payment is successf... |
| crawl4ai-raw | 5.0 | To process refunds with Stripe, you can report a refund after the original payment is successfully r... |
| scrapy+md | 4.2 | To process refunds with Stripe, you need to report the refund after the original payment is successf... |
| crawlee | 5.0 | To process refunds with Stripe, you need to follow these steps:  1. Ensure the original payment is s... |
| colly+md | 5.0 | To process refunds with Stripe, you need to follow these steps:  1. Ensure the original payment is s... |
| playwright | 5.0 | To process refunds with Stripe, you need to follow these steps:  1. Ensure the original payment is s... |

**Q8: How do I test Stripe payments in development?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | To use Stripe Checkout for payments, follow these steps:  1. **Set Up Your Environment**: Include th... |
| crawl4ai | 5.0 | To use Stripe Checkout for payments, follow these steps:  1. **Set Up Stripe.js**: Include the Strip... |
| crawl4ai-raw | 5.0 | To use Stripe Checkout for payments, follow these steps:  1. **Include Stripe.js**: Add the Stripe.j... |
| scrapy+md | 2.5 | I cannot answer this based on the provided context.... |
| crawlee | 5.0 | To use Stripe Checkout for payments, follow these steps:  1. **Create a Checkout Session**: Set up a... |
| colly+md | 5.0 | To use Stripe checkout for payments, follow these steps:  1. **Set Up Your Environment**: Ensure you... |
| playwright | 5.0 | To use Stripe checkout for payments, follow these steps:  1. **Set Up Your Environment**: Ensure you... |

**Q9: What are Stripe Connect and platform payments?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 5.0 | You can test Stripe payments in development by using test cards, test clocks, and the Stripe CLI to ... |
| crawl4ai | 5.0 | To test Stripe payments in development, follow these steps:  1. Use your test API keys while develop... |
| crawl4ai-raw | 5.0 | To test Stripe payments in development, you can follow these steps:  1. **Use Test API Keys**: Alway... |
| scrapy+md | 5.0 | You can test Stripe payments in development by using test cards and test API keys to simulate variou... |
| crawlee | 5.0 | You can test Stripe payments in development by using test cards and account numbers to trigger diffe... |
| colly+md | 5.0 | You can test Stripe payments in development by using test cards and account numbers to trigger diffe... |
| playwright | 5.0 | You can test Stripe payments in development by using test cards and account numbers to trigger diffe... |

**Q10: How do I set up usage-based billing with Stripe?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 2.2 | I cannot answer this based on the provided context.... |
| colly+md | 2.2 | I cannot answer this based on the provided context.... |
| playwright | 2.0 | I cannot answer this based on the provided context.... |

**Q11: How do I manage Stripe API keys?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q12: How do I handle Stripe rate limits?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q13: How do I use metadata with Stripe objects?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q14: How do I set up Apple Pay with Stripe?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q15: How do I issue cards with Stripe Issuing?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q16: How do I recover failed subscription payments?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q17: How does Stripe handle tax calculation for billing?**

| Tool | Score | Answer (truncated) |
|---|---|---|

**Q18: How do I migrate data to Stripe?**

| Tool | Score | Answer (truncated) |
|---|---|---|

</details>

## blog-engineering

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| **markcrawl** | 3.38 | 2.88 | 1.88 | 2.38 | 2.62 |
| crawl4ai | 3.00 | 2.88 | 2.00 | 2.38 | 2.56 |
| crawl4ai-raw | 3.12 | 2.75 | 1.75 | 2.25 | 2.47 |
| scrapy+md | 3.38 | 3.25 | 2.62 | 2.75 | 3.00 |
| crawlee | 3.12 | 3.00 | 2.00 | 2.25 | 2.59 |
| colly+md | 3.00 | 2.50 | 1.50 | 2.00 | 2.25 |
| playwright | 3.12 | 2.88 | 2.00 | 2.25 | 2.56 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for blog-engineering</summary>

**Q1: How does GitHub handle Kubernetes at scale?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 2.5 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.5 | I cannot answer this based on the provided context.... |

**Q2: How does GitHub protect against DDoS attacks?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 5.0 | Companies handle database migrations at scale using various strategies, including:  1. **Replica Mig... |
| crawlee | 2.5 | I cannot answer this based on the provided context.... |
| colly+md | 2.5 | I cannot answer this based on the provided context.... |
| playwright | 2.5 | I cannot answer this based on the provided context.... |

**Q3: How does GitHub handle MySQL database operations?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 4.8 | Engineering teams at GitHub use Haystack for exception tracking and monitoring, as well as `statsd` ... |
| crawl4ai | 3.5 | Engineering teams use Haystack for exception monitoring and Brubeck, a statsd-compatible metrics agg... |
| crawl4ai-raw | 4.0 | Engineering teams use Haystack for exception tracking and Brubeck, a statsd-compatible metrics aggre... |
| scrapy+md | 4.2 | Engineering teams use Haystack for exception tracking and monitoring, and `statsd` for metrics aggre... |
| crawlee | 4.2 | Engineering teams use Haystack for exception tracking and monitoring, and they utilize Graphite for ... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 4.2 | Engineering teams use Haystack for exception tracking and monitoring, and they utilize Graphite for ... |

**Q4: How does GitHub handle load balancing?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.5 | I cannot answer this based on the provided context.... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.5 | I cannot answer this based on the provided context.... |
| playwright | 2.0 | I cannot answer this based on the provided context.... |

**Q5: What is GitHub's approach to platform security?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.2 | I cannot answer this based on the provided context.... |
| crawlee | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.2 | I cannot answer this based on the provided context.... |

**Q6: How does GitHub optimize its architecture?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 2.5 | I cannot answer this based on the provided context.... |
| colly+md | 2.5 | I cannot answer this based on the provided context.... |
| playwright | 2.0 | I cannot answer this based on the provided context.... |

**Q7: What engineering principles does GitHub follow?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.5 | I cannot answer this based on the provided context.... |
| crawlee | 2.5 | I cannot answer this based on the provided context.... |
| colly+md | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 2.5 | I cannot answer this based on the provided context.... |

**Q8: How does GitHub improve user experience?**

| Tool | Score | Answer (truncated) |
|---|---|---|
| markcrawl | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 2.5 | I cannot answer this based on the provided context.... |
| crawlee | 2.5 | I cannot answer this based on the provided context.... |
| colly+md | 2.5 | I cannot answer this based on the provided context.... |
| playwright | 2.5 | I cannot answer this based on the provided context.... |

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

