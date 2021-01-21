import os

import winshell

# winshell.desktop()获取桌面路径
# os.path.join(winshell.desktop(), "W32Dasm.lnk")组合路径
# 如：C:\Users\Administrator\Desktop\W32Dasm.lnk
# link_filepath = os.path.join(winshell.desktop(), "W32Dasm.lnk")
#
# with winshell.shortcut(link_filepath) as link:
#     link.path = "D:\W32DasmV10.0\W32Dasm.exe"  # 目标文件
#     link.working_directory = "D:\W32DasmV10.0"  # 起始位置
if __name__ == '__main__':

    PROGRAM_DATA_PATH = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\GEOVIA'
    print(winshell.desktop())
    lnk_list = os.listdir(PROGRAM_DATA_PATH)
    for lnk in lnk_list:
        lnk_file = os.path.join(PROGRAM_DATA_PATH, lnk)
        with winshell.shortcut(lnk_file) as link:
            print('path=' + link.path)
            print('work=' + link.working_directory)
