CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_users(p_names TEXT[], p_phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
BEGIN
    IF array_length(p_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have same length';
    END IF;

    CREATE TEMP TABLE IF NOT EXISTS invalid_data (
        name TEXT,
        phone TEXT
    ) ON COMMIT DROP;

    DELETE FROM invalid_data;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9+\-() ]{7,20}$' THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_names[i]) THEN
                UPDATE phonebook
                SET phone = p_phones[i]
                WHERE name = p_names[i];
            ELSE
                INSERT INTO phonebook(name, phone)
                VALUES (p_names[i], p_phones[i]);
            END IF;
        ELSE
            INSERT INTO invalid_data(name, phone)
            VALUES (p_names[i], p_phones[i]);
        END IF;
    END LOOP;

    RAISE NOTICE 'Incorrect data:';
    FOR i IN 1..(SELECT COUNT(*) FROM invalid_data) LOOP
        NULL;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR phone = p_value;
END;
$$;