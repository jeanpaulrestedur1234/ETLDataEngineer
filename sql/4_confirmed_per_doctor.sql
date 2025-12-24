-- 4. What is the total number of confirmed appointments for each doctor?
SELECT d.name, COUNT(a.id) as total_confirmed
FROM doctors d
    LEFT JOIN appointments a ON d.id = a.doctor_id
    AND a.status = 'confirmed'
GROUP BY
    d.name
ORDER BY total_confirmed DESC;