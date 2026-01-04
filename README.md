Interactive Public Health Data Dashboard

📊 Overview

The Interactive Public Health Data Dashboard is a web application developed as a capstone project for the Master of Science in Information Technology program at the University of the People. The tool aims to empower non-technical users to explore and analyze complex health datasets from the World Health Organization (WHO) without requiring programming skills or advanced statistical training.



The application is specifically designed for journalists, policy analysts, researchers, educators, and community health advocates who need access to reliable health data for evidence-based decision making.



✨ Key Features

📈 Multiple Interactive Visualizations

Time Series Charts: Track health indicator trends across years



Comparative Bar Charts: Compare countries across selected indicators



Geographic Maps: Display the spatial distribution of health indicators



Real-time Updates: All charts update dynamically with filter changes



🔍 Multi-dimensional Data Exploration

Geographic Filtering: Select specific countries or regions



Temporal Filtering: Define year ranges using interactive sliders



Indicator Filtering: Choose from multiple health indicators



Filter Combinations: Apply multiple filters simultaneously for precise insights



⚡ High Performance \& Ease of Use

Intuitive Interface: Designed for non-technical users



Fast Response: Instant results even with large datasets



Responsive Design: Works on desktop and tablet devices



Data Export: Download filtered data in CSV format for further analysis



🛠 Technologies Used

Backend (Data Processing)

Python 3.11+ - Primary programming language



Pandas - Data processing and analysis



NumPy - Numerical operations



SQLite - Lightweight database



Frontend (User Interface)

Streamlit - Interactive web application framework



Plotly - Interactive visualization library



Custom CSS - Styling and appearance customization



Development \& Deployment Tools

Git - Version control



VS Code - Development environment



Virtual Environment - Python package isolation



Requirements.txt - Dependency management



🚀 Installation \& Setup

Prerequisites

Python 3.11 or higher



pip (Python package manager)



Git (for source code access)



Installation Steps

Clone the Project:



bash

git clone https://github.com/yourusername/public-health-dashboard.git

cd public-health-dashboard

Create Virtual Environment:



bash

python -m venv venv

source venv/bin/activate  # Linux/Mac

venv\\Scripts\\activate     # Windows

Install Dependencies:



bash

pip install -r requirements.txt

Download Data:



bash

python scripts/download\_data.py

Run the Application:



bash

streamlit run app/main.py

Open in Browser:



Navigate to http://localhost:8501



Start exploring health data!



📁 Project Structure

text

public-health-dashboard/

├── app/

│   ├── main.py              # Main application entry point

│   ├── data\_processor.py    # Data processing and transformation

│   ├── visualizations.py    # Chart generation functions

│   └── utils.py             # Utility functions

├── data/

│   ├── raw/                 # Raw data from WHO

│   ├── processed/           # Processed data

│   └── database.db          # SQLite database

├── scripts/

│   ├── download\_data.py     # Data download script

│   └── setup\_database.py    # Database setup script

├── tests/                   # Unit and integration tests

├── docs/                    # Additional documentation

├── requirements.txt         # Python dependencies

├── README.md               # This file

└── .gitignore              # Files excluded from Git

📖 Usage Guide

1\. Select Dataset

Choose the dataset to analyze from the dropdown menu



Available datasets: "Life Expectancy", "Mortality by Cause", and others



2\. Apply Filters

Countries/Regions: Select specific countries or entire regions



Time Range: Use sliders to define year ranges



Health Indicators: Choose indicators of interest



3\. Explore Visualizations

Time Series Chart: View trends over time



Bar Chart: Compare countries in a specific year



Map: View global geographical distribution



4\. Export Results

Use "Export Data" button to download filtered data



Take screenshots to document important findings



📊 Data Sources

Primary Sources

World Health Organization (WHO) - Global Health Observatory



Life expectancy at birth



Healthy life expectancy (HALE)



Mortality rates by cause



Data Quality

All data is aggregated at the population level



Contains no personally identifiable information



Available for public use with proper attribution



Includes time periods from 2000 to 2022



Data Updates

bash

\# To update data to the latest version

python scripts/download\_data.py --update

🧪 Testing

Run Tests

bash

\# All tests

pytest tests/



\# Specific tests

pytest tests/test\_data\_processor.py

pytest tests/test\_visualizations.py

Test Types

Unit Tests: Individual functions and data processing



Integration Tests: Component interactions



System Tests: Complete usage scenarios



📝 License

This project is licensed under the MIT License. See the LICENSE file for details.



Usage Terms

Attribution to the original source is required.



Modification and redistribution are permitted.



Suitable for commercial and educational use



Data accuracy not guaranteed - refer to original data sources.



🤝 Contributors

Hazem Alahmad - Main Developer



Architectural design and implementation



User interface and experience



Documentation and testing



How to Contribute

Fork the project



Create your feature branch (git checkout -b feature/AmazingFeature)



Commit your changes (git commit -m 'Add some AmazingFeature')



Push to the branch (git push origin feature/AmazingFeature)



Open a Pull Request





Describe the issue in detail with reproduction steps.



Include screenshots if possible.



General Questions

Email: h.zoom-94@hotmail.com







Special Thanks

Dr. Romana Riyaz - Academic Supervisor



University of the People - Educational framework and support



World Health Organization - High-quality publicly available data



🎓 Capstone Project

This project was developed as part of graduation requirements for the Master of Science in Information Technology (MSIT) program at the University of the People.



Course Information

Course: MSIT 5910 - Capstone Project



Student: Hazem Alahmad



Supervisor: Dr. Romana Riyaz



Term: Term 6, December 2025



Learning Outcomes Achieved

✅ Apply IT principles to solve real-world problems

✅ Design and evaluate computing solutions using best practices

✅ Analyze user needs in computing solutions

✅ Consider ethical aspects in computing practice

✅ Present research-supported arguments in computing contexts





