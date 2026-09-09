# Instrument sprites

These twelve transparent PNGs are extracted from Rob's original ChatGPT artwork
in `../source/musicians.png`. No generated replacement artwork is used.

File names use `w` for brass and `b` for woodwinds, followed by the chess role:
`K` king, `Q` queen, `R` rook, `B` bishop, `N` knight, `P` pawn.
Repeated rooks, bishops and knights share the same sprite for their side.
The existing instrument names and chess rules are unchanged.

Reproduce with Pillow and numpy installed:

```sh
python3 tools/extract_sprites.py assets/source/musicians.png
```

The extractor removes the warm background connected to each crop's perimeter,
then closes small mask gaps to preserve dark shading and boots. It retains
original RGB pixels; enclosed dark spaces remain part of the artwork.
