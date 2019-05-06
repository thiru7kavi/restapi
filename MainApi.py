from flask import Flask,request
from flask_restplus import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import fields
import yaml
import logging

app = Flask(__name__)
api = Api(app,default='Person',description='API for Managing Person info')
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def initializing_flask_config(AppFlask):
    with open('application.yml', 'r') as ml:
        flask_conf = yaml.full_load(ml)
        AppFlask.config['SQLALCHEMY_DATABASE_URI'] = flask_conf['DATABASE_URI']
        AppFlask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = flask_conf['TRACK_MODIFICATIONS']
        AppFlask.config['RESTPLUS_VALIDATE'] = flask_conf['RESTPLUS_VALIDATE']
        AppFlask.config['RESTPLUS_MASK_SWAGGER'] = flask_conf['RESTPLUS_MASK_SWAGGER']
        AppFlask.config['SWAGGER_UI_DOC_EXPANSION'] = flask_conf['DOC_EXPANSION']
        AppFlask.config['ERROR_404_HELP'] = flask_conf['RESTPLUS_ERROR_404_HELP']
initializing_flask_config(app)
db = SQLAlchemy(app)

# API model for Accessing data
personmodel = api.model('Person', {
    'identity': fields.String(readOnly=True, description='The unique identifier for Person'),
    'first_name': fields.String(required=True, description='FIRST NAME'),
    'last_name' : fields.String(required=True, description='LAST NAME'),
    'age' : fields.Integer(readOnly=True, description='AGE'),
    'favourite_colour' : fields.String(required=True, description='COLOUR'),

})

# API core
@api.route('/person')
class Create_Person(Resource):
    @api.marshal_list_with(personmodel,envelope='Persons')
    def get(self):
        try:
           person_details = person.query.all()
           return person_details
        except TypeError as e:
            logger.exception('Error couldnt Query %s', e)
    @api.response(201, 'Person successfully created.')
    @api.expect(personmodel)
    def post(self):
        try:
            data = request.json
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            age = data.get('age')
            favourite_colour = data.get('favourite_colour')
            name = first_name + last_name
            sent = person(name,first_name, last_name, age, favourite_colour)
            db.session.add(sent)
            db.session.commit()
            return 201
        except TypeError as e:
            logger.exception('Error couldnt POST %s', e)
            return 500

@api.route('/person/<int:identity>')
class Update_Person(Resource):
    @api.marshal_list_with(personmodel)
    def get(self,identity):
        try:
           person_details_id = person.query.filter(person.identity == identity).one()
           return person_details_id
        except TypeError as e:
            logger.exception('Error couldnt Query %s', e)
            return 500
    @api.response(201, 'Person successfully updated.')
    @api.expect(personmodel)
    def put(self,identity):
        try:
            data = request.json
            person_details_id = person.query.filter(person.identity == identity).one()
            person_details_id.first_name = data.get('first_name')
            person_details_id.last_name = data.get('last_name')
            person_details_id.age = data.get('age')
            person_details_id.favourite_colour = data.get('favourite_colour')
            db.session.add(person_details_id)
            db.session.commit()
            return 201
        except TypeError as e:
            logger.exception('Error couldnt PUT %s', e)
            return 500

    @api.response(201, 'Person successfully updated.')
    def delete(self,identity):
        try:
            person_details_id = person.query.filter(person.identity == identity).one()
            db.session.delete(person_details_id)
            db.session.commit()
            return 201
        except TypeError as e:
            logger.exception('Error couldnt DELETE %s', e)
            return 500

# Database model to create structure
class person(db.Model):
    identity = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    favourite_colour = db.Column(db.String(80), nullable=False)

    def __init__(self, name, first_name, last_name, age, favourite_colour):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.favourite_colour = favourite_colour

    def __repr__(self):
        return '<person %r>' % self.name

if __name__=='__main__':
    db.create_all()
    logging.info('Starting the API')
    app.run(host='0.0.0.0',debug=True)

