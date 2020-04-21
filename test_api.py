from requests import get

print(get('http://127.0.0.1:8900/api/articles').json(), '\n')
print(get('http://127.0.0.1:8900/api/articles/2').json(), '\n')
print(get('http://127.0.0.1:8900/api/users').json(), '\n')
print(get('http://127.0.0.1:8900/api/users/1').json(), '\n')
