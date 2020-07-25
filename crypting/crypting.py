import os
import zipfile
from PIL import Image


def encrypt_files(image_path, directory_path, result_path):
    """Шифрует файлы в картинку
image_path - путь к картинке, которая возьмётся за основу трояна
directory_path - путь к папке, в которой находятся файлы, которые будут зашифрованы в картинку
result_path - путь, в котором появится троян"""

    zf = zipfile.ZipFile("data.zip", "w", compression=zipfile.ZIP_DEFLATED)
    for dirname, subdirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith("data.zip"):
                continue
            zf.write(os.path.join(dirname, filename),
                     arcname=os.path.join(dirname, filename).split("/")[-1].replace('\\',
                                                                                    '/'))

    # Придумать пароль
    zf.setpassword(b"poma_loh")
    zf.close()

    with open("data.zip", "rb") as zip_:
        with open(image_path, "rb") as img:
            res_img = img.read() + zip_.read()
    os.remove("data.zip")

    with open(result_path, "wb") as file:
        file.write(res_img)


def decrypt_file(image_path, file_path):
    '''Расшифровывает троян
image_path - путь к трояну
file_path - необходимый файл в трояне'''

    img = Image.open(image_path)
    x, y = img.size
    with zipfile.ZipFile(image_path) as zf:
        # Придумать пароль
        return zf.open(file_path, pwd=f"{x}{image_path.split('/')[-1]}{y}".encode("utf-8"))



encrypt_files('data.dji', 'data', '../data/data.dji')