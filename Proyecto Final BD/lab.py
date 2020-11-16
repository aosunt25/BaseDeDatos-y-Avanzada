from datetime import date

now = date.today()

year = now.strftime("%Y")
print("year:", year)

month = now.strftime("%m")
print("month:", month)

day = now.strftime("%d")
print("day:", day)

myDate = now.strftime("%B %d, %Y")
print("Desired format is:", myDate)

# Splitting at '-' 
#print(today.split('-')) 


#Format: November 4, 2019