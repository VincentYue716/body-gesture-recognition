# Body Gesture Recognition

The body gesture recognition project is initially developed based on Face++ (An online API) and opencv.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install opencv-python.
```bash
pip install opencv-python
```

## The main principle of body gesture recognition
- Step 1: Finding the body
- Step 2: Encoding hand images by base64
- Step 3: Posting the coding to Face++ server
- Step 4: Finding the body’s skeleton from the result

## Problems
1. Face++
    - Because face++ is an online API, the latency is relatively large
    - The accuracy is still not satisfactory
    - Only briefly implement body skeleton detection