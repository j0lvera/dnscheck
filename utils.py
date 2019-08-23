import re
import json
import dns.resolver
from dns.exception import Timeout
from bottle import response
from tld import get_tld

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


def resolve_domain(domain: str, dns_server: str):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [dns_server]
    resolver.lifetime = 20
    resolver.timeout = 20

    result = [{"dns_server": dns_server}]

    for record in ids:
        try:
            answers = resolver.query(domain, record)
            data = [{"record": record, "value": rdata.to_text()} for rdata in answers]
            for item in data:
                result.append(item)
        except Timeout as e:
            """As soon as resolver times out we want to raise and stop the rest."""
            print("Timeout inside resolve_domain", e)
            raise Timeout
        except dns.exception.DNSException as e:
            """We let pass these because most of the time is specific records 
            not being present."""
            print("DNSException", e)
            pass
    return result


def validate_domain(domain: str):
    """We expect `get_tld` to throw an exception if domain is invalid."""
    schema = r"http(s?)\:\/\/"
    if not re.match(schema, domain):
        get_tld("http://{}".format(domain))
    else:
        get_tld(domain)
    return re.sub(schema, "", domain)


def jsonify(*args, **kwargs):
    if args and kwargs:
        raise TypeError("jsonify() behavior undefined when passed both args and kwargs")
    elif len(args) == 1:
        data = args[0]
    else:
        data = args or kwargs

    print("data", data)

    if "status" in data:
        response.status = data["status"]
        # Remove element from response
        del data["status"]

    response.content_type = 'application/json"'
    return json.dumps(data)
