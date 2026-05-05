from csv_loader import load_csv


# test the CSV loader
def main():

    file_path = "data/test.csv"

    dataframe = load_csv(file_path)

    print(dataframe.head())


if __name__ == "__main__":
    main()

    
