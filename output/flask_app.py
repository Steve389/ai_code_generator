```python
from flask import Flask, request

app = Flask(\_\_name__)

@app.route('/', methods=['POST'])
def handle\_post():
    data = request.get\_json()
    # Process the received JSON data here
    return 'OK'

if \_\_name__ == '\_\_main__':
    app.run(debug=True)
```