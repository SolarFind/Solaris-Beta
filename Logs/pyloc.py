import json
with open("users.log") as f:
  z = f.read()
  f.close()
z = z.replace("\n",",")  
z = "["+z+"]"
print(z)
with open("users.log.json", "w") as f:
  f.write(z)
