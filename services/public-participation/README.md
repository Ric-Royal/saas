# Public-Participation C.I.V.I.L.B.O.T - Citizens’ Intelligent Virtual Information Liaison Bot for Organizing Transparency

![Project Logo]([https://github.com/Ric-Royal/Public-Participation/blob/main/logo.png]) *(Replace with your project logo if available)*

This project aims to enhance public awareness of legislative processes by creating an intelligent WhatsApp assistant capable of fetching, processing, and delivering legislative information. The pipeline includes data scraping, text extraction from PDF files, data storage in a PostgreSQL database, and integrating a Knowledge Graph for advanced querying. Additionally, a Retrieval-Augmented Generation (RAG) system powered by Ollama is developed to handle AI-driven responses. Finally, a WhatsApp bot interfaces with the public via Twilio's API.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
  - [5. Set Up PostgreSQL and Alembic](#5-set-up-postgresql-and-alembic)
  - [6. Scrape Data and Process PDFs](#6-scrape-data-and-process-pdfs)
  - [7. Transfer Data to Knowledge Graph](#7-transfer-data-to-knowledge-graph)
  - [8. Set Up RAG System](#8-set-up-rag-system)
  - [9. Run WhatsApp Bot](#9-run-whatsapp-bot)
- [Running the Application](#running-the-application)
- [Usage](#usage)
  - [Querying Bills on WhatsApp](#querying-bills-on-whatsapp)
  - [Sending a List of Bills](#sending-a-list-of-bills)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

The **Public-Participation** project uses a combination of web scraping, natural language processing (NLP), and AI to assist in public interaction with legislative processes. The project pipeline starts with scraping and extracting data from bill documents, followed by storing the data in a PostgreSQL database, transferring it into a Neo4j Knowledge Graph, and leveraging Ollama AI to generate responses. The system is accessible via WhatsApp, allowing users to query bills and receive detailed information directly.

## Features

- **Data Scraping:** Scrape bill documents from various sources.
- **PDF Processing:** Extract and clean text from bill PDFs.
- **Database Storage:** Store extracted information in a PostgreSQL database.
- **Knowledge Graph:** Transfer data into Neo4j for structured queries.
- **AI-Powered Responses:** Use Ollama AI in a RAG system to generate intelligent responses.
- **WhatsApp Integration:** Enable user interaction via WhatsApp using Twilio’s API.
- **Logging:** Comprehensive logging for debugging and auditing.

## Architecture

![Architecture Diagram](path/to/architecture_diagram.png) *(Replace with your architecture diagram if available)*

1. **Data Scraping:** Scrapes legislative documents from online sources.
2. **Text Extraction:** Extracts relevant information from bill PDFs.
3. **PostgreSQL Database:** Stores extracted data.
4. **Neo4j Knowledge Graph:** Populates a graph-based database with legislative information.
5. **RAG System:** Uses Neo4j and Ollama to generate intelligent responses.
6. **Twilio WhatsApp API:** Enables interaction with users via WhatsApp messages.

## Directory Structure

```
Public-Participation/
├── config/
│   ├── .env
│   └── alembic.ini
├── data/
│   ├── bills_pdfs/                   # Raw bill PDFs
│   ├── processed_bills/               # Processed bill data
│   └── bills.db                       # SQLite backup of bills data
├── logs/                              # Log files
│   ├── ai_model.log
│   ├── app.log
│   ├── database_setup.log
│   ├── pdf_processor.log
│   ├── verify_bills.log
│   └── whatsapp_bot.log
├── migrations/                        # Alembic migrations for PostgreSQL
├── modules/
│   ├── ai_model.py                    # Ollama AI model script
│   ├── knowledge_graph.py             # Neo4j Knowledge Graph interaction
│   └── rag_system.py                  # RAG system implementation
├── scripts/
│   ├── database_setup.py              # Database schema setup
│   ├── pdf_processor.py               # PDF text extraction and processing
│   ├── scraper.py                     # Web scraping script
│   ├── verify_bills.py                # Verifies bill data accuracy
│   └── whatsapp_bot.py                # WhatsApp bot implementation
├── tests/                             # Unit tests
│   ├── test_ai_model.py
│   ├── test_search_bills.py
│   └── test_whatsapp.py
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
└── .gitignore                         # Ignored files
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Public-Participation.git
cd Public-Participation
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # Activate the environment
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Set up environment variables in the `config/.env` file.

```dotenv
# PostgreSQL configuration
POSTGRES_DB=public_participation
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Neo4j configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password

# Twilio configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+your_twilio_whatsapp_number

# Ollama configuration
OLLAMA_API_KEY=your_ollama_api_key
```

### 5. Set Up PostgreSQL and Alembic

1. **Create the PostgreSQL Database:**

   ```bash
   psql -U your_user -c "CREATE DATABASE public_participation;"
   ```

2. **Run Alembic Migrations:**

   ```bash
   alembic upgrade head
   ```
   ```bash
   alembic -c config/alembic.ini upgrade head
   ```

   This will set up the database schema according to the latest migration scripts.

### 6. Scrape Data and Process PDFs

Run the following scripts to scrape legislative data and process PDF files:

```bash
# Scrape data from external sources
python scripts/scraper.py

# Process PDF files and extract text
python scripts/pdf_processor.py
```

### 7. Transfer Data to Knowledge Graph

Once the PostgreSQL database is populated, transfer the data into the Neo4j Knowledge Graph.

```bash
python scripts/database_setup.py
```

```bash
python scripts/knowledge_graph.py
```

This will transfer bill data from the PostgreSQL database to Neo4j, creating nodes and relationships for advanced querying.

### 8. Set Up RAG System

Run the RAG system that combines Neo4j knowledge with Ollama AI for intelligent responses:

```bash
python modules/rag_system.py
```

### 9. Run WhatsApp Bot

1. **Start ngrok to Expose Flask Server:**

   ```bash
   ngrok http 5000
   ```

2. **Run WhatsApp Bot:**

   ```bash
   python scripts/whatsapp_bot.py
   ```

## Running the Application

The entire pipeline can be run by executing `main_phase1.py`, `ai_model.py`, and `whatsapp_bot.py` which ties together data scraping, processing, storage, and knowledge transfer. Run the following command to kick off the process:

```bash
python scripts/main_phase1.py
```
```bash
python scripts/ai_model.py
```
```bash
python scripts/whatsapp_bot.py
```

This will:

- Scrape bill data.
- Process PDF files.
- Store data in PostgreSQL.
- Transfer data to the Neo4j Knowledge Graph.
- Set up the RAG system.
- Start the WhatsApp bot for user interactions.

## Usage

### Querying Bills on WhatsApp

Once the WhatsApp bot is running, users can send messages to query bills.

Example prompt:

```
Can you provide a list of bills in Kenya?
```

The assistant will respond with a list of bills grouped by year.

### Sending a List of Bills

To retrieve a detailed list of bills:

```
Tell me about the Kenya Revenue Authority Amendment Bill 2024.
```

The assistant will provide detailed information about the bill, including title and description.

## Logging

Logs are generated for each module and stored in the `logs/` directory. This includes logs for the AI model, database setup, PDF processing, and WhatsApp interactions.

## Troubleshooting

### Common Issues

1. **Webhook Not Reaching Flask App:**
   - Ensure ngrok is running and the URL is correctly set in Twilio’s webhook configuration.

2. **Duplicate Bills in Responses:**
   - Verify that each bill is uniquely represented in Neo4j, and ensure data integrity in PostgreSQL.

3. **Connection Issues:**


   - Ensure PostgreSQL and Neo4j credentials are correct in the `.env` file.

### Steps to Resolve

1. **Review Logs:** Check log files for any errors.
2. **Test Components Individually:** Run unit tests in the `tests/` directory.
3. **Validate Environment:** Ensure that PostgreSQL, Neo4j, and Twilio are correctly set up and accessible.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Push your changes and open a pull request.



## Acknowledgements

- [Twilio](https://www.twilio.com/) for the WhatsApp API.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Neo4j](https://neo4j.com/) for the knowledge graph database.
- [Ollama](https://ollama.com/) for AI model integration.
