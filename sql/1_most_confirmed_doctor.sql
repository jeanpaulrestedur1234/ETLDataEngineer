-- 1. Which doctor has the most confirmed appointments?
SELECT d.name, COUNT(a.id) as confirmed_appointments
FROM doctors d
    JOIN appointments a ON d.id = a.doctor_id
WHERE
    a.status = 'confirmed'
GROUP BY
    d.name
ORDER BY confirmed_appointments DESC
LIMIT 1;