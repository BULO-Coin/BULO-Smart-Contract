
# The BULO Protection Smartcontract

This is the first version of the BULO Protection Smart Contract.

It's currently deployed on testnet for "Super Shit COin" ASA ID  is **79306294**.

Testnet BULO ASA ID is: **58716917**

# Using testnet and goal cli

## Using testnet

You can refer to this documentation to use MyAlgoWallet and Tinyman on testnet: <https://docs.tinyman.org/tinyman-testnet/>

For Pera wallet, it's here: <https://support.perawallet.app/en/article/connecting-to-testnet-developer-mode-1q638cf/>

**I advise you create a ew address especially for testnet**

* Testnet BULO ASA ID is: **58716917**
* Testnet "Super Shit COin" ASA ID  is **79306294**
* Testnet "BULO Protection" smartcontract ID for "Super Shit COin" is: **79494248**
* Testnet "Super Shit COin" LP Address is: **OQS7CU4JB5GVHGJ4EIJUPD4L5HABZUI2OVJM6KEKCS4XPU57PPAFZ7P5IU**
* Testnet Rescue Wallet is: **C54GYXRIWSV7RLW6YQQQATPIN3N6LFUY26EEV7IIVBVP3E7P653PB344RI**
* Testnet fake Algofaucet address is: **KNUUJRARQNGBBRWPCQL6JD6V5QTMLIRM2GTLTK2PQRUVWVYXUXVWOXGS4I**
* Testnet stupidity wallet is: **E2RG5QDYLG3X22VWBBVWARIQT2LLHQVHTXBLAZUB62MORI5SWLRYHUY2PE**
* The rugpull threshold is **10 algos**
* The success threhold is **90 algos and 10 days**

You can verify this info here: <https://testnet.algoexplorer.io/application/79494248>

## Using the goal cli

### Installing the sandbox tool on debian

The easiest way to setup a testnet node is to use the "sandbox" tool from Algorand.

It's a set of scripts that start a node docker container. It's really easy to use on Debian 11.
Here are the commands to set it up and running on Debian 11. If you want to run it on another OS, please take a look at the official documentation <https://github.com/algorand/sandbox#algorand-sandbox>

If you don't want to use docker, you can also install a real node using this documentation <https://developer.algorand.org/docs/run-a-node/setup/install/> 

**If you use a real node, just remove *./sandbox* before the goal commands**

We first update the machine and install the prerequisties

`apt update && apt upgrade && apt install ca-certificates curl gnupg lsb-release git python3`

We clone the sandbox's git repository

`git clone https://github.com/algorand/sandbox.git`

We get docker's GPG key

`curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`

We add the docker repository

`echo   "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`

We install docker and docker-compose

`apt update && apt install docker-ce docker-ce-cli containerd.io docker-compose`

We start the container on testnet

`cd sandbox && ./sandbox up testnet -v`

### Calling the smartcontract

The smartcontract is already deployed for "Super Shit COin" ASA 79306294. If you want to learn how to deploy, check "deploy_transactions.md"

**If you use a real node, just remove *./sandbox* before the goal commands**

We want to call the Ho_No_I_Got_Rugged function.

To make get you BULO back, there are several conditions:

 You must send a grouped transaction with 3 transactions:

* The first transation needs to be an algo transaction to pay for the trasaction fees (2000 microalgos = 0.002 algos)
* The second one needs to be a transfert of the rugpulled ASA you want to swap to BULO
* The third one needs to be a call to the Ho_No_I_Got_Rugged function of the smart contract.
* The three transactions must be signed by the same wallet

And the ASA must have been rugpulled (the following condition must be true):

* **The balance of Buloed_ASA_LP_Address must be lower than the Buloed_ASA_LP_lower_limit**
* You can check the value of these variables using algoexplorer: <https://testnet.algoexplorer.io/application/79494248> , in the Application Global State part. Buloed_ASA_LP_lower_limit is in microalgos, you must divide it by 1 000 000 to get the number of Algos. You can simply click the Buloed_ASA_LP_Address to look it up in algoexplorer and check its Algo balance. If you want to take a look a the variables directly from the sandbox: `./sandbox  goal app read --app-id 79494248 --global`


