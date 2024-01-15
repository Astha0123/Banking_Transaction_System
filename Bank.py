import os
import datetime
import string
from datetime import date                                # To find the date difference 

import platform
import mysql.connector
import pandas as pd
mydb=mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="astha123#&",
  database = "Bank"
);       # name of database created
mycursor=mydb.cursor()                                   # Return new Cursor Object using the connection

# Current/Today's Date
Cdate = datetime.datetime.now()                          # Current Date and Time

# Function to set date as: DD-MM-YYYY
def Set_DateFormat(d1,m1,y1):
    fDt=""
    d11= str(d1)
    m11=str(m1)
    y11=str(y1)

    if(len(d11)==1):
        d11 = '0'+d11
    if(len(m11)==1):
        m11= '0'+m11
    fDt=d11 + '-'+m11+'-'+y11
    return fDt



#--------------------------------
#Function to create a new account
#--------------------------------
def New_Customer_Entry():
    #Current/Today's Date
    dd=Cdate.day
    mm=Cdate.month
    yy=Cdate.year

    L=[]                                       # A list to append input data
    Accno = int(input("Enter the account number : "))
    L.append(Accno)
    Name= input("Enter the customer name : ")
    L.append(Name)
    Age= int(input("Enter the age of the customer : "))
    L.append(Age)
    Occupation= input("Enter the customer occupation : ")
    L.append(Occupation)
    Address= input("Enter address of the customer : ")
    L.append(Address)
    MobileNo=int(input("Enter the mobile number : "))
    L.append(MobileNo)
    AadharNo=int(input("Enter the Aadhar number : "))
    L.append(AadharNo)
    Amount= float(input("Enter the deposit amount : "))
    L.append(Amount)
    AccountType = input("Enter the Account type (Savings/Current) : ")
    L.append(AccountType)
    CurDt = str(Cdate)[0:10]                     # Current data converted into string format
    #dt_of_open = CurDt
    L.append(CurDt)
    cust =(L)                               # List L now converted into a tuple

# Using exceptions for validation
    try:
        sql="insert into Account(Accno,Name,Age,Occupation,Address,MobileNo,AadharNo,Amount,AccountType,CurDt) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql,cust)
        mydb.commit()
    except:
        print("\nHi! duplicate value not allowed")   # Error message


    
    
    
    
#-----------------------------------------
#Funstion to display account details
#-----------------------------------------
    
def View_Customers():
    print("Select a search criteria : ")
    print("1. Acc No.")
    print("2. Name")
    print("3. Mobile")
    print("4. Aadhar")
    print("5. View All")
    ch= int(input("Enter the choice : "))
    if ch==1:
        s=int(input("Enter the Account No. : "))
        rl =(s,)               # Creates a tuple with first value Account No.
        sql="select * from Account where Accno=%s"
        mycursor.execute(sql,rl)
    elif ch==2:
        s=input("Enter Name : ")
        rl =(s,)               
        sql="select * from Account where Name=%s"
        mycursor.execute(sql,rl)
    elif ch==3:
        s=int(input("Enter the Mobile No. : "))
        rl =(s,)               
        sql="select * from Account where MobileNo=%s"
        mycursor.execute(sql,rl)    
    elif ch==4:
        s=input("Enter Aadhar No. : ")
        rl =(s,)              
        sql="select * from Account where AadharNo=%s"
        mycursor.execute(sql,rl)
    elif ch==5:
        sql="select * from Account"
        mycursor.execute(sql)
    res= mycursor.fetchall()
    print("The Customer details are as follows : ")

    # Creating a dataframe using records set res.
    df=pd.DataFrame(res,columns=['Accno','Name','Age','Occupation','Address','MobileNo','Aadharno','Amount','AccountType','dt_of_open'])
    print(df)



#------------------------------------------------
#Function to modify Address or Mobile of customer
#------------------------------------------------
    
