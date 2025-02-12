# SpaceCrew - Intelligent Space Data Retrieval Agent

## Overview

SpaceCrew is an AI-powered agent system designed to analyze user queries related to space, fetch relevant data from APIs, and generate engaging summaries. Built using **CrewAI**, **LangChain**, and **Google Gemini AI**, SpaceCrew automates the retrieval and summarization of space-related information from sources such as NASA APIs.

## Features

- **Intelligent Query Analysis**: Determines the best API endpoint based on user queries.
- **Automated Data Fetching**: Retrieves data from NASA and space-related APIs.
- **Context-Aware Summarization**: Generates user-friendly summaries tailored to different knowledge levels.
- **Memory-Based Context Handling**: Maintains conversation history for better responses.

## Technologies Used

- **Python**
- **CrewAI**
- **LangChain**
- **Google Gemini AI**
- **NASA APIs**
- **Pydantic**
- **Logging**

## Installation

Ensure you have **Python 3.8+** installed.

1. Clone the repository:

   ```bash
   git clone https://github.com/shamas/spacecrew.git
   cd spacecrew
   ```

2. Install dependencies using UV:

   ```bash
   uv install
   ```

3. Set up your `.env` file:

   ```
   GEMINI_API_KEY=your_google_gemini_api_key
   NASA_API_KEY=your NASA_api_key
   ```

## Usage

Run the main script to interact with SpaceCrew:

```bash
uv run main
```

Example query:

```bash
What is today's astronomy picture of the day?
```

### Modules & Components

#### **1. SpaceCrew Class**

The `SpaceCrew` class initializes:

- **LLM (Google Gemini AI)**
- **API Tools** (NASA APOD, Open Notify, Launch Library)
- **Memory Manager** (to track conversation history)

#### **2. Agents**

| Agent               | Role & Responsibilities                                   |
| ------------------- | --------------------------------------------------------- |
| **Query Analyzer**  | Determines the best API and parameters for a given query. |
| **Data Fetcher**    | Retrieves and validates data from space-related APIs.     |
| **Data Summarizer** | Creates context-aware, engaging summaries.                |

#### **3. Workflow (Tasks)**

1. **Analyze the Query** → Identify relevant APIs & parameters.
2. **Fetch Data** → Retrieve space data using API calls.
3. **Summarize Data** → Generate an easy-to-understand summary.

## Example Output

```
==================================================
Query: What is today's astronomy picture of the day?
User Type: general
==================================================
Response:
The Astronomy Picture of the Day is [image_link]. Description: [summary]
```

## Debugging & Logging

- All logs are stored in `logging.INFO` mode.
- Errors related to missing parameters (`NoneType`) can be traced in the logs.

## Contributions

Feel free to submit issues and pull requests to improve SpaceCrew!



