import re


named_regex = '(?P<{name}>{regex})'
dep_start_tag = 'dep.start'
comment_regex = '#|//'
word_regex = '[a-z.]*'
whitespaces_regex = '[ |\\t]*'
multiple_words_regex = '(({0}{1})*)'.format(whitespaces_regex, word_regex)

match_dependency_start_regex_string = '{comment_wildcard}{start_tag}{WS}{name}{WS}{compiler_name}{WS}{compiler_params}'
match_dependency_start_regex_params = {
    'comment_wildcard' : named_regex.format(name='comment', regex=comment_regex),
    'WS': whitespaces_regex,
    'start_tag': dep_start_tag,
    'name': named_regex.format(name='name', regex= word_regex),
    'compiler_name': named_regex.format(name='compiler_name', regex=word_regex),
    'compiler_params': named_regex.format(name='compiler_arguments', regex=multiple_words_regex)
}

print(match_dependency_start_regex_string.format(**match_dependency_start_regex_params))
match_dependency = re.compile(match_dependency_start_regex_string.format(**match_dependency_start_regex_params))
test = '''


#dep.start
gast diagram.swag class asd asd



#dep.end gast
'''


result = match_dependency.finditer(test)


for i in result:
    print(i.groupdict())
# print(result)
#
for line in test.splitlines(keepends=True):
    match = match_dependency.match(line)
    if match:
        dependency_start = match.groupdict()
        dependency_start['compiler_arguments'] = [i.strip() for i in dependency_start['compiler_arguments'].split() if len(i.strip()) != 0]
        # print(dependency_start)


