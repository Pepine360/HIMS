from tester import Test

payloadPost = {"barcode" : "123456", "amount" : 5}

test1 = Test.testPost(payloadPost)

if test1:
    if test1["data"] == payloadPost:
        print("POST SUCCEEDED \n")
    else:
        print("POST FAILED\n")

