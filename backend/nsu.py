from app import create_app, db
from app.models.user import User

app = create_app()

# with app.app_context():
#     kek()

app.app_context().push()


# добавляем инстансы для cmd
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User}


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=False)
