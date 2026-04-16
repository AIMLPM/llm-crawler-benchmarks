# Retrieval Quality Comparison
<!-- style: v2, 2026-04-15 -->

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
Summary tables use the **99-query common subset** (7 sites) so all tools are compared on identical queries. Sites excluded: wikipedia-python (not all tools have data). Per-site tables show full results.

## Quick summary: best retrieval mode per tool

For each tool, the mode with the highest MRR. Most readers can stop here.

| Tool | Best mode | Hit@10 | MRR |
|---|---|---|---|
| crawlee | embedding | 92% (91/99) ±5% | 0.733 |
| playwright | embedding | 92% (91/99) ±5% | 0.727 |
| **markcrawl** | embedding | 87% (86/99) ±7% | 0.698 |
| crawl4ai-raw | embedding | 91% (90/99) ±6% | 0.694 |
| crawl4ai | embedding | 91% (90/99) ±6% | 0.694 |
| colly+md | embedding | 85% (84/99) ±7% | 0.677 |
| scrapy+md | embedding | 63% (62/99) ±9% | 0.459 |

> **Column definitions:** **Best mode** = retrieval strategy that maximizes MRR for this tool. **Hit@10** = correct source page in top 10 results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged).

## Summary: retrieval modes compared

_Computed over 99 queries on 7 common sites (blog-engineering, books-toscrape, fastapi-docs, python-docs, quotes-toscrape, react-dev, stripe-docs)._

| Tool | Mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR |
|---|---|---|---|---|---|---|---|
| crawlee | embedding | 64% (63/99) ±9% | 81% (80/99) ±8% | 87% (86/99) ±7% | 92% (91/99) ±5% | 93% (92/99) ±5% | 0.733 |
| playwright | embedding | 63% (62/99) ±9% | 81% (80/99) ±8% | 86% (85/99) ±7% | 92% (91/99) ±5% | 93% (92/99) ±5% | 0.727 |
| **markcrawl** | embedding | 61% (60/99) ±9% | 77% (76/99) ±8% | 83% (82/99) ±7% | 87% (86/99) ±7% | 88% (87/99) ±6% | 0.698 |
| crawl4ai-raw | embedding | 60% (59/99) ±9% | 77% (76/99) ±8% | 83% (82/99) ±7% | 91% (90/99) ±6% | 92% (91/99) ±5% | 0.694 |
| crawl4ai | embedding | 60% (59/99) ±9% | 77% (76/99) ±8% | 82% (81/99) ±8% | 91% (90/99) ±6% | 92% (91/99) ±5% | 0.694 |
| colly+md | embedding | 62% (61/99) ±9% | 68% (67/99) ±9% | 77% (76/99) ±8% | 85% (84/99) ±7% | 88% (87/99) ±6% | 0.677 |
| scrapy+md | embedding | 38% (38/99) ±9% | 49% (49/99) ±10% | 56% (55/99) ±10% | 63% (62/99) ±9% | 65% (64/99) ±9% | 0.459 |
| colly+md | bm25 | 23% (23/99) ±8% | 36% (36/99) ±9% | 53% (52/99) ±10% | 64% (63/99) ±9% | 75% (74/99) ±8% | 0.349 |
| **markcrawl** | bm25 | 21% (21/99) ±8% | 38% (38/99) ±9% | 49% (49/99) ±10% | 62% (61/99) ±9% | 75% (74/99) ±8% | 0.336 |
| crawl4ai | bm25 | 21% (21/99) ±8% | 36% (36/99) ±9% | 46% (46/99) ±10% | 55% (54/99) ±10% | 73% (72/99) ±9% | 0.324 |
| playwright | bm25 | 16% (16/99) ±7% | 36% (36/99) ±9% | 55% (54/99) ±10% | 70% (69/99) ±9% | 81% (80/99) ±8% | 0.317 |
| crawl4ai-raw | bm25 | 20% (20/99) ±8% | 36% (36/99) ±9% | 45% (45/99) ±10% | 55% (54/99) ±10% | 74% (73/99) ±9% | 0.315 |
| crawlee | bm25 | 16% (16/99) ±7% | 36% (36/99) ±9% | 53% (52/99) ±10% | 69% (68/99) ±9% | 81% (80/99) ±8% | 0.313 |
| scrapy+md | bm25 | 12% (12/99) ±6% | 22% (22/99) ±8% | 30% (30/99) ±9% | 38% (38/99) ±9% | 54% (53/99) ±10% | 0.211 |
| crawl4ai | hybrid | 60% (59/99) ±9% | 73% (72/99) ±9% | 84% (83/99) ±7% | 89% (88/99) ±6% | 92% (91/99) ±5% | 0.687 |
| crawlee | hybrid | 58% (57/99) ±10% | 77% (76/99) ±8% | 80% (79/99) ±8% | 90% (89/99) ±6% | 93% (92/99) ±5% | 0.685 |
| playwright | hybrid | 58% (57/99) ±10% | 75% (74/99) ±8% | 79% (78/99) ±8% | 89% (88/99) ±6% | 93% (92/99) ±5% | 0.680 |
| crawl4ai-raw | hybrid | 58% (57/99) ±10% | 72% (71/99) ±9% | 82% (81/99) ±8% | 89% (88/99) ±6% | 92% (91/99) ±5% | 0.672 |
| **markcrawl** | hybrid | 52% (51/99) ±10% | 72% (71/99) ±9% | 78% (77/99) ±8% | 86% (85/99) ±7% | 88% (87/99) ±6% | 0.628 |
| colly+md | hybrid | 52% (51/99) ±10% | 65% (64/99) ±9% | 74% (73/99) ±9% | 85% (84/99) ±7% | 88% (87/99) ±6% | 0.611 |
| scrapy+md | hybrid | 32% (32/99) ±9% | 45% (45/99) ±10% | 54% (53/99) ±10% | 60% (59/99) ±9% | 63% (62/99) ±9% | 0.412 |
| crawlee | reranked | 57% (56/99) ±10% | 80% (79/99) ±8% | 89% (88/99) ±6% | 93% (92/99) ±5% | 94% (93/99) ±5% | 0.702 |
| playwright | reranked | 57% (56/99) ±10% | 80% (79/99) ±8% | 87% (86/99) ±7% | 93% (92/99) ±5% | 94% (93/99) ±5% | 0.699 |
| crawl4ai | reranked | 58% (57/99) ±10% | 74% (73/99) ±9% | 81% (80/99) ±8% | 89% (88/99) ±6% | 92% (91/99) ±5% | 0.680 |
| crawl4ai-raw | reranked | 58% (57/99) ±10% | 73% (72/99) ±9% | 82% (81/99) ±8% | 89% (88/99) ±6% | 92% (91/99) ±5% | 0.677 |
| colly+md | reranked | 54% (53/99) ±10% | 74% (73/99) ±9% | 81% (80/99) ±8% | 87% (86/99) ±7% | 88% (87/99) ±6% | 0.651 |
| **markcrawl** | reranked | 51% (50/99) ±10% | 79% (78/99) ±8% | 83% (82/99) ±7% | 88% (87/99) ±6% | 90% (89/99) ±6% | 0.651 |
| scrapy+md | reranked | 32% (32/99) ±9% | 52% (51/99) ±10% | 58% (57/99) ±10% | 62% (61/99) ±9% | 64% (63/99) ±9% | 0.432 |

> **Column definitions:** **Hit@K** = percentage of queries where the correct source page appeared in the top K results (shown as % with raw counts). **MRR** (Mean Reciprocal Rank) = average of 1/rank for correct results (1.0 = always rank 1, 0.5 = always rank 2). **Mode** = retrieval strategy used (see definitions above).

## Summary: embedding-only (hit rate at multiple K values)

_Computed over 99 queries on 7 common sites._

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Avg words |
|---|---|---|---|---|---|---|---|---|
| crawlee | 64% (63/99) ±9% | 81% (80/99) ±8% | 87% (86/99) ±7% | 92% (91/99) ±5% | 93% (92/99) ±5% | 0.733 | 74281 | 218 |
| playwright | 63% (62/99) ±9% | 81% (80/99) ±8% | 86% (85/99) ±7% | 92% (91/99) ±5% | 93% (92/99) ±5% | 0.727 | 73656 | 220 |
| **markcrawl** | 61% (60/99) ±9% | 77% (76/99) ±8% | 83% (82/99) ±7% | 87% (86/99) ±7% | 88% (87/99) ±6% | 0.698 | 27051 | 128 |
| crawl4ai-raw | 60% (59/99) ±9% | 77% (76/99) ±8% | 83% (82/99) ±7% | 91% (90/99) ±6% | 92% (91/99) ±5% | 0.694 | 51062 | 115 |
| crawl4ai | 60% (59/99) ±9% | 77% (76/99) ±8% | 82% (81/99) ±8% | 91% (90/99) ±6% | 92% (91/99) ±5% | 0.694 | 48332 | 116 |
| colly+md | 62% (61/99) ±9% | 68% (67/99) ±9% | 77% (76/99) ±8% | 85% (84/99) ±7% | 88% (87/99) ±6% | 0.677 | 80550 | 227 |
| scrapy+md | 38% (38/99) ±9% | 49% (49/99) ±10% | 56% (55/99) ±10% | 63% (62/99) ±9% | 65% (64/99) ±9% | 0.459 | 42234 | 139 |

> **Column definitions:** **Hit@K** = correct source page in top K results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). **Chunks** = total chunks produced by this tool (across all pages in common sites). **Avg words** = mean words per chunk.

## What this means

All tools perform within a narrow band (MRR 0.757-0.799 on embedding mode). This is expected: tools crawl similar pages from the same seed URLs, and we apply identical chunking and embedding pipelines. The extraction differences that matter for [content quality](QUALITY_COMPARISON.md) largely wash out at retrieval time.

**Retrieval mode matters more than crawler choice.** Embedding search beats BM25 by roughly 2x on MRR across all tools. Hybrid and reranked modes fall between the two. Choosing the right retrieval strategy will improve your RAG pipeline far more than switching crawlers.

