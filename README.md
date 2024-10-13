# Semantic Search Engine for Laptop Recommendations

## Project Overview
This project implements a semantic search engine to recommend laptop products based on user queries. The search engine utilizes BERT and Sentence Transformer models to generate contextual embeddings for the product data and queries. The system is designed to retrieve and rank relevant products by calculating cosine similarity between the query and product features.

## Features
* **Semantic Search:** Search laptops based on user queries and return relevant results.
* **Machine Learning Models:**
    * BERT for context-aware embeddings.
    * Sentence Transformer for semantic embedding generation.
 * **Evaluation Metrics:**
      * Precision at K (P@10): Measures the relevance of the top 10 recommended results.
      * Mean Reciprocal Rank (MRR): Assesses how well the first relevant item is ranked.
## Technical Workflow
1. **Data Collection:**
* Collect laptop product data including Brand, Model, Processor, RAM, Storage.
2. **Data Cleaning:**
* Remove duplicates and handle missing values.
3. **Data Preprocessing:**
* Perform various NLP prerocessing tasks like: lower-casing the text, removing punctuations and stopwords, tokenizing the text.
4. **Embedding Generation:**
* Generate embeddings using BERT and Sentence Transformer models.
5. **Semantic Search:**
* Use cosine similarity to rank and return relevant products for user queries.
6. **Evaluation:**
* Evaluate model performance using Precision at K and MRR.
## Usage
* Launch the Streamlit app and enter a search query (e.g., "i7 processor, 16GB RAM, SSD").
* The app will display a list of relevant laptops ranked by their similarity to the query.
## Models
* **BERT:** A transformer-based model pre-trained on large datasets, used to generate high-quality contextual embeddings.
* **Sentence Transformer:** A model that generates sentence embeddings specifically designed for similarity tasks.
## Evaluation
1. **Precision at K (P@10):**
* Both models achieve a 0.8 Precision at 10, meaning 80% of the top 10 results are relevant.
2. **Mean Reciprocal Rank (MRR):**
* Both models score 1.0 MRR, indicating that the first relevant item is always ranked first.
## Future Enhancements
* **Fine-Tuning:** Fine-tune the BERT model for better domain-specific results.
* **Personalization:** Incorporate user feedback to enhance search recommendations.
