# Currency Converter App

A Flask-based currency converter application that provides real-time currency conversion and historical rate tracking.

## Features

- Currency conversion between multiple currencies
- Top 5 exchange rates display
- Historical rate tracking
- Educational currency information (Currency 101)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
# For production
pip install -r requirements.txt

# For development
pip install -r requirements/dev.txt
```

3. Create environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
flask run
```

## Project Structure

```
currencyConverter/
├── venv/
├── currency_converter_app/
│   ├── routes/
│   │   ├── main.py
│   │   └── info.py
│   └── services/
│       ├── converter.py
│       └── rate_service.py
├── data/
│   └── rates.json
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   ├── currency101.html
│   └── result.html
└── tests/
```

## Development

- Run tests: `pytest`
- Format code: `black .`
- Check style: `flake8`

## License

MIT License 