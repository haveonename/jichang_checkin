import requests, json, re, os,notify,smtp

session = requests.session()
# 机场的地址
url = os.environ.get('URL')
# 配置用户名（一般是邮箱）
email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('PASSWD')
# server酱
SCKEY = os.environ.get('SCKEY')
#SMTP
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_TLS = os.environ.get('SMTP_TLS')
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_SENDER = os.environ.get('SMTP_SENDER')
SMTP_RECEIVER = os.environ.get('SMTP_RECEIVER')
smtpConfigDict = {"smtp_host":SMTP_HOST, "smtp_port":SMTP_PORT, "smtp_tls":SMTP_TLS, "smtp_user":SMTP_USER, "smtp_password":SMTP_PASSWORD, "smtp_sender":SMTP_SENDER, "smtp_receiver":SMTP_RECEIVER}

login_url = '{}/auth/login'.format(url)
check_url = '{}/user/checkin'.format(url)


header = {
        'origin': url,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
data = {
        'email': email,
        'passwd': passwd
}

loginContent = "";
content = "";
try:
    print('进行登录...')
    response = json.loads(session.post(url=login_url,headers=header,data=data).text)
    print(response['msg'])
    loginContent = response['msg']
    # 进行签到
    result = json.loads(session.post(url=check_url,headers=header).text)
    print(result['msg'])
    content = result['msg']
    # 进行推送
    smtp.push(smtpConfigDict, loginContent + "\n" + content, "", "iKuuu签到成功")
    print("邮箱推送成功")
    notify.dingding_bot("airport签到成功", loginContent + "\n" + content)
    print("钉钉推送成功")
    if SCKEY != '':
        push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
        requests.post(url=push_url)
        print('推送成功')
except Exception as e:
    traceback.print_exc()
    notify.dingding_bot("airport签到失败",  loginContent + "\n" + content + "\n" + traceback.format_exc())
    content = '签到失败'
    print(content)
    if SCKEY != '':
        push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
        requests.post(url=push_url)
