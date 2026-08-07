import os
import tempfile
from bp_app.app import app
from bp_app.models import db, Patient

def test_registration_and_login():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Use an in-memory database for testing if possible, 
    # but the app.py hardcodes sqlite:///appointments.db.
    # To avoid messing with the real db, we can try to override it.
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # 1. Test Registration
            reg_data = {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'Password123'
            }
            response = client.post('/register', data=reg_data, follow_redirects=True)
            print(f"Registration status code: {response.status_code}")
            
            patient = Patient.query.filter_by(username='testuser').first()
            if patient:
                print(f"Patient created: {patient.username}, Email: {patient.email}")
                if patient.email == 'test@example.com':
                    print("Registration SUCCESS: Email saved correctly.")
                else:
                    print(f"Registration FAILURE: Email mismatch. Got {patient.email}")
            else:
                print("Registration FAILURE: Patient not found in DB.")
                return

            # 2. Test Login
            login_data = {
                'email': 'test@example.com',
                'password': 'Password123'
            }
            response = client.post('/login', data=login_data, follow_redirects=True)
            print(f"Login status code: {response.status_code}")
            
            if "You are now logged in." in response.get_data(as_text=True):
                print("Login SUCCESS: Found success flash message.")
            elif "dashboard" in response.request.path:
                print("Login SUCCESS: Redirected to dashboard.")
            else:
                print("Login FAILURE: Could not confirm login.")
                # print(response.get_data(as_text=True))

    os.close(db_fd)
    os.unlink(db_path)

if __name__ == "__main__":
    test_registration_and_login()
