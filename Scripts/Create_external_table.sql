create extension file_fdw2;
create server srv_file_fdw foreign data wrapper file_fdw2;


create foreign table public.url_for_check
(
	name VARCHAR(16),
	url VARCHAR(64)
)
server srv_file_fdw
options (filename '/www/get-api/ExternalTables/url_for_check.csv', format 'csv')
;

