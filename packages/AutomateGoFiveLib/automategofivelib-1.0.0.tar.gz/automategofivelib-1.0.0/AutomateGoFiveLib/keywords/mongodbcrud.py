# -*- coding: utf-8 -*-
import datetime
import time
import random
import logging
import ast

from bson import ObjectId
from pymongo import MongoClient , errors

class Mongodbcrud:

    def __init__(self):
        pass

    # Keyword 

    def mongodb_connect_to_db(self,dbHost='localhost',timeout=5000 ,  dbPort=27017, dbMaxPoolSize=10, dbNetworkTimeout=None,
                            dbDocClass=dict, dbTZAware=False):
        """
            ***|    Description     |***
            | *`Mongodb Connect To Db`* | Connects to the MongoDB host using parameters submitted  |

                
            ***|    Example     |***
            | *`Connect Mongodb With URL`* | *`mongodb+srv://username:password@host`* | *`timeout=10`* |
        """
        dbPort = int(dbPort)
        # log result
        logging.info(
                "| Connect To MondoDB | dbHost | timeout | dbPort | dbMaxPoolSize | dbNetworktimeout | dbDocClass | dbTZAware |")
        logging.info(
                "| Connect To MondoDB | %s | %s | %s | %s | %s | %s | %s |" % (dbHost , timeout , dbPort, dbMaxPoolSize, dbNetworkTimeout,
                                                                          dbDocClass, dbTZAware))

        try:
            # สร้าง MongoClient และเชื่อมต่อกับ MongoDB
            self._dbconnection = MongoClient(host=dbHost, serverSelectionTimeoutMS=timeout , port=dbPort, socketTimeoutMS=dbNetworkTimeout,
                                                        document_class=dbDocClass, tz_aware=dbTZAware,
                                                        maxPoolSize=dbMaxPoolSize)
            # เรียกดูรายการ database ที่เชื่อมต่อ
            logging.info("Connect to MongoDB Success!")
        except errors.ConnectionFailure as e:
            logging.info("Fail Connect to MongoDB: %s " % (e))
        
        return  self._dbconnection
    
    def mongodb_disconnect_from_db(self):
        """
            ***|    Description     |***
            | *`Mongodb Disconnect From Db`* | Disconnects from the MongoDB server.  |
        """
        logging.info(" Disconnect From MongoDB ")
        self._dbconnection.close()

    def mongodb_update_one(self,dbname , dbcollection , query , update):
        """
            ***|    Description     |***
            | *`Mongodb Update One`* | Update one MongoDB.  |

            ***|    Example     |***
            | ${ตัวแปร} | *`Mongodb Update One `* | dbName | dbCollection | query | update
        """
        dbname = str(dbname)
        dbcollection = str(dbcollection)
        db = self._dbconnection['%s' % (dbname)]
        collection = db['%s' % (dbcollection)]
        #Set Update
        dictquery = ast.literal_eval(query)
        dictupdate = ast.literal_eval(update)

        if '_id' in dictquery:
            dictquery['_id'] = ObjectId(dictquery['_id'])

        if 'ts' in dictquery:
            dictquery['ts'] = ObjectId(dictquery['ts'])

        if '$set' in dictupdate and 'ts' in dictupdate['$set']:
            dictupdate['$set']['ts'] = ObjectId(dictupdate['$set']['ts'])

        logging.info("dictquery : %s And Type : %s)" % (dictquery,type(dictquery)))
        logging.info("dictupdate : %s And Type : %s)" % (dictupdate,type(dictupdate)))

        try:
            #  MongoClient เชื่อมต่อกับ MongoDB และ Update one
            result = collection.update_one(
                dictquery,
                dictupdate
            )
            logging.info("Update one to Mongodb Success")
        except errors.ConnectionFailure as e:
            logging.info("Fail Update one to Mongodb: %s" % (e))

        return  result.modified_count
    
    def mongodb_convert_str_to_objectid(self,string):
        """
            ***|    Description     |***
            | *`Mongodb Convert Str To Objectid`* | Convert type string to objectid  |

            ***|    Example     |***
            | ${ตัวแปร} | *`Mongodb Convert Str To Objectid `* | string |

            result : 650f0b5a6c6b1c1f12345678
        """
        try:
            # แปลง string ให้เป็น ObjectId
            object_id = ObjectId(string)
            logging.info("ObjectId: %s" % (object_id))
        except Exception as e:
            logging.info("Fail Can't Convert string to ObjectId: %s" % (e))

        return  object_id

    def mongodb_update_timestamp_object_id(self):
        """ *******Keyword update timestamp object id*******

        keyword สำหรับ update time stamp ให้เป็นเวลาปัจจุบัน ใน field mongodb ที่เป็น
        type ObjectId

        Examples:

        | ${ตัวแปร} | mongodb_update_timestamp_object_id |
        """
        timestamp = hex(int(time.time()))[2:]
        object_id = timestamp + ''.join([hex(random.randint(0, 15))[2:] for _ in range(16)])
        thai_time = self._objectid_to_utc_thai_time(object_id)
        utc_time = self._objectid_to_utc_time(object_id)
        #แปลงค่า Type จาก string เป็น ObjectId
        ts_object_id = ObjectId(object_id)
        #log result
        logging.info("Mongodb Ts OdjectId : %s" % (object_id))
        logging.info("UTC Time : %s" % (utc_time))
        logging.info("UTC Thai Time : %s" % (thai_time))
        logging.info("ts_object_id Type : %s" % (type(ts_object_id)))
        return ts_object_id
    
    #Private Function

    def _objectid_to_utc_thai_time(self,objectid):
        # ดึง 4 ไบต์แรกของ ObjectId (8 ตัวอักษรแรก) และแปลงเป็นฐาน 10
        timestamp = int(objectid[:8], 16)
        
        # แปลง timestamp เป็นวันที่และเวลา UTC
        utc_time = datetime.datetime.utcfromtimestamp(timestamp)

        # เพิ่ม 7 ชั่วโมงเพื่อแปลงเป็นเวลาไทย (THA)
        tha_time = utc_time + datetime.timedelta(hours=7)
        
        return tha_time
    
    def _objectid_to_utc_time(self,objectid):
        # ดึง 4 ไบต์แรกของ ObjectId (8 ตัวอักษรแรก) และแปลงเป็นฐาน 10
        timestamp = int(objectid[:8], 16)
        
        # แปลง timestamp เป็นวันที่และเวลา UTC
        utc_time = datetime.datetime.utcfromtimestamp(timestamp)
        
        return utc_time