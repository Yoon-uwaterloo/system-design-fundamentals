Rate limiter (Chapter 4)

Description:
- This is a simple FastAPI-based rate limiter using Redis and a fixed window counter algorithm to limit requests per IP at the HTTP (Layer 7) level.

Useful command:
- redis-server
- redis-cli
- lsof -i 6375
- kill -9 <server-id>

Full description:
1. Rate limiting strategy (IP-based)
The current implementation uses an IP-based rate limiting strategy, where each client is identified by its IP address (request.client.host). This approach is simple and effective for basic protection. However, in production systems, user ID–based or API key–based rate limiting is often preferred because IP addresses can be shared or spoofed.

2. Algorithm used: Fixed Window Counter
This implementation uses the fixed window counter algorithm. A counter is maintained in Redis for each IP, and it resets after a fixed time window (MAX_TIME = 60 seconds). If the number of requests exceeds MAX_REQUEST = 5 within that window, further requests are rejected. As discussed in the book, this approach is simple but can lead to burst traffic at window boundaries. More advanced algorithms like token bucket or sliding window provide smoother rate limiting.

3. Rate limiting rules
The system currently applies a global rule of 5 requests per 60 seconds per IP. According to the book, rate limiting rules can be more flexible and configurable, such as defining limits based on domains (e.g., messaging, auth), request types, or user tiers. These rules are typically stored in configuration files or external systems for dynamic updates.

4. Concurrency and race conditions
The implementation uses Redis operations (get, set, incr) but does not fully address race conditions. In high-concurrency scenarios, multiple requests may read and update the counter simultaneously, leading to inaccurate counts. Production systems mitigate this using atomic operations, Lua scripts in Redis, or distributed synchronization mechanisms.

5. Layer of implementation (Layer 7)
This rate limiter operates at the HTTP application layer (Layer 7), implemented as FastAPI middleware. As described in the book, rate limiting can also be applied at other layers, such as network-level (Layer 4) or via API gateways, depending on system architecture and requirements.

6. Response behavior
When the rate limit is exceeded, the system returns an HTTP 429 (Too Many Requests) response. It includes useful metadata such as:
	•	limit information (X-RateLimit-Limit)
	•	retry time (X-RateLimit-Retry-After)
Additionally, successful responses include X-RateLimit-Remaining, indicating how many requests are left in the current window. This aligns with best practices for client transparency.

7. Monitoring and effectiveness
The current implementation does not include monitoring. In production, it is important to track metrics such as request rates, rejected requests, and system load to evaluate whether the rate limiting algorithm and rules are effective. Logging and metrics collection help identify misconfigurations or abuse patterns.

8. High-level architecture
At a high level, the system consists of a FastAPI application with middleware that intercepts incoming requests. Redis acts as a centralized store for request counters. Each request passes through the middleware, which checks the counter, enforces limits, and either forwards the request to the application or rejects it.

9. Low-level architecture
At a low level, each request triggers the following flow:
- Extract client IP from the request
- Fetch the current request count from Redis
- Initialize or increment the counter with expiration
- Compare against the threshold
- Return a 429 response if the limit is exceeded
- Otherwise, process the request and attach rate limit headers
This design is simple and efficient but would need enhancements such as atomic operations, distributed coordination, and configurable rules to scale for large systems.
