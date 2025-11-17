#!/usr/bin/env python3
"""
Ray Optics Simulation - Python Wrapper functions
"""

import os
import json
import subprocess
import base64
import sys
import shutil

def run_sim_startup_checks():
    # ========== Startup Checks ==========
    print("#", '='*65)
    print("\t\tRay Optics Simulation - Python Example")
    print("For more information about this package, see the README.md file.")
    print("#", '='*65, '\n')

    # Check if Node.js is installed
    if not shutil.which("node"):
        print("\nError: Node.js is not installed.")
        print("You can install it from https://nodejs.org/")
        sys.exit(1)

    # Check if node-canvas is installed
    canvas_check = subprocess.run(
        ["node", "-e", "try{require('canvas');process.exit(0)}catch(e){process.exit(1)}"]
    )

    if canvas_check.returncode != 0:
        print("To run this example, you need to install node-canvas:")
        print("  npm install canvas")
        sys.exit(0)

def create_gif_from_images(input_pics, output_gif, frame_rate=10):
    export_as_gif_command = [
        'ffmpeg', 
        '-hide_banner', '-loglevel', 'error',
        '-framerate', str(frame_rate),
        '-i', input_pics,
        output_gif, '-y'
    ]

    try:
        subprocess.run(export_as_gif_command, check=True)
        print(f"GIF '{output_gif}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating GIF: {e}")
    except FileNotFoundError:
        print("FFmpeg not found. Please ensure FFmpeg is installed and in your system's PATH.")

def simulate_scene(scene, file_name, dir_name=None):
    if dir_name is None:
        dir_name == file_name
    
    # ========== SIMULATE A SCENE & LOAD JSON OUTPUT ==========
    json_encoded_scene = json.dumps(scene)

    # Run the simulation using Node.js
    # Assumes runner.js is in the same directory as this script
    sim_process = subprocess.run(
        ["node", "runner.js"],
        input=json_encoded_scene.encode(),
        capture_output=True
    )

    # ========== PARSE SIM RESULT FOR P_DETECTOR RESULTS ==========
    # Check for simulator errors and warnings
    sim_result = json.loads(sim_process.stdout)
    if sim_result.get('error'):
        print(f"Simulator error: {sim_result['error']}")
    if sim_result.get('warning'):
        print(f"Simulator warning: {sim_result['warning']}")
    detector = sim_result['detectors'][0]  # Get the one (and only) detector
    
    readings = {
        'power': detector['power'], 
        'irradianceMap': detector['irradianceMap'],
        'binPositions': detector['binPositions'],
        'normal': detector['normal'], 
        'shear': detector['shear']
    }

    # ========== GET IMAGE FROM SIM RESULT ==========
    # Get the image data
    image_data = sim_result['images'][0]['dataUrl'].split(',')[1]

    # Save the image to a file
    image_path = f"{dir_name}/pics/{file_name}.png"
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(image_data))

    return readings

def simulate_scenes_wrapper(idx, x_offset, scene, dir_name): 
    return simulate_scene(scene, scene['name'], dir_name)
