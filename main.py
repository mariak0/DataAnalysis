import requests
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime
import mysql.connector
import csv




#url
url = "https://www.stats.govt.nz/assets/Uploads/Effects-of-COVID-19-on-trade/Effects-of-COVID-19-on-trade-At-15-December-2021-provisional/Download-data/effects-of-covid-19-on-trade-at-15-december-2021-provisional.csv"

#Download CSV 
response = requests.get(url)

#Decode into a string
content = response.content.decode('utf-8')

#Parse CSV 
rows = csv.reader(content.splitlines(), delimiter=',')
data = list(rows)




#MySQL server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

#cursor
mycursor = mydb.cursor()

#Create database
mycursor.execute("CREATE DATABASE IF NOT EXISTS arxes")

#connect to database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="arxes"
)



#function to show the monthly sum
def show_monthly_sum():
    #dictionary to store the sum
    sums_by_month = {}

    # sum for each month
    for row in data[1:]:
        date_str = row[2]
        value = float(row[8])
        symbol = data[7][7]

        try:
            #date string to datetime 
            date = datetime.strptime(date_str, "%d/%m/%Y")
            month = date.month

            if month in sums_by_month:
                sums_by_month[month] += value
            else:
                sums_by_month[month] = value

        except ValueError:
            #Handleerrors
            print(f"Invalid date format: {date_str}")

    #tkinter window
    root_monthly_sum = tk.Toplevel(root)
    root_monthly_sum.title("Monthly Sum")

    #tkinter Label for each month and sum value
    for month, value in sums_by_month.items():
        label_text = f"Month {month}: Sum = {value} {symbol}"
        label = tk.Label(root_monthly_sum, text=label_text)
        label.pack()

    #bar graph 
    plt.bar(sums_by_month.keys(), sums_by_month.values(), color='blue')
    plt.xlabel('Month')
    plt.ylabel('Sum of Values')
    plt.title('Sum of Values by Month')
    plt.show()

    mycursor = mydb.cursor()

    # Create table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS by_month (
            month INT PRIMARY KEY,
            sum_value FLOAT
        )
    """
    mycursor.execute(create_table_query)

    # Insert values the  table
    for month, value in sums_by_month.items():
        sql = "INSERT INTO by_month (month, sum_value) VALUES (%s, %s)"
        val = (month, value)
        mycursor.execute(sql, val)

    #Commit  changes
    mydb.commit()

    #SELECT query to retrieve data
    mycursor.execute("SELECT * FROM by_month")

    #Fetch rows 
    rows = mycursor.fetchall()

    #path for the CSV file
    csv_filename = "/Users/mariakouri/Documents/python/by_month.csv"

    #CSV file in write mode
    with open(csv_filename, mode='w', newline='') as file:
        #CSV writer 
        writer = csv.writer(file)

        #write column headers
        writer.writerow([i[0] for i in mycursor.description])

        #wWrite the data rows
        writer.writerows(rows)
    
    mycursor.close()


def show_sum_by_country():
    #dictionary to store the sum of values for each country
    sums_by_country = {}

    #sum the values for each country
    for row in data[1:]:
        country = row[4]
        value = float(row[8])
        if country in sums_by_country:
            sums_by_country[country] += value
        else:
            sums_by_country[country] = value

    #tkinter window 
    root_sum_by_country = tk.Toplevel(root)
    root_sum_by_country.title("Country")

    #Get the symbol from row 7
    symbol = data[7][7]

    #tkinter Label for each country and its sum value
    for country, value in sums_by_country.items():
        label_text = f"{country}: {value:.2f} {symbol}"
        label = tk.Label(root_sum_by_country, text=label_text)
        label.pack()

    #bar graph
    plt.bar(sums_by_country.keys(), sums_by_country.values(), color='pink')
    plt.xticks(rotation=90)
    plt.xlabel('Country')
    plt.ylabel('Value')
    plt.title('Sum of Values by Country')
    plt.show()

    mycursor = mydb.cursor()

    # new table 
    create_table_query = """
        CREATE TABLE IF NOT EXISTS by_country (
            country VARCHAR(255) PRIMARY KEY,
            sum_value FLOAT
        )
    """
    mycursor.execute(create_table_query)

    # Insert into table
    for country, value in sums_by_country.items():
        sql = "INSERT INTO by_country (country, sum_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE sum_value = %s"
        val = (country, value, value)
        mycursor.execute(sql, val)

    # Commit changes
    mydb.commit()

    # SELECT query to retrieve data
    mycursor.execute("SELECT * FROM by_country")

    #Fetch rows
    rows = mycursor.fetchall()

    #path and filename for  CSV file
    csv_filename = "/Users/mariakouri/Documents/python/by_country.csv"

    #CSV file in write mode
    with open(csv_filename, mode='w', newline='') as file:
        #CSV writer object
        writer = csv.writer(file)

        #Write headers
        writer.writerow([i[0] for i in mycursor.description])

        # data rows
        writer.writerows(rows)
    mycursor.close()




#sum by day
def show_sum_by_day():
    #dictionary 
    sums_by_day = {}

    # Loop and sum 
    for row in data[1:]:
        day = row[3]
        value = float(row[8])
        if day in sums_by_day:
            sums_by_day[day] += value
        else:
            sums_by_day[day] = value

    #new tkinter window
    root_sum_by_day = tk.Toplevel(root)
    root_sum_by_day.title("Days")

    #Get symbol from row 7
    symbol = data[7][7]

    #tkinter Label for each day and its sum value
    for day, value in sums_by_day.items():
        label_text = f"{day}: {value:.2f} {symbol}"
        label = tk.Label(root_sum_by_day, text=label_text)
        label.pack()

    #bar graph
    plt.bar(sums_by_day.keys(), sums_by_day.values(), color='black')
    plt.xticks(rotation=90)
    plt.xlabel('Day')
    plt.ylabel('Value')
    plt.title('Sum of Values by Day')
    plt.show() 

    mycursor = mydb.cursor()

    # new table 
    create_table_query = """
        CREATE TABLE IF NOT EXISTS by_day (
            day VARCHAR(255) PRIMARY KEY,
            sum_value FLOAT
        )
    """
    mycursor.execute(create_table_query)

    # Insert into the table
    for day, value in sums_by_day.items():
        sql = "INSERT INTO by_day (day, sum_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE sum_value = %s"
        val = (day, value, value)
        mycursor.execute(sql, val)

    #commit
    mydb.commit()

    #SELECT query to retrieve data
    mycursor.execute("SELECT * FROM by_day")

    #Fetch rows
    rows = mycursor.fetchall()

    # path and filename for CSV file
    csv_filename = "/Users/mariakouri/Documents/python/by_day.csv"

    #Open the CSV file in write mode
    with open(csv_filename, mode='w', newline='') as file:
        #CSV writer object
        writer = csv.writer(file)

        #Write headers
        writer.writerow([i[0] for i in mycursor.description])

        # Write the data rows
        writer.writerows(rows)
    mycursor.close()


#function sum by commodity
def show_sum_by_commodity():
    #dictionary
    sums_by_commodity = {}

    # Loopand sum 
    for row in data[1:]:
        commodity = row[5]
        value = float(row[8])
        if commodity in sums_by_commodity:
            sums_by_commodity[commodity] += value
        else:
            sums_by_commodity[commodity] = value

    #tkinter window
    root_sum_by_commodity = tk.Toplevel(root)
    root_sum_by_commodity.title("Commodity")

    #Get the symbol
    symbol = data[7][7]

    #tkinter Label for each commodity and its sum value
    for commodity, value in sums_by_commodity.items():
        label_text = f"{commodity}: {value:.2f} {symbol}"
        label = tk.Label(root_sum_by_commodity, text=label_text)
        label.pack()

    #bar graph 
    plt.bar(sums_by_commodity.keys(), sums_by_commodity.values(), color='grey')
    plt.xticks(rotation=90)
    plt.xlabel('Commodity')
    plt.ylabel('Value')
    plt.title('Sum of Values by Commodity')
    plt.show()

    mycursor = mydb.cursor()

    #Create a  table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS by_commodity (
            commodity VARCHAR(255) PRIMARY KEY,
            sum_value FLOAT
        )
    """
    mycursor.execute(create_table_query)

    # Insert into table
    for commodity, value in sums_by_commodity.items():
        sql = "INSERT INTO by_commodity (commodity, sum_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE sum_value = %s"
        val = (commodity, value, value)
        mycursor.execute(sql, val)
    mydb.commit()

    #SELECT query 
    mycursor.execute("SELECT * FROM by_commodity")

    # Fetch rows 
    rows = mycursor.fetchall()

    # path for CSV 
    csv_filename = "/Users/mariakouri/Documents/python/by_commodity.csv"

    #Open CSV 
    with open(csv_filename, mode='w', newline='') as file:
        # CSV writer object
        writer = csv.writer(file)

        # Write the column headers
        writer.writerow([i[0] for i in mycursor.description])
        # Write the data rows
        writer.writerows(rows)
    mycursor.close()