def Modify_Account():
    Accno=int(input("Enter the Account No. : "))
    print("Select the option to update : ")
    print("1. Address ")
    print("2. Mobile " )
    ch = int(input("Enter the Choice : "))
    if ch==1:
        Naddress = input("Enter new Address : ")
        query = "update Account set Address =" + "" + Naddress+ ""+ "where Accno="+str(Accno)
        cursor=mydb.cursor()
        cursor.execute(query)
        mydb.commit()
    elif ch==2:
        NMobileNo = input("Enter new Mobile No. : ")
        query = "update Account set MobileNo =" + "" + (NMobileNo)+ ""+ "where Accno="+str(Accno)
        cursor=mydb.cursor()
        cursor.execute(query)
        mydb.commit()
    else:
        print("Wrong operation")
        runAgain()




#--------------------------------------------------------
#Function to deposit/withdrawal amount in a given account
#--------------------------------------------------------
def Daily_Transaction():
    #Current/Today's Date
    dd=Cdate.day
    mm= Cdate.month
    yy= Cdate.year

    Pdt= Set_DateFormat(dd,mm,yy)   # Formatted date (dd,mm,yyyy)
    print('Date: ' , Pdt)

    L= []             # A blank list
    TAccno= int(input("Enter the Account Number: "))
    L.append(TAccno)

    # Read the record from the Account Table into the DataFrame
    df= pd.read_sql("Select Amount from Account where Accno= " + str(TAccno), mydb)
    TAmount = float(input("Enter the Amount: "))
    L.append(TAmount)

    #Transaction Date is the Current Date
    CurDt = str(Cdate)[0:10]         #Current Date converted into String Format
    #Tran_Dt=CurDt
    L.append(CurDt)

    Tran_Type= input("Enter the transaction type Deposit/Withdrawal: ")[0:15].rstrip('')
    L.append(Tran_Type)

    Description= input("Enter the transaction description: ")[0:20].rstrip('')
    L.append(Description)

    if(Tran_Type.lower()=='deposit'):
        #Creating new Balance amount by Adding to current deposit amount
        Balance=TAmount + int(df['Amount'])
        query="update Account set Amount= "+str(Balance) + "where Accno= "+ str(TAccno)
        cursor= mydb.cursor()
        cursor.execute(query)

        L.append(Balance)
        cust= (L)     # Convert List L into Tuple

        print(cust)
        # Using exceptions for validation
        try:
            # Query command to select records from both Account and Transaction table according to account number-wise
            sql="Insert into transaction(Accno, Tran_Amount,Dt_Tran, Tran_Type, Description, Balance) values(%s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql,cust)
            mydb.commit()
        except:
            print("Error in Transaction")       # Error Message

    elif(Tran_Type.lower=='withdrawal'): 
        #Creating new Balance amount by Subtracting to current withdrawal amount
        Balance= int(df['Amount'])- TAmount 
        query="update Account set Amount= "+str(Balance) + "where Accno= "+ str(TAccno)
        cursor= mydb.cursor()
        cursor.execute(query)

        L.append(Balance)
        cust= (L)     # Convert List L into Tuple

       
        # Using exceptions for validation
        try:
            sql="Insert into transaction(Accno, Tran_Amount, Dt_Tran, Tran_Type, Description, Balance) values(%s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql,cust)
            mydb.commit()
        except:
            print("\n Transaction is not Successful")       # Error Message
            runAgain()




#----------------------------------------------------------
#Function to display statement of account between two dates
#----------------------------------------------------------
def Account_Statement_DateWise():
    print("Please enter the details to view account details: ")
    Accno= int(input("Enter the Account details of tge Customer: "))
    d1= input("Enter starting date [yyyy-mm-dd]: ")
    d2= input("Enter ending date [yyyy_mm_dd]: ")
    #Using Exceptions for Validation
    try:
        # Query command to select record from both Account and Transaction table according to the Account Number and within a date Range.
        sql= "Select Account.Accno, Account.Name, Transaction.Dt_Tran, Tansaction.Tran_Amount,Transaction.Tran_Type, Transaction.Balance, Transaction.Description from Account INNER JOIN Transaction on Account.Accno = Transaction.Accno and Transaction.Accno= %s and Transaction.Dt_Tran Between %s and %s"
        rl=(Accno, d1 ,d2,)
        mycursor.execute(sql,rl)
        res = mycursor.fetchall()
        i=0
        for x in res:         # An iteration to process all records one by one from record set res
            i=i+1
            a= res[0][0]     #Account Number
            b= res[0][1]     #Account holder's name
            print("\n\nAccount No. ",a, 'Name',b)
            print("=" *100)
            print("{0:<15}{1:<30}{2:<17}{3:<25s}{4:<17s}".format("Date","Description","Amount","Deposit/Withdrawal","Balance"))
            print("=" *100)
            for x in range(0,i):
                print("{0:10s}{1:30s}{2:17s}{3:30s}{4:17s}".format(str(res[x][2]),str(res[x][6]),str(res[x][3]), str(res[x][6]),str(res[x][5])))
                print("=" *100)

                # Reading Account table data into a dataframe
                df = pd.read_sql("select Amount from Account where Accno=" + str(Accno),mydb)
                Balance= int(df['Amount'])
                print("Available Balance = ", Balance)
    except:
        print("\nHi! No Transaction in Account")         # Error Message




