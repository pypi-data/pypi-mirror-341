"""Module for accessing multiple Process Variables, served by a liteServer.
"""
__version__ = '3.3.0 2024-07-19'#receive_dictio split in two parts
#TODO: Right now the nonblocked _receive_socket is called from subscribtion thread and from channel.transaction(). Are they thread safe? 
#TODO: Recover from timeout. It is tricky. The timeout could be due to slow or stopped server, in that case do not recover.

import sys, time, socket
from os import getpid
import getpass
_timer = time.perf_counter
import threading
receive_dictio_lock = threading.Lock()

# object encoding
#import ubjson
#encoderDump = ubjson.dumpb
#encoderLoad = ubjson.loadb
#import msgpack as encoder
import cbor2 as encoder
encoderDump = encoder.dumps
encoderLoad = encoder.loads

#````````````````````````````Globals``````````````````````````````````````````
Port = 9700
PrefixLength = 4
SocketSize = 1024*64 # max size of UDP transfer
Dev,Par = 0,1
NSDelimiter = ':'# delimiter in the name field

Username = getpass.getuser()
Program = sys.argv[0]
PID = getpid()
def get_user():
    print(f'liteAcces user:{Username}, PID:{PID}, program:{Program}')
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
#````````````````````````````Helper functions`````````````````````````````````
MaxPrint = 500
def _croppedText(obj, limit=200):
    txt = str(obj)
    if len(txt) > limit:
        txt = txt[:limit]+'...'
    return txt
def _printTime(): return time.strftime("%m%d:%H%M%S")
def _printi(msg): 
    print(_croppedText(f'INFO.LA@{_printTime()}: '+msg))

def _printw(msg):
    msg = msg = _croppedText(f'WARN.LA@{_printTime()}: '+msg)
    print(msg)
    #Device.setServerStatusText(msg)

def _printe(msg): 
    msg = _croppedText(f'ERROR.LA@{_printTime()}: '+msg)
    print(msg)
    #Device.setServerStatusText(msg)

def _printv(msg):
    if PVs.Dbg > 0: print('Dbg0.LA: '+msg)
def _printvv(msg):
    if PVs.Dbg > 1: print('Dbg1.LA: '+msg)

def _croppedText(txt, limit=200):
    if len(txt) > limit:
        txt = txt[:limit]+'...'
    return txt

ReceiverStatistics = {'records':0, 'acks':0, 'bytes':0., 'retrans':0, 'time':0.}
ReceiverStatisticsLast = ReceiverStatistics.copy()
def testCallback(args):
    global ReceiverStatisticsLast
    dt = 10.
    ct = time.time()
    if ct - ReceiverStatisticsLast["time"] >= dt:
        stat = ReceiverStatistics.copy()
        del stat['time']
        for i in stat:
            stat[i] = (stat[i] - ReceiverStatisticsLast[i])
        print(f'Received in last {dt}s: {stat}')
        ReceiverStatisticsLast = ReceiverStatistics.copy()

def ip_address():
    """Platform-independent way to get local host IP address"""
    return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())\
        for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

CNSMap = {}# local map of cnsName to host:port
def _hostPort(cnsNameDev:tuple):
    """Return host;port of the cnsName,Dev try it first from already 
    registered records, or from the name service"""
    global CNSMap
    if len(cnsNameDev) == 1:
        msg = f'Device name should be a tuple (dev,name), got: {cnsNameDev}'
        #_printe(msg)
        raise NameError(msg)
    cnsName,dev = cnsNameDev
    if isinstance(cnsName,list):
        cnsName = tuple(cnsName)
    try:  
        hp,dev = CNSMap[cnsName]# check if cnsName is in local map
    except  KeyError:
        from . import liteCNS
        _printi(f'cnsName {cnsName} not in local map: {CNSMap}')
        try:
            hp = liteCNS.hostPort(cnsName)
        #except NameError:
        except Exception as e:
            msg = (f'The host name {cnsName} is not in liteCNS: {e}\n'
                f"Trying to use it as is: '{cnsName}'")
            #raise   NameError(msg)
            _printw(msg)
            hp = cnsName
        # register externally resolved cnsName in local map
        hp = hp.split(';')
        hp = tuple(hp) if len(hp)==2 else (hp[0],Port)            
        #_printi('cnsName %s is locally registered as '%cnsName+str((hp,dev)))
        CNSMap[cnsName] = hp,dev
        _printi(f'Assuming host,port: {hp}')
    except ValueError:
        msg = f'Device name wrong: {cnsNameDev}, should be of the form: host:dev'
        #_printe(msg)
        raise NameError(msg)
    h,p = hp
    try:
        h = socket.gethostbyname(h)
    except:
        _printe(f'Could not resolve host name {h}')
        sys.exit(1)
    return h,p

