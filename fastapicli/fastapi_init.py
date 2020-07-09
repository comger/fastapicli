"""
FastApiCli
author comger@gmail.com

fastapi_init.py projectname
"""
import sys
import os
import shutil
import fastapicli


def init_project(to_path="fastapi_demo"):
    """ 初始化项目 """
    root = fastapicli.__path__[0]
    from_path = root + '/fastapidemo'
    to_path = f"{os.getcwd()}/{path}"
    shutil.copytree(from_path, to_path)
    print(f"success init {path}")
    

if __name__ == '__main__':
    if len(sys.argv)>1:
        path = sys.argv[1]
        init_project(path)



    