#-------------------------------------------------
#Function to dispaly all transaction of an Account
#-------------------------------------------------
def Account_Statement():
    print("Please enter the details to view the transaction details: ")
    Accno= int(input("Enter the Account Number of the Customer: "))
    try:
        # A query command to select records from both Account and Transaction table according to account Number_Wise
        sql="Select Account.Accno, Account.Name, Transaction.Dt_Tran, Transaction.Tran_Amount, Transaction.Tran_Type, Transaction.Balance, Transaction.description from Account INNER JOIN Transaction ON Account.Accno = Transaction.Accno and Transaction.Accno= %s"
        rl= (Accno,)
        mycursor.execute(sql,rl)
        res = mycursor.fetchall()
        i=0
        for x in res:          # An iteration to process all records one by one record set res
            i=i+1
            a= res[0][0]       # Account No.
            b= res[0][1]       # Account holder's name
            print("\n\n Account No.",a, 'Name',b)
            print("="*100)
            print("{0:<15}{1:<30}{2:<17}{3:<25s}{4:17s}".format("Date","Description","Amount","Deposit/Withdrawal","Balance"))
            print("="*100)
            for x in range(0,i):
                print("{0:10s}{1:30s}{2:17s}{3:30s}{4:<17s}".format(str(res[x][2]),str(res[x][6]),str(res[x][3]),str(res[x][6]),str(res[x][5])))
                print("="*100)


                # Reading Account table data into a dataframe
                df = pd.read_sql("select Amount from Account where Accno="+str(Accno), mydb)
                Balance= int(df['Amount'])
                print("Available Balance = ", Balance )
    except:
        print("\nHi! No transaction in Account ")    #Error Message





#---------------------------------------
#Function to run program till user wants
#---------------------------------------
def runAgain():
    runAgn = input("\nDo you want to continue y/n: ")
    if(runAgn.lower()=='y'):
        if(platform.system()== "Windows"):
            print(os.system('cls'))
            MenuSet()
        else:
            print(os.system('clear'))
            MenuSet()
    else:
        print("Bye Have a Nice Day")
        mycursor.close()
    mydb.close()





#----------------------------------
# Function to display the main menu
#----------------------------------
def MenuSet():
    opt=""
    print()
    print("-------------------------------------")
    print("    Banking Transaction System")
    print("-------------------------------------")
    print("1. : Add Customer")
    print("2. : View Customer Details")
    print("3. : Deposit/Withdrawal of Money")
    print("4. : Close Account")
    print("5. : Bank Statement of a Customer")
    print("6. : Bank Statement of a Customer between two dates")
    print("7. : Modify Address or Phone Number of Customer")
    try:         #Using Exceptions For Validation
        opt = input("Enter your Choice: ")
    except ValueError:
        exit("\nHi! That's Not A Number")      #Error Message
    else:
        print("\n")         # Print New Line
    if opt=='1':
        New_Customer_Entry();
    elif opt=='2':
        View_Customers();
    elif opt=='3':
        Daily_Transaction();
    elif opt=='4':
        Account_Statement();
    elif opt=='5':
        Account_Statement_DateWise();
    elif opt=='6':
        Modify_Account();
    else:
        print("Invalid inputs. Bye")
    runAgain()


#Project Execution starts here
MenuSet()

    



              
    













        
