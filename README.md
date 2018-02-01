# 冲顶大会/百万赢家/头脑王者/UC疯狂夺金答题辅助：抓包获取题目并搜索答案
冲顶大会/百万赢家/头脑王者/UC疯狂夺金：抓包获取题目，不用图像识别:)

测试环境：Kali Linux,Python3，Android

需要的抓包工具：[mitmdump](https://github.com/mitmproxy/mitmproxy)

[mitmdump官方文档](http://docs.mitmproxy.org/en/stable/index.html)

## 使用方法
[mitmproxy安装方法](http://docs.mitmproxy.org/en/stable/install.html)

首次运行`mitmdump`或`mitmproxy`，在`.mitmproxy/`中获取证书`mitmproxy-ca-cert.cer`

在Android手机中安装证书，与电脑处于同一wifi下，手动设置代理为电脑ip地址：192.168.1.100，端口（默认）：8080

	git clone https://github.com/vanpersiexp/chongding.git
    cd chongding/
	pip3 install -r related.txt
	mitmdump -s get_question.py
	python3 search_question.py -h
	
	usage: search_question.py [-h] [-b {1,2,3,4}]

	冲顶大会/百万赢家/头脑王者/UC疯狂夺金:抓包获取题目并搜索答案。

	optional arguments:
  	-h, --help            		show this help message and exit
  	-b {1,2,3,4}, --brand {1,2,3,4}		
					选择APP，1：冲顶大会；2：百万赢家；3：头脑王者；4：UC疯狂夺金
	

## 抓包结果
冲顶大会抓包结果：
![冲顶大会](https://raw.githubusercontent.com/vanpersiexp/chongding/master/img/20180126_17.jpg)

头脑王者抓包结果：
![头脑王者](https://raw.githubusercontent.com/vanpersiexp/chongding/master/img/tounaowangzhe.jpg)

UC疯狂夺金抓包结果：
![疯狂夺金](https://raw.githubusercontent.com/vanpersiexp/chongding/master/img/fkdj_2.jpg)

## 运行效果
可以使用`example/`中的抓取的数据包*模拟测试程序*。

`search_question.py`中的`main`函数，使用`tailer`模块循环读取最新的`/tmp/raw_data.txt`文件

`tailer`模块的使用说明参考：[传送门](https://pypi.python.org/pypi/tailer)

测试方法（以冲顶大会为例，问题选取自example/chongdingdahui.txt）：

第一个终端运行：`python3 search_question.py -b 1`

第二个终端运行：`echo '42["showQuestion",{"answerTime":10,"desc":"10.汉字“趸（dǔn）”的词性不包括以下哪个?","displayOrder":9,"liveId":164,"options":"[\"动词\",\"名词\",\"副词\"]","questionId":1910,"showTime":16910135117165,"status":0,"type":"showQuestion"}]' >> /tmp/raw_data.txt`


实时运行效果如图：

冲顶大会：

![冲顶大会](https://raw.githubusercontent.com/vanpersiexp/chongding/master/img/chongdingdahui.jpg)

百万赢家：

![百万赢家](https://raw.githubusercontent.com/vanpersiexp/chongding/master/img/baiwanyingjia.jpg)

头脑王者：
![头脑王者](https://raw.githubusercontent.com/vanpersiexp/chongding/master/img/tounao.jpg)

UC疯狂夺金：
![疯狂夺金](https://raw.githubusercontent.com/vanpersiexp/chongding/master/img/fkdj_1.jpg)

## 联系方式
pu.xiaorvp@gmail.com
