# Plant Care Agent (Лабораторная №1)

AI-агент-консультант по уходу за растениями, реализованный с помощью LangGraph.

## Структура проекта
- **PlannerNode** — извлекает растение и симптомы из пользовательского запроса.
- **TrefleNode** — получает ботанические характеристики.
- **PerenualNode** — получает рекомендации по уходу.
- **DiagnosisNode** — анализирует данные и формирует предварительный диагноз.
- **WriterNode** — формирует финальные рекомендации пользователю.

## Используемые API
- [Trefle API](https://trefle.io)
- [Perenual API](https://perenual.com/docs/api)

## Запуск
```bash
pip install -r requirements.txt
python main.py