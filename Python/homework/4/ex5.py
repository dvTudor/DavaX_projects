# - Each list in the data has 3 columns: date, stop, and start
# data = (
#     ['2021-01-01', 20, 10],
#     ['2021-01-02', 20, 18],
#     ['2021-01-03', 10, 10],
#     ['2021-01-04', 102, 100],
#     ['2021-01-05', 45, 25]
# )
#
# 1. Mutate the lists in the data to add one more element indicating the difference between the two integer numbers (stop - start) and add it at index 1.
# 2. Determine on which date this newly calculated value was the largest.
# 3. Print that date

data = (
    ['2021-01-01', 20, 10],
    ['2021-01-02', 20, 18],
    ['2021-01-03', 10, 10],
    ['2021-01-04', 102, 100],
    ['2021-01-05', 45, 25]
)

max_diff = 0
max_date = ""
for entry in data:
    diff = entry[-2] - entry[-1]
    entry.insert(1, diff)
    if diff > max_diff:
        max_diff = diff
        max_date = entry[0]

print(max_date)