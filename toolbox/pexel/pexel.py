from pypexels import PyPexels
import requests
from PIL import Image
import os
from multiprocessing import Pool

API_KEY = '563492ad6f917000010000014db666f070d64bec826d5746cf55d29d'
# OUTPUT_DIR = 'E:\\user\\Pictures\\!Wallpapers\\stock'
OUTPUT_DIR = os.path.abspath(__file__)

px = PyPexels(api_key=API_KEY)


def get_image(img_url):
    # open
    img = Image.open(requests.get(img_url, stream=True).raw)

    # determine filename
    filename = img_url.split('/')[-1]
    os.path.join(OUTPUT_DIR, filename)

    # save the image
    img.save(filename)
    # print success message
    print(f"{filename} saved.")


if __name__ == '__main__':

    popular_photos = px.curated(per_page=30)

    img_url_list = [photo.src['original'] for photo in popular_photos.entries]

    pool = Pool(processes=5)
    pool_output = pool.map(get_image, img_url_list)
    pool.close()
    pool.join()

