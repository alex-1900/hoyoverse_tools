def handle_response(response):
    r"""
    同一处理接口返回对象
    :param response: requests 请求返回的对象
    """
    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()
    if data['retcode'] != 0:
        raise Exception(data)

    return data['data']
