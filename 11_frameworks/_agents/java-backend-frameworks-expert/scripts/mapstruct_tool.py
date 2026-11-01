# -*- coding: utf-8 -*-
"""
mapstruct_tool.py - generator and validator of MapStruct 1.6.3 @Mapper interfaces, based ONLY on the annotations,
attributes and rules documented by the "MapStruct 1.6.3 Reference Guide" (MPS, 2024-11-09, 96 pp.).

Does NOT compile Java, does NOT run MapStruct, does NOT access the network. Reads a JSON specification or a .java file as TEXT.
Convention: pages = PDF page of the MPS (no printed numbering).

Usage:
  python -I scripts/mapstruct_tool.py example                       # prints an example JSON specification
  python -I scripts/mapstruct_tool.py generate SPEC.json [--no-validate]
  python -I scripts/mapstruct_tool.py validate FILE.java [--json]
  python -I scripts/mapstruct_tool.py attrs [ANNOTATION]            # documented attributes (with page)

Severities: ERROR = contradicts an explicit MPS rule; WARNING = attribute/value not documented in MPS 1.6.3 (it may exist
in the real MapStruct, but the text does not allow verifying it) or an [inference] heuristic; INFO = documented reminder.
Exit: 0 without ERROR; 1 with ERROR; 2 incorrect usage.
"""
import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Attributes documented in MPS 1.6.3: annotation -> {attribute: PDF page}
# ---------------------------------------------------------------------------
ATTRS = {
    "Mapper": {
        "componentModel": 8, "uses": 40, "injectionStrategy": 32, "unmappedTargetPolicy": 10,
        "unmappedSourcePolicy": 11, "imports": 65, "config": 78, "mappingInheritanceStrategy": 79,
        "nullValueMappingStrategy": 68, "nullValueIterableMappingStrategy": 12, "nullValueMapMappingStrategy": 13,
        "nullValuePropertyMappingStrategy": 69, "nullValueCheckStrategy": 69, "typeConversionPolicy": 32,
        "builder": 11, "disableSubMappingMethodsGeneration": 36, "mappingControl": 36,
        "subclassExhaustiveStrategy": 66,
    },
    "MapperConfig": {  # "same attributes as @Mapper" (MPS p.78)
        "componentModel": 8, "uses": 40, "injectionStrategy": 32, "unmappedTargetPolicy": 10,
        "unmappedSourcePolicy": 11, "imports": 65, "mappingInheritanceStrategy": 79,
        "nullValueMappingStrategy": 68, "nullValueIterableMappingStrategy": 12, "nullValueMapMappingStrategy": 13,
        "nullValuePropertyMappingStrategy": 69, "nullValueCheckStrategy": 69, "typeConversionPolicy": 32,
        "builder": 11, "disableSubMappingMethodsGeneration": 36, "mappingControl": 36,
        "subclassExhaustiveStrategy": 66,
    },
    "Mapping": {
        "target": 14, "source": 14, "expression": 65, "constant": 64, "defaultValue": 64, "defaultExpression": 65,
        "ignore": 77, "dateFormat": 33, "numberFormat": 33, "qualifiedBy": 45, "qualifiedByName": 46,
        "resultType": 67, "conditionQualifiedBy": 73, "conditionQualifiedByName": 73,
        "nullValueCheckStrategy": 69, "nullValuePropertyMappingStrategy": 69, "mappingControl": 36,
    },
    "BeanMapping": {
        "ignoreByDefault": 15, "resultType": 67, "qualifiedBy": 45, "nullValueMappingStrategy": 68,
        "nullValuePropertyMappingStrategy": 69, "nullValueCheckStrategy": 70, "unmappedTargetPolicy": 10,
        "ignoreUnmappedSourceProperties": 11, "builder": 22, "subclassExhaustiveStrategy": 66, "mappingControl": 36,
    },
    "IterableMapping": {
        "dateFormat": 33, "numberFormat": 33, "nullValueMappingStrategy": 12, "elementTargetType": 67,
        "qualifiedBy": 84, "mappingControl": 36,
    },
    "MapMapping": {
        "valueDateFormat": 50, "nullValueMappingStrategy": 13, "keyTargetType": 67, "valueTargetType": 67,
        "mappingControl": 36,
    },
    "ValueMapping": {"source": 53, "target": 53},
    "EnumMapping": {"nameTransformationStrategy": 58, "configuration": 58},
    "SubclassMapping": {"source": 66, "target": 66, "qualifiedBy": 66, "qualifiedByName": 66},
    "InheritConfiguration": {"name": 76},
    "InheritInverseConfiguration": {"name": 77},
    "DecoratedWith": {"value": 79},
}

