import os
import subprocess

for root, dirs, files in os.walk('..'):
    subprocess.run(['fs', 'sa', root, 'jturner3', 'rlidwka'])
        
