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


commands_functions = {
    'make_good_points': fix_marks,
    'create_commendation': create_commendation,
    'remove_chastisements': remove_chastisements,
    'dance_everybody!': dance_everybody
}


if __name__ == '__main__':

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

    django.setup()

    from datacenter.models import Schoolkid, Mark, Chastisement
    from datacenter.models import Subject, Lesson, Commendation

    try:
        func = commands_functions[sys.argv[1]]
    except KeyError:
        print('Такой команды нет. Вот список доступных команд:')
        for command in commands_functions.keys():
            print(command)
        exit()
    max_number_of_arguments = 4
    args = sys.argv[2:]
    args.extend(
        [None] * (
            max_number_of_arguments - len(sys.argv[2:])
            )
        )
    func(*args)