# Documented enumerated values (per attribute); None = free
VALORES = {
    "componentModel": ({"default", "cdi", "spring", "jsr330", "jakarta", "jakarta-cdi"}, 8),
    "injectionStrategy": ({"FIELD", "CONSTRUCTOR", "SETTER"}, 32),
    "unmappedTargetPolicy": ({"ERROR", "WARN", "IGNORE"}, 10),
    "unmappedSourcePolicy": ({"ERROR", "WARN", "IGNORE"}, 11),
    "mappingInheritanceStrategy": ({"EXPLICIT", "AUTO_INHERIT_FROM_CONFIG", "AUTO_INHERIT_REVERSE_FROM_CONFIG",
                                    "AUTO_INHERIT_ALL_FROM_CONFIG"}, 79),
    "nullValueMappingStrategy": ({"RETURN_NULL", "RETURN_DEFAULT"}, 68),
    "nullValueIterableMappingStrategy": ({"RETURN_NULL", "RETURN_DEFAULT"}, 12),
    "nullValueMapMappingStrategy": ({"RETURN_NULL", "RETURN_DEFAULT"}, 13),
    "nullValuePropertyMappingStrategy": ({"SET_TO_DEFAULT", "IGNORE"}, 69),
    "nullValueCheckStrategy": ({"ON_IMPLICIT_CONVERSION", "ALWAYS"}, 69),
    "subclassExhaustiveStrategy": ({"RUNTIME_EXCEPTION"}, 66),
}
ANNOTATION_COMPONENT = {"cdi", "spring", "jsr330", "jakarta", "jakarta-cdi"}  # "annotation-based" (MPS p.9)
JAVA_LANG = {"String", "Integer", "Long", "Boolean", "Math", "Double", "Float", "Character", "Byte", "Short",
             "Object", "System", "StringBuilder", "Number", "Enum", "Class"}


class Finding:
    def __init__(self, sev, msg, pag=None, origem="from source"):
        self.sev, self.msg, self.pag, self.origem = sev, msg, pag, origem

    def to_dict(self):
        return {"severidade": self.sev, "mensagem": self.msg, "pagina": self.pag, "origem": self.origem}

    def __str__(self):
        if self.pag:
            cite = f" [from source: MPS p.{self.pag}]" if self.origem == "from source" else f" [{self.origem}; MPS p.{self.pag}]"
        else:
            cite = f" [{self.origem}]"
        return f"{self.sev}: {self.msg}{cite}"


# ---------------------------------------------------------------------------
# Mini-parser of Java annotations (text)
# ---------------------------------------------------------------------------

def find_close(s, i):
    """i points to '('; returns the index of the matching ')', respecting strings and nesting."""
    depth = 0
    j = i
    in_str = False
    in_text_block = False
    while j < len(s):
        c = s[j]
        if in_text_block:
            if s.startswith('"""', j):
                in_text_block = False
                j += 3
                continue
        elif in_str:
            if c == "\\":
                j += 2
                continue
            if c == '"':
                in_str = False
        else:
            if s.startswith('"""', j):
                in_text_block = True
                j += 3
                continue
            if c == '"':
                in_str = True
            elif c in "({":
                depth += 1
            elif c in ")}":
                depth -= 1
                if depth == 0:
                    return j
        j += 1
    return -1


