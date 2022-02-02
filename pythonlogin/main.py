from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mafn2016@cu'
app.config['MYSQL_DB'] = 'test'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM LoggedInUser WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['UserName']
            # Determine the user type
            cursor.execute('SELECT UserName FROM InventoryClerk WHERE username = %s ', [username])
            InventoryClerkFlag = cursor.fetchone()
            if InventoryClerkFlag:
                session['usertype'] = "Inventory Clerk"
                return redirect(url_for('privileged_search'))

            cursor.execute('SELECT UserName FROM SalesPeople WHERE username = %s ', [username])
            SalesPeopleFlag = cursor.fetchone()
            if SalesPeopleFlag:
                session['usertype'] = "Sales People"
                return redirect(url_for('privileged_search'))

            cursor.execute('SELECT UserName FROM ServiceWriter WHERE username = %s ', [username])
            ServiceWriterFlag = cursor.fetchone()
            if ServiceWriterFlag:
                session['usertype'] = "Service Writer"
                return redirect(url_for('privileged_search'))

            cursor.execute('SELECT UserName FROM Manager WHERE username = %s ', [username])
            ManagerFlag = cursor.fetchone()
            if ManagerFlag:
                session['usertype'] = "Manager"
                return redirect(url_for('privileged_search_manager'))

            cursor.execute('SELECT UserName FROM Owner WHERE username = %s ', [username])
            OwnerFlag = cursor.fetchone()
            if OwnerFlag:
                session['usertype'] = "Owner"
                return redirect(url_for('privileged_search_manager'))

        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!")

    return render_template('auth/login.html', title="Login")


# http://localhost:5000/home
# This will be the home page, only accessible for loggedin users

# http://localhost:5000/partdetails
# This will be the enter part details page, we need to use both GET and POST requests
@app.route('/partdetails', methods=['GET', 'POST'])
def partdetails():
    # if session["usertype"]!="Owner" or session["usertype"]!="Service Writer":
    #     flash ("You do not have access to enter part details","danger")
    #     return redirect(url_for('home'))
    if request.method == 'POST' and 'vin' in request.form and 'startdate' in request.form :
        # Create variables for easy access
        vin = request.form['vin']
        startdate = request.form['startdate']
        quantity = request.form['quantity']
        vendorname = request.form['vendorname']
        partnumber = request.form['partnumber']
        price = request.form['price']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute( "SELECT * FROM Part WHERE VIN = %s and StartDate = %s and PartNumber = %s;", (vin,startdate[:4]+'-'+startdate[4:6]+'-'+startdate[-2:],partnumber))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash("Part already exists!", "danger")
        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO Part (VIN,StartDate,PartNumber,VendorName,Quantity,Price)  VALUES (%s,%s, %s, %s, %s, %s)',(vin,startdate, partnumber, vendorname,quantity, price))
            mysql.connection.commit()
            flash("You have successfully entered this part!", "success")
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!")
    if session["usertype"] == "Owner" or session["usertype"] == "Service Writer":
        return render_template('auth/partdetail.html',title="Enter Part Details")
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))

