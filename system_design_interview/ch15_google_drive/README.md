# Design Google drive

## Step 1: Understand the Problem and Establish Design Scope (3–10 minutes)

We are designing a cloud storage system like Google Drive that allows users to upload, download, sync, and share files across devices. Core features include file storage, synchronization across multiple devices, version history, and notifications on changes. We assume support for all file types, strong reliability (no data loss), and encryption for security. With ~10M daily users and large storage needs (hundreds of petabytes), the system must be highly scalable, available, and bandwidth-efficient. Key concerns include fast sync speed, minimizing redundant data transfer, and maintaining consistency across devices.

---

## Step 2: Propose High-Level Design and Get Buy-In (10–15 minutes)

At a high level, the system consists of clients (web/mobile), API servers, metadata database, and cloud storage (e.g., S3). Files are split into smaller blocks and stored in cloud storage, while metadata (file structure, versions, block references) is stored separately in a database. A load balancer distributes traffic across API servers, and a notification service keeps clients in sync when changes occur. As shown in the diagram on page 8, the architecture separates compute (API servers), storage (cloud storage), and metadata for scalability and fault isolation. This design evolves from a single server into a distributed system with replication and sharding to handle scale and reliability.

---

## Step 3: Design Deep Dive (10–25 minutes)

The system uses block-level storage where files are split into chunks (e.g., 4MB), compressed, encrypted, and stored independently. This enables delta sync, meaning only modified blocks are uploaded, saving bandwidth. The upload flow involves sending metadata and file blocks in parallel, with block servers handling chunking and cloud storage persisting data, as illustrated in the sequence diagram on page 15. For downloads, clients receive change notifications, fetch updated metadata, and reconstruct files from blocks. A notification service (using long polling) ensures real-time sync across devices. Strong consistency is maintained via careful cache invalidation and database guarantees. Storage optimization techniques like deduplication, version limits, and cold storage reduce costs, while fault tolerance is achieved through replication, retries, and failover mechanisms.

---

## Step 4: Wrap Up (3–5 minutes)

In summary, the design focuses on efficient file storage and synchronization using block-level storage, metadata separation, and a notification-driven sync mechanism. It balances performance (delta sync, compression), reliability (replication, strong consistency), and scalability (sharding, stateless services). Additional improvements could include optimizing client-side uploads, enhancing real-time collaboration, or introducing a dedicated presence service. Overall, the system demonstrates how to build a robust, scalable, and user-friendly distributed storage platform.

---