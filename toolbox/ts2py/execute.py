import os
from toolbox.ts2py.core import main

if os.name == 'nt':
    system = 'windows'
    base_dir = 'D:/dev/proj.node/openvidu/openvidu-node-client/src/'
else:
    system = 'mac'
    base_dir = '/Users/exiszhang/proj-exis/openvidu/openvidu-node-client/src/'


for file in os.listdir(base_dir):
    main(os.path.join(base_dir, file), os.path.join('../example/out/'))
