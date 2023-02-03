# Строение репозитория

- makefile
- veryfye.py - проверяет правильность выполнения программы в обычном виде
- very_equal.py - проверят схожесть результатов работы обычной программы и её circom аналога

## src

- main.circom - основная схема, которая подключает все остальные
- *.circom - все тестируемые схемы

## tools 

- test
    - tester.js - для запуска тестов
    - utils.js  - для запуска тестов 
    - witness_calculator.js - для запуска тестов
- test.js - для запуска тестов 

- calc_witness.js - (доделать)
- check.py, check.sh - проверяют на совпадение посчитанные вводы из calculations
- gen_input.py - 
- map.js - выводит соотношения в constr.json в удобном для меня формате
- verify.py - проверяет правильность выполнения любой схемы на основе её R1CS представления

## calculations

Посчитанные tools/verify.py вводы в формате input%d%d.json

## constraints

- constr       - ограничения в формате R1CS
- constr.json  - ограничения в формате R1CS, json
- main.r1cs    - ограничения в формате R1CS, бин
- main.sym     - ограничения в формате R1CS, симметричный

## data

- calculated_input.json - возможный ввод не совпадающий с изначальным
- input.json - ввод для теста
- map.json - соотношение индексов в constr.json к переменным в схеме


