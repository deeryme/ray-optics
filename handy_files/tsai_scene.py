detector_width  = 1.5 # mm
mirror_width    = 1.0 # mm
bin_size        = 0.1

SCENE = {
  "version": 5,
  "name": "tsai_scene",
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
        "type": "Mirror",
        "p1": {"x": -mirror_width/2, "y": -4},
        "p2": {"x": mirror_width/2, "y": -4}
    },
    {
        "type": "CropBox",
        "p1": {"x": -10, "y": -10}, # Upper left corner
        "p4": {"x": 10, "y": 10},   # Lower right corner
        "width": 500                # Width of the image
    },
    {
        "type": "TextLabel",
        "x": 6.5,
        "y": 6.5,
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