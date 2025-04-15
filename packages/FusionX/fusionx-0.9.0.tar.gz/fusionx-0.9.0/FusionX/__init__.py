import os
import gdown


def save_cellx(url = 'https://drive.google.com/uc?id=1YQgjt29hUmt2JS5I1-cLUk8GVZ_mV_EF', output = 'CellX.pth'):
    home_dir = os.path.expanduser("~")
    hiden_folder_name = os.path.join(home_dir, ".cellx")
    output_path = os.path.join(home_dir, ".cellx", "CellX.pth")
    if not os.path.isfile(output_path):
        os.makedirs(hiden_folder_name, exist_ok=True)
        gdown.download(url, output_path, quiet=False)
save_cellx()
