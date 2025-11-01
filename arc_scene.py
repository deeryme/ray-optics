from numpy import sqrt

NUM_KEYS_B4_OBJS = 3

detector_width      = 1.5     # mm
bin_size            = 0.1
mirror_height       = 4.0     # mm; indicates the height of the mirror endpts
total_mirror_width  = 1.0     # mm
r                   = 0.1     # mm; radius of curvature

SCENE = {
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

def get_arc_mirror(scene, mirror_width, mirror_height,
               r, is_concave_up, x_offset=0.0, add_brand_new=False):
   
    half_width = mirror_width/2 
    p1_x = -mirror_width/2 + x_offset
    p2_x = mirror_width/2 + x_offset
    p3_x = x_offset
    d = r-sqrt(r**2-half_width**2) # perp. dist. from p3 to p1-p2 chord
    if not is_concave_up:
        d *= -1
    
    if not add_brand_new:
        scene["objs"][NUM_KEYS_B4_OBJS]["p1"]["x"] = p1_x
        scene["objs"][NUM_KEYS_B4_OBJS]["p2"]["x"] = p2_x
        scene["objs"][NUM_KEYS_B4_OBJS]["p3"]["x"] = p3_x
    else:
        p1 = {'x': p1_x, 'y': -mirror_height}
        p2 = {'x': p2_x, 'y': -mirror_height}
        p3 = {'x': p3_x, 'y': -mirror_height+d}
        arc_mirror = {"type": "ArcMirror", "p1": p1, "p2": p2, "p3": p3}
        scene["objs"].insert(NUM_KEYS_B4_OBJS, arc_mirror)

    return scene
