CREATE TABLE IF NOT EXISTS PhoneBook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE
);

CREATE OR REPLACE FUNCTION search_phonebook(pattern VARCHAR)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone
    FROM PhoneBook p
    WHERE p.name ILIKE '%' || pattern || '%'
       OR p.phone LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE upsert_user(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM PhoneBook WHERE phone = p_phone) THEN
        UPDATE PhoneBook SET name = p_name WHERE phone = p_phone;
    ELSE
        INSERT INTO PhoneBook (name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION is_valid_phone(phone VARCHAR)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN phone ~ '^[0-9+()-]{6,20}$';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_multiple_users(
    IN names VARCHAR[],
    IN phones VARCHAR[],
    OUT invalid_records TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    invalid_count INTEGER := 0;
BEGIN
    invalid_records := ARRAY[]::TEXT[];
    
    IF array_length(names, 1) != array_length(phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;
    
    FOR i IN 1..array_length(names, 1) LOOP
        IF NOT is_valid_phone(phones[i]) THEN
            invalid_count := invalid_count + 1;
            invalid_records[invalid_count] := names[i] || ':' || phones[i];
        ELSE
            CALL upsert_user(names[i], phones[i]);
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE FUNCTION get_phonebook_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    phone VARCHAR,
    total_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.name,
        p.phone,
        (SELECT COUNT(*) FROM PhoneBook) as total_count
    FROM PhoneBook p
    ORDER BY p.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_phonebook_record(
    p_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_name IS NOT NULL AND p_phone IS NOT NULL THEN
        DELETE FROM PhoneBook WHERE name = p_name AND phone = p_phone;
    ELSIF p_name IS NOT NULL THEN
        DELETE FROM PhoneBook WHERE name = p_name;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM PhoneBook WHERE phone = p_phone;
    ELSE
        RAISE EXCEPTION 'Either name or phone must be provided';
    END IF;
END;
$$; 