# http://localhost:5000/vehicledetails
# This will be the enter vehicle details page, we need to use both GET and POST requests
@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():

    cur = mysql.connection.cursor()
    cur.execute("SELECT Name from Manufacturer;")
    manufacturerlist = cur.fetchall()
    manufacturerlist = [x[0] for x in manufacturerlist]

    if request.method == 'POST' and 'vin' in request.form:
        # Create variables for easy access
        if request.form.get('selectvehicletype') == "Car":
            vehicletype = "Car"
        if request.form.get('selectvehicletype') == "SUV":
            vehicletype = "SUV"
        if request.form.get('selectvehicletype') == "Van":
            vehicletype = "Van"
        if request.form.get('selectvehicletype') == "Convertible":
            vehicletype = "Convertible"
        if request.form.get('selectvehicletype') == "Truck":
            vehicletype = "Convertible"

        vin = request.form['vin']
        modelname = request.form['modelname']
        modelyear = request.form['modelyear']
        invoiceprice = request.form['invoiceprice']
        description = request.form['description']
        manufacturename = request.form['manufacturename']
        vehiclecolor = request.form.get('vehiclecolor')
        username = session['username']
        adddate = date.today()
        if vehicletype == "Car":
            numdoors = request.form['numdoors']
        if vehicletype == "Convertible":
            rooftype = request.form['rooftype']
            backseatcount = request.form['backseatcount']
        if vehicletype=="Van":
            havedriversidebackdoor = request.form['havedriversidebackdoor']
        if vehicletype == "Truck":
            numrearaxles = request.form['numrearaxles']
            cargocovertype = request.form['cargocovertype']
            cargocapacity = request.form['cargocapacity']
        if vehicletype == "SUV":
            drivetraintype = request.form['drivetraintype']
            numcupholders = request.form['numcupholders']
            # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT VIN FROM AddVehicle WHERE VIN = %s;", (vin,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if int(modelyear) > date.today().year + 1 or int(modelyear) < 1900:
            flash("Please enter a valid model year!")
        elif account:
            flash("Vehicle already exists!")
        else:
            if vehicletype == "Car":
                cursor.execute('INSERT INTO Car VALUES (%s, %s, %s, %s, %s, %s, %s)',
                               (vin, modelname, modelyear, invoiceprice,description,numdoors,manufacturename))
            if vehicletype == "Van":
                cursor.execute('INSERT INTO Van VALUES (%s, %s, %s, %s, %s, %s, %s)',
                               (vin, modelname, modelyear, invoiceprice, description, havedriversidebackdoor, manufacturename))
            if vehicletype == "Truck":
                cursor.execute('INSERT INTO Truck VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               (vin, modelname, modelyear, invoiceprice, description, numrearaxles,cargocovertype,cargocapacity, manufacturename))
            if vehicletype == "SUV":
                cursor.execute('INSERT INTO SUV VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                               (vin, modelname, modelyear, invoiceprice, description, drivetraintype,numcupholders, manufacturename))
            if vehicletype == "Convertible":
                cursor.execute('INSERT INTO Convertible VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                               (vin, modelname, modelyear, invoiceprice, description, rooftype,backseatcount, manufacturename))
            cursor.execute('INSERT INTO VehicleColor VALUES (%s, %s)',(vin, vehiclecolor))
            cursor.execute('INSERT INTO AddVehicle VALUES (%s, %s,%s)', (username,vin, adddate))
            mysql.connection.commit()
            return redirect(url_for('add_vehicle_success', type=vehicletype, vin=vin))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!")
    if session["usertype"] == "Owner" or session["usertype"] == "Inventory Clerk":
        return render_template('auth/add_vehicle.html', title="Add Vehicle", manufacturerlist=manufacturerlist)
    else:
        flash("You do not have this access", "danger")
        return redirect(url_for('privileged_search'))

@app.route('/', methods=['GET', 'POST'])
def search_vehicle():

    session['loggedin'] = False
    session['usertype'] = ""

    cur = mysql.connection.cursor()
    cur.execute("SELECT Name from Manufacturer;")
    manufacturerlist = cur.fetchall()
    manufacturerlist = [x[0] for x in manufacturerlist]

    print(manufacturerlist)

    cur.execute("SELECT VIN FROM AddVehicle WHERE VIN NOT IN (SELECT DISTINCT VIN FROM Purchase);")
    num_vehicle_avail = len(cur.fetchall())

    yearlist = list(range(2000, 2023))
    yearlist.reverse()

    if request.method == "POST":

        ModelYear = request.form['ModelYear']
        Vehicletype = request.form['Vehicletype']
        Keyword = request.form['Keyword']
        Manufacturer = request.form['Manufacturer']
        Color = request.form['Color']
        ListpriceGT = request.form['ListpriceGT']
        ListpriceLT = request.form['ListpriceLT']

        if not ModelYear:
            ModelYear = '%'

        if not Vehicletype:
            Vehicletype = '%'

        if not Manufacturer:
            Manufacturer = '%'

        if not Color:
            Color = '%'

        if not ListpriceGT:
            ListpriceGT = 0

        if not ListpriceLT:
            ListpriceLT = 1000000000

        if not Keyword:
            Keyword = '%'
        else:
            Keyword = '%' + Keyword + '%'

        print(ModelYear)
        print(Vehicletype)
        print(Keyword)
        print(Manufacturer)
        print(Color)
        print(ListpriceGT)
        print(ListpriceLT)

        cur = mysql.connection.cursor()
        cur.execute(
        """
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description LIKE %s AS Matched,
        ListPrice, VehicleType, Color
        FROM
        (SELECT V.VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType, Color
        FROM
        (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType
        FROM
        (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "Truck" AS VehicleType
        FROM Truck
        UNION
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "Convertible" AS VehicleType
        FROM Convertible
        UNION
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "Car" AS VehicleType
        FROM Car
        UNION
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "Van" AS VehicleType
        FROM Van
        UNION
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "SUV" AS VehicleType
        FROM SUV) AS V
        WHERE VIN NOT IN (SELECT DISTINCT VIN FROM Purchase)) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN) AS V
        WHERE VehicleType LIKE %s AND ManufacturerName LIKE %s AND ModelYear LIKE %s AND Color LIKE %s AND ListPrice >= %s AND ListPrice <= %s 
        AND (ManufacturerName LIKE %s OR ModelYear LIKE %s OR ModelName LIKE %s OR Description LIKE %s)
        ORDER BY VIN ASC;
        """, (Keyword, Vehicletype, Manufacturer, ModelYear, Color, ListpriceGT, ListpriceLT, Keyword, Keyword, Keyword, Keyword)
        )
        vehicledetail = cur.fetchall()
        if len(vehicledetail) == 0:
            return redirect(url_for('error'))
        print(vehicledetail)

        return render_template("search_vehicle/search_vehicle.html", vehicledetail=vehicledetail, manufacturerlist=manufacturerlist, yearlist=yearlist, num_vehicle_avail=num_vehicle_avail)
    return render_template("search_vehicle/search_vehicle.html", manufacturerlist=manufacturerlist, yearlist=yearlist, num_vehicle_avail=num_vehicle_avail)


@app.route('/search_vehicle_drill_down/<string:type>-<string:vin>', methods=['GET', 'POST'])
def search_vehicle_drill_down(type, vin):
    cur = mysql.connection.cursor()

    if type == "Truck":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, ListPrice, Description,
        NumRearAxles, CargoCoverType, CargoCapacity, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice * 1.25 AS ListPrice, Description,
        NumRearAxles, CargoCoverType, CargoCapacity, ManufacturerName
        FROM Truck
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()

    elif type == "Convertible":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, ListPrice, Description,
        RoofType, BackSeatCount, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice * 1.25 AS ListPrice, Description,
        RoofType, BackSeatCount, ManufacturerName
        FROM Convertible
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()

    elif type == "Van":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, ListPrice, Description,
        HasDriverSideBackDoor, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice * 1.25 AS ListPrice, Description,
        HasDriverSideBackDoor, ManufacturerName
        FROM Van
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()       

    elif type == "Car":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, ListPrice, Description,
        NumDoors, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice * 1.25 AS ListPrice, Description,
        NumDoors, ManufacturerName
        FROM Car
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()
    else:
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, ListPrice, Description,
        DriveTrainType, NumCupholders, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice * 1.25 AS ListPrice, Description,
        DriveTrainType, NumCupholders, ManufacturerName
        FROM SUV
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()

    return render_template("search_vehicle/search_vehicle_drill_down.html", 
                            type=type, vin=vin, results=results)

@app.route('/add_vehicle_success/<string:type>-<string:vin>', methods=['GET', 'POST'])
def add_vehicle_success(type, vin):
    cur = mysql.connection.cursor()

    if type == "Truck":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice, ListPrice, Description,
        NumRearAxles, CargoCoverType, CargoCapacity, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        NumRearAxles, CargoCoverType, CargoCapacity, ManufacturerName
        FROM Truck
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()

    elif type == "Convertible":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice,ListPrice, Description,
        RoofType, BackSeatCount, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        RoofType, BackSeatCount, ManufacturerName
        FROM Convertible
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()

    elif type == "Van":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice, ListPrice, Description,
        HasDriverSideBackDoor, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        HasDriverSideBackDoor, ManufacturerName
        FROM Van
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()       

    elif type == "Car":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice, ListPrice, Description,
        NumDoors, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        NumDoors, ManufacturerName
        FROM Car
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()
    else:
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice, ListPrice, Description,
        DriveTrainType, NumCupholders, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        DriveTrainType, NumCupholders, ManufacturerName
        FROM SUV
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()

    return render_template("search_vehicle/add_vehicle_success.html", 
                            type=type, results=results)

@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():

    if request.method == "POST":

        ID = request.form['ID']

        cur = mysql.connection.cursor()

        cur.execute("""
        SELECT PB.CustomerID, ID, FirstName, LastName, BusinessName, EmailAddress, PhoneNumber 
        FROM
        (SELECT CustomerID, DriverLicenseNumber AS ID, FirstName, LastName, "" AS BusinessName
        FROM Person
        UNION
        SELECT CustomerID, TaxIdentificationNumber AS ID, "" AS FirstName, "" AS LastName, BusinessName 
        FROM Business) AS PB
        LEFT JOIN
        Customer C
        ON PB.CustomerID = C.CustomerID
        WHERE ID = %s;
        """, (ID,)
        )

        customer_record = cur.fetchall()

        return render_template("auth/search_customer.html", customer_record=customer_record) 
    return render_template("auth/search_customer.html")



@app.route('/privileged_search', methods=['GET', 'POST'])
def privileged_search():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Name from Manufacturer;")
    manufacturerlist = cur.fetchall()
    manufacturerlist = [x[0] for x in manufacturerlist]

    print(manufacturerlist)

    cur.execute("SELECT VIN FROM AddVehicle WHERE VIN NOT IN (SELECT DISTINCT VIN FROM Purchase);")
    num_vehicle_avail = len(cur.fetchall())

    yearlist = list(range(2000, 2023))
    yearlist.reverse()

    if request.method == "POST":

        VIN = request.form['VIN']
        ModelYear = request.form['ModelYear']
        Vehicletype = request.form['Vehicletype']
        Keyword = request.form['Keyword']
        Manufacturer = request.form['Manufacturer']
        Color = request.form['Color']
        ListpriceGT = request.form['ListpriceGT']
        ListpriceLT = request.form['ListpriceLT']

        if not VIN:
            VIN = '%'

        if not ModelYear:
            ModelYear = '%'

        if not Vehicletype:
            Vehicletype = '%'

        if not Manufacturer:
            Manufacturer = '%'

        if not Color:
            Color = '%'

        if not ListpriceGT:
            ListpriceGT = 0

        if not ListpriceLT:
            ListpriceLT = 1000000000

        if not Keyword:
            Keyword = '%'
        else:
            Keyword = '%' + Keyword + '%'

        print(ModelYear)
        print(Vehicletype)
        print(Keyword)
        print(Manufacturer)
        print(Color)
        print(ListpriceGT)
        print(ListpriceLT)

        cur = mysql.connection.cursor()
        cur.execute(
        """
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description LIKE %s AS Matched, 
        ListPrice, VehicleType, Color
        FROM
        (SELECT V.VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType, Color
        FROM
        (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType
        FROM
        (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "Truck" AS VehicleType
        FROM Truck
        UNION
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "Convertible" AS VehicleType
        FROM Convertible
        UNION
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "Car" AS VehicleType
        FROM Car
        UNION
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "Van" AS VehicleType
        FROM Van
        UNION
        SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
        InvoicePrice * 1.25 AS ListPrice, "SUV" AS VehicleType
        FROM SUV) AS V
        WHERE VIN NOT IN (SELECT DISTINCT VIN FROM Purchase)) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN) AS V
        WHERE VIN LIKE %s AND VehicleType LIKE %s AND ManufacturerName LIKE %s AND ModelYear LIKE %s AND Color LIKE %s AND ListPrice >= %s AND ListPrice <= %s 
        AND (ManufacturerName LIKE %s OR ModelYear LIKE %s OR ModelName LIKE %s OR Description LIKE %s)
        ORDER BY VIN ASC;
        """, (Keyword, VIN, Vehicletype, Manufacturer, ModelYear, Color, ListpriceGT, ListpriceLT, Keyword, Keyword, Keyword, Keyword)
        )
        vehicledetail = cur.fetchall()
        if len(vehicledetail) == 0:
            return redirect(url_for('error'))
        print(vehicledetail)

        return render_template("search_vehicle/privileged_search.html", vehicledetail=vehicledetail, manufacturerlist=manufacturerlist, yearlist=yearlist, num_vehicle_avail=num_vehicle_avail)
    return render_template("search_vehicle/privileged_search.html", manufacturerlist=manufacturerlist, yearlist=yearlist, num_vehicle_avail=num_vehicle_avail)


@app.route('/privileged_search_manager', methods=['GET', 'POST'])
def privileged_search_manager():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Name from Manufacturer;")
    manufacturerlist = cur.fetchall()
    manufacturerlist = [x[0] for x in manufacturerlist]

    print(manufacturerlist)

    cur.execute("SELECT VIN FROM AddVehicle WHERE VIN NOT IN (SELECT DISTINCT VIN FROM Purchase);")
    num_vehicle_avail = len(cur.fetchall())

    yearlist = list(range(2000, 2023))
    yearlist.reverse()

    if request.method == "POST":

        Filter = request.form['Filter']
        VIN = request.form['VIN']
        ModelYear = request.form['ModelYear']
        Vehicletype = request.form['Vehicletype']
        Keyword = request.form['Keyword']
        Manufacturer = request.form['Manufacturer']
        Color = request.form['Color']
        ListpriceGT = request.form['ListpriceGT']
        ListpriceLT = request.form['ListpriceLT']

        if not VIN:
            VIN = '%'

        if not ModelYear:
            ModelYear = '%'

        if not Vehicletype:
            Vehicletype = '%'

        if not Manufacturer:
            Manufacturer = '%'

        if not Color:
            Color = '%'

        if not ListpriceGT:
            ListpriceGT = 0

        if not ListpriceLT:
            ListpriceLT = 1000000000

        if not Keyword:
            Keyword = '%'
        else:
            Keyword = '%' + Keyword + '%'

        print(ModelYear)
        print(Vehicletype)
        print(Keyword)
        print(Manufacturer)
        print(Color)
        print(ListpriceGT)
        print(ListpriceLT)

        if Filter == "Unsold":

            cur = mysql.connection.cursor()
            cur.execute(
            """
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description LIKE %s AS Matched, 
            ListPrice, VehicleType, Color
            FROM
            (SELECT V.VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType, Color
            FROM
            (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType
            FROM
            (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Truck" AS VehicleType
            FROM Truck
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Convertible" AS VehicleType
            FROM Convertible
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Car" AS VehicleType
            FROM Car
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Van" AS VehicleType
            FROM Van
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "SUV" AS VehicleType
            FROM SUV) AS V
            WHERE VIN NOT IN (SELECT DISTINCT VIN FROM Purchase)) AS V
            LEFT JOIN
            (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
            FROM VehicleColor
            GROUP BY VIN) AS VC
            ON V.VIN = VC.VIN) AS V
            WHERE VIN LIKE %s AND VehicleType LIKE %s AND ManufacturerName LIKE %s AND ModelYear LIKE %s AND Color LIKE %s AND ListPrice >= %s AND ListPrice <= %s 
            AND (ManufacturerName LIKE %s OR ModelYear LIKE %s OR ModelName LIKE %s OR Description LIKE %s)
            ORDER BY VIN ASC;
            """, (Keyword, VIN, Vehicletype, Manufacturer, ModelYear, Color, ListpriceGT, ListpriceLT, Keyword, Keyword, Keyword, Keyword)
            )
            vehicledetail = cur.fetchall()

        elif Filter == "Sold":

            cur = mysql.connection.cursor()
            cur.execute(
            """
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description LIKE %s AS Matched, 
            ListPrice, VehicleType, Color
            FROM
            (SELECT V.VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType, Color
            FROM
            (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType
            FROM
            (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Truck" AS VehicleType
            FROM Truck
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Convertible" AS VehicleType
            FROM Convertible
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Car" AS VehicleType
            FROM Car
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Van" AS VehicleType
            FROM Van
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "SUV" AS VehicleType
            FROM SUV) AS V
            WHERE VIN IN (SELECT DISTINCT VIN FROM Purchase)) AS V
            LEFT JOIN
            (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
            FROM VehicleColor
            GROUP BY VIN) AS VC
            ON V.VIN = VC.VIN) AS V
            WHERE VIN LIKE %s AND VehicleType LIKE %s AND ManufacturerName LIKE %s AND ModelYear LIKE %s AND Color LIKE %s AND ListPrice >= %s AND ListPrice <= %s 
            AND (ManufacturerName LIKE %s OR ModelYear LIKE %s OR ModelName LIKE %s OR Description LIKE %s)
            ORDER BY VIN ASC;
            """, (Keyword, VIN, Vehicletype, Manufacturer, ModelYear, Color, ListpriceGT, ListpriceLT, Keyword, Keyword, Keyword, Keyword)
            )
            vehicledetail = cur.fetchall()

        else:

            cur = mysql.connection.cursor()
            cur.execute(
            """
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description LIKE %s AS Matched, 
            ListPrice, VehicleType, Color
            FROM
            (SELECT V.VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType, Color
            FROM
            (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, ListPrice, VehicleType
            FROM
            (SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Truck" AS VehicleType
            FROM Truck
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Convertible" AS VehicleType
            FROM Convertible
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Car" AS VehicleType
            FROM Car
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "Van" AS VehicleType
            FROM Van
            UNION
            SELECT VIN, ManufacturerName, ModelName, ModelYear, Description, 
            InvoicePrice * 1.25 AS ListPrice, "SUV" AS VehicleType
            FROM SUV) AS V
            WHERE VIN IN (SELECT DISTINCT VIN FROM AddVehicle)) AS V
            LEFT JOIN
            (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
            FROM VehicleColor
            GROUP BY VIN) AS VC
            ON V.VIN = VC.VIN) AS V
            WHERE VIN LIKE %s AND VehicleType LIKE %s AND ManufacturerName LIKE %s AND ModelYear LIKE %s AND Color LIKE %s AND ListPrice >= %s AND ListPrice <= %s 
            AND (ManufacturerName LIKE %s OR ModelYear LIKE %s OR ModelName LIKE %s OR Description LIKE %s)
            ORDER BY VIN ASC;
            """, (Keyword, VIN, Vehicletype, Manufacturer, ModelYear, Color, ListpriceGT, ListpriceLT, Keyword, Keyword, Keyword, Keyword)
            )
            vehicledetail = cur.fetchall()

        if len(vehicledetail) == 0:
            return redirect(url_for('error'))

        print(vehicledetail)

        return render_template("search_vehicle/privileged_search_manager.html", vehicledetail=vehicledetail, manufacturerlist=manufacturerlist, yearlist=yearlist, num_vehicle_avail=num_vehicle_avail)
    return render_template("search_vehicle/privileged_search_manager.html", manufacturerlist=manufacturerlist, yearlist=yearlist, num_vehicle_avail=num_vehicle_avail)

@app.route('/vehicle_detail_manager/<string:type>-<string:vin>', methods=['GET', 'POST'])
def vehicle_detail_manager(type, vin):
    cur = mysql.connection.cursor()

    if type == "Truck":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice, ListPrice, Description,
        NumRearAxles, CargoCoverType, CargoCapacity, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        NumRearAxles, CargoCoverType, CargoCapacity, ManufacturerName
        FROM Truck
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()

    elif type == "Convertible":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice,ListPrice, Description,
        RoofType, BackSeatCount, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        RoofType, BackSeatCount, ManufacturerName
        FROM Convertible
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()

    elif type == "Van":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice, ListPrice, Description,
        HasDriverSideBackDoor, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        HasDriverSideBackDoor, ManufacturerName
        FROM Van
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()       

    elif type == "Car":
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice, ListPrice, Description,
        NumDoors, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        NumDoors, ManufacturerName
        FROM Car
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()
    else:
        cur.execute(
        """
        SELECT V.VIN, ModelName, ModelYear, InvoicePrice, ListPrice, Description,
        DriveTrainType, NumCupholders, ManufacturerName, Color
        FROM
        (SELECT VIN, ModelName, ModelYear, InvoicePrice, InvoicePrice * 1.25 AS ListPrice, Description,
        DriveTrainType, NumCupholders, ManufacturerName
        FROM SUV
        WHERE VIN = %s) AS V
        LEFT JOIN
        (SELECT VIN, GROUP_CONCAT(DISTINCT Color) AS Color
        FROM VehicleColor
        GROUP BY VIN) AS VC
        ON V.VIN = VC.VIN;
        """, (vin,)
        )
        results = cur.fetchall()

    cur.execute(
        """
        SELECT VIN, AddDate, FirstName, LastName 
        FROM
        AddVehicle A
        LEFT JOIN
        (SELECT IO.UserName, FirstName, LastName
        FROM (SELECT UserName FROM InventoryClerk UNION SELECT UserName FROM Owner) AS IO
        INNER JOIN LoggedInUser L
        ON IO.UserName = L.UserName) AS S
        ON A.UserName = S.UserName
        WHERE VIN = %s;
        """, (vin,)
        )

    results_add_history = cur.fetchall()

    cur.execute(
        """
        SELECT VIN, FirstName, LastName, BusinessName, EmailAddress, PhoneNumber,
        Address, City, State, PostalCode, SoldPrice, PurchaseDate, SalesFirstName, SalesLastName
        FROM
        (SELECT VIN, CustomerID, PurchaseDate, SoldPrice, SalesFirstName, SalesLastName 
        FROM Purchase P
        LEFT JOIN
        (SELECT SO.UserName, FirstName AS SalesFirstName, LastName AS SalesLastName 
        FROM
        (SELECT UserName FROM SalesPeople UNION SELECT UserName FROM Owner) AS SO
        LEFT JOIN
        LoggedInUser L
        ON SO.UserName = L.UserName) AS U
        ON P.SalespeopleUserName = U.UserName) AS PU
        LEFT JOIN
        (SELECT 
        CP.CustomerID, CP.FirstName, CP.LastName, BusinessName, 
        EmailAddress, PhoneNumber, Address, City, State, PostalCode 
        FROM
        (SELECT C.CustomerID, FirstName, LastName, EmailAddress, PhoneNumber, Address, City, State, PostalCode 
        FROM Customer C LEFT JOIN Person P
        ON P.CustomerID = C.CustomerID) AS CP
        LEFT JOIN Business B
        ON CP.CustomerID = B.CustomerID) AS C
        ON PU.CustomerID = C.CustomerID
        WHERE VIN = %s;
        """, (vin,)
        )

    results_sale_history = cur.fetchall()

    cur.execute(
        """
        SELECT VIN, FirstName, LastName, BusinessName, ServiceFirstName, ServiceLastName,
        StartDate, DateCompleted, LaborCharges, CAST(PartCost AS DECIMAL(10,2)), 
        CAST(TotalCost AS DECIMAL(10,2)) FROM
        (SELECT VIN, StartDate, DateCompleted, LaborCharges, PartCost,
        TotalCost, CustomerID, ServiceFirstName, ServiceLastName FROM
        (SELECT 
        R.VIN, R.StartDate, DateCompleted, LaborCharges, PartCost,
        LaborCharges + IFNULL(PartCost,0) AS TotalCost, UserName, CustomerID 
        FROM
        (SELECT VIN, StartDate, DateCompleted, LaborCharges, UserName, CustomerID FROM Repair) AS R
        LEFT JOIN
            (SELECT VIN, StartDate, SUM(Quantity * Price) AS PartCost 
            FROM Part
            GROUP BY VIN, StartDate) AS NP
        ON R.VIN = NP.VIN AND R.StartDate = NP.StartDate) AS R
        LEFT JOIN
        (SELECT SO.UserName, FirstName AS ServiceFirstName, LastName AS ServiceLastName 
        FROM
        (SELECT UserName FROM ServiceWriter UNION SELECT UserName FROM Owner) AS SO
        LEFT JOIN
        LoggedInUser L
        ON SO.UserName = L.UserName) AS U
        ON R.UserName = U.UserName) AS RU
        LEFT JOIN
        (SELECT 
        CP.CustomerID, CP.FirstName, CP.LastName, BusinessName
        FROM
        (SELECT C.CustomerID, FirstName, LastName, EmailAddress, PhoneNumber, Address, City, State, PostalCode 
        FROM Customer C LEFT JOIN Person P
        ON P.CustomerID = C.CustomerID) AS CP
        LEFT JOIN Business B
        ON CP.CustomerID = B.CustomerID) AS C
        ON RU.CustomerID = C.CustomerID
        WHERE VIN = %s;
        """, (vin,)
        )

    results_repair_history = cur.fetchall()

    return render_template("search_vehicle/vehicle_detail_manager.html", 
                            type=type, vin=vin, results=results, results_add_history=results_add_history,
                            results_sale_history=results_sale_history, results_repair_history=results_repair_history)

@app.route('/error')
def error():
    return render_template("search_vehicle/error.html")

# http://localhost:5000/customerinfo
# This will be the enter vehicle details page, we need to use both GET and POST requests
@app.route('/customerinfo', methods=['GET', 'POST'])
def customerinfo():
    if request.method == 'POST' and 'customerid' in request.form :
        # Create variables for easy access
        if request.form.get('selectcustomertype')=="Business":
            customertype="Business"
        if request.form.get('selectcustomertype')=="Person":
            customertype="Person"

        customerid = request.form['customerid']
        emailaddress = request.form['emailaddress']
        phonenumber = request.form['phonenumber']
        address = request.form['address']
        postalcode = request.form['postalcode']
        city = request.form['city']
        state = request.form['state']
        if customertype=="Person":
            licensenumber=request.form['licensenumber']
            customerfirstname=request.form['customerfirstname']
            customerlastname = request.form['customerlastname']
        if customertype == "Business":
            tin = request.form['tin']
            businessname = request.form['businessname']
            businessfirstname = request.form['businessfirstname']
            businesslastname = request.form['businesslastname']
            title = request.form['title']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute( "SELECT * FROM Customer WHERE CustomerID = %s", [customerid] )
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash("Customer already exists!", "danger")
        else:
            cursor.execute('INSERT INTO Customer VALUES (%s, %s, %s, %s, %s,%s,%s)',(customerid, emailaddress, phonenumber, address, city,state,postalcode))
            if customertype=="Person":
                cursor.execute('INSERT INTO Person VALUES (%s, %s, %s, %s)',(customerid,licensenumber,customerfirstname,customerlastname))
            if customertype=="Business":
                cursor.execute('INSERT INTO Business VALUES (%s, %s, %s, %s, %s,%s)',(customerid,tin,businessname,businessfirstname,businesslastname,title))
            mysql.connection.commit()
            flash("You have successfully entered this customer!", "success")
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!")
    if session["usertype"] == "Owner" or session["usertype"] == "Sales People" or session["usertype"] == "Service Writer":
        return render_template('auth/customerinfo.html',title="Enter Customer Information")
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))

# http://localhost:5000/updatemanufacturerlist
# This will be the enter vehicle details page, we need to use both GET and POST requests
@app.route('/manufacturerlist', methods=['GET', 'POST'])
def manufacturerlist():

    cursor = mysql.connection.cursor()
    cursor.execute(
    """
    SELECT Name FROM Manufacturer
    WHERE Name NOT IN
    (SELECT ManufacturerName FROM Truck
    UNION
    SELECT ManufacturerName FROM Convertible
    UNION
    SELECT ManufacturerName FROM SUV
    UNION
    SELECT ManufacturerName FROM Van
    UNION
    SELECT ManufacturerName FROM Car);
    """
    )
    delete_list = cursor.fetchall()
    delete_list = [x[0] for x in delete_list]

    if request.method == 'POST' and ('manufacturer_to_add' or 'manufacturer_to_delete'):
        manufacturer_to_add = request.form['manufacturer_to_add']
        manufacturer_to_delete = request.form['manufacturer_to_delete']
        if request.form["submit_button"] == "Add Manufacturer":
            if not manufacturer_to_add:
                flash("Please Enter the Manufacturer Name", "danger")
            else:
                # Check if account exists using MySQL
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute( "SELECT * FROM Manufacturer WHERE Name = %s;", [manufacturer_to_add] )
                account = cursor.fetchone()
                # If account exists show error and validation checks
                if account:
                    flash("Manufacturer already exists!", "danger")
                else:
                    cursor.execute('INSERT INTO Manufacturer VALUES (%s);',[manufacturer_to_add])
                    mysql.connection.commit()
                    flash("You have successfully entered this manufacturer!", "success")
        elif request.form["submit_button"]=="Delete Manufacturer":
            # Check if account exists using MySQL
            if manufacturer_to_delete:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute( "SELECT * FROM Manufacturer WHERE Name = %s;", [manufacturer_to_delete] )
                account = cursor.fetchone()
                # If account exists show error and validation checks
                if not account:
                    flash("Manufacturer not exists!", "warning")
                    return redirect(url_for('manufacturerlist'))
                else:
                    cursor.execute('DELETE FROM Manufacturer where Name = %s;',[manufacturer_to_delete])
                    mysql.connection.commit()
                    flash("You have successfully deleted this manufacturer!", "success")
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!")
    if session["usertype"] in ["Owner", "Inventory Clerk"]:
        return render_template('auth/manufacturerlist.html',title="Update Manufacturer List", delete_list=delete_list)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))


