file = "dieText"
dies_lyst = []
with open (file, "r") as rf:
    while True:
        line = rf.readline()

        if line == "":
            break
        line = line.rstrip('\n')
        die_lyst = list(line)

        dies_lyst.append(die_lyst)


    print(dies_lyst)


