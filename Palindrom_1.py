# TODO здесь писать код
text = input('Введите строку: ')

quantity = len(text)
dict = {}

for letter in text:
    if letter not in dict:
        dict[letter] = 1
    else: dict[letter] += 1

count = 0
for i_values in dict.values():
    if i_values % 2 != 0:
        count += 1


if count <= 1:
    print('Можно сделать полиндром.')

else: print('Нельзя сделать полиндромом.')