retransmitInProgress = None
def _recvUdp(sock):
    """Receive the chopped UDP data"""
    sockAddr,port = sock.getsockname()
    #print(f'>_recvUdp {port} locked: {recvLock.locked()}')
    #with recvLock:
    global retransmitInProgress
    chunks = {sock:{}}
    tryMore = 5# Max number of allowed lost packets
    ts = _timer()
    ignoreEOD = 3

    def ask_retransmit(offsetSize):
        global retransmitInProgress
        ReceiverStatistics['retrans'] += 1
        retransmitInProgress = tuple(offsetSize)
        cmd = {'cmd':('retransmit',offsetSize)}
        _printi(f'Asking to retransmit port {port}: {cmd}')
        sock.sendto(encoderDump(cmd),addr)
    
    while tryMore:
        try:
            buf, addr = sock.recvfrom(SocketSize)
            ReceiverStatistics["records"] += 1
            ReceiverStatistics["bytes"] += len(buf)
            ReceiverStatistics["time"] = time.time()
            
        except socket.timeout as e:
            msg = f'Timeout in recvfrom {sockAddr,port}'
            # Don not return, raise exception, otherwise the pypet will not recover
            raise TimeoutError(msg)
        if buf is None:
            raise RuntimeError(msg)
        size = len(buf) - PrefixLength
        offset = int.from_bytes(buf[:PrefixLength],'big')# python3
        
        #DNP_printi(f'chunk received at port {port}: {offset,size}')

        if size > 0:
            chunks[sock][offset,size] = buf[PrefixLength:]
        if offset > 0 and not retransmitInProgress:
            # expect more chunks to come
            continue

        # check if chunk is EOD, i.e. offset,size = 0,0
        if size == 0:
            ignoreEOD -= 1
            if ignoreEOD >= 0:
                #print(f'premature EOD{ignoreEOD} received from, ignore it')
                continue
            else:
                msg = f'Looks like first chunk is missing at port {port}'
                _printw(msg)
                #This is hard to recover. Give up
                return [],0
                #return ('WARNING: '+msg).encode(), addr
                # sortedKeys = sorted(chunks[sock])
                # offsetSize = [0,sortedKeys[0][0]]
                # allAssembled = False
                # ask_retransmit(offsetSize)
                # break
        else:
            #print('First chunk received')
            pass

        if retransmitInProgress is not None:
            if (offset,size) in chunks[sock]:
                _printi(f'retransmission received {offset,size}')
            else:
                _printw(f'server failed to retransmit chunk {retransmitInProgress}')
                tryMore = 1
            retransmitInProgress = None

        # last chunk have been received, offset==0, size!=0
        # check for lost  chunks
        sortedKeys = sorted(chunks[sock])
        prev = [0,0]
        allAssembled = True
        for offset,size in sortedKeys:
            #print('check offset,size:'+str((offset,size)))
            last = prev[0] + prev[1]
            if last != offset:
                l = offset - last
                if l > 65536:
                    msg = f'Lost too many bytes at port {port}: {last,l}, data discarded'
                    _printw(msg)
                    #raise RuntimeError(msg)
                    return [],0
                    #return 'WARNING: '+msg, addr
                ask_retransmit((last, l))
                allAssembled = False
                break
            prev = [offset,size]

        if allAssembled:
            break
        #print(f'tryMore: {tryMore}')
        tryMore -= 1
    ts1 = _timer()
        
    if not allAssembled:
        msg = 'Partial assembly of %i frames'%len(chunks[sock])
        #raise BufferError(msg)
        _printw(msg)
        return [],0
        #return ('WARNING: '+msg).encode(), addr

    data = bytearray()
    sortedKeys = sorted(chunks[sock])
    for offset,size in sortedKeys:
        # _printv('assembled offset,size '+str((offset,size)))
        data += chunks[sock][(offset,size)]
    tf = _timer()
    # if len(data) > 500000:
        # _printv('received %i bytes in %.3fs, assembled in %.6fs'\
        # %(len(data),ts1-ts,tf-ts1))
    #_printi('assembled %i bytes'%len(data))
    return data, addr