# http://localhost:5000/saletransaction
# This will be the enter vehicle details page, we need to use both GET and POST requests
@app.route('/saletransaction', methods=['GET', 'POST'])
@app.route('/saletransaction/<string:vin>', methods=['GET', 'POST'])
def saletransaction(vin):
    if request.method == 'POST':
        if request.form["submit_button"]=="Validate Customer":
            #validate if customer exists. if not, redirect to enter customer info
            customerid=request.form.get('customerid')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT CustomerID FROM Customer WHERE CustomerID = %s", [customerid])
            customer = cursor.fetchone()
            if customer:
                flash("Customer exists","Success")
            else:
                flash("Customer not exist. Please enter new info","warning")
                return redirect(url_for('customerinfo'))
        elif request.form["submit_button"]=="Validate Vehicle":
            #validate if vehicle exists. If not, prohibit proceeding
            vin = request.form.get('vin')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM (select VIN from Car as A UNION select VIN from SUV as B UNION select VIN from Convertible as C UNION select VIN from Truck as D UNION select VIN from Van as E) as F WHERE VIN LIKE %s", [vin])
            vehicleininventory = cursor.fetchone()
            cursor.execute("SELECT * FROM Purchase WHERE VIN LIKE %s",[vin])
            vehicleinpurchase = cursor.fetchone()
            if vehicleinpurchase:
                flash("Vehicle already sold", "Success")
            elif vehicleininventory:
                flash("Vehicle exists and ready for sale", "Success")
            else:
                flash("Vehicle not exist. Check the inventory", "danger")

        elif request.form["submit_button"]=="Enter":
            customerid = request.form.get('customerid')
            vin = request.form.get('vin')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM Purchase WHERE VIN = %s",[vin])
            vehicleinpurchase = cursor.fetchone()
            if vehicleinpurchase:
                flash("Vehicle already sold")
            else:
                purchasedate=request.form["purchasedate"]
                soldprice=request.form["soldprice"]
                salespeopleusername=session['username']
                if not (customerid and purchasedate and soldprice):
                    flash("Please fill the form completely")
                else:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("SELECT InvoicePrice FROM (select VIN,InvoicePrice from Car as A UNION select VIN,InvoicePrice from SUV as B UNION select VIN,InvoicePrice from Convertible as C UNION select VIN,InvoicePrice from Truck as D UNION select VIN,InvoicePrice from Van as E) as F WHERE VIN = %s", [vin])
                    invoiceprice = cursor.fetchone()["InvoicePrice"]
                    print(invoiceprice)
                    if float(soldprice) <= 0.95 * invoiceprice and session["usertype"] != "Owner":
                        flash("Sold price lower than 95% of invoice price. Sale rejected!", "danger")
                    else:
                        cursor.execute("INSERT into Purchase values (%s,%s,%s,%s,%s)" ,(vin, customerid,purchasedate,soldprice,salespeopleusername))
                        mysql.connection.commit()
                        flash("You have successfully entered this transaction!", "success")
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!")
    if session["usertype"] == "Owner" or session["usertype"] == "Sales People":
        return render_template('auth/saletransaction.html', vin=vin, title="Enter Sale Transaction")
    else:
        flash("You do not have this access", "danger")
        return redirect(url_for('search_vehicle'))

