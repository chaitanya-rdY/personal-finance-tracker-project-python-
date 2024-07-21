from datetime import datetime

date_format="%d-%m-%Y"
categories={"i":"Income","e":"Expense"}
def get_date(promt,default_value=False):
    date_str=input(promt)
    if default_value and not date_str:
        return datetime.today().strftime(date_format)
    try:
        date_passed=datetime.strptime(date_str,date_format)
        return date_str
    except ValueError:
       return  get_date(promt,default_value)

def get_money():
    try:
        x=float(input("please enter money: "))
        if(x<=0):
            raise ValueError("only positive values are accepted")
        return x
    except ValueError as e:
        print(e)
        return get_money()

def get_category():
    x=input("please ente category ('i' for income , 'e' for expense) :").lower()
    if x in categories:
        return categories[x]
    print("invalid!")
    return get_category()


def get_description():
    return input("enter the description[optional]:")
    
