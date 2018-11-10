from flask import jsonify

class HttpCode():
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500


def restful_res(code,message,data):
    return jsonify(
        {
            'code':code,
            'message':message,
            'data':data
        }
    )


def success(message="",data=None):
    return restful_res(code=HttpCode.ok,message=message,data=data)

def unauth(message=""):
    return restful_res(code=HttpCode.unautherror,message=message,data=None)

def param_error(message=""):
    return restful_res(code=HttpCode.paramserror,message=message,data=None)

def server_error(message=""):
    return restful_res(code=HttpCode.servererror,message=message or 'server internal error',data=None)
