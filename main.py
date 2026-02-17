import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtCore import QDate
import pickle
import datetime
import random
import os





class Session:
    """
    When a user login successfully that user become the Session Object.
    """
    usr = None
    flag = False



class Auth:
    def __init__(self, usr = None, pas = None, flag = False, name = None, lastname = None):
        self.usr = usr
        self.pas = pas
        self.flag = flag
        self.name = f"{name} {lastname}"


class Signin(Auth):
    """
    Users are saved in a file as a dictionary
    users_dir.txt:
    Username --> {on going: [], history: [], info: {name: "", usr: "", pas: ""}, balance: int}
    """
    def dir_signer(self):
        try: #If the file is empty dosnt crash
            users: dict = user.lloader("users_dir") 
        except:
            users = {}
        self.name = f"{window6.name.text()} {window6.lastname.text()}"
        self.usr = window6.username.text()
        self.pas = window6.pas.text()
        info = {"name":self.name, "usr":self.usr, "pas":self.pas}
        users[self.usr] = {"on going": [], "history": [], "info":info ,"balance": 1500}
        with open(resource_path("data", "users_dir.txt"), "wb") as f:
            pickle.dump(users, f)

    def user_signer(self):
        """
        users.txt:
        {user: pas}
        This methode is not safe, I would add hash for the password
        """
        try: #If the file is empty dosnt crash
            users: dict = login.secret() 
        except:
            users = {}
        self.usr = window6.username.text()
        self.pas = window6.pas.text()
        if users.get(self.usr, None) == None:
            users[self.usr] = self.pas
            user.dumper("users", users)
            signin.dir_signer()
            window6.close()
            window1.show()
        else:
            window7.show()

    def main_signer(self):
        window6.show()
        



class Login(Auth):

    def secret(self):
        with open(resource_path("data", "users.txt"), "rb") as file:
            id = pickle.load(file) 
        return id

    def main_log(self):
        self.usr = window1.usrname.text()
        self.pas = window1.passwd.text()
        users = self.secret() #all the users are here, Again this is not safe.

        if users.get(self.usr) == self.pas:
            self.flag = True

        log = f"{self.usr} --> {self.pas}, {datetime.datetime.now()}, {self.flag}\n"
        with open(resource_path("data", "log.txt"), 'a') as f:
            f.write(log)

        if self.flag:
            Session.usr = self.usr
            Session.flag = self.flag
            window1.close()
            window3.mainlog.clear()
            window3.balance_dis.clear()
            window2.show()
            hotel.date_checker()  #Checks for expired reservations
        else:
            window9.show()




