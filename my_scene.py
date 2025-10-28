SCENE = {
  "version": 5,
  "name": "my_scene",
  "objs": [
    {
      "type": "AngleSource",
      "p1": {"x": 40,"y": 20},
      "p2": {"x": 40, "y": 15},
      "emisAngle": 140
    },
    {
      "type": "AngleSource",
      "p1": {"x": 43, "y": 20},
      "p2": {"x": 43, "y": 15},
      "emisAngle": 140
    },
    {
      "type": "Detector",
      "p1": {"x": 40.75, "y": 20},
      "p2": {"x": 42.25, "y": 20},
      "irradMap": True,
      "binSize": 0.1
    },
    {
      "type": "Mirror",
      "p1": {"x": 40.5, "y": 16},
      "p2": {"x": 42.5, "y": 16}
    },
    {
      "type": "CropBox",
      "p1": {"x": 32, "y": 0},
      "p4": {"x": 50, "y": 35},
      "width": 500
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