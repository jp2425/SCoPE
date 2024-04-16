
import clang.cindex
from clang.cindex import TokenKind

""" Code that can be usefull in other cases. Extraced from the clang documentation. """

def find_decl_ref_expr(node):
    for c in node.get_children():
        if c.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
            print ("Member function call via", c.type.spelling, c.displayname)
        else:
            find_decl_ref_expr(c)


def called_from(node):
    for c in node.get_children():
        if c.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
            find_decl_ref_expr(c);

def get_cursor_id(cursor, cursor_list=[]):
 
    if cursor is None:
        return None

    # FIXME: This is really slow. It would be nice if the index API exposed
    # something that let us hash cursors.
    for i, c in enumerate(cursor_list):
        if cursor == c:
            return i
    cursor_list.append(cursor)
    return len(cursor_list) - 1

def get_info(node, depth=0):
   
    children = [get_info(c, depth + 1) for c in node.get_children()]
    return {
        "id": get_cursor_id(node),
        "kind": node.kind,
        "usr": node.get_usr(),
        "spelling": node.spelling,
        "location": node.location,
        "extent.start": node.extent.start,
        "extent.end": node.extent.end,
        "is_definition": node.is_definition(),
        "definition id": get_cursor_id(node.get_definition()),
        "children": children,
    }

#pprint(("diags", [get_diag_info(d) for d in ast.diagnostics]))
#pprint(("nodes", get_info(ast.cursor)))
#walk(ast.cursor)
#print(ast)