# Consistent Hashing Notes

## 1) What is Consistent Hashing?
Consistent hashing is a technique used to distribute data across multiple servers such that when servers are added or removed, only a small subset of keys need to be redistributed. Unlike traditional hashing, which can cause widespread data reshuffling, consistent hashing minimizes data movement, making it highly suitable for scalable distributed systems where nodes frequently change.

---

## 2) Consistent Hashing vs Traditional Hashing
Traditional hashing typically uses a formula like `serverIndex = hash(key) % N`, which works well in static environments but fails in distributed systems because when the number of servers changes, almost all keys get remapped, leading to cache invalidation, network spikes, and performance degradation. In contrast, consistent hashing significantly reduces key movement when servers are added or removed, provides better scalability, and achieves more balanced load distribution (especially when enhanced with virtual nodes), making it ideal for dynamic distributed systems.

---

## 3) How Consistent Hashing Works
Consistent hashing works by mapping both servers and keys onto a circular hash ring, where the hash space ranges from `0 → 2^160 - 1` (for example, using SHA-1). Each server is hashed (based on its IP or name) and placed as a point on the ring, and keys are hashed onto the same ring. To assign a key, the system moves clockwise on the ring until it finds the first server, which becomes responsible for that key. When a new server is added, only the keys in the range between the new server and its previous neighbor (anticlockwise) are reassigned, and when a server is removed, its keys are reassigned to the next server clockwise, ensuring minimal redistribution.

---

## 4) Two Issues with Basic Consistent Hashing
Despite its advantages, basic consistent hashing has two main issues: uneven partition sizes and non-uniform key distribution. Because server positions on the ring depend on hash values, some servers may end up owning disproportionately large or small segments of the ring, causing load imbalance, while keys themselves may cluster in certain regions of the ring, leading to some servers being overloaded while others remain underutilized.

---

## 5) Solution: Virtual Nodes (Replicas)
To address these issues, consistent hashing introduces virtual nodes, where each physical server is represented by multiple points on the hash ring instead of just one. For example, a server A might be represented as A1, A2, A3, and similarly for other servers, allowing keys to map to these virtual nodes rather than directly to physical servers. This results in a much more uniform distribution of keys, reduces load variance, and improves fault tolerance, although it introduces a tradeoff in the form of increased memory usage and additional metadata management.

---

## 6) Wrap Up
Consistent hashing distributes data across servers using a hash ring and ensures that only a small fraction of keys move when the system scales, making it highly efficient for dynamic distributed environments. It significantly improves scalability, availability, and load balancing, and is widely used in real-world systems such as distributed databases (like Dynamo and Cassandra), caching systems, load balancers, and CDNs. Overall, consistent hashing is a fundamental building block for designing scalable and resilient distributed systems.