def split_top(s, sep=","):
    parts, depth, cur, in_str = [], 0, [], False
    i = 0
    while i < len(s):
        c = s[i]
        if in_str:
            cur.append(c)
            if c == "\\" and i + 1 < len(s):
                cur.append(s[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
                cur.append(c)
            elif c in "({[":
                depth += 1
                cur.append(c)
            elif c in ")}]":
                depth -= 1
                cur.append(c)
            elif c == sep and depth == 0:
                parts.append("".join(cur))
                cur = []
            else:
                cur.append(c)
        i += 1
    if "".join(cur).strip():
        parts.append("".join(cur))
    return [p.strip() for p in parts]


def parse_args(argstr):
    """'a = 1, b = {x, y}' -> {'a': '1', 'b': '{x, y}'}; a single argument without '=' becomes {'value': ...}"""
    out = {}
    for p in split_top(argstr):
        m = re.match(r"^([A-Za-z_]\w*)\s*=\s*(.*)$", p, re.S)
        if m:
            out[m.group(1)] = m.group(2).strip()
        elif p:
            out["value"] = p
    return out


def strip_comments(src):
    src = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), src, flags=re.S)
    return re.sub(r"//[^\n]*", lambda m: " " * len(m.group(0)), src)


def annotations(src):
    """List of (name, args_dict, start_pos, end_pos) for all annotations, with or without parentheses."""
    res = []
    for m in re.finditer(r"@([A-Za-z_][\w.]*)", src):
        name = m.group(1).split(".")[-1]
        j = m.end()
        k = j
        while k < len(src) and src[k] in " \t\r\n":
            k += 1
        if k < len(src) and src[k] == "(":
            e = find_close(src, k)
            if e == -1:
                continue
            res.append((name, parse_args(src[k + 1:e]), m.start(), e + 1))
        else:
            res.append((name, {}, m.start(), j))
    return res


def unquote(v):
    v = v.strip()
    m = re.match(r'^"(.*)"$', v, re.S)
    return m.group(1) if m else None


def enum_const(v):
    """'ReportingPolicy.ERROR' -> 'ERROR'; 'MappingConstants.ComponentModel.CDI' -> 'cdi' (constant)."""
    v = v.strip()
    q = unquote(v)
    if q is not None:
        return q
    return v.split(".")[-1]


# ---------------------------------------------------------------------------
# Validation of a .java file
# ---------------------------------------------------------------------------

def check_annotation(name, args, findings):
    tab = ATTRS.get(name)
    if tab is None:
        return
    for k, v in args.items():
        if k == "value" and name not in ("DecoratedWith",):
            continue
        if k not in tab:
            findings.append(Finding("WARNING", f"@{name}: attribute '{k}' is not documented in MPS 1.6.3 (the text does not allow verifying it)",
                                    None, "inference"))
            continue
        if k in VALORES:
            ok, pag = VALORES[k]
            c = enum_const(v)
            if k == "componentModel":
                cm = v.strip().split(".")[-1]
                if unquote(v) is None and cm.upper() in {x.upper().replace("-", "_") for x in ok}:
                    continue  # constant MappingConstants.ComponentModel.X (MPS p.31)
            if c not in ok and c.upper() not in {x.upper() for x in ok}:
                findings.append(Finding("WARNING", f"@{name}.{k} = {v}: undocumented value (documented: {', '.join(sorted(ok))})", pag, "from source"))


def method_decls(src):
    """Detects method declarations (heuristic): returns (name, params, start, signature_end, return_type)."""
    out = []
    rx = re.compile(r"(?<![\w.])([\w<>\[\],.? ]+?)\s+(\w+)\s*\(")
    for m in rx.finditer(src):
        nome = m.group(2)
        if nome in ("if", "for", "while", "switch", "catch", "return", "new"):
            continue
        i = m.end() - 1
        e = find_close(src, i)
        if e == -1:
            continue
        tail = src[e + 1:e + 120]
        if not re.match(r"\s*(throws\s+[\w.,\s]+)?\s*[;{]", tail):
            continue
        toks = m.group(1).strip().split()
        ret = toks[-1] if toks else ""
        if ret in ("new", "return", "else", "@interface", "class", "interface"):
            continue
        out.append((nome, src[i + 1:e], m.start(), e + 1, ret))
    return out


