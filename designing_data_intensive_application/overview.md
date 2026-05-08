# Designing Data-Intensive Applications
## The Big Ideas Behind Reliable, Scalable, and Maintainable Systems
### by Martin Kleppmann

---

# Part I: Foundations on a Single Machine
In Part I, we explored the core principles of data systems operating on a single machine. The discussion focused on scenarios where an application relies on a single database, examining how data is stored, accessed, and managed within that limited scope.

# Chapter 1: Foundations

1. **Reliability**
  Systems keep working correctly even when faults occur.
2. **Scalability**
  Systems maintain good performance as load increases.
3. **Maintainability**
  Systems are easy for engineers to understand, modify, and operate.

---

# Chapter 2: Data Models

## Relational vs Document vs Graph Databases

---

# 🏛️ Relational Databases (SQL)

## What it is
- Data stored in **tables**
- Uses **fixed schemas**
- Relationships handled with **joins**

## Best for
- Structured data
- ACID transactions
- Complex queries

## Examples
- Banking systems
- Orders/payments
- Inventory systems

## Pros
- Strong consistency
- Powerful SQL queries
- Mature ecosystem

## Cons
- Rigid schema
- Expensive joins at scale

---

# 📄 Document Databases (NoSQL)

## What it is
- Data stored as **JSON-like documents**
- Uses **flexible schemas**
- Supports nested data

## Best for
- Semi-structured data
- Frequently changing schemas
- Read-heavy applications

## Examples
- User profiles
- CMS
- Product catalogs

## Pros
- Flexible schema
- Fast reads
- Easy mapping to application objects

## Cons
- Data duplication
- Harder relationship management

---

# 🕸️ Graph Databases

## What it is
- Data stored as **nodes and edges**
- Optimized for relationships

## Best for
- Highly connected data
- Relationship-heavy queries

## Examples
- Social networks
- Recommendation systems
- Fraud detection

## Pros
- Fast relationship traversal
- Flexible structure

## Cons
- Less ideal for tabular data
- Harder scaling in some cases

---

# Chapter 3: Storage and Retrieval

---

## 🧠 Overview
Chapter 3 explains how databases store and retrieve data internally, focusing on trade-offs between:
- Read efficiency
- Write efficiency
- Storage usage

---

# 🔑 1. Database Storage Approaches

Two main approaches:
- **Log-Structured Storage (LSM Trees)**
- **In-Place Update Storage (B-Trees)**

---

# 🧱 2. LSM Trees (Log-Structured Merge Trees)

### How it works
- Writes are appended sequentially
- Data is merged and compacted later

### Core Components
- **Memtable** → in-memory writes
- **SSTables** → immutable sorted files
- **Compaction** → merges files and removes old data

### Pros
- Very fast writes
- High write throughput
- Efficient sequential disk access

### Cons
- Slower reads
- Compaction is resource intensive

---

# 🌳 3. B-Trees

### How it works
- Data stored in tree pages
- Updates happen directly on disk

### Pros
- Fast reads
- Efficient range queries
- Mature and widely used

### Cons
- Slower writes
- Random disk I/O overhead

---

# ⚖️ 4. B-Trees vs LSM Trees

| Feature | B-Trees | LSM Trees |
|---|---|---|
| Writes | Slower | Faster |
| Reads | Faster | Slower |
| Storage | More overhead | More compact |
| Best for | Read-heavy | Write-heavy |


---

# 🧠 Key Takeaways
- Storage engines involve trade-offs
- **LSM Trees** → best for write-heavy systems
- **B-Trees** → best for read-heavy workloads
- Choose based on workload and access patterns

---

# Chapter 4: Encoding and Evolution

---

## 🧭 Overview
Chapter 4 explains how data is encoded (serialized) for storage and communication, and how systems handle schema evolution over time.

---

# 🔑 1. Why Encoding Matters

Encoding converts in-memory data into formats that can be:
- Stored
- Transmitted
- Shared between systems

It enables communication between different services and software versions.

---

# 🧱 2. Encoding Formats

## a. Text-Based Formats
Examples:
- JSON
- XML
- CSV

### Pros
- Human-readable
- Widely supported

### Cons
- Larger size
- Weak typing
- Less efficient

---

## b. Binary Formats
Examples:
- Protocol Buffers
- Thrift
- Avro

### Pros
- Compact
- Fast
- Strong schema support

### Best For
- High-performance distributed systems

---

# 🧩 3. Schemas

A schema defines the structure of data.

### Approaches
- **Schema-on-write**
  - Validate before storing
  - Common in relational databases

- **Schema-on-read**
  - Interpret when reading
  - Common in NoSQL systems

---

# 🔄 4. Schema Evolution

Systems change over time, so schemas must evolve safely.

## Compatibility Types

### Backward Compatibility
New systems can read old data.

### Forward Compatibility
Old systems can read new data.

---

# 🔁 5. Dataflow Between Systems

## Through Databases
- Stored data may outlive application versions

## Through APIs
- Often REST + JSON
- Requires versioning

## Through Messaging Systems
- Producers and consumers evolve independently

---

# Part II: Scaling Across Multiple Machines
In Part II, we expand our perspective to distributed systems. We consider what changes when data storage and retrieval span multiple machines, while still assuming a single logical database. This section introduces the challenges and trade-offs involved in scaling beyond a single node.

