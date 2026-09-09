"""Extract the original user-supplied artwork without redrawing it.
Usage: python3 tools/extract_sprites.py /path/to/original.png
Requires Pillow and numpy.
"""
import sys
from collections import deque
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

source = Image.open(sys.argv[1]).convert('RGB')
# Tight cells exclude headings, role labels and neighboring instruments.
cells = {
 'wR': (45,105,165,361), 'wN': (211,112,369,361),
 'wB': (404,112,600,361), 'wQ': (610,45,775,362),
 'wK': (806,0,1018,363), 'wP': (1607,143,1747,365),
 'bR': (47,531,166,786), 'bN': (216,524,354,787),
 'bB': (402,524,540,788), 'bQ': (633,477,758,788),
 'bK': (829,476,998,788), 'bP': (1613,533,1713,789),
}
out = Path(__file__).resolve().parents[1] / 'assets/sprites'
out.mkdir(parents=True, exist_ok=True)
preview = Image.new('RGB',(6*180,2*350),(217,201,163))
draw = ImageDraw.Draw(preview)
for i,(code,box) in enumerate(cells.items()):
    crop = source.crop(box)
    rgb = np.asarray(crop).astype(int)
    r,g,b = rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    # The backdrop is dark warm brown. Black boots/outlines are neutral;
    # the brighter brown instrument details remain untouched.
    background = (r < 66) & (g < 56) & (b < 46) & (r > g) & (g > b) & ((r-g) < 19) & ((g-b) < 19)
    # Only remove backdrop reachable from the cell perimeter: this preserves
    # dark shading inside the original musicians instead of punching holes.
    h,w=background.shape
    exterior=np.zeros((h,w),dtype=bool)
    queue=deque((y,x) for y in range(h) for x in range(w) if (y in (0,h-1) or x in (0,w-1)) and background[y,x])
    while queue:
        y,x=queue.popleft()
        if exterior[y,x]: continue
        exterior[y,x]=True
        for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
            if 0<=yy<h and 0<=xx<w and background[yy,xx] and not exterior[yy,xx]: queue.append((yy,xx))
    if code == 'wK': exterior[190:,181:]=True # neighboring trombone, below the bell
    alpha = Image.fromarray(np.where(exterior,0,255).astype('uint8'))
    alpha = alpha.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    rgba = np.dstack((rgb.astype('uint8'), np.asarray(alpha)))
    sprite = Image.fromarray(rgba)
    sprite = sprite.crop(sprite.getbbox())
    sprite.save(out / f'{code}.png', optimize=True)
    sprite.thumbnail((165,310))
    x,y=(i%6)*180,(i//6)*350
    preview.paste(sprite,(x+(180-sprite.width)//2,y+315-sprite.height),sprite)
    draw.text((x+75,y+325),code,fill='black')
if len(sys.argv) > 2:
    preview.save(sys.argv[2])
