#!/usr/bin/env python3
"""
Simple HTTP Server for JD Management System
This server can run without external dependencies and serves the frontend
"""

import json
import sqlite3
import os
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import mimetypes

class JDRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for JD Management System"""
    
    def __init__(self, *args, **kwargs):
        # Initialize SQLite database
        self.init_database()
        super().__init__(*args, **kwargs)
    
    def init_database(self):
        """Initialize SQLite database with tables"""
        try:
            # Create database directory if it doesn't exist
            os.makedirs('database', exist_ok=True)
            self.conn = sqlite3.connect('database/rectool.db')  # Persistent database file
            self.cursor = self.conn.cursor()
            
            # Create job_descriptions table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS job_descriptions (
                    jd_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jd_title TEXT NOT NULL,
                    primary_skill TEXT NOT NULL,
                    secondary_skills TEXT,
                    mode TEXT NOT NULL,
                    tenure_months INTEGER NOT NULL,
                    open_positions INTEGER NOT NULL,
                    available_positions INTEGER NOT NULL,
                    experience_min REAL,
                    experience_max REAL,
                    budget_min REAL,
                    budget_max REAL,
                    jd_keywords TEXT,
                    original_jd TEXT,
                    special_instruction TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert sample data
            self.cursor.execute('''
                INSERT OR IGNORE INTO job_descriptions 
                (jd_title, primary_skill, secondary_skills, mode, tenure_months, open_positions, available_positions, experience_min, experience_max, budget_min, budget_max, jd_keywords, original_jd, special_instruction)
                VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Senior React Developer',
                'ReactJS',
                'NodeJS, MySQL, TypeScript',
                'Hybrid',
                12,
                5,
                3,
                3.0,
                5.0,
                60000.00,
                90000.00,
                'React, JavaScript, Frontend',
                'We are looking for a Senior React Developer to join our dynamic team.',
                'Candidate must join within 30 days.'
            ))
            
            self.conn.commit()
            print("✅ Database initialized with sample data")
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Health check endpoint
        if path == '/health':
            self.send_json_response({'status': 'healthy', 'service': 'jd-management-api'})
            return
        
        # API endpoints
        if path.startswith('/api/'):
            self.handle_api_request(parsed_url)
            return
        
        # Serve static files
        self.serve_static_file(path)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/api/jd/':
            self.handle_create_jd()
        else:
            self.send_error(404, "Endpoint not found")
    
    def handle_api_request(self, parsed_url):
        """Handle API requests"""
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        if path == '/api/jd/':
            self.handle_get_all_jds(query_params)
        elif path.startswith('/api/jd/') and path != '/api/jd/':
            jd_id = path.split('/')[-1]
            if jd_id.isdigit():
                self.handle_get_jd_by_id(int(jd_id))
            else:
                self.send_error(400, "Invalid JD ID")
        elif path == '/api/jd/statistics':
            self.handle_get_statistics()
        else:
            self.send_error(404, "API endpoint not found")
    
    def handle_get_all_jds(self, query_params):
        """Get all job descriptions with optional search"""
        try:
            search = query_params.get('search', [''])[0]
            page = int(query_params.get('page', ['1'])[0])
            per_page = int(query_params.get('per_page', ['10'])[0])
            
            if search:
                query = '''
                    SELECT * FROM job_descriptions 
                    WHERE jd_title LIKE ? OR primary_skill LIKE ? OR jd_keywords LIKE ?
                    ORDER BY created_at DESC
                '''
                search_term = f'%{search}%'
                self.cursor.execute(query, (search_term, search_term, search_term))
            else:
                query = 'SELECT * FROM job_descriptions ORDER BY created_at DESC'
                self.cursor.execute(query)
            
            all_jds = self.cursor.fetchall()
            
            # Pagination
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_jds = all_jds[start_idx:end_idx]
            
            # Convert to list of dictionaries
            jds_list = []
            for jd in paginated_jds:
                jds_list.append({
                    'jd_id': jd[0],
                    'jd_title': jd[1],
                    'primary_skill': jd[2],
                    'secondary_skills': jd[3],
                    'mode': jd[4],
                    'tenure_months': jd[5],
                    'open_positions': jd[6],
                    'available_positions': jd[7],
                    'experience_min': jd[8],
                    'experience_max': jd[9],
                    'budget_min': jd[10],
                    'budget_max': jd[11],
                    'jd_keywords': jd[12],
                    'original_jd': jd[13],
                    'special_instruction': jd[14],
                    'created_at': jd[15]
                })
            
            response = {
                'success': True,
                'data': jds_list,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': len(all_jds),
                    'pages': (len(all_jds) + per_page - 1) // per_page
                }
            }
            
            self.send_json_response(response)
            
        except Exception as e:
            self.send_error(500, f"Database error: {str(e)}")
    
    def handle_get_jd_by_id(self, jd_id):
        """Get job description by ID"""
        try:
            self.cursor.execute('SELECT * FROM job_descriptions WHERE jd_id = ?', (jd_id,))
            jd = self.cursor.fetchone()
            
            if jd:
                jd_dict = {
                    'jd_id': jd[0],
                    'jd_title': jd[1],
                    'primary_skill': jd[2],
                    'secondary_skills': jd[3],
                    'mode': jd[4],
                    'tenure_months': jd[5],
                    'open_positions': jd[6],
                    'available_positions': jd[7],
                    'experience_min': jd[8],
                    'experience_max': jd[9],
                    'budget_min': jd[10],
                    'budget_max': jd[11],
                    'jd_keywords': jd[12],
                    'original_jd': jd[13],
                    'special_instruction': jd[14],
                    'created_at': jd[15]
                }
                self.send_json_response({'success': True, 'data': jd_dict})
            else:
                self.send_error(404, "Job description not found")
                
        except Exception as e:
            self.send_error(500, f"Database error: {str(e)}")
    
    def handle_create_jd(self):
        """Create a new job description"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            jd_data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            required_fields = ['jd_title', 'primary_skill', 'mode', 'tenure_months', 'open_positions']
            for field in required_fields:
                if not jd_data.get(field):
                    self.send_error(400, f"Missing required field: {field}")
                    return
            
            # Insert into database
            query = '''
                INSERT INTO job_descriptions 
                (jd_title, primary_skill, secondary_skills, mode, tenure_months, open_positions, available_positions, experience_min, experience_max, budget_min, budget_max, jd_keywords, original_jd, special_instruction)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            values = (
                jd_data.get('jd_title'),
                jd_data.get('primary_skill'),
                jd_data.get('secondary_skills', ''),
                jd_data.get('mode'),
                int(jd_data.get('tenure_months')),
                int(jd_data.get('open_positions')),
                int(jd_data.get('available_positions', 0)),
                float(jd_data.get('experience_min')) if jd_data.get('experience_min') else None,
                float(jd_data.get('experience_max')) if jd_data.get('experience_max') else None,
                float(jd_data.get('budget_min')) if jd_data.get('budget_min') else None,
                float(jd_data.get('budget_max')) if jd_data.get('budget_max') else None,
                jd_data.get('jd_keywords', ''),
                jd_data.get('original_jd', ''),
                jd_data.get('special_instruction', '')
            )
            
            self.cursor.execute(query, values)
            self.conn.commit()
            
            new_jd_id = self.cursor.lastrowid
            response = {
                'success': True,
                'data': {'jd_id': new_jd_id},
                'message': 'Job description created successfully'
            }
            
            self.send_json_response(response, status_code=201)
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON data")
        except ValueError as e:
            self.send_error(400, f"Invalid data: {str(e)}")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
    
    def handle_get_statistics(self):
        """Get job description statistics"""
        try:
            # Total jobs
            self.cursor.execute('SELECT COUNT(*) FROM job_descriptions')
            total_jobs = self.cursor.fetchone()[0]
            
            # Jobs by mode
            self.cursor.execute('SELECT mode, COUNT(*) FROM job_descriptions GROUP BY mode')
            mode_counts = dict(self.cursor.fetchall())
            
            # Total positions
            self.cursor.execute('SELECT SUM(open_positions), SUM(available_positions) FROM job_descriptions')
            positions = self.cursor.fetchone()
            total_open = positions[0] or 0
            total_available = positions[1] or 0
            
            # Average tenure
            self.cursor.execute('SELECT AVG(tenure_months) FROM job_descriptions')
            avg_tenure = self.cursor.fetchone()[0] or 0
            
            stats = {
                'total_jobs': total_jobs,
                'remote_jobs': mode_counts.get('Remote', 0),
                'onsite_jobs': mode_counts.get('Onsite', 0),
                'hybrid_jobs': mode_counts.get('Hybrid', 0),
                'total_open_positions': total_open,
                'total_available_positions': total_available,
                'avg_tenure_months': round(avg_tenure, 1)
            }
            
            self.send_json_response({'success': True, 'data': stats})
            
        except Exception as e:
            self.send_error(500, f"Database error: {str(e)}")
    
    def serve_static_file(self, path):
        """Serve static files from the frontend directory"""
        if path == '/':
            path = '/index.html'
        
        # Map API routes to frontend routes
        if path.startswith('/api/'):
            path = '/index.html'
        
        # Try to serve from frontend directory
        frontend_path = os.path.join('..', 'frontend', 'public')
        file_path = os.path.join(frontend_path, path.lstrip('/'))
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Determine content type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # Fallback to index.html for SPA routing
            index_path = os.path.join(frontend_path, 'index.html')
            if os.path.exists(index_path):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                with open(index_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"🌐 {format % args}")

def run_server(port=8000):
    """Run the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, JDRequestHandler)
    
    print(f"🚀 JD Management Server starting on port {port}")
    print(f"📱 Frontend: http://localhost:{port}")
    print(f"🔌 API: http://localhost:{port}/api/")
    print(f"💚 Health: http://localhost:{port}/health")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == '__main__':
    run_server() 