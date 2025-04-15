from flask import Flask, Response
from flask import request
from flask import jsonify
from flask import make_response
from flasgger import Swagger, swag_from
from bson.objectid import ObjectId
import pymongo
import os
import datetime
import gzip
import json
import time
import lz4.frame as lz4f
import pandas as pd
import numpy as np

from SharedData.CollectionMongoDB import CollectionMongoDB

MAX_RESPONSE_SIZE_BYTES = int(10*1024*1024)

app = Flask(__name__)
app.config['APP_NAME'] = 'SharedData API'
app.config['FLASK_ENV'] = 'production'
app.config['FLASK_DEBUG'] = '0'
if not 'SHAREDDATA_SECRET_KEY' in os.environ:
    raise Exception('SHAREDDATA_SECRET_KEY environment variable not set')
if not 'SHAREDDATA_TOKEN' in os.environ:
    raise Exception('SHAREDDATA_TOKEN environment variable not set')

app.config['SECRET_KEY'] = os.environ['SHAREDDATA_SECRET_KEY']
app.config['SWAGGER'] = {
    'title': 'SharedData API',
    'uiversion': 3
}
docspath = 'ServerAPIDocs.yml'
swagger = Swagger(app, template_file=docspath)

@app.route('/api/heartbeat', methods=['GET', 'POST'])
def heartbeat():
    time.sleep(3)
    return jsonify({'heartbeat':True}), 200

