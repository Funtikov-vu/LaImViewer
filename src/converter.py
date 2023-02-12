from PIL import Image
Image.MAX_IMAGE_PIXELS = None

class Converter:
    '''
    imagepath -> tiles and info
    '''
    def __init__(self, image_path: str, tile_dir: str, tile_size: int, lvl_nums: int):
        self.image_path = image_path
        self.tile_dir = tile_dir
        self.tile_size = tile_size
        self.lvl_nums = lvl_nums

    def make_tiles(self):
        lvl = 0
        while lvl < self.lvl_nums:
            lvl_w = 99
            x0 = 0
            while x0:
                pass

