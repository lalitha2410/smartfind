from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import hashlib
import os
from search_engine import get_engine

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = "smartfind_secret_key_2024"
CORS(app)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your-api-key-here")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

users_db = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not name or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    if email in users_db:
        return jsonify({'error': 'Email already registered'}), 409
    users_db[email] = {'name': name, 'email': email, 'password': hash_password(password)}
    session['user'] = {'name': name, 'email': email}
    return jsonify({'message': 'Account created successfully', 'user': {'name': name, 'email': email}}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    user = users_db.get(email)
    if not user or user['password'] != hash_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    session['user'] = {'name': user['name'], 'email': email}
    return jsonify({'message': 'Login successful', 'user': {'name': user['name'], 'email': email}}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/me', methods=['GET'])
def me():
    user = session.get('user')
    if user:
        return jsonify({'user': user}), 200
    return jsonify({'user': None}), 200

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    engine = get_engine()
    results = engine.search(query, top_k=5)
    if not results:
        return jsonify({'results': [], 'summary': 'No products found for your query.'}), 200
    products_context = ""
    for i, p in enumerate(results, 1):
        products_context += f"{i}. {p['name']} by {p['brand']} - Rs.{p['price']} - Rating: {p['rating']}/5\n   {p['description']}\n\n"
    prompt = f"""You are a helpful product recommendation assistant for SmartFind.
A user searched for: "{query}"
Here are the top matching products:
{products_context}
Write a natural, helpful 2-3 sentence summary. Acknowledge what the user is looking for, highlight the best match and why it suits their needs, mention price range if relevant. No bullet points."""
    try:
        response = gemini_model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        summary = f"Found {len(results)} products matching your search for '{query}'."
    return jsonify({'results': results, 'summary': summary, 'query': query}), 200

@app.route('/api/products', methods=['GET'])
def get_all_products():
    engine = get_engine()
    products = engine.products_df.to_dict(orient='records')
    return jsonify({'products': products}), 200

@app.route('/api/categories', methods=['GET'])
def get_categories():
    engine = get_engine()
    categories = engine.products_df['category'].unique().tolist()
    return jsonify({'categories': categories}), 200

if __name__ == '__main__':
    print("Initializing SmartFind search engine...")
    get_engine()
    print("SmartFind is ready!")
    app.run(debug=True, port=5000)
