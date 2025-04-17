import csv

def load_csv_with_comma_quotas(filename, separator=',', delimiter='"'):
    rows = []

    # Load the CSV file using python built-in csv library:
    with open(filename, 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        x = 0
        for row in data:
            print(row)
            if x < 1:
                headers = row
            else:
                cols = {}
                for id, col in enumerate(row):
                    print(id, col)
                    cols[headers[id]] = col

                rows.append(cols)
            x = x + 1

    return rows