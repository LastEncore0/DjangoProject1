import os
import subprocess
import time
import webbrowser

django_project_path = os.getcwd()
os.chdir(django_project_path)

if not os.path.exists("manage.py"):
    print("❌ 未找到 manage.py，请检查当前目录:", django_project_path)
    exit(1)

try:
    server = subprocess.Popen(
        [r"C:\Python312\python.exe", "manage.py", "runserver"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # 等 3 秒，看看进程是否已退出
    time.sleep(3)

    # poll() 为 None 表示子进程还在运行；否则已退出
    return_code = server.poll()
    if return_code is not None:
        # 进程已退出，打印错误信息
        stdout_data, stderr_data = server.communicate()
        print("❌ Django 服务器进程已退出，错误日志如下：\n", stderr_data)
        exit(1)

    # 若进程存活，就打开浏览器
    webbrowser.open("http://127.0.0.1:8000/")

except Exception as e:
    print(f"❌ 错误：无法启动 Django 服务器 -> {str(e)}")
    exit(1)
