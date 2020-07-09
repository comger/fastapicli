"""
FastApiCli
author comger@gmail.com

fastapi_api.py -m Project -n 中文名称 -o cms所在跨径
建议在项目 main.py 文件同级建议
"""
import sys
import os
import shutil
import argparse
from tornado import template
import fastapicli


def init_logic(model, output=""):
    """ 生成逻辑代码"""
    loader = template.Loader('.')
    source_path = f"{fastapicli.__path__[0]}/logic.pyt"
    pyfbody = loader.load(source_path).generate(Model=model)
    # 保存位置
    path = f"{output}cms/logic/{str.lower(model)}.py"
    print("success created at", path)
    f = open(path, "w")
    f.write(str(pyfbody, encoding='utf-8'))
    f.close()

def init_api(model, name, output=""):
    """ 生成接口代码"""
    loader = template.Loader('.')
    source_path = f"{fastapicli.__path__[0]}/api.pyt"
    pyfbody = loader.load(source_path).generate(Model=model, name=name)
    # 保存位置
    path = f"{output}cms/api/{str.lower(model)}.py"
    print("success created at", path)
    f = open(path, "w")
    f.write(str(pyfbody, encoding='utf-8'))
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='model', type=str, default='Demo', help='target model')
    parser.add_argument('-n', '--name', dest='name', type=str, default='资源', help='target name')
    parser.add_argument('-o', '--output', dest='output', type=str, default="", help='target output folder')
    args = parser.parse_args()
    init_logic(args.model, args.output)
    init_api(args.model, args.name ,args.output)


