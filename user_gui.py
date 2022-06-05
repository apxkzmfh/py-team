#도서관리 프로그램

from tkinter import*
import tkinter.ttk
from tkinter import messagebox

import warnings
import numpy as np
import pandas as pd
import datetime
warnings.filterwarnings('ignore')

## 프레임 닫고싶은데..
## def frameexit(frame):
##    frame.grid_forget()


#회원

def Userwindow():       #메인 화면에서 회원을 눌렀을 때   
    def Usersearch():       #조회, 등록 버튼 중 조회를 눌렀을 때       
        def User_Show(event):   #treeview로 조회된 회원중 한명을 더블클릭 했을 때           
            def Change():   #회원 수정
                
                #getValue 여기도 있음(더블클릭한 treeview 값)
                #PHONE을 인덱스로 불러온 df_user 존재
                nonlocal df_user
                change_user = df_user.loc[getValue[2]]     #Treeview 더블클릭할 때 선택된 값
                change_phone = Uphone_value1.get() +'-' + Uphone_value2.get() + '-' + Uphone_value3.get()
                change_birth = year_text.get() + '.' + month_text.get() +'.' + day_text.get()
                change_mail = mail_text.get() + '@' + mail_combo.get()
                
                new_user = {"PHONE" : change_phone,
                        "NAME" : name_text.get(),
                        "BIRTH" : change_birth,
                        "GENDER" : gender_var.get(),
                        "MAIL" : change_mail,
                        "REG_DATE" :change_user['REG_DATE'],            #change_user를 이용해서 등록일, 탈퇴일, 빌린 책 개수, 탈퇴여부는 수정할 수 없게 함.
                        "OUT_DATE" :change_user['OUT_DATE'],
                        "RENT_CNT" :change_user['RENT_CNT'],
                        "DO_OUT" : change_user['DO_OUT']}
    
                df_user = df_user.reset_index()                   #변경된 전화번호 입력하기 위해 전화번호 인덱스 해제
                changeindex = df_user.index[df_user['PHONE'] == getValue[2]]
                
                df_user.loc[changeindex] = (new_user['PHONE'], new_user['NAME'], new_user['BIRTH'], new_user['GENDER'], new_user['MAIL'], new_user['REG_DATE'], new_user['OUT_DATE'],new_user['RENT_CNT'], new_user['DO_OUT'])

                df_user_notme = df_user
                df_user_notme = df_user_notme.drop(changeindex, inplace = False)        #선택했던 전화번호에 해당하는 행은 제외하고 비교하기 위해(선택한 회원의 전화번호는 안바뀔 수도 있으므로)
                
                
                if (df_user_notme['PHONE'] == new_user['PHONE']).any():
                    messagebox.showinfo("회원 수정 실패", "이미 등록된 회원입니다.")
                else:
                    df_user.to_csv("USER1.csv", index = False, encoding= 'UTF-8-sig')
                
            def Delete():   #회원 삭제
                #getValue 여기도 있음(더블클릭한 treeview 값)
                #상위 함수에 PHONE을 인덱스로 불러온 df_user 존재
                nonlocal df_user

                now = datetime.datetime.now()
                change_phone = Uphone_value1.get() +'-' + Uphone_value2.get() + '-' + Uphone_value3.get()
                change_birth = year_text.get() + '.' + month_text.get() +'.' + day_text.get()
                change_mail = mail_text.get() + '@' + mail_combo.get()
                
                if df_user.loc[getValue[2]]["RENT_CNT"] > 0 :
                    messagebox.showinfo("회원 삭제 실패", "도서 대출 중인 회원 입니다.")
                    return
                if (df_user.index != change_phone).all() or (df_user["NAME"] != name_text.get()).all() or (df_user["BIRTH"] != change_birth).all() or (df_user["GENDER"] != gender_var.get()).all() or (df_user["MAIL"] != change_mail).all():
                    messagebox.showinfo("회원 삭제 실패", "등록된 회원이 아닙니다.")
                    return
                
                df_user.loc[getValue[2],'OUT_DATE'] = now.strftime("%Y-%m-%d")
                df_user.loc[getValue[2],"DO_OUT"] = 1
                
                df_user = df_user.reset_index()
                
                df_user.to_csv("USER1.csv", index = False, encoding= 'UTF-8-sig')

            #조회된 회원 더블클릭했을 때
            selectedItem = Utreeview.focus()
            getValue = Utreeview.item(selectedItem).get('values')
            
            user_show = Toplevel()
            user_show.geometry("600x400")
            user_show.configure(background = "white")
            user_show.title("회원 정보 - " + getValue[0] + "/" + getValue[1] + "/" + getValue[2])
            
            name_label = Label(user_show, text = "이름 : ", font = ("맑은 고딕", 12), fg = "#203864", bg = "white")
            name_label.grid(row = 0, column = 0, pady =10)
            
            name_text = Entry(user_show)
            name_text.insert(0, getValue[0])
            name_text.grid(row=0,column=1, pady =10)

            #생년월일
            birth_label = Label(user_show, text = "생년월일 : ", font = ("맑은 고딕", 12), fg = "#203864", bg = "white")
            birth_label.grid(row = 1, column = 0, pady =10)
            #생년월일 년, 월, 일로 구분
            birth_value = getValue[1].split('.')
            
            year_list = list(range(1970,2011))
            year_text = tkinter.ttk.Combobox(user_show)
            year_text.config(height=5, width = 10, values = year_list)
            year_text.set(birth_value[0])
            년_label = Label(user_show, text='년', font = ("맑은 고딕", 12), fg = "#203864", bg = "white")
            
            month_list = list(range(1,13))
            month_text = tkinter.ttk.Combobox(user_show)
            month_text.config(height=5, width = 4, values = month_list)
            month_text.set(birth_value[1])
            월_label = Label(user_show, text='월', font = ("맑은 고딕", 12), fg = "#203864", bg = "white")

            day_list = list(range(1,32))
            day_text = tkinter.ttk.Combobox(user_show)
            day_text.config(height=5, width = 4, values = day_list)
            day_text.set(birth_value[2])
            일_label = Label(user_show, text='일', font = ("맑은 고딕", 12), fg = "#203864", bg = "white")
            
            year_text.grid(row=1,column=1, pady =10)
            년_label.place(x = 210, y = 55)
            month_text.place(x = 240, y = 60)
            월_label.place(x=300, y = 55)
            day_text.place(x = 330, y = 60)
            일_label.place(x = 390, y = 55)

            #전화번호
            phone_value = getValue[2].split('-')
            
            phone_label = Label(user_show, text = "전화번호 : ", font = ("맑은 고딕", 12), fg = "#203864", bg = "white")

            Uphone_value1 = Entry(user_show, width = 5)
            Uphone_value1.insert(0, phone_value[0])
            line_text1 = Label(user_show, text='-', fg = "#203864", bg = "white")

            Uphone_value2 = Entry(user_show, width = 5)
            Uphone_value2.insert(0, phone_value[1])
            line_text2 = Label(user_show, text='-', fg = "#203864", bg = "white")
                                 
            Uphone_value3 = Entry(user_show, width = 5)
            Uphone_value3.insert(0, phone_value[2])

            phone_label.grid(row = 2, column = 0, pady =10)
            Uphone_value1.place(x = 100, y = 110)
            line_text1.place(x = 140, y = 110)
            Uphone_value2.place(x = 155, y = 110)
            line_text2.place(x = 195, y = 110)
            Uphone_value3.place( x = 210, y = 110)
            
            #성별
            gender_label = Label(user_show, text = "성별 : ", font = ("맑은 고딕", 12), fg = "#203864", bg = "white")
            gender_label.grid(row = 3, column = 0, pady =10)
            gender_var = IntVar()
            b_man = Radiobutton(user_show, font = ("맑은 고딕", 10), fg = "#203864", bg = "white", text='남자', value = 1, variable = gender_var)
            b_woman = Radiobutton(user_show, font = ("맑은 고딕", 10), fg = "#203864", bg = "white", text='여자', value = 0, variable = gender_var)
            if getValue[3] == "남자" :
                b_man.select()
            else:
                b_woman.select()
            b_man.place(x = 100, y = 150)
            b_woman.place(x = 150, y = 150)
            
            mail_label = Label(user_show, text = "이메일 : ", font = ("맑은 고딕", 12), fg = "#203864", bg = "white")
            mail_label.grid(row = 4, column = 0, pady =10)

            #이메일 아이디 입력
            mail_value = getValue[4].split('@')     #@를 기준으로 아이디와 이메일주소 분리
            
            mail_text = Entry(user_show)
            mail_text.insert(0, mail_value[0])
            mail_text.grid(row=4,column=1, pady =10)
            #골뱅이는 자동 입력
            골뱅이_label = Label(user_show, text = "@", font = ("맑은 고딕", 12), fg = "#203864", bg = "white", width = 1)
            골뱅이_label.grid(row = 4, column = 2, pady = 10)
            
            #이메일 콤보박스
            mail_list = ["naver.com", "hanmail.net", "hotmail.com", "nate.com", "yahoo.co.kr", "gmail.com", "empas.com", "dreamwiz.com"]
            mail_combo = tkinter.ttk.Combobox(user_show)
            mail_combo.config(height=5, values = mail_list, state="readonly")
            mail_combo.set(mail_value[1])
            mail_combo.grid(row=4,column=3, pady =10)

            #전화번호로 df_user에 인덱스 찾고 거기에 해당하는 대출여부, 탈퇴여부 가져와서 Entry에 insert 해야함 - 해결
            
            rent_check_label = Label(user_show, text = "대출여부", font =("맑은 고딕", 12), fg = "#203864", bg = "white")
            rent_check_label.grid(row = 5, column = 0, pady = 10)
            out_check_label = Label(user_show, text = "탈퇴여부", font =("맑은 고딕", 12), fg = "#203864", bg = "white")
            out_check_label.grid(row = 5, column = 2, pady = 10)
            out_check_text = Entry(user_show)
            rent_check_text = Entry(user_show)

            df_user = pd.read_csv('USER1.csv', encoding = 'UTF-8', index_col = 'PHONE')         #PHONE을 인덱스로 불러와서 비교
            if df_user.loc[getValue[2]]['RENT_CNT'] == 0 :
                rent_check_text.insert(0, '도서대출 중이 아님')
            else :
                rent_check_text.insert(0, '도서대출 중')

            if df_user.loc[getValue[2]]['DO_OUT'] == 0 :
                out_check_text.insert(0, 'X')
            else :
                out_check_text.insert(0, 'O')
            rent_check_text.configure(state='disabled')
            out_check_text.configure(state='disabled')
            rent_check_text.grid(row = 5, column = 1, pady = 10)
            out_check_text.grid(row = 5, column = 3, pady = 10)

            change_btn = Button(user_show, text = "수정", command = Change)
            change_btn.grid(row = 6, column = 0, pady = 10)

            delete_btn = Button(user_show, text = "삭제", command = Delete)
            delete_btn.grid(row = 6, column = 1, pady = 10)

        def Searched_user():    #이름, 연락처 검색했을 때
            Utreeview.delete(*Utreeview.get_children()) #Utreeview의 모든 값들 제거
            
            for i in range(len(df_user)):               #이름, 연락처 검색한 것만 다시 조회
                if (Uname_text.get() in list_from_df_user[i][0]) & (sear_Uphone.get() in list_from_df_user[i][2]) :
                    Utreeview.insert("", "end", text = "", values=list_from_df_user[i], iid = i)
            Utreeview.bind("<Double-1>",User_Show)
                    
        #조회, 등록 중 조회 눌렀을 때
        user_info = Frame(User_window, borderwidth = 1, relief = "solid")
        user_info.place(x = 30, y = 120)
        user_info.configure(background = "white")
        usearch_label = Label(user_info, text = "회원 조회", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        usearch_label.grid(row = 0, column = 1, padx = 80, pady = 10)
        ## X_btn = Button(user_info, image = X, bd = 0, bg = "white", command = lambda:frameexit(user_info))
        ## X_btn.grid(row = 0, column = 2)

        Uname_label = Label(user_info, text = "이름 : ", fg = "#203864", bg = "white")
        Uname_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        Uname_text = Entry(user_info, width = 50)
        Uname_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        Uphone_label = Label(user_info, text = "연락처 : ", fg = "#203864", bg = "white")
        Uphone_label.grid(row = 2, column = 0, padx = 10, pady = 5)
        sear_Uphone = Entry(user_info, width = 50)
        sear_Uphone.grid(row = 2, column = 1, padx = 10, pady = 5)
        usear_btn = Button(user_info, text = "조회", command = Searched_user)
        usear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)
        
        # 조회한 회원
        
        Utreeview = tkinter.ttk.Treeview(user_info,
                                         column = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check", "U_check_exit"],
                                         displaycolumns = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check", "U_check_exit"])

        Utreeview.grid(row = 3, column = 1)

        Utreeview.column("U_name", width=50, anchor="center")
        Utreeview.heading("U_name", text="이름", anchor="center")

        Utreeview.column("U_birth", width=70, anchor="center")
        Utreeview.heading("U_birth", text="생년월일", anchor="center")

        Utreeview.column("U_hp", width=100, anchor="center")
        Utreeview.heading("U_hp", text="전화번호", anchor="center")

        Utreeview.column("U_gender", width=35, anchor="center")
        Utreeview.heading("U_gender", text="성별", anchor="center")

        Utreeview.column("U_email", width=100, anchor="center")
        Utreeview.heading("U_email", text="메일", anchor="center")

        Utreeview.column("U_check", width=70, anchor="center")
        Utreeview.heading("U_check", text="대여개수", anchor="center")

        Utreeview.column("U_check_exit", width=70, anchor="center")
        Utreeview.heading("U_check_exit", text="탈퇴여부", anchor="center")
                          
        Utreeview["show"] = "headings"

        df_user = pd.read_csv('USER1.csv', encoding = 'UTF-8')
        list_from_df_user = df_user.values.tolist()
        
        for i in range(len(list_from_df_user)):
            if list_from_df_user[i][-1] == 0 :
                list_from_df_user[i][-1] = '탈퇴X'
            else :
                list_from_df_user[i][-1] = '탈퇴O'
            
        for i in range(len(df_user)):
            list_from_df_user[i] = list_from_df_user[i][1:3]+list_from_df_user[i][:1]+list_from_df_user[i][3:5]+list_from_df_user[i][7:]
            if list_from_df_user[i][3] == 1:
                list_from_df_user[i][3] = "남자"
            else:
                list_from_df_user[i][3] = "여자"
            Utreeview.insert("", "end", text = "", values=list_from_df_user[i], iid = i)
        Utreeview.bind("<Double-1>",User_Show)
            
    def Useradd():  #회원 등록(조회, 등록중 등록)
        existcheck = 0              #중복 체크 했는지 안했는지 확인용 변수(하면 1)
        
        def Add():
            if not Uname_text1.get() :
                messagebox.showinfo("입력 오류", "이름을 입력하시오")
                return
            if not Uphone_text1.get() or not Uphone_text2.get() or not Uphone_text3.get() :
                messagebox.showinfo("입력 오류", "번호를 입력하시오")
                return
            if not Uemail_text.get() :
                messagebox.showinfo("입력 오류", "이메일을 입력하시오")
                return
            df_user = pd.read_csv('USER1.csv', encoding = 'UTF-8')
            Uphone = Uphone_text1.get() +'-' + Uphone_text2.get() + '-' +Uphone_text3.get()
            Ubirth = year_combo.get() + '.' + month_combo.get() +'.' + day_combo.get()
            Umail = Uemail_text.get() + '@' + mail_combo.get()
            
            now = datetime.datetime.now()
            new_user = {"PHONE" : Uphone,
                    "NAME" : Uname_text1.get(),
                    "BIRTH" : Ubirth,
                    "GENDER" : Ugender_var.get(),
                    "MAIL" : Umail,
                    "REG_DATE" :now.strftime("%Y-%m-%d"),
                    "OUT_DATE" : '',
                    "RENT_CNT" : 0,
                    "DO_OUT" : 0}
            if existcheck == 0:
                messagebox.showinfo("입력 오류", "중복 확인 하십시오")
                return
            
            if (df_user['PHONE']==new_user['PHONE']).any():
                messagebox.showinfo("회원 중복 확인", "이미 등록된 회원입니다.")
            else:  
                df_user = df_user.append(new_user, ignore_index=True)

                df_user = df_user.set_index(df_user['PHONE'])
                
                df_user.to_csv("USER1.csv", index = False, encoding= 'UTF-8-sig')
        def Exist_check():  #중복 체크
            nonlocal existcheck         #상위 함수에 있는 중복 확인 체크용 변수
            
            df_user = pd.read_csv('USER1.csv', encoding = 'UTF-8')
            Uphone = Uphone_text1.get() +'-' + Uphone_text2.get() + '-' + Uphone_text3.get()
  
    
            if (df_user['PHONE'] == Uphone).any() :
                messagebox.showinfo("중복된 전화번호", "이미 등록된 회원입니다.")
            else :
                messagebox.showinfo("중복 확인 완료", "등록할 수 있는 회원입니다.")
                Uphone_text1.configure(state='disabled')
                Uphone_text2.configure(state='disabled')
                Uphone_text3.configure(state='disabled')
                existcheck = 1
        #조회, 등록중 등록 눌렀을 때
        user_add = Frame(User_window, borderwidth = 1, relief = "solid")
        user_add.configure(width = 640, background = "white")
        user_add.place(x = 30, y = 120)

        uadd_label = Label(user_add, text = "회원 등록", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        uadd_label.grid(row = 0, column = 1, pady = 10)

        
        Uname_add = Label(user_add, text="이름 : ", fg = "#203864", bg = "white")
        Uname_add.grid(row=1, column=0, padx = 10, pady = 5)
        Uname_text1 = Entry(user_add, width = 15) 
        Uname_text1.grid(row=1, column=1, padx=50, pady = 5)
        
        #frame 크기를 키우기 위한 None_label
        None_label = Label(user_add, text='',width = 30, bg = "white")
        None_label.grid(row=1, column=2, pady = 5)

        #생년월일
        Ubirth_add = Label(user_add, text="생년월일 : ", fg = "#203864", bg = "white")
        year_list = list(range(1990,2011))
        year_combo = tkinter.ttk.Combobox(user_add)
        year_combo.config(height=5, width = 10, values = year_list)
        year_combo.set(year_list[0])
        년_label = Label(user_add, text="년", fg = "#203864", bg = "white")

        month_list = list(range(1,13))
        month_combo = tkinter.ttk.Combobox(user_add)
        month_combo.config(height=5, width = 4, values = month_list)
        month_combo.set(month_list[0])
        월_label = Label(user_add, text="월", fg = "#203864", bg = "white")
        
        day_list = list(range(1,32))
        day_combo = tkinter.ttk.Combobox(user_add)
        day_combo.config(height=5, width = 4, values = day_list)
        day_combo.set(day_list[0])
        일_label = Label(user_add, text="일", fg = "#203864", bg = "white")
        
        Ubirth_add.grid(row=2, column=0, pady = 5)
        year_combo.grid(row=2, column=1, pady = 5)
        년_label.place(x=240, y = 100)
        month_combo.place(x=260, y = 100)
        월_label.place(x=315, y = 100)
        day_combo.place(x=335, y = 100)
        일_label.place(x=390, y = 100)
        
        #전화번호        
        Uphone_add = Label(user_add, text="전화번호 : ", fg = "#203864", bg = "white")
        Uphone_text1 = Entry(user_add, width = 5)
        line_label1 = Label(user_add, text='-', fg = "#203864", bg = "white")
        Uphone_text2 = Entry(user_add, width = 5)
        line_label2 = Label(user_add, text='-', fg = "#203864", bg = "white")
        Uphone_text3 = Entry(user_add, width = 5)

        Uphone_add.grid(row=3, column=0, padx=10, pady = 5)
        Uphone_text1.place(x = 135, y = 130)
        line_label1.place(x = 175, y = 130)
        Uphone_text2.place(x = 185, y = 130)
        line_label2.place(x = 225, y = 130)
        Uphone_text3.place(x = 235, y = 130)

        #중복확인
        Uphone_check_btn = Button(user_add, fg = "#203864", bg = "white", text="중복확인", command = Exist_check)
        Uphone_check_btn.grid(row=3, column=2, padx=20, pady = 5)

        #성별
        Ugender_label = Label(user_add, text="성별 : ", fg = "#203864", bg = "white")
        Ugender_var = IntVar()
        btn_man = Radiobutton(user_add, text='남자', value = 1, variable = Ugender_var)
        btn_man.select()
        btn_woman = Radiobutton(user_add, text='여자', value = 0, variable = Ugender_var)
        
        Ugender_label.grid(row=4, column=0, padx=10, pady = 5)
        btn_man.place(x = 135, y = 160)
        btn_woman.place(x = 185, y = 160)

        #이메일
        Uemail_label = Label(user_add, text="이메일 : ", fg = "#203864", bg = "white")
        Uemail_text = Entry(user_add, width = 15)
        골뱅이_label = Label(user_add, text='@', fg = "#203864", bg = "white")
        mail_list = ["naver.com", "hanmail.net", "hotmail.com", "nate.com", "yahoo.co.kr", "gmail.com", "empas.com", "dreamwiz.com"]
        mail_combo = tkinter.ttk.Combobox(user_add)
        mail_combo.config(height=5, values = mail_list, state="readonly")
        mail_combo.set(mail_list[0])
            
        Uemail_label.grid(row=5, column=0, padx=10, pady = 5)
        Uemail_text.grid(row=5, column=1, padx=50, pady = 5)
        골뱅이_label.place(x=250, y = 200)
        mail_combo.place(x=270, y = 200)
        
        #사진 찾기
        Upicture_search_btn = Button(user_add, fg = "#203864", bg = "white", text="찾기")
        Upicture_search_btn.grid(row=6, column=7, padx=20, pady = 5)

        user_add_btn = Button(user_add, fg = "#203864", bg = "white", text= "등록", command = Add)
        user_add_btn.grid(row = 7, column = 7, padx = 20, pady = 20)

    #유저 윈도우 - 조회, 등록 버튼 중 클릭 (조회에서 수정, 삭제 가능)   
    User_window = Toplevel(window)
    User_window.geometry("700x500")

    user_wall_label = Label(User_window, image = user_wall)
    user_wall_label.place(x = -100, y = -2)

    user_menu = Frame(User_window, height = 30, bd = 0)
    user_menu.place(x = 0, y = 65)

    user_btn = Button(user_menu, text = "조회", width = 34, font = ("맑은 고딕", 13), fg = "#203864", bg = "white", command = Usersearch)
    user_btn1 = Button(user_menu, text = "등록", width = 34, font = ("맑은 고딕", 13), fg = "#203864", bg = "white", command = Useradd)
    
    user_btn.grid(row = 0, column = 0)
    user_btn1.grid(row = 0, column = 1)

#도서
def Bookwindow():
    def Booksearch():
        book_info = Frame(Book_window, borderwidth = 1, relief = "solid")
        book_info.place(x = 30, y = 120)
        book_info.configure(background = "white")
        # font 한글도 가능한건가...
        bsearch_label = Label(book_info, text = "도서 조회", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        bsearch_label.grid(row = 0, column = 1, padx = 80, pady = 10)
        ## X_btn = Button(user_info, image = X, bd = 0, bg = "white", command = lambda:frameexit(user_info))
        ## X_btn.grid(row = 0, column = 2)


        Bname_label = Label(book_info, text = "도서명 : ", fg = "#203864", bg = "white")
        Bname_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        Bname_text = Entry(book_info, width = 50)
        Bname_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        Bauthor_label = Label(book_info, text = "저자 : ", fg = "#203864", bg = "white")
        Bauthor_label.grid(row = 2, column = 0, padx = 10, pady = 5)
        sear_Bauthor = Entry(book_info, width = 50)
        sear_Bauthor.grid(row = 2, column = 1, padx = 10, pady = 5)
        bsear_btn = Button(book_info, text = "조회")
        bsear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)
        
        # 조회한 도서
        Btreeview = tkinter.ttk.Treeview(book_info,
                                         column = ["B_ISBN", "B_name", "B_author", "B_price", "B_URL", "B_check_rent"],
                                         displaycolumns = ["B_ISBN", "B_name", "B_author", "B_price", "B_URL", "B_check_rent"])

        Btreeview.grid(row = 3, column = 1)

        Btreeview.column("B_ISBN", width=100, anchor="center")
        Btreeview.heading("B_ISBN", text="ISBN", anchor="center")

        Btreeview.column("B_name", width=100, anchor="center")
        Btreeview.heading("B_name", text="도서명", anchor="center")

        Btreeview.column("B_author", width=80, anchor="center")
        Btreeview.heading("B_author", text="저자", anchor="center")

        Btreeview.column("B_price", width=50, anchor="center")
        Btreeview.heading("B_price", text="가격", anchor="center")

        Btreeview.column("B_URL", width=100, anchor="center")
        Btreeview.heading("B_URL", text="정보 URL", anchor="center")

        Btreeview.column("B_check_rent", width=70, anchor="center")
        Btreeview.heading("B_check_rent", text="대출여부", anchor="center")

        Btreeview["show"] = "headings"

    def Bookadd():
        book_add = Frame(Book_window, borderwidth = 1, relief = "solid")
        book_add.place(x = 30, y = 120)
        book_add.configure(background = "white")
        
        badd_label = Label(book_add, text = "회원 등록", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        badd_label.grid(row = 0, column = 1, pady = 10)

        
        BISBN_add = Label(book_add, text="ISBN : ", fg = "#203864", bg = "white")
        BISBN_add.grid(row=1, column=0, padx = 10, pady = 5)
        BISBN_text1 = Entry(book_add, width = 50) 
        BISBN_text1.grid(row=1, column=1, padx=50, pady = 5)

        Bname_add = Label(book_add, text="도서명 : ", fg = "#203864", bg = "white")
        Bname_text = Entry(book_add, width = 50)
        Bname_add.grid(row=2, column=0, padx=10, pady = 5)
        Bname_text.grid(row=2, column=1, padx=50, pady = 5)

        Bname_check_btn = Button(book_add, text="중복확인")
        Bname_check_btn.grid(row=2, column=2, padx=20, pady = 5)

        Bauthor_add = Label(book_add, text="저자 : ", fg = "#203864", bg = "white")
        Bauthor_text = Entry(book_add, width = 50) 
        Bauthor_add.grid(row=3, column=0, padx=10, pady = 5)
        Bauthor_text.grid(row=3, column=1, padx=50, pady = 5)

        Bpubli_add = Label(book_add, text="출판사 : ", fg = "#203864", bg = "white")
        Bpubli_text = Entry(book_add, width = 50) 
        Bpubli_add.grid(row=4, column=0, padx=10, pady = 5)
        Bpubli_text.grid(row=4, column=1, padx=50, pady = 5)

        Bprice_label = Label(book_add, text="가격 : ", fg = "#203864", bg = "white")
        Bprice_text = Entry(book_add, width = 50) 
        Bprice_label.grid(row=5, column=0, padx=10, pady = 5)
        Bprice_text.grid(row=5, column=1, padx=50, pady = 5)

        BURL_label = Label(book_add, text="정보 URL : ", fg = "#203864", bg = "white")
        BURL_text = Entry(book_add, width = 50) 
        BURL_label.grid(row=6, column=0, padx=10, pady = 5)
        BURL_text.grid(row=6, column=1, padx=50, pady = 5)

        Bpicture_label = Label(book_add, text="사 진 : ", fg = "#203864", bg = "white") 
        Bpicture_text = Entry(book_add, width = 50) 
        Bpicture_label.grid(row=7, column=0, padx=10, pady = 5)
        Bpicture_text.grid(row=7, column=1, padx=50, pady = 5)
        
        Bpicture_search_btn = Button(book_add, text="찾기")
        Bpicture_search_btn.grid(row=7, column=2, padx=20, pady = 5)

        bser_add_btn = Button(book_add, text= "등록")
        bser_add_btn.grid(row = 8, column = 2, padx = 20, pady = 20)
    
    Book_window = Toplevel(window)
    Book_window.geometry("700x500")

    book_wall_label = Label(Book_window, image = user_wall)
    book_wall_label.place(x = -100, y = -2)

    book_menu = Frame(Book_window, height = 30, bd = 0)
    book_menu.place(x = 0, y = 65)

    book_btn = Button(book_menu, text = "조회", width = 34, font = ("맑은 고딕", 13), fg = "#203864", bg = "white", command = Booksearch)
    book_btn1 = Button(book_menu, text = "등록", width = 34, font = ("맑은 고딕", 13), fg = "#203864", bg = "white", command = Bookadd)
    
    book_btn.grid(row = 0, column = 0)
    book_btn1.grid(row = 0, column = 1)
    
def Rentwindow():
    def rent_book():
        brent_info = Frame(Rent_window, borderwidth = 1, relief = "solid")
        brent_info.place(x = 90, y = 120)
        brent_info.configure(background = "white")
        # font 한글도 가능한건가...
        brent_label = Label(brent_info, text = "대여(도서)", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        brent_label.grid(row = 0, column = 1, padx = 80, pady = 10)
        ## X_btn = Button(user_info, image = X, bd = 0, bg = "white", command = lambda:frameexit(user_info))
        ## X_btn.grid(row = 0, column = 2)

        Brent_name_label = Label(brent_info, text = "도서명 : ", fg = "#203864", bg = "white")
        Brent_name_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        Brent_name_text = Entry(brent_info, width = 50)
        Brent_name_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        bsear_btn = Button(brent_info, text = "조회")
        bsear_btn.grid(row = 1, column = 2, padx = 20, pady = 5)

        Brent_treeview = tkinter.ttk.Treeview(brent_info,
                                         column = ["BR_name", "BR_publi", "BR_state"],
                                         displaycolumns = ["BR_name", "BR_publi", "BR_state"])

        Brent_treeview.grid(row = 3, column = 1)
        # 저자가 있는게 나으려나
        Brent_treeview.column("BR_name", width=150, anchor="center")
        Brent_treeview.heading("BR_name", text="도서명", anchor="center")

        Brent_treeview.column("BR_publi", width=100, anchor="center")
        Brent_treeview.heading("BR_publi", text="출판사", anchor="center")

        Brent_treeview.column("BR_state", width=80, anchor="center")
        Brent_treeview.heading("BR_state", text="대출상태", anchor="center")

        Brent_treeview["show"] = "headings"

    def rent_user():
        Urent_info = Frame(Rent_window, borderwidth = 1, relief = "solid")
        Urent_info.place(x = 90, y = 120)
        Urent_info.configure(background = "white")
        # font 한글도 가능한건가...
        urent_label = Label(Urent_info, text = "대여(회원)", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        urent_label.grid(row = 0, column = 1, padx = 80, pady = 10)
        ## X_btn = Button(user_info, image = X, bd = 0, bg = "white", command = lambda:frameexit(user_info))
        ## X_btn.grid(row = 0, column = 2)

        Urent_name_label = Label(Urent_info, text = "회원명 : ", fg = "#203864", bg = "white")
        Urent_name_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        Urent_name_text = Entry(Urent_info, width = 50)
        Urent_name_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        usear_btn = Button(Urent_info, text = "조회")
        usear_btn.grid(row = 1, column = 2, padx = 20, pady = 5)

        # 맞추기 싫어....
        Urent_treeview = tkinter.ttk.Treeview(Urent_info,
                                         column = ["UR_name", "UR_birth", "UR_phone", "UR_gender", "UR_email", "UR_state"],
                                         displaycolumns = ["UR_name", "UR_birth", "UR_phone", "UR_gender", "UR_email", "UR_state"])

        Urent_treeview.grid(row = 3, column = 1)
        
        Urent_treeview.column("UR_name", width=80, anchor="center")
        Urent_treeview.heading("UR_name", text="이름", anchor="center")

        Urent_treeview.column("UR_birth", width=120, anchor="center")
        Urent_treeview.heading("UR_birth", text="생년월일", anchor="center")

        Urent_treeview.column("UR_phone", width=150, anchor="center")
        Urent_treeview.heading("UR_phone", text="전화번호", anchor="center")

        Urent_treeview.column("UR_gender", width=80, anchor="center")
        Urent_treeview.heading("UR_gender", text="성별", anchor="center")

        Urent_treeview.column("UR_email", width=120, anchor="center")
        Urent_treeview.heading("UR_email", text="이메일", anchor="center")

        Urent_treeview.column("UR_state", width=100, anchor="center")
        Urent_treeview.heading("UR_state", text="대출상태", anchor="center")

        Urent_treeview["show"] = "headings"

    def rent_return():
        rent_info = Frame(Rent_window, borderwidth = 1, relief = "solid")
        rent_info.place(x = 30, y = 120)
        rent_info.configure(background = "white")
        # font 한글도 가능한건가...
        rent_label = Label(rent_info, text = "조회 / 반납", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        rent_label.grid(row = 0, column = 1, padx = 80, pady = 10)

        rent_bname_label = Label(rent_info, text = "도서명 : ", fg = "#203864", bg = "white")
        rent_bname_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        rent_bname_text = Entry(rent_info, width = 50)
        rent_bname_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        rent_uname_label = Label(rent_info, text = "회원명 : ", fg = "#203864", bg = "white")
        rent_uname_label.grid(row = 2, column = 0, padx = 10, pady = 5)
        rent_uname_text = Entry(rent_info, width = 50)
        rent_uname_text.grid(row = 2, column = 1, padx = 10, pady = 5)
        rsear_btn = Button(rent_info, text = "조회")
        rsear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)

        rent_treeview = tkinter.ttk.Treeview(rent_info,
                                         column = ["R_uname", "R_bname", "R_rentday", "R_returnday", "R_rent_check"],
                                         displaycolumns = ["R_uname", "R_bname", "R_rentday", "R_returnday", "R_rent_check"])

        rent_treeview.grid(row = 3, column = 1)
        
        rent_treeview.column("R_uname", width=120, anchor="center")
        rent_treeview.heading("R_uname", text="도서명", anchor="center")

        rent_treeview.column("R_bname", width=80, anchor="center")
        rent_treeview.heading("R_bname", text="회원명", anchor="center")

        rent_treeview.column("R_rentday", width=100, anchor="center")
        rent_treeview.heading("R_rentday", text="대출일", anchor="center")

        rent_treeview.column("R_returnday", width=100, anchor="center")
        rent_treeview.heading("R_returnday", text="반납예정일", anchor="center")

        rent_treeview.column("R_rent_check", width=80, anchor="center")
        rent_treeview.heading("R_rent_check", text="반납여부", anchor="center")

        rent_treeview["show"] = "headings"
    
    Rent_window = Toplevel(window)
    Rent_window.geometry("700x500")

    rent_wall_label = Label(Rent_window, image = user_wall)
    rent_wall_label.place(x = -100, y = -2)

    rent_menu = Frame(Rent_window, height = 30, bd = 0)
    rent_menu.place(x = 0, y = 65)

    rent_btn = Button(rent_menu, text = "대여(도서)", width = 25, font = ("맑은 고딕", 12), fg = "#203864", bg = "white", command = rent_book)
    rent_btn1 = Button(rent_menu, text = "대여(회원)", width = 25, font = ("맑은 고딕", 12), fg = "#203864", bg = "white", command = rent_user)
    rent_btn2 = Button(rent_menu, text = "조회 / 반납", width = 25, font = ("맑은 고딕", 12), fg = "#203864", bg = "white", command = rent_return)
    
    rent_btn.grid(row = 0, column = 0)
    rent_btn1.grid(row = 0, column = 1)
    rent_btn2.grid(row = 0, column = 2)


## 메인

window = Tk()
window.geometry("700x500")

wall = PhotoImage(file = "메인 화면.png")
book = PhotoImage(file = "회원.png")
user = PhotoImage(file = "책.png")
rent = PhotoImage(file = "대여.png")

user_wall = PhotoImage(file = "기본 배경.png")

## 색 조합 봐달라고 하자...

wall_label = Label(window, image = wall)
wall_label.place(x = -2, y = -2)

button_menu = Frame(window)
button_menu.place(x = 40, y = 200)

btn = Button(button_menu, image = book, bd = 1, bg="gray", command = Userwindow)
btn1 = Button(button_menu, image = user, bd = 1, bg="gray", command = Bookwindow)
btn2 = Button(button_menu, image = rent, bd = 1, bg="gray", command = Rentwindow)

btn.config(width = 200, height = 200)
btn1.config(width = 200, height = 200)
btn2.config(width = 200, height = 200)

btn.grid(row = 0, column = 1)
btn1.grid(row = 0, column = 2)
btn2.grid(row = 0, column = 3) 


window.mainloop()
