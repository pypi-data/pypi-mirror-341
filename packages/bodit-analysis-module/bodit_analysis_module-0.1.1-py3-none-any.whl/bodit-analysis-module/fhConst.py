import configparser


CONST_PATH = r"\\bodit-analysis\FarmersHands\fh-data-analysis-constants.ini"

config = configparser.ConfigParser()
config.read(CONST_PATH, encoding='utf-8')


""" Base path """
BASEPATH_RAWDATA = config['Paths'].get('BASEPATH_RAWDATA')
BASEPATH_FEATURE = config['Paths'].get('BASEPATH_FEATURE')
BASEPATH_LABEL = config['Paths'].get('BASEPATH_LABEL')
BASEPATH_MODEL = config['Paths'].get('BASEPATH_MODEL')
BASEPATH_FEATLIST = config['Paths'].get('BASEPATH_FEATLIST')
BASEPATH_PRED = config['Paths'].get('BASEPATH_PRED')
BASEPATH_TAG = config['Paths'].get('BASEPATH_TAG')
BASEPATH_PREDTAG = config['Paths'].get('BASEPATH_PREDTAG')


""" Prefix """
PREFIX_RAWDATA = config['Prefix'].get('PREFIX_RAWDATA')
PREFIX_TAG = config['Prefix'].get('PREFIX_TAG')
PREFIX_PREDTAG = config['Prefix'].get('PREFIX_PREDTAG')
PREFIX_FEAT = config['Prefix'].get('PREFIX_FEAT')
PREFIX_LABEL_STATE = config['Prefix'].get('PREFIX_LABEL_STATE')
PREFIX_LABEL_SITSTAND = config['Prefix'].get('PREFIX_LABEL_SITSTAND')
PREFIX_PRED = config['Prefix'].get('PREFIX_PRED')
PREFIX_POST = config['Prefix'].get('PREFIX_POST')


""" fhBasic """
SECTION_TABLE_PATH = config['fhBasic'].get('SECTION_TABLE_PATH')


""" fhRawdata """
ACCEL_SENSITIVITY = config['fhRawdata'].get('ACCEL_SENSITIVITY')
GYRO_SENSITIVITY = config['fhRawdata'].get('GYRO_SENSITIVITY')
SAMPLE_RATE = config['fhRawdata'].get('SAMPLE_RATE')

SAMPLE_INTERVAL = config['fhRawdata'].get('SAMPLE_INTERVAL')
ADJUST_FACTOR = config['fhRawdata'].get('ADJUST_FACTOR')

RAWDATA_INPUT_SIZE = config['fhRawdata'].get('RAWDATA_INPUT_SIZE')
WINDOW_SHAPE = config['fhRawdata'].get('WINDOW_SHAPE')
WINDOW_SIZE = config['fhRawdata'].get('WINDOW_SIZE')

""" fhDatabase """
REGION = config['fhDatabase'].get('REGION')
SECRET_NAME = config['fhDatabase'].get('SECRET_NAME')
DB_NAME = config['fhDatabase'].get('DB_NAME')
SERVICE_NAME = config['fhDatabase'].get('SERVICE_NAME')