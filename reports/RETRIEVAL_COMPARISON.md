# Retrieval Quality Comparison
<!-- style: v2, 2026-04-13 -->

Crawler choice barely matters for retrieval — retrieval mode matters more.

Does each tool's output produce embeddings that answer real questions?
This benchmark chunks each tool's crawl output, embeds it with
`text-embedding-3-small`, and measures retrieval across four modes:

- **Embedding**: Cosine similarity on OpenAI embeddings
- **BM25**: Keyword search (Okapi BM25)
- **Hybrid**: Embedding + BM25 fused via Reciprocal Rank Fusion
- **Reranked**: Hybrid candidates reranked by `cross-encoder/ms-marco-MiniLM-L-6-v2`

**109 queries** across 8 sites.
Hit rate = correct source page in top-K results. Higher is better.

## Summary: retrieval modes compared

| Tool | Mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR |
|---|---|---|---|---|---|---|---|
| **markcrawl** | embedding | 68% (74/109) ±9% | 83% (90/109) ±7% | 86% (94/109) ±6% | 91% (99/109) ±6% | 91% (99/109) ±6% | 0.759 |
| **markcrawl** | bm25 | 26% (28/109) ±8% | 43% (47/109) ±9% | 56% (61/109) ±9% | 68% (74/109) ±9% | 77% (84/109) ±8% | 0.388 |
| **markcrawl** | hybrid | 55% (60/109) ±9% | 78% (85/109) ±8% | 83% (90/109) ±7% | 91% (99/109) ±6% | 91% (99/109) ±6% | 0.675 |
| **markcrawl** | reranked | 58% (63/109) ±9% | 84% (92/109) ±7% | 88% (96/109) ±6% | 91% (99/109) ±6% | 92% (100/109) ±5% | 0.715 |
| crawl4ai | embedding | 71% (77/109) ±8% | 83% (91/109) ±7% | 89% (97/109) ±6% | 90% (98/109) ±6% | 93% (101/109) ±5% | 0.771 |
| crawl4ai | bm25 | 21% (23/109) ±8% | 39% (42/109) ±9% | 48% (52/109) ±9% | 60% (65/109) ±9% | 70% (76/109) ±9% | 0.339 |
| crawl4ai | hybrid | 57% (62/109) ±9% | 79% (86/109) ±8% | 87% (95/109) ±6% | 91% (99/109) ±6% | 92% (100/109) ±5% | 0.695 |
| crawl4ai | reranked | 66% (72/109) ±9% | 84% (92/109) ±7% | 89% (97/109) ±6% | 91% (99/109) ±6% | 91% (99/109) ±6% | 0.754 |
| crawl4ai-raw | embedding | 70% (76/109) ±9% | 83% (91/109) ±7% | 89% (97/109) ±6% | 90% (98/109) ±6% | 92% (100/109) ±5% | 0.767 |
| crawl4ai-raw | bm25 | 21% (23/109) ±8% | 38% (41/109) ±9% | 47% (51/109) ±9% | 60% (65/109) ±9% | 69% (75/109) ±9% | 0.335 |
| crawl4ai-raw | hybrid | 57% (62/109) ±9% | 78% (85/109) ±8% | 87% (95/109) ±6% | 91% (99/109) ±6% | 92% (100/109) ±5% | 0.691 |
| crawl4ai-raw | reranked | 66% (72/109) ±9% | 84% (92/109) ±7% | 89% (97/109) ±6% | 91% (99/109) ±6% | 92% (100/109) ±5% | 0.755 |
| scrapy+md | embedding | 66% (72/109) ±9% | 83% (91/109) ±7% | 91% (99/109) ±6% | 93% (101/109) ±5% | 94% (102/109) ±5% | 0.757 |
| scrapy+md | bm25 | 26% (28/109) ±8% | 40% (44/109) ±9% | 50% (55/109) ±9% | 70% (76/109) ±9% | 83% (90/109) ±7% | 0.381 |
| scrapy+md | hybrid | 61% (66/109) ±9% | 80% (87/109) ±7% | 88% (96/109) ±6% | 93% (101/109) ±5% | 93% (101/109) ±5% | 0.717 |
| scrapy+md | reranked | 55% (60/109) ±9% | 82% (89/109) ±7% | 87% (95/109) ±6% | 92% (100/109) ±5% | 94% (102/109) ±5% | 0.694 |
| crawlee | embedding | 72% (78/109) ±8% | 83% (90/109) ±7% | 88% (96/109) ±6% | 92% (100/109) ±5% | 93% (101/109) ±5% | 0.782 |
| crawlee | bm25 | 30% (33/109) ±9% | 39% (43/109) ±9% | 51% (56/109) ±9% | 68% (74/109) ±9% | 79% (86/109) ±8% | 0.401 |
| crawlee | hybrid | 62% (68/109) ±9% | 80% (87/109) ±7% | 85% (93/109) ±7% | 92% (100/109) ±5% | 92% (100/109) ±5% | 0.717 |
| crawlee | reranked | 58% (63/109) ±9% | 82% (89/109) ±7% | 86% (94/109) ±6% | 90% (98/109) ±6% | 93% (101/109) ±5% | 0.704 |
| colly+md | embedding | 69% (75/109) ±9% | 80% (87/109) ±7% | 86% (94/109) ±6% | 91% (99/109) ±6% | 92% (100/109) ±5% | 0.759 |
| colly+md | bm25 | 27% (29/109) ±8% | 39% (42/109) ±9% | 50% (55/109) ±9% | 69% (75/109) ±9% | 80% (87/109) ±7% | 0.382 |
| colly+md | hybrid | 62% (68/109) ±9% | 78% (85/109) ±8% | 83% (90/109) ±7% | 92% (100/109) ±5% | 93% (101/109) ±5% | 0.714 |
| colly+md | reranked | 53% (58/109) ±9% | 81% (88/109) ±7% | 86% (94/109) ±6% | 92% (100/109) ±5% | 94% (102/109) ±5% | 0.681 |
| playwright | embedding | 73% (80/109) ±8% | 83% (91/109) ±7% | 90% (98/109) ±6% | 94% (102/109) ±5% | 94% (102/109) ±5% | 0.799 |
| playwright | bm25 | 33% (36/109) ±9% | 42% (46/109) ±9% | 54% (59/109) ±9% | 72% (79/109) ±8% | 82% (89/109) ±7% | 0.430 |
| playwright | hybrid | 65% (71/109) ±9% | 82% (89/109) ±7% | 85% (93/109) ±7% | 94% (102/109) ±5% | 94% (102/109) ±5% | 0.737 |
| playwright | reranked | 61% (67/109) ±9% | 84% (92/109) ±7% | 89% (97/109) ±6% | 93% (101/109) ±5% | 94% (102/109) ±5% | 0.735 |

> **Column definitions:** **Hit@K** = percentage of queries where the correct source page appeared in the top K results (shown as % with raw counts). **MRR** (Mean Reciprocal Rank) = average of 1/rank for correct results (1.0 = always rank 1, 0.5 = always rank 2). **Mode** = retrieval strategy used (see definitions above).

## Summary: embedding-only (hit rate at multiple K values)

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Avg words |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 68% (74/109) ±9% | 83% (90/109) ±7% | 86% (94/109) ±6% | 91% (99/109) ±6% | 91% (99/109) ±6% | 0.759 | 22132 | 147 |
| crawl4ai | 71% (77/109) ±8% | 83% (91/109) ±7% | 89% (97/109) ±6% | 90% (98/109) ±6% | 93% (101/109) ±5% | 0.771 | 32735 | 132 |
| crawl4ai-raw | 70% (76/109) ±9% | 83% (91/109) ±7% | 89% (97/109) ±6% | 90% (98/109) ±6% | 92% (100/109) ±5% | 0.767 | 32735 | 132 |
| scrapy+md | 66% (72/109) ±9% | 83% (91/109) ±7% | 91% (99/109) ±6% | 93% (101/109) ±5% | 94% (102/109) ±5% | 0.757 | 23854 | 133 |
| crawlee | 72% (78/109) ±8% | 83% (90/109) ±7% | 88% (96/109) ±6% | 92% (100/109) ±5% | 93% (101/109) ±5% | 0.782 | 47560 | 212 |
| colly+md | 69% (75/109) ±9% | 80% (87/109) ±7% | 86% (94/109) ±6% | 91% (99/109) ±6% | 92% (100/109) ±5% | 0.759 | 42934 | 210 |
| playwright | 73% (80/109) ±8% | 83% (91/109) ±7% | 90% (98/109) ±6% | 94% (102/109) ±5% | 94% (102/109) ±5% | 0.799 | 46439 | 212 |

> **Column definitions:** **Hit@K** = correct source page in top K results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). **Chunks** = total chunks produced by this tool (across all pages in common sites). **Avg words** = mean words per chunk.

## Per-category breakdown (embedding mode)

Query categories reveal where crawlers actually differ. Categories like `js-rendered` and `structured-data` stress-test browser rendering and table extraction, while `api-function` and `conceptual` queries test basic content retrieval.

| Category | Tool | Hit@10 | MRR | Queries |
|---|---|---|---|---|
| api-function | crawlee | 97% (36/37) | 0.756 | 37 |
| api-function | colly+md | 97% (36/37) | 0.720 | 37 |
| api-function | playwright | 97% (36/37) | 0.756 | 37 |
| api-function | **markcrawl** | 95% (35/37) | 0.685 | 37 |
| api-function | crawl4ai | 95% (35/37) | 0.674 | 37 |
| api-function | crawl4ai-raw | 95% (35/37) | 0.674 | 37 |
| api-function | scrapy+md | 95% (35/37) | 0.665 | 37 |
| code-example | **markcrawl** | 100% (11/11) | 0.818 | 11 |
| code-example | crawl4ai | 100% (11/11) | 0.806 | 11 |
| code-example | crawl4ai-raw | 100% (11/11) | 0.806 | 11 |
| code-example | scrapy+md | 100% (11/11) | 0.818 | 11 |
| code-example | crawlee | 100% (11/11) | 0.821 | 11 |
| code-example | colly+md | 100% (11/11) | 0.814 | 11 |
| code-example | playwright | 100% (11/11) | 0.821 | 11 |
| conceptual | scrapy+md | 96% (25/26) | 0.773 | 26 |
| conceptual | **markcrawl** | 92% (24/26) | 0.694 | 26 |
| conceptual | crawl4ai | 92% (24/26) | 0.837 | 26 |
| conceptual | crawl4ai-raw | 92% (24/26) | 0.816 | 26 |
| conceptual | colly+md | 92% (24/26) | 0.672 | 26 |
| conceptual | playwright | 92% (24/26) | 0.783 | 26 |
| conceptual | crawlee | 88% (23/26) | 0.713 | 26 |
| cross-page | **markcrawl** | 100% (5/5) | 1.000 | 5 |
| cross-page | crawl4ai | 100% (5/5) | 1.000 | 5 |
| cross-page | crawl4ai-raw | 100% (5/5) | 1.000 | 5 |
| cross-page | scrapy+md | 100% (5/5) | 1.000 | 5 |
| cross-page | crawlee | 100% (5/5) | 1.000 | 5 |
| cross-page | colly+md | 100% (5/5) | 1.000 | 5 |
| cross-page | playwright | 100% (5/5) | 1.000 | 5 |
| factual-lookup | **markcrawl** | 88% (14/16) | 0.833 | 16 |
| factual-lookup | crawl4ai | 88% (14/16) | 0.825 | 16 |
| factual-lookup | crawl4ai-raw | 88% (14/16) | 0.825 | 16 |
| factual-lookup | scrapy+md | 88% (14/16) | 0.833 | 16 |
| factual-lookup | crawlee | 88% (14/16) | 0.875 | 16 |
| factual-lookup | colly+md | 88% (14/16) | 0.875 | 16 |
| factual-lookup | playwright | 88% (14/16) | 0.875 | 16 |
| js-rendered | **markcrawl** | 100% (5/5) | 1.000 | 5 |
| js-rendered | crawl4ai | 100% (5/5) | 0.900 | 5 |
| js-rendered | crawl4ai-raw | 100% (5/5) | 0.900 | 5 |
| js-rendered | scrapy+md | 100% (5/5) | 0.800 | 5 |
| js-rendered | crawlee | 100% (5/5) | 0.740 | 5 |
| js-rendered | colly+md | 100% (5/5) | 0.733 | 5 |
| js-rendered | playwright | 100% (5/5) | 0.750 | 5 |
| navigation | **markcrawl** | 100% (1/1) | 1.000 | 1 |
| navigation | crawl4ai | 100% (1/1) | 1.000 | 1 |
| navigation | crawl4ai-raw | 100% (1/1) | 1.000 | 1 |
| navigation | scrapy+md | 100% (1/1) | 1.000 | 1 |
| navigation | crawlee | 100% (1/1) | 1.000 | 1 |
| navigation | colly+md | 100% (1/1) | 1.000 | 1 |
| navigation | playwright | 100% (1/1) | 1.000 | 1 |
| structured-data | **markcrawl** | 75% (6/8) | 0.750 | 8 |
| structured-data | crawl4ai | 75% (6/8) | 0.604 | 8 |
| structured-data | crawl4ai-raw | 75% (6/8) | 0.604 | 8 |
| structured-data | scrapy+md | 75% (6/8) | 0.688 | 8 |
| structured-data | crawlee | 75% (6/8) | 0.750 | 8 |
| structured-data | colly+md | 75% (6/8) | 0.750 | 8 |
| structured-data | playwright | 75% (6/8) | 0.750 | 8 |

> **Column definitions:** **Category** = query type (see [METHODOLOGY.md](METHODOLOGY.md) for definitions). **Hit@10** = correct page in top 10 results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). **Queries** = number of queries in this category.

### Best tool per category

| Category | Best tool | Hit@10 | Spread |
|---|---|---|---|
| api-function | crawlee | 97% | 3% |
| code-example | **markcrawl** | 100% | 0% |
| conceptual | scrapy+md | 96% | 8% |
| cross-page | **markcrawl** | 100% | 0% |
| factual-lookup | **markcrawl** | 88% | 0% |
| js-rendered | **markcrawl** | 100% | 0% |
| navigation | **markcrawl** | 100% | 0% |
| structured-data | **markcrawl** | 75% | 0% |

_Spread = difference between best and worst tool. High spread categories are where crawler choice matters most._


## quotes-toscrape

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.917 | 18 | 14 |
| crawl4ai | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 23 | 15 |
| crawl4ai-raw | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 23 | 15 |
| scrapy+md | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 25 | 15 |
| crawlee | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 28 | 15 |
| colly+md | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 28 | 15 |
| playwright | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 28 | 15 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for quotes-toscrape</summary>

