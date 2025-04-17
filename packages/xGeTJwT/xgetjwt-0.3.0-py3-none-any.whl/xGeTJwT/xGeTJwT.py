import requests , json , concurrent.futures
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    result = cipher.encrypt(pad(plain_text, AES.block_size))
    return result.hex()

def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = Fix_PackEt(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None
        
def get_token(Uid , Pw):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {"Host": "100067.connect.garena.com", "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)", "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip, deflate, br", "Connection": "close"}
    data = {"uid": Uid, "password": Pw, "response_type": "token", "client_type": "2", "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3", "client_id": "100067"}
    response = requests.Session().post(url, headers=headers, data=data)
    a , o = response.json()["access_token"] , response.json()["open_id"]
    return GeneRaTe_ToKen(a , o)

def GeneRaTe_ToKen(a , o):
    uu = "https://loginbp.common.ggbluefox.com/MajorLogin"
    hh = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB48',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.common.ggbluefox.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
    data = bytes.fromhex('1a13323032352d30322d32362031343a30333a3237220966726565206669726528013a07312e3130392e334239416e64726f6964204f532039202f204150492d32382028504b51312e3138303930342e3030312f5631312e302e332e302e5045494d49584d294a0848616e6468656c64520d4d61726f632054656c65636f6d5a1243617272696572446174614e6574776f726b60dc0b68ee0572033333327a1d41524d3634204650204153494d4420414553207c2031383034207c203880019d1d8a010f416472656e6f2028544d29203530399201404f70656e474c20455320332e322056403333312e30202847495440636635376339632c204931636235633464316363292028446174653a30392f32332f3138299a012b476f6f676c657c34303663613862352d343633302d343062622d623535662d373834646264653262656365a2010d3130322e35322e3137362e3837aa0102656eb201206431616539613230633836633463303433666434616134373931313438616135ba010134c2010848616e6468656c64ca01135869616f6d69205265646d69204e6f74652035ea014030363538396138383431623331323064363962333138373737653939366236313838336631653162323463383263616365303439326231653761313631656133f00101ca020d4d61726f632054656c65636f6dd202023447ca03203734323862323533646566633136343031386336303461316562626665626466e003bd9203e803d772f003a017f803468004e7738804bd92039004e7739804bd9203c80401d2043f2f646174612f6170702f636f6d2e6474732e667265656669726574682d51614b46585768325f61717257642d434d58554d33673d3d2f6c69622f61726d3634e00401ea045f35623839326161616264363838653537316636383830353331313861313632627c2f646174612f6170702f636f6d2e6474732e667265656669726574682d51614b46585768325f61717257642d434d58554d33673d3d2f626173652e61706bf00403f804028a050236349a050a32303139313138303734a80503b205094f70656e474c455332b805ff7fc00504ca05094750174f05550b5135d20506416761646972da05023039e0059239ea0507616e64726f6964f2055c4b717348543376464d434e5a7a4f4966476c5a52584e657a3765646b576b5354546d6a446b6a3857313556676d44526c3257567a477a324f77342f42726259412f5a5a304e302b59416f4651477a5950744e6f51384835335534513df805fbe4068806019006019a060134a2060134')
    data = data.replace('06589a8841b3120d69b318777e996b61883f1e1b24c82cace0492b1e7a161ea3'.encode() , a.encode())
    data = data.replace('d1ae9a20c86c4c043fd4aa4791148aa5'.encode() , o.encode())
    d = encrypt_api(data.hex())
    res = requests.Session().post(uu , headers = hh , data = bytes.fromhex(d) , verify=False)
    if res.status_code == 200 and len(res.text) > 10:
        BesTo_data = json.loads(DeCode_PackEt(res .content.hex()))
        JwT_ToKen = BesTo_data['8']['data']
        return JwT_ToKen
    return False
       
def tt(u , p):
    try:
        if not u or not p:
            return 'Error'
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            token = list(ex.map(lambda x: get_token(*x), [(u, p)]))[0]
        return token
    except Exception as e:
        return e