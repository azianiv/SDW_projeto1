import pandas as pd
import requests
import json
import openai


sdw='https://sdw-2023-prd.up.railway.app'

def get_user(id):
    response = requests.get(f'{sdw}/users/{id}')
    return response.json() if response.status_code == 200 else "Náo encontrado"


db = pd.read_csv('UserData.csv')
userid = db['UserID'].tolist()

user = [user for id in userid if (user := get_user(id)) is not None]
print(json.dumps(user, indent=2))

## Transformação
my_key='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'
openai.api_key = my_key

def msg_gen(usuario):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {
                "role": "system",
                "content": "Você é um especialista em marketing bancário."
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem customizada contendo o nome {usuario['name']} sobre a importância dos investimentos. (máximo de 100 caracteres)"
            }
    ]
    )
    return completion.choices[0].message.content.strip('\"')


for usuario in user:
    news = msg_gen(usuario)
    print(news)
    usuario ['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
})
    
## Atualização de usuario
def user_update(user):
    response = requests.put(f"{sdw}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for usuario in user:
    success = user_update(usuario)
    print(f"User {usuario['name']} updated? {success}")
