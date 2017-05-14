import bz2
import itertools
import codecs

file = "/Users/nobr/Documents/2017/RC_2017-02.bz2"
file_10000 = "test.txt"

# the original script using BZ2File ... and 3 lines for test
# ...and fixing bugs:
#     1) it only writes 9999 instead of 10000
#     2) files don't do writerow
#     3) close the files


with bz2.BZ2File(file, "r") as source_file:
    with codecs.open(file_10000, 'w+', 'utf-8') as output_file:
        count = 0
        for line in source_file:
            count += 1
            if count <= 3:
                output_file.write(line)

# show what you got
print('---- Test 1 ----')
print(repr(open(file_10000).read()))
