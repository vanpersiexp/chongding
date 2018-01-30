import argparse
import re
import sys
import threading
import signal
import json
try:
    import tailer
    import requests
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import pyfiglet
except Exception:
    print("请先阅读帮助文档README.md")
    print("试试：pip3 install -r related.txt")

parser=argparse.ArgumentParser(description="冲顶大会/百万赢家/头脑王者/UC疯狂夺金:抓包获取题目并搜索答案。")
parser.add_argument("-b","--brand",dest='brand',help="选择APP，1：冲顶大会；2：百万赢家；3：头脑王者；4：UC疯狂夺金",choices=[1,2,3,4],type=int)
args=parser.parse_args()

CHROME = webdriver.Chrome()

def handlesignal(signum,frame):
    print('\033[93m'+"\n程序已停止")
    CHROME.close()
    sys.exit(0)
signal.signal(signal.SIGINT,handlesignal)

class GetAnswer(object):
    def __init__(self,brand,raw_data):
        self.brand=brand
        self.raw_data=raw_data
    def clean_cddh(self):
        try:
            self.question = self.raw_data.split(':')[2].split(',')[0].replace('"', '').replace('?', '').replace('？', '').split('.')[
                -1].strip()
            options_raw_list = self.raw_data.split(':')[5].split(',')
            self.option_list = []
            for i in range(3):
                tmp = options_raw_list[i].replace('"', '').replace(']', '').replace('[', '').replace('\\', '')
                self.option_list.append(tmp)
        except Exception as e:
            print("发生错误了：", e)
    def clean_bwyj(self):
        try:
            self.question = self.raw_data['data']['msg']['answer']['doing']['doing']['title'].replace('？','').replace('“','').replace('”','').strip()
            self.question=self.question.replace('以下','')
            options_a = self.raw_data['data']['msg']['answer']['doing']['doing']['answer']['A']['value']
            options_b = self.raw_data['data']['msg']['answer']['doing']['doing']['answer']['B']['value']
            self.option_list = [options_a, options_b]
            #百万赢家非正常选择题，有时只有两个选项
            try:
                options_c = self.raw_data['data']['msg']['answer']['doing']['doing']['answer']['C']['value']
                self.option_list.append(options_c)
            except Exception:
                pass
        except Exception:
            pass
    def clean_tnwz(self):
        try:
            self.question=self.raw_data['data']['quiz'].replace('？','').replace('“','').replace('”','').strip()
            self.question=self.question.replace('以下','')
            self.option_list=self.raw_data['data']['options']
        except Exception:
            pass
    def clean_fkdj(self):
        try:
            self.question=self.raw_data['data']['args'][0]['body']['qc'].replace('？','').replace('“','').replace('”','').strip()
            self.ac=self.raw_data['data']['args'][0]['body']['as']
            self.option_list=[]
            for i in self.ac:
                tmp=i['ac'].strip()
                self.option_list.append(tmp)
        except Exception:
            pass
    def getAnswer_chrome(self):
        global CHROME
        url_base = 'https://www.baidu.com/s?wd='
        # url_base='https://www.sogou.com/web?query='
        url = url_base + self.question
        CHROME.get(url)
    def getAnswer_index_count(self,question,option_list):
        url_base = 'http://www.baidu.com/s'
        result_dict = {}
        try:
            for option in option_list:
                r = requests.get(url_base, params={'wd': question})
                result = r.text.count(option)
                #print('\033[95m'+"首页数量统计结果：",option, ":", result)
                result_dict[result] = option
            if '不' in question:
                print('\033[91m' + "根据首页统计，答案可能是：", result_dict[min(result_dict)])
            else:
                print('\033[91m' + "根据首页统计，答案可能是：", result_dict[max(result_dict)])
            print('-'*20)
        except Exception as e:
            print("发生错误了：", e)
    def getAnswer_all_count(self,question,option_list):
        url_base = 'http://www.baidu.com/s'
        result_dict = {}
        try:
            for option in option_list:
                query = question + '+' + option
                r = requests.get(url_base, params={'wd': query})
                soup = BeautifulSoup(r.text, 'lxml')
                result = soup.find('div', {'class': 'nums'}).getText()
                result = result.replace(',', '')
                result = int(re.findall('\d+', result)[0])
                #print('\033[95m'+"全部数量统计结果：",option, ':', result)
                result_dict[result] = option
            if '不' in question:
                print('\033[91m' + "根据全部统计，答案可能是：", result_dict[min(result_dict)])
            else:
                print('\033[91m' + "根据全部统计，答案可能是：", result_dict[max(result_dict)])
            print('-'*20)
        except Exception as e:
            print("发生错误了：", e)
    def run(self):
        try:
            if self.brand == 1:
                self.clean_cddh()
            elif self.brand == 2:
                self.clean_bwyj()
            elif self.brand ==3:
                self.clean_tnwz()
            elif self.brand == 4:
                self.clean_fkdj()
            print('\033[92m' + "题目：", self.question)
            print('\033[93m' + "选项：", self.option_list)
            print('\033[95m')
            t1 = threading.Thread(target=self.getAnswer_chrome)
            t2 = threading.Thread(target=self.getAnswer_index_count, args=(self.question, self.option_list))
            t3 = threading.Thread(target=self.getAnswer_all_count, args=(self.question, self.option_list))
            t_list = [t1, t2, t3]
            for t in t_list:
                t.start()
            for t in t_list:
                t.join()
            print('*' * 50)
        except Exception as e:
            print("发生错误了：", e)



def info():
    fig=pyfiglet.Figlet('slant')
    HEADER=fig.renderText('F_ANSWER')
    WRITER='https://github.com/vanpersiexp'
    print('\033[95m'+HEADER)
    print('\033[95m'+WRITER.center(50))
    print('\033[95m'+"使用Ctrl+C停止.".center(50))

def main():
    if args.brand:
        brand_2_old=''
        brand_4_old=''
        for raw in tailer.follow(open('/tmp/raw_data.txt','r')):
            if args.brand == 1:
                if 'showQuestion' in raw:
                    game=GetAnswer(args.brand,raw)
                    game.run()
            elif args.brand == 2:
                try:
                    raw=raw.split('(')[-1].split(')')[0]
                    raw_json=json.loads(raw)
                    raw_question=raw_json['data']['msg']['answer']['doing']['doing']['title']
                    raw_question_showanswer=raw_json['data']['msg']['answer']['doing']['doing']['show_answer']
                    if not raw_question_showanswer:
                        if raw_question != brand_2_old:
                            game=GetAnswer(args.brand,raw_json)
                            game.run()
                        brand_2_old = raw_question
                except Exception:
                    continue
            elif args.brand == 3:
                raw_json=json.loads(raw)
                try:
                    raw_json['data']['quiz']
                    game=GetAnswer(args.brand,raw_json)
                    game.run()
                except Exception:
                    continue
            elif args.brand == 4:
                try:
                    if 'question' in raw:
                        if raw != brand_4_old:
                            raw_json=json.loads(raw)
                            game=GetAnswer(args.brand,raw_json)
                            game.run()
                        brand_4_old=raw
                except Exception:
                    continue
            else:
                print("python3 search_question -h")
                print("请查看帮助文档，目前仅支持4个APP的抓包获取题目。")
                sys.exit(1)
    else:
        print("python3 search_question -h")
        print("请查看帮助文档，需要选择对应的APP。")
        print("例如,选择冲顶大会:python3 search_question -b 1")
        sys.exit(1)

if __name__=='__main__':
    try:
        info()
        main()
    except Exception as e:
        print("发生错误了：",e)
    finally:
        try:
            CHROME.close()
        except Exception:
            pass
