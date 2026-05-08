# System Design Interview
## An Insider's Guide
### by Alex Xu

---

# 1. Single server setup

Everything runs on one machine:

* Web server
* Application logic
* Database
* Cache

Good for:

* MVPs
* Small traffic

Problem:

* Cannot scale well
* Single point of failure

---

# 2. Database

As traffic grows:

* Separate database from web server
* Web tier and data tier scale independently

Benefits:

* Better performance
* Easier scaling

---

# 3. Cache

Stores frequently used data in memory.

Flow:

1. Check cache
2. If miss → query DB
3. Save result in cache

Benefits:

* Faster responses
* Reduced DB load

Common eviction:

* LRU (Least Recently Used)

---

# 4. Which databases to use?

SQL (Relational)

Examples:

* MySQL
* PostgreSQL

Best for:

* Structured data
* Transactions
* Joins

NoSQL

Examples:

* MongoDB
* Cassandra
* DynamoDB

Best for:

* Huge scale
* Unstructured data
* Low latency

---

# 5. Vertical scaling vs horizontal scaling

Vertical Scaling (Scale Up)

Add:

* CPU
* RAM
* Disk

Pros:

* Simple

Cons:

* Hardware limit
* Expensive
* Single point of failure

Horizontal Scaling (Scale Out)

Add more servers.

Pros:

* Better scalability
* High availability

---

# 6. Load balancer

Distributes traffic across multiple servers.

Benefits:

* Prevents overload
* Improves availability
* Supports failover

If one server fails:

* Traffic goes to healthy servers

---

# 7. Database replication

Master-Slave Model

* Master → writes
* Slaves → reads

Benefits:

* Better read performance
* High availability
* Reliability

If master fails:

* Promote a slave to master

---

# 8. Sharding(partition)

Split large database into smaller shards.

Benefits:

* Handles massive data
* Better scalability

Challenges:

* Resharding
* Hotspot keys
* Cross-shard joins