
# UDP Serial Reader 

Программа прозвонщик с gui на pyqt5 которая отправляет команды по serial порту и читает данные по udp  для дальнейшей отрисовки.


## Установка


```bash
  python -m venv .venv 

  pip install -r requirements.txt
  
  python main.py
```
    
## Структура проекта


| Модуль |  описание               |
| :-------- |  :------------------------- |
| `bench` |  Общение по serial порту и окно подключения к устройствам |
| `device_parameters` |  Получение данных по UDP и отрисовка графиков |
| `sequence_sender` | Чтение и отправка команд из yaml файла + регистрация функций для yaml|
| `main` | Главное окно  |
| `support` |  Дополнительный функциона, а так же константы |


## Фичи

- Yaml парсер который берет из файла данные для отправки последовательности по serial. 
- Регистрация в yaml функций из питона, чтобы далее использовать их в составлении последовательностей


## Пример создания последовательности с помощью yaml 

```yaml
- Function:LogEnable:
    enable: true
- Function:sum:
    a: 1
    b: 2
- Command: [
    SetMaxPwm: 0.001,
    SetMinPwm: 0.001
    ]

- Function:LogEnable:
    enable: false

- Command:
    SetMaxPwm: "$LogEnable" # функция возвращает имя файла в который записалось логирование
    SetMinPwm: 0.001

```

