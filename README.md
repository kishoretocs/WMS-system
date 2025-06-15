# WMS-system

# 🧠 Chat with CSV using DeepSeek (via OpenRouter) - Streamlit App

This project is a lightweight, interactive Streamlit application that allows users to chat with their CSV files using natural language queries powered by DeepSeek through OpenRouter and the `pandas-ai` library.

---

## 🏗️ What I Built

- **Tech Stack**:

  - **Frontend**: Streamlit
  - **Backend**: Python 3.12
  - **AI Tool**: [DeepSeek LLM](https://openrouter.ai/) via OpenRouter
  - **Libraries**:
    - `pandas`
    - `pandasai`
    - `requests`
    - `streamlit`

- **Core Logic**:
  - User uploads a CSV file.
  - The app uses `pandasai` with a custom LLM wrapper (`OpenRouterLLM`) to generate insights from data using DeepSeek.
  - The model answers queries based on the uploaded dataset in natural language.

---

## 🛠️ How I Built It

- I used the [pandasai](https://github.com/gventuri/pandas-ai) library to enable natural language interaction with pandas DataFrames.
- The default LLM was replaced with a custom wrapper (`OpenRouterLLM`) that uses DeepSeek models hosted on [OpenRouter](https://openrouter.ai/).
- The LLM receives prompts through REST API requests using `requests` with appropriate headers including the `Authorization` bearer token.

---

## 🚀 How to Use

1. Upload your `.csv` file using the Streamlit interface.
2. Enter any question related to the data (e.g., _"What is the average revenue in Q1?"_).
3. Click on **Run Query** and get your answer — either as a DataFrame or a simple message.

---

## ⚙️ How to Set Up Locally

### ✅ Requirements

- Python 3.9 or 3.10 (recommended)
- An OpenRouter API Key (https://openrouter.ai/)
- Pip & virtual environment

### 📦 Installation Steps

```bash
# Clone the repository
git clone https://github.com/kishoretocs/WMS-system
cd csv-chat-openrouter

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

#🗝️ Configure API Key
In the textql.py, replace this line with your own API key:

llm = OpenRouterLLM(api_key="sk-or-...", model="deepseek/deepseek-r1-0528:free")
▶️ Run the App

streamlit run textql.py
App will open in your browser at http://localhost:8501

#🔗 Useful Links
OpenRouter

DeepSeek Models

PandasAI GitHub

Streamlit

#📁 Folder Structure

📦 csv-chat-openrouter/
├── openrouter_llm.py        # Custom OpenRouter LLM wrapper
├── textql.py                # Streamlit app file
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
#📬 Contact

Feel free to reach out if you have any questions!
kishoretocs@gmail.com
7358433862
```
