from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planets = db.relationship('FavoritePlanets', backref='user', lazy=True, cascade="all, delete-orphan")
    favorite_characters = db.relationship('FavoriteCharacters', backref='user', lazy=True, cascade="all, delete-orphan")
              # clase a la que haces referencia , 
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }




class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    size = db.Column(db.Integer, unique=False, nullable=False)
    favorite_planets = db.relationship('FavoritePlanets', backref='planets', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String, unique=False, nullable=False)
    favorite_characters = db.relationship('FavoriteCharacters', backref='characters', lazy=True, cascade="all, delete-orphan")


    def __repr__(self):
        return '<Characters %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class FavoritePlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def __repr__(self):
        return '<FavoritePlanets %r>' % self.planet_id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.user_id,
            # do not serialize the password, its a security breach
        }
    
class FavoriteCharacters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    # aquí las funciones para representarlo y serializarlo
    def __repr__(self):
        return '<FavoriteCharacters %r>' % self.character_id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.user_id,
            # do not serialize the password, its a security breach
        }
    


    # modelo de tablas con tablas relacionales

# meal_ingredient = db.Table("meal_ingredient",
#                            db.Column("ingredient_id", db.Integer, db.ForeignKey(
#                                "ingredients.id"), primary_key=True),
#                            db.Column("meal_id", db.Integer, db.ForeignKey(
#                                "meals.id"),  primary_key=True),
#                            )


# class Meals(db.Model):
#     __tablename__ = "meals"
#     id = db.Column(db.Integer, primary_key=True)
#     meal = db.Column(db.String(100), nullable=False)
#     ingredients = db.relationship("Ingredients", secondary=meal_ingredient,
#                                   lazy="subquery", backref=db.backref("meal_ingredients"))
#     price = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f"{self.meal}"

#     def serialize(self):
#         return {
#             "id": self.id,
#             "meal": self.meal,
#             "ingredients": self.ingredients,
#             "price": self.price
#         }


# class Ingredients(db.Model):
#     __tablename__ = "ingredients"
#     id = db.Column(db.Integer, primary_key=True)
#     ingredient = db.Column(db.String(100), nullable=False)
#     cuantity = db.Column(db.Integer, nullable=False)
#     availeable = db.Column(db.Boolean, default=True, nullable=False)

#     def __repr__(self):
#         return f"{self.ingredient}"

#     def serialize(self):
#         return {
#             "id": self.id,
#             "ingredient": self.ingredient,
#             "cuantity": self.cuantity,
#             "availeable": self.availeable
#         }