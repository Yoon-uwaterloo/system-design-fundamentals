# 🚦 Design a Rate Limiter

## 📌 What is a Rate Limiter

A **rate limiter** controls how many requests a client or service can send within a specific time window.

It is used to:
- Prevent abuse and DoS attacks
- Protect servers from overload
- Reduce infrastructure cost
- Control traffic to expensive APIs
- Ensure fair usage across users

If a client exceeds the allowed limit, the system returns:
HTTP 429 Too Many Requests

---

## 🔄 Step-by-Step Architecture

The detailed design works as follows:
1. Client sends request
2. Request first reaches rate limiter middleware
3. Middleware checks counters and timestamps in Redis
4. If request is allowed, forward it to API servers
5. If request is rate limited, return 429 Too Many Requests
6. Rate-limited requests are either dropped or sent to a message queue

---

## 🧩 Distributed rate limiter

### 1. Race condition
A race condition happens when multiple requests update the same counter at the same time.

Example:

1. Counter value in Redis = 3
2. Two requests arrive simultaneously
3. Both read the value 3
4. Both increment it to 4
5. Final value becomes 4 instead of 5

This causes incorrect rate limiting.

✅ Solutions

* Use atomic operations in Redis
* Use Lua scripts in Redis
* Use Redis sorted sets
* Avoid traditional locks because they slow down the system

---

### 2. Synchronization issue
In distributed systems, requests from the same client may hit different rate limiter servers.

Example:

* Request 1 → Rate Limiter Server A
* Request 2 → Rate Limiter Server B

If servers store counters locally, they will have inconsistent data.

✅ Solution

Use a centralized datastore like Redis.

All rate limiter servers read and update counters from the same Redis instance, ensuring:

* Consistent counters
* Accurate rate limiting
* Shared state across servers