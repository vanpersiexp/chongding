#冲顶大会
def websocket_message(flow):
    try:
        data=flow.messages[-1].content.decode('utf-8')
        with open('/tmp/raw_data.txt','a') as f:
            f.write(data+'\n')
    except Exception:
        pass

#百万赢家
def response(flow):
    try:
        data=flow.response.content.decode('utf-8')
        print(data)
        with open('/tmp/raw_data.txt','a') as f:
            f.write(data+'\n')
    except Exception:
        pass