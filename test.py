#%%
from sqlalchemy import create_engine, text

def simple_test():
    try:
        engine = create_engine('postgresql://postgres:33ZqPiWj33@217.65.3.240:5432/report_db')
        
        with engine.connect() as conn:
            print("✅ Подключение к PostgreSQL успешно!")
            
            # Простая проверка - можем ли выполнять запросы
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.scalar()
            print(f"✅ Тестовый запрос выполнен: {test_value}")
            
            # Проверяем существование базы
            result = conn.execute(text("SELECT EXISTS(SELECT 1 FROM information_schema.tables)"))
            has_tables = result.scalar()
            
            if has_tables:
                print("📋 В базе есть таблицы")
            else:
                print("📭 База пустая - можно создавать таблицы")
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")

simple_test()




# #%%
# from sqlalchemy import create_engine, text

# try:
#     engine = create_engine('postgresql://postgres:33ZqPiWj33@217.65.3.240:5432/report_db')
    
#     with engine.connect() as conn:
#         print("✅ Подключение к PostgreSQL установлено!")
        
#         # Проверяем версию БД
#         result = conn.execute(text("SELECT version()"))
#         db_version = result.scalar()
#         print(f"📊 Версия PostgreSQL: {db_version}")
        
#         # Проверяем таблицы
#         result = conn.execute(text("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = 'public'
#         """))
#         tables = result.fetchall()
#         print(f"📋 Найдено таблиц: {len(tables)}")
#         for table in tables:
#             print(f"   - {table[0]}")
            
# except Exception as e:
#     print(f"❌ Ошибка подключения: {e}")




# %%
import paramiko
import psycopg2
from sqlalchemy import create_engine, text
import time

def create_ssh_tunnel():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("🔗 Подключаемся к серверу...")
        client.connect(
            '217.65.3.240',
            port=5432,
            username='FokinaM',
            password='Wk6t%#Xv',
            look_for_keys=False,
            allow_agent=False
        )
        
        print("✅ SSH подключение установлено")
        
        # Создаем туннель
        transport = client.get_transport()
        local_port = 5432
        transport.request_port_forward('', local_port)
        
        print("🔌 Туннель создан на localhost:5432")
        
        # Подключаемся к БД
        engine = create_engine('postgresql://postgres:33ZqPiWj33@localhost:5432/report_db')
        
        with engine.connect() as conn:
            print("✅ Подключение к PostgreSQL установлено!")
            result = conn.execute(text("SELECT version()"))
            print(f"📊 Версия: {result.scalar()}")
            
        # Держим соединение открытым
        print("⏳ Туннель активен... Нажмите Ctrl+C для закрытия")
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        client.close()
        print("🔚 Соединение закрыто")

if __name__ == "__main__":
    create_ssh_tunnel()
    
    
#%%

import socket

def scan_ports(host, ports):
    print(f"🔍 Сканируем порты на {host}...")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"✅ Порт {port} ОТКРЫТ")
            else:
                print(f"❌ Порт {port} закрыт")
            sock.close()
        except Exception as e:
            print(f"⚠️  Порт {port}: {e}")

# Проверим основные порты
ports_to_check = [22, 49155, 5432, 3389, 80, 443]
scan_ports('217.65.3.240', ports_to_check)

# %%
from sqlalchemy import create_engine, text

try:
    print("🔧 Пробуем подключиться к PostgreSQL на порту 49155...")
    engine = create_engine('postgresql://postgres:33ZqPiWj33@217.65.3.240:49155/report_db')
    
    with engine.connect() as conn:
        print("🎉 УСПЕХ! PostgreSQL работает на порту 49155")
        result = conn.execute(text("SELECT version()"))
        print(f"📊 Версия: {result.scalar()}")
        
except Exception as e:
    print(f"❌ Это не PostgreSQL: {e}")
# %%

import telnetlib

try:
    print("🔧 Проверяем Telnet...")
    tn = telnetlib.Telnet('217.65.3.240', 49155, timeout=5)
    print("✅ Подключение по Telnet установлено")
    tn.close()
except:
    print("❌ Не Telnet")
# %%
import telnetlib
import time
from sqlalchemy import create_engine, text

def create_telnet_tunnel():
    try:
        print("🔗 Подключаемся к серверу через Telnet...")
        
        # Подключаемся через Telnet
        tn = telnetlib.Telnet('217.65.3.240', 49155, timeout=10)
        
        # Ждем приглашения для логина и отправляем учетные данные
        tn.read_until(b"login:", timeout=5)
        tn.write(b"FokinaM\n")
        time.sleep(1)
        
        tn.read_until(b"password:", timeout=5)
        tn.write(b"Wk6t%#Xv\n")
        time.sleep(1)
        
        print("✅ Telnet подключение установлено")
        
        # Теперь пробуем подключиться к PostgreSQL
        print("🔧 Подключаемся к PostgreSQL...")
        engine = create_engine('postgresql://postgres:33ZqPiWj33@localhost:5432/report_db')
        
        with engine.connect() as conn:
            print("🎉 УСПЕХ! Подключение к PostgreSQL установлено!")
            result = conn.execute(text("SELECT version()"))
            print(f"📊 Версия: {result.scalar()}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

create_telnet_tunnel()
# %%

import requests

try:
    response = requests.post('https://217.65.3.240/api/query', 
        json={"query": "SELECT version()"},
        auth=('postgres', '33ZqPiWj33')
    )
    if response.status_code == 200:
        print("✅ Есть веб-API для запросов")
except:
    print("❌ Нет веб-API")

# %%
