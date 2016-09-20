import re

class SectionManager():
    @classmethod
    def _parse_sections_indexes(cls, source, section_start_regex, section_end_regex):
        sections = {}
        lines = source.splitlines(keepends=True)

        start_identifier = section_identifier_config.START.COMMENT_TAG + section_identifier_config.START.TAG_NAME
        end_identifier = section_identifier_config.END.COMMENT_TAG + section_identifier_config.END.TAG_NAME

        for index, line in enumerate(lines):

            if len(line.split()) == 0:
                continue
            else:
                first_word = line.split()[0].strip()

            if first_word.lower() == start_identifier.lower():
                section_name = line.split()[1].strip()
                if section_name not in sections:
                    # this is the first match,
                    sections[section_name] = {'start': index+1}

                else:
                    # this may be and end tag if no end tag is  specified
                    if 'end' in sections[section_name]:
                        # TODO
                        print('MULTIPLE START TAGS')
                        print('two sections with the same name??')
                    else:
                        sections[section_name]['end'] = index
                continue

            if first_word.lower() == end_identifier.lower():

                section_name = line.split(end_identifier)[1].strip()

                if section_name not in sections:
                    print('END TAG BEFORE START TAG')
                    # TODO
                else:
                    if 'end' in sections[section_name]:
                        print('MULTIPLE END TAGS')
                        # TODO
                    sections[section_name]['end'] = index

        return sections

    @staticmethod
    def _extract_section(source, start, end):
        if isinstance(source, list):
            lines = source
        else:
            lines = source.splitlines(keepends=True)

        section_source = ''.join(lines[start:end])
        return section_source


    @classmethod
    def _parse_sections(cls, source, parse_config):
        # if parse_config is None:
        #     parse_config = RegionIdentifiers.DEFAULT.PYTHON

        #section = source, section info DICT

        sections_with_indexes = cls._parse_sections_indexes(source, parse_config)
        corrupt_sections = {k: v for k, v in sections_with_indexes.items() if 'end' not in v or 'start' not in v}

        if corrupt_sections:
            print('CORRUPT_SECTIONS ENDS FOR SECTIONS: ', corrupt_sections)
            raise Exception('corrupt sections')

        parsed_sections = {}
        for section_name, section_info in sections_with_indexes.items():
            extracted_source = cls._extract_section(source, **section_info)
            parsed_sections[section_name] = dict(source=extracted_source, section_info=section_info)
        return parsed_sections



