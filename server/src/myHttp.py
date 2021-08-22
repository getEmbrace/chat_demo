
def requestInfo(request):
    itemList = request.split('\r\n\r\n', 1)
    if(len(itemList) == 1):
        headers, bodys = itemList[0], ""
    else:
        headers, bodys = itemList[0], itemList[1]
    temp_list = headers.split('\r\n')
    try:
        method, urls, protocal = temp_list[0].split(' ')
    except:
        method, urls, protocal = '', '', ''
    url = urls.split('?', 1)[0]

    params = dict()
    if(len(urls.split('?', 1)) > 1):
        for item in urls.split('?')[1].split('&'):
            strlist = item.split('=', 1)
            params.update({strlist[0]: strlist[1]})

    resInfo = {
        "method": method,
        "url": url,
        "protocal": protocal,
        "field": {},
        "params": params,
        'bodys': bodys
    }
    TemDict = dict()
    for item in temp_list[1:]:
        TemDict.update({item.split(': ')[0]: item.split(': ')[1]})
    resInfo['field'] = TemDict
    return resInfo

def response(config):
    defaultConfig = {
        'protocal': 'HTTP/1.1',
        'status': 200,
        'headers': {
            'charset': 'utf-8',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Connection': 'keep-alive',
            'Content-Type':'application/json'
        },
        'body': ''
    }
    for key in config:
        value = config[key]
        if(type(value).__name__ == 'dict'):
            for key1 in value:
                defaultConfig[key][key1] = value[key1]
        else:
            defaultConfig[key] = config[key]

    data = ''
    bodyData = bytes('', 'utf-8')
    sep = '\r\n'
    for key in defaultConfig:
        value = defaultConfig[key]
        if(type(value).__name__ == 'dict'):
            for key1 in value:
                data = data + key1 + ':' + value[key1] + sep
        else:
            if(key == 'body' and type(value).__name__ == 'str'):
                data = data + sep + str(value)
            elif(key == 'body' and type(value).__name__ == 'bytes'):
                bodyData = value
                data = data + sep
            else:
                data = data + str(value) + sep

    data = data.replace('\r\n', ' ', 1)

    return bytes(data, 'utf-8') + bodyData

def request_form(request_b):
    header = request_b.split(b'\r\n\r\n', 1)
    if(len(header) == 1):
        headers, bodys = header[0], b""
    else:
        headers, bodys = header[0], header[1]
    header_list = headers.split(b'\r\n')
    try:
        method, urls, protocal = header_list[0].split(b' ')
    except:
        method, urls, protocal = b'', b'', b''
    url = urls.split(b'?', 1)[0] 
       
    params = dict()
    if(len(urls.split(b'?', 1)) > 1):
        for item in urls.split(b'?')[1].split(b'&'):
            strlist = item.split(b'=', 1)
            params.update({str(strlist[0], encoding='utf-8'): str(strlist[1], encoding='utf-8')})
    
    resInfo = {
        "method": str(method, encoding='utf-8'),
        "url": str(url, encoding='utf-8'),
        "protocal": str(protocal, encoding='utf-8'),
        "field": {},
        "params": params,
        'body': {}
    } 
    
    TemDict = dict()
    for item in header_list[1:]:
        name = str(item.split(b': ')[0], encoding='utf-8')
        value = str(item.split(b': ')[1], encoding='utf-8')
        TemDict.update({name: value})
    resInfo['field'] = TemDict

    boundary = TemDict.get('Content-Type').split('=')[1]
    formdata_list = bodys.split(bytes(boundary, encoding='utf-8'))
    
    bodyDict = dict()
    for item in formdata_list:
        if(item == b'--' or item == b'--\r\n'):
            continue  
        filesDict = {}
        header = item.split(b'\r\n\r\n', 1)[0]
        body = item.split(b'\r\n\r\n', 1)[1]
        fs = header.split(b'\r\n')
        for i in fs:
            if(i != b''):
                files = i.split(b'; ')
                for a in files:
                    if(len(a.split(b': ')) > 1):
                        filesDict.update({a.split(b': ')[0]: a.split(b': ')[1]})  
                    elif(len(a.split(b'=')) > 1):
                        filesDict.update({a.split(b'=')[0]: a.split(b'=')[1]})  
        name = str(filesDict.get(b'name'), encoding='utf-8')
        value = body.rsplit(b'\r\n', 1)[0]
        bodyDict.update({name: value})
    resInfo['body'] = bodyDict
    
    return resInfo
    