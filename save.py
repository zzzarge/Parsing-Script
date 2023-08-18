import csv

def all_keys(*args):
    keys = []
    for d in args:
        keys.extend(d)
    keys = set(keys)
    return sorted(keys)


def write_to_txt(file_name, *args):
    file = open(file=f"{file_name}.txt", mode="w", encoding="utf-8")

    for number, post in enumerate(args, 1):
        text = f"""
            {number})   {post["title"]} - {post["dollar"]} / {post["som"]}
                        {post["address"]}
                        {post["description"]}
        {post["link"]}

            """
        file.write(text)
    file.close()


def write_to_csv(file_name, *args):
    fields = all_keys(*args)
    file = open(file=f"{file_name}.csv", mode="w", encoding="utf-8")

    writer = csv.DictWriter(f=file, fieldnames=fields)
    writer.writeheader()

    writer.writerows(args)

    file.close()


