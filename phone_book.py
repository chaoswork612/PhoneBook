from pprint import pprint
import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

def split_fio(list_):
  updated_contacts_list = []
  for contact in list_:
    result = " ".join(contact[:3]).split()
    if len(result) == 2:
      result.extend(contact[2:])
    else: result.extend(contact[3:])
    updated_contacts_list.append(result)
  return updated_contacts_list



def custom_merge_logic(existing_record, new_record):
  merged_record = existing_record[:]

  for i in range(3, len(existing_record)):
    val1 = existing_record[i]
    val2 = new_record[i]
    if val1 == '' and val2 != '':
      merged_record[i] = val2
  return merged_record


def format_phone_number(match_obj):
  if match_obj is None:
    return ""

  city_code = match_obj.group(1)
  part1 = match_obj.group(2)
  part2 = match_obj.group(3)
  part3 = match_obj.group(4)
  extension = match_obj.group(5)

  formatted_number = f"+7({city_code}){part1}-{part2}-{part3}"

  if extension:
    formatted_number += f" доб.{extension}"

  return formatted_number



def merge_and_compare_records(list_of_lists):
  phone_pattern = re.compile(
    r"^\+?[78]?\s?\(?(\d{1,3})\)?[\s\-]?(\d{1,3})[\s\-]?(\d{1,2})[\s\-]?(\d{1,2})(?:[\s\-]?(?:\(|\s)?доб\.\s?(\d{4})(?:\))?)?$",
    re.IGNORECASE | re.VERBOSE
  )

  merged_dict = {}
  for record in list_of_lists:
    key = tuple(record[:2])
    if key not in merged_dict:
      merged_dict[key] = record
    else:
      existing_record = merged_dict[key]
      merged_dict[key] = custom_merge_logic(existing_record, record)
  list_ = list(merged_dict.values())
  for record in list_:
    for r in record:
      match = phone_pattern.search(r)
      if match is not None:
        formatted_phone = format_phone_number(match)
        record[record.index(r)] = formatted_phone
  return list_

updated_contacts_list = split_fio(contacts_list)
merged_result_compared = merge_and_compare_records(updated_contacts_list)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(merged_result_compared)