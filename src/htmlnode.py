class HTMLNode:
    def __init__(self, tag:str=None, value:str=None, children:list=None, props:dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise  NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""        
        html_str = ""
        for prop in self.props:
            html_str += f' {prop}="{self.props[prop]}"'
        return html_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
'''
class LeafNode(HTMLNode):
    def __init__(self, tag:str=None, value:str=None, props:dict=None):
        
        # NOTE: The value data member should be required
        if not value:     
            raise ValueError("invalid HTML: no value")
        
        # NOTE: should not allow for any children
        super().__init__(tag, value, None, props)     
        

    def to_html(self):
        if not self.tag:
        # if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
'''
# NOTES: As you may note the checks for `self.value is None` made in the to_html method as opposite to the costructor method
#        the reason for this lays in the behaviour of HTMLNode which theoretically can change it's value and/or children during it's lifecycle
#
# Option A (checks are implemented in costructor):
#   Preventing creation of HTMLNode with incorrect values but not enforcing the same behevour afterwards,
#   potentially making it possible to modify the object in a way that will lead to runtime error
#
# Option B (checks are implemented in the rendering methods):
#   Allow for creation with initially incorrect values, but ensuring the correctness during the render

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

# opposite of the LeafNode class
class ParentNode(HTMLNode):
    def __init__(self, tag:str=None, children:list=[], props:dict=None):
        super().__init__(tag, None, children, props)

    # NOTE: The tag and children arguments are required
    def to_html(self):
        if not self.tag:
            raise ValueError("invalid HTML: no value")
        if not self.children:
            raise ValueError("invalid HTML: no children`")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
