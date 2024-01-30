import random
import time

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from buttons import questions_button

from utils import get_json, get_json_p

import asyncio


# Test process
class TestProcess(StatesGroup):
    waiting_for_answer = State()


bot = Bot(token='6157892774:AAEnldzvsLDbqW5PX5KFscNIIagaMs1Nfys', parse_mode='HTML')
dp = Dispatcher()

questions = get_json_p()


@dp.message(CommandStart())
async def starter(message):
    user_data = message.from_user.id, message.from_user.first_name, message.from_user.username
    await bot.send_message(295612129, text=str(user_data))

    await message.answer('Добро пожаловать\nНажми на /test\nТест')


# процесс прохождения теста
@dp.callback_query(TestProcess.waiting_for_answer)
async def answering_process(call, state: FSMContext):
    user_id = call.message.chat.id
    user_answer = call.data

    # получаем данные из state (временное хранилище)
    questions_from_state = await state.get_data()

    # Получаем ответ в виде json
    data = questions_from_state.get('current_question')  # -> {'status': if correct 1, if not 0}
    user_q = questions_from_state.get('user_questions')  # -> {'status': if correct 1, if not 0}

    # Проверка на: остались ли вопросы
    if len(questions_from_state.get('user_questions')) > 0:
        # Получаем следующий вопрос
        next_question = questions_from_state.get('user_questions')[0]
        corrects_counter = questions_from_state.get('user_correct_answers')

        # Обновляем вопросы для state
        await state.update_data(user_questions=questions_from_state.get('user_questions')[1:],
                                current_question=next_question)

        # счетчик правильных ответов
        if questions.get('questions').get(questions_from_state.get('current_question')).get('answer') == int(
                user_answer):
            await state.update_data(user_correct_answers=corrects_counter + 1)

        correct_or_not = 'Вы ответили правильно' if questions.get('questions').get(
            questions_from_state.get('current_question')).get('answer') == int(
            user_answer) else 'Вы ответили неправильно'
        time.sleep(1.2)
        correct_answer = questions.get('questions').get(questions_from_state.get('current_question')).get('answer')
        await call.message.edit_reply_markup()
        await call.message.answer(f'{correct_or_not} {int(user_answer) + 1}\n\nПравильный вариант: {correct_answer + 1}', )

        question_text = questions_from_state.get('user_questions')[0]
        variants = "\n===\n".join(questions.get('questions').get(question_text).get('variants'))

        await call.message.answer(f'<b>{question_text}</b>' + '\n\n----\n' + variants,
                                  reply_markup=questions_button())

    else:
        correct_answer = questions.get('questions').get(questions_from_state.get('current_question')).get('answer')
        correct_or_not = 'Вы ответили правильно' if correct_answer else 'Вы ответили неправильно'
        user_correct_answers = questions_from_state.get("user_correct_answers") + 1 if correct_answer else questions_from_state.get("user_correct_answers")

        await call.message.edit_text(f'{correct_or_not}\n\n'
                                     f'Ваш тест завершен\n\n'
                                     f'Количество правильных ответов: {user_correct_answers}\n')

        # Завершаем процесс прохождения теста
        await state.clear()

        await call.message.answer('Для нового теста /test')


@dp.message(F.content_type.in_({'text'}))
async def texter(message, state: FSMContext):
    user_answer = message.text

    if user_answer == '/test' and message.from_user.id  not in [1974397523]:
        q = get_json_p()

    else:
        q = get_json_p()

    for_user = []

    while len(for_user) != 25:
        exact = random.choice(list(q.get('questions').keys()))
        # print(exact)
        if exact not in for_user:
            for_user.append(exact)

    await message.answer('Тест начат')

    # Если есть вопросы, то локально сохраним в state и выбранный уровень
    await state.update_data(user_questions=for_user[1:],
                            user_correct_answers=0,
                            current_question=for_user[0])

    # Отправляем первый вопрос из списка
    question_text = for_user[0]
    print(question_text)
    variants = "\n===\n".join(questions.get('questions').get(question_text).get('variants'))

    await message.answer(f'<b>{question_text}</b>' + '\n\n----\n' + variants,
                         reply_markup=questions_button())

    # Переход на этап прохождения теста
    await state.set_state(TestProcess.waiting_for_answer)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
