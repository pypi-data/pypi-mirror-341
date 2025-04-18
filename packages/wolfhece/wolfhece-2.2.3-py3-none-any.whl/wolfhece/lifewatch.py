from enum import Enum
from PIL import Image

class LifeWatch_Legend(Enum):
    """
    https://www.mdpi.com/2306-5729/8/1/13

    Map Class	Map Code	Related EAGLE Code	Percentage of Land Area [%] Based on 2018 Product
    Water	10	LCC-3	0.73
    Natural Material Surfaces with less than 10% vegetation	15	LCC-1_2	0.32
    Artificially sealed ground surface	20	LCC-1_1_1_3	5.75
    Building, specific structures and facilities	21	LCC-1_1_1_1 ||     LCC-1_1_1_2	1.99
    Herbaceous in rotation during the year (e.g., crops)	30	LCC-2_2	23.94
    Grassland with intensive management	35	LCC-2_2	27.57
    Grassland and scrub of biological interest	40	LCC-2_2	1.82
    Inundated grassland and scrub of biological interest	45	LCC-2_2 &     LCH-4_4_2	0.22
    Vegetation of recently disturbed area (e.g., clear cut)	48	LCC-2_2 &     LCH-3_8	2.64
    Coniferous trees (≥3 m)	50	LCC-2_1_1 &     LCH-3_1_1	11.24
    Small coniferous trees (<3 m)	51	LCC-2_1_2 &    LCH-3_1_1	0.40
    Broadleaved trees (≥3 m)	55	LCC-2_1_1 &    LCH-3_1_2	21.63
    Small broadleaved trees (<3 m) and shrubs	56	LCC-2_1_2 &    LCH-3_1_2	1.75

    Color Table (RGB with 256 entries) from tiff file
    10: 10,10,210,255
    11: 254,254,254,255
    15: 215,215,215,255
    20: 20,20,20,255
    21: 210,0,0,255
    30: 230,230,130,255
    35: 235,170,0,255
    40: 240,40,240,255
    45: 145,245,245,255
    46: 246,146,246,255
    48: 148,112,0,255
    50: 50,150,50,255
    51: 0,151,151,255
    55: 55,255,0,255
    56: 156,255,156,255
    """
    WATER = (10, (10, 210, 255))
    NATURAL_MATERIAL_SURFACES = (15, (215, 215, 215, 255))
    ARTIFICIALLY_SEALED_GROUND_SURFACE = (20, (20, 20, 20, 255))
    BUILDING = (21, (210, 0, 0, 255))
    HERBACEOUS_ROTATION = (30, (230, 230, 130, 255))
    GRASSLAND_INTENSIVE_MANAGEMENT = (35, (235, 170, 0, 255))
    GRASSLAND_SCRUB_BIOLOGICAL_INTEREST = (40, (240, 40, 240, 255))
    INUNDATED_GRASSLAND_SCRUB_BIOLOGICAL_INTEREST = (45, (145, 245, 245, 255))
    VEGETATION_RECENTLY_DISTURBED_AREA = (48, (148, 112, 0, 255))
    CONIFEROUS_TREES = (50, (50, 150, 50, 255))
    SMALL_CONIFEROUS_TREES = (51, (0, 151, 151, 255))
    BROADLEAVED_TREES = (55, (55, 255, 0, 255))
    SMALL_BROADLEAVED_TREES_SHRUBS = (56, (156, 255, 156, 255))

    NODATA11 = (11, (254,254,254,255)) # Not used
    NODATA46 = (46, (246,146,246,255)) # Not used
    NODATA100 = (100, (0, 0, 0, 255)) # Outside Belgium/Wallonia

if __name__ == "__main__":
    import numpy as np
    n = 4

    DIR = r'E:\MODREC-Vesdre\vesdre-data\LifeWatch'

    # Tif file is very large, so we need to use PIL to open it
    Image.MAX_IMAGE_PIXELS = 15885900000
    img = Image.open(DIR + r'\lifewatch_LC2018_vx19_2mLB08cog.tif',)
    img = np.asarray(img)

    ij11 = np.where(img == 11)
    ij46 = np.where(img == 46)

    print(ij11[0].shape) # must be 0
    print(ij11[1].shape) # must be 0

    img = img[::n,:-img.shape[1]//2:n]
    print(np.unique(img))

    img = Image.open(DIR +r'\lifewatch_LC2022_vx20_2mLB08cog.tif',)
    img = np.asarray(img)

    ij11 = np.where(img == 11) # must be 0
    ij46 = np.where(img == 46) # must be 0

    print(ij11[0].shape)
    print(ij11[1].shape)

    img = img[::n,:-img.shape[1]//2:n]
    print(np.unique(img))
