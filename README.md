# 🌱 AI Carbon Footprint Estimator

An interactive web application that calculates your annual carbon footprint and provides AI-powered recommendations for reducing your environmental impact.

## Features

- **Interactive Questionnaire**: Simple questions about your lifestyle (travel, transport, diet, shopping, home energy)
- **Accurate Calculations**: Research-based emission factors for realistic carbon footprint estimates
- **Visual Analytics**: Interactive charts showing your emissions breakdown
- **AI Recommendations**: Personalized advice powered by OpenAI GPT-4o
- **Progress Tracking**: Database storage to track your carbon journey over time
- **Export Results**: Download your results as CSV files

## Live Demo


## Screenshots


## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with PostgreSQL database
- **AI**: OpenAI GPT-4o for personalized recommendations
- **Visualization**: Plotly for interactive charts
- **Database**: PostgreSQL for data persistence

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL database
- OpenAI API key

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-carbon-footprint-estimator.git
cd ai-carbon-footprint-estimator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL="your_postgresql_connection_string"
export OPENAI_API_KEY="your_openai_api_key"
```

4. Run the application:
```bash
streamlit run app.py --server.port 5000
```

5. Open your browser to `http://localhost:5000`

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI recommendations

## Project Structure

```
├── app.py                 # Main Streamlit application
├── carbon_calculator.py   # Core emission calculation logic
├── ai_advisor.py          # AI-powered recommendation engine
├── database_simple.py     # Database operations
├── pyproject.toml         # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── README.md             # This file
```

## How It Works

1. **Data Collection**: Users answer questions about their lifestyle
2. **Calculation**: The app converts inputs to CO₂ emissions using scientific factors
3. **Visualization**: Results shown with interactive charts and comparisons
4. **AI Analysis**: OpenAI analyzes results and generates personalized advice
5. **Storage**: Results saved to database for progress tracking

## Emission Factors

The calculator uses research-based emission factors:

- **Flights**: 0.3 tonnes CO₂ (short) / 1.5 tonnes CO₂ (long)
- **Transport**: Varies by type (0g-180g CO₂ per km)
- **Diet**: Based on meat/dairy consumption frequency
- **Shopping**: 25kg CO₂ per £100 clothing / 15kg CO₂ per £100 general
- **Home Energy**: Based on home size and heating type

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Carbon emission factors based on research from climate science organizations
- Built with Streamlit for rapid web development
- AI recommendations powered by OpenAI
- Icons from emoji collections

