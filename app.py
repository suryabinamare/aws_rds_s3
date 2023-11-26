
# pip install flask mysql-connector-python boto3
from flask import Flask, render_template, request
import mysql.connector
import boto3

app = Flask(__name__)

# RDS credentials
db_credentials = {
    'host': 'surya-db.cg9yyqmiwyp9.us-east-2.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Binamare8*',
    'database': 'surya_database',
}
# s3 credentials
s3_credentials = {
    'aws_access_key_id': 'AKIA6HSCUECSABVCY46E',
    'aws_secret_access_key': '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',
    'region_name': 'us-east-2',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        file = request.files['file']

        # Save to RDS
        save_to_database(first_name, last_name)

        # Upload to S3
        upload_to_s3(file)

        return render_template('success.html', first_name=first_name, last_name=last_name, file_name=file.filename)

def save_to_database(first_name, last_name):
    connection = mysql.connector.connect(**db_credentials)
    cursor = connection.cursor()

    # Assuming you have a 'person' table with 'firstname' and 'lastname' columns
    query = "INSERT INTO person (firstname, lastname) VALUES (%s, %s)"
    values = (first_name, last_name)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

def upload_to_s3(file):
    s3 = boto3.client('s3', **s3_credentials)
    bucket_name = 'binamare-surya-bucket' #uncheck public access in AWS console
    key = file.filename

    s3.upload_fileobj(file, bucket_name, key)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
