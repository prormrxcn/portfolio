from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_required, current_user
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'meow12_secure_key_change_in_production'  # Change this to a secure secret key

# Initialize Flask-Login (if you need authentication)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Portfolio configuration
PORTFOLIO_CONFIG = {
    'owner': 'Prormrxcn',
    'title': 'FPGA & VLSI Portfolio',
    'description': 'Digital Systems Designer specializing in Verilog HDL and FPGA Development',
    'github_url': 'https://github.com/prormrxcn',
    'email': 'contact@prormrxcn.dev',
    'linkedin': '#',  # Add your LinkedIn URL
    'twitter': '#',   # Add your Twitter URL
}

# Navigation data for templates
nav_data = {
    'home': 'Home',
    'portfolio': 'Portfolio',
    'about': 'About',
    'contact': 'Contact'
}

# Project data - Enhanced with more details
PROJECTS_DATA = [
    {
        'id': 'snake-game-fpga',
        'title': 'Snake Game on FPGA',
        'short_description': 'A fully functional Snake game implemented on Basys 3 FPGA with VGA output, collision detection, and random food generation.',
        'long_description': '''
        This project implements a complete Snake game on the Basys 3 FPGA board using Verilog HDL. 
        The game features real-time VGA output at 640x480 resolution, sophisticated collision detection, 
        random food generation using linear feedback shift registers (LFSR), and score tracking. 
        The design is fully synthesizable and optimized for hardware without using initial blocks.
        
        Key technical achievements include precise timing control for 60Hz refresh rates, 
        efficient memory management for game state, and modular design architecture that 
        separates game logic from display controllers.
        ''',
        'technologies': ['Verilog HDL', 'VGA Controller', 'Game Logic', 'Basys 3 FPGA', 'Collision Detection', 'LFSR'],
        'github_url': 'https://github.com/prormrxcn/snake_game_verilog_vga',
        'demo_url': '#',
        'image_url': '/static/images/snake-game-demo.jpeg',  # Add project images
        'features': [
            'Real-time gameplay with VGA output at 640x480@60Hz',
            'Advanced collision detection system',
            'LFSR-based random food generation algorithm',
            'Score tracking and display system',
            'Synthesizable design without initial blocks',
            'Modular architecture for easy expansion',
            'Optimized for Basys 3 FPGA board'
        ],
        'challenges': [
            'Implementing precise timing for smooth gameplay',
            'Managing game state in hardware registers',
            'Optimizing resource utilization on FPGA'
        ],
        'status': 'Completed',
        'date': '2024-12'
    },
    {
        'id': 'ALU_32_bit',    
        'title': '32-bit ALU ASIC Design with OpenLane',
        'short_description': 'A fully synthesizable 32-bit Arithmetic Logic Unit implemented in Verilog and taped out using OpenLane with the SkyWater 130nm PDK.',
        'long_description': '''
        This project implements a robust and synthesizable 32-bit Arithmetic Logic Unit (ALU) using Verilog HDL, designed for both FPGA prototyping and ASIC implementation.
    
        The ALU performs a range of arithmetic and logic operations including addition, subtraction, AND, OR, XOR, and set-on-less-than. Initially tested on a Basys 3 FPGA board, the design was later integrated into a full ASIC development flow using OpenLane and the SkyWater 130nm PDK.

        This project reflects a deep understanding of RTL design, synthesis constraints, ASIC toolchains, and timing optimization, making it a practical and educational SoC building block.
        ''',
        'technologies': ['Verilog HDL', 'OpenLane', 'Sky130 PDK', 'ASIC Design Flow', 'FPGA', 'Digital Logic'],
        'github_url': 'https://github.com/prormrxcn/alu_32_bit',
        'demo_url': '#',
        'image_url': '/static/images/alu_32_bit.png',
        'features': [
            '32-bit ALU supporting arithmetic and logic operations',
            'Synthesis-ready Verilog with no non-synthesizable constructs',
            'Compatible with both FPGA and ASIC workflows',
            'Validated on Basys 3 FPGA board',
            'Tapeout-compatible using OpenLane and Sky130',
            'Minimal area and gate count design'
    ],
    'challenges': [
        'Designing purely synthesizable logic for ASIC flow',
        'Adhering to Sky130 standard cell constraints',
        'Running complete OpenLane ASIC flow with error-free results',
        'Debugging synthesis and placement/timing violations'
    ],
    'status': 'Completed',
    'date': '2025-07'
},
    {
        "id": "vga-hello-world",
        "title": "VGA 'HELLO WORLD' Display on Basys 3",
        "short_description": "A synthesizable Verilog module to display 'HELLO WORLD' with colorful text and a dynamic background on VGA using Basys 3 FPGA.",
        "long_description": """
        This project demonstrates a fully synthesizable Verilog VGA controller designed for the Basys 3 FPGA board, capable of rendering the text 
        'HELLO WORLD' in a vibrant, gradient-filled display. Using a 25 MHz pixel clock derived from a 100 MHz input, the design adheres to standard 
        640x480 @ 60Hz VGA timing.

        The module includes character rendering logic based on scalable 8x8 bitmaps, and dynamically colors each character with a cycling color 
        scheme (cyan, yellow, and magenta). The background is a smooth gradient derived from the horizontal and vertical pixel positions, adding 
        visual appeal.

        All logic is designed to be synthesizable without using initial blocks, and follows good FPGA design practices like clock division, 
        structured state control, and resolution-independent rendering techniques.
        """,
        "technologies": [
            "Verilog HDL",
            "VGA Protocol",
            "FPGA Synthesis",
            "Basys 3 Board",
            "Text Rendering",
            "Clock Division",
            "Scalable Character Graphics"
        ],
            "github_url": "https://github.com/prormrxcn/vga_test_hello_world_verilog",
        "demo_url": "#",
        "image_url": "/static/images/vg.jpeg",
        "features": [
            "Fully synthesizable VGA controller",
            "Character rendering with scalable bitmap fonts",
            "Colorful animated text and gradient background",
            "Compatible with 640x480 @ 60Hz VGA standard",
            "Centered text display with horizontal/vertical sync",
            "Designed for Digilent Basys 3 (Artix-7 FPGA)",
            "No use of non-synthesizable constructs"
            ],
            'challenges': [
                'Ensuring synthesis compatibility across tools',
                'Optimizing for different FPGA architectures',
                'Creating comprehensive documentation'
            ],
            'status': 'Completed',
            'date': '2024-10'
    }
]

