# TORIM - Python Application Structure
# יצירת מבנה האפליקציה בפייתון

import os
import sqlite3
import json
from datetime import datetime, timedelta

# נתוני האפליקציה
class TorimApp:
    def __init__(self):
        self.users = {}
        self.businesses = {}
        self.appointments = {}
        self.chat_messages = {}
        self.current_user_id = 1
        self.init_sample_data()
    
    def init_sample_data(self):
        """יצירת נתונים לדוגמה"""
        
        # משתמש נוכחי
        self.users[1] = {
            'id': 1,
            'name': 'יוסי לוי',
            'email': 'yossi@example.com',
            'phone': '050-1234567',
            'avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150',
            'password': 'hashed_password',
            'reliability': 95,
            'referral_code': 'YOSSI2025',
            'referred_friends': 3,
            'is_business_owner': True,
            'business_id': 1,
            'created_at': datetime.now()
        }
        
        # עסקים
        self.businesses = {
            1: {
                'id': 1,
                'name': 'מספרת הדר',
                'category': 'hair',
                'image': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400',
                'rating': 4.8,
                'review_count': 127,
                'distance': '0.5 ק"מ',
                'wait_time': '15 דק\'',
                'address': 'רחוב הרצל 45, תל אביב',
                'phone': '03-1234567',
                'description': 'מספרה מקצועית עם צוות מנוסה',
                'hours': 'ב-ו: 8:00-20:00, ש: סגור',
                'is_open': True,
                'services': [
                    {'id': 1, 'name': 'תספורת גברים', 'duration': 30, 'price': 80},
                    {'id': 2, 'name': 'תספורת נשים', 'duration': 45, 'price': 120},
                    {'id': 3, 'name': 'צביעה', 'duration': 90, 'price': 200},
                    {'id': 4, 'name': 'פן ועיצוב', 'duration': 60, 'price': 150}
                ]
            },
            2: {
                'id': 2,
                'name': 'ספא רילקס',
                'category': 'beauty',
                'image': 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=400',
                'rating': 4.9,
                'review_count': 84,
                'distance': '1.2 ק"מ',
                'wait_time': 'זמין',
                'address': 'רחוב דיזנגוף 125, תל אביב',
                'phone': '03-5555555',
                'description': 'ספא יוקרתי עם טיפולים מתקדמים',
                'hours': 'א-ו: 9:00-21:00, ש: 10:00-18:00',
                'is_open': True,
                'services': [
                    {'id': 11, 'name': 'עיסוי שוודי', 'duration': 60, 'price': 250},
                    {'id': 12, 'name': 'טיפול פנים', 'duration': 90, 'price': 350},
                    {'id': 13, 'name': 'מניקור פדיקור', 'duration': 75, 'price': 180},
                    {'id': 14, 'name': 'טיפול גוף מלא', 'duration': 120, 'price': 450}
                ]
            },
            3: {
                'id': 3,
                'name': 'רופא משה כהן',
                'category': 'medical',
                'image': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400',
                'rating': 4.7,
                'review_count': 203,
                'distance': '0.8 ק"מ',
                'wait_time': '30 דק\'',
                'address': 'רחוב אלנבי 15, תל אביב',
                'phone': '03-7777777',
                'description': 'רופא משפחה מנוסה',
                'hours': 'א-ה: 8:00-18:00, ו: 8:00-13:00',
                'is_open': True,
                'services': [
                    {'id': 21, 'name': 'בדיקה כללית', 'duration': 30, 'price': 150},
                    {'id': 22, 'name': 'חיסון', 'duration': 15, 'price': 50},
                    {'id': 23, 'name': 'בדיקת לב', 'duration': 45, 'price': 200},
                    {'id': 24, 'name': 'ייעוץ תזונה', 'duration': 60, 'price': 180}
                ]
            }
        }
        
        # תורים נוכחיים
        self.appointments[1] = {
            'id': 1,
            'user_id': 1,
            'business_id': 1,
            'business_name': 'מספרת הדר',
            'business_image': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400',
            'service_name': 'תספורת גברים',
            'service_id': 1,
            'date': '2025-09-19',
            'time': '14:30',
            'status': 'confirmed',
            'address': 'רחוב הרצל 45, תל אביב',
            'phone': '03-1234567',
            'price': 80,
            'can_cancel': True,
            'reminder': True,
            'created_at': datetime.now()
        }
        
        # הודעות צ'אט
        self.chat_messages[1] = [
            {
                'id': 1,
                'type': 'assistant',
                'text': 'שלום יוסי! 👋 אני עדן, העוזרת הדיגיטלית של TORIM. איך אוכל לעזור לך היום?',
                'time': '10:45',
                'created_at': datetime.now()
            }
        ]

# יצירת אפליקציה
app = TorimApp()

print("✅ מבנה האפליקציה נוצר בהצלחה!")
print(f"✅ {len(app.businesses)} עסקים נטענו")
print(f"✅ {len(app.appointments)} תורים פעילים")
print(f"✅ משתמש נוכחי: {app.users[1]['name']}")