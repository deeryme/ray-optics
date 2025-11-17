detector_w  = 1.5 # mm
mirror_w    = 1.0 # mm
mirror_h   = 0.0 # mm
bin_size        = 0.1


SCENE = {
  "version": 5,
  "name": "my_scene",
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
        "p1": {"x": -detector_w/2, "y": 0},
        "p2": {"x": detector_w/2, "y": 0},
        "irradMap": True,
        "binSize": bin_size
    },
    {
        "type": "Mirror",
        "p1": {"x": -mirror_w/2, "y": -mirror_h},
        "p2": {"x": mirror_w/2, "y": -mirror_h}
    },
    {
        "type": "CropBox",
        "p1": {"x": -10, "y": -10}, # Upper left corner
        "p4": {"x": 10, "y": 10},   # Lower right corner
        "width": 500                # Width of the image
    },
    {
        "type": "TextLabel",
        "x": 2.5,
        "y": 5.5,
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

def get_h_sweep_scene(scene, h_sweep_name, mirror_w, top, idx, x_offset):
    # scene = get_arc_mirror(scene, mirror_w, h, is_concave_up, x_offset)
    half_width = mirror_w/2 
    scene["objs"][3]["p1"]["x"] = -half_width + x_offset
    scene["objs"][3]["p1"]["y"] = -top
    scene["objs"][3]["p2"]["x"] =  half_width + x_offset
    scene["objs"][3]["p2"]["y"] = -top
    
    scene["objs"][-1]["text"] = f"top = {top:.4f} mm,\nMirror is\n{x_offset:.2f} mm\nfrom ctr"    
    scene['name'] = f"{h_sweep_name}_mir_pos_{idx:03}"

    return scene