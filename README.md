# Drone Delivery Network Optimization - Supply Chain using a MILP model
---

# Drone Delivery Network Optimization for Sindhupalchok, Nepal

This repository contains a prescriptive logistics optimization model designed to address last-mile medical supply and vaccine delivery challenges in the mountainous terrain of Sindhupalchok, Nepal.

Using Mixed-Integer Linear Programming (MILP), the model identifies the mathematically optimal location for drone infrastructure (Hubs) to minimize setup fees and transportation costs while accounting for seasonal weather risks like monsoon flight penalties. The project includes an interactive Streamlit dashboard allowing decision-makers to visualize the network and adjust risk parameters in real-time.

## Features

* **MILP Optimization Engine:** Solves a Fixed-Charge Location Problem to balance facility startup costs against operational drone flight expenses.
* **Monsoon Penalty Filter:** Simulates operational friction by adjusting drone travel times and costs during bad weather seasons.
* **Interactive Dashboard:** Built with Streamlit to enable public health stakeholders to interactively visualize optimal routes, costs, and hub placements without needing to read raw code.

## Project Structure

```text
├── app.py                # Main Streamlit dashboard interface
├── optimization.py       # Core MILP model code and solver configuration
├── requirements.txt      # List of dependencies for environment replication
├── data/
│   ├── clinics.csv       # Geographic coordinates for the 25 health clinics
│   └── distance_matrix.csv# Pre-computed network distances between nodes
└── README.md             # Project documentation

```

## Setup and Installation

To ensure full reproducibility, follow these steps to set up your local environment and run the dashboard:

### 1. Clone the Repository

Open your terminal and clone this repository to your local machine:

bash``
git clone https://github.com
cd humanitarian-drone-routing-nepal

```

### 2. Create a Virtual Environment

It is highly recommended to use an isolated environment to prevent dependency conflicts:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

Install all required packages and pinning tools using the provided requirements file:

```bash
pip install -r requirements.txt

```

### 4. Run the Streamlit Dashboard

Launch the interactive web application directly from your active terminal:

```bash
streamlit run app.py

```

After running this command, your terminal will generate a local network URL (usually `http://localhost:8501`). Your default browser should open the dashboard automatically. If it does not, copy and paste that URL into your browser's search bar.

## How the Optimization Works

Unlike machine learning algorithms (such as regression or XGBoost) which predict patterns, this model uses a **Branch and Bound** optimization solver to find a deterministic, best-possible solution.

The objective function minimizes:

1. **Fixed Costs:** The financial investment required to set up a drone launchpad at a given node.
2. **Variable Transportation Costs:** The cost per kilometer flown to deliver supplies from selected hubs to all 25 local health clinics, heavily adjusted by your custom weather-based constraint criteria.

```
