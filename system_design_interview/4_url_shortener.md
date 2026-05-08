# Design a URL Shortener

## What is a URL Shortener?
A URL shortener is a service that converts a long URL into a shorter URL.
When users click the short URL, they are redirected to the original long URL.

---

## architecture
1. The client sends requests to create short URLs or access existing short URLs.
2. The load balancer distributes incoming requests across multiple web servers.
3. The web servers process URL shortening and URL redirection requests
4. The cache stores frequently accessed `<shortURL, longURL>` mappings for fast retrieval.
5. The ID service generates unique IDs used to create short URLs.
6. The database permanently stores the mapping between short URLs and long URLs.


---

## URL Shortening Flow
The **URL Shortening Flow** happens when a user submits a long URL.

1. Receive long URL
2. Check if already exists
3. If exists → return existing short URL
4. Else generate unique ID
5. Store in DB

---

## URL Redirect Flow
The **URL Redirect Flow** happens when a user clicks a short URL.

1. User clicks the short URL
2. Request goes to the Load Balancer
3. Load Balancer forwards the request to Web Servers
4. Web Server checks the Cache:
   - If found → return the long URL immediately
   - If not found → query the Database
5. Database returns the original long URL
6. User is redirected to the original URL