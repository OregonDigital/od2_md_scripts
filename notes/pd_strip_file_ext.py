import pandas as pd

# Specify dtype for the 'file' column
df = pd.read_excel('pd_strip_file_ext.xlsx', dtype=str)

# Now, df['file'] will preserve the full filenames with extensions
for filename in df['file']:
    print(filename)
