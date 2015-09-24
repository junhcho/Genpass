#!/usr/bin/env python
import sys
import random

# to do:
# Clean up main

# constant definitions
lower = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
upper = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
symbols = ['!','@','#','$','%','^','&','*','(',')']
numbers = [0,1,2,3,4,5,6,7,8,9]
top = ['q','w','e','r','t','y','u','i','o','p']
mid = ['a','s','d','f','g','h','j','k','l']
bot = ['z','x','c','v','b','n','m']
WORD_MIN = 5
WORD_MAX = 12

# read the files
byLength = {5:open('res/5').readlines(),
            6:open('res/6').readlines(),
            7:open('res/7').readlines(),
            8:open('res/8').readlines(),
            9:open('res/9').readlines(),
            10:open('res/10').readlines(),
            11:open('res/11').readlines(),
            12:open('res/12').readlines(),
            13:open('res/13').readlines(),
            14:open('res/14').readlines(),
            15:open('res/15').readlines(),
            16:open('res/16').readlines(),
            17:open('res/17').readlines(),
            18:open('res/18').readlines(),
            19:open('res/19').readlines()}

types = {'l':lower,'u':upper,'s':symbols,'n':numbers}

r = random.SystemRandom()

# randomChar() will return a random element from given list.
def randomChar(list):
    elements = len(list)
    return str(random.choice(list))

# randomChars() will return a randomly generated string with "length"
#   characters, where "use" is a list of characters which correspond to a set
def randomChars(length, use):
    rpass = ''
    for i in range (0,length):
        rpass += randomChar(types[r.choice(use)])
    return rpass

# findRange(n,c) finds the indices of byLength[n] where the first letter is c
def findRange(n,c):
    sindex=-1
    eindex=-1
    for linenum in range(len(byLength[n])):
        if sindex is -1 and byLength[n][linenum][0] == c:
            sindex = linenum
        if sindex >= 0 and byLength[n][linenum][0] != c:
            eindex = linenum-1
            break
    return [sindex,eindex]

# randomWord() will return a random word of length n, starting with character c
def randomWord(n,c=0):
    if n<WORD_MIN:
        n=WORD_MIN
    if n>WORD_MAX:
        n=WORD_MAX
    if not c: # no alphabet requirement
        return r.choice(byLength[n])[:-1]
    else:
        pair = findRange(n,c)
        return r.choice(byLength[n][pair[0]:pair[1]])[:-1]

# randomWords(n) will return a number of words matching n characters
def randomWords(n,word=0):
    if n > 5000:
        n = 5000
        print("Maximum is currently 5000 characters.")
    rWords = ''
    # if there is space for the maximum length,
    if n >= WORD_MAX+WORD_MIN:
        lw = r.randint(WORD_MIN,WORD_MAX)
        rWords += randomWord(lw) + " " + randomWords(n-lw)
        return rWords
    else:
        if n>2*WORD_MIN:
            return randomWord(WORD_MIN) + " " + randomWord(n-WORD_MIN)
        else:
            return randomWord(n)

def randomString(lengths,word):
    if not word:
        return ''
    if len(word) is not len(lengths):
        return "Lengths mismatch"
    else:
        return randomWord(int(lengths[0]),word[0]) + " " + randomString(lengths[1:],word[1:])

def query(length,char=0):
    if length > WORD_MAX or length < WORD_MIN:
        return "Lengths range from " + str(WORD_MIN) + " to " + str(WORD_MAX)
    if not char:
        return len(byLength[length])
    else:
        pair = findRange(length,char)
        return pair[1]-pair[0]

# printHelp() does what it says it will do (also exits)
def printHelp():
    print("\nusage: genpass.py [-c num_chars included_chars] [-w num_chars] [-s L1L2...Ln string]")
    print("included_chars can include l, u, s or n (lower, upper, symbols, numbers)")
    print("L1L2...Ln where n = length of string")
    print("example: genpass.py -w 12 -c 3 lusn -s 565 lol\n")
    sys.exit()

# main prints output based on given parameters.
def main():
    numargs = len(sys.argv)-1
    arglist = sys.argv[1:]
    validinput = {'-c':2,'-w':2,'-s':2,'-q':2} # value is maximum arguments
    if not arglist: # no parameters
        printHelp()
    else:
        joblist = []
        index = 0
        while index < numargs:
            command = arglist[index]
            if command in validinput:
                job = []
                job.append(command)
                for x in range(1,numargs+1):
                    if index+x >= numargs:
                        joblist.append(job)
                        index+=x
                        break
                    if arglist[index+x] not in validinput:
                        job.append(arglist[index+x])
                    else:
                        index+=x
                        joblist.append(job)
                        break
            else:
                index+=1
        for job in joblist:
            input_valid = len(job)-1 # 0 if invalid; otherwise, number of parameters not including command
            if input_valid > validinput[job[0]]:
                print(str(input_valid) + " " + str(validinput[job[0]]))
                input_valid = 0
            try:
                int(job[1])
            except ValueError:
                input_valid = 0
            if input_valid:
                if job[0] == '-c':
                    if input_valid == 1:
                        print(randomChars(int(job[1]),"lun"))
                    elif input_valid == 2:
                        for char in job[2]:
                            if not char in types:
                                input_valid = 0
                        if input_valid:
                            print(randomChars(int(job[1]),job[2]))
                elif job[0] == '-w':
                    if input_valid == 1:
                        print(randomWords(int(job[1])))
                    else:
                        input_valid = 0
                elif job[0] == '-s':
                    # lowercase letters only.
                    lowercase = ''
                    for char in job[2]:
                        if char in upper:
                            lowercase += char.lower()
                        elif char in lower:
                            lowercase += char
                    print(randomString(job[1],lowercase))
                elif job[0] == '-q':
                    if input_valid == 2:
                       if job[2] in upper or job[2] in lower:
                            job[2] = job[2].lower()
                            print(query(int(job[1]),job[2]))
                    elif input_valid == 1:
                        print(query(int(job[1])))
                    else:
                        input_valid = 0
                else:
                    printHelp()
main()
