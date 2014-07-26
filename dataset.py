import json
from settings import DEBUG as DEBUG

class DataSet:
    def __init__(self, path):
        '''
        Args:
            path:      Input json file path
        '''
        self._path = path
        try:
            self._json_file = open(path, 'r')
            print "Open input file: %s successfully!" % path
        except:
            print "Open file: %s failed!" % path
        self.entities = self._make()

    def __repr__(self):
        '''
        Dataset description
        ---------------------------------
        Returns:
            des:       Descript of datset
        '''
        des = '''Data from: %s \nAll %d lines ''' % (self.get_path(), len(self.entities))
        return des

    def get_path(self):
        '''
        Return path of dataset
        ---------------------------------
        Returns:
            self._path:     Dataset path
        '''
        return self._path

    def get_all_entity_name(self):
        return self.entities.keys()

    def get_json_file(self):
        '''
        Returns:
            _json_file:     Json file
        '''
        return self._json_file

    def _make(self):
        '''
        Convert json file to dict type
        ---------------------------------
        Returns:
            entities:       entity name and attribute
        '''
        entities = {}
        print 'Start load json file'
        for line in self._json_file:
            if line.strip():
               en_name, en_attri = line.split('\t')
               entities[en_name.strip()] = json.loads(en_attri.strip())
               # entities.append(json.loads(en_attri))
        return entities

    def json_print(self):
        '''
        Pretty print dataset:
        "entity name:"
        {
            "field1": {"value1"},
            "field2": {"value2"},
            ...
        }
        '''
        for n, d in self.entities.items():
            print n
            print json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

    def entity_categories(self):
        '''
        Extract attribute type as a key, value contains entity name list 
        {'Movie':['1', '2', ...],'VideoGame':['3', '4', ...]}
        '''
        hash_type = {}
        for e_name, e_dict in self.entities.items():
            # Get type in entity e_name
            e_type = e_dict['type']
            hash_type.setdefault(e_type, [])
            hash_type[e_type].append(e_name)
        return hash_type
