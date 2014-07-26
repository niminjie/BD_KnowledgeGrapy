# encoding:utf8
import sys
import json
import seg
from dataset import DataSet
from settings import DEBUG as DEBUG
from util import *

def main():
    # Load json file
    ds_task1 = DataSet('dataset/entity.json')
    # ds_task1.json_print()
    attri_text = extract_text(ds_task1)

    for key, value in attri_text.items():
        text_each_other(attri_text)
        # for v in value:
        #     print key, v

    # hash_type = ds_task1.entity_categories()
    # extract_categories(hash_type, output_path='./categories')
    # seg_des(ds_task1, '3ac567be298fa5e87ad120778d80d7ef', 'description')

    # for attri_str, attri in dis_attri.items():
        # print >> fo, attri_str
        # # print dis_attri[attri_str]['entity'][0:2]
        # try:
            # query_entity(ds_task1, dis_attri[attri_str]['entity'][0])
            # query_entity(ds_task1, dis_attri[attri_str]['entity'][1])
        # except:
            # pass
        # print >> fo, '-' * 100

def query_entity(dataset, en_name):
    '''
    Args:
        dataset:      DataSet
        en_name:      entity name 
    Return:
        en_name pretty print
    '''
    try:
        en_json = dataset.entities[en_name]
        print >> fo, json.dumps(en_json, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')
        print >> fo, en_name
    except KeyError:
        print "Have not found entity name: %s" % en_name
        return None
    return json.dumps(en_name, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

def extract_categories(cate, input_path='dataset/entity.json', output_path='./'):
    '''
    Args:
        cate:  {'Movie':['3ac567be298fa5e87ad120778d80d7ef',...],...}
    '''
    f_name_list = cate.keys()
    data = {}

    for line in open(input_path, 'r'):
        en_name, en_des = line.split('\t')
        en_name = en_name.strip()
        en_des = en_des.strip()
        data[en_name] = en_des
    
    for f_name in f_name_list:
        entity_list = cate[f_name]
        # print entity_list
        with open(output_path + '/' + f_name, 'w') as f:
            for en_name in entity_list:
                f.write("%s\t%s\n" % (en_name.strip(), data[en_name.strip()]))
                f.flush()

def find_same_attri(en_1, en_2):
    '''
    Input two different entity name to get same attribute name
    '''
    if en_1 == en_2:
        return None;
    en_attr_1 = en_1.keys()
    en_attr_2 = en_2.keys()
    return [attr for attr in en_attr_1 if attr in en_attr_2]

def seg_des(dataset, en_name, attri_name):
    '''
    Segment a attribute in a entity
    '''
    print en_name
    entity = dataset.entities[en_name]
    before_seg = entity[attri_name]
    after_seg = []
    for text in before_seg:
        after_seg.append(seg.cut(text))
    # after_seg = seg.cut(before_seg)
    dataset.entities[en_name][attri_name] = after_seg
    # print after_seg
    if DEBUG:
        for i in xrange(len(before_seg)):
            print 'CUT %s\n TO\n %s' % (before_seg[i], after_seg[i])
            print '-' * 50
        
if __name__ == '__main__':
    fo = open('cate_out', 'wa')
    main()
