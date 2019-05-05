from twilio.rest import Client
from ..database.database import connectDB, closeDB
from ..reporter import reportError, isError

def get_phone():
    try:
        conn, cursor = connectDB()
        query = ''' SELECT phone FROM users'''
        cursor.execute(query)
        res = cursor.fetchall()
        return res[0]['phone']
    except Exception as error:
        reportError('SQL Error: Unable to retrieve channel name', error)
        closeDB(conn, cursor)

def unusual_msg(channel_name):
    # the following line needs your Twilio Account SID and Auth Token
    client = Client("AC3c8272cff870e2dc5e5ad9419ecad0a8",
                    "0d82fb7fe34ba36d7478c885816b663a")

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send SMS to any phone number
    phone = get_phone()
    client.messages.create(to=phone, #from account database
                        from_="+15623754577",
                        body="Unusual activity has been detected on " + channel_name + " based on previous activity at this time.\n - Synergy")


def reminder_msg(reminder):
    # the following line needs your Twilio Account SID and Auth Token
    client = Client("AC3c8272cff870e2dc5e5ad9419ecad0a8",
                    "0d82fb7fe34ba36d7478c885816b663a")

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send SMS to any phone number
    phone = get_phone()
    client.messages.create(to=phone,  # from account database
                           from_="+15623754577",
                           body= reminder + "\n- Synergy")
