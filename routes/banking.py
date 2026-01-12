from flask import Blueprint, jsonify, request
import os
from datetime import datetime, timedelta

banking_bp = Blueprint('banking', __name__)

# Plaid configuration
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID', '')
PLAID_SECRET = os.getenv('PLAID_SECRET', '')
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')

# Essential spending categories
ESSENTIAL_CATEGORIES = [
    'groceries', 'supermarket', 'grocery',
    'rent', 'mortgage', 'housing',
    'utilities', 'electric', 'gas', 'water', 'internet',
    'insurance', 'health insurance', 'car insurance',
    'healthcare', 'medical', 'pharmacy', 'doctor',
    'transportation', 'fuel', 'gas station', 'public transit',
    'childcare', 'education'
]

# Non-essential spending categories
NON_ESSENTIAL_CATEGORIES = [
    'dining', 'restaurant', 'fast food', 'coffee',
    'entertainment', 'movies', 'streaming', 'gaming',
    'shopping', 'clothing', 'electronics', 'amazon',
    'subscriptions', 'netflix', 'spotify',
    'travel', 'vacation', 'hotel', 'airline',
    'personal care', 'salon', 'spa'
]


def categorize_transaction(transaction):
    """
    Categorize a transaction as essential or non-essential
    
    Args:
        transaction: dict with 'category', 'name', 'amount'
    
    Returns:
        dict with original transaction plus 'is_essential' and 'category_type'
    """
    name = transaction.get('name', '').lower()
    category = transaction.get('category', '').lower()
    
    # Check if essential
    is_essential = False
    for keyword in ESSENTIAL_CATEGORIES:
        if keyword in name or keyword in category:
            is_essential = True
            break
    
    # If not essential, check if non-essential (default to non-essential if unknown)
    category_type = 'essential' if is_essential else 'non-essential'
    
    return {
        **transaction,
        'is_essential': is_essential,
        'category_type': category_type
    }


def analyze_spending(transactions):
    """
    Analyze spending patterns from transactions
    
    Returns:
        dict with spending analysis
    """
    total_spent = 0
    essential_spent = 0
    non_essential_spent = 0
    category_breakdown = {}
    
    for tx in transactions:
        amount = abs(tx.get('amount', 0))
        total_spent += amount
        
        if tx.get('is_essential', False):
            essential_spent += amount
        else:
            non_essential_spent += amount
        
        # Category breakdown
        cat = tx.get('category', 'Other')
        if cat not in category_breakdown:
            category_breakdown[cat] = 0
        category_breakdown[cat] += amount
    
    return {
        'total_spent': round(total_spent, 2),
        'essential_spent': round(essential_spent, 2),
        'non_essential_spent': round(non_essential_spent, 2),
        'essential_percent': round((essential_spent / total_spent * 100) if total_spent > 0 else 0, 1),
        'non_essential_percent': round((non_essential_spent / total_spent * 100) if total_spent > 0 else 0, 1),
        'category_breakdown': {k: round(v, 2) for k, v in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True)}
    }


@banking_bp.route('/connect', methods=['POST'])
def connect_bank():
    """
    Exchange Plaid public token for access token
    
    In production, this would use Plaid Link to get a public_token
    from the frontend, then exchange it for an access_token
    """
    data = request.json
    public_token = data.get('public_token')
    
    if not public_token:
        return jsonify({
            'success': False,
            'error': 'public_token is required'
        }), 400
    
    # In production, you would:
    # 1. Use plaid.Client to exchange public_token
    # 2. Store the access_token securely
    # 3. Return success
    
    # For now, return mock success
    return jsonify({
        'success': True,
        'message': 'Bank account connected successfully',
        'access_token': 'mock_access_token_' + public_token[:8]
    }), 200


@banking_bp.route('/spending/<access_token>', methods=['GET'])
def get_spending(access_token):
    """
    Get spending analysis for connected bank account
    
    Query params:
        - days: number of days to analyze (default 30)
    """
    days = request.args.get('days', 30, type=int)
    
    if not access_token:
        return jsonify({
            'success': False,
            'error': 'access_token is required'
        }), 400
    
    # In production, you would fetch real transactions from Plaid
    # For now, return realistic mock data
    
    mock_transactions = [
        {'name': 'Whole Foods Market', 'category': 'Groceries', 'amount': 156.32, 'date': '2025-01-10'},
        {'name': 'Shell Gas Station', 'category': 'Transportation', 'amount': 45.00, 'date': '2025-01-09'},
        {'name': 'Netflix', 'category': 'Subscriptions', 'amount': 15.99, 'date': '2025-01-08'},
        {'name': 'Uber Eats', 'category': 'Dining', 'amount': 34.50, 'date': '2025-01-08'},
        {'name': 'Electric Company', 'category': 'Utilities', 'amount': 120.00, 'date': '2025-01-07'},
        {'name': 'Amazon', 'category': 'Shopping', 'amount': 89.99, 'date': '2025-01-06'},
        {'name': 'Starbucks', 'category': 'Coffee', 'amount': 6.50, 'date': '2025-01-06'},
        {'name': 'Rent Payment', 'category': 'Housing', 'amount': 1500.00, 'date': '2025-01-01'},
        {'name': 'Health Insurance', 'category': 'Insurance', 'amount': 350.00, 'date': '2025-01-01'},
        {'name': 'Spotify', 'category': 'Subscriptions', 'amount': 10.99, 'date': '2025-01-05'},
        {'name': 'Target', 'category': 'Shopping', 'amount': 67.43, 'date': '2025-01-04'},
        {'name': 'CVS Pharmacy', 'category': 'Healthcare', 'amount': 23.50, 'date': '2025-01-03'},
        {'name': 'Movie Theater', 'category': 'Entertainment', 'amount': 28.00, 'date': '2025-01-02'},
        {'name': 'Trader Joes', 'category': 'Groceries', 'amount': 98.76, 'date': '2025-01-02'},
    ]
    
    # Categorize each transaction
    categorized = [categorize_transaction(tx) for tx in mock_transactions]
    
    # Analyze spending
    analysis = analyze_spending(categorized)
    
    # Account balances (mock)
    accounts = {
        'checking': {
            'name': 'Checking Account',
            'balance': 3450.67,
            'available': 3400.00
        },
        'savings': {
            'name': 'Savings Account',
            'balance': 12500.00,
            'available': 12500.00
        }
    }
    
    return jsonify({
        'success': True,
        'period_days': days,
        'accounts': accounts,
        'analysis': analysis,
        'transactions': categorized
    }), 200


@banking_bp.route('/accounts/<access_token>', methods=['GET'])
def get_accounts(access_token):
    """Get linked bank accounts"""
    
    # Mock account data
    accounts = [
        {
            'id': 'acc_001',
            'name': 'Checking Account',
            'type': 'checking',
            'balance': 3450.67,
            'institution': 'Chase Bank'
        },
        {
            'id': 'acc_002',
            'name': 'Savings Account',
            'type': 'savings',
            'balance': 12500.00,
            'institution': 'Chase Bank'
        }
    ]
    
    return jsonify({
        'success': True,
        'accounts': accounts,
        'total_balance': sum(acc['balance'] for acc in accounts)
    }), 200
