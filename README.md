# SmartFind — AI-Powered Product Search Engine

SmartFind is a full-stack AI product search engine that uses RAG (Retrieval Augmented Generation) with FAISS vector search and Google Gemini to deliver natural language product discovery.

## Tech Stack

**Backend**
- Python + Flask
- FAISS (vector similarity search)
- Sentence Transformers (all-MiniLM-L6-v2)
- Google Gemini 1.5 Flash (AI summaries)

**Frontend**
- Vanilla HTML/CSS/JS
- No frameworks — clean and fast

## Features

- Natural language product search ("budget headphones for gym under 10k")
- Semantic vector search using FAISS and sentence embeddings
- AI-generated summaries via Gemini RAG pipeline
- User authentication (signup/login/guest)
- 40+ products across Electronics, Footwear, Sports, Clothing, Home, Beauty
- Relevance scoring for each result

## How It Works

1. Product descriptions are encoded into vector embeddings using `all-MiniLM-L6-v2`
2. Embeddings are indexed in a FAISS flat inner product index
3. At search time, the query is embedded and compared against all products
4. Top-k matching products are retrieved
5. Retrieved products + query are passed to Gemini for a natural language summary
6. Results and summary are returned to the frontend

## Setup

### 1. Install dependencies

```bash
pip install flask flask-cors google-generativeai faiss-cpu sentence-transformers pandas
```

### 2. Add your Gemini API key

Open `backend/app.py` and replace the API key:

```python
GEMINI_API_KEY = "your_api_key_here"
```

### 3. Start the backend

```bash
cd backend
python app.py
```

Backend runs on `http://localhost:5000`

### 4. Open the frontend

Open `frontend/index.html` in your browser directly, or serve it:

```bash
cd frontend
python -m http.server 3000
```

Then go to `http://localhost:3000`

## Screenshots
<img width="2878" height="1542" alt="image" src="https://github.com/user-attachments/assets/5100209a-206d-493c-841c-1b05d7654201" />
<img width="2850" height="1542" alt="image" src="https://github.com/user-attachments/assets/1e5142a6-a1b7-4179-aaaf-baebed09841c" />
<img width="2849" height="1543" alt="image" src="https://github.com/user-attachments/assets/af591794-6790-4b3a-9435-9b7310936689" />



## Sample Queries

- "noise canceling headphones under 20000"
- "waterproof shoes for trekking"
- "smartwatch with health monitoring and long battery"
- "kitchen appliance for healthy cooking"
- "gaming laptop for students"
- "affordable bluetooth speaker for outdoor use"

## Project Structure

```
SmartFind/
├── backend/
│   ├── app.py           # Flask API server
│   ├── search_engine.py # FAISS + embeddings RAG engine
│   └── products.py      # Product dataset (40+ items)
└── frontend/
    └── index.html       # Complete frontend (single file)
```
