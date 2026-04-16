# Designing Data-Intensive Applications

## The Big Ideas Behind Reliable, Scalable, and Maintainable Systems

### by Martin Kleppmann

---

## Overview

Designing Data-Intensive Applications explains how modern software systems that handle large amounts of data are built, focusing on the core principles of reliability, scalability, and maintainability. It teaches that instead of just learning specific tools (like databases or frameworks), engineers should understand the underlying concepts—such as how data is stored, processed, replicated, and kept consistent across systems—so they can make better design decisions. The book walks through real-world technologies and trade-offs, showing how different approaches (like relational vs. NoSQL databases, batch vs. stream processing, and distributed systems) solve different problems, and emphasizes that good system design is about choosing the right combination of tools while understanding their limitations and behavior under the hood.

---

# Part 1: In Part I of this book, we discussed aspects of data systems that apply when data is stored on a single machine. this discussion assumed that there was only one database in the application

## Chapter 1: Foundations

1. **Reliability**
  Systems keep working correctly even when faults occur.
2. **Scalability**
  Systems maintain good performance as load increases.
3. **Maintainability**
  Systems are easy for engineers to understand, modify, and operate.

---

## Chapter 2: Data Models

1. **Start with your data, not the database.**
  Figure out what real-world things your app deals with: users, posts, products, orders, messages, comments, locations, and so on. Chapter 2 says data models shape how you think about the problem, so first be clear about the core entities and their relationships.
2. **Check whether your data is mostly document-like or highly connected.**
  If each item is mostly self-contained, like a profile, article, or settings object, a document model can fit well. If your data has lots of links across records, like users following users, products linked to categories, or recommendations between many entities, then relational or graph models are usually better.
3. **Look for one-to-many relationships.**
  Ask whether your data naturally forms a tree, such as a user with many addresses, a post with many sections, or an order with many line items. Chapter 2 shows that document databases are often a good fit for this kind of nested structure because related data can live together in one place.
4. **Look for many-to-one and many-to-many relationships.**
  If many records point to the same thing, like many users belonging to one region, or many students taking many courses, then joins become important. Chapter 2 warns that document models become awkward here, while relational databases handle this more naturally.
5. **Decide how much normalization you need.**
  If the same information appears in many places, storing it once and referencing it by ID can reduce duplication and inconsistency. That is useful when values may change, such as company names, categories, or locations. If you duplicate data for simplicity or speed, remember your app must keep those copies consistent.
6. **Think about how you will read the data most often.**
  If your app usually loads a whole object at once, like a full profile page or full product document, document storage can give better locality. If you often combine information from multiple entities in flexible ways, relational queries may be better. Chapter 2 emphasizes choosing the model that matches your access patterns.
7. **Decide how strict your schema should be.**
  If your data structure changes often, or different records may have different shapes, schema flexibility can help. If most records should follow the same structure, an enforced schema can improve clarity and safety. Chapter 2 frames this as schema-on-read versus schema-on-write.
8. **Choose a query style that helps you evolve.**
  Prefer declarative queries when possible. Chapter 2 explains that languages like SQL, Cypher, and SPARQL let you say what you want instead of how to fetch it, which gives the database more room to optimize and makes your app easier to maintain.
9. **Avoid forcing one model onto the wrong problem.**
  If your data is highly interconnected, graph models may be more natural than trying to force everything into documents. If your app is mostly forms and business records, relational may be simpler than graph. Chapter 2’s big message is that there is no one-size-fits-all data model.
10. **Pick the simplest model that matches your real use case.**
  Do not choose a database because it is trendy. Choose it because it matches your data shape, relationships, schema needs, and query patterns. That is the main practical lesson of Chapter 2.

---

## Chapter 3: Storage and Retrieval

1. **Decide how your app stores and retrieves data.**
  Use Chapter 3 as a practical checklist for choosing how your app stores data, what queries it must answer, and which database patterns fit those needs.
2. **Understand your app’s behavior first.**
  Start by listing your app’s main operations: what gets written, what gets read, whether users fetch single records by ID, scan ranges, or run dashboards and reports.
3. **Classify your workload type.**
  Then separate those needs into transactional workloads and analytic workloads—if your app mostly does quick reads/writes for user actions, think OLTP; if it runs heavy reports over lots of data, think OLAP, and consider a separate warehouse instead of forcing one database to do both jobs.
4. **Choose indexes carefully.**
  Next, choose indexes based on actual query patterns, because indexes speed reads but slow writes; for example, if you fetch records by exact key, a key-value or hash-style approach may work well, while range queries fit sorted indexes like B-trees or SSTables/LSM-trees better.
