import json

from random import shuffle


def read_file():
    with open('p_ek_t.txt', 'r') as file:
        reader = file.read()

    return str(reader)


error_list = []
def clean_data(data):
    global error_list
    data = data.replace('\n', '')
    q_list = data.split('++++')

    q_dict = {'questions': {}}

    for question in q_list[:-1]:
        # try:
            tem_format = question.split('====')
            print(tem_format)
            main_text = tem_format[0]
            # v1 = tem_format[1]
            # v2 = tem_format[2]
            # v3 = tem_format[3]
            # v4 = tem_format[4]
            # answer = tem_format[1]
            v1 = tem_format[1].replace('# ', '').replace('#', '')[0:] if not tem_format[1].startswith(' ') else tem_format[1].replace('# ', '').replace('#', '')[1:]
            v2 = tem_format[2].replace('# ', '').replace('#', '')[0:] if not tem_format[2].startswith(' ') else tem_format[2].replace('# ', '').replace('#', '')[1:]
            v3 = tem_format[3].replace('# ', '').replace('#', '')[0:] if not tem_format[3].startswith(' ') else tem_format[3].replace('# ', '').replace('#', '')[1:]
            v4 = tem_format[4].replace('# ', '').replace('#', '')[0:] if not tem_format[4].startswith(' ') else tem_format[4].replace('# ', '').replace('#', '')[1:]
            for ans in tem_format:
                if ans.startswith('# '):
                    answer = ans.replace("# ", '')

                elif ans.startswith('#'):
                    answer = ans.replace("#", '')
            #
            #     print(ans)

            variants = [v1.strip(), v2.strip(), v3.strip(), v4.strip()]
            shuffle(variants)
            print(variants)
            q_dict.get('questions').update({main_text: {'variants': variants,
                                                        'answer': variants.index(answer.strip())}})
        # except IndexError:
        #     error_list.append(tem_format)
        #     print(main_text, 'error')
        #
        #
        # except Exception as e:
        #     print(main_text)
        #     error_list.append(tem_format)
        #     continue
    return q_dict


def make_json(clean_data):
    with open('p_ek_t.json', 'w') as file:
        data = json.dumps(clean_data)
        file.write(data)

    return True


def get_json():
    with open('taxation.json', 'rb') as file:
        data = json.loads(file.read())

    return data

def get_json_p():
    with open('p_ek_t.json', 'rb') as file:
        data = json.loads(file.read())

    return data

# read = read_file()
# clean = clean_data(read)

# print(len(clean.get('questions')))
# print(len(error_list), error_list.remove(['']))
# print(len(error_list), error_list)



# jsoner = make_json(clean)