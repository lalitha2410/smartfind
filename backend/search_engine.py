import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer
from products import get_products

class SmartFindEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.products_df = get_products()
        self.index = None
        self.embeddings = None
        self._build_index()

    def _build_index(self):
        texts = []
        for _, row in self.products_df.iterrows():
            text = f"{row['name']} {row['brand']} {row['category']} {row['description']} price {row['price']} rupees rating {row['rating']}"
            texts.append(text)

        self.embeddings = self.model.encode(texts, show_progress_bar=False)
        self.embeddings = np.array(self.embeddings).astype('float32')

        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)

        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                product = self.products_df.iloc[idx].to_dict()
                product['relevance_score'] = float(score)
                results.append(product)

        return results

engine = None

def get_engine():
    global engine
    if engine is None:
        engine = SmartFindEngine()
    return engine
