import math
import random
from swampy.TurtleWorld import *
#
# world = TurtleWorld()
# bob = Turtle()
# print(bob)
#
# def square(t,length,d):
#     for i in range(4):
#         fd(bob,length)
#         lt(bob,d)
#
# def polygon(t,length,n):
#   for i in range(n):
#     fd(bob,length)
#     lt(bob,360/n)
#
#
#
# def cercle(bob,r):
#     circumference = 2*math.pi*r
#
#
#     polygon(bob,5,63)
#
# bob.delay = 0.01
# cercle(bob,50)
#
# wait_for_user()

# def check_fermat(a,b,c,n):
#     if(a**n + b**n == c**n):
#         print("Holy smokes,Fermat was wrong")
#     else :
#         check_fermat(random.randint(0,1000),random.randint(0,1000),random.randint(0,1000),n)
#
#
# check_fermat(2,3,4,3)



# world = TurtleWorld()
# t = Turtle()
# print(t)
#
# def draw(t, length, n):
#     if n == 0:
#         return
#
#     angle = 50
#     fd(t, length*n)
#     lt(t, angle)
#     draw(t, length, n-1)
#     rt(t, 2*angle)
#     draw(t, length, n-1)
#     lt(t, angle)
#     bk(t, length*n)
#
# #draw(t,10,10)
#
# def koch(t,length,n):
#     for i in range(4):
#         draw(t,length/3,n)
#         lt(t,60)


# #koch(t,100,2)
# def factorial(n):
#     space = ' ' * (4 * n)
#     print(space, 'factorial', n)
#     if n == 0:
#         print(space, 'returning 1')
#         return 1
#     else:
#         recurse = factorial(n-1)
#         result = n * recurse
#         print(space, 'returning', result)
#         return result
#
# factorial(10)

# def b(z):
#     prod = a(z, z)
#     print(z, prod)
#     return prod
# def a(x, y):
#     x = x + 1
#     return x * y
#
# def c(x, y, z):
#     total = x + y + z
#     square = b(total)**2
#     return square
# x = 1
# y = x + 1
# print(c(x, y+3, x+y))
#
# def first(word):
#     return word[0]
# def last(word):
#     return word[-1]
# def middle(word):
#     return word[1:-1]
#
# print(first('we') +
#      last('we') + '@@' +
#     middle('we'))
#
# def is_palindrome(word):
#
#
#     print(word[:(int(len(word)/2))])
#     print(word[int(len(word)/2)+1::][::-1])
#
#     if(word[:(int(len(word)/2))] == word[int(len(word)/2)+1::][::-1]):
#         print('yes')
#
#     else :
#         print('no')
#
# is_palindrome('redivider')

#rot13
#encryption string
#
# str  = 'idri'
#
# str1 = ''
# for c in str:
#
#     c1 = ord(c) + 7
#     str1 += chr(c1)
#
#
# print(str1)

#  digit numbers palindrome

#
"""
def is_palindrome(word):


     # print(word[:(int(len(word)/2))])
     # print(word[int(len(word)/2)+1::][::-1])

     if(word[:(int(len(word)/2))] == word[int(len(word)/2)+1::][::-1]):

         return True
         #print(word[:(int(len(word)/2))])
         #print('yes')

     else :
        pass # print('no')


for i in range(100000,999999):
    str_i = str(i)
    for j in range(0,6):
        if is_palindrome(str_i[j:]):
           if(len(str_i[j:])>1):
            print(str_i[j:])
"""

# Read file into dictionary
#
# fin = open('words.txt')
# line = fin.readline()
# word = line.split(' ')
# a = {}
# for c in word:
#    a[c] = ''
#
# print(a)

#Write a program that reads a word list from a file and prints the set of "anagrams"
#my version does not take anagrams as i am trying for something with same n of letters

#but adding am "is anagram function" can do it easily
# or checking if tuple (key of dict) contains all the chars of the word
#take each word sort the letters make a tuple which will be used as dictionary key




# fin = open('words.txt')
#
# dic = {}
# for line in fin.readlines() :
#     line = line.rstrip()
#     word = line.split(" ")
#
#     for word1 in word:
#
#         word2 = list(word1)
#         word2.sort()
#         word3 = tuple(word2)
#
#         dic.setdefault(word3,[]).append(word1)
#
#
#
# print(dic.values())

import pandas as pd
import json
import matplotlib.pyplot as plt

#read total profit of all months and show it using a line plot
# df = pd.read_csv('../Resources/sales_data.csv')
# profit_list = df['total_profit'].values
# months = df['month_number'].values
# plt.figure()
# plt.plot(months,profit_list,label = 'Month-wise Profit data of last year')
# plt.xlabel('Month number')
# plt.ylabel('Profit [$]')
# plt.xticks(months)
# plt.title('Company profit per month')
# plt.yticks([100e3,200e3,300e3,400e3,500e3])
# plt.show()

# df  = pd.read_csv('../Resources/sales_data.csv')
# profit_list = df['total_profit'].values
# months = df['month_number'].values
# plt.figure()
# plt.plot(months,profit_list,label = 'Total profit per month',color = 'r'
#          ,marker = 'o',markerfacecolor = 'k',linestyle = '-',linewidth = 3)
# plt.xlabel('months')
# plt.ylabel('profit_list')
# plt.xticks(months)
# plt.yticks([100e3,200e3,300e3,400e3,500e3])
# plt.show()

# df = pd. read_csv ('../Resources/sales_data.csv')
# profit_list = df['total_profit'].values
# plt. figure ()
# profit_range = [150e3 , 175e3 , 200e3 , 225e3 , 250e3 , 300e3 , 350e3]
# plt. hist ( profit_list , profit_range , label ='Profit data')
# plt. xlabel ('profit range [$]')
# plt. ylabel ('Actual Profit [$]')
# plt. legend (loc ='upper left' )
# plt. xticks ( profit_range )
# plt. title ('Profit data')
# plt. show ()

#7 bathing soap and face wash using subplot
"""""
df = pd.read_csv('../Resources/sales_data.csv')
months = df['month_number'].values
bathing_soap = df['bathingsoap'].values
face_wash = df['facewash']
f, axs = plt.subplots(2,1,sharex=True)
axs[0].plot(months,bathing_soap,label = 'Bathing Soap sales data',
            color = 'k', marker ='o',linewidth = 3)
axs[0].set_title('Sales data of Bathing soap')
axs[0].grid(True,linewidth = 0.5,linestyle = '--')
axs[0].legend()
axs[1].plot(months,face_wash,label = 'face wash sales data',
            color = 'r',marker = 'o',linewidth = 3)
axs[1].set_title('Sales data of face wash ')
axs[1].grid(True,linewidth = 0.5 , linestyle = '--')
axs[1].legend()

plt.xticks(months)
plt.xlabel('Month number')
plt.ylabel('Sales')
plt.show()
"""""
json_obj = '{ " Name ":" David " , " Class ":"I" , "Age ":6 }'

d = json.loads(json_obj)
print(type(d))
print(d)
d_data = json.dumps(d)

print(type(d_data))
print(d_data)