**Import your testnet wallet**

`./sandbox goal account import`
*your seed phrase here*

*Mine is EAQ54SF43KCF7WG6CD3TN3CCQMWPBG55GSJOAKXPFBSPCHA5HI5VKGYBZQ*

**Use this (or algoexplorer) to get the wallet address of the smartcontract**

`./sandbox  goal app info --app-id 79494248`

*It's 7FLPNTSK6L7ADUGYAZCONW3KPWBA7XSEYFCLQF3P5P5XHGQ3GX3BZ6WBO4 for Super Shit COin*


**Send 0.002 Algo to the smartcontract's wallet from your wallet** The tranction will be savec to a file to be grouped later

`./sandbox   goal clerk send -a 2000 \
-f EAQ54SF43KCF7WG6CD3TN3CCQMWPBG55GSJOAKXPFBSPCHA5HI5VKGYBZQ \
-t 7FLPNTSK6L7ADUGYAZCONW3KPWBA7XSEYFCLQF3P5P5XHGQ3GX3BZ6WBO4 \
-o SendALGOtransaction`

**Send SHIT from same address** Here I send 10 000 000 microSHIT. As SHIT has 2 decimals, it's 100 000 SHIT. The tranction will be savec to a file to be grouped later

`./sandbox goal asset send -a 10000000 --assetid 79306294 \
-f EAQ54SF43KCF7WG6CD3TN3CCQMWPBG55GSJOAKXPFBSPCHA5HI5VKGYBZQ \
-t 7FLPNTSK6L7ADUGYAZCONW3KPWBA7XSEYFCLQF3P5P5XHGQ3GX3BZ6WBO4 \
-o SendRUGPULLtransaction`

**Call the Ho_No_I_Got_Rugged function** The tranction will be savec to a file to be grouped later

* First foreign asset is BULO, second one is Buloed ASA
* First app-account is tinyman LP address

`./sandbox  goal app call --app-id 79494248 --app-arg "str:Ho_No_I_Got_Rugged" \
--foreign-asset "58716917"  --foreign-asset "79306294"  \
-f "EAQ54SF43KCF7WG6CD3TN3CCQMWPBG55GSJOAKXPFBSPCHA5HI5VKGYBZQ" \
--app-account "OQS7CU4JB5GVHGJ4EIJUPD4L5HABZUI2OVJM6KEKCS4XPU57PPAFZ7P5IU" \
-o Ho_No_I_Got_RuggedTransaction`

**Copy the three files from the sandbox to your computer**

`./sandbox copyFrom SendALGOtransaction`

`./sandbox copyFrom SendRUGPULLtransaction`

`./sandbox copyFrom Ho_No_I_Got_RuggedTransaction`

**Concatenate them**

`cat SendALGOtransaction SendRUGPULLtransaction  Ho_No_I_Got_RuggedTransaction > groupedtransaction`

**And send the result back to the sandbox**

`./sandbox copyTo groupedtransaction`


**Finaly, group them**

`./sandbox goal clerk group -i groupedtransaction -o groupedtransaction.grouped`

**sign the group**

`./sandbox goal clerk sign -i groupedtransaction.grouped -o groupedtransaction.grouped.signed`

**And send it**

`./sandbox goal clerk rawsend -f groupedtransaction.grouped.signed`

If the conditions are met, you'll receive you're BULO as an inner transaction. Inner transactions are a new feature of TEAL 5, and some wallets don't display them or don't notify them. Howevern, the balance is updated. However, you can see them on the application call transaction in Algoexplorer. For example, here is the app call when I set up the contract for "Super SHit COin": <https://testnet.algoexplorer.io/tx/KZOMXPCDM7NUCYHOSAO7PR2CU7XLD6V4HXMJPHGQCLZ6ZVG7HO7A>

You can see in the "Inner Transactions" part the transactions to the Rescue, Drop, and Stupidity wallet.  
