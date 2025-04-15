-- docker exec -it postgres bash

-- Create function of trigger on table
CREATE OR REPLACE FUNCTION record_change_columns()
RETURNS TRIGGER AS $$
DECLARE change_details JSONB := '{}';
DECLARE modified_by TEXT := CURRENT_USER;
DECLARE modified_at TIMESTAMP := CURRENT_TIMESTAMP;
BEGIN
IF NEW.amount IS DISTINCT FROM OLD.amount THEN
change_details := jsonb_insert(change_details, '{amount}', jsonb_build_object('old', OLD.amount, 'new', NEW.amount));
END IF;
change_details := change_details || jsonb_build_object('modified_by', modified_by, 'modified_at', modified_at);
NEW.change_info = change_details;
NEW.modified_by = modified_by; NEW.modified_at = modified_at;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for table
CREATE TRIGGER trigger_record_change_columns
BEFORE UPDATE ON transactions
FOR EACH ROW EXECUTE FUNCTION record_change_columns();

-- Add column on table
ALTER TABLE transactions ADD COLUMN modified_by TEXT, modified_at TIMESTAMP, change_info JSONB;