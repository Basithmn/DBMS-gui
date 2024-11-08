from tkinter import *
from tkinter import messagebox
import mysql.connector
import tkinter as tk
from tkinter import ttk

def connect_to_db():
    try:
        global conn, cursor
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Achu0814$',
            database='bus'
        )
        if conn.is_connected():
            print("Connected to the MySQL Database successfully!")
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

class BusServiceManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Service Management System")
        self.root.geometry("1500x800+0+0")  
        self.root.config(bg="#f6e0b5")  

       
        connect_to_db()

       
        lbltitle = Label(
            self.root,
            text="BUS SERVICE MANAGEMENT SYSTEM",
            bg="#f6e0b5",
            fg="#66545e",
            bd=20,
            relief=RIDGE,
            font=("Helvetica", 40, "bold"),
            padx=2,
            pady=6
        )
        lbltitle.pack(side=TOP, fill=X)

        
        frame = Frame(self.root, bd=12, relief=RIDGE, padx=20, bg="#eea990")
        frame.place(x=0, y=130, width=1480, height=400)

        
        Button(
            frame,
            text="Login",
            command=self.open_login_window,
            width=20,
            font=("Helvetica", 14),
            bg="#aa6f73",
            fg="#f6e0b5"
        ).pack(pady=10)

        
        Button(
            frame,
            text="Register",
            command=self.user_registration,
            width=20,
            font=("Helvetica", 14),
            bg="#aa6f73",
            fg="#f6e0b5"
        ).pack(pady=10)

    def open_login_window(self):
        login_window = Toplevel(self.root)
        login_window.title("Login")
        login_window.configure(bg="#8B4513")

        Label(login_window, text="Username:", font=("Helvetica", 14), bg="#8B4513", fg="white").grid(row=0, column=0, padx=10, pady=5)
        username_entry = Entry(login_window, font=("Helvetica", 14))
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(login_window, text="Password:", font=("Helvetica", 14), bg="#8B4513", fg="white").grid(row=1, column=0, padx=10, pady=5)
        password_entry = Entry(login_window, show="*", font=("Helvetica", 14))
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        def handle_login():
            username = username_entry.get() 
            password = password_entry.get() 
            try: 
                cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s AND status = 'approved'", (username, password)) 
                result = cursor.fetchone() 
                if result: 
                    role = result[0] 
                    login_window.destroy() 
                    if role == 'admin': 
                        self.admin_dashboard() 
                    else:
                        self.user_dashboard() 
                else: 
                    messagebox.showerror("Login Failed", "Invalid credentials or approval pending.") 
            except mysql.connector.Error as err:
                messagebox.showerror("Login Error", f"Error: {err}")

        Button(login_window, text="Login", font=("Helvetica", 14), command=handle_login, bg="#006400", fg="white").grid(row=2, column=1, pady=10)


    def user_registration(self):
        reg_window = Toplevel(self.root)
        reg_window.title("User Registration")

        Label(reg_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        username_entry = Entry(reg_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(reg_window, text="Name:").grid(row=1, column=0, padx=10, pady=5)
        name_entry = Entry(reg_window)
        name_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(reg_window, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        email_entry = Entry(reg_window)
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(reg_window, text="Password:").grid(row=3, column=0, padx=10, pady=5)
        password_entry = Entry(reg_window, show="*")
        password_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(reg_window, text="Confirm Password:").grid(row=4, column=0, padx=10, pady=5)
        confirm_password_entry = Entry(reg_window, show="*")
        confirm_password_entry.grid(row=4, column=1, padx=10, pady=5)

        def handle_registration():
            username = username_entry.get()
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()

            if password != confirm_password:
                messagebox.showerror("Password Error", "Passwords do not match!")
                return

            if not username or not name or not email or not password:
                messagebox.showerror("Input Error", "All fields are required!")
                return

           
            cursor.execute("INSERT INTO users (username, name, email, password, role, status) VALUES (%s, %s, %s, %s, %s, %s)",
                           (username, name, email, password, 'user', 'pending'))
            conn.commit()
            messagebox.showinfo("Registration Successful", "Your account has been created and is awaiting approval.")
            reg_window.destroy()

        Button(reg_window, text="Register", command=handle_registration).grid(row=5, column=1, pady=10)

    def validate_admin_login(self, password):
        if password == "admin123":
            messagebox.showinfo("Admin Login", "Admin logged in successfully!")
            return True
        else:
            messagebox.showerror("Login Failed", "Invalid admin password.")
            return False


    def approve_user(self, username):
        
        try:
            cursor.execute("UPDATE users SET status = 'approved' WHERE username = %s", (username,))
            conn.commit()
            messagebox.showinfo("Approval", f"User {username} has been approved!") 
            self.open_approval_form() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Database Error", f"Error: {err}")

    def reject_user(self, username):
        try:
            cursor.execute("UPDATE users SET status = 'rejected' WHERE username = %s", (username,))
            conn.commit()
            messagebox.showinfo("Rejection", f"User {username} has been rejected!")
            self.open_approval_form()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


    def open_approval_form(self):
        approval_window = Toplevel(self.root)
        approval_window.title("User Approval")
        approval_window.geometry("1500x800+0+0")

        cursor.execute("SELECT username, name, email FROM users WHERE status = 'pending'")
        users = cursor.fetchall()

        Label(approval_window, text="Approve Users", font=("Helvetica", 16)).pack(pady=20)

        for user in users:
            frame = Frame(approval_window, bd=2, relief=RIDGE, padx=10, pady=5) 
            frame.pack(fill='x', padx=10, pady=5) 
        
            user_info = f"Username: {user[0]} | Name: {user[1]} | Email: {user[2]}" 
            Label(frame, text=user_info, font=("Helvetica", 12)).pack(side=LEFT, padx=5) 
        
            Button(frame, text="Approve", font=("Helvetica", 12), command=lambda u=user[0]: self.approve_user(u)).pack(side=RIGHT, padx=5) 
            Button(frame, text="Reject", font=("Helvetica", 12), command=lambda u=user[0]: self.reject_user(u)).pack(side=RIGHT, padx=5)

    def admin_dashboard(self):
        dashboard_window = Toplevel(self.root)
        dashboard_window.title("Admin Dashboard")
        dashboard_window.geometry("1500x800+0+0")
        dashboard_window.configure(bg="#8B4513")

        Label(dashboard_window, text="Welcome Admin!", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)
        Button(dashboard_window, text="Approve Users", font=("Helvetica", 14), command=self.open_approval_form, bg="#aa6f73", fg="white").pack(pady=10)

    def user_dashboard(self):
        dashboard_window = Toplevel(self.root) 
        dashboard_window.title("User Dashboard") 
        dashboard_window.geometry("1500x800+0+0") 
        dashboard_window.configure(bg="#8B4513") 
        
        Label(dashboard_window, text="Welcome User!", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20) 
       
        Button(dashboard_window, text="Manage Employees", font=("Helvetica", 14), command=self.manage_employees, bg="#aa6f73", fg="white").pack(pady=10) 
        Button(dashboard_window, text="Manage Depots", font=("Helvetica", 14), command=self.manage_depots, bg="#aa6f73", fg="white").pack(pady=10) 
        Button(dashboard_window, text="Manage Routes", font=("Helvetica", 14), command=self.manage_routes, bg="#aa6f73", fg="white").pack(pady=10) 
        Button(dashboard_window, text="Manage Buses", font=("Helvetica", 14), command=self.manage_buses, bg="#aa6f73", fg="white").pack(pady=10)
    
    def manage_employees(self):
        emp_window = Toplevel(self.root)
        emp_window.title("Manage Employees")
        emp_window.geometry("1500x800+0+0")
        emp_window.configure(bg="#8B4513")

        Label(emp_window, text="Employee Management", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)
    
        Button(emp_window, text="Add Employee", font=("Helvetica", 14), command=self.add_employee, bg="#aa6f73", fg="white").pack(pady=10)
        Button(emp_window, text="View Employees", font=("Helvetica", 14), command=self.view_employees, bg="#aa6f73", fg="white").pack(pady=10)
        Button(emp_window, text="Delete Employee", font=("Helvetica", 14), command=self.delete_employee, bg="#aa6f73", fg="white").pack(pady=10)
  
    def add_employee(self):
        employee_form = Toplevel(root)
        employee_form.title("Add Employee")

        Label(employee_form, text="Employee Name:").grid(row=0, column=0, padx=10, pady=5)
        emp_name_entry = Entry(employee_form)
        emp_name_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(employee_form, text="Employee ID:").grid(row=1, column=0, padx=10, pady=5)
        emp_id_entry = Entry(employee_form)
        emp_id_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(employee_form, text="Joining Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        joining_date_entry = Entry(employee_form)
        joining_date_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(employee_form, text="Salary:").grid(row=3, column=0, padx=10, pady=5)
        salary_entry = Entry(employee_form)
        salary_entry.grid(row=3, column=1, padx=10, pady=5)

      
        Label(employee_form, text="House Name:").grid(row=4, column=0, padx=10, pady=5)
        house_name_entry = Entry(employee_form)
        house_name_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(employee_form, text="Pincode:").grid(row=5, column=0, padx=10, pady=5)
        pincode_entry = Entry(employee_form)
        pincode_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(employee_form, text="Landmark:").grid(row=6, column=0, padx=10, pady=5)
        landmark_entry = Entry(employee_form)
        landmark_entry.grid(row=6, column=1, padx=10, pady=5)

      
        Label(employee_form, text="Phone:").grid(row=7, column=0, padx=10, pady=5)
        phone_entry = Entry(employee_form)
        phone_entry.grid(row=7, column=1, padx=10, pady=5)

   
        def save_employee():
            name = emp_name_entry.get()
            emp_id = emp_id_entry.get()
            joining_date = joining_date_entry.get()
            salary = salary_entry.get()
            house_name = house_name_entry.get()
            pincode = pincode_entry.get()
            landmark = landmark_entry.get()
            phone = phone_entry.get()

            if not (name and emp_id and joining_date and salary and house_name and pincode and landmark and phone):
                messagebox.showerror("Input Error", "All fields are required.")
                return
            try:
                query_employee = """
                    INSERT INTO Employee1 (employee_name, E_id, salary, date_of_joining)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query_employee, (name, emp_id, salary, joining_date))
        
                
                query_phone = """
                    INSERT INTO Employee21 (E_id, phone)
                    VALUES (%s, %s)
                """
                cursor.execute(query_phone, (emp_id, phone))
        
             
                query_address = """
                    INSERT INTO E221 (E_id, House_name, PinCode, Landmark)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query_address, (emp_id, house_name, pincode, landmark))

        
        
                
                conn.commit()
                messagebox.showinfo("Success", "Employee added successfully!")
                save_employee.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        Button(employee_form, text="Save Employee", command=save_employee, bg="#006400", fg="white").grid(row=8, column=1, pady=20)

    def view_employees(self):
        
        
      
            query_employee = """
                SELECT * FROM  Employee1 
             """
            cursor.execute(query_employee)
            employees = cursor.fetchall()

        
            query_phone = """
                SELECT phone FROM Employee21 
            """
            cursor.execute(query_phone)
            phones = cursor.fetchall()

            query_address = """
                SELECT House_name,PinCode,Landmark FROM E221 
            """
            cursor.execute(query_address)
            addresses = cursor.fetchall()

            window = tk.Tk()
            window.title("Employee Details")

       
            tree = ttk.Treeview(window, columns=('Name', 'ID', 'Salary', 'Joining Date', 'Phone', 'House', 'PinCode', 'Landmark'), show='headings')
        
        
            tree.heading('ID', text='ID')
            tree.heading('Name', text='Name')
            tree.heading('Joining Date', text='Joining Date')
            tree.heading('Salary', text='Salary')
            tree.heading('Phone', text='Phone')
            tree.heading('House', text='House')
            tree.heading('PinCode', text='PinCode')
            tree.heading('Landmark', text='Landmark')

           
            for col in ('ID', 'Name', 'Joining Date', 'Salary', 'Phone', 'House', 'PinCode', 'Landmark'):
                tree.column(col, width=100)

            tree.pack(fill=tk.BOTH, expand=True)

            
            for emp, phone, address in zip(employees, phones, addresses):
                emp_id, emp_name, joining_date, salary = emp[:4]  
                phone_number = phone[0]
                house, pincode, landmark = address
                tree.insert('', tk.END, values=(emp_id, emp_name, joining_date, salary, phone_number, house, pincode, landmark))

   

    def delete_employee(self):
        delete_emp_window = Toplevel(self.root)
        delete_emp_window.title("Delete Employee")
        delete_emp_window.geometry("1500x800+0+0")
        delete_emp_window.configure(bg="#8B4513")

        Label(delete_emp_window, text="Delete Employee", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)

        Label(delete_emp_window, text="Employee ID:", font=("Helvetica", 14), bg="#8B4513", fg="white").pack(pady=10)
        id_entry = Entry(delete_emp_window, font=("Helvetica", 14))
        id_entry.pack(pady=10)

        def delete_employee_record():
            emp_id = id_entry.get()

            if not emp_id:
                messagebox.showerror("Input Error", "Employee ID is required!")
                return

            try:
                cursor.execute("DELETE FROM E221 WHERE E_id = %s", (emp_id,))
                cursor.execute("DELETE FROM Employee21 WHERE E_id = %s", (emp_id,))
                cursor.execute("DELETE FROM Employee1 WHERE E_id = %s", (emp_id,))

                conn.commit()
                messagebox.showinfo("Success", "Employee deleted successfully.")
                delete_emp_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        Button(delete_emp_window, text="Delete Employee", command=delete_employee_record, bg="#aa6f73", fg="white").pack(pady=20)



    def manage_depots(self):
        depot_window = Toplevel(self.root)
        depot_window.title("Manage Depot")
        depot_window.geometry("1500x800+0+0")
        depot_window.configure(bg="#8B4513")

        Label(depot_window, text="Depot Management", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)
    
        Button(depot_window, text="Add Depot", font=("Helvetica", 14), command=self.add_depot, bg="#aa6f73", fg="white").pack(pady=10)
        Button(depot_window, text="View Depot", font=("Helvetica", 14), command=self.view_depots, bg="#aa6f73", fg="white").pack(pady=10)
        Button(depot_window, text="Delete Depot", font=("Helvetica", 14), command=self.delete_depot, bg="#aa6f73", fg="white").pack(pady=10)
    
    def add_depot(self):
        depot_form = Toplevel(root)
        depot_form.title("Add Depot")

        Label(depot_form, text="Depot ID:").grid(row=0, column=0, padx=10, pady=5)
        depot_id_entry = Entry(depot_form)
        depot_id_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(depot_form, text="Pincode:").grid(row=1, column=0, padx=10, pady=5)
        depot_pincode_entry = Entry(depot_form)
        depot_pincode_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(depot_form, text="Capacity").grid(row=2, column=0, padx=10, pady=5)
        depot_capacity_entry = Entry(depot_form)
        depot_capacity_entry.grid(row=2, column=1, padx=10, pady=5)

       

   
        def save_depot():
            depot_id = depot_id_entry.get()
            pincode = depot_pincode_entry.get()
            capacity = depot_capacity_entry.get()
       
            if not (depot_id and pincode and capacity):
                messagebox.showerror("Input Error", "All fields are required.")
                return
            try:
                query_depot = """
                    INSERT INTO Depot1 (Depot_ID, Capacity)
                    VALUES (%s, %s)
                    """
                cursor.execute(query_depot, (depot_id, capacity))
        
                query_phone = """
                    INSERT INTO Depot2 (Depot_ID, Pincode )
                    VALUES (%s, %s)
                """
                cursor.execute(query_phone, (depot_id, pincode))
            
        
        
        
                conn.commit()
                messagebox.showinfo("Success", "Depot added successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")


        Button(depot_form, text="Save Depot", command=save_depot, bg="#006400", fg="white").grid(row=8, column=1, pady=20)

    def view_depots(self):
        
        
      
            query_depot = """
                SELECT * FROM  Depot1 
             """
            cursor.execute(query_depot)
            depots = cursor.fetchall()

        
            query_depotpin = """
                SELECT pincode FROM Depot2 
            """
            cursor.execute(query_depotpin)
            pins = cursor.fetchall()

            

            window = tk.Tk()
            window.title("Depot Details")

            tree = ttk.Treeview(window, columns=('ID', 'Capacity', 'Pincode'), show='headings')
        
            tree.heading('ID', text='ID')
            tree.heading('Capacity', text='Capacity')
            tree.heading('Pincode', text='Pincode')
            

            for col in ('ID', 'Capacity', 'Pincode'):
                tree.column(col, width=100)

            tree.pack(fill=tk.BOTH, expand=True)

            for depot, pin in zip(depots, pins):
                Depot_ID,Capacity = depot[:2]  
                pincode = pins[0]
                tree.insert('', tk.END, values=(Depot_ID, Capacity, pincode))

   

    def delete_depot(self):
        delete_depot_window = Toplevel(self.root)
        delete_depot_window.title("Delete Depot")
        delete_depot_window.geometry("1500x800+0+0")
        delete_depot_window.configure(bg="#8B4513")

        Label(delete_depot_window, text="Delete Depot", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)

        Label(delete_depot_window, text="Depot ID:", font=("Helvetica", 14), bg="#8B4513", fg="white").pack(pady=10)
        id_entry = Entry(delete_depot_window, font=("Helvetica", 14))
        id_entry.pack(pady=10)

        def delete_depot_record():
            depot_id = id_entry.get()

            if not depot_id:
                messagebox.showerror("Input Error", "Depot ID is required!")
                return

            try:
                cursor.execute("DELETE FROM Depot1 WHERE Depot_ID = %s", (depot_id,))
                cursor.execute("DELETE FROM Depot2 WHERE Depot_ID = %s", (depot_id,))

                conn.commit()
                messagebox.showinfo("Success", "Depot deleted successfully.")
                delete_depot_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        Button(delete_depot_window, text="Delete Depot", command=delete_depot_record, bg="#aa6f73", fg="white").pack(pady=20)
        

    def manage_routes(self):
        route_window = Toplevel(self.root)
        route_window.title("Manage Route")
        route_window.geometry("1500x800+0+0")
        route_window.configure(bg="#8B4513")

        Label(route_window, text="Route Management", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)
    
        Button(route_window, text="Add Route", font=("Helvetica", 14), command=self.add_route, bg="#aa6f73", fg="white").pack(pady=10)
        Button(route_window, text="View Route", font=("Helvetica", 14), command=self.view_route, bg="#aa6f73", fg="white").pack(pady=10)
        Button(route_window, text="Delete Route", font=("Helvetica", 14), command=self.delete_route, bg="#aa6f73", fg="white").pack(pady=10)
      
    def add_route(self):
        route_form = Toplevel(root)
        route_form.title("Add Route")

        Label(route_form, text="Route ID:").grid(row=0, column=0, padx=10, pady=5)
        route_id_entry = Entry(route_form)
        route_id_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(route_form, text="Start Depot ID:").grid(row=1, column=0, padx=10, pady=5)
        route_depotid_entry = Entry(route_form)
        route_depotid_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(route_form, text="Destination").grid(row=2, column=0, padx=10, pady=5)
        route_destination_entry = Entry(route_form)
        route_destination_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(route_form, text="Distance").grid(row=3, column=0, padx=10, pady=5)
        route_distance_entry = Entry(route_form)
        route_distance_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(route_form, text="TypeOfService").grid(row=4, column=0, padx=10, pady=5)
        route_Type_entry = Entry(route_form)
        route_Type_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(route_form, text="Duration").grid(row=5, column=0, padx=10, pady=5)
        route_duration_entry = Entry(route_form)
        route_duration_entry.grid(row=5, column=1, padx=10, pady=5)

       
       

   
        def save_route():
            route_id = route_id_entry.get()
            depot_id = route_depotid_entry.get()
            destination = route_destination_entry.get()
            distance = route_distance_entry.get()
            duration = route_duration_entry.get()
            TypeOfService  = route_Type_entry.get()

            if not (route_id and depot_id and destination and distance and duration and TypeOfService):
                messagebox.showerror("Input Error", "All fields are required.")
                return
            try:
                query_route = """
                    INSERT INTO Route11 (RouteID, Destination, Distance, Duration,TypeOfService)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query_route, (route_id, destination, distance, duration, TypeOfService))
        
                query_start = """
                    INSERT INTO StartsFrom1 (Route_ID, Depot_ID )
                    VALUES (%s, %s)
                """
                cursor.execute(query_start, (route_id, depot_id))
        
        
        
        
                conn.commit()
                messagebox.showinfo("Success", "Route added successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")


        Button(route_form, text="Save route", command=save_route, bg="#006400", fg="white").grid(row=8, column=1, pady=20)

    def view_route(self):
        
        
      
            query_route = """
                SELECT * FROM  Route11 
             """
            cursor.execute(query_route)
            routes = cursor.fetchall()

        
            query_depotroute = """
                SELECT depot_id FROM startsfrom1 
            """
            cursor.execute(query_depotroute)
            depotroute = cursor.fetchall()

            

            window = tk.Tk()
            window.title("Route Details")

            tree = ttk.Treeview(window, columns=('Route ID', 'Start Depot ID', 'Destination', 'Distance', 'Duration', 'Type Of Service'), show='headings')
        
            tree.heading('Route ID', text='Route ID')
            tree.heading('Start Depot ID', text='Start Depot ID')
            tree.heading('Destination', text='Destination')
            tree.heading('Distance', text='Distance')
            tree.heading('Duration', text='Duration')
            tree.heading('Type Of Service', text='Type Of Service')


            for col in ('Route ID', 'Start Depot ID', 'Destination', 'Distance', 'Duration', 'Type Of Service'):
                tree.column(col, width=100)

            tree.pack(fill=tk.BOTH, expand=True)

            for route,depotroute in zip(routes, depotroute):
                RouteID,Destination,Distance,Duration,TypeOfService = route[:5] 
                Depot_ID = depotroute[0]
                tree.insert('', tk.END, values=(RouteID,Depot_ID,Destination,Distance,TypeOfService,Duration))


    def delete_route(self):
        delete_route_window = Toplevel(self.root)
        delete_route_window.title("Delete Route")
        delete_route_window.geometry("1500x800+0+0")
        delete_route_window.configure(bg="#8B4513")

        Label(delete_route_window, text="Delete Route", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)

        Label(delete_route_window, text="RouteID:", font=("Helvetica", 14), bg="#8B4513", fg="white").pack(pady=10)
        id_entry = Entry(delete_route_window, font=("Helvetica", 14))
        id_entry.pack(pady=10)

        def delete_route_record():
            route_id = id_entry.get()

            if not route_id:
                messagebox.showerror("Input Error", "Route ID is required!")
                return

            try:
                cursor.execute("DELETE FROM route11 WHERE Route_ID = %s", (route_id,))
                cursor.execute("DELETE FROM startsfrom1 WHERE Route_ID = %s", (route_id,))

                conn.commit()
                messagebox.showinfo("Success", "Route deleted successfully.")
                delete_route_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        Button(delete_route_window, text="Delete Employee", command=delete_route_record, bg="#aa6f73", fg="white").pack(pady=20)


    def manage_buses(self):
        bus_window = Toplevel(self.root)
        bus_window.title("Manage Bus")
        bus_window.geometry("1500x800+0+0")
        bus_window.configure(bg="#8B4513")

        Label(bus_window, text="Bus Management", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)
    
        Button(bus_window, text="Add Bus", font=("Helvetica", 14), command=self.add_bus, bg="#aa6f73", fg="white").pack(pady=10)
        Button(bus_window, text="View Bus", font=("Helvetica", 14), command=self.view_bus, bg="#aa6f73", fg="white").pack(pady=10)
        Button(bus_window, text="Delete Bus", font=("Helvetica", 14), command=self.delete_bus, bg="#aa6f73", fg="white").pack(pady=10)
      
    def add_bus(self):
        bus_form = Toplevel(root)
        bus_form.title("Add Bus")

        Label(bus_form, text="Bonnet No:").grid(row=0, column=0, padx=10, pady=5)
        bus_bonnetno_entry = Entry(bus_form)
        bus_bonnetno_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(bus_form, text="Registration No:").grid(row=1, column=0, padx=10, pady=5)
        bus_regNo_entry = Entry(bus_form)
        bus_regNo_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(bus_form, text="capacity").grid(row=2, column=0, padx=10, pady=5)
        bus_capacity_entry = Entry(bus_form)
        bus_capacity_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(bus_form, text="Status").grid(row=3, column=0, padx=10, pady=5)
        bus_status_entry = Entry(bus_form)
        bus_status_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(bus_form, text="Type").grid(row=4, column=0, padx=10, pady=5)
        bus_Type_entry = Entry(bus_form)
        bus_Type_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(bus_form, text="DepotID").grid(row=5, column=0, padx=10, pady=5)
        bus_depotid_entry = Entry(bus_form)
        bus_depotid_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(bus_form, text="RouteID").grid(row=6, column=0, padx=10, pady=5)
        bus_routeid_entry = Entry(bus_form)
        bus_routeid_entry.grid(row=6, column=1, padx=10, pady=5)

       
       

   
        def save_bus():
            bonnet_no = bus_bonnetno_entry.get()
            registrationNO = bus_regNo_entry.get()
            capacity = bus_capacity_entry.get()
            status= bus_status_entry.get()
            Type = bus_Type_entry.get()
            depot_id  = bus_depotid_entry.get()
            routeid = bus_routeid_entry.get()

            if not (bonnet_no and registrationNO and capacity and status and Type and depot_id and routeid):
                messagebox.showerror("Input Error", "All fields are required.")
                return
            try: 
                query_route = """
                    INSERT INTO Bus (Bonnet_No, Registeration_No,depot_id, Capacity, status,Type)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                cursor.execute(query_route, (bonnet_no, registrationNO, depot_id,capacity, status, Type))
        
                query_start = """
                    INSERT INTO GoesThrough (Bonnet_No,Route_ID)
                    VALUES (%s, %s)
                """
                cursor.execute(query_start, (bonnet_no,routeid))

            
           
        
        
        
                conn.commit()
                messagebox.showinfo("Success", "Bus added successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")


        Button(bus_form, text="Save Bus", command=save_bus, bg="#006400", fg="white").grid(row=8, column=1, pady=20)

    def view_bus(self):
        view_bus_window = Toplevel(self.root)
        view_bus_window.title("View Buses")
        view_bus_window.geometry("1500x800+0+0")

        Label(view_bus_window, text="Bus List", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)

        frame = Frame(view_bus_window, bg="#8B4513")
        frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        columns = ("Bonnet Number", "Registration Number", "Depot ID", "Capacity", "Status", "Type")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=CENTER)

        try:
            cursor.execute("SELECT Bonnet_No, Registeration_No, depot_id, Capacity, Status, Type FROM Bus")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
   
    
    def delete_bus(self):
    
        delete_bus_window = Toplevel(self.root)
        delete_bus_window.title("Delete Bus")
        delete_bus_window.geometry("1500x800+0+0")
        delete_bus_window.configure(bg="#8B4513")

        Label(delete_bus_window, text="Delete Bus", font=("Helvetica", 16), bg="#8B4513", fg="white").pack(pady=20)

        Label(delete_bus_window, text="Bonnet NO:", font=("Helvetica", 14), bg="#8B4513", fg="white").pack(pady=10)
        id_entry = Entry(delete_bus_window, font=("Helvetica", 14))
        id_entry.pack(pady=10)

        def delete_bus_record():
            bus_id = id_entry.get()

            if not bus_id:
                messagebox.showerror("Input Error", "Bonnet No is required!")
                return

            try:
                cursor.execute("DELETE FROM Bus WHERE Bonnet_No = %s", (bus_id,))
                cursor.execute("DELETE FROM GoesThrough WHERE Bonnet_No = %s", (bus_id,))

                conn.commit()
                messagebox.showinfo("Success", "Bus deleted successfully.")
                delete_bus_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        Button(delete_bus_window, text="Delete bus", command=delete_bus_record, bg="#aa6f73", fg="white").pack(pady=20)

if __name__ == "__main__":
    root = Tk()
    app = BusServiceManagementSystem(root)
    root.mainloop()
