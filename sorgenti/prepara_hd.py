# -*- coding: utf-8 -*-
"""Converte le foto ingrandite con Real-ESRGAN (cartella HD) nelle versioni web del sito.
Mescola l'80% dell'ingrandimento AI con il 20% di un ingrandimento classico (Lanczos)
per un aspetto naturale, applica il duotono e salva nome-hd-{800,1600,2400}.webp.
Uso: python3 sorgenti/prepara_hd.py CARTELLA_ORIGINALI CARTELLA_HD
"""
import os, sys, glob
from PIL import Image, ImageOps

DARK, LIGHT = (10, 11, 61), (238, 240, 250)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "assets", "img")
raw, hd = sys.argv[1], sys.argv[2]
for p in sorted(glob.glob(os.path.join(hd, "*.png"))):
    nome = os.path.splitext(os.path.basename(p))[0]
    src = next((os.path.join(raw, nome + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(raw, nome + e))), None)
    ai = Image.open(p).convert("RGB")
    classico = Image.open(src).convert("RGB").resize(ai.size, Image.LANCZOS)
    im = Image.blend(ai, classico, 0.20)
    im = Image.blend(im, ImageOps.colorize(ImageOps.grayscale(im), DARK, LIGHT), 0.30)
    for s in (800, 1600, 2400):
        c = im.copy(); c.thumbnail((s, s), Image.LANCZOS)
        c.save(os.path.join(OUT, f"{nome}-hd-{s}.webp"), "WEBP", quality=80, method=6)
    for vecchio in glob.glob(os.path.join(OUT, f"{nome}-[0-9]*.webp")):
        os.remove(vecchio)
    print(nome, im.size)
