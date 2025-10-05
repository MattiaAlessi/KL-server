import subprocess

subprocess.run("pip install -r requirements.txt", shell=True)

subprocess.Popen("python logger.py", shell=True)