class Hotel(Auth):
    """
    Here you can find the Servers functions
    These are related to rooms and nott to clients
    """



    def room_finder(self, city, enter_time, exit_time, amount):  #AI was here before :), AI's idea was better for overlapping
        with open(resource_path("data", f"{city}.txt"), "rb") as f:
            data = pickle.load(f)

        all_rooms: list = data[2]
        reservations = data[1]
        available_rooms = set()  
        available = []
        enter = int(enter_time.replace("-", ""))
        exit = int(exit_time.replace("-", ""))

        for room in all_rooms:
            room_num = room[0]
            room_capacity = room[1]
            if str(amount) != "0" and room_capacity != str(amount):
                continue
            overlap = False
            for res in reservations:
                r_num, r_enter, r_exit, r_id = res
                if r_num != room_num:
                    continue
                ren = int(r_enter.replace("-", ""))
                rex = int(r_exit.replace("-", ""))
                if (enter < rex and ren < exit): #Check for overlapping rooms
                    overlap = True
                    break
            if not overlap:
                available_rooms.add(room_num)

        for i in available_rooms:
            available.append([i, user.generate_reserve_code()])

        return available

    def inputer(self):
        return  ( window2.des.currentText(),
        window2.date_enter.date().toString("yyyy-MM-dd"),
        window2.date_exit.date().toString("yyyy-MM-dd"),
        window2.passengers.text() )

    def founded_rooms(self):
        des, date_enter, date_exit, amount = hotel.inputer()
        rooms: list = self.room_finder(des, date_enter, date_exit, amount)  #rooms -> [room number, reserve number]
        self.rooms = rooms

    def myroom(self):
        window3.show()
        users: dict = user.lloader("users_dir")
        balance: int = users.get(Session.usr).get('balance', 0) 
        window3.balance_dis.clear()
        window3.balance_dis.append(str(balance))
        window3.namelog.clear()
        window3.namelog.append(f"{Session.usr}  :وارد شده به عنوان ")

    def printer_rooms(self):
        """
        appear the rooms on reserve window if there is any
        """
        self.founded_rooms()
        rooms = self.rooms
        window4.show()
        window2.close()
        window4.main_log.clear()
        des, date_enter, date_exit, amount = hotel.inputer()
        des_f: dict = user.lloader(des)
        all_rooms: list = des_f[2]

        if len(rooms) != 0:
            window4.main_log.append("  شماره رزرو                                                        قیمت    |   مقصد   |  زمان خروج  →  زمان ورود | ظرفیت اتاق    ") #This part is not compatible with the UI.
            for room in rooms:
                for r in all_rooms:
                    if r[0] == room[0]:  #Checks for room number
                        amount = r[1]  #if the amount == 0(user wanted to check for every room) the amount will not be true, so it checks it
                        Oprice = r[2]
                        delta = user.date_d(date_enter, date_exit)
                        price = Oprice * delta
                        max_price = window2.max_price.text()
                        if (max_price == None) or (max_price == "") or (price <= int(max_price)):
                            window4.main_log.append(f"    {room[1]}                                                          {price}  |  {des}   |   {date_exit} → {date_enter}   |   {amount} ")
        else:
            window4.main_log.append("در تاریخ انتخاب شده اتاقی وجود ندارد.")

    def back_to_search(self):
        window4.close()
        window2.show()

    def reserve_number(self):
        return window4.res_num.text()
    
    def reserve_checker(self) -> bool:
        """
        Checks if the reserve number input available or not.
        """
        for room in self.rooms:
            if str(room[1]) == str(self.reserve_number()):
                return True
        return False


    def main_reserve(self):
        """
        obvously its not main, actually prints reserve results
        """
        window4.close()
        window5.log_conf.clear()
        window5.show()
        if self.reserve_checker():
            window5.log_conf.append(f"در حال پردازش رزرو اتاق با شماره رزور {self.reserve_number()} ...\n هزینه رزور: {user.room_price()}")
        else:            
            window5.log_conf.append("شماره اتاقی که  دنبال آن میگردید وجود ندارد!")


    def date_checker(self):
        """
        When a user logs in this function it shows the expired reserves or notify the user about them if there is any.
        Expired, Exp_soon : lists
        serach in user history and checks the exit date with today.
        """
        def expired_shower(expired: list, exp_soon: list):
            """makes the notify page"""
            window10.notife.clear()
            if (expired or exp_soon):
                window10.show()
                if expired:
                    window10.notife.append("--رزرو هایی که منقضی شده--")
                    for exp in expired:
                        window10.notife.append(f"رزرو شما به شماره {exp.get('reserve_number')} منقضی شده است.")
                    window10.notife.append('\n')
                if exp_soon:
                    window10.notife.append("--رزرو هایی که به زودی منقضی میشوند--")
                    for exp in exp_soon:
                        window10.notife.append(f"رزور شما به {exp.get('reserve_number')} ، به مقصد {exp.get('des')} ، در تاریخ {exp.get('d_exit')} منقضی خواهد شد.")
                window10.notife.append("\nاگر فکر میکنید مشکلی پیش امده با پشتیبانی تماس بگیرید.")
            else:
                return

        with open(resource_path("data", "users_dir.txt"), 'rb') as f:
            users_dir: dict = pickle.load(f)
        muser: dict  = users_dir.get(Session.usr)
        on_going: list = muser.get('on going')
        history: list = muser.get('history')
        expired = []
        exp_soon = []
        for room in on_going[:]:
            if room.get('d_exit') == str(datetime.datetime.today().date()):
                exp_soon.append(room)
            
            elif int(str(room.get('d_exit')).replace("-",'')) < int(str(datetime.datetime.today().date()).replace("-",'')):
                expired.append(room)
                on_going.remove(room)
                history.append(room)
                history[-1]['status'] = 'تمام شده'  #I really dont remmeber how did I put [-1] and it works. lets just try not to touch.
        muser['on going'] = on_going
        muser['history'] = history
        users_dir[Session.usr] = muser
        with open(resource_path("data", "users_dir.txt"), 'wb') as f:
            pickle.dump(users_dir, f)

        expired_shower(expired, exp_soon)


        
    def cancel_checker(self) -> bool:
        """
        Not only a checker, but also changes the reserve status to "canceled" and moves the reserve from "on going" to "history"
        """
        cancel_num = window3.cancel_num.text()
        users: dict = user.lloader("users_dir")
        on_going: list = users[Session.usr]["on going"]
        history: list = users[Session.usr]['history']
        for room in on_going[:]:
            room: dict
            if str(room.get('reserve_number')) == str(cancel_num):
                try:
                    money = int(room.get('price')/2)  #returns half of the price 
                except TypeError:
                    money = 0
                des: str = room.get('des')  #destination name
                on_going.remove(room)
                history.append(room)
                history[-1]['status'] = "کنسل شده"
                users[Session.usr]['on going'] = on_going   #updates on going and history
                users[Session.usr]['history'] = history     #...   
                user.dumper("users_dir", users)
                self.des_cancel(des)
                today = datetime.datetime.today().date()
                enter_date = room.get('d_enter', today)
                if user.date_d(today, enter_date) >= 2:   #Checks for the 48 hour time
                    if user.money_retuner(money):    #if the money == 0: upper if, will do this statment's job
                        window8.cancel_text.append(f"مبلغ {money} به دلیل باقی ماندن بیش از 48 ساعت از رزرو به حسابتان بازگشت.")
                return True
        return False
    
    def canceler(self):
        """
        This only shows the user that cancalation was sueccessfull or not.
        """
        window3.close()
        window8.cancel_text.clear()
        window8.show()
        if hotel.cancel_checker():
            window8.cancel_text.append(f"رزرو به شماره {window3.cancel_num.text()} کنسل شد.")
        else:
            window8.cancel_text.append(f"رزروی به شماره {window3.cancel_num.text()} ندارید.")

    def des_cancel(self, destination):
        """
        Deletes the canceled reserve on the destination file
        """
        des = user.lloader(f"{destination}")
        cancel_num = window3.cancel_num.text()
        rez = des[1]
        for room in rez:
            if str(cancel_num) == str(room[3]):
                rez.remove(room)
                des[1] = rez
                user.dumper(destination, des)
                return
        print("ERROR in saving rooms in des")  #This Error would not happen(Prevented it before happening.)



