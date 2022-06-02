import pandas as pd
import numpy as np
from tkinter import*
import tkinter.ttk
import warnings
from tkinter import messagebox
import datetime as dt
warnings.filterwarnings('ignore')

df2=pd.read_csv('C:/Users/user/OneDrive/바탕 화면/BOOK.csv', encoding='euc-kr')

class Book:
    
    def __init__(self,book): #생성자
        self.__book=book #self.__ : private
    def get_Isbnlist(self): #접근자
        return self.__book[:0]

    #def get_AllInfo(self): # 저장할 때 정보를 전부 불러오는 용도, 우선은 사용하지 않아 더미 데이터 처리
        #return self.__book

    def save_to_csv(self): # 변동사항 생길 때마다 저장(IF-007)
        book_col=["ISBN","TITLE","AUTHOR","PUB","PRICE","LINK","DESCRIP","PRE"] # 열 이름
        bookdf=pd.DataFrame(self.__book, columns=book_col) # numpy 배열을 DataFrame 형식으로 변환
        bookdf.to_csv('C:/Users/user/OneDrive/바탕 화면/Book.csv', encoding='euc-kr') # to_csv는 numpy 배열에서 작동하지 않아 DataFrame으로 변환한 것
    
    def get_IsIn(self,isbn): # isbn이 안에 있는가 확인 (IF-001)
        if isbn in self.__book[:,0]: # 있으면 True 반환
            return True
        else:
            return False
    
    def add_Book_Info(self,inf): # 도서 등록 (IF-002)
        self.__book=np.append(self.__book,inf,asix=0)# 행 방향으로 정보 추가
        self.save_to_csv()
        
    def get_Book_info(self,isbn): # 책 정보 확인
        ind=np.where(self.__book[:,0]==isbn)#내부 인덱스를 찾아냄
        return self.__book[ind,:]# 인덱스에 해당하는 책 정보를 리턴

    def get_IsRented(self,isbn):#IF-008
        ind=np.where(self.__book[:,0]==isbn)#내부 인덱스를 찾아냄
        return self.__book[ind,7]
    def set_IsRented(self,isbn,rt):#IF-009
        ind=np.where(self.__book[:,0]==isbn)#내부 인덱스를 찾아냄
        self.__book[ind,7]=rt
        self.save_to_csv()
        
    def search_Book_ByTitle(self,title): # 책 제목으로 검색 (IF-003)
        """
        for s in len(str(title)): # 검색된 문자열을 문자열 길이만큼 반복문으로 돌림
            stitle+=s # 반복하며 문자열이 추가 됨
            if self.__book[:,1].at(stitle): # 만약 반복하다가 같은 문자열이 발견된다면
                ind=np.where(self.__book[:,1]==stitle) # 일단 인덱스를 가져옴
                if isChecked.at(ind): # 만약 이미 확인한 인덱스면
                    continue # 넘어감
                isChecked=np.append(isChecked,ind) # 확인을 했다는 의미로 추가
                search_list=np.append(search_list,self.__book[ind,:])# 제목이 유사하므로 리스트에 추가
        return search_list # 비슷한 문자열을 가진 도서목록을 출력해줌 

        """
        search_list=np.array([])# 검색된 책 정보 저장할 리스트
        found_ind=np.where(self.__book[:,1]==title)
        for i in found_ind:
            search_list=np.append(search_list,self.__book[i,:])# 제목이 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list # 반환 값 : 도서 목록
    # 일부만 일치해도 검색할 수 있게 개선 필요함
    
    def search_Book_ByAuthor(self,author): # 책 저자로 검색 (IF-004)
        search_list=np.array([])# 검색된 책 정보 저장할 리스트
        found_ind=np.where(self.__book[:,2]==author)
        for i in found_ind:
            search_list=np.append(search_list,self.__book[i,:])# 저자가 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list # 반환 값 : 도서 목록
    
    def set_Book_Info(self,inf): # 도서 수정 (IF-005)
        ind=np.where(self.__book[:,0]==inf[0])#내부 인덱스를 찾아냄
        self.__user[ind,:]=inf# 인덱스 값에 해당하는 책 정보 삽입
        self.save_to_csv()
   
    def drop_Book_Info(self,isbn): # 도서 삭제 (IF-006)
        ind=np.where(self.__book[:,0]==isbn)#내부 인덱스를 찾아냄
        self.__book=np.delete(self.__book,ind)# 인덱스 값에 해당하는 정보 삭제
        self.save_to_csv()

