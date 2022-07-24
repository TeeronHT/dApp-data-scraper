import requests
import json

def main():
	dAppList = listOfDApps()
	#print(dAppList)
	contractData(dAppList)

# Grab data from dApp ranking page 
def listOfDApps():

	# Grab data from dApp ranking page
	dAppList = []
 
	for page in range(1, 61):
		if page == 1:
			url = 'https://www.stateofthedapps.com/rankings/platform/ethereum'
		else:
			url = 'https://www.stateofthedapps.com/rankings/platform/ethereum?page=' + str(page)


		page = requests.get(url)
		with open('file.txt', 'w') as file:
			file.write(page.text)

		with open('file.txt') as file:
		    htmlDoc = list(file)

		for item in htmlDoc:
			if 'href="/dapps/' in item:
				parsed = item.split()
				for brokenDown in parsed:
					if 'href="/dapps/' in brokenDown:
						if 'submit/new' not in brokenDown and brokenDown not in dAppList:
							end = brokenDown.index('\"', 13)
							dApp = brokenDown[13:end]
							if portalDApps is True:
								dAppList.append(dApp)

	dAppList = list(set(dAppList))
	return dAppList


# Iterate through names and modify urls to find specific dApp pages
# Create a JSON file to store partitioned data 
# (List comprised of dictionaries which contain dApp name, contract, category, description, and icon)
def contractData(dAppList):

	contractList = []
	for dApp in dAppList:
		dAppUrl = 'https://www.stateofthedapps.com/dapps/' + dApp

		page = requests.get(dAppUrl)
		with open('data/' + dApp + '.txt', 'w') as file:
			file.write(page.text)

		with open('data/' + dApp + '.txt') as file:
			htmlDoc = list(file)

		data = []
		dAppData = {}
		for item in htmlDoc:
			if '<title data-n-head=\"true\">' in item:
				titleDesc = item[item.index('true') + 6 :item.index('</title>')]
				title = titleDesc[:titleDesc.index(' — ')]
				description = titleDesc[titleDesc.index(' —') + 3:]
				dAppData["dApp"] = title
				dAppData["description"] = description

			if 'class=\"category-link' in item:
				parsed = item.split()
				for brokenDown in parsed:
					if 'class=\"category-link' == brokenDown:
						category = parsed[parsed.index('class=\"category-link') + 2]
						partial = category[16:]
						end = partial.index('</a>')
						clean = partial[:end]
						dAppData["category"] = clean

			# Can import a CSV with all our networks on it
			if 'contractsKovan:[]' in item:
				kovan = item[item.index('contractsKovan') + 16:]
				kovanContracts = kovan[:kovan.index(']')]			
				kovanContracts = kovanContracts.split('\",\"')
				# print(kovanContracts)
				dAppData['KovanContracts'] = kovanContracts

				ETH = item[item.index('contractsMainnet') + 19:]
				ETHContracts = ETH[:ETH.index(']')]	
				ETHContracts = ETHContracts.split('\",\"')
				# print(ETHContracts)
				dAppData['EthereumMainnetContracts'] = ETHContracts

				rinkeby = item[item.index('contractsRinkeby') + 18:]
				rinkebyContracts = rinkeby[:rinkeby.index(']')]
				rinkebyContracts = rinkebyContracts.split('\",\"')			
				# print(rinkebyContracts)
				dAppData['RinkebyContracts'] = rinkebyContracts

		# contractsRopsten:[],contractsGoerli:[],contractsPoaMainnet:[],contractsGoChainMainnet:[],contractsXDaiMainnet:[],contractsEosMainnet:[],contractsSteemMainnet:[],contractsHiveMainnet:[],contractsLoomPlasmaChain:[],contractsLoomDAppChain:[],contractsKlaytnMainnet:[],contractsNeoMainnet:[],contractsObyteMainnet:[],contractsOstMainnet:[],contractsTronMainnet:[],contractsIconMainnet:[],contractsNearMainnet:[],contractsBscMainnet:[],contractsMoonriverMainnet:[],contractsMeterMainnet:[]


		# Data for the dApps themselves, not per contract
		data.append(dAppData)

		for key, value in data[0].items():
			if key == 'dApp':
				dAppName = value
			if key in ['KovanContracts','EthereumMainnetContracts','RinkebyContracts']:
				for contract in list(value):
					if len(contract) > 3:
						if '\"' in contract:
							contract = contract.replace('\"', "")		
						contractData = {}
						contractData['contractAddress'] = contract
						contractData['dAppName'] = dAppName
						contractData['networkName'] = key[:key.index('Contract')]

						if portalDApps(contractData) == True:
							contractList.append(contractData)

	with open('Data.json', 'w') as outfile:
		json.dump(contractList, outfile)


def portalDApps(dApp):

	portalDApps = ['Opensea', 'Opensea TestNet', 'Rarible', 'Rarible Rinkeby', 'Aave', 'Aave V3', 'Aave V2', 'Aave V1', 
				   'Decentraland', 'Uniswap V1', 'Uniswap V2', 'Uniswap V3', 'Uniswap', 'Compound', 'Sushi Swap', 'Known Origin', 
				   'Lido', 'Superrare', 'CryptoVoxel', 'Gem', 'Bored Ape Yacht Club', 'Cryptopunk', 'Foundation', 'Zora', 
				   'Sorare', 'Curv', 'CowSwap', 'ShibaSwap', 'InstadApp', 'DODO', 'Convex Finance', 'Liquity', 'Ribbon', 'Rabbithole', 
				   'Layer3', 'Otherside', 'Hyy.pe', 'Sandbox', 'ENS', 'Zapper', 'DeBank', 'APY Vision', 'Rarity Tools']

	if dApp in portalDApps:
		return True
	else:
		return False


# Function to verify is a contract is valid
def isValid(contractData):

	contractURL = 'https://etherscan.io/address/' + contractData['contractAddress']

	page = requests.get(contractURL)
	print(page.text)
	if contractData['dAppName'] in page.text:
		return True
	else:
		return False


if __name__ == '__main__':
	main()
