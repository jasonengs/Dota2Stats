import json

import pandas as pd


def rename_columns(df):
    columns = df.columns.to_list()
    results = []
    for i in columns:
        split_column_name = i.split("_")

        if len(split_column_name) > 1:
            results.append(
                split_column_name[0]
                + "".join(word.capitalize() for word in split_column_name[1:])
            )

        else:
            results.append(split_column_name[0])
    return results


def move_columns(df, start, end, at):
    col = df.columns.tolist()

    cols_to_move = col[start:end]
    cols_to_keep = [c for c in col if c not in cols_to_move]

    insert_col_at = at

    new_col_order = (
        cols_to_keep[:insert_col_at] + cols_to_move + cols_to_keep[insert_col_at:]
    )

    return new_col_order


def main():
    df = pd.read_csv("./assets/data/latest_data.csv")

    # Rename columns
    renamed_column = rename_columns(df)

    for i, col in enumerate(df.columns):
        df.columns.values[i] = renamed_column[i]

    # Save to JSON
    df.to_json("./assets/data/latest_data.json", orient="records")

    stats_key = df.columns.to_list()[5:27]

    images_key = df.columns.to_list()[27:]

    with open("./assets/data/latest_data.json", "r") as f:
        data = json.load(f)

    for hero in data:
        hero["stats"] = {key: hero.pop(key) for key in stats_key if key in hero}
        hero["images"] = {key: hero.pop(key) for key in images_key if key in hero}

    with open("./assets/data/latest_data.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()
