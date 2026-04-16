# Design a unique ID generator in distributed systems

## Step 1: Understand the Problem and Establish Design Scope (3–10 minutes)

To begin, I would clarify requirements such as ensuring IDs are globally unique, numeric, fit within 64 bits, and are sortable by time. I would confirm the expected scale (e.g., 10,000+ IDs per second), whether IDs need to be strictly sequential or just roughly time-ordered, and whether the system spans multiple data centers. It’s also important to understand constraints like latency, availability, and fault tolerance, since this is a distributed system where coordination between nodes can become a bottleneck.

---

## Step 2: Propose High-Level Design and Get Buy-In (10–15 minutes)

I would present several approaches including multi-master auto-increment, UUIDs, and a centralized ticket server, discussing their trade-offs. Multi-master replication struggles with ordering and scalability, UUIDs are large and not time-ordered, and ticket servers introduce a single point of failure. Based on the requirements, I would propose a Snowflake-style ID generator, where each machine independently generates IDs using a combination of timestamp and machine-specific information, achieving scalability and uniqueness without centralized coordination.

---

## Step 3: Design Deep Dive (10–25 minutes)

In the Snowflake design, each 64-bit ID is composed of multiple parts: a timestamp, datacenter ID, machine ID, and sequence number. The timestamp ensures IDs are time-ordered, while datacenter and machine IDs guarantee uniqueness across distributed nodes. The sequence number handles multiple IDs generated within the same millisecond. I would also address edge cases such as clock drift (using NTP or fallback strategies), machine ID assignment, and ensuring no collisions during restarts. The system should be highly available and capable of generating thousands of IDs per second per node.

---

## Step 4: Wrap Up (3–5 minutes)

To conclude, I would summarize that the Snowflake approach meets all key requirements—uniqueness, scalability, ordering, and efficiency—making it well-suited for distributed systems. I would briefly mention trade-offs and extensions, such as adjusting bit allocation for different workloads, handling clock synchronization issues, and ensuring high availability. If time permits, I would discuss monitoring, testing strategies, and how the system can evolve as scale increases.