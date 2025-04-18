#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setup_main.py
@Time    :   2025/04/14
@Author  :   Winter.Yu 
@Version :   1.0
@Contact :   winter741258@126.com
@Desc    :   None
'''

# here put the import lib
import os
from pathlib import Path
import typer
from typing_extensions import Annotated
    
translate_pys = []

 
# 编译需要的py文件
def translate_dir(path, ignore_names, ignore_files):
    pathes = os.listdir(path)
    # if path != BASE_DIR and path != '__init__.py' in pathes:
    #     with open(os.path.join(path, '__init__.py'), 'w', encoding='utf8') as f:
    #         pass
    for p in pathes:
        if p in ignore_names:
            continue
        if p.startswith('__') or p.startswith('.') or p.startswith('build'):
            continue
        f_path = os.path.join(path, p)
        if f_path in ignore_files:
            continue
        if os.path.isdir(f_path):
            translate_dir(f_path, ignore_names, ignore_files)
        else:
            if not f_path.endswith('.py') and not f_path.endswith('.pyx'):
                continue
            if f_path.endswith('__init__.py') or f_path.endswith('__init__.pyx'):
                continue
            # with open(f_path, 'r', encoding='utf8') as f:
            #     content = f.read()
            #     if not content.startswith('# cython: language_level=3'):
            #         content = '# cython: language_level=3\n' + content
            #         with open(f_path, 'w', encoding='utf8') as f1:
            #             f1.write(content)
            cythonize_path = os.path.dirname(os.path.abspath(__file__))
            os.system(f'python {cythonize_path}/_cythonize.py ' + f_path + ' build_ext --inplace')
            translate_pys.append(f_path)
            f_name = '.'.join(f_path.split('.')[:-1])
            py_file = '.'.join([f_name, 'py'])
            c_file = '.'.join([f_name, 'c'])
            # print(f"f_path: {f_path}, c_file: {c_file}, py_file: {py_file}")
            if os.path.exists(c_file):
                os.remove(c_file)
 
 
# 移除编译临时文件
def remove_dir(path, rm_path=True):
    if not os.path.exists(path):
        return
    pathes = os.listdir(path)
    for p in pathes:
        f_path = os.path.join(path, p)
        if os.path.isdir(f_path):
            remove_dir(f_path, False)
            os.rmdir(f_path)
        else:
            os.remove(f_path)
    if rm_path:
        os.rmdir(path)
 
 
# 移动编译后的文件至指定目录
def mv_to_packages(path, package_path, ignore_move):
    pathes = os.listdir(path)
    for p in pathes:
        if p.startswith('.'):
            continue
        if p in ignore_move:
            continue
        f_path = os.path.join(path, p)
        if f_path == package_path:
            continue
        p_f_path = f_path.replace(path, package_path)
        if os.path.isdir(f_path):
            if not os.path.exists(p_f_path):
                os.mkdir(p_f_path)
            mv_to_packages(f_path, p_f_path, ignore_move)
        else:
            if not f_path.endswith('.py') or f_path not in translate_pys:
                with open(f_path, 'rb') as f:
                    content = f.read()
                    with open(p_f_path, 'wb') as f:
                        f.write(content)
            if f_path.endswith('.pyd') or f_path.endswith('.so'):
                os.remove(f_path)
 
 
# 将编译后的文件重命名成：源文件名+.pyd，否则编译后的文件名会类似：myUtils.cp39-win_amd64.pyd ,just for test
def batch_rename(src_path, package_path):
    filenames = os.listdir(src_path)
    same_name = []
    package_name = Path(package_path).stem
    base_name = Path(package_path).parent
    translate_files = [(Path(file_path).parent, Path(file_path).stem) for file_path in translate_pys]
    # count = 0
    for filename in filenames:
        old_name = os.path.join(src_path, filename)
        if old_name == package_path:
            continue
        if os.path.isdir(old_name):
            # batch_rename(old_name, package_path)
            continue
        if filename[-4:] == ".pyd" or filename[-3:] == ".so":
            old_pyd = filename.split(".")
            new_pyd = str(old_pyd[0]) + "." + str(old_pyd[2])
        else:
            continue
        change_name = new_pyd
        # count += 1
        file_path = ''
        for p, f in translate_files:
            if change_name.replace('.pyd', '') == f:
                suffix = p.as_posix().split(base_name.as_posix())[1]
                p_ =  base_name / package_name / suffix.lstrip('/')
                # print(p_)
                file_path = (p_).as_posix()
                break
        if file_path:
            new_name = os.path.join(file_path, change_name)
            if change_name in filenames:
                same_name.append(change_name)
                continue
            os.rename(old_name, new_name)
            print(f"renamed {old_name} to {new_name}")

            
# 将编译后的文件重命名成：源文件名+.pyd，否则编译后的文件名会类似：myUtils.cp39-win_amd64.pyd
def rename_files(src_path):
    filenames = os.listdir(src_path)
    same_name = []
    count = 0
    for filename in filenames:
        old_name = os.path.join(src_path, filename)
        if old_name == src_path:
            continue
        if os.path.isdir(old_name):
            rename_files(old_name)
        if filename[-4:] == ".pyd" or filename[-3:] == ".so":
            old_pyd = filename.split(".")
            new_pyd = str(old_pyd[0]) + "." + str(old_pyd[2])
        else:
            continue
        change_name = new_pyd
        count += 1
        new_name = os.path.join(src_path, change_name)
        if change_name in filenames:
            same_name.append(change_name)
            continue
        os.rename(old_name, new_name)
        print(f"renamed {old_name} to {new_name}")
 
 
def run(project_dir: Annotated[str, typer.Option("--project-dir", help="需要编译的文件夹绝对路径", prompt=True)],
         package_name: Annotated[str, typer.Option("--package-name", help=" 打包文件夹名", prompt=True)],
        #  package: Annotated[bool, typer.Option("--package", help="是否将编译打包到指定文件夹内 (True)，还是和源文件在同一目录下(False)，默认True", prompt=True)] = True,
         ignore_files: Annotated[str, typer.Option("--ignore-files", help="项目根目录下不用（能）转译的py文件（夹）名，用于启动的入口脚本文件一定要加进来，多个文件名用逗号隔开",
                                                         prompt=True)] = None,
         ignore_names: Annotated[str, typer.Option("--ignore-names", help="项目子目录下不用（能）转译的'py文件（夹）名，多个文件名用逗号隔开",
                                                         prompt=True)] = None,
         ignore_move: Annotated[str, typer.Option("--ignore-move", help="不需要复制到编译文件夹的文件或者文件夹，多个文件名用逗号隔开",
                                                        prompt=True)] = None
         ):
    # 项目根目录下不用（能）转译的py文件（夹）名，用于启动的入口脚本文件一定要加进来
    # ignore_files = ['build', 'package', 'venv', '__pycache__', '.git', 'setup.py', 'setup_main.py', 'server.py', '__init__.py', 'app.py']
    ignore_files = (ignore_files.split(',') + ['build', 'package', 'venv', '__pycache__', '.git', 'setup.py', '__init__.py'] if ignore_files.lower() != 'none' 
                    else ['build', 'package', 'venv', '__pycache__', '.git', 'setup.py', '__init__.py'])
    # 项目子目录下不用（能）转译的'py文件（夹）名
    # ignore_names = ['__init__.py', 'exclude.py', 'app.py']
    ignore_names = (ignore_names.split(',') + ['__init__.py'] if ignore_names.lower() != 'none' 
                    else ['__init__.py'])
    # 不需要复制到编译文件夹的文件或者文件夹
    # ignore_move = ['venv', '__pycache__', 'server.log', 'setup.py', 'setup_main.py']
    ignore_move = (ignore_move.split(',') + ['venv', '__pycache__', 'server.log', 'setup.py', '.git'] if ignore_move.lower() != 'none' 
                   else ['venv', '__pycache__', 'server.log', 'setup.py', '.git'])
    # 需要编译的文件夹绝对路径
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = Path(project_dir).resolve().as_posix()
    # 将以上不需要转译的文件(夹)加上绝对路径
    ignore_files = [os.path.join(BASE_DIR, x) for x in ignore_files] if ignore_files else []
    # 是否将编译打包到指定文件夹内 (True)，还是和源文件在同一目录下(False)，默认True
    package = True
    if package:
        package_path = os.path.join(BASE_DIR, package_name)
    # 若没有打包文件夹，则生成一个
    if not os.path.exists(package_path):
        os.mkdir(package_path)
    translate_dir(BASE_DIR, ignore_names, ignore_files)
    # build_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')
    build_path = os.path.join(BASE_DIR, 'build')
    remove_dir(build_path)
    # print('build_path: ', build_path)
    print('removing build directory...')
    if package:
        mv_to_packages(BASE_DIR, package_path, ignore_move)
    # print(translate_pys)
    # batch_rename(os.path.dirname(os.path.abspath(__file__)), package_path)
    rename_files(package_path)
 

def main():
    typer.run(run)
    # translate_pys
 
if __name__ == '__main__':
    # run()
    main()