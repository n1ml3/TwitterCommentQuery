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

from bson.code import Code

def main():
    st.set_page_config(page_title="MongoDB Query Tool", layout="wide")
    st.title("🍃 MongoDB Query Tool")

    # Sidebar for Connection Details
    st.sidebar.header("Connection Settings")
    default_uri = "mongodb+srv://n4mle:balabolo4444@cluster0.lf5rwyq.mongodb.net/"
    uri = st.sidebar.text_input("Connection URI", value=default_uri, type="password")
    db_name = st.sidebar.text_input("Database Name", value="Comments")
    collection_name = st.sidebar.text_input("Collection Name", value="twitter2")

    # Tabs for different operations
    tab_find, tab_mr = st.tabs(["Find Query", "Map Reduce"])

    # --- Tab 1: Find Query ---
    with tab_find:
        st.subheader("Find Documents")
        default_query = "{\n    \n}"
        query_text = st.text_area("Enter your query (JSON format)", value=default_query, height=200)

        if st.button("Run Query", key="btn_find"):
            if not uri:
                st.error("Please provide a Connection URI.")
            elif not db_name or not collection_name:
                st.error("Please provide both Database Name and Collection Name.")
            else:
                try:
                    query_dict = json.loads(query_text) if query_text.strip() else {}
                    
                    collection, error = get_connection(uri, db_name, collection_name)
                    if error:
                        st.error(f"Connection Failed: {error}")
                    else:
                        results = list(collection.find(query_dict).limit(50))
                        st.subheader(f"Results ({len(results)})")
                        if results:
                            json_results = json.loads(dumps(results))
                            st.json(json_results)
                        else:
                            st.info("No documents found matching the query.")
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON format: {e}")
                except Exception as e:
                    st.error(f"Error executing query: {e}")

    # --- Tab 2: Aggregation (Map-Reduce Alternative) ---
    with tab_mr:
        st.subheader("Aggregation Pipeline")
        st.info("MongoDB Atlas Free Tier does not support Map-Reduce. Using Aggregation Pipeline instead (Faster & Supported).")

        # --- Templates ---
        agg_templates = {
            "Custom": "[\n  {\n    \"$match\": {\n      \n    }\n  }\n]",
            "Count by Class (class)": """[
  {
    "$group": {
      "_id": "$class",
      "count": { "$sum": 1 }
    }
  }
]""",
            "Word Frequency (tweet)": """[
  {
    "$project": {
      "words": {
        "$split": [{ "$toString": { "$ifNull": ["$tweet", ""] } }, " "]
      }
    }
  },
  { "$unwind": "$words" },
  {
    "$match": {
      "words": { "$ne": "" }
    }
  },
  {
    "$group": {
      "_id": "$words",
      "count": { "$sum": 1 }
    }
  },
  { "$sort": { "count": -1 } }
]""",
            "Total Length by Class": """[
  {
    "$project": {
      "class": 1,
      "length": {
        "$strLenCP": { "$toString": { "$ifNull": ["$tweet", ""] } }
      }
    }
  },
  {
    "$group": {
      "_id": "$class",
      "totalLength": { "$sum": "$length" }
    }
  }
]"""
        }

        selected_template_name = st.selectbox("Select a Template", options=list(agg_templates.keys()))
        pipeline_str_default = agg_templates[selected_template_name]

        pipeline_text = st.text_area("Aggregation Pipeline (JSON List)", value=pipeline_str_default, height=300)

        if st.button("Run Aggregation", key="btn_agg"):
            if not uri:
                st.error("Please provide a Connection URI.")
            elif not db_name or not collection_name:
                st.error("Please provide both Database Name and Collection Name.")
            else:
                try:
                    # Parse JSON pipeline
                    pipeline = json.loads(pipeline_text)
                    
                    collection, error = get_connection(uri, db_name, collection_name)
                    if error:
                        st.error(f"Connection Failed: {error}")
                    else:
                        # Execute Aggregation
                        results = list(collection.aggregate(pipeline))
                        
                        # Display Results
                        st.subheader(f"Results ({len(results)})")
                        if results:
                            json_results = json.loads(dumps(results))
                            st.json(json_results)
                        else:
                            st.info("No results returned.")
                        
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON format in Pipeline: {e}")
                except Exception as e:
                    st.error(f"Error executing Aggregation: {e}")

if __name__ == "__main__":
    main()
