import sqlite3
from sqlite3 import Error



def create_cur_conn(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        print(sqlite3.version)
        return cur, conn
    except Error as e:
        print(e)



def run_query(cur, query):
	try:
		data = cur.execute(query)
		return data
	except Error as e:
		print("There was a problem with the query:")
		print(query)
		print(e)
		raise(e)



def csvfile(file='MedianHouseholdIncome2015.csv', header=True):
	print("reading csv")
	csvfile = open(file, encoding='latin1')
	reader = csv.reader(csvfile)
	if header:
		next(reader, None)
	return csvfile, reader



def load_data(cur, table_name, 
	file='MedianHouseholdIncome2015.csv',
	table_def="area string, city string, median_income integer"):
	"""table_def in the format "area string, city string, median_income integer" """

	print("Cleaning up the db.")
	q = f"""drop table if exists {table_name}"""
	run_query(cur, q)
	#query_iterator(cur, q)

	print(f"Creating table {table_name}.")
	q = f"""create table {table_name}
			({table_def})"""
	run_query(cur, q)

	print("Loading csv data to new db table.")
	csv, reader = csvfile(file)
	
	num_cols = len(table_def.split(','))
	q = f'''insert into {table_name} values ({','.join('?' * num_cols)})'''
	for row in reader:
		cur.execute(q, row)
	print("Done!")

	csv.close()



def test_new_table(cur, rows_to_print, table_name):
	q = f"""select * from {table_name} limit {rows_to_print}"""
	data = run_query(cur, q)
	for row in data:
		print(row)




if __name__ == '__main__':
	import csv

	# Connect or create db.
	db_file = '/Users/tanya/Desktop/test.db'
	cur, conn = create_cur_conn(db_file)

	# Load data tables from csvs.
	load_data(cur, 'income')
	conn.commit()

	load_data(cur, 'poverty_level', 
	file='PercentagePeopleBelowPovertyLevel.csv',
	table_def="state string, city string, poverty_rate numeric")
	conn.commit()


	load_data(cur, 'edu_level', 
	file='PercentOver25CompletedHighSchool.csv',
	table_def="state string, city string, percent_completed_hs numeric")
	conn.commit()

	load_data(cur, 'killings', 
	file='PoliceKillingsUS.csv',
	table_def="""id integer, name string, date datetime, manner_of_death string, armed string,
	age integer, gender string, race string, city string, state string, 
	signs_of_mental_illness string, threat_level string, flee string, body_camera string""")
	conn.commit()

	load_data(cur, 'race_share', 
	file='ShareRaceByCity.csv',
	table_def="""state string, city string, share_white numeric, share_black numeric, 
	share_native numeric, share_asian numeric, share_hispanic numeric""")
	conn.commit()

	# Add a table.
	q = "drop table if exists combo_demographics;"
	run_query(cur, q)

	q = """create table combo_demographics as 
	select p.state, p.city, 
	p.poverty_rate, e.percent_completed_hs, 
	r.share_white, r.share_black, r.share_native, r.share_asian, r.share_hispanic
	from poverty_level p
	join edu_level e
	on p.state = e.state and p.city = e.city
	join race_share r
	on p.state = r.state and p.city = r.city
	order by 1,2;"""
	run_query(cur, q)



	# Test that the load worked.
	print('income:')
	test_new_table(cur, 10, 'income')
	print('poverty_level:')
	test_new_table(cur, 10, 'poverty_level')
	print('edu_level:')
	test_new_table(cur, 10, 'edu_level')
	print('killings:')
	test_new_table(cur, 10, 'killings')
	print('race_share:')
	test_new_table(cur, 10, 'race_share')
	print('combo table:')
	test_new_table(cur, 10, 'combo_demographics')

	conn.close()






