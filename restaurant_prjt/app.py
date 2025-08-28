import psycopg2
from flask import Flask, render_template, request, redirect, url_for

# Initialisation de l'application Flask
app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        dbname="restau_db",
        user="postgres",
        password="1234",
        host="localhost"
    )
    return conn
@app.route('/')
@app.route('/menu')
def menu():
  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, price FROM Menu_Items ORDER BY name;')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('menu.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """Ajoute un nouvel item au menu."""
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Menu_Items (name, price) VALUES (%s, %s);', (name, price))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('menu'))
    return render_template('add_item.html')

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    """Met à jour un item existant."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        cursor.execute('UPDATE Menu_Items SET name = %s, price = %s WHERE id = %s;', (name, price, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('menu'))
    
    cursor.execute('SELECT id, name, price FROM Menu_Items WHERE id = %s;', (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()

    if item is None:
        return "Item not found", 404
    return render_template('update_item.html', item=item)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    """Supprime un item du menu."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Menu_Items WHERE id = %s;', (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('menu'))

if __name__ == '__main__':
    app.run(debug=True)