@app.route('/repairdetail', methods=['GET', 'POST'])
def repairdetail():
    if request.method == 'POST':
        if request.form["submit_button"]=="Validate Vehicle":
            # validate if vehicle exists. If not, prohibit proceeding
            vin = request.form.get('vin')
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT PurchaseDate, VIN FROM Purchase WHERE VIN = %s",(vin,))
            vehicle = cursor.fetchone()
            if vehicle:
                flash("VIN validated! The vehicle was sold by us on " + str(vehicle[0]) + ".")
            else:
                flash("The vehicle doesn't exist or we never sold it. Please check the inventory.")

        elif request.form["submit_button"]=="Validate Customer":
            # validate if customer exists. if not, redirect to enter customer info
            vin = request.form.get('vin')
            customerid = request.form.get('customerid')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT CustomerID FROM Customer;")
            customerlist = cursor.fetchall()
            print(customerlist)
            customerlist = [x[0] for x in customerlist]
            if customerid in customerlist:
                flash("Good! The customer is in the database", "Success")
            else:
                flash("Cannot Proceed! The customer is not in the database. Please add a new customer.", "warning")
                return redirect(url_for('customerinfo'))

        elif request.form["submit_button"]=="Validate Repair":
            vin = request.form.get('vin')
            customerid = request.form.get('customerid')
            startdate = request.form["startdate"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT VIN, CustomerID, StartDate,DateCompleted FROM Repair WHERE VIN = %s AND StartDate = %s", [vin,startdate])
            repair = cursor.fetchone()
            if not repair:
                flash("This will be a new repair!")
            else:
                flash("This repair started on " + str(repair["StartDate"]) + " and completed on " + str(repair["DateCompleted"]))

        elif request.form["submit_button"]=="Enter":
            customerid = request.form.get('customerid')
            vin = request.form.get('vin')
            startdate=request.form["startdate"]
            datecompleted=request.form["datecompleted"]
            odometer=request.form["odometer"]
            laborcharges=request.form["laborcharges"]
            username = session['username']
            description = request.form["description"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if datecompleted:
                cursor.execute("INSERT into Repair values (%s,%s,%s,%s,%s,%s,%s,%s)" ,(vin, startdate,datecompleted,odometer,customerid,laborcharges,username,description))
            else:
                cursor.execute("INSERT into Repair (VIN, StartDate, Odometer, CustomerID, LaborCharges, UserName, Description) values (%s,%s,%s,%s,%s,%s,%s)" ,(vin, startdate,odometer,customerid,laborcharges,username,description))
            mysql.connection.commit()
            flash("You have successfully entered this repair!", "success")
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!")
    if session["usertype"] == "Owner" or session["usertype"] == "Service Writer":
        return render_template('auth/repairdetail.html', title="Add a Repair")
    else:
        flash("You do not have this access", "danger")
        return redirect(url_for('search_vehicle'))


@app.route('/generate_reports', methods=['GET', 'POST'])
def generate_reports():
    if session["usertype"] in ["Owner", "Manager"]:
        return render_template('auth/generate_reports.html', title="Generate Reports")
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))

