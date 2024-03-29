# Переиспользование кода и модулей

Первичной целью проекта была сборка разных продуктов 1С из одних и тех же исходников. 
Общий для разных продуктов программный код и объекты метаданных (далее общие файлы)
предполагается разместить в отдельных репозиториях (субмодулях). 

Важно! Общие файлы не могул лежать в папке с результатами распаковки.

## Переиспользование кода

Разбиение кода на несколько файлов делается с помощью областей имеющих в названии
ключевое слово include: 

    #Область include_[путь до файла]
    #КонецОбласти 

Для версий 82 и 81 все директивы компилятора автоматически экранируются 
в комментарий //v8unpack {#директива...}. ВАЖНО. Есть маленькое допущение сильно
упрощающее жизнь - код не может начинаться с директивы (замена происходит 
по \n# - просто отступите строку в начале кода)

    //v8unpack #Область include_[путь до файла]
    //v8unpack #КонецОбласти 


При разборке модуля код внутри include области вырезается и сохраняется в
отдельный файл, при сборке происходит обратная процедура.


"Путь до файла" - это путь относительно родидельского каталога папки распаковки 
(корня репозитория при рекомендованной структуре), где в качестве разделеителя 
используется символ подчеркивания.

Например, в нижеследующем примере рядом с папкой сборки будет создана папка "core",а 
в ней папка "form3" с файлом "test.1с" сожержащий весь код внутри области. В исходном 
файле формы останется только описание области.

    #Область include_core_form3_test
    ПримерКода = 1;
    #КонецОбласти

Если область include содержат другие вложенные области include они будут так же вынесены в 
отдельные папки. Путь рассчитывается так же как и для области верхнего уровня.
 
Области include могут содержать обычные области.

Пустое значение в имени include области трактуется как переход к папке верхнего уровня.

## Переиспользование макетов и форм

Для переноса любых других файлов используется используется json файл содержащий список 
файлов полежащих переносу и каталог назначения.

```json
  {
    "ExternalDataProcessor.1c": "core\\ExternalDataProcessor.1c",
    "ExternalDataProcessor.data83.json": "core\\ExternalDataProcessor.data83.json",
    "ExternalDataProcessor.json": "core\\ExternalDataProcessor.json",
    "Form": {
      "API.1c": "core\\Form\\API.1c",
      "API.form83.json": "core\\Form\\API.form83.json"
    }
  }
 ```
Чтобы не набивать руками есть генератор оглавления, который добавляет в имеющийся
файл все чего там нет.

    v8unpack.exe -I index.json src core
    
параметры 
* путь до файла индекса 
* папка с исходниками 
* каталог с общими модулями по умолчанию, если не указать заполнит пустыми значениями


# Обновление

Версия модуля строится по шаблону {мажор}.{минор}.{патч}

Смена номера мажорной или минорной версии говорит об обратной несовместимости.

Собирать исходники разобранные утилитой с другой мажорной+минорной версией нельзя!

Порядок обновления:
1. Соберите бинарник старой версией.
2. Обновите утилиту.
3. Разберите бинарник новой версией.
4. Закоммитьте изменения.


# Рекомендации

* указывайте расширение имени файла в последнем слове комментария к метаданным хранящим
бинарные данные (макеты, общие картинки и т.п.), тогда после разборки вы будете иметь 
файлы с правильным расширением.
