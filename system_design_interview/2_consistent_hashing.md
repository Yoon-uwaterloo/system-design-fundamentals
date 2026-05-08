# Consistent Hashing Notes

## 📌 What is Consistent Hashing

Consistent hashing is a distributed systems technique used to distribute data across multiple servers such that when servers are added or removed, only a small portion of keys need to be remapped.

It is commonly used in:

- Distributed caches
- Databases
- CDNs
- Load balancers

---

## 🔄 Traditional Hashing, Its Problem, and Why We Need Consistent Hashing

Traditional hashing uses:

server index = hash key / mod N

Where:

- N = number of servers

Problem

When the number of servers changes:

- Most keys get remapped
- Massive cache misses occur
- Large data movement happens

Example:

1. System has 4 servers
2. Key is mapped using hash(key) % 4
3. One server goes down
4. Now system uses hash(key) % 3
5. Most keys map to different servers

This creates:

- High network overhead
- Poor scalability
- Increased latency

✅ Consistent hashing minimizes remapping and solves this issue. 

---

## ⚙️ Mechanism

Step-by-Step Working

1. Create a circular hash ring
2. Hash servers onto the ring
3. Hash keys onto the same ring
4. Move clockwise from the key position
5. First server encountered stores the key

Server Addition

When a new server is added:

- Only nearby keys move to the new server
- Remaining keys stay unchanged

Server Removal

When a server is removed:

- Only keys belonging to that server are redistributed

This provides:

- Better scalability
- Minimal data movement
- High availability

---

## 🧩 Virtual Node

Problem Without Virtual Nodes

Servers may get uneven partitions on the ring, causing:

- Load imbalance
- Hotspots
- Uneven traffic distribution

⸻

Solution: Virtual Nodes

A physical server is represented by multiple virtual nodes on the ring.

Benefits

- Better load balancing
- More uniform key distribution
- Reduced hotspots
- Improved fault tolerance

More virtual nodes improve balance but increase metadata overhead.