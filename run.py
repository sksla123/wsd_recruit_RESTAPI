from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=app.config['FLASK_BASE_URL'], port=app.config['FLASK_PORT'], debug=app.config['FLASK_DEBUG_MODE'])