#function sum by transport mode
def show_sum_by_transport_mode():
    # dictionary
    sums_by_transport_mode = {}

    #Loop through the rows 
    for row in data[1:]:
        transport_mode = row[6]
        value = float(row[8])
        if transport_mode in sums_by_transport_mode:
            sums_by_transport_mode[transport_mode] += value
        else:
            sums_by_transport_mode[transport_mode] = value

    #new tkinter window 
    root_sum_by_transport_mode = tk.Toplevel(root)
    root_sum_by_transport_mode.title("Transport")

    #symbol
    symbol = data[7][7]

    #tkinter Label for each transport_mode and its sum value
    for transport_mode, value in sums_by_transport_mode.items():
        label_text = f"{transport_mode}: {value:.2f} {symbol}"
        label = tk.Label(root_sum_by_transport_mode, text=label_text)
        label.pack()

    #bar graph
    plt.bar(sums_by_transport_mode.keys(), sums_by_transport_mode.values(), color='green')
    plt.xticks(rotation=90)
    plt.xlabel('Transport_mode')
    plt.ylabel('Value')
    plt.title('Sum of Values by Transport_mode')
    plt.show()

    mycursor = mydb.cursor()

    #tablefor the sum by transport mode
    create_table_query = """
        CREATE TABLE IF NOT EXISTS by_transport_mode (
            transport_mode VARCHAR(255) PRIMARY KEY,
            sum_value FLOAT
        )
    """
    mycursor.execute(create_table_query)

    #Insert into table
    for transport_mode, value in sums_by_transport_mode.items():
        sql = "INSERT INTO by_transport_mode (transport_mode, sum_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE sum_value = %s"
        val = (transport_mode, value, value)
        mycursor.execute(sql, val)
    mydb.commit()

    # SELECT
    mycursor.execute("SELECT * FROM by_transport_mode")

    #Fetch allrows 
    rows = mycursor.fetchall()

    #path and filename CSV file
    csv_filename = "/Users/mariakouri/Documents/python/by_transport_mode.csv"

    #CSV file in write mode
    with open(csv_filename, mode='w', newline='') as file:
        #Create a CSV writer object
        writer = csv.writer(file)

        #Write the column headers
        writer.writerow([i[0] for i in mycursor.description])

        #Write the data rows
        writer.writerows(rows)
    mycursor.close()



