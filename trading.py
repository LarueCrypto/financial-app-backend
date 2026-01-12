from flask import Blueprint, jsonify, request
import os

trading_bp = Blueprint('trading', __name__)


@trading_bp.route('/connect', methods=['POST'])
def connect_broker():
    """
    Connect a trading/brokerage account
    
    In production, this would initiate OAuth flow with the broker
    """
    data = request.json
    broker = data.get('broker')
    
    supported_brokers = ['robinhood', 'fidelity', 'td_ameritrade', 'etrade', 'schwab', 'webull']
    
    if not broker:
        return jsonify({
            'success': False,
            'error': 'broker name is required'
        }), 400
    
    if broker.lower() not in supported_brokers:
        return jsonify({
            'success': False,
            'error': f'Unsupported broker. Supported: {", ".join(supported_brokers)}'
        }), 400
    
    # In production: initiate OAuth flow
    # For now, return mock connection
    return jsonify({
        'success': True,
        'broker': broker,
        'message': f'Connected to {broker} successfully',
        'access_token': f'mock_{broker}_token_123'
    }), 200


@trading_bp.route('/portfolio/<access_token>', methods=['GET'])
def get_portfolio(access_token):
    """
    Get portfolio data for connected broker account
    """
    if not access_token:
        return jsonify({
            'success': False,
            'error': 'access_token is required'
        }), 400
    
    # Mock portfolio data (realistic)
    holdings = [
        {
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'quantity': 15,
            'avg_cost': 178.50,
            'current_price': 185.92,
            'market_value': 2788.80,
            'gain_loss': 111.30,
            'gain_loss_percent': 4.16,
            'type': 'stock'
        },
        {
            'symbol': 'MSFT',
            'name': 'Microsoft Corporation',
            'quantity': 10,
            'avg_cost': 380.00,
            'current_price': 415.50,
            'market_value': 4155.00,
            'gain_loss': 355.00,
            'gain_loss_percent': 9.34,
            'type': 'stock'
        },
        {
            'symbol': 'GOOGL',
            'name': 'Alphabet Inc.',
            'quantity': 8,
            'avg_cost': 140.25,
            'current_price': 152.30,
            'market_value': 1218.40,
            'gain_loss': 96.40,
            'gain_loss_percent': 8.59,
            'type': 'stock'
        },
        {
            'symbol': 'SPY',
            'name': 'SPDR S&P 500 ETF',
            'quantity': 20,
            'avg_cost': 450.00,
            'current_price': 478.25,
            'market_value': 9565.00,
            'gain_loss': 565.00,
            'gain_loss_percent': 6.28,
            'type': 'etf'
        },
        {
            'symbol': 'QQQ',
            'name': 'Invesco QQQ Trust',
            'quantity': 12,
            'avg_cost': 390.00,
            'current_price': 425.80,
            'market_value': 5109.60,
            'gain_loss': 429.60,
            'gain_loss_percent': 9.18,
            'type': 'etf'
        },
        {
            'symbol': 'VTI',
            'name': 'Vanguard Total Stock Market ETF',
            'quantity': 25,
            'avg_cost': 220.00,
            'current_price': 245.30,
            'market_value': 6132.50,
            'gain_loss': 632.50,
            'gain_loss_percent': 11.50,
            'type': 'etf'
        }
    ]
    
    # Calculate totals
    total_value = sum(h['market_value'] for h in holdings)
    total_cost = sum(h['quantity'] * h['avg_cost'] for h in holdings)
    total_gain = total_value - total_cost
    
    # Asset allocation
    allocation = {}
    for h in holdings:
        asset_type = h['type']
        if asset_type not in allocation:
            allocation[asset_type] = 0
        allocation[asset_type] += h['market_value']
    
    # Convert to percentages
    allocation_percent = {k: round(v / total_value * 100, 1) for k, v in allocation.items()}
    
    # Day change (mock)
    day_change = 234.50
    day_change_percent = 0.52
    
    return jsonify({
        'success': True,
        'portfolio': {
            'total_value': round(total_value, 2),
            'total_cost': round(total_cost, 2),
            'total_gain_loss': round(total_gain, 2),
            'total_gain_loss_percent': round(total_gain / total_cost * 100, 2),
            'day_change': day_change,
            'day_change_percent': day_change_percent,
            'cash_balance': 1250.00
        },
        'holdings': holdings,
        'allocation': allocation_percent
    }), 200


@trading_bp.route('/aggregate', methods=['POST'])
def aggregate_portfolios():
    """
    Aggregate multiple broker portfolios into one view
    """
    data = request.json
    tokens = data.get('tokens', [])  # List of {broker, token} objects
    
    if not tokens:
        return jsonify({
            'success': False,
            'error': 'No broker tokens provided'
        }), 400
    
    # In production, would fetch from each broker and combine
    # For now, return combined mock data
    
    return jsonify({
        'success': True,
        'aggregated': {
            'total_value': 45230.00,
            'total_gain_loss': 3420.50,
            'brokers_connected': len(tokens),
            'holdings_count': 12
        }
    }), 200


@trading_bp.route('/transfer', methods=['POST'])
def initiate_transfer():
    """
    Initiate a fund transfer (UI only - redirects to broker)
    """
    data = request.json
    from_account = data.get('from_account')
    to_account = data.get('to_account')
    amount = data.get('amount')
    
    if not all([from_account, to_account, amount]):
        return jsonify({
            'success': False,
            'error': 'from_account, to_account, and amount are required'
        }), 400
    
    # In production: would redirect to broker's transfer page
    return jsonify({
        'success': True,
        'message': 'Transfer initiated. You will be redirected to complete the transfer.',
        'transfer': {
            'from': from_account,
            'to': to_account,
            'amount': amount,
            'status': 'pending',
            'redirect_url': f'https://broker.example.com/transfer?amount={amount}'
        }
    }), 200
