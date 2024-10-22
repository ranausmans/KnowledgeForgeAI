import os
from dotenv import load_dotenv
import google.generativeai as genai
from newsapi import NewsApiClient
import networkx as nx
import matplotlib.pyplot as plt
import json

# Load environment variables
load_dotenv()

# Configure APIs
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Set up the Generative AI model
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

# NewsAPI client
news_client = NewsApiClient(api_key=NEWS_API_KEY)

def fetch_articles(query, from_date, to_date, language="en", page_size=5):
    return news_client.get_everything(q=query, from_param=from_date, to=to_date, 
                                      language=language, sort_by='relevancy', page_size=page_size)

def clean_text(text):
    return text.replace('\n', ' ').strip()

def extract_entities(text):
    prompt = f"""
    Extract named entities from the following text. Return the results as a valid JSON array of objects, 
    where each object has 'entity' and 'type' keys. Entity types should be one of: PERSON, ORGANIZATION, LOCATION, DATE, TECHNOLOGY.
    Ensure the output is strictly in JSON format, with no additional text.

    Text: {text}

    JSON Output:
    """
    response = model.generate_content(prompt)
    try:
        json_str = response.text.strip()
        if json_str.startswith('```json'):
            json_str = json_str.split('```json', 1)[1]
        if json_str.endswith('```'):
            json_str = json_str.rsplit('```', 1)[0]
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(f"Error parsing JSON: {response.text}")
        return []

def extract_relationships(text, entities):
    entity_names = [e['entity'] for e in entities]
    prompt = f"""
    Extract relationships between the following entities found in the text. 
    Return the results as a valid JSON array of objects, where each object has 'subject', 'predicate', and 'object' keys.
    Ensure the output is strictly in JSON format, with no additional text.

    Text: {text}
    Entities: {', '.join(entity_names)}

    JSON Output:
    """
    response = model.generate_content(prompt)
    try:
        json_str = response.text.strip()
        if json_str.startswith('```json'):
            json_str = json_str.split('```json', 1)[1]
        if json_str.endswith('```'):
            json_str = json_str.rsplit('```', 1)[0]
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(f"Error parsing JSON: {response.text}")
        return []

def visualize_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    edge_labels = nx.get_edge_attributes(G, 'predicate')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Knowledge Graph Visualization")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    # Fetch articles
    articles = fetch_articles("AI OR 'machine learning' OR 'blockchain'", "2024-10-01", "2024-10-22", page_size=5)
    
    G = nx.Graph()

    for article in articles['articles']:
        print(f"\nProcessing article: {article['title']}")
        
        cleaned_text = clean_text(article['content'])
        entities = extract_entities(cleaned_text)
        
        if not entities:
            print("No entities extracted. Skipping relationship extraction.")
            continue
        
        print("Extracted entities:")
        for entity in entities:
            print(f"- {entity['entity']} ({entity['type']})")
            G.add_node(entity['entity'], type=entity['type'])
        
        relationships = extract_relationships(cleaned_text, entities)

        print("Extracted relationships:")
        for rel in relationships:
            print(f"- {rel['subject']} {rel['predicate']} {rel['object']}")
            G.add_edge(rel['subject'], rel['object'], predicate=rel['predicate'])

    print("\nTop mentioned entities:")
    print(sorted([(n, d) for n, d in G.degree()], key=lambda x: x[1], reverse=True)[:5])

    print("\nTop technologies mentioned:")
    tech_nodes = [(n, d) for n, d in G.degree() if G.nodes[n].get('type') == 'TECHNOLOGY']
    print(sorted(tech_nodes, key=lambda x: x[1], reverse=True)[:5])

    print("\nMost influential companies:")
    org_nodes = [(n, d) for n, d in G.degree() if G.nodes[n].get('type') == 'ORGANIZATION']
    print(sorted(org_nodes, key=lambda x: x[1], reverse=True)[:5])

    if G.number_of_nodes() > 0:
        visualize_graph(G)
    else:
        print("No entities or relationships extracted. Unable to create graph.")

if __name__ == "__main__":
    main()