@app.route('/parts_statistics', methods=['GET', 'POST'])
def parts_statistics():
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT VendorName, SUM(Quantity) AS NumParts, CAST(SUM(Quantity * Price) AS DECIMAL(10,2)) AS TotalCost
    FROM Part
    GROUP BY VendorName
    ORDER BY TotalCost DESC;
    """
    )
    parts_details = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/parts_statistics.html", parts_details=parts_details)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))

@app.route('/gross_customer_income', methods=['GET', 'POST'])
def gross_customer_income():
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT
        FirstName, LastName, BusinessName, 
        FirstServiceDate, LastServiceDate,
        NumRepairs, NumSales, CAST(GrossIncome AS DECIMAL(10,2)) AS GrossIncome, CPB.CustomerID
    FROM
        (SELECT
            CustomerID,
            SUM(CASE ServiceType WHEN 'Repair' THEN 1 ELSE 0 END) AS NumRepairs,
            SUM(CASE ServiceType WHEN 'Sale' THEN 1 ELSE 0 END) AS NumSales,
            MAX(ServiceDate) AS LastServiceDate,
            MIN(ServiceDate) AS FirstServiceDate,
            SUM(Income) AS GrossIncome
        FROM
            (SELECT 
                CustomerID, R.StartDate AS ServiceDate, LaborCharges + IFNULL(PartCost,0) AS Income, 'Repair' AS ServiceType 
            FROM
                (SELECT VIN, CustomerID, StartDate, LaborCharges FROM Repair) AS R
                LEFT JOIN
                    (SELECT VIN, StartDate, SUM(Quantity * Price) AS PartCost 
                    FROM Part
                    GROUP BY VIN, StartDate) AS NP
                ON R.VIN = NP.VIN AND R.StartDate = NP.StartDate
            UNION
            (SELECT CustomerID, PurchaseDate AS ServiceDate, SoldPrice AS Income, 'Sale' AS ServiceType
            FROM Purchase)) AS PR
        GROUP BY CustomerID) AS GI
        LEFT JOIN
            (SELECT 
                CP.CustomerID, CP.FirstName, CP.LastName, BusinessName 
            FROM
                (SELECT C.CustomerID, FirstName, LastName 
                FROM Customer C LEFT JOIN Person P
                ON P.CustomerID = C.CustomerID) AS CP
                LEFT JOIN Business B
                ON CP.CustomerID = B.CustomerID) AS CPB
        ON GI.CustomerID = CPB.CustomerID
    ORDER BY GrossIncome DESC, LastServiceDate DESC LIMIT 15;
    """
    )
    results = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/gross_customer_income.html", results=results)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))

