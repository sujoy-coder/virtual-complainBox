from settings import app


# For deployment in Cloud
import os
port = int(os.getenv('VCAP_APP_PORT', '5000'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port)
    # app.run(debug=True)
