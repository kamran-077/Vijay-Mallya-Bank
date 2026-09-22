#1 create class Bank
#2 CRUD operation 
#create ,read ,update , delete

import json
from pathlib import Path
import random
import string

class bank:

    database="data.json"
    data=[]
    try:
        if Path (database).exists():
            with open(database,"r")as fs:
                data = json.load (fs)
                print(data)
        else:
            print("no such file exists ")      
    except Exception as err :
        print ("the error occured")

    @classmethod
    def update(cls): 
        with open (cls.database,"w")as fs:
            fs.write(json.dumps(cls.data,indent=4))
    
    
    @staticmethod
    def generateacc():
        # to find the random account number 
        digit=random.choices(string.digits,k=4)
        alpha=random.choices(string.ascii_letters,k=4)
        id=alpha+digit
        random.shuffle(id)
        return"".join(id)
    def deposit(self):
        acc=input("enter your account no ").strip()
        pin=int(input("enter the pin"))
        userdata=[i for i in bank.data if acc ==i.get("accountno")and pin == i.get("pin") ] 
        print(userdata)      
        if  userdata == False:
            print("not a user ")
            return
        else :
            amount=int(input("enter the amount ")) 
            if amount<=0:
                print("invalid input")
            else:   
                userdata[0]["balance"]+=amount
                print("amount credited")
                bank.update()  


    def details(self):
        acc=input("enter your account no ").strip()
        pin=int(input("enter the pin"))
        userdata=[i for i in bank.data if acc ==i.get("accountno")and pin == i.get("pin") ] 
        print(userdata)      
        if  userdata == False:
            print("not a user ")
            return
        else :  
            for i in userdata[0]:
                print(i,userdata[0][i])           

    def withdraw(self):
        acc=input("enter your account no ").strip()
        pin=int(input("enter the pin"))
        amount=int(input("enter the amount to withdraw ")) 
        # for i in bank.data :
            # if acc ==[i]["accountno"]and pin == [i]["pin"]:
            #     print ("user")
            #     print(i)
            # else:
            #     print("not a user")
        userdata=[i for i in bank.data if acc ==i.get("accountno")and pin ==  i.get("pin")and amount<=i.get("balance") ] 
        print(userdata)      
        if  userdata == False:
            print("not a user ")
            return
        if amount<=0:
            print("invalid")
        elif amount>10000:
            print("amount is greater than limit")    
        else :
            if userdata[0]["balance"] > amount:
                userdata[0]["balance"]-=amount
                print("amount debited")
                bank.update()         

    def createaccount(self):
        info ={
            'name':input("enter your name "),
            "age" :int(input("enter your age")),
            "email":(input("enter your email")),
            "pin" :int(input("enter your pin")),
            "phone" :(input("enter your phone no ")),
            "accountno": bank.generateacc(),
            "balance":0
        }  
        if info["age"]>18 and len(str(info["pin"]))==4 and len(str(info["phone"]))==10: 
            bank.data.append(info)
            bank.update()
            print(bank.data)

    def delete(self):
        acc=input("enter your account no ").strip()
        pin=int(input("enter the pin"))
        userdata=[i for i in bank.data if acc ==i.get("accountno")and 
                pin ==  i.get("pin")] 
        if  userdata == False:
            print("not a user ")
            return

        else:
            print("are you sure you want to delete your account ? (yes/no)")
            choice = input()
            if choice == 'Yes':
                ind = bank.data.index(userdata[0])
                bank.data.pop(ind)
                bank.update()
                print("account")
            else :
                print("Operation treminated !")






obj= bank()
# obj.deposit()
# obj.createaccount()
# obj.details()
# obj.withdraw()



while True:
    print("\n===== bank Management System =====")
    print("1. creating account ")
    print("2. for deposite ")
    print("3. for withdraw")
    print("4. Delete user")
    print("5. update user")
    print("6. Exit")

    choice = int(input("Enter Choice: "))

    if choice == 1:
        obj.createaccount()
    elif choice == 2:
        obj.deposit()
    elif choice == 3:
      obj.withdraw()
    elif choice == 4:
        obj.delete()
    elif choice == 5:
        obj.update()    
    elif choice == 6:
        print("Exiting Program...")
        break
    else:
        print("Invalid Choice")