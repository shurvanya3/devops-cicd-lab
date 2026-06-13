# Отчёт по лабораторной работе: Настройка CI/CD и Trunk-Based Development

![CI Pipeline](https://github.com/shurvanya3/devops-cicd-lab/actions/workflows/ci.yml/badge.svg)

* **Студент:** Шурлепов И.А. / https://github.com/shurvanya3
* **Репозиторий проекта:** https://github.com/shurvanya3/devops-cicd-lab

---

## Чек-лист выполненных этапов

- [x] **Этап 1 & 2: Настройка CI-пайплайна** (Параллельный запуск Lint, Test, Security-scan через Fan-Out/Fan-In).
- [x] **Этап 3: Сборка и публикация образов** (Оптимизация Docker layer cache через `type=gha` и пуш в GHCR).
- [x] **Этап 4: Trunk-Based Development & Feature Flags** (Управление логикой через переменные окружения, защита веток).
- [x] **Этап 5: Автоматический CD-пайплайн** (Разделение на Staging и Production с ручным утверждением).
- [x] **Продвинутый функционал:** Matrix Build, Reusable Workflows, автообновление через Dependabot.

---

## Результаты работы и архитектура пайплайна

### 1. Безопасность и Trunk-Based Development (Branch Protection)
Ветка `main` полностью защищена от случайных деструктивных действий:
* прямой пуш (`git push origin main`) физически заблокирован для всех, включая администратора;
* слияние изменений возможно исключительно через **Pull Request**;
* кнопка Merge блокируется до тех пор, пока финальная джоба `quality-gate` не вернёт успешный статус (*Required Status Check*).

Успешный Pull Request с проверками:** https://github.com/shurvanya3/devops-cicd-lab/pull/1

### 2. Оптимизированная сборка и реестр образов (GHCR)
Сборка Docker-образа автоматизирована и привязана к SHA каждого коммита.
* Используется драйвер `BuildKit` и распределенное кэширование слоёв (`type=gha`), что сокращает время повторной сборки до минимума;
* настроено кэширование зависимостей Python (`pip cache`).

Ссылка на собранный пакет (Package): https://github.com/shurvanya3/devops-cicd-lab/packages

```bash
# Команда для скачивания актуального собранного образа
docker pull ghcr.io/shurvanya3/devops-cicd-lab:latest
```

### 3. Демонстрация Feature Flag & Матричное тестирование

В приложение внедрён динамический feature-флаг через эндпоинт `/greeting`. Поведение приложения меняется без пересборки Docker-образа - простой сменой переменной окружения `FEATURE_NEW_GREETING`.

- **Matrix Build:** Тестирование логики флага автоматически и параллельно запускается на **трёх версиях Python (3.10, 3.11, 3.12)** для гарантии обратной совместимости.
    
- Тесты используют фикстуру `monkeypatch` и проверяют оба состояния флага. Результаты тестов для каждой версии Python сохраняются в артефактах GitHub Actions (`pytest-report-python-*`).
    

![CI Pipeline](https://github.com/shurvanya3/devops-cicd-lab/actions/workflows/ci.yml/badge.svg)

### 4. Внедрение DRY и автоматизации (Advanced DevOps)

- **Reusable Workflows:** Логика статического анализа кода вынесена в отдельный изолированный воркфлоу `.github/workflows/reusable-lint.yml`. Главный пайплайн вызывает его с передачей входных параметров (`inputs`).
    
- **Dependabot:** В корне проекта настроен конфиг `.github/dependabot.yml`, который в автоматическом режиме каждую неделю сканирует `requirements.txt` на наличие устаревших зависимостей и самостоятельно создаёт безопасные PR для их обновления.
    

## Инструкция по локальному запуску из Docker

Запуск и проверка обеих версий функционала из одного и того же скачанного Docker-образа:

1. **Запуск со стабильным (старым) функционалом (feature-флаг выключен/отсутствует):**
    
    ```bash
    docker run -d -p 5000:5000 --name app_stable ghcr.io/shurvanya3/devops-cicd-lab:latest
    ```
    
2. **Запуск с новым функционалом (Фича-флаг активирован):**
    
    ```bash
    docker run -d -p 5001:5000 -e FEATURE_NEW_GREETING=true --name app_feature ghcr.io/shurvanya3/devops-cicd-lab:latest
    ```
