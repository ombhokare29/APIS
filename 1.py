from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello api is working fine🦾"

@app.route('/search')
def search():
    name = request.args.get('name')
    city = request.args.get('city')

    if not name or not city:
        return {"Error": "name and city are required"},400
    return f"serching for {name} and {city}"
    # return {
    #     "name" : name,
    #     "city" : city
    # }

if __name__ == '__main__' :
    app.run(debug=True)