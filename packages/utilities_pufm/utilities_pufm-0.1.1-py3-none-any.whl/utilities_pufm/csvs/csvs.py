import pandas as pd
from ydata_profiling import ProfileReport

def save_and_report(df: pd.DataFrame, save_path: str) -> None:
    """Generates a data profiling report and saves it to a file.

    This function uses the `ydata_profiling` library to create a comprehensive
    profiling report for the provided DataFrame. The report is saved as a file
    at the specified path.

    Args:
        df (pd.DataFrame): The input DataFrame for which the profiling report is generated.
        save_path (str): The file path where the profiling report will be saved.
            The path should include the file name and extension (e.g., `.html`).

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified path is invalid or cannot be accessed.
        ValueError: If the DataFrame is empty or invalid for profiling.

    Example:
        >>> import pandas as pd
        >>> from ydata_profiling import ProfileReport
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> save_and_report(df, "output_report.html")
    """
    profile = ProfileReport(df, title="report")
    profile.to_file(save_path)
    
def save_csv_file(df: pd.DataFrame, save_path: str) -> None:
    """Saves a DataFrame to a CSV file.

    This function writes the contents of the provided DataFrame to a CSV file
    at the specified path.

    Args:
        df (pd.DataFrame): The input DataFrame to be saved as a CSV file.
        save_path (str): The file path where the CSV file will be saved.
            The path should include the file name and `.csv` extension.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified path is invalid or cannot be accessed.
        PermissionError: If the program lacks the necessary permissions to write to the file.
        ValueError: If the DataFrame is empty or invalid for saving.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> save_csv_file(df, "output_data.csv")
    """
    df.to_csv(path_or_buf=save_path)