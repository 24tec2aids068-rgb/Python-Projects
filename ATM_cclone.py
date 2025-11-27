balance = 5000
pin = 1234

user_pin = int(input("Enter your PIN: "))

if user_pin == pin:
    amount = int(input("Enter amount: "))
    
    if amount <= balance:
        balance -= amount
        print("Withdrawal successful")
        print("Remaining Balance:", balance)
    else:
        print("Insufficient Balance")
else:
    print("Incorrect PIN")
