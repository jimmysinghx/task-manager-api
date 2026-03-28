from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

from app import create_app

app=create_app()
CORS(app)






if __name__ == "__main__":
    app.run(debug=True)
