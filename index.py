__version__ = "0.1.0"

import os
import dns.resolver
from dns.exception import Timeout
from bottle import Bottle, request, redirect
from cors import CorsPlugin, enable_cors
from tld import exceptions
from utils import jsonify, validate_domain, resolve_domain

app = Bottle()

ORIGINS = os.getenv("ORIGINS").split(",")
ENV = os.getenv("ENV")


@app.get("/")
def redirect_to_app():
    return redirect("https://dnscheck.now.sh")


@enable_cors
@app.post("/")
def index():
    domain = request.forms.get("domain")
    dns_server = request.forms.get("dns_server")

    if domain is None:
        return jsonify(status=400, message="Param domain missing.")

    if dns_server is None:
        return jsonify(status=400, message="Param dns_server missing.")

    try:
        domain = validate_domain(domain)
        dns_results = resolve_domain(domain, dns_server=dns_server)
        return jsonify(status=200, data=dns_results)
    except exceptions.TldDomainNotFound as e:
        print("TldDomainNotFound", e)
        return jsonify(status=400, message=str(e))
    except exceptions.TldBadUrl as e:
        print("TldBadUrl", e)
        return jsonify(status=400, message=str(e))
    except dns.resolver.NXDOMAIN as e:
        print("NXDOMAIN", e)
        return jsonify(status=404, message=e.msg)
    except dns.resolver.NoAnswer as e:
        print("NoAnswer", e)
        return jsonify(status=500, message=e.msg)
    except dns.resolver.NoNameservers as e:
        print("NoNameservers", e)
        return jsonify(status=500, message=e.msg)
    except Timeout as e:
        print("Timeout", e)
        return jsonify(
            status=504,
            message="{} A common reason for this is an invalid DNS server.".format(
                e.msg
            ),
        )


debug = True if ENV == "development" else False
app.install(CorsPlugin(origins=ORIGINS))
