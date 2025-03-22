from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
from .models import Booking
from django.utils import timezone  # Import timezone utilities
from datetime import datetime

def sse_events(request):
    def event_stream():
        last_id = Booking.objects.latest('id').id if Booking.objects.exists() else 0
        while True:
            latest_bookings = Booking.objects.filter(id__gt=last_id)
            if latest_bookings.exists():
                for booking in latest_bookings:
                    data = {
                        "event": "new_booking",
                        "slot": booking.slot.isoformat(),
                        "user": booking.user,
                    }
                    yield f"data: {json.dumps(data)}\n\n"
                last_id = latest_bookings.latest('id').id
            time.sleep(1)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    response['Access-Control-Allow-Origin'] = '*'  # Explicitly allow all origins
    return response

@csrf_exempt
def create_booking(request):
    if request.method == "POST":
        slot_str = request.POST.get("slot")  # e.g., "2025-03-22T23:05:00"
        user = request.POST.get("user")

        if not slot_str or not user:
            return JsonResponse({"status": "error", "message": "Missing slot or user"}, status=400)

        try:
            # Convert naive datetime string to timezone-aware datetime
            naive_slot = datetime.fromisoformat(slot_str.replace("T", " "))
            aware_slot = timezone.make_aware(naive_slot, timezone.get_current_timezone())

            booking = Booking.objects.create(slot=aware_slot, user=user)
            return JsonResponse({"status": "success", "slot": booking.slot.isoformat()})
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid datetime format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Slot already taken or error: {str(e)}"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
