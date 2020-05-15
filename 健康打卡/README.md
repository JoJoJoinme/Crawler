#### CDUT健康打卡自动化脚本使用指南

程序执行异常会执行相关邮件或微信推送，若执行正常，则不会推送。

#### 环境要求：

系统：Windows 10

Python版本：3.6+

#### 使用方法：

1. 将文件下载到电脑任意位置并切换到该目录
   在当前目录下按 shift+鼠标右键 打开终端
   然后pip install -r requirements.txt
   
2. 确定你要使用哪个浏览器，及对应的版本。下载相应的Driver

   我在下面放上我测试过的浏览器的Driver下载地址

   Microsoft Edge:https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

   Chrome:https://sites.google.com/a/chromium.org/chromedriver/downloads
   
3. 在**data.yml**文件中按照示例填上你的个人信息，注意用单引号框起来你的值（你也可以填多个人的信息，将会按填写顺序执行打卡)

4. ~~在**Message**文件中选择你想要的推送方式，**ft.py**为微信推送（需填写SCKEY，已在文件中注明获取方法），**CdutEmail.py**为邮件推送（需填写收件人地址，已在文件中注明填写位置）。~~

5. 打开CDUT.py文件，将第9行括号内的路径改为你的**data.yml**文件存放路径

   ```python
   with open(r'D:\python3\健康打卡\data.yml', encoding='utf-8')as fp_stream:
   ```

   在第25，26行，如果用Microsoft Edge就将另一个注释掉。反之，亦然。

   ```python
   self.driver = webdriver.Chrome('F:\Chrome Driver\chromedriver_win32\chromedriver.exe')  # 括号内为你的Chromedriver存放路径
   self.driver = webdriver.Edge('F:\Edge Driver\edgedriver_win64\msedgedriver.exe')       # 括号内为你的MicrosoftEdge driver存放路径
   ```

6. 如果以上以上工作你都顺利完成，那么你可以运行一遍，测试是否通过。

   如果没有通过那么请仔细核对上述工作是否全部完成、若还是不能请给予我反馈。
   
7. 如果顺利通过，右键管理员执行`create-task.bat`,默认设置为早上9.00打卡，你也可以用编辑器打开该文件进行修改。
   

   
   --------------------------------<font color=red>已采用bat脚本设置定时任务，以下设置不再必要，仅供参考</font>-----------------------------------
##### 配合Windows 10自带的定时任务完成每日打卡

​		虽然我们完成了每日打卡，但是每天还得手动执行一遍程序，还是有点麻烦。那么有没有自动打卡的方法呢，我们配合Windows 10 的定时任务计划即可。

​		**开始菜单（鼠标右键）**-------**计算机管理**

​		接下来如下图所示。

​		<img src="https://i.loli.net/2020/05/06/efiWkxyd98STbqc.png" alt="T_FGVHY@19RFPHRH_F3TR_O.png" style="zoom:50%;" />

python路径可以通过在命令行窗口中输入

```python
python
import sys
print(sys.path)
```

一般为`"C:\Users\用户名\AppData\Local\Programs\Python\"`路径下

程序路径即为你的**CDUT.py** 存储路径

![<img src="https://i.loli.net/2020/05/06/Fu5QhTlU2WYavrg.png" alt="img" style="zoom:72%;" />]

测试一下。通过！！！

#### 声明

本脚本仅供学习交流使用，其余任何行为均与作者无关。