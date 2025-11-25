import kagglehub
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("./large-shoe-dataset-ut-zappos50k")

print("Path to dataset files:", path)



# Start FastAPI as normal
if __name__ == "__main__":
    print("Server running")


