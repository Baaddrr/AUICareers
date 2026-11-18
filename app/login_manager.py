from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # <--- Add this line

@login_manager.user_loader
def load_user(user_id):
    from .models import User  # moved here to avoid circular import
    return User.query.get(int(user_id))
