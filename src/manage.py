#!/usr/bin/env python
from app import create_app

app = create_app()
#app.config.from_object(os.environ['APP_SETTINGS'])
#manager = Manager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
