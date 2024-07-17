from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        resp = make_response(redirect(url_for('welcome')))
        resp.set_cookie('name', name)
        resp.set_cookie('email', email)
        return resp
    return render_template('form.html')

@app.route('/welcome')
def welcome():
    name = request.cookies.get('name')
    if not name:
        return redirect(url_for('form'))
    return render_template('welcome.html', name=name)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('form')))
    resp.set_cookie('name', '', expires=0)
    resp.set_cookie('email', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(debug=True)