import pandas as pd
df = pd.read_csv("student_data.csv")
print("Original DataFrame:")
print(df)
print("\nMissing values before processing:")
print(df.isnull().sum())
df['Age'] = df['Age'].fillna(df['Age'].mean())
df['Marks'] = df['Marks'].fillna(df['Marks'].mean())
print("\nMissing values after processing:")
print(df.isnull().sum())
Q1 = df['Marks'].quantile(0.25)
Q3 = df['Marks'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
print(f"\nMarks IQR bounds: {lower_bound:.2f} to {upper_bound:.2f}")
print("Before removing outliers:", df.shape)
df = df[(df['Marks'] >= lower_bound) & (df['Marks'] <= upper_bound)]
print("After removing outliers:", df.shape) 
print("\nCleaned DataFrame:")
print(df)
