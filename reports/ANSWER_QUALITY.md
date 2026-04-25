# End-to-End RAG Answer Quality
<!-- style: v2, 2026-04-24 -->

All crawlers produce similar LLM answer quality (3.88-4.33 out of 5). colly+md leads slightly at 4.33; markcrawl ranks 5th at 3.97 — a 8.5% gap from the best. The gaps are small but consistent.

Each tool's crawled content is chunked, embedded, retrieved (top-10),
and sent to `gpt-4o-mini` to generate an answer. Answers are scored by
`gpt-4o-mini` on correctness, relevance, completeness, and usefulness (1-5 each).

**Scoring scale:** 1 = wrong/irrelevant, 2 = partially relevant, 3 = acceptable, 4 = good, 5 = excellent/complete. Scores are averaged across all queries per tool. An overall score above 4.0 indicates consistently good answers.

## Summary (104 queries across 11 sites)

| Tool | Correctness | Relevance | Completeness | Usefulness | **Overall** | Avg tokens/query |
|---|---|---|---|---|---|---|
| colly+md | 4.50 | 4.45 | 4.06 | 4.32 | **4.33 ±0.28** | 1,766 |
| crawlee | 4.50 | 4.27 | 3.95 | 4.25 | **4.24 ±0.25** | 1,396 |
| crawl4ai-raw | 4.43 | 4.26 | 3.88 | 4.17 | **4.19 ±0.24** | 1,336 |
| crawl4ai | 4.44 | 4.21 | 3.82 | 4.17 | **4.16 ±0.24** | 1,325 |
| markcrawl | 4.33 | 3.98 | 3.62 | 3.94 | **3.97 ±0.26** | 1,828 |
| scrapy+md | 4.24 | 3.93 | 3.52 | 3.89 | **3.90 ±0.30** | 1,752 |
| playwright | 4.25 | 3.91 | 3.52 | 3.85 | **3.88 ±0.26** | 1,670 |

> **Column definitions:** All scores are 1-5 averages across queries, judged by `gpt-4o-mini`. **Correctness** = factual accuracy. **Relevance** = answers the question asked. **Completeness** = covers all aspects. **Usefulness** = practical value to the user. **Overall** = mean of the four dimensions (± 95% confidence interval). **Avg tokens/query** = estimated input tokens per query (chunk words x 1.33). Gaps within the ± range are not statistically significant.

## What this means in practice

The quality gap between the best (colly+md, 4.33) and worst (playwright, 3.88) crawler is 0.45 points on a 5-point scale -- 10.4% relative. This gap is real but small.

For most use cases, your choice of crawler will not noticeably affect the quality of LLM-generated answers. All tools produce answers that score above 4.0 ("good") on average, meaning users get helpful, accurate responses regardless of which crawler feeds the pipeline.

