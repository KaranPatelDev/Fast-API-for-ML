from fastapi import FastAPI, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@app.post('/token')
def login(username: str = Form(...), password: str = Form(...)):
    if username == 'john' and password == 'pass123':
        return {'access_token': 'valid_token', 'token_type': 'bearer'}
    raise HTTPException(status_code=400, detail='Invalid Credentials')


def decode_token(token: str):
    if token == 'valid_token':
        return {'name': 'john'}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid Authentication Credentials'
    )


def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_token(token)


@app.get('/profile')
def get_profile(user=Depends(get_current_user)):
    return {'username': user['name']}


# Flow of dependency injection:
# 1. Client sends a request to /profile with Authorization header containing the token.
# 2. FastAPI sees that get_profile depends on get_current_user, so it calls get_current_user.
# 3. get_current_user depends on oauth2_scheme, so FastAPI calls oauth2_scheme to extract the token from the request.
# 4. The extracted token is passed to get_current_user, which then calls decode_token to validate it.
# 5. If the token is valid, decode_token returns user info, which is then passed to get_profile.
# 6. Finally, get_profile returns the user's profile information.
# This demonstrates how FastAPI manages nested dependencies and passes values through them.


'''

username : john
password : pass123

'''