def show_highest_day_commodity():
    #dictionary 
    highest_day_commodity = {}

    # Loop  and find the day with the highest value for each commodity
    for row in data[1:]:
        commodity = row[5]
        value = float(row[8])
        day = row[3]

        if commodity in highest_day_commodity:
            if value > highest_day_commodity[commodity][1]:
                highest_day_commodity[commodity] = (day, value)
        else:
            highest_day_commodity[commodity] = (day, value)

    #new tkinter window 
    root_highest_value_day_by_commodity = tk.Toplevel(root)
    root_highest_value_day_by_commodity.title("Highest Value Day by Commodity")

    #symbol
    symbol = data[7][7]

    #tkinter Label
    for commodity, (day, value) in highest_day_commodity.items():
        label_text = f"{day}: {value:.2f} {str(symbol)}"

        label = tk.Label(root_highest_value_day_by_commodity, text=label_text)
        label.pack()

    #bar graph
    commodities = list(highest_day_commodity.keys())
    values = [value for _, value in highest_day_commodity.values()]

    plt.bar(commodities, values, color='red')
    plt.xlabel('Commodity')
    plt.xticks(rotation=90)
    plt.ylabel('Highest Value')
    plt.title('Highest Value Day by Commodity')
    plt.show()

    mycursor = mydb.cursor()

    #new table 
    create_table_query = """
        CREATE TABLE IF NOT EXISTS highest_day_commodity (
            commodity VARCHAR(255) PRIMARY KEY,
            highest_day VARCHAR(255),
            highest_value FLOAT
        )
    """
    mycursor.execute(create_table_query)

    # Insert 
    for commodity, (day, value) in highest_day_commodity.items():
        sql = "INSERT INTO highest_day_commodity (commodity, highest_day, highest_value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE highest_day = %s, highest_value = %s"
        val = (commodity, day, value, day, value)
        mycursor.execute(sql, val)
    mydb.commit()

    #SELECT query 
    mycursor.execute("SELECT * FROM highest_day_commodity")

    #Fetch allrows 
    rows = mycursor.fetchall()

    #path and filename CSV file
    csv_filename = "/Users/mariakouri/Documents/python/highest_day_commodity.csv"

    # Open the CSV file in write mode
    with open(csv_filename, mode='w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write the column headers
        writer.writerow([i[0] for i in mycursor.description])

        # Write the data rows
        writer.writerows(rows)
    mycursor.close()


def show_top_months():
    #dictionary 
    months_value = {}

    # sum value for each month
    for row in data[1:]:
        transportation = row[6]
        commodity = row[5]
        value = float(row[8])
        date = row[2]

        if transportation == "All" and commodity in ["Milk powder, butter, and cheese", "Fruit"]:
            # Check the date
            if date and len(date) >= 7:
                month = date[3:5]  # Extract month

                if month in months_value:
                    months_value[month] += value
                else:
                    months_value[month] = value

    # Sort the months based on the total value in descending order
    sorted_months = sorted(months_value.items(), key=lambda x: x[1], reverse=True)

    #top 5 months
    top_months = sorted_months[:5]

    #symbol from row 7
    symbol = data[7][7]

    #tkinter window
    root_top_months = tk.Toplevel(root)
    root_top_months.title("Top Months")

    #tkinter Label for each month and its total value
    for month, value in top_months:
        label_text = f"Month: {month}, Total Value: {value:.2f} {str(symbol)}"
        label = tk.Label(root_top_months, text=label_text)
        label.pack()

    # Extract the months and values for plotting
    months = [month for month, _ in top_months]
    values = [value for _, value in top_months]

   
    plt.bar(months, values, color='brown')
    plt.xlabel('Month')
    plt.ylabel('Total Value')
    plt.title('Top Months')
    plt.xticks(rotation=90)
    plt.show()

    mycursor = mydb.cursor()

    #new table in the database
    create_table_query = """
        CREATE TABLE IF NOT EXISTS top_months (
            month VARCHAR(255) PRIMARY KEY,
            total_value FLOAT
        )
    """
    mycursor.execute(create_table_query)

    #Insert into the database table
    for month, value in top_months:
        sql = "INSERT INTO top_months (month, total_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE total_value = %s"
        val = (month, value, value)
        mycursor.execute(sql, val)
    mydb.commit()

    #SELECT query 
    mycursor.execute("SELECT * FROM top_months")

    #Fetch rows
    rows = mycursor.fetchall()

    # path and filename for the CSV file
    csv_filename = "/Users/mariakouri/Documents/python/top_months.csv"

    # Open the CSV file in write mode
    with open(csv_filename, mode='w', newline='') as file:
        #CSV writer object
        writer = csv.writer(file)

        #column headers
        writer.writerow([i[0] for i in mycursor.description])

        #data rows
        writer.writerows(rows)
    mycursor.close()



# main tkinter window and title
root = tk.Tk()
root.title("Covid Data Analysis")


#custom style for the widgets
style = ttk.Style()
style.configure("TButton",
                background="light blue",
                font=("Helvetica", 13),
                padding=10)

#menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


#"Exit" option
def exit_program():
    if messagebox.askokcancel("Exit", "Do you want to exit the program?"):
        root.destroy()

#message box
def about_message():
    messagebox.showinfo("Info", "Εργασία στα πλαίσια του μαθήματος Αρχές Γλωσσών Προγραμματισμού και Μεταφραστών")

#"File" menu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Menu", menu=file_menu)

#"Exit" option to the "File" menu
file_menu.add_command(label="Exit", command=exit_program)

# "Info" menu for message
file_menu.add_command(label="Info", command=about_message)

# Add a picture to the GUI
image = tk.PhotoImage(file="/Users/mariakouri/Documents/python/tmhma.png")
smaller = image.subsample(2)
label_image = ttk.Label(root, image=smaller)
label_image.pack(padx=20, pady=20)

#text
label_text1 = "Effects of Covid-19 on-trade (15-12-2021) - provisional"

# widgets
label1 = ttk.Label(root, text=label_text1, font=("Helvetica", 9))
label1.pack(pady=(0, 5))


# Create a frame
rights_frame = ttk.Frame(root)
rights_frame.pack(side="bottom", padx=20, pady=10)

#credits frame
label_credits = ttk.Label(rights_frame, text="Created by KOURI MARIA (AM: 1084526)", font=("Helvetica", 7))
label_credits.pack()

#frame for the buttons
button_frame = ttk.Frame(root)
button_frame.pack(fill="both", expand=True, padx=20)

#buttons for each action
button_monthly_sum = ttk.Button(button_frame, text="Show Monthly Sum", command=show_monthly_sum)
button_monthly_sum.grid(row=0, column=0, padx=10, pady=10)

button_sum_by_country = ttk.Button(button_frame, text="Show Sum by Country", command=show_sum_by_country)
button_sum_by_country.grid(row=0, column=1, padx=10, pady=10)

button_sum_by_day = ttk.Button(button_frame, text="Show Sum by Day", command=show_sum_by_day)
button_sum_by_day.grid(row=1, column=0, padx=10, pady=10)

button_sum_by_commodity = ttk.Button(button_frame, text="Show Sum by Commodity", command=show_sum_by_commodity)
button_sum_by_commodity.grid(row=1, column=1, padx=10, pady=10)

button_sum_by_transport_mode = ttk.Button(button_frame, text="Show Sum by Transport Mode", command=show_sum_by_transport_mode)
button_sum_by_transport_mode.grid(row=2, column=0, padx=10, pady=10)

button_day_by_highest_commodity = ttk.Button(button_frame, text="Show Day with highest value for each commodity", command=show_highest_day_commodity)
button_day_by_highest_commodity.grid(row=2, column=1, padx=10, pady=10)

button_show_top_months = ttk.Button(button_frame, text="Show 5 months with highest value (excl. trans & recycl)", command=show_top_months)
button_show_top_months.grid(row=3, column=0, padx=10, pady=10)


# Run the tkinter event loop
root.mainloop()
mydb.commit()
mydb.close()
