from flask import Blueprint, jsonify, request
import requests
import os
from datetime import datetime, timedelta

news_bp = Blueprint('news', __name__)

FINNHUB_KEY = os.getenv('FINNHUB_API_KEY', '')

# Credible financial news sources
CREDIBLE_SOURCES = {
    'top_tier': ['Reuters', 'Bloomberg', 'Wall Street Journal', 'Financial Times', 'Associated Press', 'CNBC'],
    'secondary': ['MarketWatch', 'Seeking Alpha', 'Yahoo Finance', 'Investopedia', 'Barrons'],
    'crypto': ['CoinDesk', 'The Block', 'Decrypt', 'Bitcoin Magazine', 'Cointelegraph']
}


def format_timestamp(unix_ts):
    """Convert Unix timestamp to readable format"""
    try:
        dt = datetime.fromtimestamp(unix_ts)
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "Just now"
    except:
        return "Unknown"


def get_source_credibility(source):
    """Return credibility tier for a news source"""
    source_lower = source.lower()
    
    for src in CREDIBLE_SOURCES['top_tier']:
        if src.lower() in source_lower:
            return 'high'
    
    for src in CREDIBLE_SOURCES['secondary']:
        if src.lower() in source_lower:
            return 'medium'
    
    for src in CREDIBLE_SOURCES['crypto']:
        if src.lower() in source_lower:
            return 'crypto'
    
    return 'unknown'


@news_bp.route('/', methods=['GET'])
def get_news():
    """
    Get financial news
    
    Query params:
        - category: general, forex, crypto, merger (default: general)
        - limit: number of articles (default: 10, max: 50)
        - credible_only: filter to credible sources only (default: false)
    """
    category = request.args.get('category', 'general')
    limit = min(request.args.get('limit', 10, type=int), 50)
    credible_only = request.args.get('credible_only', 'false').lower() == 'true'
    
    if not FINNHUB_KEY:
        # Return mock data if no API key
        return jsonify({
            'success': True,
            'articles': get_mock_news(category, limit),
            'source': 'mock'
        }), 200
    
    try:
        url = "https://finnhub.io/api/v1/news"
        params = {
            'category': category,
            'token': FINNHUB_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        articles = []
        for article in data[:limit * 2]:  # Get extra for filtering
            source = article.get('source', 'Unknown')
            credibility = get_source_credibility(source)
            
            # Skip if credible_only filter is on and source isn't credible
            if credible_only and credibility == 'unknown':
                continue
            
            articles.append({
                'id': article.get('id'),
                'title': article.get('headline', 'No title'),
                'summary': article.get('summary', '')[:200] + '...' if article.get('summary') else '',
                'source': source,
                'credibility': credibility,
                'url': article.get('url', ''),
                'image': article.get('image', ''),
                'published': format_timestamp(article.get('datetime', 0)),
                'timestamp': article.get('datetime', 0),
                'category': category,
                'related': article.get('related', '')
            })
            
            if len(articles) >= limit:
                break
        
        return jsonify({
            'success': True,
            'category': category,
            'count': len(articles),
            'articles': articles
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/company/<symbol>', methods=['GET'])
def get_company_news(symbol):
    """
    Get news for a specific stock/company
    
    Path params:
        - symbol: stock ticker (e.g., AAPL, MSFT)
    
    Query params:
        - days: how many days back (default: 7, max: 30)
    """
    days = min(request.args.get('days', 7, type=int), 30)
    
    if not FINNHUB_KEY:
        return jsonify({
            'success': True,
            'symbol': symbol.upper(),
            'articles': [],
            'message': 'API key not configured'
        }), 200
    
    try:
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        url = "https://finnhub.io/api/v1/company-news"
        params = {
            'symbol': symbol.upper(),
            'from': from_date,
            'to': to_date,
            'token': FINNHUB_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        articles = []
        for article in data[:20]:
            articles.append({
                'title': article.get('headline', ''),
                'summary': article.get('summary', '')[:200],
                'source': article.get('source', 'Unknown'),
                'url': article.get('url', ''),
                'published': format_timestamp(article.get('datetime', 0))
            })
        
        return jsonify({
            'success': True,
            'symbol': symbol.upper(),
            'period': f'{days} days',
            'count': len(articles),
            'articles': articles
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/sources', methods=['GET'])
def get_credible_sources():
    """Return list of credible financial news sources"""
    return jsonify({
        'success': True,
        'sources': CREDIBLE_SOURCES
    }), 200


def get_mock_news(category, limit):
    """Return mock news data when API key is not available"""
    mock_articles = [
        {
            'id': 1,
            'title': 'Federal Reserve Signals Potential Rate Cut in Q2 2025',
            'summary': 'Fed officials indicate inflation has cooled enough to consider easing monetary policy in the coming months...',
            'source': 'Reuters',
            'credibility': 'high',
            'url': '#',
            'published': '2h ago',
            'category': 'general'
        },
        {
            'id': 2,
            'title': 'Tech Stocks Rally as AI Investments Continue to Surge',
            'summary': 'Major tech companies see significant gains as artificial intelligence investments drive growth expectations...',
            'source': 'Bloomberg',
            'credibility': 'high',
            'url': '#',
            'published': '4h ago',
            'category': 'general'
        },
        {
            'id': 3,
            'title': 'Bitcoin Approaches New All-Time High Amid Institutional Buying',
            'summary': 'Cryptocurrency markets surge as major institutions increase their Bitcoin holdings...',
            'source': 'CoinDesk',
            'credibility': 'crypto',
            'url': '#',
            'published': '1h ago',
            'category': 'crypto'
        },
        {
            'id': 4,
            'title': 'S&P 500 Closes at Record High for Third Consecutive Day',
            'summary': 'Strong earnings reports and positive economic data push major indices to new records...',
            'source': 'Wall Street Journal',
            'credibility': 'high',
            'url': '#',
            'published': '6h ago',
            'category': 'general'
        },
        {
            'id': 5,
            'title': 'Oil Prices Stabilize After Middle East Tensions Ease',
            'summary': 'Crude oil futures settle as diplomatic efforts reduce geopolitical concerns...',
            'source': 'CNBC',
            'credibility': 'high',
            'url': '#',
            'published': '3h ago',
            'category': 'general'
        }
    ]
    
    # Filter by category if not general
    if category != 'general':
        mock_articles = [a for a in mock_articles if a['category'] == category]
    
    return mock_articles[:limit]
