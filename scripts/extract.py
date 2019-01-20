#!/usr/bin/env python
import glob
import subprocess

for file in glob.glob("../reports/*.pdf"):
    extract_file = file.replace("reports", "extracted").replace("pdf", "txt")
    print(extract_file)
    subprocess.call(["touch", extract_file])