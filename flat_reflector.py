#!/usr/bin/env python3
"""
Ray Optics Simulation of tangential translation of reflector above photodetector
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sim_helper_functions import run_sim_startup_checks, create_gif_from_images, simulate_scenes_wrapper
import basic_scene as my_scene
import json
import copy
import time
from multiprocessing import Pool

if __name__ == "__main__":
    run_sim_startup_checks()
    np.set_printoptions(precision=4)

    # ========== vvv CHANGE THESE vvv ==========
    mirror_h        = 4.0       # mm; indicates the height of the mirror endpts
    mirror_w        = 1.0       # mm
    max_delta_Y     = 4         # mm
    v_pts_per_mm    = 8         # <<<<<<<<<
    # ========== ^^^ CHANGE THESE ^^^ ==========
    heights = np.linspace(0,max_delta_Y,max_delta_Y*v_pts_per_mm+1)
    
    scene = copy.deepcopy(my_scene.SCENE)

    main_dir_name = "flat"
    try:
        os.makedirs(main_dir_name)
    except FileExistsError:
        print(f"{main_dir_name} directory already exists.")

    top_file_names = [] # For a flat reflector height is the same as top 
    total_sim_duration = 0.0    # seconds
    for h in heights:
        # ========== SETUP FILE STRUCTURE SIM OF A SET OF SCENES ==========
        mir_w_str = 'f'.join(f"{my_scene.mirror_w:.2f}".split('.'))
        mir_top_str = 'f'.join(f"{h:.4f}".split('.'))
        h_sweep_name = f"flat_reflector_w_{mir_w_str}mm_top_{mir_top_str}mm"
        top_file_names.append(h_sweep_name)
    
        try:
            sub_dir_name = f"{main_dir_name}/{h_sweep_name}"
            os.makedirs(sub_dir_name)
        except FileExistsError:
            print(f"{sub_dir_name} directory already exists.")

        try:    
            print(f"{sub_dir_name}/pics")
            os.makedirs(f"{sub_dir_name}/pics")
        except FileExistsError:
            print("pics sub-directory already exists.")


        # ========== RUN SIM ==========
        print(f"\n=== Running Horiz. Sweep  #{np.argmax(heights == h)} (of {len(heights)}). Top of Reflector is {h} mm above detector. ===")
        # Setup mirror translation params and preallocate space for output
        h_pts_per_mm = v_pts_per_mm
        max_delta_X = 2 # mm; mirror's lateral displacement
        num_rflt_positions = 2*max_delta_X*h_pts_per_mm+1
        x = np.linspace(-max_delta_X, max_delta_X, num_rflt_positions)
        P = np.zeros(num_rflt_positions)
        num_bin_positions = np.int64(np.ceil(my_scene.detector_w/my_scene.bin_size))
        irrad = np.zeros((num_rflt_positions, num_bin_positions))
        readings = []

        x_idxs = list(range(len(x)))
        h_sweep_scenes = [
            my_scene.get_h_sweep_scene(copy.deepcopy(scene), h_sweep_name, mirror_w, h, idx, x[idx]) for idx in x_idxs
        ]
        sim_wrapper_args = list(zip(x_idxs, x, h_sweep_scenes, [sub_dir_name]*len(x)))

        # Record the start time
        start_time = time.perf_counter()
        with Pool() as pool:
            readings = pool.starmap(simulate_scenes_wrapper, sim_wrapper_args)

        for idx in x_idxs:
            P[idx] = readings[idx]['power']
            irrad[idx,:] = readings[idx]['irradianceMap']

        # Record the end time and calculate the lateral sweep duration
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"Elapsed time: {duration:.6f} seconds")
        total_sim_duration += duration


        # ========== EXPORT DETECTOR DATA TO JSON ==========
        readings_path = f"{sub_dir_name}/{h_sweep_name}.json"
        with open(os.path.join(os.getcwd(), readings_path), 'w', newline='') as file:
            json.dump(list(readings), file)

        # ========== USE FFMPEG TO CREATE GIF FROM OUTPUT IMAGES ==========
        ffmpeg_in = f"{sub_dir_name}/pics/{h_sweep_name}_mir_pos_%3d.png"
        ffmpeg_out = f"{sub_dir_name}/{h_sweep_name}.gif"
        create_gif_from_images(ffmpeg_in, ffmpeg_out)


        # ========== USE DATA TO CREATE PLOTS ==========
        #  Plot Power vs Tangential Reflector Displacement
        power_fig = plt.figure()
        plt.title("Power vs Tangential Reflector Displacement")
        plt.plot(x, np.abs(P))
        plt.grid(True)
        plt.xlabel(r"$\Delta$x (mm from centre position)")
        plt.ylabel("$Power$")
        plt.savefig(f"{sub_dir_name}/P_v_DeltaX_{h_sweep_name}.png")

        irrad_fig = plt.figure()
        b = np.arange(num_bin_positions)
        bb, xx = np.meshgrid(b, x)
        plt.title("(Line) Irradiance as a function of \nReflector Displacement and Bin Position")
        plt.contourf(bb, xx, irrad)
        plt.colorbar()
        plt.grid(True)
        plt.ylabel(r"$\Delta$x (mm from centre position)")
        plt.xlabel(f"Bin Position (each bin is {my_scene.bin_size} mm)")
        plt.xticks(b)
        plt.savefig(f"{sub_dir_name}/Irrad_Contour_{h_sweep_name}.png")

        # plt.show()

    print('\a'*5, f"\nXY sweep complete! (Total Sim. Duration =  {total_sim_duration}s)")
    with open(f"{main_dir_name}/tops.json", 'w') as f:
        json.dump(top_file_names, f)
