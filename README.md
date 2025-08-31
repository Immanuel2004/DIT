# Dynamic Impact Tool

The **Dynamic Impact Tool** is an AI-powered Streamlit application designed to help you interactively explore, compare, and understand datasets. It uses LLMs (Groq/Ollama) to generate insights, suggest visualizations, and even chat with your data.

---

## Features

### Upload & Insights

- Upload CSV, Excel, or JSON datasets via file or file path
- Preview a sample of the dataset
- Clean data automatically
- AI-selected important columns
- Manual chart creation with dropdown controls
- Insight suggestions from AI
- Chat with your dataset

### Compare Datasets

- Upload two datasets for side-by-side or overlay comparison
- AI + user column selection for each dataset
- Visualize comparisons (bar, line, scatter)
- AI-generated comparison insights
- Ask comparison-based questions to the AI

### Summary & Export

- Full summary of AI-generated insights and charts
- Export insights and visuals as:
  - PDF report
  - PPTX presentation
- Includes user chat history, chart metadata, and more

## Installation

### Option 1: Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/dynamic-impact-tool.git
cd dynamic-impact-tool
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

GROQ_API_KEY=your_groq_key

### Option 2: Docker Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/dynamic-impact-tool.git
cd dynamic-impact-tool
```

### 2. Build and Run with Docker Compose

```bash
docker compose up --build
```

This will:
- Build the application container
- Start the required services (MongoDB, MySQL)
- Run the application on http://localhost:8501

### Environment Variables

The following environment variables are configured in docker-compose.yml:
- MONGO_URI: MongoDB connection string
- DB_HOST: MySQL host
- DB_USER: Database username
- DB_PASSWORD: Database password
- DB_NAME: Database name
- GROQ_API_KEY: Your Groq API key

# Running the App

```bash
streamlit run app.py
```
