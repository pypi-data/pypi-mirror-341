#
# Copyright 2025 Bernhard Walter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import traceback
from dataclasses import dataclass, field
from typing import Any, Dict, List

import cadquery as cq
from IPython import get_ipython
from IPython.display import display
from ipywidgets import HBox, Layout, Output, SelectMultiple
from ocp_tessellate.convert import to_ocpgroup, OcpGroup, OcpObject, OcpInstancesGroup
from ocp_tessellate.ocp_utils import make_compound, BoundingBox

from ocp_vscode.show import show, show_object, _tessellate
from cad_viewer_widget import open_viewer

#
# The Runtime part
# It hooks into __getattribute__ and intercept EVERY python call
# One should only enable replay when necessary for debugging
#


def attributes(names):
    def wrapper(cls):
        for name in names:

            def fget(self, name=name):
                if self.is_empty():
                    raise ValueError("Context empty")
                return self.stack[-1][name]

            def fset(self, value, name=name):
                if self.is_empty():
                    raise ValueError("Context empty")
                self.stack[-1][name] = value

            setattr(cls, name, property(fget, fset))
        return cls

    return wrapper


# pylint: disable=protected-access
@attributes(("func", "args", "kwargs", "obj", "shadow_obj", "children"))
class Context(object):
    def __init__(self):
        self.stack = []
        self.new()
        self.func = None
        self.args = None
        self.kwargs = None
        self.obj = None
        self.shadow_obj = None
        self.children = []

    def _to_dict(self, func, args, kwargs, obj, children, shadow_obj=None):
        return {
            "func": func,
            "args": args,
            "kwargs": kwargs,
            "obj": obj,
            "shadow_obj": shadow_obj,
            "children": children,
        }

    @property
    def length(self):
        return len(self.stack)

    def new(self):
        self.push(None, None, None, None, [], None)

    def clear(self):
        self.stack = []

    def is_empty(self):
        return self.stack == []

    def is_top_level(self):
        return len(self.stack) == 1

    def pop(self):
        if not self.is_empty():
            result = self.stack[-1]
            self.stack = self.stack[:-1]
            return result
        else:
            raise ValueError("Empty context")

    def push(self, func, args, kwargs, obj, children, shadow_obj=None):
        self.stack.append(self._to_dict(func, args, kwargs, obj, children, shadow_obj))

    def append(self, func, args, kwargs, obj, children, shadow_obj=None):
        self.stack[-1].append(
            self._to_dict(func, args, kwargs, obj, children, shadow_obj)
        )

    def update(self, func, args, kwargs, obj=None, children=None, shadow_obj=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        if obj is not None:
            self.obj = obj
        if shadow_obj is not None:
            self.shadow_obj = shadow_obj
        if children is not None:
            self.children = children

    def append_child(self, context):
        self.stack[-1]["children"].append(context)

    def __repr__(self):
        def join(a, b):
            if a == "":
                return b
            elif b == "":
                return a
            else:
                return f"{a}, {b}"

        prefix = "    " * (self.length - 1)
        if self.is_empty():
            result = f"{prefix}   >> Context empty"
        else:
            result = ""
            for i, e in enumerate(self.stack):
                args = "" if e["args"] is None else f'{e["args"]}'[1:-1]
                kwargs = (
                    ""
                    if e["kwargs"] is None
                    else ", ".join([f"{k}={v}" for k, v in e["kwargs"].items()])
                )
                result += f'{prefix} >> {i}: {e["func"]}({join(args, kwargs)}) -> {e["obj"]}, {e["shadow_obj"]}/ {e["children"]}\n'
        return result


_CTX = Context()
DEBUG = False
REPLAY = False
HELPER = {"show_bbox": True, "show_result": False}


def _trace(*objs):
    if DEBUG:
        print(*objs)


def get_context():
    return _CTX


def _add_context(self, name):
    def _blacklist(name):
        return name.startswith("_") or name in (
            "Workplane",
            "val",
            "vals",
            "all",
            "size",
            "add",
            "toOCC",
            "findSolid",
            "findFace",
            "toSvg",
            "exportSvg",
            "largestDimension",
            "Sketch",
            "_edges",
            "_faces",
            "_selection",
            "locs",
        )

    def _is_recursive(func):
        return func in ["union", "cut", "intersect", "placeSketch", "sketch"]

    def _is_recursive_end(func):
        return func in ["union", "cut", "intersect", "placeSketch", "finalize"]

    def intercept(func, prefix):
        def f(*args, **kwargs):
            _trace(prefix, f"Calling {func.__name__}{args + (kwargs,)}")
            _trace(_CTX)

            if _is_recursive_end(func.__name__):
                _ = _CTX.pop()
                _trace(prefix, "--> level down")
                _trace(_CTX)

            if _CTX.args is None:
                _trace(prefix, "Updating")
                _CTX.update(func.__name__, args, kwargs)
                _trace(_CTX)

            result = func(*args, **kwargs)

            if func.__name__ == _CTX.func:
                _CTX.obj = result
                context = _CTX.pop()

                if isinstance(result, cq.Sketch):
                    # Now deep clone the current state of the Sketch object
                    new_obj = cq.Sketch()
                    new_obj._faces = context["obj"]._faces.copy()
                    new_obj._edges = [edge.copy() for edge in context["obj"]._edges]
                    if context["obj"]._selection is None:
                        new_obj._selection = None
                        new_obj.locs = [cq.Location()]
                    else:
                        new_obj._selection = [
                            (sel if isinstance(sel, cq.Location) else sel.copy())
                            for sel in context["obj"]._selection
                        ]
                        new_obj.locs = [loc for loc in context["obj"].locs]
                    context["shadow_obj"] = new_obj

                    # for copy, moved, located, which create a copy of the object, copy the _caller stack
                    if func.__self__ != result:
                        try:
                            result._caller = func.__self__._caller
                        except:  # pylint:disable=bare-except
                            pass

                if _CTX.is_empty():
                    if isinstance(result, cq.Sketch):
                        # to not conflict with overridden __getattribute__ us try...except
                        try:
                            result._caller.append(context)
                        except Exception:  # pylint:disable=bare-except,broad-except
                            result._caller = [context]
                    else:
                        result._caller = context

                    _trace(
                        prefix,
                        f"<== finished {func.__name__}, _caller={result._caller}",
                    )
                else:
                    if context["func"] != "sketch":
                        _CTX.append_child(context)
                        _trace("<== added child", context)
                _CTX.new()

            _trace(prefix, "Leaving", func.__name__)
            _trace(_CTX)
            return result

        return f

    attr = object.__getattribute__(self, name)
    if callable(attr):
        prefix = "    " * (_CTX.length - 1)
        if not _blacklist(attr.__name__):
            _trace(prefix, "==> intercepting", attr.__name__)
            if _is_recursive(attr.__name__):
                _trace(prefix, "--> level up")
                _CTX.new()
            _trace(_CTX)

            return intercept(attr, prefix)
    return attr


#
# The UI part
# It evaluates and optimizes what the runtime part had collected
#


@dataclass
class Step:
    level: int = 0
    func: str = ""
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[Any, str] = field(default_factory=dict)
    var: str = ""
    result_name: str = ""
    result_obj: Any = None
    shadow_obj: Any = None

    def clear_func(self):
        self.func = self.args = self.kwargs = ""


class Replay(object):
    def __init__(
        self,
        deviation,
        angular_tolerance,
        edge_accuracy,
        debug,
        cad_width,
        height,
        sidecar=None,
        show_result=True,
        show_bbox=False,
    ):
        self.debug_output = Output()
        self.deviation = deviation
        self.angular_tolerance = angular_tolerance
        self.edge_accuracy = edge_accuracy
        self.debug = debug
        self.cad_width = cad_width
        self.height = height
        self.sidecar = sidecar
        self.show_result = show_result
        self.show_bbox = show_bbox
        self.reset_camera = "reset"
        self.indexes = []
        self.stack = None
        self.result = None
        self.bbox = None
        self.select_box = None
        self.viewer = open_viewer("Replay")

    def format_steps(self, raw_steps):
        def to_code(step, results):
            def to_name(obj):
                if isinstance(obj, (cq.Workplane, cq.Sketch)):
                    name = results.get(obj, None)
                else:
                    name = str(obj)
                return obj if name is None else name

            if step.func != "":
                if step.func == "newObject":
                    args = ("...",)
                else:
                    args = tuple([to_name(arg) for arg in step.args])
                code = "%s%s%s" % ("| " * step.level, step.func, args)
                code = code[:-2] if len(step.args) == 1 else code[:-1]
                if len(step.args) > 0 and len(step.kwargs) > 0:
                    code += ","
                if step.kwargs != {}:
                    code += ", ".join(
                        ["%s=%s" % (k, v) for k, v in step.kwargs.items()]
                    )
                code += ")"
                if step.result_name != "":
                    code += " => %s" % step.result_name
            elif step.var != "":
                code = "%s%s" % ("| " * step.level, step.var)
            else:
                code = "ERROR"
            return code

        steps = []
        entries = []
        obj_index = 1

        _trace("\nraw_steps")
        for s in raw_steps:
            _trace(s)

        # Build a lookup table of all Sketch and Workplane result objects
        results = {}
        for step in raw_steps:
            results[step.result_obj] = None
            if step.shadow_obj != None:
                results[step.shadow_obj] = None

        # Check all args whether they are Sketch or Workplane objects
        # and provide a variable name
        for step in raw_steps:
            for arg in step.args:
                if isinstance(arg, (cq.Workplane, cq.Sketch)):
                    results[arg] = "_v%d" % obj_index
                    obj_index += 1

        _trace("\nresults")
        for k, v in results.items():
            _trace(k, v)

        for step in raw_steps:
            if results[step.result_obj] is not None:
                step.result_name = results[step.result_obj]
            steps.append(step)

        _trace("\nsteps")
        for s in steps:
            _trace(s)

        last_level = 1000000

        for step in reversed(steps):
            if step.level < last_level:
                last_level = 1000000
                entries.insert(
                    0,
                    (
                        to_code(step, results),
                        step.result_obj if step.shadow_obj is None else step.shadow_obj,
                    ),
                )
                if step.var != "":
                    last_level = step.level

        return entries

    def to_array(self, workplane, level=0, result_name=""):
        def walk(caller, level=0, result_name=""):
            stack = [
                Step(
                    level,
                    func=caller["func"],
                    args=caller["args"],
                    kwargs=caller["kwargs"],
                    result_name=result_name,
                    result_obj=caller["obj"],
                    shadow_obj=caller["shadow_obj"],
                )
            ]
            for child in reversed(caller["children"]):
                stack = walk(child, level + 1) + stack
                for arg in child["args"]:
                    if isinstance(arg, cq.Workplane):
                        result_name = getattr(arg, "name", None)
                        stack = (
                            self.to_array(arg, level=level + 2, result_name=result_name)
                            + stack
                        )
            return stack

        stack = []

        obj = workplane
        while obj is not None:
            caller = getattr(obj, "_caller", None)
            result_name = getattr(obj, "name", "")
            if caller is not None:
                if isinstance(caller, (list, tuple)):
                    stack = [
                        Step(
                            level,
                            func=c["func"],
                            args=c["args"],
                            kwargs=c["kwargs"],
                            result_name=result_name,
                            result_obj=c["obj"],
                            shadow_obj=c["shadow_obj"],
                        )
                        for c in caller
                    ]
                else:
                    stack = walk(caller, level, result_name) + stack
                    for arg in caller["args"]:
                        if isinstance(arg, (cq.Workplane, cq.Sketch)):
                            result_name = getattr(arg, "name", "")
                            stack = (
                                self.to_array(
                                    arg, level=level + 1, result_name=result_name
                                )
                                + stack
                            )

            obj = obj.parent

        _trace("to_array")
        for s in stack:
            _trace(s)

        return stack

    def select_handler(self, change):
        with self.debug_output:
            if change["name"] == "index":
                self.select(change["new"])

    def select(self, indexes):
        self.debug_output.clear_output()
        with self.debug_output:
            self.indexes = indexes
            steps = [(i, self.stack[i][1]) for i in self.indexes]

            try:
                cad_objs = []
                for step in steps:
                    obj = step[1]
                    if (
                        hasattr(step[1], "objects") and len(step[1].objects) == 0
                    ):  # handle workplane()
                        obj = step[1].plane.origin
                    pg, instance = to_ocpgroup(
                        obj, names=["Step %02d" % step[0]], show_parent=False
                    )
                    if len(pg.objects) == 1:
                        pg = pg.objects[0]
                    cad_objs.append(OcpInstancesGroup(instance, pg))

            except Exception as ex:  # pylint:disable=broad-except
                print(ex)
                traceback.print_exc()
        # Add hidden result to start with final size and allow for comparison

        if self.show_result and (
            isinstance(self.stack[-1][1], cq.Sketch)
            or not isinstance(self.stack[-1][1].val().edges(), cq.Vector)
        ):

            result, instance = to_ocpgroup(
                self.stack[-1][1].edges(), names=["Result"], colors=["#808080"]
            )
            cad_objs.insert(0, OcpInstancesGroup(instance, result.objects[0]))
        elif self.show_bbox:
            result, instance = to_ocpgroup(
                self.bbox, names=["Bounding box"], colors=["#808080"]
            )
            cad_objs.insert(0, OcpInstancesGroup(instance, result.objects[0]))

        with self.debug_output:
            try:
                cv = show(
                    *cad_objs,
                    deviation=self.deviation,
                    angular_tolerance=self.angular_tolerance,
                    edge_accuracy=self.edge_accuracy,
                    reset_camera=self.reset_camera,
                    debug=False,
                )

                self.reset_camera = "keep"
            except Exception as ex:  # pylint:disable=broad-except
                print("\nWarning: object cannot be shown")
                if self.debug:
                    print(ex)
                    traceback.print_exc()


def replay(
    cad_obj,
    index=-1,
    deviation=0.1,
    angular_tolerance=0.2,
    edge_accuracy=None,
    debug=False,
    cad_width=800,
    height=600,
    sidecar=None,
    show_result=None,
    show_bbox=None,
):
    if not hasattr(cad_obj, "_caller"):
        print(
            "Replay wasn't enabled when creating the object. Call 'enable_replay()' before object creation. Falling back to 'show()'"
        )
        return show(cad_obj, cad_width=cad_width, height=height)

    while not _CTX.is_top_level:
        _CTX.pop()

    if not REPLAY:
        print(
            "Replay is not enabled. To do so call 'enable_replay()'. Falling back to 'show()'"
        )
        return show(cad_obj, cad_width=cad_width, height=height)
    else:
        print(
            "Use the multi select box below to select one or more steps you want to examine"
        )

    if show_bbox is None and show_result is None:
        show_bbox = HELPER["show_bbox"]
        show_result = HELPER["show_result"]
    if show_bbox and show_result:
        print("Choose either show_bbox or show_result, falling back to bbox only")
        show_result = False

    r = Replay(
        deviation,
        angular_tolerance,
        edge_accuracy,
        debug,
        cad_width,
        height,
        sidecar,
        show_result,
        show_bbox,
    )

    if isinstance(cad_obj, (cq.Workplane, cq.Sketch)):
        workplane = cad_obj
    else:
        print("Cannot replay", cad_obj)
        return None

    r.stack = r.format_steps(
        r.to_array(workplane, result_name=getattr(workplane, "name", None))
    )

    # save overall result

    instances, shapes, _, _, _ = _tessellate(r.stack[-1][1], names=["Result"])
    bbox = BoundingBox(shapes["bb"])
    r.bbox = (
        cq.Workplane()
        .box(bbox.xsize, bbox.ysize, bbox.zsize)
        .translate(bbox.center)
        .edges()
    )

    if index == -1:
        r.indexes = [len(r.stack) - 1]
    else:
        r.indexes = [index]

    r.select_box = SelectMultiple(
        options=["%02d  %s" % (i, code) for i, (code, obj) in enumerate(r.stack)],
        index=r.indexes,
        rows=len(r.stack),
        description="",
        disabled=False,
        layout=Layout(width="600px"),
    )
    r.select_box.add_class("monospace")
    r.select_box.observe(r.select_handler)
    display(HBox([r.select_box, r.debug_output]))

    r.select(r.indexes)
    return r


#
# Control functions to enable, disable and reset replay
#


def reset_replay(event=None):
    _CTX.clear()
    _CTX.new()


def enable_replay(show_bbox=True, show_result=False, warning=True, debug=False):
    global DEBUG, REPLAY, HELPER  # pylint:disable=global-statement

    DEBUG = debug

    print("\nEnabling jupyter_cadquery replay")
    cq.Workplane.__getattribute__ = _add_context
    cq.Sketch.__getattribute__ = _add_context

    if warning:
        ip = get_ipython()
        if not "reset_replay" in [
            f.__name__ for f in ip.events.callbacks["pre_run_cell"]
        ]:
            ip.events.register("pre_run_cell", reset_replay)
    REPLAY = True
    HELPER = {"show_bbox": show_bbox, "show_result": show_result}


def disable_replay():
    global REPLAY  # pylint:disable=global-statement
    print(
        "Removing replay from cadquery.Workplane (will show a final RuntimeWarning if not suppressed)"
    )
    cq.Workplane.__getattribute__ = object.__getattribute__

    ip = get_ipython()
    if "reset_replay" in [f.__name__ for f in ip.events.callbacks["pre_run_cell"]]:
        ip.events.unregister("pre_run_cell", reset_replay)
    REPLAY = False