**Executive takeaway:** Switching crawlers purely to improve answer quality is unlikely to justify the migration effort. The cost and speed differences between tools are far more impactful on your bottom line -- see [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar-level analysis.

## huggingface-transformers

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 4.12 | 3.88 | 3.12 | 3.75 | 3.72 ±1.01 |
| crawl4ai-raw | 4.12 | 3.88 | 3.12 | 3.75 | 3.72 ±1.01 |
| markcrawl | 3.25 | 2.38 | 1.62 | 2.38 | 2.41 ±0.73 |
| playwright | 3.12 | 2.38 | 1.62 | 2.25 | 2.34 ±0.54 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for huggingface-transformers</summary>

**Q1: How do I use the Pipeline class for inference in Transformers?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the Pipeline class for inference in Transformers, you can follow these steps:  1. Import the ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the Pipeline class for inference in Transformers, you can follow these steps:  1. Import the ... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do I train a model with the Hugging Face Trainer?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How do I generate text with a large language model?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| playwright | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: What are the design principles behind the Transformers library?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | The design principles behind the Transformers library are:  1. Fast and easy to use: Every model is ... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | The design principles behind the Transformers library are:  1. Fast and easy to use: Every model is ... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: What models are supported in the Transformers library?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The Transformers library supports a variety of models including those for text generation, image-to-... |
| crawl4ai | 4 | 5 | 3 | 4 | 4.0 | The Transformers library supports state-of-the-art machine learning models in text, computer vision,... |
| crawl4ai-raw | 4 | 5 | 3 | 4 | 4.0 | The Transformers library supports state-of-the-art machine learning models in text, computer vision,... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: What is the Pipeline API reference in Transformers?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The Pipeline API reference in Transformers provides a complete list of available tasks that can be p... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The Pipeline API reference in Transformers provides a complete list of available tasks that can be p... |
| playwright | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: What does the Trainer class support for distributed training?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The Trainer class supports distributed training by working with PEFT adapters out of the box. For Ze... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The Trainer class supports distributed training out of the box, including features for ZeRO-3 and FS... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: What is the Hugging Face Transformers library?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| playwright | 4 | 5 | 4 | 4 | 4.2 | The Hugging Face Transformers library is a collection of state-of-the-art AI models for PyTorch, des... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## ikea

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| markcrawl | 5.00 | 5.00 | 4.88 | 5.00 | 4.97 ±0.06 |
| crawl4ai-raw | 4.38 | 4.75 | 4.50 | 4.38 | 4.50 ±0.59 |
| crawlee | 4.25 | 4.12 | 4.00 | 4.12 | 4.12 ±0.86 |
| playwright | 4.25 | 4.00 | 3.62 | 3.88 | 3.94 ±0.80 |
| crawl4ai | 4.38 | 3.88 | 3.25 | 3.88 | 3.84 ±0.84 |
| scrapy+md | 3.38 | 2.88 | 2.50 | 2.75 | 2.88 ±0.59 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for ikea</summary>

**Q1: How much does the MALM bed frame cost at IKEA?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The MALM bed frame costs $249.00.... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The MALM bed frame costs $399.00 at IKEA.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The MALM bed frame costs $399.00 at IKEA.... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The MALM bed frame costs $249.00.... |
| playwright | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What's the price of the SLATTUM upholstered bed frame?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The price of the SLATTUM upholstered bed frame is $149.00.... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The price of the SLATTUM upholstered bed frame is $149.00.... |
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |

**Q3: Tell me about the HEMNES 8-drawer dresser**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The HEMNES 8-drawer dresser is available in black-brown, measures 63x37 3/4 inches, and is priced at... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The HEMNES 8-drawer dresser is available in a white stain finish, measuring 63x37 3/4 inches, and is... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The HEMNES 8-drawer dresser is available in black-brown and white stain colors, measuring 63x37 3/4 ... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: What's the price of the RAST 3-drawer dresser?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The price of the RAST 3-drawer dresser is $59.99.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The price of the RAST 3-drawer dresser is $59.99.... |
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |

**Q5: What bed frames does IKEA sell?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including platform beds, storage beds, daybeds, loft beds, bunk b... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including twin beds, double beds, upholstered beds, daybeds, beds... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including twin beds, double beds, upholstered beds, daybeds, beds... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including platform beds, storage beds, daybeds, loft beds, bunk b... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including platform beds, storage beds, daybeds, loft beds, bunk b... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q6: Show me IKEA's sofa and armchair selection**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of sofas and armchairs, including sofas, loveseats, modular sofas, sectionals,... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of sofas and armchairs, including:  - Sofas & sectionals - Sleeper sofas & sof... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can view IKEA's sofa and armchair selection by visiting the [Sofas & armchairs](https://www.ikea... |
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | IKEA offers a variety of sofas and armchairs, including:  - Sofas & sectionals - Sleeper sofas & sof... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | IKEA offers a variety of sofas and armchairs, including:  - Sofas & sectionals - Sleeper sofas & sof... |
| scrapy+md | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |

**Q7: What dressers and storage drawers does IKEA offer?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of dressers and storage drawers, including:  - Dressers & chests of drawers - ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of dressers and storage drawers, including:  - Dressers & chests of drawers - ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of dressers and storage drawers, including the GULLABERG series, which feature... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of dressers and storage drawers, including the GULLABERG series, which feature... |
| markcrawl | 5 | 5 | 4 | 5 | 4.8 | IKEA offers a variety of dressers and storage drawers, including dressers & chests of drawers, night... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | IKEA offers the following dressers and storage drawers:  1. **STORKLINTA 3-drawer dresser** - gray/g... |

**Q8: How much is the STOREMOLLA 8-drawer dresser at IKEA?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The STOREMOLLA 8-drawer dresser is priced at $599.99.... |
| crawl4ai-raw | 1 | 5 | 5 | 2 | 3.2 | The STOREMOLLA 8-drawer dresser is priced at $599.99.... |
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |

</details>

## kubernetes-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| scrapy+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawlee | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| markcrawl | 5.00 | 5.00 | 4.88 | 5.00 | 4.97 ±0.06 |
| colly+md | 5.00 | 5.00 | 4.88 | 5.00 | 4.97 ±0.06 |
| crawl4ai-raw | 5.00 | 5.00 | 4.88 | 4.88 | 4.94 ±0.12 |
| playwright | 5.00 | 5.00 | 4.88 | 4.88 | 4.94 ±0.12 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for kubernetes-docs</summary>

**Q1: What is a Kubernetes pod and what does it represent?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Pod is a group of one or more application containers that share storage, an IP address,... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Pod is the smallest deployable unit of computing that you can create and manage in Kube... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do Kubernetes Deployments manage replicas and rollouts?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by creating and updating instances of applicatio... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by using a higher-level API object that updates ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by using a higher-level API object that updates ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by using a declarative approach to define the de... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by using a declarative approach to define the de... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by using a declarative approach to define the de... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by providing declarative updates for Pods and Re... |

**Q3: What is a Kubernetes Service and how does it expose pods?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that defines a logical set of Pods and a policy for accessing... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes a network application running on a set of Pods, ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes a network application running on a set of Pods, ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that defines a logical set of Pods and a policy for accessing... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes a network application running on a set of Pods, ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes a network application running as one or more Pod... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes a network application running on a set of Pods, ... |

**Q4: How do I use ConfigMaps to inject configuration into pods?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use ConfigMaps to inject configuration into pods, follow these steps:  1. Create a ConfigMap or u... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use ConfigMaps to inject configuration into pods, follow these steps:  1. **Create a ConfigMap**:... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use ConfigMaps to inject configuration into pods, follow these steps:  1. **Create a ConfigMap**:... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods by following these steps:  1. Create a Conf... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods by following these steps:  1. Create a Conf... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods by following these steps:  1. Create a Conf... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods by following these steps:  1. Create a Conf... |

**Q5: How do I manage Secrets in Kubernetes?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can manage Secrets in Kubernetes using the `kubectl` command-line tool to create, edit, manage, ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To manage Secrets in Kubernetes, follow these guidelines:  1. **Enable Encryption at Rest** for Secr... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can manage Secrets in Kubernetes using the `kubectl` command-line tool. This includes creating, ... |
| markcrawl | 5 | 5 | 4 | 5 | 4.8 | You can manage Secrets in Kubernetes using the `kubectl` command-line tool to create, edit, manage, ... |
| colly+md | 5 | 5 | 4 | 5 | 4.8 | You can manage Secrets in Kubernetes using the `kubectl` command-line tool. This includes creating, ... |
| crawl4ai-raw | 5 | 5 | 4 | 4 | 4.5 | You can manage Secrets in Kubernetes using the `kubectl` command-line tool to create, edit, manage, ... |
| playwright | 5 | 5 | 4 | 4 | 4.5 | You can manage Secrets in Kubernetes using the `kubectl` command-line tool. This includes creating, ... |

**Q6: What are namespaces in Kubernetes and when should I use them?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a scope for names, allowing for the isolation of groups of resource... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of API resources within a single c... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of API resources within a single c... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of API resources within a single c... |

**Q7: How does Kubernetes Ingress route external traffic?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by using rules defined on the Ingress resource. It expose... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |

**Q8: What is a StatefulSet and when do I need one?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a Kubernetes resource that represents a set of pods with consistent identities, def... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a workload API object used to manage stateful applications in Kubernetes. It runs a... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a workload API object used to manage stateful applications in Kubernetes. It runs a... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a workload API object used to manage stateful applications, running a group of Pods... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a workload API object used to manage stateful applications that require stable, uni... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a workload API object used to manage stateful applications in Kubernetes. It runs a... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a workload API object used to manage stateful applications, running a group of Pods... |

</details>

## mdn-css

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| playwright | 4.50 | 4.25 | 4.00 | 4.25 | 4.25 ±0.96 |
| crawlee | 4.50 | 4.25 | 3.88 | 4.25 | 4.22 ±0.95 |
| crawl4ai | 4.25 | 3.88 | 3.50 | 3.88 | 3.88 ±1.08 |
| crawl4ai-raw | 4.25 | 3.88 | 3.50 | 3.88 | 3.88 ±1.08 |
| markcrawl | 3.75 | 3.25 | 2.62 | 3.12 | 3.19 ±1.05 |
| scrapy+md | 3.00 | 2.00 | 1.00 | 2.00 | 2.00 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for mdn-css</summary>

**Q1: How does the CSS display property work?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| playwright | 5 | 5 | 5 | 5 | 5.0 | The CSS display property defines how an element is displayed on the web page, determining its outer ... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do I use flexbox for page layout?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How does CSS Grid layout work?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout works by allowing you to flexibly lay out a set of block or inline elements in two d... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout works by dividing a page into a two-dimensional grid system of intersecting horizont... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout works by dividing a page into a two-dimensional grid system of intersecting horizont... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout works by dividing a page into major regions or defining the relationship in terms of... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout works by dividing a page into major regions using a two-dimensional grid system defi... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: What is the CSS box model?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a concept that describes the rectangular boxes generated for elements in a docu... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a standard that represents each element on a webpage as a rectangular box, comp... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a standard that represents each element on a webpage as a rectangular box, comp... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a module that defines the `margin` and `padding` properties, along with height,... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a module that defines the `margin` and `padding` properties, along with height,... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: How does the CSS margin property work?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The CSS margin property is a shorthand for setting the margins on all four sides of an element: top,... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The CSS margin property is a shorthand for setting the margins on all four sides of an element: top,... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The CSS margin property is a shorthand that allows you to set the margin for all four sides of an el... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The CSS margin property allows you to set the space around an element. It can be specified using one... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: How does CSS specificity determine which rules win?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by evaluating the specificity of selectors. The more spec... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by calculating the weight of selectors based on the numbe... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by calculating the weight of selectors based on three cat... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by calculating the weight of CSS selectors. When multiple... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by calculating the weight of selectors based on their com... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: How does the :hover pseudo-class work in CSS?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS matches when a user designates an item with a pointing device, such... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS matches when a user designates an item with a pointing device, such... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS matches when a user designates an item with a pointing device, such... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS matches when a user designates an item with a pointing device, such... |
| markcrawl | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: How do I create CSS animations?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 5 | 5 | 4 | 5 | 4.8 | You can create CSS animations by defining a style that describes the animation and a set of keyframe... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## newegg

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 4.38 | 4.62 | 4.25 | 4.50 | 4.44 ±0.57 |
| crawl4ai-raw | 4.38 | 4.62 | 4.25 | 4.50 | 4.44 ±0.63 |
| colly+md | 3.62 | 4.00 | 2.88 | 3.12 | 3.41 ±0.82 |
| markcrawl | 3.50 | 2.75 | 2.00 | 2.50 | 2.69 ±0.34 |
| playwright | 3.38 | 2.38 | 1.62 | 2.25 | 2.41 ±0.31 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for newegg</summary>

**Q1: What graphics cards are available at Newegg?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai-raw | 4 | 5 | 4 | 5 | 4.5 | Newegg offers a wide selection of graphics cards, including high-performance models like the GeForce... |
| crawl4ai | 3 | 5 | 4 | 4 | 4.0 | Newegg offers a wide selection of graphics cards, including high-performance models like the GeForce... |
| markcrawl | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| colly+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What laptops does Newegg sell?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Newegg sells a variety of laptops from top brands including Lenovo, HP, DELL, Acer America, ASUS, MS... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Newegg sells a variety of laptops from top brands including Lenovo, HP, DELL, Acer America, ASUS, MS... |
| markcrawl | 3 | 4 | 3 | 4 | 3.5 | Newegg sells ultrabooks and tablets, including brands like Samsung, Lenovo, and Asus.... |
| colly+md | 2 | 3 | 2 | 2 | 2.2 | Newegg sells gaming laptops.... |
| playwright | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q3: How much does the AMD Ryzen 7 9800X3D CPU cost?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The AMD Ryzen 7 9800X3D CPU costs $464.00.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The AMD Ryzen 7 9800X3D CPU costs $464.00.... |
| colly+md | 4 | 5 | 4 | 4 | 4.2 | The AMD Ryzen 7 9800X3D CPU is priced at $464.00.... |
| playwright | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q4: What is the price of the Intel Core i9-14900K?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The price of the Intel Core i9-14900K is $599.00.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The price of the Intel Core i9-14900K is $599.00.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The price of the Intel Core i9-14900K is $469.00.... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: Tell me about the GIGABYTE GeForce RTX 5090 graphics card**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| markcrawl | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| colly+md | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: How much does the SAPPHIRE Radeon RX 9070 XT cost?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The SAPPHIRE Radeon RX 9070 XT costs $769.99, with options available from $749.99 to $1,154.00.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The SAPPHIRE Radeon RX 9070 XT costs $879.99.... |
| markcrawl | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| colly+md | 1 | 5 | 1 | 1 | 2.0 | The SAPPHIRE Radeon RX 9070 XT costs $3699.99.... |

**Q7: What ASUS TUF gaming laptops are available on Newegg?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 3 | 4 | 3 | 4 | 3.5 | The available ASUS TUF gaming laptops on Newegg are:  1. **ASUS TUF Gaming A16**    - Screen Size: 1... |
| crawl4ai-raw | 2 | 4 | 3 | 3 | 3.0 | The available ASUS TUF gaming laptops on Newegg are:  1. **ASUS TUF Gaming A16**    - Screen Size: 1... |
| colly+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| markcrawl | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: What electronics categories does Newegg offer?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Newegg offers electronics categories including laptops, gaming consoles, home electronics, PC compon... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Newegg offers electronics categories including laptops, gaming consoles, home electronics, PC compon... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Newegg offers electronics categories including smartphones, tablets, GPUs, desktop PCs, monitors, la... |
| playwright | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## npr-news

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 4.33 | 3.67 | 3.00 | 3.67 | 3.67 ±0.83 |
| crawl4ai-raw | 4.33 | 3.67 | 2.83 | 3.33 | 3.54 ±0.83 |
| crawlee | 4.17 | 3.33 | 2.50 | 3.33 | 3.33 ±0.65 |
| playwright | 3.83 | 3.17 | 2.67 | 3.17 | 3.21 ±0.74 |
| markcrawl | 4.00 | 3.17 | 2.50 | 3.00 | 3.17 ±0.76 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for npr-news</summary>

**Q1: What are the latest NPR politics stories?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What world news is NPR covering?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | NPR is covering compelling and consequential stories from around the globe, including international ... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | NPR is covering compelling and consequential stories from around the globe, including international ... |
| markcrawl | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |

**Q3: Where can I find NPR business coverage?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can find NPR business coverage at the [NPR Business section](https://www.npr.org/sections/busine... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can find NPR business coverage at the [NPR Business section](https://www.npr.org/sections/busine... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can find NPR business coverage at the [Business section](https://www.npr.org/sections/business/)... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can find NPR business coverage at the [NPR Business section](https://www.npr.org/sections/busine... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q4: What health stories is NPR reporting on?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | NPR is reporting on health stories related to emerging microbial threats, including discussions with... |
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q5: What science news does NPR have?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| markcrawl | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |

**Q6: What are the main news headlines from NPR?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |

</details>

## postgres-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| scrapy+md | 3.75 | 3.12 | 2.38 | 3.12 | 3.09 ±1.00 |
| crawl4ai | 3.75 | 3.12 | 2.25 | 3.12 | 3.06 ±1.02 |
| crawlee | 3.62 | 3.12 | 2.25 | 3.00 | 3.00 ±0.97 |
| crawl4ai-raw | 3.62 | 3.00 | 2.12 | 3.00 | 2.94 ±0.93 |
| colly+md | 3.38 | 2.75 | 1.75 | 2.62 | 2.62 ±0.82 |
| playwright | 3.25 | 2.62 | 1.75 | 2.38 | 2.50 ±0.72 |
| markcrawl | 3.00 | 2.00 | 1.00 | 2.00 | 2.00 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for postgres-docs</summary>

**Q1: What data types does PostgreSQL support?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports a rich set of native data types, including:  - Primitives: Integer, Numeric, Str... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports a rich set of native data types, including:  - Primitives: Integer, Numeric, Str... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports a variety of data types, including:  - **Primitives**: Integer, Numeric, String,... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports a variety of data types, including:  - **Primitives**: Integer, Numeric, String,... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports a variety of data types, including:  - **Primitives**: Integer, Numeric, String,... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | PostgreSQL supports the following date and time types:  1. timestamp [ (p) ] [ without time zone ] 2... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What is the SQL syntax for queries in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How do indexes work in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Indexes in PostgreSQL are used to enhance database performance by providing a mapping from data key ... |
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | Indexes in PostgreSQL enhance database performance by allowing the database server to find and retri... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | Indexes in PostgreSQL enhance database performance by allowing the database server to find and retri... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | Indexes in PostgreSQL enhance database performance by allowing the server to find and retrieve speci... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: How does MVCC concurrency control work in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | MVCC (Multiversion Concurrency Control) in PostgreSQL prevents phantom reads by restricting what is ... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: How do transactions work in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: How do I set up logical replication in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: What built-in functions and operators are available in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | PostgreSQL provides a large number of functions and operators for its built-in data types. Users can... |
| crawlee | 4 | 5 | 4 | 4 | 4.2 | PostgreSQL provides a large number of functions and operators for the built-in data types, although ... |
| colly+md | 4 | 5 | 3 | 4 | 4.0 | PostgreSQL provides a large number of functions and operators for the built-in data types, although ... |
| crawl4ai-raw | 4 | 4 | 3 | 4 | 3.8 | PostgreSQL provides a large number of functions and operators for its built-in data types. Users can... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: How do I use full text search in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## react-dev

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| markcrawl | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawlee | 5.00 | 5.00 | 4.94 | 5.00 | 4.98 ±0.03 |
| playwright | 5.00 | 5.00 | 4.94 | 5.00 | 4.98 ±0.03 |
| scrapy+md | 4.88 | 4.81 | 4.69 | 4.81 | 4.80 ±0.37 |
| colly+md | 4.88 | 4.81 | 4.69 | 4.81 | 4.80 ±0.37 |
| crawl4ai | 4.69 | 4.62 | 4.31 | 4.56 | 4.55 ±0.50 |
| crawl4ai-raw | 4.69 | 4.62 | 4.31 | 4.56 | 4.55 ±0.50 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for react-dev</summary>

**Q1: How do I manage state in a React component?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To manage state in a React component, you can use the following principles:  1. **Component Ownershi... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can manage state in a React component by using the `useState` Hook. This Hook allows you to decl... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In a React component, you manage state by using the `useState` hook. This allows you to create state... |
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
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |

**Q4: What is JSX and how does React use it?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows you to write HTML-like markup inside a JavaScri... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows you to write HTML-like markup inside a JavaScri... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within a J... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |

**Q5: How do I render lists and use keys in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript’s `map()` method to transform an array of data into... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript’s `map()` method to transform an array of data into... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use the `map()` function to transform an array of data into an arr... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use the `map()` function to transform an array of data into an arr... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use the `map()` function to transform an array of data into an arr... |
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
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can pass props between React components by having a parent component provide information to its ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You pass props between React components by allowing a parent component to provide information to its... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You pass props between React components by giving them as attributes to the child components in the ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You pass props between React components by giving them as attributes in the JSX of the parent compon... |
| crawl4ai | 5 | 5 | 4 | 5 | 4.8 | React components use _props_ to communicate with each other. A parent component can pass information... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | React components use _props_ to communicate with each other. A parent component can pass information... |
| colly+md | 5 | 5 | 4 | 5 | 4.8 | React components use *props* to communicate with each other. A parent component can pass information... |

**Q8: How do I conditionally render content in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
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
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you call it at the top level of your component, passing in a... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow this syntax:  ```javascript const cachedFn = ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow this pattern:  1. Import `useCallback` from R... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you call it at the top level of your component to cache a fu... |

**Q12: How do I use the useReducer hook in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. Import the `useReducer` hook from Rea... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |

**Q13: How do I handle events like clicks in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Declare an event handler ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can handle events like clicks in React by declaring event handler functions inside your componen... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can handle events like clicks in React by declaring event handler functions inside your componen... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Declare an event handler ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Define an event handler f... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Declare an event handler ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to follow these steps:  1. Define an event handler f... |

**Q14: What is the Suspense component in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows developers to declaratively specify the loading state for par... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to declaratively specify a loading state for a part of th... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to declaratively specify a loading state for a part of th... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to declaratively specify the loading state for a part of ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to declaratively specify the loading state for a part of ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to declaratively specify the loading state for a part of ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows developers to declaratively specify the loading state for par... |

**Q15: How do I add interactivity to React components?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can add interactivity to React components by using state to manage data that changes over time a... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can add interactivity to React components by using event handlers in your JSX. These handlers ar... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can add interactivity to React components by using state to manage data that changes over time a... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | To add interactivity to React components, you can use state, which allows components to update in re... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | You can add interactivity to React components by using state, which allows components to update thei... |
| crawl4ai | 4 | 5 | 3 | 4 | 4.0 | You can add interactivity to React components by passing new data in response to user interactions, ... |
| crawl4ai-raw | 4 | 5 | 3 | 4 | 4.0 | You can add interactivity to React components by passing them new data in response to user interacti... |

**Q16: How do I install and set up a new React project?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, you can follow these steps:  1. **Set up a modular JavaSc... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, follow these steps:  1. **Install React and ReactDOM**:  ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, you can follow these steps:  1. **Create a React App**: U... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | To install and set up a new React project, you can follow these steps:  1. **Install React and React... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## rust-book

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| markcrawl | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| colly+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| scrapy+md | 4.88 | 5.00 | 4.88 | 4.88 | 4.91 ±0.18 |
| crawl4ai | 4.75 | 4.75 | 4.62 | 4.62 | 4.69 ±0.61 |
| crawl4ai-raw | 4.75 | 4.62 | 4.50 | 4.62 | 4.62 ±0.73 |
| crawlee | 4.75 | 4.62 | 4.50 | 4.62 | 4.62 ±0.73 |
| playwright | 4.75 | 4.62 | 4.38 | 4.62 | 4.59 ±0.73 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for rust-book</summary>

**Q1: What is ownership in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. It ensures that e... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. It ensures that e... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do references and borrowing work in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In Rust, references and borrowing allow you to access data without taking ownership. When you create... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to refer to a value without taking ownership of it. When you create a ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to refer to a value without taking ownership of it. When you create a ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to use a value without transferring ownership, which is known as borro... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to use a value without transferring ownership, which is known as borro... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to use a value without transferring ownership. This is known as borrow... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to use a value without transferring ownership, which is known as borro... |

**Q3: How do I define structs in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To define structs in Rust, you use the `struct` keyword followed by the name of the struct and its f... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you enter the keyword `struct` followed by the name of the struct. Insid... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you enter the keyword `struct` followed by the name of the struct. Insid... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the `struct` keyword followed by the name of the struct. Inside ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the keyword `struct` followed by the name of the struct. Inside ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the keyword `struct` followed by the name of the struct. Inside ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the keyword `struct` followed by the name of the struct. Inside ... |

**Q4: How do enums work in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust are a way to define a type that can be one of a set of possible values, known as varia... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type by enumerating its possible variants. They are used to repr... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type by enumerating its possible variants. They are used to expr... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust provide a way to define a type that can be one of a set of predefined variants. Each v... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type that can be one of a set of enumerated values. They are use... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type that can be one of a set of predefined values, known as var... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type that can be one of a set of enumerated values. They are use... |

**Q5: How do I use generics in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use generics in Rust, you can define generic types, functions, and traits.   1. **Generic Functio... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You use generics in Rust by creating definitions for items like function signatures or structs that ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You use generics in Rust by creating definitions for items like function signatures or structs that ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use generics in Rust, you define a type parameter in angle brackets (`<>`) after the name of a ty... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In Rust, you can use generics by defining functions, structs, or traits with abstract type parameter... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: What are traits in Rust and how do I define them?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Traits in Rust describe an abstract interface that types can implement. They consist of associated i... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | In Rust, a trait defines the functionality that a particular type has and can share with other types... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | In Rust, a trait defines the functionality that a particular type has and can share with other types... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Traits in Rust describe an abstract interface that types can implement, consisting of associated ite... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Traits in Rust describe an abstract interface that types can implement. A trait consists of associat... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Traits in Rust describe an abstract interface that types can implement, consisting of associated ite... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Traits in Rust describe an abstract interface that types can implement. A trait consists of associat... |

**Q7: How do closures work in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can be saved in variables or passed as arguments to ot... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can be saved in variables or passed as arguments to ot... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can be saved in variables or passed as arguments to ot... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can capture values from their surrounding scope. They ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can be saved in variables or passed as arguments to ot... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can be saved in variables or passed as arguments to ot... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can be saved in variables or passed as arguments to ot... |

**Q8: How do I handle errors with Result in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In Rust, you handle errors with the `Result` type by checking its variants: `Ok` for success and `Er... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In Rust, you handle errors with the `Result` type, which represents either a success (`Ok`) or a fai... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In Rust, you handle errors with the `Result` type, which represents either a success (`Ok`) or a fai... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | In Rust, you handle errors with the `Result` type, which represents either a success (`Ok`) or a fai... |
| scrapy+md | 4 | 5 | 4 | 4 | 4.2 | To handle errors with `Result` in Rust, you can use the `expect` method. This method allows you to s... |
| crawl4ai | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## smittenkitchen

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawlee | 3.88 | 3.25 | 2.62 | 3.25 | 3.25 ±1.03 |
| markcrawl | 3.75 | 3.12 | 2.62 | 3.12 | 3.16 ±1.06 |
| playwright | 3.75 | 3.12 | 2.50 | 3.12 | 3.12 ±1.08 |
| crawl4ai | 3.50 | 2.75 | 2.00 | 2.75 | 2.75 ±0.96 |
| crawl4ai-raw | 3.50 | 2.75 | 2.00 | 2.75 | 2.75 ±0.96 |
| scrapy+md | 3.38 | 2.50 | 1.50 | 2.50 | 2.47 ±0.68 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for smittenkitchen</summary>

**Q1: How do you make world peace cookies?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What's the recipe for miso chicken and rice?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | **Miso Chicken and Rice Recipe**  **Ingredients:** - 2 tablespoons (30ml) soy sauce - 1 tablespoon (... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How do I make ultimate banana bread?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To make ultimate banana bread, follow these steps:  1. Preheat your oven to 350 degrees F and butter... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: What's the skillet-baked macaroni and cheese recipe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: What vegan recipes are available on Smitten Kitchen?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The vegan recipes available on Smitten Kitchen include:  1. Winter Cabbage Salad with Mandarins and ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The vegan recipes available on Smitten Kitchen include:  1. Winter cabbage salad with mandarins and ... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | The vegan recipes available on Smitten Kitchen can be found under the "Vegan" category, which includ... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: Show me cookie recipes**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Here are some cookie recipes from the provided context:  1. [Brown Butter Snickerdoodles](https://sm... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Here are some cookie recipes from the provided context:  1. [Brown Butter Snickerdoodles](https://sm... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Here are the cookie recipes:  1. [Brown Butter Snickerdoodles](https://smittenkitchen.com/2025/10/br... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Here are the cookie recipes:  1. [Brown Butter Snickerdoodles](https://smittenkitchen.com/2025/10/br... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: How do you make pumpkin basque cheesecake?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: What recipes are good for winter?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The recipes mentioned as good for winter include curried lentils and sweet potatoes, lentil soup wit... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The recipes good for winter include:  1. Winter Cabbage Salad with Mandarins and Cashews 2. Winter F... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The recipes good for winter include:  1. Winter Cabbage Salad with Mandarins and Cashews 2. Winter F... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The recipes good for winter include:  1. Winter cabbage salad with mandarins and cashews 2. Baked po... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The recipes good for winter include:  1. Winter cabbage salad with mandarins and cashews 2. Baked po... |
| scrapy+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |

</details>

## stripe-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 4.89 | 4.83 | 4.78 | 4.83 | 4.83 ±0.33 |
| crawl4ai-raw | 4.89 | 4.83 | 4.78 | 4.83 | 4.83 ±0.33 |
| markcrawl | 4.89 | 4.83 | 4.67 | 4.83 | 4.81 ±0.33 |
| colly+md | 4.61 | 4.61 | 4.28 | 4.56 | 4.51 ±0.46 |
| scrapy+md | 4.61 | 4.50 | 4.22 | 4.44 | 4.44 ±0.53 |
| crawlee | 4.61 | 4.50 | 4.22 | 4.44 | 4.44 ±0.53 |
| playwright | 4.61 | 4.50 | 4.22 | 4.44 | 4.44 ±0.53 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for stripe-docs</summary>

**Q1: How do I create a payment intent with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you need to make a request to the Stripe API. Here’s a basic ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you need to make a server-side request to the Stripe API. Her... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you can use the following cURL command:  ```bash curl https:/... |
| markcrawl | 5 | 5 | 4 | 5 | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ``` curl https://ap... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | To create a PaymentIntent with Stripe, you can use the following cURL command:  ``` curl https://api... |
| colly+md | 5 | 5 | 4 | 5 | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do I handle webhooks from Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. Set up an HTTP handler to accept POST reques... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. **Create a webhook endpoint** on your server... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. **Create a webhook endpoint** on your server... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, you need to create a webhook endpoint that receives POST requests wi... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. Create a webhook endpoint on your server to ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. **Create a webhook endpoint** on your server... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, follow these steps:  1. Create a webhook endpoint on your server to ... |

**Q3: How do I set up Stripe subscriptions?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To set up Stripe subscriptions, you need to:  1. Create a [Product](https://stripe.com/docs/api/prod... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To set up Stripe subscriptions, follow these steps:  1. Install the Stripe client of your choice (av... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To set up Stripe subscriptions, follow these steps:  1. Install the Stripe client of your choice (av... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To set up Stripe subscriptions, follow these steps:  1. Create a Stripe account or sign in. 2. In th... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: How do I authenticate with the Stripe API?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To authenticate with the Stripe API, you need to use API keys. You can view and manage your API keys... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To authenticate with the Stripe API, you need to use API keys. You can view and manage your API keys... |
| markcrawl | 5 | 5 | 4 | 5 | 4.8 | To authenticate with the Stripe API, use the correct API key. Ensure you are not using a key that yo... |
| scrapy+md | 4 | 5 | 4 | 4 | 4.2 | To authenticate with the Stripe API, log in to your Stripe account using the command `stripe login`.... |
| crawlee | 4 | 5 | 4 | 4 | 4.2 | To authenticate with the Stripe API, log in and authenticate your Stripe user account to generate a ... |
| playwright | 4 | 5 | 4 | 4 | 4.2 | To authenticate with the Stripe API, log in and authenticate your Stripe user account using the comm... |
| colly+md | 3 | 4 | 3 | 4 | 3.5 | To authenticate with the Stripe API, log in to your Stripe user account to generate a set of restric... |

**Q5: How do I handle errors in the Stripe API?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should:  1. **Identify the Error Type**: Understand the type... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should:  1. Write code that gracefully handles all possible ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should:  1. **Check for Errors**: Implement error checking t... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, check for immediate errors such as a declined card. If an error ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, pay attention to the type of error encountered, such as `card_er... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should check for immediate errors when confirming payments a... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: How do I process refunds with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you need to report the refund after the original payment is successf... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can use the Stripe API or the Dashboard. For API refunds, you ne... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can use the Stripe API or the Dashboard. For API refunds, you ne... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can process refunds with Stripe by using the Refunds API or the Dashboard. To issue a refund, cr... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, go to the Payments page in the Stripe Dashboard. Select the payments... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can issue a refund for a customer by following these steps based... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, go to the Payments page in the Stripe Dashboard. Select the payments... |

**Q7: How do I use Stripe checkout for payments?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, follow these steps:  1. **Set Up Your Environment**: Include th... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, you can redirect to a Stripe-hosted payment page using the Chec... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, you can redirect to a Stripe-hosted payment page using the Chec... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, you can either redirect customers to a Stripe-hosted payment pa... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: How do I test Stripe payments in development?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use test cards, test clocks, and the Stripe CLI to s... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, use the following steps:  1. Utilize the sandbox environment... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, use the following steps:  1. Utilize the sandbox environment... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following methods:  1. **DevKit Devices**: P... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can:  1. Use a sandbox environment to simulate real-worl... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, use a sandbox environment to simulate Stripe-generated event... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following steps:  1. Set up your development... |

**Q9: What are Stripe Connect and platform payments?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to manage payments and facilitate... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to manage payments and facilitate... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows businesses, such as marketplaces and software platforms, to ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to route payments between themsel... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to facilitate payments on behalf ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to route payments between themsel... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q10: How do I set up usage-based billing with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To set up usage-based billing with Stripe, you need to follow these steps:  1. **Ingestion**: Send y... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To set up usage-based billing with Stripe, you can follow the implementation guide provided in the S... |
| colly+md | 4 | 5 | 4 | 4 | 4.2 | To set up usage-based billing with Stripe, you need to follow these steps:  1. **Create a Stripe acc... |
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
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You manage Stripe API keys by treating secret keys and restricted API keys (RAKs) as sensitive and n... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Never put secret API keys in source co... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Never put secret API keys in source co... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Never put secret API keys in source co... |

**Q12: How do I handle Stripe rate limits?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle Stripe rate limits, watch for `429` status codes and implement a retry mechanism. Follow a... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle Stripe rate limits, make your requests less frequently if you begin to receive `429` HTTP ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle Stripe rate limits, make your requests less frequently if you start receiving `429` HTTP e... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle Stripe rate limits, make your requests less frequently if you begin to receive `429` HTTP ... |
| colly+md | 5 | 5 | 4 | 5 | 4.8 | If you receive `429` HTTP errors in your testing environments, make your requests less frequently, a... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | To handle Stripe rate limits, if you begin to receive `429` HTTP errors in your testing environments... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q13: How do I use metadata with Stripe objects?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects to store custom key-value pairs that track additional infor... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value pairs to them through the `metadata`... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value pairs to them. This is done using th... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value pairs to them using the `metadata` p... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by adding it to common requests, such as processing payment... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value data to updateable objects such as A... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value data to updateable objects such as A... |

**Q14: How do I set up Apple Pay with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. Create a Stripe account. 2. Register for an... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. Create a Stripe account. 2. Register for an... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. Enroll in the Apple Developer Program. 2. S... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |

**Q15: How do I issue cards with Stripe Issuing?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, follow these steps:  1. Sign up for a Stripe account and activat... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, you first need to create a cardholder using the Stripe Issuing A... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, use the Stripe Issuing API to create a card for a cardholder by ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, you can use the Stripe Issuing API. Reference the cardholder ID ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, reference the cardholder ID and use the Stripe Issuing API. You ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, reference the cardholder ID and use the Stripe Issuing API. You ... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q16: How do I recover failed subscription payments?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you can set up a webhook endpoint to listen for the `custom... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, follow these steps:  1. Set up a webhook endpoint to listen... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, follow these steps:  1. Set up a webhook endpoint to listen... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you can enable the **Send emails when card payments fail** ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you can enable notifications to customers about failed paym... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, set up a webhook endpoint to listen for the `customer.subsc... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, set up a webhook endpoint to listen for the `customer.subsc... |

**Q17: How does Stripe handle tax calculation for billing?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing through its product, Stripe Tax, which automatically calc... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing by automatically determining the customer's location and ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing by automatically determining the customer's location and ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing by using Stripe Tax, which automatically calculates and c... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing by determining the customer's location and automatically ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Stripe calculates taxes for billing based on the customer's billing address entered during the Check... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Stripe calculates taxes for billing based on the customer's address. For new customers, it uses the ... |

**Q18: How do I migrate data to Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, you need to follow these steps:  1. **Contact Stripe**: Start the migrati... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, follow these steps:  1. Review Stripe’s migration documentation. 2. Conta... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, follow these steps:  1. Review Stripe’s migration documentation. 2. Conta... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, you can follow the standard migration process outlined in the documentati... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, you should follow these steps:  1. Understand the Stripe migration proces... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, you should follow a multi-step process that includes understanding the St... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, you should follow a multi-step process that includes understanding the St... |

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

