# Unified Finance Tracker - Backend API

A Flask-based backend for the Unified Finance Tracker app, providing APIs for blockchain wallet tracking, banking integration, trading portfolio aggregation, AI-powered financial advice, and news feeds.

## Features

- **Blockchain Tab**: Multi-chain wallet scanning (Ethereum, Polygon)
- **Banking Tab**: Plaid integration with automatic expense categorization (essential vs non-essential)
- **Trading Tab**: Multi-broker portfolio aggregation
- **AI Advisor**: OpenAI GPT-powered chat and document analysis
- **News Feed**: Financial news from credible sources via Finnhub

---

## Quick Start

### 1. Clone or Download

```bash
git clone https://github.com/YOUR_USERNAME/financial-app-backend.git
cd financial-app-backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
FLASK_ENV=development
SECRET_KEY=your-random-secret-key
OPENAI_API_KEY=sk-your-openai-key-here
ETHERSCAN_API_KEY=your-etherscan-key
FINNHUB_API_KEY=your-finnhub-key
```

### 5. Run Locally

```bash
python app.py
```

Server runs at: `http://localhost:5000`

Test it: `curl http://localhost:5000/api/health`

---

## API Endpoints

### Health Check
- `GET /api/health` - Check if backend is running

### Blockchain
- `GET /api/blockchain/wallet/<address>` - Get all assets for wallet
- `GET /api/blockchain/wallet/<address>/defi` - Get DeFi positions only

### Banking
- `POST /api/banking/connect` - Connect bank account (Plaid)
- `GET /api/banking/spending/<token>` - Get spending analysis
- `GET /api/banking/accounts/<token>` - Get linked accounts

### Trading
- `POST /api/trading/connect` - Connect broker account
- `GET /api/trading/portfolio/<token>` - Get portfolio data
- `POST /api/trading/aggregate` - Aggregate multiple portfolios
- `POST /api/trading/transfer` - Initiate transfer

### AI
- `POST /api/ai/chat` - Chat with AI advisor
- `POST /api/ai/upload-document` - Upload and analyze PDF
- `POST /api/ai/analyze` - Full financial health analysis
- `POST /api/ai/clear-conversation` - Clear chat history

### News
- `GET /api/news` - Get financial news
- `GET /api/news/company/<symbol>` - Get company-specific news
- `GET /api/news/sources` - Get list of credible sources

---

## Deploy to Railway

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Initial backend setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/financial-app-backend.git
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize GitHub and select your repository
5. Railway auto-detects Python and deploys

### Step 3: Add Environment Variables

In Railway dashboard:
1. Click your project
2. Go to **"Variables"** tab
3. Add each variable from `.env.example`:
   - `SECRET_KEY`
   - `OPENAI_API_KEY`
   - `ETHERSCAN_API_KEY`
   - `FINNHUB_API_KEY`
   - (Add others as needed)

### Step 4: Get Your API URL

After deployment, Railway provides a URL like:
```
https://financial-app-backend-production.up.railway.app
```

**This is your backend URL for Bolt!**

---

## Connect to Bolt Frontend

In your Bolt project, update the API configuration:

```javascript
// src/utils/api.ts or src/config/api.js
const API_BASE_URL = 'https://YOUR-RAILWAY-URL.up.railway.app/api';
```

---

## API Keys (Free Tiers)

| Service | Free Tier | Get Key |
|---------|-----------|---------|
| OpenAI | Pay as you go | [platform.openai.com](https://platform.openai.com) |
| Etherscan | 5 calls/sec | [etherscan.io/apis](https://etherscan.io/apis) |
| Finnhub | 60 calls/min | [finnhub.io](https://finnhub.io) |
| Plaid | Sandbox free | [plaid.com](https://plaid.com) |
| Polygonscan | 5 calls/sec | [polygonscan.com/apis](https://polygonscan.com/apis) |

---

## Project Structure

```
financial-app-backend/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Procfile              # Railway/Heroku deployment
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── routes/
    ├── __init__.py
    ├── blockchain.py     # Wallet scanning endpoints
    ├── banking.py        # Plaid/expense endpoints
    ├── trading.py        # Portfolio endpoints
    ├── ai.py             # OpenAI chat endpoints
    └── news.py           # News feed endpoints
```

---

## Troubleshooting

### CORS Errors
Backend has CORS enabled for all origins. If issues persist, check browser console.

### API Key Errors
- Verify keys are correctly set in Railway Variables
- Check Railway logs for specific errors

### OpenAI Rate Limits
- Using `gpt-4o-mini` for cost efficiency
- Implement caching for repeated queries

### Railway Deployment Issues
- Ensure `Procfile` exists
- Check `requirements.txt` has all dependencies
- View logs in Railway dashboard

---

## Cost Estimates

| Service | Monthly Cost |
|---------|--------------|
| Railway | Free tier available, ~$5/mo for hobby |
| OpenAI | ~$1-5 depending on usage |
| Etherscan | Free |
| Finnhub | Free |
| **Total** | **~$5-10/month** |

---

## Next Steps

1. Deploy backend to Railway
2. Get your backend URL
3. Update Bolt frontend with the URL
4. Test each endpoint
5. Add real Plaid integration when ready

---

## Support

Built for the Unified Finance Tracker project. For issues, check:
- Railway logs
- Browser network tab
- API response errors
