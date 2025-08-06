# - Create a file 'log.txt' with at least 5 lines of text.
# - Open the file using a context manager and read all lines.
# - Reset the file pointer.
# - Write the same content reversed (line order) to a new file 'reversed_log.txt'.

with open("log.txt") as f:
    data = f.readlines()
    # print(data)
    f.seek(0)
    # print(f.read(1))

with open("reversed_log.txt", 'w+') as f:
    data[0] = data[0][:-1]
    data[-1] = data[-1] + "\n"
    f.write(''.join(data[::-1]))