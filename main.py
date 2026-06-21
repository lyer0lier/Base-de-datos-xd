# Importación
from flask import Flask, render_template, request, redirect, session
# Conexión de la biblioteca de bases de datos
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
# Establecer la clave secreta para la sesión.
app.secret_key = 'my_top_secret_123'
# Estableciendo conexión SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creando la DB
db = SQLAlchemy(app)
# Creando la tabla

class Card(db.Model):
    # Estableciendo los campos de enrada
    # id
    id = db.Column(db.Integer, primary_key=True)
    # título
    title = db.Column(db.String(100), nullable=False)
    # Descripción
    subtitle = db.Column(db.String(300), nullable=False)
    # Texto
    text = db.Column(db.Text, nullable=False)
    # El correo electrónico del propietario de la tarjeta.
    user_email = db.Column(db.String(100), nullable=False)

    # Objeto de salida y su ID
    def __repr__(self):
        return f'<Card {self.id}>'
    

# Tarea #1. Crear la tabla de usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, unique = False)




# Lanzamiento de la página de contenido
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
            
        # Tarea #4. Implementar la verificación de usuario
        user_db = User.query.all()
        for user in user_db:
            if user.email == form_login and check_password_hash(user.password, form_password):
                session['user_email'] = user.email
                return redirect('/index')
        error = 'Invalid email or password'
        return render_template('login.html', error=error)
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Tarea #3. Implementar grabación de usuarios
        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()



        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


# Iniciar página de contenido
@app.route('/index')
def index():
    # Tarea # 4. Asegúrese de que el usuario solo vea sus propias tarjetas
    email = session.get('user_email')
    cards = Card.query.filter_by(user_email=email).all()
    return render_template('index.html', cards=cards)

# Lanzando la página de la tarjeta
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Iniciando la página de creación de tarjetas
@app.route('/create')
def create():
    return render_template('create_card.html')

# la forma de la tarjeta
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Tarea # 4. Hacer que la creación de la tarjeta se realice en nombre del usuario
        email = session['user_email']
        card = Card(title=title, subtitle=subtitle, text=text, user_email=email)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')
@app.route('/delete/<int:id>')
def delete(id):
    card = Card.query.get_or_404(id)
    
    db.session.delete(card)
    db.session.commit()
    
    return redirect('/index')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


print("Hola mundo")
if __name__ == "__main__":
    app.run(debug=True)
