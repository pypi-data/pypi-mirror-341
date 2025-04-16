# Integration Guide

This guide explains how to integrate LlamaSearch Experimental Agents: Product Growth with other systems and frameworks.

## Table of Contents
- [Python Integration](#python-integration)
- [Web Applications](#web-applications)
- [Data Pipelines](#data-pipelines)
- [External APIs](#external-apis)
- [Continuous Integration](#continuous-integration)

## Python Integration

### Basic Import

The core functionality can be easily imported into any Python project:

```python
from llamasearch_experimentalagents_product_growth.core import (
    complete_prompt, 
    chat_completion, 
    analyze_text, 
    generate_strategies
)
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMProvider
```

### As a Library

When integrating as a library, first install the package in your project:

```bash
pip install llamasearch-experimentalagents-product-growth
```

Example usage in your Python application:

```python
import pandas as pd
from llamasearch_experimentalagents_product_growth.core import analyze_text
from llamasearch_experimentalagents_product_growth.models import GrowthRecommendation

# Load your customer feedback data
feedback_df = pd.read_csv("customer_feedback.csv")

# Analyze feedback
analysis_results = analyze_text(
    text=feedback_df["feedback_text"].tolist(),
    analysis_type="sentiment_themes",
    provider=LLMProvider.OPENAI
)

# Work with the results in your application
for theme in analysis_results["themes"]:
    print(f"Theme: {theme['name']}, Sentiment: {theme['sentiment']}")
    
# Generate growth recommendations based on analysis
recommendations = generate_strategies(
    feedback_analysis=analysis_results,
    max_strategies=5
)

# Process recommendations in your application
for rec in recommendations:
    if isinstance(rec, GrowthRecommendation):
        print(f"Priority: {rec.priority.name}, Title: {rec.title}")
        print(f"Expected Impact: {rec.expected_impact}")
```

## Web Applications

### Flask Integration

Example of integrating with a Flask application:

```python
from flask import Flask, request, jsonify
from llamasearch_experimentalagents_product_growth.core import (
    analyze_text, 
    generate_strategies,
    LLMProvider
)

app = Flask(__name__)

@app.route('/api/analyze-feedback', methods=['POST'])
def analyze_feedback():
    data = request.json
    
    if not data or 'feedback' not in data:
        return jsonify({'error': 'Missing feedback data'}), 400
        
    feedback_text = data['feedback']
    provider = LLMProvider.ANTHROPIC if 'provider' in data and data['provider'].lower() == 'anthropic' else LLMProvider.OPENAI
    
    try:
        analysis = analyze_text(
            text=feedback_text,
            analysis_type=data.get('analysis_type', 'sentiment_themes'),
            provider=provider
        )
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@app.route('/api/generate-strategies', methods=['POST'])
def create_strategies():
    data = request.json
    
    if not data or 'analysis' not in data:
        return jsonify({'error': 'Missing analysis data'}), 400
        
    try:
        strategies = generate_strategies(
            feedback_analysis=data['analysis'],
            max_strategies=data.get('max_strategies', 5)
        )
        return jsonify([s.to_dict() for s in strategies])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Integration

Example of integrating with a FastAPI application:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from llamasearch_experimentalagents_product_growth.core import (
    analyze_text, 
    generate_strategies
)
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMProvider

app = FastAPI()

class FeedbackRequest(BaseModel):
    feedback: List[str]
    analysis_type: Optional[str] = "sentiment_themes"
    provider: Optional[str] = "openai"

class StrategyRequest(BaseModel):
    analysis: dict
    max_strategies: Optional[int] = 5

@app.post("/api/analyze-feedback")
async def analyze_feedback(request: FeedbackRequest):
    provider = LLMProvider.ANTHROPIC if request.provider.lower() == 'anthropic' else LLMProvider.OPENAI
    
    try:
        analysis = analyze_text(
            text=request.feedback,
            analysis_type=request.analysis_type,
            provider=provider
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-strategies")
async def create_strategies(request: StrategyRequest):
    try:
        strategies = generate_strategies(
            feedback_analysis=request.analysis,
            max_strategies=request.max_strategies
        )
        return [s.to_dict() for s in strategies]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Data Pipelines

### Integration with Airflow

Example of using LlamaSearch in an Airflow DAG:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import json
from llamasearch_experimentalagents_product_growth.core import (
    analyze_text,
    generate_strategies
)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_feedback(**kwargs):
    # Extract feedback data from your source
    df = pd.read_csv('/path/to/feedback/data.csv')
    return df['feedback_text'].tolist()

def analyze_feedback(**kwargs):
    ti = kwargs['ti']
    feedback = ti.xcom_pull(task_ids='extract_feedback')
    
    analysis = analyze_text(
        text=feedback,
        analysis_type="sentiment_themes"
    )
    
    # Save analysis results
    with open('/path/to/output/analysis.json', 'w') as f:
        json.dump(analysis, f)
    
    return analysis

def generate_growth_strategies(**kwargs):
    ti = kwargs['ti']
    analysis = ti.xcom_pull(task_ids='analyze_feedback')
    
    strategies = generate_strategies(
        feedback_analysis=analysis,
        max_strategies=10
    )
    
    # Save strategies
    with open('/path/to/output/strategies.json', 'w') as f:
        json.dump([s.to_dict() for s in strategies], f)

with DAG('customer_feedback_analysis', default_args=default_args, schedule_interval=timedelta(days=7)) as dag:
    task1 = PythonOperator(
        task_id='extract_feedback',
        python_callable=extract_feedback,
    )
    
    task2 = PythonOperator(
        task_id='analyze_feedback',
        python_callable=analyze_feedback,
    )
    
    task3 = PythonOperator(
        task_id='generate_growth_strategies',
        python_callable=generate_growth_strategies,
    )
    
    task1 >> task2 >> task3
```

## External APIs

### Webhook Integration

Example of creating a webhook that processes feedback and returns growth strategies:

```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import os
from llamasearch_experimentalagents_product_growth.core import (
    analyze_text,
    generate_strategies
)

app = Flask(__name__)

# Secret key for webhook verification
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')

def verify_signature(request_data, signature_header):
    """Verify the incoming webhook signature"""
    computed_signature = hmac.new(
        key=WEBHOOK_SECRET.encode(),
        msg=request_data,
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature_header)

@app.route('/webhook/feedback', methods=['POST'])
def webhook_feedback():
    # Verify the webhook signature
    signature = request.headers.get('X-Signature')
    if not signature or not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    data = request.json
    
    # Process the webhook data
    feedback = data.get('feedback', [])
    
    # Analyze feedback
    analysis = analyze_text(
        text=feedback,
        analysis_type="sentiment_themes"
    )
    
    # Generate strategies based on analysis
    strategies = generate_strategies(
        feedback_analysis=analysis,
        max_strategies=5
    )
    
    # Return the results
    return jsonify({
        'analysis': analysis,
        'strategies': [s.to_dict() for s in strategies]
    })

if __name__ == '__main__':
    app.run(debug=True)
```

## Continuous Integration

### GitHub Actions Integration

Example `.github/workflows/analyze-feedback.yml` file:

```yaml
name: Analyze Customer Feedback

on:
  schedule:
    - cron: '0 0 * * 1'  # Run every Monday at midnight
  workflow_dispatch:  # Allow manual triggering

jobs:
  analyze:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install llamasearch-experimentalagents-product-growth
        pip install pandas
        
    - name: Fetch latest feedback data
      run: |
        # Script to fetch the latest feedback data
        python scripts/fetch_feedback.py
      env:
        API_KEY: ${{ secrets.DATA_API_KEY }}
        
    - name: Analyze feedback and generate strategies
      run: |
        python -c "
import pandas as pd
import json
from llamasearch_experimentalagents_product_growth.core import analyze_text, generate_strategies

# Load feedback data
df = pd.read_csv('data/latest_feedback.csv')

# Analyze feedback
analysis = analyze_text(
    text=df['feedback'].tolist(),
    analysis_type='sentiment_themes'
)

# Save analysis results
with open('results/analysis.json', 'w') as f:
    json.dump(analysis, f)

# Generate growth strategies
strategies = generate_strategies(
    feedback_analysis=analysis,
    max_strategies=10
)

# Save strategies
with open('results/strategies.json', 'w') as f:
    json.dump([s.to_dict() for s in strategies], f)
        "
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        
    - name: Create report
      run: |
        # Script to create a summary report
        python scripts/create_report.py
        
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: feedback-analysis-results
        path: |
          results/analysis.json
          results/strategies.json
          results/report.pdf
```

## Best Practices for Integration

1. **Environment Variables**: Always use environment variables for sensitive information like API keys.

2. **Error Handling**: Implement proper error handling for API calls to LLM providers, which can occasionally fail.

3. **Rate Limiting**: Implement rate limiting when making multiple calls to the LLM services to avoid hitting API limits.

4. **Caching**: Consider implementing caching for LLM responses when appropriate to reduce costs and response times.

5. **Asynchronous Processing**: For web applications, consider using asynchronous processing for long-running LLM operations.

6. **Monitoring**: Implement monitoring for LLM API calls to track usage, costs, and errors.

7. **Versioning**: When integrating, specify the package version to ensure compatibility:

   ```bash
   pip install llamasearch-experimentalagents-product-growth==0.1.0
   ```

## Need More Help?

For more details, refer to the [API Reference](api_reference.md) document or reach out to our support team. 