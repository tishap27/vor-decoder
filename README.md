

# VOR Decoder

![CI](https://github.com/tishap27/vor-decoder/actions/workflows/ci.yml/badge.svg)

RTL-SDR VOR decoder, decodes the bearing from a VOR signal.

Status: decoder validated on synthetic signals. (YOW, 114.6 MHz) in progress.


## How the decoder works
1. Listen to the radio signal and pull out the audio hidden in it
2. Find the two 30 Hz tones. One is the reference (the same everywhere) and the other changes with where you are around the station
3. Compare the two tones. How far apart they are in timing tells you the direction from the station (the radial)

The program also prints two checks every second. If both look right (about 0.3 and about 480 Hz), it has locked onto a real VOR and not just noise.

## Files
- `vor_decode.py`: the decoder
- `gen_synthetic.py`: simulates VOR capture with a known bearing
- `test_synthetic.py`: round-trip tests at 7 bearings
- `check_radial.py`: expected radial and distance from the YOW VOR to a GPS position

## Usage
    pip install -r requirements.txt
    python gen_synthetic.py 135
    python vor_decode.py synthetic.iq
    python test_synthetic.py

VOR signals are horizontally polarized, so the antenna should be horizontal.

## Results
Synthetic validation: all 7 test bearings (0 to 359 degrees) decoded within 0.2 degrees.

Over-the-air results: in progress