class User(Auth):
    """
    Execpt on lloader and dumper, Here are Client side functions
    """

    def lloader(self, Fname):
        with open(resource_path("data", f"{Fname}.txt"), 'rb') as f:
            return pickle.load(f)

    def dumper(self, Fname, data):
        with open(resource_path("data", f"{Fname}.txt"), 'wb') as f:
            pickle.dump(data, f)

    def generate_reserve_code(self) -> int:  #AI was also here, the uuid idea was better than my random.randint idea
        users = self.lloader("users_dir")
        existing_codes = set()
        for uid in users.values():
            for r in uid["on going"]:
                existing_codes.add(str(r["reserve_number"]))
            for r in uid["history"]:
                existing_codes.add(str(r["reserve_number"]))
        while True:
            code = str(random.randint(10000, 99999))
            if code not in existing_codes:
                return code

    def money_retuner(self, money):
        """
        calculate and return the money that should be returned.
        """
        users = self.lloader("users_dir")
        balance = users[Session.usr]['balance']
        balance +=  money
        users[Session.usr]['balance'] = balance
        self.dumper("users_dir", users)
        window3.balance_dis.clear()
        window3.balance_dis.append(str(balance))
        return money




    def date_d(self, t_start, t_finish): #List comperhension Skills HAHAHA
        """
        calculate the time diffrence
        it was a shame that didnt used datetime.delta
        t_start and finish : "yyyy-mm-dd"
        """
        t1 = str(t_start).split('-')
        t2 = str(t_finish).split('-')

        a = [int(x) for x in t1]
        b = [int(x) for x in t2]
        res = [b[i]-a[i] for i in range(3)]
        res = [res[0]*12*30, res[1]*30, res[2]]
        x = 0
        for i in res:
            x += i
        return abs(x)

    def room_price(self):
        """
        calculate the price using room's price for every night and the date_delta function
        ... --> price
        """
        days = self.date_d(window2.date_enter.date().toString("yyyy-MM-dd"), window2.date_exit.date().toString("yyyy-MM-dd"))
        reserve_number = hotel.reserve_number()

        for room in hotel.rooms:
            if room[1] == reserve_number:
                room_number = str(room[0])
        des = window2.des.currentText()
        des_file = self.lloader(des)
        price = 0
        for r in des_file[2]:
            if r[0] == room_number:
                price = r[2] #des_file[2] = [['1', '10', 150], ['2', '2', 20], ['3', '1', 10], ['4', '3', 45]]  #Room num/amount/price   #This is awful BTW it is what it is.
                break
        return days*price
        

    def balance_checker(self, price) -> bool:
        users_dir : dict = self.lloader("users_dir")
        muser : dict = users_dir.get(Session.usr)
        balance = muser.get("balance")
        return (balance >= price)

    def reserve(self):
        """
        It was better to break this function to other functions and connects them
        """
        def room_remover(des_file):
            des_file[1].append([str(room_number), date_enter, date_exit, str(reserve_number)])
            try: #There are some reserved room that can be reserved in another time
                des_file[0].remove(str(room_number))
            except:
                pass
            with open(resource_path("data", f"{des}.txt"), "wb") as f:
                pickle.dump(des_file, f)

        if hotel.reserve_checker():
            des, date_enter, date_exit, amount = hotel.inputer()
            reserve_number = hotel.reserve_number()
            des_file = self.lloader(des)
            all_rooms = des_file[2]
            
            for room in hotel.rooms:
                if room[1] == reserve_number:
                    room_number = str(room[0])  #Finds the room number from reserve number
                    for r in all_rooms:         #finds the amount from the destination file
                        if r[0] == room[0]:
                            amount = r[1]

            users = self.lloader("users_dir")
            info: dict = users.get(Session.usr)
            price = self.room_price()
            
            if user.balance_checker(price):
                if info:#Checks if user exist in users_dir
                    reserve_info = {"reserve_number": reserve_number, "d_enter": date_enter, "d_exit": date_exit, "des": des, "amount": amount, "room_number": room_number, 'price': price}  #Here is How the data saves in history/on going
                    going: list = info.get("on going")
                    going.append(reserve_info)
                    
                    info['balance'] -= price
                    info["on going"] = going
                    users[Session.usr] = info
                    
                    room_remover(des_file)
                    self.dumper("users_dir", users)
                else:
                    print(f"ERROR in reserving for {Session.usr}")

        reenter.after_res()


    def on_going(self):
        """
        prints on going for logged user
        """
        users = self.lloader("users_dir")
        on_going = users[Session.usr]["on going"]
        window3.mainlog.append("--رزور های پیش رو--")
        if on_going:
            window3.mainlog.append("شماره رزرو | مقصد | تاریخ خروج | تاریخ ورود | ظرفیت اتاق")
            for r in on_going:
                window3.mainlog.append(f"{r['reserve_number']}     |   {r['des']}   | {r['d_exit']} → {r['d_enter']} | {r['amount']}")
        else:
            window3.mainlog.append("به نظر میرسه رزوری ندارید")


    def history(self):
        """
        same as on going
        """
        users = self.lloader("users_dir")
        history = users[Session.usr]["history"]

        window3.mainlog.append("--تاریخچه رزرو ها--")
        if history:
            window3.mainlog.append("شماره رزرو | مقصد | تاریخ خروج | تاریخ ورود | وضعیت")
            for r in history:
                window3.mainlog.append(f"{r['reserve_number']} | {r['des']} | {r['d_exit']} → {r['d_enter']}, {r['status']}")
        else:
            window3.mainlog.append("به نظر میرسه رزوری ندارید")




