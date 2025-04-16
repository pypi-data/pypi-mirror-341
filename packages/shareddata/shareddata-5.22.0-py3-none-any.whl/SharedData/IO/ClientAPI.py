import json
import requests
import os
import pandas as pd
import numpy as np
import time
import lz4.frame
import lz4.frame as lz4f


from SharedData.CollectionMongoDB import CollectionMongoDB
from SharedData.IO.SyncTable import SyncTable
from SharedData.Logger import Logger
from SharedData.Database import *


class ClientAPI:
    
    @staticmethod
    def table_subscribe_thread(table, host, port,
            lookbacklines=1000, lookbackdate=None, snapshot=False,
            bandwidth=1e6, protocol='http'):

        apiurl = f"{protocol}://{host}:{port}"
        
        records = table.records
        
        params = {                    
            'token': os.environ['SHAREDDATA_TOKEN'],            
        }

        tablename = table.tablename
        tablesubfolder = None
        if '/' in table.tablename:
            tablename = table.tablename.split('/')[0]
            tablesubfolder = table.tablename.split('/')[1] 

        url = apiurl+f"/api/subscribe/{table.database}/{table.period}/{table.source}/{tablename}"
        
        lookbackid = records.count - lookbacklines
        if tablesubfolder:
            params['tablesubfolder'] = tablesubfolder        
        if lookbacklines:
            params['lookbacklines'] = lookbacklines
        if lookbackdate:
            params['lookbackdate'] = lookbackdate
            lookbackdate = pd.Timestamp(lookbackdate)
            lookbackid, _ = records.get_date_loc(lookbackdate)
        if bandwidth:
            params['bandwidth'] = bandwidth
                
        hasindex = records.table.hasindex           
        lastmtime = pd.Timestamp('1970-01-01')
        if hasindex:
            lastmtime = np.max(records[lookbackid:]['mtime'])
            lastmtime = pd.Timestamp(np.datetime64(lastmtime))
        while True:
            try:
                params['page'] = 1
                if hasindex:
                    params['mtime'] = lastmtime
                params['count'] = records.count
                params['snapshot'] = snapshot
                snapshot = False

                response = requests.get(url, params=params)
                if response.status_code != 200:
                    if response.status_code == 204:
                        time.sleep(1)
                        continue
                    else:
                        raise Exception(response.status_code, response.text)
                
                data = lz4.frame.decompress(response.content)
                buffer = bytearray()
                buffer.extend(data)
                if len(buffer) >= records.itemsize:
                    # Determine how many complete records are in the buffer
                    num_records = len(buffer) // records.itemsize
                    # Take the first num_records worth of bytes
                    record_data = buffer[:num_records *
                                                records.itemsize]
                    # And remove them from the buffer
                    del buffer[:num_records *
                                        records.itemsize]
                    # Convert the bytes to a NumPy array of records
                    rec = np.frombuffer(
                        record_data, dtype=records.dtype)
                    if hasindex:
                        recmtime = pd.Timestamp(np.max(rec['mtime']))
                        if recmtime > lastmtime:
                            lastmtime = recmtime
                        
                    if records.table.hasindex:
                        # Upsert all records at once
                        records.upsert(rec)
                    else:
                        # Extend all records at once
                        records.extend(rec)

                pages = int(response.headers['Content-Pages'])
                if pages > 1:
                    # paginated response
                    for i in range(2, pages+1):
                        params['page'] = i                        
                        response = requests.get(url, params=params)
                        if response.status_code != 200:
                            raise Exception(response.status_code, response.text)
                        data = lz4.frame.decompress(response.content)
                        buffer = bytearray()
                        buffer.extend(data)
                        if len(buffer) >= records.itemsize:
                            # Determine how many complete records are in the buffer
                            num_records = len(buffer) // records.itemsize
                            # Take the first num_records worth of bytes
                            record_data = buffer[:num_records *
                                                        records.itemsize]
                            # And remove them from the buffer
                            del buffer[:num_records *
                                                records.itemsize]
                            # Convert the bytes to a NumPy array of records
                            rec = np.frombuffer(
                                record_data, dtype=records.dtype)
                            if hasindex:
                                recmtime = pd.Timestamp(np.max(rec['mtime']))
                                if recmtime > lastmtime:
                                    lastmtime = recmtime
                                
                            if records.table.hasindex:
                                # Upsert all records at once
                                records.upsert(rec)
                            else:
                                # Extend all records at once
                                records.extend(rec)
                        time.sleep(0.5)

                time.sleep(1)

            except Exception as e:
                msg = 'Retrying API subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)

    @staticmethod
    def table_publish_thread(table, host, port, lookbacklines, 
        lookbackdate, snapshot,bandwidth, protocol='http'):

        if port is None:
            apiurl = f"{protocol}://{host}"
        else:
            apiurl = f"{protocol}://{host}:{port}"
        
        while True:
            try:
                records = table.records
                
                params = {                    
                    'token': os.environ['SHAREDDATA_TOKEN'],            
                }

                tablename = table.tablename
                tablesubfolder = None
                if '/' in table.tablename:
                    tablename = table.tablename.split('/')[0]
                    tablesubfolder = table.tablename.split('/')[1] 

                url = apiurl+f"/api/publish/{table.database}/{table.period}/{table.source}/{tablename}"
                                
                if tablesubfolder:
                    params['tablesubfolder'] = tablesubfolder        
                if lookbacklines:
                    params['lookbacklines'] = lookbacklines
                if lookbackdate:
                    params['lookbackdate'] = lookbackdate
                    lookbackdate = pd.Timestamp(lookbackdate)            
                if bandwidth:
                    params['bandwidth'] = bandwidth
                
                
                # ask for the remote table mtime and count

                response = requests.get(url, params=params)

                if response.status_code != 200:
                    raise Exception(response.status_code, response.text)

                response = response.json()
                remotemtime = None
                if 'mtime' in response:
                    remotemtime = pd.Timestamp(response['mtime']).replace(tzinfo=None)
                remotecount = response['count']

                client = {}
                client.update(params)
                if 'mtime' in response:
                    client['mtime'] = remotemtime.timestamp()
                client['count'] = remotecount
                client = SyncTable.init_client(client,table)

                while True:
                    try:
                        client, ids2send = SyncTable.get_ids2send(client)
                        if len(ids2send) == 0:
                            time.sleep(0.001)                            
                        else:
                            rows2send = len(ids2send)
                            sentrows = 0
                            msgsize = min(client['maxrows'], rows2send)
                            bandwidth = client['bandwidth']
                            tini = time.time_ns()
                            bytessent = 0
                            while sentrows < rows2send:
                                t = time.time_ns()
                                message = records[ids2send[sentrows:sentrows +
                                                        msgsize]].tobytes()
                                compressed = lz4f.compress(message)
                                msgbytes = len(compressed)
                                bytessent+=msgbytes                        
                                msgmintime = msgbytes/bandwidth                        
                                
                                # create a post request
                                response = requests.post(url, params=params, data=compressed)
                                if response.status_code != 200:
                                    raise Exception('Failed to publish data remote!=200 !')

                                sentrows += msgsize
                                msgtime = (time.time_ns()-t)*1e-9
                                ratelimtime = max(msgmintime-msgtime, 0)
                                if ratelimtime > 0:
                                    time.sleep(ratelimtime)

                            totalsize = (sentrows*records.itemsize)/1e6
                            totaltime = (time.time_ns()-tini)*1e-9
                            if totaltime > 0:
                                transfer_rate = totalsize/totaltime
                            else:
                                transfer_rate = 0
                            client['transfer_rate'] = transfer_rate
                            client['upload'] += msgbytes
                        
                    except:
                        break

            except Exception as e:
                msg = 'Retrying API publish %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                        table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)

    @staticmethod
    def records2df(records, pkey):
        df = pd.DataFrame(records, copy=False)
        dtypes = df.dtypes.reset_index()
        dtypes.columns = ['tag', 'dtype']
        # convert object to string
        string_idx = pd.Index(['|S' in str(dt) for dt in dtypes['dtype']])
        string_idx = (string_idx) | pd.Index(dtypes['dtype'] == 'object')
        tags_obj = dtypes['tag'][string_idx].values
        for tag in tags_obj:
            try:
                df[tag] = df[tag].str.decode(encoding='utf-8', errors='ignore')
            except:
                pass
        df = df.set_index(pkey)
        return df
    
    @staticmethod
    def df2records(df, pkeycolumns, recdtype=None):
        check_pkey = True
        if len(pkeycolumns) == len(df.index.names):
            for k in range(len(pkeycolumns)):
                check_pkey = (check_pkey) & (
                    df.index.names[k] == pkeycolumns[k])
        else:
            check_pkey = False
        if not check_pkey:
            raise Exception('First columns must be %s!' % (pkeycolumns))
        
        if recdtype is None:
            df = df.reset_index()
            dtypes = df.dtypes.reset_index()
            dtypes.columns = ['tag', 'dtype']
        
            # Convert datetime columns with timezone to UTC naive datetime
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    if df[col].dt.tz is not None:
                        df[col] = df[col].dt.tz_convert('UTC').dt.tz_localize(None)
            
            # convert object to string
            tags_obj = dtypes['tag'][dtypes['dtype'] == 'object'].values
            for tag in tags_obj:
                try:
                    df[tag] = df[tag].astype(str)
                    df[tag] = df[tag].str.encode(encoding='utf-8', errors='ignore')
                except Exception as e:
                    Logger.log.error(f'df2records(): Could not convert {tag} : {e}!')
                df[tag] = df[tag].astype('|S')
                
            rec = np.ascontiguousarray(df.to_records(index=False))
            type_descriptors = [field[1] for field in rec]
            if '|O' in type_descriptors:
                errmsg = 'df2records(): Could not convert type to binary'
                Logger.log.error(errmsg)
                raise Exception(errmsg)
                    
            return rec
        else:
            df = df.reset_index()
            # Convert datetime columns with timezone to UTC naive datetime
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    if df[col].dt.tz is not None:
                        df[col] = df[col].dt.tz_convert('UTC').dt.tz_localize(None)
            
            dtypes = recdtype
            
            rec = np.full((df.shape[0],), fill_value=np.nan, dtype=dtypes)
            for col in dtypes.names:
                try:
                    if col in df.columns:
                        if pd.api.types.is_integer_dtype(dtypes[col])\
                            or pd.api.types.is_unsigned_integer_dtype(dtypes[col]):
                            df[col] = df[col].fillna(0)
                            
                        rec[col] = df[col].astype(dtypes[col])
                        
                except Exception as e:
                    Logger.log.error('df2records(): Could not convert %s!\n%s' % (col, e))

            return rec

    @staticmethod
    def get_table(database, period, source, tablename, 
            host, port=None,
            startdate=None, enddate=None, 
            symbols=None, portfolios=None, tags=None, query=None,
            page=None, per_page=None,            
            output_format='bin', token=None, user=None, output_records=False):
            
        url = host
        if port:
            url = f"{url}:{port}"

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/table/{database}/{period}/{source}/{tablename}'
        url += route

        
        if not token is None: 
            params['token'] = token 
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')

        if startdate:
            params['startdate'] = startdate
        if enddate:
            params['enddate'] = enddate
        if symbols:
            params['symbols'] = symbols
        if portfolios:
            params['portfolios'] = portfolios
        if tags:
            params['tags'] = tags
        if user:
            params['user'] = user
        if query:
            params['query'] = json.dumps(query)
        if per_page:
            params['per_page'] = per_page
        if page:
            params['page'] = page
        if output_format:
            params['format'] = output_format

        # Make the GET request
        # Request LZ4-encoded response
        headers = {
            'Accept-Encoding': 'lz4'
        }

        response = requests.get(url, params=params, headers=headers)        
        response.raise_for_status()

        if response.status_code == 204: 
            return pd.DataFrame([])
        
        # Read field metadata from headers
        names = json.loads(response.headers.get('Meta-Field-Names'))
        formats = json.loads(response.headers.get('Meta-Field-Formats'))
        pkey = json.loads(response.headers.get('Meta-Field-Pkey'))

        # Rebuild dtype
        dtype = np.dtype(list(zip(names, formats)))

        # Decompress LZ4 payload
        decompressed = lz4f.decompress(response.content)

        # Reconstruct numpy structured array
        recs = np.frombuffer(decompressed, dtype=dtype)
        if output_records:
            return recs
                
        # Convert to DataFrame
        df = ClientAPI.records2df(recs,pkey)

        return df
    
    @staticmethod
    def post_table(database, period, source, tablename, 
            host, port=None, 
            names = None, formats=None, size=None,
            value=None, overwrite=False,
            token=None, user=None):
            
        url = host
        if port:
            url = f"{url}:{port}"

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/table/{database}/{period}/{source}/{tablename}'
        url += route
        
        if not token is None: 
            params['token'] = token 
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')
        
        if user:
            params['user'] = user
        if names:
            params['names'] = json.dumps(names)
        if formats:
            params['formats'] = json.dumps(formats)
        if size:
            params['size'] = int(size)
        if overwrite:
            params['overwrite'] = overwrite
        
        if not value is None:
            if isinstance(value, pd.DataFrame):
                if names and formats:
                    hdrdtype = np.dtype({'names': names, 'formats': formats})
                    value = ClientAPI.df2records(value,DATABASE_PKEYS[database],recdtype=hdrdtype)
                else:
                    value = ClientAPI.df2records(value,DATABASE_PKEYS[database])
            elif isinstance(value, np.ndarray):
                pass
            else:
                raise Exception('value must be a pandas DataFrame')
                        
            meta_names = list(value.dtype.names)
            meta_formats = [value.dtype.fields[name][0].str for name in meta_names]
            compressed = lz4f.compress(value.tobytes())
            responsebytes = len(compressed)
            
            headers = {}
            headers['Content-Encoding'] = 'lz4'
            headers['Content-Length'] = json.dumps(responsebytes)
            headers['Meta-Field-Names'] = json.dumps(meta_names)
            headers['Meta-Field-Formats'] = json.dumps(meta_formats)
            headers['Meta-Field-Pkey'] = json.dumps(DATABASE_PKEYS[database])

            # Make the POST request
            response = requests.post(
                url,
                params=params,
                data=compressed,
                headers=headers
            )
        else:
            response = requests.post(url, params=params)

        response.raise_for_status()
        
        return response.status_code
    
    @staticmethod
    def get_collection(database, period, source, tablename, 
                        host, port=None, query=None, sort=None, 
                        page=None, per_page=None, 
                        token=None, user=None):
        
        url = host
        if port:
            url = f"{url}:{port}"

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/collection/{database}/{period}/{source}/{tablename}'
        url += route

        if not token is None:
            params['token'] = token
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')

        if user:
            params['user'] = user
        if sort:
            params['sort'] = json.dumps(sort)
        if query:
            params['query'] = json.dumps(query)

        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page    

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            if response.status_code == 204: 
                return pd.DataFrame([])
            
            # Default to JSON
            rjson = json.loads(response.content)                            
            if not 'data' in rjson:
                return pd.DataFrame([])
            df = pd.DataFrame(json.loads(rjson['data']))
            if df.empty:
                return df
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            pkey = rjson['pkey']
            df = df.set_index(pkey).sort_index()
            
            return df

        except requests.exceptions.HTTPError as http_err:
            Logger.log.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            Logger.log.error(f"Other error occurred: {err}")

        return pd.DataFrame([])  # Return an empty DataFrame in case of error
    
    @staticmethod
    def post_collection(database, period, source, tablename, 
            host, port=None, 
            value=None, 
            token=None, user=None):
            
        url = host
        if port:
            url = f"{url}:{port}"

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/collection/{database}/{period}/{source}/{tablename}'
        url += route

        if not token is None: 
            params['token'] = token 
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')

        if user:
            params['user'] = user

        if isinstance(value, pd.DataFrame):
            value = CollectionMongoDB.serialize(value.reset_index(), iso_dates=True)
        else:
            raise Exception('value must be a pandas DataFrame')            

        # Make the POST request
        response = requests.post(url, params=params, data=json.dumps(value))
        response.raise_for_status()

        return response.json()
    
    @staticmethod
    def patch_collection(database, period, source, tablename, 
            filter, update, host, port=None,
            token=None, user=None, sort=None):     
        
        url = host
        if port:
            url = f"{url}:{port}"

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/collection/{database}/{period}/{source}/{tablename}'
        url += route

        if not token is None: 
            params['token'] = token 
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')

        if user:
            params['user'] = user
        
        params['filter'] = json.dumps(filter)  # Convert filter to JSON string
        params['update'] = json.dumps(update)  # Convert update to JSON string
        if sort:
            params['sort'] = json.dumps(sort)  # Convert sort to JSON string

        try:
            response = requests.patch(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            if response.status_code == 200:
                # Default to JSON
                rjson = json.loads(response.content)
                if not 'data' in rjson:
                    return pd.DataFrame([])
                df = pd.DataFrame([json.loads(rjson['data'])])
                if df.empty:
                    return df
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                pkey = rjson['pkey']
                df = df.set_index(pkey).sort_index()
                
                return df
            elif response.status_code == 204:
                return pd.DataFrame([])
        
        except Exception as e:
            Logger.log.error(f"ClientAPI patch_collection Error: {e}")
            raise e