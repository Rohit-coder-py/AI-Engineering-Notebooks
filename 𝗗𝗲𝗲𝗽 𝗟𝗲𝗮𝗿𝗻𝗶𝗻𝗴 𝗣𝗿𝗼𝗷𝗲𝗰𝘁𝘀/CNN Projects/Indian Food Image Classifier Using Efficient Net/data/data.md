To access the dataset you can simpley paste this link in your browser : \

Link : https://www.kaggle.com/datasets/iamsouravbanerjee/indian-food-images-dataset


Also dont forget to delete all folders expect the selected one on which final model has trained beacuase the dataset have more than 50 classes but we need only five 

You can use this code : 


'' py

import os
import shutil

dataset_path = r"privode dataset path"

keep_folders = {
    "biryani",
    "butter_chicken",
    "gulab_jamun",
    "naan",
    "palak_paneer"
}

for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)

    if os.path.isdir(folder_path) and folder not in keep_folders:
        shutil.rmtree(folder_path)
        print(f"Deleted: {folder}")

print("\n✅ Done! Only the 5 selected food classes remain.")