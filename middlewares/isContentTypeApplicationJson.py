from fastapi import Request

def isContentTypeApplicationJson(request: Request) -> bool:
    print("isContentTypeApplicationJson (isContentTypeApplicationJson.py) - START")
    
    if (request.method == "GET"):
        print("isContentTypeApplicationJson (isContentTypeApplicationJson.py) - OK (GET)")
        return True

    content_type = request.headers.get("Content-Type")
    print("isContentTypeApplicationJson (isContentTypeApplicationJson.py) - content_type: " + str(content_type))
    
    if (content_type == "application/json"):
        print("isContentTypeApplicationJson (isContentTypeApplicationJson.py) - OK")
        return True
        
    print("isContentTypeApplicationJson (isContentTypeApplicationJson.py) - NOT OK")
    return False