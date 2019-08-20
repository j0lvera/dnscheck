__version__ = "0.1.0"

import re
import os
import dns.resolver
from bottle import Bottle, request, json_dumps, response
from tld import get_tld

# from tld.exceptions import TldBadUrl

app = Bottle()


print(os.getenv("ENV"))

ids = [
    "NONE",
    "A",
    "NS",
    "MD",
    "MF",
    "CNAME",
    "SOA",
    "MB",
    "MG",
    "MR",
    "NULL",
    "WKS",
    "PTR",
    "HINFO",
    "MINFO",
    "MX",
    "TXT",
    "RP",
    "AFSDB",
    "X25",
    "ISDN",
    "RT",
    "NSAP",
    "NSAP-PTR",
    "SIG",
    "KEY",
    "PX",
    "GPOS",
    "AAAA",
    "LOC",
    "NXT",
    "SRV",
    "NAPTR",
    "KX",
    "CERT",
    "A6",
    "DNAME",
    "OPT",
    "APL",
    "DS",
    "SSHFP",
    "IPSECKEY",
    "RRSIG",
    "NSEC",
    "DNSKEY",
    "DHCID",
    "NSEC3",
    "NSEC3PARAM",
    "TLSA",
    "HIP",
    "CDS",
    "CDNSKEY",
    "CSYNC",
    "SPF",
    "UNSPEC",
    "EUI48",
    "EUI64",
    "TKEY",
    "TSIG",
    "IXFR",
    "AXFR",
    "MAILB",
    "MAILA",
    "ANY",
    "URI",
    "CAA",
    "TA",
    "DLV",
]


@app.post("/")
def index():
    domain = request.forms.get("domain")

    response.set_header("Access-Control-Allow-Orogin", "dnscheck.now.sh")
    response.add_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
    response.content_type = "application/json"

    try:
        domain = validate(domain)
        dns_results = resolve(domain)
    except Exception as e:
        print("err!", e)
        response.status = 400
        return json_dumps({"message": "Invalid domain."})
    return json_dumps({"data": dns_results})


def validate(domain: str):
    """We expect `get_tld` to throw an exception if domain is invalid."""
    schema = r"http(s?)\:\/\/"
    if not re.match(schema, domain):
        tld = get_tld("http://{}".format(domain))
    else:
        tld = get_tld(domain)
    return re.sub(schema, "", domain)


def resolve(domain: str):
    result = []
    for record in ids:
        try:
            answers = dns.resolver.query(domain, record)

            data = [{"record": record, "value": rdata.to_text()} for rdata in answers]
            for item in data:
                result.append(item)
        except Exception as e:
            print(e)
    return result
