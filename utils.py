import json

from random import shuffle


def read_file():
    with open('finance.txt', 'r') as file:
        reader = file.read()

    return str(reader)


def clean_data(data):
    data = data.replace('#', '').replace('\n', '')
    q_list = data.split('++++')

    q_dict = {'questions': {}}

    for question in q_list[:-1]:
        try:
            tem_format = question.split('====')
            print(tem_format)
            main_text = tem_format[0]
            v1 = tem_format[1]
            v2 = tem_format[2]
            v3 = tem_format[3]
            v4 = tem_format[4]
            answer = tem_format[1]
            variants = [v1, v2, v3, v4]
            shuffle(variants)

            q_dict.get('questions').update({main_text: {'variants': variants,
                                                        'answer': variants.index(answer)}})
        except:
            continue
    return q_dict


def make_json(clean_data):
    with open('finance.json', 'w') as file:
        data = json.dumps(clean_data)
        file.write(data)

    return True


def get_json():
    with open('finance.json', 'rb') as file:
        data = json.loads(file.read())

    return data

# read = read_file()
# clean = clean_data(read)
# jsoner = make_json(clean)
