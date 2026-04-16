# Design a news feed system

## Step 1: Understand the Problem and Establish Design Scope (3–10 minutes)

Start by clarifying the product and scale: this feed should work for both web and mobile, let users publish posts and view friends’ posts, support text plus media like images and videos, and show items in reverse chronological order. You should also confirm constraints such as up to 5,000 friends per user and around 10 million daily active users, because those numbers directly affect storage, caching, and fanout strategy. The goal is to define a scope that is simple enough to design in an interview while still realistic.  ￼

---

## Step 2: Propose High-Level Design and Get Buy-In (10–15 minutes)

At a high level, split the system into two flows: feed publishing and news feed retrieval. For publishing, a user sends a post request through a load balancer to web servers, which call a post service to persist the post in database and cache, then trigger a fanout service to distribute that post to friends’ feeds and a notification service to alert them. For retrieval, the user requests their feed, web servers call a news feed service, and that service reads precomputed feed data from cache so the response is fast. This separation makes the design easy to explain and gives a clean foundation before discussing tradeoffs.  ￼

---

## Step 3: Design Deep Dive (10–25 minutes)

The most important deep-dive topic is fanout. Fanout on write pushes a new post to friends immediately, which makes reads fast but becomes expensive for users with huge follower counts; fanout on read builds the feed only when someone opens the app, which saves work for inactive users but slows feed loading. A practical design uses a hybrid model: push for normal users and pull for celebrities or very high-fanout accounts. The detailed publishing path fetches friend IDs from a graph database, filters them using user settings like mute or privacy rules, sends work through a message queue, and has fanout workers write <post_id, user_id> entries into the news feed cache. On the read path, the service fetches post IDs from the feed cache, hydrates them with user and post data from separate caches, and returns the completed feed, while media is served from a CDN.  ￼

---

## Step 4: Wrap Up (3–5 minutes)

To close, summarize that the system depends on two core ideas: fast publishing with asynchronous fanout and fast retrieval through aggressive caching. Mention the most important scaling extensions: keep the web tier stateless, use message queues to decouple components, shard and replicate databases as traffic grows, cache different data types separately, and monitor metrics like QPS and feed refresh latency. There is no single perfect design, so the strongest wrap-up is showing that you understand the tradeoffs and how the architecture can evolve as the product and user base grow.  ￼

---