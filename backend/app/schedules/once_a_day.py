# что-то с темплейтом, не пишет ник
# @scheduler.task('interval', id='check_taken_equipment_email',
#                 seconds=60 * 60000000 * 24)
# def check_taken_equipment():
# 	with scheduler.app.app_context():
# 		items = ItemInUse.getAll()
# 		for item in items:
# 			user = item.user
# 			print(user.user_name)
# 			if item.is_notified == 0:
# 				send_equipment_notification(user, item.item.item_name,
# 				                            item.until_datetime)
# 				item.notify()
# @scheduler.task('interval', id='check_taken_equipment_email',
#                 seconds=5)
# def do_backup():
# 	# pass тут это from sh import pg_dump или так
# 	with scheduler.app.app_context():
# 		import gzip
# 		with gzip.open('last-backup.gz', 'wb') as f:
# 			c = delegator.run('pg_dump - h localhost - U postgres stock')
# 			# print(1)
# 			f.write(c.out.encode('utf - 8'))
