import threading
import argparse
import urllib
import httpx
import re
# 发包函数
def sendHTTP(ipaddress,port):
    href = f"http://{ipaddress}:{port}"
    htmlText = httpx.get(href).text
    pattern = 'href="(.*\.\w*)"'
    sourceNames = re.findall(pattern,htmlText)[2:]
    return sourceNames

# 获取资源
def getSource(ipaddress,port,sourceName):
    href = f"http://{ipaddress}:{port}/{sourceName}"
    source = httpx.get(href).content
    with open(f"{urllib.parse.unquote(sourceName)}","wb") as fp:
        fp.write(source)

# 存活判断
def judgment_Survival(ipaddress,port):
    href = f"http://{ipaddress}:{port}"
    try:
        status_code = httpx.head(href).status_code
        if status_code != 200:
            print("抱歉，您输入的IP或Port有错")
            return 0
    except:
        print("您网络是否存在问题?")
    return 1

def getLogo():
    logo = """              welcome this tools
                　☆  *　.  　☆
            　　. ∧＿∧　∩　* ☆
            *  ☆ ( ・∀・)/ .
            　.  ⊂　　 ノ* ☆
            ☆ * (つ ノ  .☆
            　　 (ノ
    """
    print(logo)
    return -1

def getParserArgs():
    parser = argparse.ArgumentParser(description="欢迎来到HFS资源一建爬取工具")
    parser.add_argument("-a",help="指定需要探测的网站IPAddress，形如192.168.226.240",required=True)
    parser.add_argument("-p",help="指定爬取网站的端口，默认为80",default="80",type=int)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    getLogo()
    args = getParserArgs()
    ipaddress = args.a
    port = args.p
    status = judgment_Survival(ipaddress,port)
    if status:
        sourceNames = sendHTTP(ipaddress,port)
        for sourceName in sourceNames:
            t = threading.Thread(getSource(ipaddress,port,sourceName))
            t.start()
    exit()
