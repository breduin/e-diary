"""Внесение правок в базу данных электронного дневника."""
import os
import random
import django
import argparse


def _get_schoolkid(name: str):
    """Получить объект ученика по имени."""
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=name)
    except Schoolkid.MultipleObjectsReturned:
        print('С таким именем есть несколько учеников. Уточни имя.')
        return None
    except Schoolkid.DoesNotExist:
        print('С таким именем учеников нет. Уточни имя.')
        return None
    return schoolkid


def fix_marks(schoolkid):
    """Исправить оценки 2 и 3 на 5 для schoolkid с ID=kid_id."""
    bad_marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3],
        )

    marks_to_update = []
    for mark in bad_marks:
        mark.points = 5
        marks_to_update.append(mark)

    Mark.objects.bulk_update(marks_to_update, ['points'])
    return True


def remove_chastisements(schoolkid):
    """Удалить замечания для schoolkid."""
    Chastisement.objects.filter(schoolkid=schoolkid).delete()
    return True


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


def _get_subject(subject_title: str,
                 year_of_study: int
                 ):
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
        return None
    return subject


def create_commendation(
        schoolkid,
        subject,
        lesson: str,
        text=None,
        ):
    """Создать похвалу для ученика по предмету.

    Параметры:
    kid_id -- ID ученика;
    subject_title -- название предмета;
    lesson -- random/last - для записи похвалы выбирается
    случайный/последний урок.
    text -- текст похвалы. Если не задан, то выбирается случайно;
    """

    year_of_study = schoolkid.year_of_study

    order_lessons_by = 'date' if lesson == 'last' else '?'
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
    return True


def dance_everybody():
    kids = Schoolkid.objects.all()
    for kid in kids:
        fix_marks(kid)
    return True


if __name__ == '__main__':

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

    django.setup()

    from datacenter.models import Schoolkid, Mark, Chastisement
    from datacenter.models import Subject, Lesson, Commendation

    commands = {
        'make_good_points': {
            'function': fix_marks,
            'args': ['name', ],
            },
        'create_commendation': {
            'function': create_commendation,
            'args': ['name', 'subject', 'lesson'],
            },
        'remove_chastisements': {
            'function': remove_chastisements,
            'args': ['name', ],
            },
        'dance_everybody!': {
            'function': dance_everybody,
            'args': [],
            },
        }

    subjects = list(
        Subject.objects.all().distinct().values_list('title', flat=True)
        )

    parser = argparse.ArgumentParser(description='Исправь дневник!')
    parser.add_argument('command',
                        choices=commands.keys(),
                        help='укажи команду скрипта',
                        )
    parser.add_argument('--name',
                        help='укажи имя в кавычках',
                        )
    parser.add_argument('--subject',
                        help='укажи школьный предмет в кавычках',
                        choices=subjects,
                        )
    parser.add_argument('--lesson',
                        help='укажи, к какому уроку привязать похвалу',
                        choices=['last', 'random'],
                        )
    parser.add_argument('--text',
                        help='напиши текст похвалы в кавычках',
                        )
    args = parser.parse_args()

    command = args.command

    func = commands[command]['function']
    required_args = commands[command]['args']
    check_required_args_in_request = [
        bool(vars(args)[arg]) for arg in required_args
        ]

    if not all(check_required_args_in_request):
        print('''Не все аргументы указаны.проверь запрос
        и запусти скрипт ещё раз.''')
        exit()
    kwargs = {arg: vars(args)[arg] for arg in required_args}

    if 'name' in required_args:
        schoolkid = _get_schoolkid(args.name)
        if not schoolkid:
            exit()
        del kwargs['name']
        kwargs['schoolkid'] = schoolkid

    if 'subject' in required_args:
        school_subject = _get_subject(args.subject, schoolkid.year_of_study)
        if not school_subject:
            exit()
        kwargs['subject'] = school_subject

    if command == 'create_commendation' and args.text:
        kwargs['text'] = args.text

    result = func(**kwargs)
    if result:
        print('Ок, сделано.')
