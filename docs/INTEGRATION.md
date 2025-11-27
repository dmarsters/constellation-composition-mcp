# Integration Guide

## ComfyUI Integration

```python
composition = generate_constellation_composition("Orion", 1920, 1080)
focal_points = composition['focal_points']

# Position nodes at focal points
for i, point in enumerate(focal_points):
    x = point['x'] * 1920
    y = point['y'] * 1080
    # Position element i at (x, y)
```

## Midjourney Integration

Use suggested elements in prompts:

```python
themes = composition['mythology_themes']
lighting = composition['suggested_elements']['lighting']
prompt = f"scene with {lighting[0]}, embodying {themes[0]}"
```