def validate_java(src):
    f = []
    s = strip_comments(src)
    anns = annotations(s)

    mappers = [a for a in anns if a[0] in ("Mapper", "MapperConfig")]
    if not mappers:
        f.append(Finding("WARNING", "no @Mapper/@MapperConfig annotation found: nothing to validate beyond textual syntax", 14, "from source"))
    for name, args, ini, fim in anns:
        check_annotation(name, args, f)

    # @Mapper rules
    for name, args, ini, fim in mappers:
        cm_raw = args.get("componentModel")
        cm = None
        if cm_raw is not None:
            cm = enum_const(cm_raw).lower().replace("_", "-") if unquote(cm_raw) is None else unquote(cm_raw)
        if "injectionStrategy" in args and name == "Mapper" and (cm is None or cm == "default"):
            f.append(Finding("WARNING", "injectionStrategy is only used in annotation-based models (cdi, spring, jsr330...); without componentModel (or 'default') it has no practical effect",
                             9, "from source"))
        # abstract class + CONSTRUCTOR
        resto = s[fim:fim + 200]
        if "injectionStrategy" in args and enum_const(args["injectionStrategy"]) == "CONSTRUCTOR" and re.match(r"\s*(public\s+)?abstract\s+class", resto):
            f.append(Finding("WARNING", "abstract mapper with constructor injection: the guide says that for abstract classes or decorators, setter injection must be used",
                             32, "from source"))
        if cm in ("default", None) and "uses" in args:
            f.append(Finding("INFO", "in the default model, hand-written mappers in 'uses' need a public no-argument constructor", 40, "from source"))
        if "typeConversionPolicy" in args and False:
            pass

    # Standalone @Mapping rules
    imports_decl = set()
    for name, args, ini, fim in mappers:
        if "imports" in args:
            for t in re.findall(r"([A-Za-z_][\w]*)\.class", args["imports"]):
                imports_decl.add(t)
    for name, args, ini, fim in anns:
        if name != "Mapping":
            continue
        tgt = args.get("target", "?")
        if "constant" in args and "source" in args:
            f.append(Finding("ERROR", f"@Mapping(target={tgt}): constant cannot be combined with source", 64, "from source"))
        if "expression" in args:
            ex = unquote(args["expression"])
            if ex is not None and not re.match(r"^\s*java\(", ex):
                f.append(Finding("ERROR", f"@Mapping(target={tgt}): expression must use the java(...) syntax (only Java is supported)", 65, "from source"))
            if ex is not None:
                for cls in re.findall(r"(?<![\w.\"])(?:new\s+)?([A-Z]\w*)\s*[.(]", ex):
                    if cls not in JAVA_LANG and cls not in imports_decl and cls != "Mapper":
                        f.append(Finding("WARNING", f"@Mapping(target={tgt}): expression uses '{cls}' without a qualified name and without @Mapper(imports = {cls}.class): the guide says the import is not added automatically (error only when compiling the generated code)",
                                         65, "inference"))
        if "defaultExpression" in args:
            ex = unquote(args["defaultExpression"])
            if ex is not None and not re.match(r"^\s*java\(", ex):
                f.append(Finding("ERROR", f"@Mapping(target={tgt}): defaultExpression must use java(...)", 65, "from source"))
        if "constant" in args and "defaultValue" in args:
            f.append(Finding("WARNING", f"@Mapping(target={tgt}): constant and defaultValue together have no documented meaning (constant always applies)", 64, "inference"))

    # Per-method rules
    mo = re.search(r"(?:interface|class)\s+\w+[^{;]*\{", s)
    lo = mo.end() if mo else 0
    for nome, params, ini, fim, ret in method_decls(s):
        if ini < lo:
            continue
        pm = params
        n_target = pm.count("@MappingTarget")
        if n_target > 1:
            f.append(Finding("ERROR", f"method {nome}: more than one @MappingTarget parameter (only one is allowed)", 20, "from source"))
        plist = split_top(pm)
        src_params = []
        for p in plist:
            if re.search(r"@(MappingTarget|Context|TargetType|SourcePropertyName|TargetPropertyName)", p):
                continue
            mname = re.search(r"(\w+)\s*$", p)
            if mname:
                src_params.append(mname.group(1))
        meus = [a for a in anns if a[2] >= lo and a[3] <= ini]
        mps = [a for a in meus if a[0] == "Mapping"]
        if len(src_params) > 1:
            for _, args, _, _ in mps:
                srcv = unquote(args.get("source", "")) if "source" in args else None
                if srcv is not None and "." not in srcv and srcv not in src_params:
                    f.append(Finding("ERROR", f"method {nome}: with several source parameters, source = \"{srcv}\" must name the parameter (e.g. \"{src_params[0]}.{srcv}\")", 19, "from source"))
        vms = [a for a in meus if a[0] == "ValueMapping"]
        any_cnt = 0
        for _, args, _, _ in vms:
            sv = enum_const(args.get("source", "")) if "source" in args else ""
            tv = enum_const(args.get("target", "")) if "target" in args else ""
            if sv in ("ANY_REMAINING", "ANY_UNMAPPED", "<ANY_REMAINING>", "<ANY_UNMAPPED>"):
                any_cnt += 1
            if sv in ("THROW_EXCEPTION", "<THROW_EXCEPTION>"):
                f.append(Finding("ERROR", f"method {nome}: THROW_EXCEPTION can only be used in target, not in source", 55, "from source"))
            if tv in ("ANY_REMAINING", "ANY_UNMAPPED"):
                f.append(Finding("WARNING", f"method {nome}: ANY_REMAINING/ANY_UNMAPPED only apply to source", 54, "from source"))
        if any_cnt > 1:
            f.append(Finding("ERROR", f"method {nome}: ANY_REMAINING and ANY_UNMAPPED can only appear once in the set (and not at the same time)", 54, "from source"))
        if ret == "String" and any(enum_const(a[1].get("source", "")) == "ANY_REMAINING" for a in vms):
            f.append(Finding("ERROR", f"method {nome}: ANY_REMAINING in an enum -> String mapping produces an error (there is no name similarity)", 57, "from source"))
        lo = max(lo, fim)
    has_inv = any(a[0] == "InheritInverseConfiguration" for a in anns)
    if has_inv:
        for name, args, ini, fim in anns:
            if name == "Mapping" and any(k in args for k in ("expression", "defaultExpression", "defaultValue", "constant")):
                f.append(Finding("INFO", "@InheritInverseConfiguration present: expression, defaultExpression, defaultValue and constant of the source method are ignored (silently) in the inverse", 77, "from source"))
                break

    # @Qualifier: CLASS retention
    for i, (name, args, ini, fim) in enumerate(anns):
        if name == "Qualifier":
            janela = s[ini:ini + 400]
            if "@interface" in janela:
                mret = re.search(r"@Retention\(\s*(?:RetentionPolicy\.)?(\w+)\s*\)", s[max(0, ini - 250):ini + 400])
                if not mret:
                    f.append(Finding("WARNING", "qualifier without a visible @Retention: the guide requires @Retention(RetentionPolicy.CLASS)", 45, "from source"))
                elif mret.group(1) != "CLASS":
                    f.append(Finding("ERROR", f"qualifier with {mret.group(1)} retention: the guide requires RetentionPolicy.CLASS", 45, "from source"))
    return f


