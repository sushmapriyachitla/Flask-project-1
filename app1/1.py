from flask import Flask,render_template,request

app=Flask(__name__)
import pymongo

#connect to your pymango db database
client = pymongo.MongoClient("mongodb+srv://sushma:sushma123@cluster0.qkqa9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#get the database name
db = client.get_database('total_records')
#get the collection which contains the data
register = db.register  

#assigning URL's for route
@app.route('/')
def menu():
    
    return render_template("landing.html")
@app.route('/getin')
def content():
    
    return render_template("signup.html")

@app.route('/action')
def method():
    
    return render_template("login.html")


@app.route('/mynext',methods=["GET","POST"])
    #creating a function for signup page
def signup():
    # getting the requirements for signup page with get function
    username=request.form.get("username")
    password=request.form.get("password")
    phonenumber=request.form.get("phonenumber")
    email=request.form.get("email")

    
    #if email and password and phone number are valid then the data will be stored in the database
    if (validateEmail(email) and  password_check(password) and check_phonenumber(phonenumber)):
        register.insert_one({"email":email,"phone_no":phonenumber,"user_name":username,"password":password})
        # print(username,password,phonenumber,email)
        return render_template("login.html")   #it returns to the login template if success
    else:
        return render_template("error.html")  #if fails then returns to the error template



def validateEmail(email):   #validating the email
    if(email.find("@")!=-1 and email.find(".")!=-1):  #if particular symbols are present then valid by using the find function
        print("valid email")
        return True
    else:
        print("not valid email")
        return False  #if not return the false

def password_check(password): #validating the password with some conditions if those conditions are satisfied then returns the val 
          
    SpecialSym =['$', '@', '#', '%']
    val = True
      
    if len(password) < 8:
        print('length should be at least 8')
        val = False
    
    if not any(char.isdigit() for char in password):
        print('Password should have at least one numeral')
        val = False
    if not any(char.isupper() for char in password):
        print('Password should have at least one uppercase letter')
        val = False
          
    if not any(char.islower() for char in password):
        print('Password should have at least one lowercase letter')
        val = False
          
    if not any(char in SpecialSym for char in password):
        print('Password should have at least one of the symbols $@#')
        val = False
    if val:
        return val


#importing the regex module
import re
def check_phonenumber(phonenumber):   #validating the phone number  by the certain conditions if it is valid then valid or not valid
    phonenumber=str(phonenumber) 
    if(len(phonenumber))==10 and (phonenumber.isdigit()):
        output = re.findall(r"^[6789]\d{9}$",phonenumber)
        if(len(output)==1
        ):
            print("valid phonenumber")
            return True
        else:
            print("Invalid phone number")
            return False
    else:
        print("Invalid")
        return False


#routing to the login page
@app.route('/prev',methods=["GET","POST"])
def login():  #defining a function  for the login page if the sign up page is valid then it render to the login template
    email=request.form.get("email")
    password=request.form.get("password")
    # validating the data and assigning to the variable
    exits=register.find_one({"email":email,"password":password})  #it validate the sign up data with the login data  
    print(exits)
    if(exits): #if valid then render to the dashboard template 

        return render_template("dashboard.html")
    else: #else render to the error template
        return render_template("error.html")


    #     print("invalid")
#routing for the verification 
@app.route('/verify',methods=["GET","POST"])
def verify(): #defining a function for verification render to the verification template 
    return render_template("verification.html")


@app.route('/pass',methods=["GET","POST"])
def forgot_password(): 
    newpassword=request.form.get("newpassword")
    confirmpassword=request.form.get("confirmpassword")
    print(newpassword,confirmpassword)

    if(newpassword ==confirmpassword):
        print("success")
        return True
    else:
        print("not valid")
        return False



if __name__=='__main__':
    app.run(debug=True)