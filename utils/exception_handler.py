from rest_framework.views import exception_handler

def custom_exception_handler(exc,context):
    response = exception_handler(exc,context)

    if response is not None:
        response.data['errorCode'] = response.status_code
        print(response.data)

        if response.data.get('password',None):
            response.data['errorMessage'] = 'password: ' + response.data.get('password')[0]
            
        
        elif response.data.get('password2',None):
            response.data['errorMessage'] = 'password2: ' + response.data.get('password2')[0]


        elif response.data.get('username',None):
            response.data['errorMessage'] = 'username: ' + response.data.get('username')[0]
        
        elif response.data.get('detail',None):
            response.data['errorMessage'] = response.data.get('detail')


        response.data.pop('password',None)
        response.data.pop('password2',None)
        response.data.pop('username',None)
        response.data.pop('detail',None)
                                                        
    
    return response