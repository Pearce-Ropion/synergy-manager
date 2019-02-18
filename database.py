import mysql.connector as mariadb
import config
import uuid as v4

def store_usage(data):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
	
	insert_variables = []
	channels = [None, None, None, None, None, None, None, None, None, None, None, None]
	
	try:
		uuid = data.get('uuid', '0')
		
		channel_uuids(uuid)
		
		time = data.get('epoch', 0)
		currents = data.get('channels', [])
	
		col_list = ['uuid', 'time', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']
	
		insert_variables.append(uuid)
		insert_variables.append(time)

		for i in range(len(currents)):
			channels[i] = currents[i]
		
		for channel in channels:
			insert_variables.append(channel)
			
		query_placeholders = ', '.join(['%s'] * len(insert_variables))
		query_columns = ', '.join(col_list)
		
		try:
			insert_query = ''' INSERT INTO usages (%s) VALUES (%s) ''' %(query_columns, query_placeholders)
			
			cursor.execute(insert_query, insert_variables)
			conn.commit()
			
			cursor.close()
			conn.close()
			
		except (mariadb.Error, mariadb.Warning) as e:
			print('Failing on SQL')
			print(e)
			return None
		
	except Exception as e:
		print(e)
		return None
		
		
def channel_uuids( device ):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	try:
		query = ''' SELECT id FROM devices WHERE uuid = %s '''
		cursor.execute(query, (device,))
		data = cursor.fetchall()
	except (mariadb.Error, mariadb.Warning) as e:
			print('Failing on SQL')
			print(e)
			return None
	if data:
		cursor.close()
		conn.close()
		return
	else:
		insert_variables = []
		col_list = ['uuid', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']
		
		insert_variables.append(device)
		for i in range(12):
			temp = v4.uuid4()
			cid = str(temp)
			insert_variables.append(cid)
		
		query_placeholders = ', '.join(['%s'] * len(insert_variables))
		query_columns = ', '.join(col_list)
		insert_query = ''' INSERT INTO devices (%s) VALUES (%s) ''' %(query_columns, query_placeholders)
			
		cursor.execute(insert_query, insert_variables)
		conn.commit()	
		cursor.close()
		conn.close()
		
def total_usage():
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
	col_list = ['time', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']
	query_columns = ', '.join(col_list)
	get_query = ''' SELECT (%s) FROM usages ''' %(query_columns)
	cursor.execute(get_query)
	result = cursor.fetchall()
	cursor.close()
	conn.close()
	return result
	
def device_usage(device_uuid):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
 	#name_query = ''' SELECT uuid FROM devices WHERE name = (%s) ''' %(device_name)
	col_list = ['time', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']
	query_columns = ', '.join(col_list)
	get_query = ''' SELECT (%s) FROM usages WHERE uuid = (%s) ''' %(query_columns, device_uuid)
	cursor.execute(get_query)
	result = cursor.fetchall()
	cursor.close()
	conn.close()
	return result
	
def ch_usage(ch_id):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
 	d_query = ''' SELECT deviceID FROM channels WHERE channelID = (%s) ''' %(ch_id)
 	cursor.execute(d_query);
 	device_uuid = cursor.fetchall();
 	query = ''' SELECT * FROM devices WHERE uuid = (%s) ''' %(device_uuid)
 	cursor.execute(d_query);
 	all_chs = cursor.fetchall();
 	indx = all_chs.index(ch_id)
 	col = "ch" + `indx-2`	
	get_query = ''' SELECT (%s) FROM usages WHERE uuid = (%s) ''' %(col, device_uuid)
	cursor.execute(get_query)
	result = cursor.fetchall()
	cursor.close()
	conn.close()
	return result
	
def get_ch_name(ch_id):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
	d_query = ''' SELECT name FROM channels WHERE channelID = (%s) ''' %(ch_id)
	cursor.execute(d_query);
 	name = cursor.fetchall();
 	cursor.close()
	conn.close()
	return name[0]

def get_device_name(device_id):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
	d_query = ''' SELECT name FROM devices WHERE uuid = (%s) ''' %(device)
	cursor.execute(d_query);
 	name = cursor.fetchall();
 	cursor.close()
	conn.close()
	return name[0]
 	
def set_ch_name(name, ch_id, device_id):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
	cols = ['deviceID', 'channelID', 'name']
	vals = [device_id, ch_id, name]
	query_placeholders = ', '.join(['%s'] * len(vals))
	query_columns = ', '.join(cols)
	insert_query = ''' INSERT INTO channels (%s) VALUES (%s) ON DUPLICATE KEY UPDATE name=(%s)''' %(query_columns, query_placeholders,name)
	cursor.execute(insert_query, vals); 	
	cursor.close()
	conn.close()
 
def set_device_name(name, device_id):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
	cols = ['deviceID', 'name']
	vals = [device_id, name]
	query_placeholders = ', '.join(['%s'] * len(vals))
	query_columns = ', '.join(cols)
	insert_query = ''' INSERT INTO devices (%s) VALUES (%s) ON DUPLICATE KEY UPDATE name=(%s)''' %(query_columns, query_placeholders,name)
	cursor.execute(insert_query, vals);
	cursor.close()
	conn.close()
	
def set_group_name(name, id):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
	cols = ['groupID', 'name']
	vals = [id, name]
	query_placeholders = ', '.join(['%s'] * len(vals))
	query_columns = ', '.join(cols)
	insert_query = ''' INSERT INTO groups (%s) VALUES (%s) ON DUPLICATE KEY UPDATE name=(%s)''' %(query_columns, query_placeholders,name)
	cursor.execute(insert_query, vals);
	cursor.close()
	conn.close()
	
def get_groupies(id):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
	g_query = ''' SELECT * FROM groupings WHERE groupID = (%s) ''' %(id)
	cursor.execute(g_query);
 	groupies = cursor.fetchall();
 	cursor.close()
	conn.close()
	return groupies
	
def add_to_group(group_id, uuid):
	conn = mariadb.connect(user=config.user, password=config.password, database=config.database)
	cursor = conn.cursor()
	cnx.autocommit = True
	cols = ['groupId', 'uuid']
	vals = [group_id, uuid]
	query_placeholders = ', '.join(['%s'] * len(vals))
	query_columns = ', '.join(cols)
	g_query = ''' INSERT INTO groupings (%s) VALUES (%s) ''' %(query_columns, query_placeholders)
	cursor.execute(g_query, vals);
 	groupies = cursor.fetchall();
 	cursor.close()
	conn.close()
	
def create_group(name):
	temp = v4.uuid4()
	id = str(temp)
	set_group_name(name, id);
	
 		