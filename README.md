# Digital Business Card using CSS Box Model

**Name on card:** Dhairya Darji (Web Developer)
**Brand:** CodeNest Studio

A mini web project that shows a professional digital business card built with the CSS Box Model
(content, padding, border, margin). Card details are stored in a SQLite database.

## Tech stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite (created automatically as `card.db`)

## How to run
```
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Features
- Live card preview while typing
- Save card to SQLite database
- Reset to default details
- Print-friendly card
- "Show Box Model" button highlights the card's box
- Responsive for mobile and laptop

## API routes
| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Main page |
| `/api/card` | GET | Read saved card |
| `/api/card` | POST | Save card |
| `/api/card/reset` | POST | Restore default details |
