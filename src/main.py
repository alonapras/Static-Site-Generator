import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

# use the sys.argv to grab the first CLI argument to the program. Save it as the basepath. If one isn't provided, default to /.
basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

# wsl
dir_path_static = "/mnt/d/workspace/notebook/Boot.Dev/08_Build-Static-Site-Generator/static"   
dir_path_public = "/mnt/d/workspace/notebook/Boot.Dev/08_Build-Static-Site-Generator/public"   
dir_path_content = "/mnt/d/workspace/notebook/Boot.Dev/08_Build-Static-Site-Generator/content"
template_path = "/mnt/d/workspace/notebook/Boot.Dev/08_Build-Static-Site-Generator/template.html"   

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
                             
    
main()

# base = "/home/jovyan/work/notebook/Boot.Dev/08_Build-Static-Site-Generator" # jupyter
# base = "d:/workspace/notebook/Boot.Dev/08_Build-Static-Site-Generator" # windows
# base = "/mnt/d/workspace/notebook/Boot.Dev/08_Build-Static-Site-Generator" # wsl
