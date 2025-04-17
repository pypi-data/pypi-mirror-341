# Track SORT

This is a implementation of the SIMPLE ONLINE AND REALTIME TRACKING paper [1],
or SORT for short, for Python.

It essentially wraps the Rust implementation from https://gitlab.com/leandrosansilva/track-sort-rs

Its interface differs considerably from the original reference implementation
from https://github.com/abewley/sort.

## Installation

### Requirements

- A recent version of Cargo, the Rust package manager.
- Maturin

### Via PIP

```
pip install track-sort-py
```

## TODO

- Document it
- Benchmark it against reference implementation
- Publish linux binaries

## Citation

```bibtex
@inproceedings{Bewley2016_sort,
  author={Bewley, Alex and Ge, Zongyuan and Ott, Lionel and Ramos, Fabio and Upcroft, Ben},
  booktitle={2016 IEEE International Conference on Image Processing (ICIP)},
  title={Simple online and realtime tracking},
  year={2016},
  pages={3464-3468},
  keywords={Benchmark testing;Complexity theory;Detectors;Kalman filters;Target tracking;Visualization;Computer Vision;Data Association;Detection;Multiple Object Tracking},
  doi={10.1109/ICIP.2016.7533003}
}
```

[1] https://arxiv.org/pdf/1602.00763
