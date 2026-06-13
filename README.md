# Отчет по лабораторной работе: Настройка CI/CD и Trunk-Based Development

**Студент:** Шурлепов И.А. / https://github.com/shurvanya3
**Репозиторий проекта:** https://github.com/shurvanya3/devops-cicd-lab
![CI Pipeline](https://github.com/shurvanya3/devops-cicd-lab/actions/workflows/ci.yml/badge.svg)

---

## Чек-лист выполненных этапов

- [x] **Этап 1 & 2: Настройка CI-пайплайна** (Линтинг, тестирование, аудит безопасности)
- [x] **Этап 3: Сборка и публикация образов** (Интеграция с GHCR через BuildKit)
- [x] **Этап 4: Trunk-Based Development & Feature Flags** (Защита веток, Pull Request, логика флагов)
- [x] **Этап 5: Автоматический CD-пайплайн** (Развертывание на Staging/Production с ручным утверждением)

---

## Результаты работы пайплайна

### 1. Защита основной ветки (Branch Protection)
Ветка `main` полностью защищена. Прямой пуш заблокирован. Слияние изменений возможно только через Pull Request при условии:
* Успешного прохождения финальной джобы качества `quality-gate`.
* Ветка находится в состоянии *up-to-date* перед слиянием.
* Правила распространяются на администраторов репозитория.

**Ссылка на успешный Pull Request с проверками:** https://github.com/shurvanya3/devops-cicd-lab/pull/1

### 2. Сборка Docker-образа в реестр (GHCR)
Сборка Docker-образа оптимизирована с помощью драйвера `BuildKit` и кэширования слоев (`type=gha`). Образы автоматически публикуются в GitHub Packages.

**Ссылка на собранный пакет (Package):** https://github.com/shurvanya3/devops-cicd-lab/packages

**Команда для скачивания актуального образа:** 
```bash
docker pull ghcr.io/shurvanya3/devops-cicd-lab:sha-020de9c933e5305bc0b7ab4cadfd0449c354d606
```

### 3. Демонстрация Feature Flag (Тестирование флага)
В приложение внедрен эндпоинт `/greeting`, поведение которого динамически изменяется переменной окружения `FEATURE_NEW_GREETING`.

Логика покрыта тестами `pytest` с использованием фикстуры `monkeypatch` под оба сценария:

Флаг выключен (`false` или отсутствует): Эндпоинт возвращает старую стабильную версию приветствия.

Флаг включен (`true`): Эндпоинт возвращает новую версию приветствия.

Все 5 тестов (включая базовые проверки `/` и `/health`) успешно проходят в CI:
```
Status: 5 passed in _s (quality-gate:success)
```

## Как запустить приложение локально из Docker

1. **Запуск со старым функционалом (Feature-флаг выключен):**

    ```bash
    docker run -d -p 5000:5000 --name app_stable ghcr.io/shurvanya3/devops-cicd-lab:sha-<ВСТАВЬ_SHA_СВОЕГО_КОММИТА>
    ```

2. **Запуск с новым функционалом (Feature-флаг включен):**

    ```bash
    docker run -d -p 5001:5000 -e FEATURE_NEW_GREETING=true --name app_feature ghcr.io/shurvanya3/devops-cicd-lab:sha-<ВСТАВЬ_SHA_СВОЕГО_КОММИТА>
    ```

