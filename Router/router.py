from pyteal import *

# Creating a Router (Router smart contracts are ABI compliant)
router = Router(
    "my-first-router",
    # Defining what happens on, oncomplete application calls
    BareCallActions(
        # create_.only method Only triggered for create app txn
        no_op = OnCompleteAction.create_only(Approve()),

        # .call_only method triggered for non-create app calls
        opt_in = OnCompleteAction.call_only(Approve()),

        # .always method triggered for both create and non-create app calls 
        close_out = OnCompleteAction.always(Approve()), # Usually call_only, pupose of tutorial using .always
        
        # .never method Always used to reject txn, not updatable or deletable
        update_application = OnCompleteAction.never(),
        delete_application = OnCompleteAction.never(),
    ),
    # Defining what happens for clear state
    clear_state = Approve(),
)

# Registering hello method to router
@router.method
# Get user String input and output the users input
def hello(name: abi.String, *, output: abi.String):
    return output.set(Concat(Bytes("Hello "), name.get()))

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