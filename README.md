# MongoDB Streamlit Query App

A simple Python application to query MongoDB collections using a graphical interface built with Streamlit.

## Prerequisites

- Python 3.7+
- A running MongoDB instance

## Installation

1.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install streamlit pymongo
    ```

## Usage

1.  **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

2.  **Connect to MongoDB**:
    - Enter your **Connection URI** (e.g., `mongodb://localhost:27017/` or your Atlas URI).
    - Enter the **Database Name**.
    - Enter the **Collection Name**.

3.  **Query**:
    - Enter a valid JSON query in the text area (e.g., `{"age": {"$gt": 25}}`).
    - Leave it as `{}` to find all documents.
    - Click **Run Query**.

## Deployment to Streamlit Community Cloud

To host this application on [Streamlit Community Cloud](https://streamlit.io/cloud), follow these steps:

1.  **Push to GitHub**: Create a GitHub repository and push `app.py` and `requirements.txt`.
2.  **Sign in to Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
3.  **Deploy**: Click "New app", select your repository, branch, and `app.py` as the main file path.
4.  **Configuration**: If your MongoDB is not public, ensure you use a connection string that includes credentials or use Streamlit's `Secrets` management to store your URI securely.

## Notes

- The application limits results to 50 documents by default for performance.
