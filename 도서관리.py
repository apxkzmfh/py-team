#도서관리 프로그램
import re
from tkinter import*
import tkinter.ttk
from tkinter import messagebox

import warnings
import numpy as np
import pandas as pd
import datetime
warnings.filterwarnings('ignore')

## 회원

#회원 전화번호 입력할때 숫자 입력제한을 위한 함수
def PHONE_limit(Uphone_value1,Uphone_value2,Uphone_value3, user_show):      
    def Validate(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if CheckCharactersCount(value_if_allowed) and CheckAlphabet(text):
            return True;
        else:
            return False;
    vcmd = (user_show.register(Validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    Uphone_value1 = Entry(user_show, width = 5, validate = 'key', validatecommand = vcmd)   
    def CheckCharactersCount(value_if_allowed):
        if len(value_if_allowed) > 3:
            return False;
        else:
            return True
    def CheckAlphabet(text):
        condition = re.compile('[0-9]')      #알파벳만을 입력받기 위한 정규식
        isAlphabet = condition.match(text) #위에서 만든 정규식과 match하는 검사한 결과를 return 해준다
        
        if isAlphabet: # or value_if_allowed == "":
            return True
        else:
            return False
    #숫자 4개 입력제한
    def Validate2(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if CheckCharactersCount2(value_if_allowed) and CheckAlphabet2(text):
            return True;
        else:
            return False;
    vcmd = (user_show.register(Validate2), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    Uphone_value2 = Entry(user_show, width = 5, validate = 'key', validatecommand = vcmd)
    Uphone_value3 = Entry(user_show, width = 5, validate = 'key', validatecommand = vcmd)
    def CheckCharactersCount2(value_if_allowed):
        if len(value_if_allowed) > 4:
            return False;
        else:
            return True;
    def CheckAlphabet2(text):
        condition = re.compile('[0-9]')      #숫자만을 입력받기 위한 정규식
        isAlphabet = condition.match(text) #위에서 만든 정규식과 match하는 검사한 결과를 return 해준다
        
        if isAlphabet:
            return True
        else:
            return False
    return Uphone_value1, Uphone_value2, Uphone_value3

# 회원 UI
def Userwindow(): # 메인화면에서 회원 클릭
    def Usersearch(): # 회원 조회 클릭
        def User_Show(event):   #treeview로 조회된 회원중 한명을 더블클릭 했을 때           
            def Change():   #회원 수정
                #getValue 여기도 있음(더블클릭한 treeview 값)
                #PHONE을 인덱스로 불러온 df_user 존재
                nonlocal df_user
                change_user = df_user.loc[getValue[2]]     #Treeview 더블클릭할 때 선택된 값
                change_phone = Uphone_value1.get() +'-' + Uphone_value2.get() + '-' + Uphone_value3.get()
                change_birth = year_text.get() + '.' + month_text.get() +'.' + day_text.get()
                change_mail = mail_text.get() + '@' + mail_combo.get()
                if getValue[6] == '탈퇴O':
                    messagebox.showinfo("회원 수정 실패", "탈퇴한 회원은 수정할 수 없습니다.")
                    return
                try:
                    change_birth_check = datetime.datetime.strptime(change_birth, "%Y.%m.%d")
                except:
                    messagebox.showinfo("회원 수정 실패", "존재하지 않는 날짜 형식입니다.")
                    return
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
                elif not name_text.get() or len(name_text.get()) > 10 :
                    messagebox.showinfo("회원 수정 실패", "이름을 입력하시오(1~10자)")
                elif not Uphone_value1.get() or not Uphone_value2.get() or not Uphone_value3.get() :
                    messagebox.showinfo("회원 수정 실패", "번호를 입력하시오")
                elif not mail_text.get() or (len(mail_text.get() + mail_combo.get()) + 1) > 255:
                    messagebox.showinfo("회원 수정 실패", "이메일을 입력하시오")
                else:
                    df_user.to_csv("USER1.csv", index = False, encoding= 'UTF-8-sig')
                    user_show.destroy()
                    messagebox.showinfo("회원 수정 성공", "수정이 완료되었습니다.")
                    Usersearch()
                df_user = pd.read_csv('USER1.csv', encoding = 'UTF-8', index_col = 'PHONE')
                
            def Delete():   #회원 삭제
                #getValue 여기도 있음(더블클릭한 treeview 값)
                #상위 함수에 PHONE을 인덱스로 불러온 df_user 존재
                nonlocal df_user
                now = datetime.datetime.now()
                change_phone = Uphone_value1.get() +'-' + Uphone_value2.get() + '-' + Uphone_value3.get()
                change_birth = year_text.get() + '.' + month_text.get() +'.' + day_text.get()
                change_mail = mail_text.get() + '@' + mail_combo.get()

                if (df_user.index != change_phone).all() or (df_user["NAME"] != name_text.get()).all() or (df_user["BIRTH"] != change_birth).all() or (df_user["GENDER"] != gender_var.get()).all() or (df_user["MAIL"] != change_mail).all():
                    messagebox.showinfo("회원 삭제 실패", "등록된 회원이 아닙니다.")
                    return
                
                if df_user.loc[getValue[2]]["RENT_CNT"] > 0 :
                    messagebox.showinfo("회원 삭제 실패", "도서 대출 중인 회원 입니다.")
                    return
                
                if df_user.loc[getValue[2]]["DO_OUT"] == 1 :
                    messagebox.showinfo("회원 삭제 실패", "이미 탈퇴한 회원입니다.")
                    return
                df_user.loc[getValue[2],'OUT_DATE'] = now.strftime("%Y.%m.%d")
                df_user.loc[getValue[2],"DO_OUT"] = 1            
                df_user = df_user.reset_index()
                df_user.to_csv("USER1.csv", index = False, encoding= 'UTF-8-sig')
                user_show.destroy()
                Usersearch()

            #조회된 회원 더블클릭했을 때 회원 정보
            selectedItem = Utreeview.focus()
            getValue = Utreeview.item(selectedItem).get('values')
            
            user_show = Toplevel(User_window)
            # user_show.resizable(width = False, height = False)
            user_show.title("회원 정보 - " + getValue[0] + "/" + getValue[1] + "/" + getValue[2])

            user_show_label = Label(user_show, image = user_wall)
            user_show_label.pack()

            user_show_info = Frame(user_show)
            user_show_info.place(x = 100, y = 80)
            user_show_info.configure(background = "white")

            #이름
            name_label = Label(user_show_info, text = "이름 : ", fg = "#203864", bg = "white")
            name_label.grid(row = 2, column = 0, pady = 8)
        
            name_text = Entry(user_show_info)
            name_text.insert(0, getValue[0])
            name_text.grid(row = 2,column = 1, pady = 8)

            #생년월일
            birth_label = Label(user_show_info, text = "생년월일 : ", fg = "#203864", bg = "white")
            birth_label.grid(row = 3, column = 0, pady =8)
            
            #생년월일 년, 월, 일로 구분
            birth_value = getValue[1].split('.')
            
            year_list = list(range(1970,2011))
            year_text = tkinter.ttk.Combobox(user_show_info)
            year_text.config(height = 5, width = 10, values = year_list)
            year_text.set(birth_value[0])
            년_label = Label(user_show_info, text='년', fg = "#203864", bg = "white")
            
            month_list = list(range(1,13))
            month_text = tkinter.ttk.Combobox(user_show_info)
            month_text.config(height = 5, width = 4, values = month_list)
            month_text.set(birth_value[1])
            월_label = Label(user_show_info, text='월', fg = "#203864", bg = "white")

            day_list = list(range(1,32))
            day_text = tkinter.ttk.Combobox(user_show_info)
            day_text.config(height = 5, width = 4, values = day_list)
            day_text.set(birth_value[2])
            일_label = Label(user_show_info, text='일', fg = "#203864", bg = "white")
            
            year_text.grid(row = 3,column = 1, pady = 8)
            년_label.place(x = 200, y = 45)
            month_text.place(x = 240, y = 45)
            월_label.place(x = 300, y = 45)
            day_text.place(x = 330, y = 45)
            일_label.place(x = 390, y = 45)

            #전화번호
            phone_value = getValue[2].split('-')
            
            phone_label = Label(user_show_info, text = "전화번호 : ", fg = "#203864", bg = "white")

            Uphone_value1 = None
            Uphone_value2 = None
            Uphone_value3 = None
            
            Uphone_value1, Uphone_value2, Uphone_value3 = PHONE_limit(Uphone_value1,Uphone_value2,Uphone_value3, user_show)
            
            Uphone_value1.insert(0, phone_value[0])
            line_text1 = Label(user_show_info, text='-', fg = "#203864", bg = "white")


            Uphone_value2.insert(0, phone_value[1])
            line_text2 = Label(user_show_info, text='-', fg = "#203864", bg = "white")
                                 

            Uphone_value3.insert(0, phone_value[2])

            phone_label.grid(row = 4, column = 0, pady = 8)
            Uphone_value1.place(x = 185, y = 165)
            line_text1.place(x = 125, y = 80)
            Uphone_value2.place(x = 240, y = 165)
            line_text2.place(x = 180, y = 80)
            Uphone_value3.place( x = 295, y = 165)

            #성별
            gender_label = Label(user_show_info, text = "성별 : ", fg = "#203864", bg = "white")
            gender_label.grid(row = 5, column = 0, pady =8)
            gender_var = IntVar()
            b_man = Radiobutton(user_show_info, fg = "#203864", bg = "white", text='남자', value = 1, variable = gender_var)
            b_woman = Radiobutton(user_show_info, fg = "#203864", bg = "white", text='여자', value = 0, variable = gender_var)
            if getValue[3] == "남자" :
                b_man.select()
            else:
                b_woman.select()
            b_man.place(x = 90, y = 117)
            b_woman.place(x = 140, y = 117)

            # 이메일
            mail_label = Label(user_show_info, text = "이메일 : ", fg = "#203864", bg = "white")
            mail_label.grid(row = 6, column = 0, pady = 8)

            #이메일 아이디 입력
            mail_value = getValue[4].split('@')     #@를 기준으로 아이디와 이메일주소 분리
            
            mail_text = Entry(user_show_info)
            mail_text.insert(0, mail_value[0])
            mail_text.grid(row = 6,column = 1, pady = 8)
            #골뱅이는 자동 입력
            골뱅이_label = Label(user_show_info, text = "@", fg = "#203864", bg = "white", width = 1)
            골뱅이_label.grid(row = 6, column = 2, pady = 8)
            
            #이메일 콤보박스
            mail_list = ["naver.com", "hanmail.net", "hotmail.com", "nate.com", "yahoo.co.kr", "gmail.com", "empas.com", "dreamwiz.com"]
            mail_combo = tkinter.ttk.Combobox(user_show_info)
            mail_combo.config(height=5, values = mail_list, state="readonly")
            mail_combo.set(mail_value[1])
            mail_combo.grid(row = 6,column = 3, pady = 8)

            #전화번호로 df_user에 인덱스 찾고 거기에 해당하는 대출여부, 탈퇴여부 가져와서 Entry에 insert 해야함 - 해결
            rent_check_label = Label(user_show_info, text = "대출여부", fg = "#203864", bg = "white")
            rent_check_label.grid(row = 7, column = 0, pady = 5)
            out_check_label = Label(user_show_info, text = "탈퇴여부",  fg = "#203864", bg = "white")
            out_check_label.grid(row = 7, column = 2, pady = 5)
            out_check_text = Entry(user_show_info)
            rent_check_text = Entry(user_show_info)

            df_user = pd.read_csv('USER1.csv', encoding = 'UTF-8', index_col = 'PHONE')         #PHONE을 인덱스로 불러와서 비교
            if df_user.loc[getValue[2]]['RENT_CNT'] == 0 :
                rent_check_text.insert(0, '도서대출 중이 아님')
            else :
                rent_check_text.insert(0, '도서대출 중')

            if df_user.loc[getValue[2]]['DO_OUT'] == 0 :
                out_check_text.insert(0, 'X')
            else :
                out_check_text.insert(0, 'O')
            rent_check_text.configure(state='readonly')
            out_check_text.configure(state='readonly')
            rent_check_text.grid(row = 7, column = 1, pady = 5)
            out_check_text.grid(row = 7, column = 3, pady = 5)

            change_btn = Button(user_show_info, text = "수정", command = Change)
            change_btn.grid(row = 8, column = 2, pady = 10)

            delete_btn = Button(user_show_info, text = "삭제", command = Delete)
            delete_btn.grid(row = 8, column = 3, pady = 10)

        def Searched_user():    #이름, 연락처 검색했을 때
            Utreeview.delete(*Utreeview.get_children()) #Utreeview의 모든 값들 제거
            
            for i in range(len(df_user)):               #이름, 연락처 검색한 것만 다시 조회
                if (Uname_text.get() in list_from_df_user[i][0]) & (sear_Uphone.get() in list_from_df_user[i][2]) :
                    Utreeview.insert("", "end", text = "", values=list_from_df_user[i], iid = i)
            Utreeview.bind("<Double-1>",User_Show)


        #조회, 등록 중 조회 눌렀을 때
        global user_info                #조회창이랑 등록창이 이미 있을 때 닫음.
        try:
            user_add.destroy()
        except:
            pass
        try:
            user_info.destroy()
        except:
            pass
        user_info = Frame(User_window, borderwidth = 1, relief = "solid")
        user_info.place(x = 30, y = 120)
        user_info.configure(background = "white")
        usearch_label = Label(user_info, text = "회원 조회", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        usearch_label.grid(row = 0, column = 1, padx = 80, pady = 10)

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

        #조회한 회원
        Utreeview = tkinter.ttk.Treeview(user_info,
                                         column = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check_rent", "U_check_for_exit"],
                                         displaycolumns = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check_rent", "U_check_for_exit"],
                                         height = 7, show = 'headings')

        Utreeview.grid(row = 3, column = 1)

        Utreeview.column("U_name", width=60, anchor="center")
        Utreeview.heading("U_name", text="이름", anchor="center")

        Utreeview.column("U_birth", width=70, anchor="center")
        Utreeview.heading("U_birth", text="생년월일", anchor="center")

        Utreeview.column("U_hp", width=100, anchor="center")
        Utreeview.heading("U_hp", text="전화번호", anchor="center")

        Utreeview.column("U_gender", width=35, anchor="center")
        Utreeview.heading("U_gender", text="성별", anchor="center")

        Utreeview.column("U_email", width=100, anchor="center")
        Utreeview.heading("U_email", text="메일", anchor="center")

        Utreeview.column("U_check_rent", width=70, anchor="center")
        Utreeview.heading("U_check_rent", text="대출여부", anchor="center")

        Utreeview.column("U_check_for_exit", width=70, anchor="center")
        Utreeview.heading("U_check_for_exit", text="탈퇴여부", anchor="center")

        df_user = pd.read_csv('USER1.csv', encoding = 'UTF-8')
        list_from_df_user = df_user.values.tolist()
        
        try:
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
        except:
            messagebox.showinfo("조회 실패", "등록된 회원이 없습니다 -> 등록 화면으로 이동합니다.")
            Useradd()
        
        uexit_btn = Button(user_info, text = "닫기",command=lambda: user_info.destroy())
        uexit_btn.grid(row = 6, column = 2, padx = 20, pady = 5)
        
    def Useradd():  #회원 등록(조회, 등록중 등록)
        existcheck = 0              #중복 체크 했는지 안했는지 확인용 변수(하면 1)
        
        def Add():
            if not Uname_text1.get() or len(Uname_text1.get()) > 10:
                messagebox.showinfo("입력 오류", "이름을 입력하시오(1~10자)")
                return
            if not Uphone_text1.get() or not Uphone_text2.get() or not Uphone_text3.get() :
                messagebox.showinfo("입력 오류", "번호를 입력하시오")
                return
            if not Uemail_text.get() or (len(Uemail_text.get() + mail_combo.get()) + 1) > 255:
                messagebox.showinfo("입력 오류", "이메일을 입력하시오")
                return
            
            Uphone = Uphone_text1.get() +'-' + Uphone_text2.get() + '-' +Uphone_text3.get()
            Ubirth = year_combo.get() + '.' + month_combo.get() +'.' + day_combo.get()

            try:
                Ubirth_check = datetime.datetime.strptime(Ubirth, "%Y.%m.%d")
            except:
                messagebox.showinfo("입력 오류", "존재하지 않는 날짜 형식입니다.")
                return
            Umail = Uemail_text.get() + '@' + mail_combo.get()
            
            now = datetime.datetime.now()
            new_user = {"PHONE" : Uphone,
                    "NAME" : Uname_text1.get(),
                    "BIRTH" : Ubirth,
                    "GENDER" : Ugender_var.get(),
                    "MAIL" : Umail,
                    "REG_DATE" :now.strftime("%Y.%m.%d"),
                    "OUT_DATE" : '',
                    "RENT_CNT" : 0,
                    "DO_OUT" : 0}
            
            if existcheck == 0:
                messagebox.showinfo("입력 오류", "중복 확인 하십시오")
                return
            try:
                df_user = pd.read_csv('USER1.csv', encoding = 'UTF-8')
                add_index = df_user.index[df_user['PHONE'] == Uphone]
                if (df_user['PHONE'] == Uphone).any() :
                    df_user.loc[add_index] = (new_user['PHONE'], new_user['NAME'], new_user['BIRTH'], new_user['GENDER'], new_user['MAIL'], new_user['REG_DATE'], new_user['OUT_DATE'],new_user['RENT_CNT'], new_user['DO_OUT'])
                    messagebox.showinfo("회원 등록", "회원 재가입 성공")
                    df_user.to_csv("USER1.csv", index = False, encoding= 'UTF-8-sig')
                else :
                    df_user = df_user.append(new_user, ignore_index=True)
                    messagebox.showinfo("회원 등록", "회원 등록 성공")
                    df_user.to_csv("USER1.csv", index = False, encoding= 'UTF-8-sig')
            except:
                df_user = pd.DataFrame(new_user, index = [0])
                df_user.to_csv("USER1.csv", index =False, encoding = "UTF-8-sig")

        def Exist_check():  #중복 체크
            nonlocal existcheck         #상위 함수에 있는 중복 확인 체크용 변수
            try:
                df_user = pd.read_csv('USER1.csv', encoding = 'UTF-8')
                Uphone = Uphone_text1.get() +'-' + Uphone_text2.get() + '-' + Uphone_text3.get()
                
                if (df_user['PHONE'] == Uphone).any() :
                    readd_index = df_user.index[df_user['PHONE'] == Uphone]
                    if (df_user.loc[readd_index]['DO_OUT'] == 1).all():
                        existcheck = 1
                        messagebox.showinfo("중복 확인 완료", "탈퇴한 회원입니다.")           #회원 재가입 구현
                        Uphone_text1.configure(state='disabled')
                        Uphone_text2.configure(state='disabled')
                        Uphone_text3.configure(state='disabled')
                    else :
                        messagebox.showinfo("중복된 전화번호", "이미 등록된 회원입니다.")
                else :
                    if not Uphone_text1.get() or not Uphone_text2.get() or not Uphone_text3.get() :
                        messagebox.showinfo("중복 확인 실패", "번호를 입력하십시오")
                        return
                    else:
                        messagebox.showinfo("중복 확인 완료", "등록할 수 있는 회원입니다.")
                        Uphone_text1.configure(state='disabled')
                        Uphone_text2.configure(state='disabled')
                        Uphone_text3.configure(state='disabled')
                        existcheck = 1
            except:
                if not Uphone_text1.get() or not Uphone_text2.get() or not Uphone_text3.get() :
                    messagebox.showinfo("중복 확인 실패", "번호를 입력하십시오")
                    return
                else:
                    messagebox.showinfo("중복 확인 완료", "등록할 수 있는 회원입니다.")
                    Uphone_text1.configure(state='disabled')
                    Uphone_text2.configure(state='disabled')
                    Uphone_text3.configure(state='disabled')

        #조회, 등록중 등록 눌렀을 때
        global user_add                 #조회창이랑 등록창이 이미 있을 때 닫음.
        try:
            user_info.destroy()
        except:
            pass
        try:
            user_add.destroy()
        except:
            pass
        
        # 회원 등록 gui
        user_add = Frame(User_window, borderwidth = 1, relief = "solid")
        user_add.place(x = 35, y = 120)
        user_add.configure(width = 600, height = 1000, background = "white")
        uadd_label = Label(user_add, text = "회원 등록", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        uadd_label.grid(row = 0, column = 1, pady = 10)

        #이름
        Uname_add = Label(user_add, text="이름 : ", fg = "#203864", bg = "white")
        Uname_add.grid(row=1, column=0, padx = 10, pady = 5)
        Uname_text1 = Entry(user_add, width = 50) 
        Uname_text1.grid(row=1, column=1, padx=50, pady = 5)

        #frame 크기를 키우기 위한 None_label
        #None_label = Label(user_add, text='',width = 30, bg = "white")
        #None_label.grid(row=1, column=2, pady = 5)

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
        year_combo.place(x=133, y=100)
        년_label.place(x=230, y = 100)
        month_combo.place(x=260, y = 100)
        월_label.place(x=315, y = 100)
        day_combo.place(x=335, y = 100)
        일_label.place(x=390, y = 100)
        
        #전화번호        
        Uphone_add = Label(user_add, text="전화번호 : ", fg = "#203864", bg = "white")
        
        line_label1 = Label(user_add, text='-', fg = "#203864", bg = "white")
        line_label2 = Label(user_add, text='-', fg = "#203864", bg = "white")

        #숫자 입력제한
        Uphone_text1 = None
        Uphone_text2 = None
        Uphone_text3 = None
        
        Uphone_text1, Uphone_text2, Uphone_text3 = PHONE_limit(Uphone_text1,Uphone_text2,Uphone_text3, user_add)

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
        btn_man = Radiobutton(user_add, text='남자', value = 1, variable = Ugender_var, bg = "white")
        btn_man.select()
        btn_woman = Radiobutton(user_add, text='여자', value = 0, variable = Ugender_var, bg = "white")
        
        Ugender_label.grid(row=4, column=0, padx=10, pady = 5)
        btn_man.place(x = 135, y = 165)
        btn_woman.place(x = 185, y = 165)

        #이메일
        Uemail_label = Label(user_add, text="이메일 : ", fg = "#203864", bg = "white")
        Uemail_text = Entry(user_add, width = 15)
        골뱅이_label = Label(user_add, text='@', fg = "#203864", bg = "white")
        mail_list = ["naver.com", "hanmail.net", "hotmail.com", "nate.com", "yahoo.co.kr", "gmail.com", "empas.com", "dreamwiz.com"]
        mail_combo = tkinter.ttk.Combobox(user_add)
        mail_combo.config(height=5, values = mail_list, state="readonly")
        mail_combo.set(mail_list[0])
            
        Uemail_label.grid(row=5, column=0, padx=10, pady = 5)
        Uemail_text.place(x = 135, y =200)
        골뱅이_label.place(x=250, y = 200)
        mail_combo.place(x=270, y = 200)


        user_add_btn = Button(user_add, fg = "#203864", bg = "white", text= "등록", command = Add)
        user_add_btn.grid(row = 7, column = 1, padx = 10, pady = 20)

        user_exit_btn = Button(user_add, text= "닫기", fg = "#203864", bg = "white", command = lambda: user_add.destroy())
        user_exit_btn.grid(row = 7, column = 2, padx = 10, pady = 20)

    #유저 윈도우 - 조회, 등록 버튼 중 클릭 (조회에서 수정, 삭제 가능) 
    User_window = Toplevel(window)
    User_window.geometry("700x500")
    User_window.resizable(width = False, height = False)


    user_wall_label = Label(User_window, image = de_wall)
    user_wall_label.place(x = -100, y = -2)

    user_menu = Frame(User_window, height = 30, bd = 0)
    user_menu.place(x = 0, y = 65)

    user_btn = Button(user_menu, text = "회원 조회", width = 34, font = ("맑은 고딕", 13), fg = "#203864", bg = "white", command = Usersearch)
    user_btn1 = Button(user_menu, text = "회원 등록", width = 34, font = ("맑은 고딕", 13), fg = "#203864", bg = "white", command = Useradd)
    
    user_btn.grid(row = 0, column = 0)
    user_btn1.grid(row = 0, column = 1)
    
## 도서
df_book=pd.read_csv('bookcsv.csv', encoding='UTF-8')
book_list=np.array([])
book_list=np.append(book_list,df_book)
book_list=np.reshape(book_list,(int(book_list.size/8),8))
book_list=book_list[:,1:]
isbnlist = []

class Book: #도서 클래스
    
    def __init__(self,book): #생성자
        self.__book=book #self.__으로 private선언

    def save(self): # 변동사항 생길 때마다 저장
        book_col=["ISBN","TITLE","AUTHOR","PRICE","URL","PUB","RENT"] # 열 이름
        bookdf=pd.DataFrame(self.__book, columns=book_col) 
        bookdf.to_csv('bookcsv.csv', encoding='UTF-8') # to_csv작동을 위해 데이터프레임으로 변환

    def B_Info(self,n): # 도서 등록 
        self.__book=np.append(self.__book, n, axis=0)# 행 방향으로 정보 추가
        self.save()

    def check_book(self, book): #중복확인 함수
        if book in self.__book[:,1]:
            return True
        else:
            return False

    def check_isbn(self, isbn): #중복확인 함수
        if isbn in self.__book[:,0]:
            return True
        else:
            return False

    def search_booktitle(self,title): 
        slist = np.array([])
        find_ind = np.where(self.__book[:,1]==title)
        for i in find_ind:
            slist = np.append(slist,self.__book[i,:]) #도서명이 동일하면 리스트에 추가
        slist = np.reshape(slist,(int(slist.size/7),7))
        return slist

    def search_bookauthor(self,author):
        sslist = np.array([])
        find_ind = np.where(self.__book[:,2]==author)
        for i in find_ind:
            sslist=np.append(sslist,self.__book[i,:]) #저자가 동일하면 리스트에 추가
        sslist=np.reshape(sslist,(int(sslist.size/7),7))
        return sslist

    def rentbook(self, isbn): 
        find_ind = np.where(self.__book[:,0]==isbn)
        return self.__book[find_ind,6]

    def CB_book(self,isbn): # 도서 삭제
        find_ind = np.where(self.__book[:,0]==isbn)
        self.__book = np.delete(self.__book, find_ind, 0)
        self.save()
    
B=Book(book_list) #인스턴스 생성
def Bookwindow():
    def Booksearch(): #조회도 다 된듯..?
        def printbook(): #도서조회 함수
            sblist = np.array([])
            if Bname_text.get():
                sblist = B.search_booktitle(Bname_text.get()) #도서명 입력된 경우
            elif sear_Bauthor.get():
                sblist = B.search_bookauthor(sear_Bauthor.get()) #저자명 입력된 경우
            else:
                messagebox.showinfo("경고","도서명과 저자명 하나라도 입력해주세요.")
            Btreeview.delete(*Btreeview.get_children()) #다른거 조회하면 delete
            for i in range(int(sblist.size/7)): #대출여부에 따라 문장 추가
                show=[]
                for j in range(0,6): #대출여부 외에는 그대로니 for문 사용
                    show.append(sblist[i,j-1])
                Btreeview.insert("","end",text="",values=show,iid=i) 
                
        book_info = Frame(Book_window, borderwidth = 1, relief = "solid")
        book_info.place(x = 30, y = 120)
        book_info.configure(background = "white")
        bsearch_label = Label(book_info, text = "도서 조회", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        bsearch_label.grid(row = 0, column = 1, padx = 80, pady = 10)
        
        Bname_label = Label(book_info, text = "도서명 : ", fg = "#203864", bg = "white")
        Bname_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        Bname_text = Entry(book_info, width = 50)
        Bname_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        Bauthor_label = Label(book_info, text = "저자 : ", fg = "#203864", bg = "white")
        Bauthor_label.grid(row = 2, column = 0, padx = 10, pady = 5)
        sear_Bauthor = Entry(book_info, width = 50)
        sear_Bauthor.grid(row = 2, column = 1, padx = 10, pady = 5)
        bsear_btn = Button(book_info, text = "조회", command = printbook)
        bsear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)
        
        bexit_btn = Button(book_info, text= "닫기",command = lambda: book_info.destroy())
        bexit_btn.grid(row = 7, column = 2, padx = 10, pady = 20)
        
        # 조회한 도서
        Btreeview = tkinter.ttk.Treeview(book_info,
                                         column = ["B_check_rent", "B_ISBN", "B_name", "B_author", "B_price", "B_URL"],
                                         displaycolumns = ["B_check_rent", "B_ISBN", "B_name", "B_author", "B_price", "B_URL"],
                                         height = 7, show = 'headings')

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

        # 도서 정보
        def Book_show(event): #가끔 수정, 삭제 안될 때 있는데 이유는 모르겠음
            def change_book(): #모든 정보 입력 및 isbn, 도서명, 저자명, 출판사가 동일해야 수정가능...../도서등록하고 다시 실행하면 수정불가(이부분 수정필요)
                cb_list = np.array([])
                if Btextname.get()=='' or Btextauthor.get()=='' or Btextpubli.get()=='': #도서명, 저자, 출판사 하나라도 입력안되면 팝업창
                    messagebox.showinfo("경고,", "필수항목(도서명, 저자, 출판사)을 입력해주세요.\n")
                    return 0
                if B.check_isbn(int(BtextISBN.get())):
                    messagebox.showinfo("경고,", "등록되지 않은 도서입니다..\n")
                    return 0
                else:
                    rent = '대출가능'
                    cb_list = np.append(cb_list, np.array([int(BtextISBN.get()), Btextname.get(), Btextauthor.get(), Btextprice.get(), BtextURL.get(), Btextpubli.get(), rent]))
                    B.CB_book(int(BtextISBN.get()))
                    B.B_Info([cb_list])
                    messagebox.showinfo("알림","도서 수정이 완료되었습니다.")# 팝업창
                
            def delete_book(): # 모든 정보를 동일하게 입력해야 삭제 가능, 삭제 안될 때도 있음 기준은 모르겠음
                B.CB_book(int(BtextISBN.get()))
                messagebox.showinfo("알림","도서가 삭제되었습니다.") #도서삭제 팝업창
                
            bookshow = Toplevel(Book_window)
            bookshow.resizable(width = False, height = False)
            
            book_show_label = Label(bookshow, image = book_wall)
            book_show_label.pack()

            book_show_info = Frame(bookshow)
            book_show_info.place(x = 20, y = 70)
            book_show_info.configure(background = "white")
            
            BlabelISBN = Label(book_show_info, text="ISBN : ", fg = "#203864", bg = "white")
            BlabelISBN.grid(row=2, column=0, padx=60, pady = 3)
            BtextISBN = Entry(book_show_info)
            BtextISBN.grid(row=2, column=1, padx=70, pady = 3)

            Blabelname = Label(book_show_info, text="도서명 : ", fg = "#203864", bg = "white")
            Btextname = Entry(book_show_info)
            Blabelname.grid(row=3, column=0, padx=60, pady = 3)
            Btextname.grid(row=3, column=1, padx=70, pady = 3)

            Blabelauthor = Label(book_show_info, text="저자 : ", fg = "#203864", bg = "white")
            Btextauthor = Entry(book_show_info)
            Blabelauthor.grid(row=4, column=0, padx=60, pady = 3)
            Btextauthor.grid(row=4, column=1, padx=70, pady = 3)

            Blabelpubli = Label(book_show_info, text="출판사 : ", fg = "#203864", bg = "white")
            Btextpubli = Entry(book_show_info)
            Blabelpubli.grid(row=5, column=0, padx=60, pady = 3)
            Btextpubli.grid(row=5, column=1, padx=70, pady = 3)

            Blabelprice = Label(book_show_info, text="가격: ", fg = "#203864", bg = "white")
            Btextprice = Entry(book_show_info)
            Blabelprice.grid(row=6, column=0, padx=60, pady = 3)
            Btextprice.grid(row=6, column=1, padx=70, pady = 3)

            BlabelURL = Label(book_show_info, text="관련 URL : ", fg = "#203864", bg = "white") 
            BtextURL = Entry(book_show_info)
            BlabelURL.grid(row=7, column=0, padx=60, pady = 3)
            BtextURL.grid(row=7, column=1, padx=70, pady = 3)

            book_revice_btn = Button(book_show_info, text="수정", command = change_book)
            book_revice_btn.grid(row=10, column=0,padx=60, pady = 5)

            book_delete_btn = Button(book_show_info, text="삭제", command = delete_book)
            book_delete_btn.grid(row=10, column=1,padx=60, pady = 5)

            book_exit_btn = Button(book_show_info, text="닫기", command=lambda: bookshow.destroy())
            book_exit_btn.grid(row=10, column=2, padx=70, pady = 5)

        Btreeview.bind('<Double-1>', Book_show)

    def Bookadd(): #도서등록은 다 된거 같은데...
        checkbook = []
        def check(): #중복확인 함수
            if B.check_book(Bname_text.get()): #
                messagebox.showinfo("결과","이미 등록된 도서입니다.")
            elif Bname_text.get() =='':
                messagebox.showinfo("경고","도서명을 입력하세요.")
            else:
                messagebox.showinfo("결과","등록 가능한 도서입니다.")
                checkbook.append(Bname_text.get())
        def addbook():
            b_list = np.array([])
            if Bname_text.get() not in checkbook: #중복확인 버튼 안누르면 팝업창
                messagebox.showinfo("경고","중복확인 하세요.")
                return 0
            if Bname_text.get()=='' or Bauthor_text.get()=='' or Bpubli_text.get()=='': #도서명, 저자, 출판사 하나라도 입력안되면 팝업창
                messagebox.showinfo("경고,", "필수항목(도서명, 저자, 출판사)을 입력해주세요.\n")
                return 0
            rent = '대출가능'
            b_list = np.append(b_list, np.array([int(BISBN_text1.get()), Bname_text.get(), Bauthor_text.get(), Bprice_text.get(), BURL_text.get(), Bpubli_text.get(), rent]))
            B.B_Info([b_list])
            messagebox.showinfo("알림","도서 등록이 완료되었습니다.")# 팝업창
            checkbook.remove(Bname_text.get()) #중복확인을 위한 리스트 비워주기
            isbnlist.append(int(BISBN_text1.get()))

        book_add = Frame(Book_window, borderwidth = 1, relief = "solid")
        book_add.place(x = 30, y = 120)
        book_add.configure(background = "white")
        
        badd_label = Label(book_add, text = "도서 등록", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        badd_label.grid(row = 0, column = 1, pady = 10)

        
        BISBN_add = Label(book_add, text="ISBN : ", fg = "#203864", bg = "white")
        BISBN_add.grid(row=1, column=0, padx = 10, pady = 5)
        BISBN_text1 = Entry(book_add, width = 50) 
        BISBN_text1.grid(row=1, column=1, padx=50, pady = 5)


        Bname_add = Label(book_add, text="도서명 : ", fg = "#203864", bg = "white")
        Bname_text = Entry(book_add, width = 50)
        Bname_add.grid(row=2, column=0, padx=10, pady = 5)
        Bname_text.grid(row=2, column=1, padx=50, pady = 5)

        Bname_check_btn = Button(book_add, text="중복확인", command = check)
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

        bser_add_btn = Button(book_add, text= "등록", command = addbook)
        bser_add_btn.grid(row = 8, column = 1, padx = 20, pady = 20)

        bser_exit_btn = Button(book_add, text="닫기", command=lambda: book_add.destroy())
        bser_exit_btn.grid(row=8, column=2, padx=20, pady = 5)
    
    Book_window = Toplevel(window)
    Book_window.geometry("700x500")
    Book_window.resizable(width = False, height = False)

    book_wall_label = Label(Book_window, image = de_wall)
    book_wall_label.place(x = -100, y = -2)

    book_menu = Frame(Book_window, height = 30, bd = 0)
    book_menu.place(x = 0, y = 65)

    book_btn = Button(book_menu, text = "도서 조회", width = 34, font = ("맑은 고딕", 13), fg = "#203864", bg = "white", command = Booksearch)
    book_btn1 = Button(book_menu, text = "도서 등록", width = 34, font = ("맑은 고딕", 13), fg = "#203864", bg = "white", command = Bookadd)
    
    book_btn.grid(row = 0, column = 0)
    book_btn1.grid(row = 0, column = 1)

## 대여
# 회원 -> 도서 선택 눌렀을때 조회 / 반납에 추가 안됨
# 대여(회원)에 선택 누르면 인덱스에러 뜸..
# 반납할 목록 없을때 뜨는 예외처리 해야할듯

def Rentwindow():
    # 회원 - 도서 대여
    def Rent_User_Search():
        # 선택 버튼
        def Rent_User_Selected():
            def printbook(): #도서조회 함수
                sblist = np.array([])
                if Bname_text.get():
                    sblist = B.search_booktitle(Bname_text.get()) #도서명 입력된 경우
                elif sear_Bauthor.get():
                    sblist = B.search_bookauthor(sear_Bauthor.get()) #저자명 입력된 경우
                else:
                    messagebox.showinfo("경고","도서명과 저자명 하나라도 입력해주세요.")
                Btreeview.delete(*Btreeview.get_children()) #다른거 조회하면 delete
                for i in range(int(sblist.size/7)): #대출여부에 따라 문장 추가
                    show=[]
                    for j in range(0,6): #대출여부 외에는 그대로니 for문 사용
                        show.append(sblist[i,j-1])
                    Btreeview.insert("","end",text="",values=show,iid=i)

            
            selecteditem = Utreeview.focus()
            getValue = Utreeview.item(selecteditem).get('values')

            # 회원조회 후 -> 도서조회
            BUrent_info = Toplevel(Rent_window)
            BUrent_info.configure(background = "white")
            BUrent_info.title("선택한 회원 : " + getValue[0])

            BUrent_show_label = Label(BUrent_info, image = U_Brent_wall)
            BUrent_show_label.pack()

            BUrent_show_info = Frame(BUrent_info)
            BUrent_show_info.place(x = 20, y = 80)
            BUrent_show_info.configure(background = "white")

            Bname_label = Label(BUrent_show_info, text = "도서명 : ", fg = "#203864", bg = "white")
            Bname_label.grid(row = 0, column = 0, padx = 10, pady = 5)
            Bname_text = Entry(BUrent_show_info, width = 50)
            Bname_text.grid(row = 0, column = 1, padx = 10, pady = 5)
            Bauthor_label = Label(BUrent_show_info, text = "저자 : ", fg = "#203864", bg = "white")
            Bauthor_label.grid(row = 2, column = 0, padx = 10, pady = 5)
            sear_Bauthor = Entry(BUrent_show_info, width = 50)
            sear_Bauthor.grid(row = 2, column = 1, padx = 10, pady = 5)
            
            bsear_btn = Button(BUrent_show_info, text = "조회",command = printbook) # treeview에 조회정보 출력
            bsear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)
            bsear_btn2 = Button(BUrent_show_info, text = "선택") # 이거 대여 안되는거같음 
            bsear_btn2.grid(row = 4, column = 1, padx = 20, pady = 5)
            bsear_btn3 = Button(BUrent_show_info, text = "닫기", command=lambda: BUrent_info.destroy())
            bsear_btn3.grid(row = 4, column = 2, padx = 20, pady = 5)
        
            # 조회한 도서
            Btreeview = tkinter.ttk.Treeview(BUrent_show_info,
                                             column = ["B_ISBN", "B_name", "B_pub", "B_check_rent","B_author", "B_price", "B_URL"],
                                             displaycolumns = ["B_ISBN", "B_name", "B_pub", "B_check_rent", "B_author", "B_price", "B_URL"],
                                             height = 7, show = 'headings')            

            Btreeview.grid(row = 3, column = 1)

            Btreeview.column("B_ISBN", width=80, anchor="center")
            Btreeview.heading("B_ISBN", text="ISBN", anchor="center")

            Btreeview.column("B_name", width=100, anchor="center")
            Btreeview.heading("B_name", text="도서명", anchor="center")

            Btreeview.column("B_pub", width=70, anchor="center")
            Btreeview.heading("B_pub", text="출판사", anchor="center")

            Btreeview.column("B_check_rent", width=60, anchor="center")
            Btreeview.heading("B_check_rent", text="대출여부", anchor="center")

            Btreeview.column("B_author", width=60, anchor="center")
            Btreeview.heading("B_author", text="저자", anchor="center")

            Btreeview.column("B_price", width=50, anchor="center")
            Btreeview.heading("B_price", text="가격", anchor="center")

            Btreeview.column("B_URL", width=80, anchor="center")
            Btreeview.heading("B_URL", text="정보 URL", anchor="center")

            df_book = pd.read_csv('book1.csv', encoding = 'UTF-8-sig')
            list_from_df_book = df_book.values.tolist()

            # 대여(도서) 리스트
            for i in range(len(df_user)):
                list_from_df_book[i] = list_from_df_book[i][1:3] + list_from_df_book[i][6:7] + list_from_df_book[i][7:8] + list_from_df_book[i][3:6]
                Btreeview.insert("", "end", text = "", values=list_from_df_book[i], iid = i)
                Btreeview.bind("<Double-1>",Rent_User_Selected)
                
            
        def Searched_user():    #이름, 연락처 검색했을 때
            Utreeview.delete(*Utreeview.get_children()) #Utreeview의 모든 값들 제거

            for i in range(len(df_user)):               #이름, 연락처 검색한 것만 다시 조회
                if (Uname_text.get() in list_from_df_user[i][0]) & (sear_Uphone.get() in list_from_df_user[i][2]) :
                    Utreeview.insert("", "end", text = "", values=list_from_df_user[i], iid = i)
                    Utreeview.bind("<Double-1>",Rent_User_Selected)
            
        # 대여(회원) 프레임
        Rent_user_info = Frame(Rent_window, borderwidth = 1, relief = "solid")
        Rent_user_info.place(x = 30, y = 120)
        Rent_user_info.configure(background = "white")
        usearch_label = Label(Rent_user_info, text = "회원 조회", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        usearch_label.grid(row = 0, column = 1, padx = 80, pady = 10)
        Uname_label = Label(Rent_user_info, text = "이름 : ", fg = "#203864", bg = "white")
        Uname_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        Uname_text = Entry(Rent_user_info, width = 50)
        Uname_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        Uphone_label = Label(Rent_user_info, text = "연락처 : ", fg = "#203864", bg = "white")
        Uphone_label.grid(row = 2, column = 0, padx = 10, pady = 5)
        sear_Uphone = Entry(Rent_user_info, width = 50)
        sear_Uphone.grid(row = 2, column = 1, padx = 10, pady = 5)
        usear_btn = Button(Rent_user_info, text = "조회",command = Searched_user)
        usear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)
        usear_btn2 = Button(Rent_user_info, text = "선택",command = Rent_User_Selected)
        usear_btn2.grid(row = 4, column = 1, padx = 20, pady = 5)
        usear_btn3 = Button(Rent_user_info, text = "닫기", command=lambda: Rent_user_info.destroy())
        usear_btn3.grid(row = 4, column = 2, padx = 20, pady = 5)
        
        # 조회한 회원
        Utreeview = tkinter.ttk.Treeview(Rent_user_info,
                                         column = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check", "U_check_exit"],
                                         displaycolumns = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check", "U_check_exit"],
                                         height = 7, show = 'headings')
        
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
        Utreeview.heading("U_check", text="대출여부", anchor="center")
        Utreeview.column("U_check_exit", width=70, anchor="center")
        Utreeview.heading("U_check_exit", text="탈퇴여부", anchor="center")

        df_user = pd.read_csv('USER1.csv', encoding = 'utf-8-sig')
        list_from_df_user = df_user.values.tolist()

        for i in range(len(df_user)):
            
            if list_from_df_user[i][4] == 1:
                list_from_df_user[i][4] = "남자"
            else:
                list_from_df_user[i][4] = "여자"
            list_from_df_user[i] = list_from_df_user[i][2:3] + list_from_df_user[i][3:4] + list_from_df_user[i][1:2] + list_from_df_user[i][4:]
            Utreeview.insert("", "end", text = "", values=list_from_df_user[i], iid = i)
            Utreeview.bind("<Double-1>",Rent_User_Selected)

        # 여기까지
    
    # 도서 - 회원 대여
    def rent_book():
        def printbook(): #대여(도서)에서 도서조회 함수
            sblist = np.array([])
            if Brent_name_text.get():
                sblist = B.search_booktitle(Brent_name_text.get()) #도서명 입력된 경우
            elif sear_Bauthor.get():
                sblist = B.search_bookauthor(sear_Bauthor.get()) #저자명 입력된 경우
            else:
                messagebox.showinfo("경고","도서명과 저자명 하나라도 입력해주세요.")
            Brent_treeview.delete(*Brent_treeview.get_children()) #다른거 조회하면 delete
            for i in range(int(sblist.size/7)): #대출여부에 따라 문장 추가
                show=[]
                for j in range(2,8,4): #대출여부 외에는 그대로니 for문 사용
                    show.append(sblist[i,j-1])
                Brent_treeview.insert("","end",text="",values=show,iid=i)
            
        
        # 도서에서 선택 버튼눌렀을 때 출력되는 회원 화면
        def Rent_Search_book_user() :
            def Searched_user():    #이름, 연락처 검색했을 때
                Utreeview.delete(*Utreeview.get_children()) #Utreeview의 모든 값들 제거

                df_user = pd.read_csv('USER1.csv',encoding = 'utf-8-sig')

                for i in range(len(df_user)):               #이름, 연락처 검색한 것만 다시 조회
                    if (BUrent_name_text.get() in list_from_df_user[i][0]) & (Bsear_Uphone.get() in list_from_df_user[i][2]) :
                        Utreeview.insert("", "end", text = "", values=list_from_df_user[i], iid = i)
                        Utreeview.bind("<Double-1>",Rent_Search_book_user)

            selecteditem_book = Brent_treeview.focus()
            getValue_book = Brent_treeview.item(selecteditem_book).get('values')

            if getValue_book[2] == '대출 중':
                messagebox.showinfo('경고!','이미 대출 중인 도서입니다!')

            def select_User_in_Book(): #대여(도서) -> 유저 선택 후 선택버튼

                selecteditem_user = Utreeview.focus()
                getValue_user = Utreeview.item(selecteditem_user).get('values')

                response = messagebox.askokcancel('도서 대여',getValue_user[0] + ' 회원님으로 '
                                              + getValue_book[0] + ' 도서를 대여하시겠습니까?')
                
                if response == 1:
                    df_user = pd.read_csv('USER1.csv',encoding = 'utf-8-sig')
                    df_book = pd.read_csv('book1.csv',encoding = 'utf-8-sig')
                    df_rent = pd.read_csv('RENT.csv',encoding = 'utf-8-sig')
                    
                    plus_day = 14
                    today = dt.date.today()
                    new_list = [[0,1, df_book.loc[df_book.index[0]]['ISBN'], getValue_book[0], getValue_user[0],
                            today, today + dt.timedelta(days = plus_day),'대여 중',getValue_user[2]]]
                    
                    
                    df_list = pd.DataFrame(new_list, columns = df_rent.columns)
                    df_rent = pd.concat([df_rent,df_list], axis = 0)
                    
                    df_rent.to_csv('RENT.csv',index = False, encoding= 'utf-8-sig')

                    cnt_index = df_user.index[(df_user['PHONE']) == (getValue_user[2])]

                    if (df_user['RENT_CNT'][cnt_index[0]]) > 3 : # 대여한 도서가 3권일 때
                        messagebox.showinfo('경고!','이미 대여한 도서가 3권입니다!')
                    else :
                        messagebox.showinfo('대여 완료','도서가 대여되었습니다.')
                        df_user['RENT_CNT'][cnt_index[0]] += 1  # RENT_CNT 1 추가(대여횟수 증가)
                        df_user.to_csv("USER1.csv",index= False,encoding = 'utf-8-sig')

                    df_book_index = df_book.index[(df_book['TITLE'] == getValue_book[0])]
                    
                    if df_book['RENT'][df_book_index[0]] == "대출 중" :
                        messagebox.showinfo('경고!','이미 대출 중인 도서 입니다!')
                    else :
                        df_book['RENT'][df_book_index[0]] = "대출 중"
                        df_book.to_csv("book1.csv",index = False, encoding = 'utf-8-sig')

                    
                    


            
                else : # 도서 선택 -> 유저 선택 버튼 누르고 대여취소, response
                    messagebox.showinfo('대여 취소','대여가 취소되었습니다.')
                
            # 도서 - 회원
            BUrent_info = Toplevel(Rent_window)
            BUrent_info.configure(background = "white")
            BUrent_info.title("선택한 책 : " + getValue_book[0])
            
            BUrent_show_label = Label(BUrent_info, image = B_Urent_wall)
            BUrent_show_label.pack()

            BUrent_show_info = Frame(BUrent_info)
            BUrent_show_info.place(x = 20, y = 70)
            BUrent_show_info.configure(background = "white")
        
            BUrent_name_label = Label(BUrent_show_info, text = "이름 : ", fg = "#203864", bg = "white")
            BUrent_name_label.grid(row = 0, column = 0, padx = 10, pady = 5)
            BUrent_name_text = Entry(BUrent_show_info, width = 50)
            BUrent_name_text.grid(row = 0, column = 1, padx = 10, pady = 5)

            BUphone_label = Label(BUrent_show_info, text = "연락처 : ", fg = "#203864", bg = "white")
            BUphone_label.grid(row = 1, column = 0, padx = 10, pady = 5)
            Bsear_Uphone = Entry(BUrent_show_info, width = 50)
            Bsear_Uphone.grid(row = 1, column = 1, padx = 10, pady = 5)

            BUrent_btn = Button(BUrent_show_info, text = "조회",command = Searched_user)
            BUrent_btn.grid(row = 0, column = 2, padx = 20, pady = 5)
            BUrent_btn2 = Button(BUrent_show_info, text = "선택",command = select_User_in_Book)
            BUrent_btn2.grid(row = 3, column = 1, padx = 20, pady = 5)
            bsear_btn3 = Button(BUrent_show_info, text = "닫기", command=lambda: BUrent_info.destroy())
            bsear_btn3.grid(row = 3, column = 2, padx = 20, pady = 5)

            Utreeview = tkinter.ttk.Treeview(BUrent_show_info,
                                             column = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check", "U_check_exit"],
                                             displaycolumns = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check", "U_check_exit"],
                                             height = 7, show = 'headings')

            Utreeview.grid(row = 2, column = 1)

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
            Utreeview.heading("U_check", text="대출여부", anchor="center")

            Utreeview.column("U_check_exit", width=70, anchor="center")
            Utreeview.heading("U_check_exit", text="탈퇴여부", anchor="center")

            df_user = pd.read_csv('USER1.csv', encoding = 'utf-8-sig')
            list_from_df_user = df_user.values.tolist()

            for i in range(len(df_user)):
                
                if list_from_df_user[i][4] == 1:
                    list_from_df_user[i][4] = "남자"
                else:
                    list_from_df_user[i][4] = "여자"
                list_from_df_user[i] = list_from_df_user[i][2:3] + list_from_df_user[i][3:4] + list_from_df_user[i][1:2] + list_from_df_user[i][4:]
                Utreeview.insert("", "end", text = "", values=list_from_df_user[i], iid = i)
                Utreeview.bind("<Double-1>",Rent_Search_book_user)

        
        brent_info = Frame(Rent_window, borderwidth = 1, relief = "solid")
        brent_info.place(x = 90, y = 120)
        brent_info.configure(background = "white")
        brent_label = Label(brent_info, text = "대여(도서)", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        brent_label.grid(row = 0, column = 1, padx = 80, pady = 10)
        Brent_name_label = Label(brent_info, text = "도서명 : ", fg = "#203864", bg = "white")
        Brent_name_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        Brent_name_text = Entry(brent_info, width = 50)
        Brent_name_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        bsear_btn = Button(brent_info, text = "조회",command = printbook)
        bsear_btn.grid(row = 1, column = 2, padx = 20, pady = 5)
        bsear_btn2 = Button(brent_info, text = "선택",command = Rent_Search_book_user)
        bsear_btn2.grid(row = 4, column = 1, padx = 20, pady = 5)
        bsear_btn3 = Button(brent_info, text = "닫기",command=lambda: brent_info.destroy())
        bsear_btn3.grid(row = 4, column = 2, padx = 20, pady = 5)

        Brent_treeview = tkinter.ttk.Treeview(brent_info,
                                              column = ["BR_name", "BR_publi", "BR_state"],
                                              displaycolumns = ["BR_name", "BR_publi", "BR_state"],
                                              height = 7, show = 'headings')

        Brent_treeview.grid(row = 3, column = 1)
        Brent_treeview.column("BR_name", width=130, anchor="center")
        Brent_treeview.heading("BR_name", text="도서명", anchor="center")

        Brent_treeview.column("BR_publi", width=100, anchor="center")
        Brent_treeview.heading("BR_publi", text="출판사", anchor="center")

        Brent_treeview.column("BR_state", width=100, anchor="center")
        Brent_treeview.heading("BR_state", text="대출상태", anchor="center")

        df_book = pd.read_csv('book1.csv', encoding = 'utf-8-sig')
        list_from_df_book = df_book.values.tolist()
        
        for i in range(len(df_book)):
            list_from_df_book[i] = list_from_df_book[i][2:3] + list_from_df_book[i][6:7] + list_from_df_book[i][7:8]
            Brent_treeview.insert("", "end", text = "", values=list_from_df_book[i], iid = i)

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
        usear_btn = Button(Urent_info, text = "조회", command = Rent_User_Search)
        usear_btn.grid(row = 1, column = 2, padx = 20, pady = 5)
    

    def rent_return():

        def rent_return_selected(): #도서 반납 선택버튼

            selecteditem = rent_treeview.focus()
            getValue = rent_treeview.item(selecteditem).get('values')
            
            df_rent = pd.read_csv('RENT.csv',encoding = 'utf-8-sig')
            response = messagebox.askokcancel('도서 반납',getValue[1] + ' 회원님이 대여한 '
                                              + getValue[0] + ' 도서를 반납하시겠습니까?')
            
            if response == 1:
                df_rent = pd.read_csv('RENT.csv',encoding = 'utf-8-sig')
                dropindex = df_rent.index[(df_rent['TITLE'] == getValue[0])]
                df_rent.drop(dropindex, inplace = True)
                df_rent.reset_index(drop=True, inplace = True)
                
                df_rent.to_csv("RENT.csv",index = False,encoding = 'utf-8-sig')

                df_user = pd.read_csv('USER1.csv',encoding = 'cp949')
                df_book = pd.read_csv('book1.csv',encoding = 'cp949')

                cnt_index = df_user.index[(df_user['NAME']) == (getValue[1])]
                df_user['RENT_CNT'][cnt_index[0]] -= 1

                df_book_index = df_book.index[(df_book['TITLE'] == getValue[0])]
                    
                if df_book['RENT'][df_book_index[0]] == "대출 중" :
                    df_book['RENT'][df_book_index[0]] = "대여 가능"
                    df_book.to_csv('book1.csv',index = False, encoding = 'utf-8-sig')
                
                messagebox.showinfo('반납 완료','도서가 반납되었습니다.')
            else :
                messagebox.showinfo('반납 취소','반납이 취소되었습니다.')
                

        # 조회/반납 목록 없으면 뜨는 오류 해결해야함
        rent_info = Frame(Rent_window, borderwidth = 1, relief = "solid")
        rent_info.place(x = 30, y = 120)
        rent_info.configure(background = "white")
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
        rsear_btn2 = Button(rent_info, text = "선택",command = rent_return_selected)
        rsear_btn2.grid(row = 4, column = 1, padx = 20, pady = 5)
        bsear_btn3 = Button(rent_info, text = "닫기",command=lambda: rent_info.destroy())
        bsear_btn3.grid(row = 4, column = 2, padx = 20, pady = 5)

        rent_treeview = tkinter.ttk.Treeview(rent_info,
                                             column = ["R_uname", "R_bname", "R_rentday", "R_returnday", "R_rent_check"],
                                             displaycolumns = ["R_uname", "R_bname", "R_rentday", "R_returnday", "R_rent_check"],
                                             height = 7, show = 'headings')

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

        df_rent = pd.read_csv('RENT.csv', encoding = 'utf-8-sig')
        list_from_df_rent = df_rent.values.tolist()

        for i in range(len(df_rent)):
            list_from_df_rent[i] = list_from_df_rent[i][3:]
            rent_treeview.insert("", "end", text = "", values=list_from_df_rent[i], iid = i)
            rent_treeview.bind("<Double-1>",rent_return)

    Rent_window = Toplevel(window)
    Rent_window.geometry("700x500")
    Rent_window.resizable(width = False, height = False)

    rent_wall_label = Label(Rent_window, image = de_wall)
    rent_wall_label.place(x = -100, y = -2)

    rent_menu = Frame(Rent_window, height = 30, bd = 0)
    rent_menu.place(x = 0, y = 65)

    rent_btn = Button(rent_menu, text = "대여(도서)", width = 25, font = ("맑은 고딕", 12), fg = "#203864", bg = "white", command = rent_book)
    rent_btn1 = Button(rent_menu, text = "대여(회원)", width = 25, font = ("맑은 고딕", 12), fg = "#203864", bg = "white", command = Rent_User_Search)
    rent_btn2 = Button(rent_menu, text = "조회 / 반납", width = 25, font = ("맑은 고딕", 12), fg = "#203864", bg = "white", command = rent_return)
    
    rent_btn.grid(row = 0, column = 0)
    rent_btn1.grid(row = 0, column = 1)
    rent_btn2.grid(row = 0, column = 2)

## 메인
window = Tk()
window.geometry("700x500")
window.resizable(width = False, height = False)

wall = PhotoImage(file = "메인 화면.png")
book = PhotoImage(file = "회원.png")
user = PhotoImage(file = "책.png")
rent = PhotoImage(file = "대여.png")

de_wall = PhotoImage(file = "기본 배경.png")
user_wall = PhotoImage(file = "회원 정보.png")
book_wall = PhotoImage(file = "도서 정보.png")
rent_wall = PhotoImage(file = "대여 정보.png")

U_Brent_wall = PhotoImage(file = "회원-도서.png")
B_Urent_wall = PhotoImage(file = "도서-회원.png")

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
