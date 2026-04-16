# Design a Key-Value Store (System Design)

## 1) What is a Key-Value Store?
A key-value store is a non-relational database where each piece of data is stored as a unique key paired with a value, and the value can only be accessed using that key. The key is typically a short identifier (either plain text or hashed), and the value can be anything like a string, object, or list. As shown in the document (page 1), examples include mappings like `145 → john` and `147 → bob`, and the system mainly supports two operations: inserting data using `put(key, value)` and retrieving data using `get(key)`.

---

## 2) Design Goals
A well-designed distributed key-value store should be able to handle large amounts of data efficiently while maintaining high availability and low latency. It must scale horizontally as demand grows, support automatic addition and removal of servers, and provide tunable consistency so the system can balance correctness versus performance depending on use case requirements. These goals ensure the system remains fast, reliable, and flexible under heavy load and failures.

---

## 3) CAP Theorem
The CAP theorem states that a distributed system can only guarantee two out of three properties: consistency, availability, and partition tolerance. Since network partitions are unavoidable in real systems, partition tolerance is required, meaning the system must choose between consistency and availability. A CP system prioritizes consistency and may reject requests during failures to avoid stale data, while an AP system prioritizes availability and continues serving requests even if some responses are outdated. This tradeoff is fundamental in designing distributed key-value stores.

---

## 4) High-Level Architecture
In a distributed key-value store, clients interact with the system through simple APIs such as `get` and `put`, and their requests are routed to a coordinator node that acts as a proxy. The system distributes data across multiple nodes using consistent hashing, replicates data across several machines for reliability, and avoids any single point of failure by making every node capable of handling requests. This decentralized design allows the system to scale easily and remain resilient to node failures.

---

## 5) Data Partitioning
To handle large datasets, data is split across multiple servers using a technique called consistent hashing, where both servers and keys are mapped onto a logical ring. Each key is assigned to the nearest server in a clockwise direction, which ensures even distribution of data and minimizes the amount of data that needs to move when servers are added or removed. This approach enables automatic scaling and efficient load balancing across the system.

---

## 6) Data Replication
To improve reliability and availability, each key-value pair is replicated across multiple servers, typically `N` replicas, which are selected by walking clockwise on the hash ring from the key’s position. This ensures that even if some nodes fail, the data remains accessible from other replicas. Additionally, replicas are often placed in different data centers to protect against large-scale failures such as power outages or network disruptions.

---

## 7) Consistency (Quorum System)
Consistency in a distributed key-value store is managed using a quorum system defined by three parameters: `N` (number of replicas), `W` (write quorum), and `R` (read quorum). A write is considered successful once `W` replicas acknowledge it, and a read is successful after receiving responses from `R` replicas. The system can guarantee strong consistency when `W + R > N` because at least one replica will overlap between reads and writes, but lower values of `W` or `R` can improve latency at the cost of weaker consistency.

---

## 8) Consistency Models
Different systems adopt different consistency models depending on their priorities, ranging from strong consistency, where every read returns the most recent write, to weak consistency, where stale reads are possible, and eventual consistency, where all replicas converge to the same state over time. Most large-scale systems like Dynamo and Cassandra use eventual consistency because it provides better availability and performance while still ensuring data correctness in the long run.

---

## 9) Conflict Resolution (Versioning)
Because data is replicated across multiple nodes, concurrent updates can lead to conflicting versions of the same data, which must be resolved. This is handled using versioning techniques such as vector clocks, where each version of data is tagged with metadata indicating its history. By comparing these version histories, the system can determine whether one version supersedes another or if a conflict exists, in which case the conflict must be resolved either automatically or by the client.

---

## 10) Failure Handling
Failure handling is critical in distributed systems and involves detecting failures, maintaining availability, and ensuring data consistency. Failures are typically detected using a gossip protocol where nodes exchange heartbeat information to identify down nodes, and once detected, mechanisms like sloppy quorum allow the system to continue operating by using healthy nodes. Temporary failures are handled with hinted handoff, where updates are stored temporarily and synchronized later, while permanent failures are addressed using anti-entropy mechanisms like Merkle trees to efficiently detect and repair inconsistencies between replicas. Additionally, data is replicated across multiple data centers so the system can continue functioning even if an entire data center goes offline.

---

## 11) Write Path
When a write request is processed, it is first recorded in a commit log on disk to ensure durability, then stored in an in-memory cache for fast access, and eventually flushed to disk as an SSTable once the memory reaches a certain threshold. This design ensures both durability and high performance by combining fast memory operations with reliable disk storage.

---

## 12) Read Path
For read operations, the system first checks if the requested data is available in memory cache, which provides the fastest response. If the data is not in memory, the system uses a Bloom filter to quickly determine which SSTable might contain the key, retrieves the data from disk, and returns it to the client. This approach minimizes disk reads and improves overall read efficiency.

---

## 13) Final Summary
A distributed key-value store is a scalable and fault-tolerant system that uses consistent hashing to distribute data, replication to ensure availability, quorum-based techniques to balance consistency and latency, and mechanisms like vector clocks and Merkle trees to resolve conflicts and maintain data integrity, all while optimizing performance through caching and efficient storage structures.