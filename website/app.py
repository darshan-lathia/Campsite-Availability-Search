from flask import Flask, render_template, request, jsonify
import sys
import os
from datetime import datetime
import subprocess
import logging
from werkzeug.exceptions import HTTPException
import traceback
import re  # Add this at the top with other imports
import requests
from math import radians, sin, cos, sqrt, atan2
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
MAPS_API_KEY = os.environ.get('MAPS_API_KEY')
RECREATION_API_KEY = os.environ.get('RECREATION_API_KEY')

# Configure logging with timestamp
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Create timestamp for log file
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(LOG_DIR, f'camping_search_{timestamp}.log')

# Configure file handler
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=1024 * 1024,  # 1MB
    backupCount=10
)

# Configure formatter
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Update paths and environment settings
SCRIPT_DIR = '/Users/darshan/Projects/Camping_Reservation/Camping_Reservation_python_script/'
SCRIPT_NAME = 'camping_notification.py'
VENV_PYTHON = '/Users/darshan/.pyenv/versions/3.12.2/bin/python'

# Global counter for script executions
script_executions = {
    'count': 0,
    'last_executed': None,
    'sessions': set()
}

@app.route('/')
def index():
    return render_template('index.html', MAPS_API_KEY=MAPS_API_KEY)

@app.route('/results')
def results():
    return render_template('results.html', MAPS_API_KEY=MAPS_API_KEY)

@app.route('/about')
def about():
    return render_template('about.html', MAPS_API_KEY=MAPS_API_KEY)

@app.route('/history')
def history():
    return render_template('history.html', MAPS_API_KEY=MAPS_API_KEY)

def read_process_output(process):
    """Read output from process line by line and parse results"""
    results = {
        'priority': [],
        'regular': [],
        'ignored': [],
        'changes': [],
        'campground_name': None
    }
    
    try:
        # Wait for process to complete and get output
        output, error = process.communicate()
        
        # Print raw output to terminal
        print("\n=== Raw Script Output ===")
        print(output)
        if error:
            print("\n=== Script Errors ===")
            print(error)
        
        # Log output
        logger.info("\n=== Raw Script Output ===")
        logger.info(output)
        if error:
            logger.error(f"Script errors: {error}")

        current_section = None
        full_results_started = False
        
        # Process each line
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Debug: Print each line being processed
            print(f"Processing line: {line}")
            
            # Start capturing after Full Results marker
            if "=== Full Results for Reference ===" in line:
                print("Found Full Results marker")
                full_results_started = True
                continue
            
            if not full_results_started:
                continue
            
            # Identify sections
            if "**Priority Results:**" in line:
                print("Entering Priority section")
                current_section = 'priority'
                continue
            elif "**Regular Results:**" in line:
                print("Entering Regular section")
                current_section = 'regular'
                continue
            elif "**Ignored Results:**" in line:
                print("Entering Ignored section")
                current_section = 'ignored'
                continue
            
            # Capture results
            if current_section and "->" in line:
                print(f"Adding result to {current_section}: {line}")
                results[current_section].append({
                    'text': line,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                })
        
        return results
        
    except Exception as e:
        print(f"Error processing output: {str(e)}")
        logger.error(f"Error processing output: {str(e)}")
        raise e

