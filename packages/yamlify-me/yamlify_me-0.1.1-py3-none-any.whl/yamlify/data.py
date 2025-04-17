import yaml
import glob
import os

def read_folder(directory, path, data, index):
    files = glob.glob(f"{os.path.join(directory, path)}/*.yaml")
    for file in files:
        print ('reading file:', file)
        # Get name without extension
        name = file[0:-5]
        with open(file, 'r', encoding='utf-8') as stream:
            try:
                index[name] = yaml.safe_load(stream)
                data.append(index[name])
            except yaml.YAMLError as exc:
                print(exc)