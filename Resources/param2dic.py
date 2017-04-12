while(1):
    param = raw_input()
    item  = param.split('&')
    ans   = {}
    for i in item:
        key, data = i.split('=')
        ans[key] = data.replace('+', ' ')
    print ans


