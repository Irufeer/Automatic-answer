while(1):
    param = raw_input()
    item  = param.split('&')
    ans   = {}
    for i in item:
        key, data = i.split('=')
        ans[key] = data.replace('+', ' ').replace('%5E', '^')
    print ans

# while(1):
#     num = int(raw_input())
#     str = raw_input()
#     for i in range(10):
#         print "{'Item_%d': '%s'}" % (num+i, str[i])
