import pandas as pd
import csv
from datetime import datetime
from data_entry import get_category,get_date,get_description,get_money
import matplotlib.pyplot as plt
class CSV:
    CSV_FILE="finance_data.csv"
    columns=["date","amount","category","description"]
    @classmethod
    #here cls is a class cls.CSV_FILE means accesing that file
    def initialise_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df=pd.DataFrame(columns=["date","amount","category","description"])
            df.to_csv(cls.CSV_FILE,index=False)
    @classmethod
    def add_entry(cls,date,amount,category,description):
        values={
            "date":date,
            "amount":amount,
            "category":category,
            "description":description,
        }
        with open(cls.CSV_FILE,"a",newline="") as csv_file:
            writer=csv.DictWriter(csv_file,fieldnames=CSV.columns)
            writer.writerow(values)
        print("entry added successfully!")

    @classmethod
    def get_transactions(cls,start_date,end_date):
        df=pd.read_csv(CSV.CSV_FILE)
        df["date"]=pd.to_datetime(df["date"],format="%d-%m-%Y")
        start_date=datetime.strptime(start_date,"%d-%m-%Y")
        end_date=datetime.strptime(end_date,"%d-%m-%Y")
        mask=(df["date"]>=start_date) & (df["date"]<=end_date)
        filtered_df=df.loc[mask]
        if(filtered_df.empty):
            print("no transactions are found")
        else:
            print(f'transactions from {start_date.strftime("%d-%m-%Y")} to {end_date.strftime("%d-%m-%Y")} are :')
            print(filtered_df.to_string(index=False,formatters={"date":lambda x:x.strftime("%d-%m-%Y")}))
            income=filtered_df[filtered_df["category"]=="Income"]["amount"].sum()
            expense=filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()
            print("\nsummary :\n")
            print(f"Total Income : {income:.2f}")
            print(f"total_Expense : {expense:.2f}")
            print(f"\nNet Savings:{income-expense:.2f}")

        return filtered_df
   
def get_graph(df):
    df.set_index("date",inplace=True)
    income_df=df[df["category"]=="Income"].resample("D").sum().reindex(df.index,fill_value=0)
    expense_df=df[df["category"]=="Expense"].resample("D").sum().reindex(df.index,fill_value=0)
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df["amount"],label="Income",color="g")
    plt.plot(expense_df.index,expense_df["amount"],label="expense",color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def add():
    CSV.initialise_csv()
    date=get_date("enter transaction date(dd-mm-yyyy) or press enter for todays date: ",default_value=True)
    amount=get_money()
    category=get_category()
    description=get_description()
    CSV.add_entry(date,amount,category,description)

def main():
    while True:
        print("\n1.Add a New Transaction")
        print("2.view transactions and summary with in a date range")
        print("3.exit")
        x=input("please choose the choices(1,2,3) as above mentioned: ")
        if x in ["1","2","3"]:
            if(x=="1"):
                add()
            elif(x=="2"):
                start_date=get_date("please enter the starting date:",True)
                end_date=get_date("please enter the end date:",True)
                df=CSV.get_transactions(start_date,end_date)
                if input("would you want to see your summary on plt(y/n): ").lower()=="y":
                    get_graph(df)

            else:
                quit()
                
        else:
            print("valid input")
            return main()
    
if (__name__=="__main__"):
    main()
    





