### 1. Requirements & Scope Definition
i) **Define "Geo-fencing" Logic:** Determine how the system will filter results by geography (e.g., by IP address, GPS coordinates, region codes, or specific country domains).

This will start as being a rough, hard-coded geographical size and im going to start with maxiumum size of Brisbane the capital of Queensland. In future the module may have a complex capaicty to take in multiple geo-fenced locations, for MVP we start with 1 at a time.

ii) **Identify Target Data Sources:** List the specific platforms to target (e.g., Social Media (X, LinkedIn), News Aggregators, Forum Scraping, and standard Search Engines).

All major socila media networks and news media networks that operate at a national level for the target area specified.

iii) **Identify "Subject" Types:** Determine the types of subjects (e.g., Individuals, Organizations, or Locations) to tailor the search parameters.

This will mostly be people, but the MVP should be able to cater for organisations, but in the case of organisations geo-fencing can be loosened to a national query.

iv) **Legal & Ethical Guardrails:** Establish a framework for ensuring the tool operates within the Terms of Service (ToS) of targeted platforms and complies with data privacy regulations.

Certainly the MVP should constrain itself to performing inside relevant target local, state and federal guidelines, however the ethical pursuit of data is not a concern. Where a boundary can be pushed, bent or strained - but never broken - to obtain the best, most accurate and timely results possible, then this should be the protocol. Again, though under now circumstances should any law be broken. Where components of the project need to be constructed and desicions about how elegantly ride-the-line so to speak, we talk about that together.

### 2. Architecture & Modular Design

i) **Module 4: Analysis & Synthesis Engine:** An LLM-powered component to process raw, messy data into a structured summary of "publicly available details."

This is mostly constructed, the LLM is you and you are hosted on a powerful windows machine.

ii) - **Module 5: Report Generator:** A module to format the final findings into a readable format (JSON, Markdown, or PDF).

This is trivial work, however what will be a critical component at this stage is a mechanism by which at the touch of a button, i can burn any records generated. The records will be stored seperately based on subject and i will be able to select a subject to burn.

### 3. Proof of Concept (PoC)

i) Successfully automate data retrieval from one specific source (e.g., a specialized search API).

CRUCIAL: We will not be engaging 3rd party querying APIs. I realise in building our own custom engine, it will require safety mechanism to prevent such things as bot checks, rate-limiting etc as much as we can. Any advise on how i can optimise my infrastructure to support this better would be well received.

ii) - **Geo-Filtering Implementation:** Implement the logic to discard results outside the specified perimeter.

Again the purpose of geo fencing was not to discard possible relevant results outside a nominated area - it was in the hope to reduce the load on the scraping/searching API's given - if this idea is under thought or not workable or not needed and we can perform much wider national searches - perfomatively - every time, let me know.

Steps 5 and 6 seem straight forward and can be looked at more closely towards the end of the MVP.

### Technical Specifications & Infrastructure
- **Networking:** Tailscale is already implemented and in use for secure, off-LAN access.
- **Backend:** Python (FastAPI) for the API and orchestration.
- **Scraping:** Playwright (Headless) for interacting with web elements.
- **Database:** PostgreSQL or SQLite (for the "Burn" functionality).
- **LLM Inference:** Local (Ollama) - already in place.
- **Frontend:** Native iOS & Mac apps (User preference).
    - *Note:* While a web-based dashboard is often simpler for cross-platform, a native iOS approach is chosen. Primary blockers for native apps are generally limited to handling complex state transitions and ensuring consistent data mapping from the backend; however, these are manageable given the expertise.
- **Anti-Bot/Rate-Limiting Strategy:** 
    - Implementation of **User-Agent rotation** to simulate various device signatures.
    - Integration of **Proxy rotation** (if required) to mitigate IP-based rate limits.
    - Implementation of **Human-like interactions** (jitter, randomized delays, and non-linear navigation) to minimize detection risk in headless environments.
- **Playwright Evaluation:**
    - *Pros:* Superior handling of modern web elements (Shadow DOM, etc.) and robust automation for complex interactions.
    - *Cons:* Resource intensive (requires browser instances); potential detection via automation flags (requires specific patches/plugins like `playwright-extra` to mitigate); higher complexity in managing "headless" vs "headful" transitions.
