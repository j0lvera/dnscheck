__version__ = "0.1.0"

import re
import dns.resolver
from bottle import Bottle, template, request, redirect
from tld import get_tld

# from tld.exceptions import TldBadUrl

app = Bottle()


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


@app.route("/", method=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            domain = validate(request.forms.get("domain"))
        except Exception as e:
            return template("form.html", error="Invalid domain.")
        # Form submission successful
        return redirect("/{0}".format(domain))
    # GET request
    return template("form.html", error=None)


@app.get("/<domain>")
def domain(domain):
    try:
        result = resolve(domain)
    except Exception as e:
        print(e)
    return template("results.html", result=result)


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


@app.error(404)
def err404():
    return template("error.html", error="Nothing here. Sorry.")


@app.error(500)
def err500():
    return template("error.html", error="Something went wrong. Contact Juan.")
