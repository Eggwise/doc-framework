import collections
from collections import namedtuple

class Struct():
    @classmethod
    def _build_from_locals(cls, classmethod_params):
        struct = classmethod_params['cls']()
        del classmethod_params['cls']
        for k, v in classmethod_params.items():
            # if k == 'cls':
            #     continue
            # print(k , v)
            setattr(struct, k, v)
        return struct


class RegionConfig(Struct):
    START, END = [None, None]

    @classmethod
    def build(cls, START, END):
        return cls._build_from_locals(locals())


class TagConfig(Struct):
    TAG_NAME, COMMENT_TAG = [None, None]

    def create_start_identifier(self):
        return self.COMMENT_TAG + self.TAG_NAME

    @classmethod
    def build(cls, TAG_NAME, COMMENT_TAG):
        return cls._build_from_locals(locals())



PYTHON_COMMENT_TAG = '#'
OTHER_LANG_COMMENT_TAG = '//'
EMPTY_COMMENT_TAG = ''

END_REGION_TAG_NAME = 'endregion'
REGION_TAG_NAME = 'region'
INJECTABLE_TAG_NAME = 'injectable'
INJECT_TAG_NAME = 'inject'

class ParseTags():

    class REGION_START():
        PYTHON = TagConfig.build(REGION_TAG_NAME, PYTHON_COMMENT_TAG) # type: TagConfig

    class REGION_END():
        PYTHON = TagConfig.build(END_REGION_TAG_NAME, PYTHON_COMMENT_TAG)

    class INJECTABLE():
        PYTHON = TagConfig.build(INJECTABLE_TAG_NAME, PYTHON_COMMENT_TAG)

    class INJECT():
        PYTHON = TagConfig.build(INJECT_TAG_NAME, PYTHON_COMMENT_TAG)




class RegionIdentifiers():


    class DEFAULT():
        PYTHON = RegionConfig.build(ParseTags.REGION_START.PYTHON, ParseTags.REGION_END.PYTHON)





