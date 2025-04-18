import pandas as pd

def bacen_search(keyword):
    """
    Searches for a keyword in the 'Full_Name' field of a local .txt file.

    Parameter:
        keyword (str): Keyword to search for.

    Returns:
        DataFrame with the filtered results.
    """
    # Fixed path to the .txt file
    file_path = "C:/Users/lisan/OneDrive/Documentos/Python Scripts/BacenAPI/Date/dataset.txt"
    
    # Simple file reading (adjust the separator if necessary)
    df = pd.read_csv(file_path, sep=";")
    
    # Filter by partial match (case-insensitive)
    results = df[df['Full_Name'].str.contains(keyword, case=False, na=False)].copy()
    
    # Select and adjust the desired columns
    results = results[['Code', 'Full_Name', 'Unit', 'Periodicity']]
    results['Full_Name'] = results['Full_Name'].str.slice(0, 50)
    
    return results
