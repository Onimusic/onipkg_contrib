def create_csv_on_memory(header, data):
    """Método para criar CSV na memória"""
    import csv
    from io import StringIO
    file = StringIO()

    # preparando o writer
    writer = csv.writer(file, dialect='excel', delimiter=',')
    writer.writerow(header)
    for item in data:
        writer.writerow(item)
    return file
