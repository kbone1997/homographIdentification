s = "       hello world     "
s = s.strip(" ")
test = s.split(" ")
length = len(test)
t = test[length - 1]
print(len(t))