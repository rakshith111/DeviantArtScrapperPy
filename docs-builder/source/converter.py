import glob
import os
import subprocess

print(os.getcwd())

for file in (glob.glob(os.path.join(os.getcwd()+'\docs-builder\source\*.rst'))):
    print("Converting", file)

    subprocess.run(["copy", f"{file}",f"{file}.bak"], shell=True)
    subprocess.run(["rst2myst", "convert",f"{file}"], shell=True)
    subprocess.run(["del", f"{file}", ], shell=True)
