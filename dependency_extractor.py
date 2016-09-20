import re

test = '''

#dep.start gast diagram.swa asd asd

gozer

kerel

#dep.end gast
'''


def find_dependencies(source):

    ##GET START
    named_regex = '(?P<{name}>{regex})'
    dep_start_tag = 'dep.start'
    comment_regex = '#|//'
    word_regex = '[a-z.]*'
    whitespaces_regex = '[ |\\t]+'
    multiple_words_regex = '({0}{1})*'.format(whitespaces_regex, word_regex)

    match_dependency_start_regex_string = '{comment_wildcard}{start_tag}{WS}{name}{WS}{compiler_name}{compiler_args}'
    match_dependency_start_regex_params = {
        'comment_wildcard': named_regex.format(name='comment_wildcard', regex=comment_regex),
        'WS': whitespaces_regex,
        'start_tag': dep_start_tag,
        'name': named_regex.format(name='name', regex=word_regex),
        'compiler_name': named_regex.format(name='compiler_name', regex=word_regex),
        'compiler_args': named_regex.format(name='compiler_args', regex=multiple_words_regex)
    }

    match_dependency_start = re.compile(match_dependency_start_regex_string.format(**match_dependency_start_regex_params))

    #get dependencies
    dep_end_tag = 'dep.end'

    match_dependency_end_regex_string = '{comment_wildcard}{end_tag}{WS}{name}[ |\\t]*$'

    def get_line_number(the_match):
        return source.count("\n", 0, the_match.start()) + 1

    #loop over start matches and get the corresponding end match
    #then create dependency
    dependencies = []
    for start_match in match_dependency_start.finditer(source):
        line_start = get_line_number(start_match)
        match_props = start_match.groupdict()
        name = match_props['name']
        comment_wildcard = match_props['comment_wildcard']

        match_dependency_end_regex_params = {
            'comment_wildcard': comment_wildcard,
            'end_tag': dep_end_tag,
            'WS': whitespaces_regex,
            'name': named_regex.format(name='name', regex=word_regex)
        }
        match_dependency_end = list(re.finditer(match_dependency_end_regex_string.format(**match_dependency_end_regex_params), source))

        if len(match_dependency_end) ==0:
            #No end tag found for dependency section
            print('No end tag found for dependency: {0}'.format(name))
        if len(match_dependency_end) >1:
            #More than one end tag found for dependency section
            print('More than one end tag found for dependency: {0}'.format(name))
        assert  len(match_dependency_end) == 1
        end_match = match_dependency_end[0]
        line_end = get_line_number(end_match)

        dependency = Dependency.from_line_indexes(line_start, line_end, name, source, match_props['compiler_name'], match_props['compiler_args'])
        dependencies.append(dependency)


    return dependencies


class Source():
    def __init__(self, text, path):
        self.text = text
        self.path = path


    def lines(self):
        return self.text.splitlines(keepends=True)




class Dependency():


    def __str__(self):
        return self.source

    @classmethod
    def from_line_indexes(cls, start_index, end_index, name, source, compiler_name, compiler_args):
        dependency_source = ''.join(source.splitlines(keepends=True)[start_index:end_index-1])
        return cls(name=name, original_source=source, source=dependency_source,
                       compiler_name=compiler_name, compiler_args=compiler_args)


    def __init__(self, name, original_source, source, compiler_name, compiler_args):
        self.name = name
        self.original_source = original_source
        self.compiler_name = compiler_name
        self.compiler_args = compiler_args
        self.source = source


dependencies = find_dependencies(test)
