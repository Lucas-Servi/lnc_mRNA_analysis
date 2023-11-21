import os
import pandas as pd

def concatenate_files_exclude(directory_path, transcriptome, ex_folder="", extension=".sf"):
    # Walks through the directory looking for files with a given extension
    # Returns a concatenated dataframe and the number of files loaded
    double_index = list(zip(transcriptome["gene"], transcriptome["isoform"]))
    dfs = []
    number_of_files = 0
    for subdir, dirs, files in os.walk(directory_path):
        # Skip the "folder" in the directory
        if ex_folder in dirs:
            dirs.remove(ex_folder)
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(subdir, file)
                df = pd.read_csv(file_path, sep="\t").rename(columns={"Name":"isoform"})
                df = pd.merge(df,transcriptome, on="isoform", how="right").reset_index()
                df.set_index(["gene","isoform"],inplace=True)
                df["df_name"] = file_path.split("/")[-2]
                dfs.append(df)
                number_of_files += 1
    concatenated_df = pd.concat(dfs)
    return concatenated_df, number_of_files
