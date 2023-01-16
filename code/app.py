from flask import Flask, jsonify, request
import retrieve_db
import json

app=Flask(__name__)

@app.route('/kim/v1/st-retrieve', methods=['POST','GET'])
def retrieve():
    args_data=request.get_data()
    print(args_data)
    data=json.loads(args_data)
    ticker=data.get('ticker')

    response=retrieve_db.retrieve(ticker)
    return response

if __name__=='__main__':
    app.run(debug=True)


