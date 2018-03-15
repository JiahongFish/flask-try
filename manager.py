
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from first_project import app
from extension import db
from models import User

manager = Manager(app)

# Hook up app and db
migrate = Migrate(app, db)

# Add script to manager
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
