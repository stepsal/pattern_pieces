# pattern_pieces

Pattern Pieces art generation script written in Python.
Creates an image from a number of input images.
A random square of BLOCK_SIZE is take from each input image cyclically until
the NO_OF_PIECES is reached.
Output Image is created by cycling and pasting through these pieces.

## Usage

```
Pattern Pieces Art Generator

optional arguments:
  -h, --help            show this help message and exit
  -b BLOCK_SIZE, --blocksize BLOCK_SIZE
                        Block Size
  -p NO_OF_PIECES, --pieces NO_OF_PIECES
                        Number of Pieces
  -i INPUT_DIR, --input INPUT_DIR
                        input directory
```
