# Retrieval Quality Comparison
<!-- style: v2, 2026-04-24 -->

Crawler choice barely matters for retrieval — retrieval mode matters more.

Does each tool's output produce embeddings that answer real questions?
This benchmark chunks each tool's crawl output, embeds it with
`text-embedding-3-small`, and measures retrieval across four modes:

- **Embedding**: Cosine similarity on OpenAI embeddings
- **BM25**: Keyword search (Okapi BM25)
- **Hybrid**: Embedding + BM25 fused via Reciprocal Rank Fusion
- **Reranked**: Hybrid candidates reranked by `cross-encoder/ms-marco-MiniLM-L-6-v2`

**104 queries** across 11 sites.
Hit rate = correct source page in top-K results. Higher is better.
Summary tables use the **58-query common subset** (5 sites) so all tools are compared on identical queries. Sites excluded: huggingface-transformers, ikea, mdn-css, newegg, npr-news, smittenkitchen (not all tools have data). Per-site tables show full results.

## Quick summary: best retrieval mode per tool

For each tool, the mode with the highest MRR. Most readers can stop here.

| Tool | Best mode | Hit@10 | MRR |
|---|---|---|---|
| crawlee | hybrid | 95% (55/58) ±6% | 0.706 |
| playwright | embedding | 93% (54/58) ±7% | 0.696 |
| crawl4ai | hybrid | 88% (51/58) ±8% | 0.658 |
| crawl4ai-raw | hybrid | 90% (52/58) ±8% | 0.633 |
| colly+md | embedding | 83% (48/58) ±10% | 0.617 |
| markcrawl | embedding | 71% (41/58) ±11% | 0.594 |
| scrapy+md | embedding | 60% (35/58) ±12% | 0.442 |

> **Column definitions:** **Best mode** = retrieval strategy that maximizes MRR for this tool. **Hit@10** = correct source page in top 10 results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged).

## Summary: retrieval modes compared

_Computed over 58 queries on 5 common sites (kubernetes-docs, postgres-docs, react-dev, rust-book, stripe-docs)._

| Tool | Mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR |
|---|---|---|---|---|---|---|---|
| crawlee | embedding | 59% (34/58) ±12% | 76% (44/58) ±11% | 86% (50/58) ±9% | 93% (54/58) ±7% | 93% (54/58) ±7% | 0.701 |
| playwright | embedding | 57% (33/58) ±12% | 78% (45/58) ±11% | 86% (50/58) ±9% | 93% (54/58) ±7% | 93% (54/58) ±7% | 0.696 |
| colly+md | embedding | 52% (30/58) ±12% | 67% (39/58) ±12% | 76% (44/58) ±11% | 83% (48/58) ±10% | 83% (48/58) ±10% | 0.617 |
| crawl4ai | embedding | 47% (27/58) ±12% | 74% (43/58) ±11% | 79% (46/58) ±10% | 90% (52/58) ±8% | 91% (53/58) ±7% | 0.611 |
| crawl4ai-raw | embedding | 47% (27/58) ±12% | 74% (43/58) ±11% | 79% (46/58) ±10% | 90% (52/58) ±8% | 91% (53/58) ±7% | 0.611 |
| markcrawl | embedding | 52% (30/58) ±12% | 67% (39/58) ±12% | 69% (40/58) ±12% | 71% (41/58) ±11% | 71% (41/58) ±11% | 0.594 |
| scrapy+md | embedding | 34% (20/58) ±12% | 52% (30/58) ±12% | 57% (33/58) ±12% | 60% (35/58) ±12% | 66% (38/58) ±12% | 0.442 |
| crawl4ai | bm25 | 29% (17/58) ±11% | 50% (29/58) ±12% | 57% (33/58) ±12% | 67% (39/58) ±12% | 83% (48/58) ±10% | 0.424 |
| crawl4ai-raw | bm25 | 28% (16/58) ±11% | 47% (27/58) ±12% | 55% (32/58) ±12% | 67% (39/58) ±12% | 84% (49/58) ±9% | 0.408 |
| playwright | bm25 | 24% (14/58) ±11% | 50% (29/58) ±12% | 57% (33/58) ±12% | 76% (44/58) ±11% | 83% (48/58) ±10% | 0.399 |
| crawlee | bm25 | 22% (13/58) ±11% | 50% (29/58) ±12% | 57% (33/58) ±12% | 78% (45/58) ±11% | 83% (48/58) ±10% | 0.392 |
| colly+md | bm25 | 17% (10/58) ±10% | 38% (22/58) ±12% | 43% (25/58) ±12% | 59% (34/58) ±12% | 71% (41/58) ±11% | 0.307 |
| markcrawl | bm25 | 14% (8/58) ±9% | 36% (21/58) ±12% | 41% (24/58) ±12% | 52% (30/58) ±12% | 66% (38/58) ±12% | 0.276 |
| scrapy+md | bm25 | 16% (9/58) ±9% | 28% (16/58) ±11% | 36% (21/58) ±12% | 47% (27/58) ±12% | 57% (33/58) ±12% | 0.248 |
| crawlee | hybrid | 57% (33/58) ±12% | 81% (47/58) ±10% | 88% (51/58) ±8% | 95% (55/58) ±6% | 95% (55/58) ±6% | 0.706 |
| playwright | hybrid | 55% (32/58) ±12% | 79% (46/58) ±10% | 84% (49/58) ±9% | 93% (54/58) ±7% | 95% (55/58) ±6% | 0.689 |
| crawl4ai | hybrid | 53% (31/58) ±12% | 74% (43/58) ±11% | 81% (47/58) ±10% | 88% (51/58) ±8% | 93% (54/58) ±7% | 0.658 |
| crawl4ai-raw | hybrid | 50% (29/58) ±12% | 72% (42/58) ±11% | 78% (45/58) ±11% | 90% (52/58) ±8% | 93% (54/58) ±7% | 0.633 |
| colly+md | hybrid | 45% (26/58) ±12% | 64% (37/58) ±12% | 71% (41/58) ±11% | 83% (48/58) ±10% | 84% (49/58) ±9% | 0.566 |
| markcrawl | hybrid | 34% (20/58) ±12% | 57% (33/58) ±12% | 62% (36/58) ±12% | 69% (40/58) ±12% | 72% (42/58) ±11% | 0.469 |
| scrapy+md | hybrid | 28% (16/58) ±11% | 47% (27/58) ±12% | 53% (31/58) ±12% | 60% (35/58) ±12% | 62% (36/58) ±12% | 0.389 |
| playwright | reranked | 48% (28/58) ±12% | 74% (43/58) ±11% | 86% (50/58) ±9% | 95% (55/58) ±6% | 95% (55/58) ±6% | 0.647 |
| crawlee | reranked | 47% (27/58) ±12% | 72% (42/58) ±11% | 84% (49/58) ±9% | 95% (55/58) ±6% | 95% (55/58) ±6% | 0.631 |
| crawl4ai-raw | reranked | 48% (28/58) ±12% | 69% (40/58) ±12% | 79% (46/58) ±10% | 90% (52/58) ±8% | 95% (55/58) ±6% | 0.611 |
| crawl4ai | reranked | 48% (28/58) ±12% | 67% (39/58) ±12% | 79% (46/58) ±10% | 90% (52/58) ±8% | 95% (55/58) ±6% | 0.607 |
| colly+md | reranked | 38% (22/58) ±12% | 62% (36/58) ±12% | 71% (41/58) ±11% | 83% (48/58) ±10% | 83% (48/58) ±10% | 0.526 |
| markcrawl | reranked | 40% (23/58) ±12% | 59% (34/58) ±12% | 66% (38/58) ±12% | 71% (41/58) ±11% | 72% (42/58) ±11% | 0.506 |
| scrapy+md | reranked | 26% (15/58) ±11% | 41% (24/58) ±12% | 47% (27/58) ±12% | 55% (32/58) ±12% | 60% (35/58) ±12% | 0.361 |

> **Column definitions:** **Hit@K** = percentage of queries where the correct source page appeared in the top K results (shown as % with raw counts). **MRR** (Mean Reciprocal Rank) = average of 1/rank for correct results (1.0 = always rank 1, 0.5 = always rank 2). **Mode** = retrieval strategy used (see definitions above).

## Summary: embedding-only (hit rate at multiple K values)

_Computed over 58 queries on 5 common sites._

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Avg words |
|---|---|---|---|---|---|---|---|---|
| crawlee | 59% (34/58) ±12% | 76% (44/58) ±11% | 86% (50/58) ±9% | 93% (54/58) ±7% | 93% (54/58) ±7% | 0.701 | 64378 | 252 |
| playwright | 57% (33/58) ±12% | 78% (45/58) ±11% | 86% (50/58) ±9% | 93% (54/58) ±7% | 93% (54/58) ±7% | 0.696 | 61837 | 255 |
| colly+md | 52% (30/58) ±12% | 67% (39/58) ±12% | 76% (44/58) ±11% | 83% (48/58) ±10% | 83% (48/58) ±10% | 0.617 | 59743 | 259 |
| crawl4ai | 47% (27/58) ±12% | 74% (43/58) ±11% | 79% (46/58) ±10% | 90% (52/58) ±8% | 91% (53/58) ±7% | 0.611 | 36246 | 147 |
| crawl4ai-raw | 47% (27/58) ±12% | 74% (43/58) ±11% | 79% (46/58) ±10% | 90% (52/58) ±8% | 91% (53/58) ±7% | 0.611 | 38904 | 143 |
| markcrawl | 52% (30/58) ±12% | 67% (39/58) ±12% | 69% (40/58) ±12% | 71% (41/58) ±11% | 71% (41/58) ±11% | 0.594 | 33638 | 83 |
| scrapy+md | 34% (20/58) ±12% | 52% (30/58) ±12% | 57% (33/58) ±12% | 60% (35/58) ±12% | 66% (38/58) ±12% | 0.442 | 47418 | 131 |

> **Column definitions:** **Hit@K** = correct source page in top K results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). **Chunks** = total chunks produced by this tool (across all pages in common sites). **Avg words** = mean words per chunk.

## What this means

Tools span MRR 0.442-0.701 on embedding mode (a 0.259 spread). Tools crawl similar pages from the same seed URLs, and we apply identical chunking and embedding pipelines, but extraction differences -- see [content quality](QUALITY_COMPARISON.md) -- show up at retrieval time.

**Retrieval mode matters more than crawler choice.** Embedding search beats BM25 by roughly 2x on MRR across all tools. Hybrid and reranked modes fall between the two. Choosing the right retrieval strategy will improve your RAG pipeline far more than switching crawlers.

