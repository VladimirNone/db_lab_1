from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost/BankDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)


from werkzeug.debug import DebuggedApplication
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

class Borrower(db.Model):
    __tablename__ = 'Borrowers'
    borrower_id = db.Column(db.Integer, primary_key=True)
    tax_id = db.Column(db.String(15))
    entity_type = db.Column(db.Boolean)
    address = db.Column(db.String(255))
    amount = db.Column(db.Numeric(15, 2))
    conditions = db.Column(db.Text)
    legal_notes = db.Column(db.Text)
    contract_list = db.Column(db.Text)

class Individual(db.Model):
    __tablename__ = 'Individuals'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    passport = db.Column(db.String(20))
    tax_id = db.Column(db.String(15))
    insurance_id = db.Column(db.String(15))
    driver_license = db.Column(db.String(20))
    additional_docs = db.Column(db.Text)
    note = db.Column(db.Text)
    borrower_id = db.Column(db.Integer, db.ForeignKey('Borrowers.borrower_id'))

class Loan(db.Model):
    __tablename__ = 'Loans'
    id = db.Column(db.Integer, primary_key=True)
    individual_id = db.Column(db.Integer, db.ForeignKey('Individuals.id'))
    amount = db.Column(db.Numeric(15, 2))
    interest_rate = db.Column(db.Numeric(5, 2))
    rate = db.Column(db.Numeric(5, 2))
    term = db.Column(db.Integer)
    conditions = db.Column(db.Text)
    note = db.Column(db.Text)
    borrower_id = db.Column(db.Integer, db.ForeignKey('Borrowers.borrower_id'))

class BusinessLoan(db.Model):
    __tablename__ = 'BusinessLoans'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer)
    individual_id = db.Column(db.Integer, db.ForeignKey('Individuals.id'))
    amount = db.Column(db.Numeric(15, 2))
    term = db.Column(db.Integer)
    interest_rate = db.Column(db.Numeric(5, 2))
    conditions = db.Column(db.Text)
    note = db.Column(db.Text)
    borrower_id = db.Column(db.Integer, db.ForeignKey('Borrowers.borrower_id'))

with app.app_context(): 
    db.create_all() 


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/borrowers')
def show_borrowers():
    borrowers = Borrower.query.all()
    return render_template('borrowers.html', borrowers=borrowers)

@app.route('/individuals')
def show_individuals():
    individuals = Individual.query.all()
    return render_template('individuals.html', individuals=individuals)

@app.route('/loans')
def show_loans():
    loans = Loan.query.all()
    return render_template('loans.html', loans=loans)

@app.route('/business_loans')
def show_business_loans():
    business_loans = BusinessLoan.query.all()
    return render_template('business_loans.html', business_loans=business_loans)

# Edit, Delete and Add routes

@app.route('/edit/<model>/<int:id>', methods=['GET', 'POST'])
def edit(model, id):
    if model == 'borrower':
        item = Borrower.query.get_or_404(id)
    elif model == 'individual':
        item = Individual.query.get_or_404(id)
    elif model == 'loan':
        item = Loan.query.get_or_404(id)
    elif model == 'business_loan':
        item = BusinessLoan.query.get_or_404(id)
    else:
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            for key, value in request.form.items():
                if key == 'entity_type':
                    setattr(item, key, (value == '1' or value.lower() == 'true'))
                else:
                    setattr(item, key, value)
            db.session.commit()
            return redirect(url_for(f'show_{model}s'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating {model}: {str(e)}', 'error')
            return redirect(url_for('edit', model=model, id=id))

    return render_template('edit.html', item=item, model=model, getattr=getattr)

@app.route('/delete/<model>/<int:id>')
def delete(model, id):
    if model == 'borrower':
        item = Borrower.query.get_or_404(id)
    elif model == 'individual':
        item = Individual.query.get_or_404(id)
    elif model == 'loan':
        item = Loan.query.get_or_404(id)
    elif model == 'business_loan':
        item = BusinessLoan.query.get_or_404(id)
    else:
        return redirect(url_for('index'))

    try:
        db.session.delete(item)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(f'Cannot delete {model} with id {id} as it is referenced by another record.', 'error')    

    return redirect(url_for(f'show_{model}s'))

@app.route('/add/<model>', methods=['GET', 'POST'])
def add(model):
    if request.method == 'POST':
        if model == 'borrower':
            item = Borrower()
        elif model == 'individual':
            item = Individual()
        elif model == 'loan':
            item = Loan()
        elif model == 'business_loan':
            item = BusinessLoan()
        else:
            return redirect(url_for('index'))

        for key, value in request.form.items():
            if key == 'entity_type':
                setattr(item, key, (value == '1' or value.lower() == 'true'))
            else:
                setattr(item, key, value)

        try:
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding {model}: {str(e)}', 'error')
            return redirect(url_for('add', model=model))
        return redirect(url_for(f'show_{model}s'))

    if model == 'borrower':
        item = Borrower()
    elif model == 'individual':
        item = Individual()
    elif model == 'loan':
        item = Loan()
    elif model == 'business_loan':
        item = BusinessLoan()
    else:
        return redirect(url_for('index'))

    return render_template('add.html', item=item, model=model)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
