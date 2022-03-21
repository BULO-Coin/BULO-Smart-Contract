# Deploy

./sandbox copyTo ../approval_BULOProtection.teal 
./sandbox copyTo ../clear_BULOProtection.teal
./sandbox goal account list

./sandbox goal wallet new rugpuller
./sandbox goal account import
Your seed phrase here

Imported BCESG4ZANHXIZW7JQMMIF5UPPQJBJ7SLQC67JUSIIAPITQTKWSAGIGW7V4

./sandbox goal app create --creator BCESG4ZANHXIZW7JQMMIF5UPPQJBJ7SLQC67JUSIIAPITQTKWSAGIGW7V4 \
--approval-prog approval_BULOProtection.teal \
--clear-prog clear_BULOProtection.teal \
--global-byteslices 5 \
--global-ints 10 \
--local-byteslices 0 --local-ints 0 

Created app with app index **79494248**


# Setup

./sandbox  goal app info --app-id 79494248

Application account:   77CNP4NAQWSEGTMDGUJTD5Z3EBKNQZ2KWVWEG5UOI5QUUNIOEZQ2K6ZTMQ


./sandbox   goal clerk send -a 350000 -f BCESG4ZANHXIZW7JQMMIF5UPPQJBJ7SLQC67JUSIIAPITQTKWSAGIGW7V4 -t 77CNP4NAQWSEGTMDGUJTD5Z3EBKNQZ2KWVWEG5UOI5QUUNIOEZQ2K6ZTMQ

#View balance and info 
./sandbox   goal account balance -a 77CNP4NAQWSEGTMDGUJTD5Z3EBKNQZ2KWVWEG5UOI5QUUNIOEZQ2K6ZTMQ  
./sandbox  goal account info -a 77CNP4NAQWSEGTMDGUJTD5Z3EBKNQZ2KWVWEG5UOI5QUUNIOEZQ2K6ZTMQ

./sandbox  goal app read  --app-id 79494248 --global

#First foreign asset is BULO, second one is Buloed ASA
#First app-account is tinyman LP address, 2nd one is Rescue wallet, 3rd one if Faucet, 4th one is  Stupidity wallet
./sandbox goal app call --app-id 79494248 --app-arg "str:Setup" --foreign-asset "58716917"  --foreign-asset "79306294"  \
--app-account "OQS7CU4JB5GVHGJ4EIJUPD4L5HABZUI2OVJM6KEKCS4XPU57PPAFZ7P5IU" \
--app-account "C54GYXRIWSV7RLW6YQQQATPIN3N6LFUY26EEV7IIVBVP3E7P653PB344RI" \
--app-account "KNUUJRARQNGBBRWPCQL6JD6V5QTMLIRM2GTLTK2PQRUVWVYXUXVWOXGS4I" \
--app-account "E2RG5QDYLG3X22VWBBVWARIQT2LLHQVHTXBLAZUB62MORI5SWLRYHUY2PE" \
-f "BCESG4ZANHXIZW7JQMMIF5UPPQJBJ7SLQC67JUSIIAPITQTKWSAGIGW7V4" 



# I_Promise_I_will_not_Rugpull


#Send BULO from  address

./sandbox goal asset send -a 1000000000 --assetid 58716917 \
-f BCESG4ZANHXIZW7JQMMIF5UPPQJBJ7SLQC67JUSIIAPITQTKWSAGIGW7V4 \
-t 77CNP4NAQWSEGTMDGUJTD5Z3EBKNQZ2KWVWEG5UOI5QUUNIOEZQ2K6ZTMQ \
-o SendBULOtransaction 

#First foreign asset is BULO, second one is Buloed ASA\
#First app-account is tinyman LP address, 2nd one is Rescue wallet, 3rd one if Faucet, 4th one is  Stupidity wallet\
#First app arg is function name, 2nd is min liquidity in microalgo (coin is rugged), \
#3rd is max liquidity (coin is successful), 4th is minimum days to become successful \
#-f must be the same\

./sandbox  goal app call --app-id 79494248 --app-arg "str:I_Promise_I_will_not_Rugpull" \
--app-arg "int:10000000"  --app-arg "int:90000000" --app-arg "int:50"   \
--foreign-asset "58716917"  --foreign-asset "79306294"  \
-f "BCESG4ZANHXIZW7JQMMIF5UPPQJBJ7SLQC67JUSIIAPITQTKWSAGIGW7V4" \
--app-account "OQS7CU4JB5GVHGJ4EIJUPD4L5HABZUI2OVJM6KEKCS4XPU57PPAFZ7P5IU" \
--app-account "C54GYXRIWSV7RLW6YQQQATPIN3N6LFUY26EEV7IIVBVP3E7P653PB344RI" \
--app-account "KNUUJRARQNGBBRWPCQL6JD6V5QTMLIRM2GTLTK2PQRUVWVYXUXVWOXGS4I" \
--app-account "E2RG5QDYLG3X22VWBBVWARIQT2LLHQVHTXBLAZUB62MORI5SWLRYHUY2PE" \
-o I_Promise_I_will_not_RugpullTransaction

./sandbox copyFrom SendBULOtransaction 

./sandbox copyFrom I_Promise_I_will_not_RugpullTransaction

cat SendBULOtransaction I_Promise_I_will_not_RugpullTransaction > groupedtransaction

./sandbox copyTo groupedtransaction 


./sandbox goal clerk group -i groupedtransaction -o groupedtransaction.grouped

./sandbox goal clerk sign -i groupedtransaction.grouped -o groupedtransaction.grouped.signed

./sandbox goal clerk rawsend -f groupedtransaction.grouped.signed


./sandbox  goal app read  --app-id 79494248 --global
