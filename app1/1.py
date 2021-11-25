from flask import Flask,render_template,request
# from flask_mysqldb import MySQL
app=Flask(__name__)
import pymongo
# app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://sushma:sushma123@cluster0.qkqa9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('total_records')
register = db.register


@app.route('/')
def home():
    
    return render_template("signup.html")


@app.route('/mynext',methods=["GET","POST"])
def signup():
    username=request.form.get("username")
    password=request.form.get("password")
    phonenumber=request.form.get("phonenumber")
    email=request.form.get("email")

    
    
    if (validateEmail(email) and  password_check(password) and check_phonenumber(phonenumber)):
        register.insert_one({"email":email,"phone_no":phonenumber,"user_name":username,"password":password})
        # print(username,password,phonenumber,email)
        return render_template("login.html")
    else:
        return render_template("error.html")



def validateEmail(email):
    if(email.find("@")!=-1 and email.find(".")!=-1):
        print("valid email")
        return True
    else:
        print("not valid email")
        return False

def password_check(password):
          
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



import re
def check_phonenumber(phonenumber):
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



@app.route('/prev',methods=["GET","POST"])
def login():
    email=request.form.get("email")
    password=request.form.get("password")
    exits=register.find_one({"email":email,"password":password})
    print(exits)
    if(exits):

        return render_template("dashboard.html")
    else:
        return render_template("error.html")


    #     print("invalid")

@app.route('/verify',methods=["GET","POST"])
def verify():
    return render_template("verification.html")


@app.route('/pass',methods=["GET","POST"])
def forgot_password():
    newpassword=request.form.get("newpassword")
    confirmpassword=request.form.get("confirmpassword")
    print(newpassword,confirmpassword)
    if (newpassword ==confirmpassword):
        print("success")
        return True
    else:
        print("not valid")
        return False



if __name__=='__main__':
    app.run(debug=True)