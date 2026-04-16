# System Design Interview
## An Insider's Guide
### by Alex Xu

Tips
* Functional Requirements:
| Component            | Description                                                                 | Example (Ride-Sharing App)                  |
|---------------------|-----------------------------------------------------------------------------|---------------------------------------------|
| Feature / Function  | The capability or action the system provides                                | Request a ride                              |
| Actor / User        | Who interacts with the system                                               | Rider                                       |
| Input               | Data provided by the user or another system                                 | Pickup & drop-off location                  |
| Processing / Logic  | How the system handles the input                                            | Match rider with nearby driver              |
| Output              | Result returned to the user or system                                       | Driver details + ETA                        |
| Business Rules      | Constraints or rules governing the behavior                                 | Surge pricing during peak hours             |
| Edge Cases          | Handling of unusual or failure scenarios                                    | No drivers available                        |

* Non-Functional Requirements:
| Category        | Description                  |
|----------------|------------------------------|
| Performance     | Latency, throughput          |
| Scalability     | Handle growth                |
| Availability    | Uptime, fault tolerance      |
| Reliability     | Consistency, correctness     |
| Security        | Auth, data protection        |
| Maintainability | Easy to update               |
| Cost            | Infra efficiency             |