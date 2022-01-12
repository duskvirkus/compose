import subprocess

subprocess.call(['python', 'setup.py', 'clean'])
subprocess.call(['python', 'setup.py', 'install'])
subprocess.call(['python', '-m', 'pytest', './test/any'])