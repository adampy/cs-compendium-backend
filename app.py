from flask import Flask, request, jsonify
import psycopg2
import csv
import os

DB = os.environ['DATABASE_URL']
k = os.environ['KEYS'].split(";")
app = Flask(__name__)

def keycheck(request):
    key = request.headers.get('key')
    if key is None:
        return False
    if key not in k:
        return False
    return True

#----------------------------------------------------------------------

@app.route('/')
def index():
    return """<pre><h1>Compendium App Backend</h1>
<h3>/term/{termid} - gets a term with termid
/terms/{topicid} - gets terms with topicid
/allterms - gets all terms

/topic/{topicid} - gets a term with topicid
/alltopics - gets all topics

/add/term - adds term with `term`, `topic`, `definition` form data
/add/topic - adds a topic with `topic`, `colour` form data

/remove/term/{termid} - removes a term with termid
/remove/topic/{topicid} - removes a topic with topicid
</h3></pre>"""

#----TERMS----
@app.route('/term/<int:termid>', methods=['GET'])
def get_term(termid):
    '''Get a term given its ID'''
    if not keycheck(request):
        return jsonify(None)
    
    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM terms WHERE ID = %s", (termid,))
    try:
        term = cur.fetchall()
        conn.close()
        return jsonify(term)
    except IndexError:
        return jsonify(None)

@app.route('/terms/<int:topicid>', methods=['GET'])
def get_terms(topicid):
    '''Get all the terms with a given topicid'''
    if not keycheck(request):
        return jsonify(None)
    
    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM terms WHERE topicnumber = %s", (topicid,))
    try:
        terms = cur.fetchall()
        conn.close()
        return jsonify(terms)
    except Exception: #Broad error catch
        return jsonify(None)

@app.route('/allterms', methods=['GET'])
def get_all_terms():
    '''Get all the terms in the term table'''
    if not keycheck(request):
        return jsonify(None)
    
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
@app.route('/topic/<int:topicid>', methods=['GET'])
def get_topic(topicid):
    '''Get a topic given its ID'''
    if not keycheck(request):
        return jsonify(None)
    
    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics WHERE ID = %s", (topicid,))
    try:
        topic = cur.fetchall()
        conn.close()
        return jsonify(topic)
    except IndexError:
        return jsonify(None)

@app.route('/alltopics', methods=['GET'])
def get_all_topics():
    '''Get all the topics in the topic table'''
    if not keycheck(request):
        return jsonify(None)
    
    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics")
    try:
        topics = cur.fetchall()
        conn.close()
        return jsonify(topics)
    except Exception: #Broad error catch
        return jsonify(None)

#----NEWDATA----
@app.route('/add/term', methods=['POST'])
def add_term():
    '''Add a term with form data'''
    if not keycheck(request):
        return jsonify(None)

    topicid = request.form.get("topic")
    term = request.form.get("term")
    definition = request.form.get("definition")
    if topicid is None or term is None or definition is None:
        return jsonify(None)

    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("INSERT INTO terms (topicnumber, term, definition) VALUES (%s, %s, %s)", (topicid, term, definition))
    conn.commit()
    conn.close()
    return jsonify(True)

@app.route('/add/topic', methods=['POST'])
def add_topic():
    '''Adds a topic with form data'''
    if not keycheck(request):
        return jsonify(None)

    topic = request.form.get("topic")
    colour = request.form.get("colour")
    if topic is None or colour is None:
        return jsonify(None)

    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("INSERT INTO topics (topic, colour) VALUES (%s, %s)", (topic, colour))
    conn.commit()
    conn.close()
    return jsonify(True)

#----REMOVEDATA----
@app.route('/remove/term/<int:termid>', methods=['POST'])
def remove_term():
    '''Removes a term with a passed id'''
    if not keycheck(request):
        return jsonify(None)

    termid = request.form.get("termid")
    if termid is None:
        return jsonify(None)

    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("DELETE FROM terms WHERE topicnumber = %s", (termid,))
    conn.commit()
    conn.close()
    return jsonify(True)

@app.route('/remove/topic/<int:topicid>', methods=['POST'])
def remove_topic():
    '''Removes a topic with a passed id'''
    if not keycheck(request):
        return jsonify(None)

    topicid = request.form.get("topicid")
    if topicid is None:
        return jsonify(None)

    conn = psycopg2.connect(DB, sslmode='require')
    cur = conn.cursor()
    cur.execute("DELETE FROM topics WHERE id = %s", (topicid,))
    conn.commit()
    conn.close()
    return jsonify(True)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
