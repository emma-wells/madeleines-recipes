import glob
import textwrap

import re


def _sentence_to_snake(s):
    return s.lower().replace(' ', '-')


def _tidy_content(c):
    new_c = c.replace('<br>', '\n').replace('</br>', '\n')
    new_c = re.sub(r'\n(###)(?=[A-Z])', '\n### ', new_c)
    new_c = re.sub(r'^(##)(?=[A-Z])', '## ', new_c)
    new_c = re.sub(r'^(#)(?=[A-Z])', '# ', new_c)

    return new_c


def main():
    recipes = glob.glob("recipes/*/*/*.txt")

    for i, recipe_path in enumerate(recipes[::-1]):
        _, category, name, file_name = recipe_path.split('/')
        new_file_name = "2019-12-22-" + _sentence_to_snake(file_name).replace(".txt", '.markdown')

        with open(recipe_path) as fp:
            content = fp.read()

        header = textwrap.dedent(f"""
        ---
        layout: post
        title:  "{name}"
        date:   2019-12-22 12:{i // 60:02}:{i % 60:02} +0000
        categories: {_sentence_to_snake(category)}
        ---
        """).lstrip()
        print(category, name, new_file_name, file_name)

        print(header)
        new_content = header + "\n" + _tidy_content(content.replace(f'#{name}\n', ''))

        with open(f'_posts/{new_file_name}', 'w') as fp:
            fp.write(new_content)


if __name__ == "__main__":
    main()