class Reenter(Auth):
    """
    This class mostly use for switching between windows.
    """

    def logout(self):
        for w in windows:
            w.close()
        window1.show()

    def after_res(self):
        window5.close()
        if hotel.reserve_checker():
            reserve_number = hotel.reserve_number()
            des, date_enter, date_exit, amount = hotel.inputer()
            des_file = user.lloader(des)
            price = 0
                    
            price = user.room_price()
            if user.balance_checker(price):
                window3.mainlog.clear()
                window3.show()
                window3.mainlog.append(f"شماره رزور: {window4.res_num.text()} با موفقیت انجام شد.\n ")
                hotel.myroom()
            else:
                window11.show()
                window11.textBrowser.clear()
                window11.textBrowser.append("موجودی حسابت برای این سفارش کافی نیست! \n میتونی حسابتو شارژ کنی و مجددا این رزرو رو انجام بدی.")

        else:
            window2.show()

    def after_cnl(self):
        window8.close()
        window3.mainlog.clear()
        window3.show()


    def balance(self):
        users = user.lloader("users_dir")
        users[Session.usr]['balance'] += 100
        user.dumper("users_dir" ,users)
        users = user.lloader("users_dir")
        window3.balance_dis.clear()
        window3.balance_dis.append(str(users[Session.usr]['balance']))

    def back_to_search(self):
        window3.close()
        window2.show()

    def low_balance(self):
        window11.close()
        hotel.myroom()
        window3.mainlog.clear()
        window3.mainlog.append(f"موجودی شما برای رزرو به شماره {hotel.reserve_number()} کافی نبود.")




