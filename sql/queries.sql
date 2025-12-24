-- 1. Which doctor has the most confirmed appointments?
SELECT d.name, COUNT(a.booking_id) as confirmed_appointments
FROM doctors d
    JOIN appointments a ON d.doctor_id = a.doctor_id
WHERE
    a.status = 'confirmed'
GROUP BY
    d.name
ORDER BY confirmed_appointments DESC
LIMIT 1;

-- 2. How many confirmed appointments does the patient with patient_id '34' have?
SELECT COUNT(booking_id) as patient_34_confirmed_count
FROM appointments
WHERE
    patient_id = 34
    AND status = 'confirmed';

-- 3. How many cancelled appointments are there between October 21, 2025, and October 24, 2025 (inclusive)?
SELECT COUNT(booking_id) as cancelled_count
FROM appointments
WHERE
    status = 'cancelled'
    AND booking_date >= '2025-10-21 00:00:00'
    AND booking_date <= '2025-10-24 23:59:59';

-- 4. What is the total number of confirmed appointments for each doctor?
SELECT d.name, COUNT(a.booking_id) as total_confirmed
FROM doctors d
    LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
    AND a.status = 'confirmed'
GROUP BY
    d.name
ORDER BY total_confirmed DESC;