def _send_dictio(dictio, sock, hostPort:tuple):
    """low level send"""
    global LastDictio
    LastDictio = dictio.copy()
    dictio['username'] = Username
    dictio['program'] = Program
    dictio['pid'] = PID
    _printv(f'send_dictio to {hostPort}: {dictio}')
    encoded = encoderDump(dictio)
    sock.sendto(encoded, hostPort)

def _send_cmd(cmd, devParDict:dict, sock, hostPort:tuple, values=None):
    import copy
    #_printv(f'_send_cmd({cmd}.{devParDict} to {sock}')
    dpd = devParDict
    if cmd == 'set':
        if len(devParDict) != 1:
            raise ValueError('Set is supported for single device only')
        dpd = copy.deepcopy(devParDict)# that is IMPORTANT! 
        for key in dpd:
            dpd[key] += 'v',values
    devParList = list(dpd.items())
    dictio = {'cmd':(cmd,devParList)}
    #_printv('sending cmd: '+str(dictio))
    _send_dictio(dictio, sock, hostPort)

def _receive_socket(sock, ackHostPort:tuple):
    data, addr = _recvUdp(sock)
    # acknowledge the receiving
    if Access.dbgDrop_Ack > 0:
        Access.dbgDrop_Ack -= 1
    else:
        try:
            sock.sendto(b'ACK', ackHostPort)
            ReceiverStatistics['acks'] += 1
        except OSError as e:
            _printw(f'OSError: {e}')
        # _printv(f'ACK sent to {hostPort}')
        #self.sock.sendto(b'ACK', self.hostPort)
        #_printv('ACK2 sent to '+str(self.hostPort))
    return data, addr

def _decode_data(data, addr):
    """Receive and decode message from associated socket"""
    #if receive_dictio_lock.locked():
    #    _printv('receive_dictio locked')
    #with receive_dictio_lock:

    _printv('received %i bytes'%(len(data)))
    #_printv('received %i of '%len(data)+str(type(data))+' from '+str(addr)':')
    # decode received data
    # allow exception here, it will be caught in execute_cmd
    if len(data) == 0:
        _printw(f'empty reply for: {LastDictio}')
        return {}
    try:
        decoded = encoderLoad(data)
    except Exception as e:
        _printw(f'exception in encoder.load Data[{len(data)}]: {e}')
        #print(str(data)[:150])
        #raise ValueError('in _receive_dictio: '+msg)
        return {}
    #for key,val in decoded.items():
    #    print(f'received from {key}: {val.keys()}')

    if not isinstance(decoded,dict):
        #print('decoded is not dict')
        return decoded
    # JSON does not allow tuples as a keys, therefore the key is a combined string: hos:dev:par
    # Split the key strings to tuple ('host:dev','par).
    parDict = {}
    for (key, value) in decoded.items():
        key = tuple(key.rsplit(':',1))
        if len(key) == 1:
            key = key[0]
        parDict[key] = value
    for parName,item in list(parDict.items()):
        # items could by numpy arrays, the following should decode everything:
        # _printv(f'parName {parName}: {parDict[parName].keys()}')
        # check if it is numpy array
        shapeDtype = parDict[parName].get('numpy')
        if shapeDtype is not None:
            #print(f'par {parName} is numpy {shapeDtype}')
            shape,dtype = shapeDtype
            v = parDict[parName]['value']
            # it is numpy array
            from numpy import frombuffer
            parDict[parName]['value'] =\
                frombuffer(v,dtype).reshape(shape)
            del parDict[parName]['numpy']
        else:
            #print(f'not numpy {parName}')
            pass
    #print(f'\ndecoded: {parDict}')
    #print('<receive_dictio')
    return parDict

