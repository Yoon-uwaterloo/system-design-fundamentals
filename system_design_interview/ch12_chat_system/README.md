# Design a chat system

## Step 1: Understand the Problem and Establish Design Scope (3–10 minutes)

Start by clarifying requirements: we are designing a chat system that supports both one-on-one and small group conversations (e.g., up to ~100 users per group) with around tens of millions of daily active users. Core features include real-time text messaging, low delivery latency, online/offline presence indicators, multi-device synchronization, and push notifications, with messages stored permanently. We assume text-only messages (bounded size), no strict requirement for end-to-end encryption initially, and both mobile and web clients. It’s important to confirm scale, group size limits, and whether features like attachments or encryption are in scope, since these significantly impact design decisions.

---

## Step 2: Propose High-Level Design and Get Buy-In (10–15 minutes)

The user connects to the system in two ways: via HTTP requests that go through a load balancer to the API servers (for actions like login, signup, and profile updates), and via a persistent WebSocket (WS) connection directly to the real-time service. Within the real-time service, chat servers handle sending and receiving messages instantly, while presence servers track whether users are online or offline. When a message is sent, it flows through the chat servers and is stored in the distributed key-value (KV) store for persistence, ensuring chat history is saved. If the recipient is offline, the notification servers trigger push notifications, and when the user reconnects, their messages are retrieved from the KV store so they can see the full conversation history.

---

## Step 3: Design Deep Dive (10–25 minutes)

In the deep dive, focus on critical components like message flow, storage, synchronization, and presence. When a user sends a message, it is assigned a unique, time-ordered ID, stored in a key-value database, and delivered to recipients via chat servers; if recipients are offline, messages are queued and push notifications are sent. Multi-device sync is handled by tracking the latest message ID seen on each device, allowing efficient fetching of new messages. For group chat, messages are often duplicated into each recipient’s queue for simplicity (efficient for small groups). Presence is managed via heartbeat signals over WebSocket connections, ensuring accurate online/offline status without frequent flickering. Scalability is achieved through horizontal scaling of chat servers and partitioning of message data.

---

## Step 4: Wrap Up (3–5 minutes)

To conclude, the system leverages WebSocket for real-time communication, separates stateless and stateful services for scalability, and uses a key-value store for efficient message storage and retrieval. Key trade-offs include simplicity versus scalability in group messaging and consistency versus latency in message delivery. Potential improvements include adding media support, implementing end-to-end encryption, optimizing caching, and improving global latency with geo-distributed systems. Handling failures (e.g., server crashes, message retries) and ensuring high availability are also important considerations to mention as extensions in an interview setting.

---