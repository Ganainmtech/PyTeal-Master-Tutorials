from pyteal import *

router = Router(
    "pyteal-expression-example",
    BareCallActions(
        # Other Bare Call Actions are set to default never
        no_op = OnCompleteAction.create_only(Approve())
    )
)

@router.method
def create_count():
    # Use of PyTeal expressions, Python Native will not work
    return Seq(
        App.globalPut(Bytes("Count"), Int(1)),
        Approve()
    )

if __name__ == "__main__":

    try:
        approval, clear, contract = router.compile_program(version=6)
        print("App is successfully compiled!\nShout out to the #algofam :)")
    except AttributeError as e:
        print(e)
