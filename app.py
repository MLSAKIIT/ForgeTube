from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
import os
import json
import uuid
from werkzeug.utils import secure_filename
import time
import threading
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# Ensure upload and results directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Task tracking storage
tasks = {}

# Custom Jinja2 filters
@app.template_filter('timestamp_to_datetime')
def timestamp_to_datetime(timestamp):
    """Convert Unix timestamp to formatted datetime string"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Helper functions
def create_or_check_folder(folder_path):
    """
    Creates a folder if it doesn't exist.
    If folder exists, checks for files and returns error message if any are found.
    
    Args:
        folder_path (str): Path to the folder
        
    Returns:
        tuple: (success, message)
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return True, f"Created Folder: {folder_path}"
    else:
        if any(os.listdir(folder_path)):
            return False, f"Folder '{folder_path}' already exists and contains files. Please remove them or use a different folder."
        return True, f"Folder '{folder_path}' exists but is empty."

def generate_video_task(task_id, topic, duration, key_points, api_keys):
    """
    Background task to generate video
    """
    task = tasks[task_id]
    task['status'] = 'Generating script...'
    time.sleep(2)  # Simulate script generation
    
    # TODO: Replace with actual script generation
    # generator = VideoScriptGenerator(api_key=api_keys['gemini'], serp_api_key=api_keys['serp'])
    # script = generator.generate_script(topic, duration, key_points)
    
    script = {"topic": topic, "audio_script": [{"text": "This is a test script"}]}
    task['script'] = script
    task['status'] = 'Script generated'
    
    task['status'] = 'Generating images...'
    time.sleep(3)  # Simulate image generation
    
    task['status'] = 'Generating audio...'
    time.sleep(2)  # Simulate audio generation
    
    task['status'] = 'Assembling video...'
    time.sleep(3)  # Simulate video assembly
    
    task['status'] = 'Completed'
    task['result_url'] = f"/results/{task_id}.mp4" 

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create new video page"""
    if request.method == 'POST':
        # Get form data
        topic = request.form.get('topic', '')
        duration = int(request.form.get('duration', 60))
        key_points_text = request.form.get('key_points', '')
        key_points = [point.strip() for point in key_points_text.split(',') if point.strip()]
        
        # Get API keys
        gemini_api = request.form.get('gemini_api', '')
        serp_api = request.form.get('serp_api', '')
        
        # Validate inputs
        if not topic:
            return render_template('create.html', error="Topic is required")
        
        if not gemini_api or not serp_api:
            return render_template('create.html', 
                error="API keys are required. Get your Gemini API key at https://aistudio.google.com/apikey and Serp API key at https://serpapi.com")
        
        # Create task
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'topic': topic,
            'duration': duration,
            'key_points': key_points,
            'status': 'Queued',
            'created_at': time.time(),
            'api_keys': {
                'gemini': gemini_api,
                'serp': serp_api
            }
        }
        tasks[task_id] = task
        
        # Start task in background
        threading.Thread(
            target=generate_video_task, 
            args=(task_id, topic, duration, key_points, task['api_keys'])
        ).start()
        
        # Redirect to task progress page
        return redirect(url_for('task_progress', task_id=task_id))
    
    return render_template('create.html')

@app.route('/task/<task_id>')
def task_progress(task_id):
    """Task progress page"""
    task = tasks.get(task_id)
    if not task:
        return render_template('error.html', message="Task not found"), 404
    
    return render_template('progress.html', task=task)

@app.route('/api/task/<task_id>')
def task_status(task_id):
    """API endpoint to get task status"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    # Return task data without API keys for security
    safe_task = {**task}
    if 'api_keys' in safe_task:
        del safe_task['api_keys']
    
    return jsonify(safe_task)

@app.route('/refine/<task_id>', methods=['GET', 'POST'])
def refine_script(task_id):
    """Refine script page"""
    task = tasks.get(task_id)
    if not task:
        return render_template('error.html', message="Task not found"), 404
    
    if request.method == 'POST':
        feedback = request.form.get('feedback', '')
        if feedback:
            # TODO: Implement script refinement with API
            # generator = VideoScriptGenerator(api_key=task['api_keys']['gemini'], 
            #                                serp_api_key=task['api_keys']['serp'])
            # refined_script = generator.refine_script(task['script'], feedback)
            # task['script'] = refined_script
            
            # For now, just acknowledge the feedback
            task['feedback'] = feedback
            task['status'] = 'Script refined, ready to generate'
        
        return redirect(url_for('task_progress', task_id=task_id))
    
    return render_template('refine.html', task=task)

@app.route('/results/<path:filename>')
def get_result(filename):
    """Serve result files"""
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True) 