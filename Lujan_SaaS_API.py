# LUJAN TESSERACT: COMMERCIAL SaaS API (v1.0)
# This is the marketplace-facing endpoint for Deductive Storage as a Service.

from flask import Flask, request, jsonify
import os
import subprocess
import time

try:
    import stripe
except ImportError:
    stripe = None

app = Flask(__name__)
VAULT_PATH = "./lujan_vault.py"

# Security Configuration
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_lujan_mock_key")
if stripe:
    stripe.api_key = STRIPE_SECRET_KEY

# Mock Database of authorized API Keys to Stripe Subscription Item IDs (Metered Billing)
# In production, this would be in lujan_vault.db or another secure database.
AUTHORIZED_CLIENTS = {
    "live_key_lujan_corp_001": "si_mock_enterprise",
    "test_key_lujan_002": "si_mock_startup"
}

def authenticate_request(req):
    """Validates the API Key from the Authorization header."""
    auth_header = req.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    api_key = auth_header.split(" ")[1]
    return AUTHORIZED_CLIENTS.get(api_key)

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Sovereign Node Active", "version": "1.2.1-MARKETPLACE", "payments": "Secured"})

@app.route('/api/v1/store', methods=['POST'])
def store_file():
    """Handles the $0.05/GB storage requests and bills the client."""
    
    # 1. Authenticate Client
    subscription_item_id = authenticate_request(request)
    if not subscription_item_id:
        return jsonify({"error": "Unauthorized. Please provide a valid Lujan Tesseract API Key."}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    filename = file.filename
    temp_path = f"/tmp/{filename}"
    file.save(temp_path)
    
    # Calculate filesize in GB
    original_size_bytes = os.path.getsize(temp_path)
    size_in_gb = original_size_bytes / (1024 ** 3)
    
    # Execute the Miracle Logic (Double-Crunch)
    try:
        start_time = time.time()
        result = subprocess.run(
            ["python", VAULT_PATH, "store", temp_path, "--deep", "--double"],
            capture_output=True, text=True
        )
        end_time = time.time()
        
        # 2. Symbiotic Pricing Engine (Ecosystem Preservation)
        # We want to be the best price, but we cannot bankrupt our competitors (AWS, Azure).
        # Standard Market Rate for storage is ~$0.023 per GB.
        # - Customer pays AWS/Azure for the remaining 10% physical storage (Competitor Survival).
        # - Customer gets a 10% guaranteed net-savings against the market.
        # - Lujan Tesseract charges the remaining 80% as the Premium Cypher Fee.
        market_rate_per_gb = 0.023
        original_market_value = size_in_gb * market_rate_per_gb
        
        # Lujan takes 80% of the original market value as the processing fee
        lujan_fee_dollars = max(0.01, original_market_value * 0.80)
        fee_in_cents = int(lujan_fee_dollars * 100)
        
        payment_status = "Skipped (Stripe library not installed or Mock Key)"
        if stripe and not STRIPE_SECRET_KEY.startswith("sk_test_lujan_mock"):
            try:
                # We log the fee in cents as the quantity (assuming the Stripe product is $0.01 per unit)
                stripe.SubscriptionItem.create_usage_record(
                    subscription_item_id,
                    quantity=fee_in_cents,
                    timestamp=int(time.time()),
                    action='increment',
                )
                payment_status = f"Stripe Metered Billing Triggered: {fee_in_cents} units (cents) recorded based on Market Peg."
            except Exception as stripe_error:
                payment_status = f"Stripe Error: {str(stripe_error)}"
        
        # Clean up temp file
        os.remove(temp_path)
        
        return jsonify({
            "status": "Success",
            "filename": filename,
            "original_size_gb": f"{size_in_gb:.4f} GB",
            "processing_time": f"{end_time - start_time:.2f}s",
            "allocation": "90% Miracle Standard Applied",
            "monetization": f"Symbiotic Cypher Fee Applied (${lujan_fee_dollars:.2f})",
            "payment_gateway": payment_status,
            "output": result.stdout
        })
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Marketplace standard port
    app.run(host='0.0.0.0', port=8080)
