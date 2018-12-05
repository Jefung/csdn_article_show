# 系统变量
import logging
import os
import sys

project_name = "[项目名]"

# determine whether the program is running in user mode
# if it is in user mode, is_exe is True, otherwise it is False
is_exe = getattr(sys, 'frozen', False) is not False

# set user_data_dir
if os.getenv('APP' + 'DATA'):
    user_data_dir = os.path.join(os.getenv('APP' + 'DATA'), project_name)
else:
    user_data_dir = project_name

if not os.path.exists(user_data_dir):
    os.makedirs(user_data_dir)

# set debug and develop mode
is_debug = is_exe is False and os.path.exists(os.path.join(user_data_dir, 'debug'))

# set log file path and format
logging_file_path = os.path.join(user_data_dir, project_name + ".log")
logging.basicConfig(filename=logging_file_path, level=logging.INFO, format='%(asc''time)s:%(level''name)s:%(message)s')
project_dir = os.path.dirname(os.path.dirname(__file__))

# set sqlite db file
# db_file = os.path.join(user_data_dir, project_name + ".db")
db_file = r"C:\Users\jefun\Desktop\repos\csdn_spider\sqlite.db"
image_dir = r'C:\Users\jefun\Desktop\repos\csdn_spider\images'