class Rent:
    def __init__(self,rent): # 생성자
        self.__rent=rent
            
    def save_to_csv(self): # 변동사항 생길 때마다 저장
        rent_col=["SEQ","ISBN","PHONE","DATE","RETURN_DATE","RETURN_YN"]
        rentdf=pd.DataFrame(self.__rent, columns=rent_col)
        rentdf.to_csv('C:/Users/user/OneDrive/바탕 화면/Rent.csv', encoding='UTF-8')
        
    def get_Rent_Info(self,ind):#실제 인덱스 번호가 아니라 대출 테이블 내에 저장된 인덱스 번호를 넣을 것
        return self.__rent[ind-1,:]
    
    def rent_Book(self,isbn,phone,dat): # 도서대출  (IF-019)
        add_info=np.array([int(self.__rent.size/6)+1,isbn,phone,dat,dat+dt.timedelta(days=14),False])# 대출 정보를 numpy 형태로 변환
        self.__rent = np.append(self.__rent,add_info,axis=0)# 대출 목록에 추가
        self.save_to_csv()
        
    def search_Rent_ByBook(self,isbn): # ISBN으로 대출 조회 (IF-020)
        search_list = np.array([]) # 검색된 대출 정보 저장할 리스트
        found_ind = np.where(self.__rent[:,1]==isbn)
        for i in found_ind:
            search_list = np.append(search_list,self.__user[i,:])# ISBN이 동일하면 리스트에 추가
        search_list = np.reshape(search_list,(int(search_list.size/6),6))
        return search_list # 반환 값 : 대출 목록

    def search_Rent_ByUser(self, phone): # 연락처로 대출 조회 (IF-021)
        search_list = np.array([]) # 검색된 대출 정보 저장할 리스트
        found_ind = np.where(self.__rent[:,2] == phone)
        for i in found_ind:
            search_list = np.append(search_list,self.__user[i,:])# 연락처가 동일하면 리스트에 추가
        search_list = np.reshape(search_list,(int(search_list.size/6),6))
        return search_list # 반환 값 : 대출 목록
        
    def back_Book(self,ind): # 도서 반납 (IF-022)
        self.__rent[ind-1,5] = True # 인덱스 값에 해당하는 대출 반납처리
        self.save_to_csv()


    def update_rent_situation(ind): # 선택 버튼을 눌렀을 시에 대출 상태가 대출중으로 바뀌어 저장되게하고, 대출 정보 화면을 띄어주게 하는 메소드
        if BO.get_IsRented(ind):#BO.get_IsRented(ind)
            messagebox.showinfo("경고","이미 대출 중인 도서입니다.")
        #else:
            #book_list[ind,8]==TRUE
            
        #rent_show 클래스를 불러와야 함 ( 대출 정보 화면 띄워주기 ) -> gui

    #def get_book(ind): # 도서 정보를 불러오는 메소드
        #BO.get_Book_info(ind)


book_list=np.array([])
book_list=np.append(book_list,df2)
book_list=np.reshape(book_list,(int(book_list.size/9),9))
book_list=book_list[:,1:]

BO=Book(book_list)

def Book_Search():

    #def get_book_show(): # 도서 조회시 도서를 선택했을 때 book show 클래스를 불러오는 메소드 -> gui?
        #book_show.print_book_info() # 조회한 책의 정보를 출력하는 메소드
        #gui 불러오는 거니까 건드리지 않아도 됨

    def print_book_list(): # 도서 조회시 관련 도서의 리스트를 화면에 출력해주는 메소드
        #treeview랑 연계 
        searched_list=np.array([])
        if text_book_name.get(): # 도서명이 입력된 경우
            searched_list=BO.search_Book_ByTitle(text_book_name.get()) # 제목으로 도서 검색하는 함수 호출
        elif text_author.get(): # 저자명이 입력된 경우
            searched_list=BO.search_Book_ByAuthor(text_author.get()) # 책 저자로 검색하는 함수 호출
        else:
            messagebox.showinfo("경고","도서명과 저자명 둘 중 하나라도 입력하시오")
        treeview.delete(*treeview.get_children())#treeview 전체를 지우는 문장
        #treeview에 넣을 데이터 정제 과정
        #treeV=[[for i in range(8)] for j in range(int(searched_list.size)/8)]#2차원 배열
        for i in range(int(searched_list.size/8)):
            treeV=[]#
            if searched_list[i,7]:#대출 여부에 따라 문장을 다르게 삽입
                treeV.append("X")
            else:
                treeV.append("대출 중")
            for j in range(1,6):#대출여부 외에는 배치순서 동일하니 for문 처리
                treeV.append(searched_list[i,j-1])
            treeview.insert("", "end", text="", values=treeV, iid=i)
            treeview.bind("<Double-1>", Book_Show)


