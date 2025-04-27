from config import Config
from app import create_app, db
from app.models import User, Note

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Note": Note}

if __name__ == "__main__":
    app.run(debug=True)
