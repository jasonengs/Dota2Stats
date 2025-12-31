# Dota2Stats

This project implements a data pipeline that fetches raw data from Dota 2 API, cleans and aggregates it using pandas, and compute hero stats such as (Health, Mana, etc.). The result are visualized in a streamlit application with interactive bar chart visualization for comparing two heroes.

![Streamlit App](/assets/images/streamlit_app.jpeg)

## Getting Started

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.11 or higher
- uv

Install uv using pip:

```bash
pip install uv
```

Alternatively, on Windows, you can use the official standalone installer:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For other installation options, refer to the official documentation:

[uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/jasonengs/Dota2Stats.git
   cd Dota2Stats
   ```
2. Install dependencies

   All dependencies are managed via pyproject.toml

   ```sh
   uv sync
   ```

   This will create virtual environment and install all required packages

### Data Preparation

The Streamlit application depends on pre-generated CSV files.

You must run the following scrips in order before starting the app.

1. Fetch data from Dota 2 API

   Fetch raw data from API and save it as CSV files.

   ```sh
   uv run fetch_data.py
   ```

2. Clean and transform data

   Clean, transform, and aggregate the raw data

   ```sh
   uv run transform_data.py
   ```

### Running the Application

After completing the installation and data preparation steps, start teh Streamlit app:

```sh
streamlit run app.py
```

## Data Source

Data originally sourced from:

- https://www.dota2.com/datafeed/herolist?language=english

**Good Luck and Have Fun!**
