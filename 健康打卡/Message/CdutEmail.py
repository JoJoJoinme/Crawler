import smtplib
from email.mime.text import MIMEText
from email.header import Header

# mail_host = 'smtp.163.com'
# mail_user = 'cduthealth'
# mail_pass = 'BZFZTEXYFTJVDRXH'


mail_host = 'smtp.qq.com'
mail_user = 'helious.wu@foxmail.com'
mail_pass = 'lwxidhrkfrusgdgb'



# sender = 'cduthealth@163.com'
sender = 'helious.wu@foxmail.com'
receivers = ['1419069126@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱，注意用单引号括起来

html_text = """
<p>健康打卡因意外而执行错误,请手动执行打卡。待作者更新后可重新拉取代码</p>
<p><a href="https://github.com/JoJoJoinme/Crawler/tree/master/%E5%81%A5%E5%BA%B7%E6%89%93%E5%8D%A1">相关代码源地址（轻点我)</a></p>
"""
title = '健康打卡'


def sendEmail():
    message = MIMEText(html_text, 'html', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


def send_email2(SMTP_host, from_account, from_passwd, to_account, subject, content):
    email_client = smtplib.SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)
    # create msg
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    msg['To'] = to_account
    email_client.sendmail(from_account, to_account, msg.as_string())

    email_client.quit()


if __name__ == '__main__':
    sendEmail()
