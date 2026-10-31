"""Strict synthetic v2 transport reader; QName comparisons ignore prefix spelling."""

import re
from decimal import Decimal

from lxml import etree

NS = "urn:training:return:v2"


class InputIssue(Exception):
    def __init__(self, code, message, path=None, line=None, column=None):
        self.issue = {"code": code, "message": message}
        self.issue.update({k: v for k, v in {"path": path, "line": line, "column": column}.items() if v is not None})


def identity(return_id, year):
    if not isinstance(return_id, str) or not re.fullmatch(r"[A-Z0-9][A-Z0-9-]{0,39}", return_id):
        raise ValueError("Return ID must be 1–40 uppercase ASCII letters, digits or hyphens")
    if isinstance(year, bool) or not re.fullmatch(r"20[0-9]{2}", str(year)):
        raise ValueError("Year must be four ASCII digits in 2000–2099")
    return {"return_id": return_id, "year": int(year)}


def parse_xml(raw):
    try:
        raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InputIssue("MALFORMED_XML", "Input must be UTF-8") from exc
    parser = etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True, recover=False)
    try:
        root = etree.fromstring(raw, parser)
    except etree.XMLSyntaxError as exc:
        raise InputIssue("MALFORMED_XML", "XML syntax is invalid", line=exc.lineno, column=exc.position[1]) from exc
    tree = root.getroottree()
    if tree.docinfo.doctype or root.getprevious() is not None or root.getnext() is not None:
        raise InputIssue("UNSUPPORTED_XML", "DTD, comments and processing instructions are not supported")
    if tree.docinfo.encoding.upper().replace("-", "") != "UTF8":
        raise InputIssue("UNSUPPORTED_XML", "XML encoding must be UTF-8")

    def fail(node, message, code="UNSUPPORTED_XML"):
        raise InputIssue(code, message, path=tree.getpath(node), line=node.sourceline)

    def shape(node, name, child_names):
        if node.tag != f"{{{NS}}}{name}" or node.attrib:
            fail(node, f"Expected namespace-qualified {name} without attributes")
        if any(not isinstance(child.tag, str) for child in node):
            fail(node, "Comments and processing instructions are not supported")
        if [child.tag for child in node] != [f"{{{NS}}}{n}" for n in child_names]:
            fail(node, f"Expected ordered children: {', '.join(child_names)}")
        if name in {"Return", "ReturnHeader", "ReturnData", "Form1040", "Income"} and (
            (node.text or "").strip() or any((c.tail or "").strip() for c in node)
        ):
            fail(node, "Mixed content is not supported")

    def field(node, name, min_len=0, max_len=120):
        shape(node, name, [])
        value = (node.text or "").strip()
        if not min_len <= len(value) <= max_len:
            fail(node, f"{name} length must be {min_len}–{max_len}", "INVALID_FIELD")
        return value

    shape(root, "Return", ["ReturnHeader", "ReturnData"])
    header, data = root
    names = ["ReturnId", "TaxYear", "FilerName"]
    shape(header, "ReturnHeader", names + (["Contact"] if len(header) == 4 else []))
    rid = field(header[0], "ReturnId", 1, 40)
    year = field(header[1], "TaxYear", 4, 4)
    try:
        record = identity(rid, year)
    except ValueError as exc:
        fail(header, str(exc), "INVALID_FIELD")
    record["filer_name"] = field(header[2], "FilerName", 1)
    record["contact"] = field(header[3], "Contact") if len(header) == 4 else None
    shape(data, "ReturnData", ["Form1040"])
    form = data[0]
    if len(form) > 100:
        fail(form, "At most 100 Income entries", "INVALID_FIELD")
    shape(form, "Form1040", ["Income"] * len(form))
    record["income"] = []
    for entry in form:
        shape(entry, "Income", ["Label", "Amount"])
        label = field(entry[0], "Label", 1, 80)
        amount = field(entry[1], "Amount", 1, 262144)
        if not re.fullmatch(r"[0-9]+(?:\.[0-9]{1,2})?", amount) or Decimal(amount) > Decimal("999999999.99"):
            fail(entry[1], "Amount must be unsigned decimal <= 999999999.99 with at most two places", "INVALID_FIELD")
        record["income"].append({"label": label, "amount": format(Decimal(amount), ".2f")})
    return record
