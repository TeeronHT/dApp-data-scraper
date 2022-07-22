import requests
import json

def main():

#def 
	# Grab data from dApp ranking page 
	url = 'https://www.stateofthedapps.com/rankings/platform/ethereum'

	page = requests.get(url)
	with open('file.txt', 'w') as file:
		file.write(page.text)

	with open('file.txt') as file:
	    htmlDoc = list(file)

	dAppList = []
	for item in htmlDoc:
		if 'href="/dapps/' in item:
			parsed = item.split()
			for brokenDown in parsed:
				if 'href="/dapps/' in brokenDown:
					if 'submit/new' not in brokenDown and brokenDown not in dAppList:
						end = brokenDown.index('\"', 13)
						dAppList.append(brokenDown[13:end])

	dAppList = list(set(dAppList))

	# Iterate through names and modify urls to find specific dApp pages
	# Create a JSON file to store partitioned data 
	# (List comprised of dictionaries which contain dApp name, contract, category, description, and icon)

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
				ETHContracts = ETH[:ETH.index('\"]')]	
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

						#if isValid(contractData) == True:
						contractList.append(contractData)

	with open('Data.json', 'w') as outfile:
		json.dump(contractList, outfile)

# Function to verify is a contract is valid
def isValid(contractData):
	contractURL = 'https://etherscan.io/address/' + contractData['Contract Address']

	page = requests.get(contractURL)
	with open('validation/' + contractData['Contract Address'] + '.txt', 'w') as file:
		file.write(page.text)

	print(page.text)

	with open('validation/' + contractData['Contract Address'] + '.txt') as file:
		if contractData['dApp'] in file:
			return True
		else:
			return False

if __name__ == '__main__':
	main()
