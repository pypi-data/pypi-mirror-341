# pylint: disable-msg=W0622
"""cubicweb-intranet application packaging information"""

modname = "intranet"
distname = "cubicweb-intranet"

numversion = (2, 13, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "Logilab"
author_email = "contact@logilab.fr"
description = "an intranet built on the CubicWeb framework"
web = "http://cubicweb.org/project/cubicweb-intranet"
classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
]

__depends__ = {
    "cubicweb[s3]": ">=4.10.0,<5.0.0",
    "cubicweb-api": ">=0.16.1,<0.17.0",
    "cubicweb-blog": ">=3.0.0,<4.0.0",
    "cubicweb-book": ">=1.0.0,<2.0.0",
    "cubicweb-bootstrap": ">=2.0.0,<3.0.0",
    "cubicweb-card": ">=2.0.0,<3.0.0",
    "cubicweb-comment": ">=3.0.0,<4.0.0",
    "cubicweb-editorjs": ">=0.2.0,<0.3.0",
    "cubicweb-event": ">=2.0.0,<3.0.0",
    "cubicweb-file": ">=4.0.0,<5.0.0",
    "cubicweb-folder": ">=3.0.0,<4.0.0",
    "cubicweb-link": ">=2.0.0,<3.0.0",
    "cubicweb-localperms": ">=1.0.0,<2.0.0",
    "cubicweb-oauth2": ">=1.0.0,<2.0.0",
    "cubicweb-preview": ">=3.0.0,<4.0.0",
    "cubicweb-searchui": ">=1.0.0,<2.0.0",
    "cubicweb-sentry": ">=1.0.0,<2.0.0",
    "cubicweb-signedrequest": ">=3.2.2,<4.0.0",
    "cubicweb-tag": ">=3.0.0,<4.0.0",
    "cubicweb-task": ">=2.0.0,<3.0.0",
    "cubicweb-prometheus": ">=0.5.0,<0.6.0",
}
