import React, { useEffect, useState } from 'react';

function App() {
  const [bookings, setBookings] = useState([]);
  const [slot, setSlot] = useState('');
  const [user, setUser] = useState('');

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:8000/bookings/sse/');
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.event === 'new_booking') {
        // Add the new booking only if it’s not already in the list
        setBookings((prev) => {
          const exists = prev.some((b) => b.slot === data.slot);
          if (!exists) {
            return [...prev, { slot: data.slot, user: data.user }];
          }
          return prev;
        });
      }
    };

    eventSource.onerror = () => {
      console.error('SSE error');
      eventSource.close();
    };

    return () => eventSource.close();
  }, []);

  const handleBooking = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/bookings/book/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          slot: slot,
          user: user,
        }).toString(),
      });

      const result = await response.json();
      if (result.status === 'success') {
        // Add the booking to the list immediately
        setBookings((prev) => [
          ...prev,
          { slot: result.slot, user: user }, // Use the response slot (timezone-aware)
        ]);
        setSlot('');
        setUser('');
      } else {
        alert(result.message);
      }
    } catch (error) {
      console.error('Booking error:', error);
      alert('Failed to book slot');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Scheduling App</h1>
      <form onSubmit={handleBooking}>
        <input
          type="datetime-local"
          value={slot}
          onChange={(e) => setSlot(e.target.value)}
          required
        />
        <input
          type="text"
          value={user}
          onChange={(e) => setUser(e.target.value)}
          placeholder="Your name"
          required
        />
        <button type="submit">Book Slot</button>
      </form>
      <h2>Booked Slots</h2>
      <ul>
        {bookings.map((booking, index) => (
          <li key={index}>
            {booking.user} booked {new Date(booking.slot).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
