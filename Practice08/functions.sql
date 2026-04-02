CREATE OR REPLACE FUNCTION search_by_pattern(p_pattern TEXT)
RETURNS TABLE (
    id INTEGER,
    name TEXT,
    phone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name, pb.phone
    FROM phonebook pb
    WHERE pb.name ILIKE '%' || p_pattern || '%'
       OR pb.phone ILIKE '%' || p_pattern || '%';
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE (
    id INTEGER,
    name TEXT,
    phone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name, pb.phone
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;