This project is an OSINT Intelligence System designed to collect, analyze, and report on publicly available information regarding individuals and organizations, with an initial focus on a specific local region (Brisbane).

Here is my understanding of the project based on the files and structure:

1. Core Purpose & Workflow

The system acts as an intelligence pipeline that:

Gathers: Uses a scraping engine (Playwright) to collect raw data from the web.
Processes: Cleans the raw data (removing HTML noise) before passing it to a local Large Language Model (Ollama) for analysis.
Reports: Structures the LLM output into formal reports.
Manages: Provides a "Burn" mechanism to isolate and delete session-specific data, ensuring that data from different investigations remains separated.

2. Technical Architecture

Backend: Built with FastAPI (in backend/), providing the core API logic.
Intelligence/AI: Utilizes local LLMs via Ollama to process data privately on a Windows machine.
Scraping Layer: Uses Playwright (in scraping/) with features like User-Agent rotation and "human-like" behavior to bypass anti-bot measures.
Data Management: Uses SQLAlchemy for a structured database (in database/).
Network: Integrated with Tailscale for secure remote access.

3. Key Features & Design Choices

Geo-fencing: Prioritizes local, state, and federal data for the target region.
Data Integrity: Uses a "Query-First" architecture to keep search parameters and results distinct.
Privacy/Safety: Employs local LLMs to process sensitive information and includes a "Burn" feature for secure data disposal.
Frontend: Planned for native iOS and macOS applications.

4. Project Structure Overview

backend/: API routes and core application logic.
core/: Configuration, settings, and shared logic.
scraping/: Logic for navigating and extracting data from the web.
services/: Business logic, including the "burn" functionality.
utils/: Helper functions used across the project.
database/: Database models and schema definitions.

______________________________________________________________________________________________________________________________

## Appendage

Scraping Notes

Ok, this i where im not familiar with Playwirght or how web scraping works

In my head you have some strings - name, location, occupations, other query items - and the scraper needs to use those to begin searches.

These searches are the things i have no experience with, I can see the #sym:fetch_page_content function is deisgned to accept a URL string - but that then sounds the function just wants to load a web page straight away an scrape the data from it

I think there is some prelimary work that needs to be done first, and I think the scraper needs to be complexify slighty. I think it should be making generic searches using browsers or other mechanism - then when it discovers URLs that possibly relate to the subject the scraped can THEN start to load and scrape specific websites.

The job of the scraper needs to be reasonably intelligent here - i want it to:

peform preliminary searches to find more data sources(URLs for emample) that could be potentially be of a higher resolution of data about the subject
Once that prelimary compilation is done, then perform more refined scraping of those sources
The scraping engine (or possibly via consultation mid process with the LLM) needs to perform step 1 - then with the results of that, perform scrapes of potentially higher resolution data on the subject

10:03 AM
Your observation is spot on. At the moment, fetch_page_content is a low-level "mechanical" function: it takes a specific URL and grabs the text. To move from a "user query" (e.g., "Find info on John Doe in Brisbane") to "meaningful data," we need an orchestration layer between the backend and the ScrapingEngine.

To address your requirements for a more "intelligent" and multi-stage process, we should evolve the system with the following architecture:

1. The "Discovery" Phase (Step 1)
Instead of jumping straight to scraping a page, we introduce a Discovery step.

Input: The SearchRequest (name, location, etc.).
Process: The ScrapingEngine (or a new DiscoveryService) performs a broad search (e.g., via a search engine API or by navigating to search results pages).
The "Intelligence" Component: This is where the LLM (via analyzer) becomes crucial. Instead of just gathering every link, the LLM can analyze the search results to identify "High-Value" links—those that are likely to contain the specific types of information (social media, legal records, etc.) that we want.
2. The "Extraction" Phase (Step 2)
Once we have a list of "high-value" URLs:

Process: The ScrapingEngine then performs the "refined scraping" you mentioned. It visits these specific pages, handles the navigation, and extracts the raw content.
Outcome: This results in a high-quality, filtered dataset.
3. The "Analysis" Phase
Finally, this rich, multi-sourced data is passed to the analyzer to produce the final report.

Proposed Implementation Plan:
I suggest we refine the code in the following stages:

Refine ScrapingEngine: Add a method for Search/Discovery. Instead of just fetch_page_content(url), we'll have a method that handles the logic of "Search 
→
→ Filter 
→
→ Identify URLs."
Introduce a "Coordinator" or "Pipeline": We can update main.py or a new manager class to orchestrate this flow.
Route: search 
→
→ Discovery Step (Search + LLM Filtering) 
→
→ Extraction Step (Iterative Scraping) 
→
→ Analysis Step (LLM Summary).
Refine the "Intelligence": We will use the analyzer not just for the final report, but as a "decision-making" tool during the discovery phase to decide which links are worth a "deep dive."
Does this "Discovery 
→
→ Filter 
→
→ Extract" approach align with what you had in mind for the "intelligent" scraper? If so, I can begin by expanding the ScrapingEngine to handle this multi-step logic.