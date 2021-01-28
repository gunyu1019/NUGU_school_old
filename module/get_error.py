from sanic import response

forbidden = response.json({"ERROR": "접근권한이 없습니다."}, 403)

def get_error(msg, version):
    return {
        "version": version,
        "resultCode": msg
    }