class Subscriber():
    def __init__(self, hostPort:tuple, devParDict:dict, callback):
        self.name = f'{hostPort,devParDict}'
        self.hostPort = hostPort
        self.devParDict = devParDict
        self.callback = callback

class SubscriptionSocket():
    event = threading.Event()
    '''handles all subscriptions to single hostPort'''
    def __init__(self, hostPort, sock):
        #_printi(f'>subsSocket {hostPort}')
        self.name = f'{hostPort}'
        self.hostPort = tuple(hostPort)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.callback = None# holds the callback for checking
        dispatchMode = 'Thread'
        if dispatchMode == 'Thread':
            self.selector = None
            self.socket.settimeout(20)
            self.thread = threading.Thread(target=self.receivingThread)
            self.thread.daemon = True
            self.event.clear()
            self.thread.start()

    def receivingThread(self):
        _printi(f'>receiving thread started for {self.hostPort}')
        while not self.event.is_set():
            try:
                #_printv(f'>subscription receive_dict {self.socket}')
                try:
                    da = _receive_socket(self.socket, self.hostPort)
                    dictio = _decode_data(*da)
                    _printv(f'subs received: {dictio}')
                except TimeoutError as e:
                    msg = f'Timeout in subscription thread: {e}'
                    _printw(msg)
                    continue
            except Exception as e:
                msg = f'in subscription thread socket {self.name}: '+str(e)
                _printw(msg)
                #raise
                sys.exit()
            self.dispatch(dictio)
        _printi(f'<receiving thread stopped for {self.hostPort}') 
        
    def subscribe(self, subscriber):
        if self.socket is None:
            print(f'UDP socket created for {self.hostPort}')
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # just checking:
        if subscriber.hostPort != self.hostPort:
            _printe(f'Subscribe logic error in {self.name}')# this should never happen
        #_printv(f'subscribing {subscriber.name}')
        if self.callback is None:
            self.callback = subscriber.callback
        else:
            if self.callback != subscriber.callback:
                _printe(f'Only one callback is supported per hostPort, subscription for {subscriber.name} is discarded')
                return
        self.event.clear()
        _send_cmd('subscribe', subscriber.devParDict, self.socket\
        , self.hostPort)

    def unsubscribe_all(self):
        _printi(f'unsubscribing {self.hostPort}, {self.socket}')
        if self.socket is None:
            return
        _send_cmd('unsubscribe', {'*':'*'}, self.socket, self.hostPort)
        #_printi(f'killing thread of {self.name}')
        self.event.set()
        #self.thread.raise_exception()
        #print(f'shutting down {self.hostPort}')
        try:    self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e: 
            pass 
            #_printw(f'Exception in shutting down: {e}')
        #print(f'closing down {self.hostPort}')
        try:    self.socket.close()
        except Exception as e:
            _printw(f'Exception in closing: {e}')
        self.socket = None

    def dispatch(self, dictio):
        if dictio:
            #_printi(_croppedText(f'>dispatch {dictio}'))
            self.callback(dictio)
        else:
            _printw(f'empty data from {self.hostPort}')
            #if self.selector:
            #    self.selector.unregister(self.socket)
            #self.socket.close()
            return
    
subscriptionSockets = {}

