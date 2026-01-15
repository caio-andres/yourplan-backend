def response_format(code: int, data: list):
    return {"status": code, "body": {"data": data}}
