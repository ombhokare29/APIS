from flask import Flask

# this tells , “Hey Flask, start a machine that can listen to requests”

app = Flask(__name__)

#this means if someone hits(/) run the below functions

@app.route('/') 
def home():
    return "Hello"

@app.route('/user/<int:id>')
def get_user(id):
    if(id==12):
        return {
                "id":id,
                "name": "Om"
            }
    elif(id == 11):
        return {
                "id":id,
                "name": "Nikhil     "
            }



if __name__ == '__main__':
    app.run(debug=True,port=1234)