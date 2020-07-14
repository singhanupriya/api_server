from flask import Flask, request, Response,json

from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mydatabase'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'

mongo = PyMongo(app)


def api_response(msg, status_code):
    """
      for the API internal error responses for now we can use a general code
      future work:  error logger  troubleshooting using the result dict work with flask error handler(werkzeug)
    """
    return Response(

        mimetype="application/json",
        response=json.dumps(msg),
        status=status_code,

    )


@app.route('/headings', methods=['GET'])
def get_all_headings():
   #connect to the collection
  section = mongo.db.table
  output = []
  for s in section.find({},{ "_id": 0}):
      output.append(s)
  return jsonify(output)

@app.route('/headings/<headingId>', methods=['GET','OPTIONS'])
def get_one_heading(headingId):

    print(headingId)
    section = mongo.db.table
    q1 = list(section.find({"_id":ObjectId(headingId)},{"_id":0}))

    if q1:
        print(q1)
    else:
        print("heading not found ")


    return api_response({"data":q1},200)


#Add a heading
#Checks if a heading exists informs user about the same else creates heading
@app.route('/insert/<heading_name>', methods=['POST'])
def post_one_heading(heading_name):

    print(heading_name)
    section = mongo.db.table
    q1 = list(section.find({"Heading":heading_name},{"_id":0}))

    if q1:
        print(q1)
        print("Heading already exists")
        for i in q1:
            print(i)
    else:

        q2=section.insert_one({"Heading":heading_name})
        print("Heading has been successfully added ")


    return api_response({"data":q1},200)



##add para
#Checks if the para exists informs user else add that para
@app.route('/insert_para/<headingId>/<para_name>', methods=['POST'])
def post_one_para(headingId,para_name):
    section = mongo.db.table
    q1 = list(section.find({"Para":{'$elemMatch': {'title' : para_name}}}))
    print(q1)

    if q1:
        print("Para already exists")
    else:
        section.update({'_id': ObjectId(headingId)}, {'$push': {'Para': {"title": para_name}}})
        print("Para added")


    return api_response({"data":q1},200)


#delete a heading

@app.route('/delete/<headingId>', methods=['DELETE'])
def delete_a_heading(headingId):
    section = mongo.db.table
    q1 = list(section.find({"_id":ObjectId(headingId)}, {"_id": 0}))

    if q1:
        print(q1)
        q2 = section.remove({"_id":ObjectId(headingId)})
        print("Heading deleted")
        for i in q1:
            print(i)
    else:


        print("Heading doesn't exist ")

    return api_response({"data": q1}, 200)









if __name__ == '__main__':
    app.run(debug=True)