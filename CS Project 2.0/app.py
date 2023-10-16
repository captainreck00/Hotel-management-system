from flask import Flask, jsonify, request, redirect, session, render_template
from flask_session import Session
import modules.Data_functions as func
import secrets
import json

app = Flask(__name__)

app.secret_key = 'ASDHFOT568As51@#'

# App route for the login page
@app.route("/")
def index():
    if session.get('is_verified')==True:
        return redirect('/protected-page')
    else:    
        return render_template('login_page.html')

# App route for getting the email id and password from the website
@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    
    if func.verify(data['email'], data['password']):
        session['is_verified'] = True
        response_data = {"verified": "yes"}
    else:    
        response_data = {"verified": "no"}
    return jsonify(response_data)

# App route for checking the user is verified when going to /protected-page 
@app.route('/protected-page', methods=['GET'])
def protected_page():
    if session.get('is_verified')==True:
        return render_template('index.html')
    else:
        return redirect('/')
    
# App route for getting the booking details from the website and returning the room no and message 
@app.route('/protected-page', methods=['POST'])
def booking_data():
        user_data = request.get_json()

        name=user_data["Name"]
        email=user_data["Email"]
        people=user_data["Number of People"]
        room_type=user_data["Room Type"]
        phone=user_data["Phone Number"]
        checkIn=user_data["CheckIn"]
        checkOut=user_data["CheckOut"]
        preference=user_data["Preferences"]
        extrabed,gym,minibar,breakfast=user_data["Add-ons"]

        checkIn=func.date_reverse(checkIn)
        checkOut=func.date_reverse(checkOut)

        room_no=func.advance_booking(name,email,people,phone,room_type,preference,bool(gym),bool(minibar),bool(extrabed),bool(breakfast),checkIn,checkOut)
        if room_no:
            return jsonify({"message":"Room Booked","Room No":room_no})
        else:
            return jsonify({"message":"Room Booking unsuccessfull"})

#App route for getting the user info for the employees
@app.route('/customer_info', methods=['GET'])
def customer_info_page():

    # k={"name":i[0],"phone_no":i[1],"email_id":i[2],"guests":i[3],"room_no":i[4],"room_type":i[5],"addons":[i[6],i[7],i[8],i[9]],"check_in":i[10],"check_out":i[11],"amount":i[13]}
    custdata=func.sorting_time2()
    pay_data=func.pay_data()
    data={'cust':custdata,'paydata':pay_data}

    if session.get('is_verified'):
        # You can add logic here to fetch customer info or display forms.
        return render_template('details.html',data=data)
    else:
        return redirect('/')

@app.route('/customer_info',methods=['POST'])
def cust_billing():
    try:
        data = request.get_json()
        id=data['id']
        print(id)
        func.bill_paid(id)
        message="Bill Paid Successfully"
        return jsonify({'message':message})
    except:
        message="Bill Not Paid"
        return jsonify({'message':message})   
    


if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(debug=True)

