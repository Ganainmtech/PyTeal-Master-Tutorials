from pyteal import *

router = Router(
    "Atomic Transfer Example",
    BareCallActions(
        # Defining what happens during creation
        no_op = OnCompleteAction.create_only(Approve()),
    ),
)

# Using transaction types to access the txns in the atomic group 
@router.method
# Takes in two payment txn type args #--> order of args matter
def abi_multiple_pay(a:abi.PaymentTransaction, b:abi.PaymentTransaction):
    return Seq(
        # Asserting the receiver of each payment is the current app address
        Assert(a.get().receiver() == Global.current_application_address()),
        Assert(b.get().receiver() == Global.current_application_address()),
        # Asserting the amount of payment A is 1 algo
        Assert(a.get().amount() == Int(1000000)),
        # Asserting the amount of payment B is 2 algo
        Assert(b.get().amount() == Int(2000000)),
        Approve()
    )

# Using gtxn object to index into the txn in the atomic group 
@router.method
def multiple_pay(a:abi.PaymentTransaction, b:abi.PaymentTransaction):
    return Seq(
        # Indexing into the payments in the atomic group
        Assert(Gtxn[0].receiver() == Global.current_application_address()),
        Assert(Gtxn[1].receiver() == Global.current_application_address()),
        Assert(Gtxn[0].amount() == Int(1000000)),
        Assert(Gtxn[1].amount() == Int(2000000)),
        Approve()
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