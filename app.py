from flask import Flask, render_template
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

class ShopItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    #time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Shopping List item #' + str(self.id)

shoplist = [
    {
        'name':'jam'
    },
    {
        'name':'jelly'
    },
    {
        'name':'ketchup'
    },
    {
        'name':'bread'
    },
]

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if request.method=='POST':
        item_name = request.form['name']
        new_item = ShopItem(name=item_name)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/shop')
    else:
        shoplist = ShopItem.query.all()
        return render_template('shop.html', shopl=shoplist)


@app.route('/shop/delete/<int:id>')
def delete_shopitem(id):
    db.session.delete(ShopItem.query.get_or_404(id))
    db.session.commit()
    return redirect('/shop')


if __name__=='__main__':
    app.run(debug=True)

