#!/bin/sh
set -e

echo "⏳ Ожидание готовности PostgreSQL..."
while ! pg_isready -h db -U ${DB_USER} -d ${DB_NAME} -t 5 2>/dev/null; do
    echo "  PostgreSQL ещё не готов, ждём..."
    sleep 2
done
echo "✅ PostgreSQL готов!"

echo "⏳ Ожидание готовности Redis..."
while ! redis-cli -h redis -p 6379 ping 2>/dev/null | grep -q PONG; do
    echo "  Redis ещё не готов, ждём..."
    sleep 2
done
echo "✅ Redis готов!"

# Применяем миграции
echo "🔄 Применение миграций..."
python manage.py migrate --noinput

# Собираем статику
echo "📦 Сборка статики..."
python manage.py collectstatic --noinput

# Запускаем сервер
echo "🚀 Запуск Django..."
exec python manage.py runserver 0.0.0.0:8000