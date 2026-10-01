from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import Database
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
import random

# Set up template folder for both Databricks and Vercel
# Vercel uses /var/task/, Databricks uses regular paths
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

# Debug: Print available paths (visible in Vercel logs)
if os.path.exists('/var/task'):
    print(f"[DEBUG] Running in Vercel. Current dir: {current_dir}", file=sys.stderr)
    print(f"[DEBUG] Template dir: {template_dir}", file=sys.stderr)
    print(f"[DEBUG] Template dir exists: {os.path.exists(template_dir)}", file=sys.stderr)
    if os.path.exists(current_dir):
        print(f"[DEBUG] Files in current dir: {os.listdir(current_dir)}", file=sys.stderr)

app = Flask(__name__, template_folder=template_dir)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
db = Database()

# ========== ADMIN LOGIN PAGE ==========
@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        # Hardcoded admin credentials
        if username == 'admin' and password == 'James030!':
            session['admin_logged_in'] = True
            session['admin_username'] = 'admin'
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid admin credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return jsonify({'success': True})

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
        
        try:
            # Try Flask's render_template first
            return render_template('index.html', 
                                 requests=requests_data, 
                                 quote=random_quote,
                                 user=user)
        except Exception as template_error:
            # Fallback: Read HTML file directly for Vercel compatibility
            print(f"[DEBUG] Template rendering failed: {template_error}", file=sys.stderr)
            template_paths = [
                os.path.join(template_dir, 'index.html'),
                os.path.join(os.path.dirname(__file__), 'templates', 'index.html'),
                'templates/index.html',
                '/var/task/templates/index.html'
            ]
            
            for path in template_paths:
                print(f"[DEBUG] Trying path: {path}, exists: {os.path.exists(path)}", file=sys.stderr)
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        html_content = f.read()
                    # Simple template variable replacement
                    # Note: This is a basic fallback, not full Jinja2 rendering
                    from flask import Markup
                    return html_content
            
            # If all paths fail, raise the original error
            raise template_error
            
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }), 500

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
        
        # Convert and validate data types
        district_id = data.get('district_id')
        category_id = data.get('category_id')
        amount = data.get('amount')
        
        description = data.get('description', '')
        
        request_data = {
            'name': data.get('name'),
            'district_id': int(float(district_id)) if district_id else None,
            'category_id': int(float(category_id)) if category_id else None,
            'amount_needed': int(float(amount)) if amount else None,
            'description': description,
            'short_description': description[:100] if description else '',  # First 100 chars
            'detailed_message': description,  # Full description
            'user_id': session['user_id'],
            'approval_status': 'pending',
            'status': 'active',  # Changed from 'open' to 'active'
            'total_received': 0
        }
        
        new_request = db.create_request(request_data)
        
        # Save requester bank/UPI details
        receive_method = data.get('receive_method', 'bank_account')
        account_number = data.get('account_number')
        bank_name = data.get('bank_name')
        ifsc_code = data.get('ifsc_code')
        upi_id = data.get('upi_id')
        
        if account_number or bank_name or ifsc_code or upi_id:
            try:
                bank_details_data = {
                    'user_id': session['user_id'],
                    'receive_method': receive_method
                }
                
                if receive_method == 'bank_account':
                    bank_details_data['account_number'] = account_number
                    bank_details_data['bank_name'] = bank_name
                    bank_details_data['ifsc_code'] = ifsc_code
                elif receive_method == 'upi':
                    bank_details_data['upi_id'] = upi_id
                
                db.create_bank_details(bank_details_data)
            except Exception as bank_err:
                print(f'[WARN] Failed to save bank/UPI details: {bank_err}', file=sys.stderr)
        
        return jsonify({'success': True, 'request': new_request})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DONATION ==========
@app.route('/api/donate', methods=['POST'])
def donate():
    try:
        data = request.json
        
        # Guest donation (no login required) or authenticated donation
        donor_id = session.get('user_id')
        donor_name = data.get('donor_name', 'Anonymous')
        donor_email = data.get('donor_email', '')
        
        # Convert types properly
        request_id = data.get('request_id')
        amount = data.get('amount')
        
        payment_data = {
            'request_id': str(request_id),  # Ensure string/UUID format
            'donor_id': donor_id,  # Can be None for guest donations
            'amount': float(amount) if amount else 0,  # Ensure float
            'payment_method': data.get('payment_method', 'bank_transfer'),
            'donor_bank_details': data.get('donor_bank_details'),
            'payment_status': 'pending',  # Changed to pending until verified
            'notes': f'Donor: {donor_name}, Email: {donor_email}' if not donor_id else None
        }
        
        payment = db.create_payment(payment_data)
        
        # Update request total_received
        help_request = db.get_request_by_id(request_id)
        new_total = float(help_request.get('total_received', 0)) + float(amount)
        db.update_request(request_id, {'total_received': new_total})
        
        return jsonify({'success': True, 'payment': payment, 'message': 'Thank you for your donation! 🎉'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== ADMIN ROUTES ==========
@app.route('/api/admin/pending-requests')
def get_pending_requests():
    try:
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get all requests (admin can see all)
        all_requests = db.get_all_requests()
        return jsonify(all_requests)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/approve-request/<request_id>', methods=['POST'])
def approve_request(request_id):
    try:
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'Admin access required'}), 403
        
        db.update_request(request_id, {
            'approval_status': 'approved'
        })
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/reject-request/<request_id>', methods=['POST'])
def reject_request(request_id):
    try:
        if not session.get('admin_logged_in'):
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

# Vercel will handle the app execution
# Expose the app object for WSGI
if __name__ == '__main__':
    # For Databricks Apps: listen on all interfaces
    app.run(host='0.0.0.0', port=8000)
