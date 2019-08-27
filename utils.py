import json
import dns.resolver
import dns.name
import dns.query
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


def get_authoritative_nameserver(domain: str):
    """
    Looks up the Authoritative DNS server from a given domain.

    :param str domain: domain name in valid URL format
    :return: List of authoritative DNS server IPs
    :rtype: list
    """

    resolver = dns.resolver.get_default_resolver()
    nameserver = resolver.nameservers[0]

    tld_ = get_tld(domain, fix_protocol=True)

    print("looking up {0} on {1}".format(tld_, nameserver))
    query = dns.message.make_query(tld_, dns.rdatatype.NS)
    query_answer = dns.query.udp(query, nameserver)

    if len(query_answer.authority) > 0:
        rrsets = query_answer.authority
    elif len(query_answer.additional) > 0:
        rrsets = [query_answer.additional]
    else:
        rrsets = query_answer.answer

    result = []

    for rrset in rrsets:
        for rr in rrset:
            if rr.rdtype == dns.rdatatype.SOA:
                print("Same server is authoritative for {}".format(tld_))
            elif rr.rdtype == dns.rdatatype.A:
                ns = rr.items[0].address
                print("Glue record for {0}: {1}".format(rr.name, ns))
            elif rr.rdtype == dns.rdatatype.NS:
                authority = rr.target
                ns = resolver.query(authority).rrset[0].to_text()
                print(
                    "{0} {1} is authoritative for {2}; ttl {3}".format(
                        authority, ns, tld_, rrset.ttl
                    )
                )
                result.append(ns)
            else:
                print("Ignoring {}".format(rr))

    print("result", result)
    return result


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
            # print("Timeout inside resolve_domain", e)
            raise Timeout
        except dns.exception.DNSException as e:
            """We let pass these because most of the time is specific records 
            not being present."""
            # print("DNSException", e)
            pass
    return result


def validate_domain(domain: str):
    """We expect `get_tld` to throw an exception if domain is invalid."""
    res = get_tld(domain, fix_protocol=True, as_object=True)
    return res.fld


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

    response.content_type = "application/json"
    return json.dumps(data)