def _add_subscriber(hostPort:tuple, devParDict:dict, sock, callback=testCallback):
    subscriber = Subscriber(hostPort, devParDict, callback)
    # register new socket if not registered yet
    subsSocket = subscriptionSockets.get(hostPort)
    if subsSocket is None:
        print(f'adding new subscriber {hostPort}')
        subsSocket = SubscriptionSocket(hostPort, sock)
        subscriptionSockets[hostPort] =  subsSocket
        #_printv(f'new socket in publishingHouse: {hostPort}')
    subscriptionSockets[hostPort] = subsSocket
    subsSocket.subscribe(subscriber)

def unsubscribe_all():
    global subscriptionSockets
    if len(subscriptionSockets) > 0:
        for hostPort,subsSocket in subscriptionSockets.items():
            subsSocket.unsubscribe_all()
        subscriptionSockets = {}
        _printi('All unsubscribed')

pvSockets = {}
class Channel():
    Perf = False
    """Provides access to host;port.
    If a socket for host;port have been opened before, it will be reused."""
    def __init__(self, hostPort:tuple, devParDict={}, timeout=10):
        _printv(f'>Channel {hostPort,devParDict}')
        self.devParDict = devParDict
        host = hostPort[0]
        if host.lower() in ('','localhost'):
            host = ip_address()
        try:    port = int(hostPort[1])
        except: port = 9700
        self.hostPort = host,port
        self.timeout = timeout
        self.name = f'{self.hostPort}'
        self.recvMax = 1024*1024*4
        _printv('Try to reuse existing socket')
        self.sock = pvSockets.get(self.hostPort)
        if self.sock is None:
            print('There is no sockets for that host, create a new socket')
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(timeout)
            #self.sock.setblocking(False)
            #events = selectors.EVENT_READ | selectors.EVENT_WRITE
            #Sel.register(sock, events, data=message)
            pvSockets[self.hostPort] = self.sock
        _printv(f'<Channel {hostPort,devParDict}: {self.sock}')

    def _transaction(self, cmd, value=None):
        # normal transaction: send command, receive response
        if Channel.Perf:
            ts = _timer()
        _send_cmd(cmd, self.devParDict, self.sock, self.hostPort, value)
        #r = True if cmd == 'set' else _receive_dictio(self.sock, self.hostPort)
        da = _receive_socket(self.sock, self.hostPort)
        r = _decode_data(*da)
        if Channel.Perf: print('transaction time: %.5f'%(_timer()-ts))
        return r
    