## 함수
## 조회 등록 수정

## 프레임 닫고싶은데..
## def frameexit(frame):
##    frame.grid_forget()

#회원
def Userwindow():
    def Usersearch():
        user_info = Frame(User_window, borderwidth = 1, relief = "solid")
        user_info.place(x = 30, y = 120)
        user_info.configure(background = "white")
        # font 한글도 가능한건가...
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
        usear_btn = Button(user_info, text = "조회")
        usear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)
        
        # 조회한 회원
        Utreeview = tkinter.ttk.Treeview(user_info,
                                         column = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check", "U_check_for_exit"],
                                         displaycolumns = ["U_name", "U_birth", "U_hp", "U_gender", "U_email", "U_check", "U_check_for_exit"])

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

        Utreeview.column("U_check_for_exit", width=70, anchor="center")
        Utreeview.heading("U_check_for_exit", text="탈퇴여부", anchor="center")

        Utreeview["show"] = "headings"

        # 값이 나오면 어찌되려나...
        # 정보 창으로 나와야하네... 추가해야함

    def Useradd():
        user_add = Frame(User_window, borderwidth = 1, relief = "solid")
        user_add.place(x = 30, y = 120)
        user_add.configure(background = "white")
        # font 한글도 가능한건가...
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
        Uphone_check_btn.grid(row=3, column=2, padx=20, pady = 5)


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
        
        Upicture_search_btn = Button(user_add, text="찾기")
        Upicture_search_btn.grid(row=6, column=2, padx=20, pady = 5)

        user_add_btn = Button(user_add, text= "등록")
        user_add_btn.grid(row = 7, column = 2, padx = 20, pady = 20)

        
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
    def Rent_User_Search():
    
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
        usear_btn = Button(Rent_user_info, text = "조회")
        usear_btn.grid(row = 2, column = 2, padx = 20, pady = 5)
        
        # 조회한 회원
        Utreeview = tkinter.ttk.Treeview(Rent_user_info,
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
        Utreeview.heading("U_check", text="대출여부", anchor="center")
        Utreeview.column("U_check_exit", width=70, anchor="center")
        Utreeview.heading("U_check_exit", text="탈퇴여부", anchor="center")
                          
        Utreeview["show"] = "headings"
        df_user = pd.read_csv('C:/Users/user/OneDrive/바탕 화면/User (2).csv', encoding = 'cp949')
        list_from_df_user = df_user.values.tolist()
        
        for i in range(len(df_user)):
            list_from_df_user[i] = list_from_df_user[i][1:]
            Utreeview.insert("", "end", text = "", values=list_from_df_user[i], iid = i)
            
            
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
        bsear_btn = Button(brent_info, text = "조회",command = Book_Search)
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

        df_book = pd.read_csv('C:/Users/user/OneDrive/바탕 화면/BOOK.csv', encoding = 'euc-kr')
        list_from_df_book = df_book.values.tolist()
        
        for i in range(len(df_book)):
            list_from_df_book[i] = list_from_df_book[i][2:4]
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
    rent_btn1 = Button(rent_menu, text = "대여(회원)", width = 25, font = ("맑은 고딕", 12), fg = "#203864", bg = "white", command = Rent_User_Search)
    rent_btn2 = Button(rent_menu, text = "조회 / 반납", width = 25, font = ("맑은 고딕", 12), fg = "#203864", bg = "white", command = rent_return)
    
    rent_btn.grid(row = 0, column = 0)
    rent_btn1.grid(row = 0, column = 1)
    rent_btn2.grid(row = 0, column = 2)


window = Tk()
window.geometry("700x500")

wall = PhotoImage(file = "C:/Users/user/OneDrive/바탕 화면/새 폴더/도서관리(gui)/메인 화면.png")
book = PhotoImage(file = "C:/Users/user/OneDrive/바탕 화면/새 폴더/도서관리(gui)/회원.png")
user = PhotoImage(file = "C:/Users/user/OneDrive/바탕 화면/새 폴더/도서관리(gui)/책.png")
rent = PhotoImage(file = "C:/Users/user/OneDrive/바탕 화면/새 폴더/도서관리(gui)/대여.png")

user_wall = PhotoImage(file = "C:/Users/user/OneDrive/바탕 화면/새 폴더/도서관리(gui)/기본 배경.png")
# X = PhotoImage(file = "X.png")
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
