from flask import Flask,request
import logging
from flask_restplus import Resource,Api
import yaml
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import fields

app = Flask(__name__)
api = Api(app,default='Person',description='API for Managing Person info')
db = SQLAlchemy(app)
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

personmodel = api.model('Person', {
    'identity': fields.String(readOnly=True, description='The unique identifier for Person'),
    'first_name': fields.String(required=True, description='FIRST NAME'),
    'last_name' : fields.String(required=True, description='LAST NAME'),
    'age' : fields.Integer(readOnly=True, description='AGE'),
    'favourite_colour' : fields.String(required=True, description='COLOUR'),

})

@api.route('/person')
class Create_Person(Resource):
    @api.marshal_list_with(personmodel,envelope='Persons')
    def get(self):
        person_details = person.query.all()
        return person_details

    @api.response(201, 'Person successfully created.')
    @api.expect(personmodel)
    def post(self):        # use exception handler
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        age = data.get('age')
        favourite_colour = data.get('favourite_colour')
        sent = person(first_name, last_name, age, favourite_colour)
        db.session.add(sent)
        db.session.commit()
        return 201

@api.route('/person/<int:identity>')
class Update_Person(Resource):
    @api.marshal_list_with(personmodel)
    def get(self,identity):
        person_details_id = person.query.filter(person.identity == identity).one()
        return person_details_id
    @api.response(201, 'Person successfully updated.')
    @api.expect(personmodel)
    def put(self,identity):
        data = request.json
        person_details_id = person.query.filter(person.identity == identity).one()
        person_details_id.first_name = data.get('first_name')
        person_details_id.last_name = data.get('last_name')
        person_details_id.age = data.get('age')
        person_details_id.favourite_colour = data.get('favourite_colour')
        db.session.add(person_details_id)
        db.session.commit()
        return 201

    @api.response(201, 'Person successfully updated.')
    def delete(self,identity):
        person_details_id = person.query.filter(person.identity == identity).one()
        db.session.delete(person_details_id)
        db.session.commit()

def initializing_flask_config(AppFlask):
    with open('application.yml', 'r') as ml:
        flask_conf = yaml.full_load(ml)
        AppFlask.config['SQLALCHEMY_DATABASE_URI'] = flask_conf['DATABASE_URI']
        AppFlask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = flask_conf['TRACK_MODIFICATIONS']
        AppFlask.config['RESTPLUS_VALIDATE'] = flask_conf['RESTPLUS_VALIDATE']
        AppFlask.config['RESTPLUS_MASK_SWAGGER'] = flask_conf['RESTPLUS_MASK_SWAGGER']
        AppFlask.config['SWAGGER_UI_DOC_EXPANSION'] = flask_conf['RESTPLUS_SWAGGER_UI_DOC_EXPANSION']
        AppFlask.config['ERROR_404_HELP'] = flask_conf['RESTPLUS_ERROR_404_HELP']

class person(db.Model):
    identity = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    favourite_colour = db.Column(db.String(80), nullable=False)

    def __init__(self, first_name, last_name, age, favourite_colour):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.favourite_colour = favourite_colour

    def __repr__(self):
        return '<person %r>' % self.first_name

if __name__=='__main__':
    initializing_flask_config(app)
    db.create_all()
    logging.info('Starting the API')
    app.run()
