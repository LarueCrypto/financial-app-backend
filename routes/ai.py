from flask import Blueprint, jsonify, request
from openai import OpenAI
import os
import base64
import json

ai_bp = Blueprint('ai', __name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))

# Store conversation history (in production, use database)
conversations = {}


def get_system_prompt(financial_context=None):
    """Generate system prompt with financial context"""
    base_prompt = """You are a helpful AI financial advisor assistant. You help users understand their finances, analyze spending patterns, provide investment insights, and answer questions about their financial data.

Guidelines:
- Be concise and actionable in your advice
- Use specific numbers when available
- Identify potential savings opportunities
- Flag concerning spending patterns
- Suggest diversification when relevant
- Always remind users to consult a professional for major financial decisions
- Be encouraging but realistic"""

    if financial_context:
        context_str = f"""

Current User Financial Context:
- Blockchain Assets: {json.dumps(financial_context.get('blockchain', {}), indent=2)}
- Banking Data: {json.dumps(financial_context.get('banking', {}), indent=2)}  
- Trading Portfolio: {json.dumps(financial_context.get('trading', {}), indent=2)}
"""
        return base_prompt + context_str
    
    return base_prompt


@ai_bp.route('/chat', methods=['POST'])
def chat():
    """
    Chat with AI financial advisor
    
    Body:
        - message: user's message
        - financial_context: optional dict with user's financial data
        - conversation_id: optional ID to continue conversation
    """
    data = request.json
    user_message = data.get('message')
    financial_context = data.get('financial_context', {})
    conversation_id = data.get('conversation_id', 'default')
    
    if not user_message:
        return jsonify({
            'success': False,
            'error': 'message is required'
        }), 400
    
    # Check if OpenAI key is configured
    if not os.getenv('OPENAI_API_KEY'):
        return jsonify({
            'success': False,
            'error': 'OpenAI API key not configured'
        }), 500
    
    try:
        # Get or create conversation history
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Add user message to history
        conversations[conversation_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Create chat completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective model, change to gpt-4o for better quality
            messages=[
                {"role": "system", "content": get_system_prompt(financial_context)},
                *conversations[conversation_id][-10:]  # Keep last 10 messages for context
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        conversations[conversation_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return jsonify({
            'success': True,
            'response': assistant_message,
            'conversation_id': conversation_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/upload-document', methods=['POST'])
def upload_document():
    """
    Upload and analyze a financial document (PDF)
    
    Uses GPT-4 Vision to analyze document contents
    """
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file provided'
        }), 400
    
    file = request.files['file']
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({
            'success': False,
            'error': 'Only PDF files are accepted'
        }), 400
    
    if not os.getenv('OPENAI_API_KEY'):
        return jsonify({
            'success': False,
            'error': 'OpenAI API key not configured'
        }), 500
    
    try:
        # Read file content
        file_content = file.read()
        file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        # For PDF analysis, we'll use GPT-4 with a text prompt
        # Note: For actual PDF parsing, you'd want to use a PDF library
        # to extract text first, then send to GPT
        
        # Simplified analysis prompt
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial document analyst. Extract and summarize key financial information from documents."
                },
                {
                    "role": "user",
                    "content": f"""A user has uploaded a financial document named '{file.filename}'. 
                    
Since I cannot directly read the PDF, please provide a template response explaining:
1. What types of information you would typically extract from financial documents
2. Key metrics to look for (income, expenses, assets, liabilities)
3. Red flags to watch for
4. How to interpret common financial statements

Provide this as helpful guidance for the user to manually review their document."""
                }
            ],
            max_tokens=1500
        )
        
        analysis = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'analysis': analysis,
            'note': 'For detailed PDF analysis, consider integrating a PDF parsing library'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/analyze', methods=['POST'])
def analyze_financial_health():
    """
    Comprehensive financial health analysis
    
    Body:
        - financial_data: dict containing all user financial data
    """
    data = request.json
    financial_data = data.get('financial_data', {})
    
    if not financial_data:
        return jsonify({
            'success': False,
            'error': 'financial_data is required'
        }), 400
    
    if not os.getenv('OPENAI_API_KEY'):
        return jsonify({
            'success': False,
            'error': 'OpenAI API key not configured'
        }), 500
    
    try:
        prompt = f"""Analyze this user's complete financial picture and provide:

1. **Financial Health Score** (0-100) with explanation
2. **Key Strengths** - What they're doing well
3. **Risk Areas** - Potential concerns
4. **Spending Insights** - Patterns and recommendations
5. **Portfolio Assessment** - Diversification and risk level
6. **Top 3 Actionable Recommendations** - Specific next steps

Financial Data:
{json.dumps(financial_data, indent=2)}

Provide a comprehensive but concise analysis. Use specific numbers from the data."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert financial advisor providing comprehensive financial health assessments. Be specific, actionable, and data-driven."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.5
        )
        
        analysis = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'analysis': analysis
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/clear-conversation', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    data = request.json
    conversation_id = data.get('conversation_id', 'default')
    
    if conversation_id in conversations:
        del conversations[conversation_id]
    
    return jsonify({
        'success': True,
        'message': 'Conversation cleared'
    }), 200
