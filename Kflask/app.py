from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
 
db = SQLAlchemy(app) 


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    expenses = Expense.query.all() 
    return render_template('index.html', expenses=expenses)  


@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form.get('category')  
    amount = request.form.get('amount')  
    
    if category and amount:
        
        new_expense = Expense(category=category, amount=float(amount))
        
       
        db.session.add(new_expense)
        db.session.commit()

    return redirect(url_for('index'))  


@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)  
    
    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for('index'))  
@app.route('/chart')
def chart():
    return render_template('chart.html')
if __name__ == '__main__':
    app.run(debug=True)
