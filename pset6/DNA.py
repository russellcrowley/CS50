import sys
import csv
# printing debug statements are still in code to help, just uncomment
# check command line arguments
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit(0)
database = str(sys.argv[1])
DNA = str(sys.argv[2])
# open CSV file and read into memory
with open(database, "r") as database:
    csv_reader = csv.reader(database)
    candidates = list(csv_reader)
    # isolate STRs
    STR = candidates[0][1:]
# do the same for the DNA sequence
with open(DNA, "r") as DNA:
    sequence = ""
    for i in DNA:
        sequence += i
    # seq_len for indexing later
    seq_len = len(str(sequence))
STR_counts = []
# for each STR
for s in STR:
    # print("str is", s)
    max_count = 1
    temp_count = 0
    # at each point in the squence
    for i in range(seq_len):
        j = i + len(s)
        # print(sequence[i:j])
        # if the STR starts at that point
        if sequence[i: j] == s:
            temp_count += 1
            # go through the rest of sequence in STR sized blocks
            for k in range(j, seq_len, len(s)):
                # if the next block is also the STR
                if sequence[k: k + len(s)] == s:
                    # increase the counter and check if longest so far
                    temp_count += 1
                    if temp_count > max_count:
                        max_count = temp_count
                # break out of loop if doesn't match
                else:
                    temp_count = 0
                    break
        # put max_value into results string
    # print("max=", max_count)
    STR_counts.append(str(max_count))
# print(STR_counts)
# compare STR counts to each row in the CSV file for match
for person in candidates:
    # print(person)
    # person[0] is the name, the rest is their STR counts
    if person[1:] == STR_counts:
        print(person[0])
        sys.exit(0)
print("No match")
