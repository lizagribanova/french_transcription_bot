Приветствую! 

Этот проект представляет собой телеграм бот-транскриптор французского языка по МФА. 

Бот принимает французские слова и предложения и возвращает их фонетическую транскрипцию. Он учитывает основные правила чтения французского языка, включая исключения и особые случаи произношения.

Структура проекта:

flowchart LR
    Project[french_transcription_bot] --> A[main.py<br>⬇<br>Точка входа]
    Project --> B[config/<br>⬇<br>Настройки]
    Project --> C[handlers/<br>⬇<br>Обработчики]
    Project --> D[lexicon/<br>⬇<br>Ответы бота]
    Project --> E[transcription/<br>⬇<br>Транскрипция]
    Project --> F[.env.example<br>⬇<br>Переменные]
    Project --> G[requirements.txt<br>⬇<br>Зависимости]
    Project --> H[README.md<br>⬇<br>Документация]
    
    C --> C1[user.py<br>Команды]
    C --> C2[other.py<br>Сообщения]
    
    E --> E1[transcriber.py<br>Правила чтения]
    
    classDef project fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    classDef main fill:#E8F5E9,stroke:#388E3C,stroke-width:2px
    classDef folder fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    classDef sub fill:#FFF3E0,stroke:#E65100,stroke-width:2px
    
    class Project project
    class A main
    class B,C,D,E folder
    class F,G,H main
    class C1,C2,E1 sub


Айди бота в тг: @french_transcription_bot
