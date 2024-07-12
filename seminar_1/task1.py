from flask import Flask, render_template

app = Flask(__name__)

# Пример данных для категорий и товаров
products = {
    'clothes': [
        {'name': 'jacket', 'display_name': 'Jacket', 'description': 'A warm and comfortable jacket.', 'price': '$59.99'},
        {'name': 'tshirt', 'display_name': 'T-Shirt', 'description': 'A stylish T-shirt.', 'price': '$19.99'}
    ],
    'shoes': [
        {'name': 'sneakers', 'display_name': 'Sneakers', 'description': 'Comfortable and trendy sneakers.', 'price': '$49.99'},
        {'name': 'boots', 'display_name': 'Boots', 'description': 'Durable and stylish boots.', 'price': '$79.99'}
    ]
}

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/category/<category_name>')
def category(category_name):
    category_products = products.get(category_name, [])
    return render_template('category.html', category_name=category_name, products=category_products)

@app.route('/product/<product_name>')
def product(product_name):
    for category, items in products.items():
        for item in items:
            if item['name'] == product_name:
                return render_template('product.html', product_name=item['display_name'], product_description=item['description'], product_price=item['price'])
    return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True)