# ---------------------------------------------------------------------------
# Generation from a specification
# ---------------------------------------------------------------------------

EXEMPLO = {
    "package": "com.example.mapper",
    "imports": ["com.example.Car", "com.example.CarDto", "com.example.Person", "com.example.PersonDto"],
    "mapper": {"name": "CarMapper", "kind": "interface", "componentModel": "spring",
               "uses": [], "injectionStrategy": "CONSTRUCTOR", "unmappedTargetPolicy": "ERROR"},
    "methods": [
        {"name": "carToCarDto", "returns": "CarDto", "params": [{"type": "Car", "name": "car"}],
         "mappings": [{"target": "manufacturer", "source": "make"}, {"target": "seatCount", "source": "numberOfSeats"},
                      {"target": "price", "source": "price", "numberFormat": "$#.00"}]},
        {"name": "carDtoToCar", "returns": "Car", "params": [{"type": "CarDto", "name": "carDto"}],
         "inheritInverse": "carToCarDto", "mappings": [{"target": "numberOfSeats", "ignore": True}]},
        {"name": "updateCarFromDto", "returns": "void",
         "params": [{"type": "CarDto", "name": "carDto"}, {"type": "Car", "name": "car", "mappingTarget": True}],
         "inherit": "carDtoToCar"}
    ]
}