**The noise-vs-recall trade-off.** Noisier tools (crawlee, playwright) have slightly higher hit rates, but they produce 2x the chunks of leaner tools (markcrawl, scrapy+md). More chunks means higher embedding and storage costs with diminishing retrieval returns. See [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar impact.

**For most use cases, pick your crawler based on speed and cost, not retrieval quality.** The differences here are within confidence intervals. Where crawler choice _does_ matter is content quality and downstream answer quality -- see [ANSWER_QUALITY.md](ANSWER_QUALITY.md).

## Per-category breakdown (embedding mode)

Query categories reveal where crawlers actually differ. Categories like `js-rendered` and `structured-data` stress-test browser rendering and table extraction, while `api-function` and `conceptual` queries test basic content retrieval.

| Category | Tool | Hit@10 | MRR | Queries |
|---|---|---|---|---|
| api-function | crawlee | 92% (23/25) | 0.798 | 25 |
| api-function | colly+md | 88% (22/25) | 0.786 | 25 |
| api-function | playwright | 88% (22/25) | 0.784 | 25 |
| api-function | markcrawl | 84% (21/25) | 0.726 | 25 |
| api-function | crawl4ai | 84% (21/25) | 0.616 | 25 |
| api-function | crawl4ai-raw | 84% (21/25) | 0.616 | 25 |
| api-function | scrapy+md | 64% (16/25) | 0.482 | 25 |
| code-example | markcrawl | 100% (4/4) | 0.750 | 4 |
| code-example | crawl4ai | 100% (4/4) | 0.561 | 4 |
| code-example | crawl4ai-raw | 100% (4/4) | 0.561 | 4 |
| code-example | crawlee | 100% (4/4) | 0.487 | 4 |
| code-example | playwright | 100% (4/4) | 0.487 | 4 |
| code-example | scrapy+md | 100% (4/4) | 0.446 | 4 |
| code-example | colly+md | 100% (4/4) | 0.425 | 4 |
| conceptual | crawlee | 100% (22/22) | 0.705 | 22 |
| conceptual | playwright | 100% (22/22) | 0.685 | 22 |
| conceptual | crawl4ai | 100% (22/22) | 0.621 | 22 |
| conceptual | crawl4ai-raw | 100% (22/22) | 0.621 | 22 |
| conceptual | colly+md | 73% (16/22) | 0.509 | 22 |
| conceptual | markcrawl | 59% (13/22) | 0.407 | 22 |
| conceptual | scrapy+md | 55% (12/22) | 0.327 | 22 |
| cross-page | crawl4ai | 100% (2/2) | 0.750 | 2 |
| cross-page | crawl4ai-raw | 100% (2/2) | 0.750 | 2 |
| cross-page | crawlee | 100% (2/2) | 0.750 | 2 |
| cross-page | colly+md | 100% (2/2) | 0.750 | 2 |
| cross-page | playwright | 100% (2/2) | 0.750 | 2 |
| cross-page | scrapy+md | 100% (2/2) | 0.545 | 2 |
| cross-page | markcrawl | 0% (0/2) | 0.000 | 2 |
| js-rendered | markcrawl | 100% (5/5) | 0.867 | 5 |
| js-rendered | crawl4ai | 100% (5/5) | 0.522 | 5 |
| js-rendered | crawl4ai-raw | 100% (5/5) | 0.522 | 5 |
| js-rendered | playwright | 100% (5/5) | 0.440 | 5 |
| js-rendered | colly+md | 100% (5/5) | 0.353 | 5 |
| js-rendered | scrapy+md | 80% (4/5) | 0.700 | 5 |
| js-rendered | crawlee | 80% (4/5) | 0.350 | 5 |


### Best tool per category

| Category | Best tool | Hit@10 | Spread |
|---|---|---|---|
| api-function | crawlee | 92% | 28% |
| code-example | markcrawl | 100% | 0% |
| conceptual | crawl4ai | 100% | 45% |
| cross-page | crawl4ai | 100% | 100% |
| js-rendered | markcrawl | 100% | 20% |

_Spread = difference between best and worst tool. High spread categories are where crawler choice matters most._


## huggingface-transformers

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 12% (1/8) | 12% (1/8) | 12% (1/8) | 25% (2/8) | 25% (2/8) | 0.143 | 3122 | 300 |
| crawl4ai-raw | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 2372 | 300 |
| playwright | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 12% (1/8) | 0.007 | 88 | 60 |
| markcrawl | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0.000 | 425 | 50 |
| scrapy+md | — | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for huggingface-transformers</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I use the Pipeline class for inference in Transformers?** [api-function]
*(expects URL containing: `pipeline_tutorial`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/docs/optimum-habana | 0.433 | huggingface.co/docs/inference-providers | 0.423 | huggingface.co/docs/inference-providers | 0.421 |
| crawl4ai | miss | huggingface.co/docs/transformers/quicktour | 0.636 | huggingface.co/docs/transformers/quicktour | 0.598 | huggingface.co/docs/transformers/index | 0.581 |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/quicktour | 0.636 | huggingface.co/docs/transformers/quicktour | 0.598 | huggingface.co/docs/transformers/index | 0.581 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/ | 0.377 | huggingface.co/ | 0.321 | huggingface.co/ | 0.264 |


**Q2: How do I train a model with the Hugging Face Trainer?** [api-function]
*(expects URL containing: `trainer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/models | 0.657 | huggingface.co/docs/sagemaker | 0.605 | huggingface.co/docs/huggingface.js | 0.574 |
| crawl4ai | miss | discuss.huggingface.co/t/from-zero-to-my-first-hug | 0.630 | discuss.huggingface.co/t/from-zero-to-my-first-hug | 0.629 | endpoints.huggingface.co/ | 0.619 |
| crawl4ai-raw | miss | endpoints.huggingface.co | 0.619 | endpoints.huggingface.co/ | 0.619 | huggingface.co/docs/transformers/peft | 0.616 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/ | 0.420 | huggingface.co/ | 0.416 | huggingface.co/ | 0.350 |


**Q3: How do I generate text with a large language model?** [api-function]
*(expects URL containing: `llm_tutorial`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/models | 0.521 | huggingface.co/models | 0.447 | huggingface.co/docs/optimum-habana | 0.425 |
| crawl4ai | miss | huggingface.co/ServiceNow | 0.537 | huggingface.co/mayank-mishra | 0.515 | huggingface.co/LiquidAI | 0.490 |
| crawl4ai-raw | miss | huggingface.co/unsloth/Qwen3.5-35B-A3B-GGUF | 0.527 | huggingface.co/unsloth/Qwen3.5-9B-GGUF | 0.526 | huggingface.co/unsloth/Qwen3.5-35B-A3B-GGUF | 0.487 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/chat | 0.397 | huggingface.co/chat/ | 0.397 | huggingface.co/ | 0.339 |


**Q4: What are the design principles behind the Transformers library?** [conceptual]
*(expects URL containing: `philosophy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/docs | 0.476 | huggingface.co/blog | 0.460 | huggingface.co/docs/optimum-tpu | 0.451 |
| crawl4ai | miss | huggingface.co/docs/transformers/index | 0.724 | discuss.huggingface.co/categories | 0.612 | huggingface.co/docs/transformers/index | 0.608 |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.724 | discuss.huggingface.co/categories | 0.612 | huggingface.co/docs/transformers/index | 0.608 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/ | 0.416 | huggingface.co/chat/ | 0.263 | huggingface.co/chat | 0.263 |


**Q5: What models are supported in the Transformers library?** [cross-page]
*(expects URL containing: `models_timeline`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/docs | 0.538 | huggingface.co/docs/hub | 0.512 | huggingface.co/models | 0.502 |
| crawl4ai | #7 | huggingface.co/docs/transformers/index | 0.666 | discuss.huggingface.co/categories | 0.615 | huggingface.co/docs/transformers/peft | 0.597 |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.666 | discuss.huggingface.co/categories | 0.615 | huggingface.co/docs/transformers/installation | 0.598 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/ | 0.454 | huggingface.co/ | 0.392 | huggingface.co/ | 0.383 |


**Q6: What is the Pipeline API reference in Transformers?** [api-function]
*(expects URL containing: `main_classes/pipelines`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/docs | 0.453 | huggingface.co/docs/optimum-tpu | 0.450 | huggingface.co/docs/optimum | 0.435 |
| crawl4ai | miss | discuss.huggingface.co/t/why-am-i-facing-this-erro | 0.607 | discuss.huggingface.co/t/why-am-i-facing-this-erro | 0.607 | discuss.huggingface.co/t/why-am-i-facing-this-erro | 0.607 |
| crawl4ai-raw | miss | discuss.huggingface.co/t/why-am-i-facing-this-erro | 0.607 | discuss.huggingface.co/t/why-am-i-facing-this-erro | 0.607 | discuss.huggingface.co/t/why-am-i-facing-this-erro | 0.607 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/ | 0.414 | huggingface.co/ | 0.329 | huggingface.co/ | 0.285 |


**Q7: What does the Trainer class support for distributed training?** [api-function]
*(expects URL containing: `main_classes/trainer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/docs/autotrain | 0.431 | huggingface.co/docs/autotrain | 0.419 | huggingface.co/docs | 0.415 |
| crawl4ai | miss | huggingface.co/docs/transformers/peft | 0.575 | huggingface.co/docs/transformers/quicktour | 0.460 | huggingface.co/mayank-mishra | 0.458 |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/peft | 0.576 | huggingface.co/docs/transformers/quicktour | 0.460 | huggingface.co/docs/transformers/peft | 0.447 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/ | 0.269 | huggingface.co/ | 0.257 | huggingface.co/ | 0.256 |


**Q8: What is the Hugging Face Transformers library?** [conceptual]
*(expects URL containing: `transformers/index`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/docs/huggingface.js | 0.699 | huggingface.co/docs/hub | 0.612 | huggingface.co/docs | 0.591 |
| crawl4ai | #1 | huggingface.co/docs/transformers/index | 0.695 | huggingface.co/docs/transformers/installation | 0.695 | huggingface.co/docs/transformers/quicktour | 0.687 |
| crawl4ai-raw | #1 | huggingface.co/docs/transformers/index | 0.695 | huggingface.co/docs/transformers/installation | 0.695 | huggingface.co/docs/transformers/quicktour | 0.687 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | #19 | huggingface.co/ | 0.493 | huggingface.co/ | 0.440 | huggingface.co/ | 0.365 |


</details>

## ikea

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 3529 | 200 |
| crawl4ai | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 5302 | 200 |
| crawl4ai-raw | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 5882 | 200 |
| crawlee | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 8125 | 202 |
| playwright | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 7184 | 200 |
| scrapy+md | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0.000 | 2869 | 189 |
| colly+md | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for ikea</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How much does the MALM bed frame cost at IKEA?** [factual-lookup]
*(expects URL containing: `malm-bed-frame`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.626 | www.ikea.com/us/en/cat/beds-bm003/ | 0.603 | www.ikea.com/us/en/cat/beds-bm003/ | 0.601 |
| crawl4ai | miss | www.ikea.com/us/en/rooms/bedroom/how-to/teenage-be | 0.702 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.692 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.624 |
| crawl4ai-raw | miss | www.ikea.com/us/en/rooms/bedroom/how-to/teenage-be | 0.702 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.692 | www.ikea.com/us/en/cat/furniture-fu001/?page=2 | 0.681 |
| scrapy+md | miss | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.493 | www.ikea.com/us/en/cat/headboards-19064/ | 0.492 | www.ikea.com/us/en/customer-service/services/deliv | 0.485 |
| crawlee | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.632 | www.ikea.com/us/en/cat/beds-bm003/ | 0.623 | www.ikea.com/us/en/cat/beds-bm003/ | 0.619 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.632 | www.ikea.com/us/en/p/slaekt-bed-frame-with-slatted | 0.568 | www.ikea.com/us/en/p/malm-dressing-table-white-102 | 0.559 |


**Q2: What's the price of the SLATTUM upholstered bed frame?** [factual-lookup]
*(expects URL containing: `slattum-upholstered-bed`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.583 | www.ikea.com/us/en/cat/beds-bm003/ | 0.563 | www.ikea.com/us/en/cat/beds-bm003/ | 0.562 |
| crawl4ai | miss | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.632 | www.ikea.com/us/en/rooms/bedroom/ | 0.607 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.605 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.632 | www.ikea.com/us/en/rooms/bedroom/ | 0.607 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.605 |
| scrapy+md | miss | www.ikea.com/us/en/p/buslaett-chair-white-pine-906 | 0.494 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.483 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.476 |
| crawlee | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.598 | www.ikea.com/us/en/cat/beds-bm003/ | 0.570 | www.ikea.com/us/en/cat/beds-bm003/ | 0.566 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | www.ikea.com/us/en/p/slaekt-bed-frame-with-slatted | 0.646 | www.ikea.com/us/en/p/slaekt-bed-frame-with-slatted | 0.635 | www.ikea.com/us/en/p/slaekt-bed-frame-with-slatted | 0.598 |


**Q3: Tell me about the HEMNES 8-drawer dresser** [factual-lookup]
*(expects URL containing: `hemnes-8-drawer-dresser`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.642 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.614 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.613 |
| crawl4ai | miss | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.608 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.607 | www.ikea.com/us/en/cat/home-textiles-tl001/ | 0.605 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.696 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.683 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.651 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.498 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.496 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.489 |
| crawlee | miss | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.617 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.609 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.605 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.577 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.570 | www.ikea.com/us/en/ | 0.553 |


**Q4: What's the price of the RAST 3-drawer dresser?** [factual-lookup]
*(expects URL containing: `rast-3-drawer-dresser`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.588 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.588 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.585 |
| crawl4ai | miss | www.ikea.com/us/en/cat/home-textiles-tl001/ | 0.672 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.614 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.604 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.714 | www.ikea.com/us/en/cat/home-textiles-tl001/ | 0.672 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.652 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.511 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.485 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.435 |
| crawlee | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.605 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.598 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.596 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.605 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.595 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.562 |


**Q5: What bed frames does IKEA sell?** [cross-page]
*(expects URL containing: `cat/beds`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.734 | www.ikea.com/us/en/cat/beds-bm003/ | 0.691 | www.ikea.com/us/en/cat/beds-bm003/ | 0.666 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.736 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.707 | www.ikea.com/us/en/cat/beds-bm003/ | 0.661 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.736 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.707 | www.ikea.com/us/en/cat/beds-bm003/ | 0.661 |
| scrapy+md | miss | www.ikea.com/us/en/cat/headboards-19064/ | 0.602 | www.ikea.com/global/en/sitemap/ | 0.597 | www.ikea.com/us/en/cat/headboards-19064/ | 0.530 |
| crawlee | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.774 | www.ikea.com/us/en/cat/beds-bm003/ | 0.716 | www.ikea.com/us/en/cat/products-products/ | 0.656 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.774 | www.ikea.com/us/en/cat/beds-bm003/ | 0.716 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.670 |


**Q6: Show me IKEA's sofa and armchair selection** [cross-page]
*(expects URL containing: `cat/sofas-armchairs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.715 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.708 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.698 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.740 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.729 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.712 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.740 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.729 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.712 |
| scrapy+md | miss | www.ikea.com/us/en/p/buslaett-chair-white-pine-906 | 0.621 | www.ikea.com/us/en/cat/dining-chairs-25219/f/with- | 0.616 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.615 |
| crawlee | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.766 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.723 | www.ikea.com/us/en/cat/products-products/ | 0.722 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.766 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.723 | www.ikea.com/us/en/cat/products-products/ | 0.722 |


**Q7: What dressers and storage drawers does IKEA offer?** [cross-page]
*(expects URL containing: `cat/dressers-storage-drawers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.727 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.717 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.677 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.729 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.703 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.692 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.729 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.701 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.692 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.607 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.589 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.587 |
| crawlee | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.747 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.707 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.701 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.747 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.707 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.701 |


**Q8: How much is the STOREMOLLA 8-drawer dresser at IKEA?** [factual-lookup]
*(expects URL containing: `storemolla-8-drawer-dresser`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.586 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.585 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.572 |
| crawl4ai | miss | www.ikea.com/us/en/cat/gullaberg-series-700613/ | 0.657 | www.ikea.com/us/en/cat/gullaberg-series-700613/ | 0.631 | www.ikea.com/us/en/cat/home-textiles-tl001/ | 0.626 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.711 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.663 | www.ikea.com/us/en/cat/gullaberg-series-700613/ | 0.657 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.527 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.525 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.516 |
| crawlee | miss | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.589 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.587 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.585 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.573 | www.ikea.com/us/en/ | 0.571 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.559 |


</details>

## kubernetes-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 75% (6/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.875 | 11510 | 400 |
| colly+md | 75% (6/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.875 | 11471 | 398 |
| playwright | 75% (6/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.875 | 11510 | 400 |
| crawl4ai | 75% (6/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.854 | 11212 | 400 |
| crawl4ai-raw | 75% (6/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.854 | 11100 | 400 |
| markcrawl | 38% (3/8) | 75% (6/8) | 75% (6/8) | 75% (6/8) | 75% (6/8) | 0.542 | 7677 | 400 |
| scrapy+md | 0% (0/8) | 0% (0/8) | 0% (0/8) | 12% (1/8) | 12% (1/8) | 0.014 | 15932 | 328 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for kubernetes-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is a Kubernetes pod and what does it represent?** [conceptual]
*(expects URL containing: `workloads/pods`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | kubernetes.io/docs/reference/kubernetes-api/worklo | 0.735 | kubernetes.io/docs/tutorials/kubernetes-basics/exp | 0.722 | kubernetes.io/docs/concepts/workloads/pods/ | 0.693 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.776 | kubernetes.io/docs/concepts/workloads/pods/ | 0.670 | kubernetes.io/pt-br/docs/concepts/ | 0.664 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.776 | kubernetes.io/docs/concepts/workloads/pods/ | 0.670 | kubernetes.io/pt-br/docs/concepts/ | 0.664 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.693 | kubernetes.io/docs/concepts/_print/ | 0.668 | kubernetes.io/es/docs/_print/ | 0.653 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.693 | kubernetes.io/docs/concepts/workloads/pods/ | 0.670 | kubernetes.io/docs/concepts/workloads/pods/advance | 0.608 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.693 | kubernetes.io/docs/concepts/workloads/pods/ | 0.666 | kubernetes.io/docs/concepts/workloads/pods/ | 0.623 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.693 | kubernetes.io/docs/concepts/workloads/pods/ | 0.670 | kubernetes.io/docs/concepts/workloads/pods/ | 0.623 |


**Q2: How do Kubernetes Deployments manage replicas and rollouts?** [api-function]
*(expects URL containing: `controllers/deployment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/tutorials/kubernetes-basics/dep | 0.729 | kubernetes.io/docs/reference/kubernetes-api/worklo | 0.712 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.711 |
| crawl4ai | #3 | kubernetes.io/ | 0.711 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.700 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.700 |
| crawl4ai-raw | #3 | kubernetes.io/ | 0.711 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.700 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.700 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.683 | kubernetes.io/docs/concepts/_print/ | 0.680 | kubernetes.io/docs/concepts/_print/ | 0.666 |
| crawlee | #2 | kubernetes.io/ | 0.723 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.685 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.683 |
| colly+md | #2 | kubernetes.io/docs/concepts/ | 0.723 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.683 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.683 |
| playwright | #2 | kubernetes.io/ | 0.723 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.685 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.683 |


**Q3: What is a Kubernetes Service and how does it expose pods?** [conceptual]
*(expects URL containing: `services-networking/service`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/tutorials/kubernetes-basics/exp | 0.777 | kubernetes.io/docs/concepts/services-networking/se | 0.759 | kubernetes.io/docs/reference/kubernetes-api/servic | 0.726 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.770 | kubernetes.io/docs/concepts/services-networking/se | 0.735 | kubernetes.io/docs/concepts/services-networking/dn | 0.630 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.770 | kubernetes.io/docs/concepts/services-networking/se | 0.735 | kubernetes.io/docs/concepts/services-networking/dn | 0.630 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.735 | kubernetes.io/docs/concepts/_print/ | 0.722 | kubernetes.io/es/docs/_print/ | 0.702 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.758 | kubernetes.io/docs/concepts/services-networking/se | 0.727 | kubernetes.io/docs/tasks/access-application-cluste | 0.699 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.759 | kubernetes.io/docs/concepts/services-networking/se | 0.722 | kubernetes.io/docs/concepts/services-networking/se | 0.622 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.758 | kubernetes.io/docs/concepts/services-networking/se | 0.727 | kubernetes.io/docs/tasks/access-application-cluste | 0.699 |


**Q4: How do I use ConfigMaps to inject configuration into pods?** [api-function]
*(expects URL containing: `configuration/configmap`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/configuration/configma | 0.765 | kubernetes.io/docs/concepts/configuration/configma | 0.758 | kubernetes.io/docs/concepts/configuration/configma | 0.753 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.811 | kubernetes.io/docs/tasks/configure-pod-container/ | 0.778 | kubernetes.io/docs/concepts/configuration/configma | 0.769 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.811 | kubernetes.io/docs/tasks/configure-pod-container/ | 0.778 | kubernetes.io/docs/concepts/configuration/configma | 0.769 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.765 | kubernetes.io/docs/concepts/_print/ | 0.758 | kubernetes.io/docs/concepts/_print/ | 0.743 |
| crawlee | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.799 | kubernetes.io/docs/concepts/configuration/configma | 0.761 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.760 |
| colly+md | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.793 | kubernetes.io/docs/concepts/configuration/configma | 0.765 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.760 |
| playwright | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.799 | kubernetes.io/docs/concepts/configuration/configma | 0.761 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.760 |


**Q5: How do I manage Secrets in Kubernetes?** [api-function]
*(expects URL containing: `configuration/secret`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.762 | kubernetes.io/docs/reference/kubernetes-api/config | 0.743 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.735 |
| crawl4ai | #2 | kubernetes.io/docs/tasks/ | 0.803 | kubernetes.io/docs/concepts/configuration/secret/ | 0.791 | kubernetes.io/docs/concepts/security/ | 0.783 |
| crawl4ai-raw | #2 | kubernetes.io/docs/tasks/ | 0.803 | kubernetes.io/docs/concepts/configuration/secret/ | 0.791 | kubernetes.io/docs/concepts/security/ | 0.783 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.765 | kubernetes.io/docs/concepts/_print/ | 0.744 | kubernetes.io/docs/concepts/_print/ | 0.734 |
| crawlee | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.765 | kubernetes.io/docs/concepts/configuration/secret/ | 0.744 | kubernetes.io/docs/concepts/security/secrets-good- | 0.741 |
| colly+md | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.765 | kubernetes.io/docs/concepts/security/secrets-good- | 0.745 | kubernetes.io/docs/concepts/configuration/secret/ | 0.744 |
| playwright | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.765 | kubernetes.io/docs/concepts/configuration/secret/ | 0.744 | kubernetes.io/docs/concepts/security/secrets-good- | 0.741 |


**Q6: What are namespaces in Kubernetes and when should I use them?** [conceptual]
*(expects URL containing: `working-with-objects/namespaces`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/reference/kubernetes-api/cluste | 0.709 | kubernetes.io/docs/concepts/security/pod-security- | 0.658 | kubernetes.io/docs/reference/kubectl/generated/kub | 0.626 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.778 | kubernetes.io/docs/concepts/overview/working-with- | 0.737 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.716 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.778 | kubernetes.io/docs/concepts/overview/working-with- | 0.737 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.716 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.750 | kubernetes.io/docs/concepts/_print/ | 0.742 | kubernetes.io/docs/concepts/_print/ | 0.736 |
| crawlee | #2 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.746 | kubernetes.io/docs/concepts/overview/working-with- | 0.738 | kubernetes.io/docs/concepts/overview/working-with- | 0.735 |
| colly+md | #2 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.742 | kubernetes.io/docs/concepts/overview/working-with- | 0.740 | kubernetes.io/docs/concepts/overview/working-with- | 0.736 |
| playwright | #2 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.746 | kubernetes.io/docs/concepts/overview/working-with- | 0.738 | kubernetes.io/docs/concepts/overview/working-with- | 0.735 |


**Q7: How does Kubernetes Ingress route external traffic?** [conceptual]
*(expects URL containing: `services-networking/ingress`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.683 | kubernetes.io/docs/concepts/services-networking/in | 0.681 | kubernetes.io/docs/reference/kubernetes-api/servic | 0.672 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.702 | kubernetes.io/docs/concepts/services-networking/in | 0.668 | kubernetes.io/docs/concepts/services-networking/in | 0.622 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.702 | kubernetes.io/docs/concepts/services-networking/in | 0.668 | kubernetes.io/docs/concepts/services-networking/in | 0.622 |
| scrapy+md | #9 | kubernetes.io/docs/concepts/_print/ | 0.683 | kubernetes.io/docs/concepts/_print/ | 0.659 | kubernetes.io/docs/concepts/_print/ | 0.626 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.683 | kubernetes.io/docs/concepts/services-networking/in | 0.661 | kubernetes.io/docs/concepts/services-networking/in | 0.626 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.683 | kubernetes.io/docs/concepts/services-networking/in | 0.661 | kubernetes.io/docs/concepts/services-networking/in | 0.626 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.683 | kubernetes.io/docs/concepts/services-networking/in | 0.661 | kubernetes.io/docs/concepts/services-networking/in | 0.626 |


**Q8: What is a StatefulSet and when do I need one?** [api-function]
*(expects URL containing: `controllers/statefulset`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/reference/kubernetes-api/worklo | 0.656 | kubernetes.io/docs/reference/kubernetes-api/worklo | 0.643 | kubernetes.io/docs/reference/kubernetes-api/worklo | 0.633 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.678 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.667 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.627 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.678 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.667 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.627 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.711 | kubernetes.io/docs/reference/generated/kubernetes- | 0.677 | kubernetes.io/docs/concepts/_print/ | 0.658 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.711 | kubernetes.io/docs/tasks/run-application/scale-sta | 0.676 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.660 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.711 | kubernetes.io/docs/tasks/run-application/scale-sta | 0.676 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.665 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.711 | kubernetes.io/docs/tasks/run-application/scale-sta | 0.676 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.660 |


</details>

## mdn-css

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.875 | 6770 | 300 |
| crawl4ai-raw | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.875 | 6784 | 300 |
| playwright | 62% (5/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.750 | 7075 | 300 |
| crawlee | 62% (5/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.729 | 6979 | 301 |
| markcrawl | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 2012 | 300 |
| scrapy+md | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 2807 | 300 |
| colly+md | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for mdn-css</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How does the CSS display property work?** [api-function]
*(expects URL containing: `CSS/Reference/Properties/display`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/blog/interop2023-mdn-d | 0.642 | developer.mozilla.org/en-US/docs/Glossary/CSS | 0.572 | developer.mozilla.org/en-US/curriculum/core/css-la | 0.551 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.724 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.643 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.643 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.724 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.643 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.643 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.720 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.582 | developer.mozilla.org/en-US/docs/Web/CSS | 0.579 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.720 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.643 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.643 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.720 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.627 | developer.mozilla.org/en-US/docs/Web/Performance | 0.613 |


**Q2: How do I use flexbox for page layout?** [conceptual]
*(expects URL containing: `Flexible_box_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/curriculum/core/css-la | 0.544 | developer.mozilla.org/en-US/curriculum/core/css-la | 0.501 | developer.mozilla.org/en-US/blog/getting-started-w | 0.488 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.645 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.645 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.643 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.645 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.645 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.643 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.556 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.484 | developer.mozilla.org/en-US/docs/Web/CSS | 0.475 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.636 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.616 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.636 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.616 |


**Q3: How does CSS Grid layout work?** [conceptual]
*(expects URL containing: `Grid_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/blog/interop2023-mdn-d | 0.551 | developer.mozilla.org/en-US/curriculum/core/css-la | 0.549 | developer.mozilla.org/en-US/curriculum/core/css-la | 0.523 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.765 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.736 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.721 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.765 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.736 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.721 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.566 | developer.mozilla.org/en-US/docs/Web/CSS | 0.544 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.525 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.765 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.723 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.703 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.765 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.723 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.703 |


**Q4: What is the CSS box model?** [conceptual]
*(expects URL containing: `Box_model`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/curriculum/core/css-fu | 0.618 | developer.mozilla.org/en-US/blog/interop2023-mdn-d | 0.614 | developer.mozilla.org/en-US/curriculum/core/css-fu | 0.545 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.776 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.766 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.776 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.766 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.611 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.533 | developer.mozilla.org/en-US/docs/Web/CSS | 0.524 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.770 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.754 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.752 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.770 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.754 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.752 |


**Q5: How does the CSS margin property work?** [api-function]
*(expects URL containing: `Reference/Properties/margin`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/blog/interop2023-mdn-d | 0.533 | developer.mozilla.org/en-US/docs/Glossary/CSS | 0.497 | developer.mozilla.org/en-US/docs/Games/Techniques/ | 0.460 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.612 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.611 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.612 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.611 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.505 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.496 | developer.mozilla.org/en-US/docs/Web/CSS | 0.454 |
| crawlee | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.608 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.597 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.595 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.608 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.586 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.585 |


**Q6: How does CSS specificity determine which rules win?** [conceptual]
*(expects URL containing: `Cascade/Specificity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/curriculum/core/css-fu | 0.585 | developer.mozilla.org/en-US/blog/interop2023-mdn-d | 0.557 | developer.mozilla.org/en-US/docs/Glossary/CSS | 0.515 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.697 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.691 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.671 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.697 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.691 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.671 |
| scrapy+md | miss | developer.mozilla.org/de/docs/Web/API/CSSFunctionR | 0.505 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.504 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.477 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.690 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.673 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.648 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.690 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.665 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.648 |


**Q7: How does the :hover pseudo-class work in CSS?** [api-function]
*(expects URL containing: `Selectors/:hover`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/blog/css-not-pseudo-mu | 0.596 | developer.mozilla.org/en-US/blog/css-not-pseudo-mu | 0.526 | developer.mozilla.org/en-US/blog/ | 0.498 |
| crawl4ai | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.687 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.602 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.556 |
| crawl4ai-raw | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.687 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.602 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.556 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.527 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.483 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.478 |
| crawlee | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.683 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.635 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.566 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.694 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.635 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.566 |


**Q8: How do I create CSS animations?** [conceptual]
*(expects URL containing: `Animations/Using`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/blog/scroll-progress-a | 0.649 | developer.mozilla.org/en-US/blog/scroll-progress-a | 0.619 | developer.mozilla.org/en-US/curriculum/extensions/ | 0.617 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.742 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.736 | developer.mozilla.org/en-US/docs/Web/API/Web_Anima | 0.695 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.742 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.736 | developer.mozilla.org/en-US/docs/Web/API/Web_Anima | 0.695 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.596 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.567 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.491 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.728 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.725 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.709 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.728 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.725 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.709 |


</details>

## newegg

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| playwright | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 18 | 3 |
| crawl4ai | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.042 | 7116 | 200 |
| crawl4ai-raw | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.042 | 7114 | 200 |
| colly+md | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.042 | 394 | 17 |
| markcrawl | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 12% (1/8) | 0.015 | 481 | 200 |
| scrapy+md | — | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for newegg</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What graphics cards are available at Newegg?** [cross-page]
*(expects URL containing: `GPUs-Video-Graphics-Cards`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.newegg.com/insider/amd-unveils-radeon-r9-295x2 | 0.564 | www.newegg.com/insider/turn-your-living-room-into- | 0.509 | www.newegg.com/insider/ultimate-pc-gaming-accessor | 0.508 |
| crawl4ai | #3 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.716 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.665 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.655 |
| crawl4ai-raw | #3 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.716 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.665 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.655 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/sellers/?cm/sp=sell/on/newegg/foote | 0.576 | www.newegg.com/promotions/nepro/18-1881/index.html | 0.564 | www.newegg.com/promotions/nepro/18-1881/index.html | 0.564 |
| playwright | miss | www.newegg.com/ | 0.362 | www.newegg.com/ | 0.361 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.359 |


**Q2: What laptops does Newegg sell?** [cross-page]
*(expects URL containing: `Laptops-Notebooks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #12 | www.newegg.com/insider/aorus-launch-event-at-the-n | 0.579 | www.newegg.com/insider/newegg-hosts-launch-of-aoru | 0.550 | www.newegg.com/insider/whats-data/ | 0.514 |
| crawl4ai | miss | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.627 | www.newegg.com/ | 0.596 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.581 |
| crawl4ai-raw | miss | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.627 | www.newegg.com/ | 0.596 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.581 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #3 | www.newegg.com/promotions/nepro/25-1020/index.html | 0.653 | www.newegg.com/sellers/?cm/sp=sell/on/newegg/foote | 0.614 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.578 |
| playwright | #1 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.422 | www.newegg.com/ | 0.401 | www.newegg.com/ | 0.400 |


**Q3: How much does the AMD Ryzen 7 9800X3D CPU cost?** [factual-lookup]
*(expects URL containing: `ryzen-7-9800x3d`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.newegg.com/insider/amd-unveils-radeon-r9-295x2 | 0.507 | www.newegg.com/insider/amd-unveils-radeon-r9-295x2 | 0.426 | www.newegg.com/insider/introducing-geforce-gtx-tit | 0.418 |
| crawl4ai | miss | www.newegg.com/CPU-Processor/Category/ID-34 | 0.620 | www.newegg.com/Server-CPU-Processor/SubCategory/ID | 0.607 | www.newegg.com/Components-Storage/Store/ID-1 | 0.605 |
| crawl4ai-raw | miss | www.newegg.com/CPU-Processor/Category/ID-34 | 0.620 | www.newegg.com/Server-CPU-Processor/SubCategory/ID | 0.607 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.605 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.608 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.608 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.565 |
| playwright | miss | www.newegg.com/ | 0.443 | www.newegg.com/ | 0.441 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.439 |


**Q4: What is the price of the Intel Core i9-14900K?** [factual-lookup]
*(expects URL containing: `i9-14900k`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.newegg.com/insider/amd-unveils-radeon-r9-295x2 | 0.422 | www.newegg.com/insider/newegg-partnered-gigabyte-l | 0.409 | www.newegg.com/insider/select-z97-motherboards/ | 0.409 |
| crawl4ai | miss | www.newegg.com/Components-Storage/Store/ID-1 | 0.670 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.602 | www.newegg.com/tools/custom-pc-builder?cm_sp=hambu | 0.588 |
| crawl4ai-raw | miss | www.newegg.com/CPU-Processor/Category/ID-34 | 0.602 | www.newegg.com/Components-Storage/Store/ID-1 | 0.596 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.587 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.608 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.608 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.529 |
| playwright | miss | www.newegg.com/ | 0.463 | www.newegg.com/ | 0.461 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.458 |


**Q5: Tell me about the GIGABYTE GeForce RTX 5090 graphics card** [factual-lookup]
*(expects URL containing: `gv-n5090gaming`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.newegg.com/insider/introducing-geforce-gtx-tit | 0.536 | www.newegg.com/insider/amd-unveils-radeon-r9-295x2 | 0.516 | www.newegg.com/insider/amd-unveils-radeon-r9-295x2 | 0.503 |
| crawl4ai | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.631 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.630 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.621 |
| crawl4ai-raw | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.631 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.630 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.621 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.566 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.525 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.500 |
| playwright | miss | www.newegg.com/ | 0.273 | www.newegg.com/ | 0.271 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.265 |


**Q6: How much does the SAPPHIRE Radeon RX 9070 XT cost?** [factual-lookup]
*(expects URL containing: `radeon-rx-9070-xt`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.newegg.com/insider/amd-unveils-radeon-r9-295x2 | 0.523 | www.newegg.com/insider/amd-unveils-radeon-r9-295x2 | 0.450 | www.newegg.com/insider/introducing-geforce-gtx-tit | 0.393 |
| crawl4ai | miss | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.551 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.541 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.537 |
| crawl4ai-raw | miss | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.565 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.556 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.551 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.558 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.558 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.483 |
| playwright | miss | www.newegg.com/ | 0.312 | www.newegg.com/ | 0.309 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.303 |


**Q7: What ASUS TUF gaming laptops are available on Newegg?** [factual-lookup]
*(expects URL containing: `asus-tuf-gaming`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.newegg.com/insider/newegg-hosts-launch-of-aoru | 0.513 | www.newegg.com/insider/aorus-launch-event-at-the-n | 0.511 | www.newegg.com/insider/aorus-launch-event-at-the-n | 0.507 |
| crawl4ai | miss | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.593 | www.newegg.com/tools/custom-pc-builder?cm_sp=hambu | 0.592 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.587 |
| crawl4ai-raw | miss | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.592 | www.newegg.com/tools/custom-pc-builder?cm_sp=hambu | 0.592 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.587 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/promotions/nepro/25-1020/index.html | 0.606 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.572 | www.newegg.com/insider/ | 0.519 |
| playwright | miss | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.331 | www.newegg.com/ | 0.322 | www.newegg.com/ | 0.320 |


**Q8: What electronics categories does Newegg offer?** [cross-page]
*(expects URL containing: `Electronics/Store`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #26 | www.newegg.com/insider/turn-your-living-room-into- | 0.568 | www.newegg.com/insider/whats-data/ | 0.564 | www.newegg.com/insider/newegg-wins-2013-gaming-ret | 0.560 |
| crawl4ai | miss | www.newegg.com/ | 0.726 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.678 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.678 |
| crawl4ai-raw | miss | www.newegg.com/ | 0.726 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.678 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.678 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.700 | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.659 | www.newegg.com/insider/ | 0.646 |
| playwright | miss | www.newegg.com/Laptops-Notebooks/SubCategory/ID-32 | 0.362 | www.newegg.com/ | 0.359 | www.newegg.com/ | 0.358 |


</details>

## npr-news

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai-raw | 50% (3/6) | 50% (3/6) | 50% (3/6) | 50% (3/6) | 83% (5/6) | 0.532 | 6470 | 150 |
| crawl4ai | 33% (2/6) | 50% (3/6) | 50% (3/6) | 50% (3/6) | 83% (5/6) | 0.446 | 6543 | 150 |
| crawlee | 33% (2/6) | 50% (3/6) | 50% (3/6) | 50% (3/6) | 50% (3/6) | 0.434 | 8765 | 150 |
| playwright | 33% (2/6) | 50% (3/6) | 50% (3/6) | 50% (3/6) | 83% (5/6) | 0.417 | 5407 | 150 |
| markcrawl | 0% (0/6) | 33% (2/6) | 50% (3/6) | 50% (3/6) | 67% (4/6) | 0.194 | 212 | 150 |
| scrapy+md | — | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for npr-news</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What are the latest NPR politics stories?** [cross-page]
*(expects URL containing: `sections/politics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | www.npr.org/1992/08/25/100441748/the-girlish-voice | 0.641 | www.npr.org/1993/05/21/1106944/cokie-roberts-polit | 0.569 | www.npr.org/1992/01/01/4681829/the-week-in-politic | 0.531 |
| crawl4ai | #1 | www.npr.org/podcasts/510310/npr-politics-podcast/ | 0.769 | www.npr.org/2026/04/23/nx-s1-5786573/oz-pearlman-m | 0.729 | www.npr.org/ | 0.716 |
| crawl4ai-raw | #1 | www.npr.org/podcasts/510310/npr-politics-podcast/ | 0.769 | www.npr.org/2026/04/23/nx-s1-5786573/oz-pearlman-m | 0.729 | www.npr.org/ | 0.716 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | #1 | www.npr.org/podcasts/510310/npr-politics-podcast/ | 0.769 | www.npr.org/2026/04/23/nx-s1-5786573/oz-pearlman-m | 0.725 | www.npr.org/newsletter/politics | 0.700 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | www.npr.org/podcasts/510310/npr-politics-podcast/ | 0.769 | www.npr.org/2026/04/23/nx-s1-5786573/oz-pearlman-m | 0.725 | www.npr.org/sections/health/ | 0.698 |


**Q2: What world news is NPR covering?** [cross-page]
*(expects URL containing: `sections/world`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #12 | www.npr.org/1992/08/25/100441748/the-girlish-voice | 0.595 | www.npr.org/1992/08/25/100441748/the-girlish-voice | 0.507 | www.npr.org/1992/02/02/100211928/buddy-hollys-last | 0.507 |
| crawl4ai | #1 | www.npr.org/sections/world/ | 0.699 | www.npr.org/sections/news/archive | 0.691 | www.npr.org/sections/news/archive?start=placeholde | 0.691 |
| crawl4ai-raw | #1 | www.npr.org/sections/world/ | 0.693 | www.npr.org/sections/news/archive | 0.691 | www.npr.org/sections/news/archive?start=placeholde | 0.691 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | #1 | www.npr.org/podcasts/510366/state-of-the-world | 0.688 | www.npr.org/sections/national/ | 0.681 | www.npr.org/sections/technology/ | 0.681 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | www.npr.org/podcasts/510366/state-of-the-world | 0.688 | www.npr.org/sections/news/archive?start=placeholde | 0.681 | www.npr.org/2026/04/24/g-s1-118582/administration- | 0.681 |


**Q3: Where can I find NPR business coverage?** [cross-page]
*(expects URL containing: `sections/business`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | www.npr.org/1992/08/25/100441748/the-girlish-voice | 0.536 | www.npr.org/1992/01/01/4681853/the-marketplace-rep | 0.533 | www.npr.org/1993/05/21/1106944/cokie-roberts-polit | 0.504 |
| crawl4ai | #17 | www.npr.org/sections/law/ | 0.686 | www.npr.org/sections/national/ | 0.686 | www.npr.org/sections/news/ | 0.686 |
| crawl4ai-raw | #15 | www.npr.org/sections/national/ | 0.686 | www.npr.org/sections/food/ | 0.686 | www.npr.org/sections/technology/ | 0.686 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | #40 | www.npr.org/podcasts/510289/planet-money | 0.746 | www.npr.org/sections/news/ | 0.686 | www.npr.org/sections/law/ | 0.686 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #15 | www.npr.org/2026/04/23/nx-s1-5797307/europe-airlin | 0.686 | www.npr.org/2026/04/23/nx-s1-5797855/meta-layoffs- | 0.686 | www.npr.org/sections/politics/ | 0.686 |


**Q4: What health stories is NPR reporting on?** [cross-page]
*(expects URL containing: `sections/health`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.npr.org/1992/08/25/100441748/the-girlish-voice | 0.617 | www.npr.org/1993/06/17/1107002/robert-shope-co-cha | 0.569 | www.npr.org/1993/06/01/1106967/reporter-elizabeth- | 0.501 |
| crawl4ai | #12 | www.npr.org/ | 0.732 | www.npr.org/ | 0.732 | www.npr.org/ | 0.732 |
| crawl4ai-raw | #13 | www.npr.org/ | 0.732 | www.npr.org/ | 0.732 | www.npr.org/ | 0.732 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | #21 | www.npr.org/sections/immigration | 0.728 | www.npr.org/transcripts/nx-s1-5795526 | 0.728 | www.npr.org/sections/news/ | 0.728 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #3 | www.npr.org/2026/04/23/nx-s1-5795526/deafness-gene | 0.728 | www.npr.org/transcripts/nx-s1-5795526 | 0.728 | www.npr.org/2026/04/23/nx-s1-5792867/ai-chatbot-fl | 0.728 |


**Q5: What science news does NPR have?** [cross-page]
*(expects URL containing: `sections/science`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.npr.org/1992/08/25/100441748/the-girlish-voice | 0.561 | www.npr.org/1992/02/02/100211928/buddy-hollys-last | 0.521 | www.npr.org/1992/08/25/100441748/the-girlish-voice | 0.521 |
| crawl4ai | #31 | www.npr.org/2026/04/24/nx-s1-5793988/giant-octopus | 0.738 | www.npr.org/2026/04/24/nx-s1-5797863/self-aware-ro | 0.738 | www.npr.org/2026/04/24/nx-s1-5793988/giant-octopus | 0.738 |
| crawl4ai-raw | #22 | www.npr.org/2026/04/24/nx-s1-5797863/self-aware-ro | 0.738 | www.npr.org/sections/technology/ | 0.735 | www.npr.org/sections/news/archive?start=placeholde | 0.735 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | #30 | www.npr.org/2026/04/24/nx-s1-5797863/self-aware-ro | 0.735 | www.npr.org/2026/04/24/nx-s1-5797863/self-aware-ro | 0.735 | www.npr.org/sections/news/archive | 0.735 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #27 | www.npr.org/2026/04/24/nx-s1-5797863/self-aware-ro | 0.735 | www.npr.org/sections/news/ | 0.735 | www.npr.org/sections/food/ | 0.735 |


**Q6: What are the main news headlines from NPR?** [cross-page]
*(expects URL containing: `sections/news`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.npr.org/1992/08/25/100441748/the-girlish-voice | 0.614 | www.npr.org/1993/05/21/1106944/cokie-roberts-polit | 0.537 | www.npr.org/1992/08/25/100441748/the-girlish-voice | 0.533 |
| crawl4ai | #2 | www.npr.org/sections/national/ | 0.720 | www.npr.org/sections/news/ | 0.717 | www.npr.org/sections/news/archive | 0.717 |
| crawl4ai-raw | #1 | www.npr.org/sections/news/ | 0.723 | www.npr.org/sections/national/ | 0.721 | www.npr.org/sections/news/archive | 0.717 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | #2 | www.npr.org/sections/national/ | 0.696 | www.npr.org/sections/news/archive | 0.691 | www.npr.org/sections/news/archive?start=placeholde | 0.691 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #15 | www.npr.org/podcasts-and-shows | 0.679 | www.npr.org/podcasts-and-shows/ | 0.679 | www.npr.org/transcripts/nx-s1-5746844 | 0.672 |


</details>

## postgres-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 62% (5/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.755 | 2006 | 400 |
| colly+md | 62% (5/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.755 | 2014 | 398 |
| playwright | 62% (5/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.755 | 2005 | 400 |
| crawl4ai | 50% (4/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.691 | 1987 | 400 |
| crawl4ai-raw | 50% (4/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.691 | 1987 | 400 |
| scrapy+md | 25% (2/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 62% (5/8) | 0.366 | 2839 | 400 |
| markcrawl | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.062 | 3670 | 400 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for postgres-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What data types does PostgreSQL support?** [cross-page]
*(expects URL containing: `datatype`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/about/press/presskit15/en/ | 0.606 | www.postgresql.org/about/press/presskit13/es/ | 0.606 | www.postgresql.org/about/press/presskit14/ko/ | 0.606 |
| crawl4ai | #1 | www.postgresql.org/docs/current/datatype.html | 0.725 | www.postgresql.org/docs/17/datatype.html | 0.724 | www.postgresql.org/docs/18/datatype.html | 0.723 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/datatype.html | 0.725 | www.postgresql.org/docs/17/datatype.html | 0.724 | www.postgresql.org/docs/18/datatype.html | 0.723 |
| scrapy+md | #1 | www.postgresql.org/docs/9.0/datatype-datetime.html | 0.620 | www.postgresql.org/docs/current/ | 0.616 | www.postgresql.org/docs/9.1/datatype-datetime.html | 0.614 |
| crawlee | #2 | www.postgresql.org/about/ | 0.657 | www.postgresql.org/docs/current/datatype.html | 0.646 | www.postgresql.org/docs/18/datatype.html | 0.646 |
| colly+md | #2 | www.postgresql.org/about/ | 0.657 | www.postgresql.org/docs/18/datatype.html | 0.646 | www.postgresql.org/docs/17/datatype.html | 0.646 |
| playwright | #2 | www.postgresql.org/about/ | 0.657 | www.postgresql.org/docs/17/datatype.html | 0.646 | www.postgresql.org/docs/current/datatype.html | 0.646 |


**Q2: What is the SQL syntax for queries in PostgreSQL?** [conceptual]
*(expects URL containing: `sql-syntax`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/about/press/presskit92/ua/ | 0.564 | www.postgresql.org/about/press/presskit93/ua/ | 0.556 | www.postgresql.org/about/press/presskit13/es/ | 0.556 |
| crawl4ai | #37 | www.postgresql.org/docs/current/sql.html | 0.645 | www.postgresql.org/docs/18/sql.html | 0.639 | www.postgresql.org/docs/17/sql.html | 0.639 |
| crawl4ai-raw | #37 | www.postgresql.org/docs/current/sql.html | 0.646 | www.postgresql.org/docs/18/sql.html | 0.639 | www.postgresql.org/docs/17/sql.html | 0.639 |
| scrapy+md | miss | www.postgresql.org/docs/8.2/sql.html | 0.651 | www.postgresql.org/docs/7.2/tutorial.html | 0.615 | www.postgresql.org/docs/7.1/developer.html | 0.608 |
| crawlee | #23 | www.postgresql.org/docs/17/sql.html | 0.629 | www.postgresql.org/docs/18/sql.html | 0.629 | www.postgresql.org/docs/current/sql.html | 0.629 |
| colly+md | #23 | www.postgresql.org/docs/18/sql.html | 0.629 | www.postgresql.org/docs/17/sql.html | 0.629 | www.postgresql.org/docs/current/sql.html | 0.629 |
| playwright | #23 | www.postgresql.org/docs/18/sql.html | 0.629 | www.postgresql.org/docs/current/sql.html | 0.629 | www.postgresql.org/docs/17/sql.html | 0.629 |


**Q3: How do indexes work in PostgreSQL?** [conceptual]
*(expects URL containing: `indexes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/about/press/presskit18/en/ | 0.552 | www.postgresql.org/about/press/presskit17/en/ | 0.551 | www.postgresql.org/about/policies/planet-postgresq | 0.548 |
| crawl4ai | #1 | www.postgresql.org/docs/current/indexes.html | 0.610 | www.postgresql.org/docs/17/indexes.html | 0.610 | www.postgresql.org/docs/18/indexes.html | 0.607 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/indexes.html | 0.610 | www.postgresql.org/docs/17/indexes.html | 0.610 | www.postgresql.org/docs/18/indexes.html | 0.607 |
| scrapy+md | #2 | www.postgresql.org/docs/9.2/sql-createindex.html | 0.621 | www.postgresql.org/docs/8.2/locking-indexes.html | 0.618 | www.postgresql.org/docs/9.2/sql-createindex.html | 0.597 |
| crawlee | #1 | www.postgresql.org/docs/18/indexes.html | 0.612 | www.postgresql.org/docs/current/indexes.html | 0.612 | www.postgresql.org/docs/17/indexes.html | 0.610 |
| colly+md | #1 | www.postgresql.org/docs/current/indexes.html | 0.612 | www.postgresql.org/docs/18/indexes.html | 0.612 | www.postgresql.org/docs/17/indexes.html | 0.610 |
| playwright | #1 | www.postgresql.org/docs/18/indexes.html | 0.612 | www.postgresql.org/docs/current/indexes.html | 0.612 | www.postgresql.org/docs/17/indexes.html | 0.610 |


**Q4: How does MVCC concurrency control work in PostgreSQL?** [conceptual]
*(expects URL containing: `mvcc`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/about/press/presskit17/en/ | 0.448 | www.postgresql.org/about/press/presskit11/en/ | 0.445 | www.postgresql.org/about/news/pg_ivm-114-released- | 0.439 |
| crawl4ai | #1 | www.postgresql.org/docs/17/mvcc.html | 0.611 | www.postgresql.org/docs/18/mvcc.html | 0.610 | www.postgresql.org/docs/current/mvcc.html | 0.608 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/mvcc.html | 0.611 | www.postgresql.org/docs/18/mvcc.html | 0.610 | www.postgresql.org/docs/current/mvcc.html | 0.608 |
| scrapy+md | #3 | www.postgresql.org/docs/8.0/transaction-iso.html | 0.664 | www.postgresql.org/docs/8.1/transaction-iso.html | 0.662 | www.postgresql.org/docs/8.2/mvcc.html | 0.641 |
| crawlee | #1 | www.postgresql.org/docs/17/mvcc.html | 0.631 | www.postgresql.org/docs/current/mvcc.html | 0.630 | www.postgresql.org/docs/18/mvcc.html | 0.630 |
| colly+md | #1 | www.postgresql.org/docs/17/mvcc.html | 0.631 | www.postgresql.org/docs/current/mvcc.html | 0.630 | www.postgresql.org/docs/18/mvcc.html | 0.630 |
| playwright | #1 | www.postgresql.org/docs/17/mvcc.html | 0.631 | www.postgresql.org/docs/18/mvcc.html | 0.630 | www.postgresql.org/docs/current/mvcc.html | 0.630 |


**Q5: How do transactions work in PostgreSQL?** [conceptual]
*(expects URL containing: `transactions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/about/press/presskit11/en/ | 0.635 | www.postgresql.org/about/press/presskit11/fr/ | 0.598 | www.postgresql.org/about/press/presskit11/my/ | 0.588 |
| crawl4ai | #2 | www.postgresql.org/about/featurematrix/ | 0.585 | www.postgresql.org/docs/current/transactions.html | 0.581 | www.postgresql.org/docs/18/transactions.html | 0.580 |
| crawl4ai-raw | #2 | www.postgresql.org/about/featurematrix/ | 0.585 | www.postgresql.org/docs/current/transactions.html | 0.581 | www.postgresql.org/docs/18/transactions.html | 0.580 |
| scrapy+md | miss | www.postgresql.org/docs/8.4/pgbench.html | 0.626 | www.postgresql.org/docs/7.2/transaction-iso.html | 0.606 | www.postgresql.org/docs/8.0/transaction-iso.html | 0.595 |
| crawlee | #2 | www.postgresql.org/about/featurematrix/ | 0.601 | www.postgresql.org/docs/current/transactions.html | 0.591 | www.postgresql.org/docs/18/transactions.html | 0.591 |
| colly+md | #2 | www.postgresql.org/about/featurematrix/ | 0.601 | www.postgresql.org/docs/18/transactions.html | 0.591 | www.postgresql.org/docs/current/transactions.html | 0.591 |
| playwright | #2 | www.postgresql.org/about/featurematrix/ | 0.601 | www.postgresql.org/docs/18/transactions.html | 0.591 | www.postgresql.org/docs/current/transactions.html | 0.591 |


**Q6: How do I set up logical replication in PostgreSQL?** [api-function]
*(expects URL containing: `logical-replication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/about/press/presskit16/en/ | 0.715 | www.postgresql.org/about/press/presskit18/en/ | 0.684 | www.postgresql.org/about/press/presskit15/en/ | 0.662 |
| crawl4ai | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.701 | www.postgresql.org/docs/18/logical-replication.htm | 0.699 | www.postgresql.org/docs/17/logical-replication.htm | 0.694 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.701 | www.postgresql.org/docs/18/logical-replication.htm | 0.699 | www.postgresql.org/docs/17/logical-replication.htm | 0.694 |
| scrapy+md | miss | www.postgresql.org/docs/8.4/warm-standby.html | 0.540 | www.postgresql.org/docs/7.2/tutorial.html | 0.525 | www.postgresql.org/docs/8.4/warm-standby.html | 0.500 |
| crawlee | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.679 | www.postgresql.org/docs/18/logical-replication.htm | 0.679 | www.postgresql.org/docs/17/logical-replication.htm | 0.673 |
| colly+md | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.679 | www.postgresql.org/docs/current/logical-replicatio | 0.679 | www.postgresql.org/docs/17/logical-replication.htm | 0.673 |
| playwright | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.679 | www.postgresql.org/docs/current/logical-replicatio | 0.679 | www.postgresql.org/docs/17/logical-replication.htm | 0.673 |


**Q7: What built-in functions and operators are available in PostgreSQL?** [cross-page]
*(expects URL containing: `functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/about/press/presskit13/es/ | 0.621 | www.postgresql.org/about/press/presskit15/en/ | 0.621 | www.postgresql.org/about/press/presskit13/pl/ | 0.621 |
| crawl4ai | #2 | www.postgresql.org/about/ | 0.674 | www.postgresql.org/docs/17/functions.html | 0.652 | www.postgresql.org/docs/7.2/index.html | 0.652 |
| crawl4ai-raw | #2 | www.postgresql.org/about/ | 0.674 | www.postgresql.org/docs/17/functions.html | 0.652 | www.postgresql.org/docs/7.2/index.html | 0.652 |
| scrapy+md | #11 | www.postgresql.org/docs/7.1/developer.html | 0.641 | www.postgresql.org/docs/current/ | 0.640 | www.postgresql.org/docs/9.1/xfunc.html | 0.635 |
| crawlee | #1 | www.postgresql.org/docs/current/functions.html | 0.672 | www.postgresql.org/docs/18/functions.html | 0.672 | www.postgresql.org/docs/17/functions.html | 0.672 |
| colly+md | #1 | www.postgresql.org/docs/current/functions.html | 0.672 | www.postgresql.org/docs/18/functions.html | 0.672 | www.postgresql.org/docs/17/functions.html | 0.672 |
| playwright | #1 | www.postgresql.org/docs/current/functions.html | 0.672 | www.postgresql.org/docs/18/functions.html | 0.672 | www.postgresql.org/docs/17/functions.html | 0.672 |


**Q8: How do I use full text search in PostgreSQL?** [api-function]
*(expects URL containing: `textsearch`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.postgresql.org/about/press/presskit96/en/ | 0.619 | www.postgresql.org/about/news/pg_textsearch-v10-32 | 0.604 | www.postgresql.org/about/press/presskit96/de/ | 0.586 |
| crawl4ai | #2 | www.postgresql.org/docs/current/pgtrgm.html | 0.600 | www.postgresql.org/docs/17/textsearch.html | 0.591 | www.postgresql.org/docs/current/textsearch.html | 0.589 |
| crawl4ai-raw | #2 | www.postgresql.org/docs/current/pgtrgm.html | 0.600 | www.postgresql.org/docs/17/textsearch.html | 0.591 | www.postgresql.org/docs/17/textsearch.html | 0.589 |
| scrapy+md | #1 | www.postgresql.org/docs/10/textsearch-limitations. | 0.607 | www.postgresql.org/docs/9.3/textsearch-limitations | 0.604 | www.postgresql.org/docs/9.6/textsearch-limitations | 0.603 |
| crawlee | #1 | www.postgresql.org/docs/17/textsearch.html | 0.703 | www.postgresql.org/docs/current/textsearch.html | 0.702 | www.postgresql.org/docs/18/textsearch.html | 0.702 |
| colly+md | #1 | www.postgresql.org/docs/17/textsearch.html | 0.703 | www.postgresql.org/docs/18/textsearch.html | 0.702 | www.postgresql.org/docs/current/textsearch.html | 0.702 |
| playwright | #1 | www.postgresql.org/docs/17/textsearch.html | 0.703 | www.postgresql.org/docs/18/textsearch.html | 0.702 | www.postgresql.org/docs/current/textsearch.html | 0.702 |


</details>

## react-dev

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 75% (12/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 100% (16/16) | 0.859 | 3359 | 221 |
| colly+md | 75% (12/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.825 | 9345 | 291 |
| crawl4ai | 75% (12/16) | 88% (14/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 0.813 | 9472 | 500 |
| crawl4ai-raw | 75% (12/16) | 88% (14/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 0.813 | 9472 | 500 |
| scrapy+md | 69% (11/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.790 | 3513 | 216 |
| crawlee | 69% (11/16) | 81% (13/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.785 | 6434 | 217 |
| playwright | 69% (11/16) | 81% (13/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.785 | 6398 | 221 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for react-dev</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I manage state in a React component?** [conceptual]
*(expects URL containing: `state`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/managing-state | 0.725 | react.dev/learn/sharing-state-between-components | 0.709 |
| crawl4ai | #1 | react.dev/learn/preserving-and-resetting-state | 0.712 | he.react.dev/learn/managing-state | 0.706 | 18.react.dev/learn/managing-state | 0.704 |
| crawl4ai-raw | #1 | react.dev/learn/preserving-and-resetting-state | 0.712 | he.react.dev/learn/managing-state | 0.706 | 18.react.dev/learn/managing-state | 0.704 |
| scrapy+md | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |
| crawlee | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |
| colly+md | #1 | react.dev/learn/preserving-and-resetting-state#opt | 0.736 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/preserving-and-resetting-state#dif | 0.736 |
| playwright | #1 | react.dev/learn/preserving-and-resetting-state | 0.736 | react.dev/learn/reacting-to-input-with-state | 0.691 | react.dev/learn/state-a-components-memory | 0.689 |


**Q2: How does the useEffect hook work in React?** [api-function]
*(expects URL containing: `useEffect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useEffect | 0.749 | react.dev/reference/react/useEffect | 0.742 | react.dev/reference/react/useEffectEvent | 0.696 |
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
| crawlee | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/reference/react/createContext | 0.708 | react.dev/learn/passing-data-deeply-with-context | 0.705 |
| colly+md | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/reference/react/createContext | 0.708 | react.dev/learn/passing-data-deeply-with-context | 0.705 |
| playwright | #1 | react.dev/reference/react/createContext | 0.727 | react.dev/reference/react/createContext | 0.708 | react.dev/learn/passing-data-deeply-with-context | 0.705 |


**Q4: What is JSX and how does React use it?** [conceptual]
*(expects URL containing: `writing-markup-with-jsx`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/writing-markup-with-jsx | 0.727 | react.dev/learn/writing-markup-with-jsx | 0.707 | react.dev/learn/writing-markup-with-jsx | 0.706 |
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
| markcrawl | #2 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/rendering-lists | 0.721 | react.dev/learn/tutorial-tic-tac-toe | 0.716 |
| crawl4ai | #1 | react.dev/learn/rendering-lists | 0.751 | de.react.dev/learn/describing-the-ui | 0.734 | 18.react.dev/learn/describing-the-ui | 0.733 |
| crawl4ai-raw | #1 | react.dev/learn/rendering-lists | 0.751 | de.react.dev/learn/describing-the-ui | 0.733 | 18.react.dev/learn/describing-the-ui | 0.733 |
| scrapy+md | #5 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.700 |
| crawlee | #5 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.698 |
| colly+md | #6 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn#components | 0.700 |
| playwright | #5 | react.dev/learn/describing-the-ui | 0.724 | react.dev/learn/tutorial-tic-tac-toe | 0.716 | react.dev/learn | 0.700 |


**Q6: How do I use the useRef hook in React?** [api-function]
*(expects URL containing: `useRef`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useRef | 0.802 | react.dev/reference/react/useRef | 0.755 | react.dev/reference/react/useRef | 0.675 |
| crawl4ai | #1 | react.dev/reference/react/useRef | 0.732 | react.dev/learn/referencing-values-with-refs | 0.721 | react.dev/reference/react/useRef | 0.704 |
| crawl4ai-raw | #1 | react.dev/reference/react/useRef | 0.732 | react.dev/learn/referencing-values-with-refs | 0.721 | react.dev/reference/react/useRef | 0.704 |
| scrapy+md | #1 | react.dev/reference/react/useRef | 0.758 | react.dev/learn/referencing-values-with-refs | 0.719 | react.dev/reference/react/useRef | 0.674 |
| crawlee | #1 | react.dev/reference/react/useRef | 0.758 | react.dev/learn/referencing-values-with-refs | 0.719 | react.dev/reference/react/useRef | 0.674 |
| colly+md | #1 | react.dev/reference/react/useRef#reference | 0.758 | react.dev/reference/react/useRef | 0.758 | react.dev/reference/react/useRef#returns | 0.758 |
| playwright | #1 | react.dev/reference/react/useRef | 0.758 | react.dev/learn/referencing-values-with-refs | 0.719 | react.dev/reference/react/useRef | 0.674 |


**Q7: How do I pass props between React components?** [conceptual]
*(expects URL containing: `passing-props`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/passing-props-to-a-component | 0.791 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 |
| crawl4ai | #2 | de.react.dev/learn/describing-the-ui | 0.761 | react.dev/learn/passing-props-to-a-component | 0.758 | az.react.dev/learn/describing-the-ui | 0.755 |
| crawl4ai-raw | #2 | de.react.dev/learn/describing-the-ui | 0.761 | react.dev/learn/passing-props-to-a-component | 0.758 | az.react.dev/learn/describing-the-ui | 0.755 |
| scrapy+md | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |
| crawlee | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |
| colly+md | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/passing-props-to-a-component#passi | 0.787 | react.dev/learn/describing-the-ui | 0.763 |
| playwright | #1 | react.dev/learn/passing-props-to-a-component | 0.787 | react.dev/learn/describing-the-ui | 0.763 | react.dev/learn/passing-data-deeply-with-context | 0.708 |


**Q8: How do I conditionally render content in React?** [code-example]
*(expects URL containing: `conditional-rendering`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn | 0.750 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/conditional-rendering | 0.719 |
| crawl4ai | #10 | 18.react.dev/learn/describing-the-ui | 0.760 | react.dev/learn/describing-the-ui | 0.751 | de.react.dev/learn/describing-the-ui | 0.750 |
| crawl4ai-raw | #10 | 18.react.dev/learn/describing-the-ui | 0.759 | react.dev/learn/describing-the-ui | 0.751 | de.react.dev/learn/describing-the-ui | 0.750 |
| scrapy+md | #3 | react.dev/learn | 0.748 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 |
| crawlee | #2 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/describing-the-ui | 0.705 |
| colly+md | #3 | react.dev/learn | 0.748 | react.dev/learn#components | 0.748 | react.dev/learn/conditional-rendering | 0.744 |
| playwright | #2 | react.dev/learn | 0.748 | react.dev/learn/conditional-rendering | 0.744 | react.dev/learn/describing-the-ui | 0.703 |


**Q9: What is the useMemo hook for in React?** [api-function]
*(expects URL containing: `useMemo`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useMemo | 0.803 | react.dev/reference/react/useMemo | 0.736 | react.dev/reference/react/useCallback | 0.651 |
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
| markcrawl | #1 | react.dev/reference/react/useState | 0.753 | react.dev/reference/react/useState | 0.716 | react.dev/learn | 0.682 |
| crawl4ai | #1 | react.dev/reference/react/useState | 0.719 | 18.react.dev/learn | 0.698 | he.react.dev/learn | 0.695 |
| crawl4ai-raw | #1 | react.dev/reference/react/useState | 0.719 | 18.react.dev/learn | 0.698 | he.react.dev/learn | 0.695 |
| scrapy+md | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn | 0.682 |
| crawlee | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |
| colly+md | #1 | react.dev/reference/react/useState#storing-informa | 0.751 | react.dev/reference/react/useState#updating-state- | 0.751 | react.dev/reference/react/useState | 0.751 |
| playwright | #1 | react.dev/reference/react/useState | 0.751 | react.dev/learn | 0.682 | react.dev/learn/state-a-components-memory | 0.652 |


**Q11: How do I use the useCallback hook in React?** [api-function]
*(expects URL containing: `useCallback`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useCallback | 0.806 | react.dev/reference/react/useCallback | 0.747 | react.dev/learn/typescript | 0.656 |
| crawl4ai | #1 | react.dev/reference/react/useCallback | 0.703 | react.dev/reference/react/useCallback | 0.681 | react.dev/learn/typescript | 0.668 |
| crawl4ai-raw | #1 | react.dev/reference/react/useCallback | 0.703 | react.dev/reference/react/useCallback | 0.681 | react.dev/learn/typescript | 0.668 |
| scrapy+md | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.655 | react.dev/reference/react/useCallback | 0.644 |
| crawlee | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript | 0.655 | react.dev/reference/react/useCallback | 0.644 |
| colly+md | #1 | react.dev/reference/react/useCallback | 0.746 | react.dev/learn/typescript#example-hooks | 0.655 | react.dev/learn/typescript#typescript-with-react-c | 0.655 |
| playwright | #1 | react.dev/reference/react/useCallback | 0.747 | react.dev/learn/typescript | 0.655 | react.dev/reference/react/useCallback | 0.644 |


**Q12: How do I use the useReducer hook in React?** [api-function]
*(expects URL containing: `useReducer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useReducer | 0.810 | react.dev/reference/react/useReducer | 0.788 | react.dev/reference/react/useReducer | 0.733 |
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
| crawl4ai | #1 | react.dev/learn/responding-to-events | 0.690 | 18.react.dev/learn | 0.689 | az.react.dev/learn | 0.687 |
| crawl4ai-raw | #1 | react.dev/learn/responding-to-events | 0.690 | 18.react.dev/learn | 0.689 | az.react.dev/learn | 0.687 |
| scrapy+md | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.668 | react.dev/learn | 0.668 |
| crawlee | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.668 | react.dev/learn/adding-interactivity | 0.645 |
| colly+md | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn/responding-to-events#passing-event | 0.699 | react.dev/learn | 0.668 |
| playwright | #1 | react.dev/learn/responding-to-events | 0.699 | react.dev/learn | 0.668 | react.dev/learn/adding-interactivity | 0.668 |


**Q14: What is the Suspense component in React?** [api-function]
*(expects URL containing: `Suspense`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/Suspense | 0.730 | react.dev/blog/2022/03/29/react-v18 | 0.725 | react.dev/blog/2022/03/29/react-v18 | 0.712 |
| crawl4ai | #3 | react.dev/blog/2022/03/29/react-v18 | 0.734 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/reference/react/Suspense | 0.720 |
| crawl4ai-raw | #3 | react.dev/blog/2022/03/29/react-v18 | 0.734 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/reference/react/Suspense | 0.720 |
| scrapy+md | #9 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.712 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.681 |
| crawlee | #9 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.712 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.681 |
| colly+md | #1 | react.dev/blog/2022/03/29/react-v18#suspense-in-da | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.712 |
| playwright | #9 | react.dev/blog/2022/03/29/react-v18 | 0.726 | react.dev/blog/2022/03/29/react-v18 | 0.712 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.681 |


**Q15: How do I add interactivity to React components?** [conceptual]
*(expects URL containing: `adding-interactivity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.765 | react.dev/learn/adding-interactivity | 0.756 |
| crawl4ai | #13 | 18.react.dev/ | 0.830 | pl.react.dev/ | 0.830 | ru.react.dev/ | 0.830 |
| crawl4ai-raw | #13 | 18.react.dev | 0.830 | react.dev/ | 0.830 | az.react.dev/ | 0.830 |
| scrapy+md | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/learn/responding-to-events | 0.724 |
| crawlee | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |
| colly+md | #2 | react.dev/learn | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |
| playwright | #2 | react.dev/ | 0.820 | react.dev/learn/adding-interactivity | 0.756 | react.dev/reference/rsc/server-components | 0.686 |


**Q16: How do I install and set up a new React project?** [conceptual]
*(expects URL containing: `installation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | react.dev/learn/setup | 0.688 | react.dev/learn/add-react-to-an-existing-project | 0.672 | react.dev/learn/add-react-to-an-existing-project | 0.665 |
| crawl4ai | #1 | 18.react.dev/learn/installation | 0.738 | he.react.dev/learn/installation | 0.738 | he.react.dev/learn/installation | 0.727 |
| crawl4ai-raw | #1 | 18.react.dev/learn/installation | 0.738 | he.react.dev/learn/installation | 0.738 | he.react.dev/learn/installation | 0.727 |
| scrapy+md | #2 | react.dev/learn/add-react-to-an-existing-project | 0.672 | react.dev/learn/react-compiler/installation | 0.660 | react.dev/learn/creating-a-react-app | 0.642 |
| crawlee | #4 | react.dev/learn/setup | 0.693 | react.dev/learn/react-compiler | 0.678 | react.dev/learn/add-react-to-an-existing-project | 0.672 |
| colly+md | #5 | react.dev/learn/setup | 0.693 | react.dev/learn/react-compiler | 0.678 | react.dev/learn/add-react-to-an-existing-project | 0.672 |
| playwright | #4 | react.dev/learn/setup | 0.693 | react.dev/learn/react-compiler | 0.678 | react.dev/learn/add-react-to-an-existing-project | 0.672 |


</details>

## rust-book

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 62% (5/8) | 62% (5/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.699 | 6314 | 200 |
| playwright | 50% (4/8) | 75% (6/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.647 | 6314 | 200 |
| markcrawl | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 15673 | 200 |
| crawl4ai | 0% (0/8) | 75% (6/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.358 | 6074 | 200 |
| crawl4ai-raw | 0% (0/8) | 75% (6/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.358 | 6074 | 200 |
| scrapy+md | 0% (0/8) | 12% (1/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 0.094 | 12404 | 199 |
| colly+md | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.042 | 5550 | 54 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for rust-book</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is ownership in Rust?** [conceptual]
*(expects URL containing: `ch04-01-what-is-ownership`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/print.html | 0.739 | doc.rust-lang.org/book/print.html | 0.737 | doc.rust-lang.org/book/print.html | 0.712 |
| crawl4ai | #3 | doc.rust-lang.org/book/print.html | 0.784 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.761 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/print.html | 0.784 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.761 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.739 | doc.rust-lang.org/book/print.html | 0.737 | doc.rust-lang.org/book/print.html | 0.712 |
| crawlee | #1 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.739 | doc.rust-lang.org/book/print.html | 0.739 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.739 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.739 | doc.rust-lang.org/stable/book/print.html | 0.739 | doc.rust-lang.org/book/print.html | 0.737 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.739 | doc.rust-lang.org/book/print.html | 0.739 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.739 |


**Q2: How do references and borrowing work in Rust?** [conceptual]
*(expects URL containing: `ch04-02-references-and-borrowing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/src/core/borrow.rs.html | 0.679 | doc.rust-lang.org/std/primitive.reference.html | 0.675 | doc.rust-lang.org/reference/print.html | 0.674 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.838 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.787 | doc.rust-lang.org/book/print.html | 0.785 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.838 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.787 | doc.rust-lang.org/book/print.html | 0.785 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/book/print.html | 0.638 | doc.rust-lang.org/book/print.html | 0.627 |
| crawlee | #5 | doc.rust-lang.org/book/ch10-03-lifetime-syntax.htm | 0.649 | doc.rust-lang.org/stable/book/ch10-03-lifetime-syn | 0.649 | doc.rust-lang.org/book/print.html | 0.649 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/stable/book/print.html | 0.649 | doc.rust-lang.org/book/print.html | 0.638 |
| playwright | #5 | doc.rust-lang.org/stable/book/ch10-03-lifetime-syn | 0.649 | doc.rust-lang.org/book/ch10-03-lifetime-syntax.htm | 0.649 | doc.rust-lang.org/book/print.html | 0.649 |


**Q3: How do I define structs in Rust?** [api-function]
*(expects URL containing: `ch05-01-defining-structs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/print.html | 0.658 | doc.rust-lang.org/book/print.html | 0.631 | doc.rust-lang.org/book/print.html | 0.630 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.745 | doc.rust-lang.org/book/ch05-00-structs.html | 0.682 | doc.rust-lang.org/stable/book/ch05-00-structs.html | 0.682 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.745 | doc.rust-lang.org/book/ch05-00-structs.html | 0.682 | doc.rust-lang.org/stable/book/ch05-00-structs.html | 0.682 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.658 | doc.rust-lang.org/book/print.html | 0.631 | doc.rust-lang.org/book/print.html | 0.630 |
| crawlee | #1 | doc.rust-lang.org/book/ch05-00-structs.html | 0.688 | doc.rust-lang.org/stable/book/ch05-00-structs.html | 0.688 | doc.rust-lang.org/book/print.html | 0.658 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.659 | doc.rust-lang.org/stable/book/print.html | 0.659 | doc.rust-lang.org/stable/book/print.html | 0.631 |
| playwright | #1 | doc.rust-lang.org/book/ch05-00-structs.html | 0.688 | doc.rust-lang.org/stable/book/ch05-00-structs.html | 0.688 | doc.rust-lang.org/book/print.html | 0.658 |


**Q4: How do enums work in Rust?** [conceptual]
*(expects URL containing: `ch06-01-defining-an-enum`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/print.html | 0.651 | doc.rust-lang.org/reference/print.html | 0.635 | doc.rust-lang.org/book/print.html | 0.634 |
| crawl4ai | #4 | doc.rust-lang.org/book/print.html | 0.671 | doc.rust-lang.org/std/sync/atomic/index.html | 0.650 | doc.rust-lang.org/book/print.html | 0.650 |
| crawl4ai-raw | #4 | doc.rust-lang.org/book/print.html | 0.671 | doc.rust-lang.org/std/sync/atomic/index.html | 0.650 | doc.rust-lang.org/book/print.html | 0.650 |
| scrapy+md | #4 | doc.rust-lang.org/book/print.html | 0.629 | doc.rust-lang.org/book/print.html | 0.622 | doc.rust-lang.org/book/print.html | 0.614 |
| crawlee | #4 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.667 | doc.rust-lang.org/stable/book/ch06-03-if-let.html | 0.667 | doc.rust-lang.org/book/print.html | 0.629 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.629 | doc.rust-lang.org/stable/book/print.html | 0.629 | doc.rust-lang.org/book/print.html | 0.622 |
| playwright | #3 | doc.rust-lang.org/stable/book/ch06-03-if-let.html | 0.667 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.667 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.629 |


**Q5: How do I use generics in Rust?** [conceptual]
*(expects URL containing: `ch10-01-syntax`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/reference/items/generics.html | 0.702 | doc.rust-lang.org/book/print.html | 0.619 | doc.rust-lang.org/reference/items/generics.html | 0.611 |
| crawl4ai | #3 | doc.rust-lang.org/book/print.html | 0.695 | doc.rust-lang.org/book/print.html | 0.668 | doc.rust-lang.org/stable/book/ch10-01-syntax.html | 0.665 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/print.html | 0.695 | doc.rust-lang.org/book/print.html | 0.668 | doc.rust-lang.org/stable/book/ch10-01-syntax.html | 0.665 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.619 | doc.rust-lang.org/book/print.html | 0.594 | doc.rust-lang.org/book/print.html | 0.585 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch10-01-syntax.html | 0.620 | doc.rust-lang.org/book/ch10-01-syntax.html | 0.620 | doc.rust-lang.org/book/print.html | 0.619 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.619 | doc.rust-lang.org/book/print.html | 0.619 | doc.rust-lang.org/book/print.html | 0.594 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch10-01-syntax.html | 0.620 | doc.rust-lang.org/book/ch10-01-syntax.html | 0.620 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.619 |


**Q6: What are traits in Rust and how do I define them?** [conceptual]
*(expects URL containing: `ch10-02-traits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/reference/items/traits.html | 0.747 | doc.rust-lang.org/book/print.html | 0.729 | doc.rust-lang.org/reference/print.html | 0.632 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.727 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.727 | doc.rust-lang.org/book/print.html | 0.685 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.727 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.727 | doc.rust-lang.org/book/print.html | 0.685 |
| scrapy+md | #2 | doc.rust-lang.org/book/print.html | 0.729 | doc.rust-lang.org/reference/items/traits.html | 0.602 | doc.rust-lang.org/book/print.html | 0.577 |
| crawlee | #1 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.737 | doc.rust-lang.org/book/print.html | 0.729 | doc.rust-lang.org/reference/items/traits.html#dyn- | 0.594 |
| colly+md | #3 | doc.rust-lang.org/stable/book/print.html | 0.729 | doc.rust-lang.org/book/print.html | 0.729 | doc.rust-lang.org/reference/items/traits.html#dyn- | 0.601 |
| playwright | #1 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.737 | doc.rust-lang.org/book/print.html | 0.729 | doc.rust-lang.org/reference/items/traits.html | 0.594 |


**Q7: How do closures work in Rust?** [conceptual]
*(expects URL containing: `ch13-01-closures`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/print.html | 0.750 | doc.rust-lang.org/reference/print.html | 0.646 | doc.rust-lang.org/book/print.html | 0.644 |
| crawl4ai | #3 | doc.rust-lang.org/book/print.html | 0.758 | doc.rust-lang.org/book/print.html | 0.743 | doc.rust-lang.org/book/ch13-01-closures.html | 0.737 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/print.html | 0.758 | doc.rust-lang.org/book/print.html | 0.743 | doc.rust-lang.org/book/ch13-01-closures.html | 0.737 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.750 | doc.rust-lang.org/reference/types/closure.html | 0.641 | doc.rust-lang.org/book/print.html | 0.640 |
| crawlee | #1 | doc.rust-lang.org/book/ch13-01-closures.html | 0.750 | doc.rust-lang.org/book/print.html | 0.750 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.643 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.750 | doc.rust-lang.org/book/print.html | 0.750 | doc.rust-lang.org/stable/book/print.html | 0.640 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.750 | doc.rust-lang.org/book/ch13-01-closures.html | 0.750 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.643 |


**Q8: How do I handle errors with Result in Rust?** [conceptual]
*(expects URL containing: `ch09`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch09-02-recoverable-errors- | 0.848 | doc.rust-lang.org/std/result/index.html | 0.776 | doc.rust-lang.org/std/result/enum.Result.html | 0.722 |
| crawl4ai | #9 | doc.rust-lang.org/book/print.html | 0.760 | doc.rust-lang.org/std/result/enum.Result.html | 0.709 | doc.rust-lang.org/std/result/enum.Result.html | 0.683 |
| crawl4ai-raw | #9 | doc.rust-lang.org/book/print.html | 0.760 | doc.rust-lang.org/std/result/enum.Result.html | 0.709 | doc.rust-lang.org/std/result/enum.Result.html | 0.683 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.667 | doc.rust-lang.org/std/result/enum.Result.html | 0.654 | doc.rust-lang.org/std/result/enum.Result.html | 0.626 |
| crawlee | #7 | doc.rust-lang.org/book/print.html | 0.667 | doc.rust-lang.org/book/ch02-00-guessing-game-tutor | 0.663 | doc.rust-lang.org/stable/book/ch02-00-guessing-gam | 0.663 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.667 | doc.rust-lang.org/book/print.html | 0.667 | doc.rust-lang.org/std/result/enum.Result.html | 0.654 |
| playwright | #7 | doc.rust-lang.org/book/print.html | 0.667 | doc.rust-lang.org/book/ch02-00-guessing-game-tutor | 0.663 | doc.rust-lang.org/stable/book/ch02-00-guessing-gam | 0.662 |


</details>

## smittenkitchen

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 62% (5/8) | 62% (5/8) | 62% (5/8) | 62% (5/8) | 62% (5/8) | 0.629 | 11370 | 200 |
| crawl4ai | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 3895 | 200 |
| crawl4ai-raw | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 3895 | 200 |
| scrapy+md | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 40444 | 184 |
| crawlee | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 4936 | 207 |
| playwright | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 3770 | 200 |
| colly+md | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for smittenkitchen</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do you make world peace cookies?** [factual-lookup]
*(expects URL containing: `world-peace-cookies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2007/01/world-peace-cookies/ | 0.700 | smittenkitchen.com/2007/01/world-peace-cookies/ | 0.698 | smittenkitchen.com/2007/01/world-peace-cookies/ | 0.696 |
| crawl4ai | miss | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.418 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.406 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.399 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.418 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.406 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.399 |
| scrapy+md | miss | smittenkitchen.com/2015/04/salted-chocolate-chunk- | 0.431 | smittenkitchen.com/2015/04/salted-chocolate-chunk- | 0.430 | smittenkitchen.com/2015/04/salted-chocolate-chunk- | 0.427 |
| crawlee | miss | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.428 | smittenkitchen.com/./recipes/ingredient/peanut-but | 0.392 | smittenkitchen.com/about/faq/ | 0.366 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | smittenkitchen.com/recipes/sweets/cookie/?format=p | 0.428 | smittenkitchen.com/recipes/ingredient/peanut-butte | 0.392 | smittenkitchen.com/ | 0.372 |


**Q2: What's the recipe for miso chicken and rice?** [factual-lookup]
*(expects URL containing: `miso-chicken-and-rice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.743 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.705 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.694 |
| crawl4ai | miss | smittenkitchen.com/ | 0.709 | smittenkitchen.com/./recipes/ingredient/grain/?for | 0.690 | smittenkitchen.com/./recipes/ingredient/meat/chick | 0.659 |
| crawl4ai-raw | miss | smittenkitchen.com/ | 0.709 | smittenkitchen.com/./recipes/ingredient/grain/?for | 0.690 | smittenkitchen.com/./recipes/ingredient/meat/chick | 0.659 |
| scrapy+md | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.743 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.705 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.673 |
| crawlee | miss | smittenkitchen.com/./recipes/ingredient/grain/?for | 0.550 | smittenkitchen.com/ | 0.525 | smittenkitchen.com/./recipes/ingredient/meat/chick | 0.522 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | smittenkitchen.com/recipes/ingredient/grain/?forma | 0.550 | smittenkitchen.com/ | 0.525 | smittenkitchen.com/recipes/ingredient/meat/chicken | 0.522 |


**Q3: How do I make ultimate banana bread?** [factual-lookup]
*(expects URL containing: `ultimate-banana-bread`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.741 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.709 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.696 |
| crawl4ai | miss | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.667 | smittenkitchen.com/./recipes/course/muffin/?format | 0.632 | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.556 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.667 | smittenkitchen.com/./recipes/course/muffin/?format | 0.632 | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.556 |
| scrapy+md | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/? | 0.741 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.741 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.701 |
| crawlee | miss | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.492 | smittenkitchen.com/./recipes/course/muffin/?format | 0.435 | smittenkitchen.com/ | 0.424 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | smittenkitchen.com/recipes/fruit/bananas/?format=p | 0.492 | smittenkitchen.com/recipes/course/muffin/?format=p | 0.435 | smittenkitchen.com/ | 0.424 |


**Q4: What's the skillet-baked macaroni and cheese recipe?** [factual-lookup]
*(expects URL containing: `skillet-baked-macaroni-and-cheese`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2011/03/the-best-baked-spinach/ | 0.433 | smittenkitchen.com/2015/01/mushroom-marsala-pasta- | 0.426 | smittenkitchen.com/2011/03/the-best-baked-spinach/ | 0.423 |
| crawl4ai | miss | smittenkitchen.com/./recipes/course/pasta/?format= | 0.686 | smittenkitchen.com/./recipes/course/side-dish/?for | 0.667 | smittenkitchen.com/./recipes/holiday/thanksgiving/ | 0.667 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/course/pasta/?format= | 0.686 | smittenkitchen.com/./recipes/course/side-dish/?for | 0.667 | smittenkitchen.com/./recipes/holiday/thanksgiving/ | 0.667 |
| scrapy+md | #1 | smittenkitchen.com/2024/11/skillet-baked-macaroni- | 0.761 | smittenkitchen.com/2024/11/skillet-baked-macaroni- | 0.737 | smittenkitchen.com/2024/11/skillet-baked-macaroni- | 0.668 |
| crawlee | miss | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.431 | smittenkitchen.com/./recipes/course/pasta/?format= | 0.397 | smittenkitchen.com/./recipes/method/casserole/?for | 0.393 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | smittenkitchen.com/recipes/ingredient/cheese/?form | 0.431 | smittenkitchen.com/recipes/course/pasta/?format=ph | 0.397 | smittenkitchen.com/recipes/method/casserole/?forma | 0.393 |


**Q5: What vegan recipes are available on Smitten Kitchen?** [cross-page]
*(expects URL containing: `diet/vegan`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2010/03/spinach-and-chickpeas/ | 0.554 | smittenkitchen.com/2020/10/morning-glory-breakfast | 0.544 | smittenkitchen.com/2019/08/black-pepper-tofu-and-e | 0.543 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.631 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.607 | smittenkitchen.com/ | 0.576 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.628 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.607 | smittenkitchen.com/ | 0.576 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.547 | smittenkitchen.com/recipes/ | 0.539 | smittenkitchen.com/recipes/ | 0.525 |
| crawlee | #1 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.622 | smittenkitchen.com/./recipes/best-of-smitten-kitch | 0.600 | smittenkitchen.com/./recipes/diet/vegetarian/?form | 0.575 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | smittenkitchen.com/recipes/diet/vegan/?format=phot | 0.622 | smittenkitchen.com/recipes/best-of-smitten-kitchen | 0.600 | smittenkitchen.com/recipes/sweets/doughnut/?format | 0.577 |


**Q6: Show me cookie recipes** [cross-page]
*(expects URL containing: `sweets/cookie`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2019/12/unfussy-sugar-cookies/ | 0.605 | smittenkitchen.com/2007/12/peanut-butter-cookies/ | 0.554 | smittenkitchen.com/2019/12/unfussy-sugar-cookies/ | 0.551 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.612 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.571 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.562 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.612 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.571 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.562 |
| scrapy+md | miss | smittenkitchen.com/2017/10/chocolate-olive-oil-cak | 0.523 | smittenkitchen.com/2017/10/chocolate-olive-oil-cak | 0.523 | smittenkitchen.com/2017/10/chocolate-olive-oil-cak | 0.523 |
| crawlee | #1 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.622 | smittenkitchen.com/recipes/ | 0.520 | smittenkitchen.com/./recipes/sweets/cake/?format=p | 0.497 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | smittenkitchen.com/recipes/sweets/cookie/?format=p | 0.622 | smittenkitchen.com/recipes/ | 0.520 | smittenkitchen.com/recipes | 0.520 |


**Q7: How do you make pumpkin basque cheesecake?** [factual-lookup]
*(expects URL containing: `pumpkin-basque-cheesecake`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.790 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.783 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.779 |
| crawl4ai | miss | smittenkitchen.com/videos/ | 0.710 | smittenkitchen.com/./recipes/sweets/cake/?format=p | 0.710 | smittenkitchen.com/./recipes/holiday/thanksgiving/ | 0.687 |
| crawl4ai-raw | miss | smittenkitchen.com/videos/ | 0.710 | smittenkitchen.com/./recipes/sweets/cake/?format=p | 0.710 | smittenkitchen.com/./recipes/holiday/thanksgiving/ | 0.687 |
| scrapy+md | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/? | 0.402 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.402 | smittenkitchen.com/2007/07/double-chocolate-layer- | 0.398 |
| crawlee | miss | smittenkitchen.com/ | 0.648 | smittenkitchen.com/./recipes/vegetable/winter-squa | 0.501 | smittenkitchen.com/./recipes/vegetable/winter-squa | 0.463 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | smittenkitchen.com/ | 0.648 | smittenkitchen.com/recipes/sweets/cake/?format=pho | 0.412 | smittenkitchen.com/recipes/season/fall/?format=pho | 0.407 |


**Q8: What recipes are good for winter?** [cross-page]
*(expects URL containing: `season/winter`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #29 | smittenkitchen.com/2007/11/curried-lentils-and-swe | 0.537 | smittenkitchen.com/2013/01/lentil-soup-with-sausag | 0.519 | smittenkitchen.com/2013/01/lentil-soup-with-sausag | 0.514 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/season/winter/?format | 0.596 | smittenkitchen.com/recipes/ | 0.536 | smittenkitchen.com/./recipes/season/winter/?format | 0.523 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/season/winter/?format | 0.596 | smittenkitchen.com/recipes/ | 0.536 | smittenkitchen.com/./recipes/season/winter/?format | 0.521 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.542 | smittenkitchen.com/recipes/ | 0.491 | smittenkitchen.com/recipes/ | 0.488 |
| crawlee | #1 | smittenkitchen.com/./recipes/season/winter/?format | 0.593 | smittenkitchen.com/./recipes/vegetable/winter-squa | 0.555 | smittenkitchen.com/recipes/ | 0.542 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | smittenkitchen.com/recipes/season/winter/?format=p | 0.593 | smittenkitchen.com/recipes | 0.542 | smittenkitchen.com/recipes/ | 0.542 |


</details>

## stripe-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 67% (12/18) | 78% (14/18) | 78% (14/18) | 83% (15/18) | 83% (15/18) | 0.714 | 3259 | 500 |
| playwright | 39% (7/18) | 61% (11/18) | 72% (13/18) | 83% (15/18) | 83% (15/18) | 0.531 | 35610 | 500 |
| crawlee | 39% (7/18) | 61% (11/18) | 72% (13/18) | 83% (15/18) | 83% (15/18) | 0.525 | 38114 | 500 |
| colly+md | 39% (7/18) | 50% (9/18) | 72% (13/18) | 89% (16/18) | 89% (16/18) | 0.512 | 31363 | 498 |
| scrapy+md | 39% (7/18) | 61% (11/18) | 67% (12/18) | 67% (12/18) | 78% (14/18) | 0.511 | 12730 | 495 |
| crawl4ai | 28% (5/18) | 44% (8/18) | 56% (10/18) | 78% (14/18) | 78% (14/18) | 0.399 | 7501 | 493 |
| crawl4ai-raw | 28% (5/18) | 44% (8/18) | 56% (10/18) | 78% (14/18) | 78% (14/18) | 0.399 | 10271 | 491 |

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
| scrapy+md | #2 | docs.stripe.com/payments/accept-a-payment?payment- | 0.791 | docs.stripe.com/payments/payment-intents | 0.766 | docs.stripe.com/tax/custom | 0.754 |
| crawlee | #2 | docs.stripe.com/api/payment_intents/create | 0.846 | docs.stripe.com/payments/payment-intents | 0.769 | docs.stripe.com/payments/payment-intents | 0.763 |
| colly+md | #2 | docs.stripe.com/api/payment/intents/create#create/ | 0.846 | docs.stripe.com/payments/payment-intents | 0.769 | docs.stripe.com/payments/payment-intents | 0.766 |
| playwright | #1 | docs.stripe.com/payments/payment-intents | 0.769 | docs.stripe.com/payments/payment-intents | 0.763 | docs.stripe.com/payments/accept-a-payment-deferred | 0.758 |


**Q2: How do I handle webhooks from Stripe?** [api-function]
*(expects URL containing: `webhook`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/webhooks | 0.716 | docs.stripe.com/error-handling | 0.712 | docs.stripe.com/billing/taxes/collect-taxes | 0.625 |
| crawl4ai | #1 | docs.stripe.com/webhooks | 0.724 | docs.stripe.com/payments/checkout/custom-success-p | 0.705 | docs.stripe.com/get-started/use-cases/saas-subscri | 0.683 |
| crawl4ai-raw | #1 | docs.stripe.com/webhooks | 0.724 | docs.stripe.com/payments/checkout/custom-success-p | 0.705 | docs.stripe.com/get-started/use-cases/saas-subscri | 0.683 |
| scrapy+md | #1 | docs.stripe.com/webhooks?snapshot-or-thin=thin | 0.716 | docs.stripe.com/webhooks?snapshot-or-thin=thin | 0.660 | docs.stripe.com/webhooks?snapshot-or-thin=thin | 0.659 |
| crawlee | #1 | docs.stripe.com/webhooks/handling-payment-events | 0.789 | docs.stripe.com/webhooks/quickstart | 0.738 | docs.stripe.com/webhooks | 0.719 |
| colly+md | #1 | docs.stripe.com/webhooks/quickstart | 0.738 | docs.stripe.com/webhooks | 0.719 | docs.stripe.com/webhooks | 0.716 |
| playwright | #1 | docs.stripe.com/webhooks/handling-payment-events | 0.789 | docs.stripe.com/billing/subscriptions/webhooks | 0.770 | docs.stripe.com/webhooks/quickstart | 0.738 |


**Q3: How do I set up Stripe subscriptions?** [api-function]
*(expects URL containing: `subscription`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/bank-transfe | 0.731 | docs.stripe.com/billing/subscriptions/paypal | 0.727 | docs.stripe.com/billing/subscriptions/build-subscr | 0.715 |
| crawl4ai | #1 | docs.stripe.com/connect/subscriptions | 0.776 | docs.stripe.com/payments/advanced/build-subscripti | 0.740 | docs.stripe.com/billing/subscriptions/build-subscr | 0.737 |
| crawl4ai-raw | #1 | docs.stripe.com/connect/subscriptions | 0.776 | docs.stripe.com/payments/advanced/build-subscripti | 0.740 | docs.stripe.com/billing/subscriptions/build-subscr | 0.737 |
| scrapy+md | #1 | docs.stripe.com/use-stripe-apps/shopify-subscripti | 0.750 | docs.stripe.com/no-code/subscriptions | 0.727 | docs.stripe.com/use-stripe-apps/shopify-subscripti | 0.685 |
| crawlee | #1 | docs.stripe.com/connect/subscriptions | 0.786 | docs.stripe.com/no-code/subscriptions | 0.782 | docs.stripe.com/subscriptions | 0.782 |
| colly+md | #1 | docs.stripe.com/subscriptions | 0.782 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 | docs.stripe.com/billing/subscriptions/overview | 0.766 |
| playwright | #1 | docs.stripe.com/connect/subscriptions | 0.786 | docs.stripe.com/no-code/subscriptions | 0.782 | docs.stripe.com/payments/subscriptions | 0.782 |


**Q4: How do I authenticate with the Stripe API?** [api-function]
*(expects URL containing: `authentication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #9 | docs.stripe.com/keys | 0.628 | docs.stripe.com/error-handling | 0.610 | docs.stripe.com/get-started/account/set-up | 0.609 |
| crawl4ai | miss | docs.stripe.com/get-started/development-environmen | 0.695 | docs.stripe.com/samples/identity/redirect | 0.682 | docs.stripe.com/api | 0.672 |
| crawl4ai-raw | miss | docs.stripe.com/get-started/development-environmen | 0.695 | docs.stripe.com/samples/identity/redirect | 0.682 | docs.stripe.com/api | 0.672 |
| scrapy+md | #16 | docs.stripe.com/get-started/development-environmen | 0.677 | docs.stripe.com/get-started/api-request | 0.627 | docs.stripe.com/get-started/account/sso/google-wor | 0.621 |
| crawlee | #1 | docs.stripe.com/payments/3d-secure/authentication- | 0.773 | docs.stripe.com/payments/3d-secure | 0.735 | docs.stripe.com/payment-authentication/writing-que | 0.702 |
| colly+md | #2 | docs.stripe.com/payments/3d-secure | 0.735 | docs.stripe.com/payment-authentication/writing-que | 0.702 | docs.stripe.com/payments/without-card-authenticati | 0.701 |
| playwright | #2 | docs.stripe.com/payments/3d-secure | 0.735 | docs.stripe.com/payments/without-card-authenticati | 0.701 | docs.stripe.com/payments/mobile/without-card-authe | 0.701 |


**Q5: How do I handle errors in the Stripe API?** [api-function]
*(expects URL containing: `error-handling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/error-handling | 0.756 | docs.stripe.com/error-low-level | 0.722 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.696 |
| crawl4ai | miss | docs.stripe.com/api | 0.696 | docs.stripe.com/webhooks/quickstart | 0.661 | docs.stripe.com/api | 0.646 |
| crawl4ai-raw | miss | docs.stripe.com/api | 0.696 | docs.stripe.com/webhooks/quickstart | 0.661 | docs.stripe.com/api | 0.646 |
| scrapy+md | miss | docs.stripe.com/use-stripe-apps/shopify-subscripti | 0.623 | docs.stripe.com/declines/codes | 0.613 | docs.stripe.com/refunds?dashboard-or-api=dashboard | 0.585 |
| crawlee | miss | docs.stripe.com/webhooks/quickstart | 0.673 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.643 | docs.stripe.com/disputes/api | 0.634 |
| colly+md | miss | docs.stripe.com/disputes/api | 0.634 | docs.stripe.com/get-started/checklist/go-live | 0.621 | docs.stripe.com/changelog/2020-08-27/adds-error-co | 0.611 |
| playwright | miss | docs.stripe.com/webhooks/quickstart | 0.673 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.643 | docs.stripe.com/api/events | 0.602 |


**Q6: How do I process refunds with Stripe?** [api-function]
*(expects URL containing: `refund`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #32 | docs.stripe.com/billing/subscriptions/third-party- | 0.631 | docs.stripe.com/ach-deprecated | 0.621 | docs.stripe.com/account/approvals | 0.587 |
| crawl4ai | #7 | docs.stripe.com/payments/quickstart?platform=ios | 0.732 | docs.stripe.com/billing/subscriptions/third-party- | 0.712 | docs.stripe.com/connect/end-to-end-marketplace | 0.702 |
| crawl4ai-raw | #7 | docs.stripe.com/payments/quickstart?platform=ios | 0.732 | docs.stripe.com/billing/subscriptions/third-party- | 0.712 | docs.stripe.com/connect/end-to-end-marketplace | 0.702 |
| scrapy+md | #3 | docs.stripe.com/connect/charges | 0.698 | docs.stripe.com/payments/sepa-debit | 0.661 | docs.stripe.com/refunds?dashboard-or-api=api | 0.660 |
| crawlee | #1 | docs.stripe.com/api/refunds | 0.778 | docs.stripe.com/payments/quickstart?platform=ios | 0.718 | docs.stripe.com/refunds | 0.714 |
| colly+md | #1 | docs.stripe.com/refunds | 0.714 | docs.stripe.com/connect/charges | 0.698 | docs.stripe.com/connect/charges#refund-creation | 0.698 |
| playwright | #1 | docs.stripe.com/api/refunds | 0.778 | docs.stripe.com/payments/quickstart?platform=ios | 0.718 | docs.stripe.com/refunds | 0.714 |


**Q7: How do I use Stripe checkout for payments?** [js-rendered]
*(expects URL containing: `checkout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.648 | docs.stripe.com/upgrades/manage-payment-methods | 0.645 | docs.stripe.com/billing/subscriptions/build-subscr | 0.638 |
| crawl4ai | #1 | docs.stripe.com/checkout/quickstart | 0.715 | docs.stripe.com/checkout/embedded/quickstart | 0.715 | docs.stripe.com/payments/accept-a-payment?platform | 0.683 |
| crawl4ai-raw | #1 | docs.stripe.com/checkout/embedded/quickstart | 0.715 | docs.stripe.com/checkout/quickstart | 0.715 | docs.stripe.com/payments/accept-a-payment?payment- | 0.683 |
| scrapy+md | #2 | docs.stripe.com/payments | 0.665 | docs.stripe.com/payments/accept-a-payment?integrat | 0.664 | docs.stripe.com/payments/accept-a-payment?payment- | 0.664 |
| crawlee | #3 | docs.stripe.com/payments/paypay | 0.736 | docs.stripe.com/payments/online-payments | 0.731 | docs.stripe.com/checkout/quickstart | 0.716 |
| colly+md | #5 | docs.stripe.com/payments/paypay | 0.736 | docs.stripe.com/payments/online-payments#compare-f | 0.731 | docs.stripe.com/payments/online-payments | 0.731 |
| playwright | #2 | docs.stripe.com/payments/online-payments | 0.731 | docs.stripe.com/checkout/embedded/quickstart | 0.716 | docs.stripe.com/checkout/quickstart | 0.716 |


**Q8: How do I test Stripe payments in development?** [code-example]
*(expects URL containing: `testing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/automated-testing | 0.680 | docs.stripe.com/billing/testing | 0.663 | docs.stripe.com/billing/testing | 0.658 |
| crawl4ai | #7 | docs.stripe.com/get-started/test-developer-integra | 0.732 | docs.stripe.com/tax/custom | 0.705 | docs.stripe.com/payments/link/instant-bank-payment | 0.700 |
| crawl4ai-raw | #7 | docs.stripe.com/get-started/test-developer-integra | 0.732 | docs.stripe.com/tax/custom | 0.705 | docs.stripe.com/payments/link/instant-bank-payment | 0.700 |
| scrapy+md | #4 | docs.stripe.com/terminal/features/apps-on-devices/ | 0.719 | docs.stripe.com/terminal/features/apps-on-devices/ | 0.719 | docs.stripe.com/get-started/test-developer-integra | 0.712 |
| crawlee | #4 | docs.stripe.com/get-started/test-developer-integra | 0.712 | docs.stripe.com/get-started/development-environmen | 0.707 | docs.stripe.com/payments/link/instant-bank-payment | 0.688 |
| colly+md | #5 | docs.stripe.com/get-started/test-developer-integra | 0.712 | docs.stripe.com/get-started/development-environmen | 0.707 | docs.stripe.com/payments/link/instant-bank-payment | 0.688 |
| playwright | #4 | docs.stripe.com/get-started/test-developer-integra | 0.712 | docs.stripe.com/get-started/development-environmen | 0.707 | docs.stripe.com/payments/link/instant-bank-payment | 0.688 |


**Q9: What are Stripe Connect and platform payments?** [conceptual]
*(expects URL containing: `connect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #29 | docs.stripe.com/ach-deprecated | 0.654 | docs.stripe.com/get-started/account/orgs/setup | 0.646 | docs.stripe.com/capital/overview | 0.636 |
| crawl4ai | #1 | docs.stripe.com/connect | 0.771 | docs.stripe.com/payments/klarna | 0.753 | docs.stripe.com/llms.txt | 0.714 |
| crawl4ai-raw | #1 | docs.stripe.com/connect | 0.771 | docs.stripe.com/payments/klarna | 0.753 | docs.stripe.com/llms.txt | 0.714 |
| scrapy+md | #2 | docs.stripe.com/llms.txt | 0.714 | docs.stripe.com/connect/how-connect-works | 0.690 | docs.stripe.com/llms.txt | 0.686 |
| crawlee | #1 | docs.stripe.com/connect | 0.772 | docs.stripe.com/connect | 0.759 | docs.stripe.com/connect/build-full-embedded-integr | 0.756 |
| colly+md | #1 | docs.stripe.com/connect | 0.772 | docs.stripe.com/connect | 0.759 | docs.stripe.com/terminal | 0.708 |
| playwright | #1 | docs.stripe.com/connect | 0.772 | docs.stripe.com/connect | 0.759 | docs.stripe.com/connect/build-full-embedded-integr | 0.756 |


**Q10: How do I set up usage-based billing with Stripe?** [js-rendered]
*(expects URL containing: `usage-based`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.768 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.765 | docs.stripe.com/subscriptions/pricing-models/usage | 0.761 |
| crawl4ai | #6 | docs.stripe.com/billing | 0.720 | docs.stripe.com/billing/subscriptions/billing-cycl | 0.679 | docs.stripe.com/llms.txt | 0.671 |
| crawl4ai-raw | #6 | docs.stripe.com/billing | 0.720 | docs.stripe.com/billing/subscriptions/billing-cycl | 0.679 | docs.stripe.com/llms.txt | 0.671 |
| scrapy+md | #1 | docs.stripe.com/billing/subscriptions/usage-based | 0.662 | docs.stripe.com/llms.txt | 0.638 | docs.stripe.com/get-started/development-environmen | 0.602 |
| crawlee | #6 | docs.stripe.com/billing | 0.752 | docs.stripe.com/llms.txt | 0.671 | docs.stripe.com/tax/set-up | 0.671 |
| colly+md | #6 | docs.stripe.com/billing | 0.753 | docs.stripe.com/tax/set-up | 0.671 | docs.stripe.com/get-started/account/set-up#public- | 0.664 |
| playwright | #6 | docs.stripe.com/billing | 0.753 | docs.stripe.com/llms.txt | 0.671 | docs.stripe.com/tax/set-up | 0.671 |


**Q11: How do I manage Stripe API keys?** [api-function]
*(expects URL containing: `keys`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/keys | 0.774 | docs.stripe.com/keys-best-practices | 0.736 | docs.stripe.com/keys | 0.721 |
| crawl4ai | #4 | docs.stripe.com/samples/identity/redirect | 0.779 | docs.stripe.com/connect/saas/quickstart | 0.753 | docs.stripe.com/connect/marketplace/quickstart | 0.752 |
| crawl4ai-raw | #4 | docs.stripe.com/samples/identity/redirect | 0.779 | docs.stripe.com/connect/saas/quickstart | 0.753 | docs.stripe.com/connect/marketplace/quickstart | 0.752 |
| scrapy+md | #1 | docs.stripe.com/stripe-cli/keys | 0.682 | docs.stripe.com/payments/checkout/build-subscripti | 0.677 | docs.stripe.com/billing/subscriptions/build-subscr | 0.677 |
| crawlee | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/connect/saas/quickstart | 0.752 | docs.stripe.com/connect/marketplace/quickstart | 0.752 |
| colly+md | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/keys | 0.724 | docs.stripe.com/keys-best-practices | 0.682 |
| playwright | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/samples/identity/redirect | 0.779 | docs.stripe.com/connect/marketplace/quickstart | 0.752 |


**Q12: How do I handle Stripe rate limits?** [api-function]
*(expects URL containing: `rate-limits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/rate-limits | 0.720 | docs.stripe.com/rate-limits | 0.720 | docs.stripe.com/rate-limits | 0.705 |
| crawl4ai | miss | docs.stripe.com/testing | 0.670 | docs.stripe.com/payments/payment-method-rules | 0.603 | docs.stripe.com/tax/custom | 0.575 |
| crawl4ai-raw | miss | docs.stripe.com/testing | 0.670 | docs.stripe.com/payments/payment-method-rules | 0.603 | docs.stripe.com/tax/custom | 0.575 |
| scrapy+md | miss | docs.stripe.com/get-started/account/sso/scim | 0.655 | docs.stripe.com/search | 0.605 | docs.stripe.com/declines/codes | 0.576 |
| crawlee | miss | docs.stripe.com/testing | 0.674 | docs.stripe.com/tax/tax-rates | 0.625 | docs.stripe.com/money-management | 0.608 |
| colly+md | miss | docs.stripe.com/testing#cards | 0.674 | docs.stripe.com/testing | 0.674 | docs.stripe.com/tax/tax-rates | 0.624 |
| playwright | miss | docs.stripe.com/testing | 0.674 | docs.stripe.com/tax/tax-rates | 0.625 | docs.stripe.com/money-management | 0.608 |


**Q13: How do I use metadata with Stripe objects?** [api-function]
*(expects URL containing: `metadata`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/metadata/use-cases | 0.789 | docs.stripe.com/metadata/use-cases | 0.778 | docs.stripe.com/metadata | 0.768 |
| crawl4ai | miss | docs.stripe.com/api | 0.735 | docs.stripe.com/payments/payment-intents | 0.733 | docs.stripe.com/api | 0.717 |
| crawl4ai-raw | miss | docs.stripe.com/api | 0.735 | docs.stripe.com/payments/payment-intents | 0.733 | docs.stripe.com/api | 0.717 |
| scrapy+md | miss | docs.stripe.com/payments/payment-intents | 0.734 | docs.stripe.com/use-stripe-apps/shopify-subscripti | 0.720 | docs.stripe.com/api/errors/handling | 0.702 |
| crawlee | #3 | docs.stripe.com/payments/payment-intents | 0.741 | docs.stripe.com/stripe-data | 0.667 | docs.stripe.com/industry-metadata | 0.635 |
| colly+md | #7 | docs.stripe.com/payments/payment-intents | 0.734 | docs.stripe.com/api/idempotent/requests | 0.708 | docs.stripe.com/payments/checkout-sessions | 0.704 |
| playwright | miss | docs.stripe.com/payments/payment-intents | 0.741 | docs.stripe.com/api | 0.720 | docs.stripe.com/api | 0.702 |


**Q14: How do I set up Apple Pay with Stripe?** [js-rendered]
*(expects URL containing: `apple-pay`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/apple-pay | 0.747 | docs.stripe.com/apple-pay | 0.727 | docs.stripe.com/apple-pay | 0.696 |
| crawl4ai | #1 | docs.stripe.com/apple-pay | 0.754 | docs.stripe.com/apple-pay | 0.747 | docs.stripe.com/payments/quickstart?platform=ios | 0.725 |
| crawl4ai-raw | #1 | docs.stripe.com/apple-pay | 0.754 | docs.stripe.com/apple-pay | 0.747 | docs.stripe.com/payments/quickstart?platform=ios | 0.725 |
| scrapy+md | #1 | docs.stripe.com/apple-pay?platform=ios | 0.743 | docs.stripe.com/apple-pay/cartes-bancaires | 0.708 | docs.stripe.com/apple-pay?platform=ios | 0.696 |
| crawlee | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.743 | docs.stripe.com/apple-pay/cartes-bancaires | 0.728 |
| colly+md | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.743 | docs.stripe.com/apple-pay | 0.696 |
| playwright | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.743 | docs.stripe.com/payments/quickstart?platform=ios | 0.703 |


**Q15: How do I issue cards with Stripe Issuing?** [api-function]
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.709 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.662 | docs.stripe.com/issuing/integration-guides/fleet | 0.662 |
| crawl4ai | #2 | docs.stripe.com/llms.txt | 0.804 | docs.stripe.com/issuing/direct | 0.764 | docs.stripe.com/issuing | 0.750 |
| crawl4ai-raw | #2 | docs.stripe.com/llms.txt | 0.804 | docs.stripe.com/issuing/direct | 0.764 | docs.stripe.com/issuing | 0.750 |
| scrapy+md | #20 | docs.stripe.com/llms.txt | 0.731 | docs.stripe.com/js/elements_object/express_checkou | 0.698 | docs.stripe.com/js/element/other_element?type=card | 0.698 |
| crawlee | #2 | docs.stripe.com/llms.txt | 0.804 | docs.stripe.com/issuing/direct | 0.756 | docs.stripe.com/issuing | 0.752 |
| colly+md | #1 | docs.stripe.com/issuing | 0.752 | docs.stripe.com/issuing | 0.750 | docs.stripe.com/issuing/direct | 0.745 |
| playwright | #2 | docs.stripe.com/llms.txt | 0.804 | docs.stripe.com/issuing/direct | 0.756 | docs.stripe.com/issuing | 0.752 |


**Q16: How do I recover failed subscription payments?** [js-rendered]
*(expects URL containing: `revenue-recovery`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/revenue-recovery | 0.621 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.585 |
| crawl4ai | #3 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.594 |
| crawl4ai-raw | #3 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.594 |
| scrapy+md | #1 | docs.stripe.com/billing/revenue-recovery/customer- | 0.584 | docs.stripe.com/billing/revenue-recovery/recovery- | 0.582 | docs.stripe.com/billing/revenue-recovery/recovery- | 0.573 |
| crawlee | #4 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/india-recurring-payments | 0.660 | docs.stripe.com/india-recurring-payments | 0.628 |
| colly+md | #5 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/no-code/get-started#sell-online | 0.704 | docs.stripe.com/no-code/get-started#in-person | 0.704 |
| playwright | #3 | docs.stripe.com/no-code/get-started | 0.704 | docs.stripe.com/billing/collection-method | 0.605 | docs.stripe.com/billing/revenue-recovery/customer- | 0.584 |


**Q17: How does Stripe handle tax calculation for billing?** [js-rendered]
*(expects URL containing: `billing/taxes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.stripe.com/saas | 0.724 | docs.stripe.com/products-prices/how-products-and-p | 0.722 | docs.stripe.com/billing/taxes/migration | 0.716 |
| crawl4ai | #9 | docs.stripe.com/tax | 0.806 | docs.stripe.com/payments/advanced/tax | 0.751 | docs.stripe.com/tax/tax-rates | 0.742 |
| crawl4ai-raw | #9 | docs.stripe.com/tax | 0.806 | docs.stripe.com/payments/advanced/tax | 0.751 | docs.stripe.com/tax/tax-rates | 0.743 |
| scrapy+md | miss | docs.stripe.com/tax/checkout/elements | 0.703 | docs.stripe.com/llms.txt | 0.687 | docs.stripe.com/tax/custom | 0.683 |
| crawlee | miss | docs.stripe.com/tax | 0.820 | docs.stripe.com/tax/set-up | 0.744 | docs.stripe.com/tax/set-up | 0.735 |
| colly+md | #5 | docs.stripe.com/tax | 0.820 | docs.stripe.com/tax/set-up | 0.744 | docs.stripe.com/tax/set-up | 0.735 |
| playwright | #5 | docs.stripe.com/tax | 0.820 | docs.stripe.com/tax/set-up | 0.744 | docs.stripe.com/tax/set-up | 0.735 |


**Q18: How do I migrate data to Stripe?** [conceptual]
*(expects URL containing: `data-migrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.stripe.com/billing/taxes/migration | 0.728 | docs.stripe.com/billing/taxes/migration | 0.712 | docs.stripe.com/get-started/data-migrations/pan-ex | 0.711 |
| crawl4ai | #5 | docs.stripe.com/stripe-data/import-external-data | 0.724 | docs.stripe.com/billing/taxes/migration | 0.714 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.708 |
| crawl4ai-raw | #5 | docs.stripe.com/stripe-data/import-external-data | 0.724 | docs.stripe.com/billing/taxes/migration | 0.714 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.708 |
| scrapy+md | #1 | docs.stripe.com/get-started/data-migrations/paymen | 0.631 | docs.stripe.com/get-started/data-migrations/paymen | 0.608 | docs.stripe.com/sdks/stripejs-versioning | 0.605 |
| crawlee | #8 | docs.stripe.com/payments/ach-direct-debit/migratin | 0.766 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/payments/checkout/migration | 0.735 |
| colly+md | #9 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/payments/checkout/migration | 0.735 |
| playwright | #9 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/payments/checkout/migration | 0.735 |


</details>

## Methodology

- **Queries:** 104 across 11 sites, categorized by type (api-function, code-example, conceptual, structured-data, factual-lookup, cross-page, navigation, js-rendered)
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

