from chalice import Chalice
from model import db, save_db

app = Chalice(app_name='helloworld')


class CurrentUser:
    def __init__(self):
        self.state = {'username': ''} #Initial state
    
    def updateUser(self, name):
        self.state['username'] = name
        print(f"name updated to {self.state['username']}")
        
    def get_state(self):
        return self.state
        
# create current user object
Name = CurrentUser()

# api to retrieve current user
@app.route('/current_user', methods=['GET'], cors=True)
def current_user():
    request = app.current_request

    # get current user name
    user = Name.get_state()
    return {'username': user}

# api to authenticate login details
@app.route('/authenticate', methods=['GET', 'POST'], cors=True)
def authenticate():
    request = app.current_request
    
    data = db

    if request.method == 'POST':
        # Extract username and password from JSON body
        request_body = request.json_body
        username = request_body.get('username')
        password = request_body.get('password')

        # Authentication logic
        user = next((u for u in data if u['username'] == username and u['password'] == password), None)

        
        if user:
            Name.updateUser(username)
            return {'success': True, 'current_user': username}
        else:
            return {'success': False}, 401
    
    
@app.route('/create_user', methods=['GET', 'POST'], cors=True)
def create_user():
    request = app.current_request
    
    data = db
    
    # Extract username and password from JSON body
    request_body = request.json_body
    username = request_body.get('username')
    password = request_body.get('password')
    
    #Authentication logic
    if any(u['username'] == username for u in data):
        return {'success': False, 'message': 'User already exists'}, 400
    
    data.append({'username': username, 'password': password})
    
    save_db(data)
    
    return {'success': True}

@app.route('/delete_user', methods=['GET', 'POST', 'PUT'], cors=True)
def delete_user():
    request = app.current_request
    
    data = db 
       
    # Extract username
    request_body = request.json_body
    username = request_body.get('username')
    
    #check for username in database and retrieve index
    # Find the index of the entry to delete
    # for i, entry in enumerate(data):
    #     if entry['username'] == username:
    #         del data[i]
    #         break
    #     else:
    #         return {'success': False}
    if request.method == 'PUT':
        data = [entry for entry in data if entry["username"] != username]
        if data != db:
            save_db(data)
            return {'success': True}
        else:
            return {'success': False}
 
    

# @app.route('/update_user/{id}', methods=['PUT'], cors=True)
# def update_user(id):
    

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
