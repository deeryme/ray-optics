#!/usr/bin/env python3
"""
Ray Optics Simulation - Python Example

This example shows how to use the Ray Optics Simulation from Python:
1. Getting detector readings from a simple optical setup
2. Generating an image of a simple optical setup
"""

import os
import json
import subprocess
import base64
import sys
import shutil
import my_scene
import numpy as np


# ========== Startup Checks ==========
print("Ray Optics Simulation - Python Example")
print("For more information about this package, see the README.md file.")

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

try:
    dir_name = "papilliary_pics"
    os.makedirs(dir_name)
except FileExistsError:
    print(f"{dir_name} directory exists.")


# ========== GET SIM P_DETECTOR RESULTS FOR A SCENE ==========
print("\n=== Running Sim ===")
scene = my_scene.SCENE
pts_per_mm = 50
for idx, pos in enumerate(np.linspace(-2, 2, 4*pts_per_mm+1)):        
    # Convert the scene to JSON string
    scene["objs"][3]["p1"]["x"] = -my_scene.mirror_width/2 + pos
    scene["objs"][3]["p2"]["x"] =  my_scene.mirror_width/2 + pos
    json_encoded_scene = json.dumps(scene)
    print(f"mirror POS = {pos}!")
    print(f"p1 -> {scene['objs'][3]['p1']}")
    print(f"p2 -> {scene['objs'][3]['p2']}")

    # Run the simulation using Node.js
    # Assumes runner.js is in the same directory as this script
    # print("Running simulation for detector example...")
    sim_process = subprocess.run(
        ["node", "runner.js"],
        input=json_encoded_scene.encode(),
        capture_output=True
    )

    # Parse the result
    sim_result = json.loads(sim_process.stdout)

    # Check for simulator errors and warnings
    if sim_result.get('error'):
        print(f"Simulator error: {sim_result['error']}")

    if sim_result.get('warning'):
        print(f"Simulator warning: {sim_result['warning']}")

    # Display the detector results
    # print("Detector results:")
    # detector = sim_result['detectors'][0]  # Get the first detector
    # print(f"  Power: {detector['power']}")

    # print("  Irradiance map:")
    # for i in range(5):  # Print all 5 bins
    #     print(f"    Position {detector['binPositions'][i]:.2f}: {detector['irradianceMap'][i]:.6f}")


    # ========== GET IMAGE FROM SIM RESULT ==========
    # Get the image data
    image_data = sim_result['images'][0]['dataUrl'].split(',')[1]
    # print(f"Received image data (base64 encoded)")

    # Save the image to a file
    image_path = f"{dir_name}/my_scene_{idx+1:03}.png"
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(image_data))
    print(f"Image saved to {image_path}")

print("\nExamples completed!")