@app.route('/gross_customer_income_drill_down/<string:customer_id>', methods=['GET', 'POST'])
def gross_customer_income_drill_down(customer_id):
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT
        VIN, PurchaseDate, SoldPrice, ManufacturerName,
        ModelYear, ModelName, FirstName AS SalesFirstName, LastName AS SalesLastName, CustomerID
    FROM
        (SELECT
            VIN, PurchaseDate, SoldPrice, ManufacturerName,
            ModelYear, ModelName, 
            FirstName AS CustomerFirstName,
            LastName AS CustomerLastName,
            BusinessName, SalespeopleUsername, VP.CustomerID
        FROM
            (SELECT 
                P.VIN, CustomerID, PurchaseDate, SoldPrice,
                ModelYear, ModelName, SalespeopleUsername, ManufacturerName 
            FROM
                (SELECT 
                    VIN, CustomerID, PurchaseDate, SoldPrice,
                    SalespeopleUsername
                FROM Purchase) AS P
                LEFT JOIN
                    (SELECT VIN, ModelYear, ModelName, ManufacturerName FROM Truck
                    UNION
                    SELECT VIN, ModelYear, ModelName, ManufacturerName FROM Convertible
                    UNION
                    SELECT VIN, ModelYear, ModelName, ManufacturerName FROM SUV
                    UNION
                    SELECT VIN, ModelYear, ModelName, ManufacturerName FROM Van
                    UNION
                    SELECT VIN, ModelYear, ModelName, ManufacturerName FROM Car) AS V
                ON P.VIN = V.VIN) AS VP
            LEFT JOIN
                (SELECT 
                    CP.CustomerID, CP.FirstName, CP.LastName, BusinessName 
                FROM
                    (SELECT C.CustomerID, FirstName, LastName 
                    FROM Customer C LEFT JOIN Person P
                    ON P.CustomerID = C.CustomerID) AS CP
                    LEFT JOIN Business B
                    ON CP.CustomerID = B.CustomerID) AS CPB
            ON VP.CustomerID = CPB.CustomerID) AS VPC
        LEFT JOIN
            (SELECT SO.UserName, FirstName, LastName
            FROM (SELECT UserName FROM SalesPeople UNION SELECT UserName FROM Owner) AS SO
            INNER JOIN LoggedInUser L
            ON SO.UserName = L.UserName) AS S
        ON VPC.SalespeopleUsername = S.UserName
    WHERE CustomerID = %s
    ORDER BY PurchaseDate DESC, VIN ASC;
    """, (customer_id,)
    )
    results_sales = cur.fetchall()

    cur.execute(
    """
    SELECT
        VIN, StartDate, DateCompleted, Odometer, LaborCharges, 
        CAST(PartCost AS DECIMAL(10,2)) AS PartCost, CAST(TotalCost AS DECIMAL(10,2)) AS TotalCost,
        FirstName AS ServiceWriterFirstName, LastName AS ServiceWriterLastName, CR.CustomerID
    FROM
        (SELECT
            VIN, StartDate, DateCompleted, Odometer, LaborCharges, PartCost, TotalCost, UserName,
            FirstName AS CustomerFirstName, LastName AS CustomerLastName, BusinessName, CPB.CustomerID
        FROM
            (SELECT 
                R.VIN, R.StartDate, DateCompleted, Odometer, CustomerID, LaborCharges, PartCost,
                UserName, LaborCharges + IFNULL(PartCost,0) AS TotalCost 
            FROM
                (SELECT VIN, StartDate, DateCompleted, Odometer, CustomerID, LaborCharges, UserName FROM Repair) AS R
                LEFT JOIN
                    (SELECT VIN, StartDate, SUM(Quantity * Price) AS PartCost 
                    FROM Part
                    GROUP BY VIN, StartDate) AS NP
                ON R.VIN = NP.VIN AND R.StartDate = NP.StartDate) AS R
            LEFT JOIN
                (SELECT 
                    CP.CustomerID, CP.FirstName, CP.LastName, BusinessName 
                FROM
                    (SELECT C.CustomerID, FirstName, LastName 
                    FROM Customer C LEFT JOIN Person P
                    ON P.CustomerID = C.CustomerID) AS CP
                    LEFT JOIN Business B
                    ON CP.CustomerID = B.CustomerID) AS CPB
            ON R.CustomerID = CPB.CustomerID) AS CR
    LEFT JOIN
        (SELECT SO.UserName, FirstName, LastName
        FROM (SELECT UserName FROM Servicewriter UNION SELECT UserName FROM Owner) AS SO
        INNER JOIN LoggedInUser L
        ON SO.UserName = L.UserName) AS S
    ON CR.UserName = S.UserName
    WHERE CustomerID = %s
    ORDER BY DateCompleted IS NULL DESC, StartDate DESC, DateCompleted DESC, VIN ASC;
    """, (customer_id,)
    )
    results_repairs = cur.fetchall()
    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/gross_customer_income_drill_down.html", results_sales=results_sales, results_repairs=results_repairs)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))

@app.route('/repairs_by_manufacturer', methods=['GET', 'POST'])
def repairs_by_manufacturer():
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT 
        Manufacturer,
        SUM(CASE WHEN StartDate IS NOT NULL THEN 1 ELSE 0 END) AS NumRepairs,
        SUM(LaborCharges) AS AllLaborCharge,
        CAST(SUM(PartCost) AS DECIMAL(10,2)) AS AllPartCost,
        CAST(SUM(TotalCost) AS DECIMAL(10,2)) AS AllTotalCost
    FROM
        (SELECT M.Name AS Manufacturer, VIN 
        FROM
            (SELECT Name FROM Manufacturer) AS M
            LEFT JOIN
                (SELECT VIN, ManufacturerName FROM Truck
                UNION SELECT VIN, ManufacturerName FROM Convertible
                UNION SELECT VIN, ManufacturerName FROM SUV
                UNION SELECT VIN, ManufacturerName FROM Van
                UNION SELECT VIN, ManufacturerName FROM Car) AS VM
            ON M.Name = VM.ManufacturerName) AS VM
        LEFT JOIN
            (SELECT 
                R.VIN, R.StartDate, LaborCharges, PartCost,
                LaborCharges + IFNULL(PartCost,0) AS TotalCost 
            FROM
                (SELECT VIN, StartDate, LaborCharges FROM Repair) AS R
                LEFT JOIN
                    (SELECT VIN, StartDate, SUM(Quantity * Price) AS PartCost 
                    FROM Part
                    GROUP BY VIN, StartDate) AS NP
                ON R.VIN = NP.VIN AND R.StartDate = NP.StartDate) AS R
        ON VM.VIN = R.VIN
    GROUP BY Manufacturer
    ORDER BY Manufacturer ASC;
    """
    )
    results = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/repairs_by_manufacturer.html", results=results)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))


