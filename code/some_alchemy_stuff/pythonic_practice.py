import sys
import math
import webbrowser 
def write(line):
	sys.stdout.write(line)


def cubed(x):
	return (x**3)

print(math.factorial(5)*4*2)
write("Carpe")
write(" ")
write("diem\n")

print(2*cubed(3))

raw_input("Hit enter to see webpage:")
webbrowser.open("https://twitter.com")



# from sys import argv
# version, switch1, switch2, switch3 = argv
# if switch1.lower()=="true":
# 	switch1 = True
# 	print "1a"
# else:
# 	switch1 = False
# 	print "1c"
# if switch2.lower()=="true":
# 	switch2 = True
# 	print "2a"
# else:
# 	switch2 = False
# 	print "2c"
# if switch3.lower()=="true":
# 	switch3 = True
# 	print "3a"
# else:
# 	switch3 = False
# 	print "3c"
# # print "switch1: " + str(switch1)
# # print "switch2: " + str(switch2)
# #print ops
# if switch1:
# 	word1 = "Good"
# 	word2 = "Morning"
# 	word3 = "to you too!"
# 	print word1, word2
# 	print word1 + word2
# 	print word1
# 	sys.stdout.write(word1)
# 	print "hello" + word1
# 	print "hello%s" % (word1)
# 	sentence = word1 + " " + word2 + " " +word3
# 	print sentence
# if switch2:
# 	a = 0
# 	while a < 10:
# 		print a,
# 		a = a + 1
# if switch3:
# 	tmp = 3
# 	if tmp.lower() == "3.5":
# 		print "wtf python, why u magical"
# 	tmp = "testing..1.2.3"
# 	print str(tmp)
# else:
# 	print "Oh noes"