#Objects are deployed here
hotel = Hotel()
user = User()
login = Login()
reenter = Reenter()
signin = Signin()




#AI was here before
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def resource_path(*paths):
    return os.path.join(BASE_DIR, *paths)



app = QApplication(sys.argv)
loader = QUiLoader()

#Here are the windows and their UI file
#It was better to write them in a class
#But now I nearly used windows for 300 times, so I will not be able to fix them all


ui_file1 = QFile(resource_path("ui", "lg.ui"))
ui_file1.open(QFile.ReadOnly) 
window1 = loader.load(ui_file1)
ui_file1.close()
window1.action.clicked.connect(login.main_log)
window1.sign.clicked.connect(signin.main_signer)

ui_file2 = QFile(resource_path("ui", "htl.ui"))
ui_file2.open(QFile.ReadOnly) 
window2 = loader.load(ui_file2)
today = QDate.currentDate()
window2.date_enter.setMinimumDate(today)
window2.date_exit.setMinimumDate(today.addDays(1))  #add one day more than enter to exit
window2.date_enter.dateChanged.connect(
    lambda d: window2.date_exit.setMinimumDate(d.addDays(1)) 
)
window2.myrooms.clicked.connect(hotel.myroom)
window2.main_find.clicked.connect(hotel.printer_rooms)
ui_file2.close()

ui_file3 = QFile(resource_path("ui", "myrms.ui"))
ui_file3.open(QFile.ReadOnly) 
window3 = loader.load(ui_file3)
window3.logout.clicked.connect(reenter.logout)
window3.history.clicked.connect(user.history)
window3.reserves.clicked.connect(user.on_going)
window3.cancel.clicked.connect(hotel.canceler)
window3.balance.clicked.connect(reenter.balance)
window3.search.clicked.connect(reenter.back_to_search)
ui_file3.close()

ui_file4 = QFile(resource_path("ui", "res.ui"))
ui_file4.open(QFile.ReadOnly) 
window4 = loader.load(ui_file4)
window4.conf.clicked.connect(hotel.main_reserve)
window4.backtohotel.clicked.connect(hotel.back_to_search)
ui_file4.close()

ui_file5 = QFile(resource_path("ui", "cnf.ui"))
ui_file5.open(QFile.ReadOnly) 
window5 = loader.load(ui_file5)
window5.confirm.clicked.connect(user.reserve)
ui_file5.close()

ui_file6 = QFile(resource_path("ui", "sign.ui"))
ui_file6.open(QFile.ReadOnly) 
window6 = loader.load(ui_file6)
window6.conf.clicked.connect(signin.user_signer)
ui_file6.close()

ui_file7 = QFile(resource_path("ui", "usernameERR.ui"))
ui_file7.open(QFile.ReadOnly) 
window7 = loader.load(ui_file7)
window7.ok.clicked.connect(window7.close)
ui_file7.close()

ui_file8 = QFile(resource_path("ui", "cancel.ui"))
ui_file8.open(QFile.ReadOnly) 
window8 = loader.load(ui_file8)
window8.cancel_conf.clicked.connect(reenter.after_cnl)
ui_file8.close()

ui_file9 = QFile(resource_path("ui", "wrong_pas.ui"))
ui_file9.open(QFile.ReadOnly) 
window9 = loader.load(ui_file9)
window9.conf.clicked.connect(window9.close)
ui_file9.close()

ui_file10 = QFile(resource_path("ui", "notife.ui"))
ui_file10.open(QFile.ReadOnly) 
window10 = loader.load(ui_file10)
window10.conf.clicked.connect(window10.close)
ui_file10.close()

ui_file11 = QFile(resource_path("ui", "low_balance.ui"))
ui_file11.open(QFile.ReadOnly) 
window11 = loader.load(ui_file11)
window11.ok.clicked.connect(reenter.low_balance)
ui_file11.close()



windows = [window1, window2, window3, window4, window5, window6, window7, window8, window9, window10, window11]
if __name__ == "__main__":  # ...
    window1.show()
    app.exec()