5. **Pick the right storage engine.**
  After that, choose the storage engine style: prefer LSM-tree/log-structured systems when your app has lots of writes and can tolerate compaction trade-offs, and prefer B-trees when you want steadier read performance and traditional transactional behavior.
6. **Handle analytics separately if needed.**
  If your app has dashboards or reporting over huge tables, use column-oriented storage or send operational data through ETL into a data warehouse, because that is much more efficient for aggregates and scans than a row-oriented OLTP database.
7. **Test with real workloads.**
  Then validate the choice by benchmarking with your real workload, not guesses, since the chapter stresses that actual performance depends heavily on access patterns.
8. **Keep improving over time.**
  Finally, keep tuning simple: add only the indexes you truly need, watch memory use, watch write amplification and compaction, and revisit your design as usage grows so your storage matches the way your application is actually being used.

### Storage Concepts

- Log-Structured Storage Engines (SSTables, LSM-trees)  
- B-trees  
- Column-Oriented Storage (OLATP systems)  
- In-Memory Storage

---

## Chapter 4: Encoding and Evolution

1. **Identify data boundaries**
  First, list where data crosses process boundaries in your app—database rows/documents, API requests and responses, queue messages, and files.
2. **Choose data formats**
  Then choose formats for each boundary: JSON is fine for simple public APIs, while Avro, Protocol Buffers, or Thrift are better when you want compact binary data, stronger schemas, and safer evolution.
3. **Design your schema**
  Next, define your initial schema carefully, give fields stable names or tags, make new fields optional or give them defaults, and never reuse removed field identifiers.
4. **Handle unknown fields safely**
  After that, build your readers and writers so they ignore unknown fields instead of crashing, and preserve fields they do not understand when reading and writing data back.
5. **Version your schema**
  Then introduce a schema versioning strategy, such as storing schema versions centrally or embedding enough metadata so services know how to decode old and new data correctly.
6. **Evolve without breaking**
  When you change the schema, add fields before removing old ones, deploy code that can read both old and new formats, roll out writers only after readers are ready, and test compatibility with sample payloads from multiple versions.
7. **Keep APIs backward-compatible**
  For APIs and services, prefer changes that old clients can tolerate, like adding optional request or response fields, and avoid breaking formats abruptly.
8. **Treat messages as contracts**
  For queues and message brokers, treat messages like long-lived contracts: publish stable schemas and let consumers upgrade independently.

---

# Part 2: Now, in Part II, we move up a level and ask: what happens if multiple machines are involved in storage and retrieval of data? this discussion assumed that there was only one database in the application

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
6. **Design for eventual consistency**
  Eventual consistency means that replicas will become consistent over time if no new updates are made, but there is no guarantee on how long this will take. While it improves performance and availability, it requires applications to tolerate temporary inconsistencies and design around them.
7. **Handle failures and failover**
  When a leader node fails, the system must detect the failure, promote a new leader, and redirect traffic accordingly. This process can be complex and error-prone, especially with asynchronous replication where recent writes may be lost or inconsistencies may occur during failover.
8. **Know the trade-offs**
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

## Chapter 7

1. **Transactions, ACID, and guarantees**  
   A transaction is a group of database operations executed as a single unit, ensuring that either all changes are applied (commit) or none are (abort), which prevents partial updates and simplifies failure handling. These guarantees are formalized through ACID: Atomicity (all-or-nothing), Consistency (rules are preserved), Isolation (transactions don’t interfere), and Durability (data persists after commit). Together, they provide a framework for building reliable systems, although their exact implementation varies across databases.
2. **Transaction models, isolation, and trade-offs**  
   Databases implement different transaction models, ranging from strong ACID guarantees to weaker models (BASE), each balancing correctness, performance, and scalability. Isolation levels like read committed, snapshot isolation, and serializable define how much protection is provided against concurrency issues such as lost updates or inconsistent reads. Stronger guarantees (e.g., serializability) reduce anomalies but require more coordination and can impact performance, while weaker guarantees improve efficiency at the cost of increased application complexity.

## Chapter 8

1. **Unreliability and partial failure in distributed systems**  
   Distributed systems operate in an environment where failures are partial, unpredictable, and unavoidable, meaning some components may fail while others continue working. Networks can drop or delay messages, processes can pause unexpectedly, and nodes may appear dead even when they are not, making it impossible to fully trust communication or system state. Systems must be designed with the assumption that failures will happen and must handle them gracefully rather than relying on ideal conditions.
