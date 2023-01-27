from flask import Flask, render_template, request, session, send_file
from datetime import date
from weasyprint import HTML

app = Flask(__name__)
app.secret_key = 'your_secret_key'



@app.route('/')
def index():
    session['items'] =[]
    session['name']=""
    session['owner']=""
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    session['name'] = name
    owner =request.form['owner']
    session['owner'] = owner
    title=request.form['title']
    charges=request.form['charges']
    charges=int(charges)
    quantity=request.form['quantity']
    quantity=int(quantity)
    item={"title":title,"charges": charges,"quantity":quantity}
    session['items'].append(item)
    return render_template('index.html', items=session['items'])

@app.route('/invoice', methods=['POST'])
def invoice():
    today = date.today().strftime("%B %-d, %Y")
    invoice_number = 123
    duedate = "August 1, 2018"
    items=session.get('items', None)
    total = sum([i['charges']*i['quantity'] for i in items])
    rendered = render_template('invoice.html',
                            date = today,
                            name = session.get('name'),
                            owner = session.get('owner'),
                            items = items,
                            total = total,
                            invoice_number = invoice_number,
                            duedate = duedate)
    html = HTML(string=rendered)
    rendered_pdf = html.write_pdf('./static/invoice.pdf')
    return send_file(
            './static/invoice.pdf'
    )

    
if __name__ == '__main__':
    app.run()
