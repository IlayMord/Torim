# TORIM - Python Flask Application
# אפליקציית TORIM בפייתון עם Flask

import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# יצירת אפליקציית Flask
app = Flask(__name__)
app.secret_key = 'torim_secret_key_2025'

# יצירת מסד הנתונים
def init_database():
    conn = sqlite3.connect('torim.db')
    cursor = conn.cursor()
    
    # טבלת משתמשים
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        avatar TEXT,
        reliability INTEGER DEFAULT 95,
        referral_code TEXT,
        referred_friends INTEGER DEFAULT 0,
        is_business_owner BOOLEAN DEFAULT FALSE,
        business_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # טבלת עסקים
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS businesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        image TEXT,
        rating REAL DEFAULT 0.0,
        review_count INTEGER DEFAULT 0,
        distance TEXT,
        wait_time TEXT,
        address TEXT,
        phone TEXT,
        description TEXT,
        hours TEXT,
        is_open BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # טבלת שירותים
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER,
        name TEXT NOT NULL,
        duration INTEGER NOT NULL,
        price INTEGER NOT NULL,
        FOREIGN KEY (business_id) REFERENCES businesses (id)
    )''')
    
    # טבלת תורים
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        business_id INTEGER,
        service_id INTEGER,
        appointment_date DATE,
        appointment_time TIME,
        status TEXT DEFAULT 'confirmed',
        price INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (business_id) REFERENCES businesses (id),
        FOREIGN KEY (service_id) REFERENCES services (id)
    )''')
    
    # טבלת היסטוריית תורים
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointment_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        business_id INTEGER,
        service_name TEXT,
        appointment_date DATE,
        appointment_time TIME,
        status TEXT DEFAULT 'completed',
        rating INTEGER,
        review TEXT,
        price INTEGER,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (business_id) REFERENCES businesses (id)
    )''')
    
    # טבלת הודעות צ'אט
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message_type TEXT,
        message_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    conn.close()

# פונקציה להוספת נתונים לדוגמה
def populate_sample_data():
    conn = sqlite3.connect('torim.db')
    cursor = conn.cursor()
    
    # משתמש לדוגמה
    cursor.execute('''
    INSERT OR IGNORE INTO users (name, email, phone, password_hash, referral_code, is_business_owner, business_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('יוסי לוי', 'yossi@example.com', '050-1234567', 
          generate_password_hash('password123'), 'YOSSI2025', True, 1))
    
    # עסקים לדוגמה
    businesses_data = [
        ('מספרת הדר', 'hair', 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400',
         4.8, 127, '0.5 ק"מ', '15 דק\'', 'רחוב הרצל 45, תל אביב', '03-1234567',
         'מספרה מקצועית עם צוות מנוסה', 'ב-ו: 8:00-20:00, ש: סגור', True),
        
        ('ספא רילקס', 'beauty', 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=400',
         4.9, 84, '1.2 ק"מ', 'זמין', 'רחוב דיזנגוף 125, תל אביב', '03-5555555',
         'ספא יוקרתי עם טיפולים מתקדמים', 'א-ו: 9:00-21:00, ש: 10:00-18:00', True),
        
        ('רופא משה כהן', 'medical', 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400',
         4.7, 203, '0.8 ק"מ', '30 דק\'', 'רחוב אלנבי 15, תל אביב', '03-7777777',
         'רופא משפחה מנוסה', 'א-ה: 8:00-18:00, ו: 8:00-13:00', True)
    ]
    
    for business in businesses_data:
        cursor.execute('''
        INSERT OR IGNORE INTO businesses 
        (name, category, image, rating, review_count, distance, wait_time, address, phone, description, hours, is_open)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', business)
    
    # שירותים לדוגמה
    services_data = [
        # שירותי מספרת הדר
        (1, 'תספורת גברים', 30, 80),
        (1, 'תספורת נשים', 45, 120),
        (1, 'צביעה', 90, 200),
        (1, 'פן ועיצוב', 60, 150),
        
        # שירותי ספא רילקס
        (2, 'עיסוי שוודי', 60, 250),
        (2, 'טיפול פנים', 90, 350),
        (2, 'מניקור פדיקור', 75, 180),
        (2, 'טיפול גוף מלא', 120, 450),
        
        # שירותי רופא משה כהן
        (3, 'בדיקה כללית', 30, 150),
        (3, 'חיסון', 15, 50),
        (3, 'בדיקת לב', 45, 200),
        (3, 'ייעוץ תזונה', 60, 180)
    ]
    
    for service in services_data:
        cursor.execute('''
        INSERT OR IGNORE INTO services (business_id, name, duration, price)
        VALUES (?, ?, ?, ?)
        ''', service)
    
    # תור לדוגמה
    cursor.execute('''
    INSERT OR IGNORE INTO appointments 
    (user_id, business_id, service_id, appointment_date, appointment_time, price)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (1, 1, 1, '2025-09-19', '14:30', 80))
    
    # היסטוריה לדוגמה
    history_data = [
        (1, 1, 'תספורת גברים', '2025-08-15', '15:00', 'completed', 5, 'שירות מעולה, מאוד מרוצה', 80),
        (1, 2, 'עיסוי שוודי', '2025-07-28', '16:30', 'completed', 4, 'מרגיע מאוד', 250)
    ]
    
    for history in history_data:
        cursor.execute('''
        INSERT OR IGNORE INTO appointment_history
        (user_id, business_id, service_name, appointment_date, appointment_time, status, rating, review, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', history)
    
    conn.commit()
    conn.close()

# יצירת מסד הנתונים והוספת נתונים לדוגמה
init_database()
populate_sample_data()

print("✅ מסד הנתונים של TORIM נוצר בהצלחה!")
print("✅ נתונים לדוגמה נוספו")