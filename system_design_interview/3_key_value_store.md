# Design a Key-Value Store (System Design)

## What is a Key-Value Store?
A key-value store is a NoSQL database where data is stored as: key -> value

---

## Distributed Key-Value Store & CAP Theorem
To support massive scale, data is distributed across many servers.

CAP Theorem

A distributed system can only guarantee 2 of 3:

1. Consistency (C)
    All users see the latest data.
2. Availability (A)
    Every request gets a response.
3. Partition Tolerance (P)
    System continues working despite network failures.

In practice:

* Network partitions are unavoidable.
* Most distributed KV stores choose:
    * CP → consistency prioritized
    * AP → availability prioritized

Examples:

* Cassandra, DynamoDB → AP/Eventual consistency
* Traditional banking systems → CP

---

## System Components

---

### Data Partition
Goal:
* Distribute data evenly across servers.
* Minimize data movement when nodes change.

Solution: Consistent Hashing
Benefits:
* Easy scaling
* Balanced load
* Minimal reshuffling when adding/removing nodes

---

### Data Replication
To improve reliability:

* Data is copied to multiple nodes.

Example:

* Replication factor N = 3
* Same key stored on 3 servers.

Benefits:

* Fault tolerance
* High availability
* Disaster recovery

Replication is usually asynchronous.

---

### Write Path

Typical write flow:

1. Client sends write request.
2. Coordinator routes request.
3. Data written to:
    * Commit log (durability)
    * Memory cache (speed)
4. Data later flushed to disk as SSTables.

Components:

* Commit log
* MemTable / cache
* SSTables

---

### Read Path

Typical read flow:

1. Check memory cache.
2. If not found:
    * Use Bloom Filter to identify SSTable
3. Read from SSTable on disk.
4. Return result to client.

Goal:

* Minimize disk reads
* Reduce latency