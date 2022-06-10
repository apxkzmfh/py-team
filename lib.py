from tkinter import*
import tkinter.ttk
from tkinter import messagebox
import pandas as pd
import numpy as np
from tkinter import filedialog  #사진 불러오기용
from PIL import ImageTk,Image
import warnings
warnings.filterwarnings('ignore')

df_book=pd.read_csv('Book.csv', encoding='UTF-8-sig')
book_list=np.array([])
book_list=np.append(book_list,df_book)
book_list=np.reshape(book_list,(int(book_list.size/8),8))


isbnlist = []

class Book: #도서 클래스
    
    def __init__(self,book): #생성자
        self.__book=book #self.__으로 private선언

    def check_book(self, book): #중복확인 함수
        if book in self.__book[:,1]:
            return True
        else:
            return False
       

B=Book(book_list) #인스턴스 생성

## 함수
## 조회 등록 수정

## 회원
def Userwindow():
    def Usersearch():
        user_info = Frame(User_window, borderwidth = 1, relief = "solid")
        user_info.place(x = 25, y = 120)
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
        usear_btn = Button(user_info, text = "조회")
        usear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)
        
        # 조회한 회원
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

        #값 어찌나옴...
        treeValueList = [("김미경", "2000.12.19", "010-1234-5678", "여", "0123456@naver.com", "3권 대출 중", "X")]

        for i in range(len(treeValueList)):
            Utreeview.insert("", "end", text="", values=treeValueList[i], iid=i)

        uexit_btn = Button(user_info, text = "닫기",command=lambda: user_info.destroy())
        uexit_btn.grid(row = 6, column = 2, padx = 20, pady = 5)
        
        # 회원 정보
        def User_show(event):
            usershow = Toplevel(User_window)
            usershow.resizable(width = False, height = False)
            
            user_show_label = Label(usershow, image = user_wall)
            user_show_label.pack()

            user_show_info = Frame(usershow)
            user_show_info.place(x = 20, y = 70)
            user_show_info.configure(background = "white")
            
            UlabelName = Label(user_show_info, text="이름 : ", fg = "#203864", bg = "white")
            UlabelName.grid(row=2, column=0, padx=60, pady = 3)
            UtextName = Entry(user_show_info)
            UtextName.grid(row=2, column=1, padx=70, pady = 3)

            UlabelBirth = Label(user_show_info, text="생년월일 : ", fg = "#203864", bg = "white")
            UtextBirth = Entry(user_show_info)
            UlabelBirth.grid(row=3, column=0, padx=60, pady = 3)
            UtextBirth.grid(row=3, column=1, padx=70, pady = 3)

            UlabelHP = Label(user_show_info, text="전화번호 : ", fg = "#203864", bg = "white")
            UtextHP = Entry(user_show_info)
            UlabelHP.grid(row=4, column=0, padx=60, pady = 3)
            UtextHP.grid(row=4, column=1, padx=70, pady = 3)

            UlabelGender = Label(user_show_info, text="성별 : ", fg = "#203864", bg = "white")
            UtextGender = Entry(user_show_info)
            UlabelGender.grid(row=5, column=0, padx=60, pady = 3)
            UtextGender.grid(row=5, column=1, padx=70, pady = 3)

            UlabelEmail = Label(user_show_info, text="이메일: ", fg = "#203864", bg = "white")
            UtextEmail = Entry(user_show_info)
            UlabelEmail.grid(row=6, column=0, padx=60, pady = 3)
            UtextEmail.grid(row=6, column=1, padx=70, pady = 3)

            UlabelPicture = Label(user_show_info, text="사진 : ", fg = "#203864", bg = "white") 
            UtextPicture = Entry(user_show_info)
            UlabelPicture.grid(row=7, column=0, padx=60, pady = 3)
            UtextPicture.grid(row=7, column=1, padx=70, pady = 3)
            # 사진 제외?

            UlabelRent = Label(user_show_info, text="대출여부 : ", fg = "#203864", bg = "white")
            UtextRent = Entry(user_show_info)
            UlabelRent.grid(row=8, column=0, padx=60, pady = 3)
            UtextRent.grid(row=8, column=1, padx=70, pady = 3)

            UlabelExit = Label(user_show_info, text="탈퇴여부 : ", fg = "#203864", bg = "white")
            UtextExit = Entry(user_show_info)
            UlabelExit.grid(row=9, column=0, padx=60, pady = 3)
            UtextExit.grid(row=9, column=1,padx=70, pady = 3)

            user_revice_btn = Button(user_show_info, text="수정")
            user_revice_btn.grid(row=10, column=0,padx=60, pady = 5)

            user_delete_btn = Button(user_show_info, text="탈퇴")
            user_delete_btn.grid(row=10, column=1, padx=60, pady = 5)

            Uexit_btn = Button(user_show_info, text="닫기", command=lambda: usershow.destroy())
            Uexit_btn.grid(row=10, column=2, padx=70, pady = 5)


        Utreeview.bind('<Double-1>', User_show)

    def Useradd():
        user_add = Frame(User_window, borderwidth = 1, relief = "solid")
        user_add.place(x = 35, y = 120)
        user_add.configure(width = 600, height = 1000, background = "white")
        uadd_label = Label(user_add, text = "회원 등록", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        uadd_label.grid(row = 0, column = 1, pady = 10)

        Uname_add = Label(user_add, text="이름 : ", fg = "#203864", bg = "white")
        Uname_add.grid(row=1, column=0, padx = 10, pady = 5)
        Uname_text1 = Entry(user_add, width = 50) 
        Uname_text1.grid(row=1, column=1, padx=50, pady = 5)

        Ubirth_add = Label(user_add, text="생년월일 : ", fg = "#203864", bg = "white")
        Ubirth_text = Entry(user_add, width = 50)
        Ubirth_add.grid(row=2, column=0, padx=10, pady = 5)
        Ubirth_text.grid(row=2, column=1, padx=50, pady = 5)

        Uphone_add = Label(user_add, text="전화번호 : ", fg = "#203864", bg = "white")
        Uphone_text = Entry(user_add, width = 50) 
        Uphone_add.grid(row=3, column=0, padx=10, pady = 5)
        Uphone_text.grid(row=3, column=1, padx=50, pady = 5)
        
        Uphone_check_btn = Button(user_add, text="중복확인")
        Uphone_check_btn.grid(row=3, column=2, padx=10, pady = 5)

        Ugender_label = Label(user_add, text="성별 : ", fg = "#203864", bg = "white")
        Ugender_text = Entry(user_add, width = 50) 
        Ugender_label.grid(row=4, column=0, padx=10, pady = 5)
        Ugender_text.grid(row=4, column=1, padx=50, pady = 5)

        Uemail_label = Label(user_add, text="이메일 : ", fg = "#203864", bg = "white")
        Uemail_text = Entry(user_add, width = 50) 
        Uemail_label.grid(row=5, column=0, padx=10, pady = 5)
        Uemail_text.grid(row=5, column=1, padx=50, pady = 5)

        Upicture_label = Label(user_add, text="사 진 : ", fg = "#203864", bg = "white") 
        Upicture_text = Entry(user_add, width = 50) 
        Upicture_label.grid(row=6, column=0, padx=10, pady = 5)
        Upicture_text.grid(row=6, column=1, padx=50, pady = 5)
        # 사진 제외?
        
        Upicture_search_btn = Button(user_add, text="찾기")
        Upicture_search_btn.grid(row=6, column=2, padx=20, pady = 5)

        user_add_btn = Button(user_add, text= "등록")
        user_add_btn.grid(row = 7, column = 1, padx = 10, pady = 20)

        user_exit_btn = Button(user_add, text= "닫기",command = lambda: user_add.destroy())
        user_exit_btn.grid(row = 7, column = 2, padx = 10, pady = 20)

        
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
def Bookwindow():
    def Booksearch(): #조회도 다 된듯..?
        def print_book():
            df_book = pd.read_csv('Book.csv', encoding='UTF-8-sig')
            df_book = df_book.astype('str')
            list_from_df_book = (df_book.values).tolist()
            treeValueList = list_from_df_book#도서명, 저자명 검색했을때
            Btreeview.delete(*Btreeview.get_children()) #Btreeview의 모든 값들 제거
            for i in range(len(df_book)):           
                if (Bname_text.get() in list_from_df_book[i][1]) & (sear_Bauthor.get() in list_from_df_book[i][2]) :
                    Btreeview.insert("", "end", text = "", values=list_from_df_book[i], iid = i)
                
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
        bsear_btn = Button(book_info, text = "조회", command = print_book)
        bsear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)
        
        bexit_btn = Button(book_info, text= "닫기",command = lambda: book_info.destroy())
        bexit_btn.grid(row = 7, column = 2, padx = 10, pady = 20)
        
        # 조회한 도서
        Btreeview = tkinter.ttk.Treeview(book_info,
                                         column = ["B_ISBN", "B_name", "B_author", "B_price", "B_URL", "B_check_rent"],
                                         displaycolumns = ["B_ISBN", "B_name", "B_author", "B_price", "B_URL", "B_check_rent"],
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

        df_book = pd.read_csv('Book.csv', encoding='UTF-8-sig')
        list_from_df_book = (df_book.values).tolist()
        treeValueList = list_from_df_book#도서명, 저자명 검색했을때
        for i in range(len(treeValueList)):
                Btreeview.insert("", "end", text="", values=treeValueList[i], iid=i)
      
       

        # 도서 정보
        def Book_show(event): 
            def change_book(): #도서수정
                if Btextname.get()=='' or Btextauthor.get()=='' or Btextpubli.get()=='': #도서명, 저자, 출판사 하나라도 입력안되면 팝업창
                    messagebox.showinfo("경고,", "필수항목(도서명, 저자, 출판사)을 입력해주세요.\n")
                    return 0
                else:
                    df_rent = pd.read_csv('RENT.csv', encoding='UTF-8-sig')
                    df_rent = df_rent.astype('str')
                    if getValue[0] in df_rent['ISBN'].values:
                        messagebox.showinfo("알림","대여 중인 도서는 삭제할 수 없습니다.")
                        return 0
                    else:
                        try:
                            testimage = Image.open(Btextpicture.get()) 
                            testsize = testimage.size
                            if (testsize[0] <120 or testsize[0] > 135) or (testsize[1] < 160 or testsize[1] > 175) :#사진크기
                                messagebox.showinfo("경고", "지원하는 사진크기 : (120~135, 160~175)")
                                return 0
                            else:
                                df_rent = pd.read_csv('RENT.csv', encoding='UTF-8-sig')
                                if Btextname.get() in df_rent["TITLE"].values:
                                    messagebox.showinfo("경고","대여중인 도서는 수정할 수 없습니다.")
                                    return 0
                                df_book = pd.read_csv('Book.csv', encoding='UTF-8-sig')
                                dropindex = df_book.index[(df_book['ISBN'] == getValue[0])]
                                df_book = df_book.drop(dropindex)
                                df_book.reset_index
                                df_book.to_csv("Book.csv", index = False, encoding= 'UTF-8-sig')
                                rent = '대출가능'
                                readd_book = {"ISBN" : BtextISBN.get(), "TITLE" : Btextname.get(), "AUTHOR" : Btextauthor.get(), "PRICE" : Btextprice.get(), "URL" : BtextURL.get(), "RENT" : rent, "PUB" : Btextpubli.get(), "PICTURE" :  Btextpicture.get()}
                                df_book = df_book.append(readd_book, ignore_index=True)
                                df_book.to_csv("Book.csv", index = False, encoding= 'UTF-8-sig')
                                messagebox.showinfo("알림","도서 수정이 완료되었습니다.")# 팝업창
                        except FileNotFoundError:
                            messagebox.showinfo("경고", "존재하지 않는 사진 형식입니다.")
                            return 0
                
            def delete_book(): # 도서삭제
                df_book = pd.read_csv('Book.csv', encoding='UTF-8-sig')
                dropindex = df_book.index[(df_book['ISBN'] == getValue[0])]
                response = messagebox.askokcancel('알림','도서를 삭제하시겠습니까?')
                if response == 1:
                    df_rent = pd.read_csv('RENT.csv', encoding='UTF-8-sig')
                    if Btextname.get() in df_rent["TITLE"].values:
                        messagebox.showinfo("경고","대여중인 도서는 삭제할 수 없습니다.")
                        return 0
                    df_book = df_book.drop(dropindex)
                    df_book.reset_index
                    df_book.to_csv("Book.csv", index = False, encoding= 'UTF-8-sig')
                    messagebox.showinfo("알림","도서가 삭제되었습니다.") #도서삭제 팝업창
                else:
                    messagebox.showinfo("알림","도서가 삭제가 취소되었습니다.")
                    return 0

            def Bpicturefind() : #수정할 사진 찾기
                files = filedialog.askopenfilenames(title = "도서 사진을 선택하세요", filetypes = (("모든 파일", "*.*"), ("모든 파일", "*.*")), initialdir = r"도서사진")
                if len(files) > 1:
                    messagebox.showinfo("경고", "사진을 하나만 선택 하시오.")
                    return
                try:            #사진 찾는거 취소했을 때, 오류안뜨도록
                    Btextpicture.delete(0, END)
                    Btextpicture.insert(0, files[0])
                except:
                    pass

            df_book = pd.read_csv('Book.csv', encoding='UTF-8-sig')
            selectedItem = Btreeview.focus()
            getValue = Btreeview.item(selectedItem).get('values')
                
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
            BtextISBN.insert(0, getValue[0])
            BtextISBN.grid(row=2, column=1, padx=70, pady = 3)

            Blabelname = Label(book_show_info, text="도서명 : ", fg = "#203864", bg = "white")
            Btextname = Entry(book_show_info)
            Btextname.insert(0, getValue[1])
            Blabelname.grid(row=3, column=0, padx=60, pady = 3)
            Btextname.grid(row=3, column=1, padx=70, pady = 3)

            Blabelauthor = Label(book_show_info, text="저자 : ", fg = "#203864", bg = "white")
            Btextauthor = Entry(book_show_info)
            Btextauthor.insert(0, getValue[2])
            Blabelauthor.grid(row=4, column=0, padx=60, pady = 3)
            Btextauthor.grid(row=4, column=1, padx=70, pady = 3)

            Blabelpubli = Label(book_show_info, text="출판사 : ", fg = "#203864", bg = "white")
            Btextpubli = Entry(book_show_info)
            Btextpubli.insert(0, getValue[6])
            Blabelpubli.grid(row=5, column=0, padx=60, pady = 3)
            Btextpubli.grid(row=5, column=1, padx=70, pady = 3)

            Blabelprice = Label(book_show_info, text="가격: ", fg = "#203864", bg = "white")
            Btextprice = Entry(book_show_info)
            Btextprice.insert(0, getValue[3])
            Blabelprice.grid(row=6, column=0, padx=60, pady = 3)
            Btextprice.grid(row=6, column=1, padx=70, pady = 3)

            BlabelURL = Label(book_show_info, text="관련 URL : ", fg = "#203864", bg = "white") 
            BtextURL = Entry(book_show_info)
            BtextURL.insert(0, getValue[4])
            BlabelURL.grid(row=7, column=0, padx=60, pady = 3)
            BtextURL.grid(row=7, column=1, padx=70, pady = 3)

            Blabelpicture = Label(book_show_info, text = "도서 사진 : ", fg = "#203864", bg = "white")
            Btextpicture = Entry(book_show_info)
            Btextpicture.insert(0, getValue[7])
            Blabelpicture.grid(row=8, column=0, padx=60, pady = 3)
            Btextpicture.grid(row=8, column=1, padx=70, pady = 3)

            Bimg = ImageTk.PhotoImage(file = Btextpicture.get())
            Bimglabel = Label(book_show_info, image=Bimg)
            Bimglabel.place(x=485, y=0)
            
            book_revice_btn = Button(book_show_info, text="수정", command = change_book)
            book_revice_btn.grid(row=10, column=0,padx=60, pady = 5)

            book_delete_btn = Button(book_show_info, text="삭제", command = delete_book)
            book_delete_btn.grid(row=10, column=1,padx=60, pady = 5)

            book_picture_btn = Button(book_show_info, text="찾기", command = Bpicturefind)
            book_picture_btn.place(x=410,y=163)

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
            df_book=pd.read_csv('Book.csv', encoding='UTF-8-sig')
            rent = '대출가능'
            a=1
            add_book = {"ISBN" : BISBN_text1.get(), "TITLE" : Bname_text.get(), "AUTHOR" : Bauthor_text.get(), "PRICE" : Bprice_text.get(), "URL" : BURL_text.get(), "RENT" : rent, "PUB" : Bpubli_text.get(), "PICTURE" : Bpicture_text.get() }
            if Bname_text.get() not in checkbook: #중복확인 버튼 안누르면 팝업창
                messagebox.showinfo("경고","중복확인 하세요.")
                return 0
            if Bname_text.get()=='' or Bauthor_text.get()=='' or Bpubli_text.get()=='': #도서명, 저자, 출판사 하나라도 입력안되면 팝업창
                messagebox.showinfo("경고,", "필수항목(도서명, 저자, 출판사)을 입력해주세요.")
                return 0
            if not Bpicture_text.get() :
                messagebox.showinfo("경고", "사진을 등록하세요")
                return 0
            else:
                #사진크기
                try:
                    testimage = Image.open(Bpicture_text.get())
                    testsize = testimage.size
                    if (testsize[0] <120 or testsize[0] > 135) or (testsize[1] < 160 or testsize[1] > 175) :
                        messagebox.showinfo("경고", "지원하는 사진크기 : (120~135, 160~175)")
                        return 0
                    else:
                        df_book = df_book.append(add_book, ignore_index=True)
                        df_book.to_csv("Book.csv", index = False, encoding= 'UTF-8-sig')
                        messagebox.showinfo("알림","도서 등록이 완료되었습니다.")# 팝업창
                except FileNotFoundError:
                    messagebox.showinfo("경고", "존재하지 않는 사진 형식입니다.")
                    return 0
            checkbook.remove(Bname_text.get()) #중복확인을 위한 리스트 비워주기
        def findpicture() : #사진 찾기
            files = filedialog.askopenfilenames(title = "도서 사진을 선택하세요", filetypes = (("모든 파일", "*.*"), ("모든 파일", "*.*")), initialdir = r"도서사진")
            if len(files) > 1 :
                messagebox.showinfo("경고", "사진을 하나만 선택 하세요.")
                return
            try:
                Bpicture_text.delete(0, END)
                Bpicture_text.insert(0, files[0])
            except:
                pass

        
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

        Bpicture_label = Label(book_add, text="사 진 : ", fg = "#203864", bg = "white") 
        Bpicture_text = Entry(book_add, width = 50) 
        Bpicture_label.grid(row=7, column=0, padx=10, pady = 5)
        Bpicture_text.grid(row=7, column=1, padx=50, pady = 5)
         
        Bpicture_search_btn = Button(book_add, text="찾기", command = findpicture)
        Bpicture_search_btn.grid(row=7, column=2, padx=20, pady = 5)

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
def Rentwindow():
    def rent_book(): 
        brent_info = Frame(Rent_window, borderwidth = 1, relief = "solid")
        brent_info.place(x = 70, y = 120)
        brent_info.configure(background = "white")
        brent_label = Label(brent_info, text = "대여(도서)", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        brent_label.grid(row = 0, column = 1, padx = 80, pady = 10)

        Brent_name_label = Label(brent_info, text = "도서명 : ", fg = "#203864", bg = "white")
        Brent_name_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        Brent_name_text = Entry(brent_info, width = 50)
        Brent_name_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        bsear_btn = Button(brent_info, text = "조회")
        bsear_btn.grid(row = 1, column = 2, padx = 20, pady = 5)

        Brent_treeview = tkinter.ttk.Treeview(brent_info, column = ["BR_name", "BR_author", "BR_publi", "BR_state"],
                                              displaycolumns = ["BR_name", "BR_author", "BR_publi", "BR_state"],
                                              height = 7, show = 'headings')

        Brent_treeview.grid(row = 3, column = 1)
        
        Brent_treeview.column("BR_name", width=150, anchor="center")
        Brent_treeview.heading("BR_name", text="도서명", anchor="center")
        
        Brent_treeview.column("BR_author", width=70, anchor="center")
        Brent_treeview.heading("BR_author", text="저자", anchor="center")

        Brent_treeview.column("BR_publi", width=100, anchor="center")
        Brent_treeview.heading("BR_publi", text="출판사", anchor="center")

        Brent_treeview.column("BR_state", width=80, anchor="center")
        Brent_treeview.heading("BR_state", text="대출상태", anchor="center")

        def rent_show(event):
            rentshow = Toplevel(Rent_window)
            rentshow.resizable(width = False, height = False)
            
            rent_show_label = Label(rentshow, image = rent_wall)
            rent_show_label.pack()

            rent_show_info = Frame(rentshow)
            rent_show_info.place(x = 20, y = 120)
            rent_show_info.configure(background = "white")
            
            BRlabelISBN = Label(rent_show_info, text="ISBN : ", fg = "#203864", bg = "white") 
            BRtextISBN = Entry(rent_show_info)
            BRlabelISBN.grid(row=2, column=0, padx=20, pady = 3)
            BRtextISBN.grid(row=2, column=1, padx=20, pady = 3)
            
            BRlabelname = Label(rent_show_info, text="도서명 : ", fg = "#203864", bg = "white")
            BRlabelname.grid(row=3, column=0, padx=20, pady = 3)
            BRtextname = Entry(rent_show_info)
            BRtextname.grid(row=3, column=1, padx=20, pady = 3)

            BRlabelauthor = Label(rent_show_info, text="저자 : ", fg = "#203864", bg = "white")
            BRtextauthor = Entry(rent_show_info)
            BRlabelauthor.grid(row=4, column=0, padx=20, pady = 3)
            BRtextauthor.grid(row=4, column=1, padx=20, pady = 3)

            BRlabelpubli = Label(rent_show_info, text="출판사 : ", fg = "#203864", bg = "white")
            BRtextpubli = Entry(rent_show_info)
            BRlabelpubli.grid(row=5, column=0, padx=20, pady = 3)
            BRtextpubli.grid(row=5, column=1, padx=20, pady = 3)

            BRlabelprice = Label(rent_show_info, text="가격 : ", fg = "#203864", bg = "white")
            BRtextprice = Entry(rent_show_info)
            BRlabelprice.grid(row=6, column=0, padx=20, pady = 3)
            BRtextprice.grid(row=6, column=1, padx=20, pady = 3)

            BRlabelURL = Label(rent_show_info, text="관련 URL: ", fg = "#203864", bg = "white")
            BRtextURL = Entry(rent_show_info)
            BRlabelURL.grid(row=7, column=0, padx=20, pady = 3)
            BRtextURL.grid(row=7, column=1, padx=20, pady = 3)

            URlabelname = Label(rent_show_info, text="이름 : ", fg = "#203864", bg = "white")
            URlabelname.grid(row=2, column=2, padx=20, pady = 3)
            URtextname = Entry(rent_show_info)
            URtextname.grid(row=2, column=3, padx=20, pady = 3)

            URlabelBirth = Label(rent_show_info, text="생년월일 : ", fg = "#203864", bg = "white")
            URtextBirth = Entry(rent_show_info)
            URlabelBirth.grid(row=3, column=2, padx=20, pady = 3)
            URtextBirth.grid(row=3, column=3, padx=20, pady = 3)

            URlabelHP = Label(rent_show_info, text="전화번호 : ", fg = "#203864", bg = "white")
            URtextHP = Entry(rent_show_info)
            URlabelHP.grid(row=4, column=2, padx=20, pady = 3)
            URtextHP.grid(row=4, column=3, padx=20, pady = 3)

            URlabelGender = Label(rent_show_info, text="성별 : ", fg = "#203864", bg = "white")
            URtextGender = Entry(rent_show_info)
            URlabelGender.grid(row=5, column=2, padx=20, pady = 3)
            URtextGender.grid(row=5, column=3, padx=20, pady = 3)

            URlabelEmail = Label(rent_show_info, text="이메일: ", fg = "#203864", bg = "white")
            URtextEmail = Entry(rent_show_info)
            URlabelEmail.grid(row=6, column=2, padx=20, pady = 3)
            URtextEmail.grid(row=6, column=3, padx=20, pady = 3)

            labelreturnday = Label(rent_show_info, text="반납 예정일: ", fg = "#203864", bg = "white")
            textreturnday = Entry(rent_show_info)
            labelreturnday.grid(row=8, column=0, padx=20, pady = 3)
            textreturnday.grid(row=8, column=1, padx=20, pady = 3)

            labelreturncheck = Label(rent_show_info, text="반납여부: ", fg = "#203864", bg = "white")
            textreturncheck = Entry(rent_show_info)
            labelreturncheck.grid(row=8, column=2, padx=20, pady = 3)
            textreturncheck.grid(row=8, column=3, padx=20, pady = 3)

            book_delete_btn = Button(rent_show_info, text="대출완료")
            book_delete_btn.grid(row=10, column=1,padx=10, pady = 5)

            book_exit_btn = Button(rent_show_info, text="닫기", command=lambda: rentshow.destroy())
            book_exit_btn.grid(row=10, column=2, padx=10, pady = 5)

        brent_check_btn = Button(brent_info, text= "선택")
        brent_check_btn.grid(row = 4, column = 1, padx = 20, pady = 20)

        brent_exit_btn = Button(brent_info, text="닫기", command=lambda: brent_info.destroy())
        brent_exit_btn.grid(row=4, column=2, padx=20, pady = 5)

        Brent_treeview.bind('<Double-1>', rent_show) # 목록에서 선택하고 버튼 클릭..?


    def rent_user(): # 대여 가능 여부 확인
        Urent_info = Frame(Rent_window, borderwidth = 1, relief = "solid")
        Urent_info.place(x = 45, y = 120)
        Urent_info.configure(background = "white")
        urent_label = Label(Urent_info, text = "대여(회원)", font = ("맑은 고딕", 20), fg = "#203864", bg = "white")
        urent_label.grid(row = 0, column = 1, padx = 80, pady = 10)

        Urent_name_label = Label(Urent_info, text = "회원명 : ", fg = "#203864", bg = "white")
        Urent_name_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        Urent_name_text = Entry(Urent_info, width = 50)
        Urent_name_text.grid(row = 1, column = 1, padx = 10, pady = 5)
        usear_btn = Button(Urent_info, text = "조회")
        usear_btn.grid(row = 1, column = 2, padx = 20, pady = 5)

        Urent_treeview = tkinter.ttk.Treeview(Urent_info,
                                              column = ["UR_name", "UR_birth", "UR_phone", "UR_gender", "UR_email", "UR_state"],
                                              displaycolumns = ["UR_name", "UR_birth", "UR_phone", "UR_gender", "UR_email", "UR_state"],
                                              height = 7, show = 'headings')

        Urent_treeview.grid(row = 3, column = 1)
        
        Urent_treeview.column("UR_name", width=50, anchor="center")
        Urent_treeview.heading("UR_name", text="이름", anchor="center")

        Urent_treeview.column("UR_birth", width=100, anchor="center")
        Urent_treeview.heading("UR_birth", text="생년월일", anchor="center")

        Urent_treeview.column("UR_phone", width=100, anchor="center")
        Urent_treeview.heading("UR_phone", text="전화번호", anchor="center")

        Urent_treeview.column("UR_gender", width=40, anchor="center")
        Urent_treeview.heading("UR_gender", text="성별", anchor="center")

        Urent_treeview.column("UR_email", width=100, anchor="center")
        Urent_treeview.heading("UR_email", text="이메일", anchor="center")

        Urent_treeview.column("UR_state", width=70, anchor="center")
        Urent_treeview.heading("UR_state", text="대출상태", anchor="center")

        Urent_check_btn = Button(Urent_info, text= "선택")
        Urent_check_btn.grid(row = 4, column = 1, padx = 20, pady = 20)

        Urent_exit_btn = Button(Urent_info, text="닫기", command=lambda: Urent_info.destroy())
        Urent_exit_btn.grid(row=4, column=2, padx=20, pady = 5)


    def rent_return():
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

        Urent_check_btn = Button(rent_info, text= "반납")
        Urent_check_btn.grid(row = 4, column = 1, padx = 20, pady = 20)

        Urent_exit_btn = Button(rent_info, text="닫기", command=lambda: rent_info.destroy())
        Urent_exit_btn.grid(row=4, column=2, padx=20, pady = 5)

    
    Rent_window = Toplevel(window)
    Rent_window.geometry("700x500")
    Rent_window.resizable(width = False, height = False)

    rent_wall_label = Label(Rent_window, image = de_wall)
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
window.resizable(width = False, height = False)

wall = PhotoImage(file = "메인 화면.png")
book = PhotoImage(file = "회원.png")
user = PhotoImage(file = "책.png")
rent = PhotoImage(file = "대여.png")

de_wall = PhotoImage(file = "기본 배경.png")
user_wall = PhotoImage(file = "회원 정보.png")
book_wall = PhotoImage(file = "도서 정보.png")
rent_wall = PhotoImage(file = "대여 정보.png")

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
