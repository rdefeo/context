__author__ = 'robdefeo'
from context import app
if __name__ == "__main__":
    from context.settings import PORT
    # Run a test server.
    app.run(host='0.0.0.0', port=PORT, debug=True)