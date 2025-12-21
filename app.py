import streamlit as st
from pymongo import MongoClient
import json
from bson.json_util import dumps

def get_connection(uri, db_name, collection_name):
    try:
        client = MongoClient(uri)
        # Check connection
        client.admin.command('ping')
        db = client[db_name]
        collection = db[collection_name]
        return collection, None
    except Exception as e:
        return None, str(e)

def main():
    st.set_page_config(page_title="MongoDB Query Tool", layout="wide")
    st.title("🍃 MongoDB Query Tool")

    # Sidebar for Connection Details
    st.sidebar.header("Connection Settings")
    uri = st.sidebar.text_input("Connection URI", value="mongodb://localhost:27017/", type="password")
    db_name = st.sidebar.text_input("Database Name")
    collection_name = st.sidebar.text_input("Collection Name")

    # Main Area
    st.subheader("Query")
    
    default_query = "{\n    \n}"
    query_text = st.text_area("Enter your query (JSON format)", value=default_query, height=200)

    if st.button("Run Query"):
        if not db_name or not collection_name:
            st.error("Please provide both Database Name and Collection Name.")
            return

        try:
            # Parse the query string to a dictionary
            query_dict = json.loads(query_text) if query_text.strip() else {}
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON format: {e}")
            return

        # Connect and Query
        collection, error = get_connection(uri, db_name, collection_name)
        
        if error:
            st.error(f"Connection Failed: {error}")
        else:
            try:
                results = list(collection.find(query_dict).limit(50)) # Limit to 50 results for safety
                
                st.subheader(f"Results ({len(results)})")
                
                if results:
                    # Convert ObjectId and other BSON types to string for display
                    json_results = json.loads(dumps(results))
                    st.json(json_results)
                    
                    # Optional: Table view for flat data
                    # st.dataframe(json_results)
                else:
                    st.info("No documents found matching the query.")
            except Exception as e:
                st.error(f"Error executing query: {e}")

if __name__ == "__main__":
    main()
