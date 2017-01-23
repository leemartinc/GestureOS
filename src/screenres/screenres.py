import subprocess

command = subprocess.Popen(["fbset" , "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

rawOutput, error = command.communicate()

output = rawOutput.decode("utf-8")

lines = output.split("\n")
info = lines[2].strip().split(" ")
width = int(info[1])
height = int(info[2])