# Skills data with enhanced details
SKILLS_DATA = {
    'fpga': {
        'title': 'FPGA Development',
        'description': 'Experienced with Basys 3 FPGA board, synthesizable design patterns, and hardware optimization techniques. Skilled in constraint files, timing analysis, and resource optimization.',
        'icon': '🔧',
        'tools': ['Xilinx Vivado', 'Basys 3', 'Artix-7', 'Constraint Files', 'Timing Analysis']
    },
    'verilog': {
        'title': 'Verilog HDL',
        'description': 'Expert in writing clean, modular Verilog code for real-time applications without relying on initial blocks. Focus on synthesizable designs and hardware-optimized algorithms.',
        'icon': '⚡',
        'tools': ['SystemVerilog', 'Testbenches', 'Synthesis', 'Simulation', 'Design Verification']
    },
    'python': {
        'title': 'python',
        'description': 'built custom chatbots using ollama.',
        'icon': '📺',
        'tools': ['python','ollama','numpy']
    },
    'vlsi': {
        'title': 'VLSI Design',
        'description': 'Exploring foundational VLSI concepts and ASIC-level design flow for scalable digital systems. Understanding of semiconductor physics and fabrication processes.',
        'icon': '🔬',
        'tools': ['ASIC Design', 'RTL Design', 'Logic Synthesis', 'Physical Design']
    }
}

