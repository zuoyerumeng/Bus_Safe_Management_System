import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import pymysql
import pandas as pd
from tkinter import ttk

close=[0] # 程序终止标志
return_flag=[0]
user=["",0] # 用户身份
option_list=[""] # 功能选择列表

def clear(window): # 清空当前窗口所有内容
    def all_children (window): # 获取窗口的所有组件
        _list = window.winfo_children()
        for item in _list:
            if item.winfo_children() :
                _list.extend(item.winfo_children())
        return _list

    widget_list = all_children(window)
    for item in widget_list:
        item.pack_forget()

        
def login(): # 登录界面
    def check(): # 判断账号与密码是否正确
        username = username_entry.get()
        password = password_entry.get()
        if username == "1" and password == "leader":
            user[0]="leader"
            user[1]="1"
            succ_msg=tk.Label(login_window, text="登录成功！")
            succ_msg.pack()
            login_window.destroy()
        elif username == "3" and password == "routeleader":
            user[0]="route_leader"
            user[1]="3"
            succ_msg=tk.Label(login_window, text="登录成功！")
            succ_msg.pack
            login_window.destroy()
        elif username == "5" and password == "driver":
            user[0]="driver"
            user[1]="5"
            succ_msg=tk.Label(login_window, text="登录成功！")
            succ_msg.pack()
            login_window.destroy()
        else:
            if not fail[0]:
                fail_msg=tk.Label(login_window, text="登录失败，账号或密码错误！请重新输入。")
                fail_msg.pack()
                fail[0]=1
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)  

    def on_closing(): # 按下右上角关闭键时程序终止
        close[0]=1
        login_window.destroy()
        
    login_window = tk.Tk()
    fail=[0,1]
    image = tk.PhotoImage(file = r'公交汽车车队.png')
    label_img = tk.Label(image = image)
    label_img.pack()
    login_window.title("登录界面")
    welcome_label = tk.Label(login_window, text="您好，欢迎进入公交安全管理系统！请先登录。")
    welcome_label.pack()
    username_label = tk.Label(login_window, text="工号：")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.insert(tk.END, "")
    username_entry.pack()
    password_label = tk.Label(login_window, text="密码：")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.insert(tk.END, "")
    password_entry.pack()
    login_button = tk.Button(login_window, text="登录", command=check)
    login_button.pack()
    login_window.protocol("WM_DELETE_WINDOW", on_closing)
    login_window.mainloop()


def option(options:list, instruction:str)->int: # 选择功能按钮
    def show_message(option):
        option_list[0]=option
        option_window.destroy()

    def on_closing(): # 按下右上角关闭键时程序终止
        close[0]=1
        option_window.destroy()

    option_window=tk.Tk()
    option_window.title("功能选择界面")
    # 设置功能按钮
    option_type=[0]
    message_label = tk.Label(option_window, text=instruction)
    message_label.pack()
    buttons = []
    for option in options:
        button = tk.Button(option_window, text=option, command=lambda text=option: show_message(text))
        button.pack()
        buttons.append(button)
    option_window.protocol("WM_DELETE_WINDOW", on_closing)
    option_window.mainloop()    
    return option_type


def get_inputs(input_list:list, instruction:str, raw_inputs:list)->list: # 生成可视化的输入框UI界面并接收输入信息
    def get_inputs_core():
        for i,entry in enumerate(entries):
            if entry.get(): 
                input=entry.get()
                inputs[i]=input
        input_window.destroy()
    
    def return_options():
        return_flag[0]=1
        input_window.destroy()
        
    def on_closing(): # 按下右上角关闭键时程序终止
        close[0]=1
        input_window.destroy()
    
    inputs = ["" for i in range(len(input_list))]
    input_window = tk.Tk()
    input_window.title("录入界面")
    image = tk.PhotoImage(file = r'公交汽车车队.png')
    label_img = tk.Label(image = image)
    label_img.pack()
    # 输入提示信息
    label = tk.Label(input_window, text=instruction)
    label.pack()
    num_inputs = len(input_list)
    entries = []
    for i in range(num_inputs):
        label_temp=tk.Label(text=input_list[i])
        label_temp.pack()
        entry = tk.Entry(input_window)
        entry.insert(tk.END, raw_inputs[i])
        entry.pack()
        # 设置输入框的宽度和高度
        entry.configure(font=("Arial", 12), width=50)
        entry.pack()
        entries.append(entry)
    enter_button = tk.Button(input_window, text="确定", command=get_inputs_core)
    enter_button.pack()
    return_button = tk.Button(input_window, text="返回", command=return_options)
    return_button.pack()
    input_window.protocol("WM_DELETE_WINDOW", on_closing)
    input_window.mainloop()
    if not inputs: inputs=["" for i in range(len(input_list))]
    return inputs

