# Меняем оценки в электронном дневнике


## Требования

Код является свободным, ты можешь установить его и пользоваться. Для этого тебе понадобятся:

1. Python 3.8+. [см. как установить (англ.)](https://realpython.com/installing-python/), а [здесь для Debian-based (рус.)](http://userone.ru/?q=node/41).


## Запуск

- Считаем, что электронный дневник ты уже установил и запустил виртуальное окружение по инструкции из репозитория электронного дневника.
- Скачай код.
- Размести файл *change_diary.py* в той же папке, что и *manage.py*.
- Запусти скрипт командой:

```
python3 change_diary.py <команда> <аргумент1> <аргумент2> <аргумент3> <аргумент4>
```
Описание команд и их аргументов см. дальше.

## Команды
Команды сообщают скрипту, что ему делать. Аргументы - с кем и как. 

Все аргументы указывай в кавычках.

### Иcправить оценки
Исправляет указанному ученику все 2-ки и 3-ки на 5-ки. По всем предметам.

 - <команда>: ```make_good_points```
 - <аргумент1>: **обязательный** ```Фамилия Имя Отчество``` (возможно, будет достаточно Фамилия Имя)
 - <аргумент2>: ```не требуется```
 - <аргумент3>: ```не требуется```
 - <аргумент4>: ```не требуется```
 
 **Пример**
 ```
 python3 change_diary.py make_good_points 'Фролов Иван'
 ```

### Удалить замечания
Исправляет все замечания указанному ученику. По всем предметам.

 - <команда>: ```remove_chastisements```
 - <аргумент1>: **обязательный** ```Фамилия Имя Отчество``` (возможно, будет достаточно Фамилия Имя)
 - <аргумент2>: **обязательный** ```предмет```
 - <аргумент3>: ```не требуется```
 - <аргумент4>: ```не требуется```

 **Пример**
 ```
 python3 change_diary.py remove_chastisements 'Фролов Иван'
 ```

 ### Похвалить
 Добавляет похвальную запись к уроку по предмету. Опять-таки указанному ученику. Текст можешь написать сам, можешь положиться на случайный выбор скрипта.

 - <команда>: ```create_commendation```
 - <аргумент1>: **обязательный** ```Фамилия Имя Отчество``` (возможно, будет достаточно Фамилия Имя)
 - <аргумент2>: **обязательный** ```предмет```
 - <аргумент3>: **обязательный** ```random указывает скрипту брать для похвалы случайный урок.``` Если установишь last, то похвала запишется на последний урок.
 - <аргумент4>: 
 *не обязательный*   ```по умолчанию выбирается случайная ободряющая фраза.``` Если хочешь увидеть в дневнике какой-то конкретный текст, то укажи 'Хвалебный текст'.

 **Примеры**
 ```
 python3 change_diary.py create_commendation 'Фролов Иван' 'Математика' 'random' 'Да ты просто монстр!' 
 ```
  ```
 python3 change_diary.py create_commendation 'Фролов Иван' 'Музыка' 'last'
 ```

  ### Танцуют все!
 Настоящий хакер должен дарить радость людям. Да, на этой команде ты спалишься, но это будет, возможно, одно из самых ярких мгновений твоей хакерской жизни. 

 Итак - ставим ВСЕМ ПЯТЬ ПО ВСЕМ ПРЕДМЕТАМ! Всем - значит всем, без компромиссов.

 - <команда>: ```dance_everybody!```
 
 Аргументы? Да какие тут могут быть аргументы, вперёд, к славе!!!
   ```
 python3 change_diary.py dance_everybody!
 ```
 Учеников много, так что придётся немного подожать, пока скрипт осчастливит всех. Готов?


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

Теперь, если что, ты знаешь, куда обращаться ;-)