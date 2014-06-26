"""cQuery as implemented in Go, running via Python"""

import os
import subprocess

os.chdir("c:\studio\content\jobs\spiderman")
proc = subprocess.Popen(['cquery', '#MyBen'],
                        stdout=subprocess.PIPE,
                        shell=True)
for lin in proc.stdout.readlines():
    print lin.strip()
