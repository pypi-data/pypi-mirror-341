# Cythonize Python Project

please change the project root directory and run `cyze --help` to see the usage


Usage: cyze [OPTIONS]                                                                                                                          

--project-dir         TEXT  需要编译的文件夹绝对路径 [default: None] [required]   

--package-name        TEXT  打包文件夹名 [default: None] [required] 

--ignore-files        TEXT  项目根目录下不用（能）转译的py文件（夹）名，用于启动的入口脚本文件一定要加进来，多个文件名用逗号隔开  [default: None] 

--ignore-names        TEXT  项目子目录下不用（能）转译的'py文件（夹）名，多个文件名用逗号隔开 [default: None]

 --ignore-move         TEXT  不需要复制到编译文件夹的文件或者文件夹，多个文件名用逗号隔开 [default: None]

 --help                      Show this message and exit.  


