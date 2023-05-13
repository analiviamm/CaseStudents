from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request
from flask import abort
import datetime

#inicializing the app 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///StudentsDB.db'

db = SQLAlchemy(app)
app.app_context().push()

class Student(db.Model):
    __tablename__ = 'students'
    matricula = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            'matricula': self.matricula,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'email': self.email,
            'telefone': self.telefone,
            'curso': self.curso,
            'data': self.data.strftime('%d/%m/%Y')
        }
        
@app.route("/")
def home():
    return "my flask app"

#READ-list of students
@app.route("/students/list", methods = ["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_json() for student in students])

#DELETE - delete a student using the matricula number as an input in the URL
#ex: /student/delete/20004
@app.route("/student/delete/<int:matricula>")
def delete_student(matricula):
    student = Student.query.get(matricula)
    if(student is None):
        abort(404)
    db.session.delete(student)
    db.session.commit()
    return jsonify(student.to_json()), 201

#CREATE- create a student with all the data as an input in the URL
#ex:student/create?matricula=20004&nome=Ana&sobrenome=Muniz&email=livialivia2307@gmail.com
#&telefone=(85)985089427&curso=Engenharia da Computacao&data=23/07/2001
@app.route("/student/create")
def create_student():
    data_str = request.args.get('data')
    date_obj = datetime.datetime.strptime(data_str, '%d/%m/%Y')
    student = Student(
        matricula = request.args.get('matricula'),
        nome = request.args.get('nome'),
        sobrenome = request.args.get('sobrenome'),
        email = request.args.get('email'),
        telefone = request.args.get('telefone'),
        curso = request.args.get('curso'),
        data = date_obj.date()      
    )
    db.session.add(student)
    db.session.commit()
    
    return jsonify(student.to_json()), 201

#UPDATE-update all data of a student (we have to provide all information in the input)
#ex: student/update?matricula=20004&nome=Ana&sobrenome=Matos&email=ana.muniz@ime.eb.br
#&telefone=(85)985089427&curso=Engenharia da Computacao&data=23/07/2001
@app.route("/student/update/")
def update_student():
    matriculaup = int(request.args.get('matricula'))
        
    student = Student.query.filter_by(matricula = matriculaup).first()
    if student is None:
        abort(404)
    
    student.nome = request.args.get('nome')
    student.sobrenome = request.args.get('sobrenome')
    student.email = request.args.get('email')
    student.telefone = request.args.get('telefone')
    student.curso = request.args.get('curso')
    data_str = request.args.get('data')
    date_obj = datetime.datetime.strptime(data_str, '%d/%m/%Y')
    student.data = date_obj.date()
    
   
    db.session.commit()
    return jsonify(student.to_json()), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    