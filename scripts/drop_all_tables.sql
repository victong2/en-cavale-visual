-- Usage: psql -h localhost -U postgres -d postgres -a -f scripts/drop_all_tables.sql

DO $$ 
BEGIN
    -- Generate and execute drop commands for all tables
    DECLARE
        table_record RECORD;
    BEGIN
        FOR table_record IN
            SELECT tablename FROM pg_tables WHERE schemaname = 'public'
        LOOP
            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(table_record.tablename) || ' CASCADE';
        END LOOP;
    END;
END $$;