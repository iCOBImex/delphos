import csv, codecs, cStringIO

class Latin1Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to latin-1
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("latin-1")

class LatinReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="latin-1", **kwds):
        f = Latin1Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [s.encode("utf-8") for s in row]

    def __iter__(self):
        return self

class LatinWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="latin-1", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__ == "__main__":
    writer = UnicodeWriter(open("some.csv", "wb"), csv.excel, "utf-8")
    test_arr = [["", "Altern 1", "Altern 2", "Altern 3"],["Crit 1", "4", "3", "3"],["Crit 2", "1", "0", "1"],["Crit 3", "2", "2", "2"]]
    writer.writerows(test_arr)