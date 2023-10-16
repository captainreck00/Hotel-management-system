import sqlite3
import datetime


def verify(email,password):
    conn=sqlite3.connect("my_database.db")
    cursor=conn.cursor()

    cursor.execute("Select * FROM users")
    r=cursor.fetchall()
    for i in r:
        if email==i[0] and password==i[1]:
            return True
    return False    


def date_reverse(input_date):
    from datetime import datetime

    # Convert to a datetime object
    date_object = datetime.strptime(input_date, "%Y-%m-%d")

    # Format the date as "dd-mm-yyyy"
    formatted_date = date_object.strftime("%d-%m-%Y")

    return formatted_date


def advance_booking(name , email , adults , number , room_type , preference , gym , mini_bar , extra_bed ,breakfast , checkin_date , checkout_date ):

    conn = sqlite3.connect("HOTEL MANAGEMENT.db")
    cursor = conn.cursor()

    start_date = datetime.datetime.strptime(checkin_date, '%d-%m-%Y')
    end_date = datetime.datetime.strptime(checkout_date, '%d-%m-%Y')
    dates_reserved = []
    current_date = start_date
    room=0
    dates_reserved_str =""

    while current_date <= end_date:
        dates_reserved.append(current_date.strftime('%d-%m-%Y'))
        current_date += datetime.timedelta(days=1)


    for f in dates_reserved:
        dates_reserved_str = dates_reserved_str + f + " , "
       
    cursor.execute("SELECT * FROM Room_table")
    r= cursor.fetchall()

    i=0
    while i<=(len(r) - 1):
        #Selecting the row of the room no trying to be booked
        
        #
        if r[i][1] == room_type and r[i][2] == preference :

            cursor.execute(''' SELECT reserved_dates FROM Room_table WHERE Room_no = ?''' , (r[i][0] ,))
            c= cursor.fetchall()
            g=0
            for k in dates_reserved:
                if k in  c[0][0] :
                    i=i+1
                    break
                
                else:
                    g=1
                    
            # Finding the reserved dates of all the days the room has been booked
            if g == 1 :
            
                    x = c[0][0]
                    y=x
                    room =r[i][0]

                    for h in dates_reserved:
                        y = y + h +  " , " 

                    #removed it bcuz it was not needed
                    # cursor.execute('''INSERT INTO  Booking_table(Room_no , Room_type , name , email , number , adults , preference  ,gym , mini_bar , extra_bed , breakfast , reserved_dates ) 
                    #        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)  ''' , (  r[i][0] ,r[i][1] , name , email , number , adults , preference , gym , mini_bar , extra_bed , breakfast , dates_reserved_str ))

            #Inserting values in the mother table
                    
                    cursor.execute('''INSERT INTO  Mother_table(name , phone_no , email_id ,adults, Room_type , Room_no , gym , mini_bar , extra_bed , breakfast, check_in , check_out ,reserved_dates, Amount_payable ) 
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)  ''' , ( name, number , email , adults , r[i][1] , r[i][0] , gym , mini_bar , extra_bed ,breakfast ,checkin_date , checkout_date, dates_reserved_str ,  0  ))
                    
                    conn.commit()

                    booking_id=int(cursor.lastrowid)
                    print(booking_id)
                    pay_data=pay_entry(booking_id)
                    print(pay_entry(booking_id))
                    # Insert data into payment_table
                    cursor.execute('''
                        INSERT INTO payement_table (
                            roomCharges, roomServices, service, vat, gym, bed, breakfast, bar, total, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        pay_data["roomCharges"],
                        pay_data["roomService"],
                        pay_data["service"],
                        pay_data["vat"],
                        pay_data["gym"],
                        pay_data["bed"],
                        pay_data["breakfast"],
                        pay_data["bar"],
                        pay_data["roomCharges"]+pay_data["roomService"]+pay_data["service"]+pay_data["vat"]+pay_data["gym"]+pay_data["bed"]+pay_data["breakfast"]+pay_data["bar"],
                        "pending"

                    ))

                    # Commit the changes and close the connection
                    conn.commit()
                    
                    
            #Inserting dates into room table
                    cursor.execute('''UPDATE Room_table SET reserved_dates = ? WHERE Room_no = ?''',  ( y, r[i][0] ))

                    conn.commit()
                    conn.close()
                    break      
        else:
            i=i+1
    return room
            
        

def discount(check_in, amount_payable):
    
    # Finding the month the month
    date = datetime.datetime.strptime(check_in, "%d-%m-%Y")   
    month = date.month
    print("Month:", month)

    if month == 5 or month == 6 or month == 7 :
        dis = 0.1 * amount_payable
        amount_payable= amount_payable - dis
    elif month == 1 or month == 12 or month == 11 :
        dis = 0.1 * amount_payable
        amount_payable = amount_payable - dis 

    return amount_payable


def pay_entry(booking_id):
    conn = sqlite3.connect("HOTEL MANAGEMENT.db")
    cursor = conn.cursor()
   
    cursor.execute(''' SELECT * FROM Mother_table WHERE booking_id = ? ''' , ( booking_id ,)) 
    r=cursor.fetchall()
    print(r)

    try:
        check_in = r[0][11]
        room_type = r[0][6]
        gym =  r[0][7]
        mini_bar =  r[0][8]
        extra_bed =  r[0][9]
        breakfast=r[0][10]
        reserved_dates = r[0][13]
        print(reserved_dates)
    except:
        return "Invalid ID"    
    
    
    count = reserved_dates.count(",")
    roomCharge=0
    room_service_tax=0
    vat=0
    service_tax=0
    gym_pay=0
    bed_pay=0
    bar_pay=0
    breakfast_pay=0
    print(count)


    if room_type == "Deluxe room":
        amount_to_be_paid = 8000*count
        roomCharge=amount_to_be_paid

        if int(gym):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            gym_pay=500
        if int(mini_bar):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            bar_pay=500
        if int(extra_bed):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            bed_pay=500
        if int(breakfast):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            breakfast_pay=500
        
        service_tax = 0.12 * amount_to_be_paid
        vat = 0.14 * amount_to_be_paid
        room_service_tax = 0.05 * amount_to_be_paid

        amount_to_be_paid = amount_to_be_paid + service_tax + vat + room_service_tax 

        #checking the discount
        dis_amount = discount(check_in, amount_to_be_paid)
        amount_to_be_paid = dis_amount
        
    
    
    if room_type == "Premier suite":
        amount_to_be_paid = 10000*count
        roomCharge=amount_to_be_paid

        if int(gym):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            gym_pay=500
        if int(mini_bar):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            bar_pay=500
        if int(extra_bed):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            bed_pay=500
        if int(breakfast):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            breakfast_pay=500

        service_tax = 0.12 * amount_to_be_paid
        vat = 0.14 * amount_to_be_paid
        room_service_tax = 0.05 * amount_to_be_paid

        amount_to_be_paid = amount_to_be_paid + service_tax + vat + room_service_tax 

        #checking the discount
        dis_amount = discount(check_in, amount_to_be_paid)
        amount_to_be_paid = dis_amount

    if room_type == "Executive suite":
        amount_to_be_paid = 12000*count
        roomCharge=amount_to_be_paid

        if int(gym):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            gym_pay=500
        if int(mini_bar):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            bar_pay=500
        if int(extra_bed):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            bed_pay=500
        if int(breakfast):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            breakfast_pay=500

        service_tax = 0.12 * amount_to_be_paid
        vat = 0.14 * amount_to_be_paid
        room_service_tax = 0.05 * amount_to_be_paid

        amount_to_be_paid = amount_to_be_paid + service_tax + vat + room_service_tax 

        #checking the discount
        dis_amount = discount(check_in, amount_to_be_paid)
        amount_to_be_paid = dis_amount


    if room_type == "standard room":
        amount_to_be_paid = 6000*count
        roomCharge=amount_to_be_paid

        if int(gym):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            gym_pay=500
        if int(mini_bar):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            bar_pay=500
        if int(extra_bed):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            bed_pay=500
        if int(breakfast):
            amount_to_be_paid = amount_to_be_paid + (500*count)
            breakfast_pay=500

        service_tax = 0.12 * amount_to_be_paid
        vat = 0.14 * amount_to_be_paid
        room_service_tax = 0.05 * amount_to_be_paid

        amount_to_be_paid = amount_to_be_paid + service_tax + vat + room_service_tax 

        # checking the discount 
        dis_amount = discount(check_in, amount_to_be_paid)
        amount_to_be_paid = dis_amount
    
    return {"roomCharges":roomCharge,"roomService":int(room_service_tax),"service":int(service_tax),"vat":int(vat),"gym":gym_pay,"bed":bed_pay,"breakfast":breakfast_pay,"bar":bar_pay}



import sqlite3
import datetime

def sorting_time2():
    conn = sqlite3.connect("HOTEL MANAGEMENT.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Mother_table")
    data = cursor.fetchall()

    today = datetime.datetime.now().date()  # Get the current date

    present = []
    past = []
    future = []

    for item in data:
        check_in_date = datetime.datetime.strptime(item[11], '%d-%m-%Y').date()
        reserved_dates = item[11].count(',') + 1

        if check_in_date == today:
            if item[14] != 0:  # Check if the "amount" is non-zero
                past.append((check_in_date, reserved_dates, item))
            else:
                present.append((reserved_dates, item))
        elif check_in_date < today:
            past.append((check_in_date, reserved_dates, item))
        else:
            future.append((check_in_date, reserved_dates, item))

    # Sort the lists based on criteria
    present.sort(reverse=True)  # Sort by reserved dates in descending order
    past.sort(key=lambda x: (x[0], x[1]))  # Sort by check-in date and reserved dates
    future.sort(key=lambda x: (x[0], x[1]))  # Sort by check-in date and reserved dates

    # Extract the original data from the sorted lists
    present = [item[1] for item in present]
    past = [item[2] for item in past]
    future = [item[2] for item in future]

    sorted_date = [present, future, past]

    for i in range(3):
        l = []
        for j in sorted_date[i]:
            k = {
                "id": j[0],
                "name": j[1],
                "phone_no": j[2],
                "email_id": j[3],
                "guests": j[4],
                "room_no": j[5],
                "room_type": j[6],
                "addons": [j[7], j[8], j[9], j[10]],
                "check_in": j[11],
                "check_out": j[12],
                "amount": j[14]
            }
            l.append(k)
        sorted_date[i] = l

    return sorted_date



def bill_paid(booking_id):
    conn = sqlite3.connect("HOTEL MANAGEMENT.db")
    cursor = conn.cursor()

    cursor.execute(''' SELECT * FROM payement_table WHERE booking_id = ? ''' , ( booking_id ,)) 
    amount=cursor.fetchone()[9]

    cursor.execute(''' UPDATE MOther_table SET Amount_payable = ? WHERE booking_id = ? ''' ,
                (amount, booking_id))
    cursor.execute(''' UPDATE payement_table SET status = 'done' ''' )
    conn.commit()
    conn.close()

def pay_data():
    conn = sqlite3.connect("HOTEL MANAGEMENT.db")
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM payement_table WHERE status='pending' ''')
    data=cursor.fetchall()

    conn.commit()
    conn.close()

    l={}
    for i in data:
        k={"id":i[0],"roomCharges":i[1],"roomService":i[2],"service":i[3],"vat":i[4],"gym":i[5],"bed":i[6],"breakfast":i[7],"bar":i[8],"total":i[9]}
        l[i[0]]=k

    return l




