# Project Overview: OSINT Intelligence System

## 1. Core Purpose & Workflow
The system is an intelligence pipeline designed to collect, analyze, and report on publicly available information regarding individuals and organizations (initially focused on the Brisbane region). The workflow follows a three-stage process:

*   **Gathering**: A scraping engine utilizing Playwright captures raw data from various web sources.
*   **Processing**: Raw content is cleaned of HTML noise before being passed to an LLM (via Ollama) for targeted analysis.
*   **Reporting**: The system structures the final output into formal, actionable intelligence reports.

## 2. Technical Architecture & Components
The project leverages a modular architecture designed for scalability and security:

- **Backend Layer (`backend/`)**: Built with FastAPI; manages API routes and core application logic.
- **Intelligence Engine (LLM)**: Utilizes local LLMs via Ollama to process data privately on Windows hardware, ensuring sensitive information remains internal.
- **Scraping & Discovery Module (`scraping/`)**: Employs Playwright for navigating complex web structures while implementing "human-like" behavior and rotation of identifiers to bypass anti-bot measures.
- **Data Management Layer (`database/`)**: Utilizes SQLAlchemy for structured storage, ensuring data integrity across different investigation threads.
- **Security & Connectivity**: Integrated with Tailscale for secure remote access; includes a "Burn" mechanism to isolate session data—ensuring that information from one case never leaks into another.

## 3. Core Features and Design Choices
*   **Multi-Stage Discovery (Search > Filter > Extract)**: Instead of direct scraping, the system employs an intelligent discovery phase where search results are filtered by logic/LLM to identify high-value targets before deep extraction occurs.
*   **Geo-fencing**: Logic is prioritized for local and regional data relevance.
*   **Privacy & Safety**: By utilizing locally hosted models (Ollama), sensitive information remains within the user's infrastructure during analysis.

## 4. Project Structure Overview
The project follows a modular structure to separate concerns:
- `backend/`: Core API logic and routes.
- `core/`: Configuration, settings, and shared modules.
- `scraping/`: Playwright implementation for navigation and data extraction.
- `services/`: High-level business logic (e.g., the "Burn" functionality).
- `database/`: SQLAlchemy models and schema definitions.
- `utils/`: Common helper functions across all projects.

--- 
*Last Updated: 2026-10-21*
