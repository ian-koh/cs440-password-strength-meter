---README---

Hi Prof, to run this code, please follow the following steps

---Activate Virtual Environment---

1.  On your bash terminal, run this command,

source venv/bin/activate

If you are using Mac, run this command

venv\Scripts\activate.bat


---Database Setup---

1. Open your WAMP/MAMP

2. Create database: "users"

3. In your PHP MyAdmin or SQL workbench, run the passwords.sql file to input sample data. 

Make sure that the port is 3306.


--- Run services manually ---

1. There are 2 services running on Flask to be run. Using your terminal, simply run both python scripts. 
 - users.py - Port 5000
 - password-policy.py - Port 5001


--- Test ---
1. You can now test the code by going to the register.html page and login.html page respectively.




