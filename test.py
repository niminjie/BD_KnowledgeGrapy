import sys
import seg
from dataset import DataSet
from settings import DEBUG as DEBUG
from util import *
from test import *
from BD import *

def test_train_sim(ds_task1, hash_type):
    # Load json file
    for line in open("./dataset/train.txt", 'r'):
        id_1, id_2, sim = line.split("\t")
        query_entity(ds_task1, id_1.strip(), "type")
        query_entity(ds_task1, id_2.strip(), "type")
        print "------------------------------------------"

def test_minEditDistR():
    return minEditDistR("acbdeg", "acbdge")

def test_extract_categories(hash_type):
    extract_categories(hash_type, output_path='./categories')

def test_extract_text(ds_task1):
    extract_text(ds_task1)

def test_seg_des(ds_task1, en_name, attr_name):
    return seg_des(ds_task1, en_name, attr_name)
