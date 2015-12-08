import blockcypher, requests, pickle, os

#can be used to get data on old blocks

def address_display(adr):
    try:
        r = requests.get('https://www.walletexplorer.com/api/1/address-lookup?address='
		         + adr + '&caller=virginia.edu').json()
        return adr + " (" + r['label'] + ")"
    except:
        return adr


def satoshi_to_BTC(sval):
    return sval / 100000000

api_key= "a5eff945993d52cf8fce0cb1a7eda4a7"

if os.path.exists("data.txt"):
    file = open("data.txt", mode="rb")
    blockData = pickle.load(file)
    file.close()
else:
    blockData = {}

#range of blocks to download
for i in range(375000, 380000):

    block = blockcypher.get_block_overview(i, api_key=api_key)
    blockData[i] = block
    if i % 1000 == 0:
        print('1000 done')



file = open("data.txt", mode = "wb")
pickle.dump(blockData,file)
file.close()

