-- 2. How many confirmed appointments does the patient with patient_id '34' have?
SELECT COUNT(id) as patient_34_confirmed_count
FROM appointments
WHERE
    patient_id = 34
    AND status = 'confirmed';