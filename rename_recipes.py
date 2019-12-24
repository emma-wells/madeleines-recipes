import glob
import os
import shutil
import textwrap

import re


def _sentence_to_snake(s):
    return s.lower().replace(' ', '-')


def _parse_category(s):
    return s.lower().replace(' ', '-').replace('(', '').replace(')', '').replace(',', '').replace(
        '?', '').replace('.', '').replace("'", '').strip()


def _extract_name(content, name):
    first = content.splitlines()[0]
    if first.startswith('#') and not first[1:].startswith('#'):
        return first.split('#')[-1].strip()
    else:
        return name


def _tidy_content(c):
    new_c = c.replace('<br>', '\n').replace('</br>', '\n')

    _new_c = re.sub(r'\n(###)(?=[A-Za-z0-9])', '\n### ', new_c)
    if '###' in c:
        assert _new_c != new_c
    new_c = _new_c

    _new_c = re.sub(r'^(##)(?=[A-Za-z])', '## ', new_c)
    assert _new_c != new_c
    new_c = _new_c

    # _new_c = re.sub(r'^(#)(?=[A-Za-z])', '# ', new_c)
    # assert _new_c != new_c
    # new_c = _new_c

    return new_c


def main():
    txt_recipes = glob.glob("recipes/*/*/*.txt")
    md_recipes = glob.glob("recipes/*/*/*.md")
    recipes = txt_recipes + md_recipes

    for i, recipe_path in enumerate(recipes[::-1]):
        _, category, name, file_name = recipe_path.split('/')
        ext = 'txt' if file_name.endswith('txt') else 'md'
        new_category = _parse_category(category)
        categories = [category]
        new_file_name = "2019-12-22-" + new_category + '--' + _sentence_to_snake(file_name).replace(
            f".{ext}", '.markdown')
        new_image_name = 'assets/' + new_category + '/' + _sentence_to_snake(file_name).replace(
            f".{ext}", '.jpg')
        new_image_name2 = 'assets/' + new_category + '/' + _sentence_to_snake(file_name).replace(
            f".{ext}", ' 2.jpg')
        with open(recipe_path) as fp:
            content = fp.read()

        categories.extend(
            [f'From {cat}' for cat in [
                line.split('From', maxsplit=1)[1].lower().strip()
                for line in content.splitlines()
                if '##' in line and 'From' in line]
             if len(_parse_category(cat)) > 0
             ])
        print(categories)
        header = textwrap.dedent(f"""
        ---
        layout: recipe_post
        title:  "{name}"
        date:   2019-12-22 12:{i // 60:02}:{i % 60:02} +0000
        categories: {' '.join(_parse_category(c) for c in categories)}
        ---
        """).lstrip()
        print(category, name, new_file_name, file_name)

        print(header)
        extracted_name = _extract_name(content, name)
        new_content = header + "\n" + _tidy_content(content.replace(f'#{extracted_name}', '').lstrip())

        image_path = recipe_path.replace(f'.{ext}', '.jpg')
        has_image = os.path.isfile(image_path)
        if has_image:
            new_content += f'\n\n![](/{new_image_name})'
            os.makedirs(os.path.dirname(new_image_name), exist_ok=True)
            shutil.copyfile(image_path, new_image_name)
            print('IMAGE')

        image_path2 = recipe_path.replace(f'.{ext}', ' 2.jpg')
        if os.path.isfile(image_path2):
            new_content += f'\n\n![](/{new_image_name2})'
            os.makedirs(os.path.dirname(new_image_name2), exist_ok=True)
            shutil.copyfile(image_path2, new_image_name2)
            print('IMAGE2')

        if has_image or len(content.split('\n')) > 2:
            os.makedirs('_posts', exist_ok=True)
            with open(f'_posts/{new_file_name}', 'w') as fp:
                fp.write(new_content)
            for _category in categories:
                _new_category = _parse_category(_category)
                print(_category, repr(_new_category))
                with open(f'_category/{_new_category}.markdown', 'w') as fp:
                    fp.write(textwrap.dedent(f"""
                    ---
                    title: {_category}
                    tag: {_new_category}
                    permalink: "/category/{_new_category}"
                    ---
                    """).strip())

            # break
        else:
            pass
            # print("SHORT CONTENT")
            # print(content)


if __name__ == "__main__":
    main()
