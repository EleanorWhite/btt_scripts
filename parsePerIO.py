# The functionality of the program is based on btt output
# btt is a program that parses blktrace
# to start using it, take all your blktrace files and run
# blkparse -i input_filenames -d output_file_name


# This should be a file that has latency info from btt
# it will be of the form "time_of_io q2c_latency"
# you can create this with the command:
# btt -i blkparse_file -q lat.txt
#latFile = open('lat.txt_8,4_q2c.dat', 'r')

# This should be a file that has btt queue depth info
# it will be of the form "timestamp queue_depth_at_time"
# you can create this with the command:
# btt -i blkparse_file -Q qDepth
#depthFile = open('qDepth_8,4_aqd.dat', 'r')

# This should be a file with perIO info
perIO = open('perIO', 'r')

outputFile = open('genQDep', 'w')
latFile = open('latency.txt', 'w')

def parseLine(string):
    ''' Takes in a line of perio btt output and parses into a list of form
    (timestamp, action, blocknumber)
    returns an empty list if there is no info ''' 
    # different processes in the file are separated by lines of '-'s
    if (string[0:5] == '-----' or string == '\n'):
        return []
    else:
        resultsArr = string.split()

        # the first line of data will contain the drive number before 
        # the other data. We don't care about that, so we drop it.
        if resultsArr[1] == ':':
            resultsArr = resultsArr[2:]
        return resultsArr
   
def getSortedEntries():
    allEntries = []
    # add all useful lines to the entries
    for line in perIO:
        info = parseLine(line)
        if(not(info == [])):
            allEntries.append(info)
    sortedEntries = sorted(allEntries, key=lambda e:float(e[0]))
    sortedEntries = [x for x in sortedEntries if x[1] == 'Q' or x[1] == 'C']
    return sortedEntries

 
def getQDep():
    sortedEntries = getSortedEntries()
    qLen = 0
    firstFlag = True # this is true only the first time through the loop
    for entry in sortedEntries:
        # Dumb hacky way to avoid putting a newline on the last line
        #if (firstFlag):
        #    firstFlag = False
        #else:
        #    outputFile.write("\n")
        
        
        if entry[1] == 'Q':
            qLen += 1
        elif entry[1] == 'C':
            qLen -= 1
        else:
            print("One of the entries is invalid. Please check input")
        outputFile.write(str(entry[0]) + " " +  str(qLen) + "\n")


getQDep() 


def getLatency():
    perIO = open('perIO', 'r')
    startTime = 0
    for line in perIO:
        l = parseLine(line)
        if (l != []):
            if l[1] == 'Q':
                startTime = l[0]
            if l[1] == 'C':
                lat = float(l[0]) - float(startTime)
                latFile.write(str(startTime) + " " + str(lat) + "\n")

getLatency()

