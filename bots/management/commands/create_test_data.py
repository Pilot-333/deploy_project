from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bots.models import Bot, Scenario, Step, BotExecution


class Command(BaseCommand):
    help = 'Создание тестовых данных для системы ботов'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем создание тестовых данных...')

        # Создаем или получаем пользователя
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@alpina.ru',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS('Создан пользователь admin (пароль: admin123)')
            )
        else:
            self.stdout.write('Пользователь admin уже существует')

        # Создаем демонстрационного бота
        bot, bot_created = Bot.objects.get_or_create(
            name="Бизнес-консультант Alpina",
            defaults={
                'description': 'Интеллектуальный помощник для бизнес-консультаций и обучения',
                'bot_type': 'chat',
                'gpt_model': 'gpt-3.5-turbo',
                'creativity_level': 0.8,
                'max_tokens': 1500,
                'system_prompt': '''Ты - экспертный бизнес-консультант издательской группы Альпина. 
Ты помогаешь с вопросами управления, маркетинга, лидерства и профессионального развития.
Отвечай профессионально, но дружелюбно. Используй примеры из бизнес-литературы.''',
                'is_active': True,
                'created_by': user
            }
        )

        if bot_created:
            self.stdout.write(
                self.style.SUCCESS(f'Создан бот: {bot.name}')
            )
        else:
            self.stdout.write('Бот уже существует')

        # Создаем сценарий приветствия
        scenario, scenario_created = Scenario.objects.get_or_create(
            name="Сценарий знакомства",
            bot=bot,
            defaults={
                'description': 'Базовый сценарий для знакомства с пользователем и определения его потребностей',
                'is_active': True
            }
        )

        if scenario_created:
            self.stdout.write(
                self.style.SUCCESS(f'Создан сценарий: {scenario.name}')
            )

        # Очищаем существующие шаги для этого сценария (если они есть)
        Step.objects.filter(scenario=scenario).delete()

        # Создаем шаги сценария
        steps_data = [
            {
                'name': 'Приветствие',
                'step_type': 'message',
                'content': {
                    'message': '''Добро пожаловать в Alpina Digital!

Я ваш виртуальный бизнес-консультант. Помогаю с вопросами управления, лидерства, маркетинга и профессионального развития.

Расскажите, чем я могу вам помочь?'''
                },
                'order': 1
            },
            {
                'name': 'Выбор категории',
                'step_type': 'question',
                'content': {
                    'question': '''Выберите интересующую вас тему:
1. Управление и лидерство
2. Маркетинг и продажи  
3. Карьера и саморазвитие
4. Бизнес-процессы и эффективность
5. Другое''',
                    'response_template': 'Отлично! Вы выбрали тему: {user_input}. Расскажите подробнее, что именно вас интересует?'
                },
                'order': 2
            },
            {
                'name': 'Уточнение запроса',
                'step_type': 'question',
                'content': {
                    'question': 'Понятно! Что конкретно вы хотели бы узнать или обсудить в рамках этой темы?',
                    'validation_rules': {
                        'min_length': 5,
                        'max_length': 500
                    }
                },
                'order': 3
            },
            {
                'name': 'Рекомендация ресурсов',
                'step_type': 'message',
                'content': {
                    'message': '''Благодарю за уточнение! На основе вашего запроса я могу:

• Дать развернутый ответ с примерами из бизнес-практики
• Порекомендовать подходящие книги из библиотеки Альпина
• Предложить формат дальнейшего взаимодействия

Хотите продолжить в формате диалога или предпочитаете получить конкретные рекомендации?'''
                },
                'order': 4
            }
        ]

        # Создаем шаги и устанавливаем связи между ними
        previous_step = None
        created_steps = []

        for step_data in steps_data:
            step = Step.objects.create(
                name=step_data['name'],
                step_type=step_data['step_type'],
                scenario=scenario,
                content=step_data['content'],
                order=step_data['order'],
                next_step=None
            )
            created_steps.append(step)

            if previous_step:
                previous_step.next_step = step
                previous_step.save()

            previous_step = step
            self.stdout.write(
                self.style.SUCCESS(f'Создан шаг: {step.name} (порядок: {step.order})')
            )

        # Устанавливаем начальный шаг для сценария
        scenario.initial_step = created_steps[0] if created_steps else None
        scenario.save()

        # Создаем второго бота для демонстрации
        bot2, bot2_created = Bot.objects.get_or_create(
            name="HR-ассистент",
            defaults={
                'description': 'Специализированный бот для вопросов управления персоналом и HR',
                'bot_type': 'chat',
                'gpt_model': 'gpt-3.5-turbo',
                'creativity_level': 0.5,
                'max_tokens': 1000,
                'system_prompt': '''Ты - HR-эксперт с опытом в управлении персоналом, подборе сотрудников, 
оценке персонала и развитии корпоративной культуры. Отвечай точно и профессионально.''',
                'is_active': True,
                'created_by': user
            }
        )

        if bot2_created:
            self.stdout.write(
                self.style.SUCCESS(f'Создан бот: {bot2.name}')
            )

        # Создаем тестовое выполнение для демонстрации
        execution, execution_created = BotExecution.objects.get_or_create(
            bot=bot,
            user_session='demo_session_001',
            defaults={
                'scenario': scenario,
                'current_step': created_steps[0] if created_steps else None,
                'conversation_history': [
                    {"role": "user", "content": "Привет, я хочу улучшить навыки управления"},
                    {"role": "assistant",
                     "content": "Отлично! Управление - это ключевой навык современного лидера. С чего хотели бы начать?"}
                ],
                'is_completed': False
            }
        )

        if execution_created:
            self.stdout.write(
                self.style.SUCCESS('Создана демо-сессия выполнения бота')
            )

        self.stdout.write(
            self.style.SUCCESS('\nТестовые данные успешно созданы!')
        )

        self.stdout.write('\nСоздано:')
        self.stdout.write(f'   • Пользователей: {User.objects.count()}')
        self.stdout.write(f'   • Ботов: {Bot.objects.count()}')
        self.stdout.write(f'   • Сценариев: {Scenario.objects.count()}')
        self.stdout.write(f'   • Шагов: {Step.objects.count()}')
        self.stdout.write(f'   • Выполнений: {BotExecution.objects.count()}')

        self.stdout.write('\nДля проверки:')
        self.stdout.write('   • Главная страница: http://127.0.0.1:8000/')
        self.stdout.write('   • API ботов: http://127.0.0.1:8000/api/bots/')
        self.stdout.write('   • Админка: http://127.0.0.1:8000/admin/')
        self.stdout.write('   • Логин в админку: admin / admin123')