@app.route('/repairs_by_type/<string:manufacturer>', methods=['GET', 'POST'])
def repairs_by_type_drill_down(manufacturer):
    cur = mysql.connection.cursor()

    cur.execute(
    """
    SELECT 
        VehicleType AS ModelType,
        VehicleType,
        COUNT(*) AS NumRepairs,
        SUM(LaborCharges) AS AllLaborCharge,
        CAST(SUM(PartCost) AS DECIMAL(10,2)) AS AllPartCost,
        CAST(SUM(TotalCost) AS DECIMAL(10,2)) AS AllTotalCost,
        1 AS IsType
    FROM
        (SELECT VIN, ManufacturerName, "Truck" AS VehicleType FROM Truck
        UNION SELECT VIN, ManufacturerName, "Convertible" AS VehicleType FROM Convertible
        UNION SELECT VIN, ManufacturerName, "SUV" AS VehicleType FROM SUV 
        UNION SELECT VIN, ManufacturerName, "Van" AS VehicleType FROM Van
        UNION SELECT VIN, ManufacturerName, "Car" AS VehicleType FROM Car) AS VT
        RIGHT JOIN
            (SELECT 
                R.VIN, R.StartDate, LaborCharges, PartCost,
                LaborCharges + IFNULL(PartCost,0) AS TotalCost 
            FROM
                (SELECT VIN, StartDate, LaborCharges FROM Repair) AS R
                LEFT JOIN
                    (SELECT VIN, StartDate, SUM(Quantity * Price) AS PartCost 
                    FROM Part
                    GROUP BY VIN, StartDate) AS NP
                ON R.VIN = NP.VIN AND R.StartDate = NP.StartDate) AS R
        ON VT.VIN = R.VIN
    WHERE ManufacturerName = %s
    GROUP BY VehicleType
    UNION
    SELECT 
        ModelName AS ModelType,
        VehicleType,
        COUNT(*) AS NumRepairs,
        SUM(LaborCharges) AS AllLaborCharge,
        CAST(SUM(PartCost) AS DECIMAL(10,2)) AS AllPartCost,
        CAST(SUM(TotalCost) AS DECIMAL(10,2)) AS AllTotalCost,
        0 AS IsType
    FROM
        (SELECT VIN, ModelName, ManufacturerName, "Truck" AS VehicleType FROM Truck
        UNION SELECT VIN, ModelName, ManufacturerName, "Convertible" AS VehicleType FROM Convertible
        UNION SELECT VIN, ModelName, ManufacturerName, "SUV" AS VehicleType FROM SUV 
        UNION SELECT VIN, ModelName, ManufacturerName, "Van" AS VehicleType FROM Van
        UNION SELECT VIN, ModelName, ManufacturerName, "Car" AS VehicleType FROM Car) AS VT
        RIGHT JOIN
            (SELECT 
                R.VIN, R.StartDate, LaborCharges, PartCost,
                LaborCharges + IFNULL(PartCost,0) AS TotalCost 
            FROM
                (SELECT VIN, StartDate, LaborCharges FROM Repair) AS R
                LEFT JOIN
                    (SELECT VIN, StartDate, SUM(Quantity * Price) AS PartCost 
                    FROM Part
                    GROUP BY VIN, StartDate) AS NP
                ON R.VIN = NP.VIN AND R.StartDate = NP.StartDate) AS R
        ON VT.VIN = R.VIN
    WHERE ManufacturerName = %s
    GROUP BY ModelName, VehicleType
    ORDER BY VehicleType ASC, NumRepairs DESC;
    """, (manufacturer, manufacturer)
    )
    results = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/repairs_by_type_drill_down.html", results=results, manufacturer=manufacturer)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))

    
@app.route('/monthly_sales', methods=['GET', 'POST'])
def monthly_sales():
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT 
        YEAR(PurchaseDate) AS Year, MONTH(PurchaseDate) AS Month,
        COUNT(*) AS NumSold,
        SUM(SoldPrice) AS SalesIncome, (SUM(SoldPrice) - SUM(InvoicePrice)) AS NetIncome,
        (SUM(SoldPrice) / SUM(InvoicePrice) * 100) AS Ratio
    FROM
        (SELECT VIN, PurchaseDate, SoldPrice FROM Purchase) AS P
        INNER JOIN
            (SELECT VIN, InvoicePrice FROM Truck
            UNION SELECT VIN, InvoicePrice FROM Convertible
            UNION SELECT VIN, InvoicePrice FROM SUV
            UNION SELECT VIN, InvoicePrice FROM Van
            UNION SELECT VIN, InvoicePrice FROM Car) AS V
        ON P.VIN = V.VIN
    GROUP BY Year, Month
    ORDER BY Year DESC, Month DESC;
    """
    )
    results = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/monthly_sales.html", results=results)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))


@app.route('/monthly_sales_drill_down/<int:year>-<int:month>', methods=['GET', 'POST'])
def monthly_sales_drill_down(year, month):
    cur = mysql.connection.cursor()

    cur.execute(
    """
    SELECT 
        FirstName, LastName, COUNT(*) AS NumSold, SUM(SoldPrice) AS TotalSales
    FROM
        (SELECT VIN, PurchaseDate, SoldPrice, SalespeopleUsername
        FROM Purchase
        WHERE YEAR(PurchaseDate) = %s AND MONTH(PurchaseDate) = %s) AS P
        INNER JOIN
            (SELECT SO.UserName, FirstName, LastName
            FROM (SELECT UserName FROM SalesPeople UNION SELECT UserName FROM Owner) AS SO
            INNER JOIN LoggedInUser L
            ON SO.UserName = L.UserName) AS S
        ON P.SalespeopleUsername = S.UserName
    GROUP BY FirstName, LastName
    ORDER BY NumSold DESC, TotalSales DESC;
    """, (year, month)
    )
    results = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/monthly_sales_drill_down.html", year=year, month=month, results=results)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))


@app.route('/below_cost_sales', methods=['GET', 'POST'])
def below_cost_sales():
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT 
        PurchaseDate, InvoicePrice, SoldPrice, Ratio,
        CustomerFirstName, CustomerLastName, BusinessName, SalesFirstName, SalesLastName
    FROM
        (SELECT 
            PurchaseDate, InvoicePrice, SoldPrice, SalespeopleUsername, Ratio,
            CustomerFirstName, CustomerLastName, BusinessName
        FROM
            (SELECT 
                PurchaseDate, InvoicePrice, SoldPrice, CustomerID, SalespeopleUsername,
                (SoldPrice/InvoicePrice * 100) AS Ratio
            FROM
                (SELECT VIN, InvoicePrice FROM Truck
                UNION SELECT VIN, InvoicePrice FROM Convertible
                UNION SELECT VIN, InvoicePrice FROM SUV
                UNION SELECT VIN, InvoicePrice FROM Van
                UNION SELECT VIN, InvoicePrice FROM Car) AS V
            INNER JOIN Purchase P ON V.VIN = P.VIN HAVING Ratio < 100) AS VP
        LEFT JOIN
            (SELECT 
                CP.CustomerID, CP.FirstName AS CustomerFirstName, CP.LastName AS CustomerLastName, BusinessName 
            FROM
                (SELECT C.CustomerID, FirstName, LastName 
                FROM Customer C LEFT JOIN Person P
                ON P.CustomerID = C.CustomerID) CP
            LEFT JOIN Business B
            ON CP.CustomerID = B.CustomerID) AS CPB
        ON VP.CustomerID = CPB.CustomerID) AS VPC
    LEFT JOIN
        (SELECT SO.UserName, FirstName AS SalesFirstName, LastName AS SalesLastName 
        FROM (SELECT UserName FROM SalesPeople UNION SELECT UserName FROM Owner) AS SO
        INNER JOIN LoggedInUser L
        ON SO.UserName = L.UserName) AS S
    ON VPC.SalespeopleUsername = S.UserName
    ORDER BY PurchaseDate DESC, Ratio DESC;
    """
    )
    results = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/below_cost_sales.html", results=results)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))


@app.route('/avg_time_in_inventory', methods=['GET', 'POST'])
def avg_time_in_inventory():
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT 
        VehicleType, AVG(DATEDIFF(PurchaseDate, AddDate)) + 1 AS AvgDaysInventory 
    FROM
        (SELECT VT.VIN, VehicleType, AddDate FROM
            (SELECT VIN, "Truck" AS VehicleType FROM Truck
            UNION SELECT VIN, "Convertible" AS VehicleType FROM Convertible
            UNION SELECT VIN, "SUV" AS VehicleType FROM SUV 
            UNION SELECT VIN, "Van" AS VehicleType FROM Van
            UNION SELECT VIN, "Car" AS VehicleType FROM Car) AS VT
        LEFT JOIN
            (SELECT VIN, AddDate FROM AddVehicle) AS A
        ON VT.VIN = A.VIN) AS VTA
        LEFT JOIN
            (SELECT VIN, PurchaseDate FROM Purchase) AS P
        ON VTA.VIN = P.VIN
    GROUP BY VehicleType
    ORDER BY VehicleType ASC;
    """
    )
    results = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/avg_time_in_inventory.html", results=results)
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))


@app.route('/sales_by_color', methods=['GET', 'POST'])
def sales_by_color():
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT AB.Color, AllTime, ThePreviousYear, ThePrevious30Day 
    FROM
    ((SELECT A.Color, AllTime, ThePreviousYear
    FROM
    ((SELECT Color, SUM(CASE WHEN PurchaseDate IS NOT NULL THEN 1 ELSE 0 END) AS AllTime
    FROM
        (SELECT VC.VIN, Color, PurchaseDate 
        FROM
            (SELECT DISTINCT V.VIN, CASE WHEN NUM > 1 THEN "multiple" ELSE Color END AS Color
            FROM
                (SELECT VIN, COUNT(Color) AS NUM FROM VehicleColor GROUP BY VIN) AS C
            RIGHT JOIN VehicleColor V
            ON C.VIN = V.VIN) AS VC
        LEFT JOIN
            (SELECT VIN, PurchaseDate FROM Purchase) AS P
        ON VC.VIN = P.VIN) AS VCP
    GROUP BY Color) AS A
    LEFT JOIN
    (SELECT Color, SUM(CASE WHEN PurchaseDate IS NOT NULL THEN 1 ELSE 0 END) AS ThePreviousYear
    FROM
        (SELECT VC.VIN, Color, PurchaseDate 
        FROM
            (SELECT DISTINCT V.VIN, CASE WHEN NUM > 1 THEN "multiple" ELSE Color END AS Color
            FROM
                (SELECT VIN, COUNT(Color) AS NUM FROM VehicleColor GROUP BY VIN) AS C
            RIGHT JOIN VehicleColor V
            ON C.VIN = V.VIN) AS VC
        LEFT JOIN
            (SELECT VIN, PurchaseDate FROM Purchase 
            HAVING DATEDIFF((SELECT MAX(PurchaseDate) FROM Purchase), PurchaseDate) < 365) AS P 
        ON VC.VIN = P.VIN) AS VCP
    GROUP BY Color) AS B
    ON A.Color = B.Color)) AS AB
    LEFT JOIN
    (SELECT Color, SUM(CASE WHEN PurchaseDate IS NOT NULL THEN 1 ELSE 0 END) AS ThePrevious30Day
    FROM
        (SELECT VC.VIN, Color, PurchaseDate 
        FROM
            (SELECT DISTINCT V.VIN, CASE WHEN NUM > 1 THEN "multiple" ELSE Color END AS Color
            FROM
                (SELECT VIN, COUNT(Color) AS NUM FROM VehicleColor GROUP BY VIN) AS C
            RIGHT JOIN VehicleColor V
            ON C.VIN = V.VIN) AS VC
        LEFT JOIN
            (SELECT VIN, PurchaseDate FROM Purchase 
            HAVING DATEDIFF((SELECT MAX(PurchaseDate) FROM Purchase), PurchaseDate) < 30) AS P 
        ON VC.VIN = P.VIN) AS VCP
    GROUP BY Color) AS C
    ON AB.Color = C.Color)
    ORDER BY Color ASC;
    """
    )
    stats = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/sales_by_variable.html", stats=stats, variable = "Color")
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))


