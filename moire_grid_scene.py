import numpy as np

NUM_KEYS_B4_OBJS = 3

detector_width      = 1.5     # mm
bin_size            = 0.1
mirror_height       = 4.0     # mm
total_mirror_width  = 1.0     # mm
sub_mirr_len        = 100e-3  # mm
num_gaps            = 5

mirrorless_scene = {
  "version": 5,
  "name": "sub_mirr_6_scene",
  "objs": [
    {
        "type": "AngleSource",
        "p1": {"x": -1.5, "y": 0},
        "p2": {"x": -1.5, "y": -5},
        "emisAngle": 140
    },
    {
        "type": "AngleSource",
        "p1": {"x": 1.5, "y": 0},
        "p2": {"x": 1.5, "y": -5},
        "emisAngle": 140
    },
    {
        "type": "Detector",
        "p1": {"x": -detector_width/2, "y": 0},
        "p2": {"x": detector_width/2, "y": 0},
        "irradMap": True,
        "binSize": bin_size
    },
    {
        "type": "CropBox",
        "p1": {"x": -10, "y": -10}, # Upper left corner
        "p4": {"x": 10, "y": 10},   # Lower right corner
        "width": 500                # Width of the image
    },
    {
        "type": "TextLabel",
        "x": 5.5,
        "y": 7.5,
        "text": "foo",
        "fontSize": 1,
        "font": "Arial"
    }
  ],
  "width": 1500,
  "height": 900,
  "rayModeDensity": 20.085536923187668,
  "showGrid": True,
  "gridSize": 1,
  "lengthScale": 0.1,
  "origin": {
    "x": -1217.7466157567594,
    "y": -503.05228391216576
  },
  "scale": 50
}

def construct_gapped_mirror(total_width, sub_mirr_len, num_gaps):
    num_sub_mirrs = num_gaps+1
    gap_len = (total_width-num_sub_mirrs*sub_mirr_len)/num_gaps
    p1 = np.linspace(0,total_width-(sub_mirr_len+gap_len), num_sub_mirrs)
    p1 -= total_width/2   # Centre mirror about x = 0
    p2 = p1+sub_mirr_len

    gapped_mirror = []
    for sub_mirror in range(num_sub_mirrs): 
      mirror_dict = {
          "type": "Mirror",
          "p1": {"x": p1[sub_mirror], "y": -mirror_height},
          "p2": {"x": p2[sub_mirror], "y": -mirror_height}
      }
      gapped_mirror.append(mirror_dict)
    
    return gapped_mirror, p1 , p2

def insert_gapped_mirror(scene, gapped_mirror):
  for i in range(len(gapped_mirror)):
    scene["objs"].insert(NUM_KEYS_B4_OBJS, gapped_mirror[::-1][i])
  return scene