#Rishit code for sorting
# def sorting_time():

#     present=[]
#     future=[]
#     past=[]


#     conn = sqlite3.connect("HOTEL MANAGEMENT.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM Mother_table")
#     m = cursor.fetchall()

#     current_date = datetime.datetime.now().date()
    
#     i=0
    
#     while i <=(len(m)-1):
#         d = m[i][11] 
        
#         date = datetime.datetime.strptime( d , "%d-%m-%Y").date()
             
#         if date <  current_date:
#             past.append(m[i])
#             i=i+1
#         elif date == current_date:
#             present.append(m[i])
#             i=i+1
#         else:
#             future.append(m[i])
#             i=i+1
        
#         n = len(past)  
#         for k in range(n):
#             for j in range(0, n - k - 1):
#                 if past[j] > past[j + 1]:
                    
#                     past[j], past[j + 1] = past[j + 1], past[j]

#         n = len(future)  
#         for k in range(n):
#             for j in range(0, n - k - 1):
#                 if future[j] > future[j + 1]:
                    
#                     future[j], future[j + 1] = future[j + 1], future[j]

    
#     sorted_date=[present,future,past]
#     for i in range(3):
#         l=[]
#         for j in sorted_date[i]:
#             k={"id":j[0],"name":j[1],"phone_no":j[2],"email_id":j[3],"guests":j[4],"room_no":j[5],"room_type":j[6],"addons":[j[7],j[8],j[9],j[10]],"check_in":j[11],"check_out":j[12],"amount":j[14]}
#             l.append(k)
#         sorted_date[i]=l

#     return sorted_date