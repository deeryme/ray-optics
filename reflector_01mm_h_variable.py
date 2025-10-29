#!/usr/bin/env python3
"""
Ray Optics Simulation of tangential translation of reflector above photodetector
"""

import os
import numpy as np
from sim_helper_functions import run_sim_startup_checks, create_gif_from_images, simulate_scene
import basic_scene as my_scene


run_sim_startup_checks()
scene = my_scene.SCENE

# ========== SETUP FILE STRUCTURE SIM OF A SET OF SCENES ==========
mir_w_str = 'f'.join(f"{my_scene.mirror_width:.1f}".split('.'))
mir_h_str = 'f'.join(f"{my_scene.mirror_height:.1f}".split('.'))
scene['name'] = f"reflector_w_{mir_w_str}mm_h_{mir_h_str}mm"
try:
    dir_name = scene['name']
    os.makedirs(dir_name)
except FileExistsError:
    print(f"{dir_name} directory already exists.")

try:
    print(f"{dir_name}/data")
    os.makedirs(f"{dir_name}/data")
except FileExistsError:
    print("data sub-directory already exists.")

try:    
    print(f"{dir_name}/pics")
    os.makedirs(f"{dir_name}/pics")
except FileExistsError:
    print("pics sub-directory already exists.")


# ========== RUN SIM ==========
print("\n=== Running Sim ===")
pts_per_mm = 20
delta_X = 2 # mm; mirror's tangential displacement
for idx, pos in enumerate(np.linspace(-delta_X, delta_X, 2*delta_X*pts_per_mm+1)): 
    # Vary Scene Parameters
    scene["objs"][3]["p1"]["x"] = -my_scene.mirror_width/2 + pos
    scene["objs"][3]["p2"]["x"] =  my_scene.mirror_width/2 + pos
    scene["objs"][5]["text"] = f"Mirror is\n{pos:.2f} mm\nfrom ctr"       
    file_name = f"{scene['name']}_mir_pos_{idx:03}"
    simulate_scene(scene, file_name, dir_name)
    
ffmpeg_in = f"{dir_name}/pics/{scene['name']}_mir_pos_%3d.png"
ffmpeg_out = f"{dir_name}/pics/{scene['name']}.gif"
create_gif_from_images(ffmpeg_in, ffmpeg_out, 5)


print("\nExamples completed!")

