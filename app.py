from flask import Flask, request, jsonify
import psycopg2
import csv
import os

DB = os.environ['DATABASE_URL']
app = Flask(__name__)

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

#----------------------------------------------------------------------

@app.route('/')
def index():
    return """<pre><h1>Compendium App Backend</h1>
<h3>/term/{termid} - gets a term with termid
/terms/{topicid} - gets terms with topicid
/allterms - gets all terms

/topic/{topicic} - gets a term with topicid
/alltopics - gets all topics</h3></pre>"""

#----TERMS----
@app.route('/term/<int:termid>')
def get_term(termid):
    '''Get a term given its ID'''
    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM terms WHERE ID = %s", (termid,))
    try:
        term = cur.fetchall()[0]
        conn.close()
        return jsonify(term)
    except IndexError:
        return jsonify(None)

@app.route('/terms/<int:topicid>')
def get_terms(topicid):
    '''Get all the terms with a given topicid'''
    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM terms WHERE topicnumber = %s", (topicid,))
    try:
        terms = cur.fetchall()
        conn.close()
        return jsonify(terms)
    except Exception: #Broad error catch
        return jsonify(None)

@app.route('/allterms')
def get_all_terms():
    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM terms")
    try:
        terms = cur.fetchall()
        conn.close()
        return jsonify(terms)
    except Exception: #Broad error catch
        return jsonify(None)

#----TOPICS----
@app.route('/topic/<int:topicid>')
def get_topic(topicid):
    '''Get a topic given its ID'''
    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics WHERE ID = %s", (topicid,))
    try:
        topic = cur.fetchall()[0]
        conn.close()
        return jsonify(topic)
    except IndexError:
        return jsonify(None)

@app.route('/alltopics')
def get_all_topics():
    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics")
    try:
        topics = cur.fetchall()
        conn.close()
        return jsonify(topics)
    except Exception: #Broad error catch
        return jsonify(None)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
