from app.api.moex.moex import MOEX
from app.api.smart_lab.smart_lab import SmartLab
from app.builders.message_builder import Message

from app.helpers.dates import today_str

moex = MOEX()
indexes = moex.parser.moex_indexes()

indexes = moex.parser.indexes_changes(indexes)
s = moex.parser.today_prices()

message = Message.indexes_to_text(indexes)
print('\n'.join(message))
message_calendar = Message.calendar_minus_energy(indexes)
print(message_calendar)
message_reports = Message.reports(SmartLab().parser.reports())
print(message_reports)
file_output = open("_info/{}.txt".format(today_str()), 'w')
file_output.write('\n'.join(message))
file_output.write('\n'+message_calendar)
file_output.write('\n\n'+message_reports)
file_output.close()