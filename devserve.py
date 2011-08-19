import os
os.environ['VOTOGRAMA_SETTINGS'] = 'settings_development.py'

from votograma import app
app.run(debug=True, host='0.0.0.0', port=5000)