class PVs(object): #inheritance from object is needed in python2 for properties to work
    """Class, representing multiple data access objects."""
    Dbg = 0
    subscriptionsCancelled = True
    #Cache = {}

    def __init__(self, *ldoPars):
        # unpack arguments to hosRequest map
        self.channelMap = {}
        if isinstance(ldoPars[0], str):
            _printe('Device,parameter should be a list or tuple')
            return
            sys.exit(1)
        for ldoPar in ldoPars:
            #if ldoPar in PVs.Cache:
            #    _printv(f'ldoPar {ldoPar} is already exist')
            _printv(f'``````````````````Instantiating PVs ldoPar:{ldoPar}')
            ldo = ldoPar[0]
            if len(ldoPar) == 1:
                pars = '*'
            else:
                if isinstance(ldoPar[1],str):
                    ldoPar = list(ldoPar)
                    ldoPar[1] = [ldoPar[1]]
                pars = ldoPar[1:]
            try:    ldo = ldo.split(NSDelimiter)
            except: pass
            ldo = tuple(ldo)
            #if isinstance(pars,str): pars = [[pars]]
            # ldo is in form: (hostName,devName)
            ldoHost = _hostPort(ldo)
            cnsNameDev = NSDelimiter.join(ldo)
            if ldoHost not in self.channelMap:
                self.channelMap[ldoHost] = {cnsNameDev:pars}
                #_printv(f'created self.channelMap[{ldoHost,self.channelMap[ldoHost]}')
            else:
                if False:#try:
                    _printv(f'try to append old cnsNameDev {ldoHost,cnsNameDev} with {pars[0]}')
                    self.channelMap[ldoHost][cnsNameDev][0].append(pars[0])
                else:#except:
                    _printv(f'creating new cnsNameDev {ldoHost,cnsNameDev} with {pars[0]}')
                    self.channelMap[ldoHost][cnsNameDev] = pars
                print(f'updated self.channelMap[{ldoHost}: {self.channelMap[ldoHost]}')
        channelList = list(self.channelMap.items())
        _printv(f',,,,,,,,,,,,,,,,,,,channelList constructed: {channelList}')
        self.channels = [Channel(*i) for i in channelList]
        return

    def info(self):
        for channel in self.channels:
            return channel._transaction('info')

    def get(self):
        for channel in self.channels:
            return channel._transaction('get')

    def _firstValueAndTime(self):
        try:
            firstDict = self.channels[0]._transaction('get')
            if not isinstance(firstDict,dict):
                return firstDict
            firstValsTDict = list(firstDict.values())[0]
        except Exception as e:
            _printw('in _firstValueAndTime: '+str(e))
            return (None,)
        t = firstValsTDict.get('timestamp')
        v = firstValsTDict.get('value')
        return v,t

    #``````````````Property 'value````````````````````````````````````````````
    # It is for frequently needed get/set access to a single parameter
    @property
    def value(self):
        """Request from server first item of the PVs and return its 
        value and timestamp,"""
        return self._firstValueAndTime()

    @value.setter
    def value(self,value):
        """Send command to set the value to the first item of the PVs"""
        return self.set(value)
    #,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

    def read(self):
        """Return only readable parameters"""
        for channel in self.channels:
            return channel._transaction('read')

    def set(self,value):
        """On normal completion returns replies from channels.
        On error - raises RuntimeError."""
        r = {}
        for channel in self.channels[:1]:
            _printv(f'>set {channel.devParDict} {value}')
            reply = channel._transaction('set',value)
            _printv(f'<set: {reply}')
            if isinstance(reply,str):
                raise RuntimeError(reply)
            r.update(reply)
        return r

    #``````````````subscription ``````````````````````````````````````````````
    def subscribe(self, callback=testCallback):
        if len(self.channels) > 1:
            raise NameError('subscription is supported only for single host;port')
        channel = self.channels[0]
        _add_subscriber(channel.hostPort, channel.devParDict, channel.sock, callback)

    def unsubscribe(self):
        _printi(f'>PV.insubscribe: {self.channels[:1]}')
        unsubscribe_all()

#``````````````````Universal Access```````````````````````````````````````````
#PVC_PV, PVC_CB, PVC_Props = 0, 1, 2
PVC_PV, PVC_Thread = 0, 1
    
class Access():
    """Interface to Process Variables, served by liteServer.
    The pvName should be a tuple: (deviceName,parameterName)
    The full form of the device name: hostName;Port:deviceName,
    if Port is default then it can be omitted: hostName:deviceName.
    Returned values are remapped to the form {(hostDev,par):{parprop:{props}...}...}
    that could be time consuming for complex requests.
    """
    _Subscriptions = []
    __version__ = __version__
    dbgDrop_Ack = 0# Debugging. Number of ACK to drop.

    def set_dbg(dbg):
        PVs.Dbg = dbg

    def info(*devParNames):
        return PVs(*devParNames).info()

    def get(*devParNames, **kwargs):# kwargs are for compatibility with older versions
        return PVs(*devParNames).get()

    def set(dev_pars_values):
        dev,pars,values = dev_pars_values
        return PVs((dev,pars)).set(values)

    def subscribe(callback, *devParNames):
        if not callable(callback):
            _printe(('subscribe arguments are wrong,'
            'expected: subscribe(callback,(dev,par))'))
            return
        pvs = PVs(*devParNames)
        pvs.subscribe(callback)

    def unsubscribe():
        """Unsubscribe all parameters"""
        if len(subscriptionSockets) > 0:
            _printi('>Access.unsubscribe()')
            unsubscribe_all()
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
