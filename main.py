from app.api.moex.moex import MOEX
from app.builders.message_builder import Message

moex = MOEX()
indexes = moex.parser.moex_indexes()

indexes = moex.parser.indexes_changes(indexes)
s = moex.parser.today_prices()

message = Message.indexes_to_text(indexes)
print('\n'.join(message))
file_output = open('out.txt', 'w')
file_output.write('\n'.join(message))
file_output.close()