def jstr(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def gen_mapping(m):
    parts = []
    for k in ("target", "source", "expression", "constant", "defaultValue", "defaultExpression", "dateFormat",
              "numberFormat", "qualifiedByName", "resultType", "conditionQualifiedByName"):
        if k in m:
            parts.append(f"{k} = {jstr(m[k])}")
    if m.get("ignore"):
        parts.append("ignore = true")
    for k in ("qualifiedBy", "conditionQualifiedBy"):
        if k in m:
            v = m[k] if isinstance(m[k], list) else [m[k]]
            parts.append(f"{k} = {{ " + ", ".join(x + ".class" for x in v) + " }")
    for k in ("nullValueCheckStrategy", "nullValuePropertyMappingStrategy"):
        if k in m:
            enum = {"nullValueCheckStrategy": "NullValueCheckStrategy",
                    "nullValuePropertyMappingStrategy": "NullValuePropertyMappingStrategy"}[k]
            parts.append(f"{k} = {enum}.{m[k]}")
    return "    @Mapping(" + ", ".join(parts) + ")"


def validate_spec(spec):
    f = []
    mp = spec.get("mapper", {})
    cm = mp.get("componentModel", "default")
    ok, pag = VALORES["componentModel"]
    if cm not in ok:
        f.append(Finding("ERROR", f"componentModel '{cm}' is not documented (valid: {', '.join(sorted(ok))})", pag))
    inj = mp.get("injectionStrategy")
    if inj:
        if inj not in VALORES["injectionStrategy"][0]:
            f.append(Finding("ERROR", f"injectionStrategy '{inj}' is invalid (FIELD, CONSTRUCTOR, SETTER)", 32))
        if cm not in ANNOTATION_COMPONENT:
            f.append(Finding("WARNING", "injectionStrategy only applies to annotation-based models", 9))
        if inj == "CONSTRUCTOR" and mp.get("kind") == "abstract-class":
            f.append(Finding("WARNING", "abstract class: the guide recommends setter injection", 32))
    for k, (vals, pag) in VALORES.items():
        if k in mp and k not in ("componentModel", "injectionStrategy") and mp[k] not in vals:
            f.append(Finding("ERROR", f"{k} '{mp[k]}' is not documented (valid: {', '.join(sorted(vals))})", pag))
    for k in mp:
        if k not in ("name", "kind", "uses", "instanceField") and k not in ATTRS["Mapper"]:
            f.append(Finding("ERROR", f"@Mapper attribute '{k}' is not documented in MPS 1.6.3: it will not be generated", None, "inference"))
    if mp.get("instanceField") and cm != "default":
        f.append(Finding("WARNING", "an INSTANCE field with Mappers.getMapper is the convention WITHOUT dependency injection; with a DI componentModel the guide recommends obtaining the mapper by injection", 30))
    for me in spec.get("methods", []):
        params = me.get("params", [])
        if sum(1 for p in params if p.get("mappingTarget")) > 1:
            f.append(Finding("ERROR", f"method {me.get('name')}: only one @MappingTarget", 20))
        srcs = [p["name"] for p in params if not p.get("mappingTarget") and not p.get("context") and not p.get("targetType")]
        for mm in me.get("mappings", []):
            if "constant" in mm and "source" in mm:
                f.append(Finding("ERROR", f"{me.get('name')}: constant cannot have source ({mm.get('target')})", 64))
            if "expression" in mm and not str(mm["expression"]).lstrip().startswith("java("):
                f.append(Finding("ERROR", f"{me.get('name')}: expression must be java(...) ({mm.get('target')})", 65))
            for k in mm:
                if k not in ATTRS["Mapping"] and k not in ("ignore",):
                    f.append(Finding("ERROR", f"{me.get('name')}: @Mapping attribute '{k}' is not documented", None, "inference"))
            if len(srcs) > 1 and "source" in mm and "." not in mm["source"] and mm["source"] not in srcs:
                f.append(Finding("ERROR", f"{me.get('name')}: with several parameters, source must be 'param.prop' ({mm['source']})", 19))
        if "inherit" in me and "inheritInverse" in me:
            f.append(Finding("WARNING", f"{me.get('name')}: @InheritConfiguration prevails over @InheritInverseConfiguration in a conflict", 77))
        vms = me.get("valueMappings", [])
        anys = [v for v in vms if v.get("source") in ("ANY_REMAINING", "ANY_UNMAPPED")]
        if len(anys) > 1:
            f.append(Finding("ERROR", f"{me.get('name')}: ANY_REMAINING/ANY_UNMAPPED only once and not together", 54))
        if any(v.get("source") == "THROW_EXCEPTION" for v in vms):
            f.append(Finding("ERROR", f"{me.get('name')}: THROW_EXCEPTION only in target", 55))
        if me.get("returns") == "String" and any(v.get("source") == "ANY_REMAINING" for v in vms):
            f.append(Finding("ERROR", f"{me.get('name')}: ANY_REMAINING in an enum -> String mapping produces an error", 57))
    return f


def generate(spec):
    mp = spec["mapper"]
    used = {"Mapper"}
    lines = []
    attrs = []
    cm = mp.get("componentModel")
    if cm:
        attrs.append(f"componentModel = {jstr(cm)}")
    if mp.get("uses"):
        attrs.append("uses = { " + ", ".join(u + ".class" for u in mp["uses"]) + " }" if len(mp["uses"]) > 1 else f"uses = {mp['uses'][0]}.class")
    if mp.get("injectionStrategy"):
        attrs.append(f"injectionStrategy = InjectionStrategy.{mp['injectionStrategy']}")
        used.add("InjectionStrategy")
    for k, enum in (("unmappedTargetPolicy", "ReportingPolicy"), ("unmappedSourcePolicy", "ReportingPolicy"),
                    ("mappingInheritanceStrategy", "MappingInheritanceStrategy"),
                    ("nullValueMappingStrategy", "NullValueMappingStrategy"),
                    ("nullValueIterableMappingStrategy", "NullValueMappingStrategy"),
                    ("nullValueMapMappingStrategy", "NullValueMappingStrategy"),
                    ("nullValuePropertyMappingStrategy", "NullValuePropertyMappingStrategy"),
                    ("nullValueCheckStrategy", "NullValueCheckStrategy"),
                    ("subclassExhaustiveStrategy", "SubclassExhaustiveStrategy")):
        if mp.get(k):
            attrs.append(f"{k} = {enum}.{mp[k]}")
            used.add(enum)
    if mp.get("imports"):
        attrs.append("imports = { " + ", ".join(i.split(".")[-1] + ".class" for i in mp["imports"]) + " }" if len(mp["imports"]) > 1 else f"imports = {mp['imports'][0].split('.')[-1]}.class")
    body = []
    for me in spec.get("methods", []):
        for mm in me.get("mappings", []):
            body.append(gen_mapping(mm))
            used.add("Mapping")
        for vm in me.get("valueMappings", []):
            sv = vm["source"]
            tv = vm["target"]
            def ref(x):
                if x in ("ANY_REMAINING", "ANY_UNMAPPED", "NULL", "THROW_EXCEPTION"):
                    used.add("MappingConstants")
                    return "MappingConstants." + x
                return jstr(x)
            body.append(f"    @ValueMapping(source = {ref(sv)}, target = {ref(tv)})")
            used.add("ValueMapping")
        if me.get("inherit"):
            body.append(f"    @InheritConfiguration(name = {jstr(me['inherit'])})")
            used.add("InheritConfiguration")
        if me.get("inheritInverse"):
            body.append(f"    @InheritInverseConfiguration(name = {jstr(me['inheritInverse'])})")
            used.add("InheritInverseConfiguration")
        ps = []
        for p in me.get("params", []):
            pre = "@MappingTarget " if p.get("mappingTarget") else ("@Context " if p.get("context") else ("@TargetType " if p.get("targetType") else ""))
            if p.get("mappingTarget"):
                used.add("MappingTarget")
            if p.get("context"):
                used.add("Context")
            if p.get("targetType"):
                used.add("TargetType")
            ps.append(f"{pre}{p['type']} {p['name']}")
        abstract = "abstract " if mp.get("kind") == "abstract-class" else ""
        pub = "public " if mp.get("kind") == "abstract-class" else ""
        thr = f" throws {', '.join(me['throws'])}" if me.get("throws") else ""
        body.append(f"    {pub}{abstract}{me['returns']} {me['name']}({', '.join(ps)}){thr};")
        body.append("")
    out = ["// Generated by mapstruct_tool.py from a JSON specification; only attributes documented in MPS 1.6.3.",
           "// org.mapstruct.* imports: the guide shows org.mapstruct.Mapper (p.14), Qualifier (p.44), factory.Mappers (p.30);",
           "// the other library types in the same package are [inference]. Nothing was compiled."]
    if spec.get("package"):
        out.append(f"package {spec['package']};")
        out.append("")
    for i in spec.get("imports", []):
        out.append(f"import {i};")
    for u in sorted(used):
        out.append(f"import org.mapstruct.{u};")
    out.append("")
    head = "@Mapper" + (f"({', '.join(attrs)})" if attrs else "")
    out.append(head)
    kw = "public abstract class" if mp.get("kind") == "abstract-class" else "public interface"
    out.append(f"{kw} {mp['name']} {{")
    if mp.get("instanceField"):
        out.append(f"    {mp['name']} INSTANCE = Mappers.getMapper({mp['name']}.class);")
        out.append("")
    out.extend(body)
    if out[-1] == "":
        out.pop()
    out.append("}")
    text = "\n".join(out) + "\n"
    if mp.get("instanceField"):
        text = text.replace("import org.mapstruct.Mapper;", "import org.mapstruct.Mapper;\nimport org.mapstruct.factory.Mappers;")
    return text


def cmd_attrs(name):
    names = [name] if name else sorted(ATTRS)
    for n in names:
        if n not in ATTRS:
            print(f"@{n}: annotation is not in the package table (NOT COVERED or not documented in the MPS).")
            continue
        print(f"@{n}: " + ", ".join(f"{k} (MPS p.{p})" for k, p in sorted(ATTRS[n].items())))


def report(findings, as_json=False):
    if as_json:
        print(json.dumps([x.to_dict() for x in findings], ensure_ascii=False, indent=1))
    else:
        if not findings:
            print("No findings.")
        for x in findings:
            print(x)
    return 1 if any(x.sev == "ERROR" for x in findings) else 0


def main():
    ap = argparse.ArgumentParser(description="@Mapper generator/validator (MapStruct 1.6.3, only what the MPS documents)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("example")
    pg_ = sub.add_parser("generate")
    pg_.add_argument("spec")
    pg_.add_argument("--no-validate", action="store_true")
    pv = sub.add_parser("validate")
    pv.add_argument("file")
    pv.add_argument("--json", action="store_true")
    pa = sub.add_parser("attrs")
    pa.add_argument("name", nargs="?")
    a = ap.parse_args()
    if a.cmd == "example":
        print(json.dumps(EXEMPLO, ensure_ascii=False, indent=2))
        return 0
    if a.cmd == "attrs":
        cmd_attrs(a.name)
        return 0
    if a.cmd == "generate":
        try:
            spec = json.load(open(a.spec, "r", encoding="utf-8"))
        except (OSError, ValueError) as e:
            print("Unreadable specification:", e, file=sys.stderr)
            return 2
        fs = [] if a.no_validate else validate_spec(spec)
        if any(x.sev == "ERROR" for x in fs):
            report(fs)
            print("Generation aborted: fix the ERRORS in the specification.", file=sys.stderr)
            return 1
        text = generate(spec)
        print(text, end="")
        post = [] if a.no_validate else validate_java(text)
        extra = [x for x in fs + post if x.sev != "INFO" or True]
        if extra:
            print("\n// --- validation findings (MPS) ---", file=sys.stderr)
            for x in extra:
                print("// " + str(x), file=sys.stderr)
        return 1 if any(x.sev == "ERROR" for x in post) else 0
    if a.cmd == "validate":
        try:
            src = open(a.file, "r", encoding="utf-8", errors="replace").read()
        except OSError as e:
            print("Unreadable file:", e, file=sys.stderr)
            return 2
        return report(validate_java(src), a.json)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
