from flask import Blueprint, jsonify, request
import requests
import os

blockchain_bp = Blueprint('blockchain', __name__)

# API Keys
ETHERSCAN_KEY = os.getenv('ETHERSCAN_API_KEY', '')
ALCHEMY_KEY = os.getenv('ALCHEMY_API_KEY', '')
POLYGONSCAN_KEY = os.getenv('POLYGONSCAN_API_KEY', '')


def get_eth_balance(address):
    """Get ETH balance from Etherscan"""
    try:
        url = "https://api.etherscan.io/api"
        params = {
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest',
            'apikey': ETHERSCAN_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('status') == '1':
            balance_wei = int(data['result'])
            balance_eth = balance_wei / 1e18
            return {
                'chain': 'Ethereum',
                'symbol': 'ETH',
                'balance': balance_eth,
                'balance_raw': balance_wei
            }
    except Exception as e:
        print(f"Etherscan error: {e}")
    return None


def get_polygon_balance(address):
    """Get MATIC balance from Polygonscan"""
    try:
        url = "https://api.polygonscan.com/api"
        params = {
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest',
            'apikey': POLYGONSCAN_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('status') == '1':
            balance_wei = int(data['result'])
            balance_matic = balance_wei / 1e18
            return {
                'chain': 'Polygon',
                'symbol': 'MATIC',
                'balance': balance_matic,
                'balance_raw': balance_wei
            }
    except Exception as e:
        print(f"Polygonscan error: {e}")
    return None


def get_eth_tokens(address):
    """Get ERC-20 token balances from Etherscan"""
    try:
        url = "https://api.etherscan.io/api"
        params = {
            'module': 'account',
            'action': 'tokentx',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'desc',
            'apikey': ETHERSCAN_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        tokens = {}
        if data.get('status') == '1' and data.get('result'):
            for tx in data['result'][:50]:  # Limit to recent 50 transactions
                token_symbol = tx.get('tokenSymbol', 'UNKNOWN')
                token_name = tx.get('tokenName', 'Unknown Token')
                if token_symbol not in tokens:
                    tokens[token_symbol] = {
                        'symbol': token_symbol,
                        'name': token_name,
                        'contract': tx.get('contractAddress', ''),
                        'decimals': int(tx.get('tokenDecimal', 18))
                    }
        return list(tokens.values())
    except Exception as e:
        print(f"Token fetch error: {e}")
    return []


def get_defi_positions(address):
    """Get DeFi positions (simplified - would need protocol-specific APIs)"""
    # This is a simplified version - real implementation would query:
    # - Aave subgraph
    # - Uniswap subgraph
    # - Curve API
    # - Compound API
    # For now, return empty array (can be expanded later)
    
    positions = []
    
    # Example structure for when you add real DeFi integrations:
    # positions.append({
    #     'protocol': 'Aave',
    #     'type': 'lending',
    #     'asset': 'USDC',
    #     'balance': 1000.00,
    #     'apy': 3.5
    # })
    
    return positions


@blockchain_bp.route('/wallet/<address>', methods=['GET'])
def get_wallet_assets(address):
    """
    Get all assets for a wallet across multiple chains
    
    Returns:
        - Native balances (ETH, MATIC, etc.)
        - Token holdings
        - DeFi positions
    """
    if not address or len(address) != 42 or not address.startswith('0x'):
        return jsonify({
            'success': False,
            'error': 'Invalid wallet address. Must be 42 characters starting with 0x'
        }), 400
    
    try:
        # Fetch data from multiple chains
        eth_balance = get_eth_balance(address)
        polygon_balance = get_polygon_balance(address)
        tokens = get_eth_tokens(address)
        defi = get_defi_positions(address)
        
        # Compile native balances
        native_balances = []
        if eth_balance:
            native_balances.append(eth_balance)
        if polygon_balance:
            native_balances.append(polygon_balance)
        
        return jsonify({
            'success': True,
            'wallet': address,
            'assets': {
                'native_balances': native_balances,
                'tokens': tokens,
                'defi_positions': defi
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@blockchain_bp.route('/wallet/<address>/defi', methods=['GET'])
def get_wallet_defi(address):
    """Get only DeFi positions for a wallet"""
    if not address or len(address) != 42:
        return jsonify({
            'success': False,
            'error': 'Invalid wallet address'
        }), 400
    
    try:
        positions = get_defi_positions(address)
        return jsonify({
            'success': True,
            'wallet': address,
            'defi_positions': positions
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
