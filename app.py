# TORIM - Flask Application Main File
# אפליקציית TORIM בפייתון - קובץ ראשי

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime, timedelta
import os

from database import UserDatabase

app = Flask(__name__)
app.secret_key = 'torim_secret_key_2025'


@app.context_processor
def inject_datetime_helpers():
    """Expose datetime utilities to all templates."""
    return {
        'datetime': datetime,
        'timedelta': timedelta
    }

 codex/fix-errors-and-correct-code-f6tn0t
# נתוני הדגמה (משתמשים נשמרים במסד נתונים מאובטח)

class TorimData:
    def __init__(self, user_db: UserDatabase):
        self.db = user_db
        self.current_user = self._load_current_user()
        self.current_user_id = self.current_user['id']
        
        self.categories = [
            {'id': 'hair', 'name': 'מספרות', 'icon': 'scissors', 'count': 23},
            {'id': 'beauty', 'name': 'יופי ובריאות', 'icon': 'sparkles', 'count': 18},
            {'id': 'medical', 'name': 'רפואי', 'icon': 'stethoscope', 'count': 35},
            {'id': 'fitness', 'name': 'כושר ובריאות', 'icon': 'dumbbell', 'count': 12}
        ]
        
        self.businesses = [
            {
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
            {
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
            {
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
        ]
        
        self.recommendations = [
            {
                'id': 1,
                'title': 'זמן לתספורת החודשית שלך',
                'description': 'עברו 3 שבועות מהתספורת האחרונה. המערכת ממליצה לקבוע תור השבוע',
                'business_id': 1,
                'business_name': 'מספרת הדר',
                'business_image': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400',
                'priority': 'high',
                'reason': 'על בסיס ההיסטוריה שלך'
            },
            {
                'id': 2,
                'title': 'הספא החדש שכדאי לנסות',
                'description': 'ספא רילקס קיבל דירוגים מצוינים מחברים שלך. מתאים לסוף השבוע',
                'business_id': 2,
                'business_name': 'ספא רילקס',
                'business_image': 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=400',
                'priority': 'medium',
                'reason': 'המלצות חברים'
            },
            {
                'id': 3,
                'title': 'בדיקה שנתית אצל הרופא',
                'description': 'הגיע הזמן לבדיקה השנתית. רופא משה כהן זמין השבוע הבא',
                'business_id': 3,
                'business_name': 'רופא משה כהן',
                'business_image': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400',
                'priority': 'high',
                'reason': 'בדיקה תקופתית'
            }
        ]
        
        self.appointments = [
            {
                'id': 1,
                'business_id': 1,
                'business_name': 'מספרת הדר',
                'business_image': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400',
                'service_name': 'תספורת גברים',
                'date': '2025-09-19',
                'time': '14:30',
                'status': 'confirmed',
                'address': 'רחוב הרצל 45, תל אביב',
                'phone': '03-1234567',
                'price': 80,
                'can_cancel': True,
                'reminder': True
            }
        ]
        
        self.appointment_history = [
            {
                'id': 100,
                'business_id': 1,
                'business_name': 'מספרת הדר',
                'service_name': 'תספורת גברים',
                'date': '2025-08-15',
                'time': '15:00',
                'status': 'completed',
                'rating': 5,
                'review': 'שירות מעולה, מאוד מרוצה',
                'price': 80
            },
            {
                'id': 101,
                'business_id': 2,
                'business_name': 'ספא רילקס',
                'service_name': 'עיסוי שוודי',
                'date': '2025-07-28',
                'time': '16:30',
                'status': 'completed',
                'rating': 4,
                'review': 'מרגיע מאוד',
                'price': 250
            }
        ]
        
        self.chat_messages = [
            {
                'id': 1,
                'type': 'assistant',
                'text': 'שלום יוסי! 👋 אני עדן, העוזרת הדיגיטלית של TORIM. איך אוכל לעזור לך היום?',
                'time': '10:45'
            }
        ]

        self.business_dashboard = {
            'business_info': {
                'id': self.current_user.get('business_id') or 1,
                'name': 'מספרת הדר',
                'owner': self.current_user['name'],
                'phone': '03-1234567',
                'address': 'רחוב הרצל 45, תל אביב',
                'hours': 'ב-ו: 8:00-20:00'
            },
            'stats': {
                'today_appointments': 8,
                'weekly_revenue': 2400,
                'monthly_appointments': 89,
                'avg_rating': 4.8,
                'new_customers': 5,
                'returning_customers': 12
            },
            'today_schedule': [
                {
                    'id': 1,
                    'customer_name': 'שרה כהן',
                    'service': 'תספורת נשים',
                    'time': '09:00',
                    'phone': '050-9876543',
                    'status': 'confirmed'
                },
                {
                    'id': 2,
                    'customer_name': 'דוד לוי',
                    'service': 'תספורת גברים',
                    'time': '10:30',
                    'phone': '052-1234567',
                    'status': 'pending'
                },
                {
                    'id': 3,
                    'customer_name': 'רות מזרחי',
                    'service': 'צביעה',
                    'time': '14:00',
                    'phone': '054-5555555',
                    'status': 'confirmed'
                }
            ]
        }

    def _load_current_user(self):
        """Load the active user from the database, seeding defaults when needed."""
        user = self.db.get_user_by_email('yossi@example.com')
        if user:
            return user

        # Fallback seeding if the database was cleared after initialisation
        return self.db.create_user(
            name='יוסי לוי',
            email='yossi@example.com',
            phone='050-1234567',
            avatar='https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150',
            reliability=95,
            referral_code='YOSSI2025',
            referred_friends=3,
            is_business_owner=True,
            business_id=1,
            password='ChangeMe!2025'
        )

    def refresh_current_user(self):
        """Refresh current user data from the database before each request."""
        if not getattr(self, 'current_user_id', None):
            return

        user = self.db.get_user_by_id(self.current_user_id)
        if user:
            self.current_user = user

# יצירת מופע הנתונים והמסד
user_database = UserDatabase()
data = TorimData(user_database)


@app.before_request
def load_user_from_db():
    """Ensure the user information is always loaded from the database."""
    data.refresh_current_user()

# Routes (נתיבים)

@app.route('/')
def home():
    """דף הבית - המלצות"""
    return render_template('index.html', 
                         user=data.current_user,
                         recommendations=data.recommendations,
                         categories=data.categories,
                         appointments_count=len(data.appointments))

@app.route('/businesses')
def businesses():
    """דף העסקים"""
    category = request.args.get('category')
    if category:
        filtered_businesses = [b for b in data.businesses if b['category'] == category]
    else:
        filtered_businesses = data.businesses
    
    return render_template('businesses.html',
                         user=data.current_user,
                         businesses=filtered_businesses,
                         categories=data.categories,
                         selected_category=category,
                         appointments_count=len(data.appointments))

@app.route('/search')
def search():
    """דף החיפוש"""
    query = request.args.get('q', '')
    results = []
    
    if query:
        results = [b for b in data.businesses 
                  if query.lower() in b['name'].lower() 
                  or query.lower() in b['description'].lower()
                  or query.lower() in b['category'].lower()]
    
    return render_template('search.html',
                         user=data.current_user,
                         query=query,
                         results=results,
                         appointments_count=len(data.appointments))

@app.route('/profile')
def profile():
    """דף הפרופיל"""
    return render_template('profile.html',
                         user=data.current_user,
                         appointments_count=len(data.appointments))

@app.route('/my-appointments')
def my_appointments():
    """התורים שלי"""
    return render_template('my_appointments.html',
                         user=data.current_user,
                         appointments=data.appointments,
                         appointments_count=len(data.appointments))

@app.route('/appointment-history')
def appointment_history():
    """היסטוריית תורים"""
    return render_template('appointment_history.html',
                         user=data.current_user,
                         history=data.appointment_history,
                         appointments_count=len(data.appointments))

@app.route('/refer-friend')
def refer_friend():
    """הזמנת חברים"""
    return render_template('refer_friend.html',
                         user=data.current_user,
                         appointments_count=len(data.appointments))

@app.route('/ai-chat')
def ai_chat():
    """צ'אט AI"""
    return render_template('ai_chat.html',
                         user=data.current_user,
                         messages=data.chat_messages,
                         appointments_count=len(data.appointments))

@app.route('/account-settings')
def account_settings():
    """הגדרות חשבון"""
    return render_template('account_settings.html',
                         user=data.current_user,
                         appointments_count=len(data.appointments))

@app.route('/business-management')
def business_management():
    """ניהול עסק"""
    if not data.current_user['is_business_owner']:
        flash('אינך רשום כבעל עסק', 'error')
        return redirect(url_for('profile'))
    
    return render_template('business_management.html',
                         user=data.current_user,
                         dashboard=data.business_dashboard,
                         appointments_count=len(data.appointments))

# API Routes

@app.route('/api/book-appointment', methods=['POST'])
def api_book_appointment():
    """API להזמנת תור"""
    try:
        request_data = request.get_json(silent=True)
        if not isinstance(request_data, dict):
            return jsonify({'success': False, 'message': 'בקשה לא תקינה'}), 400

        business_id = request_data.get('business_id')
        service_id = request_data.get('service_id')
        date = request_data.get('date')
        time = request_data.get('time')

        if business_id is None or service_id is None or not date or not time:
            return jsonify({'success': False, 'message': 'חסרים פרטים להזמנה'}), 400
        
        # מציאת העסק והשירות
        business = next((b for b in data.businesses if b['id'] == business_id), None)
        if not business:
            return jsonify({'success': False, 'message': 'עסק לא נמצא'}), 404
        
        service = next((s for s in business['services'] if s['id'] == service_id), None)
        if not service:
            return jsonify({'success': False, 'message': 'שירות לא נמצא'}), 404
        
        # יצירת תור חדש
        new_appointment = {
            'id': len(data.appointments) + 1,
            'business_id': business_id,
            'business_name': business['name'],
            'business_image': business['image'],
            'service_name': service['name'],
            'date': date,
            'time': time,
            'status': 'confirmed',
            'address': business['address'],
            'phone': business['phone'],
            'price': service['price'],
            'can_cancel': True,
            'reminder': True
        }
        
        data.appointments.append(new_appointment)
        
        return jsonify({
            'success': True, 
            'message': 'התור נקבע בהצלחה! הפרטים מולאו אוטומטית',
            'appointment': new_appointment
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/cancel-appointment', methods=['POST'])
def api_cancel_appointment():
    """API לביטול תור"""
    try:
        request_data = request.get_json(silent=True)
        if not isinstance(request_data, dict):
            return jsonify({'success': False, 'message': 'בקשה לא תקינה'}), 400

        appointment_id = request_data.get('appointment_id')
        if appointment_id is None:
            return jsonify({'success': False, 'message': 'חסרים פרטי תור'}), 400
        
        # מציאת התור
        appointment_index = None
        for i, apt in enumerate(data.appointments):
            if apt['id'] == appointment_id:
                appointment_index = i
                break
        
        if appointment_index is None:
            return jsonify({'success': False, 'message': 'תור לא נמצא'}), 404
        
        # ביטול התור
        cancelled_appointment = data.appointments.pop(appointment_index)
        
        return jsonify({
            'success': True,
            'message': 'התור בוטל בהצלחה'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API לצ'אט AI"""
    try:
        request_data = request.get_json(silent=True)
        if not isinstance(request_data, dict):
            return jsonify({'success': False, 'message': 'בקשה לא תקינה'}), 400

        message = (request_data.get('message') or '').strip()
        if not message:
            return jsonify({'success': False, 'message': 'נא להזין הודעה'}), 400

        # הוספת הודעת המשתמש
        user_message = {
            'id': len(data.chat_messages) + 1,
            'type': 'user',
            'text': message,
            'time': datetime.now().strftime('%H:%M')
        }
        data.chat_messages.append(user_message)
        
        # יצירת תשובה אוטומטית
        ai_responses = [
            'תודה על השאלה! איך אוכל לעזור לך עוד?',
            'אני כאן לעזור! מה תרצה לדעת על הזמנת תורים?',
            'זה נשמע מעניין. האם תרצה שאמליץ על עסקים מתאימים?',
            'אוכל לעזור לך למצוא את העסק המושלם. מה אתה מחפש?',
            'מעולה! האם יש עוד משהו שאוכל לעזור לך?'
        ]
        
        import random
        ai_response = random.choice(ai_responses)
        
        ai_message = {
            'id': len(data.chat_messages) + 1,
            'type': 'assistant',
            'text': ai_response,
            'time': datetime.now().strftime('%H:%M')
        }
        data.chat_messages.append(ai_message)
        
        return jsonify({
            'success': True,
            'message': ai_message
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/get-business/<int:business_id>')
def api_get_business(business_id):
    """API לקבלת פרטי עסק"""
    business = next((b for b in data.businesses if b['id'] == business_id), None)
    if business:
        return jsonify(business)
    else:
        return jsonify({'error': 'עסק לא נמצא'}), 404

if __name__ == '__main__':
    # יצירת תיקיית templates אם לא קיימת
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    if not os.path.exists('static/css'):
        os.makedirs('static/css')
    if not os.path.exists('static/js'):
        os.makedirs('static/js')
    
    print("🚀 TORIM Flask App מתחיל...")
    print("📱 גש לכתובת: http://localhost:5000")
    print("✨ אפליקציית תורים בפייתון מוכנה!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
