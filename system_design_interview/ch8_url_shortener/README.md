# Design a url shortener

## Step 1: Understand the Problem and Establish Design Scope (3–10 minutes)

I’d start by clarifying requirements: the service must support two core flows—shortening a long URL into a short alias and redirecting the alias back to the original URL—while being highly available, scalable, and fault tolerant. I’d confirm expected scale, which here is about 100 million new URLs per day, roughly 1.1K writes/sec and, assuming a 10:1 read/write ratio, about 11.6K reads/sec. I’d also call out capacity planning: over 10 years this grows to roughly 365 billion records and around 365 TB of raw URL storage if the average long URL is 100 bytes. I’d ask whether links can expire, be deleted, or updated; for this scope, assume they cannot, which simplifies storage and consistency.

---

## Step 2: Propose High-Level Design and Get Buy-In (10–15 minutes)

At a high level, I’d expose two REST endpoints: a POST /api/v1/data/shorten that accepts a long URL and returns a short URL, and a GET /api/v1/{shortUrl} that resolves and redirects to the original long URL. The shortening path writes a mapping from short URL to long URL into persistent storage, while the redirect path looks up that mapping and returns an HTTP redirect. For redirect semantics, I’d mention the 301 vs 302 tradeoff: 301 reduces load because browsers cache the permanent redirect, while 302 is better if analytics matter because every click comes back through the service. Conceptually, the system consists of clients, load balancers, stateless web servers, a storage layer for mappings, and optionally a cache in front of the database for hot redirects.

---

## Step 3: Design Deep Dive (10–25 minutes)

For storage, I’d move from an in-memory hash table idea to a relational database that stores at least id, shortURL, and longURL, since memory alone is too expensive at this scale. For key generation, I’d prefer base-62 encoding of a globally unique numeric ID, because the character set is [0-9a-zA-Z]; 62^7 is about 3.5 trillion, so 7 characters are enough for the projected 365 billion URLs. The shortening flow is: check whether the long URL already exists, return the existing short URL if it does, otherwise generate a new unique ID, convert it to base 62, and save the new row. For redirects, since reads dominate writes, I’d put the <shortURL, longURL> mapping in cache: the load balancer sends traffic to web servers, they check cache first, fall back to the database on a miss, and then return the long URL via redirect. I’d also mention an alternative design based on hashing plus collision resolution, but base-62 with unique IDs is cleaner because it avoids collisions entirely, though it does require a robust distributed ID generator.

---

## Step 4: Wrap Up (3–5 minutes)

To close, I’d summarize that the design hinges on simple APIs, a durable mapping store, a unique ID generator with base-62 conversion, and a cache-optimized redirect path for read-heavy traffic. Then I’d mention the main production hardening points: rate limiting to prevent abuse on the shorten endpoint, easy horizontal scaling of stateless web servers, database replication and sharding as the dataset grows, analytics if the business wants click tracking, and the usual availability, consistency, and reliability tradeoffs. That shows not just a working MVP, but also awareness of how the design evolves into a real internet-scale service.

---