**The noise-vs-recall trade-off.** Noisier tools (crawlee, playwright) have slightly higher hit rates, but they produce 2x the chunks of leaner tools (markcrawl, scrapy+md). More chunks means higher embedding and storage costs with diminishing retrieval returns. See [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar impact.

**For most use cases, pick your crawler based on speed and cost, not retrieval quality.** The differences here are within confidence intervals. Where crawler choice _does_ matter is content quality and downstream answer quality -- see [ANSWER_QUALITY.md](ANSWER_QUALITY.md).

## Per-category breakdown (embedding mode)

Query categories reveal where crawlers actually differ. Categories like `js-rendered` and `structured-data` stress-test browser rendering and table extraction, while `api-function` and `conceptual` queries test basic content retrieval.

| Category | Tool | Hit@10 | MRR | Queries |
|---|---|---|---|---|
| api-function | **markcrawl** | 97% (36/37) | 0.678 | 37 |
| api-function | crawlee | 95% (35/37) | 0.752 | 37 |
| api-function | playwright | 95% (35/37) | 0.737 | 37 |
| api-function | colly+md | 95% (35/37) | 0.722 | 37 |
| api-function | crawl4ai | 92% (34/37) | 0.699 | 37 |
| api-function | crawl4ai-raw | 89% (33/37) | 0.699 | 37 |
| api-function | scrapy+md | 76% (28/37) | 0.476 | 37 |
| code-example | **markcrawl** | 100% (11/11) | 0.742 | 11 |
| code-example | crawl4ai | 100% (11/11) | 0.690 | 11 |
| code-example | crawl4ai-raw | 100% (11/11) | 0.690 | 11 |
| code-example | crawlee | 100% (11/11) | 0.680 | 11 |
| code-example | playwright | 100% (11/11) | 0.680 | 11 |
| code-example | scrapy+md | 100% (11/11) | 0.668 | 11 |
| code-example | colly+md | 100% (11/11) | 0.634 | 11 |
| conceptual | crawlee | 100% (22/22) | 0.753 | 22 |
| conceptual | playwright | 100% (22/22) | 0.753 | 22 |
| conceptual | crawl4ai-raw | 100% (22/22) | 0.722 | 22 |
| conceptual | crawl4ai | 100% (22/22) | 0.720 | 22 |
| conceptual | colly+md | 91% (20/22) | 0.707 | 22 |
| conceptual | **markcrawl** | 86% (19/22) | 0.593 | 22 |
| conceptual | scrapy+md | 77% (17/22) | 0.596 | 22 |
| cross-page | crawl4ai | 60% (3/5) | 0.600 | 5 |
| cross-page | crawl4ai-raw | 60% (3/5) | 0.600 | 5 |
| cross-page | crawlee | 60% (3/5) | 0.600 | 5 |
| cross-page | colly+md | 60% (3/5) | 0.600 | 5 |
| cross-page | playwright | 60% (3/5) | 0.600 | 5 |
| cross-page | **markcrawl** | 40% (2/5) | 0.400 | 5 |
| cross-page | scrapy+md | 20% (1/5) | 0.100 | 5 |
| factual-lookup | **markcrawl** | 90% (9/10) | 0.783 | 10 |
| factual-lookup | crawlee | 80% (8/10) | 0.642 | 10 |
| factual-lookup | playwright | 80% (8/10) | 0.642 | 10 |
| factual-lookup | crawl4ai | 80% (8/10) | 0.633 | 10 |
| factual-lookup | crawl4ai-raw | 80% (8/10) | 0.633 | 10 |
| factual-lookup | colly+md | 40% (4/10) | 0.400 | 10 |
| factual-lookup | scrapy+md | 40% (4/10) | 0.333 | 10 |
| js-rendered | **markcrawl** | 100% (5/5) | 1.000 | 5 |
| js-rendered | crawl4ai | 100% (5/5) | 0.573 | 5 |
| js-rendered | crawl4ai-raw | 100% (5/5) | 0.573 | 5 |
| js-rendered | crawlee | 100% (5/5) | 0.450 | 5 |
| js-rendered | playwright | 100% (5/5) | 0.450 | 5 |
| js-rendered | colly+md | 100% (5/5) | 0.351 | 5 |
| js-rendered | scrapy+md | 80% (4/5) | 0.500 | 5 |
| navigation | **markcrawl** | 100% (1/1) | 1.000 | 1 |
| navigation | crawlee | 100% (1/1) | 1.000 | 1 |
| navigation | colly+md | 100% (1/1) | 1.000 | 1 |
| navigation | playwright | 100% (1/1) | 1.000 | 1 |
| navigation | crawl4ai | 100% (1/1) | 0.333 | 1 |
| navigation | crawl4ai-raw | 100% (1/1) | 0.333 | 1 |
| navigation | scrapy+md | 0% (0/1) | 0.000 | 1 |
| structured-data | crawlee | 100% (8/8) | 1.000 | 8 |
| structured-data | colly+md | 100% (8/8) | 1.000 | 8 |
| structured-data | playwright | 100% (8/8) | 1.000 | 8 |
| structured-data | crawl4ai | 100% (8/8) | 0.854 | 8 |
| structured-data | crawl4ai-raw | 100% (8/8) | 0.854 | 8 |
| structured-data | **markcrawl** | 88% (7/8) | 0.875 | 8 |
| structured-data | scrapy+md | 12% (1/8) | 0.125 | 8 |


### Best tool per category

| Category | Best tool | Hit@10 | Spread |
|---|---|---|---|
| api-function | **markcrawl** | 97% | 22% |
| code-example | **markcrawl** | 100% | 0% |
| conceptual | crawl4ai | 100% | 23% |
| cross-page | crawl4ai | 60% | 40% |
| factual-lookup | **markcrawl** | 90% | 50% |
| js-rendered | **markcrawl** | 100% | 20% |
| navigation | **markcrawl** | 100% | 100% |
| structured-data | crawl4ai | 100% | 88% |

_Spread = difference between best and worst tool. High spread categories are where crawler choice matters most._


## quotes-toscrape

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 0.500 | 25 | 15 |
| crawl4ai-raw | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 0.500 | 25 | 15 |
| crawlee | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 0.500 | 33 | 15 |
| colly+md | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 0.500 | 33 | 15 |
| playwright | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 0.500 | 33 | 15 |
| **markcrawl** | 38% (3/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 0.417 | 20 | 15 |
| scrapy+md | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.062 | 22 | 15 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for quotes-toscrape</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What did Albert Einstein say about thinking and the world?** [factual-lookup]
*(expects URL containing: `author/Albert-Einstein`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | quotes.toscrape.com/tag/world/page/1/ | 0.667 | quotes.toscrape.com/tag/thinking/page/1/ | 0.646 | quotes.toscrape.com/author/Albert-Einstein | 0.568 |
| crawl4ai | #1 | quotes.toscrape.com/author/Albert-Einstein | 0.581 | quotes.toscrape.com/author/Albert-Einstein | 0.555 | quotes.toscrape.com/tag/world/page/1/ | 0.482 |
| crawl4ai-raw | #1 | quotes.toscrape.com/author/Albert-Einstein | 0.581 | quotes.toscrape.com/author/Albert-Einstein | 0.555 | quotes.toscrape.com/tag/world/page/1/ | 0.482 |
| scrapy+md | miss | quotes.toscrape.com/tag/life/ | 0.384 | quotes.toscrape.com | 0.367 | quotes.toscrape.com/tag/life/ | 0.331 |
| crawlee | #1 | quotes.toscrape.com/author/Albert-Einstein | 0.568 | quotes.toscrape.com/author/Albert-Einstein | 0.549 | quotes.toscrape.com/author/Albert-Einstein | 0.487 |
| colly+md | #1 | quotes.toscrape.com/author/Albert-Einstein/ | 0.568 | quotes.toscrape.com/author/Albert-Einstein/ | 0.549 | quotes.toscrape.com/author/Albert-Einstein/ | 0.487 |
| playwright | #1 | quotes.toscrape.com/author/Albert-Einstein | 0.568 | quotes.toscrape.com/author/Albert-Einstein | 0.549 | quotes.toscrape.com/author/Albert-Einstein | 0.487 |


**Q2: Which quotes are tagged with 'change'?** [cross-page]
*(expects URL containing: `tag/change`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | quotes.toscrape.com/tag/thinking/page/1/ | 0.478 | quotes.toscrape.com/tag/world/page/1/ | 0.456 | quotes.toscrape.com/tag/life/ | 0.440 |
| crawl4ai | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.626 | quotes.toscrape.com/tag/world/page/1/ | 0.542 | quotes.toscrape.com/tag/thinking/page/1/ | 0.528 |
| crawl4ai-raw | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.626 | quotes.toscrape.com/tag/world/page/1/ | 0.542 | quotes.toscrape.com/tag/thinking/page/1/ | 0.528 |
| scrapy+md | miss | quotes.toscrape.com | 0.481 | quotes.toscrape.com/tag/grown-ups/page/1/ | 0.448 | quotes.toscrape.com/tag/truth/ | 0.443 |
| crawlee | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.565 | quotes.toscrape.com/tag/world/page/1/ | 0.516 | quotes.toscrape.com/tag/thinking/page/1/ | 0.511 |
| colly+md | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.565 | quotes.toscrape.com/tag/world/page/1/ | 0.516 | quotes.toscrape.com/tag/thinking/page/1/ | 0.511 |
| playwright | #1 | quotes.toscrape.com/tag/change/page/1/ | 0.565 | quotes.toscrape.com/tag/world/page/1/ | 0.516 | quotes.toscrape.com/tag/thinking/page/1/ | 0.511 |


**Q3: What did Steve Martin say about sunshine?** [factual-lookup]
*(expects URL containing: `author/Steve-Martin`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/author/Steve-Martin | 0.573 | quotes.toscrape.com/ | 0.411 | quotes.toscrape.com/tag/humor/ | 0.392 |
| crawl4ai | miss | quotes.toscrape.com/tag/life/page/1/ | 0.289 | quotes.toscrape.com/tag/live/page/1/ | 0.284 | quotes.toscrape.com | 0.280 |
| crawl4ai-raw | miss | quotes.toscrape.com/tag/life/page/1/ | 0.289 | quotes.toscrape.com/tag/live/page/1/ | 0.284 | quotes.toscrape.com | 0.280 |
| scrapy+md | miss | quotes.toscrape.com/tag/simile/ | 0.314 | quotes.toscrape.com/tag/humor/ | 0.294 | quotes.toscrape.com | 0.284 |
| crawlee | miss | quotes.toscrape.com | 0.284 | quotes.toscrape.com/tag/life/page/1/ | 0.280 | quotes.toscrape.com/author/Albert-Einstein | 0.260 |
| colly+md | miss | quotes.toscrape.com | 0.284 | quotes.toscrape.com/tag/life/page/1/ | 0.280 | quotes.toscrape.com/author/Albert-Einstein/ | 0.260 |
| playwright | miss | quotes.toscrape.com | 0.284 | quotes.toscrape.com/ | 0.284 | quotes.toscrape.com/tag/life/page/1/ | 0.280 |


**Q4: What quotes are about thinking deeply?** [cross-page]
*(expects URL containing: `tag/thinking`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.539 | quotes.toscrape.com/ | 0.510 | quotes.toscrape.com/tag/inspirational/ | 0.495 |
| crawl4ai | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.594 | quotes.toscrape.com/tag/deep-thoughts/page/1/ | 0.593 | quotes.toscrape.com/tag/change/page/1/ | 0.544 |
| crawl4ai-raw | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.594 | quotes.toscrape.com/tag/deep-thoughts/page/1/ | 0.593 | quotes.toscrape.com/tag/change/page/1/ | 0.544 |
| scrapy+md | miss | quotes.toscrape.com | 0.490 | quotes.toscrape.com/tag/humor/ | 0.450 | quotes.toscrape.com/tag/life/ | 0.437 |
| crawlee | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.531 | quotes.toscrape.com/tag/deep-thoughts/page/1/ | 0.528 | quotes.toscrape.com/tag/change/page/1/ | 0.494 |
| colly+md | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.531 | quotes.toscrape.com/tag/deep-thoughts/page/1/ | 0.528 | quotes.toscrape.com/tag/change/page/1/ | 0.494 |
| playwright | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.531 | quotes.toscrape.com/tag/deep-thoughts/page/1/ | 0.528 | quotes.toscrape.com/tag/change/page/1/ | 0.494 |


**Q5: What did Eleanor Roosevelt say about life?** [factual-lookup]
*(expects URL containing: `author/Eleanor-Roosevelt`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | quotes.toscrape.com/tag/life/ | 0.507 | quotes.toscrape.com/tag/life/ | 0.506 | quotes.toscrape.com/ | 0.459 |
| crawl4ai | miss | quotes.toscrape.com/tag/life/page/1/ | 0.477 | quotes.toscrape.com/tag/life/page/1/ | 0.469 | quotes.toscrape.com/tag/inspirational/page/1/ | 0.436 |
| crawl4ai-raw | miss | quotes.toscrape.com/tag/life/page/1/ | 0.477 | quotes.toscrape.com/tag/life/page/1/ | 0.469 | quotes.toscrape.com/tag/inspirational/page/1/ | 0.436 |
| scrapy+md | miss | quotes.toscrape.com/tag/life/ | 0.479 | quotes.toscrape.com/tag/life/ | 0.478 | quotes.toscrape.com | 0.367 |
| crawlee | miss | quotes.toscrape.com/tag/life/page/1/ | 0.479 | quotes.toscrape.com/tag/life/page/1/ | 0.478 | quotes.toscrape.com/tag/inspirational/page/1/ | 0.447 |
| colly+md | miss | quotes.toscrape.com/tag/life/page/1/ | 0.479 | quotes.toscrape.com/tag/life/page/1/ | 0.478 | quotes.toscrape.com/tag/inspirational/page/1/ | 0.447 |
| playwright | miss | quotes.toscrape.com/tag/life/page/1/ | 0.479 | quotes.toscrape.com/tag/life/page/1/ | 0.477 | quotes.toscrape.com/tag/inspirational/page/1/ | 0.447 |


**Q6: Which quotes are tagged about choices and abilities?** [cross-page]
*(expects URL containing: `tag/abilities`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | quotes.toscrape.com/tag/life/ | 0.502 | quotes.toscrape.com/tag/inspirational/ | 0.482 | quotes.toscrape.com/tag/thinking/page/1/ | 0.466 |
| crawl4ai | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.679 | quotes.toscrape.com/tag/choices/page/1/ | 0.667 | quotes.toscrape.com | 0.491 |
| crawl4ai-raw | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.679 | quotes.toscrape.com/tag/choices/page/1/ | 0.667 | quotes.toscrape.com | 0.491 |
| scrapy+md | miss | quotes.toscrape.com | 0.490 | quotes.toscrape.com/tag/life/ | 0.478 | quotes.toscrape.com/tag/life/ | 0.463 |
| crawlee | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.587 | quotes.toscrape.com/tag/choices/page/1/ | 0.580 | quotes.toscrape.com | 0.493 |
| colly+md | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.587 | quotes.toscrape.com/tag/choices/page/1/ | 0.580 | quotes.toscrape.com | 0.493 |
| playwright | #1 | quotes.toscrape.com/tag/abilities/page/1/ | 0.587 | quotes.toscrape.com/tag/choices/page/1/ | 0.580 | quotes.toscrape.com | 0.493 |


**Q7: What quotes are about friendship?** [cross-page]
*(expects URL containing: `tag/friendship`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | quotes.toscrape.com/tag/life/ | 0.481 | quotes.toscrape.com/ | 0.467 | quotes.toscrape.com/tag/inspirational/ | 0.458 |
| crawl4ai | miss | quotes.toscrape.com | 0.469 | quotes.toscrape.com/ | 0.468 | quotes.toscrape.com/tag/world/page/1/ | 0.458 |
| crawl4ai-raw | miss | quotes.toscrape.com | 0.469 | quotes.toscrape.com/ | 0.468 | quotes.toscrape.com/tag/world/page/1/ | 0.458 |
| scrapy+md | #2 | quotes.toscrape.com/tag/friends/ | 0.554 | quotes.toscrape.com/tag/friendship/ | 0.552 | quotes.toscrape.com/tag/books/ | 0.468 |
| crawlee | miss | quotes.toscrape.com | 0.476 | quotes.toscrape.com/tag/life/page/1/ | 0.466 | quotes.toscrape.com/tag/thinking/page/1/ | 0.444 |
| colly+md | miss | quotes.toscrape.com | 0.476 | quotes.toscrape.com/tag/life/page/1/ | 0.466 | quotes.toscrape.com/tag/thinking/page/1/ | 0.444 |
| playwright | miss | quotes.toscrape.com | 0.476 | quotes.toscrape.com/ | 0.476 | quotes.toscrape.com/tag/life/page/1/ | 0.466 |


**Q8: What are the quotes about love?** [cross-page]
*(expects URL containing: `tag/love`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/tag/love/ | 0.586 | quotes.toscrape.com/tag/love/ | 0.574 | quotes.toscrape.com/tag/inspirational/ | 0.486 |
| crawl4ai | miss | quotes.toscrape.com | 0.478 | quotes.toscrape.com/tag/world/page/1/ | 0.477 | quotes.toscrape.com/ | 0.477 |
| crawl4ai-raw | miss | quotes.toscrape.com | 0.478 | quotes.toscrape.com/tag/world/page/1/ | 0.477 | quotes.toscrape.com/ | 0.477 |
| scrapy+md | miss | quotes.toscrape.com/tag/friendship/ | 0.525 | quotes.toscrape.com/tag/friends/ | 0.495 | quotes.toscrape.com/tag/romance/page/1/ | 0.480 |
| crawlee | miss | quotes.toscrape.com | 0.493 | quotes.toscrape.com/tag/thinking/page/1/ | 0.488 | quotes.toscrape.com/tag/world/page/1/ | 0.487 |
| colly+md | miss | quotes.toscrape.com | 0.493 | quotes.toscrape.com/tag/thinking/page/1/ | 0.488 | quotes.toscrape.com/tag/world/page/1/ | 0.487 |
| playwright | miss | quotes.toscrape.com | 0.493 | quotes.toscrape.com/ | 0.493 | quotes.toscrape.com/tag/thinking/page/1/ | 0.488 |


</details>

## books-toscrape

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 1.000 | 113 | 60 |
| colly+md | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 1.000 | 107 | 60 |
| playwright | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 1.000 | 107 | 60 |
| **markcrawl** | 90% (9/10) | 90% (9/10) | 90% (9/10) | 90% (9/10) | 90% (9/10) | 0.900 | 144 | 60 |
| crawl4ai | 70% (7/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 0.817 | 655 | 60 |
| crawl4ai-raw | 70% (7/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 0.817 | 655 | 60 |
| scrapy+md | 10% (1/10) | 10% (1/10) | 10% (1/10) | 10% (1/10) | 10% (1/10) | 0.100 | 248 | 60 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for books-toscrape</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What mystery and thriller books are in the catalog?** [structured-data]
*(expects URL containing: `category/books/mystery`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/myster | 0.495 | books.toscrape.com/catalogue/category/books/myster | 0.467 | books.toscrape.com/catalogue/shakespeares-sonnets_ | 0.458 |
| crawl4ai | #3 | books.toscrape.com/catalogue/category/books/suspen | 0.538 | books.toscrape.com/catalogue/category/books/thrill | 0.520 | books.toscrape.com/catalogue/category/books/myster | 0.513 |
| crawl4ai-raw | #3 | books.toscrape.com/catalogue/category/books/suspen | 0.538 | books.toscrape.com/catalogue/category/books/thrill | 0.520 | books.toscrape.com/catalogue/category/books/myster | 0.513 |
| scrapy+md | miss | books.toscrape.com | 0.479 | books.toscrape.com/catalogue/code-name-verity-code | 0.441 | books.toscrape.com/catalogue/cell_674/index.html | 0.439 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/myster | 0.514 | books.toscrape.com/catalogue/category/books/myster | 0.495 | books.toscrape.com/catalogue/category/books/thrill | 0.483 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/myster | 0.514 | books.toscrape.com/catalogue/category/books/myster | 0.495 | books.toscrape.com/catalogue/category/books/thrill | 0.483 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/myster | 0.514 | books.toscrape.com/catalogue/category/books/myster | 0.495 | books.toscrape.com/catalogue/category/books/thrill | 0.483 |


**Q2: What science fiction books are available?** [structured-data]
*(expects URL containing: `category/books/science-fiction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.460 | books.toscrape.com/catalogue/mesaerion-the-best-sc | 0.447 | books.toscrape.com/catalogue/mesaerion-the-best-sc | 0.441 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.533 | books.toscrape.com/catalogue/category/books/scienc | 0.471 | books.toscrape.com/catalogue/category/books_1/inde | 0.461 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.533 | books.toscrape.com/catalogue/category/books/scienc | 0.471 | books.toscrape.com/catalogue/category/books_1/inde | 0.461 |
| scrapy+md | #1 | books.toscrape.com/catalogue/mesaerion-the-best-sc | 0.441 | books.toscrape.com/catalogue/mesaerion-the-best-sc | 0.418 | books.toscrape.com/catalogue/libertarianism-for-be | 0.404 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.510 | books.toscrape.com/catalogue/category/books/scienc | 0.466 | books.toscrape.com/catalogue/category/books/scienc | 0.402 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.510 | books.toscrape.com/catalogue/category/books/scienc | 0.466 | books.toscrape.com/catalogue/category/books/scienc | 0.402 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.510 | books.toscrape.com/catalogue/category/books/scienc | 0.466 | books.toscrape.com/catalogue/category/books/scienc | 0.402 |


**Q3: What is the book Sharp Objects about?** [factual-lookup]
*(expects URL containing: `sharp-objects`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.606 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.574 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.485 |
| crawl4ai | #3 | books.toscrape.com/catalogue/the-dirty-little-secr | 0.648 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.648 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.607 |
| crawl4ai-raw | #3 | books.toscrape.com/catalogue/the-dirty-little-secr | 0.648 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.648 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.607 |
| scrapy+md | miss | books.toscrape.com/catalogue/girl-in-the-blue-coat | 0.368 | books.toscrape.com/catalogue/the-elephant-tree_968 | 0.365 | books.toscrape.com/catalogue/the-invention-of-wing | 0.360 |
| crawlee | #1 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.606 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.533 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.481 |
| colly+md | #1 | books.toscrape.com/catalogue/sharp-objects/997/ind | 0.606 | books.toscrape.com/catalogue/sharp-objects/997/ind | 0.533 | books.toscrape.com/catalogue/sharp-objects/997/ind | 0.481 |
| playwright | #1 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.606 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.533 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.481 |


**Q4: What biography books are in the catalog?** [structured-data]
*(expects URL containing: `category/books/biography`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.414 | books.toscrape.com/catalogue/category/books/autobi | 0.405 | books.toscrape.com/catalogue/set-me-free_988/index | 0.402 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.449 | books.toscrape.com/catalogue/category/books/autobi | 0.441 | books.toscrape.com/catalogue/category/books/histor | 0.435 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.449 | books.toscrape.com/catalogue/category/books/autobi | 0.441 | books.toscrape.com/catalogue/category/books/histor | 0.435 |
| scrapy+md | miss | books.toscrape.com | 0.419 | books.toscrape.com/catalogue/behind-closed-doors_9 | 0.380 | books.toscrape.com/catalogue/a-brush-of-wings-ange | 0.380 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.419 | books.toscrape.com | 0.416 | books.toscrape.com/index.html | 0.416 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.419 | books.toscrape.com/index.html | 0.416 | books.toscrape.com | 0.416 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/biogra | 0.419 | books.toscrape.com | 0.416 | books.toscrape.com/index.html | 0.416 |


**Q5: What horror books are in the catalog?** [structured-data]
*(expects URL containing: `category/books/horror`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/horror | 0.543 | books.toscrape.com/catalogue/category/books/young- | 0.419 | books.toscrape.com/catalogue/category/books/myster | 0.409 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/horror | 0.492 | books.toscrape.com/catalogue/category/books/suspen | 0.489 | books.toscrape.com/catalogue/category/books/horror | 0.484 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/horror | 0.492 | books.toscrape.com/catalogue/category/books/suspen | 0.489 | books.toscrape.com/catalogue/category/books/horror | 0.484 |
| scrapy+md | miss | books.toscrape.com | 0.463 | books.toscrape.com/catalogue/in-a-dark-dark-wood_9 | 0.433 | books.toscrape.com/catalogue/page-3.html | 0.419 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/horror | 0.515 | books.toscrape.com/catalogue/category/books/horror | 0.511 | books.toscrape.com | 0.468 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/horror | 0.515 | books.toscrape.com/catalogue/category/books/horror | 0.511 | books.toscrape.com | 0.468 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/horror | 0.515 | books.toscrape.com/catalogue/category/books/horror | 0.511 | books.toscrape.com | 0.468 |


**Q6: What poetry books can I find?** [structured-data]
*(expects URL containing: `category/books/poetry`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.552 | books.toscrape.com/catalogue/a-light-in-the-attic_ | 0.387 | books.toscrape.com/catalogue/set-me-free_988/index | 0.385 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.498 | books.toscrape.com/catalogue/category/books/poetry | 0.487 | books.toscrape.com/catalogue/category/books/poetry | 0.484 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.498 | books.toscrape.com/catalogue/category/books/poetry | 0.487 | books.toscrape.com/catalogue/category/books/poetry | 0.484 |
| scrapy+md | miss | books.toscrape.com/catalogue/you-cant-bury-them-al | 0.424 | books.toscrape.com/catalogue/you-cant-bury-them-al | 0.412 | books.toscrape.com/catalogue/shakespeares-sonnets_ | 0.401 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.545 | books.toscrape.com/catalogue/category/books/poetry | 0.472 | books.toscrape.com/catalogue/a-light-in-the-attic_ | 0.413 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.545 | books.toscrape.com/catalogue/category/books/poetry | 0.472 | books.toscrape.com/catalogue/a-light-in-the-attic/ | 0.413 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.545 | books.toscrape.com/catalogue/category/books/poetry | 0.472 | books.toscrape.com/catalogue/a-light-in-the-attic_ | 0.413 |


**Q7: What fantasy books are in the bookstore?** [structured-data]
*(expects URL containing: `category/books/fantasy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.502 | books.toscrape.com/catalogue/category/books/fantas | 0.483 | books.toscrape.com/catalogue/category/books/scienc | 0.415 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.447 | books.toscrape.com/catalogue/category/books/fantas | 0.433 | books.toscrape.com/catalogue/category/books/fantas | 0.432 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.447 | books.toscrape.com/catalogue/category/books/fantas | 0.433 | books.toscrape.com/catalogue/category/books/fantas | 0.432 |
| scrapy+md | miss | books.toscrape.com/catalogue/code-name-verity-code | 0.398 | books.toscrape.com/catalogue/the-last-painting-of- | 0.377 | books.toscrape.com/catalogue/the-guernsey-literary | 0.376 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.487 | books.toscrape.com/catalogue/category/books/fantas | 0.483 | books.toscrape.com/catalogue/category/books/fantas | 0.427 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.487 | books.toscrape.com/catalogue/category/books/fantas | 0.483 | books.toscrape.com/catalogue/category/books/fantas | 0.427 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.487 | books.toscrape.com/catalogue/category/books/fantas | 0.483 | books.toscrape.com/catalogue/category/books/fantas | 0.427 |


**Q8: What philosophy books are available to read?** [structured-data]
*(expects URL containing: `category/books/philosophy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | books.toscrape.com/catalogue/category/books/psycho | 0.375 | books.toscrape.com/catalogue/its-only-the-himalaya | 0.374 | books.toscrape.com/catalogue/category/books/nonfic | 0.366 |
| crawl4ai | #1 | books.toscrape.com/catalogue/category/books/philos | 0.454 | books.toscrape.com/catalogue/category/books/philos | 0.430 | books.toscrape.com/catalogue/category/books/philos | 0.425 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/category/books/philos | 0.454 | books.toscrape.com/catalogue/category/books/philos | 0.430 | books.toscrape.com/catalogue/category/books/philos | 0.425 |
| scrapy+md | miss | books.toscrape.com/catalogue/sophies-world_966/ind | 0.383 | books.toscrape.com/catalogue/sophies-world_966/ind | 0.376 | books.toscrape.com/catalogue/under-the-tuscan-sun_ | 0.366 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/philos | 0.449 | books.toscrape.com/catalogue/category/books/psycho | 0.380 | books.toscrape.com/catalogue/category/books/spirit | 0.362 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/philos | 0.449 | books.toscrape.com/catalogue/category/books/psycho | 0.380 | books.toscrape.com/catalogue/category/books/spirit | 0.362 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/philos | 0.449 | books.toscrape.com/catalogue/category/books/psycho | 0.380 | books.toscrape.com/catalogue/category/books/spirit | 0.362 |


**Q9: What is the book Sapiens about?** [factual-lookup]
*(expects URL containing: `sapiens`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.623 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.621 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.538 |
| crawl4ai | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.630 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.583 | books.toscrape.com/catalogue/the-dirty-little-secr | 0.578 |
| crawl4ai-raw | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.630 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.583 | books.toscrape.com/catalogue/the-dirty-little-secr | 0.578 |
| scrapy+md | miss | books.toscrape.com/catalogue/sophies-world_966/ind | 0.326 | books.toscrape.com/catalogue/the-genius-of-birds_8 | 0.324 | books.toscrape.com/catalogue/the-genius-of-birds_8 | 0.280 |
| crawlee | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.621 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.564 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.542 |
| colly+md | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.621 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.564 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.542 |
| playwright | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.621 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.564 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.542 |


**Q10: What romance novels are available?** [structured-data]
*(expects URL containing: `category/books/romance`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/romanc | 0.488 | books.toscrape.com/catalogue/category/books/romanc | 0.468 | books.toscrape.com/catalogue/category/books/new-ad | 0.419 |
| crawl4ai | #2 | books.toscrape.com/catalogue/category/books/add-a- | 0.545 | books.toscrape.com/catalogue/category/books/romanc | 0.520 | books.toscrape.com/catalogue/category/books/womens | 0.477 |
| crawl4ai-raw | #2 | books.toscrape.com/catalogue/category/books/add-a- | 0.545 | books.toscrape.com/catalogue/category/books/romanc | 0.520 | books.toscrape.com/catalogue/category/books/womens | 0.477 |
| scrapy+md | miss | books.toscrape.com | 0.415 | books.toscrape.com/catalogue/code-name-verity-code | 0.406 | books.toscrape.com/catalogue/page-3.html | 0.401 |
| crawlee | #1 | books.toscrape.com/catalogue/category/books/romanc | 0.493 | books.toscrape.com/catalogue/category/books/romanc | 0.488 | books.toscrape.com/catalogue/category/books/womens | 0.457 |
| colly+md | #1 | books.toscrape.com/catalogue/category/books/romanc | 0.493 | books.toscrape.com/catalogue/category/books/romanc | 0.488 | books.toscrape.com/catalogue/category/books/womens | 0.457 |
| playwright | #1 | books.toscrape.com/catalogue/category/books/romanc | 0.493 | books.toscrape.com/catalogue/category/books/romanc | 0.488 | books.toscrape.com/catalogue/category/books/womens | 0.457 |


</details>

## fastapi-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 75% (15/20) | 80% (16/20) | 80% (16/20) | 100% (20/20) | 100% (20/20) | 0.804 | 14215 | 500 |
| crawl4ai-raw | 75% (15/20) | 80% (16/20) | 80% (16/20) | 100% (20/20) | 100% (20/20) | 0.804 | 14207 | 500 |
| crawlee | 70% (14/20) | 85% (17/20) | 90% (18/20) | 100% (20/20) | 100% (20/20) | 0.800 | 13334 | 502 |
| playwright | 70% (14/20) | 85% (17/20) | 90% (18/20) | 100% (20/20) | 100% (20/20) | 0.800 | 13372 | 500 |
| **markcrawl** | 70% (14/20) | 80% (16/20) | 90% (18/20) | 100% (20/20) | 100% (20/20) | 0.770 | 9487 | 500 |
| scrapy+md | 65% (13/20) | 65% (13/20) | 85% (17/20) | 100% (20/20) | 100% (20/20) | 0.720 | 11790 | 495 |
| colly+md | 65% (13/20) | 65% (13/20) | 85% (17/20) | 95% (19/20) | 100% (20/20) | 0.717 | 14136 | 500 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for fastapi-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I add authentication to a FastAPI endpoint?** [api-function]
*(expects URL containing: `security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.600 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.594 | fastapi.tiangolo.com/tutorial/security/ | 0.565 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.631 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.599 | fastapi.tiangolo.com/tutorial/security/ | 0.593 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.631 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.598 | fastapi.tiangolo.com/tutorial/security/ | 0.593 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.600 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.594 | fastapi.tiangolo.com/de/advanced/json-base64-bytes | 0.550 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.604 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.591 | fastapi.tiangolo.com/tutorial/security/ | 0.568 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.600 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.594 | fastapi.tiangolo.com/de/advanced/json-base64-bytes | 0.550 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.604 | fastapi.tiangolo.com/tutorial/security/simple-oaut | 0.591 | fastapi.tiangolo.com/tutorial/security/ | 0.568 |


**Q2: How do I define query parameters in the FastAPI reference?** [api-function]
*(expects URL containing: `reference/fastapi`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #8 | fastapi.tiangolo.com/tutorial/query-params/ | 0.662 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.657 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.636 |
| crawl4ai | #1 | fastapi.tiangolo.com/es/reference/parameters/ | 0.673 | fastapi.tiangolo.com/de/reference/parameters/ | 0.672 | fastapi.tiangolo.com/reference/parameters/ | 0.671 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/es/reference/parameters/ | 0.673 | fastapi.tiangolo.com/de/reference/parameters/ | 0.672 | fastapi.tiangolo.com/reference/parameters/ | 0.671 |
| scrapy+md | #7 | fastapi.tiangolo.com/tutorial/query-params/ | 0.662 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.636 | fastapi.tiangolo.com/tutorial/query-params/ | 0.617 |
| crawlee | #2 | fastapi.tiangolo.com/tutorial/query-params/ | 0.649 | fastapi.tiangolo.com/de/reference/parameters/ | 0.646 | fastapi.tiangolo.com/reference/parameters/ | 0.642 |
| colly+md | #12 | fastapi.tiangolo.com/tutorial/query-params/ | 0.662 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.636 | fastapi.tiangolo.com/tutorial/query-params/ | 0.635 |
| playwright | #2 | fastapi.tiangolo.com/tutorial/query-params/ | 0.649 | fastapi.tiangolo.com/de/reference/parameters/ | 0.646 | fastapi.tiangolo.com/reference/parameters/ | 0.642 |


**Q3: How does FastAPI handle JSON encoding and base64 bytes?** [code-example]
*(expects URL containing: `json-base64-bytes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.609 | fastapi.tiangolo.com/zh/advanced/json-base64-bytes | 0.590 | fastapi.tiangolo.com/zh/advanced/json-base64-bytes | 0.582 |
| crawl4ai | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.654 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.645 | fastapi.tiangolo.com/reference/encoders/ | 0.634 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.654 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.645 | fastapi.tiangolo.com/reference/encoders/ | 0.634 |
| scrapy+md | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.609 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.582 | fastapi.tiangolo.com/de/advanced/json-base64-bytes | 0.573 |
| crawlee | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.647 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.606 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.579 |
| colly+md | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.609 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.582 | fastapi.tiangolo.com/de/advanced/json-base64-bytes | 0.573 |
| playwright | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.647 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.606 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.579 |


**Q4: How do I use OAuth2 with password flow in FastAPI?** [code-example]
*(expects URL containing: `simple-oauth2`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | fastapi.tiangolo.com/de/reference/openapi/models/ | 0.679 | fastapi.tiangolo.com/reference/openapi/models/ | 0.679 | fastapi.tiangolo.com/zh/reference/openapi/models/ | 0.679 |
| crawl4ai | #7 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.719 | fastapi.tiangolo.com/reference/security/ | 0.712 | fastapi.tiangolo.com/es/reference/security/ | 0.709 |
| crawl4ai-raw | #7 | fastapi.tiangolo.com/tutorial/security/first-steps | 0.720 | fastapi.tiangolo.com/reference/security/ | 0.712 | fastapi.tiangolo.com/es/reference/security/ | 0.709 |
| scrapy+md | #6 | fastapi.tiangolo.com/es/reference/openapi/models/ | 0.679 | fastapi.tiangolo.com/reference/openapi/models/ | 0.679 | fastapi.tiangolo.com/de/reference/openapi/models/ | 0.679 |
| crawlee | #5 | fastapi.tiangolo.com/reference/security/ | 0.712 | fastapi.tiangolo.com/es/reference/security/ | 0.709 | fastapi.tiangolo.com/de/reference/security/ | 0.708 |
| colly+md | #6 | fastapi.tiangolo.com/de/reference/openapi/models/ | 0.679 | fastapi.tiangolo.com/reference/openapi/models/ | 0.679 | fastapi.tiangolo.com/es/reference/openapi/models/ | 0.679 |
| playwright | #5 | fastapi.tiangolo.com/reference/security/ | 0.712 | fastapi.tiangolo.com/es/reference/security/ | 0.709 | fastapi.tiangolo.com/de/reference/security/ | 0.708 |


**Q5: How do I use WebSockets in FastAPI?** [api-function]
*(expects URL containing: `websockets`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.810 | fastapi.tiangolo.com/advanced/websockets/ | 0.662 | fastapi.tiangolo.com/advanced/testing-websockets/ | 0.638 |
| crawl4ai | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.818 | fastapi.tiangolo.com/advanced/websockets/ | 0.678 | fastapi.tiangolo.com/advanced/websockets/ | 0.672 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.818 | fastapi.tiangolo.com/advanced/websockets/ | 0.678 | fastapi.tiangolo.com/advanced/websockets/ | 0.672 |
| scrapy+md | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.810 | fastapi.tiangolo.com/advanced/websockets/ | 0.662 | fastapi.tiangolo.com/es/reference/websockets/ | 0.625 |
| crawlee | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.811 | fastapi.tiangolo.com/advanced/websockets/ | 0.657 | fastapi.tiangolo.com/advanced/websockets/ | 0.645 |
| colly+md | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.810 | fastapi.tiangolo.com/advanced/websockets/ | 0.662 | fastapi.tiangolo.com/de/reference/websockets/ | 0.625 |
| playwright | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.811 | fastapi.tiangolo.com/advanced/websockets/ | 0.657 | fastapi.tiangolo.com/advanced/websockets/ | 0.645 |


**Q6: How do I define nested Pydantic models for request bodies?** [code-example]
*(expects URL containing: `body-nested-models`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.711 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.658 | fastapi.tiangolo.com/tutorial/body/ | 0.626 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.735 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.706 | fastapi.tiangolo.com/fr/tutorial/body-nested-model | 0.636 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.735 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.706 | fastapi.tiangolo.com/fr/tutorial/body-nested-model | 0.633 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.711 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.658 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.570 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.721 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.686 | fastapi.tiangolo.com/fr/tutorial/body-nested-model | 0.603 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.711 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.658 | fastapi.tiangolo.com/tutorial/query-param-models/ | 0.570 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.721 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.686 | fastapi.tiangolo.com/fr/tutorial/body-nested-model | 0.603 |


**Q7: How do I use middleware in FastAPI?** [api-function]
*(expects URL containing: `middleware`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | fastapi.tiangolo.com/zh/reference/fastapi/ | 0.723 | fastapi.tiangolo.com/reference/fastapi/ | 0.723 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.723 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/middleware/ | 0.730 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.719 | fastapi.tiangolo.com/reference/fastapi/ | 0.716 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/middleware/ | 0.730 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.719 | fastapi.tiangolo.com/reference/fastapi/ | 0.716 |
| scrapy+md | #4 | fastapi.tiangolo.com/es/reference/fastapi/ | 0.723 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.723 | fastapi.tiangolo.com/reference/fastapi/ | 0.723 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/middleware/ | 0.719 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.718 | fastapi.tiangolo.com/reference/fastapi/ | 0.718 |
| colly+md | #4 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.723 | fastapi.tiangolo.com/reference/fastapi/ | 0.723 | fastapi.tiangolo.com/es/reference/fastapi/ | 0.723 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/middleware/ | 0.719 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.718 | fastapi.tiangolo.com/reference/fastapi/ | 0.718 |


**Q8: How do I deploy FastAPI to the cloud?** [conceptual]
*(expects URL containing: `deployment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | fastapi.tiangolo.com/ | 0.754 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.754 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.727 |
| crawl4ai | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.787 | fastapi.tiangolo.com/deployment/cloud/ | 0.786 | fastapi.tiangolo.com/deployment/cloud/ | 0.783 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.787 | fastapi.tiangolo.com/deployment/cloud/ | 0.786 | fastapi.tiangolo.com/deployment/cloud/ | 0.783 |
| scrapy+md | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.760 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.756 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.754 |
| crawlee | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.768 | fastapi.tiangolo.com/deployment/cloud/ | 0.762 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.762 |
| colly+md | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.760 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.756 | fastapi.tiangolo.com | 0.754 |
| playwright | #1 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.768 | fastapi.tiangolo.com/deployment/cloud/ | 0.762 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.762 |


**Q9: How do I handle file uploads in FastAPI?** [api-function]
*(expects URL containing: `request-files`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/zh/tutorial/request-files/ | 0.635 | fastapi.tiangolo.com/de/reference/uploadfile/ | 0.625 | fastapi.tiangolo.com/zh/reference/uploadfile/ | 0.625 |
| crawl4ai | #7 | fastapi.tiangolo.com/reference/uploadfile/ | 0.685 | fastapi.tiangolo.com/de/reference/uploadfile/ | 0.675 | fastapi.tiangolo.com/es/reference/uploadfile/ | 0.661 |
| crawl4ai-raw | #7 | fastapi.tiangolo.com/reference/uploadfile/ | 0.685 | fastapi.tiangolo.com/de/reference/uploadfile/ | 0.675 | fastapi.tiangolo.com/es/reference/uploadfile/ | 0.661 |
| scrapy+md | #4 | fastapi.tiangolo.com/reference/uploadfile/ | 0.625 | fastapi.tiangolo.com/de/reference/uploadfile/ | 0.625 | fastapi.tiangolo.com/es/reference/uploadfile/ | 0.625 |
| crawlee | #2 | fastapi.tiangolo.com/de/reference/uploadfile/ | 0.640 | fastapi.tiangolo.com/tutorial/request-files/ | 0.638 | fastapi.tiangolo.com/es/reference/uploadfile/ | 0.635 |
| colly+md | #4 | fastapi.tiangolo.com/reference/uploadfile/ | 0.625 | fastapi.tiangolo.com/de/reference/uploadfile/ | 0.625 | fastapi.tiangolo.com/es/reference/uploadfile/ | 0.625 |
| playwright | #2 | fastapi.tiangolo.com/de/reference/uploadfile/ | 0.640 | fastapi.tiangolo.com/tutorial/request-files/ | 0.638 | fastapi.tiangolo.com/es/reference/uploadfile/ | 0.635 |


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
| markcrawl | #1 | fastapi.tiangolo.com/reference/templating/ | 0.766 | fastapi.tiangolo.com/zh/reference/templating/ | 0.766 | fastapi.tiangolo.com/advanced/templates/ | 0.741 |
| crawl4ai | #1 | fastapi.tiangolo.com/advanced/templates/ | 0.765 | fastapi.tiangolo.com/es/reference/templating/ | 0.764 | fastapi.tiangolo.com/reference/templating/ | 0.761 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/advanced/templates/ | 0.765 | fastapi.tiangolo.com/es/reference/templating/ | 0.764 | fastapi.tiangolo.com/reference/templating/ | 0.761 |
| scrapy+md | #1 | fastapi.tiangolo.com/reference/templating/ | 0.766 | fastapi.tiangolo.com/es/reference/templating/ | 0.766 | fastapi.tiangolo.com/de/reference/templating/ | 0.766 |
| crawlee | #1 | fastapi.tiangolo.com/advanced/templates/ | 0.752 | fastapi.tiangolo.com/es/reference/templating/ | 0.744 | fastapi.tiangolo.com/reference/templating/ | 0.742 |
| colly+md | #1 | fastapi.tiangolo.com/es/reference/templating/ | 0.766 | fastapi.tiangolo.com/reference/templating/ | 0.766 | fastapi.tiangolo.com/de/reference/templating/ | 0.766 |
| playwright | #1 | fastapi.tiangolo.com/advanced/templates/ | 0.752 | fastapi.tiangolo.com/es/reference/templating/ | 0.744 | fastapi.tiangolo.com/reference/templating/ | 0.742 |


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
| markcrawl | #3 | fastapi.tiangolo.com/zh/reference/responses/ | 0.726 | fastapi.tiangolo.com/reference/responses/ | 0.726 | fastapi.tiangolo.com/advanced/custom-response/ | 0.676 |
| crawl4ai | #7 | fastapi.tiangolo.com/es/reference/responses/ | 0.736 | fastapi.tiangolo.com/de/reference/responses/ | 0.732 | fastapi.tiangolo.com/reference/responses/ | 0.731 |
| crawl4ai-raw | #7 | fastapi.tiangolo.com/es/reference/responses/ | 0.736 | fastapi.tiangolo.com/de/reference/responses/ | 0.732 | fastapi.tiangolo.com/reference/responses/ | 0.731 |
| scrapy+md | #4 | fastapi.tiangolo.com/reference/responses/ | 0.726 | fastapi.tiangolo.com/es/reference/responses/ | 0.726 | fastapi.tiangolo.com/de/reference/responses/ | 0.726 |
| crawlee | #6 | fastapi.tiangolo.com/es/reference/responses/ | 0.720 | fastapi.tiangolo.com/de/reference/responses/ | 0.716 | fastapi.tiangolo.com/reference/responses/ | 0.715 |
| colly+md | #4 | fastapi.tiangolo.com/reference/responses/ | 0.726 | fastapi.tiangolo.com/de/reference/responses/ | 0.726 | fastapi.tiangolo.com/es/reference/responses/ | 0.726 |
| playwright | #6 | fastapi.tiangolo.com/es/reference/responses/ | 0.720 | fastapi.tiangolo.com/de/reference/responses/ | 0.716 | fastapi.tiangolo.com/reference/responses/ | 0.715 |


**Q14: How do I configure CORS in FastAPI?** [api-function]
*(expects URL containing: `cors`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.628 | fastapi.tiangolo.com/tutorial/cors/ | 0.617 | fastapi.tiangolo.com/zh/tutorial/cors/ | 0.590 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.664 | fastapi.tiangolo.com/tutorial/cors/ | 0.639 | fastapi.tiangolo.com/es/tutorial/cors/ | 0.628 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.664 | fastapi.tiangolo.com/tutorial/cors/ | 0.639 | fastapi.tiangolo.com/es/tutorial/cors/ | 0.628 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.628 | fastapi.tiangolo.com/tutorial/cors/ | 0.570 | fastapi.tiangolo.com/de/advanced/json-base64-bytes | 0.570 |
| crawlee | #1 | fastapi.tiangolo.com/es/tutorial/cors/ | 0.632 | fastapi.tiangolo.com/tutorial/cors/ | 0.620 | fastapi.tiangolo.com/es/tutorial/cors/ | 0.577 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.628 | fastapi.tiangolo.com/de/advanced/json-base64-bytes | 0.570 | fastapi.tiangolo.com/de/advanced/json-base64-bytes | 0.570 |
| playwright | #1 | fastapi.tiangolo.com/es/tutorial/cors/ | 0.632 | fastapi.tiangolo.com/tutorial/cors/ | 0.620 | fastapi.tiangolo.com/es/tutorial/cors/ | 0.577 |


**Q15: How do I use path parameters in FastAPI?** [api-function]
*(expects URL containing: `path-params`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.676 | fastapi.tiangolo.com/tutorial/query-params/ | 0.637 | fastapi.tiangolo.com/tutorial/path-params/ | 0.629 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.658 | fastapi.tiangolo.com/tutorial/path-params/ | 0.656 | fastapi.tiangolo.com/tutorial/path-params/ | 0.640 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.658 | fastapi.tiangolo.com/tutorial/path-params/ | 0.656 | fastapi.tiangolo.com/tutorial/path-params/ | 0.640 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.677 | fastapi.tiangolo.com/tutorial/query-params/ | 0.637 | fastapi.tiangolo.com/tutorial/path-params/ | 0.629 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.669 | fastapi.tiangolo.com/tutorial/path-params/ | 0.636 | fastapi.tiangolo.com/tutorial/query-params/ | 0.634 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.676 | fastapi.tiangolo.com/tutorial/query-params/ | 0.637 | fastapi.tiangolo.com/tutorial/path-params/ | 0.629 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.669 | fastapi.tiangolo.com/tutorial/path-params/ | 0.636 | fastapi.tiangolo.com/tutorial/query-params/ | 0.634 |


**Q16: How do I run FastAPI with Docker?** [conceptual]
*(expects URL containing: `docker`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.696 | fastapi.tiangolo.com/deployment/docker/ | 0.655 | fastapi.tiangolo.com/zh-hant/deployment/docker/ | 0.645 |
| crawl4ai | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.731 | fastapi.tiangolo.com/deployment/docker/ | 0.685 | fastapi.tiangolo.com/deployment/docker/ | 0.670 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.731 | fastapi.tiangolo.com/deployment/docker/ | 0.685 | fastapi.tiangolo.com/deployment/docker/ | 0.670 |
| scrapy+md | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.696 | fastapi.tiangolo.com/deployment/docker/ | 0.655 | fastapi.tiangolo.com/es/deployment/docker/ | 0.635 |
| crawlee | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.697 | fastapi.tiangolo.com/deployment/docker/ | 0.678 | fastapi.tiangolo.com/deployment/docker/ | 0.662 |
| colly+md | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.696 | fastapi.tiangolo.com/deployment/docker/ | 0.655 | fastapi.tiangolo.com/es/deployment/docker/ | 0.635 |
| playwright | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.697 | fastapi.tiangolo.com/deployment/docker/ | 0.670 | fastapi.tiangolo.com/deployment/docker/ | 0.662 |


**Q17: How do I configure FastAPI application settings?** [code-example]
*(expects URL containing: `settings`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.692 | fastapi.tiangolo.com/zh/advanced/settings/ | 0.659 | fastapi.tiangolo.com/zh-hant/advanced/settings/ | 0.619 |
| crawl4ai | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.696 | fastapi.tiangolo.com/es/advanced/settings/ | 0.650 | fastapi.tiangolo.com/de/advanced/settings/ | 0.621 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.696 | fastapi.tiangolo.com/es/advanced/settings/ | 0.650 | fastapi.tiangolo.com/de/advanced/settings/ | 0.620 |
| scrapy+md | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.692 | fastapi.tiangolo.com/es/advanced/settings/ | 0.638 | fastapi.tiangolo.com/de/advanced/settings/ | 0.596 |
| crawlee | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.696 | fastapi.tiangolo.com/es/advanced/settings/ | 0.646 | fastapi.tiangolo.com/de/advanced/settings/ | 0.612 |
| colly+md | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.692 | fastapi.tiangolo.com/es/advanced/settings/ | 0.638 | fastapi.tiangolo.com/de/advanced/settings/ | 0.596 |
| playwright | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.696 | fastapi.tiangolo.com/es/advanced/settings/ | 0.646 | fastapi.tiangolo.com/de/advanced/settings/ | 0.612 |


**Q18: How do I use background tasks in FastAPI?** [api-function]
*(expects URL containing: `background-tasks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.692 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.683 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.675 |
| crawl4ai | #7 | fastapi.tiangolo.com/reference/background/ | 0.768 | fastapi.tiangolo.com/de/reference/background/ | 0.763 | fastapi.tiangolo.com/es/reference/background/ | 0.751 |
| crawl4ai-raw | #7 | fastapi.tiangolo.com/reference/background/ | 0.768 | fastapi.tiangolo.com/de/reference/background/ | 0.763 | fastapi.tiangolo.com/es/reference/background/ | 0.751 |
| scrapy+md | #7 | fastapi.tiangolo.com/reference/background/ | 0.731 | fastapi.tiangolo.com/es/reference/background/ | 0.731 | fastapi.tiangolo.com/de/reference/background/ | 0.731 |
| crawlee | #7 | fastapi.tiangolo.com/de/reference/background/ | 0.737 | fastapi.tiangolo.com/reference/background/ | 0.736 | fastapi.tiangolo.com/es/reference/background/ | 0.735 |
| colly+md | #7 | fastapi.tiangolo.com/de/reference/background/ | 0.731 | fastapi.tiangolo.com/es/reference/background/ | 0.731 | fastapi.tiangolo.com/reference/background/ | 0.731 |
| playwright | #7 | fastapi.tiangolo.com/de/reference/background/ | 0.737 | fastapi.tiangolo.com/reference/background/ | 0.736 | fastapi.tiangolo.com/es/reference/background/ | 0.735 |


**Q19: What are the first steps to create a FastAPI application?** [conceptual]
*(expects URL containing: `first-steps`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.659 | fastapi.tiangolo.com/zh/reference/fastapi/ | 0.659 |
| crawl4ai | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.688 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.679 | fastapi.tiangolo.com/tutorial/ | 0.668 |
| crawl4ai-raw | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.688 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.679 | fastapi.tiangolo.com/tutorial/ | 0.668 |
| scrapy+md | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/tutorial/body/ | 0.661 | fastapi.tiangolo.com/tutorial/request-files/ | 0.661 |
| crawlee | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.685 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/tutorial/sql-databases/ | 0.667 |
| colly+md | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/tutorial/sql-databases/ | 0.661 | fastapi.tiangolo.com/reference/fastapi/ | 0.659 |
| playwright | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.685 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.669 | fastapi.tiangolo.com/tutorial/sql-databases/ | 0.667 |


**Q20: How do I handle errors and exceptions in FastAPI?** [api-function]
*(expects URL containing: `handling-errors`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | fastapi.tiangolo.com/zh/reference/fastapi/ | 0.615 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.615 | fastapi.tiangolo.com/reference/fastapi/ | 0.615 |
| crawl4ai | #2 | fastapi.tiangolo.com/deployment/concepts/ | 0.632 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.628 | fastapi.tiangolo.com/reference/exceptions/ | 0.627 |
| crawl4ai-raw | #2 | fastapi.tiangolo.com/deployment/concepts/ | 0.632 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.628 | fastapi.tiangolo.com/reference/exceptions/ | 0.627 |
| scrapy+md | #5 | fastapi.tiangolo.com/deployment/concepts/ | 0.612 | fastapi.tiangolo.com/reference/fastapi/ | 0.608 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.608 |
| crawlee | #2 | fastapi.tiangolo.com/deployment/concepts/ | 0.618 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.599 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.599 |
| colly+md | #5 | fastapi.tiangolo.com/deployment/concepts/ | 0.612 | fastapi.tiangolo.com/es/reference/fastapi/ | 0.608 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.608 |
| playwright | #2 | fastapi.tiangolo.com/deployment/concepts/ | 0.618 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.599 | fastapi.tiangolo.com/de/reference/fastapi/ | 0.599 |


</details>

## python-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 68% (13/19) | 95% (18/19) | 100% (19/19) | 100% (19/19) | 100% (19/19) | 0.809 | 10496 | 500 |
| crawl4ai-raw | 68% (13/19) | 95% (18/19) | 100% (19/19) | 100% (19/19) | 100% (19/19) | 0.809 | 10496 | 500 |
| crawlee | 68% (13/19) | 95% (18/19) | 95% (18/19) | 95% (18/19) | 100% (19/19) | 0.785 | 10315 | 500 |
| playwright | 68% (13/19) | 95% (18/19) | 95% (18/19) | 95% (18/19) | 100% (19/19) | 0.785 | 10315 | 500 |
| **markcrawl** | 37% (7/19) | 74% (14/19) | 84% (16/19) | 84% (16/19) | 89% (17/19) | 0.563 | 8808 | 500 |
| colly+md | 53% (10/19) | 58% (11/19) | 63% (12/19) | 63% (12/19) | 68% (13/19) | 0.557 | 15343 | 500 |
| scrapy+md | 32% (6/19) | 42% (8/19) | 42% (8/19) | 53% (10/19) | 53% (10/19) | 0.372 | 13574 | 500 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for python-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What new features were added in Python 3.10?** [factual-lookup]
*(expects URL containing: `whatsnew/3.10`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/whatsnew/3.10.html | 0.759 | docs.python.org/3.11/contents.html | 0.652 | docs.python.org/3.12/contents.html | 0.651 |
| crawl4ai | #2 | docs.python.org/3/contents.html | 0.660 | docs.python.org/3/whatsnew/3.14.html | 0.636 | docs.python.org/3/whatsnew/3.14.html | 0.631 |
| crawl4ai-raw | #2 | docs.python.org/3/contents.html | 0.660 | docs.python.org/3/whatsnew/3.14.html | 0.636 | docs.python.org/3/whatsnew/3.14.html | 0.631 |
| scrapy+md | #1 | docs.python.org/3.11/whatsnew/3.10.html | 0.713 | docs.python.org/3/whatsnew/3.8.html | 0.697 | docs.python.org/3.11/whatsnew/3.8.html | 0.697 |
| crawlee | #3 | docs.python.org/3/contents.html | 0.652 | docs.python.org/3/contents.html | 0.630 | docs.python.org/3/whatsnew/3.14.html | 0.625 |
| colly+md | miss | docs.python.org/3/contents.html | 0.652 | docs.python.org/3/contents.html | 0.630 | docs.python.org/3/contents.html | 0.605 |
| playwright | #3 | docs.python.org/3/contents.html | 0.652 | docs.python.org/3/contents.html | 0.630 | docs.python.org/3/whatsnew/3.14.html | 0.625 |


**Q2: What does the term 'decorator' mean in Python?** [factual-lookup]
*(expects URL containing: `glossary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.python.org/3.10/whatsnew/2.4.html | 0.608 | docs.python.org/3.0/glossary.html | 0.602 | docs.python.org/2.6/glossary.html | 0.584 |
| crawl4ai | #2 | docs.python.org/3/howto/sorting.html | 0.504 | docs.python.org/3/glossary.html | 0.493 | docs.python.org/3/reference/compound_stmts.html | 0.465 |
| crawl4ai-raw | #2 | docs.python.org/3/howto/sorting.html | 0.504 | docs.python.org/3/glossary.html | 0.493 | docs.python.org/3/reference/compound_stmts.html | 0.465 |
| scrapy+md | #3 | docs.python.org/3.11/whatsnew/2.4.html | 0.610 | docs.python.org/3.11/whatsnew/2.4.html | 0.576 | docs.python.org/3.12/glossary.html | 0.535 |
| crawlee | #11 | docs.python.org/3/library/typing.html | 0.598 | docs.python.org/3/library/typing.html | 0.568 | docs.python.org/3/library/typing.html | 0.486 |
| colly+md | miss | docs.python.org/3/library/typing.html | 0.568 | docs.python.org/3/library/typing.html | 0.487 | docs.python.org/3/library/typing.html | 0.474 |
| playwright | #11 | docs.python.org/3/library/typing.html | 0.598 | docs.python.org/3/library/typing.html | 0.568 | docs.python.org/3/library/typing.html | 0.486 |


**Q3: How do I report a bug in Python?** [factual-lookup]
*(expects URL containing: `bugs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.0/bugs.html | 0.713 | docs.python.org/2.6/bugs.html | 0.672 | docs.python.org/3.3/bugs.html | 0.643 |
| crawl4ai | #1 | docs.python.org/3/bugs.html | 0.675 | docs.python.org/bugs.html | 0.675 | docs.python.org/bugs.html | 0.664 |
| crawl4ai-raw | #1 | docs.python.org/3/bugs.html | 0.675 | docs.python.org/bugs.html | 0.675 | docs.python.org/bugs.html | 0.664 |
| scrapy+md | miss | docs.python.org/3/faq/general.html | 0.662 | docs.python.org/3.11/faq/general.html | 0.662 | docs.python.org/3.11/faq/library.html | 0.614 |
| crawlee | #1 | docs.python.org/3/bugs.html | 0.641 | docs.python.org/bugs.html | 0.641 | docs.python.org/bugs.html | 0.640 |
| colly+md | #1 | docs.python.org/3/bugs.html | 0.609 | docs.python.org/3/bugs.html | 0.585 | docs.python.org/3/bugs.html | 0.577 |
| playwright | #1 | docs.python.org/3/bugs.html | 0.642 | docs.python.org/bugs.html | 0.641 | docs.python.org/bugs.html | 0.640 |


**Q4: What is Python's glossary definition of a generator?** [factual-lookup]
*(expects URL containing: `glossary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.0/glossary.html | 0.630 | docs.python.org/2.6/glossary.html | 0.617 | docs.python.org/3.10/glossary.html | 0.584 |
| crawl4ai | #1 | docs.python.org/3/glossary.html | 0.601 | docs.python.org/3/glossary.html | 0.581 | docs.python.org/3/reference/datamodel.html | 0.561 |
| crawl4ai-raw | #1 | docs.python.org/3/glossary.html | 0.601 | docs.python.org/3/glossary.html | 0.581 | docs.python.org/3/reference/datamodel.html | 0.561 |
| scrapy+md | #1 | docs.python.org/3.12/glossary.html | 0.576 | docs.python.org/3/glossary.html | 0.552 | docs.python.org/3/glossary.html | 0.550 |
| crawlee | #1 | docs.python.org/3/glossary.html | 0.612 | docs.python.org/3/glossary.html | 0.549 | docs.python.org/3/library/stdtypes.html | 0.547 |
| colly+md | miss | docs.python.org/3/library/stdtypes.html#iterator-t | 0.547 | docs.python.org/3/library/stdtypes.html#boolean-ty | 0.547 | docs.python.org/3/library/stdtypes.html#comparison | 0.547 |
| playwright | #1 | docs.python.org/3/glossary.html | 0.612 | docs.python.org/3/glossary.html | 0.549 | docs.python.org/3/library/stdtypes.html | 0.547 |


**Q5: What is the Python module index?** [navigation]
*(expects URL containing: `py-modindex`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.11/py-modindex.html | 0.852 | docs.python.org/3.12/py-modindex.html | 0.852 | docs.python.org/3.15/py-modindex.html | 0.852 |
| crawl4ai | #3 | docs.python.org/3/installing/index.html | 0.600 | docs.python.org/3/installing/index.html | 0.597 | docs.python.org/3/py-modindex.html | 0.583 |
| crawl4ai-raw | #3 | docs.python.org/3/installing/index.html | 0.600 | docs.python.org/3/installing/index.html | 0.597 | docs.python.org/3/py-modindex.html | 0.583 |
| scrapy+md | miss | docs.python.org/3.12/installing/index.html | 0.640 | docs.python.org/3.12/installing/index.html | 0.636 | docs.python.org/3.11/install/index.html | 0.635 |
| crawlee | #1 | docs.python.org/3/py-modindex.html | 0.776 | docs.python.org/3/library/modulefinder.html | 0.617 | docs.python.org/3/library/runpy.html | 0.610 |
| colly+md | #1 | docs.python.org/3/py-modindex.html | 0.776 | docs.python.org/3/genindex.html | 0.632 | docs.python.org/3/library/modulefinder.html#module | 0.620 |
| playwright | #1 | docs.python.org/3/py-modindex.html | 0.776 | docs.python.org/3/library/modulefinder.html | 0.617 | docs.python.org/3/library/runpy.html | 0.610 |


**Q6: What does the term 'iterable' mean in Python?** [factual-lookup]
*(expects URL containing: `glossary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.13/glossary.html | 0.648 | docs.python.org/3.3/glossary.html | 0.608 | docs.python.org/2.6/glossary.html | 0.565 |
| crawl4ai | #1 | docs.python.org/3/glossary.html | 0.553 | docs.python.org/3/genindex-I.html | 0.516 | docs.python.org/3/library/itertools.html | 0.514 |
| crawl4ai-raw | #1 | docs.python.org/3/glossary.html | 0.553 | docs.python.org/3/genindex-I.html | 0.516 | docs.python.org/3/library/itertools.html | 0.514 |
| scrapy+md | #1 | docs.python.org/3.12/glossary.html | 0.553 | docs.python.org/3/glossary.html | 0.540 | docs.python.org/3.12/glossary.html | 0.503 |
| crawlee | #1 | docs.python.org/3/glossary.html | 0.541 | docs.python.org/3/library/itertools.html | 0.531 | docs.python.org/3/library/itertools.html | 0.503 |
| colly+md | miss | docs.python.org/3/library/itertools.html#module-it | 0.531 | docs.python.org/3/library/itertools.html | 0.531 | docs.python.org/3/library/itertools.html | 0.529 |
| playwright | #1 | docs.python.org/3/glossary.html | 0.541 | docs.python.org/3/library/itertools.html | 0.531 | docs.python.org/3/library/itertools.html | 0.503 |


**Q7: How do I install and configure Python on my system?** [conceptual]
*(expects URL containing: `using`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #12 | docs.python.org/3.13/installing/index.html | 0.582 | docs.python.org/3.12/installing/index.html | 0.578 | docs.python.org/3.11/installing/index.html | 0.578 |
| crawl4ai | #2 | docs.python.org/3/installing/index.html | 0.596 | docs.python.org/3/using/configure.html | 0.572 | docs.python.org/3/installing/index.html | 0.554 |
| crawl4ai-raw | #2 | docs.python.org/3/installing/index.html | 0.596 | docs.python.org/3/using/configure.html | 0.572 | docs.python.org/3/installing/index.html | 0.554 |
| scrapy+md | #1 | docs.python.org/3.11/using/unix.html | 0.589 | docs.python.org/3/installing/index.html | 0.582 | docs.python.org/3.12/installing/index.html | 0.578 |
| crawlee | #2 | docs.python.org/3/installing/index.html | 0.582 | docs.python.org/3/using/configure.html#debug-build | 0.548 | docs.python.org/3/installing/index.html | 0.534 |
| colly+md | #1 | docs.python.org/3/using/ios.html#using-ios | 0.526 | docs.python.org/3/library/sys/path/init.html | 0.478 | docs.python.org/3/extending/embedding.html#embeddi | 0.475 |
| playwright | #2 | docs.python.org/3/installing/index.html | 0.582 | docs.python.org/3/using/configure.html | 0.549 | docs.python.org/3/installing/index.html | 0.534 |


**Q8: How do I use the os module for file and directory operations?** [api-function]
*(expects URL containing: `library/os`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.python.org/3.10/library/filesys.html | 0.599 | docs.python.org/3.10/library/os.html | 0.555 | docs.python.org/3.3/whatsnew/3.3.html | 0.548 |
| crawl4ai | #1 | docs.python.org/3/library/os.html | 0.596 | docs.python.org/3/library/os.html | 0.581 | docs.python.org/3/library/os.html | 0.575 |
| crawl4ai-raw | #1 | docs.python.org/3/library/os.html | 0.596 | docs.python.org/3/library/os.html | 0.581 | docs.python.org/3/library/os.html | 0.575 |
| scrapy+md | #10 | docs.python.org/3.11/tutorial/stdlib.html | 0.611 | docs.python.org/3.12/tutorial/stdlib.html | 0.611 | docs.python.org/3.11/library/filesys.html | 0.588 |
| crawlee | #3 | docs.python.org/3/library/shutil.html | 0.601 | docs.python.org/3/library/filesys.html | 0.579 | docs.python.org/3/library/os.html | 0.577 |
| colly+md | #3 | docs.python.org/3/library/shutil.html | 0.601 | docs.python.org/3/library/filesys.html | 0.579 | docs.python.org/3/library/os.html#os.kill | 0.577 |
| playwright | #3 | docs.python.org/3/library/shutil.html | 0.601 | docs.python.org/3/library/filesys.html | 0.579 | docs.python.org/3/library/os.html | 0.577 |


**Q9: How do I use pathlib for filesystem paths in Python?** [api-function]
*(expects URL containing: `library/pathlib`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.python.org/3.10/whatsnew/3.4.html | 0.625 | docs.python.org/3.10/whatsnew/3.6.html | 0.546 | docs.python.org/3.10/library/pathlib.html | 0.510 |
| crawl4ai | #1 | docs.python.org/3/library/pathlib.html | 0.573 | docs.python.org/3/library/pathlib.html | 0.552 | docs.python.org/3/library/pathlib.html | 0.551 |
| crawl4ai-raw | #1 | docs.python.org/3/library/pathlib.html | 0.573 | docs.python.org/3/library/pathlib.html | 0.552 | docs.python.org/3/library/pathlib.html | 0.551 |
| scrapy+md | miss | docs.python.org/3.11/whatsnew/3.4.html | 0.631 | docs.python.org/3.11/whatsnew/3.6.html | 0.535 | docs.python.org/3/whatsnew/3.6.html | 0.535 |
| crawlee | #1 | docs.python.org/3/library/pathlib.html | 0.519 | docs.python.org/3/library/pathlib.html | 0.514 | docs.python.org/3/library/pathlib.html | 0.512 |
| colly+md | #1 | docs.python.org/3/library/pathlib.html | 0.512 | docs.python.org/3/library/pathlib.html | 0.510 | docs.python.org/3/library/compileall.html | 0.503 |
| playwright | #1 | docs.python.org/3/library/pathlib.html | 0.519 | docs.python.org/3/library/pathlib.html | 0.514 | docs.python.org/3/library/pathlib.html | 0.512 |


**Q10: How do I parse and generate JSON in Python?** [api-function]
*(expects URL containing: `library/json`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.python.org/2.6/whatsnew/2.6.html | 0.499 | docs.python.org/3.10/whatsnew/2.6.html | 0.495 | docs.python.org/3.10/library/json.html | 0.462 |
| crawl4ai | #1 | docs.python.org/3/library/json.html | 0.505 | docs.python.org/3/library/json.html | 0.462 | docs.python.org/3/library/json.html | 0.461 |
| crawl4ai-raw | #1 | docs.python.org/3/library/json.html | 0.505 | docs.python.org/3/library/json.html | 0.462 | docs.python.org/3/library/json.html | 0.461 |
| scrapy+md | #2 | docs.python.org/3.11/whatsnew/2.6.html | 0.492 | docs.python.org/3.11/library/json.html | 0.457 | docs.python.org/3.11/tutorial/inputoutput.html | 0.416 |
| crawlee | #1 | docs.python.org/3/library/json.html | 0.467 | docs.python.org/3/library/json.html | 0.436 | docs.python.org/3/library/json.html | 0.435 |
| colly+md | #1 | docs.python.org/3/library/json.html#module-json.to | 0.479 | docs.python.org/3/library/json.html#module-json | 0.479 | docs.python.org/3/library/json.html | 0.479 |
| playwright | #1 | docs.python.org/3/library/json.html | 0.467 | docs.python.org/3/library/json.html | 0.436 | docs.python.org/3/library/json.html | 0.435 |


**Q11: How do I use asyncio for async programming in Python?** [api-function]
*(expects URL containing: `library/asyncio`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.python.org/3.10/whatsnew/3.4.html | 0.550 | docs.python.org/3.10/library/asyncio.html | 0.542 | docs.python.org/3.10/whatsnew/3.8.html | 0.532 |
| crawl4ai | #3 | docs.python.org/3/library/socket.html | 0.594 | docs.python.org/3/library/socket.html | 0.594 | docs.python.org/3/library/asyncio.html | 0.577 |
| crawl4ai-raw | #3 | docs.python.org/3/library/socket.html | 0.594 | docs.python.org/3/library/socket.html | 0.594 | docs.python.org/3/library/asyncio.html | 0.577 |
| scrapy+md | #1 | docs.python.org/3.11/library/asyncio-dev.html | 0.666 | docs.python.org/3.11/library/socket.html | 0.572 | docs.python.org/3.11/library/socket.html | 0.572 |
| crawlee | #3 | docs.python.org/3/library/socket.html | 0.572 | docs.python.org/3/library/socket.html | 0.572 | docs.python.org/3/library/asyncio-task.html#asynci | 0.561 |
| colly+md | #5 | docs.python.org/3/library/socket.html#module-socke | 0.572 | docs.python.org/3/library/socket.html#module-socke | 0.572 | docs.python.org/3/library/socket.html | 0.572 |
| playwright | #3 | docs.python.org/3/library/socket.html | 0.572 | docs.python.org/3/library/socket.html | 0.572 | docs.python.org/3/library/asyncio-task.html | 0.561 |


**Q12: How do I use type hints and the typing module in Python?** [api-function]
*(expects URL containing: `library/typing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | docs.python.org/3.12/whatsnew/3.12.html | 0.663 | docs.python.org/3.10/whatsnew/3.5.html | 0.662 | docs.python.org/3.10/whatsnew/3.10.html | 0.656 |
| crawl4ai | #1 | docs.python.org/3/library/typing.html | 0.697 | docs.python.org/3/library/typing.html | 0.696 | docs.python.org/3/library/development.html | 0.675 |
| crawl4ai-raw | #1 | docs.python.org/3/library/typing.html | 0.697 | docs.python.org/3/library/typing.html | 0.696 | docs.python.org/3/library/development.html | 0.675 |
| scrapy+md | miss | docs.python.org/3/whatsnew/3.5.html | 0.665 | docs.python.org/3.11/whatsnew/3.5.html | 0.665 | docs.python.org/3.12/whatsnew/3.11.html | 0.655 |
| crawlee | #1 | docs.python.org/3/library/typing.html | 0.667 | docs.python.org/3/library/typing.html | 0.662 | docs.python.org/3/library/typing.html | 0.653 |
| colly+md | #1 | docs.python.org/3/library/typing.html | 0.652 | docs.python.org/3/library/pydoc.html | 0.584 | docs.python.org/3/library/pydoc.html | 0.584 |
| playwright | #1 | docs.python.org/3/library/typing.html | 0.667 | docs.python.org/3/library/typing.html | 0.662 | docs.python.org/3/library/typing.html | 0.653 |


**Q13: How do I work with dates and times using the datetime module?** [api-function]
*(expects URL containing: `library/datetime`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/datetime.html | 0.591 | docs.python.org/3.10/whatsnew/2.3.html | 0.540 | docs.python.org/3.10/library/datetime.html | 0.539 |
| crawl4ai | #1 | docs.python.org/3/library/datetime.html | 0.603 | docs.python.org/3/library/datetime.html | 0.532 | docs.python.org/3/library/datetime.html | 0.518 |
| crawl4ai-raw | #1 | docs.python.org/3/library/datetime.html | 0.603 | docs.python.org/3/library/datetime.html | 0.532 | docs.python.org/3/library/datetime.html | 0.518 |
| scrapy+md | miss | docs.python.org/3.12/tutorial/stdlib.html | 0.623 | docs.python.org/3.11/tutorial/stdlib.html | 0.623 | docs.python.org/3.11/whatsnew/2.3.html | 0.561 |
| crawlee | #1 | docs.python.org/3/library/datetime.html | 0.585 | docs.python.org/3/library/datetime.html | 0.524 | docs.python.org/3/library/datetime.html | 0.505 |
| colly+md | #1 | docs.python.org/3/library/datetime.html#module-dat | 0.585 | docs.python.org/3/library/datetime.html | 0.585 | docs.python.org/3/library/datetime.html | 0.525 |
| playwright | #1 | docs.python.org/3/library/datetime.html | 0.585 | docs.python.org/3/library/datetime.html | 0.524 | docs.python.org/3/library/datetime.html | 0.505 |


**Q14: How do I use Python's logging module?** [api-function]
*(expects URL containing: `library/logging`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/logging.html | 0.551 | docs.python.org/3.10/whatsnew/2.7.html | 0.506 | docs.python.org/3.3/contents.html | 0.505 |
| crawl4ai | #1 | docs.python.org/3/library/logging.html | 0.654 | docs.python.org/3/library/logging.html | 0.606 | docs.python.org/3/library/logging.html | 0.568 |
| crawl4ai-raw | #1 | docs.python.org/3/library/logging.html | 0.654 | docs.python.org/3/library/logging.html | 0.606 | docs.python.org/3/library/logging.html | 0.568 |
| scrapy+md | miss | docs.python.org/3.11/howto/logging-cookbook.html | 0.537 | docs.python.org/3.11/whatsnew/2.3.html | 0.521 | docs.python.org/3.11/howto/logging-cookbook.html | 0.514 |
| crawlee | #1 | docs.python.org/3/library/logging.html | 0.636 | docs.python.org/3/library/logging.html | 0.596 | docs.python.org/3/library/logging.config.html | 0.552 |
| colly+md | #1 | docs.python.org/3/library/logging.html#module-logg | 0.630 | docs.python.org/3/library/logging.html | 0.630 | docs.python.org/3/library/logging.html#module-logg | 0.596 |
| playwright | #1 | docs.python.org/3/library/logging.html | 0.636 | docs.python.org/3/library/logging.html | 0.596 | docs.python.org/3/library/logging.config.html | 0.552 |


**Q15: How do I write unit tests with the unittest module?** [code-example]
*(expects URL containing: `library/unittest`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | docs.python.org/3.10/library/test.html | 0.633 | docs.python.org/3.10/library/test.html | 0.617 | docs.python.org/3.10/library/doctest.html | 0.581 |
| crawl4ai | #5 | docs.python.org/3/library/test.html | 0.649 | docs.python.org/3/library/test.html | 0.626 | docs.python.org/3/library/test.html | 0.597 |
| crawl4ai-raw | #5 | docs.python.org/3/library/test.html | 0.649 | docs.python.org/3/library/test.html | 0.626 | docs.python.org/3/library/test.html | 0.597 |
| scrapy+md | #7 | docs.python.org/3.12/library/test.html | 0.641 | docs.python.org/3.11/library/test.html | 0.641 | docs.python.org/3.11/library/test.html | 0.624 |
| crawlee | #3 | docs.python.org/3/library/test.html | 0.658 | docs.python.org/3/library/test.html | 0.612 | docs.python.org/3/library/unittest.html | 0.587 |
| colly+md | #19 | docs.python.org/3/library/test.html#module-test.su | 0.657 | docs.python.org/3/library/test.html#module-test.su | 0.657 | docs.python.org/3/library/test.html#module-test.su | 0.657 |
| playwright | #3 | docs.python.org/3/library/test.html | 0.658 | docs.python.org/3/library/test.html | 0.612 | docs.python.org/3/library/unittest.html | 0.587 |


**Q16: How do I use Python dataclasses?** [api-function]
*(expects URL containing: `library/dataclasses`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.python.org/3.10/whatsnew/3.7.html | 0.624 | docs.python.org/3.10/library/dataclasses.html | 0.599 | docs.python.org/3.10/whatsnew/3.10.html | 0.543 |
| crawl4ai | #1 | docs.python.org/3/library/dataclasses.html | 0.667 | docs.python.org/3/library/dataclasses.html | 0.655 | docs.python.org/3/library/dataclasses.html | 0.644 |
| crawl4ai-raw | #1 | docs.python.org/3/library/dataclasses.html | 0.667 | docs.python.org/3/library/dataclasses.html | 0.655 | docs.python.org/3/library/dataclasses.html | 0.644 |
| scrapy+md | #1 | docs.python.org/3.12/library/dataclasses.html | 0.630 | docs.python.org/3.11/whatsnew/3.7.html | 0.626 | docs.python.org/3/whatsnew/3.7.html | 0.626 |
| crawlee | #1 | docs.python.org/3/library/dataclasses.html | 0.631 | docs.python.org/3/library/dataclasses.html | 0.621 | docs.python.org/3/library/dataclasses.html | 0.610 |
| colly+md | #1 | docs.python.org/3/library/dataclasses.html | 0.630 | docs.python.org/3/library/dataclasses.html#module- | 0.630 | docs.python.org/3/library/dataclasses.html | 0.558 |
| playwright | #1 | docs.python.org/3/library/dataclasses.html | 0.631 | docs.python.org/3/library/dataclasses.html | 0.621 | docs.python.org/3/library/dataclasses.html | 0.610 |


**Q17: How do I use itertools for efficient iteration in Python?** [api-function]
*(expects URL containing: `library/itertools`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.python.org/3.10/whatsnew/3.10.html | 0.592 | docs.python.org/3.10/library/itertools.html | 0.568 | docs.python.org/3.10/library/itertools.html | 0.539 |
| crawl4ai | #1 | docs.python.org/3/library/itertools.html | 0.642 | docs.python.org/3/library/itertools.html | 0.641 | docs.python.org/3/library/itertools.html | 0.601 |
| crawl4ai-raw | #1 | docs.python.org/3/library/itertools.html | 0.642 | docs.python.org/3/library/itertools.html | 0.641 | docs.python.org/3/library/itertools.html | 0.601 |
| scrapy+md | miss | docs.python.org/3.11/whatsnew/3.10.html | 0.580 | docs.python.org/3.11/library/functools.html | 0.548 | docs.python.org/3.11/library/functools.html | 0.548 |
| crawlee | #1 | docs.python.org/3/library/itertools.html | 0.634 | docs.python.org/3/library/itertools.html | 0.625 | docs.python.org/3/library/itertools.html | 0.576 |
| colly+md | #1 | docs.python.org/3/library/itertools.html | 0.576 | docs.python.org/3/library/itertools.html#module-it | 0.576 | docs.python.org/3/library/itertools.html | 0.574 |
| playwright | #1 | docs.python.org/3/library/itertools.html | 0.634 | docs.python.org/3/library/itertools.html | 0.625 | docs.python.org/3/library/itertools.html | 0.576 |


**Q18: How does Python's data model work with special methods?** [conceptual]
*(expects URL containing: `reference/datamodel`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.python.org/3.10/library/datatypes.html | 0.510 | docs.python.org/3.11/contents.html | 0.507 | docs.python.org/2.6/contents.html | 0.506 |
| crawl4ai | #1 | docs.python.org/3/reference/datamodel.html | 0.596 | docs.python.org/3/reference/datamodel.html | 0.571 | docs.python.org/3/reference/datamodel.html | 0.563 |
| crawl4ai-raw | #1 | docs.python.org/3/reference/datamodel.html | 0.596 | docs.python.org/3/reference/datamodel.html | 0.571 | docs.python.org/3/reference/datamodel.html | 0.563 |
| scrapy+md | miss | docs.python.org/3.11/tutorial/classes.html | 0.519 | docs.python.org/3.12/tutorial/classes.html | 0.519 | docs.python.org/3.11/library/datatypes.html | 0.513 |
| crawlee | #1 | docs.python.org/3/reference/datamodel.html | 0.528 | docs.python.org/3/reference/datamodel.html | 0.525 | docs.python.org/3/reference/datamodel.html | 0.514 |
| colly+md | miss | docs.python.org/3/library/datatypes.html | 0.513 | docs.python.org/3/contents.html | 0.489 | docs.python.org/3/library/dataclasses.html | 0.463 |
| playwright | #1 | docs.python.org/3/reference/datamodel.html | 0.528 | docs.python.org/3/reference/datamodel.html | 0.525 | docs.python.org/3/reference/datamodel.html | 0.514 |


**Q19: What are Python's compound statements like if, for, and with?** [conceptual]
*(expects URL containing: `reference/compound_stmts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.python.org/3.10/whatsnew/2.6.html | 0.568 | docs.python.org/2.6/whatsnew/2.6.html | 0.549 | docs.python.org/3.10/whatsnew/2.5.html | 0.546 |
| crawl4ai | #1 | docs.python.org/3/reference/compound_stmts.html | 0.683 | docs.python.org/3/reference/compound_stmts.html | 0.670 | docs.python.org/3/reference/compound_stmts.html | 0.663 |
| crawl4ai-raw | #1 | docs.python.org/3/reference/compound_stmts.html | 0.683 | docs.python.org/3/reference/compound_stmts.html | 0.670 | docs.python.org/3/reference/compound_stmts.html | 0.663 |
| scrapy+md | miss | docs.python.org/3.11/tutorial/controlflow.html | 0.579 | docs.python.org/3.11/whatsnew/2.6.html | 0.571 | docs.python.org/3.11/tutorial/controlflow.html | 0.566 |
| crawlee | #1 | docs.python.org/3/reference/compound_stmts.html | 0.650 | docs.python.org/3/reference/compound_stmts.html | 0.629 | docs.python.org/3/reference/compound_stmts.html | 0.617 |
| colly+md | miss | docs.python.org/3/reference/toplevel/components.ht | 0.506 | docs.python.org/3/reference/toplevel/components.ht | 0.506 | docs.python.org/3/reference/grammar.html | 0.503 |
| playwright | #1 | docs.python.org/3/reference/compound_stmts.html | 0.650 | docs.python.org/3/reference/compound_stmts.html | 0.629 | docs.python.org/3/reference/compound_stmts.html | 0.617 |


</details>

## react-dev

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| colly+md | 75% (12/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.825 | 9345 | 291 |
| crawl4ai | 75% (12/16) | 88% (14/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 0.813 | 9477 | 500 |
| crawl4ai-raw | 75% (12/16) | 88% (14/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 0.813 | 9478 | 500 |
| **markcrawl** | 69% (11/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.804 | 3496 | 221 |
| scrapy+md | 69% (11/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.790 | 3513 | 216 |
| crawlee | 69% (11/16) | 81% (13/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.785 | 6411 | 217 |
| playwright | 69% (11/16) | 81% (13/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.785 | 6398 | 221 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for react-dev</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I manage state in a React component?** [conceptual]
*(expects URL containing: `state`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |
| crawl4ai | #1 | react.dev/learn/preserving-and-resetting-state | 0.712 | he.react.dev/learn/managing-state | 0.706 | 18.react.dev/learn/managing-state | 0.704 |
| crawl4ai-raw | #1 | react.dev/learn/preserving-and-resetting-state | 0.712 | he.react.dev/learn/managing-state | 0.706 | 18.react.dev/learn/managing-state | 0.704 |
| scrapy+md | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |
| crawlee | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |
| colly+md | #1 | react.dev/learn/preserving-and-resetting-state#opt | 0.736 | react.dev/learn/preserving-and-resetting-state#dif | 0.736 | react.dev/learn/preserving-and-resetting-state | 0.736 |
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
| colly+md | #1 | react.dev/reference/react/useEffect | 0.742 | react.dev/reference/react/useEffect#reference | 0.742 | react.dev/reference/react/useEffectEvent | 0.634 |
| playwright | #1 | react.dev/reference/react/useEffect | 0.742 | react.dev/reference/react/useEffectEvent | 0.634 | react.dev/reference/react/useEffect | 0.625 |


**Q3: How do I create and use context in React?** [api-function]
*(expects URL containing: `useContext`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/createContext | 0.730 | react.dev/learn/passing-data-deeply-with-context | 0.705 | react.dev/learn/passing-data-deeply-with-context | 0.701 |
| crawl4ai | #1 | react.dev/reference/react/createContext | 0.744 | react.dev/learn/passing-data-deeply-with-context | 0.732 | react.dev/reference/react/createContext | 0.715 |
| crawl4ai-raw | #1 | react.dev/reference/react/createContext | 0.744 | react.dev/learn/passing-data-deeply-with-context | 0.732 | react.dev/reference/react/createContext | 0.715 |
| scrapy+md | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/learn/passing-data-deeply-with-context | 0.705 | react.dev/learn/passing-data-deeply-with-context | 0.701 |
| crawlee | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/learn/passing-data-deeply-with-context | 0.710 | react.dev/reference/react/createContext | 0.708 |
| colly+md | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/reference/react/createContext | 0.708 | react.dev/learn/passing-data-deeply-with-context#s | 0.705 |
| playwright | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/reference/react/createContext | 0.708 | react.dev/learn/passing-data-deeply-with-context | 0.705 |


**Q4: What is JSX and how does React use it?** [conceptual]
*(expects URL containing: `writing-markup-with-jsx`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.707 |
| crawl4ai | #1 | react.dev/learn/writing-markup-with-jsx | 0.732 | react.dev/learn/writing-markup-with-jsx | 0.680 | he.react.dev/learn/describing-the-ui | 0.680 |
| crawl4ai-raw | #1 | react.dev/learn/writing-markup-with-jsx | 0.732 | react.dev/learn/writing-markup-with-jsx | 0.680 | he.react.dev/learn/describing-the-ui | 0.680 |
| scrapy+md | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.707 |
| crawlee | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.707 |
| colly+md | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.707 |
| playwright | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.707 |


**Q5: How do I render lists and use keys in React?** [code-example]
*(expects URL containing: `rendering-lists`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.701 |
| crawl4ai | #1 | react.dev/learn/rendering-lists | 0.751 | de.react.dev/learn/describing-the-ui | 0.733 | 18.react.dev/learn/describing-the-ui | 0.733 |
| crawl4ai-raw | #1 | react.dev/learn/rendering-lists | 0.751 | de.react.dev/learn/describing-the-ui | 0.733 | 18.react.dev/learn/describing-the-ui | 0.733 |
| scrapy+md | #5 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.700 |
| crawlee | #5 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.698 |
| colly+md | #6 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.700 |
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
| colly+md | #1 | react.dev/reference/react/useRef#returns | 0.758 | react.dev/reference/react/useRef | 0.758 | react.dev/reference/react/useRef#reference | 0.758 |
| playwright | #1 | react.dev/reference/react/useRef | 0.758 | react.dev/learn/referencing-values-with-refs | 0.719 | react.dev/reference/react/useRef | 0.674 |


**Q7: How do I pass props between React components?** [conceptual]
*(expects URL containing: `passing-props`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |
| crawl4ai | #2 | de.react.dev/learn/describing-the-ui | 0.761 | react.dev/learn/passing-props-to-a-component | 0.758 | az.react.dev/learn/describing-the-ui | 0.755 |
| crawl4ai-raw | #2 | de.react.dev/learn/describing-the-ui | 0.761 | react.dev/learn/passing-props-to-a-component | 0.758 | az.react.dev/learn/describing-the-ui | 0.755 |
| scrapy+md | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |
| crawlee | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |
| colly+md | #1 | react.dev/learn/passing-props-to-a-component#passi | 0.787 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 |
| playwright | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |


**Q8: How do I conditionally render content in React?** [code-example]
*(expects URL containing: `conditional-rendering`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn | 0.750 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/describing-the-ui | 0.703 |
| crawl4ai | #10 | 18.react.dev/learn/describing-the-ui | 0.759 | react.dev/learn/describing-the-ui | 0.751 | de.react.dev/learn/describing-the-ui | 0.750 |
| crawl4ai-raw | #10 | 18.react.dev/learn/describing-the-ui | 0.759 | react.dev/learn/describing-the-ui | 0.751 | de.react.dev/learn/describing-the-ui | 0.750 |
| scrapy+md | #3 | react.dev/learn | 0.748 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 |
| crawlee | #2 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/describing-the-ui | 0.705 |
| colly+md | #3 | react.dev/learn#components | 0.748 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 |
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
| colly+md | #1 | react.dev/reference/react/useMemo#how-to-tell-if-a | 0.736 | react.dev/reference/react/useMemo | 0.736 | react.dev/learn/react-compiler/introduction | 0.649 |
| playwright | #1 | react.dev/reference/react/useMemo | 0.736 | react.dev/learn/react-compiler/introduction | 0.649 | react.dev/reference/react/useMemo | 0.644 |


**Q10: How do I use the useState hook in React?** [api-function]
*(expects URL containing: `useState`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useState | 0.753 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |
| crawl4ai | #1 | react.dev/reference/react/useState | 0.719 | 18.react.dev/learn | 0.698 | he.react.dev/learn | 0.695 |
| crawl4ai-raw | #1 | react.dev/reference/react/useState | 0.719 | 18.react.dev/learn | 0.698 | he.react.dev/learn | 0.695 |
| scrapy+md | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn | 0.682 |
| crawlee | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |
| colly+md | #1 | react.dev/reference/react/useState#storing-informa | 0.751 | react.dev/reference/react/useState | 0.751 | react.dev/reference/react/useState#setstate | 0.751 |
| playwright | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |


**Q11: How do I use the useCallback hook in React?** [api-function]
*(expects URL containing: `useCallback`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.656 | react.dev/reference/react/useCallback | 0.643 |
| crawl4ai | #1 | react.dev/reference/react/useCallback | 0.703 | react.dev/reference/react/useCallback | 0.681 | react.dev/learn/typescript | 0.668 |
| crawl4ai-raw | #1 | react.dev/reference/react/useCallback | 0.703 | react.dev/reference/react/useCallback | 0.681 | react.dev/learn/typescript | 0.668 |
| scrapy+md | #1 | react.dev/reference/react/useCallback | 0.747 | react.dev/learn/typescript | 0.655 | react.dev/reference/react/useCallback | 0.644 |
| crawlee | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.655 | react.dev/reference/react/useCallback | 0.644 |
| colly+md | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.655 | react.dev/learn/typescript#typescript-with-react-c | 0.655 |
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
| crawl4ai | #1 | react.dev/learn/responding-to-events | 0.690 | 18.react.dev/learn | 0.689 | az.react.dev/learn | 0.686 |
| crawl4ai-raw | #1 | react.dev/learn/responding-to-events | 0.690 | 18.react.dev/learn | 0.689 | az.react.dev/learn | 0.687 |
| scrapy+md | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.668 | react.dev/learn | 0.668 |
| crawlee | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.668 | react.dev/learn/adding-interactivity | 0.645 |
| colly+md | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn/responding-to-events#passing-event | 0.699 | react.dev/learn#components | 0.668 |
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
| colly+md | #1 | react.dev/blog/2022/03/29/react-v18#suspense-in-da | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18#suspense-in-da | 0.712 |
| playwright | #9 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.712 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.681 |


**Q15: How do I add interactivity to React components?** [conceptual]
*(expects URL containing: `adding-interactivity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |
| crawl4ai | #13 | 18.react.dev | 0.830 | hi.react.dev/ | 0.830 | react.dev | 0.830 |
| crawl4ai-raw | #13 | vi.react.dev/ | 0.830 | ru.react.dev/ | 0.830 | hi.react.dev/ | 0.830 |
| scrapy+md | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/learn/state-a-components-memory | 0.724 |
| crawlee | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.685 |
| colly+md | #2 | react.dev/learn | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |
| playwright | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |


**Q16: How do I install and set up a new React project?** [conceptual]
*(expects URL containing: `installation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn/add-react-to-an-existing-project | 0.672 | react.dev/learn/react-compiler/installation | 0.660 | react.dev/ | 0.653 |
| crawl4ai | #1 | 18.react.dev/learn/installation | 0.738 | he.react.dev/learn/installation | 0.738 | he.react.dev/learn/installation | 0.727 |
| crawl4ai-raw | #1 | 18.react.dev/learn/installation | 0.738 | he.react.dev/learn/installation | 0.738 | he.react.dev/learn/installation | 0.727 |
| scrapy+md | #2 | react.dev/learn/add-react-to-an-existing-project | 0.672 | react.dev/learn/react-compiler/installation | 0.660 | react.dev/learn/creating-a-react-app | 0.642 |
| crawlee | #4 | react.dev/learn/setup | 0.693 | react.dev/learn/react-compiler | 0.678 | react.dev/learn/add-react-to-an-existing-project | 0.672 |
| colly+md | #5 | react.dev/learn/setup | 0.693 | react.dev/learn/react-compiler | 0.678 | react.dev/learn/add-react-to-an-existing-project#u | 0.672 |
| playwright | #4 | react.dev/learn/setup | 0.693 | react.dev/learn/react-compiler | 0.678 | react.dev/learn/add-react-to-an-existing-project | 0.672 |


</details>

## wikipedia-python

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 40% (4/10) | 40% (4/10) | 40% (4/10) | 40% (4/10) | 40% (4/10) | 0.400 | 2380 | 50 |
| crawl4ai | 30% (3/10) | 30% (3/10) | 40% (4/10) | 40% (4/10) | 40% (4/10) | 0.320 | 1395 | 50 |
| crawl4ai-raw | 30% (3/10) | 30% (3/10) | 40% (4/10) | 40% (4/10) | 40% (4/10) | 0.320 | 1391 | 50 |
| **markcrawl** | 20% (2/10) | 20% (2/10) | 20% (2/10) | 20% (2/10) | 20% (2/10) | 0.200 | 1044 | 50 |
| playwright | 20% (2/10) | 20% (2/10) | 20% (2/10) | 20% (2/10) | 20% (2/10) | 0.200 | 1513 | 50 |
| scrapy+md | 10% (1/10) | 10% (1/10) | 10% (1/10) | 10% (1/10) | 10% (1/10) | 0.100 | 1278 | 50 |
| colly+md | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for wikipedia-python</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: Who created the Python programming language?** [factual-lookup]
*(expects URL containing: `Python_(programming_language)`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.619 | en.wikipedia.org/wiki/Python_(programming_language | 0.553 | en.wikipedia.org/wiki/Python_(programming_language | 0.549 |
| crawl4ai | #5 | en.wikipedia.org/w/index.php?action=edit&title=Pyt | 0.680 | en.wikipedia.org/w/index.php?action=edit&title=Pyt | 0.582 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.565 |
| crawl4ai-raw | #5 | en.wikipedia.org/w/index.php?action=edit&title=Pyt | 0.680 | en.wikipedia.org/w/index.php?action=edit&title=Pyt | 0.582 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.565 |
| scrapy+md | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.553 | en.wikipedia.org/wiki/Python_(programming_language | 0.549 | en.wikipedia.org/wiki/Python_(programming_language | 0.523 |
| crawlee | #1 | en.wikipedia.org/w/index.php?title=Python_(program | 0.680 | en.wikipedia.org/w/index.php?title=Python_(program | 0.582 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.581 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | en.wikipedia.org/w/index.php?title=Python_(program | 0.680 | en.wikipedia.org/w/index.php?title=Python_(program | 0.582 | en.wikipedia.org/w/index.php?title=Python_(program | 0.553 |


**Q2: What is the Python Software Foundation?** [factual-lookup]
*(expects URL containing: `Python_Software_Foundation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.491 | en.wikipedia.org/wiki/Python_(programming_language | 0.478 | en.wikipedia.org/wiki/Python_(programming_language | 0.465 |
| crawl4ai | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.768 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.741 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.666 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.768 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.741 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.666 |
| scrapy+md | miss | en.wikipedia.org/wiki/Zope_2 | 0.519 | en.wikipedia.org/wiki/Python_(programming_language | 0.491 | en.wikipedia.org/wiki/Python_(programming_language | 0.490 |
| crawlee | #1 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.752 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.713 | en.wikipedia.org/wiki/Python_Software_Foundation | 0.649 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | en.wikipedia.org/w/index.php?title=Python_(program | 0.491 | en.wikipedia.org/w/index.php?title=Python_(program | 0.491 | en.wikipedia.org/wiki/Python_(programming_language | 0.491 |


**Q3: Who is Guido van Rossum?** [factual-lookup]
*(expects URL containing: `Guido_van_Rossum`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.428 | en.wikipedia.org/wiki/Python_(programming_language | 0.419 | en.wikipedia.org/wiki/Glue_language | 0.406 |
| crawl4ai | #1 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.778 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.726 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.708 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.778 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.726 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.708 |
| scrapy+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.465 | en.wikipedia.org/wiki/Python_(programming_language | 0.419 | en.wikipedia.org/wiki/Python_(programming_language | 0.418 |
| crawlee | #1 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.808 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.755 | en.wikipedia.org/wiki/Guido_van_Rossum | 0.703 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | en.wikipedia.org/w/index.php?title=Python_(program | 0.489 | en.wikipedia.org/w/index.php?title=Python_(program | 0.465 | en.wikipedia.org/w/index.php?title=Python_(program | 0.465 |


**Q4: What is CPython and how does it work?** [factual-lookup]
*(expects URL containing: `CPython`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.526 | en.wikipedia.org/wiki/Python_(programming_language | 0.512 | en.wikipedia.org/wiki/Python_(programming_language | 0.496 |
| crawl4ai | miss | en.wikipedia.org/w/index.php?action=edit&title=Pyt | 0.563 | en.wikipedia.org/wiki/Python_(programming_language | 0.516 | en.wikipedia.org/w/index.php?printable=yes&title=P | 0.512 |
| crawl4ai-raw | miss | en.wikipedia.org/w/index.php?action=edit&title=Pyt | 0.563 | en.wikipedia.org/wiki/Python_(programming_language | 0.516 | en.wikipedia.org/w/index.php?printable=yes&title=P | 0.512 |
| scrapy+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.526 | en.wikipedia.org/wiki/Python_(programming_language | 0.496 | en.wikipedia.org/wiki/Python_(programming_language | 0.486 |
| crawlee | miss | en.wikipedia.org/w/index.php?title=Python_(program | 0.526 | en.wikipedia.org/wiki/Python_(programming_language | 0.526 | en.wikipedia.org/w/index.php?title=Python_(program | 0.512 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | en.wikipedia.org/wiki/CPython | 0.616 | en.wikipedia.org/wiki/CPython | 0.596 | en.wikipedia.org/wiki/Python_(programming_language | 0.526 |


**Q5: How does Python compare to other programming languages?** [conceptual]
*(expects URL containing: `Comparison_of_programming_languages`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.664 | en.wikipedia.org/wiki/Python_(programming_language | 0.648 | en.wikipedia.org/wiki/Python_(programming_language | 0.641 |
| crawl4ai | miss | en.wikipedia.org/w/index.php?printable=yes&title=P | 0.682 | en.wikipedia.org/w/index.php?oldid=1349031340&titl | 0.680 | en.wikipedia.org/wiki/Python_(programming_language | 0.672 |
| crawl4ai-raw | miss | en.wikipedia.org/w/index.php?printable=yes&title=P | 0.682 | en.wikipedia.org/w/index.php?oldid=1349031340&titl | 0.680 | en.wikipedia.org/wiki/Python_(programming_language | 0.672 |
| scrapy+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.664 | en.wikipedia.org/wiki/Python_(programming_language | 0.648 | en.wikipedia.org/wiki/Python_(programming_language | 0.629 |
| crawlee | miss | en.wikipedia.org/w/index.php?title=Python_(program | 0.664 | en.wikipedia.org/wiki/Python_(programming_language | 0.664 | en.wikipedia.org/w/index.php?title=Python_(program | 0.664 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.664 | en.wikipedia.org/w/index.php?title=Python_(program | 0.664 | en.wikipedia.org/w/index.php?title=Python_(program | 0.664 |


**Q6: What is NumPy and what is it used for?** [factual-lookup]
*(expects URL containing: `NumPy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/NumPy | 0.769 | en.wikipedia.org/wiki/NumPy | 0.702 | en.wikipedia.org/wiki/NumPy | 0.655 |
| crawl4ai | miss | en.wikipedia.org/w/index.php?printable=yes&title=P | 0.448 | en.wikipedia.org/w/index.php?oldid=1349031340&titl | 0.442 | en.wikipedia.org/wiki/Python_(programming_language | 0.441 |
| crawl4ai-raw | miss | en.wikipedia.org/w/index.php?printable=yes&title=P | 0.448 | en.wikipedia.org/w/index.php?oldid=1349031340&titl | 0.442 | en.wikipedia.org/wiki/Python_(programming_language | 0.441 |
| scrapy+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.418 | en.wikipedia.org/wiki/Python_(programming_language | 0.416 | en.wikipedia.org/wiki/Python_(programming_language | 0.415 |
| crawlee | miss | en.wikipedia.org/w/index.php?title=Python_(program | 0.426 | en.wikipedia.org/wiki/Python_(programming_language | 0.418 | en.wikipedia.org/w/index.php?title=Python_(program | 0.418 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | en.wikipedia.org/wiki/Cython | 0.488 | en.wikipedia.org/wiki/Cython | 0.429 | en.wikipedia.org/w/index.php?title=Python_(program | 0.426 |


**Q7: What is SQLAlchemy and how is it used with Python?** [factual-lookup]
*(expects URL containing: `SQLAlchemy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.413 | en.wikipedia.org/wiki/Mako_(template_engine) | 0.401 | en.wikipedia.org/wiki/Python_(programming_language | 0.369 |
| crawl4ai | miss | en.wikipedia.org/w/index.php?oldid=1349031340&titl | 0.386 | en.wikipedia.org/w/index.php?printable=yes&title=P | 0.386 | en.wikipedia.org/wiki/Python_(programming_language | 0.386 |
| crawl4ai-raw | miss | en.wikipedia.org/w/index.php?printable=yes&title=P | 0.386 | en.wikipedia.org/wiki/Python_(programming_language | 0.386 | en.wikipedia.org/w/index.php?oldid=1349031340&titl | 0.386 |
| scrapy+md | miss | en.wikipedia.org/wiki/Web2py | 0.490 | en.wikipedia.org/wiki/Anaconda_(Python_distributio | 0.370 | en.wikipedia.org/wiki/Python_(programming_language | 0.369 |
| crawlee | miss | en.wikipedia.org/w/index.php?title=Python_(program | 0.369 | en.wikipedia.org/w/index.php?title=Python_(program | 0.369 | en.wikipedia.org/wiki/Python_(programming_language | 0.369 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | en.wikipedia.org/w/index.php?title=Python_(program | 0.369 | en.wikipedia.org/w/index.php?title=Python_(program | 0.369 | en.wikipedia.org/wiki/Python_(programming_language | 0.369 |


**Q8: What is metaprogramming in computer science?** [conceptual]
*(expects URL containing: `Metaprogramming`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Procedural_programming | 0.535 | en.wikipedia.org/wiki/Procedural_programming | 0.508 | en.wikipedia.org/wiki/Procedural_programming | 0.505 |
| crawl4ai | miss | en.wikipedia.org/wiki/Programming_paradigm | 0.592 | en.wikipedia.org/wiki/Imperative_programming | 0.565 | en.wikipedia.org/wiki/Procedural_programming | 0.539 |
| crawl4ai-raw | miss | en.wikipedia.org/wiki/Programming_paradigm | 0.592 | en.wikipedia.org/wiki/Imperative_programming | 0.565 | en.wikipedia.org/wiki/Procedural_programming | 0.539 |
| scrapy+md | miss | en.wikipedia.org/wiki/THE_multiprogramming_system | 0.383 | en.wikipedia.org/wiki/Python_(programming_language | 0.382 | en.wikipedia.org/wiki/Python_(programming_language | 0.376 |
| crawlee | miss | en.wikipedia.org/wiki/Programming_paradigm | 0.602 | en.wikipedia.org/wiki/Imperative_programming | 0.549 | en.wikipedia.org/wiki/Procedural_programming | 0.547 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | en.wikipedia.org/wiki/Programming_language | 0.489 | en.wikipedia.org/wiki/Programming_language | 0.465 | en.wikipedia.org/wiki/Programming_language | 0.459 |


**Q9: What are list comprehensions in programming?** [conceptual]
*(expects URL containing: `List_comprehension`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.434 | en.wikipedia.org/wiki/Category:Concurrent_programm | 0.425 | en.wikipedia.org/wiki/Wikipedia:Contents | 0.414 |
| crawl4ai | miss | en.wikipedia.org/wiki/Reflective_programming | 0.447 | en.wikipedia.org/wiki/Programming_paradigm | 0.437 | en.wikipedia.org/wiki/Python_(programming_language | 0.435 |
| crawl4ai-raw | miss | en.wikipedia.org/wiki/Reflective_programming | 0.447 | en.wikipedia.org/wiki/Programming_paradigm | 0.437 | en.wikipedia.org/w/index.php?printable=yes&title=P | 0.435 |
| scrapy+md | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.434 | en.wikipedia.org/wiki/Python_(programming_language | 0.362 | en.wikipedia.org/wiki/Python_(programming_language | 0.352 |
| crawlee | miss | en.wikipedia.org/w/index.php?title=Python_(program | 0.434 | en.wikipedia.org/w/index.php?title=Python_(program | 0.434 | en.wikipedia.org/wiki/Python_(programming_language | 0.434 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | en.wikipedia.org/w/index.php?title=Python_(program | 0.434 | en.wikipedia.org/w/index.php?title=Python_(program | 0.434 | en.wikipedia.org/wiki/Python_(programming_language | 0.434 |


**Q10: How does memory management work in programming?** [conceptual]
*(expects URL containing: `Memory_management`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Strongly_typed | 0.552 | en.wikipedia.org/wiki/Programming_language | 0.480 | en.wikipedia.org/wiki/Strongly_typed | 0.432 |
| crawl4ai | #1 | en.wikipedia.org/wiki/Memory_management | 0.703 | en.wikipedia.org/wiki/Memory_management | 0.680 | en.wikipedia.org/wiki/Memory_management | 0.676 |
| crawl4ai-raw | #1 | en.wikipedia.org/wiki/Memory_management | 0.703 | en.wikipedia.org/wiki/Memory_management | 0.680 | en.wikipedia.org/wiki/Memory_management | 0.676 |
| scrapy+md | miss | en.wikipedia.org/wiki/THE_multiprogramming_system | 0.397 | en.wikipedia.org/wiki/Python_(programming_language | 0.389 | en.wikipedia.org/wiki/THE_multiprogramming_system | 0.376 |
| crawlee | #1 | en.wikipedia.org/wiki/Memory_management | 0.685 | en.wikipedia.org/wiki/Memory_management | 0.672 | en.wikipedia.org/wiki/Operating_system | 0.649 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | en.wikipedia.org/wiki/C_(programming_language) | 0.711 | en.wikipedia.org/wiki/C_(programming_language) | 0.695 | en.wikipedia.org/wiki/C_(programming_language) | 0.522 |


</details>

## stripe-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | 67% (12/18) | 72% (13/18) | 72% (13/18) | 78% (14/18) | 78% (14/18) | 0.699 | 3266 | 500 |
| crawlee | 39% (7/18) | 61% (11/18) | 78% (14/18) | 89% (16/18) | 89% (16/18) | 0.548 | 37285 | 500 |
| playwright | 33% (6/18) | 61% (11/18) | 72% (13/18) | 89% (16/18) | 89% (16/18) | 0.515 | 36635 | 500 |
| colly+md | 39% (7/18) | 50% (9/18) | 67% (12/18) | 89% (16/18) | 89% (16/18) | 0.507 | 35156 | 498 |
| crawl4ai | 28% (5/18) | 50% (9/18) | 67% (12/18) | 78% (14/18) | 78% (14/18) | 0.416 | 7497 | 490 |
| crawl4ai-raw | 28% (5/18) | 50% (9/18) | 67% (12/18) | 78% (14/18) | 78% (14/18) | 0.414 | 10234 | 494 |
| scrapy+md | 22% (4/18) | 39% (7/18) | 44% (8/18) | 50% (9/18) | 61% (11/18) | 0.329 | 9648 | 498 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for stripe-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I create a payment intent with Stripe?** [api-function]
*(expects URL containing: `payment-intent`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/upgrades/manage-payment-methods | 0.724 | docs.stripe.com/apple-pay | 0.669 | docs.stripe.com/billing/subscriptions/build-subscr | 0.616 |
| crawl4ai | #3 | docs.stripe.com/google-pay | 0.832 | docs.stripe.com/payments/accept-a-payment?api-inte | 0.772 | docs.stripe.com/payments/payment-intents | 0.762 |
| crawl4ai-raw | #3 | docs.stripe.com/google-pay | 0.832 | docs.stripe.com/payments/accept-a-payment?api-inte | 0.772 | docs.stripe.com/payments/payment-intents | 0.762 |
| scrapy+md | #1 | docs.stripe.com/payments/payment-intents | 0.766 | docs.stripe.com/payments/payment-intents/migration | 0.703 | docs.stripe.com/payments/payment-intents/migration | 0.703 |
| crawlee | #1 | docs.stripe.com/payments/payment-intents | 0.769 | docs.stripe.com/payments/payment-intents | 0.763 | docs.stripe.com/payments/accept-a-payment-deferred | 0.758 |
| colly+md | #3 | docs.stripe.com/api/payment/intents/create#create/ | 0.846 | docs.stripe.com/payments/accept-a-payment?payment- | 0.791 | docs.stripe.com/payments/payment-intents | 0.769 |
| playwright | #2 | docs.stripe.com/api/payment_intents/create | 0.846 | docs.stripe.com/payments/payment-intents | 0.769 | docs.stripe.com/payments/payment-intents | 0.763 |


**Q2: How do I handle webhooks from Stripe?** [api-function]
*(expects URL containing: `webhook`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | docs.stripe.com/error-handling | 0.712 | docs.stripe.com/billing/taxes/collect-taxes | 0.625 | docs.stripe.com/billing/subscriptions/build-subscr | 0.624 |
| crawl4ai | #1 | docs.stripe.com/webhooks | 0.724 | docs.stripe.com/payments/checkout/custom-success-p | 0.705 | docs.stripe.com/get-started/use-cases/saas-subscri | 0.683 |
| crawl4ai-raw | #1 | docs.stripe.com/webhooks | 0.723 | docs.stripe.com/payments/checkout/custom-success-p | 0.705 | docs.stripe.com/get-started/use-cases/saas-subscri | 0.683 |
| scrapy+md | #1 | docs.stripe.com/webhooks?snapshot-or-thin=thin | 0.716 | docs.stripe.com/webhooks?snapshot-or-thin=thin | 0.660 | docs.stripe.com/webhooks?snapshot-or-thin=thin | 0.659 |
| crawlee | #1 | docs.stripe.com/webhooks/handling-payment-events | 0.789 | docs.stripe.com/billing/subscriptions/webhooks | 0.770 | docs.stripe.com/webhooks/quickstart | 0.738 |
| colly+md | #1 | docs.stripe.com/webhooks/handling-payment-events | 0.789 | docs.stripe.com/webhooks/quickstart | 0.738 | docs.stripe.com/webhooks | 0.719 |
| playwright | #1 | docs.stripe.com/webhooks/handling-payment-events | 0.789 | docs.stripe.com/billing/subscriptions/webhooks | 0.770 | docs.stripe.com/webhooks/quickstart | 0.738 |


**Q3: How do I set up Stripe subscriptions?** [api-function]
*(expects URL containing: `subscription`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.715 | docs.stripe.com/billing/subscriptions/import-subsc | 0.697 | docs.stripe.com/billing/taxes/migration | 0.687 |
| crawl4ai | #1 | docs.stripe.com/connect/subscriptions | 0.777 | docs.stripe.com/payments/advanced/build-subscripti | 0.740 | docs.stripe.com/billing/subscriptions/build-subscr | 0.737 |
| crawl4ai-raw | #1 | docs.stripe.com/connect/subscriptions | 0.776 | docs.stripe.com/payments/advanced/build-subscripti | 0.740 | docs.stripe.com/billing/subscriptions/build-subscr | 0.737 |
| scrapy+md | #14 | docs.stripe.com/tax/set-up | 0.654 | docs.stripe.com/get-started/development-environmen | 0.647 | docs.stripe.com/js/elements_object/create_link_aut | 0.636 |
| crawlee | #1 | docs.stripe.com/connect/subscriptions | 0.786 | docs.stripe.com/no-code/subscriptions | 0.782 | docs.stripe.com/subscriptions | 0.782 |
| colly+md | #1 | docs.stripe.com/connect/subscriptions | 0.786 | docs.stripe.com/no-code/subscriptions | 0.782 | docs.stripe.com/subscriptions | 0.782 |
| playwright | #1 | docs.stripe.com/connect/subscriptions | 0.786 | docs.stripe.com/no-code/subscriptions | 0.782 | docs.stripe.com/subscriptions | 0.782 |


**Q4: How do I authenticate with the Stripe API?** [api-function]
*(expects URL containing: `authentication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #34 | docs.stripe.com/keys | 0.695 | docs.stripe.com/get-started/account/set-up | 0.621 | docs.stripe.com/error-handling | 0.610 |
| crawl4ai | #31 | docs.stripe.com/get-started/development-environmen | 0.695 | docs.stripe.com/samples/identity/redirect | 0.682 | docs.stripe.com/get-started/use-cases/in-person-pa | 0.665 |
| crawl4ai-raw | miss | docs.stripe.com/get-started/development-environmen | 0.695 | docs.stripe.com/samples/identity/redirect | 0.682 | docs.stripe.com/get-started/use-cases/in-person-pa | 0.666 |
| scrapy+md | #48 | docs.stripe.com/get-started/development-environmen | 0.677 | docs.stripe.com/get-started/api-request | 0.627 | docs.stripe.com/sdks | 0.606 |
| crawlee | #2 | docs.stripe.com/payments/3d-secure | 0.735 | docs.stripe.com/payments/mobile/without-card-authe | 0.701 | docs.stripe.com/payments/without-card-authenticati | 0.701 |
| colly+md | #2 | docs.stripe.com/payments/3d-secure | 0.735 | docs.stripe.com/payments/without-card-authenticati | 0.701 | docs.stripe.com/payments/mobile/without-card-authe | 0.701 |
| playwright | #2 | docs.stripe.com/payments/3d-secure | 0.735 | docs.stripe.com/payments/mobile/without-card-authe | 0.701 | docs.stripe.com/payments/without-card-authenticati | 0.701 |


**Q5: How do I handle errors in the Stripe API?** [api-function]
*(expects URL containing: `error-handling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/error-handling | 0.722 | docs.stripe.com/error-low-level | 0.701 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.696 |
| crawl4ai | miss | docs.stripe.com/api | 0.701 | docs.stripe.com/webhooks/quickstart | 0.661 | docs.stripe.com/api | 0.652 |
| crawl4ai-raw | miss | docs.stripe.com/api | 0.701 | docs.stripe.com/webhooks/quickstart | 0.661 | docs.stripe.com/api | 0.652 |
| scrapy+md | miss | docs.stripe.com/declines | 0.610 | docs.stripe.com/automated-testing | 0.609 | docs.stripe.com/declines/card | 0.592 |
| crawlee | miss | docs.stripe.com/webhooks/quickstart | 0.673 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.643 | docs.stripe.com/disputes/responding#decide | 0.600 |
| colly+md | miss | docs.stripe.com/get-started/checklist/go-live | 0.621 | docs.stripe.com/changelog/2020-08-27/adds-error-co | 0.611 | docs.stripe.com/api/events | 0.602 |
| playwright | miss | docs.stripe.com/webhooks/quickstart | 0.673 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.643 | docs.stripe.com/api/events | 0.602 |


**Q6: How do I process refunds with Stripe?** [api-function]
*(expects URL containing: `refund`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #46 | docs.stripe.com/billing/subscriptions/third-party- | 0.626 | docs.stripe.com/ach-deprecated | 0.621 | docs.stripe.com/billing/taxes/migration | 0.557 |
| crawl4ai | #6 | docs.stripe.com/payments/quickstart?platform=ios | 0.732 | docs.stripe.com/billing/subscriptions/third-party- | 0.716 | docs.stripe.com/connect/end-to-end-marketplace | 0.702 |
| crawl4ai-raw | #6 | docs.stripe.com/payments/quickstart?platform=ios | 0.732 | docs.stripe.com/billing/subscriptions/third-party- | 0.716 | docs.stripe.com/connect/end-to-end-marketplace | 0.702 |
| scrapy+md | #2 | docs.stripe.com/issuing/purchases/authorizations | 0.686 | docs.stripe.com/payments/customer-balance/refundin | 0.651 | docs.stripe.com/payments/charges-api | 0.642 |
| crawlee | #1 | docs.stripe.com/api/refunds | 0.778 | docs.stripe.com/payments/quickstart?platform=ios | 0.718 | docs.stripe.com/refunds | 0.714 |
| colly+md | #1 | docs.stripe.com/api/refunds | 0.778 | docs.stripe.com/refunds | 0.714 | docs.stripe.com/refunds#cancel-payment | 0.714 |
| playwright | #1 | docs.stripe.com/api/refunds | 0.778 | docs.stripe.com/payments/quickstart?platform=ios | 0.718 | docs.stripe.com/refunds | 0.714 |


**Q7: How do I use Stripe checkout for payments?** [js-rendered]
*(expects URL containing: `checkout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.646 | docs.stripe.com/upgrades/manage-payment-methods | 0.645 | docs.stripe.com/billing/subscriptions/build-subscr | 0.639 |
| crawl4ai | #1 | docs.stripe.com/checkout/quickstart | 0.715 | docs.stripe.com/checkout/embedded/quickstart | 0.715 | docs.stripe.com/payments/accept-a-payment?platform | 0.683 |
| crawl4ai-raw | #1 | docs.stripe.com/checkout/embedded/quickstart | 0.715 | docs.stripe.com/checkout/quickstart | 0.715 | docs.stripe.com/payments/accept-a-payment | 0.683 |
| scrapy+md | #6 | docs.stripe.com/payments | 0.665 | docs.stripe.com/payments | 0.663 | docs.stripe.com/llms.txt | 0.662 |
| crawlee | #2 | docs.stripe.com/payments/online-payments | 0.731 | docs.stripe.com/checkout/embedded/quickstart | 0.716 | docs.stripe.com/checkout/quickstart | 0.716 |
| colly+md | #4 | docs.stripe.com/payments/online-payments#compare-f | 0.731 | docs.stripe.com/payments/online-payments | 0.731 | docs.stripe.com/payments/pay-by-bank | 0.705 |
| playwright | #2 | docs.stripe.com/payments/online-payments | 0.731 | docs.stripe.com/checkout/quickstart | 0.716 | docs.stripe.com/checkout/embedded/quickstart | 0.716 |


**Q8: How do I test Stripe payments in development?** [code-example]
*(expects URL containing: `testing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/automated-testing | 0.680 | docs.stripe.com/billing/testing | 0.677 | docs.stripe.com/automated-testing | 0.663 |
| crawl4ai | #7 | docs.stripe.com/get-started/test-developer-integra | 0.732 | docs.stripe.com/tax/custom | 0.705 | docs.stripe.com/payments/link/instant-bank-payment | 0.700 |
| crawl4ai-raw | #7 | docs.stripe.com/get-started/test-developer-integra | 0.732 | docs.stripe.com/tax/custom | 0.705 | docs.stripe.com/payments/link/instant-bank-payment | 0.700 |
| scrapy+md | #2 | docs.stripe.com/get-started/test-developer-integra | 0.712 | docs.stripe.com/connect/testing | 0.703 | docs.stripe.com/automated-testing | 0.680 |
| crawlee | #4 | docs.stripe.com/get-started/test-developer-integra | 0.712 | docs.stripe.com/get-started/development-environmen | 0.707 | docs.stripe.com/payments/link/instant-bank-payment | 0.688 |
| colly+md | #4 | docs.stripe.com/get-started/test-developer-integra | 0.712 | docs.stripe.com/get-started/development-environmen | 0.707 | docs.stripe.com/payments/link/instant-bank-payment | 0.688 |
| playwright | #4 | docs.stripe.com/get-started/test-developer-integra | 0.712 | docs.stripe.com/get-started/development-environmen | 0.707 | docs.stripe.com/payments/link/instant-bank-payment | 0.688 |


**Q9: What are Stripe Connect and platform payments?** [conceptual]
*(expects URL containing: `connect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #28 | docs.stripe.com/ach-deprecated | 0.654 | docs.stripe.com/get-started/account/orgs/setup | 0.646 | docs.stripe.com/capital/overview | 0.636 |
| crawl4ai | #1 | docs.stripe.com/connect | 0.771 | docs.stripe.com/payments/klarna | 0.753 | docs.stripe.com/llms.txt | 0.714 |
| crawl4ai-raw | #1 | docs.stripe.com/connect | 0.771 | docs.stripe.com/payments/klarna | 0.753 | docs.stripe.com/llms.txt | 0.714 |
| scrapy+md | #4 | docs.stripe.com/llms.txt | 0.714 | docs.stripe.com/llms.txt | 0.686 | docs.stripe.com/payments/payment-methods/pmd-regis | 0.666 |
| crawlee | #1 | docs.stripe.com/connect | 0.772 | docs.stripe.com/connect | 0.759 | docs.stripe.com/connect/build-full-embedded-integr | 0.756 |
| colly+md | #1 | docs.stripe.com/connect | 0.772 | docs.stripe.com/connect | 0.759 | docs.stripe.com/payments/klarna | 0.755 |
| playwright | #1 | docs.stripe.com/connect | 0.772 | docs.stripe.com/connect | 0.759 | docs.stripe.com/connect/build-full-embedded-integr | 0.756 |


**Q10: How do I set up usage-based billing with Stripe?** [js-rendered]
*(expects URL containing: `usage-based`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/usage-based- | 0.799 | docs.stripe.com/billing | 0.752 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.718 |
| crawl4ai | #5 | docs.stripe.com/billing | 0.720 | docs.stripe.com/billing/subscriptions/billing-cycl | 0.679 | docs.stripe.com/llms.txt | 0.671 |
| crawl4ai-raw | #5 | docs.stripe.com/billing | 0.720 | docs.stripe.com/billing/subscriptions/billing-cycl | 0.679 | docs.stripe.com/llms.txt | 0.671 |
| scrapy+md | #1 | docs.stripe.com/billing/subscriptions/usage-based- | 0.718 | docs.stripe.com/billing/subscriptions/usage-based- | 0.681 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.672 |
| crawlee | #6 | docs.stripe.com/billing | 0.752 | docs.stripe.com/llms.txt | 0.671 | docs.stripe.com/tax/set-up | 0.671 |
| colly+md | #7 | docs.stripe.com/billing | 0.752 | docs.stripe.com/tax/set-up | 0.671 | docs.stripe.com/get-started/account/set-up#public- | 0.664 |
| playwright | #6 | docs.stripe.com/billing | 0.752 | docs.stripe.com/llms.txt | 0.671 | docs.stripe.com/tax/set-up | 0.671 |


**Q11: How do I manage Stripe API keys?** [api-function]
*(expects URL containing: `keys`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/keys | 0.760 | docs.stripe.com/keys-best-practices | 0.738 | docs.stripe.com/keys | 0.722 |
| crawl4ai | #4 | docs.stripe.com/samples/identity/redirect | 0.779 | docs.stripe.com/connect/marketplace/quickstart | 0.753 | docs.stripe.com/connect/saas/quickstart | 0.752 |
| crawl4ai-raw | #4 | docs.stripe.com/samples/identity/redirect | 0.779 | docs.stripe.com/connect/saas/quickstart | 0.753 | docs.stripe.com/connect/marketplace/quickstart | 0.752 |
| scrapy+md | miss | docs.stripe.com/radar/reviews/auth-and-capture | 0.677 | docs.stripe.com/billing/subscriptions/prorations | 0.677 | docs.stripe.com/get-started/api-request | 0.671 |
| crawlee | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/samples/identity/redirect | 0.779 | docs.stripe.com/connect/saas/quickstart | 0.752 |
| colly+md | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/sandboxes/dashboard/manage-access# | 0.819 | docs.stripe.com/sandboxes/dashboard/manage-access# | 0.761 |
| playwright | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/samples/identity/redirect | 0.779 | docs.stripe.com/connect/marketplace/quickstart | 0.753 |


**Q12: How do I handle Stripe rate limits?** [api-function]
*(expects URL containing: `rate-limits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/rate-limits | 0.720 | docs.stripe.com/rate-limits | 0.704 | docs.stripe.com/rate-limits | 0.702 |
| crawl4ai | miss | docs.stripe.com/testing | 0.670 | docs.stripe.com/payments/payment-method-rules | 0.603 | docs.stripe.com/tax/custom | 0.575 |
| crawl4ai-raw | miss | docs.stripe.com/testing | 0.670 | docs.stripe.com/payments/payment-method-rules | 0.603 | docs.stripe.com/payments/payto | 0.580 |
| scrapy+md | miss | docs.stripe.com/testing | 0.674 | docs.stripe.com/disputes/prevention/card-testing | 0.593 | docs.stripe.com/products-prices/how-products-and-p | 0.577 |
| crawlee | miss | docs.stripe.com/testing | 0.674 | docs.stripe.com/billing/taxes/tax-rates | 0.625 | docs.stripe.com/money-management | 0.608 |
| colly+md | miss | docs.stripe.com/testing#cards | 0.674 | docs.stripe.com/testing | 0.673 | docs.stripe.com/billing/taxes/tax-rates | 0.625 |
| playwright | miss | docs.stripe.com/testing | 0.674 | docs.stripe.com/billing/taxes/tax-rates | 0.625 | docs.stripe.com/money-management | 0.608 |


**Q13: How do I use metadata with Stripe objects?** [api-function]
*(expects URL containing: `metadata`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/metadata/use-cases | 0.781 | docs.stripe.com/metadata/use-cases | 0.778 | docs.stripe.com/metadata/use-cases | 0.743 |
| crawl4ai | miss | docs.stripe.com/payments/payment-intents | 0.733 | docs.stripe.com/api | 0.727 | docs.stripe.com/api | 0.717 |
| crawl4ai-raw | miss | docs.stripe.com/payments/payment-intents | 0.733 | docs.stripe.com/api | 0.727 | docs.stripe.com/api | 0.717 |
| scrapy+md | miss | docs.stripe.com/payments/payment-intents | 0.734 | docs.stripe.com/payments/charges-api | 0.621 | docs.stripe.com/api/cards/object | 0.591 |
| crawlee | #4 | docs.stripe.com/payments/payment-intents | 0.741 | docs.stripe.com/stripe-data | 0.667 | docs.stripe.com/billing/subscriptions/analytics | 0.636 |
| colly+md | #6 | docs.stripe.com/payments/payment-intents | 0.734 | docs.stripe.com/api/idempotent/requests | 0.715 | docs.stripe.com/api/idempotent/requests | 0.708 |
| playwright | #6 | docs.stripe.com/payments/payment-intents | 0.741 | docs.stripe.com/api | 0.720 | docs.stripe.com/api | 0.715 |


**Q14: How do I set up Apple Pay with Stripe?** [js-rendered]
*(expects URL containing: `apple-pay`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/apple-pay | 0.747 | docs.stripe.com/apple-pay | 0.696 | docs.stripe.com/apple-pay | 0.695 |
| crawl4ai | #1 | docs.stripe.com/apple-pay | 0.754 | docs.stripe.com/apple-pay | 0.747 | docs.stripe.com/payments/quickstart?platform=ios | 0.725 |
| crawl4ai-raw | #1 | docs.stripe.com/apple-pay | 0.754 | docs.stripe.com/apple-pay | 0.747 | docs.stripe.com/payments/quickstart?platform=ios | 0.725 |
| scrapy+md | miss | docs.stripe.com/payments/payment-methods/pmd-regis | 0.680 | docs.stripe.com/payment-links/create | 0.641 | docs.stripe.com/payments/charges-api | 0.623 |
| crawlee | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.743 | docs.stripe.com/payments/quickstart?platform=ios | 0.703 |
| colly+md | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.743 | docs.stripe.com/apple-pay/cartes-bancaires | 0.728 |
| playwright | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.743 | docs.stripe.com/payments/quickstart?platform=ios | 0.703 |


**Q15: How do I issue cards with Stripe Issuing?** [api-function]
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.709 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.662 | docs.stripe.com/issuing/integration-guides/fleet | 0.662 |
| crawl4ai | #2 | docs.stripe.com/llms.txt | 0.804 | docs.stripe.com/issuing/direct | 0.764 | docs.stripe.com/issuing | 0.750 |
| crawl4ai-raw | #2 | docs.stripe.com/llms.txt | 0.804 | docs.stripe.com/issuing/direct | 0.764 | docs.stripe.com/issuing | 0.750 |
| scrapy+md | #14 | docs.stripe.com/llms.txt | 0.731 | docs.stripe.com/js/appendix/supported_locales | 0.698 | docs.stripe.com/js/custom_checkout | 0.698 |
| crawlee | #2 | docs.stripe.com/llms.txt | 0.804 | docs.stripe.com/issuing/direct | 0.756 | docs.stripe.com/issuing | 0.752 |
| colly+md | #1 | docs.stripe.com/issuing/direct | 0.752 | docs.stripe.com/issuing | 0.752 | docs.stripe.com/issuing | 0.750 |
| playwright | #2 | docs.stripe.com/llms.txt | 0.804 | docs.stripe.com/issuing/direct | 0.756 | docs.stripe.com/issuing/direct | 0.752 |


**Q16: How do I recover failed subscription payments?** [js-rendered]
*(expects URL containing: `revenue-recovery`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/revenue-recovery | 0.715 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.584 |
| crawl4ai | #3 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.594 |
| crawl4ai-raw | #3 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.594 |
| scrapy+md | #1 | docs.stripe.com/billing/revenue-recovery | 0.565 | docs.stripe.com/billing/revenue-recovery | 0.521 | docs.stripe.com/billing/revenue-recovery | 0.517 |
| crawlee | #3 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.585 |
| colly+md | #9 | docs.stripe.com/no-code/get-started#get-retain-sub | 0.704 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/no-code/get-started#quotes-invoice | 0.704 |
| playwright | #3 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.584 |


**Q17: How does Stripe handle tax calculation for billing?** [js-rendered]
*(expects URL containing: `billing/taxes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/taxes/tax-rates | 0.726 | docs.stripe.com/saas | 0.724 | docs.stripe.com/products-prices/how-products-and-p | 0.722 |
| crawl4ai | #3 | docs.stripe.com/tax | 0.806 | docs.stripe.com/payments/advanced/tax | 0.751 | docs.stripe.com/billing/taxes/tax-rates | 0.746 |
| crawl4ai-raw | #3 | docs.stripe.com/tax | 0.806 | docs.stripe.com/payments/advanced/tax | 0.751 | docs.stripe.com/billing/taxes/tax-rates | 0.746 |
| scrapy+md | #3 | docs.stripe.com/tax/set-up | 0.735 | docs.stripe.com/products-prices/how-products-and-p | 0.722 | docs.stripe.com/billing/taxes/collect-taxes?tax-ca | 0.690 |
| crawlee | #4 | docs.stripe.com/tax | 0.820 | docs.stripe.com/tax/set-up | 0.744 | docs.stripe.com/tax/set-up | 0.735 |
| colly+md | #4 | docs.stripe.com/tax | 0.820 | docs.stripe.com/tax/set-up | 0.744 | docs.stripe.com/tax/set-up | 0.735 |
| playwright | #4 | docs.stripe.com/tax | 0.820 | docs.stripe.com/tax/set-up | 0.744 | docs.stripe.com/tax/set-up | 0.735 |


**Q18: How do I migrate data to Stripe?** [conceptual]
*(expects URL containing: `data-migrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.stripe.com/billing/taxes/migration | 0.728 | docs.stripe.com/billing/taxes/migration | 0.722 | docs.stripe.com/get-started/data-migrations/pan-ex | 0.711 |
| crawl4ai | #5 | docs.stripe.com/stripe-data/import-external-data | 0.724 | docs.stripe.com/billing/taxes/migration | 0.714 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.708 |
| crawl4ai-raw | #5 | docs.stripe.com/stripe-data/import-external-data | 0.724 | docs.stripe.com/billing/taxes/migration | 0.714 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.708 |
| scrapy+md | miss | docs.stripe.com/sdks/stripejs-versioning | 0.605 | docs.stripe.com/sdks | 0.594 | docs.stripe.com/stripe-apps/patterns | 0.594 |
| crawlee | #9 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/payments/checkout/migration | 0.735 |
| colly+md | #8 | docs.stripe.com/payments/ach-direct-debit/migratin | 0.766 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/payments/checkout/migration | 0.735 |
| playwright | #9 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/payments/checkout/migration | 0.735 |


</details>

## blog-engineering

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| colly+md | 62% (5/8) | 75% (6/8) | 75% (6/8) | 88% (7/8) | 100% (8/8) | 0.715 | 6430 | 199 |
| **markcrawl** | 50% (4/8) | 75% (6/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.656 | 1830 | 200 |
| crawlee | 50% (4/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.649 | 6790 | 200 |
| playwright | 50% (4/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.649 | 6796 | 200 |
| crawl4ai-raw | 38% (3/8) | 62% (5/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.577 | 5967 | 200 |
| crawl4ai | 38% (3/8) | 62% (5/8) | 75% (6/8) | 100% (8/8) | 100% (8/8) | 0.570 | 5967 | 200 |
| scrapy+md | 38% (3/8) | 62% (5/8) | 62% (5/8) | 62% (5/8) | 62% (5/8) | 0.483 | 3439 | 200 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for blog-engineering</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How does GitHub handle Kubernetes at scale?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/infrastructure/kubernetes- | 0.706 | github.blog/engineering/infrastructure/kubernetes- | 0.611 | github.blog/engineering/infrastructure/glb-directo | 0.602 |
| crawl4ai | #2 | github.blog/enterprise-software/devops/ | 0.605 | github.blog/engineering/ | 0.595 | github.blog/news-insights/company-news/github-avai | 0.583 |
| crawl4ai-raw | #2 | github.blog/enterprise-software/devops/ | 0.606 | github.blog/engineering/ | 0.595 | github.blog/news-insights/company-news/github-avai | 0.583 |
| scrapy+md | #1 | github.blog/open-source/maintainers/kelsey-hightow | 0.594 | github.blog/tag/developer-experience/page/2/ | 0.588 | github.blog/engineering/ | 0.579 |
| crawlee | #2 | github.blog/enterprise-software/devops/ | 0.589 | github.blog/engineering/ | 0.579 | github.blog/engineering/architecture-optimization/ | 0.572 |
| colly+md | #1 | github.blog/engineering/architecture-optimization/ | 0.621 | github.blog/engineering/engineering-principles/git | 0.595 | github.blog/enterprise-software/collaboration/a-ch | 0.595 |
| playwright | #2 | github.blog/enterprise-software/devops/ | 0.589 | github.blog/engineering/ | 0.579 | github.blog/engineering/architecture-optimization/ | 0.572 |


**Q2: How does GitHub protect against DDoS attacks?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/platform-security/syn-floo | 0.652 | github.blog/news-insights/company-news/ddos-incide | 0.650 | github.blog/news-insights/company-news/sha-1-colli | 0.649 |
| crawl4ai | #6 | github.blog/news-insights/company-news/github-avai | 0.596 | github.blog/news-insights/company-news/addressing- | 0.578 | github.blog/news-insights/company-news/github-avai | 0.574 |
| crawl4ai-raw | #6 | github.blog/news-insights/company-news/github-avai | 0.596 | github.blog/news-insights/company-news/addressing- | 0.578 | github.blog/news-insights/company-news/github-avai | 0.574 |
| scrapy+md | #3 | github.blog/security/vulnerability-research/securi | 0.587 | github.blog/news-insights/company-news/security-al | 0.579 | github.blog/engineering/platform-security/finding- | 0.569 |
| crawlee | #1 | github.blog/engineering/platform-security/finding- | 0.569 | github.blog/news-insights/company-news/addressing- | 0.555 | github.blog/news-insights/company-news/github-avai | 0.551 |
| colly+md | #13 | github.blog/enterprise-software/governance-and-com | 0.565 | github.blog/security/supply-chain-security/strengt | 0.558 | github.blog/news-insights/company-news/github-avai | 0.551 |
| playwright | #1 | github.blog/engineering/platform-security/finding- | 0.569 | github.blog/news-insights/company-news/addressing- | 0.555 | github.blog/news-insights/company-news/github-avai | 0.551 |


**Q3: How does GitHub handle MySQL database operations?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/infrastructure/orchestrato | 0.715 | github.blog/engineering/infrastructure/orchestrato | 0.686 | github.blog/engineering/infrastructure/context-awa | 0.670 |
| crawl4ai | #1 | github.blog/engineering/infrastructure/ | 0.614 | github.blog/enterprise-software/automation/ | 0.535 | github.blog/engineering/ | 0.511 |
| crawl4ai-raw | #1 | github.blog/engineering/infrastructure/ | 0.614 | github.blog/enterprise-software/automation/ | 0.535 | github.blog/engineering/ | 0.511 |
| scrapy+md | #1 | github.blog/engineering/page/10/ | 0.631 | github.blog/engineering/page/10/ | 0.556 | github.blog/tag/insights/ | 0.541 |
| crawlee | #1 | github.blog/engineering/infrastructure/ | 0.601 | github.blog/enterprise-software/automation/ | 0.541 | github.blog/engineering/architecture-optimization/ | 0.501 |
| colly+md | #1 | github.blog/enterprise-software/automation/automat | 0.558 | github.blog/enterprise-software/automation/ | 0.541 | github.blog/enterprise-software/automation/automat | 0.529 |
| playwright | #1 | github.blog/engineering/infrastructure/ | 0.601 | github.blog/enterprise-software/automation/ | 0.541 | github.blog/engineering/architecture-optimization/ | 0.501 |


**Q4: How does GitHub handle load balancing?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/infrastructure/glb-directo | 0.693 | github.blog/engineering/infrastructure/glb-directo | 0.621 | github.blog/engineering/architecture-optimization/ | 0.572 |
| crawl4ai | #7 | github.blog/news-insights/company-news/addressing- | 0.565 | github.blog/news-insights/company-news/github-avai | 0.564 | github.blog/news-insights/company-news/github-avai | 0.561 |
| crawl4ai-raw | #5 | github.blog/news-insights/company-news/addressing- | 0.565 | github.blog/news-insights/company-news/github-avai | 0.564 | github.blog/news-insights/company-news/github-avai | 0.561 |
| scrapy+md | #1 | github.blog/engineering/page/10/ | 0.614 | github.blog/news-insights/company-news/github-avai | 0.524 | github.blog/tag/github-availability-report/ | 0.514 |
| crawlee | #3 | github.blog/news-insights/company-news/github-avai | 0.544 | github.blog/news-insights/company-news/addressing- | 0.540 | github.blog/engineering/how-we-use-github-to-be-mo | 0.531 |
| colly+md | #2 | github.blog/news-insights/company-news/github-avai | 0.544 | github.blog/engineering/engineering-principles/git | 0.528 | github.blog/enterprise-software/automation/dependa | 0.528 |
| playwright | #3 | github.blog/news-insights/company-news/github-avai | 0.544 | github.blog/news-insights/company-news/addressing- | 0.540 | github.blog/engineering/how-we-use-github-to-be-mo | 0.531 |


**Q5: What is GitHub's approach to platform security?** [conceptual]
*(expects URL containing: `platform-security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | github.blog/security/subresource-integrity/ | 0.661 | github.blog/latest/ | 0.655 | github.blog/latest/ | 0.635 |
| crawl4ai | #1 | github.blog/engineering/platform-security/ | 0.756 | github.blog/engineering/platform-security/finding- | 0.693 | github.blog/security/application-security/how-expo | 0.676 |
| crawl4ai-raw | #1 | github.blog/engineering/platform-security/ | 0.756 | github.blog/engineering/platform-security/finding- | 0.693 | github.blog/security/application-security/how-expo | 0.676 |
| scrapy+md | #2 | github.blog/security/vulnerability-research/securi | 0.710 | github.blog/engineering/platform-security/finding- | 0.693 | github.blog/tag/github-security-lab/page/2/ | 0.683 |
| crawlee | #1 | github.blog/engineering/platform-security/ | 0.740 | github.blog/engineering/platform-security/finding- | 0.693 | github.blog/engineering/platform-security/finding- | 0.644 |
| colly+md | #1 | github.blog/engineering/platform-security/ | 0.740 | github.blog/engineering/platform-security/page/2/ | 0.720 | github.blog/engineering/architecture-optimization/ | 0.707 |
| playwright | #1 | github.blog/engineering/platform-security/ | 0.740 | github.blog/engineering/platform-security/finding- | 0.693 | github.blog/engineering/platform-security/finding- | 0.644 |


**Q6: How does GitHub optimize its architecture?** [conceptual]
*(expects URL containing: `architecture-optimization`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | github.blog/engineering/infrastructure/glb-directo | 0.645 | github.blog/engineering/architecture-optimization/ | 0.644 | github.blog/engineering/infrastructure/evolution-o | 0.610 |
| crawl4ai | #2 | github.blog/news-insights/company-news/addressing- | 0.629 | github.blog/engineering/architecture-optimization/ | 0.624 | github.blog/engineering/engineering-principles/ | 0.616 |
| crawl4ai-raw | #2 | github.blog/news-insights/company-news/addressing- | 0.629 | github.blog/engineering/architecture-optimization/ | 0.624 | github.blog/engineering/engineering-principles/ | 0.616 |
| scrapy+md | #29 | github.blog/engineering/page/10/ | 0.603 | github.blog/tag/codespaces/ | 0.594 | github.blog/engineering/page/10/ | 0.587 |
| crawlee | #3 | github.blog/engineering/how-we-use-github-to-be-mo | 0.613 | github.blog/news-insights/company-news/addressing- | 0.604 | github.blog/engineering/architecture-optimization/ | 0.600 |
| colly+md | #1 | github.blog/engineering/architecture-optimization/ | 0.629 | github.blog/engineering/architecture-optimization/ | 0.624 | github.blog/engineering/architecture-optimization/ | 0.615 |
| playwright | #3 | github.blog/engineering/how-we-use-github-to-be-mo | 0.613 | github.blog/news-insights/company-news/addressing- | 0.605 | github.blog/engineering/architecture-optimization/ | 0.600 |


**Q7: What engineering principles does GitHub follow?** [conceptual]
*(expects URL containing: `engineering-principles`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | github.blog/engineering/infrastructure/transit-and | 0.646 | github.blog/engineering/engineering-principles/scr | 0.629 | github.blog/news-insights/the-library/brubeck/ | 0.629 |
| crawl4ai | #1 | github.blog/engineering/engineering-principles/ | 0.790 | github.blog/engineering/page/2/ | 0.706 | github.blog/engineering/page/11/ | 0.687 |
| crawl4ai-raw | #1 | github.blog/engineering/engineering-principles/ | 0.790 | github.blog/engineering/page/2/ | 0.706 | github.blog/engineering/page/11/ | 0.687 |
| scrapy+md | miss | github.blog/engineering/ | 0.667 | github.blog/engineering/page/10/ | 0.665 | github.blog/engineering/page/2/ | 0.665 |
| crawlee | #1 | github.blog/engineering/engineering-principles/ | 0.786 | github.blog/engineering/ | 0.667 | github.blog/engineering/page/2/ | 0.665 |
| colly+md | #1 | github.blog/engineering/engineering-principles/ | 0.786 | github.blog/engineering/engineering-principles/pag | 0.781 | github.blog/engineering/ | 0.667 |
| playwright | #1 | github.blog/engineering/engineering-principles/ | 0.786 | github.blog/engineering/ | 0.667 | github.blog/engineering/page/2/ | 0.665 |


**Q8: How does GitHub improve user experience?** [conceptual]
*(expects URL containing: `user-experience`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | github.blog/news-insights/the-library/code-in-the- | 0.621 | github.blog/news-insights/the-library/smooth-suppo | 0.600 | github.blog/news-insights/the-library/local-github | 0.600 |
| crawl4ai | #4 | github.blog/changelog/2026/?label=client-apps | 0.656 | github.blog/changelog/2026-04-08-new-pgp-signing-k | 0.656 | github.blog/engineering/how-we-use-github-to-be-mo | 0.640 |
| crawl4ai-raw | #4 | github.blog/changelog/2026-04-08-new-pgp-signing-k | 0.656 | github.blog/changelog/2026/?label=client-apps | 0.656 | github.blog/engineering/how-we-use-github-to-be-mo | 0.640 |
| scrapy+md | miss | github.blog/news-insights/product-news/sunsetting- | 0.637 | github.blog/news-insights/product-news/github-desk | 0.621 | github.blog/tag/features/ | 0.618 |
| crawlee | #35 | github.blog/changelog/2026/?label=client-apps | 0.633 | github.blog/changelog/2026-04-08-new-pgp-signing-k | 0.633 | github.blog/developer-skills/github-education/ | 0.624 |
| colly+md | #7 | github.blog/enterprise-software/automation/dependa | 0.638 | github.blog/engineering/engineering-principles/git | 0.638 | github.blog/enterprise-software/collaboration/a-ch | 0.638 |
| playwright | #35 | github.blog/changelog/2026/?label=client-apps | 0.633 | github.blog/changelog/2026-04-08-new-pgp-signing-k | 0.633 | github.blog/developer-skills/github-education/ | 0.624 |


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

## See also

- [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) — content quality differences that wash out at retrieval time but affect downstream answers
- [ANSWER_QUALITY.md](ANSWER_QUALITY.md) — where the LLM's final answers diverge despite similar retrieval
- [COST_AT_SCALE.md](COST_AT_SCALE.md) — the dollar impact of chunk count differences (2x chunks = 2x embedding cost)
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup, tool configurations, and fairness decisions

