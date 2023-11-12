import requests
import json

cookies = {
    'ig_did': '98718CD7-F349-49AD-AD2D-E6620CF26218',
    'ig_nrcb': '1',
    'mid': 'ZRe7_QALAAHzzPhHod1N_ij4Zflw',
    'datr': '_LsXZUhGA7-H2yKmZN2JPttI',
    'ds_user_id': '62355556219',
    'csrftoken': 'LWDZpDsSrciQbYYc39BcqZqUCYr8fE0v',
    'shbid': '"14877\\05462355556219\\0541731321280:01f75d55373bf3e9152bc7c5a158f37b08adf967efcfcf56c6b062ca75c31ba51435a7c2"',
    'shbts': '"1699785280\\05462355556219\\0541731321280:01f725d812b55b2ca84d59834bc495c0eed99d7521264edbc2396745cd1143e90c15ca47"',
    'sessionid': '62355556219%3ABIuhRdImAqy1KH%3A8%3AAYfLYdS-9JSzWPcJ9_bh-Ww4Pa048cAJxRF9Cvhabg',
    'rur': '"RVA\\05462355556219\\0541731329065:01f71d0f9053dc31cadd1d151a6443b3518cfcf361c6e4c26a13f9a3e143da0b5b480f6f"',
}

headers = {
    'authority': 'www.instagram.com',
    'accept': '*/*',
    'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': 'ig_did=98718CD7-F349-49AD-AD2D-E6620CF26218; ig_nrcb=1; mid=ZRe7_QALAAHzzPhHod1N_ij4Zflw; datr=_LsXZUhGA7-H2yKmZN2JPttI; ds_user_id=62355556219; csrftoken=LWDZpDsSrciQbYYc39BcqZqUCYr8fE0v; shbid="14877\\05462355556219\\0541731321280:01f75d55373bf3e9152bc7c5a158f37b08adf967efcfcf56c6b062ca75c31ba51435a7c2"; shbts="1699785280\\05462355556219\\0541731321280:01f725d812b55b2ca84d59834bc495c0eed99d7521264edbc2396745cd1143e90c15ca47"; sessionid=62355556219%3ABIuhRdImAqy1KH%3A8%3AAYfLYdS-9JSzWPcJ9_bh-Ww4Pa048cAJxRF9Cvhabg; rur="RVA\\05462355556219\\0541731329065:01f71d0f9053dc31cadd1d151a6443b3518cfcf361c6e4c26a13f9a3e143da0b5b480f6f"',
    'dpr': '1',
    'referer': 'https://www.instagram.com/day_time_events/',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="119.0.6045.106", "Chromium";v="119.0.6045.106", "Not?A_Brand";v="24.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'viewport-width': '836',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'query_hash': '37479f2b8209594dde7facb0d904896a',
    'variables': '{"id":"48825885937","first":48}'
}

def fetch_data(params, cookies, headers):
    response = requests.get('https://www.instagram.com/graphql/query/', params=params, cookies=cookies, headers=headers)
    return response.json()

def extract_usernames(data):
    usernames = []
    users = data.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('edges', [])
    for user in users:
        username = user.get('node', {}).get('username')
        if username:
            usernames.append(username)
    return usernames

usernames = []
source_name = headers['referer'].split('/')[-2]

while True:
    response = fetch_data(params, cookies, headers)
    new_usernames = extract_usernames(response)
    usernames.extend(new_usernames)

    print(f"Собрано {len(new_usernames)} имен пользователей, всего собрано {len(usernames)}")

    page_info = response['data']['user']['edge_followed_by']['page_info']
    if not page_info['has_next_page']:
        print("Сбор данных завершен.")
        break

    next_page_token = page_info['end_cursor']
    params['variables'] = json.dumps({
        "id": "48825885937",
        "first": 48,
        "after": next_page_token
    })

# Сохранение результатов в файл
with open(f'usernames_{source_name}.txt', 'w') as file:
    for username in usernames:
        file.write(f"{username}\n")