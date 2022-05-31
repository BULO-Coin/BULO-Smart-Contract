
"""BULO Coin Smartcontract"""

def approval_program():

    #When we create the smart contract, we initialise the variables
    on_creation = Seq([
        App.globalPut(Bytes("BULO_lovers_count"), Int(0)),
        App.globalPut(Bytes("Buloed_ASA_Max_Supply"), Int(0)),
        App.globalPut(Bytes("BULO_ID"), Int(0)),
        App.globalPut(Bytes("Buloed_ASA_ID"), Int(0)),
        App.globalPut(Bytes("Buloed_ASA_LP_Address"), Bytes("000")),
        App.globalPut(Bytes("RescueWallet_Address"), Bytes("111")),
        App.globalPut(Bytes("AlgoFaucetWallet_Address"), Bytes("222")),
        App.globalPut(Bytes("StupidityWallet_Address"), Bytes("222")),
        App.globalPut(Bytes("Buloed_ASA_LP_lower_limit"), Int(0)),
        App.globalPut(Bytes("Buloed_ASA_LP_upper_limit"), Int(0)),
        App.globalPut(Bytes("BULO_locked_until"), Int(0)),
        App.globalPut(Bytes("Commited_BULO"), Int(0)),
        App.globalPut(Bytes("ASA_BULO_Exchange_Rate"), Int(0)),
        App.globalPut(Bytes("Setup_complete"), Int(0)),
	    Approve()
    ])

    #The first function to call, it will opt-in the assets and setup the variables.
    #Before that, the contract must be funded with at least 0.25 Algos to be able to opt-in the ASAs
    on_setup = Seq(
        If(
            App.globalGet(Bytes("Setup_complete")) == Int(0)
        ).Then(
            Seq(
                #The contract opts-in BULO by sending a 0 value transacttion to itself
                App.globalPut(Bytes("BULO_ID"), Txn.assets[0]),
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.xfer_asset: App.globalGet(Bytes("BULO_ID")),
                        TxnField.asset_amount: Int(0),
                        TxnField.asset_receiver: Global.current_application_address(),
                    }
                ),
                InnerTxnBuilder.Submit(),
                #The contract opts-in the Buloed ASA by sending a 0 value transacttion to itself
                App.globalPut(Bytes("Buloed_ASA_ID"), Txn.assets[1]),
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.xfer_asset: App.globalGet(Bytes("Buloed_ASA_ID")),
                        TxnField.asset_amount: Int(0),
                        TxnField.asset_receiver: Global.current_application_address(),
                    }
                ),
                InnerTxnBuilder.Submit(),
                #The addresses are set
                App.globalPut(Bytes("Buloed_ASA_LP_Address"), Txn.accounts[1]),
                App.globalPut(Bytes("RescueWallet_Address"), Txn.accounts[2]),
                App.globalPut(Bytes("AlgoFaucetWallet_Address"), Txn.accounts[3]),
                App.globalPut(Bytes("StupidityWallet_Address"), Txn.accounts[4]),
                #The setup is complete, we wont be able to call this function anymore
                App.globalPut(Bytes("Setup_complete"), Int(1)),
                Approve(),
            )
        ),
        Reject(),
    )

    #No opt-in
    handle_optin = Reject()

    #No Close-out
    handle_closeout = Reject()

    #No update, contract is Immutable
    handle_updateapp = Reject()

    #No delete, contract is Immutable
    handle_deleteapp = Reject()

    #This function allow to set up the no-rugpull promise, and to commit the BULO
    #Here we want to receive 2 transactions in the group:
    #- the first one is the BULO ASA transfert to be commited
    #- the second one is the call to this function
    LockUntil_computed = ScratchVar(TealType.uint64)
    send_bulo_txn = Gtxn[Txn.group_index() - Int(1)]
    I_Promise_I_will_not_Rugpull = Seq(
        #Some preliminary checks
        Assert(
                And(
                    # the actual BULO transfert is before the app call
                    send_bulo_txn.type_enum() == TxnType.AssetTransfer,
                    # The transfered asset is indeed BULO
                    send_bulo_txn.xfer_asset() == App.globalGet(Bytes("BULO_ID")),
                    # The sender of the ASA is the same than the one calling this function
                    send_bulo_txn.sender() == Txn.sender(),
                    # The receiver of the ASA is the smartcontract address
                    send_bulo_txn.asset_receiver() == Global.current_application_address(),
                )
        ),
        #Then we check that the setup function was already called, and this function was not
        #We also check that the BULO ammount transfered is at least 100000.00 BULO
        If(
            And(
                send_bulo_txn.asset_amount() >= Int(10000000),
                App.globalGet(Bytes("Setup_complete")) == Int(1)
            )
        ).Then(
            # If everithing is OK, we fund the wallets and setup the variables
            Seq(
                #We send 2% to the rescue wallet
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.xfer_asset: App.globalGet(Bytes("BULO_ID")),
                        TxnField.asset_amount: Div(Mul(send_bulo_txn.asset_amount(), Int(2)),Int(100)),
                        TxnField.asset_receiver: App.globalGet(Bytes("RescueWallet_Address")),
                    }
                ),
                InnerTxnBuilder.Submit(),
                #We send 2% to the AlgoFaucet wallet
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.xfer_asset: App.globalGet(Bytes("BULO_ID")),
                        TxnField.asset_amount: Div(Mul(send_bulo_txn.asset_amount(), Int(2)),Int(100)),
                        TxnField.asset_receiver: App.globalGet(Bytes("AlgoFaucetWallet_Address")),
                    }
                ),
                InnerTxnBuilder.Submit(),
                #We send 1% to the Stupidity wallet
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.xfer_asset: App.globalGet(Bytes("BULO_ID")),
                        TxnField.asset_amount: Div(Mul(send_bulo_txn.asset_amount(), Int(1)),Int(100)),
                        TxnField.asset_receiver: App.globalGet(Bytes("StupidityWallet_Address")),
                    }
                ),
                InnerTxnBuilder.Submit(),
                #We setup the lower limit for the liquidity, to know when the coin is rugpulled
                App.globalPut(Bytes("Buloed_ASA_LP_lower_limit"), Btoi(Txn.application_args[1])),
                #We setup the upper limit for the liquidity, to use in conjusction with the lock_until date 
                #to know if the coin is successfull in the Did_we_succeed function
                App.globalPut(Bytes("Buloed_ASA_LP_upper_limit"), Btoi(Txn.application_args[2])),
                LockUntil_computed.store(Add(Global.latest_timestamp(),Mul(Btoi(Txn.application_args[3]),Int(86400)))),
                App.globalPut(Bytes("BULO_locked_until"), LockUntil_computed.load()),
                #We store the remaining commited BULO (ammount - 5%)
                App.globalPut(Bytes("Commited_BULO"), send_bulo_txn.asset_amount() - Div(Mul(send_bulo_txn.asset_amount(), Int(5)),Int(100))),
                #The setup is complete, we wont be able to call this function anymore
                App.globalPut(Bytes("Setup_complete"), Int(2)),
                Approve(),
            )
        ),
        Reject(),
        
    )

    ##Subroutine to compute the number of BULO to send using the amount_of_shitcoins sent by the contract caller
    ##TODO: the math need to be improved
    #We will get the max supply of the Buloed ASA
    Buloed_ASA_Total = AssetParam.total(Txn.assets[1])
    @Subroutine(TealType.uint64)
    def ComputeBuloAmmount(amount_of_shitcoins: Expr):
        #Temp var to store the result
        Computed_Bulo_Ammount = ScratchVar(TealType.uint64)
        return Seq(
            # we get the max supply of the Buloed ASA
            Buloed_ASA_Total,
            # And confirm it has a value
            Assert(Buloed_ASA_Total.hasValue()),
            If(
                #We check the provided asset is indeed the Buloed ASA to avoid id getting tinymanned
                Txn.assets[1] == App.globalGet(Bytes("Buloed_ASA_ID"))
            ).Then(
                Seq(
                    #TODO: a simple cross-multiplication for now, this needs to be improved
                    Computed_Bulo_Ammount.store(Div(Mul(amount_of_shitcoins, App.globalGet(Bytes("Commited_BULO"))),Buloed_ASA_Total.value())),
                    Return(Computed_Bulo_Ammount.load()),
                )
            ),
            #Error if the assets do not match
            Err(),
        )    


    #Here we want to receive 3 transactions in the group:
    #- the first one is an algo payment to allow the contract to pay the fees to send the BULO
    #- the second is the rugpulled ASA transfert to be swapped to BULO
    #- the third one is the call to this function
    send_Algo_txn = Gtxn[Txn.group_index() - Int(2)]
    send_ASA_txn = Gtxn[Txn.group_index() - Int(1)]
    Ho_No_I_Got_Rugged = Seq([
        # First we check that everything is OK
        Assert(
                And(
                    # We check the first transaction
                    # the actual payment is before the app call
                    send_Algo_txn.type_enum() == TxnType.Payment,
                    # The sender of the payment is the same than the one calling this function
                    send_Algo_txn.sender() == Txn.sender(),
                    # The receiver of the payment is the smartcontract address
                    send_Algo_txn.receiver() == Global.current_application_address(),
                    # The ammount is 2000 microAlgos
                    send_Algo_txn.amount() == Int(2000),
                    # We check the second transcation
                    # the Rugpulled coin is sent before the app call
                    send_ASA_txn.type_enum() == TxnType.AssetTransfer,
                    # We check the asset is indeed the rugpulled coin (before being rugpulled, it was buloed)
                    send_ASA_txn.xfer_asset() == App.globalGet(Bytes("Buloed_ASA_ID")),
                    # The sender of the ASA is the same than the one calling this function
                    send_ASA_txn.sender() == Txn.sender(),
                    # The receiver of the ASA is the smartcontract address
                    send_ASA_txn.asset_receiver() == Global.current_application_address(),
                )
        ),
        #Then, we check if the ASA was rugpulled 
        If(
            #If the Balance of the LP address is lower than the limit defined when the contract was setup, the coin is rugged
            Balance(App.globalGet(Bytes("Buloed_ASA_LP_Address"))) <= App.globalGet(Bytes("Buloed_ASA_LP_lower_limit")),
        ).Then(
            Seq(
                # We sumit an inner transaction to send the BULO to the contract caller
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.xfer_asset: App.globalGet(Bytes("BULO_ID")),
                        #The ammount to send is computed in the ComputeBuloAmmount function
                        TxnField.asset_amount: ComputeBuloAmmount(send_ASA_txn.asset_amount()),
                        TxnField.asset_receiver: Txn.sender(),
                    }
                ),
                InnerTxnBuilder.Submit(),
                #We confirm that everything went well
                Approve(),
            )
        ),
        #If not, we cancel
        Reject(),
    ])

    ##Here we want to receive a single transaction in the group: the app call
    ##This function checks if the LP exeed the upper threshold and if the lockup day have passed
    ##If it's the case, it sends half of the BULO to the RescueWallet_Address, and locks itself
    ##TODO: This needs more testing
    BULO_Balance = AssetHolding.balance(Txn.sender(), Txn.assets[0])
    BULO_To_Unlock_computed = ScratchVar(TealType.uint64)
    Did_we_succeed = Seq(
        If(
            And(
                #If the Balance of the LP address is higher than the limit defined when the contract was setup, the coin is successful
                Balance(App.globalGet(Bytes("Buloed_ASA_LP_Address"))) >= App.globalGet(Bytes("Buloed_ASA_LP_upper_limit")),
                Global.latest_timestamp() > App.globalGet(Bytes("BULO_locked_until")),
                App.globalGet(Bytes("Setup_complete")) == Int(2),
            ),
        ).Then(
            Seq(
                #We compute half the BULO
                BULO_Balance,
                Assert(BULO_Balance.hasValue()),
                BULO_To_Unlock_computed.store(Div(BULO_Balance.value(),Int(2))),
                # We sumit an inner transaction to send half the BULO to the Rescue Wallet
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.xfer_asset: App.globalGet(Bytes("BULO_ID")),
                        #The ammount is half the BULO
                        TxnField.asset_amount: BULO_To_Unlock_computed.load(),
                        TxnField.asset_receiver: App.globalGet(Bytes("RescueWallet_Address")),
                    }
                ),
                InnerTxnBuilder.Submit(),
                #We prevent this function to be called again
                App.globalPut(Bytes("Setup_complete"), Int(3)),
                #We confirm that everything went well
                Approve(),
            )
        )#.Else( #For Testing only
        #    Seq(
        #        App.globalPut(Bytes("BULO_lovers_count"), Int(69)),
        #        Approve(),
        #    )
        #)
        ,
        Reject(),
    )    

    #Depending on the application args and the groyped transaction size, we will execute different parts of the code
    handle_noop = Cond(
        [And(
            Global.group_size() == Int(2),
            Txn.application_args[0] == Bytes("I_Promise_I_will_not_Rugpull"),
        ), I_Promise_I_will_not_Rugpull],
        [And(
            Global.group_size() == Int(3),
            Txn.application_args[0] == Bytes("Ho_No_I_Got_Rugged"),
        ), Ho_No_I_Got_Rugged],
        [And(
            Global.group_size() == Int(1),
            Txn.application_args[0] == Bytes("Did_we_succeed"),
        ), Did_we_succeed],
        [And(
            Global.group_size() == Int(1),
            Txn.application_args[0] == Bytes("Setup"),
        ), on_setup]
    )

    # Main entry point of the smart contract
    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        #This is where our custom functions are written
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

    # Mode.Application specifies that this is a smart contract
    return compileTeal(program, Mode.Application, version=5)