def clean_text(text):
    """Remove ANSI escape codes and other unwanted characters"""
    # Remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)
    
    # Remove other special characters but keep basic punctuation
    text = ''.join(char for char in text if char.isprintable())
    
    return text.strip()

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        
        # Update execution stats
        script_executions['count'] += 1
        script_executions['last_executed'] = datetime.now()
        script_executions['sessions'].add(request.remote_addr)
        
        # Log search parameters and stats
        logger.info("\n=== Search Parameters ===")
        logger.info(f"Park ID: {data.get('parkId')}")
        logger.info(f"Start Date: {data.get('startDate')}")
        logger.info(f"End Date: {data.get('endDate')}")
        logger.info(f"Nights: {data.get('nights')}")
        logger.info(f"Search Preference: {data.get('searchPreference')}")
        logger.info("----------------------------------------")
        logger.info("Session Stats:")
        logger.info(f"Total Searches: {script_executions['count']}")
        logger.info(f"Last Search: {script_executions['last_executed'].strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Unique Users: {len(script_executions['sessions'])}")
        logger.info(f"Current User IP: {request.remote_addr}")
        logger.info("----------------------------------------")
        
        # Extract data from request
        park_id = data.get('parkId')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        nights = data.get('nights')
        search_preference = data.get('searchPreference')
        
        # Build command
        cmd = [
            VENV_PYTHON,
            os.path.join(SCRIPT_DIR, SCRIPT_NAME),
            '--start-date', start_date,
            '--end-date', end_date,
            '--parks', park_id,
            '--nights', str(nights),
            '--frequency', '0'
        ]

        # Add filters based on search preference
        if search_preference == 'weekends':
            cmd.extend(['--filters', 'priority'])
        elif search_preference == 'flexible':
            cmd.extend(['--filters', 'priority', 'regular'])
        else:  # all dates
            cmd.extend(['--filters', 'priority', 'regular', 'ignored'])

        print("\n=== Executing Command ===")
        print(f"Command: {' '.join(cmd)}")
        
        # Run the command and capture output directly
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR
        )

        # Parse the results
        results = {
            'priority': [],
            'regular': [],
            'ignored': [],
            'campground_name': None
        }

        current_section = None
        capture_results = False

        # Process the output line by line
        for line in result.stdout.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Capture campground name
            if "🏕" in line and "CAMPGROUND" in line:
                results['campground_name'] = clean_text(line)
                continue

            # Start capturing after Full Results marker
            if "=== Full Results for Reference ===" in line:
                capture_results = True
                continue

            if not capture_results:
                continue

            # Identify sections
            if "**Priority Results:**" in line:
                current_section = 'priority'
            elif "**Regular Results:**" in line:
                current_section = 'regular'
            elif "**Ignored Results:**" in line:
                current_section = 'ignored'
            # Capture results if we're in a section
            elif current_section and "->" in line:
                clean_line = clean_text(line)
                if clean_line:  # Only add if there's content after cleaning
                    results[current_section].append({
                        'text': clean_line,
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    })

        return jsonify({
            'success': True,
            'results': results
        })

    except Exception as e:
        print(f"\n=== Error ===\n{str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/search_campsites', methods=['POST'])
def search_campsites():
    try:
        data = request.get_json()
        lat = data.get('latitude')
        lng = data.get('longitude')
        
        # Call Recreation.gov API
        url = f'https://ridb.recreation.gov/api/v1/facilities'
        params = {
            'latitude': lat,
            'longitude': lng,
            'radius': 200,  # 200 mile radius
            'activity': 'CAMPING',
            'apikey': RECREATION_API_KEY
        }
        
        response = requests.get(url, params=params)
        campsites = response.json()
        
        campgrounds = [site for site in campsites.get('RECDATA', []) 
                     if site.get('FacilityTypeDescription') == 'Campground']
        
        return jsonify({
            'success': True,
            'campsites': [{
                'name': site.get('FacilityName'),
                'id': site.get('FacilityID'),
                'description': site.get('FacilityDescription'),
                'latitude': site.get('FacilityLatitude'),
                'longitude': site.get('FacilityLongitude')
            } for site in campgrounds]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # Now you're handling non-HTTP exceptions only
    app.logger.error(f"An error occurred: {str(e)}")
    app.logger.error(traceback.format_exc())
    return jsonify({
        "error": "An unexpected error occurred",
        "details": str(e)
    }), 500

if __name__ == '__main__':
    # Set both Flask and logging to DEBUG level
    app.logger.setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(debug=True, host='127.0.0.1', port=5000) 