@app.route('/sales_by_manufacturer', methods=['GET', 'POST'])
def sales_by_manufacturer():
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT AB.ManufacturerName, AllTime, ThePreviousYear, ThePrevious30Day
    FROM
    ((SELECT A.ManufacturerName, AllTime, ThePreviousYear
    FROM
    ((SELECT 
        ManufacturerName, COUNT(ManufacturerName) AS AllTime
    FROM
        (SELECT VM.VIN, ManufacturerName, PurchaseDate FROM
            (SELECT VIN, ManufacturerName FROM Truck
            UNION SELECT VIN, ManufacturerName FROM Convertible
            UNION SELECT VIN, ManufacturerName FROM SUV
            UNION SELECT VIN, ManufacturerName FROM Van
            UNION SELECT VIN, ManufacturerName FROM Car) AS VM
        INNER JOIN
            (SELECT VIN, PurchaseDate FROM Purchase) AS P
        ON VM.VIN = P.VIN) AS VMP
    GROUP BY ManufacturerName) AS A
    LEFT JOIN
    (SELECT 
        ManufacturerName, COUNT(ManufacturerName) AS ThePreviousYear
    FROM
        (SELECT VM.VIN, ManufacturerName, PurchaseDate FROM
            (SELECT VIN, ManufacturerName FROM Truck
            UNION SELECT VIN, ManufacturerName FROM Convertible
            UNION SELECT VIN, ManufacturerName FROM SUV
            UNION SELECT VIN, ManufacturerName FROM Van
            UNION SELECT VIN, ManufacturerName FROM Car) AS VM
        INNER JOIN
            (SELECT VIN, PurchaseDate FROM Purchase 
            HAVING DATEDIFF((SELECT MAX(PurchaseDate) FROM Purchase), PurchaseDate) < 365) AS P
        ON VM.VIN = P.VIN) AS VMP
    GROUP BY ManufacturerName) AS B
    ON A.ManufacturerName = B.ManufacturerName)) AS AB
    LEFT JOIN
    (SELECT 
        ManufacturerName, COUNT(ManufacturerName) AS ThePrevious30Day
    FROM
        (SELECT VM.VIN, ManufacturerName, PurchaseDate FROM
            (SELECT VIN, ManufacturerName FROM Truck
            UNION SELECT VIN, ManufacturerName FROM Convertible
            UNION SELECT VIN, ManufacturerName FROM SUV
            UNION SELECT VIN, ManufacturerName FROM Van
            UNION SELECT VIN, ManufacturerName FROM Car) AS VM
        INNER JOIN
            (SELECT VIN, PurchaseDate FROM Purchase 
            HAVING DATEDIFF((SELECT MAX(PurchaseDate) FROM Purchase), PurchaseDate) < 30) AS P
        ON VM.VIN = P.VIN) AS VMP
    GROUP BY ManufacturerName) AS C
    ON AB.ManufacturerName = C.ManufacturerName)
    ORDER BY ManufacturerName ASC;
    """
    )
    stats = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/sales_by_variable.html", stats=stats, variable = "Manufacturer")
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))


@app.route('/sales_by_type', methods=['GET', 'POST'])
def sales_by_type():
    cur = mysql.connection.cursor()
    cur.execute(
    """
    SELECT AB.VehicleType, AllTime, ThePreviousYear, ThePrevious30Day
    FROM
    ((SELECT A.VehicleType, AllTime, ThePreviousYear
    FROM 
    ((SELECT 
        VehicleType, SUM(CASE WHEN PurchaseDate IS NOT NULL THEN 1 ELSE 0 END) AS AllTime
    FROM
        (SELECT VT.VIN, VehicleType, PurchaseDate FROM
            (SELECT VIN, "Truck" AS VehicleType FROM Truck
            UNION SELECT VIN, "Convertible" AS VehicleType FROM Convertible
            UNION SELECT VIN, "SUV" AS VehicleType FROM SUV 
            UNION SELECT VIN, "Van" AS VehicleType FROM Van
            UNION SELECT VIN, "Car" AS VehicleType FROM Car) AS VT
        LEFT JOIN
            (SELECT VIN, PurchaseDate FROM Purchase) AS P
        ON VT.VIN = P.VIN) AS VTP
    GROUP BY VehicleType) AS A
    LEFT JOIN
    (SELECT 
        VehicleType, SUM(CASE WHEN PurchaseDate IS NOT NULL THEN 1 ELSE 0 END) AS ThePreviousYear
    FROM
        (SELECT VT.VIN, VehicleType, PurchaseDate FROM
            (SELECT VIN, "Truck" AS VehicleType FROM Truck
            UNION SELECT VIN, "Convertible" AS VehicleType FROM Convertible
            UNION SELECT VIN, "SUV" AS VehicleType FROM SUV 
            UNION SELECT VIN, "Van" AS VehicleType FROM Van
            UNION SELECT VIN, "Car" AS VehicleType FROM Car) AS VT
        LEFT JOIN
            (SELECT VIN, PurchaseDate FROM Purchase 
            HAVING DATEDIFF((SELECT MAX(PurchaseDate) FROM Purchase), PurchaseDate) < 365) AS P
        ON VT.VIN = P.VIN) AS VTP
    GROUP BY VehicleType) AS B
    ON A.VehicleType = B.VehicleType)) AS AB
    LEFT JOIN
    (SELECT 
        VehicleType, SUM(CASE WHEN PurchaseDate IS NOT NULL THEN 1 ELSE 0 END) AS ThePrevious30Day
    FROM
        (SELECT VT.VIN, VehicleType, PurchaseDate FROM
            (SELECT VIN, "Truck" AS VehicleType FROM Truck
            UNION SELECT VIN, "Convertible" AS VehicleType FROM Convertible
            UNION SELECT VIN, "SUV" AS VehicleType FROM SUV 
            UNION SELECT VIN, "Van" AS VehicleType FROM Van
            UNION SELECT VIN, "Car" AS VehicleType FROM Car) AS VT
        LEFT JOIN
            (SELECT VIN, PurchaseDate FROM Purchase 
            HAVING DATEDIFF((SELECT MAX(PurchaseDate) FROM Purchase), PurchaseDate) < 30) AS P
        ON VT.VIN = P.VIN) AS VTP
    GROUP BY VehicleType) AS C
    ON AB.VehicleType = C.VehicleType)
    ORDER BY VehicleType ASC;
    """
    )
    stats = cur.fetchall()

    if session["usertype"] in ["Owner", "Manager"]:
        return render_template("reports/sales_by_variable.html", stats=stats, variable = "Type")
    else:
        flash ("You do not have this access","danger")
        return redirect(url_for('search_vehicle'))


if __name__ =='__main__':
	app.run(debug=True)
