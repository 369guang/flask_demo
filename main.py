from flasks.ctl import create_app
from flasks.extensions import db

if __name__ == "__main__":
    app = create_app()
    db.init_app(app)
    app.run()
