# stdlib
import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4

# third-party
from flask import Flask

# local
from proof.proof import proof_of_work