2. **Limits of time, coordination, and correctness**  
   Reliable coordination is difficult because clocks are imperfect, events cannot be globally ordered with certainty, and there is no shared state across nodes. Time-based assumptions can lead to incorrect behavior (e.g., misordered writes), and detecting failures relies on uncertain mechanisms like timeouts. To manage this complexity, distributed systems rely on system models and define correctness using safety and liveness properties, allowing engineers to reason about behavior despite unreliable components.

## Chapter 9

1. **Consistency, linearizability, and trade-offs**  
   Distributed systems provide different consistency guarantees, ranging from weak models like eventual consistency to strong models like linearizability, which makes the system behave as if there is only a single up-to-date copy of the data. While stronger guarantees simplify reasoning and correctness, they come at the cost of higher latency, reduced availability during network failures, and increased coordination overhead, highlighting fundamental trade-offs in system design.
2. **Ordering, consensus, and coordination**  
   Correct behavior in distributed systems relies on ordering operations and ensuring nodes agree on shared state. Concepts like causality and total order broadcast help define how events are ordered, while consensus algorithms ensure all nodes agree on decisions such as leader election or transaction outcomes. These mechanisms are essential for building reliable systems, but are complex due to failures, network delays, and the inherent difficulty of coordination.

---

# Part 3: we will examine the issues around integrating multiple different data systems

## Chapter 10

1. **Understand batch processing**
  Batch processing is a method of processing large volumes of data all at once, rather than handling individual requests in real time. Instead of responding to user actions immediately, a batch system collects input data over a period of time and runs a job that processes the entire dataset to produce output. These jobs may take minutes, hours, or even days to complete, and are typically scheduled to run periodically, such as daily analytics or log processing.

2. **Why we need batch processing**
  Batch processing is essential because many data problems involve analyzing huge datasets that are too large or complex for real-time systems. It allows systems to efficiently compute aggregates, build indexes, train machine learning models, and generate reports by scanning entire datasets. It is also more cost-effective and scalable, since it can process data in bulk, tolerate delays, and run on distributed systems without requiring immediate responses to users.

3. **How batch processing works**
  Batch processing works by taking a large input dataset, dividing it into smaller chunks, and processing those chunks in parallel across multiple machines. A common model is MapReduce, where the system first maps input records into key-value pairs, then groups and sorts them by key, and finally reduces them by aggregating results. The output is written as new data (often files), and multiple batch jobs can be chained together into workflows where the output of one job becomes the input of the next.

## Chapter 11

1. **Understand what a stream is**  
   A stream is a continuous, unbounded sequence of events that are generated over time, where each event represents something that happened (such as a user action, system log, or sensor reading) and is typically immutable and timestamped. Unlike batch data, which is finite and processed as a whole, streams are incrementally produced and processed as they arrive, making them suitable for real-time systems. Conceptually, a stream can be viewed as an append-only log of events that records the history of changes in a system.

2. **Understand why we need streams**  
   Streams are needed because many real-world systems generate data continuously and require low-latency processing rather than waiting for periodic batch jobs. They enable real-time analytics, monitoring, and responsive applications such as fraud detection, live dashboards, recommendation systems, and notifications. Additionally, streams provide a clean way to integrate multiple systems by treating data changes as a flow of events, allowing derived systems (like caches, search indexes, and analytics platforms) to stay consistently updated with the source of truth without complex synchronization issues like dual writes.

3. **Understand how streams work**  
   Streams work by having producers generate events and append them to a log or send them through a messaging system, while consumers read and process these events, often maintaining state or producing new derived streams. In log-based systems (like Kafka), events are stored durably and ordered within partitions, and consumers track their progress using offsets, allowing them to replay or reprocess data if needed. Stream processing systems then continuously transform, aggregate, or join these event streams to produce outputs such as updated databases, analytics results, or downstream event streams, all while handling challenges like ordering, fault tolerance, and time semantics.

## Chapter 12

This chapter argues that the future of data systems lies in better data integration through dataflow architectures, where multiple specialized tools (databases, caches, search indexes, analytics systems) are combined using event logs and derived data rather than tightly coupled systems or distributed transactions. It emphasizes using batch and stream processing together to maintain and evolve derived datasets, and advocates for unbundling databases into modular components connected by reliable data pipelines. The author highlights a shift toward asynchronous, log-based systems that improve scalability, fault tolerance, and flexibility, while also stressing the importance of correctness and integrity through techniques like idempotence, end-to-end guarantees, and deterministic processing. Ultimately, the chapter envisions applications built around continuous data flows—extending even to clients—where state changes propagate in real time, enabling more robust, evolvable, and maintainable systems.
