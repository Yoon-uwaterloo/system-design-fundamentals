# 🕸️ Design a Web Crawler

## 📌 What is a Web Crawler

A **web crawler** (robot/spider) is a system that automatically browses the web to collect content (HTML pages, images, PDFs, etc.) for purposes like:

- Search engine indexing  
- Web archiving  
- Data mining  
- Monitoring (e.g., copyright violations)  

---

## 🔄 Core Algorithm

1. Start with seed URLs
2. Download pages
3. Extract links
4. Add new links to queue
5. Repeat

The step-by-step flow on page 8 explains:
1. Add seed URLs
2. Fetch URLs from frontier
3. Resolve DNS & download
4. Parse content
5. Check duplicate content
6. Extract links
7. Filter links
8. Check visited URLs
9. Add new URLs back to frontier

---

## 🧩 Key Design Challenges

### 1. Scalability

- Use distributed workers  
- Partition URL space  

---

### 2. Politeness

- Avoid overloading websites  
- Use per-host queues with delays  

**Approach:**
- Each host → separate queue  
- Each queue → one worker  

---

### 3. Prioritization

Not all pages are equally important:

- Use signals like PageRank, traffic, update frequency  
- Crawl high-value pages first  

---

### 4. Freshness

Web pages change frequently, so recrawling is necessary:

- Recrawl frequently updated pages  
- Prioritize important URLs  