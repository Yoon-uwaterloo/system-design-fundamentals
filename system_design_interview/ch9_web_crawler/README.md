# Design a web crawler

## Step 1: Understand the Problem and Establish Design Scope (3–10 minutes)

Start by clarifying the product requirements and scale. Ask whether the system needs only URL shortening or also custom aliases, expiration dates, analytics, and abuse prevention. Clarify expected traffic, such as reads per second versus writes per second, because URL shorteners are usually read-heavy. Define core requirements: given a long URL, generate a short unique alias; when users visit the short link, redirect them to the original URL with low latency and high availability. Nonfunctional goals usually include high read throughput, durability, scalability, and preventing collisions. A useful back-of-the-envelope estimate is that if the service creates millions of short URLs per day and stores them for years, the storage requirement is manageable, while the redirect path must be extremely fast because it is the hot path.

---

## Step 2: Propose High-Level Design and Get Buy-In (10–15 minutes)

At a high level, the system has two main APIs: one to create a short URL and one to resolve it. For creation, the client sends a long URL to an API service, which validates the input, generates a unique short code, stores the mapping in a database, and returns the shortened URL. For redirection, the user hits the short URL, the request goes to a read-optimized application service, which looks up the short code in a cache first and then in persistent storage if needed, and returns an HTTP redirect to the long URL. A common design is to use a key-value style data model where the short code is the key and the long URL plus metadata is the value. To support scale, place a cache in front of the database, use load balancers across stateless application servers, and optionally add an analytics pipeline that asynchronously logs clicks so the redirect path stays fast.

---

## Step 3: Design Deep Dive (10–25 minutes)

The most important deep-dive topics are short-code generation, data storage, caching, and reliability. For code generation, two common approaches are a global auto-increment ID encoded in Base62, or a random string with collision checks; Base62 is simpler and compact, while random codes avoid a central bottleneck but need collision handling. The database stores mappings like shortCode → longURL, creation time, expiration time, and user metadata, and can be sharded by short code for scale. Since redirects dominate traffic, cache popular mappings in Redis or memory to reduce database reads. To improve reliability, replicate data, use consistent hashing or range-based sharding, and make application servers stateless. Handle edge cases like expired links, deleted links, malformed URLs, and malicious destinations. Analytics such as click counts, referrers, and geolocation should be processed asynchronously through logs or a queue so the redirect request remains low latency.

---

## Step 4: Wrap Up (3–5 minutes)

To summarize, a URL shortener is a simple but highly read-heavy system built around generating unique short codes, storing durable mappings, and serving redirects with very low latency. The core design uses stateless API servers, a cache for hot links, and a persistent database for long-term storage, with careful thought given to unique ID generation and horizontal scaling. In an interview, it is good to mention tradeoffs between sequential IDs and random IDs, how to avoid collisions, how to handle analytics without slowing redirects, and how to deal with abuse such as spam or phishing. If time allows, you can also discuss custom aliases, expiration support, rate limiting, and multi-region deployment to improve availability and performance.

---