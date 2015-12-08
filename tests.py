import os, pickle, math

if os.path.exists("data.txt"):
    file = open("data.txt", mode="rb")
    blockData = pickle.load(file)
    file.close()

def cdf(bin, time):
    if bin == 0:
        return 0
    if bin > 20:
        return 1
    return 1-math.exp(-bin * 100 / time)

intervalData = {}
arrivalTimes = []
start = 383001
end = 384000
numBlocks = end-start+1
time = 0
binWidth = 100
errors = 0
for i in range(start,end):
    arrivalTime = (blockData[i]['received_time'] - blockData[i-1]['received_time']).seconds
    if arrivalTime < 7200:
        time += arrivalTime


        if arrivalTime > 10:
            arrivalTime -= 10
        arrivalTimes.append(arrivalTime)
        bin = int(arrivalTime / binWidth)
        if(bin > 20):
            bin = 20
        if bin in intervalData:
            intervalData[bin][1] += 1
        else:
            intervalData[bin] = [0,1]
    else:
        errors += 1
#average time observed
time /= numBlocks
numBlocks -= errors
for bin in intervalData:
    data = intervalData[bin]
    expected = (cdf(bin+1, time-10) - cdf(bin, time-10)) * numBlocks
    intervalData[bin][0] = expected




print("average time between arrivals " + str(time) + ' seconds')

observed = []
expected = []

chi2 = 0
for item in intervalData:
    data = intervalData[item]
    observed.append(data[1])
    expected.append(data[0])
    chi2 += math.pow(data[1]-data[0],2) / data[0]

print('chi2 = ' + str(chi2) + ' df = 20')
for num in expected:
    print(num)
for num in observed:
    print(num)

# n = 381000-380000
# binWidth = time * ((12/n)**(1/3))
#
# binWidth /= 10
# diff = math.ceil(binWidth) - binWidth
# if diff > 0.5:
#     binWidth = int(binWidth)
# elif diff <= 0.5:
#     binWidth = math.ceil(binWidth)
#
# binWidth *= 10
#
# print(binWidth)

