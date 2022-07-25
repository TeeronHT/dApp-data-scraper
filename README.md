# dAppDataScraper

Grabs list of dApps and their contract addresses from State of the dApps website.
Current pull will give you a json file containing a list of dictionaries.
Data is not complete, yet it gives a good base. 

Finds Ethereum mainnet, Rinkeby, Kovan, Goerli, and Ropsten contracts per dApp

## To Run:
```
git clone https://github.com/TeeronHT/dAppDataScraper.git
cd dAppDataScraper && python3 webScraper.py
```


To see the output, use:

```
open Data.json
```

If you are trying to display the data in retool, open the "Data Reading Test" app and drop Data.json in the file dropper. 
Then, click "Populate Table". The Contracts table in "Dapp & Contract Manager" should be filled out.
If you have changed the data and would like to reload, click "Load Data to Other App" and "Populate Table" once more.

If you would like to find the contracts for all of the dApps listed in State of the DApps, change the main method to:
```
def main():
  dAppList = listOfDApps()
  contractData(dAppList)
```

