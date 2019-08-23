__version__ = "0.1.0"

import os
import re
import dns.resolver
from bottle import Bottle, request, json_dumps, response
from cors import CorsPlugin, enable_cors
from tld import get_tld

app = Bottle()

ORIGINS = os.getenv("ORIGINS").split(",")
ENV = os.getenv("ENV")

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


@enable_cors
@app.post("/")
def index():
    domain = request.forms.get("domain")
    dns_server = request.forms.get("dns_server")

    if dns_server is None:
        response.status = 400
        response.content_type = "application/json"
        return json_dumps({"message": "Param dns_server missing."})

    response.content_type = "application/json"
    try:
        domain = validate(domain)
        dns_results = resolve(domain, dns_server=dns_server)
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


def resolve(domain: str, dns_server: str):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [dns_server]

    print("nameservers", resolver.nameservers)

    result = [{"dns_server": dns_server}]

    for record in ids:
        try:
            answers = resolver.query(domain, record)
            data = [{"record": record, "value": rdata.to_text()} for rdata in answers]
            for item in data:
                result.append(item)
        except Exception as e:
            print("error when trying to resolve", e)
    return result


debug = True if ENV == "development" else False
app.install(CorsPlugin(origins=ORIGINS))
