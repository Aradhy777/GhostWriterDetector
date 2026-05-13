# GhostWriter Detector

An AI-powered web application that detects whether text is human-written or AI-generated using advanced text analysis techniques.

## Features

✨ **Real-time Analysis** - Instantly analyze any text for AI generation indicators  
📊 **Detailed Metrics** - Vocabulary diversity, sentence complexity, readability scoring  
📈 **Visual Analytics** - Beautiful charts and visualizations of text characteristics  
📚 **History Tracking** - Keep track of all your analyses  
📥 **Export Reports** - Download analyses as JSON or TXT files  
🎨 **Modern UI** - Dark theme responsive interface  

## Tech Stack

**Backend:**
- Flask 2.3.3
- Flask-SQLAlchemy
- SQLite3
- Python 3.8+

**Frontend:**
- Bootstrap 5
- Chart.js
- HTML/CSS/JavaScript

**AI/NLP:**
- textstat (readability metrics)
- Azure Text Analytics (optional)
- OpenAI API (optional)
- numpy/pandas (analysis)

**Deployment:**
- Gunicorn
- Railway compatible
- Can run on any Python server

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd GhostWriterDetector
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

Edit `.env`:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=replace-with-a-long-random-secret
OPENAI_API_KEY=
AZURE_TEXT_ANALYTICS_API_KEY=
AZURE_TEXT_ANALYTICS_ENDPOINT=
```

Keep `.env` out of version control; it is already ignored by git.

### 5. Run Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Usage

### Analyze Text
1. Go to `/analyze` page
2. Paste or type text you want to analyze
3. Click "Analyze Text"
4. View detailed results with:
   - Human-like score
   - AI-assisted score
   - Confidence level
   - Detailed metrics breakdown
   - Visual charts

### Dashboard
- View overall statistics
- See recent analyses
- Track trends over time

### History
- Access all previous analyses
- Sort by date or scores
- View detailed reports

### Export Results
- Download as JSON for data analysis
- Export as TXT for documentation
- Print reports directly

## Deploying on Railway

If you deploy from the nested `GhostWriterDetector/` folder instead of the repo root, Railway can still use the same app.

1. Use `GhostWriterDetector/Procfile` as the start command source.
2. Install dependencies from `GhostWriterDetector/requirements.txt`.
3. Set the same environment variables as the root README describes.
4. Keep `PORT` unset locally; Railway provides it automatically in production.

The app binds to `0.0.0.0:$PORT` through Gunicorn, which is what Railway expects.

## Analysis Metrics

The application analyzes:
- **Vocabulary Diversity** - Unique words ratio
- **Sentence Complexity** - Average sentence structure
- **Readability Score** - Using Flesch Reading Ease
- **Emotional Variation** - Emotional tone indicators
- **Repetition Control** - Word frequency analysis
- **Formality Level** - Formal language indicators
- **Punctuation Diversity** - Variety of punctuation
- **Capitalization Patterns** - Case usage
- **Pronoun Usage** - Personal pronoun frequency

## Project Structure

```
GhostWriterDetector/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── .env                  # Environment variables
├── .gitignore            # Git ignore rules
│
├── models/               # Database models
│   ├── analysis.py       # Analysis model
│   └── history.py        # History model
│
├── services/             # Business logic
│   ├── text_processor.py
│   ├── scoring_engine.py
│   ├── visualization_service.py
│   ├── report_generator.py
│   ├── azure_text_analysis.py
│   └── openai_service.py
│
├── modules/              # Utilities
│   ├── database_manager.py
│   ├── validators.py
│   ├── utilities.py
│   └── helpers.py
│
├── templates/            # HTML templates
├── static/               # CSS, JS, assets
├── database/             # SQLite database
├── exports/              # Exported reports
├── uploads/              # Uploaded files
└── instance/             # Flask instance config
```

## API Endpoints

- `GET /` - Landing page
- `GET /dashboard` - Statistics dashboard
- `GET/POST /analyze` - Text analysis
- `GET /history` - Analysis history
- `GET /report/<id>` - Detailed report
- `GET /api/analysis/<id>` - JSON API
- `GET /api/export/<id>` - Export JSON
- `GET /api/export-text/<id>` - Export TXT

## Database Schema

### Analysis Table
- id (PRIMARY KEY)
- original_text (TEXT)
- human_score (FLOAT)
- ai_score (FLOAT)
- readability (FLOAT)
- emotional_variation (FLOAT)
- vocabulary_score (FLOAT)
- sentence_complexity (FLOAT)
- repetition_score (FLOAT)
- formality_score (FLOAT)
- sentiment_label (VARCHAR)
- sentence_count (INT)
- word_count (INT)
- avg_word_length (FLOAT)
- unique_words_ratio (FLOAT)
- created_at (DATETIME)

### History Table
- id (PRIMARY KEY)
- analysis_id (FOREIGN KEY)
- summary (TEXT)
- generated_report (TEXT)
- created_at (DATETIME)

## Deployment

### Railway

1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy from main branch
4. Access your deployed app

### Local Server

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

Create a Dockerfile if needed for containerization.

## Scoring Algorithm

The scoring engine analyzes multiple factors:

- **Vocabulary Diversity (15%)** - Higher = more human-like
- **Sentence Variety (15%)** - More variation = human-like
- **Emotional Variation (12%)** - Natural emotions = human-like
- **Readability (10%)** - Moderate readability = human-like
- **Formality (12%)** - Moderate formality = human-like
- **Repetition (10%)** - Low repetition = human-like
- **Punctuation (8%)** - Natural punctuation = human-like
- **Pronoun Usage (8%)** - Natural usage = human-like
- **Capitalization (5%)** - Normal patterns = human-like
- **Complexity (5%)** - Moderate complexity = human-like

Final scores:
- **Human Score**: 0-100 (higher = more human-like)
- **AI Score**: 0-100 (higher = more AI-generated)

## Important Notes

⚠️ **Disclaimer**: This tool provides analysis but is not 100% accurate. It uses statistical analysis and ML patterns. Always review results with context.

✅ **No API Keys Required**: Works without Azure or OpenAI credentials. Falls back to local analysis.

🔒 **Privacy**: Text is only stored in local database. No external logging.

## Contributing

Feel free to submit issues and pull requests!

## License

MIT License - feel free to use this project for educational purposes.

## Author

Created as a BTech AI Project

## Support

For issues or questions, open an issue on GitHub.

---

**Version**: 1.0.0  
**Last Updated**: 2026
