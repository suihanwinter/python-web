from fontTools.ttLib import TTFont
from os import path, makedirs, getcwd, remove
import re, requests, time
import numpy as np
font = TTFont('maoyan.woff')
print(font.getGlyphOrder())
