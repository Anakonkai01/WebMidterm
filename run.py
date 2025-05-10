import os
from app import create_app, db
from app.models import Product # Quan trọng cho shell context

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Product': Product}

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == 'True')