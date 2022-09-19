-- Displays all entries for the different tables
SELECT * from user;

-- Creates database
CREATE TABLE user(
	user_ID TEXT PRIMARY KEY,
	pwd TEXT NOT NULL,
	ehyp_token TEXT NOT NULL UNIQUE,
	client_ID_qp TEXT NOT NULL UNIQUE,
	client_sec_qp TEXT NOT NULL UNIQUE,
	cons_ID_qp TEXT NOT NULL UNIQUE,
	client_ID_bfx TEXT NOT NULL UNIQUE,
	client_sec_bfx TEXT NOT NULL UNIQUE,
	cons_ID_bfx TEXT NOT NULL UNIQUE,
	region TEXT NOT NULL,
)

-- Enters Admin and Testuser to the database (Bereits in der __init__ über SQLAlchemy automatisiert)
INSERT INTO user(user_id, pwd, api1_id, api2_id, api3_id, region, credential_id, credential_pwd)
VALUES('admin', 'sha256$Sz9Wu8o7Ge4tRHJC$30ae8e1a88f1135961f114c72eae375110b99e56931e5c8f18635ba86b794a3a', 'no_api1_id', 'no_api2_id', 'no_api3_id', 'no_region', 'no_cred_id', 'no_cred_pwd'),
      ('mctestface', 'sha256$FBSLtR1LhzgIHur2$da1e1b0b9669b70c31f7ecfc2e8aefebbd279f9a895549324138179e295a2228', '123', '456', '789', 'testerstadt', '0', 'passwd');

-- Example for update password query
UPDATE user
SET pwd = 'pwd'
WHERE user_id = 'user_id';

-- Example for delete user query
DELETE FROM user
WHERE user_id = 'user_id';