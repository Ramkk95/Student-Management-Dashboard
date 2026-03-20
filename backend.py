from sqlalchemy import create_engine,text
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date



server = "DESKTOP-VOOPMIC"
database = "t2"

engine = create_engine(
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

table_creation= """if not exists (select * from sys.tables where name ='t3')
begin 
    create table t3(
            name varchar(100) not null,
            roll int not null,
            clas int not null,
            address varchar(100) not null,
            stream varchar(20) not null)
end"""

with engine.connect() as conn:
    conn.execute(text(table_creation))
    conn.commit()

app=FastAPI()

class Student(BaseModel):
    name: str
    roll: int
    address: str
    clas: int
    stream: str
@app.get("/")
def read_m():
    return {"message":"Welcome"}

@app.post("/add_student")
def read_data(student: Student):
    q1="""insert into  t3 (name,roll,address,stream,clas)
          values(:name,:roll,:address,:stream,:clas)"""
    with engine.connect() as conn:
        conn.execute(text(q1),student.model_dump())
        conn.commit()
    return{"message":"Student entered successfully"}

@app.get("/student_details/{roll}")
def read_value(roll: int):
    q2=text("""select * from t3 where roll=:roll""")

    with engine.connect() as conn:
        resl=conn.execute(q2,{"roll": roll })
        res=resl.fetchone()

        if res:
            return {
                "Name": res[0],
                "roll": res[1],
                "clas": res[2],
                "address": res[3],
                "stream": res[4]
            }
        else:
            return {"message": "Student not found"}



@app.delete("/delete/{roll}")
def delete_value(roll: int):
    q4=text(""" delete from t3 where roll=:roll""")
    with engine.connect() as conn:
        conn.execute(q4,{"roll":roll})
        conn.commit()
        return {"message":"Student deleted successfuly"}


@app.get("/student_all")
def read_value_all():
    q2=text("""select * from t3 """)

    with engine.connect() as conn:
        resl=conn.execute(q2)
        res=resl.fetchall()

        if res:
            result = []
            for row in res:
                result.append({
                    "Name": row[0],
                    "roll": row[1],
                    "clas": row[2],
                    "address": row[3],
                    "stream": row[4]
                })
            return result
        else:
            return {"message": "No Data"}