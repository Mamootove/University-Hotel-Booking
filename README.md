Welcome!

This project is still under develope.

# Hotel Reservation System

This project is a hotel reservation system built with **Python** and **PySide6**, featuring user registration, login, room reservation, balance management, and reservation history.  

---

## 📂 Project Structure

Project/

│

├─ ui/ # Qt Designer UI files

│ ├─ lg.ui

│ ├─ htl.ui

│ ├─ myrms.ui

│ ├─ res.ui

│ ├─ cnf.ui

│ ├─ sign.ui

│ ├─ usernameERR.ui

│ ├─ cancel.ui

│ ├─ wrong_pas.ui

│ ├─ notife.ui

│ └─ low_balance.ui

│

├─ data/ # Data storage files

│ ├─ users.txt # Usernames and passwords

│ ├─ users_dir.txt # User information, ongoing reservations, history

│ └─ <city>.txt # Room and reservation info for each city

│

├─ main.py # Main Python code

└─

---
## Files Structuere
./data/
    ./users.txt : {usrname: password} | The password is stored unencrypted.(Will add the hash soon)
    

    ./users_dir.txt : {username : {on going: [], history:[], info: {}, balance: int}} | Making this kind of database was a bad idea, anyway "on going" and history are almost the same */history -> +{"status": status} : Changes based on cancelled or finished reserve  
    
    on going :[ {"reserve_number": reserve number, "d_enter": date enter, "d_exit": date exit, "des": des, "amount": amount, "room_number": room number, 'price': price } ]
    
    info: {name : "{name} {lastname}", usr: username, pas: password}


    ./city.txt : [unreserved, reserved, all] | unreserved , reserved, all -> list
    
    unreserved : ['5','2', ...] contain only room numbers
    
    reserved : [['2', '2025-02-10', '2025-02-12', '54875'], ...] | #[str(room number), date enter, date exit, str(reserve number)]
    
    all : [['7', '1', 30], ['8', '2', 40], ...]  | #[room number, amount, price]
    

Three accounts are perbuilt --> Mamootov: '1234', MMD: '.', '':'' 

You can check their reserves

⚠️ Since we I used pickle to store files, be careful not to modify the data files.
---

## ⚙️ Requirements

- Python 3.9+  
- PySide6  
- Standard Python modules: `pickle`, `datetime`, `random`, `os`, `sys`  

Install PySide6 with:

pip install PySide6

---

## 🚀 Running the Project

1. Place the project code along with the ui and data folders in the same directory.

2. Open a terminal and navigate to the project folder.

3. Run the main Python file:

    python main.py
---

## ⚠️ Important Notes

- Passwords are not hashed, so security is low.
- Data is stored using pickle; avoid manual file changes.
- UI is built with Qt Designer and loaded using QUiLoader.
