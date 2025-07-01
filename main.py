import argparse
import csv
from tabulate import tabulate

parser_arguments = [
    ('--file', True),
    ('--where', False),
    ('--aggregate', False)]

aggregate_operations = ['avg', 'min', 'max']


def is_number(s: str) -> bool:
    s = s.strip()
    if s.startswith('-'):
        s = s[1:]
    if '.' in s:
        left, right = s.split('.', 1)
        return left.isdigit() and right.isdigit()
    return s.isdigit()


def filter_by_where(rows: list, where: str) -> list:
    result = []
    if '>' in where:
        column, value = where.split('>')
        column, value = column.strip(), value.strip()
        for row in rows:
            if column in row:
                cell = row[column]
                if is_number(cell) and is_number(value):
                    if float(cell) > float(value):
                        result.append(row)
                else:
                    if cell > value:
                        result.append(row)
    elif '<' in where:
        column, value = where.split('<')
        column, value = column.strip(), value.strip()
        for row in rows:
            if column in row:
                cell = row[column]
                if is_number(cell) and is_number(value):
                    if float(cell) < float(value):
                        result.append(row)
                else:
                    if cell < value:
                        result.append(row)
    elif '=' in where:
        column, value = where.split('=')
        column, value = column.strip(), value.strip()
        for row in rows:
            if column in row and row[column] == value:
                result.append(row)
    else:
        raise ValueError("Invalid where condition. Use >, <, or =.")
    return result


def aggregate(rows: list, aggregate: str) -> tuple:
    if '=' not in aggregate:
        raise ValueError("Invalid aggregate condition. Use =.")
    column, operation = aggregate.split('=')
    if operation not in aggregate_operations:
        raise ValueError(
            f"Invalid operation. Supported operations: {', '.join(aggregate_operations)}")
    if not rows:
        return operation, None
    if operation == 'avg':
        total = sum(float(row[column]) for row in rows if column in row)
        count = sum(1 for row in rows if column in row)
        result = total / count if count > 0 else None
    elif operation == 'min':
        result = min(float(row[column]) for row in rows if column in row)
    elif operation == 'max':
        result = max(float(row[column]) for row in rows if column in row)
    return operation, result


def open_file(file_path: str) -> list:
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            return rows
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    except Exception as e:
        raise Exception(f"An error occurred while opening the file: {e}")


def main():
    parser = argparse.ArgumentParser()
    for arg_name, is_required in parser_arguments:
        parser.add_argument(arg_name, required=is_required)
    args = parser.parse_args()

    rows = open_file(args.file)

    if args.where:
        rows = filter_by_where(rows, args.where)
    if args.aggregate:
        operation, result = aggregate(rows, args.aggregate)
        print(tabulate([{operation: result}], headers='keys', tablefmt="grid"))
    else:
        if rows:
            print(tabulate(rows, headers='keys', tablefmt="grid"))
        else:
            print("No rows found.")


if __name__ == "__main__":
    main()
