import pandas as pd

# Load all CSVs
df1 = pd.read_csv("data/daily_sales_data_0.csv")
df2 = pd.read_csv("data/daily_sales_data_1.csv")
df3 = pd.read_csv("data/daily_sales_data_2.csv")

# Combine
df = pd.concat([df1, df2, df3])

# Keep only Pink Morsels
df = df[df["product"].str.lower() == "pink morsel"]

# Clean price column (remove $ and convert to float)
df["price"] = df["price"].astype(str).str.replace("$", "", regex=False)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Clean quantity
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# Create sales column
df["sales"] = df["quantity"] * df["price"]

# Keep required columns
df = df[["sales", "date", "region"]]

# Save
df.to_csv("task1_completed.csv", index=False)

print("Clean dataset created successfully.")