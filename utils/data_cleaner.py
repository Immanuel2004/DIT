def clean_data(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w]", "", regex=True)
    )
    df = df.dropna(how="all")             # drop rows with all NaNs
    df = df.loc[:, ~df.columns.duplicated()]  # remove duplicate columns
    return df.reset_index(drop=True)
