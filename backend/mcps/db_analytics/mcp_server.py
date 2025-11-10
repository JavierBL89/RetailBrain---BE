import kagglehub
import pandas as pd


df= pd.read_csv("/Users/javierbastandeleon/.cache/kagglehub/datasets/arge-shoe-dataset-ut-zappos50k/aryashah2k/Zappos50K.csv")
# Take the first 50 rows
df_small = df.head(50)

# Save to a new file
df_small.to_csv("db_analytics/small_dataset.csv", index=False)
print("Path to dataset files:", path)



# Start FastAPI as normal
if __name__ == "__main__":
    print("Server running")