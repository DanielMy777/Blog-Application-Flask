from src.CreateApp import create_application
from src.config import DevelopmentConfig

app, _ = create_application(DevelopmentConfig)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
