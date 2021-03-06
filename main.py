from tkinter import *
from tkinter import messagebox
import hashlib
from sql import Mysql,Sqlite
import os,re,time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import threading


# 默认是的python自带的Sqlite3数据库
# 如果需要换MySQL的请先安装模块 pymysql 和MySQL本地环境,确保能够在本地使用
# 安装完模块和配置好本地MySQL之后,将类 Login 的继承者改为Mysql
class Login(Sqlite):    # 替换Mysql

    def __init__(self):
        self.windows = Tk()
        Sqlite.__init__(self)    # 如果要换数据库~记得替换这里~

    # 加密密码
    def hash(self,username,password):
        md5 = hashlib.md5()
        md5.update((str(username)+str(password)+"guess*number").encode())
        return md5.hexdigest()

    # 匹配email地址
    def check_email_is_ok(self,email):
        pattern = re.compile(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
        return pattern.search(email)

    def sgin_email_daojishi_threading(self):
        th = threading.Thread(target=self.sgin_daojishi)
        th.setDaemon(True)
        th.start()

    def forget_email_daojishi_threading(self):
        th = threading.Thread(target=self.forget_daojishi)
        th.setDaemon(True)
        th.start()

    def sgin_daojishi(self):
        try:
            times = 60
            while times >= 1:
                times-=1
                time.sleep(1)
                self.code_btn.config(text=times)
            self.code_btn.config(text="发送")
            self.code_btn.config(state=NORMAL)
        except TclError:
            pass

    def forget_daojishi(self):
        try:
            times = 60
            while times >= 1:
                times -= 1
                time.sleep(1)
                self.find_code_btn.config(fg="#FFF")
                self.find_code_btn.config(text=times)
            self.find_code_btn.config(text="发送")
            self.find_code_btn.config(state=NORMAL)
        except TclError:
            pass

    def aboutme_windows_exit(self):
        self.aboutmes.config(state=NORMAL)    # 获取到了'关于我'窗口的关闭事件之后，按钮将恢复正常使用
        self.aboutme_windows.destroy()    # '关于我'窗口页面关闭

    def aboutme(self):
        self.aboutmes.config(state=DISABLED)# 点了之后按钮将不可用,防止多次跳出
        self.aboutme_windows = Toplevel(self.windows)
        self.aboutme_windows.wm_attributes('-topmost',1)
        self.aboutme_windows.resizable(False,False)
        self.aboutme_windows.iconbitmap(default="img/head.ico")
        ws = self.aboutme_windows.winfo_screenwidth()
        hs = self.aboutme_windows.winfo_screenheight()
        w = 300
        h = 300
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.aboutme_windows.geometry("%dx%d+%d+%d" % (w,h,x,y))
        self.aboutme_windows.title("关于我")
        self.aboutme_windows.config(bg="#222")
        text = Text(self.aboutme_windows,bg="#222",fg="#FFF",font=("楷体",15),relief="flat")
        text.pack(anchor='center')
        text.insert(END,"作者:\nCrazyRookie\n\n个人博客:\nwww.liuyangxiong.top\n\nEmail:\ncrazyrookie@163.com\n\nQQ:\n1473018671\n\n\n请勿非法使用,仅供学习！")
        text.config(state=DISABLED)
        self.aboutme_windows.protocol("WM_DELETE_WINDOW",self.aboutme_windows_exit)   # 关闭事件

    def send_feedback(self):
        if self.subject.get().strip() == "":
            self.feedback_listbox.delete(0,END)
            self.feedback_listbox.insert(END,"抱歉,请输入标题~")
        elif self.calldef.get().strip() == "" or self.calldef.get() == "QQ/Email":
            self.feedback_listbox.delete(0, END)
            self.feedback_listbox.insert(END, "抱歉,请输入联系方式")
        elif self.feedbacktext_text.get("0.0",END).strip() == "":
            self.feedback_listbox.delete(0, END)
            self.feedback_listbox.insert(END, "抱歉,请输入内容~")
        else:
            serder = "2905217710@qq.com"
            receiver = "crazyrookie@163.com"
            smtp_server = "smtp.qq.com"
            username = "2905217710@qq.com"
            password = "cswqzrqkhzzkdgjg"
            msg = MIMEText("反馈用户联系方式:{}\n\n{}".format(self.calldef.get(),self.feedbacktext_text.get("0.0",END)), 'plain', 'utf-8')
            msg['From'] = serder
            msg['To'] = receiver
            msg['Subject'] = Header(u"猜数字游戏用户反馈,标题:{}".format(self.subject.get()), "utf-8").encode()
            smtp = smtplib.SMTP_SSL(smtp_server, 465)
            smtp.login(username, password)
            smtp.sendmail(serder, receiver, msg.as_string())
            self.feedback_listbox.delete(0, END)
            self.feedback_listbox.config(fg="#FFF")
            self.feedback_listbox.insert(END, "已发送!感谢您的建议~~")

    def seed_feedback_windows_exit(self):
        self.feedbacks.config(state=NORMAL)    # 获取到了'关于我'窗口的关闭事件之后，按钮将恢复正常使用
        self.feedback_windows.destroy()    # '关于我'窗口页面关闭

    def feedback(self):
        self.feedbacks.config(state=DISABLED)    # 点了之后按钮将不可用,防止多次跳出
        self.subject = StringVar()
        self.calldef = StringVar()
        self.calldef.set("QQ/Email")
        # self.feedback_text = StringVar()
        self.feedback_windows = Toplevel(self.windows)
        self.feedback_windows.wm_attributes('-topmost',1)
        self.feedback_windows.resizable(False,False)
        self.feedback_windows.iconbitmap(default="img/head.ico")
        self.feedback_windows.config(bg="#222")
        ws = self.feedback_windows.winfo_screenwidth()
        hs = self.feedback_windows.winfo_screenheight()
        w = 450
        h = 450
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.feedback_windows.geometry("%dx%d+%d+%d" % (w,h,x,y))
        subject_label = Label(self.feedback_windows,text="标题",bg="#222",fg="#FFF",relief="flat",font=("楷体",20)).place(x=0,y=10)
        subject_entry = Entry(self.feedback_windows,bg="#333",fg="#888",relief="flat",font=("楷体",20),width=22,textvariable=self.subject)
        subject_entry.place(x=125,y=10)
        calldef_label = Label(self.feedback_windows,text="联系方式",bg="#222",fg="#FFF",relief="flat",font=("楷体",20)).place(x=0,y=50)
        calldef_entry = Entry(self.feedback_windows,bg="#333",fg="#888",relief="flat",font=("楷体",20),width=18,textvariable=self.calldef)
        calldef_entry.place(x=125,y=50)
        feedbacktext_lable = Label(self.feedback_windows,text="内容",bg="#222",fg="#FFF",relief="flat",font=("楷体",20)).place(x=0,y=100)
        self.feedbacktext_text = Text(self.feedback_windows,bg="#222",fg="#FFF",relief="solid",width=61,height=20)
        self.feedbacktext_text.place(x=10,y=140)
        send_btn = Button(self.feedback_windows,text=" 提\t交 ",bg="#222",fg="#FFF",relief="solid",font=("楷体",15),command=self.send_feedback).place(x=300,y=410)
        self.feedback_listbox = Listbox(self.feedback_windows,bg="#222",fg="red",relief="flat",font=("楷体",15),height=1)
        self.feedback_listbox.place(x=20,y=420)
        self.feedback_windows.protocol("WM_DELETE_WINDOW",self.seed_feedback_windows_exit)    # 关闭事件


    # 发送邮箱验证码
    def send_email(self,email,name):
        self.randomslist = "".join(list(map(str, random.sample(range(1, 10), 5))))
        serder = "2905217710@qq.com"
        receiver = email
        smtp_server = "smtp.qq.com"
        username = "2905217710@qq.com"
        password = "cswqzrqkhzzkdgjg"
        msg = MIMEText("验证码:{}".format(self.randomslist), 'plain', 'utf-8')
        msg['From'] = serder
        msg['To'] = receiver
        msg['Subject'] = Header(u"Hello {}".format(name), "utf-8").encode()
        smtp = smtplib.SMTP_SSL(smtp_server, 465)
        smtp.login(username, password)
        smtp.sendmail(serder, receiver, msg.as_string())
        # print(self.randomslist)

    # 发送邮箱验证码
    def sgin_send_email(self):

        if self.var_email.get().strip() == "" or self.var_email.get() == "example@email.com":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,你还没输入邮箱呐~")
        else:
            if self.check_email(self.var_email.get()) != None:
                self.information_text.delete(0, END)
                self.information_text.insert(END, "抱歉,此邮箱已被注册~")
            elif self.check_email_is_ok(self.var_email.get()) == None:
                self.information_text.delete(0, END)
                self.information_text.insert(END, "抱歉,邮箱地址错误")
            else:
                self.sgin_up_windows.wm_attributes('-topmost', 1)
                self.send_email(self.var_email.get(),self.var_username.get())
                self.code_btn.config(state=DISABLED)
                self.information_text.delete(0, END)
                self.information_text.insert(END, "已成功发送,请打开邮箱查看验证码~")
                self.information_text.config(fg="#FFF")
                self.sgin_email_daojishi_threading()

    # 检测输入的是否合法~
    def check_input_is_ok(self):
        # print(self.var_username.get().strip() == "")
        if self.var_username.get().strip() == "":
            self.information_text.delete(0,END)
            self.information_text.insert(END,"抱歉,请输入用户名~")
        elif self.var_password.get().strip() == "":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,请输入密码~")
        elif self.var_againpassword.get().strip() == "":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,请确认密码~")
        elif self.var_password.get() != self.var_againpassword.get():
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,两次密码不统一,请检查~")
        elif self.var_email.get().strip() == "" or self.var_email.get() == "example@email.com":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,请输入邮箱地址~")
        elif self.var_username.get()[0].isspace() == True or self.var_username.get()[-1].isspace() or len(self.var_username.get().split()) != 1 or self.var_username.get()[0].isdigit() == True:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,用户名格式不对,请检查~(合法格式例如:hello_123 or hello123 and @hello123)")
        elif len(self.var_password.get()) <= 6 or  [i for i in self.var_password.get() if i.isalpha()] == []:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,密码太弱,请输入6位数以上且带有一个字母~")
        elif self.check_email_is_ok(self.var_email.get()) == None:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,邮箱地址不正确,请检查~")
        elif self.check_username(self.var_username.get()) != None:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,用户名已存在~")
        elif self.check_email(self.var_email.get()) != None:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,此邮箱已被注册~")
        elif self.var_verification_code.get().strip() == "":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "请输入验证码~")
        elif self.var_verification_code.get() != self.randomslist:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "验证码错误~")
        else:
            passmd5 = self.hash(self.var_username.get(),self.var_password.get())
            self.sava(self.var_username.get(),passmd5,self.var_email.get())
            # messagebox.showinfo(title="提示:", message="用户名'{}',创建成功！快去登录试试吧~~".format(self.var_username.get()))
            self.information_text.delete(0, END)
            self.information_text.config(fg="#FFF")
            self.information_text.insert(END, "用户名'{}',创建成功！快去登录试试吧~~".format(self.var_username.get()))
            self.sginup_btn.config(state=DISABLED)

    # 登录页面
    def user_login(self):
        if self.var_name_input.get() == self.check_username(self.var_name_input.get()) or self.var_name_input.get() == self.check_email(self.var_name_input.get()):    # 检查用户名是否在数据库
            if not self.var_pass_input.get():
                messagebox.showinfo(title="提示:", message="抱歉,请输入密码~")
            else:
                if self.check_email_is_ok(self.var_name_input.get()) != None:
                    if self.hash(self.check_email_password(self.var_name_input.get())[0],self.var_pass_input.get()) != self.check_password(self.check_email_password(self.var_name_input.get())[0],self.var_pass_input.get()):
                        messagebox.showinfo(title="提示:", message="抱歉,密码错误,请重新输入~")
                    else:
                        messagebox.showinfo(title="提示:", message="Welcome,How are you~ " + self.get_username(self.var_name_input.get()))
                        self.windows.destroy()
                        Gamemain().main(self.get_username(self.var_name_input.get()))
                else:
                    if self.check_password(self.var_name_input.get(),self.var_pass_input.get()) == None:
                        messagebox.showinfo(title="提示:", message="抱歉,密码错误,请重新输入~")
                    else:
                        messagebox.showinfo(title="提示:", message="Welcome,How are you~ " + self.var_name_input.get())
                        self.windows.destroy()
                        Gamemain().main(self.var_name_input.get())
        else:
            tf = messagebox.askyesno(title="提示:", message="Sorry,username not exists~Sgin Up?")
            if tf == True:
                self.user_sign_up()

    def sign_btn_state(self):
        self.sgin_btn.config(state=NORMAL)
        self.login_btn.config(state=NORMAL)
        self.sgin_up_windows.destroy()
    # 注册页面
    def user_sign_up(self):
        self.login_btn.config(state=DISABLED)  # 点了之后按钮将不可用,防止多次跳出
        self.sgin_btn.config(state=DISABLED)  # 点了之后按钮将不可用,防止多次跳出
        self.sgin_up_windows = Toplevel(self.windows)
        self.sgin_up_windows.wm_attributes('-topmost',1)
        self.sgin_up_windows.resizable(False,False)
        self.sgin_up_windows.iconbitmap(default="img/head.ico")
        ws = self.windows.winfo_screenwidth()
        hs = self.windows.winfo_screenheight()
        w = 600
        h = 460
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.sgin_up_windows.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.sgin_up_windows.maxsize("600","420")
        self.sgin_up_windows.minsize("600","420")
        self.sgin_up_windows.title("Sgin Up")
        self.sgin_up_windows.config(bg="#222")
        Label(self.sgin_up_windows,text="Sgin Up",font=("楷体",60),bg="#222",fg="#fbd").pack(side="bottom")
        username = Label(self.sgin_up_windows,text="New Username:",font=("宋体",20),bg="#222").place(x=40,y=20)
        password = Label(self.sgin_up_windows,text="Password:",font=("宋体",20),bg="#222").place(x=97,y=70)
        passagain = Label(self.sgin_up_windows,text="Again Password:",font=("宋体",20),bg="#222").place(x=13,y=120)
        email = Label(self.sgin_up_windows,text="Email:",font=("宋体",20),bg="#222").place(x=139,y=170)
        self.varification_code = Label(self.sgin_up_windows,text="Code:",font=("宋体",25),bg="#222").place(x=140,y=230)
        self.var_username = StringVar()
        self.var_password = StringVar()
        self.var_againpassword = StringVar()
        self.var_email = StringVar()
        self.var_verification_code = StringVar()
        self.var_text = StringVar()
        self.var_email.set("example@email.com")
        inname = Entry(self.sgin_up_windows,font=("宋体",20,),bg="#333",relief="solid",textvariable=self.var_username)
        inname.place(x=240,y=20)
        inpass = Entry(self.sgin_up_windows,font=("宋体",20),bg="#333",relief="solid",textvariable=self.var_password,show="*")
        inpass.place(x=240,y=70)
        againpass = Entry(self.sgin_up_windows,font=("宋体",20),bg="#333",relief="solid",textvariable=self.var_againpassword,show="*")
        againpass.place(x=240,y=120)
        inemail = Entry(self.sgin_up_windows,font=("宋体",20),bg="#333",relief="solid",textvariable=self.var_email)
        inemail.place(x=240,y=170)
        inverification_code = Entry(self.sgin_up_windows,font=("宋体",25),insertbackground="#000",width=5,bg="#333",relief="solid",textvariable=self.var_verification_code)
        inverification_code.place(x=240,y=230)
        self.code_btn = Button(self.sgin_up_windows,font=("宋体",12),text="发送",bg="#222",width=6,relief="solid",command=self.sgin_send_email)
        self.code_btn.place(x=530,y=170)
        self.sginup_btn = Button(self.sgin_up_windows,text=" Sgin ",font=("宋体",20),bg="#222",relief="solid",command=self.check_input_is_ok,activebackground="#222")
        self.sginup_btn.place(x=430,y=230)
        self.information_text = Listbox(self.sgin_up_windows,bg="#222",fg="red",width=45,height=1,font=("微软雅黑",15),relief="flat")
        self.information_text.place(x=30, y=300)
        self.sgin_up_windows.protocol("WM_DELETE_WINDOW",self.sign_btn_state)

    # 检查新修改的密码是否ok
    def check_new_pass_is_ok(self):
        if self.new_pass.get().strip() == "":
            # messagebox.showinfo(title="提示", message="抱歉,请输入密码~")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.insert(END, "抱歉,请输入密码~")
        elif self.agagin_pass.get().strip() == "":
            # messagebox.showinfo(title="提示",message="抱歉,请确认密码~please agagin~")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.insert(END, "抱歉,请确认密码~please agagin~")
        elif self.new_pass.get() != self.agagin_pass.get():
            # messagebox.showinfo(title="提示",message="抱歉,两次输入的密码不相同~")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.insert(END, "抱歉,两次输入的密码不相同~")
        elif len(self.new_pass.get()) <= 6 or [i for i in self.new_pass.get() if i.isalpha()] == []:
            # messagebox.showinfo(title="提示:",message="抱歉,密码太弱,请输入6位数以上且带有一个字母~")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.insert(END, "抱歉,密码太弱,请输入6位数以上且带有一个字母~~")
        else:
            self.change_pass(self.hash(self.forget_name.get(),self.new_pass.get()),self.forget_name.get(),self.forget_email.get())
            # messagebox.showinfo(title="提示",message=" 修改成功!   ")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.config(fg="#FFF")
            self.change_pass_text.insert(END, "修改成功!")


    def forget_send_email(self):
        if self.check_email(self.forget_email.get()) == None:
            self.find_text.delete(0, END)
            self.find_text.insert(END, "邮箱不存在~")
        else:
            self.send_email(self.forget_email.get(),self.forget_name.get())
            self.find_code_btn.config(state=DISABLED)
            self.find_text.delete(0,END)
            self.find_text.config(fg="#FFF")
            self.find_text.insert(END,"验证码已发送，请查看邮箱~")
            self.forget_email_daojishi_threading()

    # 更改密码
    def change_password(self):
        if self.var_name_input.get().strip() == "":
            self.find_text.delete(0, END)
            self.find_text.insert(END, "用户名不得为空~")
        elif self.check_forget_pass(self.forget_name.get(),self.forget_email.get()) == None:
            self.find_text.delete(0,END)
            self.find_text.insert(END,"用户名不存在或邮箱错误~")
        elif self.find_code.get().strip() == "":
            self.find_text.delete(0, END)
            self.find_text.insert(END, "验证码不得为空~")
        elif self.find_code.get() != self.randomslist:
            self.find_text.delete(0, END)
            self.find_text.insert(END, "验证码错误~")
        else:
            self.change_pass_windows = Toplevel(self.windows)
            self.change_pass_windows.wm_attributes('-topmost',1)
            self.change_pass_windows.resizable(False,False)
            self.change_pass_windows.iconbitmap(default="img/head.ico")
            ws = self.change_pass_windows.winfo_screenwidth()
            hs = self.change_pass_windows.winfo_screenheight()
            w = 450
            h = 300
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)
            self.change_pass_windows.geometry("%dx%d+%d+%d" % (w,h,x,y))
            self.change_pass_windows.config(bg="#222")
            self.change_pass_windows.maxsize("450","300")
            self.change_pass_windows.minsize("450","300")
            self.change_pass_windows.title("Change Password~")
            icon = Label(self.change_pass_windows,text="Change Password",font=("微软雅黑",30),bg="#222",fg="#568").pack()
            new_pass_label = Label(self.change_pass_windows,text="New Password",font=("楷体",15),bg="#222").place(x=30,y=100)
            agagin_pass_label = Label(self.change_pass_windows,text="Again Password",font=("楷体",15),bg="#222").place(x=20,y=150)
            self.new_pass = StringVar()
            self.agagin_pass = StringVar()
            new_pass_btn = Entry(self.change_pass_windows,show="*",font=("楷体",15),relief="solid",bg="#222",textvariable=self.new_pass)
            new_pass_btn.place(x=190,y=100)
            agagin_pass_btn = Entry(self.change_pass_windows,show="*",font=("楷体",15),relief="solid",bg="#222",textvariable=self.agagin_pass)
            agagin_pass_btn.place(x=190,y=150)
            btn = Button(self.change_pass_windows,text="确认",font=("楷体",10),relief="solid",activebackground="#222",bg="#222",command=self.check_new_pass_is_ok).place(x=380,y=250)
            self.change_pass_text = Listbox(self.change_pass_windows,bg="#222",fg="red",width=30,height=1,font=("微软雅黑",15),relief="flat")
            self.change_pass_text.place(x=50,y=200)

    def forget_pass_btn_state(self):
        self.forget_pass_btn.config(state=NORMAL)
        self.forget_pass_windows.destroy()
    # 忘记密码
    def forget_password(self):
        self.forget_pass_btn.config(state=DISABLED)
        self.forget_pass_windows = Toplevel(self.windows)
        self.forget_pass_windows.wm_attributes('-topmost',1)
        self.forget_pass_windows.resizable(False,False)
        self.forget_pass_windows.iconbitmap(default="img/head.ico")
        ws = self.forget_pass_windows.winfo_screenwidth()
        hs = self.forget_pass_windows.winfo_screenheight()
        w = 600
        h = 300
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.forget_pass_windows.geometry("%dx%d+%d+%d" % (w,h,x,y))
        self.forget_pass_windows.maxsize("600","300")
        self.forget_pass_windows.minsize("600","300")
        self.forget_pass_windows.title("Forget Password")
        self.forget_pass_windows.config(bg="#222")
        labelname = Label(self.forget_pass_windows,text="Username",bg="#222",font=("微软雅黑",20)).place(x=50,y=50)
        labelemail = Label(self.forget_pass_windows,text="Email",bg="#222",font=("微软雅黑",20)).place(x=110,y=120)
        self.find_inverification_code = Label(self.forget_pass_windows,text="Code",bg="#222",font=("微软雅黑",20)).place(x=110,y=190)
        self.forget_name = StringVar()
        self.forget_email = StringVar()
        self.find_code = StringVar()
        if self.var_name_input.get() == "example@email.com":
            pass
        elif self.check_email_is_ok(self.var_name_input.get()):
            self.forget_email.set(self.var_name_input.get())
        elif self.var_name_input.get().split("@")[-1] not in ["qq.com", "gmail.com", "163.com"]:
            self.forget_name.set(self.var_name_input.get())
        else:
            pass
        inname = Entry(self.forget_pass_windows,textvariable=self.forget_name,font=("微软雅黑",20),bg="#222",relief="solid")
        inname.place(x=200,y=50)
        inemail = Entry(self.forget_pass_windows,textvariable=self.forget_email,font=("微软雅黑",20),bg="#222",relief="solid")
        inemail.place(x=200,y=120)
        find_inverification_code = Entry(self.forget_pass_windows,textvariable=self.find_code,font=("微软雅黑",20),bg="#222",relief="solid",width=5)
        find_inverification_code.place(x=200,y=190)
        find_btn = Button(self.forget_pass_windows,text="更改密码",font=("微软雅黑",15),relief="solid",activebackground="#222",bg="#222",fg="#FFF",command=self.change_password).place(x=450,y=180)
        self.find_code_btn = Button(self.forget_pass_windows,text="发送",font=("微软雅黑",10),relief="solid",activebackground="#222",bg="#222",fg="#FFF",command=self.forget_send_email)
        self.find_code_btn.place(x=300,y=190)
        self.find_text = Listbox(self.forget_pass_windows,bg="#222",fg="red",width=30,height=1,font=("微软雅黑",15),relief="flat")
        self.find_text.place(x=50,y=250)
        self.forget_pass_windows.protocol("WM_DELETE_WINDOW",self.forget_pass_btn_state)
    # 退出提示
    def main_windows_exit(self):
        exit_or_notexit = messagebox.askyesno(message="确定要离开了吗?")
        if exit_or_notexit:
            self.windows.quit()
        else:
            pass

    def main(self):
        self.windows.iconbitmap(default="img/head.ico")
        self.windows.wm_attributes('-topmost',1)   # 将窗口顶置~
        ws = self.windows.winfo_screenwidth()   # 获取显示器显示的宽度
        hs = self.windows.winfo_screenheight()   # 获取显示器显示的高度
        w = 800
        h = 500
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.windows.geometry('%dx%d+%d+%d' % (w, h, x, y))    # 在显示器中心出现
        self.windows.maxsize("800","500")
        self.windows.minsize("800","500")
        self.windows.title("Python Guess Number Game")
        self.windows.config(bg="#222")
        if os.name == "posix":    # 因为在Linux环境中,overrideredirect无法正常使用Entry和Button,还会导致卡死
            pass
        else:
            self.windows.overrideredirect(True)    # 去除边框
            self.exit_btn = Button(self.windows, text="Exit", command=self.main_windows_exit, relief="flat", fg="#FFFFFF",bg="#222",font=("楷体",15)).place(
                x=10, y=0)    # Windows环境下使用了overrideredirect之后就没有边框了,自己弄一个退出按钮~
        image = PhotoImage(file="img/Welcome.png")    # 设置欢迎界面
        img = Label(self.windows,image=image,width=700,bg="#222").place(x=130,y=-30)
        usename = Label(self.windows,text="username",font=("宋体",30),fg="#888",bg="#222").place(x=80,y=200)
        password = Label(self.windows,text="password",font=("宋体",30),fg="#888",bg="#222").place(x=80,y=300)
        self.var_name_input = StringVar()
        self.var_name_input.set("example@email.com")
        inname = Entry(self.windows,textvariable=self.var_name_input,font=("宋体",30),relief="solid",bg="#222")
        inname.place(x=300,y=200)
        self.var_pass_input = StringVar()
        inpass = Entry(show="❤",textvariable=self.var_pass_input,font=("宋体",30),relief="solid",bg="#222")
        inpass.place(x=300,y=300)
        self.forget_pass_btn = Button(self.windows,text="forget password?",font=("楷体",10),relief="solid",bg="#222",fg="#FFF",command=self.forget_password,activebackground="#222")
        self.forget_pass_btn.place(x=580,y=350)
        self.login_btn = Button(self.windows,text="Login",command=self.user_login,font=("宋体",20),relief="flat",bg="#222",fg="#fff",activebackground="#222")
        self.login_btn.place(x=300,y=400)
        self.sgin_btn = Button(self.windows, text="Sign up", command=self.user_sign_up, font=("宋体", 20),relief="flat",bg="#222",fg="#fff",activebackground="#222")
        self.sgin_btn.place(x=500, y=400)
        version = Label(self.windows,text="版本：V3.0.1",bg="#222",fg="#FFF").place(x=0,y=480)
        self.aboutmes = Button(self.windows,text="关于我",bg="#222",fg="#FFF",relief="flat",activebackground="#222",command=self.aboutme)
        self.aboutmes.place(x=80,y=477)
        self.feedbacks = Button(self.windows,text="反馈",bg="#222",fg="#FFF",relief="flat",activebackground="#222",command=self.feedback)
        self.feedbacks.place(x=135,y=477)
        self.windows.mainloop()

