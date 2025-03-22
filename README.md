# Setup and Run Commands

## Backend
```cd backend
python -m venv .
source bin/activate  # On Windows: bin\Activate.ps1
pip install django django-cors-headers
python scheduler/manage.py makemigrations bookings
python scheduler/manage.py migrate
python scheduler/manage.py runserver
```

## Frontend
```
cd frontend
npm install
npm run dev
npm run dev # to see changes on a different front you need two instances
```
