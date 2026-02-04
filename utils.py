import os
import pandas as pd

def concatenate_files_exclude(directory_path, transcriptome, ex_folder="", extension=".sf"):
    """
    Process RNA-Seq quantification files from a directory, excluding a specified folder.
    
    Parameters:
    -----------
    directory_path : str
        Path to directory containing quantification files
    transcriptome : pandas.DataFrame
        Reference transcriptome with 'gene' and 'isoform' columns
    ex_folder : str, optional
        Folder to exclude from processing
    extension : str, optional
        File extension to filter (default: '.sf' for Salmon output)
        
    Returns:
    --------
    pandas.DataFrame
        Combined DataFrame with all quantification data
    int
        Number of files processed
    """
    dfs = []
    number_of_files = 0
    
    # Walk through directory tree
    for subdir, dirs, files in os.walk(directory_path):
        # Skip excluded folder if present
        if ex_folder in dirs:
            dirs.remove(ex_folder)
            
        # Process each matching file
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(subdir, file)
                
                # Read and preprocess file
                df = pd.read_csv(file_path, sep="\t").rename(columns={"Name": "isoform"})
                
                # Merge with transcriptome reference
                df = pd.merge(df, transcriptome, on="isoform", how="right").reset_index(drop=True)
                
                # Set multi-index and add source information
                df.set_index(["gene", "isoform"], inplace=True)
                
                # Extract sample name from path - more robust approach
                sample_name = os.path.basename(os.path.dirname(file_path))
                df["df_name"] = sample_name
                
                dfs.append(df)
                number_of_files += 1
                
    # Combine all dataframes
    if not dfs:
        return pd.DataFrame(), 0
        
    concatenated_df = pd.concat(dfs)
    return concatenated_df, number_of_files