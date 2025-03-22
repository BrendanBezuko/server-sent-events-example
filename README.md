Thius is a very simple app to demonstrate how server sent events (instead of websockets) can work to notify multiple fronts of an update such as a booking. The use case can solve issues like double booking

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
## cURL
to check if the backend is working correctly:
```
curl -X POST http://localhost:8000/bookings/book/ \
  -d "slot=2025-03-22T15:05:00&user=john_doe" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

## Database
```
sqlite3 db.sqlite3
.tables
```