# 游戏界面
class Gamemain():

    def __init__(self):
        self.gamewindows = Tk()
        self.usename = ""
        self.password = ""


    def check_time_threading(self):
        self.check_times.config(state=DISABLED)
        self.check_times.config(relief='flat')
        self.check_times.place(x=40,y=60)
        def time_time():
            while True:
                self.check_times.config(text=time.ctime())
        th = threading.Thread(target=time_time)
        th.setDaemon(True)
        th.start()

    def exit_game_recording(self):
        self.check_game_recording_btn.config(state=NORMAL)
        self.check_game_recording_windows.destroy()
        self.check_game_recording_btn.config(relief='solid')

    def check_game_recording(self):
        self.check_game_recording_btn.config(state=DISABLED)
        self.check_game_recording_btn.config(relief='flat')
        self.check_game_recording_windows = Toplevel(self.gamewindows)
        self.check_game_recording_windows.protocol('WM_DELETE_WINDOW',self.exit_game_recording)

    def main(self,username="ee"):
        ws = self.gamewindows.winfo_screenwidth()
        hs = self.gamewindows.winfo_screenheight()
        w = 900
        h = 600
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.gamewindows.geometry("%dx%d+%d+%d" % (w,h,x,y))
        self.gamewindows.title("Python Guess Number Game (V3.0)")
        self.gamewindows.config(bg="#222")
        user_kit_lable = Label(self.gamewindows,width=30,height=10,relief='solid',bg="#222").place(x=5,y=5)
        # Label(self.gamewindows,width=)
        Label(self.gamewindows, text="亲爱哒~" + username,bg='#222',fg="#FFF",relief='flat').place(x=45, y=10)
        self.check_times = Button(self.gamewindows,text='点击查看时间',relief='solid',bg='#222',command=self.check_time_threading)
        self.check_times.place(x=70,y=60)
        self.check_game_recording_btn = Button(self.gamewindows,text="查看游戏记录",relief='solid',bg="#222",command=self.check_game_recording,font=("楷体",15))
        self.check_game_recording_btn.place(x=45,y=100)
        self.gamewindows.mainloop()


if "__main__" == __name__:
    L = Login()
    L.main()
