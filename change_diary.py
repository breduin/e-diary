"""Внесение правок в базу данных электронного дневника."""
import os
import sys
import random
import django


def _get_schoolkid(kid_name: str):
    """Получить объект ученика по имени."""
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=kid_name)
    except Schoolkid.MultipleObjectsReturned:
        print('С таким именем есть несколько учеников. Уточни имя.')
        return None
    except Schoolkid.DoesNotExist:
        print('С таким именем учеников нет. Уточни имя.')
        return None
    return schoolkid


def _fix_marks(kid_id: int):
    """Исправить оценки 2 и 3 на 5 для schoolkid с ID=kid_id."""
    bad_marks = Mark.objects.filter(
        schoolkid__id=kid_id,
        points__in=[2, 3],
        )

    marks_to_update = []
    for mark in bad_marks:
        mark.points = 5
        marks_to_update.append(mark)

    Mark.objects.bulk_update(marks_to_update, ['points'])


def fix_marks(kid_name: str, *args):
    """Исправить оценки 2 и 3 на 5 для schoolkid с именем kid_name."""
    schoolkid = _get_schoolkid(kid_name) or exit()
    _fix_marks(schoolkid.id)


def remove_chastisements(kid_name, *args):
    """Удалить замечания для schoolkid."""
    schoolkid = _get_schoolkid(kid_name) or exit()
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def _get_random_commendation():
    """Вернуть случайный текст похвалы."""
    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
    ]
    return random.choice(commendations)


def _get_subject(subject_title: str, year_of_study: int):
    """Получить объект предмета (школьной дисциплины)."""
    try:
        subject = Subject.objects.get(
            title=subject_title,
            year_of_study=year_of_study
            )
    except Subject.DoesNotExist:
        print(
            f"""Такого предмета в {year_of_study}-м классе нет.
                Уточни название."""
                )
        exit()
    return subject


def create_commendation(
        kid_name: str,
        subject_title: str,
        which_lesson: str,
        text: str,
        *args):
    """Создать похвалу для ученика по предмету.

    Параметры:
    kid_name -- имя ученика;
    subject_title -- название предмета;
    text -- текст похвалы. Если не задан, то выбирается случайно;
    which_lesson -- random/last - для записи похвалы выбирается
    случайный/последний урок.
    """

    schoolkid = _get_schoolkid(kid_name) or exit()

    year_of_study = schoolkid.year_of_study

    subject = _get_subject(subject_title, year_of_study)

    order_lessons_by = 'date' if which_lesson.lower() == 'last' else '?'
    lesson = Lesson.objects.filter(
        year_of_study=year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
        ).order_by(order_lessons_by).last()

    text = text or _get_random_commendation()

    Commendation.objects.create(
        created=lesson.date,
        schoolkid=schoolkid,
        teacher=lesson.teacher,
        text=text,
        subject=subject
        )
    return


def dance_everybody(*args):
    kids = Schoolkid.objects.all().values('id')
    for kid in kids:
        _fix_marks(kid['id'])


commands = {
    'make_good_points': {
        'function': fix_marks,
        'args_number': 1,
        },
    'create_commendation': {
        'function': create_commendation,
        'args_number': 3,
        },
    'remove_chastisements': {
        'function': remove_chastisements,
        'args_number': 1,
        },
    'dance_everybody!': {
        'function': dance_everybody,
        'args_number': 0,
        },
}


def _validate__func():
    """Валидировать функцию (команду)."""
    try:
        func = commands[sys.argv[1]]['function']
    except KeyError:
        print('Такой команды нет. Вот список доступных команд:')
        for command in commands.keys():
            print(command)
        return None
    except IndexError:
        print('Похоже, ты не указал ни одной команды. Смотри, есть вот такие:')
        for command in commands.keys():
            print(command)
        return None
    return func


def _validate_args():
    """Валидировать аргументы."""
    args = [arg.strip() for arg in sys.argv[2:]]
    required_number_of_arguments = commands[sys.argv[1]]['args_number']
    if len(args) < required_number_of_arguments:
        print('Маловато аргументов.')
        print(
            f'Для команды {sys.argv[1]} их {required_number_of_arguments}.'
            )
        return None

    if not all([bool(len(arg)) for arg in args]):
        print('Пустые строки в качестве аргументов не подходят. Заполни их.')
        return None
    return args


def get_validated_func_args():
    """Получить валидированную функцию и аргументы."""
    if not _validate__func():
        return None, None
    return _validate__func(), _validate_args()


if __name__ == '__main__':

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

    django.setup()

    from datacenter.models import Schoolkid, Mark, Chastisement
    from datacenter.models import Subject, Lesson, Commendation

    func, args = get_validated_func_args()

    if not all([func, args]):
        exit()

    max_number_of_arguments = 4
    args.extend(
        [None] * (
            max_number_of_arguments - len(sys.argv[2:])
            )
        )

    func(*args)
