from aip import AipSpeech
APP_ID = '23474300'
API_KEY = 'sluLEi1xoOTdgC7hU570Pebl'
SECRET_KEY = 'YmQxWR9Cn5rex5LQbrwl8DGr3BbkMYTg'


def tts():  # return the number of sentences.
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    content = []
    with open('./test.txt', 'r', encoding='UTF-8') as f:
        line = f.read().strip()
        content = line.split('\n')
        print(content)

    l = len(content)
    for i in range(l):
        result = client.synthesis(content[i], 'zh', 1, {'spd': 4, 'per': 4})
        filename = './test' + str(i+1) + '.wav'
        if not isinstance(result, dict):
            with open(filename, 'wb') as f:
                f.write(result)
                print(i+1, 'finished')
    return l


if __name__ == '__main__':
    tts()
