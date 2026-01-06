import os
import shutil
import re


def copy_static():
    path_dst = "public" if os.path.exists("public") else None
    if path_dst is None:
        os.mkdir("public")
        path_dst = "public"
    else:
        remove_all(path_dst)

    path_src = "static" if os.path.exists("static") else None
    if path_src is None:
        raise EnvironmentError("static dir not found")

    shutil.copytree(dst=path_dst, src=path_src, dirs_exist_ok=True)


def remove_all(path):
    if not os.path.isdir(path):
        os.remove(path)
        print(f"{path} removed")
        return

    dir_list = os.listdir(path)
    for element in dir_list:
        new_path = os.path.join(path, element)
        remove_all(new_path)
        if os.path.isdir(new_path):
            os.removedirs(new_path)
            print(f"{new_path} dir removed")
