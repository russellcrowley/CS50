# Get string from user
text = input("Text: ")
letters = 0
words = 1
sentences = 0

for letter in text:
    if letter.isalpha():
        letters += 1
    elif letter == ' ':
        words += 1
    # count sentences
    elif letter == '.' or letter == '?' or letter == '!':
        sentences += 1
# implement Coleman-Law index
L = (letters / words) * 100
S = (sentences / words) * 100
index = 0.0588 * L - 0.296 * S - 15.8
# output statement
if index < 1:
    print('Before Grade 1')
elif index >= 16:
    print('Grade 16+')
else:
    print(f'Grade {round(index)}')

