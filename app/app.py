import streamlit as st
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def semantic_search_bert(data, query, top_n=10):
    try:
        # Load pre-trained BERT model and tokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')

        # Generate BERT embedding for the query
        encoded_input = tokenizer(query, padding=True, truncation=True, return_tensors='pt')
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

        return results[['combined_features', 'similarity']]

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
        st.write(f"Product: {row['combined_features']}, Similarity: {row['similarity']:.4f}")