def permission_error(): # 提示无权限
    messagebox.showerror("权限错误","抱歉，您没有权限！")
    return 0

def exit(): # 选择继续或者退出
    def on_button_click(value):
        exit_window.destroy()
        if value == "退出":
            close[0]=1
        return
    
    def on_closing(): # 按下右上角关闭键时程序终止
        close[0]=1
        exit_window.destroy()
        
    exit_window = tk.Tk()
    exit_window.title("选择框示例")
    image = tk.PhotoImage(file = r'公交汽车车队.png')
    label_img = tk.Label(image = image)
    label_img.pack()
    label_exit = tk.Label(exit_window, text="请选择继续使用系统功能还是退出系统")
    label_exit.pack()
    button_frame = tk.Frame(exit_window)
    button_frame.pack()
    continue_button = tk.Button(button_frame, text="继续", command=lambda: on_button_click("继续"))
    continue_button.pack(side=tk.LEFT, padx=10)
    quit_button = tk.Button(button_frame, text="退出", command=lambda: on_button_click("退出"))
    quit_button.pack(side=tk.LEFT, padx=10)
    if close[0]: return
    exit_window.protocol("WM_DELETE_WINDOW", on_closing)
    exit_window.mainloop()
    

def option_loop():
    while True:
        option(["功能1：录入司机基本信息","功能2：录入汽车基本信息","功能3：录入司机的违章信息","功能4：查询某个车队下的司机基本信息","功能5：查询某名司机在某个时间段的违章详细信息","功能6：查询某个车队在某个时间段的违章统计信息"],"请在以下功能按钮中选择你想使用的功能，并点击对应的按钮：")
        if close[0]: return 
        # 连接数据库
        connection = pymysql.connect(
            host='localhost',  # 数据库主机名
            port=3306,               # 数据库端口号，默认为3306
            user='root',             # 数据库用户名
            passwd='jiang620160623', # 数据库密码
            db='bus',               # 数据库名称
            charset='utf8'           # 字符编码
        )
        option_type=int(option_list[0][2])
        inputs=["" for i in range(8)]
        while True:
            cursor = connection.cursor() # 创建游标对象
            permission=1 # 是否具有权限
            # 判断队长或路队长所管理的车队或线路编号
            if user[0]=="leader":
                cursor.execute("SELECT DISTINCT number_convoy FROM Convoy WHERE number_job_leader="+user[1]) # 队长管理的车队编号
                number_convoy=str(cursor.fetchall()[0][0])
            elif user[0]=="route_leader":
                if option_type in [4,6]:
                    permission_error()
                    break
                else: 
                    cursor.execute("SELECT DISTINCT number_route from Route WHERE number_job_routeleader="+user[1]) # 路队长管理的线路编号
                    number_route=str(cursor.fetchall()[0][0])
            else:
                if option_type!=5:
                    permission_error()
                    break

            if option_type<=3: # 录入功能
                if option_type==1: # 录入司机基本信息
                    inputs=get_inputs(["工号","线路编号","姓名","性别","年龄","电话号码","家庭住址"],"请录入司机的基本信息，包括工号、线路编号、姓名、性别、年龄、电话号码、家庭住址：",inputs[:7])
                    if close[0]: return
                    if return_flag[0]:
                        return_flag[0]=0
                        break
                    if user[0]=="leader":
                        cursor.execute("SELECT Convoy.number_convoy FROM Convoy, Route, Bus WHERE Convoy.number_convoy=Bus.number_convoy and Bus.number_route=Route.number_route and Route.number_route="+user[1])
                        result=cursor.fetchall()
                        if result:
                            if inputs[1]!=str(result[0][0]): 
                                permission=0
                        else: permission=0
                    else:
                        if inputs[1]!=number_route:
                            permission=0
                    sql="INSERT INTO Driver VALUES ("
                    string_index=[2,3,6]       

                elif option_type==2: # 录入汽车基本信息                 
                    inputs=get_inputs(["车牌号","车队编号","线路编号","座数","车型"],"请录入汽车的基本信息，包括车牌号、车队编号、线路编号、座数、车型：",inputs[:5])
                    if close[0]:return
                    if return_flag[0]:
                        return_flag[0]=0
                        break
                    if not((user[0]=="leader" and inputs[1]==number_convoy) or (user[0]=="route_leader" and inputs[2]==number_route)):
                        permission=0
                    sql="INSERT INTO Bus VALUES ("
                    string_index=[0,4]

                else: # 录入司机的违章信息
                    inputs=get_inputs(["司机工号","司机姓名","公交汽车车牌号","车队编号","线路编号","站点","时间","违章"],"请录入司机的违章信息，包括司机工号、车牌号、车队编号、站点、时间（YYYY-mm-dd HH:ii:ss格式）、违章：",inputs[:8])
                    if close[0]:return
                    if return_flag[0]:
                        return_flag[0]=0
                        break
                    if not((user[0]=="leader" and inputs[3]==number_convoy) or (user[0]=="route_leader" and inputs[4]==number_route)):
                        permission=0
                    sql="INSERT INTO Illegal VALUES ("
                    string_index=[1,2,5,6,7]
                
                for i,j in enumerate(inputs): 
                    if not j: sql+="'',"
                    elif i in string_index: sql+="'"+j+"'"+','
                    else: sql+=j+','
                sql=sql[:-1]+");"
                # if option_type==1: sql=sql[:-1]+"IF number_job NOT IN (SELECT number_job from leader)"
              
                try:
                    print(sql)
                    cursor.execute(sql) 
                    if not permission: 
                        permission_error()
                        connection.rollback()
                        continue
                    cursor.connection.commit()
                    messagebox.showinfo("录入成功","录入成功！")
                    cursor.close()
                    exit()
                    if close[0]: return
                    break
                except pymysql.Error as error:
                    connection.rollback()
                    messagebox.showerror("录入失败","录入失败！请检查你录入的信息是否符合数据要求，并重新录入。")
                
            else: # 查询功能
                if not inputs: inputs=[""]    
                cursor = connection.cursor() # 创建游标对象
                if option_type==4: # 查询某个车队下的司机基本信息
                    inputs=get_inputs(["车队编号"],"要查询某个车队下的司机基本信息，请先输入车队编号：",inputs[:1])
                    if close[0]:return
                    if return_flag[0]:
                        return_flag[0]=0
                        break
                    if inputs[0]!=number_convoy: 
                        permission=0
                    if permission:
                        sql="SELECT DISTINCT Driver.* FROM Driver, Route, Bus, Convoy WHERE Driver.number_route=Route.number_route and Route.number_route=Bus.number_route and Bus.number_convoy=Convoy.number_convoy and Convoy.number_convoy="+inputs[0]+";"
                        col=["工号","线路编号","姓名","性别","年龄","电话号码","家庭住址"]

                elif option_type==5: # 查询某名司机在某个时间段的违章详细信息
                    option(["工号","姓名"],"要查询某名司机在某个时间段的违章详细信息，请先选择通过司机的工号还是姓名查询：")
                    if close[0]: return 
                    inputs=get_inputs([option_list[0],"起始时间","结束时间"], "请输入要查询的司机的"+option_list[0]+"、时间段的起始时间和结束时间（YYYY-mm-dd HH:ii:ss格式）",inputs[:3])  
                    if close[0]: return
                    if return_flag[0]:
                        return_flag[0]=0
                        break
                    if option_list[0]=="工号": 
                        if user[0]=="leader": 
                            cursor.execute("SELECT DISTINCT Convoy.number_job_leader FROM Convoy, Bus, Driver WHERE Convoy.number_convoy=Bus.number_convoy and Bus.number_route=Driver.number_route and Driver.number_job="+inputs[0]+";")
                            result=cursor.fetchall()
                            if result: 
                                number_job=str(result[0][0])
                                if number_job!=user[1]: permission=0
                            else: permission=0
                            if permission: sql="SELECT DISTINCT * FROM Illegal WHERE number_convoy="+str(number_convoy)+" and number_job="+inputs[0]
                        elif user[0]=="route_leader": 
                            cursor.execute("SELECT DISTINCT Route.number_job_routeleader FROM Route, Driver WHERE Route.number_route=Driver.number_route and Driver.number_job="+inputs[0]+";")
                            result=cursor.fetchall()
                            if result:
                                number_job=str(result[0][0])
                                if number_job!=user[1]: permission=0  
                            else: permission=0                          
                            if permission: sql="SELECT DISTINCT * FROM Illegal WHERE number_route="+str(number_route)+" and number_job="+inputs[0]
                        else:
                            if user[1]!=inputs[0]: permission=0
                            else: sql="SELECT DISTINCT * FROM Illegal WHERE number_job="+inputs[0]
                            
                    else: 
                        if user[0]=="leader": 
                            cursor.execute("SELECT DISTINCT Convoy.number_job_leader FROM Convoy, Bus, Driver WHERE Convoy.number_convoy=Bus.number_convoy and Bus.number_route=Driver.number_route and Driver.name='"+inputs[0]+"';")
                            result=cursor.fetchall()
                            if result:
                                number_job=str(result[0][0])
                                if number_job!=user[1]: permission=0
                            else: permission=0
                            if permission: sql="SELECT DISTINCT * FROM Illegal WHERE number_convoy="+str(number_convoy)+" and name='"+inputs[0]+"'"
                        elif user[0]=="route_leader": 
                            cursor.execute("SELECT DISTINCT Route.number_job_routeleader FROM Route, Driver WHERE Route.number_route=Driver.number_route and Driver.name='"+inputs[0]+"';")
                            result=cursor.fetchall()
                            if result:
                                number_job=str(result[0][0])
                                if number_job!=user[1]: permission=0      
                            else: permission=0                      
                            if permission: sql="SELECT DISTINCT * FROM Illegal WHERE number_route="+str(number_route)+" and name='"+inputs[0]+"'"
                        else:
                            cursor.execute("SELECT DISTINCT name from Driver WHERE number_job="+user[1])
                            result=cursor.fetchall()
                            if result:
                                name=str(result[0][0])
                                if name!=inputs[0]: permission=0
                            else: permission=0
                            if permission: sql="SELECT DISTINCT * FROM Illegal WHERE name='"+inputs[0]+"'"
                    if permission: 
                        sql+=" AND time BETWEEN '"+inputs[1]+"' AND '"+inputs[2]+"';"
                        col=["司机工号","司机姓名","公交车辆车牌号","车队编号","线路编号","站点","时间","违章"]

                else: # 查询某个车队在某个时间段的违章统计信息
                    inputs=get_inputs(["车队编号","起始时间","结束时间"],"要查询某个车队在某个时间段的违章统计信息，请先输入车队编号、时间段的起始时间和结束时间（YYYY-mm-dd HH:ii:ss格式）：",inputs[:3])
                    if close[0]:return
                    if return_flag[0]:
                        return_flag[0]=0
                        break
                    if inputs[0]!=number_convoy:
                        permission=0
                    if permission:
                        if close[0]: return 
                        sql="SELECT COUNT(Illegal) AS '次数', Illegal AS '违章' FROM Illegal WHERE number_convoy="+inputs[0]+" AND time BETWEEN '"+inputs[1]+"' AND '"+inputs[2]+"' GROUP BY Illegal;"
                        col=["次数","违章"]
                
                if not permission: 
                    permission_error()
                    continue
                else:          
                    def on_closing(): # 按下右上角关闭键时程序终止
                        close_2[0]=1
                        result_window.destroy()
    
                    print(sql)
                    cursor.execute(sql)
                    close_2=[0]
                    data=cursor.fetchall()
                    result_df=pd.DataFrame(data=list(data), columns=col)
                    result_window = tk.Tk()
                    result_window.title("查询信息结果页面")
                    image = tk.PhotoImage(file = r'公交汽车车队.png')
                    label_img = tk.Label(image = image)
                    label_img.pack()
                    label_select=tk.Label(result_window, text="查询成功！查询信息结果如下：")
                    label_select.pack()
                    tree = ttk.Treeview(result_window)
                    tree["columns"] = tuple(result_df.columns)
                    for column in result_df.columns:
                        tree.heading(column, text=column)
                        tree.column(column, width=100)
                    for index, row in result_df.iterrows():
                        tree.insert("", tk.END, text=index, values=tuple(row))
                    tree.pack()
                    result_window.protocol("WM_DELETE_WINDOW", on_closing)
                    result_window.mainloop()
                    cursor.close()
                    if close_2[0]: exit()
                    if close[0]: return
                    break
                
def main():
    while True:
        login() # 登录
        if close[0]: return # 关闭界面
        option_loop()
        close[0]=0
    
        
if __name__ == "__main__":
    main()


