lst = [[1, 1, 1], [0, 4, 0], [3, 3, -1]]

# Maximum using first element
# print(max(lst, key=lambda x: x[0]))
# [3, 3, -1]



# Maximum using third element
# print(max(lst, key=lambda x: x[2]))
# [1, 1, 1]

# Maximum using sum()
# print(max(lst, key=sum))
# [3, 3, -1]

# Maximum using max
# print(max(lst, key=max))
# [3, 3, -1]
#
# # Maximum using min
# print(max(lst, key=min))
# # [1, 1, 1]



naj = max(lst, key=max)
ind = lst.index(naj)



a = [ j in i for i in lst for j in i]


print(a)

