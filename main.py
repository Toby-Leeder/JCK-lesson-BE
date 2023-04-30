# if these are not showing up, do pip install (the specific library that is missing)
# ex: if flask_cors is not showing, do "pip install flask_cors" and "pip install cors"

from hacks_api import app, db

from hacks_api.api.api import player_bp # bp for table
from hacks_api.model.model import initPlayers, initImages # initializing function
from hacks_api.api.imageapi import image_bp # bp for image


app.register_blueprint(player_bp)
app.register_blueprint(image_bp)


@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        initPlayers()
        initImages()
        # put your initializing function here


if __name__ == "__main__":
    from flask_cors import CORS
    cors = CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8199")
