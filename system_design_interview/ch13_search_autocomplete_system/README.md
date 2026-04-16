# Design a search autocomplete system

## Step 1: Understand the Problem and Establish Design Scope (3–10 minutes)

- Functional requirements
The search autocomplete system should provide real-time suggestions as a user types a query, returning a limited number of results (e.g., top 5) that match the given prefix. The suggestions should be based on historical search frequency, ensuring that more popular queries are prioritized and displayed first. The system only supports prefix-based matching (not middle-word matching), assumes queries are in lowercase English without special characters, and does not include spell check or autocorrect functionality. It should continuously collect user search inputs and update the underlying data so that future suggestions reflect user behavior and trends.
- Non-functional requirement
The system must deliver autocomplete suggestions with very low latency (ideally within ~100 milliseconds) to ensure a smooth user experience. It should be highly scalable to support millions of daily active users and handle tens of thousands of queries per second, especially during peak load. The system must maintain high availability and remain operational even in the presence of partial failures. Additionally, it should ensure relevance and correctness of results while efficiently managing storage and processing large volumes of query data. Performance optimizations such as caching and efficient data structures are essential to meet responsiveness and scalability requirements.

---

## Step 2: Propose High-Level Design and Get Buy-In (10–15 minutes)

Data gathering service: It collects user search queries and builds a frequency table by counting how often each query is searched over time. This data is later used to determine which queries are most popular.

Query service: It takes a user’s input prefix and returns the top matching queries sorted by frequency. It retrieves results by filtering queries that start with the prefix and ranking them by popularity.

---

## Step 3: Design Deep Dive (10–25 minutes)

Trie data structure: Autocomplete using a trie works by first navigating the tree to the node that matches the given prefix (taking O(p) time, where p is the prefix length), then traversing its subtree to collect all valid query strings (taking O(c), where c is the number of children), and finally sorting these results by frequency to return the top k suggestions (taking O(c log c)). For example, if a user types “tr”, the system finds the “tr” node, gathers all matching queries like “tree”, “true”, and “try”, and then returns the most frequent ones such as “true” and “try” as the top results.

Data gathering service: We collect user queries in analytics logs, aggregate them periodically to compute query frequencies, and use background workers to build a trie. The trie is stored in a database and loaded into an in-memory cache for fast lookup. This avoids expensive real-time updates and ensures low latency.

Query service: The query service is designed for low latency. Requests go through a load balancer to API servers, which fetch autocomplete results from an in-memory trie cache. Since the trie stores top-k results per prefix, lookup is O(1). On cache miss, data is fetched from persistent storage and cached. Additional optimizations like browser caching and AJAX reduce load and improve user experience.

Trie update: The trie is built offline using aggregated data. For updates, we typically rebuild the trie periodically and replace the old version, as updating nodes in real time is expensive due to propagation to ancestor nodes. For deletions, we introduce a filter layer to remove unwanted suggestions at query time and clean them asynchronously in storage.

---

## Step 4: Wrap Up (3–5 minutes)

The batch-based trie is too slow for real-time trends, so we introduce a streaming pipeline using systems like Kafka or Spark Streaming. We adjust the ranking model to prioritize recent queries and combine real-time results with historical data.

---