@app.route('/api/auth', methods=['GET', 'POST'])
def auth():
    try:
        # check for the token in the header
        clienttoken = request.headers.get('X-Custom-Authorization', '')
        if clienttoken == '':
            clienttoken = request.args.get('token','') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
        else:
            return jsonify({'authenticated':True}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscribe/<database>/<period>/<source>/<tablename>', methods=['GET'])
def subscribe(database, period, source, tablename):
    try:        
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
                
        tablesubfolder = request.args.get('tablesubfolder')  # Optional
        if tablesubfolder is not None:
            table = shdata.table(database, period, source, tablename+'/'+tablesubfolder)
        else:
            table = shdata.table(database, period, source, tablename)

        if table.table.hasindex:
            lookbacklines = request.args.get('lookbacklines', default=1000, type=int)  # Optional
            lookbackid = table.count - lookbacklines
            if 'lookbackdate' in request.args:
                lookbackdate = pd.Timestamp(request.args.get('lookbackdate'))
                lookbackid, _ = table.get_date_loc(lookbackdate)            
            if lookbackid < 0:
                lookbackid = 0

            ids2send = np.arange(lookbackid, table.count)
            if 'mtime' in request.args:
                mtime = pd.Timestamp(request.args.get('mtime'))
                newids = lookbackid + np.where(table['mtime'][ids2send] >= mtime)[0]
                ids2send = np.intersect1d(ids2send, newids)

        else:
            clientcount = request.args.get('count', default=0, type=int)  # Optional
            if clientcount<table.count:
                ids2send = np.arange(clientcount, table.count-1)
            else:
                ids2send = np.array([])
        
        rows2send = len(ids2send)
        if rows2send == 0:
            return Response(status=204)
        
        # Compress & paginate the response                
        maxrows = np.floor(MAX_RESPONSE_SIZE_BYTES/table.itemsize)
        if rows2send>maxrows:
            # paginate
            page = request.args.get('page', default=1, type=int)
            ids2send = ids2send[int((page-1)*maxrows):int(page*maxrows)]

        compressed = lz4f.compress(table[ids2send].tobytes())
        responsebytes = len(compressed)
        response = Response(compressed, mimetype='application/octet-stream')
        response.headers['Content-Encoding'] = 'lz4'
        response.headers['Content-Length'] = responsebytes        
        response.headers['Content-Pages'] = int(np.ceil(rows2send/maxrows))
        return response
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/publish/<database>/<period>/<source>/<tablename>', methods=['GET'])
def publish_get(database, period, source, tablename):
    try:        
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
                
        tablesubfolder = request.args.get('tablesubfolder')  # Optional
        if tablesubfolder is not None:
            table = shdata.table(database, period, source, tablename+'/'+tablesubfolder)
        else:
            table = shdata.table(database, period, source, tablename)

        msg = {'count': int(table.count)}

        if table.table.hasindex:
            lookbacklines = request.args.get('lookbacklines', default=1000, type=int)  # Optional
            lookbackid = table.count - lookbacklines
            if 'lookbackdate' in request.args:
                lookbackdate = pd.Timestamp(request.args.get('lookbackdate'))
                lookbackid, _ = table.get_date_loc(lookbackdate)            
            if lookbackid < 0:
                lookbackid = 0

            ids2send = np.arange(lookbackid, table.count)            
            msg['mtime'] = pd.Timestamp(np.datetime64(np.max(table['mtime'][ids2send])))

        return jsonify(msg)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/publish/<database>/<period>/<source>/<tablename>', methods=['POST'])
def publish_post(database, period, source, tablename):
    try:        
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
                
        tablesubfolder = request.args.get('tablesubfolder')  # Optional
        if tablesubfolder is not None:
            table = shdata.table(database, period, source, tablename+'/'+tablesubfolder)
        else:
            table = shdata.table(database, period, source, tablename)
        
        data = lz4f.decompress(request.data)
        buffer = bytearray()
        buffer.extend(data)
        if len(buffer) >= table.itemsize:
            # Determine how many complete records are in the buffer
            num_records = len(buffer) // table.itemsize
            # Take the first num_records worth of bytes
            record_data = buffer[:num_records *
                                        table.itemsize]
            # And remove them from the buffer
            del buffer[:num_records *
                                table.itemsize]
            # Convert the bytes to a NumPy array of records
            rec = np.frombuffer(
                record_data, dtype=table.dtype)
                
            if table.table.hasindex:
                # Upsert all records at once
                table.upsert(rec)
            else:
                # Extend all records at once
                table.extend(rec)
            
            return Response(status=200)        
        
        return Response(status=204)

    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/table/<database>/<period>/<source>/<tablename>', methods=['GET','POST'])
@swag_from(docspath)
def table(database, period, source, tablename):
    try:
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
        
        if request.method == 'POST':
            return post_table(database, period, source, tablename, request)
        elif request.method == 'GET':
            return get_table(database, period, source, tablename, request)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_table(database, period, source, tablename, request):
    tablesubfolder = request.args.get('tablesubfolder')  # Optional
    startdate = request.args.get('startdate')  # Optional
    enddate = request.args.get('enddate')  # Optional
    symbols = request.args.get('symbols')  # Optional
    portfolios = request.args.get('portfolios')  # Optional
    page = request.args.get('page', default='1')
    page = int(float(page))
    per_page = request.args.get('per_page', default='0')
    per_page = int(float(per_page))
    output_format = request.args.get('format', 'json').lower()  # 'json' by default, can be 'csv' and 'bin'
    query = request.args.get('query')
    if query:
        query = json.loads(query)  # Optional
    else:
        query = {}

    if tablesubfolder is not None:
        tbl = shdata.table(database, period, source, tablename+'/'+tablesubfolder)
    else:
        tbl = shdata.table(database, period, source, tablename)
    
    if startdate is not None:
        startdate = pd.Timestamp(startdate).normalize()
        dti, _ = tbl.get_date_loc(startdate)
        if dti == -1:
            dti = tbl.count
    else:
        dti = 0

    if enddate is not None:
        enddate = pd.Timestamp(enddate).normalize()
        _, dte = tbl.get_date_loc(enddate)
        if dte == -1:
            dte = tbl.count
    else:
        dte = tbl.count

    # filter data
    loc = np.arange(dti, dte)
    if symbols is not None:
        symbols = symbols.split(',')
        symbolloc = []
        for symbol in symbols:
            symbolloc.extend(tbl.get_symbol_loc(symbol))
        symbolloc = np.array(symbolloc)
        if len(symbolloc) > 0:
            loc = np.intersect1d(loc, symbolloc)
        else:
            loc = np.array([])

    if portfolios is not None:
        portfolios = portfolios.split(',')
        portloc = []
        for port in portfolios:
            portloc.extend(tbl.get_portfolio_loc(port))
        portloc = np.array(portloc)
        if len(portloc) > 0:
            loc = np.intersect1d(loc, portloc)
        else:
            loc = np.array([])

    # cycle query keys
    if query.keys() is not None:
        for key in query.keys():            
            if pd.api.types.is_string_dtype(tbl[key]):
                idx = tbl[loc][key] == query[key].encode()
            elif pd.api.types.is_datetime64_any_dtype(tbl[key]):
                idx = tbl[loc][key] == pd.Timestamp(query[key])
            else:                    
                idx = tbl[loc][key] == query[key]
            loc = loc[idx]
    
    if len(loc) == 0:
        return Response(status=204)
    
    # Apply pagination    
    maxrows = int(np.floor(MAX_RESPONSE_SIZE_BYTES/tbl.itemsize))
    if (per_page>maxrows) | (per_page==0):
        per_page = maxrows
    startpage = (page - 1) * per_page
    endpage = startpage + per_page    
    recs2send = tbl[loc[startpage:endpage]]
    rows2send = len(recs2send)

    accept_encoding = request.headers.get('Accept-Encoding', '')
    if output_format == 'csv':
        # Return CSV
        df = tbl.records2df(recs2send)
        df = df.reset_index()
        csv_data = df.to_csv(index=False)
        if 'gzip' in accept_encoding:
            response_csv = csv_data.encode('utf-8')
            response_compressed = gzip.compress(response_csv, compresslevel=1)
            response = Response(response_compressed, mimetype='text/csv')
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Content-Pages'] = int(np.ceil(rows2send/per_page))
            return response
        else:
            return Response(csv_data, mimetype='text/csv')
    elif output_format == 'json':
        # Return JSON
        df = tbl.records2df(recs2send)
        pkey = df.index.names
        df = df.reset_index()
        df = df.applymap(lambda x: x.isoformat() if isinstance(x, datetime.datetime) else x)
        response_data = {
            'page': page,
            'per_page': per_page,
            'total': len(loc),
            'pkey': pkey,
            'data': df.to_dict(orient='records')
        }
        if 'gzip' in accept_encoding:
            response_json = json.dumps(response_data).encode('utf-8')
            response_compressed = gzip.compress(response_json, compresslevel=1)
            response = Response(response_compressed, mimetype='application/json')
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Content-Pages'] = int(np.ceil(rows2send/per_page))
            return response
        else:
            return jsonify(response_data)
    else: #output_format=='bin'
        names = list(tbl.dtype.names)
        formats = [tbl.dtype.fields[name][0].str for name in names]        
        if 'lz4' in accept_encoding:
            compressed = lz4f.compress(recs2send.tobytes())
            responsebytes = len(compressed)        
            response = Response(compressed, mimetype='application/octet-stream')
            response.headers['Content-Encoding'] = 'lz4'
        else:
            compressed = recs2send.tobytes()
            responsebytes = len(compressed)        
            response = Response(compressed, mimetype='application/octet-stream')
            response.headers['Content-Encoding'] = 'bin'
        response.headers['Content-Length'] = responsebytes
        response.headers['Content-Pages'] = int(np.ceil(rows2send/per_page))
        response.headers['Meta-Field-Names'] = json.dumps(names)
        response.headers['Meta-Field-Formats'] = json.dumps(formats)
        response.headers['Meta-Field-Pkey'] = json.dumps(DATABASE_PKEYS[database])

        return response

def post_table(database, period, source, tablename, request):
        
    tablesubfolder = request.args.get('tablesubfolder')  # Optional
    names = request.args.get('names')  # Optional
    if names:
        names = json.loads(names)        
    formats = request.args.get('formats')  # Optional
    if formats:
        formats = json.loads(formats)
    size = request.args.get('size')  # Optional
    if size:
        size = int(size)
    overwrite = request.args.get('overwrite',False)  # Optional
    user = request.args.get('user','master')  # Optional
    value = None
    if request.data:
        value = pd.DataFrame(json.loads(request.data))  # Optional
        pkey_columns = DATABASE_PKEYS[database]
        if 'date' in pkey_columns:
            value['date'] = pd.to_datetime(value['date'])
        if all(col in value.columns for col in pkey_columns):
            value.set_index(pkey_columns, inplace=True)
        else:
            raise Exception(f'Primary key columns {pkey_columns} not found in value')
        
    if tablesubfolder is not None:
        tablename = tablename+'/'+tablesubfolder
            
    tbl = shdata.table(database, period, source, tablename,
                       names=names, formats=formats, size=size,
                       overwrite=overwrite, user=user, value=value)
    if not value is None:
        tbl.upsert(value)
            
    return jsonify({'status': 'success'}), 201

@app.route('/api/collection/<database>/<period>/<source>/<tablename>', methods=['GET','POST','PATCH'])
@swag_from(docspath)
def collection(database, period, source, tablename):
    try:
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
        
        if request.method == 'POST':
            return post_collection(database, period, source, tablename, request)
        elif request.method == 'GET':
            return get_collection(database, period, source, tablename, request)
        elif request.method == 'PATCH':
            return patch_collection(database, period, source, tablename, request)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_collection(database, period, source, tablename, request):
    # Get the collection    
    user = request.args.get('user','master')  # Optional
    tablesubfolder = request.args.get('tablesubfolder')  # Optional
    query = request.args.get('query')
    if query:
        query = json.loads(query)  # Optional
    else:
        query = {}        
    sort = request.args.get('sort')  # Optional        
    if sort:
        sort = json.loads(sort)
    else:
        sort = {}
    page = request.args.get('page', default='1')
    page = int(float(page))
    per_page = request.args.get('per_page', default='10000')
    per_page = int(float(per_page))
    output_format = request.args.get('format', 'json').lower()  # 'json' by default, can be 'csv'
    accept_encoding = request.headers.get('Accept-Encoding', '')
    
    if tablesubfolder is not None:
        tablename = tablename+'/'+tablesubfolder
    collection = shdata.collection(database, period, source, tablename, user=user)

    for key in query:
        if key == '_id':
            query[key] = ObjectId(query[key])
        elif key == 'date':
            if isinstance(query[key],dict):
                for subkey in query[key]:
                    try:
                        query[key][subkey] = pd.Timestamp(query[key][subkey])
                    except:
                        pass
            else:
                try:
                    query[key] = pd.Timestamp(query[key])
                except:
                    pass

    result = collection.find(query, sort=sort, limit=per_page, skip=(page-1)*per_page)
    if len(result) == 0:
        return jsonify({'message': 'No data found'}), 204
    
    if output_format == 'csv':
        # Return CSV
        df = collection.documents2df(result)
        csv_data = df.to_csv()
        if 'gzip' in accept_encoding:
            response_csv = csv_data.encode('utf-8')
            response_compressed = gzip.compress(response_csv, compresslevel=1)
            response = Response(response_compressed, mimetype='text/csv')
            response.headers['Content-Encoding'] = 'gzip'
            return response
        else:
            return Response(csv_data, mimetype='text/csv')
    else:
        pkey = ''
        if database in DATABASE_PKEYS:
            pkey = DATABASE_PKEYS[database]
        # Return JSON
        response_data = {
            'page': page,
            'per_page': per_page,
            'total': len(result),
            'pkey': pkey,
            'data': collection.documents2json(result)
        }

        if 'gzip' in accept_encoding:
            response_json = json.dumps(response_data).encode('utf-8')
            response_compressed = gzip.compress(response_json, compresslevel=1)
            response = Response(response_compressed, mimetype='application/json')
            response.headers['Content-Encoding'] = 'gzip'
            return response
        else:
            return Response(json.dumps(response_data), mimetype='application/json')

def post_collection(database, period, source, tablename, request):    
    tablesubfolder = request.args.get('tablesubfolder')  # Optional
    user = request.args.get('user', 'master')  # Optional
    
    if tablesubfolder is not None:
        tablename = tablename + '/' + tablesubfolder
    
    collection = shdata.collection(database, period, source, tablename, user=user)
    
    # Assuming the incoming data is JSON format
    if not request.data:
        raise Exception("No data provided for the collection")
    
    documents = json.loads(request.data)
    
    if not isinstance(documents, list):
        raise Exception("Data must be a list of documents")
    
    # Insert or update documents (using upsert if available)
    collection.upsert(documents)
    
    # return success with the ids of inserted/updated documents
    return jsonify({'status': 'success'}), 201    

def patch_collection(database, period, source, tablename, request):
    # Get the collection    
    pkey = ''
    if database in DATABASE_PKEYS:
        pkey = DATABASE_PKEYS[database]
    else:
        return jsonify({'error':'database not found'}), 400
    
    user = request.args.get('user','master')  # Optional    
    tablesubfolder = request.args.get('tablesubfolder',None)  # Optional
    if tablesubfolder is not None:
        tablename = tablename+'/'+tablesubfolder
    collection = shdata.collection(database, period, source, tablename, user=user)
    
    filter = request.args.get('filter')
    if filter is None:
        return jsonify({'error':'filter is required'}), 400    
    filter = json.loads(filter)
    for key in filter:
        if key == '_id':
            filter[key] = ObjectId(filter[key])
        elif key == 'date':
            if isinstance(filter[key],dict):
                for subkey in filter[key]:
                    try:
                        filter[key][subkey] = pd.Timestamp(filter[key][subkey])
                    except:
                        pass
            else:
                try:
                    filter[key] = pd.Timestamp(filter[key])
                except:
                    pass

    update = request.args.get('update')
    if update is None:
        return jsonify({'error':'update is required'}), 400
    update = json.loads(update)

    sort = request.args.get('sort')    
    if sort:
        sort = json.loads(sort)
    else:
        sort = {}
    
    coll = collection.collection
    res = coll.find_one_and_update(
        filter= filter, 
        update= update, 
        sort=sort, 
        return_document=pymongo.ReturnDocument.AFTER)
    
    if res:
        if '_id' in res:
            res['_id'] = str(res['_id'])
        
        for key in res:
            if pd.api.types.is_datetime64_any_dtype(res[key]) or isinstance(res[key], datetime.datetime):
                res[key] = res[key].isoformat()
        # Return JSON
        response_data = {
            'pkey': pkey,
            'data': json.dumps(res),
        }
    
        return Response(json.dumps(response_data), mimetype='application/json')
    else:
        return '', 204
       
@app.route('/api/rss', methods=['GET'])
def news():
    try:
        # Get the collection
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
        
        # Get query parameters
        filter = {}

        startdate = request.args.get('startdate')
        if startdate is not None:
            filter['time_published'] = {'$gte': startdate}

        news_text = request.args.get('news_text')
        if news_text is not None and news_text != '':
            filter["title"] = {"$regex": str(news_text), "$options": "i"}

        collection = shdata.mongodb['rss_feeds']

        docs = collection.find(filter).sort({'time_published': -1}).limit(20)
        docs = list(docs)

        response_json = CollectionMongoDB.documents2json(CollectionMongoDB,docs)
                        
        return Response(response_json, mimetype='application/json')


    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    from waitress import serve
    import logging
    # Suppress Waitress logs
    waitress_logger = logging.getLogger('waitress')
    waitress_logger.setLevel(logging.CRITICAL)
    waitress_logger.addHandler(logging.NullHandler())

    import threading
    import sys
    import time  
    import argparse

    from SharedData.SharedData import SharedData
    shdata = SharedData('SharedData.IO.ServerAPI', user='master')
    from SharedData.Logger import Logger
    from SharedData.Database import *

    Logger.log.info('Starting API Server...')
        
    parser = argparse.ArgumentParser(description="Server configuration")
    parser.add_argument('--host', default='0.0.0.0', help='Server host address')
    parser.add_argument('--port', type=int, default=8088, help='Server port number')
    parser.add_argument('--nthreads', type=int, default=4, help='Number of server threads')

    args = parser.parse_args()
    host = args.host
    port = args.port
    nthreads = args.nthreads

    heartbeat_running = True  # Flag to control the heartbeat thread

    def send_heartbeat():
        global heartbeat_running  # Access the outer scope variable
        while heartbeat_running:
            Logger.log.debug('#heartbeat#host:%s,port:%i' % (host, port))
            time.sleep(15)

    t = threading.Thread(target=send_heartbeat, args=())
    t.start()

    Logger.log.info('ROUTINE STARTED!')

    try:
        serve(
            app, 
            host=host, 
            port=port,  
            threads=nthreads,
            expose_tracebacks=False,
            asyncore_use_poll=True,
            _quiet=True,
            ident='SharedData'
        )
    except Exception as e:
        Logger.log.error(f"Waitress server encountered an error: {e}")
        heartbeat_running = False  # Stop the heartbeat thread
        t.join()  # Wait for the heartbeat thread to finish
        sys.exit(1)  # Exit the program with an error code
    finally:
        # This block will always execute, even if an exception occurs.
        # Useful for cleanup if needed.
        Logger.log.info("Server shutting down...")
        heartbeat_running = False  # Ensure heartbeat stops on normal shutdown
        t.join()  # Wait for heartbeat thread to finish
        Logger.log.info("Server shutdown complete.")
