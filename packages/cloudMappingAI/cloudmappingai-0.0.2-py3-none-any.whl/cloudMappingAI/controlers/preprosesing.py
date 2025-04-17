from PIL import Image
import os


# fungsi yang dikusukan untuk mengubah format gambar tanpa variabel yang menampungnya sekala directory
def change_image_format_to_png_directory(path_directory_image,
                                         path_directory_output,
                                         image_format_before=".tif",
                                         image_format_after=".png"):
    """ 
    deskripsi : fungsi untuk mengubah format gambar setelit sekala directory. dengan dependensi yang dipakai PIL, PIL.Image, os

    Args:
        path_directory_image (_string_): path directory gambar
        path_directory_output (_string_): path directory gambar output
        image_format_before (_string_): format gambar sebelum diubah
        image_format_after (_string_): format gambar setelah diubah

    returns:
        None

    contoh penggunaan :
        change_image_format_to_png_directory(path_directory_image, path_directory_output)
    """
    list_image = os.listdir(path_directory_image)
    list_path_image = [os.path.join(path_directory_image, image)
                       for image in list_image if f"{image_format_before}" in image]
    for list_gambar in list_path_image:
        with Image.open(list_gambar) as image:
            print(list_gambar + " success konversi ke png")
            image.save(os.path.join(path_directory_output,
                       os.path.basename(list_gambar).split(".")[0] + f"{image_format_after}"))
    print(f"{len(list_path_image)} gambar berhasil di konversi ke png")
    print("konversi ke png selesai")


# fungsi yang dikusukan untuk mengubah format gambar tanpa variabel yang menampungnya sekala satu gambar
def change_image_format_to_png_for_on_image(path_image,
                                            path_output,
                                            image_format_after=".png"):
    """
    deskripsi : fungsi untuk mengubah format gambar setelit sekala satu gambar. dengan dependensi yang dipakai PIL, PIL.Image, os

    Args:
        path_image (_string_): path gambar sebelum diubah
        path_output (_string_): path gambar setelah diubah
        image_format_after (str, optional): format gambar setelah diubah. Defaults to ".png".

    returns:
        None

    contoh penggunaan :
        change_image_format_to_png_for_on_image(path_image, path_output)
    """
    with Image.open(path_image) as image:
        image.save(os.path.join(path_output,
                                os.path.basename(path_image).split(".")[0] + f"{image_format_after}"))
    print("konversi ke png selesai, gambar disimpan di :" + path_output)


# fungsi yang dikusukan untuk mengubah format gambar dengan variabel yang menampungnya sekala directory
def list_change_image_format_to_png_directory(path_directory_image,
                                              path_directory_output,
                                              image_format_before=".tif",
                                              image_format_after=".png"):
    """
    deskripsi : fungsi untuk mengubah format gambar setelit sekala directory dengan variabel yang menampungnya. dependensi yang dipakai PIL, PIL.Image, os

    Args:
        path_directory_image (_string_): path directory gambar
        path_directory_output (_type_): path directory gambar output
        image_format_before (str, optional): format gambar sebelum diubah . Defaults to ".tif".
        image_format_after (str, optional): format gambar setelah diubah. Defaults to ".png".

    Returns:
        _list_: list gambar path setelah diubah png

    contoh penggunaan :
        list_change_image_format_to_png_directory(path_directory_image, path_directory_output)
    """
    list_image = os.listdir(path_directory_image)
    list_path_image = [os.path.join(path_directory_image, image)
                       for image in list_image if f"{image_format_before}" in image]
    for list_gambar in list_path_image:
        with Image.open(list_gambar) as image:
            print(list_gambar + " success konversi ke png")
            image.save(os.path.join(path_directory_output,
                       os.path.basename(list_gambar).split(".")[0] + f"{image_format_after}"))
    print(f"{len(list_path_image)} gambar berhasil di konversi ke png")
    print("konversi ke png selesai")
    lis_output_image_png = [os.path.join(path_directory_output, image)
                            for image in os.listdir(path_directory_output)]
    return lis_output_image_png
