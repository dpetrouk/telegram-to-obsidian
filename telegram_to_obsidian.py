import json
from os.path import join, isdir, isfile, dirname, abspath
from os import mkdir


PROJECT_DIR = '<...>/telegram-to-obsidian'
infile = join(PROJECT_DIR, 'data/result.json')

VAULT_DIR = '<...>/<vault name>'
# VAULT_DIR = join(PROJECT_DIR, 'test/main')
CHRONICS_DIR = join(VAULT_DIR, 'Chronics')

LINKS_NOTE_PREFIX = 'Notes from Teleground'


def format_text_by_type(ent):
    if ent['type'] in ['plain', 'link']:
        return ent['text']
    if ent['type'] == 'text_link':
        return f"[{ent['text']}]({ent['href']})"
    raise Exception(f"Unexpected type: {ent['type']}")

def get_post_text(text_entities):
    text = ''
    for ent in text_entities:
        text += format_text_by_type(ent)
    return text

def get_structured_text(text, dots_count = 0):
    if (separator := f"\n{'.' * dots_count}\n") in text or (separator := '\n') in text:
        head, *body = text.split(separator)
        result = {
            "head": get_structured_text(head, dots_count=dots_count + 1),
            "body": [get_structured_text(part, dots_count=dots_count + 1) for part in body]
        }
        return result
    else:
        return text.strip()

def add_indent(text, indent):
    i = "\t" * indent
    return f'{i}{text}'

def add_bullet(text):
    return f'- {text}'

def format_as_bullet(text, indent=0):
    return add_indent(add_bullet(text), indent=indent)

def format_structured_text(text, level=0):
    head = text['head']
    body = text['body']
    result = []
    if type(head) == str:
        result.append(format_as_bullet(head, indent=level))
    else:
        result.append(format_structured_text(head, level=level))
    for part in body:
        if type(part) == str:
            result.append(format_as_bullet(part, indent=level + 1))
        else:
            result.append(format_structured_text(part, level=level + 1))
    return '\n'.join(result)

def format_post_text(text):
    t = get_structured_text(text)
    if type(t) == str:
        return format_as_bullet(t)
    else:
        return format_structured_text(t)




def run():
    with open(infile, 'r') as f:
        telegram_posts = json.load(f)

    posts_by_dates = {}
    for post in telegram_posts['messages']:
        # Limit to add for testing: [:5]
        if post['type'] != 'message':
            print(f'Type is not message for {post["date"]} post: ', post)
        
        post_date = post['date'][:10]
        post_time = post['date'][11:]

        post_text = get_post_text(post['text_entities'])
        formatted_text = format_post_text(post_text)
        posts_by_dates.setdefault(post_date, []).append(formatted_text)

    # print(json.dumps(posts_by_dates, ensure_ascii=False, indent=4))

    dates = sorted(list(posts_by_dates.keys()))
    print(dates)

    for d in dates:
        lines = posts_by_dates[d]
        text = '\n\n' + '\n\n'.join(lines)

        year, month = d.split('-')[0:2]
        year_dir = join(CHRONICS_DIR, year)
        if not isdir(year_dir):
            print(f'Creating directory "{year_dir}"')
            mkdir(year_dir)

        month_dir = join(year_dir, month)
        if not isdir(month_dir):
            print(f'Creating directory "{month_dir}"')
            mkdir(month_dir)
        
        outfile = join(month_dir, f'{d}.md')
        if not isfile(outfile):
            print(f'Creating file "{outfile}"')
            with open(outfile, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print(f'Found already existing file {outfile}')
            with open(outfile, 'r', encoding='utf-8') as f:
            	current_text = f.read()
            if text in current_text:
                print('Notes are already there. Moving further')
                continue
            else:
                with open(outfile, "a") as f:
                    f.write(text)
    
    updated_notes_text = '\n' + '\n'.join([add_bullet(f'[ ] [[{d}]]') for d in dates])
    outfile = join(VAULT_DIR, f'{LINKS_NOTE_PREFIX} {dates[0]} - {dates[-1]}.md')
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(updated_notes_text)


run()

