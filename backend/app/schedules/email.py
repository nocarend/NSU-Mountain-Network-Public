from flask import current_app, render_template
from flask_mail import Message

from app import mail
from app.helpers.email_default import send_email


def send_equipment_notification(user, item, date):
	send_email('[NSU] Notification',
	           sender=current_app.config['ADMINS'][0],
	           recipients=[user.user_email],
	           text_body=render_template('email/equipment_notification.txt',
	                                     user=user.user_name, item=item,
	                                     date=date),
	           html_body=render_template('email/equipment_notification.html',
	                                     user=user.user_name, item=item,
	                                     date=date))


def send_backup():
	message = Message('Bk', sender=current_app.config['ADMINS'][0],
	               recipients=current_app.config['ADMINS'][0])
	with open('last-backup.gz', 'rb') as f:
		message.attach(filename='last-backup.gz', data=f.read())
	mail.send(message)
