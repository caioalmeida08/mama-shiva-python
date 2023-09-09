from fastapi import Request

async def isRequestBodyOK(request: Request) -> bool:
    print("isRequestBodyOK (isRequestBodyOK.py) - START")
    
    if (request.method == "GET" or request.method == "DELETE"):
        print("isRequestBodyOK (isRequestBodyOK.py) - OK (GET or DELETE)")
        return True
    
    try:
        body = await request.json()
        print("isRequestBodyOK (isRequestBodyOK.py) - body: " + str(body))
        return True
    except:
        print("isRequestBodyOK (isRequestBodyOK.py) - NOT OK")
        return False
    finally:
        print("isRequestBodyOK (isRequestBodyOK.py) - END")

async def isReservaRequestBodyOK(request: Request) -> bool:
    print("isReservaRequestBodyOK (isRequestBodyOK.py) - START")
    
    if (request.method == "GET" or request.method == "DELETE"):
        print("isReservaRequestBodyOK (isRequestBodyOK.py) - OK (GET or DELETE)")
        return True
    
    try:
        body = await request.json()
        print("isReservaRequestBodyOK (isRequestBodyOK.py) - body: " + str(body))
        return True
    except:
        print("isReservaRequestBodyOK (isRequestBodyOK.py) - NOT OK")
        return False
    finally:
        print("isReservaRequestBodyOK (isRequestBodyOK.py) - END")