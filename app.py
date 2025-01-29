from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from hashlib import sha256
import markdown

app = Flask(__name__)

# Configuring SQLAlchemy with SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Code model
class Code(db.Model):
    id = db.Column(db.String(8), primary_key=True)  # Short ID
    code_content = db.Column(db.Text, nullable=False)  # The code or markdown content

    def __repr__(self):
        return f'<Code {self.id}>'

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Save code to the database and redirect to show page
@app.route('/save', methods=['POST'])
def save_code():
    code = request.form['code']
    code_id = sha256(str(uuid.uuid4()).encode()).hexdigest()[:5]  # Short ID

    # Create a new Code object and save it to the database
    new_code = Code(id=code_id, code_content=code)
    db.session.add(new_code)
    db.session.commit()

    return redirect(url_for('show_code', code_id=code_id))

# Show the code with its ID
@app.route('/<code_id>')
def show_code(code_id):
    code_entry = Code.query.get_or_404(code_id)
    
    # Convert Markdown to HTML
    html_code = markdown.markdown(code_entry.code_content)

    return render_template('show_code.html', code=html_code, code_id=code_id)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8002)
