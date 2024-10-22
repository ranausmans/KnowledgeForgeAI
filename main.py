import os
from dotenv import load_dotenv
import google.generativeai as genai
from data_collection.news_api import NewsAPIClient
from data_preprocessing.text_cleaner import TextCleaner
from nlp.entity_extractor import EntityExtractor
from nlp.relationship_extractor import RelationshipExtractor
from visualization.graph_visualizer import visualize_graph
import networkx as nx

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def main():
    # Initialize components
    news_client = NewsAPIClient()
    text_cleaner = TextCleaner()
    entity_extractor = EntityExtractor()
    relationship_extractor = RelationshipExtractor()

    # Fetch 5 articles about Apple
    articles = news_client.fetch_articles("Apple", "2024-10-21", "2024-10-22", language="en", page_size=5)

    if not articles:
        print("No articles found. Please check your News API key and query parameters.")
        return

    G = nx.Graph()

    for article in articles:
        print(f"\nProcessing article: {article['title']}")

        try:
            # Process the article
            cleaned_text = text_cleaner.clean_text(article['content'])
            entities = entity_extractor.extract_entities(cleaned_text)
            
            if not entities:
                print("No entities extracted. Skipping relationship extraction.")
                continue
            
            relationships = relationship_extractor.extract_relationships(cleaned_text, entities)

            # Print extracted information
            print("\nExtracted Entities:")
            for entity in entities:
                print(f"- {entity['entity']} ({entity['type']})")
                G.add_node(entity['entity'], type=entity['type'])

            print("\nExtracted Relationships:")
            for rel in relationships:
                print(f"- {rel['subject']} {rel['predicate']} {rel['object']}")
                G.add_edge(rel['subject'], rel['object'], predicate=rel['predicate'])
        
        except Exception as e:
            print(f"Error processing article: {e}")
            continue

    if G.number_of_nodes() > 0:
        # Visualize the graph
        visualize_graph(G)
    else:
        print("No entities or relationships extracted. Unable to create graph.")

if __name__ == "__main__":
    main()
