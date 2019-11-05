import os
from toolbox.ts2py.core import main

candidates = [
    '/Users/exiszhang/proj-exis/openvidu/openvidu-node-client/src/',
    'D:/dev/proj.node/openvidu/openvidu-node-client/src/',
]

base_dir = None
for candidate in candidates:
    if os.path.isdir(candidate):
        base_dir = candidate

if not base_dir:
    print("base_dir not found in any given locations, tried: ")
    for candidate in candidates:
        print('-', candidate)
    raise FileNotFoundError()

for file in os.listdir(base_dir):
    main(os.path.join(base_dir, file), os.path.join('../example/output/'))
