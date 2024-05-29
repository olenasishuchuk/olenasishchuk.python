import bcrypt

USER_SCHEME = ("id", "first_name", "second_name", "email", "password")
RECORD_SCHEME = ("id", "date", "content", "user", "title")
ENTITIES = ('User', 'Record')

users = [
    "User(id=1, first_name=test name, second_name=test surname, email=test@test.test, password=123)",
    "User(id=2, first_name=another test name, second_name=another test surname, email=test1@test.test, password=456)",
    "User(id=3, first_name=test name x1, second_name=test surname x2, email=test123@test.test)",
    "User(id=4, first_name=, second_name=test surname x3, email=train@test.test)",
         ]

records = [
    "Record(id=1, date=26.02.2004, content=Some example #1, user=1, title=Example title)",
    "Record(id=2, date=01.10.2013, content=Some example #2, user=3, title=Example title one)",
    "Record(id=3, date=12.13.2008, content=Some example #3, user=2, title=Example title of user 2)"
]

def _get_entity(s: str) -> str:
  """Gets named entity ('User' or 'Record') from string.

  Args:
    s(str): string with User or Record entity.

  Returns:
    string: extracted entity.
  """
  # print(s)
  if ENTITIES[0] in s:
    return ENTITIES[0]
  elif ENTITIES[1] in s:
    return ENTITIES[1]
  else:
    return ""

# for user in users:
#   _get_entity(user)

# for record in records:
#   _get_entity(record)

def _get_entity_item(item: str, string: str) -> str:
  # print("Found!")
  idx = string.index(item + "=")
  # print(f"Index of first character of {item + '='} is {idx}")
  search_index = idx + len(item + '=')
  # print(f"Index of the last character of {item + '='} is {search_index}")
  # search from
  i = search_index
  sub_string = ""
  while string[i] != ',' and string[i] != ')':
    sub_string += string[i]
    i += 1
  return sub_string
  
def parse_string(string: str) -> dict:
  """Each of functions below should parse input string.
  Function must identify entety: record or user.
  Implement function to parse standard input string based on example:

  record: "Record(id=1, date=26.02.2004, content=Some example,
                   user=1, title=Example title)"
  user:    "User(id=1, first_name=test name, second_name=test surname,
                 email=test@test.test, password=123)"
  Args:
    string (str): represents entity like examples.

  Return:
    dict: {'record': {"id": 1, "date": datetime.datetime, 'content':
                      'Some example',"user": 1, 'title': "Example title"}}
          or
          {'user': {"id": 1, 'first_name': 'test_name', ...,
                    "password": hash(password)}}

  """
  entity = _get_entity(s=string)

  dist = {}

  if entity == ENTITIES[0]:
    for item in USER_SCHEME:
      if item + "=" in string:
        dist[item] = _get_entity_item(item, string)
    return { 'user': dist }
  elif entity == ENTITIES[1]:
    for item in RECORD_SCHEME:
      if item + "=" in string:
        dist[item] = _get_entity_item(item, string)
    return { 'record': dist }
  else:
    return {}

  
def create_record(record: str) -> dict:
  """
  Performs creation operation. Input: string with record. Output: parsed string
  converted into dict (json).

  Args:
    record (str): "Record(id=1, date=26.02.2004, content=Some example,
                   user=1, 'title'=Example title)"
  Returns:
    dict: record = {"id": 1, "date": datetime.datetime, 'content': 'Some example',
                    "user": 1, 'title': "Example title"}

  # parse string and get record in dict, record = ...
  # DATABASE.append(record)

  """

  # replace with record
  return dict(parse_string(record))['record']

def create_user(user: str) -> dict:
  """
  Performs creation operation. Input: string with record. Output: parsed string
  converted into dict (json).

  Args:
    user (str): "User(id=1, first_name=test name, second_name=test surname,
                 email=test@test.test, password=123)"
  Returns:
    None

  dict: user = {"id": 1, 'first_name': 'test_name', ...,
                  "poassword": hash(password) }
  DATABASE.append(dict)

  """

  created_user = dict(parse_string(user))['user']

  if 'password' in created_user:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(created_user['password'].encode('utf-8'), salt)
    created_user['password'] = hashed
  
  # replace with user
  return created_user

# Password hashing: https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/
  
def update_record(record: str) -> dict:
  """
  Performs update operation. Input: string with record. Output: parsed string
  converted into dict (json).

  Args:
    record (str): "Record(id=1, date=24.02.2004, content=Some example,
                   user=1, 'title'=Example title)"
  Returns:
    dict: record = {"id": 1, "date": datetime.datetime, 'content': 'Some example',
                    "user": 1, 'title': "Example title"}

  """

  id = _get_entity_item('id', record)

  result = None

  for idx, item in enumerate(DATABASE):
    if item['id'] == id and 'content' in item:
      result = create_record(record)
      DATABASE[idx] = result

  return result


def update_user(user: str) -> dict:
  id = _get_entity_item('id', user)

  result = None

  for idx, item in enumerate(DATABASE):
    if item['id'] == id and 'content' not in item:
      result = create_user(user)
      DATABASE[idx] = result

  return result

def read_record(record_content: str) -> dict:
  """
  Returns record by given content. Search DATABASE, find and return record.

  Args:
    record_content (string): record content.

  Returns:
    dict: record = {"id": 1, "date": datetime.datetime, 'content': 'Some example',
                    "user": 1, 'title': "Example title"}

  """

  for item in DATABASE:
    if 'content' in item:
      if item['content'] == record_content:
        return item

def delete_record(record_id: int) -> dict:
  """
  removes record by given id. Search DATABASE, find and delete record by id from
          DATABASE.

  Args:
    record_id (int): record id.

  Returns:
    dict: record = {"id": 1, "date": datetime.datetime, 'content': 'Some example',
                    "user": 1, 'title': "Example title"}

  """

  for idx, item in enumerate(DATABASE):
    if 'content' in item:
      if item['id'] == record_id:
        DATABASE.pop(idx)

DATABASE = list()

for user in users:
  DATABASE.append(create_user(user))

for record in records:
  DATABASE.append(create_record(record))

user_1 = "User(id=1, first_name=test name, second_name=test surname, email=test@test.test, password=123)"
record_1 = "Record(id=1, date=26.02.2005, content=Some example, user=1, title=Example title)"

print('Initial DATABASE')
print(*DATABASE, sep='\n')

update_user(user_1)
update_record(record_1)

print('\nUpdated DATABASE')
print(*DATABASE, sep='\n')

print('\nRead record')
print(read_record('Some example'))

delete_record('2')

print("\nDelete record")
print(*DATABASE, sep='\n')

"""parse(record) -> dict: dict_record
  if check DATABASE if dict_record already exists == True:
    return
  else:
    DATABASE.append(dict_record)
"""