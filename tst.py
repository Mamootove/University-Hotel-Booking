import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def resource_path(*paths):
    return os.path.join(BASE_DIR, *paths)

with open(resource_path("data" ,"users_dir.txt"), 'rb') as f:
    res = (pickle.load(f))

for r in res:
    print(f" {r}   --->   {res[r]}")