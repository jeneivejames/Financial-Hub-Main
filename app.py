from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import Database
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
db = Database()

# ========== HOME PAGE ==========
@app.route('/')
def index():
    try:
        requests_data = db.get_all_requests()
        quotes = db.get_all_quotes()
        random_quote = random.choice(quotes) if quotes else {'text': 'Together we can make a difference', 'author': 'Anonymous'}
        
        user = None
        if 'user_id' in session:
            user = db.get_user_by_id(session['user_id'])
        
        return render_template('index.html', 
                             requests=requests_data, 
                             quote=random_quote,
                             user=user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== AUTHENTICATION ==========
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        phone = data.get('phone')
        
        # Check if user exists
        existing = db.get_user_by_email(email)
        if existing:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create user
        password_hash = generate_password_hash(password)
        user = db.create_user({
            'email': email,
            'password_hash': password_hash,
            'full_name': full_name,
            'phone': phone,
            'role': 'user'
        })
        
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        session['user_role'] = user['role']
        
        return jsonify({'success': True, 'user': user})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        user = db.get_user_by_email(email)
        if not user or not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        session['user_role'] = user['role']
        
        return jsonify({'success': True, 'user': {'email': user['email'], 'full_name': user['full_name'], 'role': user['role']}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# ========== REQUEST SUBMISSION ==========
@app.route('/api/submit-request', methods=['POST'])
def submit_request():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Please login first'}), 401
        
        data = request.json
        request_data = {
            'name': data.get('name'),
            'age': data.get('age'),
            'district_id': data.get('district_id'),
            'category_id': data.get('category_id'),
            'amount': data.get('amount'),
            'description': data.get('description'),
            'user_id': session['user_id'],
            'approval_status': 'pending'  # Needs admin approval
        }
        
        new_request = db.create_request(request_data)
        return jsonify({'success': True, 'request': new_request})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DONATION ==========
@app.route('/api/donate', methods=['POST'])
def donate():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Please login first'}), 401
        
        data = request.json
        payment_data = {
            'request_id': data.get('request_id'),
            'donor_id': session['user_id'],
            'amount': data.get('amount'),
            'payment_method': data.get('payment_method', 'bank_transfer'),
            'donor_bank_details': data.get('donor_bank_details'),
            'payment_status': 'completed'
        }
        
        payment = db.create_payment(payment_data)
        
        # Update request total_received
        help_request = db.get_request_by_id(data.get('request_id'))
        new_total = float(help_request.get('total_received', 0)) + float(data.get('amount'))
        db.update_request(data.get('request_id'), {'total_received': new_total})
        
        return jsonify({'success': True, 'payment': payment})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== ADMIN ROUTES ==========
@app.route('/api/admin/approve-request/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    try:
        if 'user_id' not in session or session.get('user_role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        db.update_request(request_id, {
            'approval_status': 'approved',
            'approved_by': session['user_id']
        })
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/reject-request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    try:
        if 'user_id' not in session or session.get('user_role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.json
        db.update_request(request_id, {
            'approval_status': 'rejected',
            'rejection_reason': data.get('reason')
        })
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DATA ENDPOINTS ==========
@app.route('/api/districts')
def get_districts():
    districts = db.get_all_districts()
    return jsonify(districts)

@app.route('/api/categories')
def get_categories():
    categories = db.get_all_categories()
    return jsonify(categories)

@app.route('/api/quotes')
def get_quotes():
    quotes = db.get_all_quotes()
    return jsonify(quotes)

@app.route('/api/request/<int:request_id>')
def get_request(request_id):
    help_request = db.get_request_by_id(request_id)
    payments = db.get_payments_for_request(request_id)
    return jsonify({'request': help_request, 'payments': payments})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
