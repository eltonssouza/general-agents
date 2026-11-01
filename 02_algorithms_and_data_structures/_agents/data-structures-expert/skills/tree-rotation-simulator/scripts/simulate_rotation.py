# -*- coding: utf-8 -*-
"""
simulate_rotation.py - deterministic simulator of BST rotations, following the rotate_left/rotate_right code
of "Open Data Structures" (Pat Morin, Edition 0.1Gbeta, ODS p.165-166). Pages = PDF (printed = N - 12).

Checks what the book states (ODS p.165-166): the rotation preserves the BST property (same in-order sequence) and the
depth of w decreases by 1 while that of u increases by 1. It also checks the parent/child pointers and the root.
The number of changed pointers is NOT given by the book; the simulator counts the fields that changed (an
experimental result, [extrapolation]). No network; read-only.
Usage: python -I simulate_rotation.py --dir left --node 20
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


class Node:
    def __init__(self, key):
        self.x = key
        self.left = None
        self.right = None
        self.parent = None


class Tree:
    def __init__(self):
        self.r = None

    def rotate_left(self, u):
        w = u.right
        if w is None:
            raise ValueError("node %s has no right child" % u.x)
        w.parent = u.parent
        if w.parent is not None:
            if w.parent.left is u:
                w.parent.left = w
            else:
                w.parent.right = w
        u.right = w.left
        if u.right is not None:
            u.right.parent = u
        u.parent = w
        w.left = u
        if u is self.r:
            self.r = w
            self.r.parent = None
        return w

    def rotate_right(self, u):
        w = u.left
        if w is None:
            raise ValueError("node %s has no left child" % u.x)
        w.parent = u.parent
        if w.parent is not None:
            if w.parent.left is u:
                w.parent.left = w
            else:
                w.parent.right = w
        u.left = w.right
        if u.left is not None:
            u.left.parent = u
        u.parent = w
        w.right = u
        if u is self.r:
            self.r = w
            self.r.parent = None
        return w


def in_order(u, out):
    if u is not None:
        in_order(u.left, out)
        out.append(u.x)
        in_order(u.right, out)


def depth(u):
    d = 0
    while u.parent is not None:
        u = u.parent
        d += 1
    return d


def links_ok(u):
    if u is None:
        return True
    for c in (u.left, u.right):
        if c is not None and c.parent is not u:
            return False
    return links_ok(u.left) and links_ok(u.right)


def snapshot(nodes):
    return {k: (id(n.left), id(n.right), id(n.parent)) for k, n in nodes.items()}


def build_sample():
    t = Tree()
    nodes = {k: Node(k) for k in (10, 20, 25, 30, 40)}
    t.r = nodes[20]
    nodes[20].left, nodes[10].parent = nodes[10], nodes[20]
    nodes[20].right, nodes[30].parent = nodes[30], nodes[20]
    nodes[30].left, nodes[25].parent = nodes[25], nodes[30]
    nodes[30].right, nodes[40].parent = nodes[40], nodes[30]
    return t, nodes


def draw(u, prefix="", is_left=True):
    if u is not None:
        draw(u.right, prefix + ("|   " if is_left else "    "), False)
        print(prefix + ("`-- " if is_left else ",-- ") + str(u.x))
        draw(u.left, prefix + ("    " if is_left else "|   "), True)


def main(argv=None):
    ap = argparse.ArgumentParser(description="BST rotation simulator (Open Data Structures, Morin)")
    ap.add_argument("--dir", choices=["left", "right"], default="left")
    ap.add_argument("--node", type=int, default=20, help="node to rotate: 10, 20, 25, 30 or 40")
    a = ap.parse_args(argv)
    t, nodes = build_sample()
    if a.node not in nodes:
        print("Node %d does not exist. Nodes: %s" % (a.node, sorted(nodes)))
        return 1
    u = nodes[a.node]
    before = []
    in_order(t.r, before)
    snap0 = snapshot(nodes)
    child = u.right if a.dir == "left" else u.left
    d_u0, d_w0 = depth(u), (depth(child) if child is not None else None)
    print("=== BEFORE (pages = PDF; printed = N - 12) ===")
    draw(t.r)
    print("In-order: %s" % before)
    try:
        w = t.rotate_left(u) if a.dir == "left" else t.rotate_right(u)
    except ValueError as e:
        print("Error: %s" % e)
        return 1
    after = []
    in_order(t.r, after)
    print("\n=== AFTER: rotate_%s at node %d ===" % (a.dir, a.node))
    draw(t.r)
    print("In-order: %s" % after)
    snap1 = snapshot(nodes)
    changed = sum(1 for k in nodes for j in range(3) if snap0[k][j] != snap1[k][j])
    print("\n=== CHECKS ===")
    print("In-order sequence preserved:          %s [from source] (ODS p.165-166)" % (before == after))
    print("Parent/child pointers consistent:    %s" % links_ok(t.r))
    print("Root has no parent:                  %s" % (t.r.parent is None))
    print("Depth of w (promoted):               %d -> %d; of u (demoted): %d -> %d [from source] (ODS p.166)"
          % (d_w0, depth(w), d_u0, depth(u)))
    ok_depth = depth(w) == d_w0 - 1 and depth(u) == d_u0 + 1
    print("w moves up 1 and u moves down 1:     %s" % ok_depth)
    print("left/right/parent fields changed:    %d (experimental count in this example) [extrapolation]" % changed)
    return 0 if (before == after and links_ok(t.r) and ok_depth) else 1


if __name__ == "__main__":
    sys.exit(main())