@app.route('/')
def home():
    """Home page route - Single page application"""
    return render_template('index.html', 
                         title=f'{PORTFOLIO_CONFIG["owner"]} - {PORTFOLIO_CONFIG["title"]}',
                         config=PORTFOLIO_CONFIG,
                         nav_data=nav_data,
                         projects=PROJECTS_DATA[:3],  # Show only featured projects
                         skills=SKILLS_DATA)

@app.route('/portfolio')
def portfolio():
    """Portfolio page route - Show all projects"""
    return render_template('portfolio.html', 
                         title=f'Portfolio - {PORTFOLIO_CONFIG["title"]}',
                         config=PORTFOLIO_CONFIG,
                         nav_data=nav_data,
                         projects=PROJECTS_DATA)

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html', 
                         title=f'About - {PORTFOLIO_CONFIG["owner"]}',
                         config=PORTFOLIO_CONFIG,
                         nav_data=nav_data,
                         skills=SKILLS_DATA)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just flash a success message
        if name and email and subject and message:
            flash(f'Thank you {name}! Your message has been sent.', 'success')
            
            # Log the message (in production, save to database or send email)
            print(f"New contact message:")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            print(f"Timestamp: {datetime.now()}")
            
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all fields.', 'error')
    
    return render_template('contact.html', 
                         title=f'Contact - {PORTFOLIO_CONFIG["owner"]}',
                         config=PORTFOLIO_CONFIG,
                         nav_data=nav_data)

@app.route('/project/<project_id>')
def project_detail(project_id):
    """Individual project detail page"""
    project = next((p for p in PROJECTS_DATA if p['id'] == project_id), None)
    
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('portfolio'))
    
    return render_template('project_detail.html', 
                         title=f'{project["title"]} - Project Details',
                         config=PORTFOLIO_CONFIG,
                         nav_data=nav_data,
                         project=project)

# API endpoints for dynamic content
@app.route('/api/projects')
def api_projects():
    """API endpoint to get all projects"""
    return jsonify(PROJECTS_DATA)

@app.route('/api/project/<project_id>')
def api_project(project_id):
    """API endpoint to get a specific project"""
    project = next((p for p in PROJECTS_DATA if p['id'] == project_id), None)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/skills')
def api_skills():
    """API endpoint to get all skills"""
    return jsonify(SKILLS_DATA)

@app.route('/api/contact', methods=['POST'])
def api_contact():
    """API endpoint for contact form submission"""
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        if all([name, email, subject, message]):
            # Process the contact form data
            # In production, you would send an email or save to database
            print(f"API Contact submission:")
            print(f"Name: {name}, Email: {email}")
            print(f"Subject: {subject}, Message: {message}")
            
            return jsonify({'status': 'success', 'message': f'Thank you {name}! Your message has been sent.'})
        else:
            return jsonify({'status': 'error', 'message': 'Please fill in all fields.'}), 400
    
    return jsonify({'status': 'error', 'message': 'Invalid request format.'}), 400

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html', 
                         title='Page Not Found',
                         config=PORTFOLIO_CONFIG,
                         nav_data=nav_data), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html', 
                         title='Internal Server Error',
                         config=PORTFOLIO_CONFIG,
                         nav_data=nav_data), 500

# Template context processor to make common data available to all templates
@app.context_processor
def inject_common_data():
    return {
        'config': PORTFOLIO_CONFIG,
        'nav_data': nav_data,
        'current_year': datetime.now().year
    }

# Optional: User loader for Flask-Login (if you implement authentication)
@login_manager.user_loader
def load_user(user_id):
    # This would typically load a user from your database
    # For now, return None since we're not implementing authentication
    return None

# Static file serving for development
@app.route('/static/images/<filename>')
def serve_images(filename):
    """Serve project images"""
    # In production, serve static files with nginx or similar
    return app.send_static_file(f'images/{filename}')

if __name__ == '__main__':
    # Create static directories if they don't exist
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)