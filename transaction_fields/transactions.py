from pyteal import *

"""
Simple RSVP App
Methods:
- pay: check if the account opted in, paid 1 ALGO, and create local states
- check_paid: check if the account has paid
"""

router = Router(
    "Simple RSVP App",
    BareCallActions(
        no_op = OnCompleteAction.create_only(Approve()),
        opt_in = OnCompleteAction.call_only(Approve()),
        close_out = OnCompleteAction.always(Approve()),
    ),
    clear_state = Approve(),
 )

@router.method
def pay(pay: abi.PaymentTransaction):
    return Seq(
        # Checking if account is opted in
        Assert(App.optedIn(Txn.sender(), Global.current_application_id())),
        # Checking if payment txn has sent 1 algo
        Assert(pay.get().amount() == Int(1000000)),
        # Getting the receiver and checking if its current app address
        Assert(pay.get().receiver() == Global.current_application_address()),
        # Creating local state
        App.localPut(Txn.sender(), Bytes("paid"), Bytes("True")),
        Approve()
    ) 

@router.method
def check_paid(*, output: abi.String):
    # Reading the local state of the sender of txn
    paid_state = App.localGet(Txn.sender(), Bytes("paid"))
    return Seq(
        # If its true out put the paid state
        Assert(paid_state == Bytes("True")),
        output.set(paid_state)
    )

if __name__ == "__main__":
    import os
    import json

    path = os.path.dirname(os.path.abspath(__file__))
    approval, clear, contract = router.compile_program(version=8)

    # Dump out the contract as json that can be read in by any of the SDKs
    with open(os.path.join(path, "artifacts/contract.json"), "w") as f:
        f.write(json.dumps(contract.dictify(), indent=2))

    # Write out the approval and clear programs
    with open(os.path.join(path, "artifacts/approval.teal"), "w") as f:
        f.write(approval)

    with open(os.path.join(path, "artifacts/clear.teal"), "w") as f:
        f.write(clear)