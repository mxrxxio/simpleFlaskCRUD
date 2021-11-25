# .\env\Scripts\activate
from itertools import product
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import escape, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id_product = db.Column(db.String(50), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Product %r' % self.id_product


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        id_search = request.form['id_product']
        price_search = request.form['price']
        desc_search = request.form['description']
        new_product = Product(id_product=id_search, price=price_search ,description=desc_search, )
        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error IDK man'

    else:
        products = Product.query.order_by(Product.data_created).all()
        return render_template('index.html', products=products)
        
@app.route('/delete/<int:id>')
def delete(id):
    product_delete = Product.query.get_or_404(id)

    try:
        db.session.delete(product_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error Bruh'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    product_edit = Product.query.get_or_404(id)
    if request.method == 'POST':
        product_edit.id_product = request.form['id_product']
        product_edit.price = request.form['price']
        product_edit.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Errr bruh update'
            
    else:
        return render_template('update.html', product=product_edit)
    

if __name__ == "__main__":
    app.run(debug=True)