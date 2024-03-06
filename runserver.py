import os

def run_server():
    
    os.system('python manage.py runserver 0.0.0.0:8000')
    
if __name__ == "__main__":
        run_server()