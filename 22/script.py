with open("input.txt", "r") as file:
    input = file.readlines()
    # remove newline characters and parse int
    input = [int(x.strip()) for x in input]

seeds = input


def mix(secretNumber, val):
    return secretNumber ^ val


def prune(secretNumber):
    return secretNumber % 16777216


def getRandomNumber(secretNumber):
    secretNumber = prune(mix(secretNumber, secretNumber * 64))
    secretNumber = prune(mix(secretNumber, secretNumber // 32))
    secretNumber = prune(mix(secretNumber, secretNumber * 2048))

    return secretNumber


def processBuyer(secretNumber):
    max = 2001
    i = 0
    previousDigit = None
    buyerSeq = {}
    lastFourChanges = []

    while i < max:
        digit = int(str(secretNumber)[-1])

        if previousDigit is None:
            change = ""
        else:
            change = digit - previousDigit

        if i > 0:
            if len(lastFourChanges) < 4:
                lastFourChanges.append(change)
            else:
                lastFourChanges.pop(0)
                lastFourChanges.append(change)

        if len(lastFourChanges) == 4:
            seq = ",".join([str(x) for x in lastFourChanges])

            if not seq in buyerSeq:
                buyerSeq[seq] = digit

            # if digit > buyerSeq[seq]:
            #     buyerSeq[seq] = digit

        i += 1
        previousDigit = digit

        newNum = getRandomNumber(secretNumber)
        secretNumber = newNum
        # print(f"{secretNumber} {digit} ({change}) {lastFourChanges}")
    return [buyerSeq, secretNumber]


firstLevel = 0
c = 0
sequences = {}

for secretNumber in seeds:
    buyerSeq, finalNumber = processBuyer(secretNumber)

    for seq in buyerSeq:
        if not seq in sequences:
            sequences[seq] = {"max": 0, "seq": []}

        sequences[seq]["seq"].append(buyerSeq[seq])
        sequences[seq]["max"] += buyerSeq[seq]

    firstLevel += finalNumber
    print(f"{c}:{secretNumber}: {finalNumber}")
    c += 1
    # print(buyerSeq)

maxBananas = 0
maxSeq = None

# order sequences seq max
sequences = {
    k: v
    for k, v in sorted(sequences.items(), key=lambda item: item[1]["max"], reverse=True)
}

output = ""

for val in sequences:
    output += f"{val}: {sequences[val]}\n"

# print output into output.txt file
with open("output.txt", "w") as file:
    file.write(output)
secondLevel = list(sequences.values())[0]

# print the first sequence in sequnces
print(f"{list(sequences.keys())[0]}: {secondLevel}")

# for seq in sequences:
#     if sequences[seq] > maxBananas:
#         maxBananas = sequences[seq]
#         maxSeq = seq
# print(f"{maxSeq}: {maxBananas}")


print(firstLevel)
# print(secondLevel)
