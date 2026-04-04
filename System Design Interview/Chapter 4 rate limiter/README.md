# Design a Rate Limiter

## Step 1: Understand the Problem and Establish Design Scope (3–10 minutes)

Before jumping into architecture, clarify the requirements.

### Key Questions
1. Is this a **client-side** rate limiter or a **server-side** rate limiter?
2. Should API requests be limited based on:
   - IP address
   - User ID
   - API key
   - Other properties
3. What is the **scale of the system**?
   - This helps decide whether we need one or multiple rate limiter instances.
4. Does it need to work in a **distributed system**?
   - This introduces concerns like:
     - race conditions
     - synchronization issues
5. Do we need to **inform users** when they are throttled?
6. Where should the rate limiter be implemented?
   - Inside the server
   - In an API gateway

### Requirements
- Accurately limit excessive requests
- Low latency
- Low memory usage
- Support distributed rate limiting
- Clear exception handling for throttled users
- High fault tolerance

---

## Step 2: Propose High-Level Design and Get Buy-In (10–15 minutes)
<img width="607" height="249" alt="Screenshot 2026-04-04 at 3 37 26 AM" src="https://github.com/user-attachments/assets/f0cfdd69-863f-49e4-b2c9-1aa657a8dfe4" />

### High-Level Architecture
- The client sends a request to the **rate limiting middleware**
- The middleware checks the request counter in **Redis**
- Redis is a good fit because:
  - it is in-memory and very fast
  - it supports atomic operations like `INCR`
  - it supports key expiration with `EXPIRE`
  - it works well in distributed systems

### Request Flow
1. The client sends a request to the rate limiting middleware
2. The middleware fetches the counter from the corresponding bucket in Redis
3. The middleware checks whether the limit has been reached

#### If the limit is reached
- Reject the request

#### If the limit is not reached
- Forward the request to the API servers
- Increment the counter in Redis
- Save the updated value back to Redis

---

## Step 3: Design Deep Dive (10–25 minutes)
<img width="611" height="473" alt="Screenshot 2026-04-04 at 3 37 09 AM" src="https://github.com/user-attachments/assets/113946df-822b-49e2-a8cf-70de2cbab91a" />

### Detailed Design
- Rules are stored on disk
- Workers frequently pull rules from disk and store them in cache
- When a client sends a request, it first goes through the rate limiter middleware
- The middleware:
  - loads rules from cache
  - fetches counters and last request timestamps from Redis
  - decides whether the request should pass or be throttled

### Decision Logic
#### If the request is not rate limited
- Forward it to the API servers

#### If the request is rate limited
- Return **HTTP 429 Too Many Requests**
- The request is either:
  - dropped
  - or forwarded to a queue for later processing

### Important Distributed System Concerns

#### 1. Race Condition
In a distributed environment, multiple servers may read and update the same counter at the same time.

Example:
- Two requests read the same counter value
- Both think they are allowed
- Both increment it
- This may allow more requests than intended

Possible solutions:
- Use atomic Redis operations
- Use Lua scripts in Redis
- Use sorted sets depending on the algorithm

#### 2. Synchronization Issue
If multiple rate limiter servers exist, they must share the same state.

Solution:
- Use a centralized datastore such as Redis

---

## Step 4: Wrap Up (3–5 minutes)

At the end, discuss trade-offs, limitations, and possible improvements.

### Topics Worth Discussing

#### Pros
- Fast request checking
- Works well with Redis
- Easy to scale horizontally
- Supports distributed systems

#### Cons
- Redis can become a bottleneck if not scaled properly
- Distributed coordination adds complexity
- Some algorithms are more memory-heavy than others

### Improvements
1. **Multi-data center setup**
   - Reduce latency by placing rate limiter instances closer to users
2. **Synchronize data with eventual consistency**
   - Improves scalability in distributed deployments
3. **Monitoring**
   - Track throttled requests
   - Measure latency
   - Observe Redis health
   - Detect unusual traffic spikes

---

## Additional Discussion Points
- Hard vs soft rate limiting
- Choice of rate limiting algorithm:
  - Token bucket
  - Leaky bucket
  - Fixed window counter
  - Sliding window log
  - Sliding window counter
- Whether to implement the limiter in:
  - application code
  - middleware
  - API gateway

---

## Final Summary
A good rate limiter design should be:
- accurate
- low latency
- memory efficient
- fault tolerant
- distributed
- easy to monitor and improve
