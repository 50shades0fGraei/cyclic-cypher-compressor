#!/usr/bin/env python3
# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.

import os
import io
import zipfile
from flask import Flask, request, jsonify, send_file
import stripe

app = Flask(__name__)

# Security Configuration
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
PRICE_USD = 80.00

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

# ============================================================================
# IN-MEMORY ARTIFACT GENERATOR
# ============================================================================
def generate_artifact_zip():
    """Generates the downloadable artifact purely in-memory (Stateless)."""
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add the core engine and wrapper
        try:
            zf.write("core/cyberdna_engine.py", arcname="core/cyberdna_engine.py")
        except FileNotFoundError:
            pass # Ensure file presence physically, but handle gracefully
            
        try:
            zf.write("double_crunch_marketplace.py", arcname="double_crunch_marketplace.py")
            zf.write("MARKETPLACE_DOUBLE_CRUNCH_README.md", arcname="README.md")
        except FileNotFoundError:
            pass
            
    memory_file.seek(0)
    return memory_file

# ============================================================================
# BEAUTIFUL FRONTEND (Stateless HTML)
# ============================================================================
HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Randall Double Crunch | Purchase</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{
            background: #05050A;
            color: #fff;
            font-family: 'Inter', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        .card {{
            background: #0a0e17;
            border: 1px solid rgba(0,242,255,0.3);
            border-radius: 20px;
            padding: 50px;
            max-width: 500px;
            text-align: center;
            box-shadow: 0 0 60px rgba(0,242,255,0.1);
        }}
        h1 {{
            color: #00f2ff;
            font-weight: 800;
            margin-bottom: 20px;
            letter-spacing: -1px;
        }}
        p {{
            color: #8892b0;
            line-height: 1.6;
            margin-bottom: 30px;
        }}
        .price {{
            font-size: 3rem;
            font-weight: 800;
            color: #fff;
            margin-bottom: 30px;
        }}
        .btn {{
            display: inline-block;
            background: #00f2ff;
            color: #000;
            padding: 16px 40px;
            border-radius: 12px;
            font-weight: 800;
            text-decoration: none;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: none;
            cursor: pointer;
            width: 100%;
            transition: 0.2s;
        }}
        .btn:hover {{
            background: #fff;
        }}
        .legal {{
            font-size: 0.8rem;
            color: #4a5568;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>DOUBLE CRUNCH</h1>
        <p>Unlock the mathematical limit in recursive data consolidation. Instantly collapses structural data streams using the True Cypher Gap Sum Architecture.</p>
        <div class="price">${PRICE_USD:.0f}</div>
        <form action="/create-checkout-session" method="POST">
            <button type="submit" class="btn">Purchase Lifetime License</button>
        </form>
        <div class="legal">One-time purchase. Single-device unmetered royalty.</div>
    </div>
</body>
</html>
"""

# ============================================================================
# ROUTES
# ============================================================================
@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    if not STRIPE_SECRET_KEY:
        return jsonify({"error": "Stripe keys missing on deployment."}), 500
        
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Lujan Randall Double Crunch',
                        'description': 'True Cypher Engine + Command Line Tools (Lifetime License)'
                    },
                    'unit_amount': int(PRICE_USD * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{BASE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{BASE_URL}/?cancelled=1"
        )
        # We redirect directly to Stripe
        from flask import redirect
        return redirect(session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success')
def success():
    session_id = request.args.get('session_id')
    
    if STRIPE_SECRET_KEY:
        try:
            # Verify the payment is deeply authentic
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status != "paid":
                return "Payment not verified.", 403
        except Exception:
            return "Invalid session.", 403
            
    # Serve the ZIP dynamically instantly in-memory
    memory_file = generate_artifact_zip()
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='Lujan_Double_Crunch_Full_Artifact.zip'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