**Q1: What did Albert Einstein say about thinking and the world?** [factual-lookup]
*(expects URL containing: `author/Albert-Einstein`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | quotes.toscrape.com/tag/thinking/page/1/ | 0.646 | quotes.toscrape.com/tag/change/page/1/ | 0.577 | quotes.toscrape.com/author/Albert-Einstein | 0.568 |
| crawl4ai | #1 | quotes.toscrape.com/author/Albert-Einstein | 0.581 | quotes.toscrape.com/author/Albert-Einstein | 0.555 | quotes.toscrape.com/tag/thinking/page/1/ | 0.481 |
| crawl4ai-raw | #1 | quotes.toscrape.com/author/Albert-Einstein | 0.581 | quotes.toscrape.com/author/Albert-Einstein | 0.555 | quotes.toscrape.com/tag/thinking/page/1/ | 0.481 |
| scrapy+md | #1 | quotes.toscrape.com/author/Albert-Einstein/ | 0.568 | quotes.toscrape.com/author/Albert-Einstein/ | 0.549 | quotes.toscrape.com/author/Albert-Einstein/ | 0.487 |
| crawlee | #1 | quotes.toscrape.com/author/Albert-Einstein | 0.568 | quotes.toscrape.com/author/Albert-Einstein | 0.549 | quotes.toscrape.com/author/Albert-Einstein | 0.487 |
| colly+md | #1 | quotes.toscrape.com/author/Albert-Einstein | 0.568 | quotes.toscrape.com/author/Albert-Einstein | 0.549 | quotes.toscrape.com/author/Albert-Einstein | 0.487 |
| playwright | #1 | quotes.toscrape.com/author/Albert-Einstein | 0.568 | quotes.toscrape.com/author/Albert-Einstein | 0.549 | quotes.toscrape.com/author/Albert-Einstein | 0.487 |


**Q2: Which quotes are tagged with 'change'?** [cross-page]
*(expects URL containing: `tag/change`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.600 | quotes.toscrape.com/tag/thinking/page/1/ | 0.478 | quotes.toscrape.com/tag/life/ | 0.440 |
| crawl4ai | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.626 | quotes.toscrape.com/tag/thinking/page/1/ | 0.528 | quotes.toscrape.com/ | 0.485 |
| crawl4ai-raw | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.626 | quotes.toscrape.com/tag/thinking/page/1/ | 0.528 | quotes.toscrape.com/ | 0.485 |
| scrapy+md | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.584 | quotes.toscrape.com/tag/thinking/page/1/ | 0.524 | quotes.toscrape.com/ | 0.481 |
| crawlee | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.565 | quotes.toscrape.com/tag/thinking/page/1/ | 0.511 | quotes.toscrape.com/ | 0.487 |
| colly+md | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.565 | quotes.toscrape.com/tag/thinking/page/1/ | 0.511 | quotes.toscrape.com/ | 0.487 |
| playwright | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.565 | quotes.toscrape.com/tag/thinking/page/1/ | 0.511 | quotes.toscrape.com/ | 0.487 |


**Q3: What did Steve Martin say about sunshine?** [factual-lookup]
*(expects URL containing: `author/Steve-Martin`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/author/Steve-Martin | 0.573 | quotes.toscrape.com/ | 0.411 | quotes.toscrape.com/tag/life/ | 0.303 |
| crawl4ai | #1 | quotes.toscrape.com/author/Steve-Martin | 0.553 | quotes.toscrape.com/tag/life/ | 0.289 | quotes.toscrape.com/ | 0.280 |
| crawl4ai-raw | #1 | quotes.toscrape.com/author/Steve-Martin | 0.553 | quotes.toscrape.com/tag/life/ | 0.289 | quotes.toscrape.com/ | 0.280 |
| scrapy+md | #1 | quotes.toscrape.com/author/Steve-Martin/ | 0.538 | quotes.toscrape.com/ | 0.284 | quotes.toscrape.com/tag/life/ | 0.280 |
| crawlee | #1 | quotes.toscrape.com/author/Steve-Martin | 0.464 | quotes.toscrape.com/ | 0.284 | quotes.toscrape.com/tag/life/ | 0.280 |
| colly+md | #1 | quotes.toscrape.com/author/Steve-Martin | 0.464 | quotes.toscrape.com/ | 0.284 | quotes.toscrape.com/tag/life/ | 0.280 |
| playwright | #1 | quotes.toscrape.com/author/Steve-Martin | 0.464 | quotes.toscrape.com/ | 0.284 | quotes.toscrape.com/tag/life/ | 0.280 |


**Q4: What quotes are about thinking deeply?** [cross-page]
*(expects URL containing: `tag/thinking`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.539 | quotes.toscrape.com/ | 0.510 | quotes.toscrape.com/tag/life/ | 0.480 |
| crawl4ai | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.594 | quotes.toscrape.com/tag/change/page/1/ | 0.544 | quotes.toscrape.com/ | 0.497 |
| crawl4ai-raw | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.594 | quotes.toscrape.com/tag/change/page/1/ | 0.544 | quotes.toscrape.com/ | 0.497 |
| scrapy+md | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.546 | quotes.toscrape.com/tag/change/page/1/ | 0.497 | quotes.toscrape.com/ | 0.490 |
| crawlee | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.531 | quotes.toscrape.com/tag/change/page/1/ | 0.494 | quotes.toscrape.com/ | 0.491 |
| colly+md | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.531 | quotes.toscrape.com/tag/change/page/1/ | 0.494 | quotes.toscrape.com/ | 0.491 |
| playwright | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.531 | quotes.toscrape.com/tag/change/page/1/ | 0.494 | quotes.toscrape.com/ | 0.491 |


**Q5: What did Eleanor Roosevelt say about life?** [factual-lookup]
*(expects URL containing: `author/Eleanor-Roosevelt`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/author/Eleanor-Roosevelt | 0.623 | quotes.toscrape.com/tag/life/ | 0.507 | quotes.toscrape.com/tag/life/ | 0.506 |
| crawl4ai | #1 | quotes.toscrape.com/author/Eleanor-Roosevelt | 0.620 | quotes.toscrape.com/tag/life/ | 0.477 | quotes.toscrape.com/tag/life/ | 0.469 |
| crawl4ai-raw | #1 | quotes.toscrape.com/author/Eleanor-Roosevelt | 0.620 | quotes.toscrape.com/tag/life/ | 0.477 | quotes.toscrape.com/tag/life/ | 0.469 |
| scrapy+md | #1 | quotes.toscrape.com/author/Eleanor-Roosevelt/ | 0.587 | quotes.toscrape.com/tag/life/ | 0.479 | quotes.toscrape.com/tag/life/ | 0.478 |
| crawlee | #1 | quotes.toscrape.com/author/Eleanor-Roosevelt | 0.526 | quotes.toscrape.com/tag/life/ | 0.479 | quotes.toscrape.com/tag/life/ | 0.478 |
| colly+md | #1 | quotes.toscrape.com/author/Eleanor-Roosevelt | 0.526 | quotes.toscrape.com/tag/life/ | 0.479 | quotes.toscrape.com/tag/life/ | 0.478 |
| playwright | #1 | quotes.toscrape.com/author/Eleanor-Roosevelt | 0.526 | quotes.toscrape.com/tag/life/ | 0.479 | quotes.toscrape.com/tag/life/ | 0.477 |


**Q6: Which quotes are tagged about choices and abilities?** [cross-page]
*(expects URL containing: `tag/abilities`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.673 | quotes.toscrape.com/tag/choices/page/1/ | 0.654 | quotes.toscrape.com/tag/life/ | 0.502 |
| crawl4ai | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.679 | quotes.toscrape.com/tag/choices/page/1/ | 0.667 | quotes.toscrape.com/ | 0.491 |
| crawl4ai-raw | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.679 | quotes.toscrape.com/tag/choices/page/1/ | 0.667 | quotes.toscrape.com/ | 0.491 |
| scrapy+md | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.622 | quotes.toscrape.com/tag/choices/page/1/ | 0.614 | quotes.toscrape.com/ | 0.490 |
| crawlee | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.587 | quotes.toscrape.com/tag/choices/page/1/ | 0.580 | quotes.toscrape.com/ | 0.493 |
| colly+md | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.587 | quotes.toscrape.com/tag/choices/page/1/ | 0.580 | quotes.toscrape.com/ | 0.493 |
| playwright | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.587 | quotes.toscrape.com/tag/choices/page/1/ | 0.580 | quotes.toscrape.com/ | 0.493 |


**Q7: What quotes are about friendship?** [cross-page]
*(expects URL containing: `tag/friendship`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/tag/friendship/ | 0.598 | quotes.toscrape.com/tag/life/ | 0.481 | quotes.toscrape.com/ | 0.467 |
| crawl4ai | #1 | quotes.toscrape.com/tag/friendship/ | 0.576 | quotes.toscrape.com/tag/books/page/1/ | 0.475 | quotes.toscrape.com/ | 0.469 |
| crawl4ai-raw | #1 | quotes.toscrape.com/tag/friendship/ | 0.576 | quotes.toscrape.com/tag/books/page/1/ | 0.475 | quotes.toscrape.com/ | 0.469 |
| scrapy+md | #1 | quotes.toscrape.com/tag/friendship/ | 0.552 | quotes.toscrape.com/tag/books/page/1/ | 0.468 | quotes.toscrape.com/tag/life/ | 0.466 |
| crawlee | #1 | quotes.toscrape.com/tag/friendship/ | 0.550 | quotes.toscrape.com/tag/books/page/1/ | 0.484 | quotes.toscrape.com/ | 0.476 |
| colly+md | #1 | quotes.toscrape.com/tag/friendship/ | 0.550 | quotes.toscrape.com/tag/books/page/1/ | 0.484 | quotes.toscrape.com/ | 0.476 |
| playwright | #1 | quotes.toscrape.com/tag/friendship/ | 0.550 | quotes.toscrape.com/tag/books/page/1/ | 0.484 | quotes.toscrape.com/ | 0.476 |


**Q8: What are the quotes about love?** [cross-page]
*(expects URL containing: `tag/love`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/tag/love/page/1/ | 0.586 | quotes.toscrape.com/tag/love/page/1/ | 0.574 | quotes.toscrape.com/tag/friendship/ | 0.492 |
| crawl4ai | #1 | quotes.toscrape.com/tag/love/page/1/ | 0.570 | quotes.toscrape.com/tag/love/page/1/ | 0.563 | quotes.toscrape.com/tag/friendship/ | 0.529 |
| crawl4ai-raw | #1 | quotes.toscrape.com/tag/love/page/1/ | 0.570 | quotes.toscrape.com/tag/love/page/1/ | 0.563 | quotes.toscrape.com/tag/friendship/ | 0.529 |
| scrapy+md | #1 | quotes.toscrape.com/tag/love/page/1/ | 0.555 | quotes.toscrape.com/tag/love/page/1/ | 0.546 | quotes.toscrape.com/tag/friendship/ | 0.525 |
| crawlee | #1 | quotes.toscrape.com/tag/love/page/1/ | 0.555 | quotes.toscrape.com/tag/love/page/1/ | 0.546 | quotes.toscrape.com/tag/friendship/ | 0.542 |
| colly+md | #1 | quotes.toscrape.com/tag/love/page/1/ | 0.555 | quotes.toscrape.com/tag/love/page/1/ | 0.546 | quotes.toscrape.com/tag/friendship/ | 0.542 |
| playwright | #1 | quotes.toscrape.com/tag/love/page/1/ | 0.555 | quotes.toscrape.com/tag/love/page/1/ | 0.546 | quotes.toscrape.com/tag/friendship/ | 0.542 |


</details>

## books-toscrape

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 80% (8/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 0.800 | 139 | 60 |
| crawl4ai | 50% (5/10) | 70% (7/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 0.603 | 628 | 60 |
| crawl4ai-raw | 50% (5/10) | 70% (7/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 0.603 | 628 | 60 |
| scrapy+md | 70% (7/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 0.750 | 130 | 60 |
| crawlee | 80% (8/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 0.800 | 134 | 60 |
| colly+md | 80% (8/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 0.800 | 134 | 60 |
| playwright | 80% (8/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 80% (8/10) | 0.800 | 134 | 60 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for books-toscrape</summary>

**Q1: What mystery and thriller books are in the catalog?** [structured-data]
*(expects URL containing: `category/books/mystery`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/myster | 0.495 | books.toscrape.com/catalogue/category/books/thrill | 0.481 | books.toscrape.com/catalogue/category/books/myster | 0.467 |
| crawl4ai | #3 | books.toscrape.com/catalogue/category/books/suspen | 0.538 | books.toscrape.com/catalogue/category/books/thrill | 0.520 | books.toscrape.com/catalogue/category/books/myster | 0.513 |
| crawl4ai-raw | #3 | books.toscrape.com/catalogue/category/books/suspen | 0.538 | books.toscrape.com/catalogue/category/books/thrill | 0.520 | books.toscrape.com/catalogue/category/books/myster | 0.513 |
| scrapy+md | #1 | books.toscrape.com/catalogue/category/books/myster | 0.495 | books.toscrape.com/ | 0.479 | books.toscrape.com/catalogue/category/books/suspen | 0.460 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/myster | 0.514 | books.toscrape.com/catalogue/category/books/myster | 0.495 | books.toscrape.com/catalogue/category/books/thrill | 0.483 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/myster | 0.514 | books.toscrape.com/catalogue/category/books/myster | 0.495 | books.toscrape.com/catalogue/category/books/thrill | 0.483 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/myster | 0.514 | books.toscrape.com/catalogue/category/books/myster | 0.495 | books.toscrape.com/catalogue/category/books/thrill | 0.483 |


**Q2: What science fiction books are available?** [structured-data]
*(expects URL containing: `category/books/science-fiction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.460 | books.toscrape.com/catalogue/libertarianism-for-be | 0.410 | books.toscrape.com/catalogue/category/books/scienc | 0.396 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.533 | books.toscrape.com/catalogue/category/books/scienc | 0.471 | books.toscrape.com/catalogue/libertarianism-for-be | 0.465 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.533 | books.toscrape.com/catalogue/category/books/scienc | 0.471 | books.toscrape.com/catalogue/libertarianism-for-be | 0.465 |
| scrapy+md | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.510 | books.toscrape.com/catalogue/libertarianism-for-be | 0.404 | books.toscrape.com/catalogue/category/books/scienc | 0.394 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.510 | books.toscrape.com/catalogue/category/books/scienc | 0.466 | books.toscrape.com/catalogue/libertarianism-for-be | 0.404 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.510 | books.toscrape.com/catalogue/category/books/scienc | 0.466 | books.toscrape.com/catalogue/libertarianism-for-be | 0.404 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.510 | books.toscrape.com/catalogue/category/books/scienc | 0.466 | books.toscrape.com/catalogue/libertarianism-for-be | 0.404 |


**Q3: What is the book Sharp Objects about?** [factual-lookup]
*(expects URL containing: `sharp-objects`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.606 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.574 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.485 |
| crawl4ai | #5 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.648 | books.toscrape.com/catalogue/the-coming-woman-a-no | 0.648 | books.toscrape.com/catalogue/the-dirty-little-secr | 0.648 |
| crawl4ai-raw | #5 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.648 | books.toscrape.com/catalogue/the-coming-woman-a-no | 0.648 | books.toscrape.com/catalogue/the-dirty-little-secr | 0.648 |
| scrapy+md | #1 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.606 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.481 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.447 |
| crawlee | #1 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.606 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.533 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.481 |
| colly+md | #1 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.606 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.533 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.481 |
| playwright | #1 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.606 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.533 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.481 |


**Q4: What biography books are in the catalog?** [structured-data]
*(expects URL containing: `category/books/biography`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.415 | books.toscrape.com/catalogue/category/books/autobi | 0.405 | books.toscrape.com/catalogue/set-me-free_988/index | 0.402 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.449 | books.toscrape.com/catalogue/category/books/autobi | 0.441 | books.toscrape.com/catalogue/category/books/busine | 0.434 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.449 | books.toscrape.com/catalogue/category/books/autobi | 0.441 | books.toscrape.com/catalogue/category/books/busine | 0.434 |
| scrapy+md | #2 | books.toscrape.com/ | 0.419 | books.toscrape.com/catalogue/category/books/biogra | 0.377 | books.toscrape.com/catalogue/starving-hearts-trian | 0.373 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.419 | books.toscrape.com/ | 0.416 | books.toscrape.com/catalogue/category/books_1/inde | 0.389 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.419 | books.toscrape.com/ | 0.416 | books.toscrape.com/catalogue/category/books_1/inde | 0.389 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.419 | books.toscrape.com/ | 0.416 | books.toscrape.com/catalogue/category/books_1/inde | 0.389 |


**Q5: What horror books are in the catalog?** [structured-data]
*(expects URL containing: `category/books/horror`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/horror | 0.543 | books.toscrape.com/catalogue/category/books/young- | 0.419 | books.toscrape.com/catalogue/category/books/thrill | 0.418 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/horror | 0.492 | books.toscrape.com/catalogue/category/books/suspen | 0.489 | books.toscrape.com/catalogue/category/books/horror | 0.485 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/horror | 0.492 | books.toscrape.com/catalogue/category/books/suspen | 0.489 | books.toscrape.com/catalogue/category/books/horror | 0.484 |
| scrapy+md | #1 | books.toscrape.com/catalogue/category/books/horror | 0.515 | books.toscrape.com/ | 0.463 | books.toscrape.com/catalogue/category/books/horror | 0.440 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/horror | 0.515 | books.toscrape.com/catalogue/category/books/horror | 0.511 | books.toscrape.com/ | 0.468 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/horror | 0.515 | books.toscrape.com/catalogue/category/books/horror | 0.511 | books.toscrape.com/ | 0.468 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/horror | 0.515 | books.toscrape.com/catalogue/category/books/horror | 0.511 | books.toscrape.com/ | 0.468 |


**Q6: What poetry books can I find?** [structured-data]
*(expects URL containing: `category/books/poetry`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.552 | books.toscrape.com/catalogue/the-black-maria_991/i | 0.388 | books.toscrape.com/catalogue/set-me-free_988/index | 0.385 |
| crawl4ai | #2 | books.toscrape.com/catalogue/page-2.html | 0.507 | books.toscrape.com/catalogue/category/books/poetry | 0.498 | books.toscrape.com/catalogue/category/books/poetry | 0.487 |
| crawl4ai-raw | #2 | books.toscrape.com/catalogue/page-2.html | 0.506 | books.toscrape.com/catalogue/category/books/poetry | 0.498 | books.toscrape.com/catalogue/category/books/poetry | 0.487 |
| scrapy+md | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.545 | books.toscrape.com/catalogue/shakespeares-sonnets_ | 0.401 | books.toscrape.com/catalogue/category/books/poetry | 0.389 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.545 | books.toscrape.com/catalogue/category/books/poetry | 0.472 | books.toscrape.com/catalogue/shakespeares-sonnets_ | 0.412 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.545 | books.toscrape.com/catalogue/category/books/poetry | 0.472 | books.toscrape.com/catalogue/shakespeares-sonnets_ | 0.412 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.545 | books.toscrape.com/catalogue/category/books/poetry | 0.472 | books.toscrape.com/catalogue/shakespeares-sonnets_ | 0.412 |


**Q7: What fantasy books are in the bookstore?** [structured-data]
*(expects URL containing: `category/books/fantasy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.502 | books.toscrape.com/catalogue/category/books/fantas | 0.483 | books.toscrape.com/catalogue/category/books/scienc | 0.415 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.447 | books.toscrape.com/catalogue/category/books/fantas | 0.433 | books.toscrape.com/catalogue/category/books/fantas | 0.432 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.447 | books.toscrape.com/catalogue/category/books/fantas | 0.433 | books.toscrape.com/catalogue/category/books/fantas | 0.432 |
| scrapy+md | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.487 | books.toscrape.com/catalogue/category/books/fantas | 0.483 | books.toscrape.com/catalogue/category/books/scienc | 0.416 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.487 | books.toscrape.com/catalogue/category/books/fantas | 0.483 | books.toscrape.com/catalogue/category/books/fantas | 0.427 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.487 | books.toscrape.com/catalogue/category/books/fantas | 0.483 | books.toscrape.com/catalogue/category/books/fantas | 0.427 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.487 | books.toscrape.com/catalogue/category/books/fantas | 0.483 | books.toscrape.com/catalogue/category/books/fantas | 0.427 |


**Q8: What philosophy books are available to read?** [structured-data]
*(expects URL containing: `category/books/philosophy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | books.toscrape.com/catalogue/category/books/psycho | 0.375 | books.toscrape.com/catalogue/its-only-the-himalaya | 0.374 | books.toscrape.com/catalogue/category/books_1/inde | 0.365 |
| crawl4ai | miss | books.toscrape.com/catalogue/category/books/psycho | 0.414 | books.toscrape.com/catalogue/category/books/spirit | 0.407 | books.toscrape.com/catalogue/category/books/autobi | 0.406 |
| crawl4ai-raw | miss | books.toscrape.com/catalogue/category/books/psycho | 0.414 | books.toscrape.com/catalogue/category/books/spirit | 0.407 | books.toscrape.com/catalogue/category/books/autobi | 0.406 |
| scrapy+md | miss | books.toscrape.com/catalogue/libertarianism-for-be | 0.363 | books.toscrape.com/catalogue/category/books/psycho | 0.362 | books.toscrape.com/catalogue/libertarianism-for-be | 0.362 |
| crawlee | miss | books.toscrape.com/catalogue/libertarianism-for-be | 0.387 | books.toscrape.com/catalogue/category/books/psycho | 0.380 | books.toscrape.com/catalogue/libertarianism-for-be | 0.363 |
| colly+md | miss | books.toscrape.com/catalogue/libertarianism-for-be | 0.387 | books.toscrape.com/catalogue/category/books/psycho | 0.380 | books.toscrape.com/catalogue/libertarianism-for-be | 0.363 |
| playwright | miss | books.toscrape.com/catalogue/libertarianism-for-be | 0.387 | books.toscrape.com/catalogue/category/books/psycho | 0.380 | books.toscrape.com/catalogue/libertarianism-for-be | 0.363 |


**Q9: What is the book Sapiens about?** [factual-lookup]
*(expects URL containing: `sapiens`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.623 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.621 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.538 |
| crawl4ai | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.630 | books.toscrape.com/catalogue/starving-hearts-trian | 0.615 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.583 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.630 | books.toscrape.com/catalogue/starving-hearts-trian | 0.615 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.583 |
| scrapy+md | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.621 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.542 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.416 |
| crawlee | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.621 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.564 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.542 |
| colly+md | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.621 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.564 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.542 |
| playwright | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.621 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.564 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.542 |


**Q10: What romance novels are available?** [structured-data]
*(expects URL containing: `category/books/romance`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | books.toscrape.com/catalogue/category/books/new-ad | 0.419 | books.toscrape.com/catalogue/category/books/christ | 0.414 | books.toscrape.com/catalogue/category/books/womens | 0.413 |
| crawl4ai | miss | books.toscrape.com/catalogue/category/books/add-a- | 0.545 | books.toscrape.com/catalogue/category/books/womens | 0.477 | books.toscrape.com/catalogue/category/books/adult- | 0.470 |
| crawl4ai-raw | miss | books.toscrape.com/catalogue/category/books/add-a- | 0.545 | books.toscrape.com/catalogue/category/books/womens | 0.477 | books.toscrape.com/catalogue/category/books/adult- | 0.470 |
| scrapy+md | miss | books.toscrape.com/catalogue/category/books/womens | 0.457 | books.toscrape.com/catalogue/category/books/new-ad | 0.422 | books.toscrape.com/ | 0.415 |
| crawlee | miss | books.toscrape.com/catalogue/category/books/womens | 0.457 | books.toscrape.com/catalogue/category/books/womens | 0.437 | books.toscrape.com/catalogue/category/books/new-ad | 0.429 |
| colly+md | miss | books.toscrape.com/catalogue/category/books/womens | 0.457 | books.toscrape.com/catalogue/category/books/womens | 0.437 | books.toscrape.com/catalogue/category/books/new-ad | 0.429 |
| playwright | miss | books.toscrape.com/catalogue/category/books/womens | 0.457 | books.toscrape.com/catalogue/category/books/womens | 0.437 | books.toscrape.com/catalogue/category/books/new-ad | 0.429 |


</details>

## fastapi-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 65% (13/20) | 90% (18/20) | 95% (19/20) | 100% (20/20) | 100% (20/20) | 0.779 | 3413 | 153 |
| crawl4ai | 75% (15/20) | 95% (19/20) | 100% (20/20) | 100% (20/20) | 100% (20/20) | 0.835 | 4143 | 153 |
| crawl4ai-raw | 75% (15/20) | 95% (19/20) | 100% (20/20) | 100% (20/20) | 100% (20/20) | 0.835 | 4144 | 153 |
| scrapy+md | 65% (13/20) | 90% (18/20) | 100% (20/20) | 100% (20/20) | 100% (20/20) | 0.781 | 3741 | 153 |
| crawlee | 75% (15/20) | 100% (20/20) | 100% (20/20) | 100% (20/20) | 100% (20/20) | 0.858 | 3856 | 153 |
| colly+md | 65% (13/20) | 90% (18/20) | 95% (19/20) | 100% (20/20) | 100% (20/20) | 0.777 | 3871 | 153 |
| playwright | 75% (15/20) | 100% (20/20) | 100% (20/20) | 100% (20/20) | 100% (20/20) | 0.858 | 3857 | 153 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for fastapi-docs</summary>

**Q1: How do I add authentication to a FastAPI endpoint?** [api-function]
*(expects URL containing: `security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.600 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.594 | fastapi.tiangolo.com/tutorial/security/ | 0.565 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.631 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.599 | fastapi.tiangolo.com/tutorial/security/ | 0.593 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.631 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.598 | fastapi.tiangolo.com/tutorial/security/ | 0.593 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.600 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.594 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.550 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.604 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.591 | fastapi.tiangolo.com/tutorial/security/ | 0.568 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.600 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.594 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.550 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.604 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.591 | fastapi.tiangolo.com/tutorial/security/ | 0.568 |


**Q2: How do I define query parameters in the FastAPI reference?** [api-function]
*(expects URL containing: `reference/fastapi`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | fastapi.tiangolo.com/tutorial/query-params/ | 0.662 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.657 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.636 |
| crawl4ai | #1 | fastapi.tiangolo.com/reference/parameters/ | 0.671 | fastapi.tiangolo.com/tutorial/query-params/ | 0.662 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.659 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/reference/parameters/ | 0.671 | fastapi.tiangolo.com/tutorial/query-params/ | 0.662 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.659 |
| scrapy+md | #5 | fastapi.tiangolo.com/tutorial/query-params/ | 0.662 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.636 | fastapi.tiangolo.com/tutorial/query-params/ | 0.617 |
| crawlee | #2 | fastapi.tiangolo.com/tutorial/query-params/ | 0.649 | fastapi.tiangolo.com/reference/parameters/ | 0.642 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.634 |
| colly+md | #8 | fastapi.tiangolo.com/tutorial/query-params/ | 0.662 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.636 | fastapi.tiangolo.com/tutorial/query-params/ | 0.635 |
| playwright | #2 | fastapi.tiangolo.com/tutorial/query-params/ | 0.649 | fastapi.tiangolo.com/reference/parameters/ | 0.642 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.634 |


**Q3: How does FastAPI handle JSON encoding and base64 bytes?** [code-example]
*(expects URL containing: `json-base64-bytes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.609 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.582 | fastapi.tiangolo.com/tutorial/encoder/ | 0.579 |
| crawl4ai | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.654 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.645 | fastapi.tiangolo.com/reference/encoders/ | 0.635 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.654 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.645 | fastapi.tiangolo.com/reference/encoders/ | 0.635 |
| scrapy+md | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.609 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.582 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.572 |
| crawlee | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.647 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.606 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.578 |
| colly+md | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.609 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.582 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.572 |
| playwright | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.647 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.606 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.579 |


**Q4: How do I use OAuth2 with password flow in FastAPI?** [code-example]
*(expects URL containing: `simple-oauth2`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | fastapi.tiangolo.com/reference/openapi/models/ | 0.679 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.670 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.657 |
| crawl4ai | #5 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.719 | fastapi.tiangolo.com/reference/security/ | 0.712 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.706 |
| crawl4ai-raw | #5 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.719 | fastapi.tiangolo.com/reference/security/ | 0.712 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.706 |
| scrapy+md | #4 | fastapi.tiangolo.com/reference/openapi/models/ | 0.679 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.667 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.657 |
| crawlee | #3 | fastapi.tiangolo.com/reference/security/ | 0.712 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.682 | fastapi.tiangolo.com/advanced/security/oauth2-scop | 0.674 |
| colly+md | #4 | fastapi.tiangolo.com/reference/openapi/models/ | 0.679 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.667 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.657 |
| playwright | #3 | fastapi.tiangolo.com/reference/security/ | 0.712 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.682 | fastapi.tiangolo.com/advanced/security/oauth2-scop | 0.674 |


**Q5: How do I use WebSockets in FastAPI?** [api-function]
*(expects URL containing: `websockets`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.810 | fastapi.tiangolo.com/advanced/websockets/ | 0.662 | fastapi.tiangolo.com/advanced/testing-websockets/ | 0.638 |
| crawl4ai | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.818 | fastapi.tiangolo.com/advanced/websockets/ | 0.678 | fastapi.tiangolo.com/advanced/websockets/ | 0.672 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.818 | fastapi.tiangolo.com/advanced/websockets/ | 0.678 | fastapi.tiangolo.com/advanced/websockets/ | 0.672 |
| scrapy+md | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.810 | fastapi.tiangolo.com/advanced/websockets/ | 0.662 | fastapi.tiangolo.com/reference/websockets/ | 0.625 |
| crawlee | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.811 | fastapi.tiangolo.com/advanced/websockets/ | 0.657 | fastapi.tiangolo.com/advanced/websockets/ | 0.645 |
| colly+md | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.810 | fastapi.tiangolo.com/advanced/websockets/ | 0.662 | fastapi.tiangolo.com/reference/websockets/ | 0.625 |
| playwright | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.811 | fastapi.tiangolo.com/advanced/websockets/ | 0.657 | fastapi.tiangolo.com/advanced/websockets/ | 0.645 |


**Q6: How do I define nested Pydantic models for request bodies?** [code-example]
*(expects URL containing: `body-nested-models`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.711 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.658 | fastapi.tiangolo.com/tutorial/body/ | 0.626 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.735 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.706 | fastapi.tiangolo.com/tutorial/body/ | 0.592 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.735 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.706 | fastapi.tiangolo.com/tutorial/body/ | 0.592 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.711 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.658 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.570 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.721 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.686 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.564 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.711 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.658 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.570 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.721 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.686 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.564 |


**Q7: How do I use middleware in FastAPI?** [api-function]
*(expects URL containing: `middleware`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | fastapi.tiangolo.com/reference/fastapi/ | 0.723 | fastapi.tiangolo.com/tutorial/middleware/ | 0.711 | fastapi.tiangolo.com/advanced/middleware/ | 0.639 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/middleware/ | 0.730 | fastapi.tiangolo.com/reference/fastapi/ | 0.716 | fastapi.tiangolo.com/tutorial/middleware/ | 0.707 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/middleware/ | 0.730 | fastapi.tiangolo.com/reference/fastapi/ | 0.716 | fastapi.tiangolo.com/tutorial/middleware/ | 0.707 |
| scrapy+md | #2 | fastapi.tiangolo.com/reference/fastapi/ | 0.723 | fastapi.tiangolo.com/tutorial/middleware/ | 0.711 | fastapi.tiangolo.com/advanced/middleware/ | 0.639 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/middleware/ | 0.719 | fastapi.tiangolo.com/reference/fastapi/ | 0.718 | fastapi.tiangolo.com/advanced/middleware/ | 0.643 |
| colly+md | #2 | fastapi.tiangolo.com/reference/fastapi/ | 0.723 | fastapi.tiangolo.com/tutorial/middleware/ | 0.711 | fastapi.tiangolo.com/advanced/middleware/ | 0.639 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/middleware/ | 0.719 | fastapi.tiangolo.com/reference/fastapi/ | 0.718 | fastapi.tiangolo.com/advanced/middleware/ | 0.643 |


**Q8: How do I deploy FastAPI to the cloud?** [conceptual]
*(expects URL containing: `deployment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | fastapi.tiangolo.com/ | 0.754 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.754 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.727 |
| crawl4ai | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.787 | fastapi.tiangolo.com/deployment/cloud/ | 0.786 | fastapi.tiangolo.com/deployment/cloud/ | 0.783 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.787 | fastapi.tiangolo.com/deployment/cloud/ | 0.786 | fastapi.tiangolo.com/deployment/cloud/ | 0.783 |
| scrapy+md | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.760 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.756 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.754 |
| crawlee | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.768 | fastapi.tiangolo.com/deployment/cloud/ | 0.762 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.762 |
| colly+md | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.760 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.756 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.754 |
| playwright | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.768 | fastapi.tiangolo.com/deployment/cloud/ | 0.762 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.762 |


**Q9: How do I handle file uploads in FastAPI?** [api-function]
*(expects URL containing: `request-files`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | fastapi.tiangolo.com/reference/uploadfile/ | 0.625 | fastapi.tiangolo.com/tutorial/request-files/ | 0.604 | fastapi.tiangolo.com/tutorial/request-files/ | 0.596 |
| crawl4ai | #3 | fastapi.tiangolo.com/reference/uploadfile/ | 0.685 | fastapi.tiangolo.com/reference/uploadfile/ | 0.641 | fastapi.tiangolo.com/tutorial/request-files/ | 0.638 |
| crawl4ai-raw | #3 | fastapi.tiangolo.com/reference/uploadfile/ | 0.685 | fastapi.tiangolo.com/reference/uploadfile/ | 0.640 | fastapi.tiangolo.com/tutorial/request-files/ | 0.638 |
| scrapy+md | #2 | fastapi.tiangolo.com/reference/uploadfile/ | 0.625 | fastapi.tiangolo.com/tutorial/request-files/ | 0.604 | fastapi.tiangolo.com/tutorial/request-files/ | 0.594 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/request-files/ | 0.638 | fastapi.tiangolo.com/reference/uploadfile/ | 0.634 | fastapi.tiangolo.com/tutorial/request-files/ | 0.598 |
| colly+md | #2 | fastapi.tiangolo.com/reference/uploadfile/ | 0.625 | fastapi.tiangolo.com/tutorial/request-files/ | 0.604 | fastapi.tiangolo.com/tutorial/request-files/ | 0.593 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/request-files/ | 0.638 | fastapi.tiangolo.com/reference/uploadfile/ | 0.634 | fastapi.tiangolo.com/tutorial/request-files/ | 0.600 |


**Q10: How do I write async tests for FastAPI applications?** [code-example]
*(expects URL containing: `async-tests`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/async-tests/ | 0.750 | fastapi.tiangolo.com/tutorial/testing/ | 0.623 | fastapi.tiangolo.com/advanced/async-tests/ | 0.604 |
| crawl4ai | #1 | fastapi.tiangolo.com/advanced/async-tests/ | 0.747 | fastapi.tiangolo.com/tutorial/testing/ | 0.657 | fastapi.tiangolo.com/advanced/async-tests/ | 0.632 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/advanced/async-tests/ | 0.747 | fastapi.tiangolo.com/tutorial/testing/ | 0.657 | fastapi.tiangolo.com/advanced/async-tests/ | 0.632 |
| scrapy+md | #1 | fastapi.tiangolo.com/advanced/async-tests/ | 0.750 | fastapi.tiangolo.com/tutorial/testing/ | 0.623 | fastapi.tiangolo.com/advanced/async-tests/ | 0.604 |
| crawlee | #1 | fastapi.tiangolo.com/advanced/async-tests/ | 0.727 | fastapi.tiangolo.com/tutorial/testing/ | 0.644 | fastapi.tiangolo.com/advanced/async-tests/ | 0.617 |
| colly+md | #1 | fastapi.tiangolo.com/advanced/async-tests/ | 0.750 | fastapi.tiangolo.com/tutorial/testing/ | 0.623 | fastapi.tiangolo.com/advanced/async-tests/ | 0.604 |
| playwright | #1 | fastapi.tiangolo.com/advanced/async-tests/ | 0.727 | fastapi.tiangolo.com/tutorial/testing/ | 0.644 | fastapi.tiangolo.com/advanced/async-tests/ | 0.617 |


**Q11: How do I use Jinja2 templates in FastAPI?** [code-example]
*(expects URL containing: `templating`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/reference/templating/ | 0.766 | fastapi.tiangolo.com/advanced/templates/ | 0.741 | fastapi.tiangolo.com/reference/templating/ | 0.685 |
| crawl4ai | #1 | fastapi.tiangolo.com/advanced/templates/ | 0.765 | fastapi.tiangolo.com/reference/templating/ | 0.761 | fastapi.tiangolo.com/reference/templating/ | 0.702 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/advanced/templates/ | 0.765 | fastapi.tiangolo.com/reference/templating/ | 0.761 | fastapi.tiangolo.com/reference/templating/ | 0.702 |
| scrapy+md | #1 | fastapi.tiangolo.com/reference/templating/ | 0.766 | fastapi.tiangolo.com/advanced/templates/ | 0.741 | fastapi.tiangolo.com/reference/templating/ | 0.685 |
| crawlee | #1 | fastapi.tiangolo.com/advanced/templates/ | 0.752 | fastapi.tiangolo.com/reference/templating/ | 0.742 | fastapi.tiangolo.com/reference/templating/ | 0.692 |
| colly+md | #1 | fastapi.tiangolo.com/reference/templating/ | 0.766 | fastapi.tiangolo.com/advanced/templates/ | 0.741 | fastapi.tiangolo.com/reference/templating/ | 0.685 |
| playwright | #1 | fastapi.tiangolo.com/advanced/templates/ | 0.752 | fastapi.tiangolo.com/reference/templating/ | 0.742 | fastapi.tiangolo.com/reference/templating/ | 0.692 |


**Q12: How do I use dependency injection in FastAPI?** [conceptual]
*(expects URL containing: `dependencies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.755 | fastapi.tiangolo.com/features/ | 0.706 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.635 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.780 | fastapi.tiangolo.com/features/ | 0.719 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.672 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.780 | fastapi.tiangolo.com/features/ | 0.719 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.672 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.755 | fastapi.tiangolo.com/features/ | 0.706 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.635 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.767 | fastapi.tiangolo.com/features/ | 0.706 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.652 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.755 | fastapi.tiangolo.com/features/ | 0.706 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.635 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.767 | fastapi.tiangolo.com/features/ | 0.706 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.652 |


**Q13: How do I return custom response classes in FastAPI?** [api-function]
*(expects URL containing: `custom-response`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | fastapi.tiangolo.com/reference/responses/ | 0.726 | fastapi.tiangolo.com/advanced/custom-response/ | 0.676 | fastapi.tiangolo.com/reference/responses/ | 0.675 |
| crawl4ai | #3 | fastapi.tiangolo.com/reference/responses/ | 0.731 | fastapi.tiangolo.com/reference/responses/ | 0.691 | fastapi.tiangolo.com/advanced/custom-response/ | 0.688 |
| crawl4ai-raw | #3 | fastapi.tiangolo.com/reference/responses/ | 0.731 | fastapi.tiangolo.com/reference/responses/ | 0.691 | fastapi.tiangolo.com/advanced/custom-response/ | 0.688 |
| scrapy+md | #2 | fastapi.tiangolo.com/reference/responses/ | 0.726 | fastapi.tiangolo.com/advanced/custom-response/ | 0.676 | fastapi.tiangolo.com/reference/responses/ | 0.675 |
| crawlee | #2 | fastapi.tiangolo.com/reference/responses/ | 0.715 | fastapi.tiangolo.com/advanced/custom-response/ | 0.674 | fastapi.tiangolo.com/reference/responses/ | 0.673 |
| colly+md | #2 | fastapi.tiangolo.com/reference/responses/ | 0.726 | fastapi.tiangolo.com/advanced/custom-response/ | 0.676 | fastapi.tiangolo.com/reference/responses/ | 0.675 |
| playwright | #2 | fastapi.tiangolo.com/reference/responses/ | 0.715 | fastapi.tiangolo.com/advanced/custom-response/ | 0.674 | fastapi.tiangolo.com/reference/responses/ | 0.673 |


**Q14: How do I configure CORS in FastAPI?** [api-function]
*(expects URL containing: `cors`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.628 | fastapi.tiangolo.com/tutorial/cors/ | 0.617 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.570 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.664 | fastapi.tiangolo.com/tutorial/cors/ | 0.639 | fastapi.tiangolo.com/tutorial/cors/ | 0.626 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.664 | fastapi.tiangolo.com/tutorial/cors/ | 0.639 | fastapi.tiangolo.com/tutorial/cors/ | 0.626 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.628 | fastapi.tiangolo.com/tutorial/cors/ | 0.570 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.570 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.620 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.570 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.570 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.628 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.570 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.570 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.620 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.570 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.570 |


**Q15: How do I use path parameters in FastAPI?** [api-function]
*(expects URL containing: `path-params`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.676 | fastapi.tiangolo.com/tutorial/query-params/ | 0.637 | fastapi.tiangolo.com/tutorial/path-params/ | 0.629 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.658 | fastapi.tiangolo.com/tutorial/path-params/ | 0.656 | fastapi.tiangolo.com/tutorial/path-params/ | 0.640 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.658 | fastapi.tiangolo.com/tutorial/path-params/ | 0.656 | fastapi.tiangolo.com/tutorial/path-params/ | 0.640 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.676 | fastapi.tiangolo.com/tutorial/query-params/ | 0.637 | fastapi.tiangolo.com/tutorial/path-params/ | 0.629 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.669 | fastapi.tiangolo.com/tutorial/path-params/ | 0.636 | fastapi.tiangolo.com/tutorial/query-params/ | 0.634 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.676 | fastapi.tiangolo.com/tutorial/query-params/ | 0.637 | fastapi.tiangolo.com/tutorial/path-params/ | 0.629 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.669 | fastapi.tiangolo.com/tutorial/path-params/ | 0.636 | fastapi.tiangolo.com/tutorial/query-params/ | 0.634 |


**Q16: How do I run FastAPI with Docker?** [conceptual]
*(expects URL containing: `docker`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.696 | fastapi.tiangolo.com/deployment/docker/ | 0.655 | fastapi.tiangolo.com/deployment/docker/ | 0.633 |
| crawl4ai | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.731 | fastapi.tiangolo.com/deployment/docker/ | 0.685 | fastapi.tiangolo.com/deployment/docker/ | 0.670 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.731 | fastapi.tiangolo.com/deployment/docker/ | 0.685 | fastapi.tiangolo.com/deployment/docker/ | 0.670 |
| scrapy+md | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.696 | fastapi.tiangolo.com/deployment/docker/ | 0.655 | fastapi.tiangolo.com/deployment/docker/ | 0.633 |
| crawlee | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.697 | fastapi.tiangolo.com/deployment/docker/ | 0.678 | fastapi.tiangolo.com/deployment/docker/ | 0.662 |
| colly+md | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.696 | fastapi.tiangolo.com/deployment/docker/ | 0.655 | fastapi.tiangolo.com/deployment/docker/ | 0.633 |
| playwright | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.697 | fastapi.tiangolo.com/deployment/docker/ | 0.670 | fastapi.tiangolo.com/deployment/docker/ | 0.662 |


**Q17: How do I configure FastAPI application settings?** [code-example]
*(expects URL containing: `settings`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.692 | fastapi.tiangolo.com/how-to/conditional-openapi/ | 0.586 | fastapi.tiangolo.com/how-to/configure-swagger-ui/ | 0.584 |
| crawl4ai | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.696 | fastapi.tiangolo.com/how-to/conditional-openapi/ | 0.613 | fastapi.tiangolo.com/advanced/settings/ | 0.602 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.696 | fastapi.tiangolo.com/how-to/conditional-openapi/ | 0.613 | fastapi.tiangolo.com/advanced/settings/ | 0.602 |
| scrapy+md | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.692 | fastapi.tiangolo.com/how-to/conditional-openapi/ | 0.584 | fastapi.tiangolo.com/how-to/configure-swagger-ui/ | 0.584 |
| crawlee | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.696 | fastapi.tiangolo.com/advanced/settings/ | 0.589 | fastapi.tiangolo.com/advanced/settings/ | 0.585 |
| colly+md | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.692 | fastapi.tiangolo.com/how-to/conditional-openapi/ | 0.586 | fastapi.tiangolo.com/how-to/configure-swagger-ui/ | 0.584 |
| playwright | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.696 | fastapi.tiangolo.com/advanced/settings/ | 0.589 | fastapi.tiangolo.com/advanced/settings/ | 0.585 |


**Q18: How do I use background tasks in FastAPI?** [api-function]
*(expects URL containing: `background-tasks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.692 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.683 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.675 |
| crawl4ai | #3 | fastapi.tiangolo.com/reference/background/ | 0.768 | fastapi.tiangolo.com/reference/background/ | 0.740 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.736 |
| crawl4ai-raw | #3 | fastapi.tiangolo.com/reference/background/ | 0.768 | fastapi.tiangolo.com/reference/background/ | 0.740 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.736 |
| scrapy+md | #3 | fastapi.tiangolo.com/reference/background/ | 0.731 | fastapi.tiangolo.com/reference/background/ | 0.713 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.692 |
| crawlee | #3 | fastapi.tiangolo.com/reference/background/ | 0.736 | fastapi.tiangolo.com/reference/background/ | 0.697 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.693 |
| colly+md | #3 | fastapi.tiangolo.com/reference/background/ | 0.731 | fastapi.tiangolo.com/reference/background/ | 0.713 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.692 |
| playwright | #3 | fastapi.tiangolo.com/reference/background/ | 0.736 | fastapi.tiangolo.com/reference/background/ | 0.697 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.693 |


**Q19: What are the first steps to create a FastAPI application?** [conceptual]
*(expects URL containing: `first-steps`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/reference/fastapi/ | 0.659 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.657 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.688 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.679 | fastapi.tiangolo.com/tutorial/ | 0.668 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.688 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.679 | fastapi.tiangolo.com/tutorial/ | 0.668 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/tutorial/body/ | 0.661 | fastapi.tiangolo.com/tutorial/request-files/ | 0.661 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.685 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/tutorial/sql-databases/ | 0.667 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/tutorial/sql-databases/ | 0.661 | fastapi.tiangolo.com/reference/fastapi/ | 0.658 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.685 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/tutorial/sql-databases/ | 0.667 |


**Q20: How do I handle errors and exceptions in FastAPI?** [api-function]
*(expects URL containing: `handling-errors`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | fastapi.tiangolo.com/reference/fastapi/ | 0.615 | fastapi.tiangolo.com/deployment/concepts/ | 0.612 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.606 |
| crawl4ai | #2 | fastapi.tiangolo.com/deployment/concepts/ | 0.632 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.628 | fastapi.tiangolo.com/reference/exceptions/ | 0.627 |
| crawl4ai-raw | #2 | fastapi.tiangolo.com/deployment/concepts/ | 0.632 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.628 | fastapi.tiangolo.com/reference/exceptions/ | 0.627 |
| scrapy+md | #3 | fastapi.tiangolo.com/deployment/concepts/ | 0.612 | fastapi.tiangolo.com/reference/fastapi/ | 0.608 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.606 |
| crawlee | #2 | fastapi.tiangolo.com/deployment/concepts/ | 0.618 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.599 | fastapi.tiangolo.com/reference/fastapi/ | 0.597 |
| colly+md | #3 | fastapi.tiangolo.com/deployment/concepts/ | 0.612 | fastapi.tiangolo.com/reference/fastapi/ | 0.608 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.606 |
| playwright | #2 | fastapi.tiangolo.com/deployment/concepts/ | 0.618 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.599 | fastapi.tiangolo.com/reference/fastapi/ | 0.597 |


</details>

## python-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 63% (12/19) | 84% (16/19) | 89% (17/19) | 100% (19/19) | 100% (19/19) | 0.744 | 9479 | 500 |
| crawl4ai | 63% (12/19) | 79% (15/19) | 95% (18/19) | 100% (19/19) | 100% (19/19) | 0.734 | 13248 | 500 |
| crawl4ai-raw | 63% (12/19) | 79% (15/19) | 95% (18/19) | 100% (19/19) | 100% (19/19) | 0.734 | 13248 | 500 |
| scrapy+md | 58% (11/19) | 84% (16/19) | 100% (19/19) | 100% (19/19) | 100% (19/19) | 0.730 | 10421 | 328 |
| crawlee | 63% (12/19) | 79% (15/19) | 95% (18/19) | 100% (19/19) | 100% (19/19) | 0.745 | 13304 | 500 |
| colly+md | 63% (12/19) | 79% (15/19) | 95% (18/19) | 100% (19/19) | 100% (19/19) | 0.745 | 13221 | 500 |
| playwright | 63% (12/19) | 79% (15/19) | 95% (18/19) | 100% (19/19) | 100% (19/19) | 0.745 | 13304 | 500 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for python-docs</summary>

**Q1: What new features were added in Python 3.10?** [factual-lookup]
*(expects URL containing: `whatsnew/3.10`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/whatsnew/3.10.html | 0.757 | docs.python.org/3.11/contents.html | 0.652 | docs.python.org/3.12/contents.html | 0.651 |
| crawl4ai | #1 | docs.python.org/3.10/whatsnew/3.10.html | 0.749 | docs.python.org/3.10/whatsnew/index.html | 0.704 | docs.python.org/3.10/whatsnew/index.html | 0.704 |
| crawl4ai-raw | #1 | docs.python.org/3.10/whatsnew/3.10.html | 0.749 | docs.python.org/3.10/whatsnew/index.html | 0.704 | docs.python.org/3.10/whatsnew/index.html | 0.704 |
| scrapy+md | #1 | docs.python.org/3.10/whatsnew/3.10.html | 0.759 | docs.python.org/3.10/whatsnew/3.10.html | 0.692 | docs.python.org/3.10/whatsnew/3.10.html | 0.692 |
| crawlee | #1 | docs.python.org/3.10/whatsnew/3.10.html | 0.759 | docs.python.org/3.10/whatsnew/3.10.html | 0.692 | docs.python.org/3.10/whatsnew/3.10.html | 0.692 |
| colly+md | #1 | docs.python.org/3.10/whatsnew/3.10.html | 0.759 | docs.python.org/3.10/whatsnew/3.10.html | 0.692 | docs.python.org/3.10/whatsnew/3.10.html | 0.692 |
| playwright | #1 | docs.python.org/3.10/whatsnew/3.10.html | 0.759 | docs.python.org/3.10/whatsnew/3.10.html | 0.692 | docs.python.org/3.10/whatsnew/3.10.html | 0.692 |


**Q2: What does the term 'decorator' mean in Python?** [factual-lookup]
*(expects URL containing: `glossary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.1/glossary.html | 0.612 | docs.python.org/3.10/whatsnew/2.4.html | 0.608 | docs.python.org/3.0/glossary.html | 0.602 |
| crawl4ai | #1 | docs.python.org/3.0/glossary.html | 0.650 | docs.python.org/3.1/glossary.html | 0.643 | docs.python.org/3.10/whatsnew/2.4.html | 0.592 |
| crawl4ai-raw | #1 | docs.python.org/3.0/glossary.html | 0.650 | docs.python.org/3.1/glossary.html | 0.643 | docs.python.org/3.10/whatsnew/2.4.html | 0.592 |
| scrapy+md | #3 | docs.python.org/3.10/whatsnew/2.4.html | 0.608 | docs.python.org/3.10/whatsnew/2.4.html | 0.565 | docs.python.org/3.10/glossary.html | 0.565 |
| crawlee | #1 | docs.python.org/3.1/glossary.html | 0.611 | docs.python.org/3.10/whatsnew/2.4.html | 0.610 | docs.python.org/3.0/glossary.html | 0.603 |
| colly+md | #1 | docs.python.org/3.1/glossary.html | 0.611 | docs.python.org/3.10/whatsnew/2.4.html | 0.608 | docs.python.org/3.0/glossary.html | 0.603 |
| playwright | #1 | docs.python.org/3.1/glossary.html | 0.611 | docs.python.org/3.10/whatsnew/2.4.html | 0.610 | docs.python.org/3.0/glossary.html | 0.603 |


**Q3: How do I report a bug in Python?** [factual-lookup]
*(expects URL containing: `bugs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.0/bugs.html | 0.713 | docs.python.org/3.1/bugs.html | 0.673 | docs.python.org/2.7/bugs.html | 0.643 |
| crawl4ai | #1 | docs.python.org/3.0/bugs.html | 0.743 | docs.python.org/3.1/bugs.html | 0.705 | docs.python.org/3.0/about.html | 0.693 |
| crawl4ai-raw | #1 | docs.python.org/3.0/bugs.html | 0.743 | docs.python.org/3.1/bugs.html | 0.705 | docs.python.org/3.0/about.html | 0.693 |
| scrapy+md | #1 | docs.python.org/3.12/bugs.html | 0.609 | docs.python.org/3.15/bugs.html | 0.609 | docs.python.org/3/bugs.html | 0.609 |
| crawlee | #1 | docs.python.org/3.0/bugs.html | 0.713 | docs.python.org/3.1/bugs.html | 0.673 | docs.python.org/2.7/bugs.html | 0.672 |
| colly+md | #1 | docs.python.org/3.0/bugs.html | 0.713 | docs.python.org/3.1/bugs.html | 0.673 | docs.python.org/2.7/bugs.html | 0.672 |
| playwright | #1 | docs.python.org/3.0/bugs.html | 0.713 | docs.python.org/3.1/bugs.html | 0.673 | docs.python.org/2.7/bugs.html | 0.672 |


**Q4: What is Python's glossary definition of a generator?** [factual-lookup]
*(expects URL containing: `glossary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.0/glossary.html | 0.630 | docs.python.org/3.6/glossary.html | 0.615 | docs.python.org/3.10/glossary.html | 0.584 |
| crawl4ai | #1 | docs.python.org/3.13/glossary.html | 0.657 | docs.python.org/3.10/glossary.html | 0.634 | docs.python.org/3.5/glossary.html | 0.608 |
| crawl4ai-raw | #1 | docs.python.org/3.13/glossary.html | 0.657 | docs.python.org/3.10/glossary.html | 0.634 | docs.python.org/3.5/glossary.html | 0.608 |
| scrapy+md | #1 | docs.python.org/3.13/glossary.html | 0.585 | docs.python.org/3.13/glossary.html | 0.581 | docs.python.org/3.11/glossary.html | 0.580 |
| crawlee | #1 | docs.python.org/3.0/glossary.html | 0.632 | docs.python.org/3.6/glossary.html | 0.614 | docs.python.org/3.14/glossary.html | 0.612 |
| colly+md | #1 | docs.python.org/3.0/glossary.html | 0.632 | docs.python.org/3.6/glossary.html | 0.615 | docs.python.org/3.13/glossary.html | 0.585 |
| playwright | #1 | docs.python.org/3.0/glossary.html | 0.631 | docs.python.org/3.6/glossary.html | 0.614 | docs.python.org/3.14/glossary.html | 0.612 |


**Q5: What is the Python module index?** [navigation]
*(expects URL containing: `py-modindex`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/py-modindex.html | 0.852 | docs.python.org/3.3/py-modindex.html | 0.852 | docs.python.org/3.5/py-modindex.html | 0.852 |
| crawl4ai | #1 | docs.python.org/3.1/modindex.html | 0.648 | docs.python.org/3.3/py-modindex.html | 0.647 | docs.python.org/3.4/py-modindex.html | 0.646 |
| crawl4ai-raw | #1 | docs.python.org/3.1/modindex.html | 0.648 | docs.python.org/3.3/py-modindex.html | 0.647 | docs.python.org/3.4/py-modindex.html | 0.646 |
| scrapy+md | #1 | docs.python.org/3.12/py-modindex.html | 0.776 | docs.python.org/3.14/py-modindex.html | 0.776 | docs.python.org/3.13/py-modindex.html | 0.776 |
| crawlee | #1 | docs.python.org/3.5/py-modindex.html | 0.776 | docs.python.org/3.7/py-modindex.html | 0.776 | docs.python.org/3.6/py-modindex.html | 0.776 |
| colly+md | #1 | docs.python.org/3.11/py-modindex.html | 0.776 | docs.python.org/3.15/py-modindex.html | 0.776 | docs.python.org/3.12/py-modindex.html | 0.776 |
| playwright | #1 | docs.python.org/3.5/py-modindex.html | 0.776 | docs.python.org/3.13/py-modindex.html | 0.776 | docs.python.org/3.12/py-modindex.html | 0.776 |


**Q6: What does the term 'iterable' mean in Python?** [factual-lookup]
*(expects URL containing: `glossary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.13/glossary.html | 0.648 | docs.python.org/3.3/glossary.html | 0.608 | docs.python.org/3.10/whatsnew/2.2.html | 0.561 |
| crawl4ai | #1 | docs.python.org/3.0/glossary.html | 0.605 | docs.python.org/3.11/glossary.html | 0.597 | docs.python.org/3.5/glossary.html | 0.596 |
| crawl4ai-raw | #1 | docs.python.org/3.0/glossary.html | 0.605 | docs.python.org/3.11/glossary.html | 0.597 | docs.python.org/3.5/glossary.html | 0.595 |
| scrapy+md | #1 | docs.python.org/3.13/glossary.html | 0.648 | docs.python.org/3.10/whatsnew/2.2.html | 0.561 | docs.python.org/3.10/library/itertools.html | 0.558 |
| crawlee | #1 | docs.python.org/3.13/glossary.html | 0.648 | docs.python.org/3.3/glossary.html | 0.606 | docs.python.org/3.6/glossary.html | 0.558 |
| colly+md | #1 | docs.python.org/3.13/glossary.html | 0.648 | docs.python.org/3.3/glossary.html | 0.606 | docs.python.org/3.10/whatsnew/2.2.html | 0.561 |
| playwright | #1 | docs.python.org/3.13/glossary.html | 0.648 | docs.python.org/3.3/glossary.html | 0.606 | docs.python.org/3.6/glossary.html | 0.558 |


**Q7: How do I install and configure Python on my system?** [conceptual]
*(expects URL containing: `using`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #10 | docs.python.org/3.13/installing/index.html | 0.582 | docs.python.org/3.11/installing/index.html | 0.578 | docs.python.org/3.12/installing/index.html | 0.578 |
| crawl4ai | #1 | docs.python.org/3.10/using/unix.html | 0.604 | docs.python.org/3.13/installing/index.html | 0.591 | docs.python.org/3.11/installing/index.html | 0.588 |
| crawl4ai-raw | #1 | docs.python.org/3.10/using/unix.html | 0.605 | docs.python.org/3.13/installing/index.html | 0.591 | docs.python.org/3.11/installing/index.html | 0.588 |
| scrapy+md | #4 | docs.python.org/3.13/installing/index.html | 0.582 | docs.python.org/3.12/installing/index.html | 0.578 | docs.python.org/3.11/installing/index.html | 0.578 |
| crawlee | #4 | docs.python.org/3.13/installing/index.html | 0.582 | docs.python.org/3.12/installing/index.html | 0.578 | docs.python.org/3.11/installing/index.html | 0.578 |
| colly+md | #4 | docs.python.org/3.13/installing/index.html | 0.582 | docs.python.org/3.12/installing/index.html | 0.578 | docs.python.org/3.11/installing/index.html | 0.578 |
| playwright | #4 | docs.python.org/3.13/installing/index.html | 0.582 | docs.python.org/3.12/installing/index.html | 0.578 | docs.python.org/3.11/installing/index.html | 0.578 |


**Q8: How do I use the os module for file and directory operations?** [api-function]
*(expects URL containing: `library/os`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/os.html | 0.555 | docs.python.org/3.3/whatsnew/3.3.html | 0.548 | docs.python.org/3.10/whatsnew/3.3.html | 0.535 |
| crawl4ai | #1 | docs.python.org/3.10/library/os.html | 0.580 | docs.python.org/3.10/library/os.html | 0.552 | docs.python.org/3.10/library/os.html | 0.532 |
| crawl4ai-raw | #1 | docs.python.org/3.10/library/os.html | 0.580 | docs.python.org/3.10/library/os.html | 0.552 | docs.python.org/3.10/library/os.html | 0.532 |
| scrapy+md | #1 | docs.python.org/3.10/library/os.html | 0.555 | docs.python.org/3.10/whatsnew/3.3.html | 0.535 | docs.python.org/3.12/whatsnew/3.12.html | 0.514 |
| crawlee | #1 | docs.python.org/3.10/library/os.html | 0.555 | docs.python.org/3.3/whatsnew/3.3.html | 0.550 | docs.python.org/3.10/whatsnew/3.3.html | 0.535 |
| colly+md | #1 | docs.python.org/3.10/library/os.html | 0.555 | docs.python.org/3.3/whatsnew/3.3.html | 0.550 | docs.python.org/3.10/whatsnew/3.3.html | 0.535 |
| playwright | #1 | docs.python.org/3.10/library/os.html | 0.555 | docs.python.org/3.3/whatsnew/3.3.html | 0.550 | docs.python.org/3.10/whatsnew/3.3.html | 0.535 |


**Q9: How do I use pathlib for filesystem paths in Python?** [api-function]
*(expects URL containing: `library/pathlib`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | docs.python.org/3.4/whatsnew/3.4.html | 0.634 | docs.python.org/3.10/whatsnew/3.4.html | 0.625 | docs.python.org/3.10/whatsnew/3.6.html | 0.546 |
| crawl4ai | #5 | docs.python.org/3.4/whatsnew/3.4.html | 0.621 | docs.python.org/3.10/whatsnew/3.4.html | 0.619 | docs.python.org/3.10/whatsnew/3.6.html | 0.577 |
| crawl4ai-raw | #5 | docs.python.org/3.4/whatsnew/3.4.html | 0.621 | docs.python.org/3.10/whatsnew/3.4.html | 0.619 | docs.python.org/3.10/whatsnew/3.6.html | 0.577 |
| scrapy+md | #3 | docs.python.org/3.10/whatsnew/3.4.html | 0.625 | docs.python.org/3.10/whatsnew/3.6.html | 0.546 | docs.python.org/3.10/library/pathlib.html | 0.510 |
| crawlee | #5 | docs.python.org/3.4/whatsnew/3.4.html | 0.634 | docs.python.org/3.10/whatsnew/3.4.html | 0.625 | docs.python.org/3.10/whatsnew/3.6.html | 0.546 |
| colly+md | #5 | docs.python.org/3.4/whatsnew/3.4.html | 0.634 | docs.python.org/3.10/whatsnew/3.4.html | 0.625 | docs.python.org/3.10/whatsnew/3.6.html | 0.546 |
| playwright | #5 | docs.python.org/3.4/whatsnew/3.4.html | 0.634 | docs.python.org/3.10/whatsnew/3.4.html | 0.625 | docs.python.org/3.10/whatsnew/3.6.html | 0.546 |


**Q10: How do I parse and generate JSON in Python?** [api-function]
*(expects URL containing: `library/json`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.python.org/3.10/whatsnew/2.6.html | 0.495 | docs.python.org/3.10/library/json.html | 0.462 | docs.python.org/3.10/library/json.html | 0.413 |
| crawl4ai | #2 | docs.python.org/3.10/whatsnew/2.6.html | 0.508 | docs.python.org/3.10/library/json.html | 0.454 | docs.python.org/3.10/library/json.html | 0.453 |
| crawl4ai-raw | #2 | docs.python.org/3.10/whatsnew/2.6.html | 0.508 | docs.python.org/3.10/library/json.html | 0.454 | docs.python.org/3.10/library/json.html | 0.453 |
| scrapy+md | #2 | docs.python.org/3.10/whatsnew/2.6.html | 0.495 | docs.python.org/3.10/library/json.html | 0.458 | docs.python.org/3.10/library/json.html | 0.413 |
| crawlee | #2 | docs.python.org/3.10/whatsnew/2.6.html | 0.492 | docs.python.org/3.10/library/json.html | 0.438 | docs.python.org/3.10/library/json.html | 0.429 |
| colly+md | #2 | docs.python.org/3.10/whatsnew/2.6.html | 0.495 | docs.python.org/3.10/library/json.html | 0.458 | docs.python.org/3.10/library/json.html | 0.417 |
| playwright | #2 | docs.python.org/3.10/whatsnew/2.6.html | 0.492 | docs.python.org/3.10/library/json.html | 0.438 | docs.python.org/3.10/library/json.html | 0.429 |


**Q11: How do I use asyncio for async programming in Python?** [api-function]
*(expects URL containing: `library/asyncio`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.python.org/3.4/whatsnew/3.4.html | 0.555 | docs.python.org/3.10/whatsnew/3.4.html | 0.550 | docs.python.org/3.10/library/asyncio-task.html | 0.548 |
| crawl4ai | #3 | docs.python.org/3.10/library/socket.html | 0.597 | docs.python.org/3.10/library/socket.html | 0.597 | docs.python.org/3.10/library/asyncio-task.html | 0.569 |
| crawl4ai-raw | #3 | docs.python.org/3.10/library/socket.html | 0.597 | docs.python.org/3.10/library/socket.html | 0.597 | docs.python.org/3.10/library/asyncio-task.html | 0.569 |
| scrapy+md | #4 | docs.python.org/3.10/library/socket.html | 0.572 | docs.python.org/3.10/library/socket.html | 0.572 | docs.python.org/3.10/whatsnew/3.4.html | 0.550 |
| crawlee | #5 | docs.python.org/3.10/library/socket.html | 0.572 | docs.python.org/3.10/library/socket.html | 0.572 | docs.python.org/3.4/whatsnew/3.4.html | 0.555 |
| colly+md | #5 | docs.python.org/3.10/library/socket.html | 0.572 | docs.python.org/3.10/library/socket.html | 0.572 | docs.python.org/3.4/whatsnew/3.4.html | 0.555 |
| playwright | #5 | docs.python.org/3.10/library/socket.html | 0.572 | docs.python.org/3.10/library/socket.html | 0.572 | docs.python.org/3.4/whatsnew/3.4.html | 0.555 |


**Q12: How do I use type hints and the typing module in Python?** [api-function]
*(expects URL containing: `library/typing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | docs.python.org/3.12/whatsnew/3.12.html | 0.663 | docs.python.org/3.10/whatsnew/3.5.html | 0.662 | docs.python.org/3.5/whatsnew/3.5.html | 0.661 |
| crawl4ai | #8 | docs.python.org/3.10/whatsnew/3.5.html | 0.697 | docs.python.org/3.5/whatsnew/3.5.html | 0.691 | docs.python.org/3.12/whatsnew/3.12.html | 0.674 |
| crawl4ai-raw | #8 | docs.python.org/3.10/whatsnew/3.5.html | 0.697 | docs.python.org/3.5/whatsnew/3.5.html | 0.691 | docs.python.org/3.12/whatsnew/3.12.html | 0.674 |
| scrapy+md | #5 | docs.python.org/3.12/whatsnew/3.12.html | 0.664 | docs.python.org/3.10/whatsnew/3.5.html | 0.663 | docs.python.org/3.10/whatsnew/3.10.html | 0.656 |
| crawlee | #6 | docs.python.org/3.12/whatsnew/3.12.html | 0.663 | docs.python.org/3.10/whatsnew/3.5.html | 0.662 | docs.python.org/3.5/whatsnew/3.5.html | 0.661 |
| colly+md | #6 | docs.python.org/3.12/whatsnew/3.12.html | 0.663 | docs.python.org/3.10/whatsnew/3.5.html | 0.662 | docs.python.org/3.5/whatsnew/3.5.html | 0.661 |
| playwright | #6 | docs.python.org/3.12/whatsnew/3.12.html | 0.663 | docs.python.org/3.10/whatsnew/3.5.html | 0.662 | docs.python.org/3.5/whatsnew/3.5.html | 0.661 |


**Q13: How do I work with dates and times using the datetime module?** [api-function]
*(expects URL containing: `library/datetime`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/datetime.html | 0.591 | docs.python.org/3.10/whatsnew/2.3.html | 0.540 | docs.python.org/3.10/library/datetime.html | 0.539 |
| crawl4ai | #1 | docs.python.org/3.10/library/datetime.html | 0.594 | docs.python.org/3.10/whatsnew/2.3.html | 0.551 | docs.python.org/3.10/library/datetime.html | 0.522 |
| crawl4ai-raw | #1 | docs.python.org/3.10/library/datetime.html | 0.594 | docs.python.org/3.10/whatsnew/2.3.html | 0.551 | docs.python.org/3.10/library/datetime.html | 0.522 |
| scrapy+md | #1 | docs.python.org/3.10/library/datetime.html | 0.591 | docs.python.org/3.10/whatsnew/2.3.html | 0.540 | docs.python.org/3.10/library/datetime.html | 0.539 |
| crawlee | #1 | docs.python.org/3.10/library/datetime.html | 0.591 | docs.python.org/3.10/whatsnew/2.3.html | 0.540 | docs.python.org/3.10/library/datetime.html | 0.536 |
| colly+md | #1 | docs.python.org/3.10/library/datetime.html | 0.591 | docs.python.org/3.10/whatsnew/2.3.html | 0.540 | docs.python.org/3.10/library/datetime.html | 0.539 |
| playwright | #1 | docs.python.org/3.10/library/datetime.html | 0.591 | docs.python.org/3.10/whatsnew/2.3.html | 0.540 | docs.python.org/3.10/library/datetime.html | 0.536 |


**Q14: How do I use Python's logging module?** [api-function]
*(expects URL containing: `library/logging`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/logging.html | 0.550 | docs.python.org/2.7/whatsnew/2.7.html | 0.506 | docs.python.org/3.10/whatsnew/2.7.html | 0.506 |
| crawl4ai | #1 | docs.python.org/3.10/library/logging.html | 0.600 | docs.python.org/3.10/library/logging.html | 0.535 | docs.python.org/3.10/whatsnew/2.4.html | 0.533 |
| crawl4ai-raw | #1 | docs.python.org/3.10/library/logging.html | 0.600 | docs.python.org/3.10/library/logging.html | 0.535 | docs.python.org/3.10/whatsnew/2.4.html | 0.533 |
| scrapy+md | #1 | docs.python.org/3.10/library/logging.html | 0.558 | docs.python.org/3.10/whatsnew/2.7.html | 0.506 | docs.python.org/3.10/library/logging.config.html | 0.501 |
| crawlee | #1 | docs.python.org/3.10/library/logging.html | 0.557 | docs.python.org/2.7/whatsnew/2.7.html | 0.506 | docs.python.org/3.10/whatsnew/2.7.html | 0.506 |
| colly+md | #1 | docs.python.org/3.10/library/logging.html | 0.558 | docs.python.org/2.7/whatsnew/2.7.html | 0.506 | docs.python.org/3.10/whatsnew/2.7.html | 0.506 |
| playwright | #1 | docs.python.org/3.10/library/logging.html | 0.558 | docs.python.org/2.7/whatsnew/2.7.html | 0.506 | docs.python.org/3.10/whatsnew/2.7.html | 0.506 |


**Q15: How do I write unit tests with the unittest module?** [code-example]
*(expects URL containing: `library/unittest`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/unittest.html | 0.542 | docs.python.org/3.10/library/unittest.html | 0.523 | docs.python.org/3.10/library/unittest.html | 0.520 |
| crawl4ai | #3 | docs.python.org/3.10/whatsnew/3.4.html | 0.544 | docs.python.org/3.4/whatsnew/3.4.html | 0.541 | docs.python.org/3.10/library/unittest.html | 0.539 |
| crawl4ai-raw | #3 | docs.python.org/3.10/whatsnew/3.4.html | 0.544 | docs.python.org/3.4/whatsnew/3.4.html | 0.541 | docs.python.org/3.10/library/unittest.html | 0.539 |
| scrapy+md | #1 | docs.python.org/3.10/library/unittest.html | 0.543 | docs.python.org/3.10/library/unittest.html | 0.523 | docs.python.org/3.10/library/unittest.html | 0.520 |
| crawlee | #1 | docs.python.org/3.10/library/unittest.html | 0.543 | docs.python.org/3.10/library/unittest.html | 0.523 | docs.python.org/3.10/library/unittest.html | 0.520 |
| colly+md | #1 | docs.python.org/3.10/library/unittest.html | 0.543 | docs.python.org/3.10/library/unittest.html | 0.523 | docs.python.org/3.10/library/unittest.html | 0.520 |
| playwright | #1 | docs.python.org/3.10/library/unittest.html | 0.543 | docs.python.org/3.10/library/unittest.html | 0.523 | docs.python.org/3.10/library/unittest.html | 0.520 |


**Q16: How do I use Python dataclasses?** [api-function]
*(expects URL containing: `library/dataclasses`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.python.org/3.7/whatsnew/3.7.html | 0.624 | docs.python.org/3.10/whatsnew/3.7.html | 0.624 | docs.python.org/3.10/library/dataclasses.html | 0.600 |
| crawl4ai | #4 | docs.python.org/3.10/whatsnew/3.10.html | 0.679 | docs.python.org/3.10/whatsnew/3.7.html | 0.669 | docs.python.org/3.7/whatsnew/3.7.html | 0.668 |
| crawl4ai-raw | #4 | docs.python.org/3.10/whatsnew/3.10.html | 0.679 | docs.python.org/3.10/whatsnew/3.7.html | 0.669 | docs.python.org/3.7/whatsnew/3.7.html | 0.668 |
| scrapy+md | #2 | docs.python.org/3.10/whatsnew/3.7.html | 0.624 | docs.python.org/3.10/library/dataclasses.html | 0.599 | docs.python.org/3.10/whatsnew/3.10.html | 0.544 |
| crawlee | #3 | docs.python.org/3.10/whatsnew/3.7.html | 0.624 | docs.python.org/3.7/whatsnew/3.7.html | 0.624 | docs.python.org/3.10/library/dataclasses.html | 0.611 |
| colly+md | #3 | docs.python.org/3.10/whatsnew/3.7.html | 0.624 | docs.python.org/3.7/whatsnew/3.7.html | 0.624 | docs.python.org/3.10/library/dataclasses.html | 0.599 |
| playwright | #3 | docs.python.org/3.7/whatsnew/3.7.html | 0.624 | docs.python.org/3.10/whatsnew/3.7.html | 0.624 | docs.python.org/3.10/library/dataclasses.html | 0.611 |


**Q17: How do I use itertools for efficient iteration in Python?** [api-function]
*(expects URL containing: `library/itertools`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.python.org/3.10/whatsnew/3.10.html | 0.592 | docs.python.org/3.10/library/itertools.html | 0.568 | docs.python.org/3.10/library/itertools.html | 0.538 |
| crawl4ai | #5 | docs.python.org/3.10/whatsnew/3.10.html | 0.639 | docs.python.org/3.12/whatsnew/3.12.html | 0.578 | docs.python.org/3.10/whatsnew/3.3.html | 0.566 |
| crawl4ai-raw | #5 | docs.python.org/3.10/whatsnew/3.10.html | 0.639 | docs.python.org/3.12/whatsnew/3.12.html | 0.578 | docs.python.org/3.10/whatsnew/3.3.html | 0.566 |
| scrapy+md | #2 | docs.python.org/3.10/whatsnew/3.10.html | 0.592 | docs.python.org/3.10/library/itertools.html | 0.568 | docs.python.org/3.12/whatsnew/3.12.html | 0.538 |
| crawlee | #2 | docs.python.org/3.10/whatsnew/3.10.html | 0.592 | docs.python.org/3.10/library/itertools.html | 0.568 | docs.python.org/3.12/whatsnew/3.12.html | 0.538 |
| colly+md | #2 | docs.python.org/3.10/whatsnew/3.10.html | 0.592 | docs.python.org/3.10/library/itertools.html | 0.568 | docs.python.org/3.12/whatsnew/3.12.html | 0.538 |
| playwright | #2 | docs.python.org/3.10/whatsnew/3.10.html | 0.592 | docs.python.org/3.10/library/itertools.html | 0.568 | docs.python.org/3.12/whatsnew/3.12.html | 0.538 |


**Q18: How does Python's data model work with special methods?** [conceptual]
*(expects URL containing: `reference/datamodel`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/reference/datamodel.html | 0.531 | docs.python.org/3.15/contents.html | 0.510 | docs.python.org/3.11/contents.html | 0.507 |
| crawl4ai | #1 | docs.python.org/3.10/reference/datamodel.html | 0.606 | docs.python.org/3.14/glossary.html | 0.554 | docs.python.org/3.10/reference/datamodel.html | 0.551 |
| crawl4ai-raw | #1 | docs.python.org/3.10/reference/datamodel.html | 0.607 | docs.python.org/3.14/glossary.html | 0.554 | docs.python.org/3.10/reference/datamodel.html | 0.551 |
| scrapy+md | #1 | docs.python.org/3.10/reference/datamodel.html | 0.531 | docs.python.org/3.15/contents.html | 0.507 | docs.python.org/3.11/contents.html | 0.500 |
| crawlee | #1 | docs.python.org/3.10/reference/datamodel.html | 0.531 | docs.python.org/3.15/contents.html | 0.507 | docs.python.org/3.11/contents.html | 0.500 |
| colly+md | #1 | docs.python.org/3.10/reference/datamodel.html | 0.531 | docs.python.org/3.15/contents.html | 0.507 | docs.python.org/3.11/contents.html | 0.500 |
| playwright | #1 | docs.python.org/3.10/reference/datamodel.html | 0.531 | docs.python.org/3.15/contents.html | 0.507 | docs.python.org/3.11/contents.html | 0.500 |


**Q19: What are Python's compound statements like if, for, and with?** [conceptual]
*(expects URL containing: `reference/compound_stmts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/reference/compound_stmts.html | 0.638 | docs.python.org/3.10/whatsnew/2.6.html | 0.568 | docs.python.org/3.10/whatsnew/2.5.html | 0.546 |
| crawl4ai | #1 | docs.python.org/3.10/reference/compound_stmts.html | 0.671 | docs.python.org/3.10/reference/compound_stmts.html | 0.635 | docs.python.org/3.10/reference/compound_stmts.html | 0.635 |
| crawl4ai-raw | #1 | docs.python.org/3.10/reference/compound_stmts.html | 0.671 | docs.python.org/3.10/reference/compound_stmts.html | 0.635 | docs.python.org/3.10/reference/compound_stmts.html | 0.635 |
| scrapy+md | #1 | docs.python.org/3.10/reference/compound_stmts.html | 0.638 | docs.python.org/3.10/whatsnew/2.6.html | 0.568 | docs.python.org/3.10/whatsnew/2.5.html | 0.546 |
| crawlee | #1 | docs.python.org/3.10/reference/compound_stmts.html | 0.638 | docs.python.org/3.10/whatsnew/2.6.html | 0.568 | docs.python.org/3.10/whatsnew/2.5.html | 0.546 |
| colly+md | #1 | docs.python.org/3.10/reference/compound_stmts.html | 0.638 | docs.python.org/3.10/whatsnew/2.6.html | 0.568 | docs.python.org/3.10/whatsnew/2.5.html | 0.546 |
| playwright | #1 | docs.python.org/3.10/reference/compound_stmts.html | 0.638 | docs.python.org/3.10/whatsnew/2.6.html | 0.568 | docs.python.org/3.10/whatsnew/2.5.html | 0.546 |


</details>

## react-dev

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 69% (11/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.804 | 3496 | 221 |
| crawl4ai | 81% (13/16) | 100% (16/16) | 100% (16/16) | 100% (16/16) | 100% (16/16) | 0.885 | 4756 | 221 |
| crawl4ai-raw | 75% (12/16) | 100% (16/16) | 100% (16/16) | 100% (16/16) | 100% (16/16) | 0.854 | 4756 | 221 |
| scrapy+md | 69% (11/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.804 | 3557 | 221 |
| crawlee | 69% (11/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.790 | 6444 | 221 |
| colly+md | 69% (11/16) | 81% (13/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.785 | 6355 | 221 |
| playwright | 69% (11/16) | 81% (13/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.785 | 6355 | 221 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for react-dev</summary>

**Q1: How do I manage state in a React component?** [conceptual]
*(expects URL containing: `state`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |
| crawl4ai | #1 | react.dev/learn/preserving-and-resetting-state | 0.712 | react.dev/learn/state-a-components-memory | 0.701 | react.dev/learn/managing-state | 0.701 |
| crawl4ai-raw | #1 | react.dev/learn/preserving-and-resetting-state | 0.712 | react.dev/learn/state-a-components-memory | 0.701 | react.dev/learn/managing-state | 0.701 |
| scrapy+md | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |
| crawlee | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |
| colly+md | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |
| playwright | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |


**Q2: How does the useEffect hook work in React?** [api-function]
*(expects URL containing: `useEffect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useEffect | 0.742 | react.dev/reference/react/useEffectEvent | 0.634 | react.dev/reference/react/useEffect | 0.625 |
| crawl4ai | #1 | react.dev/reference/react/useEffect | 0.716 | react.dev/reference/rules/components-and-hooks-mus | 0.644 | react.dev/reference/react/useEffectEvent | 0.631 |
| crawl4ai-raw | #1 | react.dev/reference/react/useEffect | 0.716 | react.dev/reference/rules/components-and-hooks-mus | 0.644 | react.dev/reference/react/useEffectEvent | 0.631 |
| scrapy+md | #1 | react.dev/reference/react/useEffect | 0.742 | react.dev/reference/react/useEffectEvent | 0.634 | react.dev/reference/react/useEffect | 0.625 |
| crawlee | #1 | react.dev/reference/react/useEffect | 0.742 | react.dev/reference/react/useEffectEvent | 0.634 | react.dev/reference/react/useEffect | 0.625 |
| colly+md | #1 | react.dev/reference/react/useEffect | 0.742 | react.dev/reference/react/useEffectEvent | 0.634 | react.dev/reference/react/useEffect | 0.625 |
| playwright | #1 | react.dev/reference/react/useEffect | 0.742 | react.dev/reference/react/useEffectEvent | 0.634 | react.dev/reference/react/useEffect | 0.625 |


**Q3: How do I create and use context in React?** [api-function]
*(expects URL containing: `useContext`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/createContext | 0.730 | react.dev/learn/passing-data-deeply-with-context | 0.705 | react.dev/learn/passing-data-deeply-with-context | 0.701 |
| crawl4ai | #1 | react.dev/reference/react/createContext | 0.744 | react.dev/learn/passing-data-deeply-with-context | 0.737 | react.dev/reference/react/createContext | 0.715 |
| crawl4ai-raw | #1 | react.dev/reference/react/createContext | 0.744 | react.dev/learn/passing-data-deeply-with-context | 0.732 | react.dev/reference/react/createContext | 0.715 |
| scrapy+md | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/learn/passing-data-deeply-with-context | 0.705 | react.dev/learn/passing-data-deeply-with-context | 0.701 |
| crawlee | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/learn/passing-data-deeply-with-context | 0.710 | react.dev/reference/react/createContext | 0.708 |
| colly+md | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/reference/react/createContext | 0.708 | react.dev/learn/passing-data-deeply-with-context | 0.705 |
| playwright | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/reference/react/createContext | 0.708 | react.dev/learn/passing-data-deeply-with-context | 0.705 |


**Q4: What is JSX and how does React use it?** [conceptual]
*(expects URL containing: `writing-markup-with-jsx`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.708 | react.dev/learn/writing-markup-with-jsx | 0.707 |
| crawl4ai | #1 | react.dev/learn/writing-markup-with-jsx | 0.732 | react.dev/learn/writing-markup-with-jsx | 0.680 | react.dev/learn/writing-markup-with-jsx | 0.668 |
| crawl4ai-raw | #1 | react.dev/learn/writing-markup-with-jsx | 0.732 | react.dev/learn/writing-markup-with-jsx | 0.680 | react.dev/learn/writing-markup-with-jsx | 0.668 |
| scrapy+md | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.707 |
| crawlee | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.707 |
| colly+md | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.707 |
| playwright | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.707 |


**Q5: How do I render lists and use keys in React?** [code-example]
*(expects URL containing: `rendering-lists`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.701 |
| crawl4ai | #1 | react.dev/learn/rendering-lists | 0.751 | react.dev/learn/describing-the-ui | 0.726 | react.dev/learn/describing-the-ui | 0.723 |
| crawl4ai-raw | #1 | react.dev/learn/rendering-lists | 0.751 | react.dev/learn/describing-the-ui | 0.726 | react.dev/learn/describing-the-ui | 0.723 |
| scrapy+md | #4 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.700 |
| crawlee | #5 | react.dev/learn/describing-the-ui | 0.723 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.698 |
| colly+md | #5 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.700 |
| playwright | #5 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.700 |


**Q6: How do I use the useRef hook in React?** [api-function]
*(expects URL containing: `useRef`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useRef | 0.755 | react.dev/learn/referencing-values-with-refs | 0.719 | react.dev/reference/react/useRef | 0.675 |
| crawl4ai | #1 | react.dev/reference/react/useRef | 0.732 | react.dev/learn/referencing-values-with-refs | 0.721 | react.dev/reference/react/useRef | 0.704 |
| crawl4ai-raw | #1 | react.dev/reference/react/useRef | 0.732 | react.dev/learn/referencing-values-with-refs | 0.721 | react.dev/reference/react/useRef | 0.704 |
| scrapy+md | #1 | react.dev/reference/react/useRef | 0.758 | react.dev/learn/referencing-values-with-refs | 0.719 | react.dev/reference/react/useRef | 0.674 |
| crawlee | #1 | react.dev/reference/react/useRef | 0.758 | react.dev/learn/referencing-values-with-refs | 0.719 | react.dev/reference/react/useRef | 0.674 |
| colly+md | #1 | react.dev/reference/react/useRef | 0.758 | react.dev/learn/referencing-values-with-refs | 0.719 | react.dev/reference/react/useRef | 0.674 |
| playwright | #1 | react.dev/reference/react/useRef | 0.758 | react.dev/learn/referencing-values-with-refs | 0.719 | react.dev/reference/react/useRef | 0.674 |


**Q7: How do I pass props between React components?** [conceptual]
*(expects URL containing: `passing-props`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |
| crawl4ai | #1 | react.dev/learn/passing-props-to-a-component | 0.758 | react.dev/learn/describing-the-ui | 0.745 | react.dev/learn/describing-the-ui | 0.706 |
| crawl4ai-raw | #1 | react.dev/learn/passing-props-to-a-component | 0.758 | react.dev/learn/describing-the-ui | 0.745 | react.dev/learn/describing-the-ui | 0.705 |
| scrapy+md | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |
| crawlee | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.755 | react.dev/learn/passing-data-deeply-with-context | 0.708 |
| colly+md | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |
| playwright | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |


**Q8: How do I conditionally render content in React?** [code-example]
*(expects URL containing: `conditional-rendering`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn | 0.750 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/describing-the-ui | 0.703 |
| crawl4ai | #3 | react.dev/learn/describing-the-ui | 0.751 | react.dev/learn | 0.734 | react.dev/learn/conditional-rendering | 0.722 |
| crawl4ai-raw | #3 | react.dev/learn/describing-the-ui | 0.751 | react.dev/learn | 0.734 | react.dev/learn/conditional-rendering | 0.722 |
| scrapy+md | #2 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/describing-the-ui | 0.703 |
| crawlee | #2 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/describing-the-ui | 0.704 |
| colly+md | #2 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/describing-the-ui | 0.703 |
| playwright | #2 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/describing-the-ui | 0.703 |


**Q9: What is the useMemo hook for in React?** [api-function]
*(expects URL containing: `useMemo`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useMemo | 0.736 | react.dev/learn/react-compiler/introduction | 0.649 | react.dev/reference/react/useMemo | 0.644 |
| crawl4ai | #1 | react.dev/reference/react/useMemo | 0.710 | react.dev/reference/react/useMemo | 0.700 | react.dev/learn/react-compiler/introduction | 0.675 |
| crawl4ai-raw | #1 | react.dev/reference/react/useMemo | 0.710 | react.dev/reference/react/useMemo | 0.700 | react.dev/learn/react-compiler/introduction | 0.675 |
| scrapy+md | #1 | react.dev/reference/react/useMemo | 0.736 | react.dev/learn/react-compiler/introduction | 0.649 | react.dev/reference/react/useMemo | 0.644 |
| crawlee | #1 | react.dev/reference/react/useMemo | 0.736 | react.dev/learn/react-compiler/introduction | 0.649 | react.dev/reference/react/useMemo | 0.644 |
| colly+md | #1 | react.dev/reference/react/useMemo | 0.736 | react.dev/learn/react-compiler/introduction | 0.649 | react.dev/reference/react/useMemo | 0.644 |
| playwright | #1 | react.dev/reference/react/useMemo | 0.736 | react.dev/learn/react-compiler/introduction | 0.649 | react.dev/reference/react/useMemo | 0.644 |


**Q10: How do I use the useState hook in React?** [api-function]
*(expects URL containing: `useState`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useState | 0.753 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |
| crawl4ai | #1 | react.dev/reference/react/useState | 0.719 | react.dev/learn | 0.695 | react.dev/learn/state-a-components-memory | 0.663 |
| crawl4ai-raw | #1 | react.dev/reference/react/useState | 0.719 | react.dev/learn | 0.695 | react.dev/learn/state-a-components-memory | 0.663 |
| scrapy+md | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |
| crawlee | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |
| colly+md | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |
| playwright | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |


**Q11: How do I use the useCallback hook in React?** [api-function]
*(expects URL containing: `useCallback`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.656 | react.dev/reference/react/useCallback | 0.643 |
| crawl4ai | #1 | react.dev/reference/react/useCallback | 0.703 | react.dev/reference/react/useCallback | 0.681 | react.dev/learn/typescript | 0.668 |
| crawl4ai-raw | #1 | react.dev/reference/react/useCallback | 0.703 | react.dev/reference/react/useCallback | 0.681 | react.dev/learn/typescript | 0.668 |
| scrapy+md | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.655 | react.dev/reference/react/useCallback | 0.644 |
| crawlee | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.655 | react.dev/reference/react/useCallback | 0.644 |
| colly+md | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.655 | react.dev/reference/react/useCallback | 0.644 |
| playwright | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.655 | react.dev/reference/react/useCallback | 0.644 |


**Q12: How do I use the useReducer hook in React?** [api-function]
*(expects URL containing: `useReducer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useReducer | 0.788 | react.dev/reference/react/useReducer | 0.733 | react.dev/reference/react/useReducer | 0.716 |
| crawl4ai | #1 | react.dev/reference/react/useReducer | 0.764 | react.dev/reference/react/useReducer | 0.740 | react.dev/reference/react/useReducer | 0.716 |
| crawl4ai-raw | #1 | react.dev/reference/react/useReducer | 0.764 | react.dev/reference/react/useReducer | 0.740 | react.dev/reference/react/useReducer | 0.716 |
| scrapy+md | #1 | react.dev/reference/react/useReducer | 0.785 | react.dev/reference/react/useReducer | 0.735 | react.dev/reference/react/useReducer | 0.716 |
| crawlee | #1 | react.dev/reference/react/useReducer | 0.785 | react.dev/reference/react/useReducer | 0.735 | react.dev/reference/react/useReducer | 0.716 |
| colly+md | #1 | react.dev/reference/react/useReducer | 0.785 | react.dev/reference/react/useReducer | 0.735 | react.dev/reference/react/useReducer | 0.716 |
| playwright | #1 | react.dev/reference/react/useReducer | 0.785 | react.dev/reference/react/useReducer | 0.735 | react.dev/reference/react/useReducer | 0.716 |


**Q13: How do I handle events like clicks in React?** [code-example]
*(expects URL containing: `responding-to-events`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.673 | react.dev/learn/adding-interactivity | 0.668 |
| crawl4ai | #1 | react.dev/learn/responding-to-events | 0.690 | react.dev/learn | 0.682 | react.dev/learn/adding-interactivity | 0.674 |
| crawl4ai-raw | #1 | react.dev/learn/responding-to-events | 0.690 | react.dev/learn | 0.682 | react.dev/learn/adding-interactivity | 0.676 |
| scrapy+md | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.668 | react.dev/learn/adding-interactivity | 0.668 |
| crawlee | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.668 | react.dev/learn/adding-interactivity | 0.645 |
| colly+md | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.668 | react.dev/learn/adding-interactivity | 0.668 |
| playwright | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.668 | react.dev/learn/adding-interactivity | 0.668 |


**Q14: What is the Suspense component in React?** [api-function]
*(expects URL containing: `Suspense`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #9 | react.dev/blog/2022/03/29/react-v18 | 0.725 | react.dev/blog/2022/03/29/react-v18 | 0.712 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.690 |
| crawl4ai | #3 | react.dev/blog/2022/03/29/react-v18 | 0.734 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/reference/react/Suspense | 0.720 |
| crawl4ai-raw | #3 | react.dev/blog/2022/03/29/react-v18 | 0.734 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/reference/react/Suspense | 0.720 |
| scrapy+md | #9 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.712 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.681 |
| crawlee | #9 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.712 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.681 |
| colly+md | #9 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.712 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.681 |
| playwright | #9 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.712 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.681 |


**Q15: How do I add interactivity to React components?** [conceptual]
*(expects URL containing: `adding-interactivity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |
| crawl4ai | #2 | react.dev/ | 0.830 | react.dev/learn/adding-interactivity | 0.752 | react.dev/reference/rsc/server-components | 0.720 |
| crawl4ai-raw | #2 | react.dev/ | 0.830 | react.dev/learn/adding-interactivity | 0.752 | react.dev/reference/rsc/server-components | 0.720 |
| scrapy+md | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/learn/queueing-a-series-of-state-updates | 0.724 |
| crawlee | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |
| colly+md | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |
| playwright | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |


**Q16: How do I install and set up a new React project?** [conceptual]
*(expects URL containing: `installation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn/add-react-to-an-existing-project | 0.672 | react.dev/learn/react-compiler/installation | 0.660 | react.dev/ | 0.653 |
| crawl4ai | #1 | react.dev/learn/installation | 0.695 | react.dev/learn/installation | 0.693 | react.dev/learn/installation | 0.682 |
| crawl4ai-raw | #2 | react.dev/learn/add-react-to-an-existing-project | 0.696 | react.dev/learn/installation | 0.695 | react.dev/learn/installation | 0.693 |
| scrapy+md | #2 | react.dev/learn/add-react-to-an-existing-project | 0.672 | react.dev/learn/react-compiler/installation | 0.660 | react.dev/learn/creating-a-react-app | 0.642 |
| crawlee | #3 | react.dev/learn/setup | 0.693 | react.dev/learn/react-compiler | 0.678 | react.dev/learn/installation | 0.666 |
| colly+md | #4 | react.dev/learn/setup | 0.693 | react.dev/learn/react-compiler | 0.678 | react.dev/learn/add-react-to-an-existing-project | 0.672 |
| playwright | #4 | react.dev/learn/setup | 0.693 | react.dev/learn/react-compiler | 0.678 | react.dev/learn/add-react-to-an-existing-project | 0.672 |


</details>

## wikipedia-python

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 0.700 | 1024 | 50 |
| crawl4ai | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 0.700 | 1243 | 50 |
| crawl4ai-raw | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 0.700 | 1243 | 50 |
| scrapy+md | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 0.700 | 1309 | 50 |
| crawlee | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 0.700 | 2148 | 50 |
| colly+md | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 70% (7/10) | 0.700 | 1378 | 50 |
| playwright | 60% (6/10) | 60% (6/10) | 60% (6/10) | 60% (6/10) | 60% (6/10) | 0.600 | 1112 | 42 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for wikipedia-python</summary>

**Q1: Who created the Python programming language?** [factual-lookup]
*(expects URL containing: `Python_(programming_language)`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.619 | en.wikipedia.org/wiki/Python_(programming_language | 0.553 | en.wikipedia.org/wiki/Python_(programming_language | 0.549 |
| crawl4ai | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.553 | en.wikipedia.org/wiki/Python_(programming_language | 0.538 | en.wikipedia.org/wiki/Python_(programming_language | 0.523 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.553 | en.wikipedia.org/wiki/Python_(programming_language | 0.538 | en.wikipedia.org/wiki/Python_(programming_language | 0.523 |
| scrapy+md | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.553 | en.wikipedia.org/wiki/Python_(programming_language | 0.549 | en.wikipedia.org/wiki/Python_(programming_language | 0.523 |
| crawlee | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.553 | en.wikipedia.org/wiki/Python_(programming_language | 0.549 | en.wikipedia.org/wiki/Python_(programming_language | 0.515 |
| colly+md | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.553 | en.wikipedia.org/wiki/Python_(programming_language | 0.549 | en.wikipedia.org/wiki/Python_(programming_language | 0.523 |
| playwright | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.553 | en.wikipedia.org/wiki/Python_(programming_language | 0.549 | en.wikipedia.org/wiki/Python_(programming_language | 0.523 |


**Q2: What is the Python Software Foundation?** [factual-lookup]
*(expects URL containing: `Python_Software_Foundation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.783 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.713 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.695 |
| crawl4ai | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.768 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.741 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.666 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.768 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.741 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.666 |
| scrapy+md | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.755 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.713 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.649 |
| crawlee | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.757 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.713 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.649 |
| colly+md | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.755 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.713 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.649 |
| playwright | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.755 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.713 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.649 |


**Q3: Who is Guido van Rossum?** [factual-lookup]
*(expects URL containing: `Guido_van_Rossum`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.428 | en.wikipedia.org/wiki/Python_(programming_language | 0.419 | en.wikipedia.org/wiki/Python_(programming_language | 0.400 |
| crawl4ai | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.421 | en.wikipedia.org/wiki/Python_(programming_language | 0.417 | en.wikipedia.org/wiki/Python_(programming_language | 0.412 |
| crawl4ai-raw | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.421 | en.wikipedia.org/wiki/Python_(programming_language | 0.418 | en.wikipedia.org/wiki/Python_(programming_language | 0.412 |
| scrapy+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.465 | en.wikipedia.org/wiki/Python_(programming_language | 0.419 | en.wikipedia.org/wiki/Python_(programming_language | 0.418 |
| crawlee | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.468 | en.wikipedia.org/wiki/Python_(programming_language | 0.419 | en.wikipedia.org/wiki/Python_(programming_language | 0.419 |
| colly+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.465 | en.wikipedia.org/wiki/Python_(programming_language | 0.419 | en.wikipedia.org/wiki/Python_(programming_language | 0.418 |
| playwright | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.463 | en.wikipedia.org/wiki/Python_(programming_language | 0.419 | en.wikipedia.org/wiki/Python_(programming_language | 0.418 |


**Q4: What is CPython and how does it work?** [factual-lookup]
*(expects URL containing: `CPython`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.526 | en.wikipedia.org/wiki/Python_(programming_language | 0.512 | en.wikipedia.org/wiki/Python_(programming_language | 0.496 |
| crawl4ai | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.516 | en.wikipedia.org/wiki/Python_(programming_language | 0.504 | en.wikipedia.org/wiki/Python_(programming_language | 0.498 |
| crawl4ai-raw | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.516 | en.wikipedia.org/wiki/Python_(programming_language | 0.504 | en.wikipedia.org/wiki/Python_(programming_language | 0.498 |
| scrapy+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.526 | en.wikipedia.org/wiki/Python_(programming_language | 0.496 | en.wikipedia.org/wiki/Python_(programming_language | 0.486 |
| crawlee | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.526 | en.wikipedia.org/wiki/Python_(programming_language | 0.496 | en.wikipedia.org/wiki/Python_(programming_language | 0.486 |
| colly+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.526 | en.wikipedia.org/wiki/Python_(programming_language | 0.496 | en.wikipedia.org/wiki/Python_(programming_language | 0.486 |
| playwright | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.526 | en.wikipedia.org/wiki/Python_(programming_language | 0.496 | en.wikipedia.org/wiki/Python_(programming_language | 0.486 |


**Q5: How does Python compare to other programming languages?** [conceptual]
*(expects URL containing: `Comparison_of_programming_languages`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.664 | en.wikipedia.org/wiki/Python_(programming_language | 0.648 | en.wikipedia.org/wiki/Python_(programming_language | 0.641 |
| crawl4ai | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.672 | en.wikipedia.org/wiki/Python_(programming_language | 0.666 | en.wikipedia.org/wiki/Python_(programming_language | 0.649 |
| crawl4ai-raw | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.672 | en.wikipedia.org/wiki/Python_(programming_language | 0.666 | en.wikipedia.org/wiki/Python_(programming_language | 0.649 |
| scrapy+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.664 | en.wikipedia.org/wiki/Python_(programming_language | 0.648 | en.wikipedia.org/wiki/Python_(programming_language | 0.629 |
| crawlee | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.664 | en.wikipedia.org/wiki/Python_(programming_language | 0.648 | en.wikipedia.org/wiki/Python_(programming_language | 0.629 |
| colly+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.664 | en.wikipedia.org/wiki/Python_(programming_language | 0.648 | en.wikipedia.org/wiki/Python_(programming_language | 0.629 |
| playwright | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.664 | en.wikipedia.org/wiki/Python_(programming_language | 0.648 | en.wikipedia.org/wiki/Python_(programming_language | 0.629 |


**Q6: What is NumPy and what is it used for?** [factual-lookup]
*(expects URL containing: `NumPy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/NumPy | 0.769 | en.wikipedia.org/wiki/NumPy | 0.702 | en.wikipedia.org/wiki/NumPy | 0.655 |
| crawl4ai | #1 | en.wikipedia.org/wiki/NumPy | 0.758 | en.wikipedia.org/wiki/NumPy | 0.730 | en.wikipedia.org/wiki/NumPy | 0.680 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/NumPy | 0.758 | en.wikipedia.org/wiki/NumPy | 0.730 | en.wikipedia.org/wiki/NumPy | 0.680 |
| scrapy+md | #1 | en.wikipedia.org/wiki/NumPy | 0.769 | en.wikipedia.org/wiki/NumPy | 0.702 | en.wikipedia.org/wiki/NumPy | 0.655 |
| crawlee | #1 | en.wikipedia.org/wiki/NumPy | 0.769 | en.wikipedia.org/wiki/NumPy | 0.702 | en.wikipedia.org/wiki/NumPy | 0.655 |
| colly+md | #1 | en.wikipedia.org/wiki/NumPy | 0.769 | en.wikipedia.org/wiki/NumPy | 0.702 | en.wikipedia.org/wiki/NumPy | 0.655 |
| playwright | #1 | en.wikipedia.org/wiki/NumPy | 0.769 | en.wikipedia.org/wiki/NumPy | 0.702 | en.wikipedia.org/wiki/NumPy | 0.655 |


**Q7: What is SQLAlchemy and how is it used with Python?** [factual-lookup]
*(expects URL containing: `SQLAlchemy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/SQLAlchemy | 0.651 | en.wikipedia.org/wiki/SQLAlchemy | 0.582 | en.wikipedia.org/wiki/SQLAlchemy | 0.573 |
| crawl4ai | #1 | en.wikipedia.org/wiki/SQLAlchemy | 0.679 | en.wikipedia.org/wiki/SQLAlchemy | 0.620 | en.wikipedia.org/wiki/SQLAlchemy | 0.599 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/SQLAlchemy | 0.679 | en.wikipedia.org/wiki/SQLAlchemy | 0.620 | en.wikipedia.org/wiki/SQLAlchemy | 0.599 |
| scrapy+md | #1 | en.wikipedia.org/wiki/SQLAlchemy | 0.681 | en.wikipedia.org/wiki/SQLAlchemy | 0.573 | en.wikipedia.org/wiki/SQLAlchemy | 0.551 |
| crawlee | #1 | en.wikipedia.org/wiki/SQLAlchemy | 0.681 | en.wikipedia.org/wiki/SQLAlchemy | 0.573 | en.wikipedia.org/wiki/SQLAlchemy | 0.551 |
| colly+md | #1 | en.wikipedia.org/wiki/SQLAlchemy | 0.681 | en.wikipedia.org/wiki/SQLAlchemy | 0.573 | en.wikipedia.org/wiki/SQLAlchemy | 0.551 |
| playwright | #1 | en.wikipedia.org/wiki/SQLAlchemy | 0.681 | en.wikipedia.org/wiki/SQLAlchemy | 0.573 | en.wikipedia.org/wiki/SQLAlchemy | 0.551 |


**Q8: What is metaprogramming in computer science?** [conceptual]
*(expects URL containing: `Metaprogramming`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/Metaprogramming | 0.773 | en.wikipedia.org/wiki/Metaprogramming | 0.698 | en.wikipedia.org/wiki/Metaprogramming | 0.643 |
| crawl4ai | #1 | en.wikipedia.org/wiki/Metaprogramming | 0.725 | en.wikipedia.org/wiki/Metaprogramming | 0.697 | en.wikipedia.org/wiki/Metaprogramming | 0.647 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/Metaprogramming | 0.725 | en.wikipedia.org/wiki/Metaprogramming | 0.697 | en.wikipedia.org/wiki/Metaprogramming | 0.647 |
| scrapy+md | #1 | en.wikipedia.org/wiki/Metaprogramming | 0.720 | en.wikipedia.org/wiki/Metaprogramming | 0.698 | en.wikipedia.org/wiki/Metaprogramming | 0.693 |
| crawlee | #1 | en.wikipedia.org/wiki/Metaprogramming | 0.720 | en.wikipedia.org/wiki/Metaprogramming | 0.698 | en.wikipedia.org/wiki/Metaprogramming | 0.691 |
| colly+md | #1 | en.wikipedia.org/wiki/Metaprogramming | 0.720 | en.wikipedia.org/wiki/Metaprogramming | 0.698 | en.wikipedia.org/wiki/Metaprogramming | 0.693 |
| playwright | #1 | en.wikipedia.org/wiki/Metaprogramming | 0.720 | en.wikipedia.org/wiki/Metaprogramming | 0.698 | en.wikipedia.org/wiki/Metaprogramming | 0.693 |


**Q9: What are list comprehensions in programming?** [conceptual]
*(expects URL containing: `List_comprehension`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/List_comprehensions | 0.734 | en.wikipedia.org/wiki/List_comprehensions | 0.698 | en.wikipedia.org/wiki/List_comprehensions | 0.631 |
| crawl4ai | #1 | en.wikipedia.org/wiki/List_comprehensions | 0.731 | en.wikipedia.org/wiki/List_comprehensions | 0.727 | en.wikipedia.org/wiki/List_comprehensions | 0.662 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/List_comprehensions | 0.731 | en.wikipedia.org/wiki/List_comprehensions | 0.727 | en.wikipedia.org/wiki/List_comprehensions | 0.662 |
| scrapy+md | #1 | en.wikipedia.org/wiki/List_comprehensions | 0.722 | en.wikipedia.org/wiki/List_comprehensions | 0.696 | en.wikipedia.org/wiki/List_comprehensions | 0.631 |
| crawlee | #1 | en.wikipedia.org/wiki/List_comprehensions | 0.719 | en.wikipedia.org/wiki/List_comprehensions | 0.696 | en.wikipedia.org/wiki/List_comprehensions | 0.642 |
| colly+md | #1 | en.wikipedia.org/wiki/List_comprehensions | 0.722 | en.wikipedia.org/wiki/List_comprehensions | 0.696 | en.wikipedia.org/wiki/List_comprehensions | 0.643 |
| playwright | #1 | en.wikipedia.org/wiki/List_comprehensions | 0.722 | en.wikipedia.org/wiki/List_comprehensions | 0.696 | en.wikipedia.org/wiki/List_comprehensions | 0.643 |


**Q10: How does memory management work in programming?** [conceptual]
*(expects URL containing: `Memory_management`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/Memory_management | 0.672 | en.wikipedia.org/wiki/Memory_management | 0.665 | en.wikipedia.org/wiki/Memory_management | 0.631 |
| crawl4ai | #1 | en.wikipedia.org/wiki/Memory_management | 0.703 | en.wikipedia.org/wiki/Memory_management | 0.680 | en.wikipedia.org/wiki/Memory_management | 0.676 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/Memory_management | 0.703 | en.wikipedia.org/wiki/Memory_management | 0.680 | en.wikipedia.org/wiki/Memory_management | 0.676 |
| scrapy+md | #1 | en.wikipedia.org/wiki/Memory_management | 0.679 | en.wikipedia.org/wiki/Memory_management | 0.672 | en.wikipedia.org/wiki/Memory_management | 0.631 |
| crawlee | #1 | en.wikipedia.org/wiki/Memory_management | 0.679 | en.wikipedia.org/wiki/Memory_management | 0.672 | en.wikipedia.org/wiki/Memory_management | 0.631 |
| colly+md | #1 | en.wikipedia.org/wiki/Memory_management | 0.679 | en.wikipedia.org/wiki/Memory_management | 0.672 | en.wikipedia.org/wiki/Memory_management | 0.631 |
| playwright | miss | en.wikipedia.org/wiki/Strongly_typed | 0.550 | en.wikipedia.org/wiki/Assertion_(programming) | 0.417 | en.wikipedia.org/wiki/Strongly_typed | 0.415 |


</details>

## stripe-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 67% (12/18) | 72% (13/18) | 72% (13/18) | 78% (14/18) | 78% (14/18) | 0.696 | 2772 | 257 |
| crawl4ai | 61% (11/18) | 72% (13/18) | 78% (14/18) | 78% (14/18) | 89% (16/18) | 0.677 | 3379 | 257 |
| crawl4ai-raw | 61% (11/18) | 72% (13/18) | 78% (14/18) | 78% (14/18) | 89% (16/18) | 0.677 | 3378 | 257 |
| scrapy+md | 50% (9/18) | 78% (14/18) | 83% (15/18) | 89% (16/18) | 89% (16/18) | 0.631 | 3035 | 257 |
| crawlee | 67% (12/18) | 72% (13/18) | 83% (15/18) | 94% (17/18) | 94% (17/18) | 0.732 | 15683 | 257 |
| colly+md | 67% (12/18) | 78% (14/18) | 83% (15/18) | 94% (17/18) | 94% (17/18) | 0.743 | 14661 | 254 |
| playwright | 67% (12/18) | 72% (13/18) | 83% (15/18) | 94% (17/18) | 94% (17/18) | 0.735 | 15680 | 257 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for stripe-docs</summary>

**Q1: How do I create a payment intent with Stripe?** [api-function]
*(expects URL containing: `payment-intent`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/upgrades/manage-payment-methods | 0.724 | docs.stripe.com/apple-pay | 0.669 | docs.stripe.com/billing/subscriptions/build-subscr | 0.616 |
| crawl4ai | miss | docs.stripe.com/upgrades/manage-payment-methods | 0.722 | docs.stripe.com/apple-pay | 0.671 | docs.stripe.com/upgrades/manage-payment-methods | 0.629 |
| crawl4ai-raw | miss | docs.stripe.com/upgrades/manage-payment-methods | 0.722 | docs.stripe.com/apple-pay | 0.671 | docs.stripe.com/upgrades/manage-payment-methods | 0.629 |
| scrapy+md | miss | docs.stripe.com/upgrades/manage-payment-methods | 0.720 | docs.stripe.com/apple-pay | 0.669 | docs.stripe.com/billing/subscriptions/build-subscr | 0.621 |
| crawlee | miss | docs.stripe.com/upgrades/manage-payment-methods | 0.722 | docs.stripe.com/agentic-commerce/apps/accept-payme | 0.676 | docs.stripe.com/apple-pay | 0.668 |
| colly+md | miss | docs.stripe.com/upgrades/manage-payment-methods | 0.720 | docs.stripe.com/agentic-commerce/apps/accept-payme | 0.676 | docs.stripe.com/apple-pay | 0.669 |
| playwright | miss | docs.stripe.com/upgrades/manage-payment-methods | 0.722 | docs.stripe.com/agentic-commerce/apps/accept-payme | 0.676 | docs.stripe.com/apple-pay | 0.668 |


**Q2: How do I handle webhooks from Stripe?** [api-function]
*(expects URL containing: `webhook`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | docs.stripe.com/error-handling | 0.712 | docs.stripe.com/billing/taxes/collect-taxes | 0.625 | docs.stripe.com/billing/subscriptions/build-subscr | 0.624 |
| crawl4ai | #16 | docs.stripe.com/error-handling | 0.714 | docs.stripe.com/billing/subscriptions/build-subscr | 0.687 | docs.stripe.com/billing/subscriptions/build-subscr | 0.680 |
| crawl4ai-raw | #16 | docs.stripe.com/error-handling | 0.714 | docs.stripe.com/billing/subscriptions/build-subscr | 0.687 | docs.stripe.com/billing/subscriptions/build-subscr | 0.680 |
| scrapy+md | #6 | docs.stripe.com/error-handling | 0.712 | docs.stripe.com/billing/subscriptions/build-subscr | 0.624 | docs.stripe.com/billing/taxes/collect-taxes | 0.621 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/webhooks | 0.770 | docs.stripe.com/error-handling | 0.715 | docs.stripe.com/billing/subscriptions/build-subscr | 0.633 |
| colly+md | #1 | docs.stripe.com/billing/subscriptions/webhooks | 0.770 | docs.stripe.com/error-handling | 0.712 | docs.stripe.com/billing/subscriptions/build-subscr | 0.633 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/webhooks | 0.770 | docs.stripe.com/error-handling | 0.715 | docs.stripe.com/billing/subscriptions/build-subscr | 0.633 |


**Q3: How do I set up Stripe subscriptions?** [api-function]
*(expects URL containing: `subscription`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.715 | docs.stripe.com/billing/taxes/migration | 0.687 | docs.stripe.com/billing/subscriptions/build-subscr | 0.672 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.737 | docs.stripe.com/billing/subscriptions/build-subscr | 0.721 | docs.stripe.com/billing/subscriptions/build-subscr | 0.716 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.737 | docs.stripe.com/billing/subscriptions/build-subscr | 0.721 | docs.stripe.com/billing/subscriptions/build-subscr | 0.716 |
| scrapy+md | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.714 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.713 | docs.stripe.com/billing/subscriptions/build-subscr | 0.672 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/paypal | 0.778 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 |
| colly+md | #1 | docs.stripe.com/billing/subscriptions/paypal | 0.778 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/paypal | 0.778 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 |


**Q4: How do I authenticate with the Stripe API?** [api-function]
*(expects URL containing: `authentication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #31 | docs.stripe.com/keys | 0.695 | docs.stripe.com/error-handling | 0.610 | docs.stripe.com/get-started/account/activate | 0.609 |
| crawl4ai | miss | docs.stripe.com/apis | 0.652 | docs.stripe.com/apis | 0.649 | docs.stripe.com/get-started/account/activate | 0.644 |
| crawl4ai-raw | miss | docs.stripe.com/apis | 0.652 | docs.stripe.com/apis | 0.649 | docs.stripe.com/get-started/account/activate | 0.644 |
| scrapy+md | miss | docs.stripe.com/apis | 0.672 | docs.stripe.com/get-started/account | 0.632 | docs.stripe.com/apis | 0.625 |
| crawlee | #1 | docs.stripe.com/payment-authentication/writing-que | 0.702 | docs.stripe.com/apis | 0.672 | docs.stripe.com/keys | 0.665 |
| colly+md | #1 | docs.stripe.com/payment-authentication/writing-que | 0.702 | docs.stripe.com/apis | 0.672 | docs.stripe.com/keys | 0.665 |
| playwright | #1 | docs.stripe.com/payment-authentication/writing-que | 0.702 | docs.stripe.com/apis | 0.672 | docs.stripe.com/keys | 0.665 |


**Q5: How do I handle errors in the Stripe API?** [api-function]
*(expects URL containing: `error-handling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/error-handling | 0.722 | docs.stripe.com/error-low-level | 0.701 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.696 |
| crawl4ai | #3 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.695 | docs.stripe.com/error-low-level | 0.668 | docs.stripe.com/error-handling | 0.664 |
| crawl4ai-raw | #3 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.695 | docs.stripe.com/error-low-level | 0.668 | docs.stripe.com/error-handling | 0.664 |
| scrapy+md | #3 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.696 | docs.stripe.com/error-low-level | 0.656 | docs.stripe.com/error-handling | 0.649 |
| crawlee | #1 | docs.stripe.com/error-handling | 0.793 | docs.stripe.com/error-low-level | 0.782 | docs.stripe.com/error-codes | 0.705 |
| colly+md | #1 | docs.stripe.com/error-handling | 0.793 | docs.stripe.com/error-low-level | 0.781 | docs.stripe.com/error-codes | 0.705 |
| playwright | #1 | docs.stripe.com/error-handling | 0.793 | docs.stripe.com/error-low-level | 0.782 | docs.stripe.com/error-codes | 0.705 |


**Q6: How do I process refunds with Stripe?** [api-function]
*(expects URL containing: `refund`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/billing/subscriptions/third-party- | 0.626 | docs.stripe.com/ach-deprecated | 0.621 | docs.stripe.com/billing/taxes/migration | 0.557 |
| crawl4ai | #11 | docs.stripe.com/billing/subscriptions/third-party- | 0.716 | docs.stripe.com/ach-deprecated | 0.618 | docs.stripe.com/get-started/account | 0.571 |
| crawl4ai-raw | #11 | docs.stripe.com/billing/subscriptions/third-party- | 0.716 | docs.stripe.com/ach-deprecated | 0.618 | docs.stripe.com/get-started/account | 0.571 |
| scrapy+md | #3 | docs.stripe.com/billing/subscriptions/third-party- | 0.625 | docs.stripe.com/ach-deprecated | 0.621 | docs.stripe.com/apple-pay/disputes-refunds | 0.596 |
| crawlee | #9 | docs.stripe.com/billing/subscriptions/third-party- | 0.628 | docs.stripe.com/ach-deprecated | 0.621 | docs.stripe.com/billing/revenue-recovery | 0.590 |
| colly+md | #3 | docs.stripe.com/billing/subscriptions/third-party- | 0.625 | docs.stripe.com/ach-deprecated | 0.621 | docs.stripe.com/apple-pay/disputes-refunds | 0.596 |
| playwright | #9 | docs.stripe.com/billing/subscriptions/third-party- | 0.629 | docs.stripe.com/ach-deprecated | 0.621 | docs.stripe.com/billing/revenue-recovery | 0.590 |


**Q7: How do I use Stripe checkout for payments?** [js-rendered]
*(expects URL containing: `checkout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.646 | docs.stripe.com/upgrades/manage-payment-methods | 0.645 | docs.stripe.com/billing/subscriptions/build-subscr | 0.639 |
| crawl4ai | #2 | docs.stripe.com/upgrades/manage-payment-methods | 0.664 | docs.stripe.com/billing/subscriptions/build-subscr | 0.655 | docs.stripe.com/billing/subscriptions/paypal | 0.644 |
| crawl4ai-raw | #2 | docs.stripe.com/upgrades/manage-payment-methods | 0.664 | docs.stripe.com/billing/subscriptions/build-subscr | 0.655 | docs.stripe.com/billing/subscriptions/paypal | 0.644 |
| scrapy+md | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.646 | docs.stripe.com/upgrades/manage-payment-methods | 0.645 | docs.stripe.com/billing/subscriptions/build-subscr | 0.639 |
| crawlee | #5 | docs.stripe.com/agentic-commerce/apps/accept-payme | 0.681 | docs.stripe.com/billing/subscriptions/third-party- | 0.655 | docs.stripe.com/atlas/accept-payments | 0.650 |
| colly+md | #6 | docs.stripe.com/agentic-commerce/apps/accept-payme | 0.681 | docs.stripe.com/billing/subscriptions/third-party- | 0.655 | docs.stripe.com/atlas/accept-payments | 0.650 |
| playwright | #4 | docs.stripe.com/agentic-commerce/apps/accept-payme | 0.681 | docs.stripe.com/billing/subscriptions/third-party- | 0.655 | docs.stripe.com/atlas/accept-payments | 0.650 |


**Q8: How do I test Stripe payments in development?** [code-example]
*(expects URL containing: `testing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/automated-testing | 0.680 | docs.stripe.com/billing/testing | 0.677 | docs.stripe.com/automated-testing | 0.663 |
| crawl4ai | #1 | docs.stripe.com/automated-testing | 0.693 | docs.stripe.com/get-started/data-migrations/pan-im | 0.679 | docs.stripe.com/billing/testing | 0.675 |
| crawl4ai-raw | #1 | docs.stripe.com/automated-testing | 0.693 | docs.stripe.com/get-started/data-migrations/pan-im | 0.679 | docs.stripe.com/billing/testing | 0.675 |
| scrapy+md | #1 | docs.stripe.com/automated-testing | 0.680 | docs.stripe.com/automated-testing | 0.663 | docs.stripe.com/billing/testing | 0.658 |
| crawlee | #1 | docs.stripe.com/automated-testing | 0.719 | docs.stripe.com/automated-testing | 0.680 | docs.stripe.com/automated-testing | 0.663 |
| colly+md | #1 | docs.stripe.com/automated-testing | 0.719 | docs.stripe.com/automated-testing | 0.680 | docs.stripe.com/automated-testing | 0.663 |
| playwright | #1 | docs.stripe.com/automated-testing | 0.719 | docs.stripe.com/automated-testing | 0.680 | docs.stripe.com/automated-testing | 0.663 |


**Q9: What are Stripe Connect and platform payments?** [conceptual]
*(expects URL containing: `connect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/ach-deprecated | 0.654 | docs.stripe.com/get-started/account/orgs/setup | 0.646 | docs.stripe.com/capital/overview | 0.636 |
| crawl4ai | #5 | docs.stripe.com/get-started/account/orgs/setup | 0.657 | docs.stripe.com/capital/overview | 0.647 | docs.stripe.com/capital/how-stripe-capital-works | 0.646 |
| crawl4ai-raw | #5 | docs.stripe.com/get-started/account/orgs/setup | 0.657 | docs.stripe.com/capital/overview | 0.647 | docs.stripe.com/capital/how-stripe-capital-works | 0.646 |
| scrapy+md | #5 | docs.stripe.com/ach-deprecated | 0.654 | docs.stripe.com/get-started/account/orgs/setup | 0.646 | docs.stripe.com/capital/overview | 0.640 |
| crawlee | #5 | docs.stripe.com/ach-deprecated | 0.661 | docs.stripe.com/get-started/account/orgs/setup | 0.646 | docs.stripe.com/capital/overview | 0.640 |
| colly+md | #5 | docs.stripe.com/ach-deprecated | 0.654 | docs.stripe.com/get-started/account/orgs/setup | 0.646 | docs.stripe.com/capital/overview | 0.640 |
| playwright | #5 | docs.stripe.com/ach-deprecated | 0.661 | docs.stripe.com/get-started/account/orgs/setup | 0.646 | docs.stripe.com/capital/overview | 0.640 |


**Q10: How do I set up usage-based billing with Stripe?** [js-rendered]
*(expects URL containing: `usage-based`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/usage-based- | 0.799 | docs.stripe.com/billing | 0.752 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.718 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/usage-based- | 0.738 | docs.stripe.com/billing | 0.721 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.719 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/usage-based- | 0.738 | docs.stripe.com/billing | 0.720 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.719 |
| scrapy+md | #2 | docs.stripe.com/billing | 0.752 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.721 | docs.stripe.com/billing/subscriptions/usage-based- | 0.718 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.836 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.812 | docs.stripe.com/billing/subscriptions/usage-based- | 0.772 |
| colly+md | #1 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.836 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.812 | docs.stripe.com/billing/subscriptions/usage-based | 0.772 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.836 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.812 | docs.stripe.com/billing/subscriptions/usage-based | 0.772 |


**Q11: How do I manage Stripe API keys?** [api-function]
*(expects URL containing: `keys`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/keys | 0.760 | docs.stripe.com/keys-best-practices | 0.738 | docs.stripe.com/keys | 0.722 |
| crawl4ai | #1 | docs.stripe.com/keys | 0.714 | docs.stripe.com/keys-best-practices | 0.706 | docs.stripe.com/keys | 0.702 |
| crawl4ai-raw | #1 | docs.stripe.com/keys | 0.714 | docs.stripe.com/keys-best-practices | 0.706 | docs.stripe.com/keys | 0.702 |
| scrapy+md | #1 | docs.stripe.com/keys-best-practices | 0.682 | docs.stripe.com/billing/subscriptions/prorations | 0.677 | docs.stripe.com/billing/subscriptions/build-subscr | 0.677 |
| crawlee | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/keys/restricted-api-keys | 0.755 | docs.stripe.com/keys | 0.724 |
| colly+md | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/keys/restricted-api-keys | 0.755 | docs.stripe.com/keys | 0.724 |
| playwright | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/keys/restricted-api-keys | 0.755 | docs.stripe.com/keys | 0.724 |


**Q12: How do I handle Stripe rate limits?** [api-function]
*(expects URL containing: `rate-limits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/rate-limits | 0.720 | docs.stripe.com/rate-limits | 0.704 | docs.stripe.com/rate-limits | 0.702 |
| crawl4ai | #1 | docs.stripe.com/rate-limits | 0.738 | docs.stripe.com/rate-limits | 0.721 | docs.stripe.com/rate-limits | 0.717 |
| crawl4ai-raw | #1 | docs.stripe.com/rate-limits | 0.738 | docs.stripe.com/rate-limits | 0.721 | docs.stripe.com/rate-limits | 0.717 |
| scrapy+md | #1 | docs.stripe.com/rate-limits | 0.720 | docs.stripe.com/rate-limits | 0.705 | docs.stripe.com/rate-limits | 0.702 |
| crawlee | #1 | docs.stripe.com/rate-limits | 0.791 | docs.stripe.com/rate-limits | 0.720 | docs.stripe.com/rate-limits | 0.705 |
| colly+md | #1 | docs.stripe.com/rate-limits | 0.791 | docs.stripe.com/rate-limits | 0.720 | docs.stripe.com/rate-limits | 0.705 |
| playwright | #1 | docs.stripe.com/rate-limits | 0.791 | docs.stripe.com/rate-limits | 0.720 | docs.stripe.com/rate-limits | 0.705 |


**Q13: How do I use metadata with Stripe objects?** [api-function]
*(expects URL containing: `metadata`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/metadata/use-cases | 0.781 | docs.stripe.com/metadata/use-cases | 0.778 | docs.stripe.com/metadata/use-cases | 0.743 |
| crawl4ai | #1 | docs.stripe.com/metadata/use-cases | 0.783 | docs.stripe.com/metadata/use-cases | 0.763 | docs.stripe.com/metadata/use-cases | 0.741 |
| crawl4ai-raw | #1 | docs.stripe.com/metadata/use-cases | 0.783 | docs.stripe.com/metadata/use-cases | 0.763 | docs.stripe.com/metadata/use-cases | 0.741 |
| scrapy+md | #1 | docs.stripe.com/metadata/use-cases | 0.778 | docs.stripe.com/metadata/use-cases | 0.743 | docs.stripe.com/metadata/use-cases | 0.730 |
| crawlee | #1 | docs.stripe.com/metadata/use-cases | 0.778 | docs.stripe.com/metadata | 0.759 | docs.stripe.com/metadata/use-cases | 0.746 |
| colly+md | #1 | docs.stripe.com/metadata/use-cases | 0.778 | docs.stripe.com/metadata | 0.759 | docs.stripe.com/metadata/use-cases | 0.746 |
| playwright | #1 | docs.stripe.com/metadata/use-cases | 0.778 | docs.stripe.com/metadata | 0.759 | docs.stripe.com/metadata/use-cases | 0.746 |


**Q14: How do I set up Apple Pay with Stripe?** [js-rendered]
*(expects URL containing: `apple-pay`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/apple-pay | 0.746 | docs.stripe.com/apple-pay | 0.696 | docs.stripe.com/apple-pay | 0.695 |
| crawl4ai | #1 | docs.stripe.com/apple-pay/cartes-bancaires | 0.778 | docs.stripe.com/apple-pay | 0.754 | docs.stripe.com/apple-pay | 0.746 |
| crawl4ai-raw | #1 | docs.stripe.com/apple-pay/cartes-bancaires | 0.778 | docs.stripe.com/apple-pay | 0.754 | docs.stripe.com/apple-pay | 0.746 |
| scrapy+md | #1 | docs.stripe.com/apple-pay | 0.742 | docs.stripe.com/apple-pay/cartes-bancaires | 0.708 | docs.stripe.com/apple-pay | 0.696 |
| crawlee | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.742 | docs.stripe.com/apple-pay/cartes-bancaires | 0.728 |
| colly+md | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.742 | docs.stripe.com/apple-pay/cartes-bancaires | 0.728 |
| playwright | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.742 | docs.stripe.com/apple-pay/cartes-bancaires | 0.728 |


**Q15: How do I issue cards with Stripe Issuing?** [api-function]
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.709 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.662 | docs.stripe.com/issuing/integration-guides/fleet | 0.662 |
| crawl4ai | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.691 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.688 | docs.stripe.com/issuing/integration-guides/embedde | 0.681 |
| crawl4ai-raw | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.690 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.688 | docs.stripe.com/issuing/integration-guides/embedde | 0.681 |
| scrapy+md | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.719 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.662 | docs.stripe.com/issuing/integration-guides/fleet | 0.662 |
| crawlee | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.719 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.662 | docs.stripe.com/issuing/integration-guides/fleet | 0.662 |
| colly+md | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.719 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.662 | docs.stripe.com/issuing/integration-guides/fleet | 0.662 |
| playwright | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.719 | docs.stripe.com/issuing/integration-guides/fleet | 0.662 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.661 |


**Q16: How do I recover failed subscription payments?** [js-rendered]
*(expects URL containing: `revenue-recovery`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/revenue-recovery | 0.715 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.584 |
| crawl4ai | #1 | docs.stripe.com/billing/revenue-recovery/recovery- | 0.613 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.594 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/revenue-recovery/recovery- | 0.613 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.594 |
| scrapy+md | #2 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.584 | docs.stripe.com/billing/revenue-recovery/recovery- | 0.582 |
| crawlee | #2 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.584 | docs.stripe.com/billing/revenue-recovery/recovery- | 0.582 |
| colly+md | #2 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.585 | docs.stripe.com/billing/revenue-recovery/recovery- | 0.582 |
| playwright | #2 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.584 | docs.stripe.com/billing/revenue-recovery/recovery- | 0.582 |


**Q17: How does Stripe handle tax calculation for billing?** [js-rendered]
*(expects URL containing: `billing/taxes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/taxes/tax-rates | 0.726 | docs.stripe.com/saas | 0.724 | docs.stripe.com/billing/taxes/migration | 0.716 |
| crawl4ai | #1 | docs.stripe.com/billing/taxes/tax-rates | 0.746 | docs.stripe.com/saas | 0.735 | docs.stripe.com/billing/taxes/migration | 0.711 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/taxes/tax-rates | 0.746 | docs.stripe.com/saas | 0.735 | docs.stripe.com/billing/taxes/migration | 0.711 |
| scrapy+md | #1 | docs.stripe.com/billing/taxes/tax-rates | 0.726 | docs.stripe.com/saas | 0.724 | docs.stripe.com/billing/taxes/migration | 0.716 |
| crawlee | #1 | docs.stripe.com/billing/taxes/tax-rates | 0.726 | docs.stripe.com/saas | 0.724 | docs.stripe.com/billing/taxes/migration | 0.718 |
| colly+md | #1 | docs.stripe.com/billing/taxes/tax-rates | 0.726 | docs.stripe.com/saas | 0.724 | docs.stripe.com/billing/taxes/migration | 0.718 |
| playwright | #1 | docs.stripe.com/billing/taxes/tax-rates | 0.726 | docs.stripe.com/saas | 0.724 | docs.stripe.com/billing/taxes/migration | 0.718 |


**Q18: How do I migrate data to Stripe?** [conceptual]
*(expects URL containing: `data-migrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.stripe.com/billing/taxes/migration | 0.728 | docs.stripe.com/billing/taxes/migration | 0.722 | docs.stripe.com/get-started/data-migrations/pan-ex | 0.711 |
| crawl4ai | #1 | docs.stripe.com/get-started/data-migrations/pan-im | 0.717 | docs.stripe.com/billing/taxes/migration | 0.714 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.708 |
| crawl4ai-raw | #1 | docs.stripe.com/get-started/data-migrations/pan-im | 0.717 | docs.stripe.com/billing/taxes/migration | 0.714 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.708 |
| scrapy+md | #3 | docs.stripe.com/billing/taxes/migration | 0.728 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.708 | docs.stripe.com/get-started/data-migrations/pan-ex | 0.690 |
| crawlee | #6 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/billing/taxes/migration | 0.728 |
| colly+md | #6 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/billing/taxes/migration | 0.728 |
| playwright | #6 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/billing/taxes/migration | 0.728 |


</details>

## blog-engineering

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 50% (4/8) | 75% (6/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.660 | 1791 | 200 |
| crawl4ai | 75% (6/8) | 75% (6/8) | 75% (6/8) | 75% (6/8) | 88% (7/8) | 0.757 | 5315 | 200 |
| crawl4ai-raw | 75% (6/8) | 75% (6/8) | 75% (6/8) | 75% (6/8) | 75% (6/8) | 0.753 | 5315 | 200 |
| scrapy+md | 75% (6/8) | 75% (6/8) | 88% (7/8) | 88% (7/8) | 100% (8/8) | 0.791 | 1636 | 200 |
| crawlee | 62% (5/8) | 62% (5/8) | 62% (5/8) | 62% (5/8) | 75% (6/8) | 0.635 | 5963 | 200 |
| colly+md | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 62% (5/8) | 0.512 | 3286 | 123 |
| playwright | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 5969 | 200 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for blog-engineering</summary>

**Q1: How does GitHub handle Kubernetes at scale?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/infrastructure/kubernetes- | 0.706 | github.blog/engineering/infrastructure/kubernetes- | 0.611 | github.blog/engineering/infrastructure/glb-directo | 0.602 |
| crawl4ai | #1 | github.blog/engineering/infrastructure/kubernetes- | 0.750 | github.blog/engineering/infrastructure/kubernetes- | 0.660 | github.blog/engineering/infrastructure/kubernetes- | 0.642 |
| crawl4ai-raw | #1 | github.blog/engineering/infrastructure/kubernetes- | 0.750 | github.blog/engineering/infrastructure/kubernetes- | 0.660 | github.blog/engineering/infrastructure/kubernetes- | 0.642 |
| scrapy+md | #1 | github.blog/engineering/infrastructure/kubernetes- | 0.710 | github.blog/engineering/infrastructure/kubernetes- | 0.611 | github.blog/engineering/infrastructure/kubernetes- | 0.596 |
| crawlee | #1 | github.blog/engineering/infrastructure/kubernetes- | 0.710 | github.blog/engineering/infrastructure/kubernetes- | 0.611 | github.blog/engineering/infrastructure/kubernetes- | 0.596 |
| colly+md | #1 | github.blog/engineering/architecture-optimization/ | 0.559 | github.blog/engineering/infrastructure/evolution-o | 0.558 | github.blog/news-insights/the-library/benchmarking | 0.536 |
| playwright | #1 | github.blog/engineering/infrastructure/building-re | 0.466 | github.blog/engineering/infrastructure/building-re | 0.426 | github.blog/engineering/infrastructure/building-re | 0.417 |


**Q2: How does GitHub protect against DDoS attacks?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/platform-security/syn-floo | 0.652 | github.blog/news-insights/company-news/ddos-incide | 0.650 | github.blog/news-insights/company-news/sha-1-colli | 0.649 |
| crawl4ai | #1 | github.blog/news-insights/company-news/ddos-incide | 0.678 | github.blog/news-insights/company-news/ddos-incide | 0.675 | github.blog/news-insights/company-news/sha-1-colli | 0.653 |
| crawl4ai-raw | #1 | github.blog/news-insights/company-news/ddos-incide | 0.678 | github.blog/news-insights/company-news/ddos-incide | 0.675 | github.blog/news-insights/company-news/sha-1-colli | 0.653 |
| scrapy+md | #1 | github.blog/news-insights/company-news/ddos-incide | 0.650 | github.blog/news-insights/company-news/sha-1-colli | 0.649 | github.blog/news-insights/company-news/ddos-incide | 0.648 |
| crawlee | #1 | github.blog/news-insights/company-news/ddos-incide | 0.650 | github.blog/news-insights/company-news/sha-1-colli | 0.649 | github.blog/news-insights/company-news/ddos-incide | 0.648 |
| colly+md | #1 | github.blog/engineering/platform-security/syn-floo | 0.577 | github.blog/engineering/architecture-optimization/ | 0.550 | github.blog/latest/ | 0.542 |
| playwright | #1 | github.blog/news-insights/company-news/gh-ost-gith | 0.508 | github.blog/news-insights/company-news/gh-ost-gith | 0.495 | github.blog/news-insights/company-news/gh-ost-gith | 0.475 |


**Q3: How does GitHub handle MySQL database operations?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/infrastructure/orchestrato | 0.715 | github.blog/engineering/infrastructure/orchestrato | 0.686 | github.blog/engineering/infrastructure/context-awa | 0.670 |
| crawl4ai | #1 | github.blog/engineering/infrastructure/orchestrato | 0.695 | github.blog/engineering/infrastructure/context-awa | 0.608 | github.blog/news-insights/company-news/gh-ost-gith | 0.594 |
| crawl4ai-raw | #1 | github.blog/engineering/infrastructure/orchestrato | 0.695 | github.blog/engineering/infrastructure/context-awa | 0.608 | github.blog/news-insights/company-news/gh-ost-gith | 0.594 |
| scrapy+md | #1 | github.blog/engineering/infrastructure/orchestrato | 0.688 | github.blog/engineering/infrastructure/context-awa | 0.577 | github.blog/news-insights/company-news/gh-ost-gith | 0.556 |
| crawlee | #1 | github.blog/engineering/infrastructure/orchestrato | 0.688 | github.blog/engineering/infrastructure/context-awa | 0.577 | github.blog/news-insights/company-news/gh-ost-gith | 0.556 |
| colly+md | #46 | github.blog/news-insights/the-library/basic-auth-p | 0.459 | github.blog/news-insights/the-library/scheduled-db | 0.459 | github.blog/news-insights/the-library/paris-git-tr | 0.459 |
| playwright | #1 | github.blog/news-insights/the-library/exception-mo | 0.448 | github.blog/news-insights/the-library/exception-mo | 0.447 | github.blog/news-insights/the-library/exception-mo | 0.441 |


**Q4: How does GitHub handle load balancing?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/infrastructure/glb-directo | 0.693 | github.blog/engineering/infrastructure/glb-directo | 0.621 | github.blog/engineering/architecture-optimization/ | 0.572 |
| crawl4ai | #1 | github.blog/engineering/infrastructure/glb-directo | 0.625 | github.blog/engineering/architecture-optimization/ | 0.577 | github.blog/engineering/infrastructure/context-awa | 0.555 |
| crawl4ai-raw | #1 | github.blog/engineering/infrastructure/glb-directo | 0.625 | github.blog/engineering/architecture-optimization/ | 0.577 | github.blog/engineering/infrastructure/context-awa | 0.555 |
| scrapy+md | #1 | github.blog/engineering/infrastructure/glb-directo | 0.620 | github.blog/engineering/architecture-optimization/ | 0.550 | github.blog/news-insights/company-news/sha-1-colli | 0.526 |
| crawlee | #1 | github.blog/engineering/infrastructure/glb-directo | 0.620 | github.blog/engineering/architecture-optimization/ | 0.550 | github.blog/news-insights/company-news/sha-1-colli | 0.526 |
| colly+md | #1 | github.blog/engineering/infrastructure/glb-directo | 0.620 | github.blog/engineering/architecture-optimization/ | 0.550 | github.blog/engineering/architecture-optimization/ | 0.507 |
| playwright | #1 | github.blog/news-insights/the-library/easy-peezy-c | 0.431 | github.blog/news-insights/the-library/deploying-wi | 0.430 | github.blog/news-insights/the-library/easy-peezy-c | 0.425 |


**Q5: What is GitHub's approach to platform security?** [conceptual]
*(expects URL containing: `platform-security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | github.blog/security/subresource-integrity/ | 0.658 | github.blog/latest/ | 0.655 | github.blog/latest/ | 0.635 |
| crawl4ai | #18 | github.blog/security/subresource-integrity/ | 0.676 | github.blog/latest/ | 0.656 | github.blog/latest/ | 0.643 |
| crawl4ai-raw | miss | github.blog/security/subresource-integrity/ | 0.676 | github.blog/latest/ | 0.656 | github.blog/latest/ | 0.643 |
| scrapy+md | #4 | github.blog/latest/ | 0.639 | github.blog/security/subresource-integrity/ | 0.633 | github.blog/latest/ | 0.621 |
| crawlee | miss | github.blog/latest/ | 0.639 | github.blog/security/subresource-integrity/ | 0.633 | github.blog/latest/ | 0.621 |
| colly+md | #19 | github.blog/latest/ | 0.639 | github.blog/security/subresource-integrity/ | 0.633 | github.blog/latest/ | 0.621 |
| playwright | #1 | github.blog/news-insights/the-library/services-gal | 0.358 | github.blog/news-insights/the-library/services-gal | 0.348 | github.blog/news-insights/the-library/services-gal | 0.335 |


**Q6: How does GitHub optimize its architecture?** [conceptual]
*(expects URL containing: `architecture-optimization`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | github.blog/engineering/infrastructure/glb-directo | 0.645 | github.blog/engineering/architecture-optimization/ | 0.644 | github.blog/engineering/infrastructure/evolution-o | 0.610 |
| crawl4ai | #1 | github.blog/engineering/architecture-optimization/ | 0.676 | github.blog/engineering/infrastructure/evolution-o | 0.660 | github.blog/engineering/architecture-optimization/ | 0.615 |
| crawl4ai-raw | #1 | github.blog/engineering/architecture-optimization/ | 0.676 | github.blog/engineering/infrastructure/evolution-o | 0.660 | github.blog/engineering/architecture-optimization/ | 0.615 |
| scrapy+md | #1 | github.blog/engineering/architecture-optimization/ | 0.622 | github.blog/engineering/infrastructure/evolution-o | 0.613 | github.blog/engineering/architecture-optimization/ | 0.574 |
| crawlee | #1 | github.blog/engineering/architecture-optimization/ | 0.622 | github.blog/engineering/infrastructure/evolution-o | 0.613 | github.blog/engineering/architecture-optimization/ | 0.574 |
| colly+md | #1 | github.blog/engineering/architecture-optimization/ | 0.622 | github.blog/engineering/infrastructure/evolution-o | 0.613 | github.blog/engineering/architecture-optimization/ | 0.574 |
| playwright | #1 | github.blog/news-insights/the-library/the-api/ | 0.412 | github.blog/news-insights/the-library/the-api/ | 0.392 | github.blog/news-insights/the-library/the-api/ | 0.390 |


**Q7: What engineering principles does GitHub follow?** [conceptual]
*(expects URL containing: `engineering-principles`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | github.blog/engineering/infrastructure/transit-and | 0.646 | github.blog/engineering/engineering-principles/scr | 0.629 | github.blog/news-insights/the-library/brubeck/ | 0.629 |
| crawl4ai | #1 | github.blog/engineering/engineering-principles/mov | 0.636 | github.blog/engineering/engineering-principles/scr | 0.631 | github.blog/engineering/infrastructure/evolution-o | 0.601 |
| crawl4ai-raw | #1 | github.blog/engineering/engineering-principles/mov | 0.636 | github.blog/engineering/engineering-principles/scr | 0.631 | github.blog/engineering/infrastructure/evolution-o | 0.601 |
| scrapy+md | #1 | github.blog/engineering/engineering-principles/mov | 0.670 | github.blog/engineering/engineering-principles/scr | 0.670 | github.blog/engineering/user-experience/topics/ | 0.586 |
| crawlee | #13 | github.blog/news-insights/company-news/gh-ost-gith | 0.585 | github.blog/news-insights/the-library/our-rubygem- | 0.585 | github.blog/news-insights/the-library/check-your-u | 0.585 |
| colly+md | #47 | github.blog/news-insights/the-library/github-free- | 0.586 | github.blog/news-insights/the-library/new-to-git/ | 0.586 | github.blog/news-insights/the-library/more-textmat | 0.586 |
| playwright | #1 | github.blog/news-insights/the-library/facebook-s-m | 0.323 | github.blog/news-insights/the-library/facebook-s-m | 0.317 | github.blog/news-insights/the-library/facebook-s-m | 0.316 |


**Q8: How does GitHub improve user experience?** [conceptual]
*(expects URL containing: `user-experience`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #30 | github.blog/news-insights/the-library/code-in-the- | 0.621 | github.blog/news-insights/the-library/local-github | 0.600 | github.blog/news-insights/the-library/cross-platfo | 0.598 |
| crawl4ai | miss | github.blog/news-insights/the-library/smooth-suppo | 0.625 | github.blog/news-insights/the-library/github-debug | 0.622 | github.blog/news-insights/the-library/code-in-the- | 0.611 |
| crawl4ai-raw | #48 | github.blog/news-insights/the-library/smooth-suppo | 0.625 | github.blog/news-insights/the-library/github-debug | 0.622 | github.blog/news-insights/the-library/code-in-the- | 0.611 |
| scrapy+md | #13 | github.blog/engineering/engineering-principles/scr | 0.596 | github.blog/news-insights/the-library/the-tree-sli | 0.596 | github.blog/engineering/infrastructure/kubernetes- | 0.596 |
| crawlee | miss | github.blog/news-insights/the-library/net-neutrali | 0.596 | github.blog/news-insights/the-library/http-cloning | 0.596 | github.blog/news-insights/the-library/smooth-suppo | 0.596 |
| colly+md | miss | github.blog/news-insights/the-library/janky/ | 0.596 | github.blog/news-insights/the-library/pushes/ | 0.596 | github.blog/latest/ | 0.596 |
| playwright | #1 | github.blog/engineering/infrastructure/building-re | 0.468 | github.blog/engineering/infrastructure/building-re | 0.461 | github.blog/engineering/infrastructure/building-re | 0.444 |


</details>

## Methodology

- **Queries:** 109 across 8 sites, categorized by type (api-function, code-example, conceptual, structured-data, factual-lookup, cross-page, navigation, js-rendered)
- **Embedding model:** `text-embedding-3-small` (1536 dimensions)
- **Chunking:** Markdown-aware, 400 word max, 50 word overlap
- **Retrieval modes:** Embedding (cosine), BM25 (Okapi), Hybrid (RRF k=60), Reranked (`cross-encoder/ms-marco-MiniLM-L-6-v2`)
- **Retrieval:** Hit rate reported at K = 1, 3, 5, 10, 20, plus MRR
- **Reranking:** Top-50 candidates from hybrid search, reranked to top-20
- **Chunk sensitivity:** Tested at ~256tok, ~512tok, ~1024tok
- **Confidence intervals:** Wilson score interval (95%)
- **Same chunking and embedding** for all tools — only extraction quality varies
- **No fine-tuning or tool-specific optimization** — identical pipeline for all

See [METHODOLOGY.md](METHODOLOGY.md) for full test setup, tool configurations,
and fairness decisions.

Retrieval similarity across tools is expected — the same URLs, chunking, and
embedding model are used. The real differentiator shows up in
[ANSWER_QUALITY.md](ANSWER_QUALITY.md), where the LLM's final answers diverge
despite similar retrieval.

