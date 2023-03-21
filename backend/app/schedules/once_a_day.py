from app import scheduler
from app.models.item_in_use import ItemInUse
from app.schedules.email import send_equipment_notification


# что-то с темплейтом, не пишет ник
@scheduler.task('interval', id='check_taken_equipment_email',
                seconds=60 * 60 * 24)
def check_taken_equipment():
	with scheduler.app.app_context():
		items = ItemInUse.getAll()
		for item in items:
			user = item.user
			print(user.user_name)
			if item.is_notified == 0:
				send_equipment_notification(user, item.item.item_name,
				                            item.until_datetime)
				item.notify()
