-- 3. How many cancelled appointments are there between October 21, 2025, and October 24, 2025 (inclusive)?
SELECT COUNT(id) as cancelled_count
FROM appointments
WHERE
    status = 'cancelled'
    AND booking_date >= '2025-10-21 00:00:00'
    AND booking_date <= '2025-10-24 23:59:59';