import streamlit as st
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

synonym_dict = {
    "laptop": ["notebook", "portable computer", "ultrabook", "chromebook"],
    "microsoft": ["Microsoft", "Surface", "Surface Pro", "Surface Book", "Surface Laptop"],
    "msi": ["MSI", "GF", "GL", "Prestige", "Modern"],
    "intel": ["Intel Core", "Pentium", "Celeron"],
    "amd": ["AMD Ryzen", "Athlon"],
    "ram": ["RAM", "Memory", "DDR5"],
    "color": ["Black", "Silver", "Grey", "Space Grey", "Matte Black", "Blue", "White", "Gold"],
    "battery_life": ["battery backup", "extended battery"],
    "touchscreen": ["touch display", "interactive screen", "multi-touch", "fingerprint reader"],
    "graphics": ["Integrated Graphics", "Discrete Graphics"],
    "operating_system": ["Windows", "macOS", "Linux", "Chrome OS", "Ubuntu", "Fedora"],
    "connectivity": ["Wi-Fi", "Bluetooth", "USB-C", "Thunderbolt", "HDMI", "Ethernet", "4G LTE", "5G"],
    "audio": ["Dolby Audio", "stereo speakers", "Bang & Olufsen", "Harman Kardon"],
    "build": ["metal body", "plastic body", "aluminum chassis", "carbon fiber"],
    "weight": ["lightweight", "portable", "thin and light", "ultra-light"]
}

# Create a mapping function for the synonyms
def map_synonyms(query):
    words = query.lower().split()
    expanded_query = []
    for word in words:
        # Add the word itself
        expanded_query.append(word)
        # Check if the word has synonyms in the dictionary
        if word in synonym_dict:
            expanded_query.extend(synonym_dict[word])
    return ' '.join(expanded_query)

# Function to perform semantic search using BERT
def semantic_search_bert(data, query, top_n=10):
    try:
        # Load pre-trained BERT model and tokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')

        # Map synonyms in the query
        expanded_query = map_synonyms(query)

        # Generate BERT embedding for the query
        encoded_input = tokenizer(expanded_query, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = model(**encoded_input)

        # Extract the CLS token's embedding as the query embedding
        query_embedding = model_output.last_hidden_state[:, 0, :].squeeze().numpy()  # 2D array

        # Ensure the product embeddings are in the correct shape (list of 1D vectors)
        product_embeddings = [embedding.squeeze() for embedding in data['feature_embedding'].tolist()]

        # Calculate cosine similarity between the query embedding and product embeddings
        similarities = cosine_similarity([query_embedding], product_embeddings)

        # Add similarity scores to the DataFrame
        data['similarity'] = similarities[0]

        # Sort by similarity and return top_n results
        results = data.sort_values(by='similarity', ascending=False).head(top_n)

        return results[['processed_title', 'similarity']]

    except Exception as e:
        print(f"Error during semantic search: {e}")
        return None

# Load precomputed product embeddings (from model_building.ipynb)
@st.cache_data
def load_data():
    # Load your data (replace with actual path or data loading method)
    data = pd.read_pickle('bert_embeddings.pkl')
    return data

# Streamlit UI
st.title("BERT-based Semantic Search Engine")

data = load_data()

# Search bar
search_query = st.text_input("Search for a product:")

# Display search results dynamically
if search_query:
    st.write("Searching for:", search_query)
    results = semantic_search_bert(data, search_query)

    st.subheader("Top Recommendations:")
    for index, row in results.iterrows():
        st.write(f"Product: {row['processed_title']}, Similarity: {row['similarity']:.4f}")