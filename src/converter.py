from PIL import Image

Image.MAX_IMAGE_PIXELS = None
import os

META_FILENAME = 'info.txt'


class Converter:
    '''
    imagepath -> tiles and info
    meta: image resolution
    '''

    def __init__(self, image_path: str, tile_dir: str, tile_size: int, lvl_nums: int, ext: str):
        self.image_path = image_path
        self.tile_dir = tile_dir
        self.tile_size = tile_size
        self.lvl_nums = lvl_nums
        self.image = Image.open(image_path)
        self.make_tile_dirs()
        self.ext = ext

    def make_tile_dirs(self):
        os.makedirs(self.tile_dir, exist_ok=True)
        for i in range(self.lvl_nums):
            os.makedirs(os.path.join(self.tile_dir, str(i)), exist_ok=True)

    def coords_fname(self, x0, y0, x1, y1, ext='png'):
        return f"{str(x0)}_{str(y0)}_{str(x1)}_{str(y1)}.{ext}"

    def generate_meta(self):
        meta = {
            'height': self.image.height,
            'width': self.image.width,
            'tile_dir': self.tile_dir,
            'image_path': self.image_path,
            'tile_size': self.tile_size,
            'lvl_nums': self.lvl_nums,
            'ext': self.ext
        }
        meta_path = os.path.join(self.tile_dir, META_FILENAME)
        with open(meta_path, 'w') as f:
            for key in meta:
                f.write(key+":")
                f.write(str(meta[key]))
                f.write('\n')
        return meta

    def make_tiles(self):
        x0 = 0
        while x0 < self.image.width:
            x1 = x0 + self.tile_size
            x1 = min(x1, self.image.width)
            y0 = 0
            while y0 < self.image.height:
                y1 = y0 + self.tile_size
                y1 = min(y1, self.image.height)
                tile = self.image.crop((x0, y0, x1, y1))
                lvl = 0
                tile.save(os.path.join(self.tile_dir, str(lvl), self.coords_fname(x0, y0, x1, y1)))
                w = tile.width
                h = tile.height
                lvl = 1
                while lvl < self.lvl_nums:
                    w //= 2
                    h //= 2
                    if w < 2:
                        w = 2
                    if h < 2:
                        h = 2
                    tile_level = tile.resize((w, h))
                    tile_level.save(os.path.join(self.tile_dir, str(lvl), self.coords_fname(x0, y0, x1, y1)))
                    tile_level.close()
                    lvl += 1
                tile.close()
                y0 = y1
            x0 = x1


# if __name__ == "__main__":
#     import datetime

#     s1 = datetime.datetime.now()
#     params = {
#         'image_path': r"C:\Users\buriv\PycharmProjects\LaIm\ex1.jpeg",
#         'tile_dir': r"C:\Users\buriv\PycharmProjects\LaIm\tiles",
#         'tile_size': 2000,
#         'lvl_nums': 5,
#         'ext': 'png'
#     }
#     conv = Converter(**params)
#     conv.make_tiles()
#     conv.generate_meta()
#     print(datetime.datetime.now() - s1)
#     conv.image.close()