## Chapter 5

1. **Understand replication**
  Replication is the process of keeping copies of the same data across multiple machines (nodes) in a distributed system. It is used to reduce latency by placing data closer to users, improve fault tolerance so the system can continue working even if some nodes fail, and increase scalability by allowing more machines to serve read requests. The challenge in replication is not copying static data, but keeping all replicas consistent when the data changes over time.
2. **Use single-leader replication**
  In single-leader replication, one node (the leader) handles all write operations while other nodes (followers) replicate data from it. Clients send writes to the leader, which then propagates changes to followers, while reads can be served from either the leader or followers. This model is simple and widely used, but it can lead to stale reads if followers lag behind the leader.
3. **Understand multi-leader replication**
  Multi-leader replication allows multiple nodes to accept write operations, and each node replicates changes to the others. This model is useful for multi-datacenter deployments and offline-capable applications, but it introduces the problem of write conflicts when different nodes modify the same data concurrently, requiring conflict resolution strategies.
4. **Understand leaderless replication**
  Leaderless replication removes the concept of a leader entirely, allowing clients to write to multiple replicas directly. Systems like Cassandra use this approach with quorum-based reads and writes, where data is considered valid if enough nodes respond. This model provides high availability and fault tolerance but makes consistency harder to reason about.
5. **Choose replication mode carefully**
  Replication can be synchronous, where the leader waits for replicas to confirm a write before responding to the client, or asynchronous, where the leader responds immediately without waiting. Synchronous replication provides stronger consistency guarantees but reduces availability, while asynchronous replication improves performance but risks data loss if the leader fails before replication completes.
6. **Know the trade-offs**
  Replication is essential for building scalable and reliable systems, but it introduces trade-offs between consistency, availability, and performance. Single-leader replication is simpler but less flexible, while multi-leader and leaderless approaches provide higher availability at the cost of increased complexity and weaker consistency guarantees.

## Chapter 6

1. **Understand partitioning**  
   Partitioning is a way of breaking a large database down into smaller ones, where each piece of data belongs to exactly one partition. The main reason for wanting to partition data is scalability, as different partitions can be placed on different nodes so that data storage and query load can be distributed across many machines.
2. **Know the goal of partitioning**  
   The main goal of partitioning is to spread data and query load evenly across multiple machines while avoiding hot spots. Choosing the right partitioning strategy and managing rebalancing are essential for achieving scalability.
3. **Combine partitioning with replication**  
   Partitioning is usually combined with replication, so that copies of each partition are stored on multiple nodes. This means that, even though each record belongs to exactly one partition, it may still be stored on several different nodes for fault tolerance.
4. **Partition by key range**  
   One way of partitioning is to assign a continuous range of keys to each partition, allowing efficient range queries and ordered data access. However, certain access patterns can lead to hot spots, where one partition receives a disproportionate amount of traffic.
5. **Partition by hash of key**  
   Many distributed datastores use a hash function to determine the partition for a given key, which helps distribute data evenly across nodes. However, hashing destroys the ordering of keys, making range queries inefficient.
6. **Understand secondary index partitioning**  
   A secondary index also needs to be partitioned, and there are two possibilities for doing this.
7. **Use document-partitioned indexes**  
   Document-partitioned index: the secondary indexes are stored in the same partition as the primary key and value. This means that only a single partition needs to be updated on write, but a read of the secondary index requires a scatter/gather across all partitions.
8. **Use term-partitioned indexes (global index)**  
   Term-partitioned index (global index): the secondary indexes are partitioned separately, using the indexed values. An entry in the secondary index may include records from all partitions of the primary key. When a document is written, several partitions of the secondary index need to be updated; however, a read can be served from a single partition.

---

# Part III: Integrating Multiple Data Systems
In Part III, we move further into complexity by exploring how different data systems interact. This section examines the challenges of integrating multiple technologies, focusing on how to combine them effectively to build cohesive, reliable applications.

## Chapter 10

1. **Understand batch processing**
Batch processing is a way of processing large amounts of data all at once, usually on a schedule rather than continuously.
Instead of handling events immediately as they happen, the system:
- Collects data over time
- Runs a job over the entire dataset
- Produces results afterward

2. **Why we need batch processing**
We use batch processing because it:
* Efficiently processes huge datasets
* Optimizes throughput over speed
* Supports historical analysis
* Can recompute derived data reliably
* Handles failures well

3. **How batch processing works**
Typical flow:
1. Read data
2. Transform/filter/aggregate
3. Write output

Key concepts:
* Unix pipelines
* MapReduce (Map + Reduce stages)
* Distributed filesystems
* Parallel processing across many machines

## Chapter 11

1. **Understand what a stream is**  
A stream is:
A continuous flow of events happening over time.
Instead of processing a complete dataset,
stream systems process data:
* Incrementally
* Continuously
* In real time

2. **Understand why we need streams**  
Streams are needed for:
* Real-time processing
* Low latency systems
* Event-driven applications
* Continuous analytics
* Keeping systems synchronized

3. **Understand how streams work**  
Streams usually work with:

* Append-only logs
* Producers sending events
* Consumers processing events
* Partitioned streams for scalability
* Stateful processing and fault tolerance

Examples:

* Kafka
* Flink
* Kinesis