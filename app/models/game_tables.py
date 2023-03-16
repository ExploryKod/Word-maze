from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Letters(db.Model):
        # Id : Field which stores unique id for every row in
        # database table
        id = db.Column(db.Integer, primary_key=True)
        round_1 = db.Column(db.String(50), unique=False, nullable=True)
        round_2 = db.Column(db.String(50), unique=False, nullable=True)
        round_3 = db.Column(db.String(50), unique=False, nullable=True)
        secrets_id = db.relationship('Secrets', backref='letters', lazy='dynamic')
       
        def __repr__(self):
            return f"3 secrets words : {self.secret_1} {self.secret_2} {self.secret_3}"

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(50), unique=False, nullable=True)
    guess = db.Column(db.String(150), unique=False, nullable=True)
    # Many answers and many scores for one user
    user_scores = db.relationship('Scores', backref='users', lazy='dynamic', cascade = "all, delete, delete-orphan")
    user_answers = db.relationship('Guess', backref='users', lazy='dynamic', cascade = "all, delete, delete-orphan")

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
       self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"username : {self.username}"

class Secrets(db.Model):
        # Id : Field which stores unique id for every row in
        # database table
        id = db.Column(db.Integer, primary_key=True)
        secret_1 = db.Column(db.String(100), unique=False, nullable=False)
        secret_2 = db.Column(db.String(100), unique=False, nullable=False)
        secret_3 = db.Column(db.String(100), unique=False, nullable=False)
        secret_4 = db.Column(db.String(100), unique=False, nullable=True)
        secret_5 = db.Column(db.String(100), unique=False, nullable=True)
        theme = db.Column(db.String(100), unique=False, nullable=True)
        # foreign key referring to the PK of a series of letters from the 3 words above
        letters_id = db.Column(db.Integer, db.ForeignKey('letters.id'))
        
        def __repr__(self):
            return f"Secrets : {self.secret_1} {self.secret_2} {self.secret_3} {self.secret_4} {self.secret_5} {self.theme}"

class Guess(db.Model):
    # Id : Field which stores unique id for every row in
    # database table
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(150), unique=False, nullable=False)
    round = db.Column(db.Integer, unique=False, nullable=True)
    # foreign key referring to the PK of Users (Many answers by user)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Answer : {self.word}"

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, unique=False, nullable=True)
    score_object = db.Column(db.String(150), unique=False, nullable=True)
    # foreign key referring to the PK of Users (Many scores by user) - FK is on the many side
    scores_id = db.Column(db.String, db.ForeignKey("users.id"))
