import os
from supabase import create_client, Client

class Database:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)
    
    # ========== HELP REQUESTS ==========
    def get_all_requests(self):
        # Fetch requests, districts, and categories separately to avoid FK cache issues
        requests_response = self.supabase.table('help_requests').select('*').execute()
        requests = requests_response.data
        
        # Build lookup dicts for districts and categories
        districts = {d['id']: d for d in self.get_all_districts()}
        categories = {c['id']: c for c in self.get_all_categories()}
        
        # Enrich each request with district and category names
        for req in requests:
            district_id = req.get('district_id')
            category_id = req.get('category_id')
            req['districts'] = districts.get(district_id, {'name': 'Unknown'})
            req['categories'] = categories.get(category_id, {'name': 'Unknown'})
        
        return requests
    
    def get_request_by_id(self, request_id):
        response = self.supabase.table('help_requests').select('*').eq('id', request_id).execute()
        if not response.data:
            return None
        req = response.data[0]
        
        # Enrich with district and category names
        districts = {d['id']: d for d in self.get_all_districts()}
        categories = {c['id']: c for c in self.get_all_categories()}
        req['districts'] = districts.get(req.get('district_id'), {'name': 'Unknown'})
        req['categories'] = categories.get(req.get('category_id'), {'name': 'Unknown'})
        
        return req
    
    def create_request(self, data):
        response = self.supabase.table('help_requests').insert(data).execute()
        return response.data[0] if response.data else None
    
    def update_request(self, request_id, data):
        response = self.supabase.table('help_requests').update(data).eq('id', request_id).execute()
        return response.data[0] if response.data else None
    
    # ========== USERS ==========
    def get_user_by_email(self, email):
        response = self.supabase.table('users').select('*').eq('email', email).execute()
        return response.data[0] if response.data else None
    
    def create_user(self, data):
        response = self.supabase.table('users').insert(data).execute()
        return response.data[0] if response.data else None
    
    def get_user_by_id(self, user_id):
        response = self.supabase.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None
    
    # ========== BANK DETAILS ==========
    def get_bank_details_by_user(self, user_id):
        response = self.supabase.table('bank_details').select('*').eq('user_id', user_id).execute()
        return response.data[0] if response.data else None
    
    def create_bank_details(self, data):
        response = self.supabase.table('bank_details').insert(data).execute()
        return response.data[0] if response.data else None
    
    # ========== PAYMENTS ==========
    def create_payment(self, data):
        response = self.supabase.table('payments').insert(data).execute()
        return response.data[0] if response.data else None
    
    def get_payments_for_request(self, request_id):
        response = self.supabase.table('payments').select('*').eq('request_id', request_id).execute()
        return response.data
    
    def update_payment_status(self, payment_id, status):
        response = self.supabase.table('payments').update({'payment_status': status}).eq('id', payment_id).execute()
        return response.data[0] if response.data else None
    
    # ========== QUOTES ==========
    def get_random_quote(self):
        # Get a random quote
        response = self.supabase.table('quotes').select('*').limit(1).execute()
        return response.data[0] if response.data else None
    
    def get_all_quotes(self):
        response = self.supabase.table('quotes').select('*').execute()
        return response.data
    
    # ========== DISTRICTS & CATEGORIES ==========
    def get_all_districts(self):
        response = self.supabase.table('districts').select('*').execute()
        return response.data
    
    def get_all_categories(self):
        response = self.supabase.table('categories').select('*').execute()
        return response.data
